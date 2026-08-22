## Mathematical approach

`hybrid-ds-julia` is intended for mechanistic dynamical models in which continuous-time evolution is interrupted or altered by explicit discrete events. The central modeling task is to make both components first-class objects: users specify the continuous right-hand side, the conditions under which events occur, the state or parameter updates caused by those events, and the quantities to be analyzed, calibrated, or optimized.

The package is motivated by models such as PK/PD and QSP systems with repeated dosing, treatment holds, toxicity thresholds, therapy switches, missed doses, adherence scenarios, and measurement-driven policies. The same mathematical structure applies more broadly to biological, clinical, industrial, ecological, and engineered systems.

Stochastic event processes, multistate transition intensities, and neural jump extensions are considered as longer-term research directions in the AI/ML and mathematical extensions section. The deterministic ODE-and-event framework described here remains the core numerical and methodological foundation for those possible extensions.

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

Multiple shooting divides the horizon into \(r\) intervals. Each interval receives its own initial state \(z_j\). The numerical problem enforces continuity or hybrid transition consistency between intervals.

For interval \(j\), let:

\[
x_j(t_j)=z_j,
\]

and let \(\varphi_j(z_j,\theta)\) denote the event-aware flow to the end of that interval. A standard continuity constraint is:

\[
c_j(z_j,z_{j+1},\theta)
=
\varphi_j(z_j,\theta)-z_{j+1}
=
0.
\]

If a known event lies at an interval boundary, the constraint must incorporate the corresponding reset map:

\[
c_j(z_j,z_{j+1},\theta)
=
R_j\left(\varphi_j(z_j,\theta),\theta\right)-z_{j+1}
=
0.
\]

Multiple shooting can improve conditioning because local trajectory errors do not compound unchecked over the entire horizon. It can also expose problematic intervals, support parallel propagation of segments, and provide a natural structure for event-aware optimization.

Its costs include additional decision variables, continuity constraints, Jacobian blocks, nonlinear-programming overhead, and more complex handling of events that move across interval boundaries as parameters change.

### Event count, event structure, and tractability

Event count matters, but not all events have the same computational cost or scientific risk.

#### Scheduled events

Scheduled events have known times. Their sequence is usually fixed, and their primary costs are reset execution, solver reinitialization, and derivative propagation through the reset map.

For a model with \(m_s\) scheduled events, repeated monthly doses, planned inspections, or known input changes may be computationally manageable even when \(m_s\) is large, provided the resets are simple and the continuous dynamics are well conditioned.

#### State-triggered events

State-triggered events require guard evaluation and root localization. Their timing and ordering can change with parameters, initial conditions, or controls.

Let \(m_g\) be the number of realized state-triggered events. Their cost is approximately included in:

\[
m_g C_{\mathrm{root}}.
\]

But their practical impact may be much larger near grazing, simultaneous crossings, or chattering. A modest number of difficult state-triggered events can be more problematic than many scheduled events.

#### Guard count versus realized event count

A model may define many possible guards even if only a few fire during one trajectory. Let \(G\) denote the number of guards checked. Guard evaluation can become nontrivial when:

- \(G\) is large;
- Each guard depends on expensive derived quantities;
- Guards require communication across distributed components;
- Many guards become nearly active at once;
- Root-finding repeatedly evaluates a large guard set.

The package should distinguish **defined guards**, **active guards**, and **realized events** in diagnostic output.

#### Chattering and Zeno-like behavior

A model can generate repeated events in a short interval. Examples include a treatment rule that immediately reactivates after a hold, a relay controller without hysteresis, or a mechanical contact model with repeated impacts.

A rough warning sign is a rapidly growing event count:

\[
m(t+\Delta t)-m(t)\gg 1
\]

for a very small \(\Delta t\).

The package should provide safeguards such as:

- Hysteresis recommendations;
- Minimum dwell times;
- Event-count limits;
- Diagnostics for repeated same-time events;
- Explicit reporting of solver termination due to event pathology.

### Dimension-specific planning guide

The following guidance is deliberately approximate. Actual cost depends on stiffness, sparsity, solver choice, event geometry, data volume, objective complexity, and implementation quality.

| State dimension | Typical use | Recommended initial strategy | Main risks |
|---:|---|---|---|
| \(n < 20\) | Small PK/PD, tumor--immune, control, or teaching models | Direct event-aware simulation; forward sensitivities; finite perturbation checks; small multistart studies | Overconfidence in gradients near event changes; under-tested event semantics |
| \(20 \leq n < 100\) | Moderate QSP, physiological, engineering, or process models | Exploit sparsity if present; directional sensitivities; selected forward sensitivities; careful solver benchmarking | Dense sensitivity propagation becomes expensive; event logs become harder to inspect manually |
| \(100 \leq n < 1{,}000\) | Larger QSP, network, discretized, or multicomponent models | Sparse Jacobians; matrix-free products; adjoints for scalar objectives; multiple shooting when needed | Stiffness, memory, event-adjoint complexity, expensive calibration loops |
| \(n \geq 1{,}000\) | Large networks, spatial discretizations, multiscale or ensemble systems | Sparse/structured methods; reduced-order modeling; surrogate models; HPC or cloud ensembles; avoid full dense matrices | Full \(n^2\) objects become infeasible; dense saltation matrices and full sensitivities are generally not practical |

The same table must be interpreted jointly with parameter count \(p\), event count \(m\), and the number of repeated solves required. A 50-state model with 10,000 parameters or 1,000 costly events may be harder than a sparse 500-state model with a handful of parameters and scheduled events.

### Fixed-budget planning

Before launching a large study, define the available compute budget:

\[
B_{\mathrm{wall}},
\qquad
B_{\mathrm{CPU}},
\qquad
B_{\mathrm{memory}},
\qquad
B_{\mathrm{cost}}.
\]

These represent limits on wall-clock time, aggregate CPU or GPU time, memory, and financial cost.

If one evaluation costs approximately \(C_{\mathrm{eval}}\) seconds of compute, then a serial study can perform roughly:

\[
N_{\mathrm{eval}}
\approx
\frac{B_{\mathrm{CPU}}}{C_{\mathrm{eval}}}.
\]

With \(w\) workers and parallel efficiency \(\eta\in(0,1]\), the wall-clock estimate is:

\[
T_{\mathrm{wall}}
\approx
\frac{N_{\mathrm{eval}}C_{\mathrm{eval}}}{\eta w}.
\]

A realistic study must account for:

- Initial compilation and environment setup;
- Failed simulations;
- Data loading and checkpointing;
- Optimization iterations that terminate early or require restarts;
- Heterogeneous trajectory cost across parameter sets;
- Worker imbalance;
- Debugging and benchmark time.

#### Example planning workflow

1. Run a nominal event-aware solve.
2. Measure elapsed time, allocations, accepted steps, rejected steps, event count, and root-finding diagnostics.
3. Repeat for representative parameter sets, including stiff, near-threshold, and high-event scenarios.
4. Measure the cost of the derivative method actually intended for use.
5. Estimate the number of solves required by calibration, uncertainty analysis, optimization, or policy search.
6. Add a contingency factor before provisioning compute.

A reasonable early contingency factor may be 2--10x, depending on uncertainty in event behavior and solver robustness.

### Illustrative AWS estimates

Cloud costs vary substantially by region, instance type, operating system, pricing model, storage, data transfer, and date. The following examples are planning illustrations rather than current quotes.

Suppose a model requires 30 seconds for one event-aware forward solve on one CPU core, and a calibration workflow requires 20,000 solves. The raw serial compute requirement is:

\[
20{,}000\times 30\ \mathrm{s}
=
600{,}000\ \mathrm{s}
\approx 167\ \mathrm{CPU\ hours}.
\]

With 32 effective workers and 75% parallel efficiency:

\[
T_{\mathrm{wall}}
\approx
\frac{167}{32\times 0.75}
\approx 7\ \mathrm{hours}.
\]

If a particular compute configuration costs, for illustration, \$1.50 per instance-hour and uses four such instances for approximately seven hours, the rough compute charge would be:

\[
4\times 7\times \$1.50
=
\$42.
\]

This calculation excludes storage, orchestration, data transfer, failed jobs, retries, and the cost of development time. It also assumes the workload parallelizes well.

For a gradient-based calibration with an adjoint cost of roughly five forward solves per objective evaluation, the compute demand could rise substantially. If 1,000 optimization iterations each require one objective-and-gradient evaluation, and each costs 150 seconds, then:

\[
1{,}000\times 150\ \mathrm{s}
\approx 42\ \mathrm{CPU\ hours}.
\]

This may still be modest on a cloud cluster, but only if event handling, checkpointing, and adjoint replay are stable. In practice, implementation and validation effort may dominate raw compute cost.

### Benchmark before scaling

A package intended for serious hybrid-model workflows should include benchmark cases that vary at least:

- State dimension \(n\);
- Parameter dimension \(p\);
- Number of scheduled events;
- Number and conditioning of state-triggered events;
- Stiff versus nonstiff dynamics;
- Sparse versus dense Jacobian structure;
- Local versus global reset maps;
- Smooth versus near-grazing event geometry;
- Single shooting versus multiple shooting;
- Forward versus adjoint derivative tasks.

Each benchmark should report more than wall-clock time. Useful outputs include:

- Solver and tolerance configuration;
- Accepted and rejected steps;
- Event count and event types;
- Root-finding calls or diagnostics where available;
- Memory allocation;
- Derivative-check error away from event-sequence changes;
- Failure mode if the solve or derivative calculation is not valid;
- Hardware and software versions.

### Workflow recommendations

For small models, prioritize correctness, interpretability, and derivative validation before optimization.

For medium models, exploit structure early: sparse Jacobians, local resets, selected sensitivity directions, and carefully chosen observation models.

For large models, avoid default dense formulations. Do not propagate full state-transition matrices or dense parameter-sensitivity matrices unless the problem size demonstrably permits them. Prefer matrix-free products, sparse methods, adjoints for scalar objectives, reduced-order representations, and parallel trajectory ensembles.

For all scales, treat the event sequence as a scientific output. A fast optimization result is not useful if it relies on unstable event ordering, unresolved chattering, poorly localized guard crossings, or a model whose intervention logic is not interpretable.

## Opportunities for parallelization

Hybrid models offer several forms of parallelism, but event handling changes which strategies are effective. The most reliable parallelism is usually across independent trajectories or independent optimization starts. Parallelizing within one event-rich trajectory is more difficult because each event can depend on the preceding continuous state, event time, and mode.

### Parallelism levels

A hybrid-model workflow can often be decomposed at several levels:

1. **Across independent parameter sets:** multistart calibration, profile likelihoods, parameter sweeps, and global sensitivity studies.
2. **Across uncertainty samples:** Monte Carlo trajectories, virtual-patient cohorts, bootstrap replicates, or stochastic realizations.
3. **Across candidate policies:** dose schedules, thresholds, monitoring rules, or controller settings.
4. **Across multiple-shooting intervals:** subject to continuity constraints and event-boundary handling.
5. **Within linear algebra kernels:** sparse factorizations, Jacobian-vector products, adjoint operations, and batched neural-network evaluations.
6. **Across independent models or scenarios:** different mechanisms, disease subtypes, interventions, or data splits.

The first three are often embarrassingly parallel and should be the first targets for scaling.

### Embarrassingly parallel trajectory ensembles

Suppose \(M\) independent trajectories must be simulated, each with average cost \(C_{\mathrm{solve}}\). The serial cost is:

\[
C_{\mathrm{serial}}
\approx
M C_{\mathrm{solve}}.
\]

With \(w\) workers and efficiency \(\eta\), the wall time is approximately:

\[
T_{\mathrm{wall}}
\approx
\frac{M C_{\mathrm{solve}}}{\eta w}.
\]

Examples include:

- Virtual-patient simulations across sampled parameter sets;
- Dose-response grids;
- Alternative adherence scenarios;
- Threshold-policy comparisons;
- Cross-validation folds;
- Bootstrap resampling;
- Randomized initial conditions;
- Independent experimental designs.

The main engineering requirements are reproducible random-number streams, structured result collection, failure handling, and logging of event summaries for each trajectory.

### Monte Carlo and uncertainty quantification

For uncertainty quantification, each sample may produce a different event sequence. This is scientifically important: uncertainty can change not only continuous outcomes but also whether a treatment hold occurs, which event happens first, or whether a threshold is ever reached.

A useful output is therefore not only a distribution of terminal states but also distributions of:

- Event counts;
- Event times;
- Mode occupancy times;
- Probability of each event type;
- Probability of a clinically or operationally relevant event sequence;
- Constraint violations;
- Policy switching frequency.

Parallel Monte Carlo is usually straightforward, but rare events may require variance-reduction methods, importance sampling, splitting methods, or carefully designed scenario analysis.

### Parallel multistart and population optimization

Global optimization and calibration often require many candidate evaluations. These are natural candidates for distributed execution:

- Random multistart local optimization;
- Evolutionary algorithms;
- Particle-based methods;
- Bayesian optimization batches;
- Population Monte Carlo;
- Approximate Bayesian computation;
- Profile likelihoods;
- Parameter grids or Latin-hypercube designs.

Hybrid models add a complication: two candidate parameter sets may generate different event sequences, so the objective landscape can be nonsmooth or piecewise smooth. Parallel evaluation remains useful, but optimization diagnostics should record event-sequence changes and solver failures rather than treating all objective evaluations as equivalent.

### Multiple shooting and time-domain decomposition

Multiple shooting can expose parallelism because each interval propagation can be performed separately once its interval-initial state is specified. However, the intervals are coupled by continuity constraints and event maps.

For \(r\) intervals, one can evaluate:

\[
\varphi_1(z_1,\theta),
\ldots,
\varphi_r(z_r,\theta)
\]

in parallel, then assemble the continuity constraints.

This can be attractive for long trajectories, unstable systems, or parameter-estimation problems with many observation intervals. But event times that move across interval boundaries complicate the formulation. A robust implementation should either:

- Place known scheduled events at fixed interval boundaries;
- Allow event-aware interval propagation with clear ownership rules; or
- Adaptively redefine intervals while tracking derivative consequences.

### GPU opportunities and limitations

GPUs can be useful when a workflow consists of many similar, independent, moderately sized trajectories or large batched neural-network evaluations. Potential applications include:

- Large virtual-patient ensembles;
- Batched surrogate-model evaluation;
- Neural differential-equation components;
- Fixed-step or regularly structured simulation kernels;
- Large matrix operations arising in learned models.

GPU acceleration is less straightforward when:

- Each trajectory has a different event count or event sequence;
- Root finding creates irregular control flow;
- Adaptive time stepping varies widely across samples;
- Resets require dynamic memory allocation or complex branching;
- The model is small and host-device transfer dominates;
- Sparse linear algebra is irregular or poorly supported.

A practical strategy is often hybrid: run event-rich trajectory orchestration on CPUs while using GPUs for batched smooth computations, neural components, or large ensembles with similar structure.

### AWS Batch and cloud orchestration

For large independent workloads, cloud orchestration can separate the scientific model from the execution layer. A typical pattern is:

1. Package the Julia environment and model code in a reproducible container.
2. Define one job input per parameter set, uncertainty sample, policy, or optimization start.
3. Submit jobs to a managed batch system.
4. Write structured results and event logs to durable storage.
5. Aggregate successful and failed jobs separately.
6. Reproduce selected runs locally or in a controlled environment.

Cloud execution should record:

- Git commit or package version;
- Julia and dependency versions;
- Solver and tolerance settings;
- Random seed or stream identifier;
- Input parameter set;
- Hardware or instance type;
- Wall time and memory use;
- Event summary;
- Failure status and diagnostic output.

The package itself need not implement cloud infrastructure in its first version. It should, however, make independent simulations reproducible, serializable, and easy to invoke from scripts or workflow managers.
