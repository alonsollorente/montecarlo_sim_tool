# wt_sim
## Abstract

This master thesis addresses the challenge of evaluating Simultaneous Localization and Mapping (SLAM) algorithms, particularly for niche applications such as Inland Waterway Transport (IWT). Existing tools and methods for performance assessment of SLAM solutions are often inadequate, typically relying on empirical analysis against common datasets, which can lead to over-tuned and less generalizable solutions.

To overcome this, the thesis introduces a novel Monte Carlo evaluation tool developed in the Gazebo simulation environment using the ROS framework. This tool allows for the empirical performance assessment of SLAM algorithms with statistical guarantees and control over various scenarios, including potential breakdown situations such as stochastic model mismatches or sensor failures. The setup emulates a diverse sensor suite on a 3D model of a vehicle within a replicated real-world environment.

The evaluation system involves configuring the vehicle and sensor setup, executing predefined trajectories, and collecting noisy data along with ground truth. This dataset is then used to evaluate the performance of SLAM methods. The outputs undergo comprehensive statistical analysis to assess robustness and effectiveness.

Specifically for this thesis, the AURORA vessel served as the primary experimental setup. AURORA is a research vessel equipped with a sophisticated array of sensors, including multiple LIDARs, IMUs, and cameras. The vessel was used to navigate the urban canals of Berlin, providing a realistic and challenging environment for SLAM evaluation. The recorded data from these experiments, along with the simulated scenarios in Gazebo—adapted to match the urban canals of Berlin and AURORA's sensory setup—offered a comprehensive dataset for assessing the performance of two LIDAR-Inertial SLAM solutions: Fast-LIO 2 and LIO-SAM. The real-world measurements were crucial in validating the simulation results and ensuring the robustness of the evaluated SLAM methods.

The methodology is application and sensor agnostic, making it a versatile tool for researchers in various transport applications.
