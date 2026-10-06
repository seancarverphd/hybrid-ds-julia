# hybrid-ds-julia

## Planned paper: gradient-based optimization of chemotherapy and immunotherapy

This project applies established hybrid dynamical-systems methods to
gradient-based optimization of pulsed chemotherapy and immunotherapy in
published tumor–immune models.

The first planned paper will extend the treatment-regimen analyses of Pang,
Shen, and Zhao (2016) and Zhao, Pang, and Li (2021). Rather than relying only
on selected-regimen comparisons and parameter sweeps, the project will
formulate explicit treatment objectives and compute their gradients,
including the effects of parameter-dependent intervention times.

The contribution is an extension of the computational analysis of these
models. It does not require introducing new biological mechanisms or
changing the published equations. Any changes to the model structure will
be identified separately from the optimization methodology.

**Current stage: research design / pre-prototype.**

The repository currently contains mathematical formulations, research notes,
and an implementation plan. It does not yet contain a runnable Julia
implementation, verified numerical optimization results, or a completed
paper.

See [STATUS-software.md](STATUS-software.md) for software implementation
status and [README-software.md](README-software.md) for the broader
computational design.

## Research objective and contribution

The published papers investigate how treatment amounts, timing, frequency,
and combinations affect tumor dynamics. They derive analytical conditions
for tumor elimination or tumor-free attractivity and use numerical
calculations to identify and compare treatment regimens.

The planned extension is to formulate explicit optimization problems for
selected models and solve them using verified objective-function gradients.

Writing the continuous treatment decision variables as θ, the intended
problem has the form

```math
\min_{\theta \in \Theta} J(\theta),
```

where J is a stated treatment objective and Θ specifies the admissible
decisions and constraints.

The final objective, optimization variables, treatment horizon, and
constraints remain to be selected. They will be defined explicitly rather
than inferred from visual comparisons of simulated trajectories.

The mathematical work supporting this optimization will account for:

- Continuous evolution between treatment events.
- The dependence of scheduled treatment times on decision variables.
- Treatment reset maps and their derivatives.
- The dependence of state-triggered intervention times on decision variables.
- The resulting effects on subsequent trajectories and the objective function.

The project builds on established hybrid-systems methods, including smooth
variational equations, event-time derivatives, saltation-style transition
derivatives, and multiple shooting where appropriate. It does not claim
these methods as new.

The intended first-paper contribution is their application, verification,
and use in treatment optimization for the selected published models.
Claims about novelty relative to the wider literature will require a
separate literature assessment.

## Published models

### Pang, Shen, and Zhao (2016)

*Mathematical Modelling and Analysis of the Tumor Treatment Regimens with
Pulsed Immunotherapy and Chemotherapy*

The basic model couples immune-cell and tumor-cell dynamics with a
chemotherapy drug-concentration state.

Immunotherapy adds cytotoxic T lymphocytes at scheduled treatment times.
Chemotherapy produces a scheduled increment in drug concentration, which
then decays continuously and affects both immune and tumor cells.

The paper investigates:

- Pulsed immunotherapy.
- Pulsed chemotherapy.
- Combined immunotherapy and chemotherapy.
- Chemotherapy with drug resistance.
- Two-drug combination chemotherapy.
- Immunotherapy combined with two-drug chemotherapy.

Its analytical results and numerical regimen comparisons provide starting
points for reproduction and optimization.

For example, the paper compares two-drug regimens with equal total
concentration increments but different allocations between drugs. This
provides a concrete question to revisit through an explicitly constrained
optimization problem, rather than only comparing the selected allocations.

The paper also contains scalar immune-cell and drug-concentration
subsystems with closed-form solutions. These provide useful verification
cases for scheduled-event simulation and sensitivity calculations.

The first paper will use a selected subset of this model family.
Implementing every resistance and combination-treatment variant is not a
prerequisite.

### Zhao, Pang, and Li (2021)

*Analysis of a hybrid impulsive tumor-immune model with immunotherapy and
chemotherapy*

This paper first studies chemotherapy and immunotherapy administered on
different schedules. Chemotherapy instantaneously reduces immune-cell and
tumor-cell populations, while immunotherapy adds immune cells.

The paper then introduces a state-feedback model combining:

- Immunotherapy administered at prescribed times.
- Chemotherapy administered when tumor biomass reaches a specified threshold.

In this model, chemotherapy timing is determined by the trajectory rather
than prescribed independently. Changing a treatment parameter or threshold
can therefore change when chemotherapy occurs.

This model provides the central state-triggered application for the planned
hybrid sensitivity and optimization work.

Its chemotherapy effects are represented by fractional reductions in cell
populations, not by an explicit drug-concentration state. These fractions
will be described as treatment-effect parameters unless an additional
dose–response relationship is introduced.

The published threshold model does not explicitly represent a toxicity
state or treatment-hold/restart mechanism. Such additions would be separate
model extensions, not part of reproducing the original model or necessary
to establish the first paper's optimization contribution.

## Computational approach and verification

### Gradients through treatment events

On continuous trajectory segments, sensitivities will be propagated using
the variational equations of the active vector field.

At scheduled interventions, the calculation will include reset derivatives
and, when treatment times depend on optimization variables, the corresponding
timing contributions.

At state-triggered interventions, it will include the derivative of the
implicitly defined intervention time and the appropriate derivative through
the reset and subsequent flow.

Automatic differentiation may be used to obtain derivatives of smooth
ingredients, such as vector fields, guards, and reset maps. It will not be
treated as a substitute for specifying and verifying the complete hybrid
derivative.

### Verification supporting optimization

Verification is supporting work for the paper's optimization objective,
not a substitute for that objective.

The planned verification sequence will distinguish:

1. Scheduled-event calculations checked against closed-form subsystem results.
2. State-triggered calculations checked against independently derived
   analytical event-time and output sensitivities in a tractable benchmark.
3. Application of the verified calculations to the nonlinear treatment models.
4. Evaluation of the resulting objective-function gradients and optimization
   outcomes under documented numerical settings.

Analytical reference formulas will be evaluated with attention to
floating-point error, ODE integration error, and event-localization error.

The full nonlinear tumor–immune models will not be treated as exact
sensitivity references merely because their trajectories can be simulated.

Finite-difference step-size sweeps may be included as controlled diagnostics
of numerical limitations. Finite differences will not be the primary
sensitivity method or the verification standard.

### Multiple shooting

Event-structured multiple shooting will be considered where it is needed
to support stable trajectory and gradient calculations.

The formulation will connect continuous trajectory segments through
explicit treatment events and their associated constraints and derivatives.

Multiple shooting will be used when justified by the selected problem,
rather than assumed necessary for every simulation or optimization example.

### Event structure and optimization limits

Gradient calculations will be evaluated under stated regularity assumptions,
including transversal state-triggered crossings and a locally unchanged
event sequence.

The implementation and analysis will identify cases in which a parameter
change:

- Creates or removes an intervention.
- Changes the order of interventions.
- Produces a near-grazing threshold crossing.
- Moves an intervention across the treatment horizon.
- Makes an ordinary smooth derivative inappropriate.

Integer treatment counts will not be treated as continuous gradient variables.
Where treatment count is a decision, it will require a separate discrete
comparison or a suitably formulated mixed discrete–continuous problem.

Numerical optimization results will be described according to the evidence
obtained. A converged gradient-based calculation will not, by itself, be
presented as proof of global optimality.

## First-paper plan, scope, and documentation

### Planned sequence

1. Select the published model variants and specify their parameters, initial
   conditions, and treatment-event conventions.
2. Implement the selected models and reproduce relevant analytical results
   and numerical examples.
3. Verify scheduled-event and state-triggered sensitivity calculations.
4. Define the treatment objective, continuous decision variables, admissible
   ranges, and constraints.
5. Implement and evaluate gradient-based optimization.
6. Compare the optimized regimens with selected reference regimens under the
   same objective and constraints.
7. Report reproducibility details, numerical conditioning, and limitations
   associated with event-structure changes.

Candidate decision variables include treatment amounts, treatment intervals
or times, and the tumor threshold triggering chemotherapy. Their precise
meaning will follow the selected model.

Published regimen comparisons and parameter sweeps remain useful as reference
cases and diagnostic tools. The extension is to supplement them with an
explicit optimization formulation and verified gradients—not to discard
them.

### Immediate scope

The first paper is a mathematical and computational study of selected
published treatment models.

It will not claim:

- Clinical validation.
- Patient-specific treatment recommendations.
- That a model-optimized regimen is an appropriate clinical dosing strategy.
- A new biological mechanism unless one is explicitly introduced and justified.
- A production-ready pharmacology software package.

Fitting models to data, learned residual models, population inference,
broader treatment-protocol extensions, and pharmacometrics interoperability
remain longer-term directions. They are not prerequisites for the first
paper.

The implementation will evaluate and reuse existing Julia/SciML capabilities
where appropriate. A new package-level abstraction is not assumed necessary;
the contribution may consist of reproducible model implementations,
verified sensitivity calculations, and optimization examples.

### Documentation

- [STATUS-software.md](STATUS-software.md): software implementation status,
  verification standards, and software-development milestones.
- [README-software.md](README-software.md): broader mathematical and software
  design, ecosystem context, and possible future directions.
- [README-extensive-original.md](README-extensive-original.md):
  preserved extensive research notes, literature context, and broader
  project directions.

### Model references

Pang, L., Shen, L., & Zhao, Z. (2016). Mathematical Modelling and Analysis
of the Tumor Treatment Regimens with Pulsed Immunotherapy and Chemotherapy.
*Computational and Mathematical Methods in Medicine*, 2016, Article 6260474.
DOI: 10.1155/2016/6260474.

Zhao, Z., Pang, L., & Li, Q. (2021). Analysis of a hybrid impulsive
tumor-immune model with immunotherapy and chemotherapy.
*Chaos, Solitons & Fractals*, 144, 110617.
DOI: 10.1016/j.chaos.2020.110617.