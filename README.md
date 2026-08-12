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
  - [SDE / stochastic methods](#sde--stochastic-methods)
  - [AI, ML, and neural-network methods](#ai-ml-and-neural-network-methods)
  - [Mechanistic crop models and trait optimization](#mechanistic-crop-models-and-trait-optimization)

*A Julia package under development for quantitative systems pharmacology (QSP) and PK/PD models that need to handle real treatment logic: dosing pulses, treatment holidays, toxicity holds, threshold-triggered interventions, therapy switches, and other hybrid structure.*

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

## Mathematical approach

### Piecewise-smooth formulation

A typical mechanistic model is represented by a state vector `x`, with dynamics treated as piecewise smooth:

```text
dx/dt = f_k(x, t)   for t in [t_k, t_{k+1})
```

where the index `k` labels the active interaction or control regime. Whenever the system crosses an event surface—for example, a dosing time, a toxicity threshold, or the activation of a new interaction term—the governing vector field changes from `f_k` to `f_{k+1}`. This places the model in the general class of **hybrid dynamical systems**, where continuous trajectories are punctuated by discrete structural changes.

For a QSP or PK/PD modeler, this is the difference between treating doses and intervention rules as small perturbations in an otherwise smooth system and treating them explicitly as regime-changing events that the solver and sensitivity calculations are designed to respect.

### Jump phenomena and impulsive updates

Many application-facing models are not only piecewise smooth in the sense that the governing vector field changes between regimes; they also contain **explicit jump phenomena**, where the state itself is updated discontinuously at an event time.

This distinction matters computationally. Between jumps, one integrates a smooth differential-equation segment; at a jump, one applies an explicit state update; after the jump, one restarts integration under the same or a different vector field. That viewpoint makes it easier to generalize from one treatment model to a broad class of event-rich mechanistic models.

A standard representation is:

```text
dx/dt = f_k(x, t)          for t in (t_k, t_{k+1})
x(t_k^+) = G_k(x(t_k^-), p)
```

where `x(t_k^-)` denotes the state immediately before the event, `x(t_k^+)` the state immediately after it, and `G_k` is a jump map that may depend on parameters `p`.

It also matters for sensitivities and optimization. If the event is a prescribed-time reset, then the sensitivity update uses the Jacobian of the jump map `G_k`. If the event time depends on the state, then the correct first-order update across the event is the **saltation matrix**, which combines the jump-map Jacobian with the timing correction induced by the shift in event time.

In PK/PD terms, these jump maps are not exotic abstractions. They are a direct formalization of dosing rules, pulsed interventions, and state-triggered treatment updates that already appear in many mechanistic workflows.

### Variational equations

Let `n` denote the dimension of the original state vector. To obtain well-conditioned sensitivities, the package is intended to evolve both the state `x(t)` and the Jacobian of the flow.

Along each smooth segment, the Jacobian of the flow `J(t) = ∂x(t) / ∂x(t_k)` satisfies:

```text
dJ/dt = (D_x f_k)(x(t), t) · J(t),   with   J(t_k) = I
```

where `D_x f_k` denotes the Jacobian of `f_k` with respect to the state.

This yields an augmented system of dimension `n + n^2`: the original `n` equations together with the `n^2` variational equations. The point is to propagate local sensitivities in a way that respects the event-driven structure of the model.

For hybrid systems, this continuous sensitivity propagation is only part of the story. The other part of the story is, of course, the events. The sensitivity of the smooth flow must be composed with the local sensitivity update at the event. For scheduled events, such as bolus dosing at predetermined times, the jump sensitivity is simply the Jacobian of the jump map. For state-triggered events, such as toxicity-triggered interventions, the sensitivity must account for the fact that nearby trajectories reach the event surface at different times. The resulting local sensitivity update is called the saltation matrix.

Without these event-aware sensitivity updates, gradients for dose, timing, and schedule optimization can become noisy or misleading around events. With them, gradient-based methods have a better chance of behaving as reliably in event-rich models as they do in smoother settings.

### Multiple shooting

Given a sequence of event times or event surfaces, the full trajectory can be reformulated as a **multiple-shooting problem**:

- Integrate the model separately on each smooth segment.
- Use the variational equations to compute the Jacobian of each segment map.
- Apply the appropriate jump-map Jacobian for scheduled resets, or the saltation matrix for state-triggered events.
- Use a Newton-type solver to adjust the segment start points so that the end of each segment matches the beginning of the next, enforcing a single continuous trajectory across all segments where continuity is required and the prescribed jump conditions where impulses occur.

This often yields a better-conditioned trajectory and sensitivity framework than naive single shooting when the model contains many event-driven structural changes or explicit impulsive interventions. For QSP- and PK/PD-facing workflows, the practical value is that multiple shooting can stabilize computations in models with many events, making continuation, fitting, and schedule comparison less brittle than they may be under a naive all-at-once forward simulation strategy.

### Automatic differentiation

**Automatic differentiation** is central to the package vision because it provides a practical way to compute Jacobians of the vector field, Jacobians of jump maps, and gradients of scalar objectives without fragile finite-difference approximations. In event-driven, high-dimensional mechanistic models, this is especially valuable when those derivatives are used inside variational equations, jump updates, multiple-shooting solvers, and gradient-based optimization loops.

From a workflow perspective, automatic differentiation is part of what can make hybrid simulation usable in practice rather than only analyzable on paper.

## AI/ML mathematical extensions

The deterministic framework above provides the mathematical foundation for the following possible AI/ML extensions. These are research directions rather than requirements of the initial package scope; the near-term priority remains a transparent, validated deterministic hybrid core.

### Mechanistic--neural hybrid systems

A natural later extension of `hybrid-ds-julia` is a mechanistic--neural hybrid model, including variants often described as neural ordinary differential equations or universal differential equations. In a pure neural ODE, a neural network defines all or most of the continuous-time vector field. In a mechanistic--neural hybrid, the known pharmacology remains explicit and a neural network represents a limited, declared source of uncertainty: an unmodeled biological interaction, a latent process, an observation mechanism, or a model-discrepancy term.

A representative hybrid-regime formulation is:

```text
dx/dt = f_k(x, t, p) + g_{θ,k}(x, t, p)
```

Here `f_k` is the mechanistic vector field in regime `k`, `g_{θ,k}` is a neural-network correction with weights `θ`, and scheduled doses, jump maps, event surfaces, and treatment rules remain explicit. For example, a tumor--immune model could retain its PK structure, dosing pulses, toxicity guard, and treatment-hold logic while learning an uncertain immune-mediated killing term, resistance mechanism, or latent biomarker process.

The main difference between this approach and a conventional mechanistic hybrid model is that the continuous biological dynamics are no longer assumed to be completely specified. The neural component adds flexibility within each regime. It does not, by itself, discover or replace the hybrid structure: a known toxicity threshold should still be encoded as a guard; a known dose should still be represented as a scheduled jump; and a known therapy change should still be represented as a mode transition or reset. This separation allows the neural component to improve fit or represent missing biology without sacrificing the interpretability of clinical decision logic.

The numerical ideas underlying `hybrid-ds-julia` extend directly to this setting. Between events, variational equations use the Jacobian of the combined field, including derivatives of the neural correction with respect to state, mechanistic parameters, and possibly neural-network weights. Automatic differentiation can provide these derivatives. At a scheduled reset, sensitivity propagation still uses the jump-map Jacobian. At a state-triggered event, the saltation update still accounts for perturbation-induced shifts in event time. Thus, neural components do not make event-aware sensitivities unnecessary; they make it more important to distinguish uncertainty in continuous biology from explicitly modeled intervention structure.

ReLU-based neural networks introduce an additional piecewise-smooth structure. Each activation boundary is a codimension-one surface in state space, and the network has a distinct affine representation within each region of fixed activation pattern. When a ReLU network contributes only to a continuous vector field, a transverse activation crossing generally does not cause a state jump: ReLU is continuous, and the corresponding saltation update is the identity when the full vector field is continuous across that boundary. However, the vector-field Jacobian changes, so variational integration must continue using the Jacobian in the newly active region.

The principal pain points are the large number of possible activation regions in deep ReLU networks, nonunique classical derivatives at activation boundaries, and loss of ordinary differentiability at grazing events, simultaneous activation changes, or event-sequence changes. These issues can complicate adjoints, Newton iterations, continuation, and bifurcation analysis. A practical initial design would use smooth activations, such as softplus, tanh, or Swish, for neural corrections to continuous biological dynamics, while reserving explicit guards, resets, and mode transitions for known clinical events. ReLU neural ODEs and generalized sensitivity analysis remain an important later research direction, especially where learned piecewise-linear structure is itself scientifically informative.

### Physics-informed neural networks

Physics-informed neural networks, or PINNs, use mechanistic equations as constraints during neural-network training. Rather than treating an ODE solver as the sole means of generating a trajectory, a PINN represents an unknown state trajectory with a neural network and penalizes deviations from governing equations, observed data, and initial or boundary conditions. In a QSP or PK/PD setting, this can help reconstruct latent state trajectories and estimate parameters from sparse, irregularly sampled, noisy, or partially observed data.

The difference from a mechanistic--neural hybrid is the role of the neural network. In a mechanistic--neural hybrid, the network is part of the differential equation itself and represents an unknown term in the evolving dynamics. In a PINN, the network more often represents the solution trajectory or a parameterized approximation to it, while the mechanistic ODE remains a constraint in the training objective. The distinction is not absolute: a workflow can use both a learned correction term and physics-informed training.

A hybrid physics-informed formulation must extend the usual smooth ODE residual to account for events. At scheduled resets, the learned trajectory must satisfy the jump map; at state-triggered events, it must represent both the guard condition and the possibility that perturbations alter event time. Thus, an event-rich QSP model should be organized around smooth segments, jump conditions, and mode-dependent dynamics rather than one global smooth residual. This is a natural point of contact with the event-aware simulation, sensitivity, and multiple-shooting abstractions proposed by `hybrid-ds-julia`.

Pain points include sensitivity to loss weighting, network architecture, collocation-point placement, stiffness, parameter nonidentifiability, and competing data and physics residuals. Sharp transients, multiple time scales, and switching boundaries are especially challenging for a single globally smooth network approximation. A later research direction is an event-aware or segmented PINN workflow in which `hybrid-ds-julia` defines intervals, guards, resets, and hybrid sensitivities while mode-conditioned neural models reconstruct latent trajectories from sparse data.

### Neural hybrid automata

Neural hybrid automata use neural networks or other learned components to infer modes, mode-specific dynamics, guards, transitions, and sometimes reset behavior from data. Instead of starting with a fully specified set of treatment regimes and clinical rules, a neural hybrid automaton attempts to identify some or all of the discrete structure that explains observed trajectories.

This differs from the preceding approaches in the amount of hybrid structure learned from data. A mechanistic--neural hybrid assumes clinically meaningful modes, guards, and resets are known while learning limited continuous-time corrections. A PINN normally assumes governing equations are known and uses them to constrain reconstruction. A neural hybrid automaton can instead learn the mode decomposition and transition structure themselves. It offers greater flexibility, but correspondingly weaker direct interpretability unless learned modes can be validated and given clear biological or clinical meaning.

In pharmacology, mode labels and transition rules may be confounded with unobserved covariates, measurement noise, patient heterogeneity, missing doses, or a misspecified continuous model. Hard learned mode decisions also complicate gradient-based fitting, uncertainty quantification, and counterfactual regimen analysis. A promising use in `hybrid-ds-julia` is therefore model discovery and hypothesis generation: data-driven methods could propose candidate modes or transition mechanisms, after which scientifically credible candidates could be translated into explicit hybrid models with interpretable guards, jump maps, and sensitivity calculations.

### Neural jump SDEs

Neural jump stochastic differential equations combine continuous-time learned dynamics with stochastic fluctuations and random jump events. A representative form is:

```text
dx = f_θ(x, t) dt + σ_θ(x, t) dW_t + J_θ(x, t) dN_t.
```

Here `W_t` represents continuous random variation and `N_t` a counting process for random events. Neural components may represent the drift, diffusion, jump size, jump intensity, or latent event process. For pharmacology, such models could eventually represent irregular adherence, unrecorded interventions, stochastic toxicity or flare events, and cellular or molecular variability.

Neural jump SDEs should be distinguished from the mechanistic stochastic hybrid models described in the test-bed section below. In a mechanistic stochastic model, the state variables, drift, diffusion form, scheduled dose maps, jump maps, event rules, and observation model are specified from biological and pharmacological knowledge; data estimate parameters, latent states, and uncertainty. In a neural jump SDE, one or more of these functions is represented by a trainable neural network. Compared with neural hybrid automata, transitions need not be deterministic functions of guards; compared with PINNs, the model represents a distribution over paths rather than only a constrained deterministic trajectory.

The technical challenges are substantial. Inference may require particle filtering, sequential Monte Carlo, variational inference, or repeated simulation for approximate likelihood evaluation. It can be difficult to distinguish random jumps from observation noise, unmeasured covariates, model discrepancy, or an inadequately specified deterministic event rule. Gradient estimates can be high variance when jump times change. The appropriate future path is staged: first establish reliable deterministic event-aware methods, then add one narrow mechanistic stochastic model class, and only later evaluate learned jump mechanisms when available data justify their added flexibility.

## Test beds

### First biomedical target

The first biomedical model planned for this workflow is the hybrid impulsive tumor–immune model with immunotherapy and chemotherapy studied in *[Analysis of a Hybrid Impulsive Tumor-Immune Model with Immunotherapy and Chemotherapy](https://www.sciencedirect.com/science/article/abs/pii/S0960077920310080)*.

This model is intended to serve as the flagship early implementation target for the package, not just as a motivating example. It is a strong first biomedical target because the hybrid structure is not incidental: treatment is represented through pulsed interventions of different frequencies, so the long-term behavior depends directly on event timing, treatment scheduling, and the interaction between continuous tumor–immune dynamics and impulsive updates.

From a pharmacology and QSP perspective, it sits close to the kinds of questions decision-makers care about: how treatment frequency, timing, and combination strategy influence tumor control, loss of control, and the robustness of a regimen under changing conditions.

### Next biomedical extensions

After the Zhao model, the natural next step is a hierarchy of higher-dimensional hybrid models that preserve its core treatment-logic structure while adding the pharmacology and resistance features developed in Pang et al. (*[Mathematical Modelling and Analysis of the Tumor Treatment Regimens with Pulsed Immunotherapy and Chemotherapy](https://onlinelibrary.wiley.com/doi/10.1155/2016/6260474)*).

The Zhao model is a strong first flagship because it is genuinely hybrid in a way that matters for translational modeling: it combines continuous tumor–immune dynamics with fixed-time immunotherapy pulses and state-triggered chemotherapy when tumor burden reaches a threshold. That makes it ideal for establishing the package’s core workflow—event-aware simulation, jump handling, sensitivity propagation across events, and schedule-facing analysis—in a system that is small enough to understand clearly yet rich enough to demonstrate why hybrid structure matters.

The next stage is to extend that model upward in dimension without losing its threshold-driven hybrid logic. A first generalization would add an explicit chemotherapy concentration variable, producing a 3D hybrid model that retains Zhao’s event structure while introducing a PK-like state absent from the original formulation. From there, the model can be expanded to include drug-resistant tumor subpopulations and eventually multiple chemotherapy agents on distinct schedules, yielding 4D and 6D variants that incorporate features present in Pang et al., such as explicit drug concentrations, resistant subpopulations, and multidrug treatment structure. This creates a coherent model ladder for `hybrid-ds-julia`: Zhao as the entry-point flagship, followed by increasingly realistic hybrid QSP-style models that stress-test the same numerical machinery in settings closer to PK/PD, resistance, and treatment optimization.

### Mechanistic stochastic and Bayesian extensions

A natural later extension of `hybrid-ds-julia` is a mechanistically specified stochastic hybrid model. In this approach, the modeler specifies the biological state variables, continuous drift structure, diffusion or process-noise model, scheduled dose maps, state-triggered event rules, and observation model in advance. The unknowns generally include parameters, patient-level effects, latent states, and uncertainty about competing mechanistic hypotheses—not the basic mathematical form of the dynamics.

For example, a stochastic tumor–immune model could retain explicit tumor-growth and immune-cell interactions, pharmacokinetic states, scheduled treatment pulses, and toxicity-triggered holds while using an SDE to represent intrinsic biological variability or unobserved patient-level fluctuations. Bayesian or particle-based inference could then estimate parameters and update uncertainty as new measurements become available. This differs from the neural jump SDE approaches discussed in [AI/ML mathematical extensions](#aiml-mathematical-extensions), in which some or all of the drift, diffusion, jump-size, or event-intensity functions are represented by learned neural components.

In a sequential Bayesian workflow, the posterior from one inference step becomes the prior for the next, while the model dynamics determine how new data update the likelihood. This is a standard perspective in sequential Bayesian updating and related Monte Carlo methods.

For stochastic models, the smooth ODE dynamics between events are replaced by a stochastic differential equation (SDE) that generates continuous but typically nowhere differentiable sample paths between jumps. Impulsive dose times, threshold-triggered jumps, and regime switches remain explicitly represented in the hybrid structure, but the continuous evolution between events is now driven by drift and diffusion terms rather than a deterministic vector field. In that setting, the solver would propagate sample paths between events, apply jump maps at intervention times, and use the resulting transition law or predictive distribution to evaluate likelihood contributions for new observations. A natural goal in such workflows is to compute not only sensitivities of individual sample paths, but also sensitivities of moments or summary functionals—for example, mean exposure, variance of biomarker trajectories, or event-time distributions—with respect to parameters and schedule design. In practice, these stochastic sensitivities would be obtained from variational SDEs for pathwise parameter derivatives and from Monte Carlo estimators, including pathwise-gradient or score-function/Malliavin-weight methods, for sensitivities of expectations and other statistics of interest.

This suggests a Bayesian extension layer in which hybrid simulation is combined with MCMC, sequential tempered MCMC, or particle-filtering ideas. The practical role of `hybrid-ds-julia` in such a workflow would be to provide event-aware deterministic or stochastic simulation, expose the hybrid structure cleanly enough to support likelihood construction, and eventually enable sensitivity-aware inference for parameter learning, schedule learning, or virtual-patient updating in event-rich mechanistic models.

### Filippov pseudo-Hopf normal form

Before applying these ideas to more complex biomedical models, it is useful to validate them on a low-dimensional system whose analytical structure is well understood. A natural choice is the planar Filippov **pseudo-Hopf** normal form in the “two invisible tangencies” case studied by Kuznetsov, Rinaldi, and Gragnani in *[One-parameter Bifurcations in Planar Filippov Systems](https://pure.iiasa.ac.at/id/eprint/6817/)*.

This system is a strong test bed for `hybrid-ds-julia` because it is two-dimensional, canonical in the Filippov literature, and exercises exactly the non-smooth machinery the package aims to provide: event detection at the switching surface, handling of sliding and crossing dynamics, construction of Poincaré maps for hybrid orbits, and continuation of limit cycles through a discontinuity-induced bifurcation.

A natural early milestone is to reproduce the pseudo-Hopf scenario robustly—tracking the birth of the crossing limit cycle, its stability, and its dependence on a bifurcation parameter—before turning to higher-dimensional biomedical models.

## Other disease applications

The first application and tests of `hybrid-ds-julia` will be in immuno-oncology, where event-aware hybrid modeling is especially relevant because treatment schedules, combination regimens, biomarker thresholds, resistance, and therapy switching are central to the biology and the decision-making context.

In **cardiometabolic disease**, especially diabetes and obesity, the **continuous part** is glucose, insulin, and broader metabolic-state evolution over time, while the **discrete part** is meals, insulin boluses, dose changes, hypoglycemia rescue actions, and other threshold-triggered interventions. Hybrid modeling matters here because glycemic control questions hinge on both gradual metabolic dynamics and abrupt, rule-driven actions that reshape those dynamics.

In **neurology and CNS disease**, the **continuous part** is slow disease progression and biomarker evolution—for example, neurodegeneration or lesion burden—while the **discrete part** is clinical decision logic: regimen changes, rescue interventions, stage transitions, and other state-dependent treatment updates. Hybrid modeling matters here because episodic decisions, relapses, and threshold-based escalations punctuate an otherwise gradual trajectory.

In **immunology and inflammation**, the **continuous part** is the inflammatory and immune-state dynamics—cytokines, cell populations, and tissue damage—while the **discrete part** is flare-triggered rescue therapy, tapering decisions, switching between treatment strategies, and agent-based or cellular events that induce regime changes. Hybrid modeling matters here because flare–remission patterns are shaped by both ongoing immune dynamics and intermittent, guideline- or state-driven interventions.

In **infectious disease, especially tuberculosis**, the **continuous part** is within-host infection, immune response, and pathogen-growth dynamics, while the **discrete part** is combination therapy, adherence or missed-dose events, resistance-triggered regimen changes, and latent-to-active transitions that switch the system into new regimes. Hybrid modeling matters here because long-term outcomes depend critically on when therapy is taken, when resistance emerges, and when latent infection reactivates—not just on average exposure.

Overall, the value of `hybrid-ds-julia` is greatest in disease areas where the questions are not just about the continuous evolution of a biomarker, but also about when interventions occur and how those interventions change the governing dynamics.

## Other computational biology applications

Although `hybrid-ds-julia` is initially focused on QSP, PK/PD, and translational pharmacology, the same numerical framework applies more broadly to computational-biology models in which continuous biological dynamics interact with discrete interventions, threshold rules, regulatory switches, or changing interaction structure. These applications are not intended to dilute the pharmacology-first implementation strategy. Rather, they provide scientifically meaningful test beds in which event-aware simulation, sensitivity propagation, multiple shooting, continuation, and optimization can be developed and validated.

### Predator--prey, pest management, and adaptive harvesting

In predator--prey, food-web, and pest-management models, the **continuous part** consists of population growth, predation, resource limitation, competition, migration, seasonal forcing, and population recovery. The **discrete part** can include harvesting pulses, predator stocking, pesticide applications, biological-control releases, threshold-based management actions, seasonal policy changes, extinction or reintroduction rules, and switching in refuge or feeding behavior.

These systems provide a natural family of low-dimensional hybrid test beds because they can exhibit multiple equilibria, oscillations, threshold effects, and bifurcations even before intervention logic is added. Hybrid management rules make intervention timing part of the scientific question: for example, when a pest population should trigger biological control, how harvesting intensity should change after a population threshold is crossed, or whether a small change in intervention timing shifts the system from persistent coexistence to collapse.

This application is also directly relevant to the Filippov pseudo-Hopf and sliding-dynamics benchmark proposed elsewhere in this README. In ecological models with a discontinuous threshold policy—for example, switching harvesting, chemical control, refuge use, or predator behavior when a population ratio crosses a boundary—the vector fields on either side of the switching surface can point toward that surface. In that case, trajectories may remain on the boundary for a finite time and evolve according to a Filippov sliding vector field. Such models can therefore contain sliding regions, pseudo-equilibria, grazing events, and sliding bifurcations, making them particularly useful for validating switching-surface handling, continuation, and sensitivity calculations near non-smooth transitions.

### Crop growth, canopy competition, and precision agriculture

In crop models, the **continuous part** can include plant biomass, developmental stage, leaf area, canopy structure, soil moisture, nutrient availability, pest burden, pathogen burden, and yield-related traits. The **discrete part** can include changes in plant interaction networks as canopies overlap, irrigation and fertigation events, planting and harvest, pruning, pest-management interventions, water- or nutrient-stress thresholds, and biological interventions such as RNA sprays, viral gene modulation, or signalling peptides.

This application connects directly to the original Bambara-groundnut motivation for the package. In a multiscale crop model, plant trajectories may remain continuous while local interaction structure and growth rates change abruptly as new canopy-competition relationships become active. The same framework could eventually support precision-agriculture questions involving adaptive irrigation, fertilization, pest management, and robust management policies under weather, soil, and population variability. The common mathematical issue is the same as in pharmacology: a continuous biological system is shaped by interventions and interaction changes that occur at discrete times or thresholds.

Sliding dynamics are not usually an intrinsic feature of crop-growth or canopy-competition models. Many crop events are scheduled, impulsive, or produce a one-time change in the active vector field, so trajectories cross the corresponding event surface rather than remain on it. Sliding could arise, however, in an idealized discontinuous feedback controller—for example, if irrigation or fertigation switches instantaneously at a soil-moisture or plant-water-stress threshold and the competing vector fields both drive the system toward that threshold. In practice, hysteresis, actuator delay, or smooth control laws may be more realistic than sustained Filippov sliding, but the possibility is relevant when designing threshold-based management policies.

### Gene regulatory networks, cell-cycle control, and synthetic biology

In gene-regulatory, cell-cycle, and synthetic-biology models, the **continuous part** consists of mRNA, protein, metabolite, signalling molecule, and cell-population concentrations, together with degradation, translation, enzymatic reactions, feedback, and transport. The **discrete part** can include transcriptional activation or repression, regulatory modules switching between active and inactive states, cell-cycle checkpoints, threshold-based cell-fate decisions, inducible gene expression, optogenetic stimulation, cell division, and externally applied molecular pulses.

These systems are useful because the switching logic is often closely tied to known biological mechanisms. A hybrid representation can preserve interpretable regulatory rules while allowing continuous concentration dynamics to be analyzed with event-aware sensitivities. Potential future applications include parameter estimation for switching gene circuits, optimization of pulsed induction schedules, continuation of cellular oscillations, and analysis of how threshold perturbations alter cell-fate or cell-cycle outcomes.

Sliding dynamics can occur in piecewise-affine and Filippov formulations of gene-regulatory networks. For example, if regulatory threshold rules define different vector fields on either side of a switching domain and the flows point toward that domain, a solution may remain on the switching surface for a finite interval. Such sliding-mode solutions have been studied in piecewise-linear models of genetic regulatory networks. Whether sliding is biologically appropriate in a particular model requires care: a sharp Boolean or threshold approximation may produce sliding where a more detailed Hill-function, stochastic, or time-delayed model would instead produce a rapid but smooth transition. This makes gene regulation a useful research setting for comparing explicit non-smooth formulations with smooth regularizations.

### Microbial communities, bioreactors, and pulsed interventions

In microbial-community and bioreactor models, the **continuous part** can include microbial biomass, substrate concentrations, metabolites, dissolved oxygen, pH, temperature, and the relative abundance of competing populations. The **discrete part** can include batch feeding, dilution, harvesting, inoculation, antibiotic or phage pulses, oxygen-control policies, environmental shifts, metabolic-regime changes, and threshold-triggered changes in operating conditions.

These models could serve as useful intermediate test beds between low-dimensional ecological systems and higher-dimensional QSP models. They can combine multiple time scales, partial observability, pulsed interventions, population competition, and regime changes while retaining relatively direct experimental interpretation. Event-aware simulation and sensitivity analysis could support design of feed schedules, perturbation experiments, control policies, and robust operating regimes in the presence of biological variability.

Sliding dynamics are not generally expected in ordinary batch or fed-batch models with scheduled inputs. They can arise in idealized discontinuous feedback settings, however, such as instantaneous switching of aeration, dilution, pH control, substrate feed, or antibiotic administration at a specified threshold. If the vector fields on both sides direct the state toward the operating boundary, a Filippov sliding description can be mathematically appropriate. In laboratory and industrial settings, hysteresis, sampling intervals, actuator limits, and controller dynamics will often regularize this behavior, but the non-smooth limit can still be a valuable model for understanding threshold-control design and numerical robustness.

## Example applications

The same mathematical and computational ideas can be used across a range of mechanistic modeling problems in pharmacology and beyond.

### QSP and PK/PD

In QSP and PK/PD, `hybrid-ds-julia` is intended to make event-aware simulation, variational sensitivity propagation, and multiple shooting natural parts of the workflow for models with dosing pulses, treatment holidays, toxicity holds, and threshold-mediated biological responses.

This makes it easier to study how the timing and logic of interventions shape long-term outcomes such as remission, relapse, resistance, or sustained control. It also opens the door to more systematic optimization over dose, timing, and treatment rules rather than relying only on hand-picked regimen comparisons.

### Translational pharmacology

Many of the most important translational questions are inherently dynamical: whether a schedule sustains control, whether biomarker trajectories indicate a regime shift, or whether a mechanism remains effective under realistic interruptions or patient heterogeneity. `hybrid-ds-julia` is intended to support this layer by making it easier to represent treatment logic, biomarker thresholds, and intervention schedules explicitly inside mechanistic models. That can help identify which strategies are robust, which are fragile, and which biological hypotheses are most consistent with clinically relevant patterns of response.

### SAR progression and mechanism differentiation

SAR studies are central to hit-to-lead and lead-optimization work, but the link between SAR and downstream dynamical treatment behavior is often indirect. Compounds are often compared on potency, selectivity, or exposure metrics, but not always on how those differences propagate through a mechanistic disease model under realistic regimens. A hybrid dynamical-systems workflow could help close that gap by mapping compound-level differences into model parameters and then studying how those differences alter qualitative treatment regimes. In that setting, mechanism differentiation becomes more than comparing endpoint potency: it becomes possible to ask which mechanism or chemotype gives a wider and more robust therapeutic regime under realistic intervention logic.

### Autoimmune and inflammatory disease

Autoimmune and inflammatory diseases are another promising domain because their trajectories often involve flares, remission, tapering, rescue therapy, and long periods of partial control. These state changes are biologically and clinically important, and they are often driven by interventions or thresholds that make the system effectively hybrid even when the underlying biological model is written as a differential equation.

A hybrid dynamical-systems workflow would allow these disease trajectories to be analyzed in terms of regime changes and event timing. In practical terms, that could support better tapering strategies, more informative biomarker interpretation, and more systematic comparison of regimens intended to maintain remission while minimizing drug burden.

### Crop science and precision agriculture

Although the primary intended destination of the package is pharmacology, the original motivating example came from crop science, where mechanistic multiscale models can also exhibit hybrid structure. This example remains valuable because it illustrates the broader claim of the project: that there are scientifically important mechanistic domains in which hybrid structure is present, but the corresponding mathematical tools are not yet routine.

Crop science is therefore not the main target for the package, but it remains an instructive example of why such a package could be useful.

## Original crop-science motivation

The immediate technical motivation came from the multiscale Bambara-groundnut model of Dodd et al., which couples plant-level differential equations to canopy-level competition.

In that model, each plant evolves according to nonlinear growth equations, while changing interaction structure determines local competition and ultimately influences yield. When the active interaction structure is fixed, the model evolves smoothly; when a new interaction becomes active, trajectories remain continuous but growth rates change abruptly. That makes the full coupled system a natural example of a **hybrid dynamical system** rather than a globally smooth differential-equation model.

The analogy to pharmacology is direct: canopy occlusion changes local growth rates in much the same way that dosing rules, toxicity thresholds, or therapy switches change the effective dynamics in QSP models. Different scientific domain, same underlying mathematical issue of event-triggered changes in structure.

## Software plan

Planned implementation details include:

- **Language:** Julia.
- **Differential-equation integration and sensitivity infrastructure:** SciML / [`DifferentialEquations.jl`](https://github.com/SciML/DifferentialEquations.jl) and related tools.
- **Boundary-value and shooting infrastructure:** `BoundaryValueDiffEq.jl` and related shooting workflows.
- **Automatic differentiation:** likely `ForwardDiff.jl` or `ReverseDiff.jl`, subject to testing and performance considerations.
- **Optimization:** `Optimization.jl`, `Optim.jl`, `NLopt.jl`, or custom Newton-style solvers.

Related Julia ecosystem tools and references:

- **[`BifurcationKit.jl`](https://github.com/bifurcationkit/BifurcationKit.jl)** — Julia tooling for bifurcation analysis.
- **[`DynamicalSystems.jl`](https://github.com/JuliaDynamics/DynamicalSystems.jl)** — JuliaDynamics library for nonlinear dynamics and time-series analysis.
- **[`HybridSystems.jl`](https://github.com/blegat/HybridSystems.jl)** — a general Julia interface for hybrid systems and hybrid automata, relevant as ecosystem context even though `hybrid-ds-julia` is intended to emphasize event-aware simulation, sensitivities, and optimization for mechanistic QSP and PK/PD models.

As the package matures, selected connectors or translation layers to external platforms—for example, data/event formats compatible with NONMEM, nlmixr2/RxODE, or Pumas—may be added where they clearly support hybrid workflows without duplicating full NLME functionality.

## Roadmap

The project is organized in stages, moving from a minimal deterministic hybrid core toward QSP-facing workflows, selected stochastic extensions, and more demanding non-smooth benchmarks.

### Stage 1 — Narrow deterministic core

- Implement a minimal Julia package skeleton with tests and documentation.
- Represent hybrid and impulsive systems with:
  - smooth differential-equation flows between events,
  - explicit jump maps at dose times,
  - and event surfaces for state-triggered interventions.
- Implement variational-equation propagation for piecewise-smooth and impulsive models, including sensitivity updates across jumps.
- Integrate automatic differentiation for:
  - vector-field Jacobians,
  - jump-map Jacobians,
  - and gradients of scalar objectives.
- Add multiple-shooting support across event-defined segments.

Primary outcome: a small, reliable deterministic core that already demonstrates the central mathematical identity of the package.

### Stage 2 — Flagship biomedical workflow

- Develop one fully documented flagship biomedical example centered on hybrid tumor–immune treatment dynamics.
- Show the full workflow from model definition to event-aware simulation, sensitivity propagation, and schedule- or parameter-facing analysis.
- Use the example as a tutorial, benchmark, and proof-of-concept for clinically meaningful event-driven modeling questions.
- Add one or more higher-dimensional extensions of the flagship model to introduce explicit PK states, resistance structure, and more realistic multi-regimen treatment logic while preserving the same event-aware workflow.
- Add tests and reproducible scripts so the example also serves as a numerical validation target.

Primary outcome: a compact end-to-end demonstration stack that makes the package credible to both hybrid-systems and pharmacology audiences.

### Stage 3 — QSP-facing workflows

- Build convenience abstractions for repeated dosing, treatment holidays, toxicity holds, rescue interventions, and therapy switching.
- Add objective functions and workflows for schedule comparison, schedule optimization, and event-aware parameter estimation.
- Support virtual-patient style parameter exploration and uncertainty analysis in event-rich mechanistic models.
- Improve ergonomics so the package helps answer pharmacology questions that are decision-facing rather than purely mathematical.
- Explore mechanistic--neural correction terms or physics-informed state reconstruction only after the deterministic event-aware workflow is stable and benchmarked.

Primary outcome: a package that begins to look like useful QSP and PK/PD workflow infrastructure rather than only a mathematical prototype.

### Stage 4 — Mechanistic stochastic and Bayesian extensions

- Identify one mechanistically specified stochastic hybrid model class that is genuinely relevant for pharmacology.
- Provide a clean event-aware simulation interface for that class, including jumps or regime changes at predictable or state-dependent times.
- Replace the deterministic ODE between events with an SDE for the continuous part, so that the interface can generate continuous but nowhere differentiable sample paths while still respecting impulsive doses and threshold-triggered jumps.
- Connect that simulation layer to one concrete inference workflow, such as sequential Bayesian updating or particle-based likelihood evaluation.
- Explore sensitivity-aware inference for both pathwise quantities and moments or summary functionals—for example, expectations of exposure, biomarker trajectories, or event times—using variational SDEs for pathwise parameter derivatives and Monte Carlo estimators, including pathwise-gradient or score-function/Malliavin-weight methods, for derivatives of expectations, but only where the deterministic abstractions and numerical stability are already robust enough to support it.
- Evaluate neural jump SDE methods only as a later, optional extension when data justify learning an uncertain stochastic mechanism rather than specifying it mechanistically.

Primary outcome: a staged stochastic extension that broadens the package without diluting its core design.

### Stage 5 — Filippov and benchmark suite

- Implement low-dimensional Filippov and pseudo-Hopf benchmarks as method-validation problems.
- Use them to test event detection accuracy, switching-surface handling, continuation of hybrid periodic orbits, and sensitivity robustness near non-smooth transitions.
- Compare naive workflows against structure-aware hybrid numerics.
- Use benchmark notes to document what is being validated and why it matters numerically.

Primary outcome: a stronger testing identity grounded in serious hybrid-systems numerics.

### Stage 6 — Refinement and specialization

- Harden numerics, including step-size control, event-detection tolerances, and sensitivity robustness.
- Improve documentation strategy through concise conceptual docs, worked examples, benchmark notes, and short application essays.
- Explore additional autoimmune, inflammatory, or PK/PD examples where hybrid structure is genuinely informative.
- Investigate ReLU-based piecewise-smooth neural ODEs, generalized sensitivities, and hybrid continuation only as specialized research extensions, with explicit treatment of activation-boundary degeneracies.
- Revisit licensing and packaging based on collaboration opportunities and the eventual institutional home of the project.

Primary outcome: a research-grade codebase and documentation set that clearly communicates a distinctive methodological identity.

### Stage 7 — Interoperability and import/export bridges

- Design and implement import/export bridges between `hybrid-ds-julia` and established pharmacometric and QSP platforms such as NONMEM, nlmixr2/RxODE, Monolix, and Pumas.
- Map data-driven event specifications—for example, EVID, AMT, TIME, MTIME, CMT, RATE, II, ADDL, and SS—and IF/THEN dosing logic into explicit hybrid dynamical-system structures such as piecewise-smooth flows, jump maps, and saltation matrices, and provide a way to translate hybrid models back into those platforms’ formats where appropriate.
- Ensure that complex models do not need to be respecified by hand to move between platforms; instead, use these bridges to allow modelers to experiment with event-aware simulation, sensitivities, and optimization on top of their existing NLME and QSP infrastructure.
- Treat interoperability as a maintained feature rather than a one-off conversion script, with tests and examples that demonstrate round-tripping of representative QSP and PK/PD models.

Primary outcome: a practical interoperability layer that makes `hybrid-ds-julia` usable in concert with mainstream pharmacometric and QSP toolchains, lowering adoption barriers by avoiding wholesale model rewrites.

## Licensing and IP posture

This repository is currently marked **“All rights reserved.”** In practical terms, that means the code is not yet licensed for reuse or redistribution; it is shared here to illustrate ongoing work, not as a finished open-source product.

That posture is **provisional rather than permanent**. The goal is to keep IP options open so that future collaborators or an employer can help determine the most appropriate long-term model—whether that is an internal company library, a company-backed open-source project, or a hybrid arrangement that balances community access with strategic needs.

Issues, discussion, and scientific feedback are welcome, but reuse requires explicit permission.

The directional preference is toward an eventual open-source model once a stable institutional home and governance structure are in place, but for now the repository is public for visibility and discussion while the IP remains flexible and the codebase continues to evolve.

## Test beds

### First biomedical target

The first biomedical model planned for this workflow is the hybrid impulsive tumor–immune model with immunotherapy and chemotherapy studied in *[Analysis of a Hybrid Impulsive Tumor-Immune Model with Immunotherapy and Chemotherapy](https://www.sciencedirect.com/science/article/abs/pii/S0960077920310080)*.

This model is intended to serve as the flagship early implementation target for the package, not just as a motivating example. It is a strong first biomedical target because the hybrid structure is not incidental: treatment is represented through pulsed interventions of different frequencies, so the long-term behavior depends directly on event timing, treatment scheduling, and the interaction between continuous tumor–immune dynamics and impulsive updates.

From a pharmacology and QSP perspective, it sits close to the kinds of questions decision-makers care about: how treatment frequency, timing, and combination strategy influence tumor control, loss of control, and the robustness of a regimen under changing conditions.

### Next biomedical extensions

After the Zhao model, the natural next step is a hierarchy of higher-dimensional hybrid models that preserve its core treatment-logic structure while adding the pharmacology and resistance features developed in Pang et al. (*[Mathematical Modelling and Analysis of the Tumor Treatment Regimens with Pulsed Immunotherapy and Chemotherapy](https://onlinelibrary.wiley.com/doi/10.1155/2016/6260474)*).

The Zhao model is a strong first flagship because it is genuinely hybrid in a way that matters for translational modeling: it combines continuous tumor–immune dynamics with fixed-time immunotherapy pulses and state-triggered chemotherapy when tumor burden reaches a threshold. That makes it ideal for establishing the package’s core workflow—event-aware simulation, jump handling, sensitivity propagation across events, and schedule-facing analysis—in a system that is small enough to understand clearly yet rich enough to demonstrate why hybrid structure matters.

The next stage is to extend that model upward in dimension without losing its threshold-driven hybrid logic. A first generalization would add an explicit chemotherapy concentration variable, producing a 3D hybrid model that retains Zhao’s event structure while introducing a PK-like state absent from the original formulation. From there, the model can be expanded to include drug-resistant tumor subpopulations and eventually multiple chemotherapy agents on distinct schedules, yielding 4D and 6D variants that incorporate features present in Pang et al., such as explicit drug concentrations, resistant subpopulations, and multidrug treatment structure. This creates a coherent model ladder for `hybrid-ds-julia`: Zhao as the entry-point flagship, followed by increasingly realistic hybrid QSP-style models that stress-test the same numerical machinery in settings closer to PK/PD, resistance, and treatment optimization.

### Mechanistic stochastic and Bayesian extensions

A natural later extension of `hybrid-ds-julia` is a mechanistically specified stochastic hybrid model. In this approach, the modeler specifies the biological state variables, continuous drift structure, diffusion or process-noise model, scheduled dose maps, state-triggered event rules, and observation model in advance. The unknowns generally include parameters, patient-level effects, latent states, and uncertainty about competing mechanistic hypotheses—not the basic mathematical form of the dynamics.

For example, a stochastic tumor–immune model could retain explicit tumor-growth and immune-cell interactions, pharmacokinetic states, scheduled treatment pulses, and toxicity-triggered holds while using an SDE to represent intrinsic biological variability or unobserved patient-level fluctuations. Bayesian or particle-based inference could then estimate parameters and update uncertainty as new measurements become available. This differs from the neural jump SDE approaches discussed in [AI/ML mathematical extensions](#aiml-mathematical-extensions), in which some or all of the drift, diffusion, jump-size, or event-intensity functions are represented by learned neural components.

In a sequential Bayesian workflow, the posterior from one inference step becomes the prior for the next, while the model dynamics determine how new data update the likelihood. This is a standard perspective in sequential Bayesian updating and related Monte Carlo methods.

For stochastic models, the smooth ODE dynamics between events are replaced by a stochastic differential equation (SDE) that generates continuous but typically nowhere differentiable sample paths between jumps. Impulsive dose times, threshold-triggered jumps, and regime switches remain explicitly represented in the hybrid structure, but the continuous evolution between events is now driven by drift and diffusion terms rather than a deterministic vector field. In that setting, the solver would propagate sample paths between events, apply jump maps at intervention times, and use the resulting transition law or predictive distribution to evaluate likelihood contributions for new observations. A natural goal in such workflows is to compute not only sensitivities of individual sample paths, but also sensitivities of moments or summary functionals—for example, mean exposure, variance of biomarker trajectories, or event-time distributions—with respect to parameters and schedule design. In practice, these stochastic sensitivities would be obtained from variational SDEs for pathwise parameter derivatives and from Monte Carlo estimators, including pathwise-gradient or score-function/Malliavin-weight methods, for sensitivities of expectations and other statistics of interest.

This suggests a Bayesian extension layer in which hybrid simulation is combined with MCMC, sequential tempered MCMC, or particle-filtering ideas. The practical role of `hybrid-ds-julia` in such a workflow would be to provide event-aware deterministic or stochastic simulation, expose the hybrid structure cleanly enough to support likelihood construction, and eventually enable sensitivity-aware inference for parameter learning, schedule learning, or virtual-patient updating in event-rich mechanistic models.

### Filippov pseudo-Hopf normal form

Before applying these ideas to more complex biomedical models, it is useful to validate them on a low-dimensional system whose analytical structure is well understood. A natural choice is the planar Filippov **pseudo-Hopf** normal form in the “two invisible tangencies” case studied by Kuznetsov, Rinaldi, and Gragnani in *[One-parameter Bifurcations in Planar Filippov Systems](https://pure.iiasa.ac.at/id/eprint/6817/)*.

This system is a strong test bed for `hybrid-ds-julia` because it is two-dimensional, canonical in the Filippov literature, and exercises exactly the non-smooth machinery the package aims to provide: event detection at the switching surface, handling of sliding and crossing dynamics, construction of Poincaré maps for hybrid orbits, and continuation of limit cycles through a discontinuity-induced bifurcation.

A natural early milestone is to reproduce the pseudo-Hopf scenario robustly—tracking the birth of the crossing limit cycle, its stability, and its dependence on a bifurcation parameter—before turning to higher-dimensional biomedical models.

## Other disease applications

The first application and tests of `hybrid-ds-julia` will be in immuno-oncology, where event-aware hybrid modeling is especially relevant because treatment schedules, combination regimens, biomarker thresholds, resistance, and therapy switching are central to the biology and the decision-making context.

In **cardiometabolic disease**, especially diabetes and obesity, the **continuous part** is glucose, insulin, and broader metabolic-state evolution over time, while the **discrete part** is meals, insulin boluses, dose changes, hypoglycemia rescue actions, and other threshold-triggered interventions. Hybrid modeling matters here because glycemic control questions hinge on both gradual metabolic dynamics and abrupt, rule-driven actions that reshape those dynamics.

In **neurology and CNS disease**, the **continuous part** is slow disease progression and biomarker evolution—for example, neurodegeneration or lesion burden—while the **discrete part** is clinical decision logic: regimen changes, rescue interventions, stage transitions, and other state-dependent treatment updates. Hybrid modeling matters here because episodic decisions, relapses, and threshold-based escalations punctuate an otherwise gradual trajectory.

In **immunology and inflammation**, the **continuous part** is the inflammatory and immune-state dynamics—cytokines, cell populations, and tissue damage—while the **discrete part** is flare-triggered rescue therapy, tapering decisions, switching between treatment strategies, and agent-based or cellular events that induce regime changes. Hybrid modeling matters here because flare–remission patterns are shaped by both ongoing immune dynamics and intermittent, guideline- or state-driven interventions.

In **infectious disease, especially tuberculosis**, the **continuous part** is within-host infection, immune response, and pathogen-growth dynamics, while the **discrete part** is combination therapy, adherence or missed-dose events, resistance-triggered regimen changes, and latent-to-active transitions that switch the system into new regimes. Hybrid modeling matters here because long-term outcomes depend critically on when therapy is taken, when resistance emerges, and when latent infection reactivates—not just on average exposure.

Overall, the value of `hybrid-ds-julia` is greatest in disease areas where the questions are not just about the continuous evolution of a biomarker, but also about when interventions occur and how those interventions change the governing dynamics.

## Other computational biology applications

Although `hybrid-ds-julia` is initially focused on QSP, PK/PD, and translational pharmacology, the same numerical framework applies more broadly to computational-biology models in which continuous biological dynamics interact with discrete interventions, threshold rules, regulatory switches, or changing interaction structure. These applications are not intended to dilute the pharmacology-first implementation strategy. Rather, they provide scientifically meaningful test beds in which event-aware simulation, sensitivity propagation, multiple shooting, continuation, and optimization can be developed and validated.

### Predator--prey, pest management, and adaptive harvesting

In predator--prey, food-web, and pest-management models, the **continuous part** consists of population growth, predation, resource limitation, competition, migration, seasonal forcing, and population recovery. The **discrete part** can include harvesting pulses, predator stocking, pesticide applications, biological-control releases, threshold-based management actions, seasonal policy changes, extinction or reintroduction rules, and switching in refuge or feeding behavior.

These systems provide a natural family of low-dimensional hybrid test beds because they can exhibit multiple equilibria, oscillations, threshold effects, and bifurcations even before intervention logic is added. Hybrid management rules make intervention timing part of the scientific question: for example, when a pest population should trigger biological control, how harvesting intensity should change after a population threshold is crossed, or whether a small change in intervention timing shifts the system from persistent coexistence to collapse.

This application is also directly relevant to the Filippov pseudo-Hopf and sliding-dynamics benchmark proposed elsewhere in this README. In ecological models with a discontinuous threshold policy—for example, switching harvesting, chemical control, refuge use, or predator behavior when a population ratio crosses a boundary—the vector fields on either side of the switching surface can point toward that surface. In that case, trajectories may remain on the boundary for a finite time and evolve according to a Filippov sliding vector field. Such models can therefore contain sliding regions, pseudo-equilibria, grazing events, and sliding bifurcations, making them particularly useful for validating switching-surface handling, continuation, and sensitivity calculations near non-smooth transitions.

### Crop growth, canopy competition, and precision agriculture

In crop models, the **continuous part** can include plant biomass, developmental stage, leaf area, canopy structure, soil moisture, nutrient availability, pest burden, pathogen burden, and yield-related traits. The **discrete part** can include changes in plant interaction networks as canopies overlap, irrigation and fertigation events, planting and harvest, pruning, pest-management interventions, water- or nutrient-stress thresholds, and biological interventions such as RNA sprays, viral gene modulation, or signalling peptides.

This application connects directly to the original Bambara-groundnut motivation for the package. In a multiscale crop model, plant trajectories may remain continuous while local interaction structure and growth rates change abruptly as new canopy-competition relationships become active. The same framework could eventually support precision-agriculture questions involving adaptive irrigation, fertilization, pest management, and robust management policies under weather, soil, and population variability. The common mathematical issue is the same as in pharmacology: a continuous biological system is shaped by interventions and interaction changes that occur at discrete times or thresholds.

Sliding dynamics are not usually an intrinsic feature of crop-growth or canopy-competition models. Many crop events are scheduled, impulsive, or produce a one-time change in the active vector field, so trajectories cross the corresponding event surface rather than remain on it. Sliding could arise, however, in an idealized discontinuous feedback controller—for example, if irrigation or fertigation switches instantaneously at a soil-moisture or plant-water-stress threshold and the competing vector fields both drive the system toward that threshold. In practice, hysteresis, actuator delay, or smooth control laws may be more realistic than sustained Filippov sliding, but the possibility is relevant when designing threshold-based management policies.

### Gene regulatory networks, cell-cycle control, and synthetic biology

In gene-regulatory, cell-cycle, and synthetic-biology models, the **continuous part** consists of mRNA, protein, metabolite, signalling molecule, and cell-population concentrations, together with degradation, translation, enzymatic reactions, feedback, and transport. The **discrete part** can include transcriptional activation or repression, regulatory modules switching between active and inactive states, cell-cycle checkpoints, threshold-based cell-fate decisions, inducible gene expression, optogenetic stimulation, cell division, and externally applied molecular pulses.

These systems are useful because the switching logic is often closely tied to known biological mechanisms. A hybrid representation can preserve interpretable regulatory rules while allowing continuous concentration dynamics to be analyzed with event-aware sensitivities. Potential future applications include parameter estimation for switching gene circuits, optimization of pulsed induction schedules, continuation of cellular oscillations, and analysis of how threshold perturbations alter cell-fate or cell-cycle outcomes.

Sliding dynamics can occur in piecewise-affine and Filippov formulations of gene-regulatory networks. For example, if regulatory threshold rules define different vector fields on either side of a switching domain and the flows point toward that domain, a solution may remain on the switching surface for a finite interval. Such sliding-mode solutions have been studied in piecewise-linear models of genetic regulatory networks. Whether sliding is biologically appropriate in a particular model requires care: a sharp Boolean or threshold approximation may produce sliding where a more detailed Hill-function, stochastic, or time-delayed model would instead produce a rapid but smooth transition. This makes gene regulation a useful research setting for comparing explicit non-smooth formulations with smooth regularizations.

### Microbial communities, bioreactors, and pulsed interventions

In microbial-community and bioreactor models, the **continuous part** can include microbial biomass, substrate concentrations, metabolites, dissolved oxygen, pH, temperature, and the relative abundance of competing populations. The **discrete part** can include batch feeding, dilution, harvesting, inoculation, antibiotic or phage pulses, oxygen-control policies, environmental shifts, metabolic-regime changes, and threshold-triggered changes in operating conditions.

These models could serve as useful intermediate test beds between low-dimensional ecological systems and higher-dimensional QSP models. They can combine multiple time scales, partial observability, pulsed interventions, population competition, and regime changes while retaining relatively direct experimental interpretation. Event-aware simulation and sensitivity analysis could support design of feed schedules, perturbation experiments, control policies, and robust operating regimes in the presence of biological variability.

Sliding dynamics are not generally expected in ordinary batch or fed-batch models with scheduled inputs. They can arise in idealized discontinuous feedback settings, however, such as instantaneous switching of aeration, dilution, pH control, substrate feed, or antibiotic administration at a specified threshold. If the vector fields on both sides direct the state toward the operating boundary, a Filippov sliding description can be mathematically appropriate. In laboratory and industrial settings, hysteresis, sampling intervals, actuator limits, and controller dynamics will often regularize this behavior, but the non-smooth limit can still be a valuable model for understanding threshold-control design and numerical robustness.

## Example applications

The same mathematical and computational ideas can be used across a range of mechanistic modeling problems in pharmacology and beyond.

### QSP and PK/PD

In QSP and PK/PD, `hybrid-ds-julia` is intended to make event-aware simulation, variational sensitivity propagation, and multiple shooting natural parts of the workflow for models with dosing pulses, treatment holidays, toxicity holds, and threshold-mediated biological responses.

This makes it easier to study how the timing and logic of interventions shape long-term outcomes such as remission, relapse, resistance, or sustained control. It also opens the door to more systematic optimization over dose, timing, and treatment rules rather than relying only on hand-picked regimen comparisons.

### Translational pharmacology

Many of the most important translational questions are inherently dynamical: whether a schedule sustains control, whether biomarker trajectories indicate a regime shift, or whether a mechanism remains effective under realistic interruptions or patient heterogeneity. `hybrid-ds-julia` is intended to support this layer by making it easier to represent treatment logic, biomarker thresholds, and intervention schedules explicitly inside mechanistic models. That can help identify which strategies are robust, which are fragile, and which biological hypotheses are most consistent with clinically relevant patterns of response.

### SAR progression and mechanism differentiation

SAR studies are central to hit-to-lead and lead-optimization work, but the link between SAR and downstream dynamical treatment behavior is often indirect. Compounds are often compared on potency, selectivity, or exposure metrics, but not always on how those differences propagate through a mechanistic disease model under realistic regimens. A hybrid dynamical-systems workflow could help close that gap by mapping compound-level differences into model parameters and then studying how those differences alter qualitative treatment regimes. In that setting, mechanism differentiation becomes more than comparing endpoint potency: it becomes possible to ask which mechanism or chemotype gives a wider and more robust therapeutic regime under realistic intervention logic.

### Autoimmune and inflammatory disease

Autoimmune and inflammatory diseases are another promising domain because their trajectories often involve flares, remission, tapering, rescue therapy, and long periods of partial control. These state changes are biologically and clinically important, and they are often driven by interventions or thresholds that make the system effectively hybrid even when the underlying biological model is written as a differential equation.

A hybrid dynamical-systems workflow would allow these disease trajectories to be analyzed in terms of regime changes and event timing. In practical terms, that could support better tapering strategies, more informative biomarker interpretation, and more systematic comparison of regimens intended to maintain remission while minimizing drug burden.

### Crop science and precision agriculture

Although the primary intended destination of the package is pharmacology, the original motivating example came from crop science, where mechanistic multiscale models can also exhibit hybrid structure. This example remains valuable because it illustrates the broader claim of the project: that there are scientifically important mechanistic domains in which hybrid structure is present, but the corresponding mathematical tools are not yet routine.

Crop science is therefore not the main target for the package, but it remains an instructive example of why such a package could be useful.

## Original crop-science motivation

The immediate technical motivation came from the multiscale Bambara-groundnut model of Dodd et al., which couples plant-level differential equations to canopy-level competition.

In that model, each plant evolves according to nonlinear growth equations, while changing interaction structure determines local competition and ultimately influences yield. When the active interaction structure is fixed, the model evolves smoothly; when a new interaction becomes active, trajectories remain continuous but growth rates change abruptly. That makes the full coupled system a natural example of a **hybrid dynamical system** rather than a globally smooth differential-equation model.

The analogy to pharmacology is direct: canopy occlusion changes local growth rates in much the same way that dosing rules, toxicity thresholds, or therapy switches change the effective dynamics in QSP models. Different scientific domain, same underlying mathematical issue of event-triggered changes in structure.

## Software plan

Planned implementation details include:

- **Language:** Julia.
- **Differential-equation integration and sensitivity infrastructure:** SciML / [`DifferentialEquations.jl`](https://github.com/SciML/DifferentialEquations.jl) and related tools.
- **Boundary-value and shooting infrastructure:** `BoundaryValueDiffEq.jl` and related shooting workflows.
- **Automatic differentiation:** likely `ForwardDiff.jl` or `ReverseDiff.jl`, subject to testing and performance considerations.
- **Optimization:** `Optimization.jl`, `Optim.jl`, `NLopt.jl`, or custom Newton-style solvers.

Related Julia ecosystem tools and references:

- **[`BifurcationKit.jl`](https://github.com/bifurcationkit/BifurcationKit.jl)** — Julia tooling for bifurcation analysis.
- **[`DynamicalSystems.jl`](https://github.com/JuliaDynamics/DynamicalSystems.jl)** — JuliaDynamics library for nonlinear dynamics and time-series analysis.
- **[`HybridSystems.jl`](https://github.com/blegat/HybridSystems.jl)** — a general Julia interface for hybrid systems and hybrid automata, relevant as ecosystem context even though `hybrid-ds-julia` is intended to emphasize event-aware simulation, sensitivities, and optimization for mechanistic QSP and PK/PD models.

As the package matures, selected connectors or translation layers to external platforms—for example, data/event formats compatible with NONMEM, nlmixr2/RxODE, or Pumas—may be added where they clearly support hybrid workflows without duplicating full NLME functionality.

## Roadmap

The project is organized in stages, moving from a minimal deterministic hybrid core toward QSP-facing workflows, selected stochastic extensions, and more demanding non-smooth benchmarks.

### Stage 1 — Narrow deterministic core

- Implement a minimal Julia package skeleton with tests and documentation.
- Represent hybrid and impulsive systems with:
  - smooth differential-equation flows between events,
  - explicit jump maps at dose times,
  - and event surfaces for state-triggered interventions.
- Implement variational-equation propagation for piecewise-smooth and impulsive models, including sensitivity updates across jumps.
- Integrate automatic differentiation for:
  - vector-field Jacobians,
  - jump-map Jacobians,
  - and gradients of scalar objectives.
- Add multiple-shooting support across event-defined segments.

Primary outcome: a small, reliable deterministic core that already demonstrates the central mathematical identity of the package.

### Stage 2 — Flagship biomedical workflow

- Develop one fully documented flagship biomedical example centered on hybrid tumor–immune treatment dynamics.
- Show the full workflow from model definition to event-aware simulation, sensitivity propagation, and schedule- or parameter-facing analysis.
- Use the example as a tutorial, benchmark, and proof-of-concept for clinically meaningful event-driven modeling questions.
- Add one or more higher-dimensional extensions of the flagship model to introduce explicit PK states, resistance structure, and more realistic multi-regimen treatment logic while preserving the same event-aware workflow.
- Add tests and reproducible scripts so the example also serves as a numerical validation target.

Primary outcome: a compact end-to-end demonstration stack that makes the package credible to both hybrid-systems and pharmacology audiences.

### Stage 3 — QSP-facing workflows

- Build convenience abstractions for repeated dosing, treatment holidays, toxicity holds, rescue interventions, and therapy switching.
- Add objective functions and workflows for schedule comparison, schedule optimization, and event-aware parameter estimation.
- Support virtual-patient style parameter exploration and uncertainty analysis in event-rich mechanistic models.
- Improve ergonomics so the package helps answer pharmacology questions that are decision-facing rather than purely mathematical.
- Explore mechanistic--neural correction terms or physics-informed state reconstruction only after the deterministic event-aware workflow is stable and benchmarked.

Primary outcome: a package that begins to look like useful QSP and PK/PD workflow infrastructure rather than only a mathematical prototype.

### Stage 4 — Mechanistic stochastic and Bayesian extensions

- Identify one mechanistically specified stochastic hybrid model class that is genuinely relevant for pharmacology.
- Provide a clean event-aware simulation interface for that class, including jumps or regime changes at predictable or state-dependent times.
- Replace the deterministic ODE between events with an SDE for the continuous part, so that the interface can generate continuous but nowhere differentiable sample paths while still respecting impulsive doses and threshold-triggered jumps.
- Connect that simulation layer to one concrete inference workflow, such as sequential Bayesian updating or particle-based likelihood evaluation.
- Explore sensitivity-aware inference for both pathwise quantities and moments or summary functionals—for example, expectations of exposure, biomarker trajectories, or event times—using variational SDEs for pathwise parameter derivatives and Monte Carlo estimators, including pathwise-gradient or score-function/Malliavin-weight methods, for derivatives of expectations, but only where the deterministic abstractions and numerical stability are already robust enough to support it.
- Evaluate neural jump SDE methods only as a later, optional extension when data justify learning an uncertain stochastic mechanism rather than specifying it mechanistically.

Primary outcome: a staged stochastic extension that broadens the package without diluting its core design.

### Stage 5 — Filippov and benchmark suite

- Implement low-dimensional Filippov and pseudo-Hopf benchmarks as method-validation problems.
- Use them to test event detection accuracy, switching-surface handling, continuation of hybrid periodic orbits, and sensitivity robustness near non-smooth transitions.
- Compare naive workflows against structure-aware hybrid numerics.
- Use benchmark notes to document what is being validated and why it matters numerically.

Primary outcome: a stronger testing identity grounded in serious hybrid-systems numerics.

### Stage 6 — Refinement and specialization

- Harden numerics, including step-size control, event-detection tolerances, and sensitivity robustness.
- Improve documentation strategy through concise conceptual docs, worked examples, benchmark notes, and short application essays.
- Explore additional autoimmune, inflammatory, or PK/PD examples where hybrid structure is genuinely informative.
- Investigate ReLU-based piecewise-smooth neural ODEs, generalized sensitivities, and hybrid continuation only as specialized research extensions, with explicit treatment of activation-boundary degeneracies.
- Revisit licensing and packaging based on collaboration opportunities and the eventual institutional home of the project.

Primary outcome: a research-grade codebase and documentation set that clearly communicates a distinctive methodological identity.

### Stage 7 — Interoperability and import/export bridges

- Design and implement import/export bridges between `hybrid-ds-julia` and established pharmacometric and QSP platforms such as NONMEM, nlmixr2/RxODE, Monolix, and Pumas.
- Map data-driven event specifications—for example, EVID, AMT, TIME, MTIME, CMT, RATE, II, ADDL, and SS—and IF/THEN dosing logic into explicit hybrid dynamical-system structures such as piecewise-smooth flows, jump maps, and saltation matrices, and provide a way to translate hybrid models back into those platforms’ formats where appropriate.
- Ensure that complex models do not need to be respecified by hand to move between platforms; instead, use these bridges to allow modelers to experiment with event-aware simulation, sensitivities, and optimization on top of their existing NLME and QSP infrastructure.
- Treat interoperability as a maintained feature rather than a one-off conversion script, with tests and examples that demonstrate round-tripping of representative QSP and PK/PD models.

Primary outcome: a practical interoperability layer that makes `hybrid-ds-julia` usable in concert with mainstream pharmacometric and QSP toolchains, lowering adoption barriers by avoiding wholesale model rewrites.

## Licensing and IP posture

This repository is currently marked **“All rights reserved.”** In practical terms, that means the code is not yet licensed for reuse or redistribution; it is shared here to illustrate ongoing work, not as a finished open-source product.

That posture is **provisional rather than permanent**. The goal is to keep IP options open so that future collaborators or an employer can help determine the most appropriate long-term model—whether that is an internal company library, a company-backed open-source project, or a hybrid arrangement that balances community access with strategic needs.

Issues, discussion, and scientific feedback are welcome, but reuse requires explicit permission.

The directional preference is toward an eventual open-source model once a stable institutional home and governance structure are in place, but for now the repository is public for visibility and discussion while the IP remains flexible and the codebase continues to evolve.