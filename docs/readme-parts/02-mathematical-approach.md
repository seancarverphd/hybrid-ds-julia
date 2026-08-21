## Mathematical approach

`hybrid-ds-julia` is intended for mechanistic dynamical models in which continuous-time evolution is interrupted or altered by explicit discrete events. The central modeling task is to make both components first-class objects: users specify the continuous right-hand side, the conditions under which events occur, the state or parameter updates caused by those events, and the quantities to be analyzed, calibrated, or optimized.

The package is motivated by models such as PK/PD and QSP systems with repeated dosing, treatment holds, toxicity thresholds, therapy switches, missed doses, adherence scenarios, and measurement-driven policies. The same mathematical structure applies more broadly to biological, clinical, industrial, ecological, and engineered systems.

### Continuous dynamics, modes, and events

A hybrid model contains a continuous state:

\[
x(t)\in\mathbb{R}^{n},
\]

and a discrete mode:

\[
q(t)\in\mathcal{Q}.
\]

Within a mode, the continuous state follows an ODE:

\[
\dot{x}(t)=f_{q(t)}\bigl(x(t),t,\theta,u(t)\bigr),
\]

where:

- \(x(t)\) is the continuous state;
- \(q(t)\) identifies the active mode;
- \(\theta\) is a parameter vector;
- \(u(t)\) represents scheduled inputs, external forcing, observations, or control actions.

The mode can encode, for example:

- Treatment on, held, tapered, or switched;
- Active versus inactive controller;
- Pre-contact versus post-contact mechanics;
- Batch, fed-batch, cleaning, or harvest phase;
- Normal, fault, islanded, or restoration grid state;
- Active, passive, exploratory, or recovery behavioral mode.

An event may occur at a known time, such as a scheduled dose or infusion start, or when a guard condition becomes true:

\[
g_i(x(t),t,\theta)=0.
\]

At an event, the model can update its state, parameters, input, or mode:

\[
x^+=R_i(x^-,t,\theta),
\]

\[
\theta^+=P_i(\theta^-,x^-,t),
\]

\[
q^+=T_i(q^-,x^-,t).
\]

The pre-event and post-event states are denoted by \(x^-\) and \(x^+\). A reset need not make the state discontinuous. It can leave \(x\) continuous while changing the governing right-hand side, active parameters, input schedule, or decision policy.

### Scheduled and state-triggered events

Scheduled events occur at known times:

\[
t=t_1,t_2,\ldots,t_K.
\]

Examples include:

- Oral doses;
- Infusion starts and stops;
- Laboratory draws;
- Planned treatment changes;
- Scheduled maintenance;
- Known stimulation pulses;
- Planned irrigation or feed changes.

State-triggered events occur when a continuous trajectory reaches a guard surface:

\[
g_i(x,t,\theta)=0.
\]

Examples include:

- A toxicity biomarker crossing a hold threshold;
- Tumor burden crossing an adaptive-treatment threshold;
- Battery charge reaching a dispatch limit;
- Temperature crossing a thermostat threshold;
- Foot contact with the ground;
- A balance variable crossing a stepping threshold;
- A pathogen or viral-load measurement reaching a treatment-switch criterion.

State-triggered events require event detection and root localization. Their timing depends on the state, parameters, inputs, and numerical trajectory. This dependence is central to hybrid sensitivity analysis, calibration, and optimization.

### Event maps and hybrid semantics

A useful hybrid model must specify more than an `if` statement. For each event, the model should make clear:

1. **Guard:** What condition triggers the event?
2. **Direction:** Does the event apply on an upward crossing, downward crossing, or either direction?
3. **Priority:** What happens if multiple guards are satisfied at the same time?
4. **Reset:** Which states, parameters, inputs, or modes change?
5. **Persistence:** Does the new mode remain active until another event occurs?
6. **Rearming:** Can the same event trigger immediately again?
7. **Termination:** Does the event end the simulation or merely change its future evolution?
8. **Observability:** Which event times, state values, and mode changes are logged?

Explicit event semantics are important for scientific reproducibility. A model should not rely on undocumented callback order, hidden mutable global state, or ambiguous treatment of simultaneous events.

### Hybrid trajectories and measurements

The state trajectory may be continuous, piecewise smooth, or discontinuous depending on the reset map. The derivative is commonly discontinuous at event times even when the state itself remains continuous.

A model may be linked to observations through a measurement equation:

\[
y_j=h_j(x(t_j),q(t_j),\theta)+\varepsilon_j,
\]

where \(y_j\) is an observation at time \(t_j\), \(h_j\) maps hidden state and mode to an observable quantity, and \(\varepsilon_j\) represents measurement noise or discrepancy.

This distinction matters in scientific applications. A model should separate:

- Directly measured quantities;
- Latent states inferred from measurements;
- Parameters estimated from data;
- Externally imposed events;
- State-triggered events;
- Assumptions that are not directly observable.

### Dosing, pulses, and treatment holds

A common PK/PD event is an instantaneous bolus dose. If \(A(t)\) is an amount in a compartment, a dose at time \(t_k\) can be represented as:

\[
A(t_k^+)=A(t_k^-)+D_k.
\]

An infusion can be represented by a mode-dependent forcing term:

\[
\dot{A}=\cdots+u_{\mathrm{infusion}}(t),
\]

with discrete events turning the infusion on, changing its rate, or turning it off.

A treatment hold may leave all biological states continuous while changing a treatment-rate parameter or input:

\[
u(t)=0
\quad\text{when}\quad
z(t)\geq z_{\mathrm{hold}},
\]

where \(z(t)\) is a toxicity or safety state. Treatment can later resume under a separate rule:

\[
u(t)=u_0
\quad\text{when}\quad
z(t)\leq z_{\mathrm{resume}}.
\]

Using distinct hold and resume thresholds creates hysteresis and can prevent rapid repeated switching near a single threshold.

### Threshold policies and mode-dependent control

Many hybrid models include decision policies. A general state-dependent policy may take the form:

\[
u(t)=\pi_{q(t)}\bigl(x(t),\hat{x}(t),t,\theta\bigr),
\]

where \(\hat{x}(t)\) may be an estimated state based on noisy or delayed observations.

Examples include:

- Hold treatment when toxicity exceeds a threshold;
- Escalate treatment when a biomarker remains above a threshold;
- Apply a corrective balance step when a stability margin is crossed;
- Dispatch energy storage when price and state of charge meet a rule;
- Switch HVAC mode when temperature crosses a hysteresis band;
- Start a feed phase when substrate concentration reaches a prescribed range.

The policy itself should be specified separately from the physical, biological, or operational plant where possible. This makes it easier to compare competing policies without rewriting the underlying state dynamics.

### Event logging and reproducibility

A hybrid solution should provide more than sampled trajectories. It should record an event log containing, at minimum:

- Event identifier;
- Event time;
- Pre-event mode and post-event mode;
- Guard value or event cause;
- Pre-event and post-event state values when relevant;
- Parameter or input changes;
- Whether the event was scheduled or state triggered;
- Solver status and any root-finding diagnostics.

For scientific and engineering use, the event log is part of the result. It allows users to verify that a treatment hold occurred when intended, distinguish an imposed dose from a state-triggered policy event, diagnose unexpected repeated events, and compare event sequences across parameter sets.

### Numerical considerations near events

Event-driven ODE simulation is not equivalent to integrating one smooth vector field over the whole horizon. Event handling requires attention to:

- Guard-function scaling;
- Event direction;
- Root-finding tolerances;
- Simultaneous or nearly simultaneous events;
- Reinitialization after state or parameter jumps;
- Discontinuous forcing;
- Rapid repeated events;
- Grazing trajectories;
- Event ordering;
- Mode consistency after reset.

A transversal event crosses its guard surface with nonzero rate:

\[
\frac{d}{dt}g_i(x(t),t,\theta)\neq 0.
\]

Such crossings are generally well behaved. A grazing event has approximately zero crossing rate:

\[
\frac{d}{dt}g_i(x(t),t,\theta)\approx 0.
\]

Near grazing, small parameter or state changes can create large changes in event time, event count, or event order. This can make gradients poorly conditioned or undefined in the ordinary smooth sense.

### Validation of hybrid models

Validation should address both continuous trajectories and discrete behavior.

For a proposed model, useful checks include:

- Do state units, parameters, and event maps have a consistent interpretation?
- Are scheduled doses or interventions applied at the intended times?
- Do guards trigger only in the intended direction?
- Are threshold policies protected against unintended chattering?
- Does event order remain stable under small numerical-tolerance changes?
- Are state resets physically, biologically, or operationally defensible?
- Are event times and post-event states reproducible?
- Does the model reproduce held-out trajectories, events, or outcomes?
- Does an alternative mechanism explain the observations equally well?

Model fit alone is insufficient. A model can reproduce observed trajectories while assigning them to the wrong latent mechanism, especially when hidden states are weakly measured or confounded.

## Computational scaling, event complexity, and practical compute budgets

This section is for users planning a substantial simulation, calibration, sensitivity-analysis, optimization, control, or uncertainty-quantification workflow. It explains how computational requirements depend on state dimension, parameter dimension, event count, event geometry, solver choices, and the repeated-evaluation demands of the intended task.

This README is intentionally modular. Readers who need only a small event-aware simulation can skip much of this section. Readers planning high-dimensional models, gradient-based inference, multiple shooting, event-aware optimization, or cloud-scale parameter studies should use this section to select an appropriate numerical formulation before investing substantial implementation or compute time.

The central point is:

> The difficulty of a hybrid model is not determined by state dimension alone. It depends on the interaction among continuous dynamics, parameter dimension, event frequency, event conditioning, derivative requirements, solver behavior, and the number of repeated simulations required by the intended workflow.

### Model notation and baseline cost

Consider a mode-dependent hybrid ODE:

\[
\dot{x}(t)=f_{q(t)}\bigl(x(t),t,\theta,u(t)\bigr),
\]

where:

- \(x(t)\in\mathbb{R}^{n}\) is the continuous state vector;
- \(n\) is the number of continuous state variables;
- \(q(t)\) is a discrete mode;
- \(\theta=(\theta_1,\ldots,\theta_p)\in\mathbb{R}^{p}\) is the parameter vector;
- \(p\) is the number of scalar parameters whose effects may be analyzed, estimated, or optimized.

Depending on the application, \(\theta\) may include kinetic rates, PK/PD parameters, initial-condition parameters, controller gains, event thresholds, reset-map parameters, dose sizes, or policy parameters.

Let:

- \(m\) be the number of realized events during one simulated trajectory;
- \(G\) be the number of guard functions evaluated for state-triggered events;
- \(N\) be the number of accepted time-integration steps;
- \(r\) be the number of intervals in a multiple-shooting formulation;
- \(C_f\) be the cost of evaluating the continuous right-hand side \(f_q\);
- \(C_{\mathrm{root}}\) be the additional cost of locating one state-triggered event;
- \(C_{\mathrm{reset}}\) be the cost of executing its reset, mode change, and associated bookkeeping.

For a nominal hybrid simulation without derivative propagation, define the first-order bookkeeping cost:

\[
C_{\mathrm{solve}}
:=
N C_f
+
m\left(C_{\mathrm{root}}+C_{\mathrm{reset}}\right).
\]

This is the approximate cost of one **forward solve**. It is not a complete solver-performance model. In particular, it omits or absorbs into the constants:

- Rejected adaptive steps;
- Dense interpolation;
- Guard-function evaluation;
- Explicit Jacobian construction;
- Sparse factorization or preconditioning;
- Linear solves for implicit methods;
- Memory allocation;
- Compilation time;
- Disk I/O and checkpointing;
- Parallelization overhead;
- Numerical difficulty near discontinuities.

Scheduled events—such as a known dose at a known time—are often cheaper than state-triggered events because their times are supplied directly. A threshold crossing requires detection and localization, and may force solver reinitialization.

### What makes an event difficult?

A state-triggered event is commonly defined by a guard:

\[
g_i(x(t),t,\theta)=0.
\]

When the event occurs, the model may apply a state reset:

\[
x^+=R_i(x^-,t,\theta),
\]

change parameters,

\[
\theta^+=P_i(\theta^-,x^-,t),
\]

or change the active mode:

\[
q^+=T_i(q^-,x^-,t).
\]

The vector field may therefore switch from:

\[
\dot{x}=f_{q^-}(x,t,\theta)
\]

to:

\[
\dot{x}=f_{q^+}(x,t,\theta).
\]

A hybrid event has three computational effects:

1. The solver must detect and localize the event time.
2. The model must execute the reset or mode change.
3. A derivative-aware method must account for the fact that perturbations can change both the event time and the post-event state.

The third effect is crucial. A parameter change can cause an event to occur earlier or later, causing the system to spend a different amount of time under the pre-event and post-event vector fields. This is why differentiating only the smooth ODE segments is not enough.

#### Transversal events

An event is transversal when:

\[
\frac{d}{dt}g_i(x(t),t,\theta)\neq 0.
\]

Such events are usually well behaved for root finding and first-order sensitivity analysis.

#### Grazing events

At a grazing event:

\[
\frac{d}{dt}g_i(x(t),t,\theta)\approx 0.
\]

Small changes in state or parameters can then produce large changes in event time, cause an event to appear or disappear, or alter event ordering. Grazing events can therefore create:

- Very small solver steps;
- Large, unstable, or undefined local sensitivities;
- Poor gradient-based optimization behavior;
- Ambiguous event classification;
- Scientific fragility in threshold-based policy conclusions.

This is not merely a numerical problem. It often means that the underlying intervention, contact, switching, or decision rule is structurally sensitive.

### Jacobians, variational flow, and \(O(n^2)\) state equations

There are two related but distinct \(n\times n\) objects.

The first is the **state Jacobian** of the vector field:

\[
J_x(t)
=
\frac{\partial f_q}{\partial x}
\bigl(x(t),t,\theta\bigr)
\in\mathbb{R}^{n\times n}.
\]

If dense, it has \(n^2\) entries. However, it is not automatically an additional set of \(n^2\) ODE states. A numerical method may form it explicitly, approximate it, exploit sparsity, use Jacobian-vector products, generate it by automatic differentiation, or avoid forming it in explicit methods.

The second object is the **state-transition matrix**, or Jacobian of the flow with respect to the initial condition:

\[
\Phi(t,t_0)
=
\frac{\partial x(t)}{\partial x(t_0)}
\in\mathbb{R}^{n\times n}.
\]

If the full state-transition matrix is propagated, it satisfies:

\[
\dot{\Phi}(t)
=
J_x(t)\Phi(t,t_0),
\qquad
\Phi(t_0,t_0)=I_n.
\]

This does introduce \(n^2\) additional scalar differential equations. Together with the original state equations, the augmented smooth system has:

\[
n+n^2
\]

continuous scalar states.

The full matrix \(\Phi\) is useful when a method needs derivatives of the flow with respect to **all** initial-state directions. Examples include:

- Dense multiple-shooting Jacobian blocks;
- Stability analysis;
- Floquet or Poincaré-map calculations;
- Full local linearization of a trajectory;
- Some Newton, sequential-quadratic-programming, and second-order methods;
- Sensitivity of a full terminal state with respect to a full initial state.

For a hybrid event, a first-order perturbation is updated through a saltation matrix or equivalent event derivative:

\[
\delta x^+
=
\Xi\,\delta x^-.
\]

Consequently,

\[
\Phi^+
=
\Xi\Phi^-.
\]

For dense matrices, directly multiplying two \(n\times n\) matrices costs:

\[
O(n^3)
\]

per event. This is a key distinction: a dense \(O(n^2)\) event update applies to one tangent vector or one adjoint vector, while propagation of the **full** state-transition matrix requires a dense matrix-matrix update.

#### Directional variational equations

Users should not propagate a full state-transition matrix by default.

If only one initial-condition direction is needed, propagate one tangent vector:

\[
v(t)
=
\frac{\partial x(t)}{\partial\alpha}
\in\mathbb{R}^{n},
\]

which satisfies:

\[
\dot{v}=J_xv.
\]

This requires only \(n\) additional differential equations. At an event:

\[
v^+=\Xi v^-.
\]

For dense \(\Xi\), this costs:

\[
O(n^2)
\]

per event.

More generally, propagating \(k\) selected tangent directions requires an \(n\times k\) matrix:

\[
V(t)\in\mathbb{R}^{n\times k},
\]

with:

\[
\dot{V}=J_xV.
\]

The added continuous-state dimension is then:

\[
nk,
\]

rather than:

\[
n^2.
\]

This is often preferable when only a few perturbation directions, control directions, or shooting-variable directions are needed.

### Forward parameter sensitivities

Parameter sensitivities are distinct from the initial-condition state-transition matrix. Define:

\[
S_\theta(t)
=
\frac{\partial x(t)}{\partial\theta}
\in\mathbb{R}^{n\times p}.
\]

On smooth intervals, the forward variational equations are:

\[
\dot{S}_\theta
=
J_xS_\theta
+
J_\theta,
\]

where:

\[
J_\theta
=
\frac{\partial f_q}{\partial\theta}
\in\mathbb{R}^{n\times p}.
\]

Propagating all forward parameter sensitivities therefore introduces:

\[
np
\]

additional scalar differential equations. Together with the original state equations, the augmented system has:

\[
n+np
=
n(1+p)
\]

continuous scalar states.

If both the full initial-condition transition matrix and all parameter sensitivities are required, then the augmented system contains:

\[
n+n^2+np
\]

continuous scalar states.

#### Dense cost

For dense dynamics, evaluation of:

\[
J_xS_\theta
\]

costs approximately:

\[
O(n^2p)
\]

per variational update. The sensitivity matrix itself requires:

\[
O(np)
\]

memory.

A rough dense cost model is:

\[
C_{\mathrm{forward\ sens}}
\approx
O\!\left(
N(C_f+n^2p)
+
m(C_{\mathrm{root}}+C_{\mathrm{reset}}+n^2p)
\right).
\]

At an event, the parameter sensitivity update has schematic form:

\[
S_\theta^+
=
\Xi S_\theta^-
+
B_{\theta},
\]

where \(B_\theta\) contains derivatives associated with explicit parameter dependence in the guard, reset map, or mode transition. It is generally not enough to use only:

\[
S_\theta^+=\Xi S_\theta^-.
\]

For a dense \(n\times p\) sensitivity matrix, the leading matrix multiplication cost at each event is approximately:

\[
O(n^2p).
\]

#### Sparse and structured models

Dense asymptotic estimates can substantially overstate cost when the model is sparse.

Let \(z\) be the number of nonzero entries of \(J_x\). A sparse product may cost closer to:

\[
O(zp)
\]

than:

\[
O(n^2p).
\]

Similarly, many hybrid resets are local. A dose may alter one compartment; a treatment hold may change one parameter; a contact event may affect a limited subset of velocity components. If event derivatives are sparse, block structured, or low rank, their updates can be much cheaper than dense worst-case formulas imply.

For a large model, the useful questions are therefore:

- How many state variables are there?
- How many parameters are differentiated?
- Is the Jacobian sparse?
- How many guard functions are active?
- How many state variables does each reset affect?
- Is the event update local, sparse, or low rank?
- Are full matrices required, or only matrix-vector products?

#### When forward sensitivities are useful

Forward sensitivities are commonly attractive when the parameter count is modest:

\[
p\ll n,
\]

or more generally when only a small number of parameters need derivatives.

Examples include:

- Dose amount, dose interval, or infusion rate;
- A few PK/PD rate constants;
- A toxicity threshold;
- A handful of controller gains;
- An event threshold or reset parameter;
- Local sensitivity analysis of a calibrated model.

Forward methods are also useful during early model development because they can be inspected and compared with carefully selected finite perturbations away from events.

### Saltation-aware hybrid derivatives

At an event, classical smooth variational propagation is incomplete because perturbations change event timing.

For a transition from mode \(I\) to mode \(J\), a saltation matrix has schematic form:

\[
\Xi
=
D_xR
+
\frac{
\left(
f_J
-
D_xR\,f_I
-
D_tR
\right)
D_xg
}{
D_tg+D_xg\,f_I
}.
\]

The exact formula depends on event convention, guard, reset map, and time dependence. The denominator:

\[
D_tg+D_xg\,f_I
\]

is the instantaneous rate of crossing the event surface.

When that denominator is near zero, the event is near grazing and hybrid sensitivities can become large, ill-conditioned, or undefined in the ordinary differentiable sense.

| Carried derivative object | Shape | Event update | Dense direct cost per event |
|---|---:|---:|---:|
| One tangent direction \(v\) | \(n\times 1\) | \(v^+=\Xi v^-\) | \(O(n^2)\) |
| \(k\) tangent directions \(V\) | \(n\times k\) | \(V^+=\Xi V^-\) | \(O(n^2k)\) |
| Full state-transition matrix \(\Phi\) | \(n\times n\) | \(\Phi^+=\Xi\Phi^-\) | \(O(n^3)\) |
| Parameter sensitivity matrix \(S_\theta\) | \(n\times p\) | \(S_\theta^+=\Xi S_\theta^-+B_\theta\) | \(O(n^2p)\) |
| One adjoint vector \(\lambda\) | \(n\times 1\) | \(\lambda^-=\Xi^\top\lambda^+\) | \(O(n^2)\) |

These are dense worst-case costs. Sparse, local, low-rank, and matrix-free structures can reduce them substantially.

### Automatic differentiation

Automatic differentiation, or AD, is valuable for computing derivatives of smooth right-hand sides, reset maps, objectives, and numerical kernels. It does not automatically guarantee a correct hybrid derivative.

For example, an informal branch:

```julia
if g(x, t) <= 0
    apply_reset!()
end
```

does not by itself ensure that differentiation accounts for how a change in \(\theta\) shifts the time when the guard becomes zero.

For state-triggered hybrid events, a correct derivative generally needs:

- The smooth derivative before the event;
- The derivative of the guard;
- The derivative of event time;
- The derivative of the reset map;
- The vector-field change after the event.

AD may still be part of a correct implementation. For example, it can generate \(J_x\), \(J_\theta\), guard derivatives, reset derivatives, and discrete-adjoint calculations. But it should not be described as a replacement for hybrid sensitivity theory.

### Adjoint sensitivities

Suppose the objective is scalar:

\[
\mathcal{L}
=
\ell_T(x(T),\theta)
+
\sum_{j=1}^{m}
\ell_j(x(t_j^-),x(t_j^+),\theta).
\]

Examples include:

- Final tumor burden plus cumulative toxicity;
- Negative log likelihood of longitudinal data;
- Tracking error plus energy cost;
- Total time below a therapeutic threshold;
- Total process yield minus operating cost;
- A control objective with penalties for interventions or mode switches.

An adjoint method propagates a vector:

\[
\lambda(t)\in\mathbb{R}^{n}
\]

backward through the trajectory.

For a scalar objective, its key advantage is that the active derivative state is \(O(n)\), rather than \(O(np)\). The method does not carry a separate state-sensitivity column for every parameter.

A useful planning relation is:

\[
C_{\mathrm{adjoint}}
\approx
\alpha C_{\mathrm{solve}}
+
C_{\mathrm{checkpoint}}
+
mC_{\mathrm{event\ adjoint}},
\]

where:

- \(C_{\mathrm{solve}}\) is the nominal forward-solve cost defined above;
- \(\alpha\) is a practical constant capturing backward integration, replay, interpolation, and derivative work;
- \(C_{\mathrm{checkpoint}}\) is memory, storage, or recomputation cost;
- \(C_{\mathrm{event\ adjoint}}\) is the cost of reverse propagation across each event.

The constant \(\alpha\) is not generally one. Adjoint methods exchange dependence on parameter count for trajectory storage, checkpointing, replay, and event-adjoint complexity.

#### When adjoints are attractive

Adjoints are usually attractive when:

\[
p\gg 1,
\]

and the objective is scalar or low dimensional.

Examples include:

- Large parameter-estimation problems;
- Gradient-based calibration;
- Optimal experimental design;
- Policy optimization;
- Neural-network or high-dimensional surrogate parameters;
- Repeated optimization of a scalar cost.

#### Hybrid adjoint requirements

A hybrid adjoint must traverse every event correctly in reverse time. It must account for:

- Event-time dependence;
- Reset-map derivatives;
- Mode changes;
- Objective terms at events;
- Event ordering;
- Terminal events;
- Simultaneous events;
- Checkpointing around discontinuities;
- Reproducibility of the nominal event sequence.

Adjoints may not be the best first method when:

- Only a few parameters matter;
- Events are frequent;
- The event sequence changes under small perturbations;
- Grazing or chattering occurs;
- The model is strongly stiff;
- The objective is high dimensional;
- The event semantics are still being developed;
- Reliable debugging matters more than asymptotic speed.

A practical progression is:

1. Validate the nominal event-driven solve.
2. Implement and test a small forward or directional sensitivity calculation.
3. Check selected derivatives against perturbation calculations away from events.
4. Add explicit hybrid event-derivative handling.
5. Introduce adjoints only when parameter dimension or repeated evaluations justify their added complexity.

### Multiple shooting

Single shooting integrates from one initial condition across the full time horizon. It can be effective for short, stable trajectories. It can become poorly conditioned when trajectories are long, unstable, stiff, highly sensitive, or repeatedly reset.

Multiple shooting divides the time horizon into \(r\) intervals and introduces a state variable at each boundary:

\[
z_i\approx x(t_i),
\qquad
i=0,\ldots,r-1.
\]

Each interval is propagated independently. Continuity conditions enforce:

\[
c_i(z_i,z_{i+1},\theta)
=
\Phi_i(z_i,\theta)-z_{i+1}
=
0,
\]

where \(\Phi_i\) is the hybrid flow map over interval \(i\).

#### Problem dimension

The shooting-state decision variables have approximate dimension:

\[
rn.
\]

The continuity constraints have approximate dimension:

\[
(r-1)n.
\]

With \(p\) global parameters, the decision-vector dimension is approximately:

\[
rn+p.
\]

Thus multiple shooting trades:

\[
\text{a larger constrained optimization problem}
\]

for:

\[
\text{better conditioning and local control of trajectory mismatch}.
\]

#### Dense flow-map derivatives

A dense Newton or SQP method may require:

\[
A_i
=
\frac{\partial\Phi_i}{\partial z_i}
\in\mathbb{R}^{n\times n}.
\]

These are segment-level state-transition matrices. Retaining them across all shooting intervals requires approximately:

\[
O(rn^2)
\]

storage.

If derivatives with respect to parameters are retained:

\[
B_i
=
\frac{\partial\Phi_i}{\partial\theta}
\in\mathbb{R}^{n\times p},
\]

the additional storage is approximately:

\[
O(rnp).
\]

For dense models, if a full state-transition matrix is propagated and updated at each event, the naive event-update work can be approximately:

\[
O(mn^3).
\]

This is one reason that large-scale multiple-shooting methods often use sparse Jacobian representations, block-sparse continuity constraints, Jacobian-vector products, adjoint-vector products, matrix-free Krylov solvers, condensing, low-rank update structure, carefully selected segment boundaries, or reduced-order models.

#### Why multiple shooting can help

Multiple shooting is useful when:

- Long horizons amplify unstable directions;
- Small parameter changes create large trajectory changes;
- The model has multiple time scales;
- A fit must match measurements at intermediate times;
- Repeated events make full-horizon single shooting poorly conditioned;
- The optimizer starts far from a feasible trajectory;
- Different portions of the trajectory follow different modes.

For hybrid models, useful segment boundaries may occur at:

- Scheduled doses or interventions;
- Data collection times;
- Known controller mode changes;
- Expected gait or contact phases;
- Known process phase changes;
- Before and after particularly sensitive threshold regions.

Unknown state-triggered events may remain inside a shooting interval. Treating their times as explicit decision variables is possible, but adds event-consistency and transversality constraints.

### Event count, event structure, and tractability

The number of events \(m\) matters, but event conditioning and structure matter just as much.

#### Well-separated transversal events

If events are well separated and transversal, each event adds a bounded root-localization and reset cost. With a local or sparse reset, actual cost may be modest.

#### Grazing and event-sequence changes

If a parameter perturbation changes:

\[
A\rightarrow B\rightarrow C
\]

into:

\[
A\rightarrow C,
\]

then the trajectory can be differentiable within a fixed event sequence but nonsmooth across the boundary between sequences.

A gradient computed under the nominal event sequence may still be locally useful, but it should not be treated as globally reliable. Implementations should log and diagnose:

- Near-grazing crossings;
- Nearly simultaneous events;
- Changes in event count;
- Changes in event order;
- Repeated immediate events;
- Excessive root-finding iterations;
- Solver step collapse near a guard.

#### Chattering

Chattering occurs when a system repeatedly switches near the same event surface. Possible remedies, when physically justified, include:

- Hysteresis bands;
- Minimum dwell time;
- Refractory periods;
- Compliant or relaxation dynamics;
- Event aggregation;
- Smooth approximations for purely numerical switches;
- Differential-inclusion or complementarity formulations.

A model should not silently suppress chattering without recording that choice. The correct response depends on the domain mechanism.

### Dimension-specific planning guide

| Model regime | Reasonable first approach | Main scaling risk | Practical response |
|---|---|---|---|
| \(n\lesssim 50\), \(p\lesssim 20\), modest \(m\) | Direct simulation and directional/forward derivatives | Event correctness | Log events; validate selected derivatives |
| \(n\sim10^2\)–\(10^3\), \(p\ll n\), sparse dynamics | Sparse forward sensitivities | Jacobian products | Preserve sparsity; use matrix-free products where possible |
| \(n\sim10^2\)–\(10^4\), large \(p\), scalar objective | Event-aware adjoint | Checkpointing and event gradients | Validate on reduced benchmark cases |
| Long, unstable, or event-sensitive horizon | Multiple shooting | \(rn\) variables and block Jacobians | Segment at meaningful interventions or data times |
| Full stability or flow-map analysis | Full \(\Phi\) only if necessary | \(n^2\) states and \(O(n^3)\) dense event updates | Use directional products or reduced-order analysis if possible |
| Dense \(n\gtrsim10^3\), large \(p\) | Model reduction or specialized tools | Dense linear algebra | Exploit low rank, sparsity, locality, or surrogates |
| Frequent grazing/chattering | Nonsmooth or regularized formulation | Derivatives may fail | Reformulate events; use hysteresis or alternative methods |
| Primarily discrete operational problem | Discrete-event simulation or optimization | ODE machinery may add little | Use hybrid ODE methods only if a continuous state is central |

### Fixed-budget planning

A practical workflow consumes many more evaluations than one nominal simulation.

Let:

\[
K
\]

be the number of objective-and-gradient evaluations required by an optimizer, sampler, calibration procedure, uncertainty study, or experimental-design loop.

Then:

\[
C_{\mathrm{total}}
=
K C_{\mathrm{eval+grad}}.
\]

For a fixed computational budget \(B\):

\[
K C_{\mathrm{eval+grad}}
\leq B.
\]

A local optimization may require tens to hundreds of evaluations. Multistart optimization may require thousands. Bayesian calibration, posterior sampling, global search, or broad uncertainty quantification may require tens of thousands to millions.

If one objective-and-gradient evaluation costs 10 seconds, then:

\[
100{,}000
\times
10\ \mathrm{seconds}
=
1{,}000{,}000\ \mathrm{seconds},
\]

which is approximately:

\[
278\ \mathrm{single-worker\ hours}.
\]

Parallelization can reduce wall-clock time, but it does not reduce total compute consumption.

#### State dimension versus events under a fixed budget

Users commonly face tradeoffs among:

- More state variables;
- More parameters;
- More accurate event localization;
- More explicitly resolved events;
- Tighter solver tolerances;
- More optimization starts;
- More uncertainty samples;
- More sophisticated measurement models;
- More expensive derivatives;
- More detailed data assimilation.

Increasing \(n\) can increase ODE, Jacobian, linear-solver, and memory cost. Increasing \(p\) can dominate forward-sensitivity cost. Increasing \(m\) can increase root finding, resets, solver restarts, and derivative updates. Increasing \(K\) can dominate all per-solve costs.

A disciplined sequence is:

1. Start with the smallest state model that represents the mechanism of interest.
2. Include only events that meaningfully alter state, dynamics, parameters, or policy.
3. Validate nominal trajectories and event order.
4. Add a small, interpretable parameter set.
5. Benchmark representative objective-and-gradient evaluations.
6. Estimate the required number \(K\) of evaluations.
7. Then select cloud hardware and a compute budget.

### Illustrative AWS estimates

Cloud cost should be estimated from measured wall time on representative workloads, not from asymptotics alone.

For any EC2 instance with hourly price \(P_{\mathrm{hr}}\), the raw cost of a single objective-plus-gradient evaluation of duration \(t_{\mathrm{eval}}\) seconds is:

\[
\mathrm{cost/evaluation}
=
\frac{t_{\mathrm{eval}}}{3600}
P_{\mathrm{hr}}.
\]

AWS bills eligible EC2 usage in one-second increments with a 60-second minimum; actual cost depends on the selected region, operating system, instance family, storage, transfer, and purchase model. Use the AWS Pricing Calculator and current regional instance prices before committing to a large run.

For illustration only, if an instance costs:

\[
P_{\mathrm{hr}}=\$0.10/\mathrm{hour},
\]

then:

| Objective + gradient wall time | Raw compute cost |
|---:|---:|
| 1 second | $0.000028 |
| 10 seconds | $0.000278 |
| 1 minute | $0.00167 |
| 10 minutes | $0.0167 |
| 1 hour | $0.10 |

At this illustrative rate:

| Budget | Raw instance-hours | 10-second evaluations | 1-minute evaluations | 10-minute evaluations |
|---:|---:|---:|---:|---:|
| $10 | 100 | 36,000 | 6,000 | 600 |
| $100 | 1,000 | 360,000 | 60,000 | 6,000 |
| $1,000 | 10,000 | 3.6 million | 600,000 | 60,000 |

These are arithmetic upper bounds, not performance guarantees. Real throughput can be lower because of Julia compilation and warm-up, failed integrations, event pathologies, checkpointing, disk I/O, data movement, peak-memory limits, queueing, optimizer overhead, imperfect parallel efficiency, and separately launched short-lived jobs.

For many short tasks, keep workers alive and batch evaluations rather than launching a new instance for every simulation.

### Benchmark before scaling

Before purchasing substantial cloud compute, benchmark a representative objective-and-gradient evaluation with:

- The intended state dimension \(n\);
- The intended parameter dimension \(p\);
- The intended number of guard functions \(G\);
- Representative realized event counts \(m\);
- The intended solver and tolerances;
- The intended stiff/nonstiff treatment;
- Dense, sparse, or matrix-free derivatives;
- The intended forward, adjoint, or multiple-shooting method;
- Realistic data, objective, and output handling.

Record:

- Mean, median, and worst-case wall time;
- Accepted and rejected solver steps;
- Event counts and root-finding iterations;
- Peak memory;
- Event ordering and near-grazing diagnostics;
- Gradient-validation error on test cases;
- Failure rate;
- Parallel scaling efficiency;
- Expected number \(K\) of evaluations.

A nominal simulation that runs quickly can still lead to an impractical workflow if event-aware gradients are slow, optimization requires many restarts, or event sequences are unstable across candidate parameter values.

### Workflow recommendations

#### Exploratory simulation

For exploratory work:

- Prefer low-dimensional, interpretable states;
- Use scheduled events where timing is known;
- Log event times, guards, reset maps, and active modes;
- Plot guards near crossings;
- Perturb parameters slightly to inspect event-order stability;
- Validate event semantics before adding optimization.

#### Local sensitivity analysis

For local sensitivity analysis:

- Begin with a small parameter vector;
- Use directional or forward sensitivities when feasible;
- Compare selected derivatives with perturbation calculations away from guards;
- Record whether perturbations alter event time, count, or ordering;
- Treat grazing and sequence changes as model warnings rather than numerical noise.

#### Parameter estimation and optimization

For estimation and optimization:

- Use constrained low-dimensional parameterizations first;
- Use multiple shooting when long-horizon single shooting is poorly conditioned;
- Validate hybrid derivatives before trusting optimizer convergence;
- Record event sequences at candidate solutions;
- Penalize physically implausible parameter values and pathological switching;
- Use multistart, profile, or alternative-method checks where local minima are plausible.

#### Uncertainty quantification

For uncertainty quantification:

- Recognize that the number of evaluations may dominate cost;
- Parallelize independent trajectories where possible;
- Use sensitivity screening, surrogates, or reduced-order models where justified;
- Track uncertainty in event occurrence and event order, not only uncertainty in continuous parameters;
- Report failure modes and unidentifiable regions explicitly.

#### Policy optimization and control

For policy and control problems:

- Specify what information the policy sees and when;
- Distinguish scheduled from state-triggered actions;
- Include safety, intervention-frequency, and switching costs;
- Test robustness to measurement error, delay, missing data, and parameter uncertainty;
- Validate policies under held-out scenarios and alternative mechanistic assumptions.

### Scope and limitations

`hybrid-ds-julia` is intended to support transparent hybrid ODE models, explicit events, and progressively more sophisticated analysis. It should not imply that every event-rich model admits a stable, meaningful, inexpensive, or globally differentiable gradient.

Extra care is required for:

- Grazing events;
- Chattering or Zeno-like switching;
- Simultaneous events with ambiguous ordering;
- Discontinuous objectives;
- Event-sequence changes under small perturbations;
- Strong stiffness with frequent events;
- High-dimensional dense state models;
- Long-horizon unstable trajectories;
- Poorly measured or weakly identifiable parameters;
- Safety-critical or clinically consequential decision rules.

In these settings, model reduction, sparse or matrix-free methods, hysteresis, regularization, multiple shooting, derivative-free optimization, nonsmooth methods, robust control, or specialized domain software may be more appropriate than a straightforward gradient-based hybrid ODE workflow.

The relevant question is not only whether a model can be simulated once. It is whether its event logic, derivatives, numerical behavior, calibration assumptions, uncertainty, and computational requirements are understood well enough for the intended scientific, engineering, or decision-support use.

## Opportunities for parallelization

Hybrid models often contain substantial parallelism, but the most useful strategy depends on the level at which work is independent. In most applications, the highest-value and lowest-risk parallelism is **across complete trajectories**: different parameter vectors, initial conditions, subjects, experimental scenarios, Monte Carlo draws, optimization starts, or candidate policies can be simulated independently.

This distinction matters because one hybrid trajectory usually has a sequential causal structure. A state-triggered event must be detected before its reset is applied, and the post-event state determines all later continuous evolution and future events. Therefore, a single event-rich trajectory rarely parallelizes as easily as a large collection of independent trajectories.

The recommended order of implementation is:

1. Parallelize independent simulations first.
2. Parallelize objective components, data partitions, or shooting intervals where mathematically valid.
3. Exploit sparse linear algebra and threaded linear solvers inside individual large simulations.
4. Consider GPUs only when the problem has sufficiently many uniform, compatible trajectories or large data-parallel kernels.
5. Use multi-node parallelism only after measuring single-node performance and identifying a genuine scaling bottleneck.

### Parallelism levels

| Level | Parallel work unit | Typical use | Main limitation |
|---|---|---|---|
| Across trajectories | One complete simulation | Ensembles, parameter sweeps, Monte Carlo, multistart optimization | Usually the best first target |
| Across objective terms | Independent subjects, experiments, or data blocks | Population calibration, cross-validation, likelihood evaluation | Shared parameters require reduction of results |
| Across shooting intervals | Segment integrations | Multiple shooting, long horizons | Continuity constraints couple segments |
| Within one solve | Linear algebra, Jacobian products, large RHS evaluations | Large sparse or PDE-discretized models | Event handling remains sequential |
| Across derivative directions | Tangent directions or selected columns | Small batches of directional sensitivities | Memory grows with directions |
| Across optimizer candidates | Population methods, multistart, Bayesian sampling | Global search and robustness studies | Uneven event-rich trajectories cause load imbalance |
| On GPUs | Many compatible trajectories or kernels | Monte Carlo, parameter sweeps, batched small ODEs | Dynamic callbacks and divergent event paths can reduce efficiency |

### Embarrassingly parallel trajectory ensembles

The simplest and often most effective strategy is to run complete hybrid trajectories independently.

Examples include:

- Different parameter vectors in a parameter sweep;
- Different initial conditions;
- Different dose schedules or treatment policies;
- Different adherence realizations;
- Different patients or virtual subjects;
- Different perturbation protocols;
- Different weather, demand, or disturbance realizations;
- Monte Carlo samples;
- Bootstrap replicates;
- Multistart optimization candidates;
- Cross-validation folds;
- Posterior samples or likelihood evaluations;
- Candidate experimental designs.

If trajectory \(k\) solves:

\[
\dot{x}_k=f_{q_k}(x_k,t,\theta_k),
\]

with its own event sequence, initial condition, parameter vector, or random seed, then it can normally run independently of all other trajectories.

If one trajectory has cost \(C_{\mathrm{solve}}\), and there are \(L\) independent trajectories, the total serial work is approximately:

\[
L C_{\mathrm{solve}}.
\]

With \(W\) effective workers, the ideal wall time is:

\[
T_{\mathrm{ideal}}
\approx
\frac{L C_{\mathrm{solve}}}{W}.
\]

Actual speedup is lower because of worker startup and compilation, unequal trajectory runtimes, different event counts, failed trajectories, memory contention, data transfer, result aggregation, and serial portions of optimization or orchestration.

A useful practical model is:

\[
T_{\mathrm{wall}}
\approx
\frac{L\overline{C}_{\mathrm{solve}}}{W}
+
T_{\mathrm{overhead}}
+
T_{\mathrm{imbalance}},
\]

where \(T_{\mathrm{imbalance}}\) reflects the fact that event-rich or stiff trajectories may take much longer than typical trajectories.

### Parallel parameter sweeps and scenario analysis

Parameter sweeps are particularly natural for hybrid models. A user may evaluate:

\[
\theta^{(1)},\theta^{(2)},\ldots,\theta^{(L)},
\]

or different schedules:

\[
u^{(1)}(t),u^{(2)}(t),\ldots,u^{(L)}(t).
\]

Each simulation can include its own event times, guard crossings, and reset sequence.

A treatment-model ensemble may vary initial disease burden, patient-specific PK parameters, adherence patterns, dose intervals, toxicity thresholds, resistance parameters, monitoring schedules, and treatment-switch rules. A locomotion ensemble may vary initial posture, sensory delay, feedback gains, ground-contact parameters, perturbation magnitude, stepping threshold, controller mode, and noise realization.

A parameter sweep is often more informative than optimizing one nominal model because it exposes regions where event count, event order, stability, or feasibility changes.

### Monte Carlo and uncertainty quantification

Monte Carlo simulations are generally trajectory-parallel.

Suppose uncertain parameters or disturbances are sampled as:

\[
\theta^{(k)}\sim\pi(\theta),
\qquad
k=1,\ldots,L.
\]

For each sample, a hybrid trajectory produces an output:

\[
y^{(k)}
=
\mathcal{H}\bigl(x^{(k)},q^{(k)},\theta^{(k)}\bigr).
\]

The resulting ensemble can estimate quantities such as:

\[
\mathbb{E}[y],
\qquad
\mathrm{Var}(y),
\qquad
\Pr(y\in\mathcal{A}),
\]

or the probability that a threshold, treatment hold, failure event, or unsafe state occurs.

Hybrid uncertainty quantification should report discrete uncertainty as well as continuous uncertainty. Useful outputs include:

- Probability that a treatment hold occurs;
- Distribution of event times;
- Probability of a specific event sequence;
- Probability of a controller mode switch;
- Probability of treatment failure;
- Distribution of event count;
- Probability that a trajectory enters a chattering regime.

For large ensembles, workers should use dynamic scheduling rather than equal-sized static blocks when trajectory costs are highly variable.

### Parallel multistart and population optimization

Many hybrid optimization problems are nonconvex because of nonlinear dynamics, multiple modes, threshold decisions, event-sequence changes, discontinuous feasibility boundaries, parameter nonidentifiability, or multiple stable attractors.

A robust workflow often uses multiple starting points:

\[
\theta_0^{(1)},\ldots,\theta_0^{(L)}.
\]

Each local optimization can run independently until its results are collected and compared.

This is an attractive use of distributed compute because the principal coupling occurs only at the beginning and end of each optimization run.

Examples include:

- Multistart parameter estimation;
- Comparing treatment-policy parameterizations;
- Searching controller-gain spaces;
- Optimizing alternative experimental protocols;
- Population-based evolutionary algorithms;
- Particle-swarm or CMA-ES style methods;
- Bayesian optimization with batch candidate evaluation;
- Independent MCMC chains.

For a population-based optimizer with \(L\) candidates per generation, the evaluation stage is often parallel:

\[
\mathcal{L}\bigl(\theta^{(1)}\bigr),
\ldots,
\mathcal{L}\bigl(\theta^{(L)}\bigr).
\]

The update from one generation to the next is usually synchronized, so the speedup depends on the slowest candidate evaluation in each generation.

### Parallel likelihoods, subjects, and experiments

Many inference objectives decompose across independent data units.

Suppose a shared parameter vector \(\theta\) is fitted to data from \(S\) subjects, experiments, sites, or trials:

\[
\mathcal{L}(\theta)
=
\sum_{s=1}^{S}
\mathcal{L}_s(\theta).
\]

If each subject or experiment has a conditionally independent trajectory:

\[
\dot{x}_s=f_{q_s}(x_s,t,\theta,\eta_s),
\]

then objective and gradient contributions can be computed independently:

\[
\mathcal{L}_s(\theta),
\qquad
\nabla_\theta\mathcal{L}_s(\theta).
\]

They are then reduced:

\[
\mathcal{L}(\theta)
=
\sum_{s=1}^{S}\mathcal{L}_s(\theta),
\]

\[
\nabla_\theta\mathcal{L}(\theta)
=
\sum_{s=1}^{S}\nabla_\theta\mathcal{L}_s(\theta).
\]

This is appropriate for population PK/PD analyses, multiple virtual patients, treatment arms, replicated animal experiments, movement trials, environmental sites, production batches, or building units.

Care is required if the model contains shared latent variables, global resource constraints, coupling among subjects, or a hierarchical statistical model that requires joint inference. In that case, simulation may still be parallel, but the inference or likelihood-reduction step may be more complicated.

### Multiple shooting and time-domain decomposition

Multiple shooting introduces a natural but limited form of time-domain parallelism.

Let the interval:

\[
[t_0,T]
\]

be divided into \(r\) shooting segments:

\[
[t_0,t_1],
[t_1,t_2],
\ldots,
[t_{r-1},T].
\]

Given tentative shooting-node states:

\[
z_0,z_1,\ldots,z_{r-1},
\]

the segment flows:

\[
\Phi_i(z_i,\theta)
\]

can be integrated independently.

The continuity residuals:

\[
c_i
=
\Phi_i(z_i,\theta)-z_{i+1}
\]

are then assembled.

This yields a parallel pattern:

1. Distribute segment integrations.
2. Compute local trajectory outputs and local derivative information.
3. Assemble continuity constraints and objective contributions.
4. Solve the coupled optimization or linearized correction problem.
5. Update shooting nodes and repeat.

The continuous segment solves parallelize, but the nonlinear-programming or linear-system solve that reconciles all continuity constraints remains coupled.

Multiple shooting can reduce wall time for large problems only if each segment is computationally substantial, communication and assembly overhead are modest, the optimizer exploits block sparsity, and event handling within each segment remains stable. It is not automatically beneficial for short inexpensive trajectories.

### Parallel directional derivatives

A full forward sensitivity matrix has shape:

\[
S_\theta
=
\frac{\partial x}{\partial\theta}
\in\mathbb{R}^{n\times p}.
\]

The \(p\) columns correspond to parameter directions. In principle, subsets of those columns can be propagated in parallel.

If the parameter set is divided into \(B\) blocks:

\[
\theta=
\left(
\theta^{[1]},
\theta^{[2]},
\ldots,
\theta^{[B]}
\right),
\]

then sensitivity blocks can be computed separately:

\[
S_\theta
=
\left[
S^{[1]}
\;
S^{[2]}
\;
\cdots
\;
S^{[B]}
\right].
\]

This can be useful when the state dimension is moderate, the parameter count is larger than one worker can handle efficiently, the event sequence is fixed and reproducible, and memory is sufficient.

However, this is often not the first parallelization target. Trajectory-level parallelism is usually simpler and has lower communication requirements.

A full state-transition matrix:

\[
\Phi(t,t_0)\in\mathbb{R}^{n\times n}
\]

can likewise be computed by propagating blocks of tangent directions. But if a dense full \(\Phi\) is required, the total amount of arithmetic remains large:

\[
O(n^3)
\]

for dense matrix-matrix updates at an event. Parallelism reduces wall time only if memory bandwidth, communication, and dense-linear-algebra implementation scale effectively.

### Parallelism inside one large trajectory

A single large hybrid trajectory may benefit from internal parallelism when continuous dynamics are high dimensional.

Possible sources include:

- Threaded right-hand-side evaluation;
- Sparse Jacobian construction;
- Parallel Jacobian-vector products;
- Parallel residual evaluation;
- Threaded sparse linear solves;
- Multithreaded dense BLAS/LAPACK operations;
- Parallel PDE spatial discretizations;
- GPU kernels for large vectorized state updates;
- Parallel observation-model evaluation;
- Parallel objective contributions at measurement times.

This form of parallelism is most promising when \(n\) is large and continuous-state updates have substantial arithmetic intensity.

It is less useful for small ODE systems with frequent scalar event logic. In that setting, synchronization, branching, cache effects, and task overhead can exceed the work performed per step.

Hybrid events constrain within-trajectory parallelism because they establish a temporal dependency:

\[
x(t^-)
\rightarrow
\text{event detection}
\rightarrow
x(t^+)
\rightarrow
\text{future trajectory}.
\]

No later segment of the same single-shooting trajectory can be finalized until event state and mode are known.

### Shared-memory threading

Julia supports shared-memory multithreading: multiple tasks may execute simultaneously on CPU threads while sharing one process memory space.

Shared-memory threading is appropriate when model data are naturally shared, trajectory calculations are relatively small, communication overhead should be minimal, or many independent simulations fit on one machine.

Important implementation considerations include:

- Avoid mutation of shared arrays from multiple trajectories;
- Give each trajectory independent state, cache, random-number generator, and output storage;
- Avoid global mutable state in callback functions;
- Do not rely on callback execution order across trajectories;
- Use reproducible per-trajectory random seeds when stochastic perturbations are present;
- Check whether the ODE solver, linear solver, and BLAS libraries are already using threads to avoid oversubscription.

Oversubscription occurs when outer trajectory threading and inner linear algebra threading both attempt to use all available cores. Benchmark combinations deliberately.

### Distributed-memory parallelism

Julia also supports distributed computing with multiple processes that have separate memory spaces. These processes can run on one machine or across multiple machines.

Distributed processes are appropriate when individual trajectories are moderately expensive, memory requirements exceed a single process or node, many simulations must run independently, failure isolation is useful, or a cluster or cloud environment is available.

Distributed execution introduces additional requirements:

- Serialize or package model code and dependencies consistently;
- Move only necessary data to workers;
- Avoid repeatedly transferring large immutable input data;
- Aggregate small summaries rather than complete time-series trajectories when possible;
- Save detailed trajectories to worker-local or object storage only when needed;
- Record package versions, solver options, random seeds, and hardware metadata;
- Design jobs to tolerate worker failure and restart.

For cloud runs, independent-trajectory workloads are usually better candidates for distributed parallelism than tightly coupled single-trajectory time-domain decomposition.

### GPU opportunities and limitations

GPUs are most attractive when many trajectories have similar numerical structure and can run in a batched, data-parallel fashion.

Good GPU candidates include:

- Large Monte Carlo ensembles;
- Parameter sweeps;
- Large collections of short, similarly structured trajectories;
- Batched initial-condition studies;
- GPU-compatible neural ODE or surrogate components;
- High-dimensional vectorized state updates;
- Large sparse or dense linear-algebra kernels;
- Ensemble uncertainty quantification.

Hybrid event logic creates GPU-specific challenges:

- Different trajectories may experience different event counts;
- Different trajectories may cross different guards;
- Root-finding iterations may differ;
- Branching can cause warp divergence;
- Dynamic allocation and arbitrary callback logic may not compile or perform well on GPU hardware;
- Event sequences may create irregular memory access;
- Some solvers, callbacks, AD paths, and linear algebra routines may not be GPU compatible.

Therefore, GPU acceleration should be treated as a later optimization step, not a default assumption.

> GPUs are most promising for large ensembles of similar trajectories with predictable event structure. CPUs are often simpler and more robust for a small number of irregular, stiff, event-rich trajectories.

### Load balancing for event-rich ensembles

Hybrid ensembles often have variable trajectory cost.

One trajectory might have:

\[
m=0
\]

events and finish quickly. Another may have:

\[
m\gg 1,
\]

many rejected steps, stiffness, a near-grazing threshold, or chattering. Static assignment of the same number of simulations to each worker can leave some workers idle while one worker processes difficult cases.

Use dynamic scheduling when run times vary substantially:

- Queue individual trajectories or small batches;
- Allow idle workers to request additional work;
- Use work-stealing or dynamic map scheduling where appropriate;
- Group simulations with similar expected cost only if that cost can be predicted reliably;
- Treat solver failures and event pathologies as first-class outcomes to log and reschedule or analyze.

For Monte Carlo work, collecting only summary statistics can improve scaling:

\[
\left(
\text{objective},
\text{event count},
\text{event times},
\text{terminal state},
\text{failure code}
\right),
\]

rather than retaining every state value at every solver time point for every realization.

### Reproducibility under parallel execution

Parallel execution can make results harder to reproduce unless the workflow is designed carefully.

For each trajectory, record:

- A deterministic trajectory identifier;
- Parameter vector;
- Initial condition;
- Random seed or random-number-generator state;
- Solver and tolerance configuration;
- Event/callback configuration;
- Package and Julia versions;
- Hardware and worker information;
- Event log;
- Outcome status and failure diagnostics.

A robust strategy is to derive a per-trajectory seed from a master seed and trajectory identifier:

\[
\mathrm{seed}_k
=
h(\mathrm{master\ seed},k),
\]

where \(h\) is a deterministic hash or seed-generation rule.

Do not rely on the order in which parallel tasks happen to finish. Completion order can vary across machines and runs even when individual numerical calculations are deterministic.

### AWS Batch and cloud orchestration

For large independent trajectory ensembles, AWS Batch array jobs are a natural cloud-execution pattern. An array job creates multiple child jobs from one submission; each child job can use its assigned array index to select a parameter block, replicate, optimization start, or simulation batch.

A practical array-job design is:

1. Build a container with a fixed Julia version, project environment, model code, and scripts.
2. Store immutable input data and parameter grids in object storage or package them with the job.
3. Assign each child job a deterministic subset of trajectory indices.
4. Write per-job summaries, diagnostics, and optional detailed outputs.
5. Run a final aggregation job after the array completes.
6. Record the container image digest, git commit, package manifest, and random-seed policy.

Multi-node parallel jobs are possible when one tightly coupled computation must span multiple machines, but they require distributed-communication libraries and more complex orchestration. They are generally not the first choice for independent hybrid trajectories.

### Parallelization strategy by workflow

| Workflow | Best first parallelization target | Usually avoid first |
|---|---|---|
| Parameter sweep | Independent parameter vectors | Distributed full state-transition matrices |
| Monte Carlo uncertainty analysis | Independent random draws | GPU use before checking event divergence |
| Population PK/PD simulation | Virtual patients or subjects | One tightly coupled multi-node solve |
| Multistart calibration | Independent starts | Parallelizing every small derivative column |
| Bayesian sampling | Independent chains or batched proposals | Shared mutable likelihood state |
| Multiple shooting | Segment solves and subject-level data blocks | Excessive segmentation of cheap trajectories |
| Large stiff sparse model | Threaded/sparse internal linear algebra | GPU migration without compatibility testing |
| Policy optimization | Candidate policies and scenarios | Assuming a single trajectory can be time-parallelized |
| Experimental design | Candidate designs and simulated replicates | Retaining every full trajectory unnecessarily |

### Recommended implementation sequence

A practical staged plan is:

1. **Make one trajectory correct.** Validate continuous dynamics, guard functions, reset maps, event ordering, and diagnostics.
2. **Make one trajectory reproducible.** Fix solver settings, seeds, data versions, and output schema.
3. **Benchmark one trajectory.** Measure wall time, memory, accepted/rejected steps, event count, and output size.
4. **Run a small threaded ensemble.** Test 2, 4, and 8 workers. Confirm numerical reproducibility and absence of shared-state errors.
5. **Measure speedup and memory.** Compare observed speedup with ideal scaling. Inspect whether event-rich trajectories create load imbalance.
6. **Move independent work to distributed processes or cloud jobs.** Do this when trajectories are expensive enough to justify process, machine, or container overhead.
7. **Consider GPU execution only after profiling.** Confirm that callbacks, event structure, solver choice, and model code are compatible and that trajectories are sufficiently uniform.
8. **Consider multi-node coupled parallelism only for proven bottlenecks.** Use it for large structured problems whose internal linear algebra or multiple-shooting formulation genuinely requires it.

### Scope and limitations

Parallelism reduces wall-clock time when work is independent or can be decomposed with limited communication. It does not remove underlying arithmetic, memory, event-handling, or numerical-conditioning costs.

In hybrid systems, the main limitations are structural:

- Events within one trajectory create temporal dependencies;
- Grazing and chattering can make some trajectories much more expensive than others;
- Event-sequence changes can complicate derivative calculations;
- GPU efficiency can fall when trajectories diverge in branches, event counts, or root-finding paths;
- Multiple shooting makes segment propagation parallel but retains globally coupled continuity constraints;
- Distributed computing adds serialization, scheduling, data-transfer, and reproducibility responsibilities.

The best initial use of parallel computing in `hybrid-ds-julia` is therefore likely to be reproducible ensembles of independent trajectories. More tightly coupled parallel methods should be introduced only where benchmarking shows that they solve a meaningful computational bottleneck.
