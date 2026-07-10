---
title: "Geometrically-Grounded Uncertainty Quantification for Foundational 3D Vision Models"
shortTitle: "SE(3) Uncertainty for VGGT"
hook: "A 3D foundation model that knows when it's wrong."
oneLiner: >
  Extends VGGT with a decoupled branch predicting full 6×6 camera-pose
  covariances on the SE(3) manifold. The uncertainty calibrates with a single
  temperature, structurally matches Bundle-Adjustment covariances, and spikes
  exactly on mislocalized frames — a built-in failure detector.
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
featured: true
order: 2
---

<!-- The direct PDF link lives only on /thesis/, where it is rendered
     conditionally: the button appears once the owner-supplied PDF exists at
     public/thesis/vanni-2026-bsc-thesis.pdf. Do not commit a placeholder PDF.
     A code link is added only when a cleaned public repo exists. -->

**Problem.** Feed-forward 3D foundation models made reconstruction fast and
robust, but they answer with a single deterministic guess. Downstream systems —
sensor fusion, active vision, robotics — need to know *how much* to trust each
pose, not just what it is.

**Idea.** Keep VGGT's state-of-the-art mean prediction frozen, and train a
parallel lightweight branch to predict a full $6 \times 6$ covariance over
each camera pose, formulated properly on $\mathrm{SE}(3)$: body-centric
perturbations on the Lie algebra, a left-invariant metric that reconciles
meters with radians, and a scale-aware negative log-likelihood with a
curriculum that prevents degenerate collapse.

**Why it matters.** On CO3D the learned covariances calibrate with a single
temperature and structurally match the analytical covariances of classical
Bundle Adjustment; on EPIC-KITCHENS the predicted variance spikes exactly on
mislocalized frames. That turns a black-box reconstructor into a component you
can put inside a probabilistic pipeline — and gives it a failure detector for
free.
