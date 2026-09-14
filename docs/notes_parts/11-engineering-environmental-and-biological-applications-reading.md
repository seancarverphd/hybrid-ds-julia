### Biomanufacturing and industrial biotechnology

This section collects application-domain references for mechanistic, event-aware models of bioprocesses, industrial operations, energy systems, environmental management, infrastructure, robotics, and sensorimotor systems. They are starting points for model formulation and validation, not substitutes for domain-specific simulators, operational constraints, or expert review.

#### Batch, fed-batch, and continuous bioprocesses

- Nielsen, J., Villadsen, J., and Lidén, G. (2017). *Bioreaction Engineering Principles* (3rd ed.). Springer.

  This textbook covers microbial and cell-culture kinetics, stoichiometry, transport, reactor design, and batch, fed-batch, and continuous bioprocess operation. It provides a foundation for defining mass-balance states, feed inputs, phase changes, and harvest or cleaning events in mechanistic bioprocess models.

- Villadsen, J., Nielsen, J., and Lidén, G. (2011). *Bioreaction Engineering Principles* (3rd ed.). Springer.

  See the annotated 2017 third-edition entry above in [Batch, fed-batch, and continuous bioprocesses](#batch-fed-batch-and-continuous-bioprocesses). Retain only the edition actually intended for the bibliography if the two entries refer to the same work.

- Banga, J. R., Balsa-Canto, E., Moles, C. G., and Alonso, A. A. (2003). Improving food processing using modern optimization methods. *Trends in Food Science & Technology*, 14, 131–144. https://doi.org/10.1016/S0924-2244(03)00074-2

  This review surveys optimization methods in food processing, including process design, operation, and control. Its scope illustrates how mechanistic dynamic models can be coupled to operational objectives and constraints.

- Smets, I. Y., Claes, J. E., November, E. J., Bastin, G. P., and Van Impe, J. F. (2004). Optimal control of a fed-batch fermentation process. *Journal of Process Control*, 14, 379–386. https://doi.org/10.1016/S0959-1524(03)00075-3

  This study applies optimal-control methods to a fed-batch fermentation process. It is a direct application analogue for models in which feed changes, phase transitions, and operating constraints must be represented explicitly.

- Tebbani, S., and colleagues. Optimal switching control of fed-batch fermentation processes. Consult primary literature for the intended organism and product.

#### Quality control, maintenance, and process transitions

- Isermann, R. (2006). *Fault-Diagnosis Systems: An Introduction from Fault Detection to Fault Tolerance*. Springer.

  This textbook covers model-based and data-driven fault detection, isolation, diagnosis, and fault-tolerant control. It is useful for representing fault states, alarms, maintenance actions, and recovery modes as explicit hybrid transitions.

- Jardine, A. K. S., Lin, D., and Banjevic, D. (2006). A review on machinery diagnostics and prognostics implementing condition-based maintenance. *Mechanical Systems and Signal Processing*, 20(7), 1483–1510. https://doi.org/10.1016/j.ymssp.2005.09.012

  This review surveys condition-based maintenance, diagnostics, prognostics, and maintenance-decision concepts. It provides context for coupling continuous degradation states to inspection, alarm, repair, and replacement events.

- Qin, S. J. (2012). Survey on data-driven industrial process monitoring and diagnosis. *Annual Reviews in Control*, 36(2), 220–234. https://doi.org/10.1016/j.arcontrol.2012.09.004

  This review covers data-driven process monitoring and fault diagnosis, including statistical and machine-learning methods. It is relevant to observation models and anomaly-detection components that may supplement, rather than replace, a mechanistic hybrid process model.

### Energy systems and power grids

#### Storage, demand response, faults, and restoration

- Kundur, P. (1994). *Power System Stability and Control*. McGraw-Hill.

  This textbook covers power-system dynamics, stability, control, protection, and operating phenomena across generation and transmission systems. It provides foundational context for continuous electromechanical dynamics coupled to switching, protection, fault, and restoration events.

- Sauer, P. W., and Pai, M. A. (1998). *Power System Dynamics and Stability*. Prentice Hall.

  This textbook introduces power-system dynamic models and stability analysis, with emphasis on generators, networks, and control systems. It is useful for constructing reduced-order event-aware grid models with clearly stated physical and protection assumptions.

- Hiskens, I. A., and Pai, M. A. (2000). Trajectory sensitivity analysis of hybrid systems. *IEEE Transactions on Circuits and Systems I*, 47(2), 204–220. https://doi.org/10.1109/81.828568

  This paper develops trajectory sensitivity analysis for power systems with discrete events and topology changes. It is a closely related application example for event-time dependence, switching, and sensitivity propagation in `hybrid-ds-julia`.

- Milano, F. (2010). *Power System Modelling and Scripting*. Springer.

  This textbook covers mathematical modeling and scripting for power-system analysis, including dynamic models and simulation workflows. It is useful for translating domain-specific components into transparent state, parameter, and event representations.

- DIgSILENT GmbH. PowerFactory documentation. Consult current documentation for dynamic simulation, events, protection, and Modelica/FMI interoperability.

- PSCAD, EMTP-RV, PSS®E, and related power-system simulation documentation. Consult the tool appropriate to the intended study.

### Supply chains, logistics, and operations

#### Inventory, routing, production, and maintenance

- Simchi-Levi, D., Kaminsky, P., and Simchi-Levi, E. (2008). *Designing and Managing the Supply Chain* (3rd ed.). McGraw-Hill.

  This textbook covers supply-chain design, inventory, transportation, sourcing, and operational tradeoffs. It provides broad background for systems where continuous inventory or backlog states interact with discrete replenishment, routing, production, and disruption decisions.

- Bertazzi, L., and Speranza, M. G. (2012). Inventory routing problems: An introduction. *EURO Journal on Transportation and Logistics*, 1, 307–326. https://doi.org/10.1007/s13676-012-0016-7

  This review introduces inventory-routing formulations that coordinate inventory decisions with vehicle routes. It is useful for representing inventories as evolving states and deliveries or route changes as scheduled or policy-driven discrete actions.

- Kleywegt, A. J., Nori, V. S., and Savelsbergh, M. W. P. (2002). The stochastic inventory routing problem with direct deliveries. *Transportation Science*, 36(1), 94–118. https://doi.org/10.1287/trsc.36.1.94.562

  This paper studies inventory routing under stochastic demand and direct-delivery decisions. It illustrates how uncertainty and discrete operational choices can be coupled to evolving inventory states.

- Pinedo, M. (2022). *Scheduling: Theory, Algorithms, and Systems* (6th ed.). Springer.

  This textbook covers deterministic and stochastic scheduling models, algorithms, and applications. It provides a broad reference for production, service, and maintenance systems in which releases, setups, jobs, and resource assignments are discrete operational events.

- Dekker, R. (1996). Applications of maintenance optimization models: A review and analysis. *Reliability Engineering & System Safety*, 51(3), 229–240. https://doi.org/10.1016/0951-8320(95)00076-3

  This review surveys maintenance-optimization models and their application settings. It is relevant to hybrid workflows that link continuous deterioration or condition measures to inspection, repair, replacement, and downtime decisions.

### Ecosystems, agriculture, and environmental management

#### Crop growth, irrigation, and pest management

- Jones, J. W., Hoogenboom, G., Porter, C. H., et al. (2003). The DSSAT cropping system model. *European Journal of Agronomy*, 18, 235–265. https://doi.org/10.1016/S1161-0301(02)00107-7

  This paper describes DSSAT, a crop-modeling framework that represents crop development, soil processes, weather, and management inputs. It is useful background for modeling planting, irrigation, fertilization, and harvest as interventions applied to continuous crop and soil states.

- Holzworth, D. P., Huth, N. I., deVoil, P. G., et al. (2014). APSIM—Evolution towards a new generation of agricultural systems simulation. *Environmental Modelling & Software*, 62, 327–350. https://doi.org/10.1016/j.envsoft.2014.07.009

  This paper describes the APSIM agricultural-systems modeling framework and its modular treatment of crops, soils, climate, and management. It provides a useful application reference for event-rich agricultural management models, while detailed applications should use the maintained domain software and local calibration.

- Steduto, P., Hsiao, T. C., Raes, D., and Fereres, E. (2009). *AquaCrop—The FAO Crop Model to Simulate Yield Response to Water*. FAO.

  This reference presents AquaCrop, a crop-water productivity model focused on yield response to water. It is useful for irrigation-scheduling questions where water balance evolves continuously but irrigation decisions occur as discrete actions.

- Chaves, M. M., Zarrouk, O., Francisco, R., et al. (2010). Deficit irrigation and partial root zone drying: A review. *Journal of Experimental Botany*, 61(7), 1965–1975. https://doi.org/10.1093/jxb/erq112

  This review covers deficit-irrigation and partial-root-zone-drying strategies, their physiological effects, and agronomic tradeoffs. It provides domain context for comparing irrigation policies but does not substitute for crop-, soil-, and region-specific validation.

- Consult integrated pest-management, crop-model, hydrology, and agricultural-extension literature for the intended crop, region, and intervention.

#### Fisheries, wildlife, and invasive-species control

- Clark, C. W. (2010). *Mathematical Bioeconomics: The Mathematics of Conservation* (3rd ed.). Wiley.

  This textbook covers renewable-resource economics, population dynamics, harvesting, and optimal control. It provides foundational scope for management models in which continuous population dynamics interact with seasonal harvest, quotas, closures, or control actions.

- Hilborn, R., and Walters, C. J. (1992). *Quantitative Fisheries Stock Assessment*. Chapman and Hall.

  This textbook covers population-dynamics models, stock assessment, uncertainty, and fisheries-management decisions. It is useful for connecting biological state estimation to harvest-policy and monitoring decisions.

- Lenhart, S., and Workman, J. T. (2007). *Optimal Control Applied to Biological Models*. Chapman and Hall/CRC.

  This textbook introduces optimal-control methods through biological applications, including population and resource-management models. It provides mathematical background for evaluating intervention schedules and constraints in ecological systems.

- Impulsive differential-equation and seasonal-harvest literature for fishery, wildlife, and invasive-species management. Consult species-specific primary research.

#### Water, land, and climate-adaptation systems

- Loucks, D. P., and van Beek, E. (2017). *Water Resource Systems Planning and Management* (2nd ed.). Springer.

  This textbook covers water-resource planning, reservoir operation, hydrology, optimization, uncertainty, and multiobjective decision-making. It is useful for systems where continuous storage and flow dynamics meet discrete releases, restrictions, flood operations, or allocation rules.

- Yeh, W. W.-G. (1985). Reservoir management and operations models: A state-of-the-art review. *Water Resources Research*, 21(12), 1797–1818. https://doi.org/10.1029/WR021i012p01797

  This review surveys reservoir-operation models, objectives, constraints, and optimization approaches. It provides a compact entry point for modeling storage dynamics together with release and operating-policy decisions.

- IPCC. Assessment Reports and Working Group reports on impacts, adaptation, and vulnerability. Consult the current assessment cycle.

- Consult region-specific hydrologic, groundwater, flood-risk, and climate-adaptation literature for operational applications.

### Infrastructure, robotics, and engineered systems

#### Buildings, HVAC, and thermal management

- Wetter, M. (2011). Co-simulation of building energy and control systems with the Building Controls Virtual Test Bed. *Journal of Building Performance Simulation*, 4(3), 185–203. https://doi.org/10.1080/19401493.2010.518631

  This paper presents a co-simulation environment for building-energy and control systems. It is useful for models that couple thermal states to supervisory control, occupancy changes, equipment switching, and other operational events.

- Aswani, A., Master, N., Taneja, J., Krioukov, A., Culler, D., and Tomlin, C. (2012). Energy-efficient building HVAC control using hybrid system LBMPC. *arXiv:1204.4717*. https://arxiv.org/abs/1204.4717

  This paper applies learning-based model-predictive control to an HVAC system with hybrid dynamics. It is a close application analogue for keeping discrete operating modes explicit while using data to improve model or controller performance.

- Afram, A., and Janabi-Sharifi, F. (2014). Theory and applications of HVAC control systems—A review of model predictive control. *Building and Environment*, 72, 343–355. https://doi.org/10.1016/j.buildenv.2013.11.016

  This review surveys model-predictive-control approaches for HVAC systems, including models, objectives, constraints, and implementation issues. It provides broad scope for thermal-control applications where switching equipment and comfort constraints create event-aware decisions.

- EnergyPlus documentation and Modelica Buildings Library documentation. Consult current versions for detailed building-energy simulation.

#### Transportation and autonomous systems

- Rajamani, R. (2012). *Vehicle Dynamics and Control* (2nd ed.). Springer.

  This textbook covers vehicle dynamics, state estimation, and control for ground vehicles. It provides foundational models for continuous motion and actuation, while maneuver changes, supervisory logic, and safety interventions can be represented as discrete modes or events.

- Paden, B., Čáp, M., Yong, S. Z., Yershov, D., and Frazzoli, E. (2016). A survey of motion planning and control techniques for self-driving urban vehicles. *IEEE Transactions on Intelligent Vehicles*, 1(1), 33–55. https://doi.org/10.1109/TIV.2016.2578706

  This review surveys motion planning and control methods for autonomous urban driving. Its scope includes routing, behavior planning, trajectory generation, and control, making it useful context for distinguishing high-level discrete decisions from continuous vehicle dynamics.

- Althoff, M., and Dolan, J. M. (2014). Online verification of automated road vehicles using reachability analysis. *IEEE Transactions on Robotics*, 30(4), 903–918. https://doi.org/10.1109/TRO.2014.2312453

  This paper applies reachability analysis to online safety verification for automated road vehicles. It is relevant to safety-oriented analysis of hybrid systems, where discrete decisions and uncertain continuous trajectories must be assessed together.

- Consult current formal-verification, simulation, traffic-control, and vehicle-platform literature for the intended application.

#### Robotics, contact mechanics, and fault management

- Henzinger, T. A. (1996). The theory of hybrid automata. In *Proceedings of the 11th Annual IEEE Symposium on Logic in Computer Science*, 278–292. https://doi.org/10.1109/LICS.1996.561342

  See the annotated entry in Part 09, [Hybrid transitions, saltation matrices, and event-aware derivatives](#hybrid-transitions-saltation-matrices-and-event-aware-derivatives). Hybrid automata provide the formal language for modes, flows, guards, and resets used across robotics and other event-driven systems.

- Tedrake, R. (2023). *Underactuated Robotics: Algorithms for Walking, Running, Swimming, Flying, and Manipulation*. Online textbook and course notes. https://underactuated.csail.mit.edu/

  This online textbook covers dynamics, control, optimization, planning, contact, locomotion, and manipulation for underactuated robots. It provides a broad practical and mathematical foundation for contact-rich systems with impacts, lift-off, controller transitions, and hybrid mode changes.

- Manchester, I. R., and Slotine, J.-J. E. (2017). Control contraction metrics: Convex and intrinsic criteria for nonlinear feedback design. *IEEE Transactions on Automatic Control*, 62(6), 3046–3053. https://doi.org/10.1109/TAC.2017.2668380

  This paper develops control-contraction metrics for nonlinear feedback design. It is relevant as a nonlinear-control reference for continuous-mode dynamics, though contact, reset, and switching effects require additional hybrid analysis.

- Drake documentation. Consult current documentation for `MultibodyPlant`, joints, actuators, force elements, springs, compliant contact, hydroelastic contact, and contact-model choices.

- Isermann, R. (2006). *Fault-Diagnosis Systems: An Introduction from Fault Detection to Fault Tolerance*. Springer.

  See the annotated entry in [Quality control, maintenance, and process transitions](#quality-control-maintenance-and-process-transitions).

#### Postural control, locomotion, and sensorimotor behavior

- Grizzle, J. W., Abba, G., and Plestan, F. (2001). Asymptotically stable walking for biped robots: Analysis via systems with impulse effects. *IEEE Transactions on Automatic Control*, 46(1), 51–64. https://doi.org/10.1109/9.898695

  This paper analyzes bipedal walking as a system with impulse effects, using impacts and periodic-orbit stability. It is a direct hybrid-systems example in which event maps and continuous flows jointly determine gait behavior.

- Westervelt, E. R., Grizzle, J. W., Chevallereau, C., Choi, J. H., and Morris, B. (2007). *Feedback Control of Dynamic Bipedal Robot Locomotion*. CRC Press.

  This textbook develops models and feedback-control methods for dynamic bipedal locomotion, including hybrid dynamics, impacts, periodic orbits, and gait stabilization. It is a foundational reference for contact-driven mode transitions and event-aware control.

- Burden, S. A., Revzen, S., and Sastry, S. S. (2015). Model reduction near periodic orbits of hybrid dynamical systems. *IEEE Transactions on Automatic Control*, 60(10), 2626–2639. https://doi.org/10.1109/TAC.2015.2409453

  This paper studies model reduction near periodic orbits in hybrid dynamical systems. It is relevant to analyzing reduced-order behavior in locomotion and other event-driven periodic systems.

- Blickhan, R. (1989). The spring-mass model for running and hopping. *Journal of Biomechanics*, 22(11–12), 1217–1227. https://doi.org/10.1016/0021-9290(89)90224-8

  This paper presents the spring-mass model as a reduced-order description of running and hopping. It is useful for building interpretable continuous-phase locomotion models before adding contact, switching, or sensory-control events.

- Holmes, P., Full, R. J., Koditschek, D., and Guckenheimer, J. (2006). The dynamics of legged locomotion: Models, analyses, and challenges. *SIAM Review*, 48(2), 207–304. https://doi.org/10.1137/S003614450444513X

  This review covers models, analysis, and open problems in legged locomotion across biomechanics and robotics. It provides broad scope for hybrid locomotion, including impacts, compliant contact, reduced-order models, and control challenges.
