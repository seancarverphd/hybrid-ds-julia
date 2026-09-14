# hybrid-ds-julia *(working title)*

### Domain-facing hybrid systems for QSP and PK/PD

> **Status: research design / pre-prototype.**
>
> `hybrid-ds-julia` investigates how established hybrid-systems methods can be applied, analytically validated, and made reproducible for mechanistic quantitative systems pharmacology (QSP) and pharmacokinetic/pharmacodynamic (PK/PD) models with scheduled and state-triggered treatment interventions.
>
> The working title reflects the initial focus on hybrid dynamical systems in Julia. It may change as the project’s relationship to existing Julia packages and its eventual pharmacology-facing scope become clearer.
>
> The project does not claim to introduce hybrid dynamical systems, variational equations, saltation matrices, automatic differentiation, or multiple shooting as new methods. Its initial aim is narrower: construct analytically verifiable hybrid benchmarks and determine whether an event-aware Julia/SciML workflow can make established methods usable and transparent for QSP and PK/PD models.
>
> This repository currently contains a mathematical design, a proposed benchmark sequence, and research notes. It is not yet a runnable Julia package, a validated sensitivity implementation, a pharmacometrics workflow, or clinical-decision software.

## Motivation

Mechanistic QSP and PK/PD models often evolve continuously between interventions but are governed by discrete treatment logic. Examples include:

- Doses administered at prescribed times
- Infusion starts, stops, dose reductions, or missed doses
- A toxicity or safety state that triggers a treatment hold
- A recovery threshold that permits treatment restart
- A biomarker, disease-burden, or tumor threshold that triggers a therapy switch
- Protocol rules that alter future treatment, measurement, or monitoring

Such logic is often encoded as incidental callback code or informal external bookkeeping. In a hybrid model, it is part of the mathematical specification.

A hybrid model contains a continuous state

```math
x(t) \in \mathbb R^n
```

and a discrete mode

```math
q(t) \in \mathcal Q
```

While the active mode is $q(t)$, the continuous state evolves according to

```math
\dot{x}(t)
=
f_{q(t)}
\bigl(
x(t),
t,
\theta,
v_{q(t)}(t)
\bigr)
```

where $\theta \in \mathbb R^p$ is a parameter vector and $v_q(t)$ is a continuous input, forcing term, or control signal active while the model is in mode $q$.

Scheduled bolus doses, infusion starts or stops, planned therapy changes, protocol visits, and other instantaneous actions are represented separately as explicit scheduled transitions. They are not implicitly absorbed into the continuous input $v_q(t)$.

Let

```math
\mathcal E
\subseteq
\mathcal Q \times \mathcal Q
```

denote the permitted directed transitions. A transition, or edge, is written

```math
e = (q^-, q^+) \in \mathcal E
```

where $q^-$ is the active mode immediately before the event and $q^+$ is the mode immediately afterward.

A state-triggered transition is associated with a guard

```math
g_e\bigl(x(t), t, \theta\bigr) = 0
```

At an event, the transition can reset the continuous state, change an input or parameter, and enter the target mode:

```math
x^+
=
R_e\bigl(x^-, q^-, t, \theta\bigr),
\qquad
q^+
=
\\mathrm{target}(e)
```

Here $x^-$ and $x^+$ denote the continuous state immediately before and after the transition. The reset map $R_e$ may be the identity map when the continuous state remains unchanged and only the mode, input, or a future protocol action changes:

```math
R_{\texttt{on} \to \texttt{hold}}
\bigl(x^-, \texttt{on}, t, \theta\bigr)
=
x^-
```

For a treatment hold, the transition can nevertheless change the future continuous dynamics by selecting a different active input. For example, an infusion protocol may use

```math
v_{\texttt{on}}(t)
=
v_{\mathrm{inf}}(t),
\qquad
v_{\texttt{hold}}(t)
=
0
```

The continuous state may include pharmacokinetic amount states as well as biological, pharmacodynamic, biomarker, disease, and toxicity states. For example, in an illustrative IV-bolus model,

```math
x(t)
=
\bigl(
A_c(t),
x_{\mathrm{bio}}(t),
z_{\mathrm{tox}}(t)
\bigr)
```

where:

- $A_c(t)$ is the amount of drug in a central PK compartment
- $x_{\mathrm{bio}}(t)$ denotes the remaining biological, pharmacodynamic, biomarker, disease, or tumor–immune states
- $z_{\mathrm{tox}}(t)$ is an illustrative continuous toxicity or safety-burden state used by the treatment protocol

A scheduled IV-bolus dose $D_k$ at time $t_k$ updates the central amount state:

```math
A_c(t_k^+)
=
A_c(t_k^-)
+
D_k
```

The other continuous state components are unchanged by the instantaneous bolus itself, though they subsequently evolve under dynamics affected by drug exposure. If central concentration is needed, it can be defined by

```math
C_c(t)
=
\frac{A_c(t)}{V_c}
```

where $V_c$ is a central-compartment volume parameter.

This is an illustrative IV-bolus convention. For oral, subcutaneous, or other extravascular administration, a scheduled dose would update an appropriate depot or absorption-compartment amount state instead. An infusion is normally represented by a continuous, mode-dependent input rate over a specified time interval rather than by an instantaneous amount jump.

A scheduled dose should be logged even when it is not administered. For example, a dose may occur at a prescribed protocol time while the system is in `hold`; its event log should record the planned dose, incoming mode, action taken—administered, withheld, modified, or rescheduled—and post-event mode.

A complete hybrid treatment model therefore includes continuous dynamics, scheduled interventions, permitted transitions, guards, guard direction, reset maps, event priority, event-enabling and rearming rules, mode transitions, and a reproducible event log.

**Event-enabling and rearming rules** specify which transitions are eligible in each mode and when a transition that has fired becomes eligible again. The toxicity state $z_{\mathrm{tox}}(t)$ provides a simple illustrative example.

A treatment-hold transition may be enabled only while treatment is active:

```math
e_{\mathrm{hold}}
=
(\texttt{on}, \texttt{hold})
```

with guard

```math
g_{e_{\mathrm{hold}}}(x)
=
z_{\mathrm{tox}}
-
z_{\mathrm{hold}}
```

The hold transition occurs when the toxicity state crosses the upper threshold from below. The one-sided derivative is evaluated using the incoming mode, so it encodes the direction of the guard crossing:

```math
z_{\mathrm{tox}}
\bigl(
\tau_{\mathrm{hold}}
\bigr)
=
z_{\mathrm{hold}},
\qquad
\dot{z}_{\mathrm{tox}}
\bigl(
\tau_{\mathrm{hold}}^-
\bigr)
>
0
```

After this transition, the model is in mode `hold`, so $e_{\mathrm{hold}}$ is no longer enabled.

A distinct recovery/restart transition can be enabled only while treatment is held:

```math
e_{\mathrm{restart}}
=
(\texttt{hold}, \texttt{on})
```

with guard

```math
g_{e_{\mathrm{restart}}}(x)
=
z_{\mathrm{tox}}
-
z_{\mathrm{restart}}
```

The restart transition occurs when the toxicity state crosses the lower recovery threshold from above. Again, the one-sided derivative is evaluated using the incoming mode:

```math
z_{\mathrm{tox}}
\bigl(
\tau_{\mathrm{restart}}
\bigr)
=
z_{\mathrm{restart}},
\qquad
\dot{z}_{\mathrm{tox}}
\bigl(
\tau_{\mathrm{restart}}^-
\bigr)
<
0,
\qquad
z_{\mathrm{restart}}
<
z_{\mathrm{hold}}
```

The resulting mode sequence is

```math
\texttt{on}
\xrightarrow{
z_{\mathrm{tox}} = z_{\mathrm{hold}}
}
\texttt{hold}
\xrightarrow{
z_{\mathrm{tox}} = z_{\mathrm{restart}}
}
\texttt{on}
```

The distinct thresholds create hysteresis. They prevent immediate retoggling at a single threshold, and the mode-dependent enabling rules specify when the hold transition becomes eligible, or rearmed, again.

The toxicity state in this illustration is not assumed to represent every safety process in every QSP or PK/PD model. In a specific application, it could represent a measured safety biomarker, a latent toxicity burden, a modeled adverse-effect state, or another explicitly defined treatment-management criterion.

## Established methods and software

The mathematical tools relevant to this project are established, and in some domains they are used in end-to-end computational workflows.

Legged robotics and hybrid mechanics are canonical examples. A legged system evolves continuously during stance and swing, then undergoes discrete transitions at heel strike, liftoff, impact, contact creation or release, and controller switches. Hybrid-system tools can be used across the workflow: to specify a plant, simulate trajectories, locate events, linearize through transitions, propagate sensitivities, optimize trajectories, and design or analyze feedback controllers.

Saltation matrices and related event-transition derivatives are established first-order tools for state-triggered hybrid transitions. They account for both the shift in event time induced by a perturbation and the reset or mode change applied at that event. The broader hybrid-systems literature identifies applications including robotics, power circuits, and computational neuroscience.

The most mature end-to-end software workflows in hybrid mechanics are typically domain-facing. Their modeling interfaces, examples, and optimization pipelines are organized around multibody or rigid-body dynamics, unilateral contact, kinematic constraints, geometry, actuators, and related mechanical structures. Those are the appropriate abstractions when heel strikes, liftoff, impact, and contact are the events of interest. Drake, for example, is a model-based robotics toolbox for simulation, planning, control, and optimization.

Mechanistic QSP and PK/PD models have a different natural plant description: coupled biochemical, physiological, pharmacological, cellular, or population-level ODEs. Their discrete transitions may represent administered or withheld doses, protocol-defined visits, toxicity holds, recovery-triggered restarts, biomarker thresholds, therapy switches, or changes in an observation process.

| Hybrid mechanics / robotics | QSP and PK/PD analogue |
|---|---|
| State: positions and velocities | State: exposure, biomarkers, cell populations, toxicity, disease burden |
| Continuous stance or swing dynamics | Continuous PK/PD, QSP, physiological, or tumor–immune dynamics |
| Heel strike, liftoff, impact, or contact guard | Toxicity, biomarker, efficacy, or safety threshold guard |
| Contact impulse or velocity reset | Dose increment, withheld dose, therapy switch, or mode change |
| Contact/controller mode | Treatment `on`, `hold`, `restart`, `reduced dose`, or `switch` mode |
| Motion objective and contact constraints | Efficacy, safety, exposure, burden, and treatment-protocol objectives |
| Trajectory optimization | Dose, schedule, and policy comparison or optimization |

The project does not claim that hybrid mathematics is new, or that mechanics software is inadequate for mechanical applications. It investigates whether established hybrid variational methods can be made comparably transparent, analytically verifiable, and reproducible in a pharmacology-facing Julia/SciML workflow whose basic objects are mechanistic ODE models and treatment-protocol semantics rather than rigid-body/contact models.

## Mathematical approach

Let

```math
x(t; x_0, \theta)
\in
\mathbb R^n
```

denote the continuous trajectory associated with initial condition $x_0$ and parameter vector

```math
\theta
\in
\mathbb R^p
```

Two related Jacobian-valued sensitivity objects are useful.

The state-transition matrix is the Jacobian of the flow with respect to the initial condition:

```math
\Phi(t,t_0)
=
\frac{
\partial x(t; x_0, \theta)
}{
\partial x_0
}
\in
\mathbb R^{n \times n}
```

The parameter-sensitivity matrix is the Jacobian of the trajectory with respect to the parameter vector:

```math
S_\theta(t)
=
\frac{
\partial x(t; x_0, \theta)
}{
\partial \theta
}
\in
\mathbb R^{n \times p}
```

These are vector- and matrix-valued variational quantities. For a state of dimension $n$ and parameter vector of dimension $p$:

- $\Phi(t,t_0)$ has shape $n \times n$
- $S_\theta(t)$ has shape $n \times p$
- $D_xf_q$ has shape $n \times n$
- $D_\theta f_q$ has shape $n \times p$

For a single selected initial-condition direction or parameter direction, the corresponding sensitivity is a vector rather than a full matrix.

### Smooth trajectory segments

While the discrete mode is fixed at $q$, the continuous dynamics are

```math
\dot{x}(t)
=
f_q
\bigl(
x(t),
t,
\theta,
v_q(t)
\bigr)
```

The state Jacobian of the active vector field is

```math
D_xf_q
\bigl(
x(t),
t,
\theta,
v_q(t)
\bigr)
\in
\mathbb R^{n \times n}
```

and the parameter Jacobian of the active vector field is

```math
D_\theta f_q
\bigl(
x(t),
t,
\theta,
v_q(t)
\bigr)
\in
\mathbb R^{n \times p}
```

The smooth variational equations are

```math
\dot{\Phi}(t,t_0)
=
D_xf_q
\bigl(
x(t),
t,
\theta,
v_q(t)
\bigr)
\Phi(t,t_0),
\qquad
\Phi(t_0,t_0)
=
I_n
```

and

```math
\dot{S}_\theta(t)
=
D_xf_q
\bigl(
x(t),
t,
\theta,
v_q(t)
\bigr)
S_\theta(t)
+
D_\theta f_q
\bigl(
x(t),
t,
\theta,
v_q(t)
\bigr)
```

The first equation propagates perturbations in the initial continuous state. The second propagates perturbations in model parameters, including both the effect of a perturbed state and the direct effect of a perturbed parameter on the active vector field.

### State-triggered transitions

A perturbation of an initial condition or parameter can change the time at which a guard is reached. It can therefore change the duration of the pre-event flow, the state reaching the transition, and the post-event mode or reset state.

For an edge

```math
e = (q^-,q^+)
```

a scalar guard

```math
g_e(x,t,\theta)=0
```

defines a state-triggered transition. For this scalar guard,

```math
D_xg_e
\in
\mathbb R^{1 \times n},
\qquad
D_\theta g_e
\in
\mathbb R^{1 \times p}
```

are respectively the state and parameter derivatives of the guard function.

If the transition occurs at time $\tau_e$, then

```math
g_e
\bigl(
x(\tau_e^-),
\tau_e,
\theta
\bigr)
=
0
```

The transition’s reset map is

```math
R_e
\bigl(
x^-,
q^-,
\tau_e,
\theta
\bigr)
```

which maps the pre-event continuous state to the post-event continuous state:

```math
x^+
=
R_e
\bigl(
x^-,
q^-,
\tau_e,
\theta
\bigr)
```

The derivative

```math
D_xR_e
```

is the Jacobian of the reset map with respect to the pre-event continuous state. The reset may be the identity map when only the mode or the mode-dependent continuous input changes.

At a suitable transversal event, a saltation matrix or equivalent event-transition derivative propagates a first-order state perturbation through transition $e$:

```math
\delta x^+
=
\Xi_e \delta x^-
```

The transition derivative $\Xi_e$ depends on the incoming vector field $f_{q^-}$, the outgoing vector field $f_{q^+}$, the guard $g_e$, the reset map $R_e$, explicit time or parameter dependence, and the adopted event convention.

For parameter sensitivities, a schematic transition update is

```math
S_\theta^+
=
\Xi_e S_\theta^-
+
\Gamma_{e,\theta}
```

where

```math
\Gamma_{e,\theta}
```

is the additive parameter-dependent contribution arising from explicit parameter dependence in the guard, reset map, vector fields, or transition specification. Its exact form depends on the adopted event convention and on which quantities are held fixed. This schematic relation is not, by itself, a complete implementation formula; the benchmark specification will state and derive the convention-specific update used for validation.

Transversality requires the guard to be crossed at nonzero rate:

```math
\frac{d}{dt}
g_e
\bigl(
x(t),
t,
\theta
\bigr)
\neq
0
```

Near a grazing event, the crossing rate is close to zero:

```math
\frac{d}{dt}
g_e
\bigl(
x(t),
t,
\theta
\bigr)
\approx
0
```

In that regime, small perturbations can produce large changes in event time, create or remove events, or alter event order. An ordinary smooth derivative may then be poorly conditioned or may not be the appropriate mathematical object.

### Automatic differentiation

Automatic differentiation can be used to obtain derivatives of smooth ingredients, including

```math
D_xf_q,
\qquad
D_\theta f_q,
\qquad
D_xg_e,
\qquad
D_\theta g_e,
\qquad
D_xR_e
```

It does not by itself settle the derivative of an implicitly defined state-triggered event time, the derivative of an event transition, or behavior at a changed event sequence. In the intended workflow, AD is a component of hybrid variational calculation, not a substitute for hybrid event analysis.

### Event-structured multiple shooting

For long, unstable, stiff, or strongly event-sensitive problems, an event-structured multiple-shooting formulation may be appropriate.

One natural construction partitions the trajectory at scheduled or realized state-triggered transitions:

```math
[t_0,\tau_1],
\quad
[\tau_1,\tau_2],
\quad
\dots,
\quad
[\tau_m,T]
```

Let $z_i$ denote the shooting state immediately after transition $i-1$. Let $q_i^-$ denote the mode active on the segment ending at $\tau_i$, and let

```math
e_i
=
(q_i^-,q_i^+)
```

denote the transition realized at time $\tau_i$.

The mode-specific flow on the $i$-th smooth segment is denoted

```math
\varphi_{q_i^-}
\bigl(
\tau_i,
\tau_{i-1}^+;
z_i,
\theta
\bigr)
```

It maps the shooting state $z_i$, defined immediately after the preceding transition, to the pre-event state immediately before the transition at $\tau_i$.

The reset map

```math
R_{e_i}
\bigl(
x^-,
q_i^-,
\tau_i,
\theta
\bigr)
```

is the reset equation associated with the realized edge $e_i$. It maps the pre-event continuous state to the post-event state. It may be the identity map if the transition changes only the active mode or a mode-dependent input.

A schematic event-aware connection constraint is therefore

```math
c_i(z_i,z_{i+1},\theta)
=
R_{e_i}
\!\left(
\varphi_{q_i^-}
\bigl(
\tau_i,
\tau_{i-1}^+;
z_i,
\theta
\bigr),
q_i^-,
\tau_i,
\theta
\right)
-
z_{i+1}
=
0
```

The next shooting state is

```math
z_{i+1}
=
x(\tau_i^+)
```

and the mode after the transition is

```math
q_i^+
=
\mathrm{target}(e_i)
```

For a prescribed event time, $\tau_i$ is known. For a state-triggered transition, write $\tau_i=\tau_i(z_i,\theta)$; the dependence on $z_i$ and $\theta$ is suppressed in the preceding flow and reset notation only for readability. The event time is determined implicitly by

```math
g_{e_i}
\!\left(
\varphi_{q_i^-}
\bigl(
\tau_i(z_i,\theta),
\tau_{i-1}^+;
z_i,
\theta
\bigr),
\tau_i(z_i,\theta),
\theta
\right)
=
0
```

The Jacobian of the connection constraint must include derivatives of the smooth flow and the dependence of event time and post-event state on shooting variables and parameters:

```math
\frac{
\partial \tau_i(z_i,\theta)
}{
\partial z_i
},
\qquad
\frac{
\partial \tau_i(z_i,\theta)
}{
\partial \theta
}
```

A saltation matrix $\Xi_{e_i}$, or an equivalent derivative of the event-defined transition map, is the natural hybrid-system object for this connection.

A shooting discretization need not use a node at every event in every application. However, any segment that crosses state-triggered transitions must be treated as an event-aware flow, and its derivative must incorporate those transitions correctly. For the first analytic benchmark, placing segment boundaries at each transition gives the clearest formulation.

## Existing Julia ecosystem

### `HybridSystems.jl` and JuliaReach

`HybridSystems.jl` is an existing general-purpose Julia interface for defining and working with hybrid systems, including hybrid automata, switched systems, continuous subsystems, and discrete transitions. Its stated purpose is to support hybrid-systems algorithms independently of a particular data structure. Related JuliaReach tooling uses hybrid-system representations for reachability analysis and hybrid optimal-control problems.

This project is not intended to replace `HybridSystems.jl`, its system representations, or associated reachability and control tools.

The proposed focus of `hybrid-ds-julia` is more application-facing:

- Mechanistic continuous-time models expressed naturally as QSP, PK/PD, physiological, or tumor–immune ODEs
- Treatment-protocol semantics including scheduled doses, infusions, visits, holds, restarts, dose modifications, biomarker thresholds, and therapy switches
- Explicit, reproducible event logs and pre-event/post-event conventions
- Analytic benchmark models with independently known event-time and terminal-output derivatives
- Hybrid variational sensitivity propagation, including saltation-style event-transition derivatives where appropriate
- Potential event-structured multiple-shooting formulations that connect smooth segments across scheduled and state-triggered transitions

The initial technical question is whether `HybridSystems.jl`, SciML event/callback and sensitivity tools, and existing multiple-shooting capabilities can already be composed to support this workflow. If so, the appropriate contribution may be examples, analytic benchmarks, documentation, and interoperability rather than a new package-level abstraction. If not, any added layer should remain narrow, interoperable, and built on the established ecosystem.

| Aspect | `HybridSystems.jl` / associated JuliaReach tools | `hybrid-ds-julia` under investigation |
|---|---|---|
| Primary role | General hybrid-system and hybrid-automaton representation/interface | QSP/PK/PD-facing workflow, examples, validation, and potentially narrow utilities |
| Natural model language | Hybrid automata, modes, switched systems, continuous subsystems, transitions | Mechanistic QSP, PK/PD, physiology, and tumor–immune ODE models plus treatment protocols |
| Associated analyses | Reachability and hybrid optimal control through related tools | Event logging, analytic sensitivity benchmarks, event-time derivatives, fitting and protocol analysis if validated |
| Typical conceptual example | Bouncing ball, switching, hybrid automata, safety/reachability | Scheduled dosing, treatment hold/restart, threshold-triggered therapy change |
| Core event objects | Modes, transitions, automata, invariants, reset maps | Doses, infusions, visits, treatment modes, guards, thresholds, hold/restart rules, observation times |
| Sensitivity focus | Not the primary claim of the package interface | Hybrid variational/event-transition sensitivity workflow, subject to analytic validation |
| Relationship | Existing foundation to evaluate and reuse | Potentially a domain-facing layer, benchmark suite, or integration pattern—not a replacement |

The repository name is a working title and may change if a more specific pharmacology-facing name better reflects a complementary role alongside existing Julia hybrid-systems packages.

### SciML event handling and sensitivities

Julia/SciML already provides important components of the computational foundation:

- Differential-equation solvers
- Root-found state-triggered events and prescribed-time actions
- Callback interfaces for event detection and solver-level actions
- Symbolic event representations
- Several forward, adjoint, and automatic-differentiation-based sensitivity approaches
- Multiple-shooting formulations in several problem settings

In SciML, a **callback** is a solver-level instruction that evaluates an event condition or prescribed time and applies an action—such as a reset, parameter update, mode change, or event-log entry—when the event occurs. A continuous callback detects a zero of a condition function, potentially within an integration step; a discrete callback evaluates a Boolean condition at step endpoints.

**A callback specifies a solver-level action at an event; hybrid variational analysis specifies how first-order perturbations and sensitivities propagate through that event.** For state-triggered transitions, this includes the dependence of event time on initial conditions and parameters, as well as the derivative of any reset and the post-event vector field.

Existing SciML sensitivity methods already support many differential equations with events and callbacks, but support is algorithm- and event-structure-dependent. The project’s purpose is not to assume a gap in that support. Rather, it is to identify the appropriate existing formulation, validate it against analytic hybrid benchmarks, and determine whether the specific combination of state-triggered treatment-protocol semantics, event-aware sensitivities, and event-structured multiple shooting is already supported end to end.

The project therefore does not begin from the premise that a new solver, event system, sensitivity package, or generic multiple-shooting method is needed. Its question is more specific:

> Can existing Julia/SciML components be composed into a mathematically coherent, reproducible, and analytically validated workflow for mechanistic treatment-protocol models with state-triggered transitions?

The intended workflow would:

1. Represent the continuous plant as a mechanistic ODE model of PK, PD, physiology, disease, or tumor–immune dynamics
2. Represent scheduled doses, infusions, measurements, and protocol visits alongside state-triggered toxicity, biomarker, efficacy, or safety transitions
3. Partition a trajectory into smooth segments separated by relevant scheduled or realized state-triggered transitions when event-structured multiple shooting is required
4. Connect adjacent segments through the appropriate event-aware map: flow to the event, guard condition, reset or mode update, and post-event initial condition
5. Propagate smooth variational sensitivities within segments and the appropriate event-time or transition derivative across state-triggered events
6. Validate the complete calculation against analytically tractable hybrid benchmarks with independently known derivatives

Existing Julia tools provide event handling, sensitivity analysis, and multiple shooting as individual capabilities. A central question is whether their present composition already supplies the event-structured, saltation-aware workflow described here, or whether a narrowly scoped extension, benchmark suite, or QSP/PK/PD-facing interface would add value.

## Analytic validation standard

The central validation target is a hybrid model with independently derived analytic sensitivities, accurate to round-off error under a stated event convention and regularity assumptions.

For a selected parameter direction, with the initial condition $x_0$ held fixed, the benchmark should make it possible to obtain analytically

```math
\tau(x_0,\theta),
\qquad
\frac{\partial \tau}{\partial \theta},
\qquad
x(T;x_0,\theta),
\qquad
\frac{\partial x(T;x_0,\theta)}{\partial \theta}
```

where $\tau(x_0,\theta)$ is a state-triggered event time and $T$ is a terminal time after the transition. Initial-condition sensitivities are treated analogously, with $\theta$ held fixed.

The benchmark should separately test:

- Smooth-segment variational propagation
- The derivative of guard-crossing time
- The transition derivative through a reset or mode change
- The terminal-state or scalar-objective derivative
- Convergence under documented ODE-solver and root-localization tolerances
- The stated assumptions of transversality and locally fixed event sequence

The first exact state-triggered benchmark should be deliberately low dimensional and analytically transparent. Biological realism is not its criterion; an independently known hybrid derivative is.

For a computed sensitivity $S_{\mathrm{computed}}(T)$ and analytic reference $S_{\mathrm{exact}}(T)$, a representative normalized error measure is

```math
\frac{
\left\|
S_{\mathrm{computed}}(T)
-
S_{\mathrm{exact}}(T)
\right\|
}{
\max\!\left(
1,
\left\|
S_{\mathrm{exact}}(T)
\right\|
\right)
}
```

Interpretation of that error requires the numerical tolerances, event-location behavior, and event sequence to be reported.

## Finite differences

Finite differences are neither the project’s primary sensitivity method nor its validation oracle.

For an output $J(x_0,\theta)$, a forward difference in one selected scalar parameter direction, with $x_0$ and all other parameters held fixed, is

```math
\frac{
J(x_0,\theta+h)-J(x_0,\theta)
}{
h
}
```

In a smooth Float64 calculation, the balance between truncation and round-off error often imposes a practical lower scale related to

```math
\sqrt{\epsilon_{\mathrm{mach}}}
```

which is roughly $10^{-8}$ in relative scale, before accounting for ODE-solution and event-location error.

Hybrid models introduce another constraint. The perturbation $h$ must also remain small enough to preserve the relevant event structure: event existence, crossing branch, event order, reset sequence, and mode sequence. Schematically, a useful quotient would require

```math
h_{\mathrm{numerical}}
\lesssim
|h|
\lesssim
h_{\mathrm{structure}}
```

The interval may be empty:

```math
h_{\mathrm{structure}}
\lesssim
h_{\mathrm{numerical}}
```

This can occur near grazing events or near boundaries where a parameter perturbation creates, removes, or reorders events. A finite-difference sweep may therefore show no stable accuracy plateau even where a hybrid derivative is meaningful within a fixed local event sequence.

Finite differences may be included as a controlled negative comparison to demonstrate this limitation. They are not the criterion by which the hybrid variational method is judged correct.

## Candidate benchmark ladder

### A. Exact scheduled-impulse tests

The first unit benchmarks will use scalar or low-dimensional systems with prescribed impulse times and closed-form flows. These tests verify:

- Scheduled-event conventions
- Pre-event and post-event state conventions
- Reset-map semantics
- Repeated impulse handling
- Event logging
- Exact parameter and initial-condition sensitivities

Pang, Shen, and Zhao (2016) provides useful source structures. It includes scalar immune-cell and drug-concentration subsystems with exponential flow between fixed-time impulses and explicit periodic solutions. Because the event times are prescribed, these systems test fixed-time reset propagation rather than state-triggered event-time sensitivity.

### B. Exact state-triggered hybrid test

The primary mathematical validation benchmark will be a deliberately selected low-dimensional hybrid system with:

- A transversal guard
- Analytically known event time and event-time derivative
- A specified reset or mode transition
- An analytically known post-event flow
- An analytic terminal-state or output derivative

This benchmark will test hybrid variational propagation and the corresponding saltation-style event transition directly against an independent analytic reference.

### C. Application-motivated tumor–immune test

Zhao, Pang, and Li (2021) provides a later application-motivated test case: a nonlinear tumor–immune model combining scheduled immunotherapy pulses with chemotherapy triggered when tumor biomass reaches a threshold. It contains the hybrid ingredients relevant here: scheduled events, a state-triggered guard, nontrivial resets, and nonlinear coupled continuous dynamics.

It is a candidate stress test after the exact benchmark has validated the core method. It is not initially an exact-derivative oracle: the paper treats the threshold model numerically, and an independently derived analytic reference or an analytically tractable reduction would be required before using it as an exact sensitivity benchmark.

## Scope and non-goals

The immediate objective is a narrow, reproducible benchmark sequence. This repository does not currently claim to provide:

- A general-purpose hybrid ODE solver
- A new or validated saltation-matrix library
- An event-aware adjoint method
- A production QSP, PK/PD, or pharmacometrics package
- Clinical decision support or treatment recommendations
- Model qualification for a specific drug, disease, or patient population
- Broad interoperability with other modeling environments
- Neural, reinforcement-learning, stochastic, GPU, cloud, or distributed implementations

Some possible extensions are outlined below. None is a current implementation claim; each is contingent on analytic validation of the initial benchmark and evidence that existing Julia/SciML and pharmacometrics tools do not already meet the relevant need.

## Possible future directions

The directions below are not current implementation commitments. Each depends on a validated analytic benchmark, an informed assessment of existing Julia tools, and a concrete use case.

### Fitting hybrid mechanistic models to data

A later workflow may fit mechanistic hybrid models to longitudinal PK, biomarker, disease-burden, toxicity, or related data through an observation model such as

```math
y_j
=
h\bigl(
x(t_j),
q(t_j),
\theta
\bigr)
+
\varepsilon_j
```

Here $y_j$ is an observation at time $t_j$, $h$ maps continuous state and treatment mode to the observation, and $\varepsilon_j$ represents noise or discrepancy.

The issue is not simply ODE fitting. Parameters may alter event time, event count, event order, cumulative exposure, and the mode active at observation times. A future implementation would need to establish where hybrid variational derivatives support likelihood-based calibration or optimization, and where event-structure changes require regime-aware, nonsmooth, or derivative-free approaches.

### Mechanistic–AI residual models

A mechanistic hybrid model may represent known PK/PD, physiological, or treatment-protocol structure while leaving systematic residual discrepancy in the dynamics or observation process.

One possible continuous-dynamics formulation is

```math
\dot{x}(t)
=
f_{q(t)}
\bigl(
x(t),
t,
\theta,
v_{q(t)}(t)
\bigr)
+
r_\phi
\bigl(
x(t),
q(t),
t,
v_{q(t)}(t)
\bigr)
```

where $r_\phi$ is a learned residual model.

A more conservative alternative is an observation residual:

```math
y_j
=
h\bigl(
x(t_j),
q(t_j),
\theta
\bigr)
+
r_\phi
\bigl(
x(t_j),
q(t_j),
t_j
\bigr)
+
\varepsilon_j
```

These extensions should retain explicit event semantics. They should distinguish known scheduled interventions from learned effects, explicit guards from learned discontinuities, mechanistic parameters from residual-model parameters, predictive performance from mechanistic identifiability, and interpolation within observed regimes from extrapolation across changed treatment policies.

### Mixed-effects and population hybrid models

A pharmacometrics-oriented extension could represent between-subject variation in continuous parameters, treatment thresholds, observation models, or adherence processes. For subject $i$,

```math
\theta_i
=
\Theta(\eta_i,\beta),
\qquad
\eta_i
\sim
\mathcal N(0,\Omega)
```

with a subject-specific hybrid trajectory

```math
\dot{x}_i(t)
=
f_{q_i(t)}
\bigl(
x_i(t),
t,
\theta_i,
v_{q_i(t)}(t)
\bigr)
```

This should follow a validated deterministic single-subject workflow. Population inference adds the statistical difficulties of random effects, partial observability, sparse irregular sampling, and potential variation in discrete treatment transitions.

### Interoperability with `HybridSystems.jl`

Before defining a new representation for modes, guards, resets, and transitions, the project may evaluate interoperability with `HybridSystems.jl` and related JuliaReach tools.

Questions include whether a treatment-protocol model can be represented naturally as a hybrid automaton while retaining an idiomatic mechanistic ODE formulation; whether scheduled dosing and state-triggered treatment transitions map cleanly to existing abstractions; and whether the same model can support both SciML simulation and JuliaReach-associated reachability or control analysis.

A new domain-facing wrapper would be justified only if generic representations cannot express needed treatment-protocol semantics clearly and reproducibly.

### Interoperability with Pumas

Pumas is a logical first pharmacometrics interoperability target because it is Julia-native, pharmacometrics-facing, and represents drug administration through dosage-regimen and subject-event mechanisms. Pumas provides an integrated environment for pharmacometric model simulation, estimation, and related analysis.

The first goal would not be complete automatic model translation. Narrow initial pathways could include:

- Reconstructing a Pumas model’s continuous ODE dynamics and scheduled dosing regimen in a hybrid benchmark workflow
- Exporting or reproducing event logs containing time, amount, route, compartment, treatment mode, and state-triggered actions
- Comparing baseline Pumas and Julia/SciML simulations under matched scheduled-event conventions
- Determining how a state-triggered hold, restart, or treatment switch can be represented within a Pumas-compatible workflow or whether it requires an explicitly composed SciML-level approach
- Documenting differences in pre-event/post-event conventions, observation timing, dosing semantics, parameterization, and solver configuration

The question is not whether Pumas can represent standard scheduled dosing. It is how state-triggered treatment-protocol logic, reproducible event semantics, and hybrid sensitivity information can be represented and validated in a Pumas-facing workflow.

### Interoperability with other pharmacometrics ecosystems

After a narrow Pumas pathway is understood, later work could evaluate transparent, reproducible comparison harnesses or limited exchange workflows with other commonly used pharmacometrics environments.

Possible targets might include NONMEM, Monolix, nlmixr2/RxODE, Phoenix/WinNonlin, R, SAS, Stan, or related internal workflows, depending on a concrete use case and permitted interfaces.

The appropriate first goal is transparent comparison, not universal bidirectional conversion:

- A documented simple ODE model
- A matched dosing and event record
- A matched observation table and unit convention
- A reproducible simulation comparison
- An explicit record of model, event, solver, or estimation features that do not translate

Differences in model languages, solver defaults, estimation algorithms, event semantics, datasets, proprietary formats, validation requirements, and licenses may preclude exact equivalence. Cross-platform benchmark cases may be more valuable than an ambitious automatic translator.

### Hybrid protocol and policy optimization

After analytic validation and basic calibration, the framework could be used to study dose, dosing interval, threshold values, hold duration, restart criteria, or monitoring frequency.

A generic objective could combine efficacy and safety:

```math
\mathcal J(\theta,\pi)
=
\Phi\bigl(
x(T),
q(T)
\bigr)
+
\int_0^T
L\bigl(
x(t),
q(t),
v_{q(t)}(t)
\bigr)\,dt
+
\sum_k
C_k\bigl(
x(\tau_k^-),
x(\tau_k^+),
q(\tau_k^-),
q(\tau_k^+)
\bigr)
```

where $\pi$ is a parameterized treatment policy and $\tau_k$ are realized event times.

Gradient-based optimization may be appropriate inside a fixed transversal event regime. It may become unreliable when a step changes event count, event ordering, or the existence of a treatment hold. Any future optimization work should therefore assess regime-aware, nonsmooth, or derivative-free alternatives rather than assume a globally smooth objective.

### Benchmark and reproducibility suite

A practical future contribution may be a public suite of compact hybrid benchmarks for QSP/PK/PD-facing event semantics.

Each benchmark could provide:

- A mathematical specification of states, parameters, modes, guards, resets, priorities, and rearming rules
- A reference event log
- Solver and tolerance settings
- Analytic state, event-time, or sensitivity results when available
- A finite-difference failure illustration where appropriate
- A reproducibility test across documented solver configurations
- A statement distinguishing numerical verification from application-motivated demonstration

Such a suite could help compare implementations, clarify event conventions, reveal numerical edge cases, and determine whether a new domain-facing abstraction adds value.

## Current contents

The repository currently includes:

- A mathematical design and terminology for hybrid ODE models
- A proposed analytic-validation and benchmark sequence
- Background reading and application notes
- Documentation-maintenance tooling

No runnable Julia/SciML model, validated benchmark result, or released package is currently claimed.

## Feedback sought

Feedback is especially welcome on:

1. The choice of an analytically tractable state-triggered hybrid benchmark with exact-to-round-off derivatives
2. Appropriate saltation or equivalent event-transition conventions for such a benchmark
3. Existing Julia/SciML tools, examples, and research that should be treated as the starting point
4. Whether existing event, sensitivity, and multiple-shooting tools already compose into the event-structured hybrid workflow described here
5. The appropriate boundary between a QSP/PK/PD-facing workflow and functionality already provided by established SciML, `HybridSystems.jl`, JuliaReach, and Pumas tools

## References

- Pang, L., Shen, L., and Zhao, Z. (2016). *Mathematical Modelling and Analysis of the Tumor Treatment Regimens with Pulsed Immunotherapy and Chemotherapy*. *Computational and Mathematical Methods in Medicine*, Article ID 6260474. <https://doi.org/10.1155/2016/6260474>

- Zhao, Z., Pang, L., and Li, Q. (2021). *Analysis of a hybrid impulsive tumor-immune model with immunotherapy and chemotherapy*. *Chaos, Solitons & Fractals*, 144, 110617. <https://doi.org/10.1016/j.chaos.2020.110617>

- Kong, N., Payne, S., Zhu, J., and Johnson, A. M. (2024). *Saltation Matrices: The Essential Tool for Linearizing Hybrid Dynamical Systems*. *IEEE Control Systems Magazine*.

- `HybridSystems.jl` documentation and repository. General hybrid-system definitions and interfaces in Julia, including hybrid automata and switched systems.

- SciML documentation for callbacks, forward sensitivity analysis, and multiple shooting.
