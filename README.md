# hybrid-ds-julia

*A Julia package under development that brings event-aware simulation, variational equations, multiple shooting, and automatic differentiation to mechanistic models with dosing events, thresholds, switching logic, and other hybrid structure.*

The main intended application area is **quantitative systems pharmacology (QSP) and PK/PD**, where mechanistic models are used to study dose and schedule optimization, response heterogeneity, relapse and remission dynamics, and translational decision-making.

Many pharmacology models are treated numerically as if they were globally smooth, even though the scientific questions that matter most often involve **event-driven changes** in treatment logic or biological regime. Dosing pulses, treatment holidays, toxicity holds, rescue interventions, threshold-mediated responses, and therapy switches all create the kind of piecewise-smooth structure for which hybrid dynamical-systems methods are naturally suited.

This project aims to make those methods more usable in domain-facing workflows. The goal is not to rebuild low-level solver infrastructure from scratch, but to build a practical layer on top of Julia’s scientific-computing ecosystem that helps modelers work more effectively with trajectories that cross many events and decision boundaries.

The near-term goal is a compact deterministic core with one flagship biomedical example.

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

## Current direction

The immediate focus is to turn the current mathematical and conceptual foundation into a small but credible research platform by implementing a narrow deterministic core and one flagship biomedical example. The package will be strongest if its first public milestones are reproducible, technically convincing, and clearly tied to end-to-end event-aware workflows.

## Current status

The repository currently functions primarily as a conceptual and methodological foundation for the package. The next implementation targets are a deterministic hybrid core, a fully worked flagship biomedical example, and accompanying documentation that shows the workflow from model specification through simulation, sensitivities, and schedule- or parameter-facing analysis.

## Mathematical approach

### Piecewise-smooth formulation

A typical mechanistic model is represented by a state vector `x`, with dynamics treated as piecewise smooth:

```text
dx/dt = f_k(x, t)   for t in [t_k, t_{k+1})
```

where the index `k` labels the active interaction or control regime.

Whenever the system crosses an event surface—for example, a dosing time, a toxicity threshold, or the activation of a new interaction term—the governing vector field changes from `f_k` to `f_{k+1}`. This places the model in the general class of **hybrid dynamical systems**, where continuous trajectories are punctuated by discrete structural changes.

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

It also matters for sensitivities and optimization. If the model contains jump maps, then derivatives must be propagated not only through the continuous flow but also through the jump itself, using the Jacobian of the map `G_k`. In that sense, impulsive models are not a special corner case but one of the main motivating classes for the package.

### Variational equations

Let `n` denote the dimension of the original state vector. To obtain well-conditioned sensitivities, the package is intended to evolve both the state `x(t)` and the Jacobian of the flow.

Along each segment, the Jacobian of the flow `J(t) = ∂x(t) / ∂x(t_k)` satisfies

```text
dJ/dt = (D_x f_k)(x(t), t) · J(t),   with   J(t_k) = I
```

where `D_x f_k` denotes the Jacobian of `f_k` with respect to the state.

This yields an augmented system of dimension `n + n^2`: the original `n` equations together with the `n^2` variational equations. The point is to propagate local sensitivities in a way that respects the event-driven structure of the model.

For impulsive models, this continuous sensitivity propagation is only part of the story. At a jump time, the sensitivity variables must also be updated by differentiating the jump map `G_k`, so that the full sensitivity calculation respects both the smooth flow and the discontinuous intervention.

### Multiple shooting

Given a sequence of event times or event surfaces, the full trajectory can be reformulated as a **multiple-shooting problem**:

- Integrate the model separately on each smooth segment.
- Use the variational equations to compute the Jacobian of each segment map.
- Apply the appropriate jump-map updates at impulsive events.
- Use a Newton-type solver to adjust the segment start points so that the end of each segment matches the beginning of the next, enforcing a single continuous trajectory across all segments where continuity is required and the prescribed jump conditions where impulses occur.

This often yields a better-conditioned trajectory and sensitivity framework than naive single shooting when the model contains many event-driven structural changes or explicit impulsive interventions.

### Automatic differentiation

**Automatic differentiation** is central to the package vision because it provides a practical way to compute Jacobians of the vector field, Jacobians of jump maps, and gradients of scalar objectives without fragile finite-difference approximations.

In event-driven, high-dimensional mechanistic models, this is especially valuable when those derivatives are used inside variational equations, jump updates, multiple-shooting solvers, and gradient-based optimization loops.

## Test beds

### First biomedical target

The first biomedical model planned for this workflow is the hybrid impulsive tumor–immune model with immunotherapy and chemotherapy studied in *[Analysis of a Hybrid Impulsive Tumor-Immune Model with Immunotherapy and Chemotherapy](https://www.sciencedirect.com/science/article/abs/pii/S0960077920310080)*.

This model is intended to serve as the flagship early implementation target for the package, not just as a motivating example. It is a strong first biomedical target because the hybrid structure is not incidental: treatment is represented through pulsed interventions of different frequencies, so the long-term behavior depends directly on event timing, treatment scheduling, and the interaction between continuous tumor–immune dynamics and impulsive updates. From a pharmacology and QSP perspective, it sits close to questions decision-makers care about: how treatment frequency, timing, and combination strategy influence tumor control.

### Bayesian and stochastic extensions

A natural later extension of `hybrid-ds-julia` is to Bayesian inference for stochastic or partially observed hybrid models. In a sequential Bayesian workflow, the posterior from one inference step becomes the prior for the next, while the model dynamics determine how new data update the likelihood; this is a standard perspective in sequential Bayesian updating and related Monte Carlo methods.

For stochastic models, the continuous dynamics can be written as an SDE between events, with impulsive dose times, threshold-triggered jumps, or regime switches represented explicitly in the hybrid structure. In that setting, the solver would propagate sample paths between events, apply jump maps at intervention times, and use the resulting transition law or predictive distribution to evaluate likelihood contributions for new observations.

This suggests a Bayesian extension layer in which hybrid simulation is combined with MCMC, sequential tempered MCMC, or particle-filtering ideas. The practical role of `hybrid-ds-julia` in such a workflow would be to provide event-aware deterministic or stochastic simulation, expose the hybrid structure cleanly enough to support likelihood construction, and eventually enable sensitivity-aware inference for parameter learning, schedule learning, or virtual-patient updating in event-rich mechanistic models.

### Filippov pseudo-Hopf normal form

Before applying these ideas to complex biomedical models, it is useful to validate them on a low-dimensional system whose analytical structure is well understood. A natural choice is the planar Filippov **pseudo-Hopf** normal form in the “two invisible tangencies” case studied by Kuznetsov, Rinaldi, and Gragnani in *[One-parameter Bifurcations in Planar Filippov Systems](https://pure.iiasa.ac.at/id/eprint/6817/)*.

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
- **[`HybridSystems.jl`](https://github.com/blegat/HybridSystems.jl)** — a general Julia interface for hybrid systems and hybrid automata, relevant as ecosystem context even though `hybrid-ds-julia` is intended to emphasize event-aware simulation, sensitivities, and optimization for mechanistic QSP and PK/PD models.

## Roadmap

The project is organized in stages, moving from a minimal deterministic hybrid core toward QSP-facing workflows, selected stochastic extensions, and more demanding non-smooth benchmarks.

### Stage 1 — Narrow deterministic core

- Implement a minimal Julia package skeleton with tests and documentation.
- Represent hybrid and impulsive systems with:
  - smooth ODE flows between events,
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

- Develop one fully documented flagship biomedical example centered on hybrid tumor-immune treatment dynamics.
- Show the full workflow from model definition to event-aware simulation, sensitivity propagation, and schedule- or parameter-facing analysis.
- Use the example as a tutorial, benchmark, and proof-of-concept for clinically meaningful event-driven modeling questions.
- Add tests and reproducible scripts so the example also serves as a numerical validation target.

Primary outcome: a compact end-to-end demonstration stack that makes the package credible to both hybrid-systems and pharmacology audiences.

### Stage 3 — QSP-facing workflows

- Build convenience abstractions for repeated dosing, treatment holidays, toxicity holds, rescue interventions, and therapy switching.
- Add objective functions and workflows for schedule comparison, schedule optimization, and event-aware parameter estimation.
- Support virtual-patient style parameter exploration and uncertainty analysis in event-rich mechanistic models.
- Improve ergonomics so the package helps answer pharmacology questions that are decision-facing rather than purely mathematical.

Primary outcome: a package that begins to look like useful QSP and PK/PD workflow infrastructure rather than only a mathematical prototype.

### Stage 4 — Stochastic and Bayesian extensions

- Identify one stochastic hybrid model class that is genuinely relevant for pharmacology.
- Provide a clean event-aware simulation interface for that class, including jumps or regime changes at predictable or state-dependent times.
- Connect that simulation layer to one concrete inference workflow, such as sequential Bayesian updating or particle-based likelihood evaluation.
- Explore sensitivity-aware inference only where the deterministic abstractions are already robust enough to support it.

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
- Revisit licensing and packaging based on collaboration opportunities and the eventual institutional home of the project.

Primary outcome: a research-grade codebase and documentation set that clearly communicates a distinctive methodological identity.

## Future directions

The next phase of `hybrid-ds-julia` should focus on turning the current mathematical and conceptual foundation into a small, credible research platform that is useful both to hybrid-systems specialists and to QSP / PK-PD practitioners.

Near-term development should remain narrow: one deterministic core, one flagship biomedical example, and one compact end-to-end workflow from model specification to simulation, sensitivities, and parameter- or schedule-facing analysis. That is likely more valuable than trying to cover every hybrid-system variant too early.

Longer term, the package should expand in a staged way toward QSP-facing abstractions, differentiable hybrid simulation as a defining feature, selective stochastic and Bayesian extensions, and low-dimensional Filippov benchmarks used as serious numerical validation problems. At the same time, the repository should continue to evolve as both software and technical narrative, with worked examples, benchmark notes, and concise documentation that make the methodological identity of the project immediately clear.

## Licensing and IP posture

This repository is currently marked **“All rights reserved.”** In practical terms, that means the code is not yet licensed for reuse or redistribution; it is shared here to illustrate ongoing work, not as a finished open-source product.

That posture is **provisional rather than permanent**. The goal is to keep IP options open so that future collaborators or an employer can help determine the most appropriate long-term model—whether that is an internal company library, a company-backed open-source project, or a hybrid arrangement that balances community access with strategic needs.

Issues, discussion, and scientific feedback are welcome, but reuse requires explicit permission.

The directional preference is toward an eventual open-source model once a stable institutional home and governance structure are in place, but for now the repository is public for visibility and discussion while the IP remains flexible and the codebase continues to evolve.

## Further reading

The list below is intended as a starting point for readers who want to explore the surrounding literature; it includes a mix of sources that directly shaped this project and others identified as clearly relevant while mapping the broader landscape.

### Related hybrid-systems papers in other domains

- Hereid, A., Kolathaya, S., Hubicki, J., & Ames, A. D. (2015). *Hybrid Zero Dynamics based Multiple Shooting Optimization with Applications to Bipedal Robotic Walking*. *IEEE International Conference on Robotics and Automation (ICRA)*. [Link](http://ames.caltech.edu/icra_2015_multiple_shooting.pdf)  
  This paper is particularly relevant because it combines hybrid locomotion dynamics with multiple-shooting optimization and derivative-based numerical updates. It validates the idea that hybrid systems with impacts and discrete events can be treated using structured multiple shooting and analytically informed sensitivities, closely parallel to the numerical philosophy behind `hybrid-ds-julia` even though the application domain is bipedal robotic walking rather than pharmacology.

- Johnson, A. M., Burden, S. A., & Koditschek, D. E. (2016). *A hybrid systems model for simple manipulation and self-manipulation systems*. *The International Journal of Robotics Research*. [Link](http://faculty.washington.edu/sburden/_papers/JohnsonBurden2016ijrr.pdf)  
  This paper is relevant because it develops a formal hybrid dynamical-systems model for robotic systems with intermittent impacts and contact changes, exactly the kind of event-driven structure that motivates `hybrid-ds-julia`. Although the application domain is robotics rather than pharmacology, the underlying numerical and conceptual issues—mode changes, discontinuities, reset logic, and mathematically consistent event handling—are closely analogous.

- Li, H., & Wensing, P. M. (2020). *Hybrid Systems Differential Dynamic Programming for Whole-Body Motion Planning of Legged Robots*. [Link](http://arxiv.org/abs/2006.08102)  
  This paper is relevant because it treats trajectory optimization for systems with impacts and state-based switching, showing how optimization must be adapted when dynamics are hybrid rather than globally smooth. That is directly aligned with the long-term aim of making event-aware sensitivities and optimization central features of `hybrid-ds-julia`.

- Fariba, F., Eslami, M., & Jafari Shahbazzadeh, M. (2023). *Stability Analysis and Voltage Control in the Power System Based on the Hybrid Automata Model*. *Mathematical Problems in Engineering*. [Link](https://onlinelibrary.wiley.com/doi/10.1155/2023/5037957)  
  This paper is relevant because it uses a hybrid automata framework to represent the interaction of continuous power-system dynamics with discrete switching events such as disturbances, capacitor-bank actions, and transformer operations. Its relevance here is not domain overlap, but methodological overlap: it shows that hybrid formalisms become useful whenever system behavior depends on both continuous evolution and discrete supervisory logic.

- Odunlami, B. G., Netto, M., & Susuki, Y. (2025). *Hybrid dynamical systems modeling of power systems*. [Link](https://arxiv.org/abs/2509.02822)  
  This paper is relevant because it surveys hybrid modeling approaches for modern power systems, including hybrid automata, switched systems, and piecewise-affine formulations. It helps reinforce a broader claim behind `hybrid-ds-julia`: hybrid methods are not a niche construction for one scientific field, but a general framework for domains where continuous dynamics interact with discrete events, controls, and switching structure.

### Core dynamical systems / hybrid methods

- Guckenheimer, J., & Holmes, P. (1983). *Nonlinear Oscillations, Dynamical Systems, and Bifurcations of Vector Fields*. Springer. [Link](https://doi.org/10.1137/1026128)  
  A classic reference for geometric dynamical systems, periodic orbits, variational ideas, and bifurcations. It provides much of the mathematical background that motivates the methodology behind this project.

- Kuznetsov, Y. A., Rinaldi, S., & Gragnani, A. (2003). *One-parameter bifurcations in planar Filippov systems*. *International Journal of Bifurcation and Chaos*. [Link](https://pure.iiasa.ac.at/id/eprint/6817/)  
  A foundational paper on codimension-one bifurcations in planar Filippov systems. It is especially useful here because it organizes the local and global bifurcation picture in a way that supports computational test problems.

- Castillo, J., Llibre, J., & Verduzco, F. (2017). *The pseudo-Hopf bifurcation for planar discontinuous piecewise linear differential systems*. *Nonlinear Dynamics*, 90, 1829–1840. [Link](https://doi.org/10.1007/s11071-017-3766-9)  
  A useful reference for pseudo-Hopf behavior in planar discontinuous systems. It is relevant when choosing a low-dimensional Filippov benchmark for testing continuation and cycle-detection ideas.

- Glendinning, P. (2016). *Classification of boundary equilibrium bifurcations in planar Filippov systems*. *Chaos*, 26(1), 013108. [Link](https://pubmed.ncbi.nlm.nih.gov/26826860/)  
  A focused treatment of boundary equilibrium bifurcations, which are central when equilibria collide with switching manifolds. This is especially relevant for threshold-based biological or control models.

- Li, C., Qian, H., Yang, J., & Dougherty, E. R. (2012). *Dynamical Modeling of Drug Effect Using Hybrid Systems*. *EURASIP Journal on Bioinformatics and Systems Biology*. [Link](https://pmc.ncbi.nlm.nih.gov/articles/PMC3639233/)  
  A clear example of hybrid-systems thinking applied directly to pharmacology. It helps connect abstract hybrid dynamical-systems ideas to drug-effect modeling in a biomedical setting.

- Belta, C., Habets, L. C. G. J. M., Kumar, V., Mink, A., & Weiss, R. (2013). *Disease processes as hybrid dynamical systems*. [Link](https://arxiv.org/abs/1208.3858)  
  A broad conceptual framing of disease progression and treatment as a hybrid dynamical process. It is useful here because it shows that hybrid-system language is not limited to engineering examples and can be applied naturally to biomedical processes.

### QSP / PK–PD concepts and practice

- Pang, L., Shen, L., & Zhao, Z. (2016). *Mathematical Modelling and Analysis of the Tumor Treatment Regimens with Pulsed Immunotherapy and Chemotherapy*. *Computational and Mathematical Methods in Medicine*. [Link](https://pmc.ncbi.nlm.nih.gov/articles/PMC4779848/)  
  A central motivation for this repository. The paper studies pulsed immunotherapy and chemotherapy in a low-dimensional hybrid treatment setting and shows how regimen timing, minimum effective concentration, drug half-life, and resistance can shape tumor-control outcomes.

- Zhao, Z., Pang, L., & Li, Q. (2021). *Analysis of a hybrid impulsive tumor–immune model with immunotherapy and chemotherapy*. *Chaos, Solitons & Fractals*, 144, 110617. [Link](https://doi.org/10.1016/j.chaos.2020.110617)  
  A particularly relevant follow-on paper because it studies a hybrid impulsive tumor–immune model with fixed-time pulsed immunotherapy and state-feedback impulsive chemotherapy. It is one of the closest recent matches to the event-aware treatment logic that `hybrid-ds-julia` is intended to support.

- Kim, B., Cho, Y., Nie, Q., & Jung, S. (2016). *Stability of a tumor–immune model with state-dependent impulses*. *Discrete Dynamics in Nature and Society*, 2016, 2979414. [Link](https://doi.org/10.1155/2016/2979414)  
  An example of state-dependent impulsive treatment, where therapy is triggered when the system crosses a threshold. It provides a concrete case of hybrid structure driven by biological state rather than only by fixed dosing schedules.

- Wang, X., & Zhang, Y. (2021). *Dynamics of immunotherapy antitumor models with impulsive control strategy*. *Mathematical Methods in the Applied Sciences*. [Link](https://doi.org/10.1002/mma.7788)  
  A useful impulsive-treatment reference showing that antitumor models with impulsive control remain an active area of mathematical development. It strengthens the case for hybrid and event-aware numerical workflows in mechanistic oncology models.

- Grebogi, C., Ren, H., Baptista, M. S., & Yang, H. (2017). *Impulsive chemotherapy strategies for tumors: a Lyapunov approach*. *Philosophical Transactions of the Royal Society A*, 375, 20160221. [Link](https://doi.org/10.1098/rsta.2016.0221)  
  An impulse-control treatment analysis using Lyapunov and comparison techniques to derive analytical conditions on chemotherapeutic dose and timing. It reinforces the view that impulsive methods are a natural mathematical language for tumor chemotherapy scheduling.

- Arteaga-Bejarano, R., & Torres, L. (2024). *Multi-dose pharmacokinetic models on time scales*. *Journal of Pharmacokinetics and Pharmacodynamics*. [Link](https://doi.org/10.1007/s10928-024-09920-z)  
  Uses time-scale calculus to unify continuous elimination with discrete dosing events in multi-dose PK models. It is functionally equivalent to jump-map dosing in an impulsive framework, but formulated in a continuous–discrete unification language.

- Wu, F., Piotrowska, M. J., & Capuani, F. (2020). *Introduction to dynamical systems analysis in quantitative systems pharmacology: basic concepts and applications*. *Translational and Clinical Pharmacology*, 28(4), 149–159. [Link](https://pmc.ncbi.nlm.nih.gov/articles/PMC7533163/)  
  A useful bridge between dynamical-systems theory and QSP practice. It supports the broader claim that dynamical-systems methods belong naturally inside QSP workflows, even when the models are not yet treated explicitly as hybrid systems.

- Milberg, O., Gong, C., Jafarnejad, M., et al. (2021). *Quantitative Systems Pharmacology Approaches for Immuno-Oncology: Adding Virtual Patients to the Development Paradigm*. *Clinical Pharmacology & Therapeutics*, 109(3), 605–618. [Link](https://pmc.ncbi.nlm.nih.gov/articles/PMC7983940/)  
  A strong open-access QSP review focused on immuno-oncology. It is useful for situating mechanistic and hybrid workflows within the broader model-informed drug-development landscape.

- Moutik, H., Metrane, A., & Rachik, M. (2022). *Recent applications of quantitative systems pharmacology and machine learning models in drug development*. *Frontiers in Pharmacology*, 12. [Link](https://pmc.ncbi.nlm.nih.gov/articles/PMC8528185/)  
  A recent review of QSP applications across therapeutic areas, with particular attention to immuno-oncology and integration with machine learning. It is helpful for placing this repository in the broader current QSP landscape.

### Sensitivity, adjoint, and automatic differentiation

- Rackauckas, C., Nie, Q., et al. (2020). *Accelerated pharmacometrics with adaptive solvers and automatic differentiation in Pumas*. *bioRxiv* 2020.11.28.402297. [Link](https://doi.org/10.1101/2020.11.28.402297)  
  Demonstrates forward-mode automatic differentiation applied directly to NLME population PK/PD models in a production pharmacometrics platform built on Julia and DifferentialEquations.jl. It shows that AD-backed sensitivities are already entering PK/PD practice, albeit mainly in smooth ODE settings.

- Fröhlich, F., Kaltenbacher, B., Theis, F. J., & Hasenauer, J. (2017). *Scalable parameter estimation for large-scale ODE models of biochemical reaction networks*. *PLoS Computational Biology*, 13(1), e1005331. [Link](https://doi.org/10.1371/journal.pcbi.1005331)  
  Implements continuous adjoint sensitivity analysis for large biochemical ODE systems. While the domain is systems biology rather than QSP/PK/PD, the methodology and tooling (AMICI) are directly relevant to large mechanistic pharmacology models.

- Stapor, P., Fröhlich, F., & Hasenauer, J. (2017). *Optimization of ODE models using the adjoint-state method and automatic differentiation*. *Bioinformatics*, 33(7), 1049–1056. [Link](https://doi.org/10.1093/bioinformatics/btx676)  
  Implements forward sensitivity (variational) equations with correct jump conditions at events, providing exactly the sensitivity jump formulas needed for dosing events. The test cases are systems biology models, but the techniques apply directly to event-rich pharmacological ODEs.

- Rackauckas, C., Irurzun-Arana, I., McDonald, T., & Trocóniz, I. (2020). *Differential equations and pharmacometrics: recent developments and future directions*. *Trends in Pharmacological Sciences*, 41(11), 882–895. [Link](https://doi.org/10.1016/j.tips.2020.09.005)  
  A conceptual review that discusses adjoint methods, stochastic simulation, and scientific machine learning for PK/PD. It does not implement adjoint sensitivity in a pharmacological model but helps frame where hybrid-ds-julia fits in future PK/PD tooling.

### SDE / stochastic methods

- Baili, A. (2022). *Hybrid stochastic differential systems in pharmacokinetics*. *IMA Journal of Mathematical Control and Information*, 39(1), 22–53. [Link](https://academic.oup.com/imamci/article-abstract/39/1/22/6454652)  
  A strong PK-side reference because it explicitly formulates pharmacokinetic dynamics as a hybrid stochastic differential system with predictable and spontaneous jumps. Although stochastic rather than deterministic, it shows that hybrid formulations are actively being developed for pharmacokinetic problems.

- Rackauckas, C., Irurzun-Arana, I., McDonald, T., & Trocóniz, I. (2020). *Differential equations and pharmacometrics: recent developments and future directions*. *Trends in Pharmacological Sciences*, 41(11), 882–895. [Link](https://doi.org/10.1016/j.tips.2020.09.005)  
  A useful overview of how stochastic differential equations, stochastic simulation algorithms, and related modern differential-equation methods are entering pharmacometrics. It is especially relevant for positioning future hybrid-ds-julia work relative to broader PK/PD numerical-methods development.

- Oduola, W., & Li, X. (2018). *Multiscale Tumor Modeling With Drug Pharmacokinetic/Pharmacodynamic Information Using Stochastic Hybrid Systems*. *Cancer Informatics*, 17. [Link](https://pmc.ncbi.nlm.nih.gov/articles/PMC6073835/)  
  Although not an impulsive-DE or Filippov paper, it is still useful as an example of stochastic hybrid modeling in a pharmacological cancer setting. It helps mark the boundary between architectural “hybrid” modeling and the more formal event-aware numerical methods targeted by this repository.

### Mechanistic crop models and trait optimization

- Dodd, A. N., Tindall, M. J., Massawe, F., et al. (2023). *A multiscale mathematical model describing the growth and development of bambara groundnut*. *Journal of Theoretical Biology*, 560. [Link](https://pubmed.ncbi.nlm.nih.gov/36509139/)  
  A major conceptual motivation for this project. It shows how changing interaction structure in a multiscale biological model can create hybrid or piecewise-smooth behavior even outside the usual engineering examples.

- Azam-Ali, S. N., Sesay, A, Karikari, S. K., Massawe, F. J., Aguilar-Manjarrez, J., Bannayan, M., & Hampson, K. J. (2001). *Assessing the potential of an underutilized crop — a case study using bambara groundnut*. *Experimental Agriculture*, 37(4), 433–472. [Link](https://www.fao.org/4/y0494e/y0494e05.htm)  
  A broader agronomic and modeling reference for bambara groundnut. It helps situate the crop-science side of the project in a larger mechanistic and applied context.

- Karunaratne, A. S., Hoogenboom, G., & Boote, K. J. (2024). *Adapting the CROPGRO model to simulate growth, development, and yield of Bambara groundnut (Vigna subterranea L. Verdc), an underutilized crop*. *European Journal of Agronomy*, 160, 127347. [Link](https://www.sciencedirect.com/science/article/abs/pii/S1161030124002004)  
  A recent crop-modeling paper showing continued interest in mechanistic and multiscale modeling for bambara groundnut. It is useful for seeing how crop-system modeling remains an active applied-math domain.