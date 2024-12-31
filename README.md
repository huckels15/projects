# Projects for 17D Application

Hello Sir/Ma'am, thank you for taking the time to look at my programming portfolio. Contained in this Github repository are some of the most interesting projects I have worked on over the years. In this top-level README, there are high-level descriptions of each of the projects inside the repo.

## `/adversarial_playground`
The `adversarial_playground` subdirectory contains the Adversarial Playground application myself and two others built for our capstone project in Advanced Practical Data Science at Harvard University. The Adversarial Playground app was hosted on Google Cloud Platform and allowed users to launch four different model evasion attacks on road sign classification models, skin cancer classification models, or a custom model the user uploads.

## `/computer_arch_finalproj`
The `/computer_arch_finalproj` contains my solution for the final project in Computer Organization at West Point. This project made use of the C programming language, parallelism, and hashing to parse a large dataset containing network probes. According to Dr. Matthews, my solution had the fastest runtime for our year group.

## `/Holdem`
The `/Holdem` directory contains myself and another cadet's final project for Software Testing and Development at West Point. Holdem is a simple Scala app that simulates a game of Texas Holdem poker using a Scala Swing GUI and backend using a MVC architecture.

## `/sandboxing`
The `/sandboxing` directory contains my solution for a project from Systems Security at Harvard University. The sandbox is implemented in the C programming language using `ptrace` and restricts the execution of a python script. The sandbox uses pid namespacing, forces the process to execute under a non-privileged uid, restricts forking, and prevents `connect()` sys calls.

## `/TinyML_robustness_analysis`
The `/TinyML_robustness_analysis` directory contains the code for my ongoing thesis project at Harvard University "Practical Attacks on Tiny Intelligence: Analyzing the Effects of Model Extraction and Transferability on Tiny Machine Learning Models". This project aims to investigate the effects of model extraction attacks and model evasion attacks on Tiny Machine Learning models. Specifically, this project looks at a two-step attack chain where the attacker first extracts a functionally equivalent victim model using either Copycat CNN or Knockoff Nets and then attacks the target model using adversarial examples generated on the functionally equivalent model. A schematic of the project can be found in that directory's README. 
