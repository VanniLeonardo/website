---
title: "Geometrically-Grounded Uncertainty Quantification for Foundational 3D Vision Models"
kind: "BSc thesis"
institution: "Bocconi University"
supervisor: "Prof. Alessandro Pigati"
year: 2026
pdf: "/thesis/vanni-2026-bsc-thesis.pdf"
description: "BSc thesis extending VGGT with camera-pose uncertainty on SE(3), for learned structure from motion."
---

## Summary

Modern 3D foundation models reconstruct a scene in a single forward pass, but
they give one answer with no sense of how far to trust it. This thesis teaches
one of them to report when it is likely to be wrong.

## Abstract

Foundation models for 3D vision such as VGGT predict camera poses without any
measure of confidence, which makes them difficult to use wherever
probabilistic reasoning matters, from sensor fusion to active vision. The
thesis extends VGGT with a separate covariance branch that predicts a full
$6 \times 6$ camera-pose covariance, formulated rigorously on the
$\mathrm{SE}(3)$ manifold: a body-centric perturbation model on the Lie
algebra $\mathfrak{se}(3)$, a left-invariant weighted metric reconciling
translational and rotational units, and a scale-aware negative log-likelihood
trained with a curriculum for stability. Experiments on CO3D show that a
single temperature calibrates the learned uncertainty and that its structure
matches the analytical covariances of classical bundle adjustment. Robustness
tests on EPIC-KITCHENS show the predicted variance rising sharply on frames
the model has placed wrongly, which gives the system a built-in failure
detector.

## Contributions

- **A probabilistic extension of a foundation model.** VGGT predicts a full
  distribution over camera poses instead of a single estimate, while its
  existing pose prediction is preserved exactly through a frozen pathway.
- **A separate covariance head.** A parallel lightweight branch conditioned on
  visual evidence, the solver's internal state, and an explicit embedding of
  scene scale.
- **Geometric rigour on Lie groups.** Body-centric perturbations on
  $\mathfrak{se}(3)$, a weighted left-invariant Riemannian metric, and a
  scale-aware negative log-likelihood with Cholesky-parameterized covariances.
- **A stable training strategy.** A curriculum that begins with
  regularization over scale, conditioning and balance, followed by fine-tuning
  on the negative log-likelihood, which prevents the covariances from
  collapsing.

<!-- FIGURES: export two from the thesis PDF and place in src/assets/thesis/:
     1. Calibration plot (Figure 2, p.33). Caption: "Temperature scaling
        (T = 3.33) aligns the empirical Mahalanobis CDF with the theoretical
        chi-squared ideal."
     2. One uncertainty-ellipsoid render — recommended: the Kitchen sequence
        (Figure 6) or Pyramid sequence (Figure 5). Caption: "Predicted
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
