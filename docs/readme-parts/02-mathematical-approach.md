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
