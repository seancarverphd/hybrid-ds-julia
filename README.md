# hybrid-ds-julia

*A Julia package under development for event-aware simulation, variational equations, multiple shooting, and automatic differentiation in mechanistic models with dosing events, thresholds, switching logic, and other hybrid structure.*

The main intended application area is **quantitative systems pharmacology (QSP) and PK/PD**, where mechanistic models are used to study dose and schedule optimization, relapse and remission dynamics, response heterogeneity, and translational decision-making.

Many pharmacology models are treated numerically as if hybrid structure were only a minor implementation detail, even though the scientifically important behavior often depends on **event-driven changes** in treatment logic or biological regime. Dosing pulses, treatment holidays, toxicity holds, rescue interventions, threshold-mediated responses, and therapy switches all create the kind of hybrid structure for which dynamical-systems methods are especially useful.

This project aims to make those methods more usable in domain-facing workflows. The goal is not to rebuild low-level solver infrastructure from scratch, but to build a practical layer on top of Julia’s scientific-computing ecosystem for models whose trajectories cross many events and decision boundaries.

## At a glance

- **Domain focus:** QSP, PK/PD, and mechanistic pharmacology models with dosing events, thresholds, switching rules, and other hybrid structure.
- **Method focus:** automatic differentiation, variational equations, multiple shooting, and event-aware simulation for piecewise-smooth and impulsive systems.
- **Initial technical target:** AD-backed sensitivities for impulsive treatment models in the spirit of Pang et al.
- **Later extension:** Filippov systems with discontinuous vector fields and possible sliding dynamics on switching surfaces.

## Why this project

This repository sits at the interface of **mechanistic pharmacology**, **QSP**, **PK/PD**, and **hybrid dynamical systems**.

The motivating use cases are:

- **Treatment-schedule dependence** — comparing regimens, continuing solutions across timing and dose parameters, and understanding when small changes in regimen logic produce large changes in long-term outcome.
- **Optimization, fitting, and model comparison** — using event-aware sensitivities and multiple shooting when models contain impulses, event surfaces, or threshold-triggered changes.
- **Mechanism differentiation and SAR** — connecting compound-level differences not only to potency and exposure, but also to the qualitative treatment regimes they induce under realistic intervention logic.
- **Translational decision support** — embedding biomarker thresholds, toxicity triggers, and regimen rules explicitly in the model so outputs speak more directly to robust schedule design and clinically meaningful regime changes.

The broader aim is to make hybrid dynamical-systems workflows directly usable in pharmacology and QSP settings where mechanistic models are already valued, but where event-aware numerical methods are still not standard practice.

## Why QSP and PK/PD first

QSP and PK/PD are the main intended application areas because they already rely heavily on mechanistic ODE models and are tied to questions pharmacology actually cares about.

Representative examples include:

- Immuno-oncology models with pulsed dosing and immune-response events.
- Autoimmune and inflammatory disease models with flare-remission dynamics, tapering, and rescue therapy.
- PK/PD models with treatment switching, toxicity holds, or state-triggered interventions.

These are exactly the kinds of systems in which trajectories may evolve on smooth segments while treatment logic introduces events, jumps, resets, or changes in the active dynamics. That structure motivates event-aware simulation, variational sensitivity propagation, multiple shooting, and automatic differentiation.

For that reason, the repository begins with the kinds of hybrid structure that are common in pharmacology — pulses, thresholds, switching, and event-triggered updates — and only later moves to more specialized discontinuous systems such as Filippov models.

## Motivation

This project grew out of the observation that variational equations, multiple shooting, and automatic differentiation for event-driven models remain underused in several mechanistic fields, including pharmacology, crop science, and precision agriculture.

These methods were part of doctoral training in dynamical systems at Cornell, including work with John Guckenheimer on hybrid dynamical systems. That background motivates the package at a methodological level: the aim is to bring tools that are standard in some parts of dynamical systems closer to scientific domains where mechanistic models are common but hybrid workflows are still comparatively rare.

Work inspired by Dodd et al. reinforced the broader point that methods which feel standard in one mathematical community are often not standard in nearby application domains. That insight helped motivate the move toward QSP and PK/PD, where mechanistic models increasingly matter for model-informed development, but where models with impulses, treatment thresholds, and other non-smooth features still need stronger hybrid-system workflows than are commonly available in domain-facing software.

## Original crop-science motivation

The immediate technical motivation came from the multiscale bambara groundnut model of Dodd et al., which couples plant-level nonlinear ODEs to canopy-level interaction structure. When the active interaction structure is fixed, the system evolves smoothly; when a new interaction becomes active, growth rates can change abruptly. That makes the full model a natural example of hybrid structure rather than a single uniform smooth system.

The analogy to pharmacology is direct: canopy occlusion changes local growth rates in much the same way that dosing rules, toxicity thresholds, or therapy switches change effective dynamics in QSP and PK/PD models. Different scientific domain, same underlying mathematical issue — event-triggered changes in structure.

That history matters because it shows that the package is not motivated by a narrow domain pivot alone. The underlying goal is to support mechanistic models whose scientifically meaningful behavior depends on hybrid structure, regardless of whether the application begins in crop science, ecology, pharmacology, or biomedicine.

## Mathematical viewpoint

A typical mechanistic model is treated as piecewise smooth:

```text
dx/dt = f_k(x, t),   t in [t_k, t_{k+1})
```

where `k` labels the currently active interaction or control regime.

Whenever the system encounters an event — for example, a dosing time, a toxicity threshold, or the activation of a new interaction term — the active vector field may change, or the state may be updated by a jump map. This places the model in the general class of **hybrid dynamical systems**, where continuous evolution is punctuated by discrete structural changes.

### Variational equations

Let `n` denote the dimension of the original state vector. To obtain well-conditioned sensitivities, the package is intended to evolve both the state `x(t)` and the Jacobian of the flow.

Along each smooth segment, the Jacobian of the flow `J(t) = ∂x(t) / ∂x(t_k)` satisfies

```text
dJ/dt = (D_x f_k)(x(t), t) * J(t),   with   J(t_k) = I
```

where `D_x f_k` denotes the Jacobian of `f_k` with respect to the state.

This yields an augmented system of dimension `n + n^2`: the original `n` equations together with the `n^2` variational equations. The point is to propagate local sensitivities in a way that respects event-driven structure.

### Multiple shooting

Given a sequence of event times or event surfaces, the full trajectory can be reformulated as a **multiple-shooting problem**:

- Integrate the model separately on each smooth segment.
- Use the variational equations to compute the Jacobian of each segment map.
- Use a Newton-type solver to adjust the segment start points so that the end of each segment matches the beginning of the next, enforcing a single continuous trajectory across all segments.

This often yields a better-conditioned trajectory and sensitivity framework than naive single shooting when the model contains many event-driven structural changes.

### Automatic differentiation

Automatic differentiation is central to the package vision because it provides a practical way to compute vector-field Jacobians, jump-map Jacobians, and gradients of scalar objectives without fragile finite-difference approximations.

For scalar objectives depending on many parameters, reverse-mode differentiation is often the more scalable choice. In that sense, part of the package vision is analogous to backpropagation in machine learning: propagate information forward through hybrid trajectories, then propagate gradients backward through both continuous flow segments and event maps.

## Pang-type treatment models

A useful reference point for this project is Pang et al. (2016), who studied low-dimensional tumor-treatment models with pulsed immunotherapy and chemotherapy.

Their contribution was to show that regimen timing, drug half-life, minimum effective concentration, and resistance mechanisms can be analyzed directly in a hybrid treatment framework, yielding explicit qualitative conditions for tumor elimination or persistence. This makes the paper a strong conceptual bridge between classical analytical modeling and the computational workflow envisioned here.

`hybrid-ds-julia` is intended to extend that line of work in directions that are difficult to handle analytically: larger mechanistic models, event-rich treatment logic, state-triggered interventions, toxicity holds, adaptive schedules, and parameter- or schedule-optimization problems.

In those settings, event-aware simulation needs to be paired with variational equations, automatic differentiation, and multiple shooting to obtain stable sensitivities, fit parameters, continue solutions across changing regimens, and optimize treatment rules in the presence of many events and jumps.

### Why jump-aware methods are needed

The relevant hybrid structure is not limited to discontinuities in the derivatives. In pulsed treatment models, the system often contains **jumps in the flow itself**: the state evolves continuously between interventions, but is reset instantaneously at dosing times.

Computationally, this does not require a different conceptual framework from the one used for piecewise-smooth systems. It requires an event-aware formulation in which continuous segments are integrated normally, events are located accurately, and the state is updated by an explicit jump map before integration resumes.

For that reason, the same core methods — variational equations, multiple shooting, and automatic differentiation — still apply. The essential requirement is that the hybrid model expose both pieces of its dynamics: the smooth vector field governing each continuous segment and the jump map governing each discrete update. The continuous part contributes the usual flow Jacobian; the jump contributes its own Jacobian, which must also be propagated if one wants correct sensitivities, stable shooting conditions, or gradient-based optimization in the presence of repeated events.

If a jump is written as \(x^{+} = G(x^{-}, p)\), then the solver must propagate derivatives through both the continuous flow and the map \(G\). This means representing not only the jump itself but also its Jacobian with respect to state and parameters. In realistic extensions of Pang-type models, maintaining those derivatives by hand quickly becomes brittle. Automatic differentiation provides a natural way to compute these jump Jacobians accurately and consistently, which is one reason the methods implemented in `hybrid-ds-julia` are necessary for extending analytically tractable impulsive models into larger, event-rich QSP and PK/PD workflows.

## Example applications

The same mathematical and computational ideas can be used across a range of mechanistic modeling problems.

### QSP and PK/PD

Many QSP and PK/PD models already contain hybrid structure in practice. A package like `hybrid-ds-julia` is intended to make event-aware simulation, variational sensitivity propagation, multiple shooting, and reverse-mode gradient workflows natural parts of the modeling stack.

That would make it easier to study not only how strongly a drug acts, but how the timing and logic of interventions shape long-term outcomes such as remission, relapse, resistance, or sustained control. It also opens the door to more systematic optimization over dose, timing, and treatment rules rather than relying only on hand-picked regimen comparisons.

### Mechanistic pharmacology and translational strategy

Many of the most important translational questions are inherently dynamical: whether a schedule sustains control, whether biomarker trajectories indicate a regime shift, or whether a mechanism remains effective under realistic interruptions or patient heterogeneity.

`hybrid-ds-julia` is intended to support this layer by making it easier to represent treatment logic, biomarker thresholds, and intervention schedules explicitly inside mechanistic models. That can help identify which strategies are robust, which are fragile, and which biological hypotheses are most consistent with clinically relevant patterns of response.

### SAR progression and mechanism differentiation

SAR studies are central to hit-to-lead and lead optimization, but the link between SAR and downstream dynamical treatment behavior is often indirect.

A hybrid dynamical-systems workflow could help close that gap by mapping compound-level differences into model parameters and then studying how those differences alter qualitative treatment regimes under realistic regimens. In that setting, mechanism differentiation becomes more than comparing endpoint potency: it becomes possible to ask which mechanism or chemotype yields a wider and more robust therapeutic regime.

### Autoimmune and inflammatory disease

Autoimmune and inflammatory diseases are another promising domain because their trajectories often involve flares, remission, tapering, rescue therapy, and long periods of partial control. These state changes are biologically and clinically important, and they are often driven by interventions or thresholds that make the system effectively hybrid even when the underlying biological model is written as an ODE.

A hybrid dynamical-systems workflow would allow these disease trajectories to be analyzed in terms of regime changes and event timing. In practical terms, that could support better tapering strategies, more informative biomarker interpretation, and more systematic comparison of regimens intended to maintain remission while minimizing drug burden.

### Crop science and precision agriculture

Although the primary intended destination of the package is pharmacology, the original motivating example came from crop science. That example remains useful because it illustrates a broader point: hybrid structure appears in scientifically important mechanistic models well beyond the traditional hybrid-systems canon.

Crop science is therefore not the main target for the package, but it remains an instructive example of why such a package could be useful.

## Later Filippov and sliding dynamics

Although the package is motivated first by impulsive and event-driven QSP/PK/PD models, a later extension is to Filippov systems, where the vector field is discontinuous across a switching surface and trajectories may slide along that surface when the flows on both sides point toward it.

This kind of phenomenon is different from a simple event-triggered jump. In impulsive models, an event surface detects a dosing time or threshold crossing and then triggers a discrete update. In Filippov systems, the switching surface can become part of the continuous evolution itself, because the dynamics on both sides constrain the trajectory to remain on that surface for a nonzero time interval.

Representative biological examples include:

- **Predator–prey and pest-management models** with threshold harvesting, refuge activation, or control policies that switch when prey or predator density crosses a management threshold.
- **Plant-disease control models** in which cutting or replanting policies switch on and off when infected or susceptible populations cross intervention thresholds, producing Filippov dynamics and possible sliding behavior on the control boundary.
- More generally, ecological or epidemiological systems with rapid threshold-based intervention logic, where repeated switching in the idealized limit is represented mathematically by sliding on the switching manifold.

These models matter here for two reasons. First, they show that Filippov phenomena are not merely abstract dynamical-systems curiosities; they arise naturally when biological or management rules are represented as sharp threshold policies. Second, they provide a stringent computational test of the package beyond impulsive treatment models, because they require accurate handling of switching surfaces, crossing and sliding regions, and bifurcations specific to discontinuous vector fields.

For that reason, a Filippov benchmark is best treated as an advanced milestone. It extends the package from event-aware simulation of impulsive and piecewise-smooth biomedical models to the more demanding setting of discontinuous differential systems, where sliding dynamics, pseudo-equilibria, and discontinuity-induced bifurcations must be handled explicitly.

## Software plan

Planned implementation details include:

- **Language:** Julia.
- **ODE integration and sensitivity infrastructure:** SciML / `DifferentialEquations.jl` and related tools.
- **Boundary-value and shooting infrastructure:** `BoundaryValueDiffEq.jl` and related shooting workflows.
- **Automatic differentiation:** reverse-mode or adjoint-oriented approaches are likely to be most useful for parameter-rich problems; `ReverseDiff.jl` is a natural candidate.
- **Optimization:** `Optimization.jl`, `Optim.jl`, `NLopt.jl`, or custom Newton-style solvers.

Related Julia ecosystem tools:

- [`DifferentialEquations.jl`](https://github.com/SciML/DifferentialEquations.jl)
- [`BoundaryValueDiffEq.jl`](https://github.com/SciML/BoundaryValueDiffEq.jl)
- [`BifurcationKit.jl`](https://github.com/bifurcationkit/BifurcationKit.jl)
- [`DynamicalSystems.jl`](https://github.com/JuliaDynamics/DynamicalSystems.jl)
- [`ReverseDiff.jl`](https://github.com/JuliaDiff/ReverseDiff.jl)
- [`Optimization.jl`](https://github.com/SciML/Optimization.jl)

## Status and roadmap

This project is currently in the **early design and implementation** phase, with a roadmap aimed at pharmacology-relevant proof-of-concept workflows.

Current work is focused on setting up AD-backed Jacobians and a simple Pang-style impulsive model to exercise the automatic-differentiation, variational-equation, and event-handling pipeline.

Near-term milestones:

- [ ] Build a minimal Julia package skeleton, including module structure, dependencies, and tests.
- [ ] Integrate automatic differentiation for vector-field Jacobians, jump-map Jacobians, and objective gradients.
- [ ] Implement variational-equation propagation for piecewise-smooth and impulsive models, including sensitivity updates across jump maps.
- [ ] Implement multiple-shooting support across event-defined segments, including segments separated by explicit state jumps.
- [ ] Validate the workflow on a low-dimensional pulsed tumor-treatment model motivated by Pang et al.
- [ ] Demonstrate a pharmacology-relevant hybrid workflow focused on schedule dependence and robustness to treatment timing.
- [ ] Extend the workflow to an autoimmune or inflammatory disease example with flare/remission dynamics, tapering rules, or rescue therapy represented explicitly as event structure.
- [ ] Add a Filippov benchmark as an advanced nonsmooth testbed for crossing, sliding, pseudo-equilibria, and discontinuity-induced bifurcations.

## Licensing and IP posture

This repository is currently marked **All rights reserved**. In practical terms, that means the code is not yet licensed for reuse or redistribution; it is shared to illustrate ongoing work rather than as a finished open-source product.

That posture is provisional rather than permanent. Long-term licensing will depend on future collaborators or an employer and may eventually move toward an open-source model.

## Further reading

### Core dynamical systems and hybrid methods

- Guckenheimer, J., & Holmes, P. (1983). *Nonlinear Oscillations, Dynamical Systems, and Bifurcations of Vector Fields*. Springer. [Link](https://www.semanticscholar.org/paper/Nonlinear-Oscillations,-Dynamical-Systems,-and-of-Guckenheimer-Holmes/70e3da6c426ca384f78fa782f0d7f8ec344be7c3)  
  A classic reference for geometric dynamical systems, periodic orbits, variational ideas, and bifurcations. It provides much of the mathematical background that motivates the methodology behind this project.

- Kuznetsov, Y. A., Rinaldi, S., & Gragnani, A. (2003). *One-parameter bifurcations in planar Filippov systems*. *International Journal of Bifurcation and Chaos*. [Link](https://pure.iiasa.ac.at/id/eprint/6817/)  
  A foundational paper on codimension-one bifurcations in planar Filippov systems. It is especially useful here because it organizes the local and global bifurcation picture in a way that supports computational test problems.

- Di Bernardo, M., Pagano, D. J., & Ponce, E. (2008). *Bifurcations in planar Filippov systems: a case study approach*. [Link](https://ddd.uab.cat/pub/prepub/2007/hdl_2072_4693/Pr748.pdf)  
  A concrete and example-driven treatment of bifurcation structure in planar Filippov systems. It works well as a companion to the Kuznetsov–Rinaldi–Gragnani paper when building intuition for piecewise-smooth phenomena.

- Glendinning, P. (2016). *Classification of boundary equilibrium bifurcations in planar Filippov systems*. *Chaos*, 26(1), 013108. [Link](https://pubmed.ncbi.nlm.nih.gov/26826860/)  
  A focused treatment of boundary equilibrium bifurcations, which are central when equilibria collide with switching manifolds. This is especially relevant for threshold-based biological or control models.

- Castillo, J., Llibre, J., & Verduzco, F. (2017). *The pseudo-Hopf bifurcation for planar discontinuous piecewise linear differential systems*. *Nonlinear Dynamics*, 90, 1829–1840. [Link](https://doi.org/10.1007/s11071-017-3766-9)  
  A useful reference for pseudo-Hopf behavior in planar discontinuous systems. It is relevant when choosing a low-dimensional Filippov benchmark for testing continuation and cycle-detection ideas.

- Li, C., Qian, H., Yang, J., & Dougherty, E. R. (2012). *Dynamical Modeling of Drug Effect Using Hybrid Systems*. *EURASIP Journal on Bioinformatics and Systems Biology*. [Link](https://pmc.ncbi.nlm.nih.gov/articles/PMC3639233/)  
  A clear example of hybrid-systems thinking applied directly to pharmacology. It helps connect abstract hybrid dynamical-systems ideas to drug-effect modeling in a biomedical setting.

- Belta, C., Habets, L. C. G. J. M., Kumar, V., Mink, A., & Weiss, R. (2013). *Disease processes as hybrid dynamical systems*. [Link](https://arxiv.org/pdf/1208.3858.pdf)  
  A broad conceptual framing of disease progression and treatment as a hybrid dynamical process. It is useful here because it shows that hybrid-system language is not limited to engineering examples and can be applied naturally to biomedical processes.

### QSP and PK/PD directions

- Pang, L., Shen, L., & Zhao, Z. (2016). *Mathematical Modelling and Analysis of the Tumor Treatment Regimens with Pulsed Immunotherapy and Chemotherapy*. *Computational and Mathematical Methods in Medicine*. [Link](https://pmc.ncbi.nlm.nih.gov/articles/PMC4779848/)  
  A central motivation for this repository. The paper studies pulsed immunotherapy and chemotherapy in a low-dimensional hybrid treatment setting and shows how regimen timing, minimum effective concentration, drug half-life, and resistance can shape tumor-control outcomes.

- Li, J., Xu, Y., Feng, X., & Li, J. (2021). *Analysis of a Hybrid Impulsive Tumor-Immune Model with Immunotherapy and Chemotherapy*. *Chaos, Solitons & Fractals*, 145, 110772. [Link](https://www.sciencedirect.com/science/article/abs/pii/S0960077920310080)  
  A more explicitly impulsive tumor–immune treatment model that is useful as a later biomedical target. It strengthens the case for event-aware numerical methods in treatment-scheduling problems.

- Milberg, O., Gong, C., Jafarnejad, M., et al. (2020). *Quantitative Systems Pharmacology Approaches for Immuno-Oncology: Adding Virtual Patients to the Development Paradigm*. *Clinical Pharmacology & Therapeutics*, 109(3), 605–618. [Link](https://pmc.ncbi.nlm.nih.gov/articles/PMC7983940/)  
  A strong open-access QSP review focused on immuno-oncology. It is useful for situating mechanistic and hybrid workflows within the broader model-informed drug-development landscape.

- Stamatakos, G. S., Kolokotroni, E. A., Dionysiou, D. D., & Georgiadi, E. C. (2018). *Multiscale Tumor Modeling With Drug Pharmacokinetic/Pharmacodynamic Information Using Stochastic Hybrid Systems*. *Cancer Informatics*. [Link](https://journals.sagepub.com/doi/abs/10.1177/1176935118790262)  
  A hybrid modeling example that explicitly links tumor dynamics with PK/PD information. It is useful for seeing how hybrid mathematical structure enters multiscale biomedical modeling.

- Moutik, H., Metrane, A., & Rachik, M. (2022). *Recent applications of quantitative systems pharmacology and machine learning models in drug development*. *Frontiers in Pharmacology*, 12. [Link](https://pmc.ncbi.nlm.nih.gov/articles/PMC8528185/)  
  A recent review of QSP applications across therapeutic areas, with particular attention to immuno-oncology and integration with machine learning. It is helpful for placing this repository in the broader current QSP landscape.

### Crop and multiscale motivation

- Dodd, A. N., Tindall, M. J., Massawe, F., et al. (2023). *A multiscale mathematical model describing the growth and development of bambara groundnut*. *Journal of Theoretical Biology*, 560. [Link](https://pubmed.ncbi.nlm.nih.gov/36509139/)  
  A major conceptual motivation for this project. It shows how changing interaction structure in a multiscale biological model can create hybrid or piecewise-smooth behavior even outside the usual engineering examples.

- Azam-Ali, S. N., Sesay, A., Karikari, S. K., Massawe, F. J., Aguilar-Manjarrez, J., Bannayan, M., & Hampson, K. J. (2001). *Assessing the potential of an underutilized crop — a case study using bambara groundnut*. *Experimental Agriculture*, 37(4), 433–472. [Link](https://www.fao.org/4/y0494e/y0494e05.htm)  
  A broader agronomic and modeling reference for bambara groundnut. It helps situate the crop-science side of the project in a larger mechanistic and applied context.

- Karunaratne, A. S., Hoogenboom, G., & Boote, K. J. (2024). *Adapting the CROPGRO model to simulate growth, development, and yield of Bambara groundnut (Vigna subterranea L. Verdc), an underutilized crop*. *European Journal of Agronomy*, 160, 127347. [Link](https://www.sciencedirect.com/science/article/abs/pii/S1161030124002004)  
  A recent crop-modeling paper showing continued interest in mechanistic and multiscale modeling for bambara groundnut. It is useful for seeing how crop-system modeling remains an active applied-math domain.

### Biological Filippov examples

- Kuznetsov, Y. A., Rinaldi, S., & Gragnani, A. (2003). *One-parameter bifurcations in planar Filippov systems*. *International Journal of Bifurcation and Chaos*. [Link](https://pure.iiasa.ac.at/id/eprint/6817/)  
  This paper also serves as a biological application example because it includes a predator–prey exploitation problem. That makes it especially helpful for linking abstract Filippov bifurcation theory to ecological threshold-policy models.

- Glendinning, P. (2016). *Classification of boundary equilibrium bifurcations in planar Filippov systems*. *Chaos*, 26(1), 013108. [Link](https://pubmed.ncbi.nlm.nih.gov/26826860/)  
  This paper is particularly relevant when a biological or control threshold causes an equilibrium to collide with a switching boundary. That mechanism appears naturally in policy-based ecological and biomedical switching models.

- Castillo, J., Llibre, J., & Verduzco, F. (2017). *The pseudo-Hopf bifurcation for planar discontinuous piecewise linear differential systems*. *Nonlinear Dynamics*, 90, 1829–1840. [Link](https://doi.org/10.1007/s11071-017-3766-9)  
  A useful benchmark-style paper for testing crossing cycles and bifurcation computations in nonsmooth planar systems. It is especially relevant if the package later includes continuation or cycle-location tools for Filippov models.