## Other medical conditions and beyond

Hybrid dynamical systems are useful when a problem combines continuous evolution with consequential discrete events. The continuous component may represent biological burden, drug concentration, inflammation, physiological state, resource level, equipment condition, inventory quality, temperature, or another evolving state. Events may include dosing, treatment changes, diagnostic results, threshold crossings, failures, maintenance, interventions, policy changes, contact transitions, or environmental shocks.

The examples below are promising not simply because they belong to a particular disease, scientific discipline, or industry. They are promising when the relevant continuous states, event mechanisms, measurements, and decision questions can be defined well enough to support calibration, validation, uncertainty analysis, and—where appropriate—optimization or control.

### Existing hybrid-systems methods and software

Hybrid dynamical systems, switched systems, impulsive differential equations, event-triggered simulation, and threshold-based control are established approaches across engineering, biology, medicine, manufacturing, energy systems, robotics, and operations research. In several domains, mature specialist methods and software already exist. Multibody robotics platforms support mechanically detailed contact and actuator models; power-system packages support load-flow, transient, electromagnetic-transient, and protection studies; neural simulators support detailed biophysical neurons and network events; and domain-specific PK/PD, bioprocess, and operations tools support established workflows.

`hybrid-ds-julia` is not intended to replace those specialized ecosystems. Its intended contribution is a complementary, transparent workflow for researchers who can state a mechanistic model as continuous-time differential equations together with discrete events, thresholds, dosing schedules, treatment holds, switching policies, and reset maps. This interface is especially natural when the model does not require a full rigid-body specification, a network power-flow representation, a detailed compartmental-neuron model, or a domain-specific simulation language.

The goal is therefore not to claim that hybrid modeling is new in the domains below. Rather, it is to provide an accessible Julia-native framework for reduced-order and domain-facing models in which the investigator directly specifies the continuous dynamics, event conditions, reset maps, measurements, and analysis objectives.

### Pharmaceutical development and translational medicine

#### Some infectious diseases: tuberculosis and HIV

Tuberculosis and HIV are strong examples of settings in which continuous biological and pharmacological states interact with clinically consequential discrete treatment events.

For tuberculosis, relevant continuous states can include pathogen burden, drug exposure, host response, lesion- or compartment-specific burden where justified, and emergence of drug resistance. Important discrete events include treatment initiation, individual doses and missed doses, regimen changes, microbiological monitoring, adverse events, treatment interruption, and treatment completion. This structure supports questions about adherence, dose scheduling, pharmacokinetic variability, resistance risk, and monitoring policies.

For HIV, relevant states can include viral load, susceptible and infected cells, immune response, CD4 count, drug concentrations, and—when justified by the model—latent viral reservoirs. Relevant events include antiretroviral-therapy initiation, routine doses, missed doses, long-acting injections, treatment interruption, viral-load monitoring, resistance testing, regimen changes, and treatment of opportunistic infections. Such models can support analysis of viral suppression, rebound risk, adherence patterns, drug exposure, and treatment-switch decisions.

Mechanistic infectious-disease modeling already includes within-host pathogen dynamics, PK/PD, resistance, adherence, and treatment-optimization research. Tuberculosis pharmacometric work links drug exposure to microbiological response and compares candidate dosing regimens; HIV has a mature literature on viral dynamics, antiretroviral exposure, immune response, treatment interruption, and rebound. `hybrid-ds-julia` is complementary when scheduled or state-triggered events—doses, missed doses, long-acting injections, monitoring visits, toxicity holds, resistance thresholds, or regimen switches—must be represented explicitly.

Forward or directional sensitivities can quantify the influence of biological, pharmacological, and adherence parameters. Constrained optimization can compare dosing, monitoring, or switching policies when objectives and safety constraints are explicit. Neither should be interpreted as a clinical recommendation without disease-specific calibration, validation, and appropriate clinical expertise.

These applications are promising when the model is tied to clearly defined quantities and decisions, such as pathogen or viral burden, drug exposure, resistance, adherence, and monitoring. They should not be presented as replacements for clinical diagnosis or as a means of inferring unmeasured individual mechanisms from sparse records.

#### Oncology and adaptive cancer therapy

Cancer treatment naturally combines continuous tumor and host dynamics with discrete clinical decisions. Continuous states may include tumor burden, tumor subclones, immune activity, biomarker levels, drug concentrations, toxicity burden, organ function, and treatment response. Discrete events include chemotherapy, targeted therapy, immunotherapy, radiotherapy, surgery, imaging, biopsy, dose reduction, treatment holiday, progression, and regimen switching.

Potential applications include adaptive treatment scheduling, comparison of dose-intensity and toxicity tradeoffs, resistance-aware therapy, biomarker-triggered treatment changes, and simulation of alternative monitoring schedules. The most credible models are anchored to explicit tumor-growth, PK/PD, toxicity, and measurement assumptions and evaluated against appropriately matched clinical or experimental data.

Mathematical oncology already uses ODE, PDE, stochastic, agent-based, evolutionary, and PK/PD models to study tumor growth, resistance, toxicity, and treatment scheduling. Adaptive-therapy research is particularly relevant because tumor burden is monitored at surveillance times and treatment may start, pause, resume, or change when prespecified thresholds are crossed.

`hybrid-ds-julia` can provide a transparent implementation for continuous tumor, resistant-clone, biomarker, drug-exposure, and toxicity states coupled to discrete surveillance, dosing, treatment-holiday, and regimen-switch events. Hybrid sensitivity analysis can identify which parameters or threshold rules drive predicted control or failure. Constrained optimization can compare policy classes while preserving explicit toxicity, dosing, monitoring, and feasibility constraints.

The package should not imply that a simplified tumor model is sufficient to select treatment for an individual. Its appropriate role is to represent stated biological and policy assumptions, analyze their consequences, compare alternative intervention rules, and identify what measurements would be most useful for distinguishing competing models.

#### Immunology, inflammation, and autoimmune disease

Inflammatory and autoimmune conditions can involve continuous disease activity, cytokine signaling, tissue damage, biomarker trajectories, drug concentrations, and recovery processes, along with discrete events such as flare recognition, induction therapy, maintenance therapy, tapering, treatment escalation, infection, surgery, and laboratory monitoring.

Hybrid models may be useful for studying treatment timing, induction-versus-maintenance strategies, therapeutic monitoring, flare-sensitive dosing policies, and the tradeoff between disease control and adverse effects. They are most appropriate when the intended biological state variables and observable biomarkers have a defensible mechanistic relationship.

Existing mathematical immunology and autoimmune-disease literature includes models of tolerance, immune activation, flare-like behavior, tissue damage, treatment response, and drug combinations across many disease indications. Such models often use continuous immune-cell, cytokine, biomarker, and drug-exposure states, while induction, maintenance, tapering, monitoring, adverse-event holds, and escalation are naturally event-based.

`hybrid-ds-julia` can support explicit treatment policies layered on top of mechanistic models, including sensitivity analysis for uncertain immune or PK/PD parameters and constrained comparison of tapering, escalation, and monitoring rules. Any disease-specific use still requires a defensible biological state model, indication-specific calibration, and careful consideration of parameter identifiability.

#### Other PK/PD and quantitative systems pharmacology applications

More generally, `hybrid-ds-julia` can support PK/PD and quantitative systems pharmacology models in which drug concentrations and biological states evolve continuously while clinical actions occur at discrete times.

Examples include:

- Repeated oral, intravenous, infusion, or depot dosing
- Dose interruptions, missed doses, and adherence scenarios
- Therapeutic-drug-monitoring policies
- Drug combinations and interaction effects
- Biomarker-triggered dose adjustment
- Toxicity thresholds and treatment holds
- Resistance or tolerance thresholds
- Sequential, cyclic, and adaptive treatment regimens

PK/PD and QSP modeling already provide established frameworks for characterizing drug concentration, target engagement, biomarker response, efficacy, toxicity, variability, and treatment response. `hybrid-ds-julia` is most relevant where treatment delivery or decision rules create genuine discontinuities: bolus or infusion doses, missed doses, treatment cycles, dose holds, delayed starts, switching protocols, threshold-triggered monitoring, and sequential therapies.

The framework can support local or global sensitivity analysis, parameter estimation, uncertainty propagation, and constrained regimen optimization when event derivatives are handled correctly. It is complementary to—not a replacement for—validated population-PK, nonlinear mixed-effects, regulatory pharmacometrics, and disease-specific QSP workflows.

### Clinical operations and treatment delivery

#### Dose scheduling, adherence, and monitoring

Clinical treatment delivery includes event-rich processes that interact with continuous biological response. Medication starts, scheduled doses, missed doses, infusions, refill gaps, laboratory tests, adverse events, and treatment changes may be represented as discrete events. Drug exposure, treatment response, toxicity, and selected biomarkers may evolve continuously.

Potential uses include comparing dosing schedules, studying the effects of adherence patterns, evaluating monitoring intervals, simulating escalation rules, and examining how delayed measurements or delayed treatment changes affect outcomes.

Dose scheduling and therapeutic monitoring are intrinsically hybrid: drug and response states evolve continuously, while dosing, missed-dose episodes, refills, laboratory draws, alert generation, clinician review, and treatment adjustment occur at discrete times. Existing pharmacometric and control-oriented approaches study these problems through PK/PD modeling, therapeutic-drug monitoring, feedback control, and optimization.

`hybrid-ds-julia` can provide explicit event-level simulation of adherence scenarios and monitoring policies, together with sensitivity analysis for pharmacokinetic variability, measurement delay, and threshold choice. Policy optimization should remain constrained by clinically established safety limits and evaluated prospectively before any real-world use.

#### Hospital and critical-care workflows

Hospital and intensive-care settings contain many hybrid processes: patient physiology evolves continuously, while medications, ventilation changes, procedures, laboratory results, transfers, alarms, and care-team decisions occur as discrete events.

Possible applications include simulation of protocolized treatment pathways, monitoring thresholds, resource constraints, escalation or de-escalation decisions, fluid and drug administration schedules, and interactions between operational delays and physiological response. Such work requires careful validation and should not be treated as a substitute for clinical judgment.

Critical-care and hospital modeling already includes physiological simulation, alarm design, queuing, discrete-event simulation, and clinical decision-support research. The hybrid formulation is appropriate when a continuous physiological or pharmacological model is coupled to interventions, laboratory results, procedures, care-team decisions, transfers, and resource constraints.

`hybrid-ds-julia` can support reduced-order protocol simulations and sensitivity studies of timing, threshold, and delay assumptions. Discrete-event and workflow simulators may be preferable when physiology is not central. Optimization or control claims in this setting require unusually careful safety constraints, calibration, prospective evaluation, and clinician oversight.

#### Digital health and closed-loop care

Wearables, home monitoring, remote-care platforms, and clinical decision-support systems increasingly combine continuous streams of measurements with discrete interventions. Continuous signals may include glucose, activity, heart rate, blood pressure, oxygen saturation, temperature, or symptom trends. Events may include alerts, patient-reported outcomes, medication reminders, clinician review, telehealth visits, treatment adjustments, and device failures.

Hybrid models can help prototype monitoring policies, alert thresholds, intervention timing, and robustness to missing or delayed data. Safety-critical decision support requires substantial external validation, human-factors evaluation, and appropriate clinical oversight.

Closed-loop health technologies already combine continuous sensing, control algorithms, alerts, and discrete treatment or communication events. `hybrid-ds-julia` can provide a transparent research environment for exploring threshold policies, delayed or missing measurements, event-triggered intervention, and robustness to sensor noise.

Sensitivity and optimization analyses should report uncertainty, failure modes, alert burden, and safety constraints rather than treating a simulated policy as ready for deployment.

### Biomanufacturing and industrial biotechnology

#### Batch, fed-batch, and continuous bioprocesses

Bioprocesses often combine continuous reactor dynamics with discrete operating actions. Continuous states can include biomass, substrate concentrations, product concentration, dissolved oxygen, pH, temperature, and metabolic activity. Discrete events can include feed changes, sampling, sensor calibration, contamination response, batch transitions, harvest, cleaning, and controller-mode changes.

Potential applications include feed scheduling, yield optimization, process monitoring, disturbance analysis, scale-up studies, and comparison of batch, fed-batch, and continuous-production strategies.

Bioprocess modeling and control already use mass-balance ODEs, soft sensors, process analytical technology, model-predictive control, switching control, and optimization for batch, fed-batch, and continuous manufacturing. Feed changes, sampling, mode changes, harvest, cleaning, contamination response, and equipment faults make many workflows explicitly hybrid.

`hybrid-ds-julia` can complement specialized process-control platforms by enabling compact, transparent ODE-and-event prototypes, hybrid sensitivity analysis, feed-schedule optimization, and investigation of threshold or switching policies. Plant deployment requires validated kinetics, measurement models, operational constraints, and integration with established manufacturing-control systems.

#### Quality control, maintenance, and process transitions

Manufacturing systems evolve under continuous wear, throughput, energy use, inventory levels, and quality metrics, while maintenance, inspection, repair, changeovers, quality holds, and shutdowns occur as discrete events.

Hybrid models can support predictive-maintenance policies, quality-control strategies, scheduling of inspection and calibration, response to process deviations, and evaluation of tradeoffs among yield, downtime, risk, and operating cost.

Existing manufacturing, reliability, and operations research includes condition monitoring, maintenance optimization, discrete-event simulation, and process-control methods. `hybrid-ds-julia` is most relevant where a continuous degradation, quality, thermal, chemical, or inventory state interacts directly with event-driven inspection, maintenance, production, and policy logic.

Sensitivity analysis can identify whether a policy is dominated by degradation rate, sensor noise, maintenance threshold, repair time, demand assumptions, or process variability. Optimization can compare constrained maintenance and production policies when the continuous state model is meaningful and the decision rules are explicit.

### Energy systems and power grids

#### Storage dispatch and demand response

Energy storage and demand-response systems have continuously varying states of charge, load, renewable generation, prices, temperature, and equipment health. Discrete events include dispatch commands, charging or discharging transitions, tariff changes, demand-response activations, maintenance, and equipment failures.

Hybrid models can support storage-control policies, peak-shaving analysis, microgrid operation, tariff-sensitive dispatch, and evaluation of resilience under uncertain demand and generation.

Energy-system research already uses optimal control, stochastic control, mixed-integer optimization, detailed power-system simulation, and model-predictive control. `hybrid-ds-julia` is most useful for transparent reduced-order models in which storage dynamics, thermal limits, degradation, price signals, and discrete dispatch decisions interact.

Sensitivity analysis can identify dependence on demand, generation, degradation, tariff, and threshold assumptions. Constrained optimization can compare dispatch policies while making state-of-charge, reliability, and equipment constraints explicit.

#### Grid operations, faults, and restoration

Electrical-grid dynamics can change rapidly in response to discrete switching events, generator trips, line faults, protection actions, islanding, restoration decisions, and weather-related disruptions. Continuous states may include voltage, frequency, power flows, thermal loading, and reserve margins.

Potential applications include contingency analysis, fault response, restoration sequencing, protection-policy testing, and resilience planning. Real-world deployment requires high-quality system data, strong safety controls, and domain-specific validation.

Power systems are a mature hybrid-systems domain. Voltage, frequency, power flow, thermal loading, and machine or converter states evolve continuously, while faults, protection-device actions, line trips, switching, islanding, reconnection, and restoration decisions produce discrete transitions. Mature tools already support power flow, transient stability, electromagnetic-transient simulation, protection studies, and grid planning.

`hybrid-ds-julia` should therefore be framed as complementary for reduced-order event-aware models, methodological research, sensitivity studies, and optimization prototypes rather than as a replacement for power-system simulation suites. Event-time sensitivity and reset-aware trajectory analysis may be useful when evaluating protection thresholds, switching policies, or restoration sequences.

### Supply chains, logistics, and operations

#### Inventory, routing, and service-level policies

Supply-chain systems combine continuously changing inventory, demand, capacity, lead times, quality, and cost with discrete decisions such as ordering, shipment, routing, allocation, stockout, expedited delivery, and supplier disruption.

Hybrid models can support reorder policies, safety-stock design, allocation strategies, service-level analysis, disruption planning, and sensitivity analysis for uncertain demand or lead times.

Supply-chain research already relies heavily on discrete-event simulation, mathematical programming, agent-based models, stochastic control, and simulation optimization. `hybrid-ds-julia` is most appropriate when meaningful continuous dynamics must be retained—for example, perishable-inventory decay, equipment wear, energy use, fluid or bulk-material levels, temperature-sensitive quality loss, or continuously evolving demand and capacity signals.

Sensitivity analysis can clarify which lead-time, demand, degradation, or capacity assumptions dominate a policy result, while optimization can compare constrained reorder or maintenance policies. Where the system is primarily discrete, established optimization and discrete-event tools will usually be the better primary choice.

#### Production planning and maintenance

Production systems combine continuous machine condition, work-in-process, throughput, and energy use with discrete events such as job release, setup, tool replacement, machine failure, repair, shift change, quality inspection, and production rescheduling.

Possible applications include maintenance scheduling, bottleneck analysis, production sequencing, spare-parts planning, and evaluation of resilience to equipment failure or fluctuating demand.

This area already has mature scheduling, reliability, optimization, and discrete-event simulation methods. `hybrid-ds-julia` may be useful when a continuous degradation, quality, inventory, thermal, or process state affects the timing and consequences of discrete planning decisions. It is not intended to displace specialized mixed-integer scheduling or discrete-event manufacturing tools when continuous dynamics are secondary.

### Ecosystems, agriculture, and environmental management

#### Crop growth, irrigation, and pest management

Agricultural systems have continuous states such as soil moisture, nutrient availability, crop biomass, plant stress, pest population, and weather-driven growth. Discrete events include planting, irrigation, fertilizer application, pesticide treatment, harvest, rainfall events, equipment failure, and regulatory restrictions.

Hybrid models can support irrigation scheduling, pest-management strategies, input optimization, yield-risk analysis, and assessment of weather-sensitive farm-management policies.

Agricultural modeling already uses crop simulators, soil-water models, weather forecasts, optimal control, precision-agriculture tools, and integrated pest-management frameworks. `hybrid-ds-julia` can provide a compact event-aware framework for simplified or reduced-order models in which irrigation, planting, fertilization, spraying, harvest, or policy restrictions alter continuously evolving crop, soil, water, or pest states.

Sensitivity analysis can identify which growth, weather, soil, and intervention parameters dominate an outcome. Constrained optimization can compare management policies while respecting water availability, input limits, environmental constraints, and uncertainty. Results should be interpreted alongside domain-specific crop, hydrology, and climate models when operational accuracy is required.

#### Fisheries, wildlife, and invasive-species control

Population dynamics, habitat condition, resource availability, and disease prevalence may evolve continuously, while harvest seasons, stocking, habitat interventions, hunting quotas, surveillance detections, barriers, and control actions occur discretely.

Potential applications include harvest-policy design, invasive-species response, surveillance planning, intervention timing, and comparison of conservation strategies under ecological uncertainty.

Ecological modeling already uses population dynamics, optimal harvesting, impulsive differential equations, seasonal management, and stochastic simulation. Hybrid models are natural when continuous population or habitat states interact with seasonal harvest, stocking, detection, release, barrier, or control events.

`hybrid-ds-julia` can support hypothesis-driven policy comparisons and sensitivity analysis, but ecological predictions remain constrained by observation uncertainty, model misspecification, climate variability, and the possibility of unmeasured ecological interactions.

#### Water, land, and climate-adaptation systems

Water reservoirs, groundwater, soil moisture, land condition, pollutant concentration, and ecosystem resilience can evolve continuously. Discrete events include releases, pumping, irrigation restrictions, flood-control actions, infrastructure failures, wildfire, land-use changes, and emergency policy measures.

Hybrid models can assist scenario analysis, infrastructure planning, drought and flood management, adaptive water allocation, and robustness analysis under climate uncertainty.

Hydrologic, climate, and land-management fields already maintain sophisticated domain models. `hybrid-ds-julia` is most relevant for transparent reduced-order models, threshold-policy prototypes, and event-aware management analysis rather than replacement of comprehensive hydrologic, climate, or geographic simulation systems.

### Infrastructure, robotics, and engineered systems

#### Buildings, HVAC, and thermal management

Buildings and thermal systems have continuously evolving temperature, humidity, occupancy-related loads, energy use, and equipment condition. Discrete events include thermostat changes, occupancy transitions, maintenance, equipment faults, demand-response signals, and changes in operating mode.

Potential applications include energy optimization, fault detection, comfort-management policies, maintenance scheduling, and evaluation of control strategies under changing weather and occupancy.

Hybrid control, system identification, and model-predictive control are established approaches in building-energy research. Thermal mass, temperature, humidity, storage state, and energy use evolve continuously, while thermostats, compressors, occupancy changes, demand-response commands, faults, and controller modes produce discrete transitions.

`hybrid-ds-julia` can be used for reduced-order thermal models, event-aware threshold-policy simulations, sensitivity analysis for uncertain loads and heat-transfer parameters, and constrained optimization of comfort-versus-energy tradeoffs. It complements rather than replaces detailed building-energy simulators and building-management systems.

#### Transportation and autonomous systems

Transportation systems involve continuous motion, fuel or battery state, traffic flow, vehicle health, and environmental conditions, alongside discrete events such as route changes, intersections, signal changes, charging stops, incidents, passenger pickup or dropoff, and vehicle failures.

Hybrid models may support routing, fleet dispatch, charging policies, traffic-control design, safety analysis, and testing of control policies in simulated operating conditions.

Transportation and autonomous-systems research already includes hybrid automata, model-predictive control, traffic-flow models, vehicle dynamics, routing algorithms, formal verification, and simulation environments. `hybrid-ds-julia` can support reduced-order event-aware simulations, sensitivity analysis of threshold and timing assumptions, and constrained policy optimization.

High-fidelity vehicle simulation, safety assurance, and formal verification remain the province of specialized tools and domain-specific workflows.

#### Robotics, inspection, and fault management

Robotics is a foundational hybrid-systems domain. Continuous robot dynamics interact with discrete contact, impact, grasp, release, controller switching, perception updates, task transitions, replanning, faults, and human intervention.

Specialized multibody platforms already support detailed robotic simulation. For example, platforms such as Drake provide APIs for bodies, joints, frames, actuators, force elements, geometry, gravity, springs, and contact. These tools are appropriate when a user can provide a detailed mechanical specification. They are not the intended replacement target for `hybrid-ds-julia`.

Detailed robotics software can represent compliance through springs, force elements, compliant contact, and related constitutive models. The practical distinction is not whether compliance is possible; it is that these tools require the user to formulate a mechanical multibody system and select its contact and compliance representation.

`hybrid-ds-julia` is complementary. It can support lower-dimensional or non-rigid-body models in which the investigator states continuous equations and event maps directly. This includes reduced-order control models, event-triggered policy models, biologically motivated sensorimotor models, plant-plus-controller models, and cross-domain hybrid systems whose state equations do not originate in a multibody description.

Sensitivity analysis of event timing and reset maps can inform threshold selection and robustness studies. Optimization can compare controller, inspection, or fault-management policies subject to explicit constraints. The package should not be described as a substitute for high-fidelity mechanical simulation, established robotics middleware, or formal safety verification.

#### Postural control, locomotion, and sensorimotor behavior

Human and robotic balance and locomotion combine continuous biomechanical and neural-control dynamics with discrete events such as foot contact, lift-off, heel strike, toe-off, perturbations, sensory changes, controller switching, recovery steps, and transitions between behavioral or gait phases.

Legged locomotion is a canonical hybrid dynamical-system problem. Continuous dynamics evolve during stance and swing, while contact transitions and impact maps introduce discrete changes. Existing work includes hybrid zero dynamics, virtual constraints, compliant-leg and spring-mass models, contact and impact mechanics, phase-dependent control, and gait optimization.

`hybrid-ds-julia` is not intended to replace detailed multibody and gait-design tools. It can complement them for lower-dimensional, interpretable models in which the researcher specifies the equations, switching surfaces, reset maps, sensory signals, estimators, and control rules directly.

Potential applications include:

- Inverted-pendulum stance models
- Multi-segment posture models
- Spring-mass and compliant-leg locomotion
- Stance-to-step transitions
- Perturbation and recovery responses
- Sensory reweighting
- Delayed sensory feedback
- Phase-dependent visual, vestibular, tactile, or proprioceptive control
- Event-triggered balance corrections
- Active sensing and sensorimotor adaptation

Hybrid sensitivity analysis is especially relevant because perturbations can alter both contact timing and post-impact state. Optimization can compare stable gait, recovery, sensing, or control policies while making the corresponding assumptions explicit.
