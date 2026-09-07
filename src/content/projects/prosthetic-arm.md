---
title: "Intelligent Prosthetic Arm: real-time vision for grasp validation"
shortTitle: "Prosthetic Arm Vision"
hook: "Checking whether a grasp is possible before the hand closes."
oneLiner: >
  A live pipeline combining object detection, monocular depth, segmentation,
  hand tracking, and Kalman-filtered 3D state. It feeds a model that judges
  whether a grasp is feasible from the object's 3D geometry and the user's
  hand pose, for a prosthetic arm controlled by EEG.
abstract: >
  A collaboration between BAINSA, the Bocconi AI and Neuroscience Association,
  and Politecnico di Milano, to build a prosthetic arm that combines EEG-based
  control with computer vision. I led the vision side. The pipeline runs in
  real time and combines object detection, monocular depth estimation,
  segmentation, hand-pose tracking, 3D bounding boxes, and Kalman-filtered
  state tracking. It feeds a grasp-validation model that judges feasibility
  from the object's 3D geometry and the user's hand pose. The project ships
  with a graphical demo and a Docker setup.
tags:
  - real-time CV
  - object detection
  - monocular depth
  - segmentation
  - hand tracking
  - Kalman filtering
  - Docker
role: "Computer Vision Lead and Project Lead, BAINSA and Politecnico di Milano."
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
  caption: "Grasp validation running live at about 27 frames per second. On the left a feasible pinch is accepted (green box, Grasp: True 0.79). On the right a closed fist on the same object is rejected (red box, Grasp: False). Both frames show the tracked hand landmarks and the object's 3D box."
featured: true
order: 3
---

**Problem.** A prosthetic hand controlled by EEG receives a noisy, low
bandwidth signal of the user's intent. Before the hand closes around an
object, something has to check whether the grasp is actually feasible, in real
time and from a single camera.

**Idea.** Combine object detection, monocular depth, segmentation, and
hand-pose tracking into a Kalman-filtered 3D state for both the hand and the
target object. A validation model then judges the intended grasp using the
object's 3D geometry and the hand pose together.

**Why it matters.** Grasp validation is the safety layer between the user
thinking about a grasp and the motors moving. The pipeline runs live, ships
with a graphical demo and a Docker setup, and the report is public.
