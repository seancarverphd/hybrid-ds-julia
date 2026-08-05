# hybrid-ds-julia

*A Julia package under development for quantitative systems pharmacology (QSP) and PK/PD models that need to handle real treatment logic: dosing pulses, treatment holidays, toxicity holds, threshold-triggered interventions, therapy switches, and other hybrid structure.*

`hybrid-ds-julia` is aimed at **event-aware simulation, sensitivities, and optimization** for mechanistic models whose behavior depends not only on continuous dynamics, but also on when and how clinically meaningful events occur.

The main intended application area is **quantitative systems pharmacology (QSP) and PK/PD**, with a **flagship focus on immuno-oncology tumor–immune models** where treatment is inherently schedule- and event-driven. In that setting, the framework is meant to support dose and schedule optimization, response heterogeneity, relapse and remission dynamics, mechanism differentiation, and translational decision-making.

One promising application is early-phase immunotherapy dose-finding, where toxicity-driven holds, rechallenge, delayed adverse events, and complex schedules are common. In that setting, the framework can help represent treatment decision rules directly inside mechanistic models so that dose, schedule, efficacy, and toxicity can be studied together.

The goal of this project is not to rebuild low-level solver infrastructure from scratch. Instead, it is to build a practical layer on top of Julia’s scientific-computing ecosystem that helps modelers work more effectively with trajectories that cross many events and decision boundaries, while remaining close to the kinds of schedule- and intervention-facing questions that matter in translational pharmacology.

The near-term goal is a compact deterministic core with one flagship biomedical example, a short sequence of higher-dimensional extensions, and one end-to-end workflow that makes the package’s value immediately visible to QSP and PK/PD users.

## What this package is not

`hybrid-ds-julia` is **not** intended to be a full pharmacometrics or NLME platform, a general hybrid-automata toolbox, or a broad symbolic mathematics system. It aims instead to be a focused, event-aware numerical layer for mechanistic QSP and PK/PD models—something that complements existing differential-equation and pharmacometric ecosystems rather than replacing them.

## Why this matters

Many of the most important pharmacology questions are not only about **how much drug is present**, but also about **when interventions happen**, **when thresholds are crossed**, and **how treatment logic changes over time**.

In QSP and PK/PD, those questions appear whenever modelers need to compare regimens, understand relapse versus sustained control, explore toxicity management strategies, or represent adaptive treatment rules that depend on state, schedule, or biomarker thresholds.

These are mainstream translational questions, but they are often handled numerically using workflows that implicitly assume the full model is globally smooth. That is often sufficient for coarse analyses, but it can become fragile when the scientific question depends directly on dose timing, event-triggered interventions, threshold logic, or other regime changes.

`hybrid-ds-julia` is motivated by that gap. The biological questions are already central to QSP and PK/PD practice; what is often missing is a practical, domain-facing numerical layer that treats event structure as a first-class part of the model rather than as an awkward exception.

Key use cases include:

- **Treatment-schedule dependence** — comparing regimens, continuing solutions across timing and dose parameters, and understanding when small changes in regimen logic produce large changes in long-term outcome.
- **Optimization, fitting, and model comparison** — using event-aware sensitivities and multiple shooting to improve conditioning when models contain impulses, event surfaces, or threshold-triggered changes.
- **Mechanism differentiation and SAR** — connecting compound- or mechanism-level differences not only to potency and exposure, but also to the qualitative treatment regimes they produce under realistic intervention logic.
- **Translational decision support** — embedding biomarker thresholds, toxicity triggers, and regimen logic explicitly in the model so outputs speak more directly to robust schedule design and clinically meaningful regime changes.

The longer-term aim is to make hybrid dynamical-systems workflows directly usable for decision-focused pharmacology and QSP work that needs to connect mechanistic models to schedule design, mechanism-of-action differentiation, and early clinical strategy.

## Who is building this

`hybrid-ds-julia` is being developed by **Sean Carver, Ph.D.**, an applied mathematician with doctoral training in dynamical systems at Cornell University, including work with John Guckenheimer on hybrid dynamical-systems models. That background includes variational equations, multiple shooting, continuation methods, and the geometric viewpoint on periodic orbits, bifurcations, and sensitivities that underlies much of modern work in both smooth and hybrid systems.

A preprint of a 2009 paper that Sean Carver published as first author in the journal *Chaos*, with John Guckenheimer and Noah Cowan as coauthors, is available [here](https://limbs.lcsr.jhu.edu/wp-content/papercite-data/pdf/carverlateral2009.pdf). That work, carried out in the laboratory of Noah Cowan, involved hybrid-system computations in which accurate simulation and sensitivity propagation across events were essential.

The preprint contains nine figures in total, and the last three figures, on pages 33–35, are especially relevant here because they visualize the deadbeat manifold described in the text. Each pixel in these plots is the result of solving a boundary value problem, and the manifold is built by solving successive boundary value problems along trajectories that traverse event times, with sensitivities propagated through those events rather than approximated by finite differences. Those figures serve as evidence of prior work on accurate simulation and sensitivity analysis for a hybrid dynamical system. Their construction depends on numerically accurate event handling, boundary value continuation across hybrid transitions, and structured sensitivity propagation. In problems of this kind, naive shooting methods paired with finite-difference sensitivities, even in double-precision arithmetic, are often too ill-conditioned to produce convergent Newton iterates or reliable optimization steps. Permission is currently pending to reproduce these figures and their captions directly in this repository. In the meantime, readers who wish to examine them can consult the linked preprint on the LIMBS website maintained by Noah Cowan, which has been cleared for posting and includes the figures, their captions, and the surrounding discussion explaining what is being visualized and how the computations were carried out.

## Motivation

This project grew out of the observation that many advanced dynamical-systems methods—especially variational equations, multiple shooting, and automatic differentiation for event-driven models—are well developed mathematically but are not yet standard parts of QSP- and PK/PD-facing software workflows.

More broadly, methods that feel standard in one mathematical community are often not standard in nearby application domains. That gap appears clearly in immuno-oncology, QSP, and PK/PD, where mechanistic models are increasingly used for model-informed development but where event-aware sensitivities, impulsive updates, and hybrid treatment logic still need stronger workflow support than is commonly available in domain-facing tools.

The core claim of `hybrid-ds-julia` is therefore not that hybrid mathematics is new. It is that many translational modeling questions already have hybrid structure, and that making these methods usable in practice could improve how those questions are simulated, differentiated, and optimized.

## Why QSP and PK/PD first

QSP and PK/PD are the main intended application areas because they already rely heavily on mechanistic differential-equation models and because many of their most important questions are inherently schedule- and intervention-dependent.

Representative examples include:

- **Immuno-oncology QSP models** with pulsed dosing, immune-response events, or combination treatment logic.
- **Autoimmune and inflammatory disease models** with flare-remission dynamics, tapering, rescue therapy, or biomarker-triggered intervention rules.
- **Mechanistic PK/PD models** with treatment switching, toxicity holds, dose delays, or state-triggered interventions.

These are exactly the kinds of systems in which the state trajectory may remain continuous while the governing equations, treatment rules, or state updates change at event times. That structure suggests event-aware simulation, variational sensitivity propagation, multiple shooting, and automatic differentiation rather than treating the entire trajectory as if it were globally smooth.

At the workflow level, most current QSP and PK/PD practice is built around general differential-equation, PBPK, and pharmacometric toolchains. `hybrid-ds-julia` is not meant to replace that ecosystem. Instead, it aims to complement it with a hybrid numerical layer for models where event structure materially affects simulation, sensitivities, optimization, or translational interpretation.

## Current direction

The immediate focus is to turn the current mathematical and conceptual foundation into a small but credible research platform by implementing a narrow deterministic core, one flagship biomedical example, and a short