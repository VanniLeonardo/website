---
title: "Intelligent Prosthetic Arm — Real-Time Vision for Grasp Validation"
shortTitle: "Prosthetic Arm Vision"
hook: "Real-time vision for a hand that can't afford to guess."
oneLiner: >
  A live pipeline — detection, monocular depth, segmentation, hand tracking,
  Kalman-filtered 3D state — feeding a hybrid model that validates grasp
  feasibility from 3D object geometry and user hand pose, for an
  EEG-controlled prosthetic arm.
abstract: >
  A collaboration between BAINSA (Bocconi AI & Neuroscience Association) and
  Politecnico di Milano to build an intelligent prosthetic arm combining
  EEG-based control with computer vision. I led the vision side: a real-time
  pipeline combining object detection, monocular depth estimation,
  segmentation, hand-pose tracking, 3D bounding boxes, and Kalman-filtered 3D
  state tracking, feeding a hybrid grasp-validation model that assesses
  feasibility from 3D object geometry and user hand pose. Ships with a GUI
  demo and a Docker setup.
tags:
  - real-time CV
  - object detection
  - monocular depth
  - segmentation
  - hand tracking
  - Kalman filtering
  - Docker
role: "Computer Vision Lead / Project Lead (BAINSA × Politecnico di Milano)"
status: public
period: "Sep 2024 – Jun 2025"
links:
  - label: "Code (GitHub)"
    url: "https://github.com/VanniLeonardo/Prosthetic-Arm"
  - label: "Report (ResearchGate)"
    url: "https://www.researchgate.net/publication/393399982_Vision-Based_Grasp_Validation_for_Prosthetic_Arms_using_3D_Scene_Analysis"
figure:
  src: "../../assets/prosthetic/grasp-validation.png"
  alt: "Two frames from the live demo. Left: a pinch grasp on a bottle, green box, labelled Grasp True 0.79. Right: a closed fist on the same bottle, red box, labelled Grasp False. Both frames overlay tracked hand landmarks and run at about 27 frames per second."
  caption: "Grasp validation running live at ~27 FPS: a feasible pinch (green, Grasp: True 0.79) and an infeasible fist on the same object (red, Grasp: False), with tracked hand landmarks and the object's 3D box."
featured: true
order: 3
---

**Problem.** An EEG-controlled prosthetic hand gets a noisy, low-bandwidth
intent signal from the user. Before it closes around an object, something has
to check — in real time, from a single camera — whether the grasp is actually
feasible.

**Idea.** Fuse object detection, monocular depth, segmentation, and hand-pose
tracking into Kalman-filtered 3D state for both the hand and the target, then
validate the intended grasp with a hybrid model that reasons about 3D object
geometry and hand pose together.

**Why it matters.** Grasp validation is the safety layer between "the user
thought about grasping" and "the motors move." The pipeline runs live, ships
with a GUI demo and a Docker setup, and the report is public.
