# hybrid-ds-julia

## Introduction

`hybrid-ds-julia` is an event-aware numerical layer for mechanistic QSP and PK/PD models that need to represent real treatment logic: dosing pulses, treatment holidays, toxicity holds, threshold-triggered interventions, therapy switches, and other hybrid structure. It is not a replacement for established pharmacometric platforms such as NONMEM, nlmixr2/RxODE, Monolix, or Pumas; instead, it is designed to sit alongside them and address numerical issues that arise when models contain many events, jumps, and regime changes.

In many current workflows, dosing and other events are encoded via data tables and IF/THEN logic, with sensitivities obtained by finite differences and trajectories treated as if they were globally smooth. Around events, that combination can lead to ill-conditioned gradients, brittle schedule optimization, and noisy parameter sensitivities. By contrast, `hybrid-ds-julia` is built to propagate variational equations across piecewise-smooth flows, apply analytically derived jump and saltation maps at event times, and use multiple shooting to stabilize trajectories and boundary-value computations. The aim is to make those hybrid dynamical-systems tools practically usable for decision-focused pharmacology, so that modelers can study dose, timing, and treatment logic without re-specifying complex models from scratch or fighting fragile numerics around events.

## Table of contents

- [Introduction](#hybrid-ds-julia)
- [What this package is not](#what-this-package-is-not)
- [Why this matters](#why-this-matters)
- [Who is building this](#who-is-building-this)
- [Motivation](#motivation)
- [Why QSP and PK/PD first](#why-qsp-and-pkpd-first)
- [AI-enabled hybrid modeling for translational pharmacology](#ai-enabled-hybrid-modeling-for-translational-pharmacology)
- [Diversity and equity in workflows](#diversity-and-equity-in-workflows)
  - [Diversity in the population](#diversity-in-the-population)
  - [Equity in healthcare](#equity-in-healthcare)
- [Current direction](#current-direction)
- [Current status](#current-status)
- [Mathematical approach](#mathematical-approach)
  - [Piecewise-smooth formulation](#piecewise-smooth-formulation)
  - [Jump phenomena and impulsive updates](#jump-phenomena-and-impulsive-updates)
  - [Variational equations](#variational-equations)
  - [Multiple shooting](#multiple-shooting)
  - [Automatic differentiation](#automatic-differentiation)
- [AI/ML mathematical extensions](#aiml-mathematical-extensions)
  - [Mechanistic--neural hybrid systems](#mechanistic--neural-hybrid-systems)
  - [Physics-informed neural networks](#physics-informed-neural-networks)
  - [Neural hybrid automata](#neural-hybrid-automata)
  - [Neural jump SDEs](#neural-jump-sdes)
- [Test beds](#test-beds)
  - [First biomedical target](#first-biomedical-target)
  - [Next biomedical extensions](#next-biomedical-extensions)
  - [Mechanistic stochastic and Bayesian extensions](#mechanistic-stochastic-and-bayesian-extensions)
  - [Filippov pseudo-Hopf normal form](#filippov-pseudo-hopf-normal-form)
- [Other disease applications](#other-disease-applications)
- [Other computational biology applications](#other-computational-biology-applications)
  - [Predator--prey, pest management, and adaptive harvesting](#predator--prey-pest-management-and-adaptive-harvesting)
  - [Crop growth, canopy competition, and precision agriculture](#crop-growth-canopy-competition-and-precision-agriculture)
  - [Gene regulatory networks, cell-cycle control, and synthetic biology](#gene-regulatory-networks-cell-cycle-control-and-synthetic-biology)
  - [Microbial communities, bioreactors, and pulsed interventions](#microbial-communities-bioreactors-and-pulsed-interventions)
  - [Epidemiology, public-health policy, and adaptive intervention](#epidemiology-public-health-policy-and-adaptive-intervention)
- [Example applications](#example-applications)
  - [QSP and PK/PD](#qsp-and-pkpd)
  - [Translational pharmacology](#translational-pharmacology)
  - [SAR progression and mechanism differentiation](#sar-progression-and-mechanism-differentiation)
  - [Autoimmune and inflammatory disease](#autoimmune-and-inflammatory-disease)
  - [Crop science and precision agriculture](#crop-science-and-precision-agriculture)
- [Original crop-science motivation](#original-crop-science-motivation)
- [Software plan](#software-plan)
- [Roadmap](#roadmap)
  - [Stage 1 — Narrow deterministic core](#stage-1--narrow-deterministic-core)
  - [Stage 2 — Flagship biomedical workflow](#stage-2--flagship-biomedical-workflow)
  - [Stage 3 — QSP-facing workflows](#stage-3--qsp-facing-workflows)
  - [Stage 4 — Mechanistic stochastic and Bayesian extensions](#stage-4--mechanistic-stochastic-and-bayesian-extensions)
  - [Stage 5 — Filippov and benchmark suite](#stage-5--filippov-and-benchmark-suite)
  - [Stage 6 — Refinement and specialization](#stage-6--refinement-and-specialization)
  - [Stage 7 — Interoperability and import/export bridges](#stage-7--interoperability-and-importexport-bridges)
- [Licensing and IP posture](#licensing-and-ip-posture)
- [Further reading](#further-reading)
  - [Related hybrid-systems papers in other domains](#related-hybrid-systems-papers-in-other-domains)
  - [Core dynamical systems / hybrid methods](#core-dynamical-systems--hybrid-methods)
  - [QSP / PK–PD concepts and practice](#qsp--pkpd-concepts-and-practice)
  - [Sensitivity, adjoint, and automatic differentiation](#sensitivity-adjoint-and-automatic-differentiation)
  - [Mechanistic stochastic and Bayesian methods](#mechanistic-stochastic-and-bayesian-methods)
  - [Mechanistic--neural hybrid systems](#mechanistic--neural-hybrid-systems)
  - [Physics-informed neural networks](#physics-informed-neural-networks)
  - [Neural hybrid automata](#neural-hybrid-automata)
  - [Neural jump SDEs](#neural-jump-sdes)
  - [Epidemiology, adaptive intervention, and public-health policy](#epidemiology-adaptive-intervention-and-public-health-policy)
  - [Mechanistic crop models and trait optimization](#mechanistic-crop-models-and-trait-optimization)

*A Julia package under development for quantitative systems pharmacology (QSP) and PK/PD models that need to handle real treatment logic: dosing pulses, treatment holidays, toxicity holds, threshold-triggered interventions, therapy switches, and other hybrid structure.*

Although QSP and PK/PD are the package’s primary application areas, the same event-aware methods may also be useful in other computational-biology settings where continuous biological dynamics interact with pulses, thresholds, switching rules, or adaptive interventions. Examples include autoimmune and inflammatory disease, infectious disease, metabolic disease, cell and gene therapy, ecological and pest-management models, crop and precision-agriculture systems, gene-regulatory networks, microbial communities, bioreactors, and epidemiological models with adaptive public-health policies; see [Other disease applications](#other-disease-applications), [Other computational biology applications](#other-computational-biology-applications), and [Example applications](#example-applications). The framework may also be combined with AI, machine learning, and neural-network components to estimate uncertain biological interactions, reconstruct latent states, learn constrained model-discrepancy terms, or represent stochastic event-rich dynamics while retaining explicit mechanistic and treatment logic; see [AI-enabled hybrid modeling for translational pharmacology](#ai-enabled-hybrid-modeling-for-translational-pharmacology) and [AI/ML mathematical extensions](#aiml-mathematical-extensions).

`hybrid-ds-julia` is aimed at **event-aware simulation, sensitivities, and optimization** for mechanistic models whose behavior depends not only on continuous dynamics, but also on when and how clinically meaningful events occur. The main intended application area is **quantitative systems pharmacology (QSP) and PK/PD**, with a **flagship focus on immuno-oncology tumor–immune models** where treatment is inherently schedule- and event-driven.

One promising application is early-phase immunotherapy dose-finding, where toxicity-driven holds, rechallenge, delayed adverse events, and complex schedules are common. In that setting, the framework can help represent treatment decision rules directly inside mechanistic models so that dose, schedule, efficacy, and toxicity can be studied together.

The goal of this project is not to rebuild low-level solver infrastructure from scratch. Instead, it is to build a practical layer on top of Julia’s scientific-computing ecosystem that helps modelers work more effectively with trajectories that cross many events and decision boundaries, while remaining close to the kinds of schedule- and intervention-facing questions that matter in translational pharmacology.

The near-term goal is a compact deterministic core with one flagship biomedical example, a short sequence of higher-dimensional extensions, and one end-to-end workflow that makes the package’s value immediately visible to QSP and PK/PD users.

## What this package is not

`hybrid-ds-julia` is **not** intended to be a full pharmacometrics or NLME platform, a general hybrid-automata toolbox, or a broad symbolic mathematics system. It aims instead to be a focused, event-aware numerical layer for mechanistic QSP and PK/PD models—something that complements existing differential-equation and pharmacometric ecosystems.

However, interoperability with established pharmacometric and QSP platforms is part of the longer-term vision. In particular, import and export pathways for models and event specifications from tools such as NONMEM, nlmixr2/RxODE, Pumas, and related ecosystems are being considered so that hybrid workflows can be explored without respecifying complex models from scratch.

## Why this matters

Many of the most important pharmacology questions are not only about **how much drug is present**, but also about **when interventions happen**, **when thresholds are crossed**, and **how treatment logic changes over time**.

In QSP and PK/PD, those questions appear whenever modelers need to compare regimens, understand relapse versus sustained control, explore toxicity management strategies, or represent adaptive treatment rules that depend on state, schedule, or biomarker thresholds.

These are mainstream translational questions, but they are often handled numerically using workflows that are sufficient for coarse analyses yet can become fragile when the scientific question depends directly on dose timing, event-triggered interventions, threshold logic, or other regime changes.

`hybrid-ds-julia` is motivated by that gap. The biological questions are already central to QSP and PK/PD practice; what is often missing is a practical, domain-facing numerical layer that treats event structure as a first-class part of the model rather than as an awkward exception.

Key use cases include:

- **Treatment-schedule dependence** — comparing regimens, continuing solutions across timing and dose parameters, and understanding when small changes in regimen logic produce large changes in long-term outcome.
- **Optimization, fitting, and model comparison** — using event-aware sensitivities and multiple shooting to improve conditioning when models contain impulses, event surfaces, or threshold-triggered changes.
- **Mechanism differentiation and SAR** — connecting compound- or mechanism-level differences not only to potency and exposure, but also to the qualitative treatment regimes they produce under realistic intervention logic.
- **Translational decision support** — embedding biomarker thresholds, toxicity triggers, and regimen logic explicitly in the model so outputs speak more directly to robust schedule design and clinically meaningful regime changes.

The longer-term aim is to make hybrid dynamical-systems workflows directly usable for decision-focused pharmacology and QSP work that needs to connect mechanistic models to schedule design, mechanism-of-action differentiation, and early clinical strategy.

## Who is building this

`hybrid-ds-julia` is being developed by **Sean Carver, Ph.D.**, an applied mathematician with doctoral training in dynamical systems at Cornell University, including work with John Guckenheimer on hybrid dynamical-systems models. That background includes variational equations, multiple shooting, continuation methods, and the geometric viewpoint on periodic orbits, bifurcations, and sensitivities that underlies much of modern work in both smooth and hybrid systems.

A preprint of a 2009 paper that Sean Carver published as first author in the journal *Chaos*, with John Guckenheimer and Noah Cowan as coauthors, is available [here](https://limbs.lcsr.jhu.edu/wp-content/papercite-data/pdf/carverlateral2009.pdf). That work, carried out in the laboratory of Noah Cowan, involved hybrid-system computations in which accurate simulation and sensitivity propagation across events were essential. The preprint contains nine figures in total, and the last three figures, on pages 33–35, are especially relevant here because they visualize the deadbeat manifold described in the text. Each pixel in these plots is the result of solving a boundary value problem, and the manifold is built by solving successive boundary value problems along trajectories that traverse event times, with sensitivities propagated through those events rather than approximated by finite differences. Those figures serve as evidence of prior work on accurate simulation and sensitivity analysis for a hybrid dynamical system. Their construction depends on numerically accurate event handling, boundary value continuation across hybrid transitions, and structured sensitivity propagation. In problems of this kind, naive shooting methods paired with finite-difference sensitivities, even in double-precision arithmetic, are often too ill-conditioned to produce convergent Newton iterates or reliable optimization steps. Permission is currently pending to reproduce these figures and their captions directly in this repository. In the meantime, readers who wish to examine them can consult the linked preprint on the LIMBS website maintained by Noah Cowan, which has been cleared for posting and includes the figures, their captions, and the surrounding discussion explaining what is being visualized and how the computations were carried out.

## Motivation

This project grew out of the observation that many advanced dynamical-systems methods—especially variational equations, multiple shooting, and automatic differentiation for event-driven models—are well developed mathematically but are not yet standard parts of QSP- and PK/PD-facing software workflows.

More broadly, methods that feel standard in one mathematical community are often not standard in nearby application domains. That gap appears clearly in immuno-oncology, QSP, and PK/PD, where mechanistic models are increasingly used for model-informed development but where event-aware sensitivities, impulsive updates, and hybrid treatment logic still need stronger workflow support than is commonly available in domain-facing tools.

To reiterate, the core claim of `hybrid-ds-julia` is not that hybrid mathematics is new. It is that many translational modeling questions already have hybrid structure, and that making event-aware sensitivity propagation and trajectory optimization usable in practice could substantially improve how those questions are simulated and analyzed.

## Why QSP and PK/PD first

QSP and PK/PD are the main intended application areas because they already rely heavily on mechanistic differential-equation models and because many of their most important questions are inherently schedule- and intervention-dependent.

Representative examples include:

- **Immuno-oncology QSP models** with pulsed dosing, immune-response events, or combination treatment logic.
- **Autoimmune and inflammatory disease models** with flare-remission dynamics, tapering, rescue therapy, or biomarker-triggered intervention rules.
- **Mechanistic PK/PD models** with treatment switching, toxicity holds, dose delays, or state-triggered interventions.

These are exactly the kinds of systems in which the state trajectory may remain continuous while the governing equations, treatment rules, or state updates change at event times.

At the workflow level, most current QSP and PK/PD practice is built around general differential-equation, PBPK, and pharmacometric toolchains. `hybrid-ds-julia` is not meant to replace that ecosystem. Instead, it aims to complement it with a hybrid numerical layer for models where event structure materially affects simulation, sensitivities, optimization, or translational interpretation.

## AI-enabled hybrid modeling for translational pharmacology

`hybrid-ds-julia` is primarily an event-aware numerical layer for mechanistic QSP and PK/PD models. Its longer-term relevance to AI-enabled model-informed drug development lies in combining explicit biological and clinical structure with learned components where data are informative and mechanistic knowledge is incomplete.

Potential directions include mechanistic--neural hybrid models, in which a neural network represents an uncertain biological interaction or model-discrepancy term; physics-informed neural networks for latent-state reconstruction and parameter learning from sparse data; neural hybrid automata for data-driven discovery of candidate modes and transition structure; and neural jump SDEs for stochastic event-rich processes. These methods could support regimen optimization, translational prediction, virtual-patient updating, and decision support while retaining explicit representations of known doses, toxicity thresholds, treatment holds, therapy switches, and other clinically meaningful event logic.

The intended role of `hybrid-ds-julia` is not to replace mechanistic pharmacology with a black-box predictor. Instead, it is to provide the event-aware simulation, sensitivity, and optimization structure needed to connect learned components to mechanistic models in a way that remains interpretable, testable, and relevant to treatment decisions. The mathematical implications, limitations, and possible implementations of these approaches are discussed in [AI/ML mathematical extensions](#aiml-mathematical-extensions).

## Diversity and equity in workflows

These methods naturally extend to questions of diversity and equity because they allow population-level variability and decision rules to be represented explicitly in the dynamics rather than averaged away. By treating event logic, thresholds, and treatment schedules as first-class components of the model, `hybrid-ds-julia` can be used to explore how heterogeneous patient trajectories respond to real-world intervention policies and access constraints.

### Diversity in the population

In a population setting, hybrid, event-aware workflows make it straightforward to embed variation in pharmacokinetics, pharmacodynamics, immune dynamics, and treatment decision rules across virtual patients. Differences in comorbidities, concomitant medications, biomarker baselines, and toxicity susceptibility can be represented as structured heterogeneity in continuous parameters and event thresholds, while variation in adherence, clinic visit patterns, and rescue criteria appear as heterogeneity in the discrete treatment logic. Because the solver and sensitivities are designed to respect regime changes, one can then study how small shifts in regimen design, monitoring frequency, or threshold policies produce large differences in long-term outcomes across a diverse cohort, rather than only at an “average” patient level.

### Equity in healthcare

Equity questions arise whenever access, monitoring, and intervention timing differ across patient groups, even for the same nominal regimen. Within a hybrid QSP or PK/PD model, those differences can be formalized as alternative event structures: delayed or missed doses, sparser biomarker sampling, higher thresholds for toxicity-driven holds, or different rescue rules and treatment switches. By simulating such policy- and access-induced event differences side by side, `hybrid-ds-julia` can help quantify how inequities in care pathways translate into inequities in exposure, disease control, and toxicity risk, and can support schedule and decision-rule designs that are more robust across structurally disadvantaged subgroups. The aim is not only to capture biological heterogeneity, but also to make disparities in treatment delivery visible at the level of mechanistic trajectories and their sensitivities, where they can inform more equitable regimen and monitoring strategies.

## Current direction

The immediate focus is to turn the current mathematical and conceptual foundation into a small but credible research platform by implementing a narrow deterministic core, one flagship biomedical example, and a short sequence of higher-dimensional extensions.

The package will be strongest if its first public milestones are reproducible, technically convincing, and clearly tied to end-to-end event-aware workflows that a QSP or PK/PD modeler can recognize: model specification, simulation across events, sensitivity propagation through jumps and regime changes, and schedule- or parameter-facing analysis.

That near-term scope is intentionally narrow. A focused, working demonstration is more valuable at this stage than broad coverage of every hybrid-system variant.

## Current status

The repository currently functions primarily as a conceptual and methodological foundation for the package.

The next implementation targets are:

- a deterministic hybrid core,
- a fully worked flagship biomedical example,
- a short sequence of higher-dimensional biomedical extensions,
- and accompanying documentation that shows the workflow from model specification through simulation, sensitivities, and schedule- or parameter-facing analysis.

The initial flagship example will be chosen to make the translational value of the package clear early: not only that the model is hybrid in a mathematical sense, but that event-aware numerics improve the ability to compare regimens, analyze treatment logic, and reason about clinically meaningful regime changes.