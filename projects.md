# Projects

## Imaging and Perception Systems for Robotics

### FringeTact: Contact and Force Sensing with Photoelastic Imaging
folder: FringeTact
topic: Sensor design and prototyping
name: FringeTact
selected_work: 1
lead: Feimei Chen | Asif Sijan
members: Munir Zarea | Roxanne Kate Balanay | Riki MacMillan | Christian Moore | Tyler R. Ray | Frankie Zhu | Akshat Dave | Tianlu Wang
pi: Huaijin Chen
short: A transparent tactile sensor reads patterns of light to locate contact and estimate normal and shear forces.
description: When an object presses on a photoelastic block, stress changes the polarization of light passing through it. Front and side cameras observe the resulting fringes. The same transparent surface also lets a camera see the object in contact.
approach: A finite-element model simulates stress inside the block. A polarized-light renderer translates that stress into images used to train a network, which is then fine-tuned on real camera pairs. The network estimates contact footprint, pressure and shear, and integrates them to recover net force.
question: How can a camera measure contact forces?
preview: images/previews/fringetact.webp
summary: FringeTact reads patterns of polarized light in a transparent sensor to locate contact and measure normal and shear forces.
cover: contact-force.webp
caption: Front and side views of the sensor, simulated fringes and predicted contact maps during a sphere drag. Arrows show shear direction.
video: contact-demo.mp4
video_poster: contact-demo-poster.webp
video_caption: The video shows real camera footage next to predicted fringe patterns as the load changes. The plot tracks force over time.
detail: sensor.webp
detail_caption: Two cameras view the photoelastic cube through crossed polarizers. The exploded view shows the optical and mechanical components.
---

### PolarTact3D: Single-Shot Tactile 3D Shape and Color Sensing with Polarization Imaging
folder: PolarTact3D
topic: Sensor design and prototyping
name: PolarTact3D
website: https://polartact3d.github.io/
members: Kai Garcia | Mairi Yoshioka | Christian Moore | Tyler Ray | Tianlu Wang | Frances Zhu | Huaijin Chen
short: A polarization camera captures both the 3D shape and color of a contact surface in a single shot.
description: A clear polyethylene film conforms to an object when the sensor is pressed against it. A polarization camera sees the object’s color through the film and records polarization patterns that reveal the surface orientation. The team compared physics-based and neural methods for recovering shape and tested the sensor on surfaces that included transparent and reflective objects. PolarTact3D received the third-place Best Paper Award at the RSS 2025 Workshop on Navigating Contact Dynamics in Robotics.
cover: sensor-pipeline.webp
caption: The sensor design and the steps for reconstructing surface shape from polarization images.
detail: surface-reconstructions.webp
detail_caption: Example contact surfaces reconstructed with the neural and physics-based methods.
field_photo: images/events/rss-2025-polartact3d-poster.webp
field_caption: Kai Garcia presents PolarTact3D at the RSS Workshop on Navigating Contact Dynamics in Robotics on June 25, 2025.
---

### Snapshot Hyperspectral Imaging with Diffractive Optical Elements
folder: DOE-HSI
topic: Sensor design and prototyping
name: Snapshot hyperspectral imaging
selected_work: 2
question: How can a camera capture a spectrum at every pixel in one exposure?
cover: doe-otf-map.png
caption: A diffractive optical element encodes the scene on a monochrome sensor. The diagram shows how the optical measurement and its simulation are used for spectral reconstruction.
summary: Diffractive optics encode wavelength information in one exposure so we can reconstruct the spectrum at each pixel.
detail: doe-psf-grid.png
detail_caption: Reconstructed spectral bands (left) and the corresponding ground-truth bands (right) for the same scene.
lead: Chuanjun Zheng
pi: Huaijin Chen
members: Feimei Chen
short: We design diffractive optical elements for compact, fast, light-efficient hyperspectral cameras that capture spectral information in one exposure.
description: With an optimized diffractive optical element (DOE), different spectral components produce distinct, spatially varying point spread functions on the detector. We can design the element for narrow spectral responses, measured by their full width at half maximum (FWHM). Narrower responses improve spectral resolution and reduce interference between bands. Using one sensor measurement, we can reconstruct the full spectrum at each pixel.
---

### 3PT and 3PTv2 for Robotic Manipulation
folder: 3PT
topic: Perception for robotic manipulation
name: 3PT and 3PTv2
page_layout: brief
short: We developed the 3D-Object Perception Transformer (3PT) with Google Intrinsic. Given a 3D model of a part, 3PT estimates the part’s position and orientation in a color image. Its successor, 3PTv2, can guide a robot as it aligns a charging plug with a vehicle’s port.
website: https://www.intrinsic.ai/publications/3pt-cvpr2026
website_label: Learn more on the Intrinsic website
resources: [3PT paper](publications/#kalra2026_3pt) · [3PTv2 paper](publications/#kalra2026_3ptv2) · [BOP results](https://bop.felk.cvut.cz/leaderboards/pose-detection-unseen-bop24/bop-classic-core/)
members_label: CIRP researchers
members: Agastya Kalra | Huaijin Chen
cover: robot-charging.webp
caption: A robot uses 3PTv2 to locate a charging port and guide a plug into place on three different vehicles.
selected_work: 4
question: How can a robot estimate the pose of an unfamiliar object from a color image?
summary: The 3D-Object Perception Transformer (3PT) and its successor, 3PTv2, use a part’s 3D model to estimate its pose in camera images for tasks such as bin picking and plug insertion.
preview: images/previews/kalra2026_3pt.webp
preview_caption: 3PT estimates the poses of metal parts piled in a bin.
highlight_video_from: kalra2026_3pt
---

### Autonomous Coconut Rhinoceros Beetle Infestation Management
folder: FRC2026
topic: Agricultural robotics
field_photo: images/gallery/palm_capture.jpg
field_caption: Members of the field team observing palms in Hawaiʻi.
name: Field robotics for palm health
preview: images/previews/crb-symposium-demo.webp
preview_fit: cover
caption: The team demonstrates a robotic arm and palm simulation.
gallery_title: Robot development and fieldwork
gallery_caption_frc_2: A team member uses the physical arm to control the simulated arm.
gallery_caption_frc_3: A palm tree and nearby test objects in the simulation.
gallery_caption_team_assembly: The UH Mānoa and University of Michigan teams assemble the palm-climbing robot for the 2026 Farm Robotics Challenge.
gallery_caption_visit_crb_response: A field visit with the CRB Response team and UH Mānoa collaborators Daniel Jenkins and Xing Wei to learn about drone-based beetle control.
summary: We are developing a palm-climbing robot to inspect trees and treat coconut rhinoceros beetle infestations.
lead_label: Perception system lead
lead: Christian Moore
advisors: Huaijin Chen | [Daniel Jenkins](https://www.ctahr.hawaii.edu/site/Bio.aspx?ID=JENKIDAN) | [Ryan Kurasaki](https://www.ctahr.hawaii.edu/site/Bio.aspx?ID=KURASRYA) | [Tianlu Wang](https://sites.google.com/view/uhm-sail/people) | [Daniel Drew](https://danieldrew.me/) | [Xiaonan (Sean) Huang](https://soft.robotics.umich.edu/team/)
members_label: University of Hawaiʻi at Mānoa team
members: Rona Lei Duldulao | Lucas Horsman | Wilson Huynh | Erik Bendickson | Christian Komo | Zadon Padello | Tyler Mak | Elijah Saloma | Kanta Saito | Ella Self | Andrew He | Lukas Moroz | Riki MacMillan | Alex Tokunaga | Owen Bramley
collaborators_label: University of Michigan team
collaborators: Nilay Choudhury | Xinqi Zhang | Yuchen You | Haobo Fang | Siyuan Zheng | Ronen Dujovny | Adrian Wang | Mingxuan He
short: A palm-climbing robot designed to inspect trees and treat coconut rhinoceros beetle infestations.
description: The team is developing a mechanism to climb palms and an end effector to apply pesticides and trim flowers. They use simulation and teleoperated trials to study how the arm interacts with a tree before hardware tests. We thank NVIDIA for supporting this work on palm health for the 2026 Farm Robotics Challenge.
---

### Pineapple Counting and Sizing with Aerial and Ground Robots
folder: FRC2025
topic: Agricultural robotics
short: Team ʻĀina paired a drone that counts pineapples with a ground robot that measures fruit size at Dole Plantation.
description: The UH Mānoa undergraduate team used aerial images to count pineapples across a field and rover footage to reconstruct individual fruit in 3D. The system won the $10,000 Excellence in Productivity (Air) award at the 2025 Farm Robotics Challenge. We thank NVIDIA for supporting Team ʻĀina’s pineapple mapping project.
website: https://www.hawaii.edu/news/2025/05/13/farm-robotics-challenge-2025-winner/
cover: pineapple-field-rover.jpg
caption: Team ʻĀina prepares its rover to survey pineapples at Dole Plantation. Photo from UH News.
gallery_title: Fieldwork and presentations
gallery_caption_adjusting_the_rover: Team members adjust the rover’s frame to clear the pineapple leaves. Photo from UH News.
gallery_caption_surveying_pineapple_rows: The rover travels between pineapple rows to collect images of individual fruit. Photo from UH News.
gallery_caption_team_aina: Team ʻĀina with the survey drone and ground robot. Photo from UH News.
gallery_caption_summit_presentation: Christian Komo presents Team ʻĀina’s pineapple mapping system at the Plug and Play Summit.
preview_fit: cover
supplement: frc2025.html
lead: Christian Komo
advisors_label: Faculty advising team lead
advisors: Huaijin Chen
members: Kai Garcia | Mikhail Shkaralevich | Tyler Mak | Rona Lei Duldulao | Lucas Horsman | Zadon Padello | Wilson Huynh | Erik Bendickson
---

### FishEye: Robust 3D Fish Measurement from Single Image or Video
folder: FishEye
topic: Marine robotics and perception
name: FishEye
related: FishPod
lead: Ethan Chung
pi: Huaijin Chen
members: Vincent Chan
short: We’re developing a low-cost way to estimate a fish’s length and volume from a photo or video.
description: FishEye uses deep learning to detect and segment fish in photos or videos from ordinary cameras, including smartphones. It uses transformer-based camera calibration and depth estimation to reconstruct each fish in 3D and estimate its length. A ping-pong ball can serve as a scale reference. We’re developing FishEye for field measurements in fisheries, ecological research, and aquaculture.
caption: FishEye detects the fish, estimates depth, and reconstructs its body in 3D for measurement.
---

### FishPod: Underwater Stereo Vision for Fish Measurement
folder: FishPod
topic: Marine robotics and perception
name: FishPod
related: FishEye
pi: Huaijin Chen
members: Feimei Chen | Riki MacMillan | Munir Zarea
short: FishPod uses a stereo camera mounted on a remotely operated underwater vehicle to estimate fish length from paired video frames.
description: The system detects and tracks fish, segments their outlines, and matches points along their body axes between the two camera views. Stereo triangulation locates the endpoints in 3D so the system can estimate body length.
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
topic: Human–robot interaction
name: Robot–tablet interaction in older adults
lead: Yang Qian
pi: Huaijin Chen
members: Christian Moore | Ethan Chung | Sean Hiroki Flynn | Riki MacMillan
short: We use a robot and tablet in brief, standardized sessions with older adults to measure behavioral markers of cognitive concern that are difficult to capture with paper-based, tablet-only, or static voice-based screening.
description: A humanoid robot introduces each task, directs the participant’s attention, and responds as the conversation unfolds. The tablet records answers, drawings, taps, and response times. We study these records alongside speech and movement to see how cognitive concerns relate to a participant’s responses. The study does not provide a clinical diagnosis of mild cognitive impairment (MCI).
caption: The humanoid robot introduces the tasks, and the tablet records participants’ responses.
gallery_caption_cube_task_active_2026_04_14: The tablet shows the numbered and lettered circles used in the sequencing task.
gallery_caption_cube_task_briefing_2026_04_14: The briefing shows participants how to connect the circles in order.
gallery_caption_task2_animals_demo_2026_04_14: The instructions introduce the animal-naming task and show the pictures participants will see.
---

## Physics-Informed AI for Scientific Instrumentation

### Physics-Informed Machine Learning for Accelerated Discovery and Dynamics Analysis in Ultrafast X-Ray Diffraction
folder: XRD-ML
topic: Predicting instrument response
name: Learning ultrafast X-ray dynamics
lead: Ethan Chung
pi: Huaijin Chen
members: Vincent Chan
short: We use simulated atomic motion to predict how X-ray scattering changes over time, then compare those predictions with experimental measurements.
description: Ultrafast X-ray photon correlation spectroscopy (XPCS) tracks how materials change over time, from atomic to microscopic scales. We train models on simulated atomic motion to predict the temporal correlation functions measured in XPCS experiments. That gives us a way to test simulations against measurements of supercooled liquids and materials undergoing the glass transition.
caption: Simulated argon structures at different densities and temperatures.
---

### ML-Driven Surrogate Modeling for FEL Oscillator Cavity Optimization
folder: FEL-Oscillator
topic: Predicting instrument response
name: Modeling free-electron lasers
lead: Ethan Chung
pi: Huaijin Chen
members:
short: We build surrogate models to speed up simulations of free-electron laser oscillators and help researchers tune the laser cavity.
description: Testing a range of cavity designs in a simulator such as GINGER can take considerable computing time. We’re training models to predict how changes in mirror spacing and cavity length affect the electron beam energy and the radiation it produces. If the models can replace some full simulation sweeps, researchers could compare designs faster and tune the laser’s gain, stability, and spectrum in real time.
caption: A free-electron laser oscillator showing the electron source, accelerator, undulator, and cavity mirrors.
---

### ImagingBench: Can AI Solve Imaging Problems?
folder: CIBench
topic: Evaluating frontier models for imaging applications
name: ImagingBench
selected_work: 3
slug: imagingbench
website: https://cirplab-fourier.taildc92d1.ts.net/
website_label: Learn more on the ImagingBench website
page_layout: brief
lead: Ethan Chung
pi: Huaijin Chen
members: Chuanjun Zheng | Jasper Tan | Jingxi Li
short: ImagingBench evaluates frontier multimodal AI models on 22 tasks, from predicting what a camera will record to reconstructing a scene from sensor measurements.
question: What have frontier multimodal AI models learned about image formation?
preview: images/previews/imagingbench-expert.png
preview_caption: Under the ImagingBench Expert protocol, Gemini-3.1-Flash-Image scored 61.4 out of 100, followed by GPT-Image-2 (57.3), FLUX.2-Pro (56.6), GPT-Image-1.5 (50.2), Qwen-Image-Edit-2511 (42.7), and HunyuanImage-3.0 (26.5).
summary: ImagingBench tests six models on 22 computational imaging tasks, including reconstructing scenes from lensless measurements and predicting what a sensor would record.
cover: benchmark.webp
caption: ImagingBench task families and model comparisons.
---

### Satellite-Derived Shorelines
folder: SDS
topic: Evaluating frontier models for imaging applications
name: Satellite-derived shorelines
lead: Joel Nicolow
pi: Dr. Charles Fletcher
members:
short: We compare shorelines estimated from satellite images with reference shorelines to test how well mapping methods transfer from one coast to another.
description: Field and aerial surveys are costly, and a method that detects the shoreline on one coast can miss it on another. We use hand-labeled satellite images and reference shorelines from Hawaiʻi and elsewhere to compare geospatial foundation models, other pretrained vision models, lightweight neural networks, and traditional thresholding methods. We’re building a common benchmark and open-source mapping tools for researchers, coastal managers, and communities.
caption: The map shows where Hawaiʻi’s shorelines advanced or retreated over five years.
gallery_caption_sds_shorelines_superimposed_on_drone_image: Shorelines derived from satellite imagery overlaid on a drone photo.
gallery_caption_sandies_sds_example_and_transect_intersections: Examples of shoreline detection and intersections with coastal transects.
gallery_caption_sat_image_examples: The same coastline seen by different satellite sensors.
gallery_caption_segmentation_method_comparison: Comparison of land and water segmentation methods on the same stretch of coast.
---
