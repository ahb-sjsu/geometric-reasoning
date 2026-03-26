import sys
sys.path.insert(0, "src")
sys.path.insert(0, "../structural-fuzzing/src")
from astar_v3 import hybrid_solve
r = hybrid_solve("Find the digit sum of 2^{10}.", verbose=True)
print(f"Answer: {r.answer}")
print(f"Path: {r.astar_result.format_path() if r.astar_result else 'none'}")
