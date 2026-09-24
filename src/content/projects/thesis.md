---
title: "Geometrically-Grounded Uncertainty Quantification for Foundational 3D Vision Models"
shortTitle: "SE(3) Uncertainty for VGGT"
hook: "A 3D foundation model that says how much to trust the poses it predicts."
oneLiner: >
  Extends VGGT with a separate branch that predicts a full 6x6 camera-pose
  covariance on the SE(3) manifold, while the backbone and the pose predictor
  stay frozen. The uncertainty ranks frames by their pose error and matches
  the structure of the covariance that bundle adjustment computes.
abstract: >
  Foundation models for 3D vision such as VGGT predict camera poses without
  any measure of confidence, which makes them difficult to use wherever
  probabilistic reasoning matters, from sensor fusion to active vision. This
  thesis extends VGGT with a separate covariance branch that predicts a full
  6x6 camera-pose covariance, formulated on the SE(3) manifold. It uses a
  body-centric perturbation model on the Lie algebra se(3), a left-invariant
  weighted metric that reconciles translational and rotational units, and a
  scale-aware negative log-likelihood trained with a curriculum for stability.
  On held-out CO3D sequences the predicted uncertainty ranks frames by their
  pose error and has the right scale on typical frames, though the errors are
  heavier-tailed than a Gaussian. Its structure matches the analytical
  covariance of bundle adjustment. On dynamic EPIC-KITCHENS video the
  uncertainty is large across the whole reconstruction, correctly signalling
  that it is unreliable.
tags:
  - 3D vision
  - structure-from-motion
  - SE(3) / Lie groups
  - uncertainty estimation
  - VGGT
  - probabilistic deep learning
role: "Sole author, BSc thesis. Supervised by Prof. Alessandro Pigati, Bocconi University."
status: completed
period: "2026"
links:
  - label: "Thesis page"
    url: "/thesis/"
  - label: "Code (GitHub)"
    url: "https://github.com/VanniLeonardo/Bachelor-Thesis"
  - label: "Thesis (PDF)"
    url: "https://github.com/VanniLeonardo/Bachelor-Thesis/releases/download/v1.0.0/bachelor_thesis.pdf"
featured: true
order: 2
---


**Problem.** Feed-forward 3D foundation models made reconstruction fast and
robust, but they answer with a single estimate and no measure of confidence.
Downstream systems such as sensor fusion, active vision, and robotics need to
know how far to trust each pose, not only what the pose is.

**Idea.** Keep VGGT's backbone and pose prediction frozen, and train a second
lightweight branch to predict a full $6 \times 6$ covariance for each camera
pose, formulated on $\mathrm{SE}(3)$. The branch uses body-centric
perturbations on the Lie algebra, a left-invariant metric that reconciles
meters with radians, and a negative log-likelihood with a curriculum that
prevents the covariances from collapsing.

**Why it matters.** On CO3D the predicted uncertainty ranks frames by their
pose error and its structure matches the analytical covariance of classical
bundle adjustment; the fitted temperature is 1.01, so the head is already
calibrated on typical frames. On EPIC-KITCHENS it reports that a dynamic
reconstruction is unreliable as a whole, though it does not single out the
individual frames that are misplaced. This turns an otherwise deterministic
reconstructor into a component that can be used in probabilistic pipelines,
without modifying its frozen pose predictor.
