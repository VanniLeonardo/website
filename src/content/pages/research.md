---
title: "Research"
description: "Research interests of Leonardo Vanni: 3D and 4D computer vision, egocentric vision, geometric learning."
---

Most of my work sits where 3D vision meets geometry. Three threads:

## Dynamic 3D reconstruction in the wild

Real video — especially egocentric video — is full of events that break the
assumptions of current 4D representations: objects get cut, opened, broken,
taken apart. **TopoEgo**, my ongoing first-author project, extends 4D Gaussian
Splatting with piece-wise rigid kinematic tracking so that topological changes
are modeled explicitly rather than smeared away, and introduces a benchmark
for these events built from EPIC-KITCHENS and Ego4D.

## Reliable 3D foundation models

Feed-forward models like VGGT made reconstruction fast and robust, but they
answer with a single deterministic guess. My [bachelor thesis](/thesis/) gave
VGGT a probabilistically grounded notion of confidence — full $6 \times 6$
camera-pose covariances on $\mathrm{SE}(3)$ — so the model can tell you when
not to trust it. I'm interested in what calibrated geometric confidence
unlocks downstream: sensor fusion, active vision, robotics.

## Geometry as an inductive bias

Lie groups, manifold-aware losses, and topological structure aren't formalism
for its own sake — they're what makes models behave correctly under the
transformations the world actually applies. A secondary ongoing direction
applies a similar mindset to formal mathematics: discrete diffusion models for
theorem proving in Lean, with the Lean kernel as an automated verifier.
