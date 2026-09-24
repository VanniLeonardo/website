---
title: "Geometrically-Grounded Uncertainty Quantification for Foundational 3D Vision Models"
kind: "BSc thesis"
institution: "Bocconi University"
supervisor: "Prof. Alessandro Pigati"
year: 2026
pdf: "https://github.com/VanniLeonardo/Bachelor-Thesis/releases/download/v1.0.0/bachelor_thesis.pdf"
repo: "https://github.com/VanniLeonardo/Bachelor-Thesis"
release: "https://github.com/VanniLeonardo/Bachelor-Thesis/releases/tag/v1.0.0"
description: "BSc thesis extending VGGT with camera-pose uncertainty on SE(3), for learned structure from motion."
---

## Summary

Modern 3D foundation models reconstruct a scene in a single forward pass, but
they give one answer with no measure of how much to trust it. This thesis
gives one of them a distribution over the poses it predicts, and asks how far
that distribution can be believed.

## Abstract

Foundation models for 3D vision such as VGGT predict camera poses without any
measure of confidence, which makes them difficult to use wherever
probabilistic reasoning matters, from sensor fusion to active vision. The
thesis extends VGGT with a separate covariance branch that predicts a full
$6 \times 6$ camera-pose covariance, formulated rigorously on the
$\mathrm{SE}(3)$ manifold: a body-centric perturbation model on the Lie
algebra $\mathfrak{se}(3)$, a left-invariant weighted metric reconciling
translational and rotational units, trained with a curriculum for stability.
The backbone and the mean-pose pathway stay frozen, so the point estimates of
the base model are unchanged. On held-out CO3D sequences the predicted
uncertainty ranks frames by their pose error and has the right scale on
typical frames, though the errors are heavier-tailed than the Gaussian model
assumes. Its structure matches the analytical covariance of bundle adjustment
on example scenes. On dynamic EPIC-KITCHENS video the uncertainty is large
across the whole reconstruction, correctly signalling that it is unreliable.

This is the revised version released in September 2026. Implementation errors
in the original training and evaluation code were found while preparing the
public release; they were corrected, the model was retrained, and every
quantitative result and figure was recomputed with the released code.

## Contributions

- **A probabilistic extension of a foundation model.** VGGT predicts a full
  distribution over camera poses instead of a single estimate, while its
  existing pose prediction is preserved exactly through a frozen pathway.
- **A separate covariance head.** A parallel lightweight branch conditioned on
  visual evidence and the solver's internal state.
- **Geometric rigour on Lie groups.** Body-centric perturbations on
  $\mathfrak{se}(3)$, a weighted left-invariant Riemannian metric, and a
  negative log-likelihood with Cholesky-parameterized covariances.
- **A stable training strategy.** A curriculum that begins with
  regularization over scale, conditioning and balance, followed by fine-tuning
  on the negative log-likelihood, which prevents the covariances from
  collapsing.


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
