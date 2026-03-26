# Sketch: Software Phase-Locked Loop on SPD Manifolds

**Status:** Rough sketch for future chapter. Origin: BirdCLEF 2026 soundscape problem.

## Core Idea

A phase-locked loop (PLL) tracks a signal buried in noise by continuously adjusting an internal oscillator to match. Replace the oscillator with a geometric template on SPD(n) and the phase detector with geodesic distance — you get a tracker that "locks on" to a species' spectral signature through noise, overlap, and drift.

## Architecture

```
Incoming spectrogram window
        |
        v
  [Phase Detector] --- geodesic distance d(Σ_window, Σ_template) on SPD(n)
        |
        v
  [Loop Filter] --- exponential moving average on the manifold
        |                (Karcher mean with decaying weights)
        v
  [VCO / Template Update] --- Σ_template evolves along geodesic
        |                      toward Σ_window when lock is strong
        v
  [Lock Indicator] --- confidence: 1/(1 + d²/σ²)
```

## Mathematical Sketch

### State Space

- Template covariance: $\Sigma_{\text{tpl}} \in \text{SPD}(n)$, initialized from training data for each species
- Lock state: $\phi \in [0, 1]$ (0 = unlocked, 1 = locked)
- Frequency estimate: spectral centroid trajectory $\omega(t)$

### Phase Detector (on SPD manifold)

For incoming spectrogram window, compute covariance $\Sigma_w$ of mel band energies.

Phase error using Log-Euclidean metric:

$$e(t) = \|\log(\Sigma_w) - \log(\Sigma_{\text{tpl}})\|_F$$

Or affine-invariant metric:

$$e(t) = \|\log(\Sigma_{\text{tpl}}^{-1/2} \Sigma_w \Sigma_{\text{tpl}}^{-1/2})\|_F$$

### Loop Filter

Exponential moving average of phase error on the manifold. Not Euclidean averaging — use Karcher mean with decaying weights:

$$\bar{\Sigma}_{t+1} = \arg\min_{\Sigma \in \text{SPD}(n)} \sum_{k=0}^{t} \alpha^{t-k} \, d^2(\Sigma, \Sigma_k)$$

In practice, approximate with one step of Riemannian gradient descent:

$$\bar{\Sigma}_{t+1} = \bar{\Sigma}_t^{1/2} \exp\left(\beta \log(\bar{\Sigma}_t^{-1/2} \Sigma_w \bar{\Sigma}_t^{-1/2})\right) \bar{\Sigma}_t^{1/2}$$

where $\beta \in (0, 1)$ is the loop bandwidth.

### VCO / Template Update

When locked ($\phi > \theta$), the template drifts toward the observed signal — tracking frequency drift, distance changes, etc:

$$\Sigma_{\text{tpl}} \leftarrow \text{geodesic}(\Sigma_{\text{tpl}}, \Sigma_w, \beta \cdot \phi)$$

When unlocked, template stays fixed (free-running oscillator).

### Lock Detector

$$\phi(t) = \frac{1}{1 + e(t)^2 / \sigma^2}$$

Threshold $\theta$ determines lock/unlock transitions. Hysteresis prevents chattering:
- Lock when $\phi > \theta_{\text{high}}$
- Unlock when $\phi < \theta_{\text{low}}$

### Multi-Species Bank

Run N PLLs in parallel (one per species template). Each PLL independently tracks its species. A species is "present" in the soundscape window when its PLL is locked.

This is analogous to a filterbank / channelizer in radio — each channel locks onto a different carrier frequency. Here each channel locks onto a different geometric signature.

## Properties

1. **Noise robustness**: PLL inherently rejects noise outside the loop bandwidth
2. **Frequency tracking**: handles Doppler drift from moving birds
3. **Intermittent signals**: lock indicator naturally handles burst signals — locks during calls, unlocks during silence
4. **Multi-label**: parallel PLL bank gives independent detection per species
5. **No retraining needed**: templates computed from training data, PLL parameters tuned once

## Connections to Existing Framework

- Phase detector = geodesic distance on SPD(n) (Chapter 20.2)
- Loop filter = Riemannian exponential moving average (new)
- Lock detector = confidence metric from manifold distance (similar to DRI, Chapter 20.5)
- Multi-species bank = structural fuzzing sensitivity analysis over species dimension
- Template initialization = SPD cluster centroids from training data

## Open Questions

- Optimal loop bandwidth $\beta$ vs noise level — relate to manifold curvature?
- Relationship between PLL lock time and Pisano-like periodicity of bird calls
- Can TDA persistent homology features improve the lock detector? (topological lock)
- Adaptive bandwidth: widen when searching, narrow when locked (like a real PLL)
- Connection to Kalman filtering on SPD manifolds (the loop filter IS a manifold Kalman filter)

## Code Sketch

```python
class GeometricPLL:
    """Phase-locked loop on SPD(n) for tracking spectral signatures."""

    def __init__(self, template_cov, bandwidth=0.1, lock_threshold=0.7):
        self.template = template_cov  # SPD(n) matrix
        self.bandwidth = bandwidth
        self.lock_threshold = lock_threshold
        self.lock_state = 0.0
        self.sigma = 1.0  # noise floor estimate

    def update(self, window_cov):
        """Process one spectrogram window. Returns (locked, confidence)."""
        # Phase detector: geodesic distance on SPD(n)
        error = log_euclidean_distance(window_cov, self.template)

        # Lock detector
        confidence = 1.0 / (1.0 + error**2 / self.sigma**2)
        locked = confidence > self.lock_threshold

        # Template update (VCO) — only when locked
        if locked:
            self.template = spd_geodesic(
                self.template, window_cov,
                t=self.bandwidth * confidence)

        self.lock_state = confidence
        return locked, confidence


class SpeciesPLLBank:
    """Parallel PLL bank — one per species."""

    def __init__(self, species_templates):
        self.plls = {
            species: GeometricPLL(template)
            for species, template in species_templates.items()
        }

    def process_window(self, window_cov):
        """Returns dict of {species: confidence} for locked species."""
        detections = {}
        for species, pll in self.plls.items():
            locked, conf = pll.update(window_cov)
            if locked:
                detections[species] = conf
        return detections
```
