## Estimation of muscle torques from EMG and kinematics during planar arm movements (2018)
_Nicola Lotti and Vittorio Sanguinetti_

The dataset used in this project comes from the following cited experiment conducted by Lotti and Sanguinetti.
The experiment involves a myoprocessor model which is capable of predicting the muscle forces during planar arm
movements in real time. They reported a two-step parameter estimation procedure which involves both isometric force
generation and actual movements. For what concerns our project we are interested in the isometric force prediction.

Their approach to isometric force estimation is a polynomial model of muscle geometry that gave some reliable 
results. Since we don't have the knowledge required to work with such models we took from this paper only the part
of preprocessing the EMG signals as our guideline and the experiment explanation to understand the nature of the dataset.

## Hand grip force estimation via EMG imaging (2022) DOI:10.1016/j.bspc.2022.103550

The study introduces a framework for estimating hand grip force using surface electromyography (sEMG) signals, addressing the need for standardized muscle health assessments through a novel approach.
A lightweight, low-cost eight-channel EMG measurement system was employed, with eight Myoware EMG sensors placed around the forearm to capture electrical activity from primary muscles, while a force-sensing resistor (FSR) measured grip force during contractions.
Data was collected from seven healthy male subjects, with sEMG signals recorded in overlapping segments, and the mean absolute voltage (MAV) was extracted and normalized to establish a logarithmic relationship with grip force.
The relationship between EMG features and grip force was modeled using ordinary least squares regression, and a pairwise voltage difference method was adapted from Electrical Impedance Tomography (EIT) to generate images representing muscle activation patterns.
Additionally, a Vision Transformer (ViT) network was implemented to enhance force estimation from the reconstructed images, demonstrating the potential of combining traditional signal processing with advanced machine learning techniques for reliable muscle health assessment.