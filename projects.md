# Projects

## Computational Imaging for Robotic Perception

### FringeTact: Contact and Force Sensing with Photoelastic Imaging
folder: FringeTact
name: FringeTact
lead: Feimei Chen | Asif Sijan
members: Munir Zarea | Roxanne Kate Balanay | Riki MacMillan | Christian Moore | Tyler R. Ray | Frankie Zhu | Akshat Dave | Tianlu Wang
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

### PolarTact3D: Single-Shot Tactile 3D Shape and Color Sensing with Polarization Imaging
folder: PolarTact3D
name: PolarTact3D
website: https://polartact3d.github.io/
members: Kai Garcia | Mairi Yoshioka | Tyler Ray | Tianlu Wang | Frances Zhu | Huaijin Chen
short: A polarization camera captures both the 3D shape and color of a contact surface in a single shot.
description: A clear polyethylene film conforms to an object when the sensor is pressed against it. A polarization camera sees the object’s color through the film and records polarization patterns that reveal the surface orientation. The team compared physics-based and neural methods for recovering shape and tested the sensor on surfaces that included transparent and reflective objects. PolarTact3D received the third-place Best Paper Award at the RSS 2025 Workshop on Navigating Contact Dynamics in Robotics.
cover: sensor-pipeline.webp
caption: The sensor design and the steps for reconstructing surface shape from polarization images.
detail: surface-reconstructions.webp
detail_caption: Example contact surfaces reconstructed with the neural and physics-based methods.
---

### Snapshot Hyperspectral Imaging with Diffractive Optical Elements
folder: DOE-HSI
name: Snapshot hyperspectral imaging
selected_work: 2
cover: doe-otf-map.png
caption: A diffractive optical element encodes the scene on a monochrome sensor. The diagram shows how the optical measurement and its simulation are used for spectral reconstruction.
summary: Diffractive optics encode wavelength information in a single exposure, enabling reconstruction of the spectrum at each pixel.
detail: doe-psf-grid.png
detail_caption: Reconstructed spectral bands (left) and the corresponding ground-truth bands (right) for the same scene.
lead: Chuanjun Zheng
pi: Huaijin Chen
members: Feimei Chen
short: We develop diffractive optical elements that encode spectral information in a single sensor measurement, enabling compact, fast, and light-efficient hyperspectral imaging.
description: We develop diffractive optical elements (DOEs) for snapshot hyperspectral imaging, where wavelength-dependent information is optically encoded into a single sensor measurement. An optimized DOE transforms different spectral components into distinct, spatially varying point spread functions on the detector. The DOE can be engineered to achieve narrow spectral responses, characterized by a small full width at half maximum (FWHM). Narrower responses improve spectral resolution and reduce inter-band interference. Together with computational reconstruction, this optical encoding supports accurate recovery of the full spectral profile at each pixel and enables a compact, high-speed, and light-efficient hyperspectral imaging system.
---

### Autonomous Coconut Rhinoceros Beetle Infestation Management
folder: FRC2026
field_photo: images/gallery/palm_capture.jpg
field_caption: Members of the field team observing palms in Hawaiʻi.
name: Field robotics for palm health
selected_work: 1
preview: images/previews/crb-symposium-demo.webp
caption: The team demonstrates a robotic arm and palm simulation.
gallery_caption_frc_2: A team member uses the physical arm to control the simulated arm.
gallery_caption_frc_3: A palm tree and nearby test objects in the simulation.
summary: We are developing a palm-climbing robot to inspect trees and treat coconut rhinoceros beetle infestations.
lead: Christian Moore
pi: Huaijin Chen
advisors: Daniel Jenkins | Ryan Kurasaki | Tianlu Wang | Daniel Drew | Xiaonan (Sean) Huang
members_label: University of Hawaiʻi at Mānoa team
members: Rona Lei Duldulao | Lucas Horsman | Wilson Huynh | Erik Bendickson | Christian Komo | Zadon Padello | Tyler Mak | Elijah Saloma | Kanta Saito | Ella Self | Andrew He | Lukas Moroz | Riki MacMillan | Alex Tokunaga | Owen Bramley
collaborators_label: University of Michigan team
collaborators: Nilay Choudhury | Xinqi Zhang | Yuchen You | Haobo Fang | Siyuan Zheng | Ronen Dujovny | Adrian Wang | Mingxuan He
short: A palm-climbing robot designed to inspect trees and treat coconut rhinoceros beetle infestations.
description: The team is developing a palm-climbing mechanism and an end effector for pesticide deployment and flower trimming. Simulated and teleoperated trials are used to study how the arm can interact with the tree before testing on hardware.
---

### FishEye: Robust 3D Fish Measurement from Single Image or Video
folder: FishEye
name: FishEye
related: FishPod
lead: Ethan Chung
pi: Huaijin Chen
members: Vincent Chan
short: We develop a low-cost computer vision pipeline for estimating fish length and volume from single images or videos using detection, segmentation, depth estimation, and 3D reconstruction.
description: FishEye measures fish in 3D using consumer-grade devices such as smartphone cameras. The system detects and segments fish with deep learning. It uses transformer-based camera calibration and depth estimation to reconstruct fish in 3D from one or more images. It measures length from those reconstructions and can use a ping-pong ball as an optional scale reference. The goal is to provide practical, field-deployable fish measurement tools for sustainable fisheries, ecological research, and aquaculture monitoring.
caption: FishEye detects the fish, estimates depth, and reconstructs its body in 3D for measurement.
---

### FishPod: Underwater Stereo Vision for Fish Measurement
folder: FishPod
name: FishPod
related: FishEye
pi: Huaijin Chen
members: Feimei Chen | Riki MacMillan | Munir
short: FishPod mounts a stereo camera on an underwater remotely operated vehicle to estimate fish length from paired video frames.
description: The system detects and tracks fish, segments their outlines, and matches points along their body axes between the two camera views. Stereo triangulation recovers the endpoints in 3D and yields an estimate of body length.
cover: stereo-pipeline.webp
preview: images/projects/FishPod/03-field-deployment.webp
caption: The FishPod workflow, from stereo video capture on an underwater vehicle to a 3D estimate of fish length.
gallery_title: Hardware, deployment and measurements
gallery_caption_01_method_comparison: Fish measurement approaches and the computing setups they use.
gallery_caption_02_hardware_design: The stereo camera and Raspberry Pi in a sealed housing, shown mounted on the vehicle.
gallery_caption_03_field_deployment: Preparing the vehicle and lowering it into the water during field deployment.
gallery_caption_04_recording_environments: Example frames from four recording environments.
gallery_caption_05_field_captures: The recording setups alongside example left and right stereo views.
gallery_caption_06_length_estimates: Four examples with estimated fish depth and body length.
---

### Robot-Tablet Multimodal Behavioral Phenotyping for Cognitive Concern in Older Adults
folder: MCI
name: Robot–tablet interaction in older adults
lead: Yang Qian
pi: Huaijin Chen
members: Christian Moore | Ethan Chung | Sean Hiroki Flynn | Riki MacMillan
short: We use a robot and tablet in brief, standardized sessions with older adults to measure behavioral markers of cognitive concern that are difficult to capture with paper-based, tablet-only, or static voice-based screening.
description: This project develops an embodied assessment platform for brief, standardized sessions with older adults. A humanoid robot delivers contingent speech, orienting cues, and task prompts, while a tablet captures response timing, task performance, and interaction events with high precision. The project measures clinically relevant behaviors, including speech, response timing, drawing, tapping, motion, and conversational adaptation, to study cognitive concern without directly diagnosing mild cognitive impairment (MCI).
caption: The assessment platform combines a humanoid robot with a tablet for delivering tasks and recording responses.
gallery_caption_cube_task_active_2026_04_14: The tablet shows the numbered and lettered circles used in the sequencing task.
gallery_caption_cube_task_briefing_2026_04_14: The briefing shows participants how to connect the circles in order.
gallery_caption_task2_animals_demo_2026_04_14: The instructions introduce the animal-naming task and show the pictures participants will see.
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
preview_caption: Under the ImagingBench Expert protocol, Gemini-3.1-Flash-Image scored 61.4 out of 100, followed by GPT-Image-2 (57.3), FLUX.2-Pro (56.6), GPT-Image-1.5 (50.2), Qwen-Image-Edit-2511 (42.7), and HunyuanImage-3.0 (26.5).
summary: ImagingBench tests six models on 22 computational imaging tasks. Can they recover a scene from a lensless measurement or simulate what a sensor would record for a given scene?
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
description: This project develops machine learning methods for interpreting ultrafast X-ray photon correlation spectroscopy (XPCS), which tracks structural changes over time from the atomic scale to the microscale. A central challenge is connecting atomistic simulations to quantities that XPCS can measure, especially in studies of the glass transition and supercooled liquids. Models learn from simulated dynamics and predict the temporal correlation functions that XPCS measures. This lets researchers compare simulations directly with experiments and study the microscopic processes behind changes in materials.
caption: Simulated argon structures at different densities and temperatures.
---

### Satellite-Derived Shorelines
folder: SDS
name: Satellite-derived shorelines
lead: Joel Nicolow
pi: Dr. Charles Fletcher
members:
short: We develop and test methods for mapping shorelines from satellite imagery across different coastal environments in Hawaiʻi and beyond.
description: This project develops methods for mapping shorelines from satellite imagery and evaluates how well they work across regions. Coastal erosion is an urgent challenge in Hawaiʻi. Field and aerial surveys are costly and limited in coverage, and existing automated methods often work well only in certain regions or on certain types of coasts. The project combines reference shoreline positions from local and global sources with hand-annotated satellite scenes to compare foundation and pretrained geospatial vision models, lightweight neural networks, and traditional thresholding methods. The goal is to provide a standardized benchmark and more reliable open-source tools for researchers, coastal managers, and communities.
caption: The map shows where shorelines in Hawaiʻi eroded or grew over a five-year period.
gallery_caption_sds_shorelines_superimposed_on_drone_image: Shorelines derived from satellite imagery overlaid on a drone photo.
gallery_caption_sandies_sds_example_and_transect_intersections: Examples of shoreline detection and intersections with coastal transects.
gallery_caption_sat_image_examples: The same coastline seen by different satellite sensors.
gallery_caption_segmentation_method_comparison: Comparison of land and water segmentation methods on the same stretch of coast.
---

### ML-Driven Surrogate Modeling for FEL Oscillator Cavity Optimization
folder: FEL-Oscillator
name: Modeling free-electron lasers
lead: Ethan Chung
pi: Huaijin Chen
members:
short: We build machine learning surrogate models to accelerate free-electron laser oscillator simulations and support faster cavity design, tuning, and optimization.
description: Free-electron laser (FEL) oscillators are commonly modeled with computationally intensive tools such as GINGER. This project develops surrogate models to predict how changes in cavity geometry, including mirror spacing and cavity length, affect electron beam energy and the resulting radiation. The goal is to replace some full simulation sweeps so researchers can explore designs faster, tune the cavity in real time, and better control gain, stability, and spectral properties.
caption: A free-electron laser oscillator showing the electron source, accelerator, undulator, and cavity mirrors.
---
