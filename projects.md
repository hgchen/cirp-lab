# Projects

## Computational Imaging for Robotic Perception

### FringeTact: Contact and Force Sensing with Photoelastic Imaging
folder: FringeTact
name: FringeTact
lead: Feimei Chen
members: Asif Sijan | Munir Zarea | Roxanne Kate Balanay | Riki MacMillan | Christian Moore | Tyler R. Ray | Frankie Zhu | Akshat Dave | Tianlu Wang
pi: Huaijin Chen
short: A transparent tactile sensor reads patterns of light to locate contact and estimate normal and shear forces.
description: When an object presses on a photoelastic block, stress changes the polarization of light passing through it. Front and side cameras observe the resulting fringes. The same transparent surface also lets a camera see the object in contact.
approach: A finite-element model simulates stress inside the block. A polarized-light renderer translates that stress into images used to train a network, which is then fine-tuned on real camera pairs. The network estimates contact footprint, pressure and shear, and integrates them to recover net force.
question: How can a camera measure contact forces?
preview: images/previews/fringetact.webp
summary: FringeTact reads patterns of polarized light in a transparent sensor to locate contact and measure forces both into and across its surface.
cover: contact-force.webp
caption: Front and side views of the sensor, simulated fringes and predicted contact maps during a sphere drag. Arrows show shear direction.
video: contact-demo.mp4
video_poster: contact-demo-poster.webp
video_caption: Real camera footage and predicted fringe patterns are shown side by side as the load changes. The plot tracks force over time.
detail: sensor.webp
detail_caption: Two cameras view the photoelastic cube through crossed polarizers. The exploded view shows the optical and mechanical components.
---

### Snapshot Hyperspectral Imaging with Diffractive Optical Elements
folder: DOE-HSI
name: Snapshot hyperspectral imaging
lead: Chuanjun Zheng
pi: Huaijin Chen
members: Feimei Chen
short: We develop diffractive optical elements for snapshot hyperspectral imaging that encode spectral information into a single sensor measurement for compact, high-speed, and light-efficient spectral perception.
description: We develop diffractive optical elements (DOEs) for snapshot hyperspectral imaging, where wavelength-dependent information is optically encoded into a single sensor measurement. By optimizing the DOE structure, different spectral components are transformed into distinct spatially varying point spread functions on the detector. The DOE can be engineered to achieve narrow spectral responses, characterized by a small full width at half maximum (FWHM), which improves spectral resolution and reduces inter-band interference. Together with computational reconstruction, this optical encoding supports accurate recovery of the full spectral profile at each pixel and enables a compact, high-speed, and light-efficient hyperspectral imaging system.
---

### Autonomous Coconut Rhinoceros Beetle Infestation Management
folder: FRC2026
field_photo: images/gallery/palm_capture.jpg
field_caption: Members of the field team observing palms in Hawaiʻi.
name: Field robotics for palm health
lead: Christian Moore
pi: Huaijin Chen
members: Riki MacMillan | Kanta Saito | Wilson Huynh | Elijah Saloma
short: A climbing robot for inspecting and treating coconut rhinoceros beetle infestations in palms.
description: The team is developing a palm-climbing mechanism and an end effector for pesticide deployment and flower trimming. Simulated and teleoperated trials are used to study how the arm can interact with the tree before testing on hardware.
---

### FishEye: Robust 3D Fish Measurement from Single Image or Video
folder: FishEye
name: FishEye
lead: Ethan Chung
pi: Huaijin Chen
members: Vincent Chan
short: We develop a low-cost computer vision pipeline for estimating fish length and volume from single images or videos using detection, segmentation, depth estimation, and 3D reconstruction.
description: FishEye is a scalable pipeline for automatic 3D fish morphometry using consumer-grade devices such as smartphone cameras. The system combines deep learning based detection and segmentation, transformer-based camera calibration, depth estimation, and 3D reconstruction from single or multiple images. It then derives geometric length measurements from reconstructed models and can use ping pong ball detection as an optional fiducial marker for scale calibration. The goal is to provide practical, field-deployable fish measurement tools for sustainable fisheries, ecological research, and aquaculture monitoring.
---

### Robot-Tablet Multimodal Behavioral Phenotyping for Cognitive Concern in Older Adults
folder: MCI
name: Robot–tablet interaction in older adults
lead: Yang Qian
pi: Huaijin Chen
members: Christian Moore | Ethan Chung | Sean Hiroki Flynn | Riki MacMillan
short: We develop a robot-tablet platform for brief, standardized interaction with older adults to capture multimodal behavioral biomarkers of cognitive concern beyond what paper, tablet-only, or static voice-based screening can measure.
description: Robot-Tablet Multimodal Behavioral Phenotyping for Cognitive Concern in Older Adults develops an embodied assessment platform for brief, standardized interaction with older adults. A humanoid robot delivers contingent speech, orienting cues, and task prompts, while a tablet captures response timing, task performance, and interaction events with high precision. Rather than diagnosing MCI directly, the project focuses on measuring clinically relevant multimodal behavioral biomarkers, including speech, response timing, drawing, tapping, motion, and conversational adaptation, that are difficult to capture with paper-only, tablet-only, or static voice-based screening.
---

## Physics-Informed AI

### ImagingBench: Can AI Solve Imaging Problems?
folder: CIBench
name: ImagingBench
slug: imagingbench
website: https://cirplab-fourier.taildc92d1.ts.net/
lead: Ethan Chung
pi: Huaijin Chen
members: Chuanjun Zheng | Jasper Tan | Jingxi Li
short: ImagingBench tests what multimodal AI models have learned about image formation and reconstruction.
description: Can an image model recover a scene when the sensor measurement looks nothing like a photograph? ImagingBench evaluates six models on tasks spanning optics, image processing, inverse reconstruction, computational sensing and calibration. Twenty of the 22 tasks produce images. Lens design and camera calibration produce text and are scored separately.
approach: Inverse tasks ask a model to reconstruct an image using either an expert’s instructions or an image-specific plan written by a vision–language model. Five tasks also run in the forward direction, asking the model to simulate a sensor measurement from a clean image. Specialized methods outperform general-purpose models on lensless imaging and holography, where a plausible picture can still be an inaccurate reconstruction.
question: What have multimodal AI models learned about image formation?
preview: images/previews/imagingbench-expert.png
preview_caption: ImagingBench Expert protocol. Overall scores on the 0–100 scale are Gemini-3.1-Flash-Image 61.4, GPT-Image-2 57.3, FLUX.2-Pro 56.6, GPT-Image-1.5 50.2, Qwen-Image-Edit-2511 42.7 and HunyuanImage-3.0 26.5.
summary: ImagingBench tests six models on 22 computational imaging tasks. Can they recover a scene from a lensless measurement, or simulate what a sensor records when given the scene?
cover: benchmark.webp
caption: The five task families and three evaluation settings, alongside the aggregate performance reported for each model.
detail: reconstructions.webp
detail_caption: Example measurements, model outputs and reference images across 12 benchmark tasks. Open the figure to inspect individual rows.
---

### Physics-Informed Machine Learning for Accelerated Discovery and Dynamics Analysis in Ultrafast X-Ray Diffraction
folder: XRD-ML
name: Learning ultrafast X-ray dynamics
lead: Ethan Chung
pi: Huaijin Chen
members: Vincent Chan
short: We develop physics-informed machine learning methods that connect atomistic simulations with ultrafast X-ray measurements for faster discovery and dynamics analysis.
description: This project builds machine learning methods for interpreting ultrafast X-ray photon correlation spectroscopy, which provides time-resolved access to structural dynamics across atomic to microscale regimes. A central challenge is the gap between atomistic simulations and experimentally measurable XPCS observables, especially for glass transition and supercooled liquid studies. The project learns dynamical representations from simulation data and predicts temporal correlation functions measured in XPCS, enabling direct quantitative comparison between simulation and experiment. This creates a pathway for interpreting XPCS data and studying microscopic mechanisms behind complex material dynamics.
---

### Satellite-Derived Shorelines
folder: SDS
name: Satellite-derived shorelines
lead: Joel Nicolow
pi: Dr. Charles Fletcher
members:
short: We develop and benchmark satellite-derived shoreline segmentation methods that generalize across diverse coastal environments, enabling more reliable and scalable shoreline monitoring in Hawaii and beyond.
description: Satellite-Derived Shorelines develops and evaluates shoreline segmentation methods for satellite-derived shoreline monitoring under realistic geographic domain shifts. Coastal erosion is an urgent challenge in Hawaii, but traditional field and aerial surveys are costly and sparse, while existing SDS extraction approaches often fail to generalize beyond narrow coastal morphologies or regions. This project combines global and local ground-truth shoreline positions with hand-annotated satellite scenes spanning diverse coastal environments to benchmark foundation and pretrained geospatial vision models, lightweight neural networks, and traditional thresholding methods. The goal is to provide a standardized benchmark and more robust open-source SDS tools that support reliable shoreline monitoring for researchers, coastal managers, and communities worldwide.
---

### ML-Driven Surrogate Modeling for FEL Oscillator Cavity Optimization
folder: FEL-Oscillator
name: Modeling free-electron lasers
lead: Ethan Chung
pi: Huaijin Chen
members:
short: We build machine learning surrogate models to accelerate free-electron laser oscillator simulations and support faster cavity design, tuning, and optimization.
description: This project develops a machine learning framework to accelerate and augment simulations of free-electron laser oscillators, which are commonly modeled with computationally intensive tools such as GINGER. The work focuses on predicting electron beam energy evolution and output radiation characteristics as functions of cavity geometry, including mirror spacing and cavity length. By replacing some expensive simulation sweeps with learned surrogate models, the system can support rapid parameter exploration, real-time tuning, more efficient design optimization, and improved control over FEL performance metrics such as gain, stability, and spectral properties.
---
