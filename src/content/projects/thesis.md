---
title: "Geometrically-Grounded Uncertainty Quantification for Foundational 3D Vision Models"
oneLiner: "Extending the VGGT 3D foundation model with SE(3)-consistent uncertainty estimation for learned structure-from-motion."
abstract: >
  Foundational 3D models such as VGGT regress camera poses deterministically,
  with no measure of confidence — which makes them unusable wherever
  probabilistic reasoning matters, from sensor fusion to active vision. This
  thesis extends VGGT with a decoupled covariance branch that predicts a full
  6×6 camera-pose covariance, formulated rigorously on the SE(3) manifold: a
  body-centric perturbation model on the Lie algebra se(3), a left-invariant
  weighted metric reconciling translational and rotational units, and a
  scale-aware negative log-likelihood trained with a curriculum strategy for
  stability. On CO3D, the learned uncertainty is calibratable with a single
  temperature and structurally matches analytical covariances from Bundle
  Adjustment; on EPIC-KITCHENS, the predicted variance spikes exactly on
  mislocalized frames — a built-in failure detector.
tags:
  - 3D vision
  - structure-from-motion
  - SE(3) / Lie groups
  - uncertainty estimation
  - VGGT
  - probabilistic deep learning
role: "Sole author (BSc thesis) — supervised by Prof. Alessandro Pigati, Bocconi University"
status: completed
period: "2026"
links:
  - label: "Thesis page"
    url: "/thesis/"
  - label: "Thesis (PDF)"
    url: "/thesis/vanni-2026-bsc-thesis.pdf"
featured: true
order: 2
---

<!-- The PDF is the acknowledgements-free version, supplied by Leonardo into
     public/thesis/. Do not commit a placeholder PDF. A code link is added only
     when a cleaned public repo exists (future phase). -->
