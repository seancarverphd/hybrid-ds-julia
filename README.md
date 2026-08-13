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

## Mathematical approach

The mathematical core of `hybrid-ds-julia` is built around piecewise-smooth dynamical systems with events, jumps, and regime changes. The package is intended for models in which the continuous state evolution matters, but where clinically or biologically meaningful behavior also depends on discrete intervention logic.

The main ingredients are:

- piecewise-smooth flows,
- event surfaces and threshold crossings,
- impulsive state updates,
- variational equations,
- saltation matrices,
- multiple shooting,
- and automatic differentiation that respects hybrid structure.

The central practical idea is that event handling should not be treated as a numerical afterthought. If an event changes the state, the governing equations, or the future treatment logic, then the sensitivity of the trajectory must account for that transition explicitly.

### Piecewise-smooth formulation

Consider a state vector

\[
x(t) \in \mathbb{R}^n
\]

with parameters

\[
\theta \in \mathbb{R}^p.
\]

Between events, the state evolves according to an ordinary differential equation:

\[
\dot{x} = f_i(x, t, \theta),
\]

where \(i\) denotes the currently active regime or mode.

For example, a QSP or PK/PD model may have different right-hand sides before treatment, during dosing, during a treatment holiday, after a toxicity hold, or after switching to a rescue therapy. The continuous state can include drug concentrations, tumor burden, immune-cell populations, cytokines, biomarkers, organ-toxicity variables, or latent disease-state variables.

A regime change can occur at a scheduled time, such as a planned dose, or when an event function reaches zero:

\[
h(x, t, \theta) = 0.
\]

Examples include:

- a toxicity biomarker crossing a hold threshold,
- tumor burden crossing a progression threshold,
- a biomarker triggering dose escalation or de-escalation,
- a planned dosing time,
- a treatment-cycle boundary,
- or a state-dependent switch between treatment rules.

The governing equation after the event may differ from the equation before the event:

\[
\dot{x} = f^-(x, t, \theta)
\quad \longrightarrow \quad
\dot{x} = f^+(x, t, \theta).
\]

This piecewise-smooth formulation is broad enough to cover scheduled dosing, threshold-triggered treatment logic, state-dependent regimen changes, and many other hybrid structures relevant to translational pharmacology.

### Jump phenomena and impulsive updates

Some events change only the active vector field, while others directly change the state. A bolus dose, for example, may instantaneously increase a drug concentration; a treatment reset may change a latent state; and a therapy switch may update one or more treatment-control variables.

Such events can be represented by a jump map:

\[
x^+ = R(x^-, t, \theta),
\]

where \(x^-\) is the state immediately before the event and \(x^+\) is the state immediately after it.

A simple bolus-dose example might be written as:

\[
C^+ = C^- + D,
\]

where \(C\) is a concentration state and \(D\) is the administered dose. More complicated reset maps can depend on the current state, time, treatment history, parameters, or decision rules.

In a QSP setting, impulsive updates may represent:

- bolus or infusion-start dosing events,
- dose reductions or treatment restarts,
- therapy switches,
- biomarker-triggered intervention changes,
- state resets associated with surgery or cell therapy,
- or protocol-defined changes in treatment-control states.

Accurate event simulation requires locating the event time and applying the appropriate reset map. But for optimization, inference, continuation, and sensitivity analysis, it is also necessary to propagate how perturbations in parameters or initial conditions affect the timing and effect of that event.

### Variational equations

For a smooth system,

\[
\dot{x} = f(x,t,\theta),
\]

the sensitivity of the state with respect to parameters can be represented by

\[
S(t) = \frac{\partial x(t)}{\partial \theta}.
\]

Between events, the parameter sensitivity satisfies the variational equation

\[
\dot{S}
=
\frac{\partial f}{\partial x} S
+
\frac{\partial f}{\partial \theta}.
\]

Similarly, the state-transition matrix with respect to initial conditions satisfies

\[
\dot{\Phi}
=
\frac{\partial f}{\partial x}\Phi.
\]

These equations provide derivatives that are much more informative and numerically stable than repeatedly perturbing parameters with finite differences, particularly in high-dimensional systems or in problems where the trajectory must satisfy a boundary condition, periodicity condition, or optimization constraint.

However, a hybrid trajectory is not globally smooth. When a trajectory crosses an event surface or undergoes a reset, the sensitivities must be updated to account for the fact that both the event time and the post-event state depend on the perturbation.

That is where saltation matrices and jump-sensitivity maps enter.

### Saltation matrices

Suppose a trajectory crosses an event surface

\[
h(x,t,\theta)=0
\]

and transitions from vector field \(f^-\) to vector field \(f^+\). In the simplest state-triggered case without an explicit state reset, the perturbation in the state is mapped across the event by a saltation matrix.

For an autonomous event surface \(h(x)=0\), the standard saltation matrix is

\[
\Xi
=
I
+
\frac{(f^+ - f^-)\nabla h^\top}
{\nabla h^\top f^-}.
\]

Here:

- \(I\) is the identity matrix,
- \(\nabla h\) is the normal vector to the event surface,
- \(f^-\) is the vector field immediately before the event,
- and \(f^+\) is the vector field immediately after the event.

The denominator

\[
\nabla h^\top f^-
\]

measures the transverse speed with which the trajectory crosses the event surface. When this quantity is near zero, the event is close to grazing or tangential contact, and sensitivities can become large or ill-conditioned. Such situations are scientifically important because they often correspond to boundaries between qualitatively different treatment outcomes or decision regimes.

For reset events of the form

\[
x^+ = R(x^-,t,\theta),
\]

the corresponding sensitivity update includes derivatives of the reset map as well as corrections for event-time dependence. The exact form depends on whether the event is scheduled, state-triggered, parameter-triggered, or time-dependent, but the key principle is unchanged:

> Sensitivities must be propagated through the event map, not estimated by ignoring the event or perturbing across it blindly.

This is especially important for dosing schedules, toxicity holds, threshold-triggered treatment changes, and other settings where small parameter changes can alter both the state at the event and the time at which the event occurs.

### Multiple shooting

Single shooting integrates one long trajectory from a starting point and adjusts initial conditions or parameters until a terminal condition is met. For long time horizons, stiff systems, unstable dynamics, repeated events, or periodic-orbit problems, this can become poorly conditioned.

Multiple shooting addresses that problem by dividing the time horizon into shorter segments. Rather than solving for one initial condition, the method introduces intermediate states:

\[
x_0, x_1, \ldots, x_m,
\]

with each segment integrated over a shorter interval. The solution is then obtained by enforcing continuity constraints between segments:

\[
x_{k+1}
-
\Phi_k(x_k,\theta)
=
0,
\]

where \(\Phi_k\) denotes the flow map over the \(k\)-th interval, including any events that occur within that interval.

For a hybrid system, the segment maps may include:

- continuous integration under one or more vector fields,
- scheduled impulses,
- state-triggered events,
- jump maps,
- and saltation-based sensitivity updates.

This segmentation improves numerical conditioning because unstable directions do not have to be carried through one long integration interval before correction. It also makes it easier to isolate difficult events, place shooting nodes near regime transitions, and formulate boundary-value problems involving periodicity, treatment-cycle consistency, or prescribed endpoint conditions.

Representative uses include:

- finding periodic treatment-cycle solutions,
- computing trajectories that connect clinically meaningful states,
- continuing solutions as dose or schedule parameters vary,
- stabilizing long-horizon optimization,
- and constructing manifolds or separatrices that organize treatment-response regimes.

### Automatic differentiation

Automatic differentiation can provide accurate derivatives of model components without manually deriving every Jacobian entry. In a hybrid model, however, standard differentiation through a solver is not enough if event timing, mode changes, or reset maps are handled implicitly.

The relevant derivatives include:

\[
\frac{\partial f}{\partial x},
\qquad
\frac{\partial f}{\partial \theta},
\qquad
\frac{\partial R}{\partial x},
\qquad
\frac{\partial R}{\partial \theta},
\qquad
\frac{\partial h}{\partial x},
\qquad
\frac{\partial h}{\partial \theta}.
\]

These quantities can be obtained using automatic differentiation for the smooth pieces of the model, then combined with explicit hybrid sensitivity formulas at events.

The intended workflow is therefore:

1. Use automatic differentiation to obtain derivatives of the continuous vector fields, event functions, and reset maps.
2. Integrate the continuous variational equations between events.
3. Detect scheduled or state-triggered events accurately.
4. Apply reset maps and saltation-based sensitivity updates at those events.
5. Assemble the resulting derivatives into shooting, continuation, fitting, or optimization calculations.

This hybrid-aware approach is more structured than finite-difference workflows because it separates the continuous and discrete sources of sensitivity. It also makes diagnostic failures more interpretable: poor conditioning can be traced to unstable continuous dynamics, near-grazing event crossings, discontinuous treatment logic, or insufficiently informative data rather than being hidden inside a noisy finite-difference estimate.

The package will aim to expose this structure directly to users. Rather than asking modelers to derive saltation maps by hand for every use case, `hybrid-ds-julia` should provide reusable event-aware abstractions that can be combined with Julia’s existing differential-equation, sensitivity-analysis, and optimization tools.

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

## Other disease applications

Although the initial focus is QSP and PK/PD, the same event-aware numerical framework can apply to a broad range of mechanistic disease models.

Examples include:

- **Autoimmune disease** — flare-remission dynamics, tapering schedules, rescue therapy, and biomarker-triggered escalation or de-escalation.
- **Inflammatory disease** — treatment holidays, adaptive biologic dosing, threshold-based switching, and toxicity management.
- **Infectious disease** — pulsed antimicrobial therapy, adherence interruptions, resistance thresholds, treatment switching, and pathogen-load triggers.
- **Metabolic disease** — intermittent interventions, glucose-triggered dosing rules, meal events, and state-dependent control policies.
- **Neurological disease** — stimulation protocols, medication cycling, threshold-triggered intervention, and episodic symptom dynamics.
- **Cell and gene therapy** — conditioning regimens, infusion events, expansion phases, delayed toxicity, and intervention rules based on cytokine or biomarker dynamics.
- **Cardiovascular disease** — intermittent treatment, device-triggered interventions, threshold-based alarms, and adaptive control of physiological states.

The common feature is not any particular disease area. It is the coexistence of continuous biological dynamics and discrete intervention logic.

In all of these settings, the central questions are similar:

- How does timing affect long-term outcome?
- Which thresholds or intervention rules are responsible for a qualitative change in behavior?
- How robust is a schedule across plausible parameter variation?
- Can model sensitivities identify leverage points for safer or more effective treatment strategies?
- Do different treatment policies create distinct dynamical regimes that should be analyzed separately?

## Other computational biology applications

The same hybrid dynamical-systems methods can also support computational-biology applications outside human disease modeling. In each case, the continuous state dynamics may be governed by differential equations, while interventions, environmental changes, threshold rules, or experimental protocols introduce discrete events and regime transitions.

### Predator--prey, pest management, and adaptive harvesting

Ecological models often include continuous population dynamics together with discrete harvesting, stocking, pesticide application, predator release, seasonal transitions, or threshold-based management decisions.

A simple predator--prey system might be represented as

\[
\dot{N}
=
rN
\left(
1-\frac{N}{K}
\right)
-
\frac{aNP}{1+bN},
\]

\[
\dot{P}
=
c\frac{aNP}{1+bN}
-
dP,
\]

where \(N\) is prey or pest abundance and \(P\) is predator abundance.

A management intervention can be represented by a pulse or reset map. For example, pesticide application at time \(t_k\) might produce

\[
N(t_k^+)
=
(1-\rho_k)N(t_k^-),
\]

while periodic predator release could produce

\[
P(t_k^+)
=
P(t_k^-)
+
R_k.
\]

State-triggered intervention rules are also common. A pest-management policy may apply control only when pest abundance exceeds a threshold:

\[
N(t)
\geq
N_{\mathrm{threshold}}.
\]

This naturally creates a hybrid system in which management actions depend on the evolving ecological state.

Potential uses of `hybrid-ds-julia` include:

- comparing the timing and intensity of pesticide or biological-control pulses,
- optimizing harvesting or stocking schedules,
- identifying threshold policies that avoid pest outbreaks,
- studying resilience and recovery after interventions,
- and analyzing how uncertainty in growth or predation rates affects management outcomes.

### Crop growth, canopy competition, and precision agriculture

Crop and plant-growth models combine continuous developmental and physiological processes with discrete management events such as planting, irrigation, fertilization, pesticide application, pruning, harvest, and abrupt weather changes.

A stylized crop-growth model may include biomass \(W\), soil-water availability \(M\), nutrient availability \(N\), and canopy state \(L\):

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
\ell_N(N),
\]

where \(I(t)\) and \(F(t)\) represent irrigation and fertilizer inputs.

Discrete management events may be represented by impulsive updates such as

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

A state-dependent precision-agriculture policy might trigger irrigation when soil moisture falls below a threshold:

\[
M(t)
\leq
M_{\mathrm{irrigation}}.
\]

Similarly, fertilization, pest intervention, or canopy management may be activated only when one or more sensor-derived variables enter a specified range.

Hybrid methods are relevant because the timing of those interventions can strongly affect cumulative growth, resource use, and final yield. A small change in irrigation timing, for example, may matter much more during a sensitive growth stage than at another point in the season.

Potential uses include:

- optimizing irrigation and fertilization schedules,
- comparing threshold-based versus fixed-calendar interventions,
- quantifying sensitivity of yield to timing and dose of inputs,
- analyzing crop-response regimes under different environmental conditions,
- and incorporating weather, sensor, or management events into a coherent dynamical model.

### Gene regulatory networks, cell-cycle control, and synthetic biology

Gene regulatory networks often exhibit thresholding, switching, pulses, feedback, and state-dependent transitions. These features arise naturally from transcriptional regulation, bistability, cell-cycle checkpoints, inducible expression systems, optogenetic stimulation, and experimental interventions.

A simple regulatory interaction can be represented using a Hill-function response:

\[
\dot{x}
=
\frac{\alpha}{1+\left(\frac{y}{K}\right)^n}
-
\delta_x x,
\]

\[
\dot{y}
=
\frac{\beta x^m}{L^m+x^m}
-
\delta_y y.
\]

Depending on parameters, such systems can display switch-like behavior, oscillations, or multiple stable states.

Hybrid structure enters when a regulatory program changes at a threshold or when an experiment applies a pulse. For example, an inducible expression experiment might update an input state at selected times:

\[
u(t_k^+)
=
u(t_k^-)
+
A_k.
\]

A cell-cycle checkpoint may activate when a damage variable exceeds a threshold, changing the active regulatory dynamics:

\[
D(t)
\geq
D_{\mathrm{checkpoint}}.
\]

Synthetic-biology control systems can also contain explicit mode changes, such as light-on/light-off stimulation protocols, nutrient shifts, temperature changes, or feedback controllers that switch based on fluorescent reporter levels.

Potential uses include:

- optimizing pulse timing for gene-expression control,
- studying sensitivity of switching behavior to parameter uncertainty,
- identifying interventions that move a system between stable phenotypic states,
- designing feedback rules for synthetic circuits,
- and estimating event-aware sensitivities in models with checkpoint or threshold logic.

### Microbial communities, bioreactors, and pulsed interventions

Microbial communities and bioreactor systems often involve continuous growth, substrate consumption, metabolite production, competition, and feedback together with pulsed feeding, dilution, inoculation, antibiotic exposure, environmental shifts, and threshold-based control.

A simple chemostat-style model may include microbial biomass \(X\), substrate \(S\), and product \(P\):

\[
\dot{X}
=
\mu(S)X
-
D X,
\]

\[
\dot{S}
=
D(S_{\mathrm{in}}-S)
-
\frac{1}{Y}\mu(S)X,
\]

\[
\dot{P}
=
q_P(S)X
-
D P,
\]

where \(D\) is a dilution rate, \(Y\) is a yield coefficient, and \(\mu(S)\) describes substrate-limited growth.

A pulsed feeding event can be represented by

\[
S(t_k^+)
=
S(t_k^-)
+
F_k.
\]

A contamination, inhibition, or oxygen-limitation event may trigger a change in the governing dynamics when a metabolite or process variable crosses a threshold.

In microbial ecology, similar structures arise through antibiotic pulses, nutrient switching, periodic disturbance, inoculation, or host-mediated environmental changes. These events can alter community composition, drive transitions between ecological states, or create history-dependent responses that are not captured well by purely smooth models.

Potential uses include:

- optimizing feed schedules and dilution policies in bioreactors,
- analyzing resilience of microbial communities after pulsed perturbations,
- studying antibiotic scheduling and resistance dynamics,
- comparing threshold-based versus periodic control rules,
- and using event-aware sensitivities to identify parameters that control transitions between productive and unproductive regimes.

### Epidemiology, public-health policy, and adaptive intervention

Epidemiological systems have continuous transmission, progression, recovery, and immunity dynamics, but policy and care pathways routinely introduce hybrid structure. Vaccination campaigns, school or workplace closures, antiviral treatment starts, isolation protocols, testing thresholds, hospital-capacity triggers, and changes in public-health guidance can all change the effective dynamics at specific times or when surveillance indicators cross a threshold.

A basic susceptible–infectious–recovered model can be written as

\[
\dot{S}
=
-\beta(t)\frac{SI}{N},
\]

\[
\dot{I}
=
\beta(t)\frac{SI}{N}
-
\gamma I,
\]

\[
\dot{R}
=
\gamma I.
\]

Hybrid policy structure enters when the transmission rate, testing intensity, treatment availability, or intervention state changes. For example, a threshold-triggered intervention may reduce effective transmission when infections exceed a policy threshold:

\[
I(t)
\geq
I_{\mathrm{trigger}}
\quad \Longrightarrow \quad
\beta(t)
=
\beta_{\mathrm{restricted}}.
\]

When cases fall below a reopening threshold,

\[
I(t)
\leq
I_{\mathrm{release}}
\quad \Longrightarrow \quad
\beta(t)
=
\beta_{\mathrm{baseline}}.
\]

Vaccination or prophylaxis campaigns can be represented by jump maps such as

\[
S(t_k^+)
=
S(t_k^-)
-
V_k,
\]

\[
R(t_k^+)
=
R(t_k^-)
+
V_k,
\]

where \(V_k\) is the number or proportion effectively vaccinated at the event time.

More detailed models can include exposed, hospitalized, intensive-care, treated, isolated, or age-stratified compartments. They can also represent delayed test results, treatment eligibility rules, limited hospital capacity, supply constraints, and region-specific intervention policies.

Potential uses of `hybrid-ds-julia` include:

- comparing fixed-calendar and threshold-triggered nonpharmaceutical interventions,
- optimizing the timing of vaccination, testing, treatment, or prophylaxis campaigns,
- studying hysteresis in policy rules, such as distinct intervention and reopening thresholds,
- quantifying sensitivity of epidemic outcomes to trigger thresholds, reporting delays, and intervention timing,
- evaluating robustness of adaptive policies across uncertainty in transmission, behavior, and adherence,
- and representing inequities in access to testing, treatment, vaccination, or timely intervention as explicit differences in event timing and policy structure.

This application area is especially well suited to hybrid sensitivity analysis because policy conclusions can depend sharply on when a threshold is crossed. Small changes in transmission, surveillance delay, intervention timing, or available capacity may change whether a region experiences a short outbreak, repeated intervention cycles, or sustained healthcare-system stress. Event-aware derivatives and multiple shooting can help distinguish genuine policy-regime boundaries from numerical artifacts.

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

## `docs/readme-parts/09-further-reading.md`

```md
## Further reading

This list is intended as a starting point rather than a comprehensive bibliography. It includes foundational hybrid-systems references, QSP and PK/PD context, sensitivity and automatic-differentiation methods, AI-enabled mechanistic modeling, and application areas relevant to the package.

### Related hybrid-systems papers in other domains

- Carver, S., Guckenheimer, J., & Cowan, N. J. (2009). *Lateral stability of the spring-loaded inverted pendulum model of running and the influence of step-to-step transition dynamics*. Chaos. A preprint is available through [the LIMBS website](https://limbs.lcsr.jhu.edu/wp-content/papercite-data/pdf/carverlateral2009.pdf). This paper is relevant because it uses hybrid-system computations in which accurate event handling, boundary-value methods, and structured sensitivity propagation are essential.
- di Bernardo, M., Budd, C. J., Champneys, A. R., & Kowalczyk, P. (2008). *Piecewise-smooth Dynamical Systems: Theory and Applications*. Springer. A broad introduction to discontinuity-induced bifurcations, switching systems, and piecewise-smooth dynamics.
- Goebel, R., Sanfelice, R. G., & Teel, A. R. (2012). *Hybrid Dynamical Systems: Modeling, Stability, and Robustness*. Princeton University Press. A foundational treatment of hybrid-system modeling and analysis.
- van der Schaft, A. J., & Schumacher, H. (2000). *An Introduction to Hybrid Dynamical Systems*. Springer. A useful reference for systems that combine continuous dynamics and discrete transitions.

### Core dynamical systems / hybrid methods

- Guckenheimer, J., & Holmes, P. (1983). *Nonlinear Oscillations, Dynamical Systems, and Bifurcations of Vector Fields*. Springer. Foundational material on dynamical systems, periodic orbits, bifurcations, and stability.
- Kuznetsov, Y. A. (2004). *Elements of Applied Bifurcation Theory* (3rd ed.). Springer. A standard reference for local bifurcations and continuation-oriented analysis.
- Leine, R. I., & Nijmeijer, H. (2013). *Dynamics and Bifurcations of Non-Smooth Mechanical Systems*. Springer. Relevant to piecewise-smooth systems, impacts, switching, and discontinuity-induced bifurcations.
- Nordmark, A. B. (1991). Non-periodic motion caused by grazing incidence in an impact oscillator. *Journal of Sound and Vibration*, 145(2), 279–297. A classic treatment of grazing events and their dynamical consequences.
- Filippov, A. F. (1988). *Differential Equations with Discontinuous Righthand Sides*. Springer. A foundational source for differential equations with discontinuous vector fields and sliding dynamics.

### QSP / PK–PD concepts and practice

- van der Graaf, P. H., & Benson, N. (2011). Systems pharmacology: Bridging systems biology and pharmacokinetics-pharmacodynamics (PKPD) in drug discovery and development. *Pharmaceutical Research*, 28, 1460–1464. A concise early statement of the systems-pharmacology perspective.
- Peterson, M. C., & Riggs, M. M. (2015). A physiologically based pharmacokinetic model of a monoclonal antibody against interleukin 6 in mice: A platform for translational model-based drug development. *Drug Metabolism and Disposition*, 43(8), 1143–1154. An example of mechanistic modeling in translational pharmacology.
- Agoram, B. M., Martin, S. W., & van der Graaf, P. H. (2007). The role of mechanism-based pharmacokinetic-pharmacodynamic models in translational research. *CPT: Pharmacometrics & Systems Pharmacology* and related systems-pharmacology literature. Useful background on mechanism-based translational modeling.
- Sorger, P. K., Allerheiligen, S. R. B., Abernethy, D. R., Altman, R. B., Brouwer, K. L. R., Califano, A., D’Argenio, D. Z., Iyengar, R., Jusko, W. J., Lalonde, R., et al. (2011). *Quantitative and Systems Pharmacology in the Post-genomic Era: New Approaches to Discovering Drugs and Understanding Therapeutic Mechanisms*. NIH White Paper. A major framing document for QSP.
- van der Graaf, P. H., Benson, N., & related authors. QSP and model-informed drug development literature. QSP provides a framework for mechanistic models that combine drug exposure, biological pathways, disease state, and quantitative data to support in silico experiments and translational decisions. [QSP overview](https://www.mathworks.com/discovery/quantitative-systems-pharmacology.html)

### Sensitivity, adjoint, and automatic differentiation

- Rackauckas, C., Ma, Y., Dixit, V., Guo, X., Innes, M., Revels, J., Nyberg, J., & Ivaturi, V. (2020). Universal differential equations for scientific machine learning. *arXiv:2001.04385*. Relevant to combining mechanistic differential equations, machine learning, and differentiable simulation.
- Rackauckas, C., & Nie, Q. (2017). DifferentialEquations.jl – A performant and feature-rich ecosystem for solving differential equations in Julia. *Journal of Open Research Software*, 5(1), 15. Background on the Julia differential-equation ecosystem on which `hybrid-ds-julia` is intended to build.
- Rackauckas, C., et al. (2019). DiffEqFlux.jl — A Julia library for neural differential equations. *arXiv:1902.02376*. Relevant to differentiable simulation and scientific machine learning in Julia.
- Cao, Y., Li, S., Petzold, L., & Serban, R. (2003). Adjoint sensitivity analysis for differential-algebraic equations: The adjoint DAE system and its numerical solution. *SIAM Journal on Scientific Computing*, 24(3), 1076–1089. Relevant background for gradient-based estimation and optimization.
- Walther, A., & Griewank, A. (2012). *Getting Started with ADOL-C*. In *Combinatorial Scientific Computing*. Chapman and Hall/CRC. A useful introduction to automatic differentiation concepts and implementation.

### Mechanistic stochastic and Bayesian methods

- Wilkinson, D. J. (2011). *Stochastic Modelling for Systems Biology* (2nd ed.). Chapman and Hall/CRC. A broad introduction to stochastic models for biological systems.
- Gillespie, D. T. (1977). Exact stochastic simulation of coupled chemical reactions. *The Journal of Physical Chemistry*, 81(25), 2340–2361. The classic stochastic simulation algorithm for reaction systems.
- Allen, L. J. S. (2017). *A Primer on Stochastic Epidemics*. Springer. A useful introduction to stochastic epidemic modeling and uncertainty in compartmental systems.
- Gelman, A., Carlin, J. B., Stern, H. S., Dunson, D. B., Vehtari, A., & Rubin, D. B. (2013). *Bayesian Data Analysis* (3rd ed.). CRC Press. General Bayesian methodology relevant to parameter inference and uncertainty quantification.
- Carpenter, B., Gelman, A., Hoffman, M. D., Lee, D., Goodrich, B., Betancourt, M., Brubaker, M., Guo, J., Li, P., & Riddell, A. (2017). Stan: A probabilistic programming language. *Journal of Statistical Software*, 76(1), 1–32. Relevant to Bayesian inference workflows and gradient-based posterior computation.

### Mechanistic--neural hybrid systems

- Mann, J., et al. (2024). Mechanism-based organization of neural networks to emulate biological and pharmacological processes. This work is relevant because it reorganizes neural-network layers to reflect biological and pharmacological process structure rather than treating the model as an unconstrained black box. [Article](https://pmc.ncbi.nlm.nih.gov/articles/PMC11130269/)
- Moutik, M., et al. Review of hybrid quantitative systems pharmacology and machine-learning approaches. See also [AI/ML mathematical extensions](#aiml-mathematical-extensions), especially [Mechanistic--neural hybrid systems](#mechanistic--neural-hybrid-systems). This literature is relevant to combining structured mechanistic models with learned components while preserving interpretation of pharmacological and biological state variables.
- Fochesato, A., et al. (2025). Building hybrid pharmacometric–machine-learning models in practice. This tutorial reviews hybrid pharmacometric and machine-learning model considerations, including reporting and validation issues. [Article](https://pmc.ncbi.nlm.nih.gov/articles/PMC12823305/)
- Coupling quantitative systems pharmacology modelling to machine learning. *Frontiers in Systems Biology* (2024). Discusses how QSP and ML can be combined, including biology-informed neural-network approaches. [Article](https://www.frontiersin.org/journals/systems-biology/articles/10.3389/fsysb.2024.1380685/full)
- Pinto, A., Ramos, et al. A general hybrid modeling framework for systems biology. Relevant to combining mechanistic models and deep neural networks while retaining structured biological representations.

Further work enabled by `hybrid-ds-julia` would be to combine these mechanistic–neural architectures with explicit event surfaces, dose maps, toxicity holds, and therapy-switch transitions. This would allow learned model-discrepancy terms to improve prediction while preserving known treatment and biological logic.

### Physics-informed neural networks

- Raissi, M., Perdikaris, P., & Karniadakis, G. E. (2019). Physics-informed neural networks: A deep learning framework for solving forward and inverse problems involving nonlinear partial differential equations. *Journal of Computational Physics*, 378, 686–707. The foundational PINN reference.
- Karniadakis, G. E., Kevrekidis, I. G., Lu, L., Perdikaris, P., Wang, S., & Yang, L. (2021). Physics-informed machine learning. *Nature Reviews Physics*, 3, 422–440. A broad review of physics-informed machine learning.
- Erdem, D., et al. (2024). Learning chemotherapy drug action via universal physics-informed neural networks. This work applies a physics-informed approach to QSP models to identify hidden drug-action terms from synthetic and in-vitro data. [Preprint](https://arxiv.org/html/2404.08019v1)
- A current landscape of integrating QSP and machine learning. *CPT: Pharmacometrics & Systems Pharmacology* (2022). Discusses PINNs and biologically informed neural networks as methods for combining mechanistic ODE structure with data-driven learning in QSP. [Article](https://pmc.ncbi.nlm.nih.gov/articles/PMC8837505/)
- Rackauckas, C., et al. (2020). Universal differential equations for scientific machine learning. *arXiv:2001.04385*. Relevant to using neural components inside structured differential-equation models.

For `hybrid-ds-julia`, the important extension would be hybrid PINNs that enforce not only continuous ODE residuals but also scheduled-dose jump maps, state-triggered guard conditions, reset maps, and continuity or discontinuity constraints at event times. Such tools could support latent-state reconstruction and parameter estimation from sparse, irregular, event-rich longitudinal data.

### Neural hybrid automata

- Goebel, R., Sanfelice, R. G., & Teel, A. R. (2012). *Hybrid Dynamical Systems: Modeling, Stability, and Robustness*. Princeton University Press. A foundation for explicit representations of modes, guards, and reset maps.
- van der Schaft, A. J., & Schumacher, H. (2000). *An Introduction to Hybrid Dynamical Systems*. Springer. A foundational treatment of hybrid automata and continuous-discrete system structure.
- Pinto, A., Ramos, et al. A general hybrid modeling framework for systems biology. Relevant to machine-learning components combined with structured biological dynamics and interoperable systems-biology representations.
- Moutik, M., et al. Review of QSP and machine-learning integration. See also [AI/ML mathematical extensions](#aiml-mathematical-extensions). This literature is relevant to identifying where learned components can complement, rather than replace, explicit mechanistic structure.
- di Bernardo, M., Budd, C. J., Champneys, A. R., & Kowalczyk, P. (2008). *Piecewise-smooth Dynamical Systems: Theory and Applications*. Springer. Relevant to switching boundaries, mode transitions, and regime-dependent dynamics.

A neural-hybrid-automaton direction for `hybrid-ds-julia` would retain known clinical modes—such as active treatment, reduced dose, hold, recovery, and rescue therapy—while using data-driven components only where latent mode structure, mode-dependent dynamics, or transition conditions are genuinely uncertain.

### Neural jump SDEs

- Jia, J., & Benson, A. R. (2019). Neural jump stochastic differential equations. *Advances in Neural Information Processing Systems*. [Paper](https://proceedings.neurips.cc/paper_files/paper/9177-neural-jump-stochastic-differential-equations.pdf)
- Jia, J., & Benson, A. R. (2019). Neural jump stochastic differential equations. [arXiv:1905.10403](https://arxiv.org/abs/1905.10403). The paper introduces a data-driven framework that learns continuous latent dynamics together with discrete stochastic events.
- Baili, et al. Neural jump SDE-related work. See also [AI/ML mathematical extensions](#ai/ml-mathematical-extensions), especially [Neural jump SDEs](#neural-jump-sdes). This reference should be used alongside the final verified bibliographic citation for the Baili paper before release.
- Krystul, J. (2006). Stochastic differential equations on hybrid state spaces. Relevant background for jump diffusion and hybrid stochastic-system formulations.
- Wilkinson, D. J. (2011). *Stochastic Modelling for Systems Biology* (2nd ed.). Chapman and Hall/CRC. Background for stochastic biological dynamics and simulation.

Within `hybrid-ds-julia`, a neural-jump-SDE extension would distinguish known scheduled clinical interventions from uncertain or latent stochastic events. It could support uncertainty-aware virtual-patient simulations, models of treatment interruptions or adherence variation, and estimation of stochastic biological perturbations without obscuring the explicit treatment policy.

### Epidemiology, adaptive intervention, and public-health policy

- Hethcote, H. W. (2000). The mathematics of infectious diseases. *SIAM Review*, 42(4), 599–653. A classic review of compartmental epidemic models and their mathematical analysis.
- Brauer, F., Castillo-Chavez, C., & Feng, Z. (2019). *Mathematical Models in Epidemiology*. Springer. A broad reference for deterministic and stochastic epidemic modeling.
- Funk, S., Salathé, M., & Jansen, V. A. A. (2010). Modelling the influence of human behaviour on the spread of infectious diseases: A review. *Journal of the Royal Society Interface*, 7(50), 1247–1256. Relevant to feedback between epidemic state, behavior, and intervention responses.
- Ferguson, N. M., et al. (2020). Impact of non-pharmaceutical interventions (NPIs) to reduce COVID-19 mortality and healthcare demand. Imperial College COVID-19 Response Team Report 9. An example of intervention timing and policy structure affecting epidemic outcomes.
- Kissler, S. M., Tedijanto, C., Goldstein, E., Grad, Y. H., & Lipsitch, M. (2020). Projecting the transmission dynamics of SARS-CoV-2 through the postpandemic period. *Science*, 368(6493), 860–868. Relevant to intervention cycles, seasonality, and long-term epidemic-policy dynamics.

These references motivate work in which `hybrid-ds-julia` represents threshold-triggered interventions, vaccination pulses, testing and treatment rules, capacity constraints, and hysteretic reopening policies directly inside epidemiological models. Event-aware sensitivities could help identify policy thresholds at which small changes in timing, reporting delay, or intervention strength produce qualitatively different epidemic trajectories.

### Mechanistic crop models and trait optimization

- Thornley, J. H. M., & France, J. (2007). *Mathematical Models in Agriculture: Quantitative Methods for the Plant, Animal and Ecological Sciences* (2nd ed.). CABI. A broad resource for mechanistic agricultural models.
- Yin, X., & Struik, P. C. (2010). Modelling the crop: From system dynamics to systems biology. *Journal of Experimental Botany*, 61(8), 2171–2183. Relevant to linking crop physiological models with systems-level analysis.
- Hammer, G. L., Messina, C., van Oosterom, E., & Chapman, S. (2019). Crop design for adaptation to the drought and high-temperature risks anticipated in future climates. *Crop Science*, 59(5), 2093–2110. Relevant to trait-by-environment interactions and crop-design questions.
- APSIM Initiative. APSIM: Agricultural Production Systems sIMulator. A widely used platform for crop, soil, and management simulation.
- Jones, J. W., et al. (2003). The DSSAT cropping system model. *European Journal of Agronomy*, 18(3–4), 235–265. A foundational reference for crop-system simulation.

These references provide context for using hybrid event-aware methods in crop growth, irrigation, fertilization, canopy competition, and trait-optimization problems where the timing of discrete management actions can be as important as the continuous biological dynamics.
```
