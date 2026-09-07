---
title: "Experience"
description: "Experience of Leonardo Vanni. Open-source contributions to Kornia, medical 3D vision, real-time perception for a prosthetic arm, and machine learning engineering at Accenture."
# Roles, newest first. Every bullet must be supported by the current CV.
# `featured` entries also appear, without bullets, on the homepage.
entries:
  - role: "Open-Source Contributor"
    organization: "Kornia"
    period: "June 2026 – present"
    featured: true
    bullets:
      - "Added MAE, RMSE, and bad-pixel stereo disparity metrics, with tests and documentation."
      - "Removed import-time TorchScript decorators across the geometry module, which improves import behaviour across the library."
    links:
      - label: "Disparity metrics (PR #3743)"
        url: "https://github.com/kornia/kornia/pull/3743"
      - label: "TorchScript fix (PR #3757)"
        url: "https://github.com/kornia/kornia/pull/3757"
  - role: "Computer Vision Researcher"
    organization: "Vision Dental"
    period: "June 2025 – September 2025"
    featured: true
    bullets:
      - "Built a GPU-accelerated CT reconstruction and 3D U-Net pipeline that segments and classifies scans, producing reports at the level of individual teeth and lesions."
      - "Added ensemble-based voxel uncertainty, temperature calibration, and abstention on high-risk predictions when confidence is low."
  - role: "Computer Vision Lead, Intelligent Prosthetic Arm"
    organization: "Politecnico di Milano & Bocconi AI and Neuroscience Association"
    period: "September 2024 – June 2025"
    featured: true
    bullets:
      - "Led 3D scene perception for an EEG-controlled prosthetic arm, combining object detection, monocular depth, segmentation, hand tracking, and Kalman-filtered state estimation."
      - "Implemented real-time grasp validation from object geometry and hand pose, with a graphical demonstrator and a containerized deployment."
    links:
      - label: "Code (GitHub)"
        url: "https://github.com/VanniLeonardo/Prosthetic-Arm"
      - label: "Report (ResearchGate)"
        url: "https://www.researchgate.net/publication/393399982_Vision-Based_Grasp_Validation_for_Prosthetic_Arms_using_3D_Scene_Analysis"
  - role: "Machine Learning Engineer, Data and AI"
    organization: "Accenture"
    period: "June 2025 – September 2025"
    featured: true
    bullets:
      - "Built a BERT and medical-LLM pipeline mapping diagnoses to a 20,000-class medical ontology with 94% accuracy."
      - "Increased OCR and OpenCV document throughput from 2 to 15 documents per minute, a 7.5 times improvement."
# Compact teaching and leadership block, shown below the roles.
teaching:
  - role: "Teaching Assistant, Mathematical Analysis II"
    organization: "Bocconi University"
    period: "January 2025 – July 2026"
    note: "Selected by faculty to design and deliver three lectures on multivariable analysis and optimization."
  - role: "AI Tutor Developer, Advanced Analysis and Optimization I"
    organization: "Bocconi University"
    period: "January 2025 – July 2026"
    note: "Developed the official course tutor for personalized guidance on ODE theory."
  - role: "Guest Speaker"
    organization: "Bocconi Summer School"
    period: "2025"
    note: "Delivered a computer-vision lecture and practical workshop."
  - role: "Head of Research"
    organization: "Bocconi AI and Neuroscience Association"
    period: "October 2023 – July 2026"
    note: "Coordinated and mentored 60 student researchers, defining ML projects with faculty and external research partners."
  - role: "Cofounder"
    organization: "Bocconi Association for Mathematical Sciences"
    period: "July 2025 – July 2026"
    note: "Established a faculty-mentored training program for the Imperial–Cambridge Mathematics Competition; placed 45th of 680 in round one and qualified for round two."
---

Research and engineering roles across open source, medical imaging, robotics
perception, and applied machine learning.
