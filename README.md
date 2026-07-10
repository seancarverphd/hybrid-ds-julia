# hybrid-ds-julia

*A Julia package under development for quantitative systems pharmacology (QSP) and PK/PD models that need to handle real treatment logic: dosing pulses, treatment holidays, toxicity holds, threshold-triggered interventions, therapy switches, and other hybrid structure.*

`hybrid-ds-julia` is aimed at **event-aware simulation, sensitivities, and optimization** for mechanistic models whose behavior depends not only on continuous dynamics, but also on when and how clinically meaningful events occur.

The main intended application area is **quantitative systems pharmacology (QSP) and PK/PD**, where mechanistic models are used to study dose and schedule optimization, response heterogeneity, relapse and remission dynamics, mechanism differentiation, and translational decision-making.

Many pharmacology models are still treated numerically as if they were globally smooth, even when the scientific and translational questions of interest depend directly on **event-driven changes** in treatment logic or biological regime. Dosing pulses, treatment holidays, toxicity holds, rescue interventions, threshold-mediated responses, and therapy switches all create the kind of piecewise-smooth or impulsive structure for which hybrid dynamical-systems methods are naturally suited.

The goal of this project is not to rebuild low-level solver infrastructure from scratch. Instead, it is to build a practical layer on top of Julia’s scientific-computing ecosystem that helps modelers work more effectively with trajectories that cross many events and decision boundaries, while remaining close to the kinds of schedule- and intervention-facing questions that matter in translational pharmacology.

The near-term goal is a compact deterministic core with one flagship biomedical example and one end-to-end workflow that makes the package’s value immediately visible to QSP and PK/PD users.

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

## Motivation

This project grew out of the observation that many advanced dynamical-systems methods—especially variational equations, multiple shooting, and automatic differentiation for event-driven models—are well developed mathematically but are not yet standard parts of QSP- and PK/PD-facing software workflows.

Those methods were part of doctoral training in dynamical systems at Cornell, including work with John Guckenheimer on hybrid dynamical-systems models. Guckenheimer coauthored *[Nonlinear Oscillations, Dynamical Systems, and Bifurcations of Vector Fields](https://doi.org/10.1137/1026128)*, a canonical reference for the geometric, variational, and bifurcation tools that underpin many modern treatments of periodic orbits and sensitivities in both smooth and hybrid systems.

Later work in other mechanistic domains reinforced a broader point: methods that feel standard in one mathematical community are often not standard in nearby application domains. That insight led naturally toward immuno-oncology, QSP, and PK/PD, where mechanistic models are increasingly used for model-informed development but where event-aware sensitivities, impulsive updates, and hybrid treatment logic still need stronger workflow support than is commonly available in domain-facing tools.

The core claim of `hybrid-ds-julia` is therefore not that hybrid mathematics is new. It is that many current translational modeling questions already have hybrid structure, and that making those methods usable in practice could improve how those questions are simulated, differentiated, and optimized.

## Why QSP and PK/PD first

QSP and PK/PD are the main intended application areas because they already rely heavily on mechanistic ODE models and because many of their most important questions are inherently schedule- and intervention-dependent.

Representative examples include:

- **Immuno-oncology QSP models** with pulsed dosing, immune-response events, or combination treatment logic.
- **Autoimmune and inflammatory disease models** with flare-remission dynamics, tapering, rescue therapy, or biomarker-triggered intervention rules.
- **Mechanistic PK/PD models** with treatment switching, toxicity holds, dose delays, or state-triggered interventions.

These are exactly the kinds of systems in which the state trajectory may remain continuous while the governing equations, treatment rules, or state updates change at event times. That structure suggests event-aware simulation, variational sensitivity propagation, multiple shooting, and automatic differentiation rather than treating the entire trajectory as if it were globally smooth.

At the workflow level, most current QSP and PK/PD practice is built around general ODE, PBPK, and pharmacometric toolchains. `hybrid-ds-julia` is not meant to replace that ecosystem. Instead, it aims to complement it with a hybrid numerical layer for models where event structure materially affects simulation, sensitivities, optimization, or translational interpretation.

## Current direction

The immediate focus is to turn the current mathematical and conceptual foundation into a small but credible research platform by implementing a narrow deterministic core and one flagship biomedical example.

The package will be strongest if its first public milestones are reproducible, technically convincing, and clearly tied to end-to-end event-aware workflows that a QSP or PK/PD modeler can recognize: model specification, simulation across events, sensitivity propagation through jumps and regime changes, and schedule- or parameter-facing analysis.

That near-term scope is intentionally narrow. A focused, working demonstration is more valuable at this stage than broad coverage of every hybrid-system variant.

## Current status

The repository currently functions primarily as a conceptual and methodological foundation for the package.

The next implementation targets are:

- a deterministic hybrid core,
- a fully worked flagship biomedical example,
- and accompanying documentation that shows the workflow from model specification through simulation, sensitivities, and schedule- or parameter-facing analysis.

The initial flagship example will be chosen to make the translational value of the package clear early: not only that the model is hybrid in a mathematical sense, but that event-aware numerics improve the ability to compare regimens, analyze treatment logic, and reason about clinically meaningful regime changes.

## Mathematical approach

### Piecewise-smooth formulation

A typical mechanistic model is represented by a state vector `x`, with dynamics treated as piecewise smooth:

```text
dx/dt = f_k(x, t)   for t in [t_k, t_{k+1})
```

where the index `k` labels the active interaction or control regime.

Whenever the system crosses an event surface—for example, a dosing time, a toxicity threshold, or the activation of a new interaction term—the governing vector field changes from `f_k` to `f_{k+1}`. This places the model in the general class of **hybrid dynamical systems**, where continuous trajectories are punctuated by discrete structural changes.

For a QSP or PK/PD modeler, this is the difference between treating doses and intervention rules as small perturbations in an otherwise smooth system and treating them explicitly as regime-changing events that the solver and sensitivity calculations are designed to respect.

### Jump phenomena and impulsive updates

Many application-facing models are not only piecewise smooth in the sense that the governing vector field changes between regimes; they also contain **explicit jump phenomena**, where the state itself is updated discontinuously at an event time.

A standard representation is

```text
dx/dt = f_k(x, t)          for t in (t_k, t_{k+1})
x(t_k^+) = G_k(x(t_k^-), p)
```

where `x(t_k^-)` denotes the state immediately before the event, `x(t_k^+)` the state immediately after it, and `G_k` is a jump map that may depend on parameters `p`.

In pharmacology and QSP, this is a natural way to represent bolus dosing, pulsed immunotherapy, chemotherapy injections, rescue interventions, treatment resets, or threshold-triggered updates. A fixed-time dose can be modeled as a scheduled jump; a toxicity hold or state-triggered rescue action can be modeled as an event-surface crossing followed by a jump map.

This distinction matters computationally. Between jumps, one integrates a smooth ODE segment; at a jump, one applies an explicit state update; after the jump, one restarts integration under the same or a different vector field. That viewpoint makes it easier to generalize from one treatment model to a broad class of event-rich mechanistic models.

It also matters for sensitivities and optimization. If the model contains jump maps, then derivatives must be propagated not only through the continuous flow but also through the jump itself, using the Jacobian of the map `G_k`.

In PK/PD terms, these jump maps are not exotic abstractions. They are a direct formalization of dosing rules, pulsed interventions, and state-triggered treatment updates that already appear in many mechanistic workflows.

### Variational equations

Let `n` denote the dimension of the original state vector. To obtain well-conditioned sensitivities, the package is intended to evolve both the state `x(t)` and the Jacobian of the flow.

Along each segment, the Jacobian of the flow `J(t) = ∂x(t) / ∂x(t_k)` satisfies

```text
dJ/dt = (D_x f_k)(x(t), t) · J(t),   with   J(t_k) = I
```

where `D_x f_k` denotes the Jacobian of `f_k` with respect to the state.

This yields an augmented system of dimension `n + n^2`: the original `n` equations together with the `n^2` variational equations. The point is to propagate local sensitivities in a way that respects the event-driven structure of the model.

For impulsive models, this continuous sensitivity propagation is only part of the story. At a jump time, the sensitivity variables must also be updated by differentiating the jump map `G_k`, so that the full sensitivity calculation respects both the smooth flow and the discontinuous intervention.

Without these jump-aware variational updates, gradients for dose, timing, and schedule optimization can become noisy or misleading around events. With them, gradient-based methods have a better chance of behaving as reliably in event-rich models as they do in smoother settings.

### Multiple shooting

Given a sequence of event times or event surfaces, the full trajectory can be reformulated as a **multiple-shooting problem**:

- Integrate the model separately on each smooth segment.
- Use the variational equations to compute the Jacobian of each segment map.
- Apply the appropriate jump-map updates at impulsive events.
- Use a Newton-type solver to adjust the segment start points so that the end of each segment matches the beginning of the next, enforcing a single continuous trajectory across all segments where continuity is required and the prescribed jump conditions where impulses occur.

This often yields a better-conditioned trajectory and sensitivity framework than naive single shooting when the model contains many event-driven structural changes or explicit impulsive interventions.

For QSP- and PK/PD-facing workflows, the practical value is that multiple shooting can stabilize computations in models with many events, making continuation, fitting, and schedule comparison less brittle than they may be under a naive all-at-once forward simulation strategy.

### Automatic differentiation

**Automatic differentiation** is central to the package vision because it provides a practical way to compute Jacobians of the vector field, Jacobians of jump maps, and gradients of scalar objectives without fragile finite-difference approximations.

In event-driven, high-dimensional mechanistic models, this is especially valuable when those derivatives are used inside variational equations, jump updates, multiple-shooting solvers, and gradient-based optimization loops.

From a workflow perspective, automatic differentiation is part of what can make hybrid simulation usable in practice rather than only analyzable on paper.

## Test beds

### First biomedical target

The first biomedical model planned for this workflow is the hybrid impulsive tumor–immune model with immunotherapy and chemotherapy studied in *[Analysis of a Hybrid Impulsive Tumor-Immune Model with Immunotherapy and Chemotherapy](https://www.sciencedirect.com/science/article/abs/pii/S0960077920310080)*.

This model is intended to serve as the flagship early implementation target for the package, not just as a motivating example. It is a strong first biomedical target because the hybrid structure is not incidental: treatment is represented through pulsed interventions of different frequencies, so the long-term behavior depends directly on event timing, treatment scheduling, and the interaction between continuous tumor–immune dynamics and impulsive updates.

From a pharmacology and QSP perspective, it sits close to the kinds of questions decision-makers care about: how treatment frequency, timing, and combination strategy influence tumor control, loss of control, and the robustness of a regimen under changing conditions.

### Bayesian and stochastic extensions

A natural later extension of `hybrid-ds-julia` is to Bayesian inference for stochastic or partially observed hybrid models. In a sequential Bayesian workflow, the posterior from one inference step becomes the prior for the next, while the model dynamics determine how new data update the likelihood; this is a standard perspective in sequential Bayesian updating and related Monte Carlo methods.

For stochastic models, the continuous dynamics can be written as an SDE between events, with impulsive dose times, threshold-triggered jumps, or regime switches represented explicitly in the hybrid structure. In that setting, the solver would propagate sample paths between events, apply jump maps at intervention times, and use the resulting transition law or predictive distribution to evaluate likelihood contributions for new observations.

This suggests a Bayesian extension layer in which hybrid simulation is combined with MCMC, sequential tempered MCMC, or particle-filtering ideas. The practical role of `hybrid-ds-julia` in such a workflow would be to provide event-aware deterministic or stochastic simulation, expose the hybrid structure cleanly enough to support likelihood construction, and eventually enable sensitivity-aware inference for parameter learning, schedule learning, or virtual-patient updating in event-rich mechanistic models.

### Filippov pseudo-Hopf normal form

Before applying these ideas to more complex biomedical models, it is useful to validate them on a low-dimensional system whose analytical structure is well understood. A natural choice is the planar Filippov **pseudo-Hopf** normal form in the “two invisible tangencies” case studied by Kuznetsov, Rinaldi, and Gragnani in *[One-parameter Bifurcations in Planar Filippov Systems](https://pure.iiasa.ac.at/id/eprint/6817/)*.

This system is a strong test bed for `hybrid-ds-julia` because it is two-dimensional, canonical in the Filippov literature, and exercises exactly the non-smooth machinery the package aims to provide: event detection at the switching surface, handling of sliding and crossing dynamics, construction of Poincaré maps for hybrid orbits, and continuation of limit cycles through a discontinuity-induced bifurcation.

A natural early milestone is to reproduce the pseudo-Hopf scenario robustly—tracking the birth of the crossing limit cycle, its stability, and its dependence on a bifurcation parameter—before turning to higher-dimensional biomedical models.

## Example applications

The same mathematical and computational ideas can be used across a range of mechanistic modeling problems in pharmacology and beyond.

### QSP and PK/PD

Many QSP and PK/PD models already contain hybrid structure in practice: dosing pulses, treatment holidays, state-dependent interventions, switching therapies, toxicity holds, and threshold-mediated biological responses. A package like `hybrid-ds-julia` is intended to make event-aware simulation, variational sensitivity propagation, and multiple shooting natural parts of the workflow for these models.

That would make it easier to study how the timing and logic of interventions shape long-term outcomes such as remission, relapse, resistance, or sustained control. It also opens the door to more systematic optimization over dose, timing, and treatment rules rather than relying only on hand-picked regimen comparisons.

### Translational pharmacology

Many of the most important translational questions are inherently dynamical: whether a schedule sustains control, whether biomarker trajectories indicate a regime shift, or whether a mechanism remains effective under realistic interruptions or patient heterogeneity.

`hybrid-ds-julia` is intended to support this layer by making it easier to represent treatment logic, biomarker thresholds, and intervention schedules explicitly inside mechanistic models. That can help identify which strategies are robust, which are fragile, and which biological hypotheses are most consistent with clinically relevant patterns of response.

### SAR progression and mechanism differentiation

SAR studies are central to hit-to-lead and lead-optimization work, but the link between SAR and downstream dynamical treatment behavior is often indirect. Compounds are often compared on potency, selectivity, or exposure metrics, but not always on how those differences propagate through a mechanistic disease model under realistic regimens.

A hybrid dynamical-systems workflow could help close that gap by mapping compound-level differences into model parameters and then studying how those differences alter qualitative treatment regimes. In that setting, mechanism differentiation becomes more than comparing endpoint potency: it becomes possible to ask which mechanism or chemotype gives a wider and more robust therapeutic regime under realistic intervention logic.

### Autoimmune and inflammatory disease

Autoimmune and inflammatory diseases are another promising domain because their trajectories often involve flares, remission, tapering, rescue therapy, and long periods of partial control. These state changes are biologically and clinically important, and they are often driven by interventions or thresholds that make the system effectively hybrid even when the underlying biological model is written as an ODE.

A hybrid dynamical-systems workflow would allow these disease trajectories to be analyzed in terms of regime changes and event timing. In practical terms, that could support better tapering strategies, more informative biomarker interpretation, and more systematic comparison of regimens intended to maintain remission while minimizing drug burden.

### Crop science and precision agriculture

Although the primary intended destination of the package is pharmacology, the original motivating example came from crop science, where mechanistic multiscale models can also exhibit hybrid structure. This example remains valuable because it illustrates the broader claim of the project: that there are scientifically important mechanistic domains in which hybrid structure is present, but the corresponding mathematical tools are not yet routine.

Crop science is therefore not the main target for the package, but it remains an instructive example of why such a package could be useful.

## Original crop-science motivation

The immediate technical motivation came from the multiscale bambara groundnut model of Dodd et al., which couples plant-level ODEs to canopy-level competition.

In that model, each plant evolves according to nonlinear growth equations, while changing interaction structure determines local competition and ultimately influences yield. When the active interaction structure is fixed, the model evolves smoothly; when a new interaction becomes active, trajectories remain continuous but growth rates change abruptly. That makes the full coupled system a natural example of a **hybrid dynamical system** rather than a globally smooth ODE.

The analogy to pharmacology is direct: canopy occlusion changes local growth rates in much the same way that dosing rules, toxicity thresholds, or therapy switches change the effective dynamics in QSP models. Different scientific domain, same underlying mathematical issue of event-triggered changes in structure.