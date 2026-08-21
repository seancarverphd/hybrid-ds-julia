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
- AI/ML and neural-network extensions to fit hybrid models to data, including model parameters, residual dynamics, latent states, observation models, or event-related components where appropriate;
- Model-based reinforcement-learning extensions to learn decision policies that select actions based on an expected long-term reward or utility structure, using the event-aware hybrid model for simulation, counterfactual trajectory evaluation, planning, or model-based policy learning. Candidate algorithms include Probabilistic Ensembles with Trajectory Sampling (PETS) and Model-Based Policy Optimization (MBPO);
- Model-free reinforcement-learning extensions to learn value functions or decision policies directly from observed or simulated hybrid-system trajectories, without requiring the policy-learning algorithm to invoke an explicit predictive dynamics model. These methods can provide comparative baselines or be useful when parts of the system dynamics are unknown, misspecified, or impractical to model explicitly. Candidate algorithms include Deep Q-Networks (DQN) and Advantage Actor--Critic (A2C);
- Parallel ensembles, distributed execution, and large-scale benchmarking;
- Carefully scoped applications in biomedical, scientific, and engineering domains.

The package should not be interpreted as a replacement for domain-specific simulators, clinical judgment, regulatory pharmacometrics, specialized power-system tools, detailed multibody robotics platforms, neural simulators, or validated production systems. Its intended role is complementary: a transparent framework for mechanistic ODE-and-event models when the user can state the relevant dynamics and transitions directly.

## Why hybrid models?

A smooth ODE model has the form:

\[
\dot{x}(t)=f(x(t),t,\theta),
\]

where \(x(t)\) is a continuous state and \(\theta\) is a parameter vector.

A hybrid model additionally has a discrete mode \(q(t)\), a time-varying input \(u(t)\), event conditions, and updates:

\[
\dot{x}(t)=f_{q(t)}(x(t),t,\theta,u(t)),
\]

where \(u(t)\) denotes an input that affects the system dynamics. Depending on the application, it may be an externally specified forcing signal, a scheduled intervention, or a control action. For example, \(u(t)\) may represent a drug infusion rate, dose schedule, environmental exposure, actuator command, or controller output. Later sections distinguish exogenous inputs, scheduled actions, and closed-loop actions selected by a policy.

For event \(i\), the model specifies a guard:

\[
g_i(x(t),q(t),u(t),t,\theta)=0,
\]

and event updates such as:

\[
x^+=R_i(x^-,q^-,u^-,t,\theta),
\qquad
q^+=T_i(q^-,x^-,u^-,t,\theta).
\]

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

## Mathematical approach

`hybrid-ds-julia` is intended for mechanistic dynamical models in which continuous-time evolution is interrupted or altered by explicit discrete events. The central modeling task is to make both components first-class objects: users specify the continuous right-hand side, the conditions under which events occur, the state or parameter updates caused by those events, and the quantities to be analyzed, calibrated, or optimized.

The package is motivated by models such as PK/PD and QSP systems with repeated dosing, treatment holds, toxicity thresholds, therapy switches, missed doses, adherence scenarios, and measurement-driven policies. The same mathematical structure applies more broadly to biological, clinical, industrial, ecological, and engineered systems.

### Continuous dynamics, modes, and events

A hybrid model contains a continuous state:

\[
x(t)\in\mathbb{R}^{n},
\]

and a discrete mode:

\[
q(t)\in\mathcal{Q}.
\]

Within a mode, the continuous state follows an ODE:

\[
\dot{x}(t)=f_{q(t)}\bigl(x(t),t,\theta,u(t)\bigr),
\]

where:

- \(x(t)\) is the continuous state;
- \(q(t)\) identifies the active mode;
- \(\theta\) is a parameter vector;
- \(u(t)\) represents scheduled inputs, external forcing, observations, or control actions.

The mode can encode, for example:

- Treatment on, held, tapered, or switched;
- Active versus inactive controller;
- Pre-contact versus post-contact mechanics;
- Batch, fed-batch, cleaning, or harvest phase;
- Normal, fault, islanded, or restoration grid state;
- Active, passive, exploratory, or recovery behavioral mode.

An event may occur at a known time, such as a scheduled dose or infusion start, or when a guard condition becomes true:

\[
g_i(x(t),t,\theta)=0.
\]

At an event, the model can update its state, parameters, input, or mode:

\[
x^+=R_i(x^-,t,\theta),
\]

\[
\theta^+=P_i(\theta^-,x^-,t),
\]

\[
q^+=T_i(q^-,x^-,t).
\]

The pre-event and post-event states are denoted by \(x^-\) and \(x^+\). A reset need not make the state discontinuous. It can leave \(x\) continuous while changing the governing right-hand side, active parameters, input schedule, or decision policy.

### Scheduled and state-triggered events

Scheduled events occur at known times:

\[
t=t_1,t_2,\ldots,t_K.
\]

Examples include:

- Oral doses;
- Infusion starts and stops;
- Laboratory draws;
- Planned treatment changes;
- Scheduled maintenance;
- Known stimulation pulses;
- Planned irrigation or feed changes.

State-triggered events occur when a continuous trajectory reaches a guard surface:

\[
g_i(x,t,\theta)=0.
\]

Examples include:

- A toxicity biomarker crossing a hold threshold;
- Tumor burden crossing an adaptive-treatment threshold;
- Battery charge reaching a dispatch limit;
- Temperature crossing a thermostat threshold;
- Foot contact with the ground;
- A balance variable crossing a stepping threshold;
- A pathogen or viral-load measurement reaching a treatment-switch criterion.

State-triggered events require event detection and root localization. Their timing depends on the state, parameters, inputs, and numerical trajectory. This dependence is central to hybrid sensitivity analysis, calibration, and optimization.

### Event maps and hybrid semantics

A useful hybrid model must specify more than an `if` statement. For each event, the model should make clear:

1. **Guard:** What condition triggers the event?
2. **Direction:** Does the event apply on an upward crossing, downward crossing, or either direction?
3. **Priority:** What happens if multiple guards are satisfied at the same time?
4. **Reset:** Which states, parameters, inputs, or modes change?
5. **Persistence:** Does the new mode remain active until another event occurs?
6. **Rearming:** Can the same event trigger immediately again?
7. **Termination:** Does the event end the simulation or merely change its future evolution?
8. **Observability:** Which event times, state values, and mode changes are logged?

Explicit event semantics are important for scientific reproducibility. A model should not rely on undocumented callback order, hidden mutable global state, or ambiguous treatment of simultaneous events.

### Hybrid trajectories and measurements

The state trajectory may be continuous, piecewise smooth, or discontinuous depending on the reset map. The derivative is commonly discontinuous at event times even when the state itself remains continuous.

A model may be linked to observations through a measurement equation:

\[
y_j=h_j(x(t_j),q(t_j),\theta)+\varepsilon_j,
\]

where \(y_j\) is an observation at time \(t_j\), \(h_j\) maps hidden state and mode to an observable quantity, and \(\varepsilon_j\) represents measurement noise or discrepancy.

This distinction matters in scientific applications. A model should separate:

- Directly measured quantities;
- Latent states inferred from measurements;
- Parameters estimated from data;
- Externally imposed events;
- State-triggered events;
- Assumptions that are not directly observable.

### Dosing, pulses, and treatment holds

A common PK/PD event is an instantaneous bolus dose. If \(A(t)\) is an amount in a compartment, a dose at time \(t_k\) can be represented as:

\[
A(t_k^+)=A(t_k^-)+D_k.
\]

An infusion can be represented by a mode-dependent forcing term:

\[
\dot{A}=\cdots+u_{\mathrm{infusion}}(t),
\]

with discrete events turning the infusion on, changing its rate, or turning it off.

A treatment hold may leave all biological states continuous while changing a treatment-rate parameter or input:

\[
u(t)=0
\quad\text{when}\quad
z(t)\geq z_{\mathrm{hold}},
\]

where \(z(t)\) is a toxicity or safety state. Treatment can later resume under a separate rule:

\[
u(t)=u_0
\quad\text{when}\quad
z(t)\leq z_{\mathrm{resume}}.
\]

Using distinct hold and resume thresholds creates hysteresis and can prevent rapid repeated switching near a single threshold.

### Threshold policies and mode-dependent control

Many hybrid models include decision policies. A general state-dependent policy may take the form:

\[
u(t)=\pi_{q(t)}\bigl(x(t),\hat{x}(t),t,\theta\bigr),
\]

where \(\hat{x}(t)\) may be an estimated state based on noisy or delayed observations.

Examples include:

- Hold treatment when toxicity exceeds a threshold;
- Escalate treatment when a biomarker remains above a threshold;
- Apply a corrective balance step when a stability margin is crossed;
- Dispatch energy storage when price and state of charge meet a rule;
- Switch HVAC mode when temperature crosses a hysteresis band;
- Start a feed phase when substrate concentration reaches a prescribed range.

The policy itself should be specified separately from the physical, biological, or operational plant where possible. This makes it easier to compare competing policies without rewriting the underlying state dynamics.

### Event logging and reproducibility

A hybrid solution should provide more than sampled trajectories. It should record an event log containing, at minimum:

- Event identifier;
- Event time;
- Pre-event mode and post-event mode;
- Guard value or event cause;
- Pre-event and post-event state values when relevant;
- Parameter or input changes;
- Whether the event was scheduled or state triggered;
- Solver status and any root-finding diagnostics.

For scientific and engineering use, the event log is part of the result. It allows users to verify that a treatment hold occurred when intended, distinguish an imposed dose from a state-triggered policy event, diagnose unexpected repeated events, and compare event sequences across parameter sets.

### Numerical considerations near events

Event-driven ODE simulation is not equivalent to integrating one smooth vector field over the whole horizon. Event handling requires attention to:

- Guard-function scaling;
- Event direction;
- Root-finding tolerances;
- Simultaneous or nearly simultaneous events;
- Reinitialization after state or parameter jumps;
- Discontinuous forcing;
- Rapid repeated events;
- Grazing trajectories;
- Event ordering;
- Mode consistency after reset.

A transversal event crosses its guard surface with nonzero rate:

\[
\frac{d}{dt}g_i(x(t),t,\theta)\neq 0.
\]

Such crossings are generally well behaved. A grazing event has approximately zero crossing rate:

\[
\frac{d}{dt}g_i(x(t),t,\theta)\approx 0.
\]

Near grazing, small parameter or state changes can create large changes in event time, event count, or event order. This can make gradients poorly conditioned or undefined in the ordinary smooth sense.

### Validation of hybrid models

Validation should address both continuous trajectories and discrete behavior.

For a proposed model, useful checks include:

- Do state units, parameters, and event maps have a consistent interpretation?
- Are scheduled doses or interventions applied at the intended times?
- Do guards trigger only in the intended direction?
- Are threshold policies protected against unintended chattering?
- Does event order remain stable under small numerical-tolerance changes?
- Are state resets physically, biologically, or operationally defensible?
- Are event times and post-event states reproducible?
- Does the model reproduce held-out trajectories, events, or outcomes?
- Does an alternative mechanism explain the observations equally well?

Model fit alone is insufficient. A model can reproduce observed trajectories while assigning them to the wrong latent mechanism, especially when hidden states are weakly measured or confounded.

## Computational scaling, event complexity, and practical compute budgets

This section is for users planning a substantial simulation, calibration, sensitivity-analysis, optimization, control, or uncertainty-quantification workflow. It explains how computational requirements depend on state dimension, parameter dimension, event count, event geometry, solver choices, and the repeated-evaluation demands of the intended task.

This README is intentionally modular. Readers who need only a small event-aware simulation can skip much of this section. Readers planning high-dimensional models, gradient-based inference, multiple shooting, event-aware optimization, or cloud-scale parameter studies should use this section to select an appropriate numerical formulation before investing substantial implementation or compute time.

The central point is:

> The difficulty of a hybrid model is not determined by state dimension alone. It depends on the interaction among continuous dynamics, parameter dimension, event frequency, event conditioning, derivative requirements, solver behavior, and the number of repeated simulations required by the intended workflow.

### Model notation and baseline cost

Consider a mode-dependent hybrid ODE:

\[
\dot{x}(t)=f_{q(t)}\bigl(x(t),t,\theta,u(t)\bigr),
\]

where:

- \(x(t)\in\mathbb{R}^{n}\) is the continuous state vector;
- \(n\) is the number of continuous state variables;
- \(q(t)\) is a discrete mode;
- \(\theta=(\theta_1,\ldots,\theta_p)\in\mathbb{R}^{p}\) is the parameter vector;
- \(p\) is the number of scalar parameters whose effects may be analyzed, estimated, or optimized.

Depending on the application, \(\theta\) may include kinetic rates, PK/PD parameters, initial-condition parameters, controller gains, event thresholds, reset-map parameters, dose sizes, or policy parameters.

Let:

- \(m\) be the number of realized events during one simulated trajectory;
- \(G\) be the number of guard functions evaluated for state-triggered events;
- \(N\) be the number of accepted time-integration steps;
- \(r\) be the number of intervals in a multiple-shooting formulation;
- \(C_f\) be the cost of evaluating the continuous right-hand side \(f_q\);
- \(C_{\mathrm{root}}\) be the additional cost of locating one state-triggered event;
- \(C_{\mathrm{reset}}\) be the cost of executing its reset, mode change, and associated bookkeeping.

For a nominal hybrid simulation without derivative propagation, define the first-order bookkeeping cost:

\[
C_{\mathrm{solve}}
:=
N C_f
+
m\left(C_{\mathrm{root}}+C_{\mathrm{reset}}\right).
\]

This is the approximate cost of one **forward solve**. It is not a complete solver-performance model. In particular, it omits or absorbs into the constants:

- Rejected adaptive steps;
- Dense interpolation;
- Guard-function evaluation;
- Explicit Jacobian construction;
- Sparse factorization or preconditioning;
- Linear solves for implicit methods;
- Memory allocation;
- Compilation time;
- Disk I/O and checkpointing;
- Parallelization overhead;
- Numerical difficulty near discontinuities.

Scheduled events—such as a known dose at a known time—are often cheaper than state-triggered events because their times are supplied directly. A threshold crossing requires detection and localization, and may force solver reinitialization.

### What makes an event difficult?

A state-triggered event is commonly defined by a guard:

\[
g_i(x(t),t,\theta)=0.
\]

When the event occurs, the model may apply a state reset:

\[
x^+=R_i(x^-,t,\theta),
\]

change parameters,

\[
\theta^+=P_i(\theta^-,x^-,t),
\]

or change the active mode:

\[
q^+=T_i(q^-,x^-,t).
\]

The vector field may therefore switch from:

\[
\dot{x}=f_{q^-}(x,t,\theta)
\]

to:

\[
\dot{x}=f_{q^+}(x,t,\theta).
\]

A hybrid event has three computational effects:

1. The solver must detect and localize the event time.
2. The model must execute the reset or mode change.
3. A derivative-aware method must account for the fact that perturbations can change both the event time and the post-event state.

The third effect is crucial. A parameter change can cause an event to occur earlier or later, causing the system to spend a different amount of time under the pre-event and post-event vector fields. This is why differentiating only the smooth ODE segments is not enough.

#### Transversal events

An event is transversal when:

\[
\frac{d}{dt}g_i(x(t),t,\theta)\neq 0.
\]

Such events are usually well behaved for root finding and first-order sensitivity analysis.

#### Grazing events

At a grazing event:

\[
\frac{d}{dt}g_i(x(t),t,\theta)\approx 0.
\]

Small changes in state or parameters can then produce large changes in event time, cause an event to appear or disappear, or alter event ordering. Grazing events can therefore create:

- Very small solver steps;
- Large, unstable, or undefined local sensitivities;
- Poor gradient-based optimization behavior;
- Ambiguous event classification;
- Scientific fragility in threshold-based policy conclusions.

This is not merely a numerical problem. It often means that the underlying intervention, contact, switching, or decision rule is structurally sensitive.

### Jacobians, variational flow, and \(O(n^2)\) state equations

There are two related but distinct \(n\times n\) objects.

The first is the **state Jacobian** of the vector field:

\[
J_x(t)
=
\frac{\partial f_q}{\partial x}
\bigl(x(t),t,\theta\bigr)
\in\mathbb{R}^{n\times n}.
\]

If dense, it has \(n^2\) entries. However, it is not automatically an additional set of \(n^2\) ODE states. A numerical method may form it explicitly, approximate it, exploit sparsity, use Jacobian-vector products, generate it by automatic differentiation, or avoid forming it in explicit methods.

The second object is the **state-transition matrix**, or Jacobian of the flow with respect to the initial condition:

\[
\Phi(t,t_0)
=
\frac{\partial x(t)}{\partial x(t_0)}
\in\mathbb{R}^{n\times n}.
\]

If the full state-transition matrix is propagated, it satisfies:

\[
\dot{\Phi}(t)
=
J_x(t)\Phi(t,t_0),
\qquad
\Phi(t_0,t_0)=I_n.
\]

This does introduce \(n^2\) additional scalar differential equations. Together with the original state equations, the augmented smooth system has:

\[
n+n^2
\]

continuous scalar states.

The full matrix \(\Phi\) is useful when a method needs derivatives of the flow with respect to **all** initial-state directions. Examples include:

- Dense multiple-shooting Jacobian blocks;
- Stability analysis;
- Floquet or Poincaré-map calculations;
- Full local linearization of a trajectory;
- Some Newton, sequential-quadratic-programming, and second-order methods;
- Sensitivity of a full terminal state with respect to a full initial state.

For a hybrid event, a first-order perturbation is updated through a saltation matrix or equivalent event derivative:

\[
\delta x^+
=
\Xi\,\delta x^-.
\]

Consequently,

\[
\Phi^+
=
\Xi\Phi^-.
\]

For dense matrices, directly multiplying two \(n\times n\) matrices costs:

\[
O(n^3)
\]

per event. This is a key distinction: a dense \(O(n^2)\) event update applies to one tangent vector or one adjoint vector, while propagation of the **full** state-transition matrix requires a dense matrix-matrix update.

#### Directional variational equations

Users should not propagate a full state-transition matrix by default.

If only one initial-condition direction is needed, propagate one tangent vector:

\[
v(t)
=
\frac{\partial x(t)}{\partial\alpha}
\in\mathbb{R}^{n},
\]

which satisfies:

\[
\dot{v}=J_xv.
\]

This requires only \(n\) additional differential equations. At an event:

\[
v^+=\Xi v^-.
\]

For dense \(\Xi\), this costs:

\[
O(n^2)
\]

per event.

More generally, propagating \(k\) selected tangent directions requires an \(n\times k\) matrix:

\[
V(t)\in\mathbb{R}^{n\times k},
\]

with:

\[
\dot{V}=J_xV.
\]

The added continuous-state dimension is then:

\[
nk,
\]

rather than:

\[
n^2.
\]

This is often preferable when only a few perturbation directions, control directions, or shooting-variable directions are needed.

### Forward parameter sensitivities

Parameter sensitivities are distinct from the initial-condition state-transition matrix. Define:

\[
S_\theta(t)
=
\frac{\partial x(t)}{\partial\theta}
\in\mathbb{R}^{n\times p}.
\]

On smooth intervals, the forward variational equations are:

\[
\dot{S}_\theta
=
J_xS_\theta
+
J_\theta,
\]

where:

\[
J_\theta
=
\frac{\partial f_q}{\partial\theta}
\in\mathbb{R}^{n\times p}.
\]

Propagating all forward parameter sensitivities therefore introduces:

\[
np
\]

additional scalar differential equations. Together with the original state equations, the augmented system has:

\[
n+np
=
n(1+p)
\]

continuous scalar states.

If both the full initial-condition transition matrix and all parameter sensitivities are required, then the augmented system contains:

\[
n+n^2+np
\]

continuous scalar states.

#### Dense cost

For dense dynamics, evaluation of:

\[
J_xS_\theta
\]

costs approximately:

\[
O(n^2p)
\]

per variational update. The sensitivity matrix itself requires:

\[
O(np)
\]

memory.

A rough dense cost model is:

\[
C_{\mathrm{forward\ sens}}
\approx
O\!\left(
N(C_f+n^2p)
+
m(C_{\mathrm{root}}+C_{\mathrm{reset}}+n^2p)
\right).
\]

At an event, the parameter sensitivity update has schematic form:

\[
S_\theta^+
=
\Xi S_\theta^-
+
B_{\theta},
\]

where \(B_\theta\) contains derivatives associated with explicit parameter dependence in the guard, reset map, or mode transition. It is generally not enough to use only:

\[
S_\theta^+=\Xi S_\theta^-.
\]

For a dense \(n\times p\) sensitivity matrix, the leading matrix multiplication cost at each event is approximately:

\[
O(n^2p).
\]

#### Sparse and structured models

Dense asymptotic estimates can substantially overstate cost when the model is sparse.

Let \(z\) be the number of nonzero entries of \(J_x\). A sparse product may cost closer to:

\[
O(zp)
\]

than:

\[
O(n^2p).
\]

Similarly, many hybrid resets are local. A dose may alter one compartment; a treatment hold may change one parameter; a contact event may affect a limited subset of velocity components. If event derivatives are sparse, block structured, or low rank, their updates can be much cheaper than dense worst-case formulas imply.

For a large model, the useful questions are therefore:

- How many state variables are there?
- How many parameters are differentiated?
- Is the Jacobian sparse?
- How many guard functions are active?
- How many state variables does each reset affect?
- Is the event update local, sparse, or low rank?
- Are full matrices required, or only matrix-vector products?

#### When forward sensitivities are useful

Forward sensitivities are commonly attractive when the parameter count is modest:

\[
p\ll n,
\]

or more generally when only a small number of parameters need derivatives.

Examples include:

- Dose amount, dose interval, or infusion rate;
- A few PK/PD rate constants;
- A toxicity threshold;
- A handful of controller gains;
- An event threshold or reset parameter;
- Local sensitivity analysis of a calibrated model.

Forward methods are also useful during early model development because they can be inspected and compared with carefully selected finite perturbations away from events.

### Saltation-aware hybrid derivatives

At an event, classical smooth variational propagation is incomplete because perturbations change event timing.

For a transition from mode \(I\) to mode \(J\), a saltation matrix has schematic form:

\[
\Xi
=
D_xR
+
\frac{
\left(
f_J
-
D_xR\,f_I
-
D_tR
\right)
D_xg
}{
D_tg+D_xg\,f_I
}.
\]

The exact formula depends on event convention, guard, reset map, and time dependence. The denominator:

\[
D_tg+D_xg\,f_I
\]

is the instantaneous rate of crossing the event surface.

When that denominator is near zero, the event is near grazing and hybrid sensitivities can become large, ill-conditioned, or undefined in the ordinary differentiable sense.

| Carried derivative object | Shape | Event update | Dense direct cost per event |
|---|---:|---:|---:|
| One tangent direction \(v\) | \(n\times 1\) | \(v^+=\Xi v^-\) | \(O(n^2)\) |
| \(k\) tangent directions \(V\) | \(n\times k\) | \(V^+=\Xi V^-\) | \(O(n^2k)\) |
| Full state-transition matrix \(\Phi\) | \(n\times n\) | \(\Phi^+=\Xi\Phi^-\) | \(O(n^3)\) |
| Parameter sensitivity matrix \(S_\theta\) | \(n\times p\) | \(S_\theta^+=\Xi S_\theta^-+B_\theta\) | \(O(n^2p)\) |
| One adjoint vector \(\lambda\) | \(n\times 1\) | \(\lambda^-=\Xi^\top\lambda^+\) | \(O(n^2)\) |

These are dense worst-case costs. Sparse, local, low-rank, and matrix-free structures can reduce them substantially.

### Automatic differentiation

Automatic differentiation, or AD, is valuable for computing derivatives of smooth right-hand sides, reset maps, objectives, and numerical kernels. It does not automatically guarantee a correct hybrid derivative.

For example, an informal branch:

```julia
if g(x, t) <= 0
    apply_reset!()
end
```

does not by itself ensure that differentiation accounts for how a change in \(\theta\) shifts the time when the guard becomes zero.

For state-triggered hybrid events, a correct derivative generally needs:

- The smooth derivative before the event;
- The derivative of the guard;
- The derivative of event time;
- The derivative of the reset map;
- The vector-field change after the event.

AD may still be part of a correct implementation. For example, it can generate \(J_x\), \(J_\theta\), guard derivatives, reset derivatives, and discrete-adjoint calculations. But it should not be described as a replacement for hybrid sensitivity theory.

### Adjoint sensitivities

Suppose the objective is scalar:

\[
\mathcal{L}
=
\ell_T(x(T),\theta)
+
\sum_{j=1}^{m}
\ell_j(x(t_j^-),x(t_j^+),\theta).
\]

Examples include:

- Final tumor burden plus cumulative toxicity;
- Negative log likelihood of longitudinal data;
- Tracking error plus energy cost;
- Total time below a therapeutic threshold;
- Total process yield minus operating cost;
- A control objective with penalties for interventions or mode switches.

An adjoint method propagates a vector:

\[
\lambda(t)\in\mathbb{R}^{n}
\]

backward through the trajectory.

For a scalar objective, its key advantage is that the active derivative state is \(O(n)\), rather than \(O(np)\). The method does not carry a separate state-sensitivity column for every parameter.

A useful planning relation is:

\[
C_{\mathrm{adjoint}}
\approx
\alpha C_{\mathrm{solve}}
+
C_{\mathrm{checkpoint}}
+
mC_{\mathrm{event\ adjoint}},
\]

where:

- \(C_{\mathrm{solve}}\) is the nominal forward-solve cost defined above;
- \(\alpha\) is a practical constant capturing backward integration, replay, interpolation, and derivative work;
- \(C_{\mathrm{checkpoint}}\) is memory, storage, or recomputation cost;
- \(C_{\mathrm{event\ adjoint}}\) is the cost of reverse propagation across each event.

The constant \(\alpha\) is not generally one. Adjoint methods exchange dependence on parameter count for trajectory storage, checkpointing, replay, and event-adjoint complexity.

#### When adjoints are attractive

Adjoints are usually attractive when:

\[
p\gg 1,
\]

and the objective is scalar or low dimensional.

Examples include:

- Large parameter-estimation problems;
- Gradient-based calibration;
- Optimal experimental design;
- Policy optimization;
- Neural-network or high-dimensional surrogate parameters;
- Repeated optimization of a scalar cost.

#### Hybrid adjoint requirements

A hybrid adjoint must traverse every event correctly in reverse time. It must account for:

- Event-time dependence;
- Reset-map derivatives;
- Mode changes;
- Objective terms at events;
- Event ordering;
- Terminal events;
- Simultaneous events;
- Checkpointing around discontinuities;
- Reproducibility of the nominal event sequence.

Adjoints may not be the best first method when:

- Only a few parameters matter;
- Events are frequent;
- The event sequence changes under small perturbations;
- Grazing or chattering occurs;
- The model is strongly stiff;
- The objective is high dimensional;
- The event semantics are still being developed;
- Reliable debugging matters more than asymptotic speed.

A practical progression is:

1. Validate the nominal event-driven solve.
2. Implement and test a small forward or directional sensitivity calculation.
3. Check selected derivatives against perturbation calculations away from events.
4. Add explicit hybrid event-derivative handling.
5. Introduce adjoints only when parameter dimension or repeated evaluations justify their added complexity.

### Multiple shooting

Single shooting integrates from one initial condition across the full time horizon. It can be effective for short, stable trajectories. It can become poorly conditioned when trajectories are long, unstable, stiff, highly sensitive, or repeatedly reset.

Multiple shooting divides the time horizon into \(r\) intervals and introduces a state variable at each boundary:

\[
z_i\approx x(t_i),
\qquad
i=0,\ldots,r-1.
\]

Each interval is propagated independently. Continuity conditions enforce:

\[
c_i(z_i,z_{i+1},\theta)
=
\Phi_i(z_i,\theta)-z_{i+1}
=
0,
\]

where \(\Phi_i\) is the hybrid flow map over interval \(i\).

#### Problem dimension

The shooting-state decision variables have approximate dimension:

\[
rn.
\]

The continuity constraints have approximate dimension:

\[
(r-1)n.
\]

With \(p\) global parameters, the decision-vector dimension is approximately:

\[
rn+p.
\]

Thus multiple shooting trades:

\[
\text{a larger constrained optimization problem}
\]

for:

\[
\text{better conditioning and local control of trajectory mismatch}.
\]

#### Dense flow-map derivatives

A dense Newton or SQP method may require:

\[
A_i
=
\frac{\partial\Phi_i}{\partial z_i}
\in\mathbb{R}^{n\times n}.
\]

These are segment-level state-transition matrices. Retaining them across all shooting intervals requires approximately:

\[
O(rn^2)
\]

storage.

If derivatives with respect to parameters are retained:

\[
B_i
=
\frac{\partial\Phi_i}{\partial\theta}
\in\mathbb{R}^{n\times p},
\]

the additional storage is approximately:

\[
O(rnp).
\]

For dense models, if a full state-transition matrix is propagated and updated at each event, the naive event-update work can be approximately:

\[
O(mn^3).
\]

This is one reason that large-scale multiple-shooting methods often use sparse Jacobian representations, block-sparse continuity constraints, Jacobian-vector products, adjoint-vector products, matrix-free Krylov solvers, condensing, low-rank update structure, carefully selected segment boundaries, or reduced-order models.

#### Why multiple shooting can help

Multiple shooting is useful when:

- Long horizons amplify unstable directions;
- Small parameter changes create large trajectory changes;
- The model has multiple time scales;
- A fit must match measurements at intermediate times;
- Repeated events make full-horizon single shooting poorly conditioned;
- The optimizer starts far from a feasible trajectory;
- Different portions of the trajectory follow different modes.

For hybrid models, useful segment boundaries may occur at:

- Scheduled doses or interventions;
- Data collection times;
- Known controller mode changes;
- Expected gait or contact phases;
- Known process phase changes;
- Before and after particularly sensitive threshold regions.

Unknown state-triggered events may remain inside a shooting interval. Treating their times as explicit decision variables is possible, but adds event-consistency and transversality constraints.

### Event count, event structure, and tractability

The number of events \(m\) matters, but event conditioning and structure matter just as much.

#### Well-separated transversal events

If events are well separated and transversal, each event adds a bounded root-localization and reset cost. With a local or sparse reset, actual cost may be modest.

#### Grazing and event-sequence changes

If a parameter perturbation changes:

\[
A\rightarrow B\rightarrow C
\]

into:

\[
A\rightarrow C,
\]

then the trajectory can be differentiable within a fixed event sequence but nonsmooth across the boundary between sequences.

A gradient computed under the nominal event sequence may still be locally useful, but it should not be treated as globally reliable. Implementations should log and diagnose:

- Near-grazing crossings;
- Nearly simultaneous events;
- Changes in event count;
- Changes in event order;
- Repeated immediate events;
- Excessive root-finding iterations;
- Solver step collapse near a guard.

#### Chattering

Chattering occurs when a system repeatedly switches near the same event surface. Possible remedies, when physically justified, include:

- Hysteresis bands;
- Minimum dwell time;
- Refractory periods;
- Compliant or relaxation dynamics;
- Event aggregation;
- Smooth approximations for purely numerical switches;
- Differential-inclusion or complementarity formulations.

A model should not silently suppress chattering without recording that choice. The correct response depends on the domain mechanism.

### Dimension-specific planning guide

| Model regime | Reasonable first approach | Main scaling risk | Practical response |
|---|---|---|---|
| \(n\lesssim 50\), \(p\lesssim 20\), modest \(m\) | Direct simulation and directional/forward derivatives | Event correctness | Log events; validate selected derivatives |
| \(n\sim10^2\)–\(10^3\), \(p\ll n\), sparse dynamics | Sparse forward sensitivities | Jacobian products | Preserve sparsity; use matrix-free products where possible |
| \(n\sim10^2\)–\(10^4\), large \(p\), scalar objective | Event-aware adjoint | Checkpointing and event gradients | Validate on reduced benchmark cases |
| Long, unstable, or event-sensitive horizon | Multiple shooting | \(rn\) variables and block Jacobians | Segment at meaningful interventions or data times |
| Full stability or flow-map analysis | Full \(\Phi\) only if necessary | \(n^2\) states and \(O(n^3)\) dense event updates | Use directional products or reduced-order analysis if possible |
| Dense \(n\gtrsim10^3\), large \(p\) | Model reduction or specialized tools | Dense linear algebra | Exploit low rank, sparsity, locality, or surrogates |
| Frequent grazing/chattering | Nonsmooth or regularized formulation | Derivatives may fail | Reformulate events; use hysteresis or alternative methods |
| Primarily discrete operational problem | Discrete-event simulation or optimization | ODE machinery may add little | Use hybrid ODE methods only if a continuous state is central |

### Fixed-budget planning

A practical workflow consumes many more evaluations than one nominal simulation.

Let:

\[
K
\]

be the number of objective-and-gradient evaluations required by an optimizer, sampler, calibration procedure, uncertainty study, or experimental-design loop.

Then:

\[
C_{\mathrm{total}}
=
K C_{\mathrm{eval+grad}}.
\]

For a fixed computational budget \(B\):

\[
K C_{\mathrm{eval+grad}}
\leq B.
\]

A local optimization may require tens to hundreds of evaluations. Multistart optimization may require thousands. Bayesian calibration, posterior sampling, global search, or broad uncertainty quantification may require tens of thousands to millions.

If one objective-and-gradient evaluation costs 10 seconds, then:

\[
100{,}000
\times
10\ \mathrm{seconds}
=
1{,}000{,}000\ \mathrm{seconds},
\]

which is approximately:

\[
278\ \mathrm{single-worker\ hours}.
\]

Parallelization can reduce wall-clock time, but it does not reduce total compute consumption.

#### State dimension versus events under a fixed budget

Users commonly face tradeoffs among:

- More state variables;
- More parameters;
- More accurate event localization;
- More explicitly resolved events;
- Tighter solver tolerances;
- More optimization starts;
- More uncertainty samples;
- More sophisticated measurement models;
- More expensive derivatives;
- More detailed data assimilation.

Increasing \(n\) can increase ODE, Jacobian, linear-solver, and memory cost. Increasing \(p\) can dominate forward-sensitivity cost. Increasing \(m\) can increase root finding, resets, solver restarts, and derivative updates. Increasing \(K\) can dominate all per-solve costs.

A disciplined sequence is:

1. Start with the smallest state model that represents the mechanism of interest.
2. Include only events that meaningfully alter state, dynamics, parameters, or policy.
3. Validate nominal trajectories and event order.
4. Add a small, interpretable parameter set.
5. Benchmark representative objective-and-gradient evaluations.
6. Estimate the required number \(K\) of evaluations.
7. Then select cloud hardware and a compute budget.

### Illustrative AWS estimates

Cloud cost should be estimated from measured wall time on representative workloads, not from asymptotics alone.

For any EC2 instance with hourly price \(P_{\mathrm{hr}}\), the raw cost of a single objective-plus-gradient evaluation of duration \(t_{\mathrm{eval}}\) seconds is:

\[
\mathrm{cost/evaluation}
=
\frac{t_{\mathrm{eval}}}{3600}
P_{\mathrm{hr}}.
\]

AWS bills eligible EC2 usage in one-second increments with a 60-second minimum; actual cost depends on the selected region, operating system, instance family, storage, transfer, and purchase model. Use the AWS Pricing Calculator and current regional instance prices before committing to a large run.

For illustration only, if an instance costs:

\[
P_{\mathrm{hr}}=\$0.10/\mathrm{hour},
\]

then:

| Objective + gradient wall time | Raw compute cost |
|---:|---:|
| 1 second | $0.000028 |
| 10 seconds | $0.000278 |
| 1 minute | $0.00167 |
| 10 minutes | $0.0167 |
| 1 hour | $0.10 |

At this illustrative rate:

| Budget | Raw instance-hours | 10-second evaluations | 1-minute evaluations | 10-minute evaluations |
|---:|---:|---:|---:|---:|
| $10 | 100 | 36,000 | 6,000 | 600 |
| $100 | 1,000 | 360,000 | 60,000 | 6,000 |
| $1,000 | 10,000 | 3.6 million | 600,000 | 60,000 |

These are arithmetic upper bounds, not performance guarantees. Real throughput can be lower because of Julia compilation and warm-up, failed integrations, event pathologies, checkpointing, disk I/O, data movement, peak-memory limits, queueing, optimizer overhead, imperfect parallel efficiency, and separately launched short-lived jobs.

For many short tasks, keep workers alive and batch evaluations rather than launching a new instance for every simulation.

### Benchmark before scaling

Before purchasing substantial cloud compute, benchmark a representative objective-and-gradient evaluation with:

- The intended state dimension \(n\);
- The intended parameter dimension \(p\);
- The intended number of guard functions \(G\);
- Representative realized event counts \(m\);
- The intended solver and tolerances;
- The intended stiff/nonstiff treatment;
- Dense, sparse, or matrix-free derivatives;
- The intended forward, adjoint, or multiple-shooting method;
- Realistic data, objective, and output handling.

Record:

- Mean, median, and worst-case wall time;
- Accepted and rejected solver steps;
- Event counts and root-finding iterations;
- Peak memory;
- Event ordering and near-grazing diagnostics;
- Gradient-validation error on test cases;
- Failure rate;
- Parallel scaling efficiency;
- Expected number \(K\) of evaluations.

A nominal simulation that runs quickly can still lead to an impractical workflow if event-aware gradients are slow, optimization requires many restarts, or event sequences are unstable across candidate parameter values.

### Workflow recommendations

#### Exploratory simulation

For exploratory work:

- Prefer low-dimensional, interpretable states;
- Use scheduled events where timing is known;
- Log event times, guards, reset maps, and active modes;
- Plot guards near crossings;
- Perturb parameters slightly to inspect event-order stability;
- Validate event semantics before adding optimization.

#### Local sensitivity analysis

For local sensitivity analysis:

- Begin with a small parameter vector;
- Use directional or forward sensitivities when feasible;
- Compare selected derivatives with perturbation calculations away from guards;
- Record whether perturbations alter event time, count, or ordering;
- Treat grazing and sequence changes as model warnings rather than numerical noise.

#### Parameter estimation and optimization

For estimation and optimization:

- Use constrained low-dimensional parameterizations first;
- Use multiple shooting when long-horizon single shooting is poorly conditioned;
- Validate hybrid derivatives before trusting optimizer convergence;
- Record event sequences at candidate solutions;
- Penalize physically implausible parameter values and pathological switching;
- Use multistart, profile, or alternative-method checks where local minima are plausible.

#### Uncertainty quantification

For uncertainty quantification:

- Recognize that the number of evaluations may dominate cost;
- Parallelize independent trajectories where possible;
- Use sensitivity screening, surrogates, or reduced-order models where justified;
- Track uncertainty in event occurrence and event order, not only uncertainty in continuous parameters;
- Report failure modes and unidentifiable regions explicitly.

#### Policy optimization and control

For policy and control problems:

- Specify what information the policy sees and when;
- Distinguish scheduled from state-triggered actions;
- Include safety, intervention-frequency, and switching costs;
- Test robustness to measurement error, delay, missing data, and parameter uncertainty;
- Validate policies under held-out scenarios and alternative mechanistic assumptions.

### Scope and limitations

`hybrid-ds-julia` is intended to support transparent hybrid ODE models, explicit events, and progressively more sophisticated analysis. It should not imply that every event-rich model admits a stable, meaningful, inexpensive, or globally differentiable gradient.

Extra care is required for:

- Grazing events;
- Chattering or Zeno-like switching;
- Simultaneous events with ambiguous ordering;
- Discontinuous objectives;
- Event-sequence changes under small perturbations;
- Strong stiffness with frequent events;
- High-dimensional dense state models;
- Long-horizon unstable trajectories;
- Poorly measured or weakly identifiable parameters;
- Safety-critical or clinically consequential decision rules.

In these settings, model reduction, sparse or matrix-free methods, hysteresis, regularization, multiple shooting, derivative-free optimization, nonsmooth methods, robust control, or specialized domain software may be more appropriate than a straightforward gradient-based hybrid ODE workflow.

The relevant question is not only whether a model can be simulated once. It is whether its event logic, derivatives, numerical behavior, calibration assumptions, uncertainty, and computational requirements are understood well enough for the intended scientific, engineering, or decision-support use.

## Opportunities for parallelization

Hybrid models often contain substantial parallelism, but the most useful strategy depends on the level at which work is independent. In most applications, the highest-value and lowest-risk parallelism is **across complete trajectories**: different parameter vectors, initial conditions, subjects, experimental scenarios, Monte Carlo draws, optimization starts, or candidate policies can be simulated independently.

This distinction matters because one hybrid trajectory usually has a sequential causal structure. A state-triggered event must be detected before its reset is applied, and the post-event state determines all later continuous evolution and future events. Therefore, a single event-rich trajectory rarely parallelizes as easily as a large collection of independent trajectories.

The recommended order of implementation is:

1. Parallelize independent simulations first.
2. Parallelize objective components, data partitions, or shooting intervals where mathematically valid.
3. Exploit sparse linear algebra and threaded linear solvers inside individual large simulations.
4. Consider GPUs only when the problem has sufficiently many uniform, compatible trajectories or large data-parallel kernels.
5. Use multi-node parallelism only after measuring single-node performance and identifying a genuine scaling bottleneck.

### Parallelism levels

| Level | Parallel work unit | Typical use | Main limitation |
|---|---|---|---|
| Across trajectories | One complete simulation | Ensembles, parameter sweeps, Monte Carlo, multistart optimization | Usually the best first target |
| Across objective terms | Independent subjects, experiments, or data blocks | Population calibration, cross-validation, likelihood evaluation | Shared parameters require reduction of results |
| Across shooting intervals | Segment integrations | Multiple shooting, long horizons | Continuity constraints couple segments |
| Within one solve | Linear algebra, Jacobian products, large RHS evaluations | Large sparse or PDE-discretized models | Event handling remains sequential |
| Across derivative directions | Tangent directions or selected columns | Small batches of directional sensitivities | Memory grows with directions |
| Across optimizer candidates | Population methods, multistart, Bayesian sampling | Global search and robustness studies | Uneven event-rich trajectories cause load imbalance |
| On GPUs | Many compatible trajectories or kernels | Monte Carlo, parameter sweeps, batched small ODEs | Dynamic callbacks and divergent event paths can reduce efficiency |

### Embarrassingly parallel trajectory ensembles

The simplest and often most effective strategy is to run complete hybrid trajectories independently.

Examples include:

- Different parameter vectors in a parameter sweep;
- Different initial conditions;
- Different dose schedules or treatment policies;
- Different adherence realizations;
- Different patients or virtual subjects;
- Different perturbation protocols;
- Different weather, demand, or disturbance realizations;
- Monte Carlo samples;
- Bootstrap replicates;
- Multistart optimization candidates;
- Cross-validation folds;
- Posterior samples or likelihood evaluations;
- Candidate experimental designs.

If trajectory \(k\) solves:

\[
\dot{x}_k=f_{q_k}(x_k,t,\theta_k),
\]

with its own event sequence, initial condition, parameter vector, or random seed, then it can normally run independently of all other trajectories.

If one trajectory has cost \(C_{\mathrm{solve}}\), and there are \(L\) independent trajectories, the total serial work is approximately:

\[
L C_{\mathrm{solve}}.
\]

With \(W\) effective workers, the ideal wall time is:

\[
T_{\mathrm{ideal}}
\approx
\frac{L C_{\mathrm{solve}}}{W}.
\]

Actual speedup is lower because of worker startup and compilation, unequal trajectory runtimes, different event counts, failed trajectories, memory contention, data transfer, result aggregation, and serial portions of optimization or orchestration.

A useful practical model is:

\[
T_{\mathrm{wall}}
\approx
\frac{L\overline{C}_{\mathrm{solve}}}{W}
+
T_{\mathrm{overhead}}
+
T_{\mathrm{imbalance}},
\]

where \(T_{\mathrm{imbalance}}\) reflects the fact that event-rich or stiff trajectories may take much longer than typical trajectories.

### Parallel parameter sweeps and scenario analysis

Parameter sweeps are particularly natural for hybrid models. A user may evaluate:

\[
\theta^{(1)},\theta^{(2)},\ldots,\theta^{(L)},
\]

or different schedules:

\[
u^{(1)}(t),u^{(2)}(t),\ldots,u^{(L)}(t).
\]

Each simulation can include its own event times, guard crossings, and reset sequence.

A treatment-model ensemble may vary initial disease burden, patient-specific PK parameters, adherence patterns, dose intervals, toxicity thresholds, resistance parameters, monitoring schedules, and treatment-switch rules. A locomotion ensemble may vary initial posture, sensory delay, feedback gains, ground-contact parameters, perturbation magnitude, stepping threshold, controller mode, and noise realization.

A parameter sweep is often more informative than optimizing one nominal model because it exposes regions where event count, event order, stability, or feasibility changes.

### Monte Carlo and uncertainty quantification

Monte Carlo simulations are generally trajectory-parallel.

Suppose uncertain parameters or disturbances are sampled as:

\[
\theta^{(k)}\sim\pi(\theta),
\qquad
k=1,\ldots,L.
\]

For each sample, a hybrid trajectory produces an output:

\[
y^{(k)}
=
\mathcal{H}\bigl(x^{(k)},q^{(k)},\theta^{(k)}\bigr).
\]

The resulting ensemble can estimate quantities such as:

\[
\mathbb{E}[y],
\qquad
\mathrm{Var}(y),
\qquad
\Pr(y\in\mathcal{A}),
\]

or the probability that a threshold, treatment hold, failure event, or unsafe state occurs.

Hybrid uncertainty quantification should report discrete uncertainty as well as continuous uncertainty. Useful outputs include:

- Probability that a treatment hold occurs;
- Distribution of event times;
- Probability of a specific event sequence;
- Probability of a controller mode switch;
- Probability of treatment failure;
- Distribution of event count;
- Probability that a trajectory enters a chattering regime.

For large ensembles, workers should use dynamic scheduling rather than equal-sized static blocks when trajectory costs are highly variable.

### Parallel multistart and population optimization

Many hybrid optimization problems are nonconvex because of nonlinear dynamics, multiple modes, threshold decisions, event-sequence changes, discontinuous feasibility boundaries, parameter nonidentifiability, or multiple stable attractors.

A robust workflow often uses multiple starting points:

\[
\theta_0^{(1)},\ldots,\theta_0^{(L)}.
\]

Each local optimization can run independently until its results are collected and compared.

This is an attractive use of distributed compute because the principal coupling occurs only at the beginning and end of each optimization run.

Examples include:

- Multistart parameter estimation;
- Comparing treatment-policy parameterizations;
- Searching controller-gain spaces;
- Optimizing alternative experimental protocols;
- Population-based evolutionary algorithms;
- Particle-swarm or CMA-ES style methods;
- Bayesian optimization with batch candidate evaluation;
- Independent MCMC chains.

For a population-based optimizer with \(L\) candidates per generation, the evaluation stage is often parallel:

\[
\mathcal{L}\bigl(\theta^{(1)}\bigr),
\ldots,
\mathcal{L}\bigl(\theta^{(L)}\bigr).
\]

The update from one generation to the next is usually synchronized, so the speedup depends on the slowest candidate evaluation in each generation.

### Parallel likelihoods, subjects, and experiments

Many inference objectives decompose across independent data units.

Suppose a shared parameter vector \(\theta\) is fitted to data from \(S\) subjects, experiments, sites, or trials:

\[
\mathcal{L}(\theta)
=
\sum_{s=1}^{S}
\mathcal{L}_s(\theta).
\]

If each subject or experiment has a conditionally independent trajectory:

\[
\dot{x}_s=f_{q_s}(x_s,t,\theta,\eta_s),
\]

then objective and gradient contributions can be computed independently:

\[
\mathcal{L}_s(\theta),
\qquad
\nabla_\theta\mathcal{L}_s(\theta).
\]

They are then reduced:

\[
\mathcal{L}(\theta)
=
\sum_{s=1}^{S}\mathcal{L}_s(\theta),
\]

\[
\nabla_\theta\mathcal{L}(\theta)
=
\sum_{s=1}^{S}\nabla_\theta\mathcal{L}_s(\theta).
\]

This is appropriate for population PK/PD analyses, multiple virtual patients, treatment arms, replicated animal experiments, movement trials, environmental sites, production batches, or building units.

Care is required if the model contains shared latent variables, global resource constraints, coupling among subjects, or a hierarchical statistical model that requires joint inference. In that case, simulation may still be parallel, but the inference or likelihood-reduction step may be more complicated.

### Multiple shooting and time-domain decomposition

Multiple shooting introduces a natural but limited form of time-domain parallelism.

Let the interval:

\[
[t_0,T]
\]

be divided into \(r\) shooting segments:

\[
[t_0,t_1],
[t_1,t_2],
\ldots,
[t_{r-1},T].
\]

Given tentative shooting-node states:

\[
z_0,z_1,\ldots,z_{r-1},
\]

the segment flows:

\[
\Phi_i(z_i,\theta)
\]

can be integrated independently.

The continuity residuals:

\[
c_i
=
\Phi_i(z_i,\theta)-z_{i+1}
\]

are then assembled.

This yields a parallel pattern:

1. Distribute segment integrations.
2. Compute local trajectory outputs and local derivative information.
3. Assemble continuity constraints and objective contributions.
4. Solve the coupled optimization or linearized correction problem.
5. Update shooting nodes and repeat.

The continuous segment solves parallelize, but the nonlinear-programming or linear-system solve that reconciles all continuity constraints remains coupled.

Multiple shooting can reduce wall time for large problems only if each segment is computationally substantial, communication and assembly overhead are modest, the optimizer exploits block sparsity, and event handling within each segment remains stable. It is not automatically beneficial for short inexpensive trajectories.

### Parallel directional derivatives

A full forward sensitivity matrix has shape:

\[
S_\theta
=
\frac{\partial x}{\partial\theta}
\in\mathbb{R}^{n\times p}.
\]

The \(p\) columns correspond to parameter directions. In principle, subsets of those columns can be propagated in parallel.

If the parameter set is divided into \(B\) blocks:

\[
\theta=
\left(
\theta^{[1]},
\theta^{[2]},
\ldots,
\theta^{[B]}
\right),
\]

then sensitivity blocks can be computed separately:

\[
S_\theta
=
\left[
S^{[1]}
\;
S^{[2]}
\;
\cdots
\;
S^{[B]}
\right].
\]

This can be useful when the state dimension is moderate, the parameter count is larger than one worker can handle efficiently, the event sequence is fixed and reproducible, and memory is sufficient.

However, this is often not the first parallelization target. Trajectory-level parallelism is usually simpler and has lower communication requirements.

A full state-transition matrix:

\[
\Phi(t,t_0)\in\mathbb{R}^{n\times n}
\]

can likewise be computed by propagating blocks of tangent directions. But if a dense full \(\Phi\) is required, the total amount of arithmetic remains large:

\[
O(n^3)
\]

for dense matrix-matrix updates at an event. Parallelism reduces wall time only if memory bandwidth, communication, and dense-linear-algebra implementation scale effectively.

### Parallelism inside one large trajectory

A single large hybrid trajectory may benefit from internal parallelism when continuous dynamics are high dimensional.

Possible sources include:

- Threaded right-hand-side evaluation;
- Sparse Jacobian construction;
- Parallel Jacobian-vector products;
- Parallel residual evaluation;
- Threaded sparse linear solves;
- Multithreaded dense BLAS/LAPACK operations;
- Parallel PDE spatial discretizations;
- GPU kernels for large vectorized state updates;
- Parallel observation-model evaluation;
- Parallel objective contributions at measurement times.

This form of parallelism is most promising when \(n\) is large and continuous-state updates have substantial arithmetic intensity.

It is less useful for small ODE systems with frequent scalar event logic. In that setting, synchronization, branching, cache effects, and task overhead can exceed the work performed per step.

Hybrid events constrain within-trajectory parallelism because they establish a temporal dependency:

\[
x(t^-)
\rightarrow
\text{event detection}
\rightarrow
x(t^+)
\rightarrow
\text{future trajectory}.
\]

No later segment of the same single-shooting trajectory can be finalized until event state and mode are known.

### Shared-memory threading

Julia supports shared-memory multithreading: multiple tasks may execute simultaneously on CPU threads while sharing one process memory space.

Shared-memory threading is appropriate when model data are naturally shared, trajectory calculations are relatively small, communication overhead should be minimal, or many independent simulations fit on one machine.

Important implementation considerations include:

- Avoid mutation of shared arrays from multiple trajectories;
- Give each trajectory independent state, cache, random-number generator, and output storage;
- Avoid global mutable state in callback functions;
- Do not rely on callback execution order across trajectories;
- Use reproducible per-trajectory random seeds when stochastic perturbations are present;
- Check whether the ODE solver, linear solver, and BLAS libraries are already using threads to avoid oversubscription.

Oversubscription occurs when outer trajectory threading and inner linear algebra threading both attempt to use all available cores. Benchmark combinations deliberately.

### Distributed-memory parallelism

Julia also supports distributed computing with multiple processes that have separate memory spaces. These processes can run on one machine or across multiple machines.

Distributed processes are appropriate when individual trajectories are moderately expensive, memory requirements exceed a single process or node, many simulations must run independently, failure isolation is useful, or a cluster or cloud environment is available.

Distributed execution introduces additional requirements:

- Serialize or package model code and dependencies consistently;
- Move only necessary data to workers;
- Avoid repeatedly transferring large immutable input data;
- Aggregate small summaries rather than complete time-series trajectories when possible;
- Save detailed trajectories to worker-local or object storage only when needed;
- Record package versions, solver options, random seeds, and hardware metadata;
- Design jobs to tolerate worker failure and restart.

For cloud runs, independent-trajectory workloads are usually better candidates for distributed parallelism than tightly coupled single-trajectory time-domain decomposition.

### GPU opportunities and limitations

GPUs are most attractive when many trajectories have similar numerical structure and can run in a batched, data-parallel fashion.

Good GPU candidates include:

- Large Monte Carlo ensembles;
- Parameter sweeps;
- Large collections of short, similarly structured trajectories;
- Batched initial-condition studies;
- GPU-compatible neural ODE or surrogate components;
- High-dimensional vectorized state updates;
- Large sparse or dense linear-algebra kernels;
- Ensemble uncertainty quantification.

Hybrid event logic creates GPU-specific challenges:

- Different trajectories may experience different event counts;
- Different trajectories may cross different guards;
- Root-finding iterations may differ;
- Branching can cause warp divergence;
- Dynamic allocation and arbitrary callback logic may not compile or perform well on GPU hardware;
- Event sequences may create irregular memory access;
- Some solvers, callbacks, AD paths, and linear algebra routines may not be GPU compatible.

Therefore, GPU acceleration should be treated as a later optimization step, not a default assumption.

> GPUs are most promising for large ensembles of similar trajectories with predictable event structure. CPUs are often simpler and more robust for a small number of irregular, stiff, event-rich trajectories.

### Load balancing for event-rich ensembles

Hybrid ensembles often have variable trajectory cost.

One trajectory might have:

\[
m=0
\]

events and finish quickly. Another may have:

\[
m\gg 1,
\]

many rejected steps, stiffness, a near-grazing threshold, or chattering. Static assignment of the same number of simulations to each worker can leave some workers idle while one worker processes difficult cases.

Use dynamic scheduling when run times vary substantially:

- Queue individual trajectories or small batches;
- Allow idle workers to request additional work;
- Use work-stealing or dynamic map scheduling where appropriate;
- Group simulations with similar expected cost only if that cost can be predicted reliably;
- Treat solver failures and event pathologies as first-class outcomes to log and reschedule or analyze.

For Monte Carlo work, collecting only summary statistics can improve scaling:

\[
\left(
\text{objective},
\text{event count},
\text{event times},
\text{terminal state},
\text{failure code}
\right),
\]

rather than retaining every state value at every solver time point for every realization.

### Reproducibility under parallel execution

Parallel execution can make results harder to reproduce unless the workflow is designed carefully.

For each trajectory, record:

- A deterministic trajectory identifier;
- Parameter vector;
- Initial condition;
- Random seed or random-number-generator state;
- Solver and tolerance configuration;
- Event/callback configuration;
- Package and Julia versions;
- Hardware and worker information;
- Event log;
- Outcome status and failure diagnostics.

A robust strategy is to derive a per-trajectory seed from a master seed and trajectory identifier:

\[
\mathrm{seed}_k
=
h(\mathrm{master\ seed},k),
\]

where \(h\) is a deterministic hash or seed-generation rule.

Do not rely on the order in which parallel tasks happen to finish. Completion order can vary across machines and runs even when individual numerical calculations are deterministic.

### AWS Batch and cloud orchestration

For large independent trajectory ensembles, AWS Batch array jobs are a natural cloud-execution pattern. An array job creates multiple child jobs from one submission; each child job can use its assigned array index to select a parameter block, replicate, optimization start, or simulation batch.

A practical array-job design is:

1. Build a container with a fixed Julia version, project environment, model code, and scripts.
2. Store immutable input data and parameter grids in object storage or package them with the job.
3. Assign each child job a deterministic subset of trajectory indices.
4. Write per-job summaries, diagnostics, and optional detailed outputs.
5. Run a final aggregation job after the array completes.
6. Record the container image digest, git commit, package manifest, and random-seed policy.

Multi-node parallel jobs are possible when one tightly coupled computation must span multiple machines, but they require distributed-communication libraries and more complex orchestration. They are generally not the first choice for independent hybrid trajectories.

### Parallelization strategy by workflow

| Workflow | Best first parallelization target | Usually avoid first |
|---|---|---|
| Parameter sweep | Independent parameter vectors | Distributed full state-transition matrices |
| Monte Carlo uncertainty analysis | Independent random draws | GPU use before checking event divergence |
| Population PK/PD simulation | Virtual patients or subjects | One tightly coupled multi-node solve |
| Multistart calibration | Independent starts | Parallelizing every small derivative column |
| Bayesian sampling | Independent chains or batched proposals | Shared mutable likelihood state |
| Multiple shooting | Segment solves and subject-level data blocks | Excessive segmentation of cheap trajectories |
| Large stiff sparse model | Threaded/sparse internal linear algebra | GPU migration without compatibility testing |
| Policy optimization | Candidate policies and scenarios | Assuming a single trajectory can be time-parallelized |
| Experimental design | Candidate designs and simulated replicates | Retaining every full trajectory unnecessarily |

### Recommended implementation sequence

A practical staged plan is:

1. **Make one trajectory correct.** Validate continuous dynamics, guard functions, reset maps, event ordering, and diagnostics.
2. **Make one trajectory reproducible.** Fix solver settings, seeds, data versions, and output schema.
3. **Benchmark one trajectory.** Measure wall time, memory, accepted/rejected steps, event count, and output size.
4. **Run a small threaded ensemble.** Test 2, 4, and 8 workers. Confirm numerical reproducibility and absence of shared-state errors.
5. **Measure speedup and memory.** Compare observed speedup with ideal scaling. Inspect whether event-rich trajectories create load imbalance.
6. **Move independent work to distributed processes or cloud jobs.** Do this when trajectories are expensive enough to justify process, machine, or container overhead.
7. **Consider GPU execution only after profiling.** Confirm that callbacks, event structure, solver choice, and model code are compatible and that trajectories are sufficiently uniform.
8. **Consider multi-node coupled parallelism only for proven bottlenecks.** Use it for large structured problems whose internal linear algebra or multiple-shooting formulation genuinely requires it.

### Scope and limitations

Parallelism reduces wall-clock time when work is independent or can be decomposed with limited communication. It does not remove underlying arithmetic, memory, event-handling, or numerical-conditioning costs.

In hybrid systems, the main limitations are structural:

- Events within one trajectory create temporal dependencies;
- Grazing and chattering can make some trajectories much more expensive than others;
- Event-sequence changes can complicate derivative calculations;
- GPU efficiency can fall when trajectories diverge in branches, event counts, or root-finding paths;
- Multiple shooting makes segment propagation parallel but retains globally coupled continuity constraints;
- Distributed computing adds serialization, scheduling, data-transfer, and reproducibility responsibilities.

The best initial use of parallel computing in `hybrid-ds-julia` is therefore likely to be reproducible ensembles of independent trajectories. More tightly coupled parallel methods should be introduced only where benchmarking shows that they solve a meaningful computational bottleneck.

## AI/ML mathematical extensions

The deterministic hybrid framework is intended to remain useful on its own. However, a natural longer-term direction is to combine mechanistic QSP and PK/PD models with machine-learning components when biological structure is partly known but key interactions, patient-specific effects, or unresolved mechanisms are not.

The goal is not to replace mechanistic pharmacology with black-box prediction. Instead, the opportunity is to preserve known biological, pharmacological, and clinical structure while learning limited parts of the model from data. In this setting, event-aware simulation and sensitivity propagation remain important because the learned component must coexist with dosing events, treatment holds, threshold-triggered decisions, therapy switches, and other discrete intervention logic.

Four related directions are particularly relevant:

- mechanistic--neural hybrid systems,
- physics-informed neural networks,
- neural hybrid automata,
- and neural jump stochastic differential equations.

Each presents a different balance between mechanistic interpretability, data requirements, uncertainty representation, and flexibility in representing unknown dynamics.

### Mechanistic--neural hybrid systems

A mechanistic--neural hybrid model retains a structured differential-equation model for the components that are biologically or pharmacologically understood, while using a neural network to represent an uncertain interaction, forcing term, correction, or model-discrepancy component.

A generic form is

\[
\dot{x}
=
f_{\mathrm{mech}}(x,t,\theta)
+
f_{\mathrm{NN}}(x,t,u,\phi),
\]

where:

- \(x\) is the mechanistic state,
- \(f_{\mathrm{mech}}\) is the known mechanistic model,
- \(u\) denotes interventions such as dose, schedule, or treatment state,
- \(f_{\mathrm{NN}}\) is a learned neural correction,
- \(\theta\) contains mechanistic parameters,
- and \(\phi\) contains neural-network parameters.

For QSP and PK/PD, the mechanistic component may describe drug disposition, receptor occupancy, tumor growth, immune-cell dynamics, cytokine production, or toxicity pathways. The neural component can then represent a partially known feedback mechanism, an omitted mediator, a context-dependent interaction, or a structured discrepancy between the mechanistic model and observed data.

A useful example is an immuno-oncology model in which the known system represents tumor burden, effector-cell dynamics, checkpoint-inhibitor exposure, and a toxicity biomarker. If the precise relationship between tumor microenvironment state and immune suppression is uncertain, a neural term could be used to model that interaction while keeping dosing, pharmacokinetics, known immune-cell processes, and toxicity-hold rules explicit.

For hybrid models, the neural component may also depend on the active regime:

\[
\dot{x}
=
f_i(x,t,\theta)
+
f_{\mathrm{NN},i}(x,t,u,\phi),
\]

where \(i\) identifies the current treatment mode. For example, one learned correction may apply during active therapy, another during a treatment holiday, and another after a toxicity-driven hold.

The role of `hybrid-ds-julia` would be to ensure that the learned and mechanistic components both participate in event-aware simulation and sensitivity analysis. A neural correction should not obscure the fact that the treatment rule itself is hybrid. If a toxicity threshold is crossed, the resulting hold or switch must still be represented by an explicit event surface and reset or mode-transition map.

Potential uses include:

- learning uncertain biological interactions while retaining known PK, dosing, and intervention structure,
- calibrating mechanistic models to longitudinal biomarker or tumor-burden data,
- identifying patient-specific deviations from an otherwise shared mechanistic model,
- learning context-dependent pharmacodynamic effects,
- and improving predictive accuracy without discarding mechanistic interpretability.

The main scientific challenge is identifiability. A neural network can absorb model mismatch, noise, or missing mechanisms, but if it is too flexible it can make mechanistic parameters difficult to interpret. Successful hybrid implementations will therefore need regularization, biologically informed architecture choices, constrained parameterizations, out-of-sample validation, and explicit tests of whether the learned component improves decision-relevant predictions rather than merely fitting observed trajectories.

### Physics-informed neural networks

Physics-informed neural networks, or PINNs, represent a state trajectory with a neural network and train that network using both observational data and a loss term that penalizes violations of the governing differential equations.

For a system

\[
\dot{x}
=
f(x,t,\theta),
\]

a neural approximation

\[
\hat{x}(t;\phi)
\]

can be trained by minimizing a loss of the form

\[
\mathcal{L}
=
\mathcal{L}_{\mathrm{data}}
+
\lambda_{\mathrm{ODE}}
\mathcal{L}_{\mathrm{ODE}}
+
\lambda_{\mathrm{IC}}
\mathcal{L}_{\mathrm{IC}}
+
\lambda_{\mathrm{event}}
\mathcal{L}_{\mathrm{event}},
\]

where:

- \(\mathcal{L}_{\mathrm{data}}\) measures agreement with observations,
- \(\mathcal{L}_{\mathrm{ODE}}\) penalizes violations of the continuous governing equations,
- \(\mathcal{L}_{\mathrm{IC}}\) enforces initial or boundary conditions,
- and \(\mathcal{L}_{\mathrm{event}}\) enforces jump, reset, or mode-transition conditions.

For hybrid QSP and PK/PD systems, the final term is essential. A model that learns a smooth trajectory through a bolus dose, treatment hold, threshold-triggered switch, or state reset may appear numerically adequate while failing to preserve the actual intervention logic that matters for interpretation and decision-making.

A hybrid PINN may therefore use separate neural representations for different time segments or modes:

\[
\hat{x}_1(t), \hat{x}_2(t), \ldots, \hat{x}_m(t),
\]

with matching conditions at event times. If an event occurs at time \(\tau_k\), the training loss can include:

\[
\hat{x}_{k+1}(\tau_k^+)
-
R_k\left(
\hat{x}_{k}(\tau_k^-),
\tau_k,
\theta
\right),
\]

so that the learned trajectory satisfies the prescribed jump map.

For state-triggered events, the model must also account for the event condition:

\[
h\left(
\hat{x}(\tau_k),
\tau_k,
\theta
\right)
=
0.
\]

This can be challenging because the event time itself may be unknown and depend on the learned trajectory. One approach is to represent event times as trainable variables; another is to use domain decomposition, with separate neural approximations on intervals whose boundaries correspond to detected or inferred events.

Within `hybrid-ds-julia`, PINN-related functionality would be most useful for inverse problems and sparse-data settings. Potential applications include:

- reconstructing latent biological states from sparse biomarker measurements,
- estimating patient-specific parameters from irregularly sampled clinical data,
- inferring unobserved immune or disease compartments,
- calibrating event-rich PK/PD models when direct simulation-based optimization is difficult,
- and combining mechanistic constraints with data-driven trajectory reconstruction.

PINNs are not automatically superior to conventional solver-based fitting. They can be difficult to train, sensitive to loss weighting, and challenged by stiffness, sharp transitions, discontinuities, and high-dimensional state spaces. For the present project, their value is likely to be greatest when they are used selectively—for example, to infer latent states or learn constrained corrections—rather than as a universal replacement for event-aware numerical integration.

### Neural hybrid automata

A hybrid automaton represents a system using discrete modes, continuous dynamics within each mode, and transitions between modes. A neural hybrid automaton extends this idea by allowing neural networks to learn part of the mode-dependent dynamics, transition conditions, reset maps, or mode-assignment logic from data.

A generic hybrid-automaton representation can be written as:

\[
q(t) \in \mathcal{Q},
\]

\[
\dot{x}
=
f_{q(t)}(x,t,\theta),
\]

with transitions

\[
q^- \rightarrow q^+
\]

when an event condition is satisfied, potentially accompanied by a reset map

\[
x^+
=
R_{q^-\rightarrow q^+}(x^-,t,\theta).
\]

In a neural hybrid automaton, one or more of these components may be learned:

\[
\dot{x}
=
f_{q,\mathrm{mech}}(x,t,\theta)
+
f_{q,\mathrm{NN}}(x,t,\phi),
\]

or the transition guard itself may be represented by a learned classifier or score function:

\[
h_{q^-\rightarrow q^+}(x,t;\phi)
=
0.
\]

For translational pharmacology, the discrete modes could represent clinically interpretable states such as:

- active treatment,
- reduced-dose treatment,
- treatment hold,
- recovery or monitoring,
- rescue therapy,
- relapse management,
- or post-progression treatment.

A neural component could then be used to learn which latent physiological conditions make a transition likely, which modes best describe observed treatment-response patterns, or how the continuous dynamics differ between modes.

For example, longitudinal real-world data may show that patients with apparently similar baseline covariates follow different toxicity and recovery trajectories after treatment interruption. A neural hybrid automaton could be used to learn whether those trajectories are better represented by distinct latent modes, while retaining explicit treatment rules and biologically interpretable state variables.

The advantage of this approach is that it can combine data-driven discovery with a model structure that remains aligned with actual treatment logic. Rather than learning an unrestricted recurrent predictor, the model still distinguishes continuous evolution from discrete decisions and regime changes.

The risks are substantial. Mode discovery can be non-identifiable; different combinations of modes, guards, and reset maps may fit the same data. In addition, a learned transition rule may be difficult to interpret clinically unless it is constrained by known protocol rules, toxicity criteria, or biological thresholds.

For `hybrid-ds-julia`, neural hybrid automata are therefore a longer-term direction. The package’s immediate contribution would be to provide robust representation and differentiation of known hybrid structure. Learned modes and transition rules should be added only where data support them and where their scientific role is clearly distinguishable from known intervention logic.

### Neural jump SDEs

Deterministic hybrid systems describe treatment schedules and state transitions clearly, but biological and clinical systems also contain stochasticity. Patient response, immune dynamics, adherence, measurement error, unobserved confounders, and timing variability can all produce behavior that is not well represented by a single deterministic trajectory.

A jump stochastic differential equation can be written as:

\[
dX_t
=
f(X_t,t,\theta)\,dt
+
g(X_t,t,\theta)\,dW_t
+
J(X_{t^-},t,\theta)\,dN_t,
\]

where:

- \(X_t\) is the stochastic state,
- \(f\) is the drift,
- \(g\) is the diffusion coefficient,
- \(W_t\) is a Wiener process,
- \(N_t\) is a counting process,
- and \(J\) describes the state change associated with a jump.

A neural jump SDE replaces one or more of these components with a neural-network parameterization:

\[
dX_t
=
f_{\mathrm{NN}}(X_t,t,\phi)\,dt
+
g_{\mathrm{NN}}(X_t,t,\phi)\,dW_t
+
J_{\mathrm{NN}}(X_{t^-},t,\phi)\,dN_t.
\]

For mechanistic pharmacology, a more interpretable approach is often to retain known structure and learn only selected components:

\[
dX_t
=
f_{\mathrm{mech}}(X_t,t,\theta)\,dt
+
g_{\mathrm{NN}}(X_t,t,\phi)\,dW_t
+
J_{\mathrm{mech/NN}}(X_{t^-},t,\theta,\phi)\,dN_t.
\]

The jump process may represent known scheduled dosing events, random treatment interruptions, toxicity-triggered state changes, hospitalization events, unobserved perturbations, or other abrupt changes in the disease or treatment process.

In a QSP or PK/PD context, neural jump SDEs could be useful for:

- representing between-patient variability beyond static random effects,
- modeling stochastic immune-cell or disease-state fluctuations,
- learning heterogeneous response dynamics from repeated longitudinal measurements,
- quantifying uncertainty in the timing and impact of treatment interruptions,
- and simulating distributions of outcomes under alternative dosing and monitoring policies.

The event-aware perspective remains important even in the stochastic setting. Scheduled doses, protocol-defined holds, and known therapy switches should not be treated as arbitrary random jumps merely because the overall model includes uncertainty. Instead, a model may include both deterministic intervention events and stochastic jumps:

\[
X^+
=
R_{\mathrm{scheduled}}(X^-,t,\theta)
\]

at known times, together with random jump processes for unplanned or latent events.

This separation helps preserve interpretability. It distinguishes actions taken by the treatment protocol from random biological or clinical disruptions.

The main limitations are computational. Inference for neural jump SDEs can be expensive, stochastic gradients can be noisy, and data may not identify the separate effects of drift, diffusion, jump intensity, and jump magnitude. These methods are therefore most appropriate after the deterministic hybrid core is well tested and after benchmark data sets establish whether stochastic structure improves decision-relevant predictions.

For `hybrid-ds-julia`, neural jump SDEs belong to a research-facing extension layer rather than the first implementation milestone. The package can nevertheless be designed so that its deterministic event abstractions—guards, reset maps, regime transitions, and event-aware sensitivities—form a coherent foundation for later stochastic and learned extensions.


## Test beds

The initial test beds should be scientifically recognizable, numerically demanding enough to demonstrate the value of hybrid methods, and small enough to support reproducible end-to-end workflows.

The purpose is not to claim immediate coverage of every QSP or PK/PD application. The purpose is to establish a sequence of examples in which event-aware simulation, variational equations, saltation updates, multiple shooting, and schedule-facing analysis can be validated and compared with simpler workflows.

The proposed sequence begins with a compact deterministic treatment model, expands to higher-dimensional biomedical systems, and then adds stochastic and Filippov-style benchmark problems.

### First biomedical target

The first flagship biomedical example should be an **immuno-oncology tumor–immune QSP model with pulsed dosing and toxicity-triggered treatment holds**.

A representative model can include states for:

\[
T(t) = \text{tumor burden},
\]

\[
E(t) = \text{effector immune-cell activity},
\]

\[
C(t) = \text{drug concentration},
\]

\[
B(t) = \text{toxicity or biomarker burden}.
\]

Between events, a compact model might have the form

\[
\dot{T}
=
r_T T
\left(
1-\frac{T}{K_T}
\right)
-
k_E E T,
\]

\[
\dot{E}
=
s_E
+
\alpha_E
\frac{T}{K_E+T}
-
d_E E
-
\gamma_E C E,
\]

\[
\dot{C}
=
-k_C C,
\]

\[
\dot{B}
=
\alpha_B C
+
\beta_B E
-
k_B B.
\]

This system is only illustrative. The specific biological components can be adjusted as the benchmark is refined. The key point is that the model should contain a treatment-control structure with clinically interpretable events.

For example, at planned dosing times \(t_k\),

\[
C(t_k^+)
=
C(t_k^-)
+
D_k,
\]

where \(D_k\) is the administered dose.

A toxicity hold may be triggered when

\[
B(t)
\geq
B_{\mathrm{hold}},
\]

causing a transition from an active-treatment mode to a hold mode. In the hold mode, scheduled doses are skipped until toxicity falls below a recovery threshold:

\[
B(t)
\leq
B_{\mathrm{restart}}.
\]

The system can therefore have modes such as:

- treatment active,
- treatment hold,
- recovery monitoring,
- reduced-dose rechallenge,
- or alternative therapy.

The scientific questions are straightforward and decision-relevant:

- Which schedules suppress tumor burden while avoiding prolonged toxicity?
- How sensitive are outcomes to dose interval, dose intensity, or hold thresholds?
- Does a small change in a threshold produce a large change in time on treatment or long-term tumor control?
- Are some treatment schedules robust across plausible parameter variation?
- Do different mechanisms of action produce distinct schedule-response regimes?

The numerical questions are equally important:

- Can the simulator locate threshold crossings reliably?
- Are event times and state resets reproducible under solver tolerances?
- Do sensitivities propagated through the hold and restart events agree with local perturbation experiments?
- Does multiple shooting improve conditioning for long-horizon schedule optimization?
- Where do grazing events or near-threshold trajectories produce ill-conditioned derivatives?

This first example should be intentionally compact. It should be understandable from the README and reproducible from a small number of scripts or notebooks. Its role is to demonstrate the full workflow: model specification, event handling, simulation, sensitivity propagation, and schedule-facing analysis.

### Next biomedical extensions

After the initial tumor–immune treatment-hold model, the next examples should increase biological and numerical complexity without changing the core message of the package.

Possible extensions include:

- **Combination therapy models** with separate dosing schedules, synergistic or antagonistic effects, and treatment rules that depend on multiple biomarkers.
- **Autoimmune or inflammatory disease models** with flare-remission dynamics, steroid tapering, rescue therapy, or biomarker-triggered treatment escalation.
- **Cell therapy models** with conditioning regimens, cell infusion events, delayed expansion phases, cytokine-release toxicity, and dose-adjustment logic.
- **PK/PD models with adaptive dosing** in which treatment changes depend on drug concentration, target engagement, toxicity, or efficacy biomarkers.
- **Longitudinal virtual-patient studies** in which parameter heterogeneity and decision rules are varied together to assess regimen robustness across plausible patient populations.

A useful second-stage benchmark may involve a higher-dimensional model with two or more treatment agents, a toxicity state, and a state-triggered decision policy. That would allow the package to demonstrate both scheduled impulses and state-dependent transitions in the same system.

For example, a combination-treatment model could include:

\[
C_1(t),
\qquad
C_2(t),
\]

for two drug exposures, along with tumor, immune, and toxicity states. A treatment rule might reduce or stop one agent when toxicity crosses a threshold while allowing the other to continue. Such a model naturally produces hybrid trajectories whose interpretation depends on the timing and ordering of events.

These extensions should be selected for their ability to demonstrate a practical progression:

1. A small deterministic event-driven model.
2. A higher-dimensional QSP-style model.
3. A model with multiple treatment modes and competing intervention rules.
4. A cohort or virtual-patient workflow.
5. A stochastic or uncertainty-aware extension.

### Mechanistic stochastic and Bayesian extensions

Once the deterministic hybrid core is stable, the package can expand toward stochastic and Bayesian workflows for systems in which uncertainty, heterogeneity, or random events materially affect the scientific question.

A first stochastic extension could add random effects, stochastic forcing, or event-time variability to an otherwise deterministic treatment model. For example, patient-level parameters may be sampled from a distribution:

\[
\theta_i
\sim
p(\theta \mid \eta_i),
\]

where \(i\) indexes a virtual patient and \(\eta_i\) represents patient-specific random effects.

This can be combined with deterministic treatment events and state-triggered treatment logic. The resulting workflow would allow users to ask not only whether a schedule works for a nominal trajectory, but also how robust the schedule is across a population.

A more advanced extension could represent uncertainty in unobserved biology through stochastic differential equations or jump processes:

\[
dX_t
=
f(X_t,t,\theta)\,dt
+
g(X_t,t,\theta)\,dW_t
+
J(X_{t^-},t,\theta)\,dN_t.
\]

The deterministic scheduled intervention structure remains explicit, while stochastic terms represent biological fluctuations, unobserved disturbances, variable adherence, or random clinical events.

Bayesian parameter inference is another natural extension. A modeler may specify priors over mechanistic parameters:

\[
p(\theta),
\]

combine those with a likelihood for longitudinal observations:

\[
p(y \mid \theta),
\]

and obtain a posterior distribution:

\[
p(\theta \mid y)
\propto
p(y \mid \theta)p(\theta).
\]

For hybrid models, the likelihood can depend strongly on event timing, treatment holds, threshold crossings, and reset states. Event-aware sensitivities can therefore be useful for gradient-based inference, Laplace approximations, variational methods, or Hamiltonian Monte Carlo workflows.

The main purpose of this stage is not to provide a complete Bayesian pharmacometrics platform. It is to demonstrate that hybrid event structure can be retained when uncertainty is introduced, rather than being simplified away before inference or population analysis begins.

### Filippov pseudo-Hopf normal form

A mathematically focused benchmark should accompany the biomedical examples. One useful candidate is a Filippov pseudo-Hopf normal form, which provides a compact test problem for switching surfaces, discontinuous vector fields, bifurcation structure, and hybrid sensitivity calculations.

A Filippov system has different vector fields on different sides of a switching surface. In two dimensions, one may write:

\[
\dot{x}
=
f^+(x,\mu)
\qquad \text{when } h(x)>0,
\]

\[
\dot{x}
=
f^-(x,\mu)
\qquad \text{when } h(x)<0,
\]

where \(h(x)=0\) defines the switching boundary and \(\mu\) is a bifurcation parameter.

A pseudo-Hopf bifurcation is a nonsmooth analogue of a Hopf-type transition, in which a periodic orbit or related oscillatory behavior arises through the interaction of the vector fields and the switching boundary rather than through the classical smooth-system eigenvalue crossing alone.

This benchmark is useful because it can expose numerical issues that are harder to see in a high-dimensional biomedical model:

- transverse crossing versus tangential contact with a switching surface,
- sensitivity growth near grazing events,
- discontinuous changes in the vector field,
- continuation of periodic orbits across parameter changes,
- and conditioning of shooting formulations near nonsmooth bifurcations.

The Filippov benchmark should not be positioned as a biomedical model. Its purpose is to validate the mathematical core of the package under controlled conditions where known hybrid behavior can be reproduced, visualized, and compared across numerical methods.

A complete benchmark workflow could include:

- direct simulation of trajectories on both sides of the switching surface,
- event detection and mode transitions,
- computation of periodic-orbit candidates,
- multiple-shooting refinement,
- variational and saltation-based sensitivities,
- parameter continuation,
- and comparison against finite-difference sensitivities.

Together, the biomedical and Filippov test beds create a complementary validation strategy. The biomedical models demonstrate translational relevance, while the normal-form benchmark demonstrates that the underlying hybrid numerical machinery behaves correctly in a setting where nonsmooth dynamics can be examined directly.

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

### Specific labs and authors

The examples in this section identify research programs whose published work is potentially relevant to the scientific and technical scope of `hybrid-ds-julia`. They are included as invitations to technical scrutiny, not as endorsements or claims of collaboration. In each case, the relevant question is whether the package's combination of continuous-time ODE models, explicit events, threshold rules, reset maps, sensitivity analysis, and constrained optimization would usefully complement existing domain-specific theory, software, experiments, and analysis workflows.

These research programs already use sophisticated modeling, estimation, control, simulation, and experimental methods. `hybrid-ds-julia` is not intended to replace established specialized tools. Its potential value is as a transparent Julia-native environment for reduced-order or mechanistic hybrid models in which the researcher directly specifies continuous dynamics and the discrete events that alter them.

#### Jeka and Kiemel: human postural control and locomotion

John Jeka and Tim Kiemel's work on human upright posture, multisensory integration, multijoint coordination, balance, locomotion, and system identification provides an especially direct scientific motivation for interpretable hybrid sensorimotor models.

Their research combines structured perturbation experiments, sensory manipulation, feedback-control models, biomechanical plant models, state estimation, and system-identification approaches. This body of work illustrates how a model can be meaningfully tied to experimental data rather than used only as a generic simulation.

A reduced postural-control model may contain continuous states for body-segment position and velocity, center-of-mass motion, muscle activation, sensory estimates, controller states, or sensory weights. Events may include perturbation onset and offset, sensory-reference changes, foot contact, stepping thresholds, recovery steps, changes in visual or support-surface conditions, and controller-mode transitions.

A generic formulation might be:

\[
\dot{x}(t)=f_{q(t)}(x(t),u(t),\theta),
\]

where the state includes biomechanical and neural-control variables, the input includes visual, vestibular, proprioceptive, tactile, or platform-perturbation signals, and the mode represents stance, stepping, recovery, sensory context, or controller configuration.

The potential role of `hybrid-ds-julia` would be to implement reduced-order models transparently. For example, it could support an inverted-pendulum or multi-segment plant coupled to a sensory estimator and feedback controller, with explicit delayed feedback, perturbation events, state-dependent stepping thresholds, and reset maps associated with contact or recovery.

Potential uses include:

- Simulating sensory perturbation experiments with explicit event timing
- Comparing sensory reweighting, state-estimation, and controller-gain hypotheses
- Modeling stance-to-step transitions or balance-recovery actions
- Studying how delays, noise, and sensory availability affect stability
- Performing sensitivity analysis for sensory gains, mechanical parameters, thresholds, and delays
- Comparing control policies subject to realistic force, stepping, or stability constraints
- Designing perturbation protocols that discriminate among competing hypotheses

The package should not be assumed to replace the laboratory's existing experimental, theoretical, and identification methods. The relevant question is whether its explicit event, reset, and sensitivity semantics would make particular lower-dimensional models easier to reproduce, compare, or extend.

#### Ahrens Lab: whole-brain zebrafish sensorimotor behavior

The Ahrens Lab at HHMI Janelia Research Campus studies how large neuronal populations support flexible behavior in larval zebrafish. Its experimental approach combines whole-brain imaging, virtual-reality behavioral paradigms, fictive locomotor recordings, computational analysis, genetics, anatomy, and targeted perturbation. The laboratory's work on motor adaptation, sensorimotor transformations, behavioral-state switching, and positional homeostasis is particularly relevant to reduced-order hybrid dynamical models.

The potential fit is not that whole-brain neural data should be replaced by a low-dimensional ODE model. Rather, a hybrid model could provide a compact and falsifiable representation of a specific mechanistic hypothesis: a small number of neural, sensory, behavioral, or internal-estimate variables evolve continuously; experimentally imposed perturbations and behavioral actions occur as discrete events; and explicit feedback links motor output to the subsequent sensory environment.

For example, in closed-loop virtual-reality paradigms, fictive swim output changes visual feedback, which changes sensory input and then changes later neural activity and motor output. A model might include continuous states for sensory evidence, motor-vigor drive, estimated self-location, accumulated prediction error, neural-population activity, or glial state. It could include discrete events for swim bouts, stimulus onset or offset, changes in visuomotor gain, externally imposed displacement, action-outcome mismatch, behavioral-state transitions, and experimental perturbations.

A general state-and-event representation could be written as:

\[
\dot{x}(t)=f_{q(t)}\bigl(x(t),u(t),\theta\bigr),
\]

where \(x(t)\) represents a reduced neural-behavioral state, \(u(t)\) represents sensory input or experimental drive, \(\theta\) contains physiological and control parameters, and \(q(t)\) identifies an active behavioral or experimental mode. At an event condition \(g_i(x,t)=0\), the mode and state could change through:

\[
x^+=R_i(x^-,\theta),
\qquad
q^+=T_i(q^-,x^-).
\]

The important scientific question is whether a proposed state, guard, or reset corresponds to experimentally observable quantities and predicts data not used for fitting.

Motor-adaptation experiments with altered visual feedback in a closed-loop virtual environment provide one useful target. In a hybrid formulation, a visual-gain manipulation is an experimental mode switch; fictive swim bouts are discrete motor events; neural and adaptation variables may evolve continuously between bouts; and predictions can be compared with neural activity, behavioral output, and the time course of recalibration. Sensitivity analysis could ask whether predicted adaptation depends most strongly on feedback gain, sensory delay, adaptation time constant, or an internal prediction-error gain.

Brain-wide sensorimotor-transformation experiments suggest a modular architecture that separates sensory encoding, intermediate sensorimotor transformation, motor command, and locomotor output. A reduced hybrid model should not equate correlation with instantaneous motor output to causal motor command. It could instead compare feedforward sensory-to-motor mapping, recurrent state estimation, or state-dependent action-selection architectures against data obtained under multiple visual-feedback conditions.

Behavioral-state switching after unsuccessful action is an especially direct candidate for a threshold model. A stylized hypothesis could include a continuous variable \(e(t)\) representing accumulated evidence that action is futile:

\[
\dot{e}(t)=-\lambda e(t)
\]

between swimming events, with a discrete update after an unsuccessful bout:

\[
e^+=e^-+\alpha.
\]

A threshold condition could define a transition from an active mode to a suppressed or passive behavioral mode:

\[
q^+=\mathrm{passive}
\quad\text{when}\quad
e(t)\geq\vartheta.
\]

This is a stylized hypothesis, not a claim that the biological system follows this exact equation. Its value would be to make assumptions about integration, decay, thresholding, and recovery explicit and quantitatively testable against behavioral and neural/glial data. Competing models could use nonlinear accumulation, state-dependent thresholds, stochastic event effects, adaptation of \(\alpha\), or an additional latent arousal state.

Work on self-location memory and positional homeostasis provides another natural control-theoretic example. A model could include an internal self-location estimate:

\[
\dot{\hat{p}}(t)=v_{\mathrm{self}}(t),
\qquad
e_p(t)=p_{\mathrm{reference}}-\hat{p}(t),
\]

where \(\hat{p}(t)\) is an internal position estimate and \(e_p(t)\) is a position error. An imposed displacement can be represented as a reset or perturbation to physical position, sensory input, internal estimate, or some combination, depending on the mechanistic hypothesis. Corrective swim-bout probability, direction, vigor, or termination could be modeled as a state-dependent event policy.

Potential uses of `hybrid-ds-julia` in this setting include:

- Simulation of closed-loop virtual-environment protocols with explicit sensory delay and visuomotor gain changes
- Reduced-order models of motor adaptation, sensory prediction error, and behavioral-state switching
- Event-aware estimation of parameters from neural, glial, fictive-swim, and behavioral data
- Comparison of alternative reset maps for imposed displacement, failed action, sensory perturbation, or behavioral transition
- Sensitivity analysis for feedback gain, delay, evidence accumulation, state decay, threshold location, and controller gain
- Simulation-based comparison of competing mechanistic hypotheses
- Constrained optimization of perturbation timing or gain schedules to distinguish between competing models

The limitation is equally important. Whole-brain neural data are high dimensional, experimentally rich, and shaped by circuitry that cannot in general be reduced to a small number of ODE states without strong assumptions. Any use of `hybrid-ds-julia` would therefore need a deliberately limited scientific target, biologically interpretable reduced states, a clear measurement model, alternative-hypothesis comparison, and tests using held-out perturbation conditions.

The package would complement—not replace—whole-brain imaging pipelines, statistical neural-population analysis, machine learning, circuit mapping, or causal perturbation experiments.

#### Cowan and the LIMBS Laboratory: locomotion, active sensing, system identification, and hybrid mechanics

The Locomotion in Mechanical and Biological Systems (LIMBS) Laboratory, directed by Noah J. Cowan at Johns Hopkins University, studies how animals and robots move, sense, navigate, adapt, and control behavior. Its work spans control theory, nonlinear and geometric mechanics, system identification, robotics, active sensing, neuromechanics, animal locomotion, and experimental analysis of biological control systems.

This research program is already deeply connected to the mathematical territory of hybrid dynamical systems. Contacts, impacts, gait transitions, task changes, mode switches, sensory perturbations, actuator saturation, threshold-triggered behaviors, and intermittent control can all introduce discontinuous changes into otherwise continuous mechanical and neural dynamics.

The relevant question is therefore not whether the LIMBS Laboratory needs a generic claim that hybrid systems are important. The specific question is whether `hybrid-ds-julia` could provide a useful and technically correct implementation environment for a particular class of reduced-order models, experimental protocols, sensitivity calculations, or optimization problems.

The intended role for `hybrid-ds-julia` would be complementary to established robotics, control, identification, and simulation tools. It would not replace multibody simulators, geometric-mechanics formulations, experiment-specific identification methods, robot middleware, or mature optimal-control workflows. Its possible niche is a transparent Julia-native workflow in which a researcher directly specifies:

- A continuous-time plant, controller, estimator, or sensory-state model
- Guard conditions defining contact, behavioral, measurement, or protocol events
- Reset maps, parameter changes, or mode transitions at those events
- A schedule of externally imposed perturbations or sensory manipulations
- Objectives, constraints, and parameter sets for sensitivity analysis or policy comparison

A generic reduced-order formulation might be:

\[
\dot{x}(t)=f_{q(t)}\bigl(x(t),u(t),\theta\bigr),
\]

where \(x(t)\) contains mechanical, sensory, neural, controller, or estimator states; \(u(t)\) denotes external forcing or measured sensory input; \(\theta\) contains plant, controller, and measurement parameters; and \(q(t)\) denotes an active contact, gait, behavioral, or controller mode. An event may be defined by:

\[
g_i(x,t,\theta)=0,
\]

with a state and mode update:

\[
x^+=R_i(x^-,\theta),
\qquad
q^+=T_i(q^-,x^-).
\]

The technical value of this representation is that event conditions and event maps are first-class model components rather than informal post-processing logic. It permits a modeler to ask how conclusions change when an impact occurs earlier or later, when a sensory threshold is crossed, when an actuator saturates, when a controller switches, or when an experiment introduces a perturbation.

The LIMBS Laboratory's work on animal locomotion and active sensing provides several plausible test cases. In mechanical locomotion, continuous state may include position, velocity, body orientation, joint configuration, internal compliance, actuator state, and controller state. Discrete events may include foot contact, lift-off, collision, stick-slip transition, takeoff, landing, gait-phase change, or perturbation-triggered recovery step. In active sensing, the state may additionally include a sensory reference, internal estimate, or policy variable; discrete events may include probe movements, sensory sampling, abrupt stimulus changes, or switches between tracking and exploratory behavior.

The laboratory's research on the relation between mechanics and sensory decoding is especially relevant. Work on refuge tracking in weakly electric knifefish emphasizes that locomotor mechanics shape sensory information, and that understanding the sensory system requires modeling the closed loop between the animal, its plant, its movement, and its sensory input. A hybrid extension becomes appropriate when the experiment or hypothesized controller involves discrete sensory movements, abrupt perturbations, mode changes, contact events, or thresholded behavioral decisions.

Potential uses of `hybrid-ds-julia` in this research area include:

- Reduced-order models of locomotor plants coupled to neural feedback controllers
- Simulation of stance, stepping, contact, lift-off, and perturbation-recovery transitions
- Explicit experimental-protocol models with visual, vestibular, tactile, mechanical, or electrosensory stimuli that change at scheduled or state-dependent times
- Active-sensing models with intermittent measurements, sampling actions, state-dependent probing, or mode-dependent sensory gains
- Closed-loop system-identification studies comparing plant, controller, estimator, delay, noise, and event assumptions
- Sensitivity analysis for feedback gain, mechanical stiffness, damping, sensory delay, threshold placement, reset-map parameters, and event-time variation
- Optimization of constrained controller, sensing, or perturbation policies
- Reproducible compact examples that expose equations, events, assumptions, and diagnostics directly

Hybrid sensitivity requires special care. In a smooth ODE model, sensitivities can be obtained by integrating variational equations. In a hybrid model, a parameter perturbation can also change the time at which an event occurs and the post-event state. A correct first-order calculation must therefore account for both continuous evolution and event-induced variation, for example through a saltation-matrix or equivalent reset-aware update.

The most important questions for the LIMBS Laboratory are concrete:

1. Which research models would benefit from an explicit ODE-plus-guard-plus-reset interface rather than an existing multibody, control, or identification workflow?
2. Are there scientifically useful reduced-order examples in locomotion, active sensing, or experimental perturbation for which event-time sensitivity is central?
3. What event semantics, differentiation behavior, optimization interface, or numerical diagnostics would be required for the package to be technically trustworthy in this setting?
4. Which existing workflows should the package interoperate with, rather than attempt to reproduce?
5. Can one identify a compact benchmark in which the package adds reproducibility, interpretable event logic, or sensitivity analysis beyond what present tools already provide?

The package should be judged useful only if it addresses a real gap in those questions. It should not be described as a replacement for established expertise in nonlinear mechanics, closed-loop identification, control, or robotic experimentation.

#### Fortune: feedback control, locomotor variability, and active sensing in weakly electric fish

Eric S. Fortune studies mechanisms and evolution of animal behavior, with important work on sensorimotor control, active sensing, locomotion, electrosensory behavior, refuge tracking, behavioral variability, and feedback control in weakly electric fish. He is currently an Associate Professor of Biological Sciences at the New Jersey Institute of Technology.

The potential relevance of `hybrid-ds-julia` is strongest where a model must represent continuous closed-loop locomotor and sensory dynamics together with explicitly discrete actions, manipulations, or behavioral modes. It is not that refuge tracking or active sensing must be treated as hybrid by default. Many experimental tasks can be analyzed well with smooth linear, nonlinear, frequency-domain, or system-identification methods. A hybrid representation becomes worthwhile only when the scientific question depends on transitions, intermittent actions, state-dependent sensing, abrupt environmental changes, trial-protocol events, or mode-dependent control.

A generic closed-loop formulation might separate plant, controller, and sensory dynamics:

\[
\dot{x}_p=f_p(x_p,u,\theta_p),
\]

\[
\dot{x}_c=f_c(x_c,y,\theta_c),
\]

\[
u=\pi_{q(t)}(x_c,y,\theta_\pi),
\]

where \(x_p\) represents locomotor plant state, \(x_c\) represents internal controller or estimator state, \(y\) represents sensory input, and \(q(t)\) represents a behavioral or experimental mode. The sensory signal may depend on both animal motion and environment:

\[
y(t)=h\bigl(x_p(t),r(t),\theta_s\bigr)+\eta(t),
\]

where \(r(t)\) is refuge or environmental motion and \(\eta(t)\) represents sensory or measurement noise.

A hybrid extension can represent events such as:

- Onset, offset, or abrupt phase changes of refuge motion
- Transitions between predictable and unpredictable stimulus regimes
- Changes in refuge dynamics or destabilizing feedback
- Discrete probe movements or active-sensing actions
- Sensory perturbation, temporary occlusion, jamming, or social electrosensory events
- Threshold-triggered changes in tracking gain, body position, swimming direction, or control strategy
- Trial boundaries, conditioning events, or changes in sensory context
- Switching between locomotor, exploratory, stationary, or recovery modes

Research on the critical role of locomotion mechanics in decoding sensory systems provides a key conceptual basis. Refuge tracking in *Eigenmannia* is useful for sensorimotor-control research precisely because locomotor mechanics and sensory encoding must be understood together in closed loop. The package could support a reduced-order implementation in which fish mechanics, sensory-image dynamics, neural control, and experimental forcing are explicit components.

This would allow investigators to test which conclusions depend on plant dynamics, controller dynamics, sensory delay, feedback gain, or stimulus structure. An experiment could compare modes such as:

\[
q\in\{
\mathrm{predictable},
\mathrm{unpredictable},
\mathrm{sensory\ cue\ available},
\mathrm{sensory\ cue\ absent}
\},
\]

with each mode selecting a different controller gain, estimator gain, delay, noise level, or active-sensing policy.

The point would not be to infer an unobserved controller from a small dataset without constraint. Rather, the model would formalize competing hypotheses and ask whether they make distinguishable predictions under carefully designed perturbation experiments.

Work on sensorimotor adaptation to destabilizing dynamics is particularly suitable for this kind of model. A gradual or abrupt change in the relation between fish movement and sensory consequences can be represented as a parameter change in the plant, sensory environment, or closed-loop feedback pathway. The model could compare competing explanations:

\[
\text{plant adaptation},
\qquad
\text{controller-gain adaptation},
\qquad
\text{state-estimator adaptation},
\qquad
\text{mode switching},
\]

or combinations of these mechanisms.

Potential uses of `hybrid-ds-julia` in this setting include:

- Event-aware closed-loop simulations of refuge tracking and active-sensing tasks
- Joint plant-controller-estimator models with explicit feedback and perturbation protocols
- Comparison of smooth versus switching control laws under predictable, destabilizing, or noisy conditions
- Sensitivity analysis for plant parameters, sensory delay, feedback gain, internal-model parameters, noise level, and transition thresholds
- Analysis of how trial timing or stimulus structure affects identifiability of plant and controller parameters
- Optimization of perturbation schedules or stimulus designs that distinguish competing feedback-control hypotheses
- Simulation of individual variability in locomotor plant dynamics and robustness to controller/plant mismatch
- Explicit representation of trial boundaries and intervention times as part of the model

The relationship between individual variability and feedback control is especially important. If different animals have different locomotor plants but performance remains robust, a model can ask whether the controller is individualized, whether feedback compensates for mismatch, or whether multiple plant/controller pairs produce similarly effective closed-loop behavior.

The central technical challenge is closed-loop identification. Because the animal's action changes the sensory stimulus later used to infer the controller, open-loop assumptions can produce biased or misleading estimates. A hybrid model adds another requirement: if events change the stimulus, controller, or state, parameter sensitivities must include changed event timing and reset maps.

Questions for Dr. Fortune and collaborators include:

1. Which experimental phenomena genuinely require a discrete mode, event, or reset model rather than a smooth closed-loop representation?
2. Are stimulus-predictability changes, active-sensing actions, trial events, or destabilizing perturbations best modeled as externally scheduled inputs, state-triggered events, or changes in controller architecture?
3. Would reset-aware sensitivity analysis add scientific value in designing experiments or testing robustness of closed-loop hypotheses?
4. What quantities are observable well enough to constrain a reduced-order hybrid model?
5. Which results would demonstrate that the package adds value beyond established frequency-domain, system-identification, and control-theoretic tools?

`hybrid-ds-julia` should be useful here only as a transparent hypothesis-testing and simulation environment. It should not be presented as a replacement for detailed experimental analysis, closed-loop system identification, or the biological insight that comes from the fish model itself.

#### Hines and the NEURON ecosystem: neural and network simulation with events, discontinuities, and multiscale control

Michael L. Hines has made foundational contributions to computational neuroscience through the NEURON simulation environment and related work on numerical methods, variable-step integration, parallel neural-network simulation, event-driven mechanisms, interoperability, and reproducible modeling. NEURON is a mature and extensively validated environment for simulating biophysically detailed neurons and neural networks, including compartmental morphology, cable equations, membrane mechanisms, ion channels, synapses, stochastic processes, stimulation, and distributed network computation.

The relationship between `hybrid-ds-julia` and NEURON must therefore be stated with particular care. `hybrid-ds-julia` is not intended to compete with, replace, or reproduce NEURON. A general ODE-and-event package would not provide NEURON's mature infrastructure for morphologically detailed cable models, domain-specific model descriptions, synaptic event handling, mechanism libraries, network simulation, variable-step solvers, parallel execution, validation history, ModelDB ecosystem, or broad community expertise.

The possible role for `hybrid-ds-julia` is instead at a different modeling layer: reduced-order, system-level, experimental-protocol, control, optimization, or cross-domain models in which neural or cellular dynamics interact with externally defined discrete interventions, policies, thresholds, and non-neural states.

In that role, the package might serve as:

- A compact environment for low-dimensional neural mass, neural population, conductance-based, oscillator, or state-space surrogate models
- A systems-level wrapper around a reduced neural model coupled to behavior, biomechanics, pharmacology, stimulation, or experimental control
- A tool for explicit intervention schedules, threshold-triggered stimulation, adaptive closed-loop control, dosing events, and experimental-protocol logic
- A platform for sensitivity analysis and constrained optimization of systems that include neural states but are not principally compartmental-neuron simulations
- A possible pre- or post-processing companion to detailed NEURON simulations, if a scientifically and technically sound coupling interface can be defined

A reduced-order hybrid neural system could be written as:

\[
\dot{x}(t)=f_{q(t)}\bigl(x(t),I(t),p(t),\theta\bigr),
\]

where \(x(t)\) includes neural, synaptic, network, cellular, behavioral, or physiological states; \(I(t)\) is stimulation or synaptic drive; \(p(t)\) represents intervention or protocol state; \(\theta\) contains biophysical or phenomenological parameters; and \(q(t)\) selects an active treatment, stimulation, behavioral, or experimental mode.

Events might include:

- Current-pulse onset, offset, amplitude change, or waveform change
- Synaptic input, spike detection, or network event
- State-dependent stimulation triggered by a measured neural or behavioral variable
- Electrode, recording, or stimulation artifact events
- Seizure-like threshold crossing, burst termination, or mode transition
- Closed-loop neuromodulation action
- Drug administration, concentration threshold, receptor-blockade change, or washout protocol
- Trial onset, sensory stimulus transition, task phase, reinforcement signal, or behavioral action
- A coupling event between a detailed neuronal simulator and a reduced external system

At cellular and network levels, NEURON already treats several of these problems as first-class concerns. It supports variable-order and variable-step integration, event delivery, parallel networks, and detailed biophysical mechanisms. The existing sophistication has two implications for `hybrid-ds-julia`.

First, the package should not make generic claims such as “NEURON cannot model events” or “hybrid event support is missing from neural simulators.” Such claims would be false or misleading. Event-driven synaptic mechanisms and network simulation are central to modern computational-neuroscience tools.

Second, any proposed complementarity must identify a genuinely distinct use case. A plausible distinction is between an event internal to a detailed neural-network simulation and an event that changes the governing model at the system or experimental-policy level:

\[
\text{neural dynamics}
\longrightarrow
\text{estimated biomarker}
\longrightarrow
\text{stimulation decision}
\longrightarrow
\text{changed stimulation protocol}
\longrightarrow
\text{future neural and behavioral dynamics}.
\]

A model of this form might combine a low-dimensional neural state, a behavioral state, a measurement process, an estimator, and a thresholded controller. The hybrid framework would make a decision rule explicit:

\[
\text{apply stimulation if }\hat{z}(t)\geq z_{\mathrm{threshold}},
\]

or:

\[
\text{change mode if}
\int_{t-T}^{t}\phi(x(s))\,ds
\geq\Theta.
\]

Such a model could be useful for studying assumptions in adaptive stimulation, experimental design, neuroprosthetic control, pharmacological intervention, or neural-behavioral coupling. It is not a substitute for detailed cellular simulation when morphology, spatial ion dynamics, dendritic integration, channel kinetics, or network connectivity are essential to the scientific question.

Potential uses of `hybrid-ds-julia` in a NEURON-adjacent context include:

- Reduced-order neural or neural-mass models coupled to discrete stimulation, recording, behavioral, or treatment events
- Simulation of adaptive closed-loop stimulation policies with explicit safety thresholds, delays, measurement noise, and control constraints
- Comparison of open-loop, scheduled, threshold-triggered, and estimator-based stimulation protocols
- Sensitivity analysis for stimulation amplitude, timing, delay, measurement noise, state-estimator parameters, and intervention thresholds
- Constrained optimization of stimulation schedules or control policies in low-dimensional surrogate models
- Neural-behavioral or neural-pharmacological systems in which external subsystems are naturally represented by ODEs and discrete events
- Experimental-design simulation that compares which stimulation or measurement schedules distinguish competing hypotheses
- Development of reduced-order surrogates for use when a full multicompartment network simulation would be too costly inside a policy-optimization loop

The numerical requirements are demanding. State-triggered events can cause discontinuities in parameters, inputs, modes, or states. When estimating gradients or sensitivities, a correct method must include the dependence of event timing on parameters and state, not merely differentiate the smooth intervals between events. If an external decision rule depends on a threshold crossing, then both threshold-crossing time and state transition must be handled consistently.

A possible future interoperability direction would be deliberately modest: use detailed NEURON simulations to generate data or reduced-order surrogates, then use `hybrid-ds-julia` for system-level policy exploration; or use a reduced-order external model to determine stimulation or intervention protocols subsequently evaluated in NEURON. Direct co-simulation would require explicit agreement about time stepping, event ordering, state transfer, units, reproducibility, and numerical error control. It should not be claimed until demonstrated on a concrete benchmark.

Questions for Dr. Hines and the NEURON community include:

1. What system-level hybrid problems are not already adequately handled by NEURON, CoreNEURON, Python control scripts, or existing co-simulation workflows?
2. Would a Julia-native reduced-order ODE-and-event environment be useful for adaptive stimulation, neural-behavioral coupling, pharmacological protocols, or multiscale policy modeling?
3. What would a scientifically meaningful NEURON-adjacent benchmark look like?
4. Which event semantics, solver guarantees, sensitivity methods, and numerical diagnostics would be necessary before using such a workflow for neural applications?
5. Is one-way model exchange, surrogate fitting, protocol export, or direct co-simulation the most realistic interoperability target?
6. Which capabilities should remain explicitly outside project scope because NEURON and related neuroscience ecosystems already address them more effectively?

The most credible position is one of complementarity. `hybrid-ds-julia` may become useful for transparent low-dimensional systems models and event-aware intervention policies that sit around, above, or alongside detailed neural simulation. It should not present itself as an alternative implementation of NEURON's core scientific and computational mission.

## Domains where `hybrid-ds-julia` would be less helpful

### Why these settings are difficult

Hybrid dynamical systems become difficult to use responsibly when recorded events do not identify the continuous state that is meant to drive the model.

A dataset may record appointments, prescriptions, diagnostic codes, symptom questionnaires, hospitalizations, medication changes, and changes in function. These observations can establish that a person’s symptoms or care pathway changed. They may not establish whether the dominant driver was one disease-specific biological process, multiple interacting processes, a co-occurring condition, medication effects, behavior, environmental exposures, changing access to care, or a combination of these factors.

In such settings, a model can often represent observable parts of the chain:

- Timing of documented clinical events
- Medication and treatment exposure
- Healthcare utilization
- Symptom and functional-status documentation
- Selected physiological measurements
- Monitoring and care-pathway decisions

The difficult step is causal identification: determining which latent continuous state generated the observations, how that state changes over time, and whether an intervention caused a subsequent change. A model may fit observed trajectories while assigning them to the wrong mechanism.

More formally, if \(y(t)\) is an observed symptom or function score, it may depend on several partially unobserved processes:

\[
y(t)=f_1(x_1(t))+f_2(x_2(t))+\cdots+f_k(x_k(t))+\epsilon(t).
\]

When the relevant \(x_i(t)\) are poorly measured, nonunique, or causally confounded, fitting a model to \(y(t)\) does not establish which process is responsible. This is a limitation of measurement and causal identifiability, not a judgment about the legitimacy or severity of any illness.

### Some infectious and post-infectious conditions

Infection itself is not a limitation. Tuberculosis and HIV, for example, can be suitable applications when pathogen burden, drug exposure, treatment schedules, resistance, and relevant biomarkers are sufficiently defined and measured.

Challenges arise in some infectious and post-infectious settings when persistent symptoms have multiple possible contributors and available observations do not identify the biological process that should form the model’s continuous state. In these settings, event history may be useful for descriptive or care-pathway analysis but insufficient for disease-specific mechanistic inference.

#### Long COVID

Long COVID can involve discrete, timestamped events such as acute infection, reinfection, hospitalization, medication changes, diagnostic testing, rehabilitation, work-disability transitions, and follow-up visits. These events can support carefully scoped monitoring, care-pathway, utilization, or organ-specific models.

The central difficulty is that long COVID is heterogeneous, its mechanisms remain incompletely resolved, and routine laboratory results do not reliably distinguish it from other illnesses. Persistent symptoms may reflect multiple possible and potentially interacting processes, including immune dysregulation, tissue injury, altered autonomic function, post-intensive-care effects, concurrent conditions, medication effects, and contextual factors.

`hybrid-ds-julia` may be useful for explicitly limited questions, such as rehabilitation scheduling, monitoring policies, longitudinal function tracking, or a well-defined organ-specific complication. It should not be presented as a validated model that identifies a single cause of an individual’s persistent symptoms or selects individualized treatment on that basis.

#### Persistent symptoms following Lyme disease treatment

Lyme disease can be a suitable target for carefully scoped models of tick exposure, early infection, antimicrobial PK/PD, treatment scheduling, and objectively documented manifestations such as arthritis, neurologic disease, or carditis.

Persistent nonspecific symptoms following appropriate treatment are a more difficult modeling target. Fatigue, pain, cognitive complaints, and reduced function may have several possible contributors, including reinfection, delayed or incomplete diagnosis, immune or tissue effects, co-occurring illness, sleep disturbance, medication effects, other infections, and causes unrelated to active *Borrelia* infection.

A model may represent treatment timing, diagnostic testing, antibiotic exposure, symptom documentation, and follow-up care. Those events alone do not establish whether a persistent symptom trajectory represents ongoing infection, treatment failure, a post-infectious process, or another contributor. Models in this setting should remain carefully scoped and should not be used to infer an individual’s unmeasured mechanism or justify individualized treatment without strong external validation.

### ME/CFS

Myalgic encephalomyelitis/chronic fatigue syndrome (ME/CFS) is a particularly clear example of a setting in which clinically meaningful events can be recorded without providing an identified disease-specific continuous state.

Potentially modelable observations include symptom and function tracking, healthcare encounters, medication events, orthostatic measurements where available, activity and rest records, work or school participation, and patient-reported post-exertional symptom worsening. Such information may support descriptive longitudinal analysis, monitoring workflows, and explicitly limited care-pathway questions.

The central challenge is that there is no confirmatory diagnostic test or validated biomarker that identifies ME/CFS as a single measurable biological state. Fatigue, post-exertional symptom worsening, pain, sleep disturbance, cognitive difficulty, autonomic symptoms, and functional limitation can coexist with other conditions or be influenced by multiple processes. Alternative explanations, comorbidities, medication effects, sleep disorders, activity patterns, and time-varying illness severity can confound relationships between recorded interventions and subsequent outcomes.

For example, a treatment change may occur because a person was already worsening. An observational model could then associate the treatment with worse later symptoms even when worsening, rather than treatment, caused both the intervention and the later outcome.

`hybrid-ds-julia` should therefore not be framed as identifying an individual’s ME/CFS mechanism or selecting treatment from sparse symptom and event records. It may still support descriptive symptom/function trajectories, monitoring systems, care-delivery operations, and sensitivity analyses that make competing assumptions explicit.

### Mental health and complex behavioral care

Mental health, substance use, and other forms of complex behavioral care can contain rich event histories: medication changes, therapy sessions, emergency visits, admissions, discharges, symptom-scale measurements, relapse episodes, substance-use treatment events, housing changes, employment changes, and social-service interventions.

These events can support operational models of access, scheduling, continuity of care, monitoring, crisis response, capacity planning, and service delivery. Validated symptom scales may also support carefully defined descriptive or predictive tasks.

However, mechanistic individual-level disease models can be difficult because symptoms and outcomes depend on many interacting, time-varying influences. These can include social and economic conditions, therapeutic relationship, trauma exposure, family and community support, concurrent physical illness, substance use, medication adherence, treatment availability, clinician selection, and patient preferences.

Treatment-selection confounding is especially important. A medication change, hospitalization, or intensive intervention often occurs because symptoms, risk, or social circumstances were already worsening. A model trained only on observational event histories can mistake this association for a causal treatment effect.

In these settings, `hybrid-ds-julia` may be useful for care-pathway simulation, resource planning, monitoring workflows, and sensitivity analysis. It should not be assumed to recover a single latent disease mechanism from routine records or to make unvalidated individualized treatment recommendations.

### What remains appropriate in difficult settings

A setting being less suitable for a mechanistic hybrid model does not make it unsuitable for all modeling. In the difficult domains above, `hybrid-ds-julia` may still be useful when the model’s purpose and limitations are explicit.

Appropriate uses may include:

- Descriptive models of symptom, function, or care trajectories
- Monitoring and measurement workflows
- Simulation of care pathways, referral rules, service capacity, and follow-up schedules
- Cohort-level hypothesis generation
- Sensitivity analyses across multiple explicitly stated causal assumptions
- Analyses of missingness, delay, monitoring frequency, and measurement uncertainty
- Operational studies that do not claim to identify disease-specific biology
- Educational simulations that distinguish observed events from hypothesized latent mechanisms

Such models should state clearly which states are directly measured, which are inferred, which assumptions are uncertain, and which decisions the model is not validated to support. They should not be used as a substitute for diagnosis, clinical judgment, informed consent, or external validation in the population and setting where they would be applied.

## Example applications

The following examples illustrate the kinds of translational and decision-facing questions that `hybrid-ds-julia` is intended to support. They are not separate product claims; they are examples of how event-aware simulation, sensitivities, and trajectory analysis can be used when mechanistic models include real intervention logic.

### QSP and PK/PD

In QSP and PK/PD, many model outputs depend on more than continuous exposure-response relationships. Treatment schedules, dose holds, switches, biomarker thresholds, and protocol rules can determine whether a trajectory enters one long-term regime or another.

For example, an immuno-oncology model may include:

- tumor growth and immune-mediated killing,
- drug exposure and clearance,
- treatment-cycle dosing,
- toxicity accumulation,
- and a treatment-hold rule triggered by a toxicity biomarker.

A clinically relevant question is not only whether a nominal dose reduces tumor burden. It may also be whether a schedule produces sustained control, temporary response followed by relapse, prolonged treatment interruption, or unacceptable toxicity.

With event-aware simulation, the model can represent the full treatment logic directly:

\[
C(t_k^+)
=
C(t_k^-)
+
D_k
\]

at planned dose times, together with threshold-triggered treatment holds such as

\[
B(t)
\geq
B_{\mathrm{hold}}
\quad \Longrightarrow \quad
\text{hold treatment}.
\]

If toxicity subsequently recovers,

\[
B(t)
\leq
B_{\mathrm{restart}}
\quad \Longrightarrow \quad
\text{restart or reduce treatment}.
\]

The resulting trajectory can be analyzed with respect to dose size, dose interval, treatment-hold thresholds, restart thresholds, and patient-specific parameter variation.

Potential QSP and PK/PD applications include:

- schedule comparison for pulsed, cyclic, or intermittent dosing,
- toxicity-aware dose optimization,
- treatment-holiday and rechallenge analysis,
- adaptive dosing based on biomarker thresholds,
- combination-therapy sequencing,
- virtual-patient studies with heterogeneous event thresholds,
- and sensitivity analysis of clinically meaningful outcome metrics.

A major practical advantage is that the analysis can focus on questions that are already meaningful to pharmacologists and clinicians:

- How much time is spent on treatment?
- How often are doses held or reduced?
- What is the cumulative exposure before toxicity forces a switch?
- Which parameters determine whether recovery and rechallenge are possible?
- How sensitive is a proposed schedule to changes in patient biology or measurement thresholds?

### Translational pharmacology

The package is intended to support translational workflows in which mechanistic models are used to connect preclinical observations, biomarker dynamics, and treatment strategies to early clinical decisions.

A translational model may combine:

- pharmacokinetics,
- target engagement,
- pathway modulation,
- biomarker response,
- tumor or disease burden,
- toxicity,
- and treatment-management logic.

The hybrid structure arises because real treatment development involves decisions and interventions that are not continuously varying. Examples include:

- dose escalation or de-escalation,
- treatment delay,
- stopping rules,
- cohort transitions,
- rescue medication,
- biomarker-triggered enrichment,
- and protocol-defined dose modifications.

A useful workflow can therefore be framed as a sequence:

1. Specify a mechanistic model and a treatment-control policy.
2. Simulate the resulting hybrid trajectory.
3. Compute sensitivities of outcomes and event times to model parameters and schedule variables.
4. Compare candidate regimens or decision rules.
5. Identify robust regions of the design space rather than optimizing only for one nominal parameter set.
6. Examine whether the conclusions change near event boundaries, threshold crossings, or treatment-regime transitions.

This perspective is particularly relevant in early development, where uncertainty is high and the goal is often to distinguish between plausible mechanisms, identify useful biomarkers, and choose dose or schedule ranges that remain reasonable across uncertainty.

### SAR progression and mechanism differentiation

Structure–activity relationship work often focuses on potency, selectivity, exposure, and safety properties. Those measurements remain essential, but mechanistic models can add another layer of interpretation: whether compounds with different pharmacological profiles generate meaningfully different dynamical treatment regimes under realistic dosing and intervention constraints.

For example, two compounds may have similar short-term tumor-growth inhibition in vitro but differ in:

- target residence time,
- exposure persistence,
- immune activation,
- toxicity accumulation,
- feedback effects,
- or the ability to sustain a response after dosing is reduced or interrupted.

A hybrid QSP model can make those differences visible at the regimen level.

Suppose a compound-specific parameter vector is written as

\[
\theta_j,
\]

where \(j\) indexes candidate compounds. The model may then produce an outcome map

\[
\mathcal{O}(\theta_j, D, \tau, \pi),
\]

where:

- \(D\) represents dose,
- \(\tau\) represents schedule timing,
- and \(\pi\) represents a treatment policy, such as a toxicity-hold or restart rule.

The outcome may include tumor control, biomarker suppression, cumulative exposure, time in toxicity hold, relapse probability, or time to progression.

The goal is not to claim that a model can replace experimental SAR. Rather, the model can help organize mechanistic hypotheses and prioritize experiments by asking questions such as:

- Does a change in potency alter the optimal schedule, or only the dose scale?
- Does a longer-lived effect improve robustness to missed doses or treatment holidays?
- Does one mechanism produce a wider safe scheduling window than another?
- Are certain compound properties especially valuable because they reduce sensitivity to toxicity-driven holds?
- Which measurements would most reduce uncertainty in mechanism-dependent regimen predictions?

This provides a way to connect compound properties to decision-relevant dynamical behavior rather than treating each property as an isolated optimization target.

### Autoimmune and inflammatory disease

Autoimmune and inflammatory disease models often have flare-remission behavior, delayed response, treatment tapering, rescue therapy, and biomarker-based adjustment. These features make them natural applications for hybrid dynamical-systems methods.

A conceptual model might include inflammatory activity \(I\), regulatory immune activity \(R\), drug exposure \(C\), and a toxicity or adverse-effect burden \(B\):

\[
\dot{I}
=
\alpha_I I
-
k_R R I
-
k_C C I,
\]

\[
\dot{R}
=
s_R
-
d_R R
+
\eta_C C,
\]

\[
\dot{C}
=
-k_C^{\mathrm{elim}}C,
\]

\[
\dot{B}
=
\alpha_B C
-
k_B B.
\]

A treatment policy may initiate rescue therapy during a flare:

\[
I(t)
\geq
I_{\mathrm{flare}}
\quad \Longrightarrow \quad
\text{administer rescue treatment},
\]

or taper treatment when disease activity remains controlled:

\[
I(t)
\leq
I_{\mathrm{control}}
\quad \Longrightarrow \quad
\text{reduce maintenance treatment}.
\]

The model can then be used to study:

- when tapering produces sustained control versus relapse,
- whether rescue therapy should be triggered earlier or later,
- how biomarker noise affects threshold-based decisions,
- whether treatment holidays create beneficial recovery or destabilizing flare cycles,
- and how patient heterogeneity changes the balance between efficacy and adverse effects.

The same numerical issues appear as in oncology: event times may be central to the outcome, small changes in thresholds can alter the treatment path, and long-horizon simulation may become sensitive to repeated regime changes.

### Crop science and precision agriculture

The event-aware framework also applies to crop models, where continuous growth and environmental dynamics interact with discrete management actions.

A crop-growth system may include biomass, water availability, nutrient status, canopy development, and pest pressure. Interventions such as irrigation, fertilization, pesticide application, planting, harvest, and greenhouse climate changes occur at specific times or in response to sensor thresholds.

For example, a precision-irrigation policy could apply water when soil moisture falls below a threshold:

\[
M(t)
\leq
M_{\mathrm{threshold}}
\quad \Longrightarrow \quad
M(t^+)
=
M(t^-)
+
\Delta M.
\]

A nutrient-management policy could apply fertilizer after a sensor-derived nutrient variable falls below a specified level:

\[
N(t)
\leq
N_{\mathrm{threshold}}
\quad \Longrightarrow \quad
N(t^+)
=
N(t^-)
+
\Delta N.
\]

The hybrid model can then be used to compare:

- fixed-calendar and sensor-triggered irrigation,
- alternative fertilizer timing and dose strategies,
- pest-intervention thresholds,
- crop responses to heat or water-stress events,
- and robustness of management policies across weather and soil conditions.

In this setting, variational equations and event-aware sensitivities can help identify which thresholds, schedule variables, or biological parameters most affect final yield, water use, nutrient efficiency, or resilience to environmental stress.

The original crop-science motivation for this project is retained in the following section because it remains a meaningful example of how hybrid dynamical-systems methods can support decision-facing biological modeling outside pharmacology.

## Original crop-science motivation

The project originally grew from an interest in crop-growth, canopy-competition, and trait-optimization models. That motivation remains relevant because plant and crop systems often combine smooth biological growth processes with discrete environmental and management events.

Examples include:

- planting and harvest dates,
- irrigation and fertilization pulses,
- pruning and thinning,
- pest-control interventions,
- greenhouse temperature or light schedules,
- drought and heat-stress events,
- developmental-stage transitions,
- and sensor-triggered management decisions.

A crop model may represent biomass accumulation, canopy development, competition for light, water uptake, nutrient dynamics, and reproductive allocation as continuous processes. Yet the outcomes of practical interest—yield, resilience, resource efficiency, and trait value—may depend strongly on the timing of discrete interventions.

For example, a plant-growth model may include biomass \(W\), leaf area or canopy state \(L\), soil-water availability \(M\), and nutrient availability \(N\):

\[
\dot{W}
=
\alpha L
\frac{M}{K_M+M}
\frac{N}{K_N+N}
-
\delta_W W,
\]

\[
\dot{L}
=
g_L(W,L)
-
\delta_L L,
\]

\[
\dot{M}
=
I(t)
-
u_M(W,L,M)
-
\ell_M(M),
\]

\[
\dot{N}
=
F(t)
-
u_N(W,L,N)
-
\ell_N(N).
\]

Here, \(I(t)\) and \(F(t)\) may include irrigation and fertilizer interventions. At selected event times, the model may apply impulsive updates:

\[
M(t_k^+)
=
M(t_k^-)
+
\Delta M_k,
\]

\[
N(t_k^+)
=
N(t_k^-)
+
\Delta N_k.
\]

The system can also include state-triggered rules. For example, irrigation may occur when soil moisture crosses a lower threshold:

\[
M(t)
\leq
M_{\mathrm{trigger}}.
\]

In a more advanced setting, the intervention policy may depend on developmental stage, weather forecasts, crop stress indicators, or competing resource constraints.

This type of model is structurally similar to the QSP and PK/PD systems emphasized elsewhere in the repository:

- continuous states evolve according to mechanistic differential equations,
- scheduled interventions introduce jumps or changes in forcing,
- threshold conditions trigger mode changes,
- and the timing of events affects long-term outcomes.

The crop-science examples remain useful because they provide intuitive applications for multiple shooting, event-aware sensitivities, and optimization. A crop-management problem can be stated in terms of measurable outcomes such as yield, water use, fertilizer efficiency, or resilience to stress, while still presenting the same numerical challenges that appear in treatment-schedule optimization.

## Software plan

The initial software plan is deliberately narrow. The package should establish a reliable deterministic hybrid core before expanding toward broad model coverage, sophisticated inference, or AI-enabled extensions.

The first implementation should build on Julia’s existing scientific-computing ecosystem rather than recreating solver infrastructure. The package should focus on reusable abstractions for hybrid model specification, event-aware sensitivity propagation, shooting formulations, and user-facing analysis workflows.

The intended design principles are:

- preserve compatibility with existing Julia differential-equation tooling where practical,
- represent event logic explicitly rather than burying it inside ad hoc callbacks,
- distinguish scheduled events from state-triggered events,
- support reset maps and mode changes as first-class model components,
- expose event-aware sensitivities in a form suitable for optimization and inference,
- provide clear diagnostics when trajectories approach grazing or ill-conditioned event configurations,
- and make examples reproducible enough to serve as scientific benchmarks.

A possible early API could allow users to define:

\[
\mathcal{H}
=
\{
\mathcal{Q},
f_q,
h_{q\rightarrow q'},
R_{q\rightarrow q'},
\mathcal{E}_{\mathrm{scheduled}}
\},
\]

where:

- \(\mathcal{Q}\) is a set of modes,
- \(f_q\) is the continuous vector field in mode \(q\),
- \(h_{q\rightarrow q'}\) is an event or guard function,
- \(R_{q\rightarrow q'}\) is a reset map,
- and \(\mathcal{E}_{\mathrm{scheduled}}\) contains scheduled intervention events.

A modeler should be able to specify a system in terms close to the scientific problem:

- what states evolve continuously,
- what interventions occur at fixed times,
- what thresholds trigger a transition,
- how the state changes at each event,
- and what outcomes should be optimized or analyzed.

The package can then construct the numerical machinery required for simulation and sensitivity propagation.

The first user-facing capabilities should include:

- deterministic simulation of hybrid ODE models,
- scheduled event handling,
- state-triggered event detection,
- reset maps and mode transitions,
- continuous variational equations between events,
- saltation or jump-sensitivity updates at events,
- trajectory diagnostics,
- and simple multiple-shooting formulations.

The first examples should prioritize clarity over biological scope. A user should be able to inspect a compact model, run a schedule comparison, visualize event times, compute sensitivities, and understand why the event-aware method differs from a finite-difference perturbation workflow.

Potential supporting components include:

- data structures for modes, events, guards, reset maps, and scheduled interventions,
- wrappers around standard Julia ODE and callback functionality,
- utilities for propagating state-transition and parameter-sensitivity matrices,
- multiple-shooting problem construction,
- continuation or parameter-sweep helpers,
- plotting utilities for trajectories, event times, modes, and sensitivity diagnostics,
- and benchmark scripts that compare hybrid-aware derivatives with finite-difference approximations.

The design should remain modular. A modeler interested only in accurate simulation should not be required to use multiple shooting. A user interested in schedule optimization should be able to build on the same event abstractions without rewriting the model. Future AI, Bayesian, and stochastic extensions should reuse the same representation of known scheduled events, state-triggered transitions, and reset maps.

Interoperability is also an important longer-term design goal. Many QSP and PK/PD models already exist in established ecosystems, and their value should not be lost when hybrid analysis is needed. The package should eventually support import, export, or translation pathways for model structures and dosing/event specifications associated with tools such as NONMEM, nlmixr2/RxODE, Pumas, and related pharmacometric workflows.

The package does not need to solve every interoperability problem in its first release. An initial milestone could focus on clear, documented pathways for recreating a limited class of models or event schedules. Later stages can expand toward more automated translation, validation against reference simulations, and bidirectional exchange of model definitions or simulation outputs.

The immediate objective is to demonstrate a complete and credible workflow, not to maximize feature count:

1. Define a hybrid mechanistic model.
2. Simulate it accurately across scheduled and state-triggered events.
3. Propagate sensitivities through those events.
4. Use the resulting derivatives in schedule, parameter, or boundary-value analysis.
5. Compare the results with simpler finite-difference or single-shooting approaches.
6. Document where hybrid-aware methods materially improve reliability, conditioning, or interpretability.

## Original crop-science motivation

The project originally grew from an interest in crop-growth, canopy-competition, and trait-optimization models. That motivation remains relevant because plant and crop systems often combine smooth biological growth processes with discrete environmental and management events.

Examples include:

- planting and harvest dates,
- irrigation and fertilization pulses,
- pruning and thinning,
- pest-control interventions,
- greenhouse temperature or light schedules,
- drought and heat-stress events,
- developmental-stage transitions,
- and sensor-triggered management decisions.

A crop model may represent biomass accumulation, canopy development, competition for light, water uptake, nutrient dynamics, and reproductive allocation as continuous processes. Yet the outcomes of practical interest—yield, resilience, resource efficiency, and trait value—may depend strongly on the timing of discrete interventions.

For example, a plant-growth model may include biomass \(W\), leaf area or canopy state \(L\), soil-water availability \(M\), and nutrient availability \(N\):

\[
\dot{W}
=
\alpha L
\frac{M}{K_M+M}
\frac{N}{K_N+N}
-
\delta_W W,
\]

\[
\dot{L}
=
g_L(W,L)
-
\delta_L L,
\]

\[
\dot{M}
=
I(t)
-
u_M(W,L,M)
-
\ell_M(M),
\]

\[
\dot{N}
=
F(t)
-
u_N(W,L,N)
-
\ell_N(N).
\]

Here, \(I(t)\) and \(F(t)\) may include irrigation and fertilizer interventions. At selected event times, the model may apply impulsive updates:

\[
M(t_k^+)
=
M(t_k^-)
+
\Delta M_k,
\]

\[
N(t_k^+)
=
N(t_k^-)
+
\Delta N_k.
\]

The system can also include state-triggered rules. For example, irrigation may occur when soil moisture crosses a lower threshold:

\[
M(t)
\leq
M_{\mathrm{trigger}}.
\]

In a more advanced setting, the intervention policy may depend on developmental stage, weather forecasts, crop stress indicators, or competing resource constraints.

This type of model is structurally similar to the QSP and PK/PD systems emphasized elsewhere in the repository:

- continuous states evolve according to mechanistic differential equations,
- scheduled interventions introduce jumps or changes in forcing,
- threshold conditions trigger mode changes,
- and the timing of events affects long-term outcomes.

The crop-science examples remain useful because they provide intuitive applications for multiple shooting, event-aware sensitivities, and optimization. A crop-management problem can be stated in terms of measurable outcomes such as yield, water use, fertilizer efficiency, or resilience to stress, while still presenting the same numerical challenges that appear in treatment-schedule optimization.

## Software plan

The initial software plan is deliberately narrow. The package should establish a reliable deterministic hybrid core before expanding toward broad model coverage, sophisticated inference, or AI-enabled extensions.

The first implementation should build on Julia’s existing scientific-computing ecosystem rather than recreating solver infrastructure. The package should focus on reusable abstractions for hybrid model specification, event-aware sensitivity propagation, shooting formulations, and user-facing analysis workflows.

The intended design principles are:

- preserve compatibility with existing Julia differential-equation tooling where practical,
- represent event logic explicitly rather than burying it inside ad hoc callbacks,
- distinguish scheduled events from state-triggered events,
- support reset maps and mode changes as first-class model components,
- expose event-aware sensitivities in a form suitable for optimization and inference,
- provide clear diagnostics when trajectories approach grazing or ill-conditioned event configurations,
- and make examples reproducible enough to serve as scientific benchmarks.

A possible early API could allow users to define:

\[
\mathcal{H}
=
\{
\mathcal{Q},
f_q,
h_{q\rightarrow q'},
R_{q\rightarrow q'},
\mathcal{E}_{\mathrm{scheduled}}
\},
\]

where:

- \(\mathcal{Q}\) is a set of modes,
- \(f_q\) is the continuous vector field in mode \(q\),
- \(h_{q\rightarrow q'}\) is an event or guard function,
- \(R_{q\rightarrow q'}\) is a reset map,
- and \(\mathcal{E}_{\mathrm{scheduled}}\) contains scheduled intervention events.

A modeler should be able to specify a system in terms close to the scientific problem:

- what states evolve continuously,
- what interventions occur at fixed times,
- what thresholds trigger a transition,
- how the state changes at each event,
- and what outcomes should be optimized or analyzed.

The package can then construct the numerical machinery required for simulation and sensitivity propagation.

The first user-facing capabilities should include:

- deterministic simulation of hybrid ODE models,
- scheduled event handling,
- state-triggered event detection,
- reset maps and mode transitions,
- continuous variational equations between events,
- saltation or jump-sensitivity updates at events,
- trajectory diagnostics,
- and simple multiple-shooting formulations.

The first examples should prioritize clarity over biological scope. A user should be able to inspect a compact model, run a schedule comparison, visualize event times, compute sensitivities, and understand why the event-aware method differs from a finite-difference perturbation workflow.

Potential supporting components include:

- data structures for modes, events, guards, reset maps, and scheduled interventions,
- wrappers around standard Julia ODE and callback functionality,
- utilities for propagating state-transition and parameter-sensitivity matrices,
- multiple-shooting problem construction,
- continuation or parameter-sweep helpers,
- plotting utilities for trajectories, event times, modes, and sensitivity diagnostics,
- and benchmark scripts that compare hybrid-aware derivatives with finite-difference approximations.

The design should remain modular. A modeler interested only in accurate simulation should not be required to use multiple shooting. A user interested in schedule optimization should be able to build on the same event abstractions without rewriting the model. Future AI, Bayesian, and stochastic extensions should reuse the same representation of known scheduled events, state-triggered transitions, and reset maps.

Interoperability is also an important longer-term design goal. Many QSP and PK/PD models already exist in established ecosystems, and their value should not be lost when hybrid analysis is needed. The package should eventually support import, export, or translation pathways for model structures and dosing/event specifications associated with tools such as NONMEM, nlmixr2/RxODE, Pumas, and related pharmacometric workflows.

The package does not need to solve every interoperability problem in its first release. An initial milestone could focus on clear, documented pathways for recreating a limited class of models or event schedules. Later stages can expand toward more automated translation, validation against reference simulations, and bidirectional exchange of model definitions or simulation outputs.

The immediate objective is to demonstrate a complete and credible workflow, not to maximize feature count:

1. Define a hybrid mechanistic model.
2. Simulate it accurately across scheduled and state-triggered events.
3. Propagate sensitivities through those events.
4. Use the resulting derivatives in schedule, parameter, or boundary-value analysis.
5. Compare the results with simpler finite-difference or single-shooting approaches.
6. Document where hybrid-aware methods materially improve reliability, conditioning, or interpretability.

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
