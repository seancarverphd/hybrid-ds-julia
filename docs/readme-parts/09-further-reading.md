## Further reading

This section is organized to mirror the mathematical, computational, application, and limitation sections of this README. It is intentionally a curated starting point rather than a comprehensive bibliography. Readers should consult original papers, authoritative guidelines, maintained software documentation, and domain experts before relying on a model for scientific, engineering, clinical, or operational decisions.

### Hybrid-systems foundations, events, and sensitivity analysis

#### Hybrid transitions, saltation matrices, and event-aware derivatives

- Goebel, R., Sanfelice, R. G., and Teel, A. R. (2012). *Hybrid Dynamical Systems: Modeling, Stability, and Robustness*. Princeton University Press.

- di Bernardo, M., Budd, C. J., Champneys, A. R., and Kowalczyk, P. (2008). *Piecewise-Smooth Dynamical Systems: Theory and Applications*. Springer.

- Kong, N. J., Payne, J. J., Zhu, J., and Johnson, A. M. (2024). Saltation matrices: The essential tool for linearizing hybrid dynamical systems. *Proceedings of the IEEE*, 112(2), 161–196.

- Saccon, A., van de Wouw, N., and Nijmeijer, H. (2014). Sensitivity analysis of hybrid systems with state jumps with application to trajectory tracking. *Proceedings of the IEEE Conference on Decision and Control*.

- Galvanetto, U., and Magri, L. (2020). Modeling and sensitivity analysis methodology for hybrid dynamical systems. *Journal of Computational and Nonlinear Dynamics*, 15(2).

#### Multiple shooting, optimization, and parallel simulation

- Bock, H. G., and Plitt, K. J. (1984). A multiple shooting algorithm for direct solution of optimal control problems. *Proceedings of the IFAC World Congress*.

- Diehl, M., Bock, H. G., Diedam, H., and Wieber, P.-B. (2006). Fast direct multiple shooting algorithms for optimal robot control. In *Fast Motions in Biomechanics and Robotics*.

- Betts, J. T. (2010). *Practical Methods for Optimal Control and Estimation Using Nonlinear Programming* (2nd ed.). SIAM.

- Rackauckas, C., and Nie, Q. (2017). DifferentialEquations.jl—A performant and feature-rich ecosystem for solving differential equations in Julia. *Journal of Open Research Software*, 5(1), 15.

- Rackauckas, C., Ma, Y., Dixit, V., et al. (2020). Universal differential equations for scientific machine learning. *arXiv:2001.04385*.

- SciML. SciMLSensitivity.jl documentation: sensitivity algorithms for differential equations, including hybrid equations with events and callbacks. Consult the versioned documentation matching the installed package.

- SciML. DifferentialEquations.jl and SciMLBase ensemble-simulation documentation. Consult the versioned documentation matching the installed package.

### Pharmaceutical development and translational medicine

#### Tuberculosis and HIV

- Perelson, A. S., Neumann, A. U., Markowitz, M., Leonard, J. M., and Ho, D. D. (1996). HIV-1 dynamics in vivo: Virion clearance rate, infected cell life-span, and viral generation time. *Science*, 271(5255), 1582–1586.

- Rong, L., and Perelson, A. S. (2009). Modeling HIV persistence, the latent reservoir, and viral blips. *Journal of Theoretical Biology*, 260(2), 308–331.

- Hill, A. L., Rosenbloom, D. I. S., Fu, F., Nowak, M. A., and Siliciano, R. F. (2014). Predicting the outcomes of treatment to eradicate the latent reservoir for HIV-1. *Proceedings of the National Academy of Sciences*, 111(37), 13475–13480.

- World Health Organization. Consolidated guidelines on the use of antiretroviral drugs for treating and preventing HIV infection. Consult the current edition and associated viral-load-monitoring guidance.

- World Health Organization. Consolidated guidelines on tuberculosis: Module 4: Treatment. Consult the current edition and regimen-specific updates.

- Shibata, M., et al. (2024). Pharmacokinetic–pharmacodynamic modeling of tuberculosis time-to-positivity and colony-forming-unit data to compare linezolid dosing regimens. *Antimicrobial Agents and Chemotherapy*.

#### Oncology and adaptive cancer therapy

- Gatenby, R. A., Silva, A. S., Gillies, R. J., and Frieden, B. R. (2009). Adaptive therapy. *Cancer Research*, 69(11), 4894–4903.

- Zhang, J., Cunningham, J. J., Brown, J. S., and Gatenby, R. A. (2017). Integrating evolutionary dynamics into treatment of metastatic castrate-resistant prostate cancer. *Nature Communications*, 8, 1816.

- West, J. B., et al. (2020). A survey of open questions in adaptive therapy: Bridging mathematics and clinical translation. *eLife*, 9, e84263.

- Enriquez-Navas, P. M., et al. (2016). Exploiting evolutionary principles to prolong tumor control in preclinical models of breast cancer. *Science Translational Medicine*, 8(327), 327ra24.

- Anderson, A. R. A., Quaranta, V., and collaborators. Mathematical oncology reviews and primary studies on tumor ecology, resistance, and treatment scheduling. Consult indication-specific literature.

#### Immunology, inflammation, and autoimmune disease

- Eftimie, R., Bramson, J. L., and Earn, D. J. D. (2011). Interactions between the immune system and cancer: A brief review of non-spatial mathematical models. *Bulletin of Mathematical Biology*, 73, 2–32.

- Iwami, S., Takeuchi, Y., and others. Mathematical models of autoimmune-disease dynamics, tolerance, flare-up, and dormancy. Consult disease-specific primary literature.

- Kuhlmann, T., et al. (2024). Mathematical modeling in autoimmune diseases: A review of onset, progression, and treatment-effect models. *Frontiers in Immunology*.

- Germain, R. N. (2012). Maintaining system homeostasis: The third law of Newtonian immunology. *Nature Immunology*, 13, 902–906.

- Consult disease-specific guidance, mechanistic studies, and pharmacometric literature for the intended autoimmune or inflammatory indication.

#### PK/PD and quantitative systems pharmacology

- Mager, D. E., and Jusko, W. J. (2001). General pharmacokinetic model for drugs exhibiting target-mediated drug disposition. *Journal of Pharmacokinetics and Pharmacodynamics*, 28, 507–532.

- Danhof, M., de Jongh, J., De Lange, E. C. M., Della Pasqua, O., Ploeger, B. A., and Voskuyl, R. A. (2007). Mechanism-based pharmacokinetic-pharmacodynamic modeling: Biophase distribution, receptor theory, and dynamical systems analysis. *Annual Review of Pharmacology and Toxicology*, 47, 357–400.

- Marshall, S. F., Burghaus, R., Cosson, V. F., et al. (2016). Good practices in model-informed drug discovery and development: Practice, application, and documentation. *CPT: Pharmacometrics & Systems Pharmacology*, 5, 93–122.

- Sorger, P. K., et al. (2011). Quantitative and systems pharmacology in the post-genomic era: New approaches to discovering drugs and understanding therapeutic mechanisms. *NIH White Paper*.

- U.S. Food and Drug Administration. Model-informed drug development and population pharmacokinetic guidance and related regulatory materials. Consult current guidance.

### Clinical operations and treatment delivery

#### Dose scheduling, adherence, and therapeutic monitoring

- Sheiner, L. B., and Steimer, J.-L. (2000). Pharmacokinetic/pharmacodynamic modeling in drug development. *Annual Review of Pharmacology and Toxicology*, 40, 67–95.

- Mould, D. R., and Upton, R. N. (2012). Basic concepts in population modeling, simulation, and model-based drug development. *CPT: Pharmacometrics & Systems Pharmacology*, 1, e6.

- Kang, J. S., and Lee, M. H. (2009). Overview of therapeutic drug monitoring. *The Korean Journal of Internal Medicine*, 24(1), 1–10.

- Nieuwlaat, R., et al. (2014). Interventions for enhancing medication adherence. *Cochrane Database of Systematic Reviews*.

#### Hospital, critical care, and digital health

- Clermont, G., Angus, D. C., DiRusso, S. M., Griffin, M., and Linde-Zwirble, W. T. (2004). Predicting hospital mortality for patients in the intensive care unit: A comparison of artificial neural networks with logistic regression models. *Critical Care Medicine*, 29, 291–296.

- Heldt, T., et al. Physiological modeling, monitoring, and control literature for intensive-care and clinical decision-support systems. Consult condition-specific literature.

- Behar, J. A., et al. (2018). Remote health monitoring and wearable physiological sensing: Methods and applications. Consult current reviews and validation studies.

- U.S. Food and Drug Administration. Clinical decision support software and software-as-a-medical-device guidance. Consult current guidance.

### Biomanufacturing and industrial biotechnology

#### Batch, fed-batch, and continuous bioprocesses

- Nielsen, J., Villadsen, J., and Lidén, G. (2017). *Bioreaction Engineering Principles* (3rd ed.). Springer.

- Villadsen, J., Nielsen, J., and Lidén, G. (2011). *Bioreaction Engineering Principles* (3rd ed.). Springer.

- Banga, J. R., Balsa-Canto, E., Moles, C. G., and Alonso, A. A. (2003). Improving food processing using modern optimization methods. *Trends in Food Science & Technology*, 14, 131–144.

- Smets, I. Y., et al. (2004). Optimal control of a fed-batch fermentation process. *Journal of Process Control*, 14, 379–386.

- Tebbani, S., and colleagues. Optimal switching control of fed-batch fermentation processes. Consult primary literature for the intended organism and product.

#### Quality control, maintenance, and process transitions

- Isermann, R. (2006). *Fault-Diagnosis Systems: An Introduction from Fault Detection to Fault Tolerance*. Springer.

- Jardine, A. K. S., Lin, D., and Banjevic, D. (2006). A review on machinery diagnostics and prognostics implementing condition-based maintenance. *Mechanical Systems and Signal Processing*, 20(7), 1483–1510.

- Qin, S. J. (2012). Survey on data-driven industrial process monitoring and diagnosis. *Annual Reviews in Control*, 36(2), 220–234.

### Energy systems and power grids

#### Storage, demand response, faults, and restoration

- Kundur, P. (1994). *Power System Stability and Control*. McGraw-Hill.

- Sauer, P. W., and Pai, M. A. (1998). *Power System Dynamics and Stability*. Prentice Hall.

- Hiskens, I. A., and Pai, M. A. (2000). Trajectory sensitivity analysis of hybrid systems. *IEEE Transactions on Circuits and Systems I*, 47(2), 204–220.

- Milano, F. (2010). *Power System Modelling and Scripting*. Springer.

- DIgSILENT GmbH. PowerFactory documentation. Consult current documentation for dynamic simulation, events, protection, and Modelica/FMI interoperability.

- PSCAD, EMTP-RV, PSS®E, and related power-system simulation documentation. Consult the tool appropriate to the intended study.

### Supply chains, logistics, and operations

#### Inventory, routing, production, and maintenance

- Simchi-Levi, D., Kaminsky, P., and Simchi-Levi, E. (2008). *Designing and Managing the Supply Chain* (3rd ed.). McGraw-Hill.

- Bertazzi, L., and Speranza, M. G. (2012). Inventory routing problems: An introduction. *EURO Journal on Transportation and Logistics*, 1, 307–326.

- Kleywegt, A. J., Nori, V. S., and Savelsbergh, M. W. P. (2002). The stochastic inventory routing problem with direct deliveries. *Transportation Science*, 36(1), 94–118.

- Pinedo, M. (2022). *Scheduling: Theory, Algorithms, and Systems* (6th ed.). Springer.

- Dekker, R. (1996). Applications of maintenance optimization models: A review and analysis. *Reliability Engineering & System Safety*, 51(3), 229–240.

### Ecosystems, agriculture, and environmental management

#### Crop growth, irrigation, and pest management

- Jones, J. W., et al. (2003). The DSSAT cropping system model. *European Journal of Agronomy*, 18, 235–265.

- Holzworth, D. P., et al. (2014). APSIM—Evolution towards a new generation of agricultural systems simulation. *Environmental Modelling & Software*, 62, 327–350.

- Steduto, P., Hsiao, T. C., Raes, D., and Fereres, E. (2009). *AquaCrop—The FAO Crop Model to Simulate Yield Response to Water*. FAO.

- Chaves, M. M., et al. (2010). Deficit irrigation and partial root zone drying: A review. *Journal of Experimental Botany*, 61(7), 1965–1975.

- Consult integrated pest-management, crop-model, hydrology, and agricultural-extension literature for the intended crop, region, and intervention.

#### Fisheries, wildlife, and invasive-species control

- Clark, C. W. (2010). *Mathematical Bioeconomics: The Mathematics of Conservation* (3rd ed.). Wiley.

- Hilborn, R., and Walters, C. J. (1992). *Quantitative Fisheries Stock Assessment*. Chapman and Hall.

- Lenhart, S., and Workman, J. T. (2007). *Optimal Control Applied to Biological Models*. Chapman and Hall/CRC.

- Impulsive differential-equation and seasonal-harvest literature for fishery, wildlife, and invasive-species management. Consult species-specific primary research.

#### Water, land, and climate-adaptation systems

- Loucks, D. P., and van Beek, E. (2017). *Water Resource Systems Planning and Management* (2nd ed.). Springer.

- Yeh, W. W.-G. (1985). Reservoir management and operations models: A state-of-the-art review. *Water Resources Research*, 21(12), 1797–1818.

- IPCC. Assessment Reports and Working Group reports on impacts, adaptation, and vulnerability. Consult the current assessment cycle.

- Consult region-specific hydrologic, groundwater, flood-risk, and climate-adaptation literature for operational applications.

### Infrastructure, robotics, and engineered systems

#### Buildings, HVAC, and thermal management

- Wetter, M. (2011). Co-simulation of building energy and control systems with the Building Controls Virtual Test Bed. *Journal of Building Performance Simulation*, 4(3), 185–203.

- Aswani, A., Master, N., Taneja, J., Krioukov, A., Culler, D., and Tomlin, C. (2012). Energy-efficient building HVAC control using hybrid system LBMPC. *arXiv:1204.4717*.

- Afram, A., and Janabi-Sharifi, F. (2014). Theory and applications of HVAC control systems—A review of model predictive control. *Building and Environment*, 72, 343–355.

- EnergyPlus documentation and Modelica Buildings Library documentation. Consult current versions for detailed building-energy simulation.

#### Transportation and autonomous systems

- Rajamani, R. (2012). *Vehicle Dynamics and Control* (2nd ed.). Springer.

- Paden, B., Čáp, M., Yong, S. Z., Yershov, D., and Frazzoli, E. (2016). A survey of motion planning and control techniques for self-driving urban vehicles. *IEEE Transactions on Intelligent Vehicles*, 1(1), 33–55.

- Althoff, M., and Dolan, J. M. (2014). Online verification of automated road vehicles using reachability analysis. *IEEE Transactions on Robotics*, 30(4), 903–918.

- Consult current formal-verification, simulation, traffic-control, and vehicle-platform literature for the intended application.

#### Robotics, contact mechanics, and fault management

- Henzinger, T. A. (1996). The theory of hybrid automata. In *Proceedings of the 11th Annual IEEE Symposium on Logic in Computer Science*.

- Tedrake, R. (2023). *Underactuated Robotics: Algorithms for Walking, Running, Swimming, Flying, and Manipulation*. Online textbook and course notes.

- Manchester, I. R., and Slotine, J.-J. E. (2017). Control contraction metrics: Convex and intrinsic criteria for nonlinear feedback design. *IEEE Transactions on Automatic Control*, 62(6), 3046–3053.

- Drake documentation. Consult current documentation for `MultibodyPlant`, joints, actuators, force elements, springs, compliant contact, hydroelastic contact, and contact-model choices.

- Isermann, R. (2006). *Fault-Diagnosis Systems: An Introduction from Fault Detection to Fault Tolerance*. Springer.

#### Postural control, locomotion, and sensorimotor behavior

- Grizzle, J. W., Abba, G., and Plestan, F. (2001). Asymptotically stable walking for biped robots: Analysis via systems with impulse effects. *IEEE Transactions on Automatic Control*, 46(1), 51–64.

- Westervelt, E. R., Grizzle, J. W., Chevallereau, C., Choi, J. H., and Morris, B. (2007). *Feedback Control of Dynamic Bipedal Robot Locomotion*. CRC Press.

- Burden, S. A., Revzen, S., and Sastry, S. S. (2015). Model reduction near periodic orbits of hybrid dynamical systems. *IEEE Transactions on Automatic Control*, 60(10), 2626–2639.

- Blickhan, R. (1989). The spring-mass model for running and hopping. *Journal of Biomechanics*, 22(11–12), 1217–1227.

- Holmes, P., Full, R. J., Koditschek, D., and Guckenheimer, J. (2006). The dynamics of legged locomotion: Models, analyses, and challenges. *SIAM Review*, 48(2), 207–304.

### Specific labs and authors

#### Jeka and Kiemel: postural control, multisensory integration, and locomotion

- Jeka, J. J., Kiemel, T., Creath, R., Horak, F., and Peterka, R. J. (2004). Controlling human upright posture: Velocity information is more accurate than position or acceleration. *Journal of Neurophysiology*, 92(4), 2368–2379.

- Kiemel, T., Oie, K. S., and Jeka, J. J. (2002). Multisensory fusion and the stochastic structure of postural sway. *Biological Cybernetics*, 87, 262–277.

- Creath, R., Kiemel, T., Horak, F., and Jeka, J. J. (2008). The role of vestibular and somatosensory systems in intersegmental dynamics during stance. *Experimental Brain Research*, 183, 509–517.

- Hsu, W.-L., Scholz, J. P., Schöner, G., Jeka, J. J., and Kiemel, T. (2007). Control and estimation of posture during quiet stance depends on multijoint coordination. *Journal of Neurophysiology*, 97(4), 3024–3035.

- Kiemel, T., Elahi, A. J., and Jeka, J. J. (2008). Identification of the plant for upright stance in humans: Multiple movement patterns from a single neural strategy. *Journal of Neurophysiology*, 100, 3394–3406.

- Logan, D., Kiemel, T., and Jeka, J. J. (2016). Using a system identification approach to investigate subtask control during human locomotion. *Frontiers in Computational Neuroscience*, 10, 146.

#### Ahrens Lab: zebrafish sensorimotor behavior and whole-brain dynamics

- Ahrens, M. B., Li, J. M., Orger, M. B., Robson, D. N., Schier, A. F., Engert, F., and Portugues, R. (2012). Brain-wide neuronal dynamics during motor adaptation in zebrafish. *Nature*, 485, 471–477.

- Chen, X., Mu, Y., Hu, Y., Kuan, A. T., Nikitchenko, M., Randlett, O., Chen, A. B., Gavornik, J. P., Sompolinsky, H., Engert, F., and Ahrens, M. B. (2018). Brain-wide organization of neuronal activity and convergent sensorimotor transformations in larval zebrafish. *Neuron*, 100, 876–890.e5.

- Mu, Y., Bennett, D. V., Rubinov, M., Narayan, S., Yang, C.-T., Tanimoto, M., Mensh, B. D., Looger, L. L., and Ahrens, M. B. (2019). Glia accumulate evidence that actions are futile and suppress unsuccessful behavior. *Cell*, 178, 27–43.e19.

- Yang, E., Zwart, M. F., James, B., Rubinov, M., Wei, Z., Narayan, S., Vladimirov, N., Mensh, B. D., Fitzgerald, J. E., and Ahrens, M. B. (2022). A brainstem integrator for self-location memory and positional homeostasis in zebrafish. *Cell*, 185, 5011–5027.e20.

- Ahrens Lab, HHMI Janelia Research Campus. Laboratory website, publications, and public datasets. Consult current laboratory materials.

#### Cowan and the LIMBS Laboratory: mechanics, active sensing, and system identification

- Cowan, N. J., and Fortune, E. S. (2007). The critical role of locomotion mechanics in decoding sensory systems. *Journal of Neuroscience*, 27(5), 1123–1128.

- Sefati, S., Neveln, I. D., Roth, E., Mitchell, T. R. T., Snyder, J. B., MacIver, M. A., Fortune, E. S., and Cowan, N. J. (2013). Mutually opposing forces during locomotion can eliminate the tradeoff between maneuverability and stability. *Proceedings of the National Academy of Sciences*, 110(47), 18798–18803.

- Cowan, N. J., Ankarali, M. M., Dyhr, J. P., Madhav, M. S., Roth, E., Sefati, S., Sponberg, S., Stamper, S. A., Fortune, E. S., and Daniel, T. L. (2014). Feedback control as a framework for understanding tradeoffs in biology. *Integrative and Comparative Biology*, 54(2), 223–237.

- LIMBS Laboratory, Johns Hopkins University. Research materials and publication list. Consult current laboratory materials.

#### Fortune: weakly electric fish, active sensing, and feedback control

- Cowan, N. J., and Fortune, E. S. (2007). The critical role of locomotion mechanics in decoding sensory systems. *Journal of Neuroscience*, 27(5), 1123–1128.

- Roth, E., Zhuang, K., Stamper, S. A., Fortune, E. S., and Cowan, N. J. (2011). Stimulus predictability mediates a switch in locomotor smooth-pursuit performance for *Eigenmannia virescens*. *Journal of Experimental Biology*, 214, 1170–1180.

- Madhav, M. S., Stamper, S. A., Fortune, E. S., and Cowan, N. J. (2013). Closed-loop stabilization of the jamming avoidance response reveals its locally unstable and globally nonlinear dynamics. *Journal of Experimental Biology*, 216, 4272–4284.

- Yang, Y., Yared, D. G., Fortune, E. S., and Cowan, N. J. (2024). Sensorimotor adaptation to destabilizing dynamics in weakly electric fish. *Current Biology*.

- Fortune, E. S. and collaborators. Primary research on locomotion, active sensing, sensory feedback, and behavioral variability in weakly electric fish. Consult current publication lists.

#### Hines and the NEURON ecosystem: neural and network simulation

- Hines, M. L., and Carnevale, N. T. (1997). The NEURON simulation environment. *Neural Computation*, 9(6), 1179–1209.

- Hines, M. L., and Carnevale, N. T. (2001). NEURON: A tool for neuroscientists. *The Neuroscientist*, 7(2), 123–135.

- Hines, M. L., and Carnevale, N. T. (2004). Discrete event simulation in the NEURON environment. *Neurocomputing*, 58–60, 1117–1122.

- Migliore, M., Cannia, C., Lytton, W. W., Markram, H., and Hines, M. L. (2006). Parallel network simulations with NEURON. *Journal of Computational Neuroscience*, 21, 119–129.

- Hines, M. L., Davison, A. P., and Muller, E. (2009). NEURON and Python. *Frontiers in Neuroinformatics*, 3, 1.

- Carnevale, N. T., and Hines, M. L. (2006). *The NEURON Book*. Cambridge University Press.

- NEURON and CoreNEURON documentation; ModelDB. Consult current documentation and model repositories.

### Domains where mechanistic hybrid modeling is more limited

The following readings are included to support careful treatment of causal identification, diagnostic uncertainty, symptom heterogeneity, alternative explanations, comorbidity, treatment-selection confounding, and appropriate limits on individualized mechanistic inference.

#### ME/CFS

- National Academy of Medicine. (2015). *Beyond Myalgic Encephalomyelitis/Chronic Fatigue Syndrome: Redefining an Illness*. National Academies Press.

- U.S. Centers for Disease Control and Prevention. ME/CFS clinical overview, diagnostic guidance, and diagnostic criteria. Consult current guidance.

- National Institute for Health and Care Excellence. (2021). *Myalgic encephalomyelitis (or encephalopathy)/chronic fatigue syndrome: Diagnosis and management* (NG206).

- Nacul, L., et al. (2020). How myalgic encephalomyelitis/chronic fatigue syndrome is diagnosed and managed in primary care. Consult current systematic reviews and guidance.

#### Long COVID and persistent post-infectious symptoms

- World Health Organization. A clinical case definition of post COVID-19 condition by a Delphi consensus. Consult current WHO materials.

- U.S. Centers for Disease Control and Prevention. Long COVID clinical overview and clinical guidance. Consult current guidance.

- RECOVER Initiative. Publications, cohort resources, and current evidence on post-acute sequelae of SARS-CoV-2 infection. Consult current materials.

- Davis, H. E., McCorkell, L., Vogel, J. M., and Topol, E. J. (2023). Long COVID: Major findings, mechanisms, and recommendations. *Nature Reviews Microbiology*, 21, 133–146.

- Thaweethai, T., et al. (2023). Development of a definition of postacute sequelae of SARS-CoV-2 infection. *JAMA*, 329(22), 1934–1946.

#### Persistent symptoms following Lyme disease treatment

- Lantos, P. M., Rumbaugh, J., Bockenstedt, L. K., et al. (2021). Clinical practice guidelines by the Infectious Diseases Society of America, American Academy of Neurology, and American College of Rheumatology: 2020 guidelines for the prevention, diagnosis, and treatment of Lyme disease. *Clinical Infectious Diseases*, 72(1), e1–e48.

- U.S. Centers for Disease Control and Prevention. Lyme disease and prolonged symptoms following Lyme disease. Consult current guidance.

- National Academies of Sciences, Engineering, and Medicine. (2025). *Charting a Path Toward New Treatments for Lyme Infection-Associated Chronic Illnesses*. National Academies Press.

- Bobe, J. R., Jutras, B. L., Horn, E. J., et al. (2021). Recent progress in Lyme disease and remaining challenges. *Frontiers in Medicine*, 8, 666554.

#### Mental health and complex behavioral care

- Hernán, M. A., and Robins, J. M. (2020). *Causal Inference: What If*. Chapman and Hall/CRC.

- Shadish, W. R., Cook, T. D., and Campbell, D. T. (2002). *Experimental and Quasi-Experimental Designs for Generalized Causal Inference*. Houghton Mifflin.

- Greenland, S., Pearl, J., and Robins, J. M. (1999). Causal diagrams for epidemiologic research. *Epidemiology*, 10(1), 37–48.

- National Institute of Mental Health. Research Domain Criteria and current research resources. Consult current materials.

- Consult disorder-specific clinical guidelines, epidemiological studies, treatment-trial literature, and implementation-science research for the intended mental-health or behavioral-care application.
