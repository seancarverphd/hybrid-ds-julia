# hybrid-ds-julia

*A Julia package under development that brings event-aware simulation, variational equations, multiple shooting, and automatic differentiation to mechanistic models with dosing events, thresholds, switching logic, and other hybrid structure.*

The main intended application area is **quantitative systems pharmacology (QSP) and PK/PD**, where mechanistic models are used to study dose and schedule optimization, response heterogeneity, relapse and remission dynamics, and translational decision-making.

Many pharmacology models are treated numerically as if they were globally smooth, even though the scientific questions that matter most often involve **event-driven changes** in treatment logic or biological regime. Dosing pulses, treatment holidays, toxicity holds, rescue interventions, threshold-mediated responses, and therapy switches all create the kind of piecewise-smooth structure for which hybrid dynamical-systems methods are naturally suited.

This project aims to make those methods more usable in domain-facing workflows. The goal is not to rebuild low-level solver infrastructure from scratch, but to build a practical layer on top of Julia’s scientific-computing ecosystem that helps modelers work more effectively with trajectories that cross many events and decision boundaries.

## Why this matters

This project is deliberately positioned at the interface of **mechanistic pharmacology**, **QSP**, and **PK/PD-driven translational decision-making**.

Key use cases include:

- **Treatment-schedule dependence** — comparing regimens, continuation across timing and dose parameters, and understanding when small changes in regimen logic produce large changes in long-term outcome.
- **Optimization, fitting, and model comparison** — using event-aware sensitivities and multiple shooting to improve conditioning when models contain impulses, event surfaces, or threshold-triggered changes.
- **Mechanism differentiation and SAR** — connecting compound- or mechanism-level differences not only to potency and exposure, but also to the qualitative treatment regimes they produce under realistic intervention logic.
- **Translational decision support** — embedding biomarker thresholds, toxicity triggers, and regimen logic explicitly in the model so outputs speak more directly to robust schedule design and clinically meaningful regime changes.

The goal is to make hybrid dynamical-systems workflows directly usable for the kinds of decision-focused pharmacology and QSP roles that need to connect mechanistic models to SAR progression, mechanism-of-action differentiation, and early clinical strategy.

## Motivation

This project grew out of the observation that advanced dynamical-systems techniques—especially variational equations, multiple shooting, and automatic differentiation for event-driven models—remain underused in several mechanistic fields, including pharmacology, crop science, and precision agriculture.

These methods were part of doctoral training in dynamical systems at Cornell, including work with John Guckenheimer on a hybrid dynamical-systems model of locomotion. Guckenheimer coauthored *[Nonlinear Oscillations, Dynamical Systems, and Bifurcations of Vector Fields](https://doi.org/10.1137/1026128)*, a canonical reference for the geometric, variational, and bifurcation tools that underpin many modern treatments of periodic orbits and sensitivities in both smooth and hybrid systems.

Later work inspired by Dodd et al. highlighted that methods that feel standard in one mathematical community are often not standard in nearby application domains. That insight led naturally toward immuno-oncology, QSP, and PK/PD, where mechanistic models increasingly matter for model-informed development, but where models with impulses, treatment thresholds, and other non-smooth features still need stronger hybrid-system workflows than are commonly available in domain-facing software.

## Why QSP and PK/PD first

QSP and PK/PD are the main intended application areas because they already rely heavily on mechanistic ODE models and are tied to questions pharmacology considers important.

Representative examples include:

- Immuno-oncology QSP models with dosing and immune-response events.
- Autoimmune and inflammatory disease models with flare-remission dynamics, tapering, and rescue therapy.
- Mechanistic PK/PD models with treatment switching, toxicity holds, or state-triggered interventions.

These are exactly the kinds of systems in which a model can remain continuous in state while its governing equations change at event times. That structure suggests event-aware simulation, variational sensitivity propagation, multiple shooting, and automatic differentiation rather than treating the full trajectory as if it were globally smooth.

## Original crop-science motivation

The immediate technical motivation came from the multiscale bambara groundnut model of Dodd et al., which couples plant-level ODEs to canopy-level competition.

In that model, each plant evolves according to nonlinear growth equations, while changing interaction structure determines local competition and ultimately influences yield. When the active interaction structure is fixed, the model evolves smoothly; when a new interaction becomes active, trajectories remain continuous but growth rates change abruptly. That makes the full coupled system a natural example of a **hybrid dynamical system** rather than a globally smooth ODE.

The analogy to pharmacology is direct: canopy occlusion changes local growth rates in much the same way that dosing rules, toxicity thresholds, or therapy switches change the effective dynamics in QSP models. Different scientific domain, same underlying mathematical issue of event-triggered changes in structure.

## Mathematical approach

### Piecewise-smooth formulation

A typical mechanistic model is represented by a state vector `x`, with dynamics treated as piecewise smooth:

```text
dx/dt = f_k(x, t)   for t in [t_k, t_{k+1})
```

where the index `k` labels the active interaction or control regime.

Whenever the system crosses an event surface—for example, a dosing time, a toxicity threshold, or the activation of a new interaction term—the governing vector field changes from `f_k` to `f_{k+1}`. This places the model in the general class of **hybrid dynamical systems**, where continuous trajectories are punctuated by discrete structural changes.

### Variational equations

Let `n` denote the dimension of the original state vector. To obtain well-conditioned sensitivities, the package is intended to evolve both the state `x(t)` and the Jacobian of the flow.

Along each segment, the Jacobian of the flow `J(t) = ∂x(t) / ∂x(t_k)` satisfies

```text
dJ/dt = (D_x f_k)(x(t), t) · J(t),   with   J(t_k) = I
```

where `D_x f_k` denotes the Jacobian of `f_k` with respect to the state.

This yields an augmented system of dimension `n + n^2`: the original `n` equations together with the `n^2` variational equations. The point is to propagate local sensitivities in a way that respects the event-driven structure of the model.

### Multiple shooting

Given a sequence of event times or event surfaces, the full trajectory can be reformulated as a **multiple-shooting problem**:

- Integrate the model separately on each smooth segment.
- Use the variational equations to compute the Jacobian of each segment map.
- Use a Newton-type solver to adjust the segment start points so that the end of each segment matches the beginning of the next, enforcing a single continuous trajectory across all segments.

This often yields a better-conditioned trajectory and sensitivity framework than naive single shooting when the model contains many event-driven structural changes.

### Automatic differentiation

**Automatic differentiation** is central to the package vision because it provides a practical way to compute Jacobians of the vector field and gradients of scalar objectives without fragile finite-difference approximations.

In event-driven, high-dimensional mechanistic models, this is especially valuable when those derivatives are used inside variational equations, multiple-shooting solvers, and gradient-based optimization loops.

## Test beds

### Filippov pseudo-Hopf normal form

Before applying these ideas to complex biomedical models, it is useful to validate them on a low-dimensional system whose analytical structure is well understood. A natural choice is the planar Filippov **pseudo-Hopf** normal form in the “two invisible tangencies” case studied by Kuznetsov, Rinaldi, and Gragnani in *[One-parameter Bifurcations in Planar Filippov Systems](https://pure.iiasa.ac.at/id/eprint/6817/)*.

This system is a strong test bed for `hybrid-ds-julia` because it is two-dimensional, canonical in the Filippov literature, and exercises exactly the non-smooth machinery the package aims to provide: event detection at the switching surface, handling of sliding and crossing dynamics, construction of Poincaré maps for hybrid orbits, and continuation of limit cycles through a discontinuity-induced bifurcation.

A natural early milestone is to reproduce the pseudo-Hopf scenario robustly—tracking the birth of the crossing limit cycle, its stability, and its dependence on a bifurcation parameter—before turning to higher-dimensional biomedical models.

### First biomedical target

The first biomedical model planned for this workflow is the hybrid impulsive tumor–immune model with immunotherapy and chemotherapy studied in *[Analysis of a Hybrid Impulsive Tumor-Immune Model with Immunotherapy and Chemotherapy](https://www.sciencedirect.com/science/article/abs/pii/S0960077920310080)*.

This is a strong first biomedical target because the hybrid structure is not incidental: treatment is represented through pulsed interventions of different frequencies, so the long-term behavior depends directly on event timing, treatment scheduling, and the interaction between continuous tumor–immune dynamics and impulsive updates. From a pharmacology and QSP perspective, it sits close to questions decision-makers care about: how treatment frequency, timing, and combination strategy influence tumor control.

## Example applications

The same mathematical and computational ideas can be used across a range of mechanistic modeling problems in pharmacology and beyond.

### QSP and PK/PD

Many QSP and PK/PD models already contain hybrid structure in practice: dosing pulses, treatment holidays, state-dependent interventions, switching therapies, toxicity holds, and threshold-mediated biological responses. A package like `hybrid-ds-julia` is intended to make event-aware simulation, variational sensitivity propagation, and multiple shooting natural parts of the workflow for these models.

That would make it easier to study not only how strongly a drug acts, but how the timing and logic of interventions shape long-term outcomes such as remission, relapse, resistance, or sustained control. It also opens the door to more systematic optimization over dose, timing, and treatment rules rather than relying only on hand-picked regimen comparisons.

### Mechanistic pharmacology and translational strategy

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

## Software plan

Planned implementation details include:

- **Language:** Julia.
- **ODE integration and sensitivity infrastructure:** SciML / [`DifferentialEquations.jl`](https://github.com/SciML/DifferentialEquations.jl) and related tools.
- **Boundary-value and shooting infrastructure:** `BoundaryValueDiffEq.jl` and related shooting workflows.
- **Automatic differentiation:** likely `ForwardDiff.jl` or `ReverseDiff.jl`, subject to testing and performance considerations.
- **Optimization:** `Optimization.jl`, `Optim.jl`, `NLopt.jl`, or custom Newton-style solvers.

Related Julia ecosystem tools and references:

- **[`BifurcationKit.jl`](https://github.com/bifurcationkit/BifurcationKit.jl)** — Julia tooling for bifurcation analysis.
- **[`DynamicalSystems.jl`](https://github.com/JuliaDynamics/DynamicalSystems.jl)** — JuliaDynamics library for nonlinear dynamics and time-series analysis.

## Status and near-term roadmap

This project is currently in the **early design and implementation** phase, with a roadmap aimed at pharmacology-relevant proof-of-concept workflows.

Near-term milestones:

- [ ] Build a minimal Julia package skeleton, including module structure, dependencies, and tests.
- [ ] Integrate automatic differentiation for vector-field Jacobians and objective gradients.
- [ ] Implement variational-equation propagation for piecewise-smooth models (using AD-backed Jacobians).
- [ ] Implement multiple-shooting support across event-defined segments (using AD-backed sensitivities).
- [ ] Validate the workflow on the planar Filippov pseudo-Hopf normal form as a controlled non-smooth testbed for hybrid dynamics, event detection, and sensitivities.
- [ ] Demonstrate the workflow on a hybrid tumor–immune QSP example of pharmacological relevance, focusing on schedule dependence and robustness to treatment timing.
- [ ] Extend the workflow to an autoimmune or inflammatory disease example with flare/remission dynamics, tapering rules, or rescue therapy represented explicitly as event structure.
- [ ] Package the result as reusable software intended for practitioners outside traditional dynamical-systems communities.

## Licensing and IP posture

This repository is currently marked **“All rights reserved.”** In practical terms, that means the code is not yet licensed for reuse or redistribution; it is shared here to illustrate ongoing work, not as a finished open-source product.

That posture is **provisional rather than permanent**. The goal is to keep IP options open so that future collaborators or an employer can help determine the most appropriate long-term model—whether that is an internal company library, a company-backed open-source project, or a hybrid arrangement that balances community access with strategic needs.

The directional preference is toward an eventual open-source model once a stable institutional home and governance structure are in place, but for now the repository is public for visibility and discussion while the IP remains flexible.

## Further reading

The list below is intended as a starting point for readers who want to explore the surrounding literature; it includes a mix of sources that directly shaped this project and others identified as clearly relevant while mapping the broader landscape.

### Core dynamical systems / hybrid methods

- **[Nonlinear Oscillations, Dynamical Systems, and Bifurcations of Vector Fields](https://doi.org/10.1137/1026128)** — John Guckenheimer and Philip Holmes.
- **[One-parameter Bifurcations in Planar Filippov Systems](https://pure.iiasa.ac.at/id/eprint/6817/)** — Kuznetsov, Rinaldi, and Gragnani, *International Journal of Bifurcation and Chaos*, 2003.
- **[The Pseudo-Hopf Bifurcation for Planar Discontinuous Piecewise Linear Differential Systems](https://ddd.uab.cat/pub/artpub/2017/gsduab_4516/nondyn_a2017v90p1829preprint.pdf)** — Castillo, Llibre, and Verduzco, *Nonlinear Dynamics*, 2017.
- **[Classification of Boundary Equilibrium Bifurcations in Planar Filippov Systems](https://pubmed.ncbi.nlm.nih.gov/26826860/)** — Glendinning et al., *Chaos*, 2016.
- **[Dynamical Modeling of Drug Effect Using Hybrid Systems](https://pmc.ncbi.nlm.nih.gov/articles/PMC3639233/)** — Li, Qian, Yang, and Dougherty, *EURASIP Journal on Bioinformatics and Systems Biology*, 2012.

### QSP / PK–PD concepts and practice

- **Quantitative Systems Pharmacology Modeling in Immuno-Oncology: Hypothesis Testing, Dose Optimization, and Efficacy Prediction** — representative IO-focused QSP work.
- **[Analysis of a Hybrid Impulsive Tumor-Immune Model with Immunotherapy and Chemotherapy](https://www.sciencedirect.com/science/article/abs/pii/S0960077920310080)** — hybrid tumor–immune model with pulsed treatment schedules.
- **Recent Applications of Quantitative Systems Pharmacology and Model-Informed Drug Development** — review literature on QSP in oncology and related areas.
- **Integrating Multiscale Modeling with Drug Effects for Cancer Treatment** — multiscale mechanistic modeling with a systems pharmacology perspective.
- **[Disease Processes as Hybrid Dynamical Systems](https://arxiv.org/abs/1208.3858)** — hybrid treatment scheduling and control-theoretic framing for biomedical models.
- **State-Dependent Impulsive Control Strategies for a Tumor-Immune Model** — representative state-dependent impulsive treatment analysis.
- **[Multiscale Tumor Modeling With Drug Pharmacokinetic/Pharmacodynamic Information Using Stochastic Hybrid Systems](https://journals.sagepub.com/doi/abs/10.1177/1176935118790262)** — representative hybrid tumor framework linking PK/PD to tumor modeling.

### Mechanistic crop models and trait optimization

- **A Multiscale Mathematical Model Describing the Growth and Development of Bambara Groundnut** — Dodd et al., *Journal of Theoretical Biology*, 2023.
- Papers on canopy structure, light interception, and crop growth modeling that emphasize mechanistic treatment of plant traits and planting arrangements.