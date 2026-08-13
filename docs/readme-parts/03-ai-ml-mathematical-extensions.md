## AI/ML mathematical extensions

The deterministic hybrid framework is intended to remain useful on its own. However, a natural longer-term direction is to combine mechanistic QSP and PK/PD models with machine-learning components when biological structure is partly known but key interactions, patient-specific effects, or unresolved mechanisms are not.

The goal is not to replace mechanistic pharmacology with black-box prediction. Instead, the opportunity is to preserve known biological, pharmacological, and clinical structure while learning limited parts of the model from data. In this setting, event-aware simulation and sensitivity propagation remain important because the learned component must coexist with dosing events, treatment holds, threshold-triggered decisions, therapy switches, and other discrete intervention logic.

Four related directions are particularly relevant:

- mechanistic--neural hybrid systems,
- physics-informed neural networks,
- neural hybrid automata,
- and neural jump stochastic differential equations.

Each presents a different balance between mechanistic interpretability, data requirements, uncertainty representation, and flexibility in representing unknown dynamics.

### Mechanistic--neural hybrid systems

A mechanistic--neural hybrid model retains a structured differential-equation model for the components that are biologically or pharmacologically understood, while using a neural network to represent an uncertain interaction, forcing term, correction, or model-discrepancy component.

A generic form is

\[
\dot{x}
=
f_{\mathrm{mech}}(x,t,\theta)
+
f_{\mathrm{NN}}(x,t,u,\phi),
\]

where:

- \(x\) is the mechanistic state,
- \(f_{\mathrm{mech}}\) is the known mechanistic model,
- \(u\) denotes interventions such as dose, schedule, or treatment state,
- \(f_{\mathrm{NN}}\) is a learned neural correction,
- \(\theta\) contains mechanistic parameters,
- and \(\phi\) contains neural-network parameters.

For QSP and PK/PD, the mechanistic component may describe drug disposition, receptor occupancy, tumor growth, immune-cell dynamics, cytokine production, or toxicity pathways. The neural component can then represent a partially known feedback mechanism, an omitted mediator, a context-dependent interaction, or a structured discrepancy between the mechanistic model and observed data.

A useful example is an immuno-oncology model in which the known system represents tumor burden, effector-cell dynamics, checkpoint-inhibitor exposure, and a toxicity biomarker. If the precise relationship between tumor microenvironment state and immune suppression is uncertain, a neural term could be used to model that interaction while keeping dosing, pharmacokinetics, known immune-cell processes, and toxicity-hold rules explicit.

For hybrid models, the neural component may also depend on the active regime:

\[
\dot{x}
=
f_i(x,t,\theta)
+
f_{\mathrm{NN},i}(x,t,u,\phi),
\]

where \(i\) identifies the current treatment mode. For example, one learned correction may apply during active therapy, another during a treatment holiday, and another after a toxicity-driven hold.

The role of `hybrid-ds-julia` would be to ensure that the learned and mechanistic components both participate in event-aware simulation and sensitivity analysis. A neural correction should not obscure the fact that the treatment rule itself is hybrid. If a toxicity threshold is crossed, the resulting hold or switch must still be represented by an explicit event surface and reset or mode-transition map.

Potential uses include:

- learning uncertain biological interactions while retaining known PK, dosing, and intervention structure,
- calibrating mechanistic models to longitudinal biomarker or tumor-burden data,
- identifying patient-specific deviations from an otherwise shared mechanistic model,
- learning context-dependent pharmacodynamic effects,
- and improving predictive accuracy without discarding mechanistic interpretability.

The main scientific challenge is identifiability. A neural network can absorb model mismatch, noise, or missing mechanisms, but if it is too flexible it can make mechanistic parameters difficult to interpret. Successful hybrid implementations will therefore need regularization, biologically informed architecture choices, constrained parameterizations, out-of-sample validation, and explicit tests of whether the learned component improves decision-relevant predictions rather than merely fitting observed trajectories.

### Physics-informed neural networks

Physics-informed neural networks, or PINNs, represent a state trajectory with a neural network and train that network using both observational data and a loss term that penalizes violations of the governing differential equations.

For a system

\[
\dot{x}
=
f(x,t,\theta),
\]

a neural approximation

\[
\hat{x}(t;\phi)
\]

can be trained by minimizing a loss of the form

\[
\mathcal{L}
=
\mathcal{L}_{\mathrm{data}}
+
\lambda_{\mathrm{ODE}}
\mathcal{L}_{\mathrm{ODE}}
+
\lambda_{\mathrm{IC}}
\mathcal{L}_{\mathrm{IC}}
+
\lambda_{\mathrm{event}}
\mathcal{L}_{\mathrm{event}},
\]

where:

- \(\mathcal{L}_{\mathrm{data}}\) measures agreement with observations,
- \(\mathcal{L}_{\mathrm{ODE}}\) penalizes violations of the continuous governing equations,
- \(\mathcal{L}_{\mathrm{IC}}\) enforces initial or boundary conditions,
- and \(\mathcal{L}_{\mathrm{event}}\) enforces jump, reset, or mode-transition conditions.

For hybrid QSP and PK/PD systems, the final term is essential. A model that learns a smooth trajectory through a bolus dose, treatment hold, threshold-triggered switch, or state reset may appear numerically adequate while failing to preserve the actual intervention logic that matters for interpretation and decision-making.

A hybrid PINN may therefore use separate neural representations for different time segments or modes:

\[
\hat{x}_1(t), \hat{x}_2(t), \ldots, \hat{x}_m(t),
\]

with matching conditions at event times. If an event occurs at time \(\tau_k\), the training loss can include:

\[
\hat{x}_{k+1}(\tau_k^+)
-
R_k\left(
\hat{x}_{k}(\tau_k^-),
\tau_k,
\theta
\right),
\]

so that the learned trajectory satisfies the prescribed jump map.

For state-triggered events, the model must also account for the event condition:

\[
h\left(
\hat{x}(\tau_k),
\tau_k,
\theta
\right)
=
0.
\]

This can be challenging because the event time itself may be unknown and depend on the learned trajectory. One approach is to represent event times as trainable variables; another is to use domain decomposition, with separate neural approximations on intervals whose boundaries correspond to detected or inferred events.

Within `hybrid-ds-julia`, PINN-related functionality would be most useful for inverse problems and sparse-data settings. Potential applications include:

- reconstructing latent biological states from sparse biomarker measurements,
- estimating patient-specific parameters from irregularly sampled clinical data,
- inferring unobserved immune or disease compartments,
- calibrating event-rich PK/PD models when direct simulation-based optimization is difficult,
- and combining mechanistic constraints with data-driven trajectory reconstruction.

PINNs are not automatically superior to conventional solver-based fitting. They can be difficult to train, sensitive to loss weighting, and challenged by stiffness, sharp transitions, discontinuities, and high-dimensional state spaces. For the present project, their value is likely to be greatest when they are used selectively—for example, to infer latent states or learn constrained corrections—rather than as a universal replacement for event-aware numerical integration.

### Neural hybrid automata

A hybrid automaton represents a system using discrete modes, continuous dynamics within each mode, and transitions between modes. A neural hybrid automaton extends this idea by allowing neural networks to learn part of the mode-dependent dynamics, transition conditions, reset maps, or mode-assignment logic from data.

A generic hybrid-automaton representation can be written as:

\[
q(t) \in \mathcal{Q},
\]

\[
\dot{x}
=
f_{q(t)}(x,t,\theta),
\]

with transitions

\[
q^- \rightarrow q^+
\]

when an event condition is satisfied, potentially accompanied by a reset map

\[
x^+
=
R_{q^-\rightarrow q^+}(x^-,t,\theta).
\]

In a neural hybrid automaton, one or more of these components may be learned:

\[
\dot{x}
=
f_{q,\mathrm{mech}}(x,t,\theta)
+
f_{q,\mathrm{NN}}(x,t,\phi),
\]

or the transition guard itself may be represented by a learned classifier or score function:

\[
h_{q^-\rightarrow q^+}(x,t;\phi)
=
0.
\]

For translational pharmacology, the discrete modes could represent clinically interpretable states such as:

- active treatment,
- reduced-dose treatment,
- treatment hold,
- recovery or monitoring,
- rescue therapy,
- relapse management,
- or post-progression treatment.

A neural component could then be used to learn which latent physiological conditions make a transition likely, which modes best describe observed treatment-response patterns, or how the continuous dynamics differ between modes.

For example, longitudinal real-world data may show that patients with apparently similar baseline covariates follow different toxicity and recovery trajectories after treatment interruption. A neural hybrid automaton could be used to learn whether those trajectories are better represented by distinct latent modes, while retaining explicit treatment rules and biologically interpretable state variables.

The advantage of this approach is that it can combine data-driven discovery with a model structure that remains aligned with actual treatment logic. Rather than learning an unrestricted recurrent predictor, the model still distinguishes continuous evolution from discrete decisions and regime changes.

The risks are substantial. Mode discovery can be non-identifiable; different combinations of modes, guards, and reset maps may fit the same data. In addition, a learned transition rule may be difficult to interpret clinically unless it is constrained by known protocol rules, toxicity criteria, or biological thresholds.

For `hybrid-ds-julia`, neural hybrid automata are therefore a longer-term direction. The package’s immediate contribution would be to provide robust representation and differentiation of known hybrid structure. Learned modes and transition rules should be added only where data support them and where their scientific role is clearly distinguishable from known intervention logic.

### Neural jump SDEs

Deterministic hybrid systems describe treatment schedules and state transitions clearly, but biological and clinical systems also contain stochasticity. Patient response, immune dynamics, adherence, measurement error, unobserved confounders, and timing variability can all produce behavior that is not well represented by a single deterministic trajectory.

A jump stochastic differential equation can be written as:

\[
dX_t
=
f(X_t,t,\theta)\,dt
+
g(X_t,t,\theta)\,dW_t
+
J(X_{t^-},t,\theta)\,dN_t,
\]

where:

- \(X_t\) is the stochastic state,
- \(f\) is the drift,
- \(g\) is the diffusion coefficient,
- \(W_t\) is a Wiener process,
- \(N_t\) is a counting process,
- and \(J\) describes the state change associated with a jump.

A neural jump SDE replaces one or more of these components with a neural-network parameterization:

\[
dX_t
=
f_{\mathrm{NN}}(X_t,t,\phi)\,dt
+
g_{\mathrm{NN}}(X_t,t,\phi)\,dW_t
+
J_{\mathrm{NN}}(X_{t^-},t,\phi)\,dN_t.
\]

For mechanistic pharmacology, a more interpretable approach is often to retain known structure and learn only selected components:

\[
dX_t
=
f_{\mathrm{mech}}(X_t,t,\theta)\,dt
+
g_{\mathrm{NN}}(X_t,t,\phi)\,dW_t
+
J_{\mathrm{mech/NN}}(X_{t^-},t,\theta,\phi)\,dN_t.
\]

The jump process may represent known scheduled dosing events, random treatment interruptions, toxicity-triggered state changes, hospitalization events, unobserved perturbations, or other abrupt changes in the disease or treatment process.

In a QSP or PK/PD context, neural jump SDEs could be useful for:

- representing between-patient variability beyond static random effects,
- modeling stochastic immune-cell or disease-state fluctuations,
- learning heterogeneous response dynamics from repeated longitudinal measurements,
- quantifying uncertainty in the timing and impact of treatment interruptions,
- and simulating distributions of outcomes under alternative dosing and monitoring policies.

The event-aware perspective remains important even in the stochastic setting. Scheduled doses, protocol-defined holds, and known therapy switches should not be treated as arbitrary random jumps merely because the overall model includes uncertainty. Instead, a model may include both deterministic intervention events and stochastic jumps:

\[
X^+
=
R_{\mathrm{scheduled}}(X^-,t,\theta)
\]

at known times, together with random jump processes for unplanned or latent events.

This separation helps preserve interpretability. It distinguishes actions taken by the treatment protocol from random biological or clinical disruptions.

The main limitations are computational. Inference for neural jump SDEs can be expensive, stochastic gradients can be noisy, and data may not identify the separate effects of drift, diffusion, jump intensity, and jump magnitude. These methods are therefore most appropriate after the deterministic hybrid core is well tested and after benchmark data sets establish whether stochastic structure improves decision-relevant predictions.

For `hybrid-ds-julia`, neural jump SDEs belong to a research-facing extension layer rather than the first implementation milestone. The package can nevertheless be designed so that its deterministic event abstractions—guards, reset maps, regime transitions, and event-aware sensitivities—form a coherent foundation for later stochastic and learned extensions.
