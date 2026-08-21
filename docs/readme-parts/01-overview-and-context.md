# hybrid-ds-julia

A Julia-focused research-software project for building, simulating, analyzing, and eventually optimizing hybrid dynamical-systems models. The intended focus is mechanistic ODE models whose continuous dynamics are altered by discrete events such as doses, missed doses, treatment holds, toxicity thresholds, therapy switches, measurements, controller transitions, and other state- or time-triggered interventions.

**Work in progress.** `hybrid-ds-julia` and this README are evolving research-software and documentation projects. The mathematical formulations, implementation plans, application discussions, examples, benchmarks, and references should be treated as provisional unless explicitly identified as implemented, tested, or literature-verified. Interfaces, capabilities, claims, and priorities may change as the package develops and as expert feedback and additional verification are incorporated.

This README is intentionally detailed and modular. Use the table of contents to navigate directly to the mathematical methods, implementation details, computational considerations, application domains, or examples most relevant to your work; readers do not need to read the document linearly.

**Scope, authorship, and verification status.**  This document was drafted and expanded with assistance from a large language model. The assistant was used to help organize material, generate prose, identify possible literature and software context, and formulate questions and technical explanations. Its use does not constitute independent validation of the scientific, mathematical, clinical, engineering, software, or literature claims made here.

Readers should treat the application discussions, software comparisons, computational-scaling guidance, and cited research context as material requiring verification against original literature, authoritative software documentation, and domain-specific expertise before relying on it for research, engineering, clinical, or operational decisions.

The immuno-oncology material supporting the flagship first test bed has received a focused literature review and should be read together with its cited sources. The other application-domain sections, including broader disease, engineering, and author/laboratory discussions, have not yet received the same level of systematic literature verification. They are best understood as structured hypotheses, potential directions, and invitations for expert correction rather than validated claims of applicability.
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

- [Overview](#overview)
- [Project goals](#project-goals)
- [Why hybrid models?](#why-hybrid-models)
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
    - [Fortune: feedback control, locomotor variability, and active sensing in weakly electric fish](#fortune-feedback-control-locomotor-variability-and-active-sensing-in-weakly-electric-fish)
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
- AI/ML/Neural Network extensions to allow hybrid models to be fit to data,
- Parallel ensembles, distributed execution, and large-scale benchmarking;
- Carefully scoped applications in biomedical, scientific, and engineering domains.

The package should not be interpreted as a replacement for domain-specific simulators, clinical judgment, regulatory pharmacometrics, specialized power-system tools, detailed multibody robotics platforms, neural simulators, or validated production systems. Its intended role is complementary: a transparent framework for mechanistic ODE-and-event models when the user can state the relevant dynamics and transitions directly.

## Why hybrid models?

A smooth ODE model has the form:

\[
\dot{x}(t)=f(x(t),t,\theta),
\]

where \(x(t)\) is a continuous state and \(\theta\) is a parameter vector.

A hybrid model additionally has a discrete mode \(q(t)\), event conditions, and updates:

\[
\dot{x}(t)=f_{q(t)}(x(t),t,\theta,u(t)),
\]

with an event guard:

\[
g_i(x(t),t,\theta)=0,
\]

and an event update such as:

\[
x^+=R_i(x^-,t,\theta),
\qquad
q^+=T_i(q^-,x^-,t).
\]

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

## Intended users and use cases