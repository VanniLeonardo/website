---
title: "Geometrically-Grounded Uncertainty Quantification for Foundational 3D Vision Models"
kind: "BSc thesis"
institution: "Bocconi University"
supervisor: "Prof. Alessandro Pigati"
year: 2026
pdf: "/thesis/vanni-2026-bsc-thesis.pdf"
description: "BSc thesis extending VGGT with SE(3)-consistent camera-pose uncertainty for learned structure-from-motion."
---

## In one breath

Modern 3D foundation models reconstruct a scene in a single forward pass, but
they give one answer with no sense of how much to trust it. This thesis
teaches one of them to know when it might be wrong.

## Abstract

Foundational 3D models such as VGGT regress camera poses deterministically,
with no measure of confidence — which makes them unusable wherever
probabilistic reasoning matters, from sensor fusion to active vision. The
thesis extends VGGT with a decoupled covariance branch that predicts a full
$6 \times 6$ camera-pose covariance, formulated rigorously on the
$\mathrm{SE}(3)$ manifold: a body-centric perturbation model on the Lie
algebra $\mathfrak{se}(3)$, a left-invariant weighted metric reconciling
translational and rotational units, and a scale-aware negative log-likelihood
trained with a curriculum strategy for stability. Experiments on CO3D show
the learned uncertainty is calibratable with a single temperature and
structurally matches analytical covariances from classical Bundle Adjustment,
while robustness tests on EPIC-KITCHENS show the predicted variance spiking
exactly on mislocalized frames — a built-in failure detector.

## Contributions

- **Probabilistic extension of a foundational model** — VGGT predicts a full
  distribution over camera poses instead of a point estimate, while its
  state-of-the-art mean prediction is preserved exactly (frozen pathway).
- **Decoupled covariance head** — a parallel, lightweight branch conditioned
  on visual evidence, the solver's internal state, and an explicit scene-scale
  embedding.
- **Geometric rigor on Lie groups** — body-centric perturbations on
  $\mathfrak{se}(3)$, a weighted left-invariant Riemannian metric, and a
  scale-aware NLL with Cholesky-parameterized covariances.
- **Stable training strategy** — a regularization-first curriculum
  (scale, conditioning, balance) followed by NLL fine-tuning, preventing
  degenerate collapse.

<!-- FIGURES: export two from the thesis PDF and place in src/assets/thesis/:
     1. Calibration plot (Figure 2, p.33) — caption: "Temperature scaling
        (T = 3.33) aligns the empirical Mahalanobis CDF with the theoretical
        chi-squared ideal."
     2. One uncertainty-ellipsoid render — recommended: the Kitchen sequence
        (Figure 6) or Pyramid sequence (Figure 5) — caption: "Predicted
        translational uncertainty grows with distance from the reference
        camera and aligns with COLMAP's analytical covariance axes." -->

<!-- ## Cite

```bibtex
@thesis{vanni2026geometric,
  author      = {Vanni, Leonardo},
  title       = {Geometrically-Grounded Uncertainty Quantification
                 for Foundational 3D Vision Models},
  school      = {Bocconi University},
  year        = {2026},
  type        = {BSc thesis},
  note        = {Supervisor: Alessandro Pigati}
}
``` -->
