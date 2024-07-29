# Quantitative SLAM Evaluation
## Abstract

This letter addresses the challenge of evaluating Simultaneous Localization and Mapping (SLAM) algorithms, highlighting the limitations of existing assessment tools that often lead to over-tuned and less generalized solutions. We introduce a novel Monte Carlo evaluation tool developed in the Gazebo simulation environment using the ROS framework. This tool enables empirical performance assessment of SLAM algorithms with statistical guarantees, simulating diverse scenarios, including sensor failures and model mismatches. The system, application, and sensor agnostic, evaluates SLAM performance using noisy data from a 3D vehicle model equipped with a diverse sensor suite in a replicated real-world environment.

For this study, we used both conventional and proposed methods to evaluate two LiDAR-Inertial SLAM algorithms, Fast-LIO 2 and LIO-SAM, using datasets from a maritime domain. The proposed method demonstrated superior versatility and robustness in assessing SLAM performance.

