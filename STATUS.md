# Project status

**Last updated:** 2026-09-14

## Current stage

`hybrid-ds-julia` is a research-design project in the **pre-prototype** stage.

The repository currently contains technical documentation, mathematical
formulations, proposed benchmark directions, reading notes, and an
implementation roadmap. It does not yet contain a runnable Julia/SciML QSP or
PK/PD implementation, a published numerical benchmark result, or a validated
hybrid variational sensitivity workflow.

The immediate purpose of the project is to define analytically verifiable
hybrid benchmark cases and obtain informed technical feedback before investing
in a larger software abstraction. The project is intended to evaluate and build
on existing Julia/SciML, `HybridSystems.jl`, JuliaReach, and pharmacometrics
capabilities where appropriate—not to assume that existing infrastructure must
be replaced.

## Available now

The repository currently provides:

- A mathematical vocabulary for continuous states \(x(t)\), discrete modes
  \(q(t)\), directed transitions \(e=(q^-,q^+)\), scheduled transitions,
  state-triggered guards, reset maps, mode-dependent continuous inputs, and
  reproducible event logs;
- A hybrid variational framing based on smooth-segment variational equations
  and saltation-style event-transition derivatives at suitable transversal
  events;
- A proposed benchmark ladder that separates analytic verification from later
  application-motivated demonstrations;
- A treatment-protocol example involving scheduled dosing, mode-dependent
  treatment status, toxicity-triggered holds, and recovery-triggered restarts;
- A validation-oriented account of event-time sensitivity, event order,
  transversality, and grazing; and
- Background research notes, application hypotheses, references, and
  longer-term questions.

## Not yet implemented

The repository does **not** yet provide:

- Julia source code for a hybrid QSP, PK/PD, physiology, or tumor–immune model;
- A `Project.toml` environment for a reproducible Julia implementation;
- A tested SciML simulation using scheduled and state-triggered transitions;
- An implementation of smooth variational equations, a saltation matrix, or an
  equivalent event-transition derivative;
- A verified comparison with an independently derived analytic hybrid
  sensitivity;
- An event-structured multiple-shooting implementation connecting smooth
  segments through guard, reset, and mode-transition constraints;
- A verified assessment of how existing SciML event handling, sensitivity
  methods, and multiple-shooting tools compose for the proposed workflow;
- Parameter estimation, uncertainty quantification, hybrid optimization, or
  policy-analysis workflows;
- A package API, release, or stable interface; or
- Validation against experimental, clinical, or pharmacometrics reference data.

## Next implementation milestones

### Milestone 1: exact scheduled-transition benchmark

Implement a small Julia/SciML model with prescribed event times, closed-form
continuous flow, explicit reset semantics, and analytic state and sensitivity
results.

This benchmark will test:

- Scheduled-event conventions;
- Pre-event and post-event state conventions;
- Repeated reset handling;
- Event-log structure;
- Smooth variational propagation; and
- Exact parameter and initial-condition sensitivities.

A useful source structure is a scalar impulsive PK or treatment model with
exponential flow between prescribed impulses. This is a fixed-time transition
test; it does not by itself validate state-triggered event-time sensitivity.

### Milestone 2: exact state-triggered hybrid benchmark

Implement a deliberately low-dimensional hybrid system with:

1. A continuous state and mode-dependent vector field;
2. A transversal state-triggered guard;
3. An explicitly specified edge
  ```math
   e=(q^-,q^+);
   ```
4. A reset map
  ```math
   x^+
   =
   R_e(x^-,q^-,\tau_e,\theta);
  ```
5. Analytically known event time and event-time derivative;
6. Analytically known post-event flow; and
7. An analytic derivative of a terminal state or scalar output.

The central comparison will be between the computed hybrid variational result
and an independently derived analytic derivative, accurate to the documented
scale of floating-point arithmetic, ODE integration, and root localization.

### Milestone 3: finite-difference limitation study

For the exact state-triggered benchmark, perform a finite-difference
step-size sweep only as a controlled diagnostic.

Its purpose is to illustrate that a perturbation must be both:

```math
\text{large enough to overcome numerical error}
```

and

```math
\text{small enough to preserve event existence, event branch, event order,
reset sequence, and mode sequence}.
```

In hybrid systems, that usable interval may be absent. Finite differences are
not the primary sensitivity method or the validation oracle.

### Milestone 4: synthetic treatment-protocol demonstration

Extend the validated workflow to a synthetic QSP/PK/PD-style model with:

1. A PK amount state, pharmacodynamic or biological states, and an illustrative
   toxicity or safety-burden state;
2. Scheduled repeated dosing or a mode-dependent continuous infusion input;
3. A state-triggered treatment-hold transition;
4. A recovery-triggered restart transition;
5. Distinct hold and restart thresholds to create hysteresis;
6. Explicit transition-enabling and rearming rules;
7. A structured event log recording administered and withheld doses, holds,
   restarts, and mode changes; and
8. Clearly documented transition priorities, pre-event/post-event conventions,
   solver settings, and numerical limitations.

This milestone is a synthetic methodological demonstration. It is not intended
to fit patient data, recommend treatment, establish a biological mechanism, or
claim clinical validation.

## Evidence standard for later claims

A capability will be described as implemented only when the repository
contains:

- Reproducible code;
- A documented Julia environment and dependency specification;
- A stated mathematical model and event convention;
- A minimal test or verification procedure;
- Relevant solver, root-finding, and numerical-tolerance settings;
- A statement of the modeling and event-structure conditions under which the
  capability has been evaluated; and
- A distinction between analytic verification, numerical demonstration, and
  application-motivated illustration.

Claims about hybrid sensitivity behavior should distinguish at least the
following regimes:

- Transversal guard crossings with a locally unchanged event sequence;
- Near-grazing crossings, where event times and transition derivatives may be
  poorly conditioned;
- Parameter or initial-condition perturbations that create, remove, or reorder
  events;
- Transitions with state resets versus identity resets that change only a mode
  or mode-dependent input; and
- Settings in which an ordinary smooth derivative is not the appropriate
  mathematical object.

## Licensing

Licensing is under review. No license is granted at this stage
