---
title: "Geometrically-Grounded Uncertainty Quantification for Foundational 3D Vision Models"
shortTitle: "SE(3) Uncertainty for VGGT"
hook: "A 3D foundation model that reports when its own pose estimates are unreliable."
oneLiner: >
  Extends VGGT with a separate branch that predicts a full 6x6 camera-pose
  covariance on the SE(3) manifold. A single temperature calibrates the
  uncertainty, its structure matches the covariances produced by bundle
  adjustment, and it rises sharply on frames the model has placed wrongly,
  which gives the system a built-in failure detector.
abstract: >
  Foundation models for 3D vision such as VGGT predict camera poses without
  any measure of confidence, which makes them difficult to use wherever
  probabilistic reasoning matters, from sensor fusion to active vision. This
  thesis extends VGGT with a separate covariance branch that predicts a full
  6x6 camera-pose covariance, formulated on the SE(3) manifold. It uses a
  body-centric perturbation model on the Lie algebra se(3), a left-invariant
  weighted metric that reconciles translational and rotational units, and a
  scale-aware negative log-likelihood trained with a curriculum for stability.
  On CO3D, a single temperature calibrates the learned uncertainty and its
  structure matches the analytical covariances of bundle adjustment. On
  EPIC-KITCHENS, the predicted variance rises sharply on frames the model has
  placed wrongly, which gives the system a built-in failure detector.
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
featured: true
order: 2
---

<!-- The direct PDF link lives only on /thesis/, where it is rendered
     conditionally: the button appears once the owner-supplied PDF exists at
     public/thesis/vanni-2026-bsc-thesis.pdf. Do not commit a placeholder PDF.
     A code link is added only when a cleaned public repo exists. -->

**Problem.** Feed-forward 3D foundation models made reconstruction fast and
robust, but they answer with a single estimate and no measure of confidence.
Downstream systems such as sensor fusion, active vision, and robotics need to
know how far to trust each pose, not only what the pose is.

**Idea.** Keep VGGT's existing pose prediction frozen, and train a second
lightweight branch to predict a full $6 \times 6$ covariance for each camera
pose, formulated on $\mathrm{SE}(3)$. The branch uses body-centric
perturbations on the Lie algebra, a left-invariant metric that reconciles
meters with radians, and a scale-aware negative log-likelihood with a
curriculum that prevents the covariances from collapsing.

**Why it matters.** On CO3D the learned covariances calibrate with a single
temperature, and their structure matches the analytical covariances of
classical bundle adjustment. On EPIC-KITCHENS the predicted variance rises
sharply on frames the model has placed wrongly. This turns an otherwise
deterministic reconstructor into a component that can be used in probabilistic
pipelines, without modifying its frozen pose predictor.
