## Original crop-science motivation

The project originally grew from an interest in crop-growth, canopy-competition, and trait-optimization models. That motivation remains relevant because plant and crop systems often combine smooth biological growth processes with discrete environmental and management events.

Examples include:

- planting and harvest dates,
- irrigation and fertilization pulses,
- pruning and thinning,
- pest-control interventions,
- greenhouse temperature or light schedules,
- drought and heat-stress events,
- developmental-stage transitions,
- and sensor-triggered management decisions.

A crop model may represent biomass accumulation, canopy development, competition for light, water uptake, nutrient dynamics, and reproductive allocation as continuous processes. Yet the outcomes of practical interest—yield, resilience, resource efficiency, and trait value—may depend strongly on the timing of discrete interventions.

For example, a plant-growth model may include biomass \(W\), leaf area or canopy state \(L\), soil-water availability \(M\), and nutrient availability \(N\):

\[
\dot{W}
=
\alpha L
\frac{M}{K_M+M}
\frac{N}{K_N+N}
-
\delta_W W,
\]

\[
\dot{L}
=
g_L(W,L)
-
\delta_L L,
\]

\[
\dot{M}
=
I(t)
-
u_M(W,L,M)
-
\ell_M(M),
\]

\[
\dot{N}
=
F(t)
-
u_N(W,L,N)
-
\ell_N(N).
\]

Here, \(I(t)\) and \(F(t)\) may include irrigation and fertilizer interventions. At selected event times, the model may apply impulsive updates:

\[
M(t_k^+)
=
M(t_k^-)
+
\Delta M_k,
\]

\[
N(t_k^+)
=
N(t_k^-)
+
\Delta N_k.
\]

The system can also include state-triggered rules. For example, irrigation may occur when soil moisture crosses a lower threshold:

\[
M(t)
\leq
M_{\mathrm{trigger}}.
\]

In a more advanced setting, the intervention policy may depend on developmental stage, weather forecasts, crop stress indicators, or competing resource constraints.

This type of model is structurally similar to the QSP and PK/PD systems emphasized elsewhere in the repository:

- continuous states evolve according to mechanistic differential equations,
- scheduled interventions introduce jumps or changes in forcing,
- threshold conditions trigger mode changes,
- and the timing of events affects long-term outcomes.

The crop-science examples remain useful because they provide intuitive applications for multiple shooting, event-aware sensitivities, and optimization. A crop-management problem can be stated in terms of measurable outcomes such as yield, water use, fertilizer efficiency, or resilience to stress, while still presenting the same numerical challenges that appear in treatment-schedule optimization.

## Software plan

The initial software plan is deliberately narrow. The package should establish a reliable deterministic hybrid core before expanding toward broad model coverage, sophisticated inference, or AI-enabled extensions.

The first implementation should build on Julia’s existing scientific-computing ecosystem rather than recreating solver infrastructure. The package should focus on reusable abstractions for hybrid model specification, event-aware sensitivity propagation, shooting formulations, and user-facing analysis workflows.

The intended design principles are:

- preserve compatibility with existing Julia differential-equation tooling where practical,
- represent event logic explicitly rather than burying it inside ad hoc callbacks,
- distinguish scheduled events from state-triggered events,
- support reset maps and mode changes as first-class model components,
- expose event-aware sensitivities in a form suitable for optimization and inference,
- provide clear diagnostics when trajectories approach grazing or ill-conditioned event configurations,
- and make examples reproducible enough to serve as scientific benchmarks.

A possible early API could allow users to define:

\[
\mathcal{H}
=
\{
\mathcal{Q},
f_q,
h_{q\rightarrow q'},
R_{q\rightarrow q'},
\mathcal{E}_{\mathrm{scheduled}}
\},
\]

where:

- \(\mathcal{Q}\) is a set of modes,
- \(f_q\) is the continuous vector field in mode \(q\),
- \(h_{q\rightarrow q'}\) is an event or guard function,
- \(R_{q\rightarrow q'}\) is a reset map,
- and \(\mathcal{E}_{\mathrm{scheduled}}\) contains scheduled intervention events.

A modeler should be able to specify a system in terms close to the scientific problem:

- what states evolve continuously,
- what interventions occur at fixed times,
- what thresholds trigger a transition,
- how the state changes at each event,
- and what outcomes should be optimized or analyzed.

The package can then construct the numerical machinery required for simulation and sensitivity propagation.

The first user-facing capabilities should include:

- deterministic simulation of hybrid ODE models,
- scheduled event handling,
- state-triggered event detection,
- reset maps and mode transitions,
- continuous variational equations between events,
- saltation or jump-sensitivity updates at events,
- trajectory diagnostics,
- and simple multiple-shooting formulations.

The first examples should prioritize clarity over biological scope. A user should be able to inspect a compact model, run a schedule comparison, visualize event times, compute sensitivities, and understand why the event-aware method differs from a finite-difference perturbation workflow.

Potential supporting components include:

- data structures for modes, events, guards, reset maps, and scheduled interventions,
- wrappers around standard Julia ODE and callback functionality,
- utilities for propagating state-transition and parameter-sensitivity matrices,
- multiple-shooting problem construction,
- continuation or parameter-sweep helpers,
- plotting utilities for trajectories, event times, modes, and sensitivity diagnostics,
- and benchmark scripts that compare hybrid-aware derivatives with finite-difference approximations.

The design should remain modular. A modeler interested only in accurate simulation should not be required to use multiple shooting. A user interested in schedule optimization should be able to build on the same event abstractions without rewriting the model. Future AI, Bayesian, and stochastic extensions should reuse the same representation of known scheduled events, state-triggered transitions, and reset maps.

Interoperability is also an important longer-term design goal. Many QSP and PK/PD models already exist in established ecosystems, and their value should not be lost when hybrid analysis is needed. The package should eventually support import, export, or translation pathways for model structures and dosing/event specifications associated with tools such as NONMEM, nlmixr2/RxODE, Pumas, and related pharmacometric workflows.

The package does not need to solve every interoperability problem in its first release. An initial milestone could focus on clear, documented pathways for recreating a limited class of models or event schedules. Later stages can expand toward more automated translation, validation against reference simulations, and bidirectional exchange of model definitions or simulation outputs.

The immediate objective is to demonstrate a complete and credible workflow, not to maximize feature count:

1. Define a hybrid mechanistic model.
2. Simulate it accurately across scheduled and state-triggered events.
3. Propagate sensitivities through those events.
4. Use the resulting derivatives in schedule, parameter, or boundary-value analysis.
5. Compare the results with simpler finite-difference or single-shooting approaches.
6. Document where hybrid-aware methods materially improve reliability, conditioning, or interpretability.
