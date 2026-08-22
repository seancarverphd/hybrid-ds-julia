# hybrid-ds-julia

A Julia-focused research-software project for building, simulating, analyzing, and eventually optimizing hybrid dynamical-systems models. The intended focus is mechanistic ODE models whose continuous dynamics are altered by discrete events such as doses, missed doses, treatment holds, toxicity thresholds, therapy switches, measurements, controller transitions, and other state- or time-triggered interventions.

**Work in progress.** `hybrid-ds-julia` and this README are evolving research-software and documentation projects. The mathematical formulations, implementation plans, application discussions, examples, benchmarks, and references should be treated as provisional unless explicitly identified as implemented, tested, or literature-verified. Interfaces, capabilities, claims, and priorities may change as the package develops and as expert feedback and additional verification are incorporated.

This README is intentionally detailed and modular. Use the table of contents to navigate directly to the mathematical methods, implementation details, computational considerations, application domains, or examples most relevant to your work; readers do not need to read the document linearly.

## Scope, authorship, and verification status

This document was drafted and expanded with assistance from a large language model. The assistant was used to help organize material, generate prose, identify possible literature and software context, and formulate questions and technical explanations. Its use does not constitute independent validation of the scientific, mathematical, clinical, engineering, software, or literature claims made here.

Readers should treat the application discussions, software comparisons, computational-scaling guidance, and cited research context as material requiring verification against original literature, authoritative software documentation, and domain-specific expertise before relying on it for research, engineering, clinical, or operational decisions.

The immuno-oncology material supporting the flagship first test bed has received a focused literature review and should be read together with its cited sources. The other application-domain sections, including broader disease, engineering, and author/laboratory discussions, have not yet received the same level of systematic literature verification. They are best understood as structured hypotheses, potential directions, and invitations for expert correction rather than validated claims of applicability.

## Aims, potential users, and questions

The project is aimed at users who have or can formulate a mechanistic continuous-time model and need to represent events as part of the model rather than as informal external bookkeeping.

Potential users include:

- Researchers building PK/PD, QSP, infectious-disease, oncology, immunology, or treatment-control models;
- Scientists studying reduced-order models of physiology, behavior, sensorimotor control, or adaptation;
- Engineers working with event-driven process, energy, thermal, mechanical, or control models;
- Operations researchers whose systems include both meaningful continuous states and discrete decisions;
- Developers who need transparent event semantics, reproducible event logs, and sensitivity-aware hybrid simulation.

Potential questions include:

- How do different dosing or adherence schedules alter drug exposure and response?
- When should a threshold-triggered treatment hold be activated or released?
- How sensitive is a predicted event time to a parameter, initial condition, or measurement delay?
- When does a control or treatment policy become unstable, unsafe, or prone to chattering?
- How do alternative monitoring or switching rules compare under uncertainty?
- What measurements or perturbations best distinguish competing mechanistic hypotheses?

The package is not inherently appropriate merely because a problem has discrete events. It is most useful when the continuous state model, event logic, available measurements, and intended inference or decision problem can be stated and validated responsibly.

## Table of contents

- [Scope, authorship, and verification status](#scope-authorship-and-verification-status)
- [Aims, potential users, and questions](#aims-potential-users-and-questions)
- [Overview](#overview)
- [Project goals](#project-goals)
- [Why hybrid models?](#why-hybrid-models)
- [Why immuno-oncology first?](#why-immuno-oncology-first)
- [Intended users and use cases](#intended-users-and-use-cases)
- [Mathematical approach](#mathematical-approach)
  - [Continuous dynamics, modes, and events](#continuous-dynamics-modes-and-events)
  - [Scheduled and state-triggered events](#scheduled-and-state-triggered-events)
  - [Event maps and hybrid semantics](#event-maps-and-hybrid-semantics)
  - [Hybrid trajectories and measurements](#hybrid-trajectories-and-measurements)
  - [Dosing, pulses, and treatment holds](#dosing-pulses-and-treatment-holds)
  - [Threshold policies and mode-dependent control](#threshold-policies-and-mode-dependent-control)
  - [Event logging and reproducibility](#event-logging-and-reproducibility)
  - [Numerical considerations near events](#numerical-considerations-near-events)
  - [Validation of hybrid models](#validation-of-hybrid-models)
- [Computational scaling, event complexity, and practical compute budgets](#computational-scaling-event-complexity-and-practical-compute-budgets)
  - [Model notation and baseline cost](#model-notation-and-baseline-cost)
  - [What makes an event difficult?](#what-makes-an-event-difficult)
  - [Jacobians, variational flow, and O(n²) state equations](#jacobians-variational-flow-and-on2-state-equations)
  - [Forward parameter sensitivities](#forward-parameter-sensitivities)
  - [Saltation-aware hybrid derivatives](#saltation-aware-hybrid-derivatives)
  - [Automatic differentiation](#automatic-differentiation)
  - [Adjoint sensitivities](#adjoint-sensitivities)
  - [Multiple shooting](#multiple-shooting)
  - [Event count, event structure, and tractability](#event-count-event-structure-and-tractability)
  - [Dimension-specific planning guide](#dimension-specific-planning-guide)
  - [Fixed-budget planning](#fixed-budget-planning)
  - [Illustrative AWS estimates](#illustrative-aws-estimates)
  - [Benchmark before scaling](#benchmark-before-scaling)
  - [Workflow recommendations](#workflow-recommendations)
- [Opportunities for parallelization](#opportunities-for-parallelization)
  - [Parallelism levels](#parallelism-levels)
  - [Embarrassingly parallel trajectory ensembles](#embarrassingly-parallel-trajectory-ensembles)
  - [Monte Carlo and uncertainty quantification](#monte-carlo-and-uncertainty-quantification)
  - [Parallel multistart and population optimization](#parallel-multistart-and-population-optimization)
  - [Multiple shooting and time-domain decomposition](#multiple-shooting-and-time-domain-decomposition)
  - [GPU opportunities and limitations](#gpu-opportunities-and-limitations)
  - [AWS Batch and cloud orchestration](#aws-batch-and-cloud-orchestration)
- [AI/ML and mathematical extensions](#aiml-and-mathematical-extensions)
- [Test beds](#test-beds)
- [Other medical conditions and beyond](#other-medical-conditions-and-beyond)
  - [Existing hybrid-systems methods and software](#existing-hybrid-systems-methods-and-software)
  - [Pharmaceutical development and translational medicine](#pharmaceutical-development-and-translational-medicine)
    - [Some infectious diseases: tuberculosis and HIV](#some-infectious-diseases-tuberculosis-and-hiv)
    - [Oncology and adaptive cancer therapy](#oncology-and-adaptive-cancer-therapy)
    - [Immunology, inflammation, and autoimmune disease](#immunology-inflammation-and-autoimmune-disease)
    - [Other PK/PD and quantitative systems pharmacology applications](#other-pkpd-and-quantitative-systems-pharmacology-applications)
  - [Clinical operations and treatment delivery](#clinical-operations-and-treatment-delivery)
    - [Dose scheduling, adherence, and monitoring](#dose-scheduling-adherence-and-monitoring)
    - [Hospital and critical-care workflows](#hospital-and-critical-care-workflows)
    - [Digital health and closed-loop care](#digital-health-and-closed-loop-care)
  - [Biomanufacturing and industrial biotechnology](#biomanufacturing-and-industrial-biotechnology)
  - [Energy systems and power grids](#energy-systems-and-power-grids)
  - [Supply chains, logistics, and operations](#supply-chains-logistics-and-operations)
  - [Ecosystems, agriculture, and environmental management](#ecosystems-agriculture-and-environmental-management)
  - [Infrastructure, robotics, and engineered systems](#infrastructure-robotics-and-engineered-systems)
    - [Postural control, locomotion, and sensorimotor behavior](#postural-control-locomotion-and-sensorimotor-behavior)
  - [Specific labs and authors](#specific-labs-and-authors)
    - [Jeka and Kiemel: human postural control and locomotion](#jeka-and-kiemel-human-postural-control-and-locomotion)
    - [Ahrens Lab: whole-brain zebrafish sensorimotor behavior](#ahrens-lab-whole-brain-zebrafish-sensorimotor-behavior)
    - [Cowan and the LIMBS Laboratory: locomotion, active sensing, system identification, and hybrid mechanics](#cowan-and-the-limbs-laboratory-locomotion-active-sensing-system-identification-and-hybrid-mechanics)
    - [Fortune: feedback control, locomotor variability, and active sensing in weakly electric fish](#fortune-feedback-control-locomotion-variability-and-active-sensing-in-weakly-electric-fish)
    - [Hines and the NEURON ecosystem: neural and network simulation with events, discontinuities, and multiscale control](#hines-and-the-neuron-ecosystem-neural-and-network-simulation-with-events-discontinuities-and-multiscale-control)
- [Domains where `hybrid-ds-julia` would be less helpful](#domains-where-hybrid-ds-julia-would-be-less-helpful)
  - [Why these settings are difficult](#why-these-settings-are-difficult)
  - [Some infectious and post-infectious conditions](#some-infectious-and-post-infectious-conditions)
    - [Long COVID](#long-covid)
    - [Persistent symptoms following Lyme disease treatment](#persistent-symptoms-following-lyme-disease-treatment)
  - [ME/CFS](#mecfs)
  - [Mental health and complex behavioral care](#mental-health-and-complex-behavioral-care)
  - [What remains appropriate in difficult settings](#what-remains-appropriate-in-difficult-settings)
- [Example applications](#example-applications)
- [Crop motivation and software plan](#crop-motivation-and-software-plan)
- [Roadmap and licensing](#roadmap-and-licensing)
- [Further reading](#further-reading)
  - [Hybrid-systems foundations, events, and sensitivity analysis](#hybrid-systems-foundations-events-and-sensitivity-analysis)
  - [Pharmaceutical development and translational medicine](#pharmaceutical-development-and-translational-medicine-1)
  - [Clinical operations and treatment delivery](#clinical-operations-and-treatment-delivery-1)
  - [Biomanufacturing and industrial biotechnology](#biomanufacturing-and-industrial-biotechnology-1)
  - [Energy systems and power grids](#energy-systems-and-power-grids-1)
  - [Supply chains, logistics, and operations](#supply-chains-logistics-and-operations-1)
  - [Ecosystems, agriculture, and environmental management](#ecosystems-agriculture-and-environmental-management-1)
  - [Infrastructure, robotics, and engineered systems](#infrastructure-robotics-and-engineered-systems-1)
  - [Specific labs and authors](#specific-labs-and-authors-1)
  - [Domains where mechanistic hybrid modeling is more limited](#domains-where-mechanistic-hybrid-modeling-is-more-limited)

## Overview

Many scientific and engineering systems evolve continuously most of the time but change qualitatively when discrete events occur. A drug concentration may decay continuously until the next dose. A toxicity state may rise until treatment is held. A tumor may evolve under one therapy until surveillance triggers a treatment holiday or switch. A manufacturing process may follow mass-balance dynamics until a feed change, harvest, fault, or cleaning transition. A robot or animal may follow continuous dynamics until contact, lift-off, a perturbation, or a controller switch.

These are hybrid dynamical systems: systems combining continuous-time dynamics with explicit discrete events, mode changes, thresholds, and reset maps.

`hybrid-ds-julia` aims to make this structure explicit and reproducible. Rather than hiding treatment schedules, policy thresholds, or mode changes in ad hoc code, a model should state:

- The continuous state variables and their governing equations;
- The model parameters and inputs;
- The discrete modes that change the governing dynamics;
- The scheduled and state-triggered event conditions;
- The reset maps, parameter changes, or policy changes caused by events;
- The observations, objectives, and constraints used for analysis.

The project is intended to add value on two complementary levels.

First, it is **domain-facing**. It provides conventions and workflows for applying hybrid dynamical-systems methods to precision medicine and targeted problems in basic biological research. In these settings, continuous biological dynamics must be integrated with scientifically meaningful events such as interventions, dosing, threshold crossings, treatment holds, protocol transitions, and changes in experimental condition.

Second, it is **methodological**. The project aims to provide event-aware sensitivity propagation and optimization for hybrid dynamical systems in Julia. These capabilities are important because a parameter or decision variable can affect not only the continuous trajectory between events, but also the time at which an event occurs, the state reset applied at that event, and the discrete mode entered afterwards. Correctly propagating these effects is necessary for reliable parameter estimation, gradient-based optimization, optimal control, uncertainty analysis, and model-based reinforcement learning.

This second contribution is potentially useful across application domains, including engineering, robotics, energy systems, biology, and medicine. Accordingly, `hybrid-ds-julia` is intended to be domain-facing without being domain-limited: its initial biological applications motivate and validate the software, while its event-aware numerical methods may be reusable whenever a Julia hybrid-systems model requires sensitivity analysis or optimization.

The project is designed to complement, rather than replace, Julia's existing ecosystem. General-purpose tools already provide differential-equation solvers, automatic differentiation, sensitivity methods, optimization, and reachability analysis. `hybrid-ds-julia` addresses the integration problem that arises when these tasks must be performed through hybrid events, including event-time dependence, guard conditions, reset maps, and mode transitions. Its contribution is therefore a hybrid-event-aware layer and workflow, together with application-specific utilities where needed.

The initial motivation is hybrid QSP and PK/PD modeling, especially models involving repeated dosing, adherence scenarios, treatment interruptions, treatment holds, toxicity thresholds, monitoring rules, and adaptive interventions. The same formal structure can be useful in other areas when the continuous state, event semantics, and decision problem are sufficiently well specified.

## Project goals

The project is intended to support a progression from transparent simulation to progressively more demanding analysis.

Near-term goals include:

- Clear representations of continuous ODE dynamics, modes, guards, scheduled events, and reset maps;
- Reproducible event-aware simulation and event logging;
- Test beds involving dosing, threshold-triggered intervention, treatment holds, and therapy switching;
- Diagnostic tools for event timing, event order, repeated events, and numerical failure;
- A Julia-native workflow compatible with the broader SciML ecosystem where appropriate.

Longer-term goals include:

- Directional variational equations and forward parameter sensitivities;
- Saltation-aware event derivatives;
- Multiple shooting for long, unstable, or event-sensitive trajectories;
- Event-compatible adjoint methods where mathematically and numerically justified;
- Calibration, uncertainty quantification, constrained optimization, and policy comparison;
- Stochastic hybrid-system extensions, including uncertainty-aware event models, multistate transitions, and recurrent or competing clinical events where justified by data and scientific context;
- AI/ML and neural-network extensions to fit hybrid models to data, including model parameters, residual dynamics, latent states, observation models, or event-related components where appropriate;
- Model-based reinforcement-learning extensions to learn decision policies that select actions based on an expected long-term reward or utility structure, using the event-aware hybrid model for simulation, counterfactual trajectory evaluation, planning, or model-based policy learning. Candidate algorithms include Probabilistic Ensembles with Trajectory Sampling (PETS) and Model-Based Policy Optimization (MBPO);
- Model-free reinforcement-learning extensions to learn value functions or decision policies directly from observed or simulated hybrid-system trajectories, without requiring the policy-learning algorithm to invoke an explicit predictive dynamics model. These methods can provide comparative baselines or be useful when parts of the system dynamics are unknown, misspecified, or impractical to model explicitly. Candidate algorithms include Deep Q-Networks (DQN) and Advantage Actor--Critic (A2C);
- Parallel ensembles, distributed execution, and large-scale benchmarking;
- Carefully scoped applications in biomedical, scientific, and engineering domains.

The package should not be interpreted as a replacement for domain-specific simulators, clinical judgment, regulatory pharmacometrics, specialized power-system tools, detailed multibody robotics platforms, neural simulators, or validated production systems. Its intended role is complementary: a transparent framework for mechanistic ODE-and-event models when the user can state the relevant dynamics and transitions directly.

## Why hybrid models?

A smooth ODE model has the form:

$$
\dot{x}(t)=f(x(t),t,\theta),
$$

where \(x(t)\) is a continuous state and \(\theta\) is a parameter vector.

A hybrid model additionally has a discrete mode \(q(t)\), a time-varying input \(u(t)\), event conditions, and updates:

$$
\dot{x}(t)=f_{q(t)}(x(t),t,\theta,u(t)),
$$

where \(u(t)\) denotes an input that affects the system dynamics. Depending on the application, it may be an externally specified forcing signal, a scheduled intervention, or a control action. For example, \(u(t)\) may represent a drug infusion rate, dose schedule, environmental exposure, actuator command, or controller output. Later sections distinguish exogenous inputs, scheduled actions, and closed-loop actions selected by a policy.

For event \(i\), the model specifies a guard:

$$
g_i(x(t),q(t),u(t),t,\theta)=0,
$$

and event updates such as:

$$
x^+=R_i(x^-,q^-,u^-,t,\theta),
\qquad
q^+=T_i(q^-,x^-,u^-,t,\theta).
$$

The dependence on \(q^-\), \(u^-\), and \(\theta\) is shown explicitly because the event outcome may depend on the pre-event mode, the intervention then in effect, and fixed or patient-specific parameters; unnecessary arguments may be omitted in a particular model.

This framework can represent:

- An instantaneous bolus dose;
- An infusion start, stop, or rate change;
- A missed dose or adherence interruption;
- A treatment hold caused by toxicity;
- A treatment restart after a safety state recovers;
- A threshold-driven therapy switch;
- A contact or impact event;
- A controller transition;
- A failure, maintenance, or restoration event;
- A scheduled or state-triggered experiment perturbation.

The main benefit is not simply that discrete events can be simulated. It is that event conditions, event order, reset maps, and mode changes are explicit mathematical components of the model and can be logged, tested, analyzed, and—when conditions permit—differentiated or optimized.

## Why immuno-oncology first?

`hybrid-ds-julia` is intended to fill a domain-facing niche between general hybrid-systems software and applications in precision medicine and targeted basic research in biology. Its purpose is not only to provide a generic representation of continuous dynamics, discrete modes, guards, and reset maps. It is to make those concepts usable for biological and clinical models in which the events themselves have scientific meaning: dose administration, treatment interruption, immune activation, safety-threshold crossing, disease progression, treatment reassessment, and regimen change.

The initial application domain is tentatively immuno-oncology. This choice is strategic rather than exclusive: the software is intended to support additional biological and precision-medicine applications as the framework matures. Immuno-oncology provides a strong first test case because it combines continuous tumor--immune dynamics with treatment actions and clinically meaningful discrete events, while also offering an established mathematical-modeling literature from which initial benchmark problems can be drawn.

Several considerations motivate this initial focus.

1. **A documented hybrid-systems entry point.** The focused literature review identified a 2021 hybrid-systems formulation in immuno-oncology using mathematical analysis of a two-dimensional hybrid system. Such low-dimensional analytic methods can be highly informative, but they do not directly generalize to higher-dimensional patient-relevant models. Numerical simulation, event handling, sensitivity analysis, parameter estimation, and constrained optimization can remain applicable as state dimension and biological detail increase. In the literature review conducted to date, no later immuno-oncology work was identified that uses a comparable hybrid-systems formulation. This is a provisional literature-review finding, not a claim that no such work exists.

2. **Low-dimensional, analyzable models as test beds.** Existing tumor--immune and immunotherapy models with a small number of state variables have already received mathematical analysis. They provide strong initial test beds because known qualitative behavior, equilibria, stability properties, or treatment-response regimes can be used to verify simulation, event handling, reset logic, mode transitions, sensitivity calculations, and optimization workflows before moving to more complex models.

3. **Clear paths toward biologically relevant extensions.** The existing literature includes more realistic but less fully analyzed extensions, including drug resistance, combination chemotherapy with two or more drugs, and mixed immunotherapy--chemotherapy strategies. These extensions create natural opportunities to test whether an event-aware numerical framework can accommodate additional state variables, treatment actions, regimen-switching logic, and constraints without requiring a wholly new analytic treatment for every model extension.

4. **Potential practical relevance.** Expert input indicates that event-aware hybrid dynamical modeling could be useful in this domain. The intended initial role is methodological and research-oriented: transparent simulation, comparison of intervention rules, hypothesis generation, and eventual links to model-based optimization or reinforcement learning. It is not a claim that the framework is ready for clinical recommendation or autonomous treatment selection.

5. **The most scrutinized initial literature base.** To date, immuno-oncology is the application area whose relevant modeling literature has received the most detailed review and verification by the `hybrid-ds-julia` development effort. Starting from the best-understood literature base makes it possible to define reproducible benchmark models, document assumptions explicitly, and evaluate whether the framework adds value before broadening to other domains.

The first implementation goal is therefore to reproduce one or more well-characterized low-dimensional tumor--immune models, add clinically or biologically meaningful event dynamics, and compare numerical simulation and optimization results with known analytical behavior where such results are available. Subsequent versions can introduce resistance, multi-drug therapy, combination chemotherapy, and mixed immunotherapy--chemotherapy models.

## Intended users and use cases

The project is aimed at users who have or can formulate a mechanistic continuous-time model and need to represent events as part of the model rather than as informal external bookkeeping.

Potential users include:

- Researchers building PK/PD, QSP, infectious-disease, oncology, immunology, or treatment-control models;
- Scientists studying reduced-order models of physiology, behavior, sensorimotor control, or adaptation;
- Engineers working with event-driven process, energy, thermal, mechanical, or control models;
- Operations researchers whose systems include both meaningful continuous states and discrete decisions;
- Developers who need transparent event semantics, reproducible event logs, and sensitivity-aware hybrid simulation.

Potential questions include:

- How do different dosing or adherence schedules alter drug exposure and response?
- When should a threshold-triggered treatment hold be activated or released?
- How sensitive is a predicted event time to a parameter, initial condition, or measurement delay?
- When does a control or treatment policy become unstable, unsafe, or prone to chattering?
- How do alternative monitoring or switching rules compare under uncertainty?
- What measurements or perturbations best distinguish competing mechanistic hypotheses?

The package is not inherently appropriate merely because a problem has discrete events. It is most useful when the continuous state model, event logic, available measurements, and intended inference or decision problem can be stated and validated responsibly.
