"""LLM-as-Parser: structured extraction for the A* tool-space solver.

Replaces all regex-based extract_* tools with a single LLM call that
converts problem text into structured JSON. The A* solver then operates
on the structured representation, not raw text.

Architecture:
  Problem text → [LLM: one call] → Structured JSON → [A*: search] → Answer

The LLM is used ONLY for parsing/understanding, never for reasoning.
All mathematical reasoning is done by the deterministic A* tool chain.
"""

from __future__ import annotations

import json
import re
import time
from dataclasses import dataclass
from typing import Optional

from astar_solver import SearchState, ValueType, ToolOperator, ToolRegistry


# =============================================================================
# STRUCTURED PROBLEM REPRESENTATION
# =============================================================================

EXTRACTION_PROMPT = """You are a mathematical problem parser. Convert the problem into a structured JSON object.

Output ONLY valid JSON with these possible fields (include only what's relevant):

{
  "problem_type": "modular_power" | "fibonacci" | "binomial" | "derangement" | "sum_formula" | "triangle" | "circle" | "gcd" | "divisor_count" | "divisor_sum" | "digit_sum" | "expression" | "counting" | "polynomial" | "sequence" | "other",
  "base": <integer>,           // for a^b mod m problems
  "exponent": <integer>,       // for a^b mod m problems
  "modulus": <integer>,         // for mod problems
  "fib_n": <integer>,          // for Fibonacci F(n)
  "binom_n": <integer>,        // for C(n,k)
  "binom_k": <integer>,        // for C(n,k)
  "derangement_n": <integer>,  // for D(n)
  "sum_type": "squares" | "cubes" | "arithmetic" | "geometric",
  "sum_n": <integer>,          // upper limit of sum
  "sum_first": <integer>,      // first term (arithmetic/geometric)
  "sum_diff": <integer>,       // common difference (arithmetic)
  "sum_ratio": <fraction>,     // common ratio (geometric)
  "triangle_sides": [a, b, c], // triangle side lengths
  "geo_query": "area" | "perimeter" | "inradius" | "circumradius",
  "circle_radius": <integer>,
  "gcd_a": <integer>,
  "gcd_b": <integer>,
  "divisor_n": <integer>,      // for divisor count/sum
  "divisor_query": "count" | "sum",
  "digit_value": <integer or expression string>,  // for digit sum
  "digit_query": "digit_sum" | "digital_root",
  "expression": "<math expression>",  // for direct evaluation
  "mod_expr_type": "product_of_powers" | "sum_of_powers",
  "mod_expr_factors": [{"base": N, "exp": N}, ...],
  "count_range": [lo, hi],     // for counting problems
  "count_divisor": <integer>,   // divisible by
  "count_not": true,            // NOT divisible
  "count_or_divisors": [d1, d2], // divisible by d1 OR d2
  "target_answer_mod": <integer>  // if answer should be mod something
}

Problem: """


@dataclass
class ParsedProblem:
    """Structured representation of a math problem."""
    raw: dict
    problem_type: str
    confidence: float = 1.0

    def get(self, key: str, default=None):
        return self.raw.get(key, default)


# =============================================================================
# LLM PARSING BACKENDS
# =============================================================================

def parse_with_claude(problem_text: str, api_key: str = "") -> Optional[ParsedProblem]:
    """Parse problem using Claude API."""
    try:
        import anthropic
        client = anthropic.Anthropic(api_key=api_key) if api_key else anthropic.Anthropic()
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=500,
            messages=[{
                "role": "user",
                "content": EXTRACTION_PROMPT + problem_text,
            }],
        )
        text = response.content[0].text.strip()
        # Extract JSON from response
        json_match = re.search(r'\{.*\}', text, re.DOTALL)
        if json_match:
            data = json.loads(json_match.group())
            return ParsedProblem(
                raw=data,
                problem_type=data.get("problem_type", "other"),
            )
    except Exception as e:
        print(f"Claude parse failed: {e}")
    return None


def parse_with_local_llm(problem_text: str, model_url: str = "http://localhost:8080") -> Optional[ParsedProblem]:
    """Parse problem using a local LLM (llama.cpp server, vLLM, etc.)."""
    try:
        import urllib.request
        import urllib.error

        payload = json.dumps({
            "prompt": EXTRACTION_PROMPT + problem_text,
            "max_tokens": 500,
            "temperature": 0.0,
            "stop": ["\n\n"],
        }).encode()

        req = urllib.request.Request(
            f"{model_url}/v1/completions",
            data=payload,
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read())
            text = result["choices"][0]["text"].strip()
            json_match = re.search(r'\{.*\}', text, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group())
                return ParsedProblem(
                    raw=data,
                    problem_type=data.get("problem_type", "other"),
                )
    except Exception as e:
        print(f"Local LLM parse failed: {e}")
    return None


def parse_with_sympy_latex(problem_text: str) -> Optional[ParsedProblem]:
    """Parse LaTeX expressions using SymPy's parse_latex."""
    try:
        from sympy.parsing.latex import parse_latex
        from sympy import symbols

        # Extract LaTeX math expressions
        math_exprs = re.findall(r'\$(.+?)\$|\\[(](.+?)\\[)]', problem_text)
        parsed = {}
        for groups in math_exprs:
            expr_str = groups[0] or groups[1]
            try:
                expr = parse_latex(expr_str)
                parsed[expr_str] = str(expr)
            except Exception:
                pass

        if parsed:
            return ParsedProblem(
                raw={"latex_parsed": parsed, "problem_type": "other"},
                problem_type="other",
                confidence=0.5,
            )
    except ImportError:
        pass
    return None


def parse_with_regex_fallback(problem_text: str) -> ParsedProblem:
    """Regex-based fallback parser (the current approach, kept as safety net)."""
    data = {"problem_type": "other"}
    text = problem_text
    tl = text.lower()

    # ---- HIGH PRIORITY: check compound patterns BEFORE simple modular_power ----

    # Product of powers mod: A^a * B^b mod M
    m = re.search(r'(\d+)\s*[\^]\s*[{]?(\d+)[}]?\s*(?:\*|·|×|\\cdot)\s*(\d+)\s*[\^]\s*[{]?(\d+)[}]?\s*(?:mod|\\pmod)\s*[{]?(\d+)[}]?', text)
    if m:
        data.update({"problem_type": "expression", "mod_expr_type": "product_of_powers",
                      "mod_expr_factors": [{"base":int(m.group(1)),"exp":int(m.group(2))},
                                            {"base":int(m.group(3)),"exp":int(m.group(4))}],
                      "modulus": int(m.group(5))})
        return ParsedProblem(raw=data, problem_type="expression")

    # Sum of powers mod: A^a + B^b mod M
    m = re.search(r'(\d+)\s*[\^]\s*[{]?(\d+)[}]?\s*\+\s*(\d+)\s*[\^]\s*[{]?(\d+)[}]?\s*(?:mod|\\pmod)\s*[{]?(\d+)[}]?', text)
    if m:
        data.update({"problem_type": "expression", "mod_expr_type": "sum_of_powers",
                      "mod_expr_factors": [{"base":int(m.group(1)),"exp":int(m.group(2))},
                                            {"base":int(m.group(3)),"exp":int(m.group(4))}],
                      "modulus": int(m.group(5))})
        return ParsedProblem(raw=data, problem_type="expression")

    # Sum formulas (before modular_power to avoid "1000^2 mod 10007" match)
    sq = re.search(r'1\s*\^\s*2\s*\+\s*2\s*\^\s*2.*?\+\s*(\d+)\s*\^\s*2', tl)
    if sq:
        n = int(sq.group(1))
        data.update({"problem_type": "sum_formula", "sum_type": "squares", "sum_n": n})
        mod_m = re.search(r'(?:mod|\\pmod)\s*[{]?(\d+)[}]?', text)
        if mod_m: data["modulus"] = int(mod_m.group(1))
        return ParsedProblem(raw=data, problem_type="sum_formula")

    if 'sum of squares' in tl or 'sum of cubes' in tl:
        st = "squares" if "squares" in tl else "cubes"
        nm = re.search(r'(\d+)\^\s*[23]', tl)
        if not nm: nm = re.search(r'(\d+)', tl)
        if nm:
            data.update({"problem_type": "sum_formula", "sum_type": st, "sum_n": int(nm.group(1))})
            mod_m = re.search(r'(?:mod|\\pmod)\s*[{]?(\d+)[}]?', text)
            if mod_m: data["modulus"] = int(mod_m.group(1))
            return ParsedProblem(raw=data, problem_type="sum_formula")

    # Digit sum (before modular_power to avoid "2^{10}" match)
    if 'digit sum' in tl or ('sum of' in tl and 'digit' in tl):
        m2 = re.search(r'(?:digit sum|sum of.*digits).*?(\d+)\s*[\^]\s*[{]?(\d+)[}]?', tl)
        if m2:
            data.update({"problem_type": "digit_sum", "digit_value": int(m2.group(1))**int(m2.group(2)),
                          "digit_query": "digit_sum"})
            return ParsedProblem(raw=data, problem_type="digit_sum")
        m1 = re.search(r'(?:digit sum|sum of.*digits).*?(\d+)', tl)
        if m1:
            data.update({"problem_type": "digit_sum", "digit_value": int(m1.group(1)),
                          "digit_query": "digit_sum"})
            return ParsedProblem(raw=data, problem_type="digit_sum")

    if 'digital root' in tl:
        mr = re.search(r'digital root.*?(\d+)', tl)
        if mr:
            data.update({"problem_type": "digit_sum", "digit_value": int(mr.group(1)),
                          "digit_query": "digital_root"})
            return ParsedProblem(raw=data, problem_type="digit_sum")

    # ---- STANDARD: simple modular power ----

    # Modular power: a^b mod m
    m = re.search(r'(\d+)\s*[\^]\s*[{]?(\d+)[}]?\s*(?:\\pmod|\\bmod|mod)\s*[{]?(\d+)[}]?', text)
    if m:
        data.update({"problem_type": "modular_power", "base": int(m.group(1)),
                      "exponent": int(m.group(2)), "modulus": int(m.group(3))})
        return ParsedProblem(raw=data, problem_type="modular_power")

    # Remainder
    m = re.search(r'remainder.*?(\d+)\s*[\^]\s*[{]?(\d+)[}]?.*?divided.*?(\d+)', tl)
    if m:
        data.update({"problem_type": "modular_power", "base": int(m.group(1)),
                      "exponent": int(m.group(2)), "modulus": int(m.group(3))})
        return ParsedProblem(raw=data, problem_type="modular_power")

    # Last N digits
    m = re.search(r'last\s+(\w+)\s+digits?.*?(\d+)\s*[\^]\s*[{]?(\d+)', tl)
    if m:
        word_map = {"one":1,"two":2,"three":3,"four":4,"five":5}
        nd = word_map.get(m.group(1)) or int(m.group(1))
        data.update({"problem_type": "modular_power", "base": int(m.group(2)),
                      "exponent": int(m.group(3)), "modulus": 10**nd})
        return ParsedProblem(raw=data, problem_type="modular_power")

    # Fibonacci
    m = re.search(r'[fF]\s*[_({\[]?\s*(\d+).*?(?:mod|\\pmod)\s*[{]?(\d+)', text)
    if m and ('fibonacci' in tl or 'f(' in tl):
        data.update({"problem_type": "fibonacci", "fib_n": int(m.group(1)),
                      "modulus": int(m.group(2))})
        return ParsedProblem(raw=data, problem_type="fibonacci")

    # Binomial
    m = re.search(r'(?:[Cc]\s*\(\s*(\d+)\s*,\s*(\d+)\s*\)|\\binom\s*[{](\d+)[}]\s*[{](\d+)[}])', text)
    if m:
        n = int(m.group(1) or m.group(3))
        k = int(m.group(2) or m.group(4))
        mod_m = re.search(r'(?:mod|\\pmod)\s*[{]?(\d+)[}]?', text)
        data.update({"problem_type": "binomial", "binom_n": n, "binom_k": k})
        if mod_m:
            data["modulus"] = int(mod_m.group(1))
        return ParsedProblem(raw=data, problem_type="binomial")

    # Derangement
    if 'derangement' in tl:
        m = re.search(r'(\d+)\s*(?:elements?|objects?)', tl)
        if m:
            data.update({"problem_type": "derangement", "derangement_n": int(m.group(1))})
            last_m = re.search(r'last\s+(\w+)\s+digits?', tl)
            if last_m:
                word_map = {"one":1,"two":2,"three":3,"four":4,"five":5}
                nd = word_map.get(last_m.group(1)) or int(last_m.group(1))
                data["target_answer_mod"] = 10**nd
            return ParsedProblem(raw=data, problem_type="derangement")

    # GCD
    m = re.search(r'gcd\s*\(\s*(\d+)\s*,\s*(\d+)\s*\)', text, re.IGNORECASE)
    if m:
        data.update({"problem_type": "gcd", "gcd_a": int(m.group(1)), "gcd_b": int(m.group(2))})
        return ParsedProblem(raw=data, problem_type="gcd")

    # Divisors
    m = re.search(r'(?:how many|number of|count).*?divisors.*?(\d+)', tl)
    if m:
        data.update({"problem_type": "divisor_count", "divisor_n": int(m.group(1)), "divisor_query": "count"})
        return ParsedProblem(raw=data, problem_type="divisor_count")

    m = re.search(r'sum.*?divisors.*?(\d+)', tl)
    if m:
        data.update({"problem_type": "divisor_sum", "divisor_n": int(m.group(1)), "divisor_query": "sum"})
        return ParsedProblem(raw=data, problem_type="divisor_sum")

    # Digit sum
    if 'digit sum' in tl or 'sum of' in tl and 'digit' in tl:
        m2 = re.search(r'(?:digit sum|sum of.*digits).*?(\d+)\s*[\^]\s*[{]?(\d+)[}]?', tl)
        if m2:
            data.update({"problem_type": "digit_sum", "digit_value": int(m2.group(1))**int(m2.group(2)),
                          "digit_query": "digit_sum"})
            return ParsedProblem(raw=data, problem_type="digit_sum")
        m1 = re.search(r'(?:digit sum|sum of.*digits).*?(\d+)', tl)
        if m1:
            data.update({"problem_type": "digit_sum", "digit_value": int(m1.group(1)),
                          "digit_query": "digit_sum"})
            return ParsedProblem(raw=data, problem_type="digit_sum")

    if 'digital root' in tl:
        m = re.search(r'digital root.*?(\d+)', tl)
        if m:
            data.update({"problem_type": "digit_sum", "digit_value": int(m.group(1)),
                          "digit_query": "digital_root"})
            return ParsedProblem(raw=data, problem_type="digit_sum")

    # Triangle
    m = re.search(r'(?:sides?|lengths?)\s*(?:are\s+|of\s+)?(\d+)\s*,\s*(\d+)\s*(?:,\s*and\s*|\s*,\s*and\s+|,\s*)(\d+)', tl)
    if not m:
        m = re.search(r'(\d+)\s*,\s*(\d+)\s*(?:,\s*)?and\s*(\d+)', tl)
    if m and 'triangle' in tl:
        sides = [int(m.group(1)), int(m.group(2)), int(m.group(3))]
        query = "area"
        if "perimeter" in tl: query = "perimeter"
        elif "inradius" in tl or "incircle" in tl: query = "inradius"
        elif "circumradius" in tl: query = "circumradius"
        data.update({"problem_type": "triangle", "triangle_sides": sides, "geo_query": query})
        return ParsedProblem(raw=data, problem_type="triangle")

    # Sum formulas
    sq = re.search(r'1\s*\^\s*2\s*\+\s*2\s*\^\s*2.*?\+\s*(\d+)\s*\^\s*2', tl)
    if sq:
        n = int(sq.group(1))
        data.update({"problem_type": "sum_formula", "sum_type": "squares", "sum_n": n})
        mod_m = re.search(r'(?:mod|\\pmod)\s*[{]?(\d+)[}]?', text)
        if mod_m: data["modulus"] = int(mod_m.group(1))
        return ParsedProblem(raw=data, problem_type="sum_formula")

    if 'sum of squares' in tl or 'sum of cubes' in tl:
        st = "squares" if "squares" in tl else "cubes"
        m = re.search(r'(\d+)\^\s*[23]', tl)
        if not m: m = re.search(r'(\d+)', tl)
        if m:
            data.update({"problem_type": "sum_formula", "sum_type": st, "sum_n": int(m.group(1))})
            mod_m = re.search(r'(?:mod|\\pmod)\s*[{]?(\d+)[}]?', text)
            if mod_m: data["modulus"] = int(mod_m.group(1))
            return ParsedProblem(raw=data, problem_type="sum_formula")

    # Arithmetic series
    m = re.search(r'sum\s+(\d+)\s*\+\s*(\d+)\s*\+\s*(\d+).*?\+\s*(\d+)', tl)
    if not m:
        m = re.search(r'(\d+)\s*\+\s*(\d+)\s*\+\s*(\d+)\s*\+\s*.*?\+\s*(\d+)', tl)
    if m:
        a1, a2, a3, an = int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4))
        d = a2 - a1
        if d == a3 - a2 and d != 0:
            n = (an - a1) // d + 1
            data.update({"problem_type": "sum_formula", "sum_type": "arithmetic",
                          "sum_n": n, "sum_first": a1, "sum_diff": d})
            return ParsedProblem(raw=data, problem_type="sum_formula")

    # Counting
    if 'how many' in tl and 'integer' in tl:
        m = re.search(r'(?:between|from)\s*(\d+)\s*(?:and|to)\s*(\d+)', tl)
        if m:
            lo, hi = int(m.group(1)), int(m.group(2))
            data.update({"problem_type": "counting", "count_range": [lo, hi]})
            if 'not divisible' in tl:
                dm = re.search(r'not divisible by\s*(\d+)', tl)
                if dm: data.update({"count_divisor": int(dm.group(1)), "count_not": True})
            elif re.search(r'divisible by\s*(\d+)\s*or\s*(\d+)', tl):
                dm = re.search(r'divisible by\s*(\d+)\s*or\s*(\d+)', tl)
                data["count_or_divisors"] = [int(dm.group(1)), int(dm.group(2))]
            elif 'divisible by' in tl:
                dm = re.search(r'divisible by\s*(\d+)', tl)
                if dm: data["count_divisor"] = int(dm.group(1))
            return ParsedProblem(raw=data, problem_type="counting")

    # Generic expression
    m = re.search(r'(?:find|compute|evaluate|calculate)\s+([\d\s\+\-\*/\^\(\)\{\}]+)', text, re.IGNORECASE)
    if m:
        expr = re.sub(r'[{}]', '', m.group(1))
        expr = re.sub(r'\^', '**', expr)
        data.update({"problem_type": "expression", "expression": expr.strip()})
        mod_m = re.search(r'(?:mod|\\pmod)\s*[{]?(\d+)[}]?', text)
        if mod_m: data["modulus"] = int(mod_m.group(1))
        return ParsedProblem(raw=data, problem_type="expression")

    return ParsedProblem(raw=data, problem_type="other", confidence=0.0)


# =============================================================================
# STRUCTURED STATE BUILDER
# =============================================================================

def build_initial_state(parsed: ParsedProblem) -> SearchState:
    """Convert a parsed problem directly into an A* initial state.

    This replaces ALL extract_* tools — the state is pre-populated
    with structured values, so A* starts directly at the computation step.
    """
    state = SearchState()
    p = parsed.raw
    pt = parsed.problem_type

    if pt == "modular_power":
        state.set_value("base", p["base"], ValueType.INTEGER, "llm_parser")
        state.set_value("exponent", p["exponent"], ValueType.INTEGER, "llm_parser")
        state.set_value("modulus", p["modulus"], ValueType.INTEGER, "llm_parser")

    elif pt == "fibonacci":
        state.set_value("fib_n", p["fib_n"], ValueType.INTEGER, "llm_parser")
        state.set_value("fib_modulus", p["modulus"], ValueType.INTEGER, "llm_parser")

    elif pt == "binomial":
        state.set_value("binom_n", p["binom_n"], ValueType.INTEGER, "llm_parser")
        state.set_value("binom_k", p["binom_k"], ValueType.INTEGER, "llm_parser")
        state.set_value("comb_type", "binomial", ValueType.EXPRESSION, "llm_parser")
        if "modulus" in p:
            state.set_value("comb_modulus", p["modulus"], ValueType.INTEGER, "llm_parser")

    elif pt == "derangement":
        state.set_value("derangement_n", p["derangement_n"], ValueType.INTEGER, "llm_parser")
        state.set_value("comb_type", "derangement", ValueType.EXPRESSION, "llm_parser")
        if "target_answer_mod" in p:
            state.set_value("comb_modulus", p["target_answer_mod"], ValueType.INTEGER, "llm_parser")

    elif pt == "sum_formula":
        state.set_value("sum_type", p["sum_type"], ValueType.EXPRESSION, "llm_parser")
        state.set_value("sum_n", p["sum_n"], ValueType.INTEGER, "llm_parser")
        if "sum_first" in p:
            state.set_value("sum_a1", p["sum_first"], ValueType.INTEGER, "llm_parser")
        if "sum_diff" in p:
            state.set_value("sum_d", p["sum_diff"], ValueType.INTEGER, "llm_parser")
        if "modulus" in p:
            state.set_value("sum_modulus", p["modulus"], ValueType.INTEGER, "llm_parser")

    elif pt == "triangle":
        sides = tuple(p["triangle_sides"])
        state.set_value("geo_type", "triangle", ValueType.EXPRESSION, "llm_parser")
        state.set_value("tri_sides", sides, ValueType.SEQUENCE, "llm_parser")
        state.set_value("geo_query", p.get("geo_query", "area"), ValueType.EXPRESSION, "llm_parser")

    elif pt == "gcd":
        state.set_value("gcd_a", p["gcd_a"], ValueType.INTEGER, "llm_parser")
        state.set_value("gcd_b", p["gcd_b"], ValueType.INTEGER, "llm_parser")

    elif pt == "divisor_count":
        from sympy import factorint
        state.set_value("modulus_factors", factorint(p["divisor_n"]), ValueType.EXPRESSION, "llm_parser")

    elif pt == "divisor_sum":
        state.set_value("sod_n", p["divisor_n"], ValueType.INTEGER, "llm_parser")

    elif pt == "digit_sum":
        state.set_value("digit_query", p["digit_query"], ValueType.EXPRESSION, "llm_parser")
        state.set_value("digit_value", p["digit_value"], ValueType.INTEGER, "llm_parser")

    elif pt == "counting":
        constraint = {"lo": p["count_range"][0], "hi": p["count_range"][1]}
        if "count_or_divisors" in p:
            constraint["type"] = "divisible_or_range"
            constraint["d1"] = p["count_or_divisors"][0]
            constraint["d2"] = p["count_or_divisors"][1]
        elif p.get("count_not"):
            constraint["type"] = "not_divisible_range"
            constraint["divisor"] = p["count_divisor"]
        elif "count_divisor" in p:
            constraint["type"] = "divisible_range"
            constraint["divisor"] = p["count_divisor"]
        state.set_value("count_constraint", constraint, ValueType.EXPRESSION, "llm_parser")

    elif pt == "expression":
        if "mod_expr_type" in p:
            state.set_value("mod_expr", {
                "type": p["mod_expr_type"],
                "factors" if "product" in p["mod_expr_type"] else "terms": p["mod_expr_factors"],
            }, ValueType.EXPRESSION, "llm_parser")
            state.set_value("mod_expr_modulus", p["modulus"], ValueType.INTEGER, "llm_parser")
        elif "expression" in p:
            state.set_value("expression", p["expression"], ValueType.EXPRESSION, "llm_parser")
            if "modulus" in p:
                state.set_value("expr_modulus", p["modulus"], ValueType.INTEGER, "llm_parser")

    # Always keep problem text for fallback
    state.set_value("problem_text", "", ValueType.EXPRESSION, "llm_parser")

    return state


# =============================================================================
# UNIFIED SOLVER: parse → search
# =============================================================================

def solve_parsed(
    problem_text: str,
    use_llm: bool = False,
    api_key: str = "",
    verbose: bool = False,
) -> dict:
    """Parse problem with best available method, then A* search.

    Args:
        problem_text: Math problem in LaTeX or plain text
        use_llm: If True, try Claude API first
        api_key: Anthropic API key (optional, uses env var if empty)
        verbose: Print debug info

    Returns:
        dict with answer, path, metrics, parser_used, elapsed
    """
    import astar_solver
    from astar_extended import extend_registry, extended_heuristic
    from astar_v2 import _register_deep_nt_tools, v2_heuristic
    from astar_v3 import _register_multistep_tools, v3_heuristic

    t0 = time.time()

    # Step 1: Parse
    parsed = None
    parser_used = "none"

    if use_llm:
        parsed = parse_with_claude(problem_text, api_key)
        if parsed:
            parser_used = "claude"

    if not parsed:
        parsed = parse_with_regex_fallback(problem_text)
        parser_used = "regex"

    if verbose:
        print(f"Parser: {parser_used}")
        print(f"Parsed: {json.dumps(parsed.raw, indent=2)}")

    # Step 2: Build initial state from parsed problem
    initial_state = build_initial_state(parsed)

    # Step 3: A* search (skip extraction tools — state is pre-populated)
    original_heuristic = astar_solver.heuristic
    astar_solver.heuristic = v3_heuristic

    original_init = ToolRegistry._register_all_tools
    def patched_init(self):
        original_init(self)
        extend_registry(self)
        _register_deep_nt_tools(self)
        _register_multistep_tools(self)
    ToolRegistry._register_all_tools = patched_init

    try:
        import heapq
        registry = ToolRegistry()

        # Start from the pre-populated state (not raw text)
        h0 = v3_heuristic(initial_state)
        open_set = [(initial_state.g_cost + h0, 0, initial_state)]
        visited = set()
        counter = 0
        states_explored = 0
        best_state = None

        while open_set and states_explored < 2000:
            f_cost, _, current = heapq.heappop(open_set)
            state_key = current.state_key()
            if state_key in visited:
                continue
            visited.add(state_key)
            states_explored += 1

            if verbose and states_explored <= 5:
                applicable = [t.name for t in registry.applicable_tools(current)]
                print(f"  State {states_explored}: {applicable}")

            # Goal test
            if current.candidate_answer is not None and current.answer_confidence >= 0.95:
                elapsed = time.time() - t0
                path = []
                s = current
                while s:
                    if s.producing_tool: path.append(s.producing_tool)
                    s = s.parent
                path.reverse()

                return {
                    "answer": current.candidate_answer,
                    "path": path,
                    "states_explored": states_explored,
                    "parser_used": parser_used,
                    "parsed_type": parsed.problem_type,
                    "elapsed": elapsed,
                }

            if best_state is None or (
                current.candidate_answer is not None
                and (best_state.candidate_answer is None
                     or current.answer_confidence > best_state.answer_confidence)
            ):
                best_state = current

            for tool in registry.applicable_tools(current):
                if tool.name in current.applied_tools:
                    continue
                try:
                    for new_state in tool.apply(current):
                        nk = new_state.state_key()
                        if nk not in visited:
                            h = v3_heuristic(new_state)
                            counter += 1
                            heapq.heappush(open_set, (new_state.g_cost + h, counter, new_state))
                except Exception:
                    continue

    finally:
        astar_solver.heuristic = original_heuristic
        ToolRegistry._register_all_tools = original_init

    elapsed = time.time() - t0

    if best_state and best_state.candidate_answer is not None:
        return {
            "answer": best_state.candidate_answer,
            "path": [],
            "states_explored": states_explored,
            "parser_used": parser_used,
            "parsed_type": parsed.problem_type,
            "elapsed": elapsed,
        }

    return {
        "answer": None,
        "path": [],
        "states_explored": states_explored,
        "parser_used": parser_used,
        "parsed_type": parsed.problem_type,
        "elapsed": elapsed,
    }


# =============================================================================
# TEST SUITE
# =============================================================================

if __name__ == "__main__":
    import math

    def fib_mod_fast(n, m):
        if n <= 1: return n % m
        def mm(A,B,mod):
            return [[(A[0][0]*B[0][0]+A[0][1]*B[1][0])%mod,(A[0][0]*B[0][1]+A[0][1]*B[1][1])%mod],
                    [(A[1][0]*B[0][0]+A[1][1]*B[1][0])%mod,(A[1][0]*B[0][1]+A[1][1]*B[1][1])%mod]]
        def mp(M,p,mod):
            r=[[1,0],[0,1]]; b=M
            while p:
                if p%2: r=mm(r,b,mod)
                b=mm(b,b,mod); p//=2
            return r
        return mp([[1,1],[1,0]],n,m)[0][1]

    from astar_extended import _lucas_binomial

    def derangement(n):
        if n<=1: return [1,0][n]
        a,b=1,0
        for i in range(2,n+1): a,b=b,(i-1)*(a+b)
        return b

    d6=1000//6; d10=1000//10; lcm610=(6*10)//math.gcd(6,10); d_both=1000//lcm610

    problems = [
        ("NT1", "Find 2^{2024} mod 7.", pow(2,2024,7)),
        ("NT2", "Find 3^{999} mod 13.", pow(3,999,13)),
        ("NT3", "Find the last three digits of 7^{999}.", pow(7,999,1000)),
        ("NT4", "What is the remainder when 17^{2023} is divided by 100?", pow(17,2023,100)),
        ("SEQ1", "Find F(1000000) mod 10007, where F(n) is the nth Fibonacci number.", fib_mod_fast(1000000,10007)),
        ("COMB1", "Compute \\binom{100}{3}.", 161700),
        ("COMB2", "Compute \\binom{1000}{2} \\pmod{997}.", (1000*999//2)%997),
        ("COMB3", "Find the number of derangements of 5 elements (permutations with no fixed points).", 44),
        ("COMB4", "Find the number of derangements of 8 elements. Give the last three digits.", derangement(8)%1000),
        ("ALG1", "Find the sum of squares 1^2 + 2^2 + ... + 100^2.", 338350),
        ("ALG2", "Find the sum 3 + 7 + 11 + ... + 399.", 20100),
        ("ALG3", "Find the sum of squares 1^2 + 2^2 + ... + 1000^2 mod 10007.", 333833500%10007),
        ("GEO1", "A triangle has sides 3, 4, and 5. Find its area.", 6),
        ("GEO2", "A triangle has sides 7, 24, and 25. Find its perimeter.", 56),
        ("DNT1", "Find gcd(12345678, 87654321).", math.gcd(12345678,87654321)),
        ("DNT2", "How many positive divisors does 360 have?", 24),
        ("DNT3", "Find the sum of all positive divisors of 360.", 1170),
        ("MS1", "Find 2^{100} * 3^{50} mod 97.", (pow(2,100,97)*pow(3,50,97))%97),
        ("MS2", "Find 7^{256} + 11^{128} mod 1000.", (pow(7,256,1000)+pow(11,128,1000))%1000),
        ("MS3", "How many integers between 1 and 1000 are divisible by 7?", 1000//7),
        ("MS4", "How many integers between 1 and 10000 are not divisible by 3?", 10000-10000//3),
        ("MS5", "How many integers between 1 and 1000 are divisible by 6 or 10?", d6+d10-d_both),
        ("MS6", "Find the digit sum of 99999.", 45),
        ("MS7", "Find the digital root of 123456789.", 1+((123456789-1)%9)),
        ("MS8", "Find the digit sum of 2^{10}.", sum(int(d) for d in str(2**10))),
        ("MS9", "Compute 2^{10} + 3^{5} - 4^{3}.", 2**10+3**5-4**3),
    ]

    print("=" * 70)
    print("LLM-AS-PARSER + A* SOLVER (regex fallback mode)")
    print("=" * 70)

    total = correct = 0
    total_time = 0.0

    for name, problem, expected in problems:
        total += 1
        result = solve_parsed(problem, use_llm=False, verbose=False)
        ok = result["answer"] == expected
        correct += ok
        total_time += result["elapsed"]

        status = "PASS" if ok else "FAIL"
        if ok:
            path = " -> ".join(result["path"]) if result["path"] else "direct"
            print(f"  [PASS] {name:6s} = {result['answer']}  "
                  f"[{result['parsed_type']}] ({result['states_explored']} states, {result['elapsed']:.3f}s)")
        else:
            print(f"  [FAIL] {name:6s}  Expected: {expected}, Got: {result['answer']}  "
                  f"[{result['parsed_type']}]")

    print(f"\nRESULTS: {correct}/{total} ({100*correct/total:.0f}%)")
    print(f"Total time: {total_time:.3f}s, Avg: {total_time/total:.3f}s")
    print("=" * 70)
