---
title: "TopoEgo: Topological-Aware 4D Gaussian Splatting for Egocentric Vision"
oneLiner: "4D Gaussian Splatting for egocentric video where objects are cut, split, fractured, and taken apart."
abstract: >
  Current 4D Gaussian Splatting methods assume scene topology never changes: a
  connected object must remain connected. Egocentric video violates this
  constantly — cutting, opening, breaking, disassembly — and continuous
  deformation fields respond with severe stretching and ghosting artifacts.
  TopoEgo extends rigid tracking into a piece-wise rigid kinematic tracker,
  using spacetime clustering to route canonical Gaussians into independent
  post-event SE(3) branches at topological boundaries. The project also
  introduces the TopoEgo benchmark: curated EPIC-KITCHENS and Ego4D sequences
  with camera poses, dense 2D segmentation masks, and temporal state-change
  annotations for discontinuous egocentric interactions.
tags:
  - 4D Gaussian Splatting
  - egocentric vision
  - dynamic scene reconstruction
  - SE(3)
  - benchmark
role: "First author"
# Affiliation note: Tombari can alternatively be listed as "(TUM & Google)" —
# many of his papers use the dual affiliation. Confirm his preference before launch.
collaborators: "with Chiara Plizzari (Bocconi University), Stefano Gasperini (TUM), and Federico Tombari (TUM & Google)"
status: ongoing
period: "Jan 2026 – present"
comingSoon: "Paper, code, and the TopoEgo benchmark will be released publicly upon acceptance."
featured: true
order: 1
---

<!-- No body content in v1. No links, no figures, no results — binding rule.
     On public release: promote to /projects/topoego/, add paper/code/benchmark
     links, replace comingSoon with links array. -->
