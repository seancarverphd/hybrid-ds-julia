## AI/ML mathematical extensions

The deterministic hybrid framework is intended to remain useful on its own. However, a natural longer-term direction is to combine mechanistic QSP and PK/PD models with machine-learning components when biological structure is partly known but key interactions, patient-specific effects, or unresolved mechanisms are not.

The goal is not to replace mechanistic pharmacology with black-box prediction. Instead, the opportunity is to preserve known biological, pharmacological, and clinical structure while learning limited parts of the model from data. In this setting, event-aware simulation and sensitivity propagation remain important because the learned component must coexist with dosing events, treatment holds, threshold-triggered decisions, therapy switches, and other discrete intervention logic.

Four related directions are particularly relevant:

- Mechanistic--neural hybrid systems;
- Physics-informed neural networks;
- Neural hybrid automata; and
- Neural jump stochastic differential equations.

Each presents a different balance between mechanistic interpretability, data requirements, uncertainty representation, and flexibility in representing unknown dynamics.

### Mechanistic--neural hybrid systems

A mechanistic--neural hybrid model retains a structured differential-equation model for the components that are biologically or pharmacologically understood, while using a neural network to represent an uncertain interaction, forcing term, correction, or model-discrepancy component.

A generic form is:

$$
\dot{x}
=
f_{\mathrm{mech}}(x,t,\theta)
+
f_{\mathrm{NN}}(x,t,u,\phi),
$$

where:

- \(x\) is the mechanistic state;
- \(f_{\mathrm{mech}}\) is the known mechanistic model;
- \(u\) denotes interventions such as dose, schedule, or treatment state;
- \(f_{\mathrm{NN}}\) is a learned neural correction;
- \(\theta\) contains mechanistic parameters; and
- \(\phi\) contains neural-network parameters.

For QSP and PK/PD, the mechanistic component may describe drug disposition, receptor occupancy, tumor growth, immune-cell dynamics, cytokine production, or toxicity pathways. The neural component can then represent a partially known feedback mechanism, an omitted mediator, a context-dependent interaction, or a structured discrepancy between the mechanistic model and observed data.

A useful example is an immuno-oncology model in which the known system represents tumor burden, effector-cell dynamics, checkpoint-inhibitor exposure, and a toxicity biomarker. If the precise relationship between tumor microenvironment state and immune suppression is uncertain, a neural term could be used to model that interaction while keeping dosing, pharmacokinetics, known immune-cell processes, and toxicity-hold rules explicit.

For hybrid models, the neural component may also depend on the active regime:

$$
\dot{x}
=
f_i(x,t,\theta)
+
f_{\mathrm{NN},i}(x,t,u,\phi),
$$

where \(i\) identifies the current treatment mode. For example, one learned correction may apply during active therapy, another during a treatment holiday, and another after a toxicity-driven hold.

The role of `hybrid-ds-julia` would be to ensure that the learned and mechanistic components both participate in event-aware simulation and sensitivity analysis. A neural correction should not obscure the fact that the treatment rule itself is hybrid. If a toxicity threshold is crossed, the resulting hold or switch must still be represented by an explicit event surface and reset or mode-transition map.

Potential uses include:

- Learning uncertain biological interactions while retaining known PK, dosing, and intervention structure;
- Calibrating mechanistic models to longitudinal biomarker or tumor-burden data;
- Identifying patient-specific deviations from an otherwise shared mechanistic model;
- Learning context-dependent pharmacodynamic effects; and
- Improving predictive accuracy without discarding mechanistic interpretability.

The main scientific challenge is identifiability. A neural network can absorb model mismatch, noise, or missing mechanisms, but if it is too flexible it can make mechanistic parameters difficult to interpret. Successful hybrid implementations will therefore need regularization, biologically informed architecture choices, constrained parameterizations, out-of-sample validation, and explicit tests of whether the learned component improves decision-relevant predictions rather than merely fitting observed trajectories.

### Physics-informed neural networks

Physics-informed neural networks, or PINNs, represent a state trajectory with a neural network and train that network using both observational data and a loss term that penalizes violations of the governing differential equations.

For a system:

$$
\dot{x}
=
f(x,t,\theta),
$$

a neural approximation:

$$
\hat{x}(t;\phi)
$$

can be trained by minimizing a loss of the form:

$$
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
$$

where:

- \(\mathcal{L}_{\mathrm{data}}\) measures agreement with observations;
- \(\mathcal{L}_{\mathrm{ODE}}\) penalizes violations of the continuous governing equations;
- \(\mathcal{L}_{\mathrm{IC}}\) enforces initial or boundary conditions; and
- \(\mathcal{L}_{\mathrm{event}}\) enforces jump, reset, or mode-transition conditions.

For hybrid QSP and PK/PD systems, the final term is essential. A model that learns a smooth trajectory through a bolus dose, treatment hold, threshold-triggered switch, or state reset may appear numerically adequate while failing to preserve the actual intervention logic that matters for interpretation and decision-making.

A hybrid PINN may therefore use separate neural representations for different time segments or modes:

$$
\hat{x}_1(t), \hat{x}_2(t), \ldots, \hat{x}_m(t),
$$

with matching conditions at event times. If an event occurs at time \(\tau_k\), the training loss can include:

$$
\hat{x}_{k+1}(\tau_k^+)
-
R_k\left(
\hat{x}_{k}(\tau_k^-),
\tau_k,
\theta
\right),
$$

so that the learned trajectory satisfies the prescribed jump map.

For state-triggered events, the model must also account for the event condition:

$$
h\left(
\hat{x}(\tau_k),
\tau_k,
\theta
\right)
=
0.
$$

This can be challenging because the event time itself may be unknown and depend on the learned trajectory. One approach is to represent event times as trainable variables; another is to use domain decomposition, with separate neural approximations on intervals whose boundaries correspond to detected or inferred events.

Within `hybrid-ds-julia`, PINN-related functionality would be most useful for inverse problems and sparse-data settings. Potential applications include:

- Reconstructing latent biological states from sparse biomarker measurements;
- Estimating patient-specific parameters from irregularly sampled clinical data;
- Inferring unobserved immune or disease compartments;
- Calibrating event-rich PK/PD models when direct simulation-based optimization is difficult; and
- Combining mechanistic constraints with data-driven trajectory reconstruction.

PINNs are not automatically superior to conventional solver-based fitting. They can be difficult to train, sensitive to loss weighting, and challenged by stiffness, sharp transitions, discontinuities, and high-dimensional state spaces. For the present project, their value is likely to be greatest when they are used selectively—for example, to infer latent states or learn constrained corrections—rather than as a universal replacement for event-aware numerical integration.

### Neural hybrid automata

A hybrid automaton represents a system using discrete modes, continuous dynamics within each mode, and transitions between modes. A neural hybrid automaton extends this idea by allowing neural networks to learn part of the mode-dependent dynamics, transition conditions, reset maps, or mode-assignment logic from data.

A generic hybrid-automaton representation can be written as:

$$
q(t) \in \mathcal{Q},
$$

$$
\dot{x}
=
f_{q(t)}(x,t,\theta),
$$

with transitions:

$$
q^- \rightarrow q^+
$$

when an event condition is satisfied, potentially accompanied by a reset map:

$$
x^+
=
R_{q^-\rightarrow q^+}(x^-,t,\theta).
$$

In a neural hybrid automaton, one or more of these components may be learned:

$$
\dot{x}
=
f_{q,\mathrm{mech}}(x,t,\theta)
+
f_{q,\mathrm{NN}}(x,t,\phi),
$$

or the transition guard itself may be represented by a learned classifier or score function:

$$
h_{q^-\rightarrow q^+}(x,t;\phi)
=
0.
$$

For translational pharmacology, the discrete modes could represent clinically interpretable states such as:

- Active treatment;
- Reduced-dose treatment;
- Treatment hold;
- Recovery or monitoring;
- Rescue therapy;
- Relapse management; or
- Post-progression treatment.

A neural component could then be used to learn which latent physiological conditions make a transition likely, which modes best describe observed treatment-response patterns, or how the continuous dynamics differ between modes.

For example, longitudinal real-world data may show that patients with apparently similar baseline covariates follow different toxicity and recovery trajectories after treatment interruption. A neural hybrid automaton could be used to learn whether those trajectories are better represented by distinct latent modes, while retaining explicit treatment rules and biologically interpretable state variables. The advantage of this approach is that it can combine data-driven discovery with a model structure that remains aligned with actual treatment logic. Rather than learning an unrestricted recurrent predictor, the model still distinguishes continuous evolution from discrete decisions and regime changes.

The risks are substantial. Mode discovery can be non-identifiable; different combinations of modes, guards, and reset maps may fit the same data. In addition, a learned transition rule may be difficult to interpret clinically unless it is constrained by known protocol rules, toxicity criteria, or biological thresholds.

For `hybrid-ds-julia`, neural hybrid automata are therefore a longer-term direction. The package’s immediate contribution would be to provide robust representation and differentiation of known hybrid structure. Learned modes and transition rules should be added only where data support them and where their scientific role is clearly distinguishable from known intervention logic.

### Stochastic hybrid systems

A stochastic hybrid system combines continuous dynamics, discrete modes or events, and one or more sources of uncertainty. In pharmacology or immuno-oncology, uncertainty may arise from between-patient heterogeneity, intrinsic biological variability, adherence, measurement error, unobserved physiological disturbances, or stochastic transitions between cell or disease states.

A generic formulation can combine continuous stochastic dynamics:

$$
dX_t
=
f_{q(t)}(X_t,a(t),t,\theta)\,dt
+
g_{q(t)}(X_t,a(t),t,\theta)\,dW_t,
$$

with scheduled or state-triggered events:

$$
X^+
=
R_i(X^-,q^-,a^-,t,\theta,\xi_i),
\qquad
q^+
=
T_i(q^-,X^-,a^-,t,\theta,\zeta_i),
$$

where \(W_t\) represents continuous stochastic forcing and \(\xi_i\) and \(\zeta_i\) represent random variation in reset outcomes or transition selection. A model need not include every source of randomness: it may retain deterministic clinical interventions while introducing stochasticity only in biological dynamics, observations, unplanned events, or latent-state transitions.

For `hybrid-ds-julia`, stochastic hybrid systems are a longer-term extension. The initial deterministic event-aware core remains valuable because it provides the guards, reset maps, mode logic, sensitivity abstractions, and numerical tests on which stochastic extensions can build. The immediate goal is not to reproduce full multiscale agent-based or cellular-automaton models, but to support a staged path from deterministic ODE-and-event models to uncertainty-aware stochastic hybrid models where data and scientific questions justify the additional complexity.

#### Competing events, multistate models, and point processes

A cause-specific competing-events survival model can supply transition intensities for stochastic hybrid events. Let \(N_i(t)\) count events of type \(i\), such as a toxicity-triggered treatment hold, progression, hospitalization, treatment discontinuation, or death. The cause-specific intensity is:

$$
\lambda_i(t \mid \mathcal{H}_t)
=
\lim_{\Delta t\downarrow 0}
\frac{
\Pr\{N_i(t+\Delta t)-N_i(t)=1\mid\mathcal{H}_t\}
}{
\Delta t
}.
$$

The total event intensity is:

$$
\lambda_{\mathrm{tot}}(t)
=
\sum_{i=1}^{K}\lambda_i(t),
$$

and, conditional on an event occurring at time \(t\), its type can be sampled with probability:

$$
\Pr\{\text{event type}=i\mid\text{event at }t,\mathcal{H}_t\}
=
\frac{\lambda_i(t\mid\mathcal{H}_t)}
{\lambda_{\mathrm{tot}}(t\mid\mathcal{H}_t)}.
$$

The intensities can depend on the continuous patient state, discrete mode, treatment action, time, and history:

$$
\lambda_i(t\mid\mathcal{H}_t)
=
\lambda_{i,\phi}
\bigl(
X_t,
q(t),
a(t),
\mathcal{H}_t,
t
\bigr),
$$

where \(\phi\) denotes parameters of the event-risk model. When event \(i\) occurs, the model applies its event-specific reset and mode-transition maps:

$$
X^+
=
R_i(X^-,q^-,a^-,t,\theta),
\qquad
q^+
=
T_i(q^-,X^-,a^-,t,\theta).
$$

Classical competing-risks models are most directly applicable when one event precludes the others for the endpoint being modeled. Death, for example, precludes future progression observations. Toxicity holds, hospitalization, and progression may instead be recurrent or sequential events. In those settings, the appropriate generalization is a history-dependent multistate point-process model, with event-specific transition intensities from each current mode.

For example, treatment-active mode may have outgoing transitions:

$$
\mathrm{treatment\ active}
\rightarrow
\{
\mathrm{treatment\ held},
\mathrm{treatment\ reassessment},
\mathrm{hospitalized},
\mathrm{dead}
\}.
$$

A stochastic event model can therefore combine mechanistic continuous dynamics with survival-analysis estimates of event risk, while preserving clinically interpretable reset maps and treatment-mode transitions. In a precision-medicine setting, this creates a bridge among longitudinal PK/PD or QSP modeling, recurrent-event and competing-risks survival analysis, multistate clinical trajectories, and uncertainty-aware policy evaluation.

### Neural jump stochastic differential equations

Neural jump stochastic differential equations are a data-driven extension of hybrid dynamical models for settings in which a latent state evolves continuously between events, while the timing, type, and effect of some events are uncertain and must be learned from data. They are particularly suited to temporal point-process data, where the conditional rate of a future event depends on the evolving latent state and prior event history.

They should not replace explicit representations of known clinical interventions. Scheduled doses, protocol-defined treatment holds, and mandated therapy switches remain deterministic event maps when their timing and logic are known. Neural jump SDEs are more appropriate for uncertain biological, behavioral, or care-process events, such as unplanned treatment interruption, adherence changes, acute adverse events, hospitalization, or irregular progression detection.

A jump stochastic differential equation can be written as:

$$
dX_t
=
f(X_t,t,\theta)\,dt
+
g(X_t,t,\theta)\,dW_t
+
J(X_{t^-},t,\theta)\,dN_t,
$$

where:

- \(X_t\) is the stochastic state;
- \(f\) is the drift;
- \(g\) is the diffusion coefficient;
- \(W_t\) is a Wiener process;
- \(N_t\) is a counting process; and
- \(J\) describes the state change associated with a jump.

A neural jump SDE replaces one or more of these components with a neural-network parameterization:

$$
dX_t
=
f_{\mathrm{NN}}(X_t,t,\phi)\,dt
+
g_{\mathrm{NN}}(X_t,t,\phi)\,dW_t
+
J_{\mathrm{NN}}(X_{t^-},t,\phi)\,dN_t.
$$

In a partly mechanistic formulation, it is often preferable to retain known PK/PD or QSP structure while learning only selected components:

$$
dX_t
=
f_{\mathrm{mech}}(X_t,t,\theta)\,dt
+
g_{\mathrm{NN}}(X_t,t,\phi)\,dW_t
+
J_{\mathrm{mech/NN}}(X_{t^-},t,\theta,\phi)\,dN_t.
$$

A neural point-process component may represent a history-dependent event intensity:

$$
\lambda_i(t\mid\mathcal{H}_t)
=
\lambda_{i,\phi}
\bigl(
X_t,
q(t),
a(t),
\mathcal{H}_t,
t
\bigr).
$$

The jump process may represent random treatment interruptions, toxicity-triggered state changes not adequately represented by fixed thresholds, hospitalization events, unobserved perturbations, or other abrupt changes in the disease or treatment process. Known scheduled doses and protocol-defined holds should remain explicit deterministic events rather than being converted into black-box stochastic jumps.

In a QSP or PK/PD context, neural jump SDEs could be useful for:

- Representing between-patient variability beyond static random effects;
- Modeling stochastic immune-cell or disease-state fluctuations;
- Learning heterogeneous response dynamics from repeated longitudinal measurements;
- Quantifying uncertainty in the timing and impact of treatment interruptions;
- Estimating event risk from patient state and history; and
- Simulating distributions of outcomes under alternative dosing and monitoring policies.

The main limitations are scientific as well as computational. Sparse, irregular data may not identify the separate effects of drift, diffusion, jump intensity, and jump magnitude. A learned event intensity can reflect monitoring, documentation, access, or clinician behavior rather than biology alone. Inference can be expensive, stochastic gradients can be noisy, and clinical causal or policy use requires explicit treatment of confounding, calibrated uncertainty, external validation, and a defined context of use.

For `hybrid-ds-julia`, neural jump SDEs belong to a research-facing extension layer rather than the first implementation milestone. The package can nevertheless be designed so that its deterministic event abstractions—guards, reset maps, regime transitions, and event-aware sensitivities—form a coherent foundation for later stochastic and learned extensions.

## Treatment actions, histories, and learned policies

Here, \(a(t)\) denotes the treatment action or intervention in effect at time \(t\). The action may include a dose, infusion rate, dose interval, drug choice, combination regimen, or monitoring schedule. As with \(x^-\) and \(q^-\), \(a^-\) denotes the action in effect immediately before an event, whereas \(a^+\) denotes the next action selected after that event.

The action is not generally a function only of the current observed measurements. In clinical settings, treatment decisions often depend on the available patient history \(\mathcal{H}_t\), including prior treatments, cumulative exposure, prior toxicities, imaging results, laboratory trajectories, biomarkers, and previously observed events. Let:

$$
\mathcal{H}_t
=
\bigl(
o_{0:t},
a_{0:t^-},
e_{0:t}
\bigr)
$$

denote this information history. A state-estimation procedure can use \(\mathcal{H}_t\) to construct a current estimated or belief state \(\hat{s}(t)\). The policy \(\pi_{\omega}\), learned through reinforcement learning, then selects the treatment action:

$$
a(t)
=
\pi_{\omega}
\bigl(
\hat{s}(t),
\mathcal{H}_t,
t
\bigr).
$$

Here, \(\omega\) denotes the learned parameters of the policy—for example, the weights and biases of a neural network or the coefficients of another parameterized decision rule.

At an event time, the post-event action is therefore:

$$
a^+
=
\pi_{\omega}
\bigl(
\hat{s}^+,
\mathcal{H}^+,
t
\bigr),
$$

where \(\hat{s}^+\) and \(\mathcal{H}^+\) incorporate the newly observed event and its associated clinical information.

## Model-free and model-based reinforcement learning

Reinforcement-learning methods differ in whether they use an explicit predictive model of the environment. In model-free RL, the algorithm learns a value function, a policy, or both directly from observed state--action--reward trajectories. It does not explicitly learn or invoke a model that predicts how the patient state will evolve under candidate treatment actions. Model-free methods can therefore be useful when a reliable patient model is unavailable, but they can require substantial data and may be difficult to interpret or validate when clinical outcomes are delayed and high-stakes.

In model-based RL, the algorithm uses a transition model to predict the consequences of candidate actions. In precision medicine, this model may be a mechanistic PK/PD model, a disease-progression model, a learned statistical model, or a hybrid combination of these components. The model can be used to simulate counterfactual treatment trajectories, assess uncertainty, enforce constraints, and plan over clinically meaningful outcomes such as disease control, toxicity, treatment burden, and survival.

`HybridSystems.jl` and `hybrid-ds-julia` are complementary in this setting. `HybridSystems.jl` provides a general Julia interface for defining hybrid systems with continuous flows, discrete modes, guards, transitions, and reset maps. `hybrid-ds-julia` is intended to build on, interoperate with, or adopt ideas from that general representation while supplying an event-aware sensitivity and optimization workflow and domain-facing conventions for QSP, PK/PD, precision medicine, and targeted biological research. In this way, the patient model can represent continuous processes such as drug exposure, tumor burden, physiological response, and toxicity between events, while also representing discrete events such as dose administration, laboratory-triggered treatment holds, adverse events, progression assessments, regimen transitions, and hospitalization. Event guards determine when an event occurs, and reset maps and mode transitions specify how the patient state, clinical mode, or permissible treatment actions change after the event.

For example, a hybrid patient model may predict continuous tumor response and toxicity while treatment is active. If toxicity reaches a prespecified threshold, an event guard can trigger a transition from an active-treatment mode to a treatment-hold mode. A learned policy can then choose the post-event action using the updated estimated patient state and clinical history:

$$
a^+
=
\pi_{\omega}
\bigl(
\hat{s}^+,
\mathcal{H}^+,
t
\bigr),
$$

where \(\pi_{\omega}\) is the treatment policy learned by the RL procedure, \(\hat{s}^+\) is the post-event estimated patient state, and \(\mathcal{H}^+\) is the information history after incorporating the event, new observations, prior treatments, and prior toxicities.

The distinction is not absolute. A practical system can combine a structured hybrid model with learned residual dynamics, a learned value function, or a learned policy. In this setting, the hybrid-system layer supplies the event-aware dynamical model, while the RL component learns how to select treatment actions or improve a treatment policy using real or simulated patient trajectories.

### Model-free algorithms

Examples of model-free RL algorithms include:

- **Q-learning:** learns an action-value function and is most natural for relatively small, discrete state and action spaces.
- **Deep Q-Network (DQN):** uses a neural network to approximate the action value \(Q(s,a)\); it is most directly suited to a discrete action set, such as choosing among prespecified dose levels, regimen options, or treatment actions.
- **Double DQN** and **Dueling DQN:** variants intended to improve the stability or value estimation of DQN-style methods.
- **Policy-gradient methods:** directly optimize a parameterized policy, potentially for either discrete or continuous actions.
- **Actor--critic methods:** learn both a policy (the actor) and a value or action-value function (the critic). Examples include Advantage Actor--Critic (A2C/A3C), Proximal Policy Optimization (PPO), Deep Deterministic Policy Gradient (DDPG), Twin Delayed DDPG (TD3), and Soft Actor--Critic (SAC).

For a clinical action space defined by a finite set of dose levels or regimen choices, DQN-style methods may be a reasonable initial baseline. For continuous dose, infusion-rate, or multidimensional treatment actions, actor--critic methods such as TD3 or SAC are more natural candidates.

### Model-based algorithms

Model-based approaches differ in how they use the predictive model:

- **Model-predictive control (MPC):** repeatedly optimizes a finite-horizon treatment plan using the current patient-state estimate and executes only the first action before replanning. MPC is not necessarily RL, but it is a strong model-based planning baseline and can be combined with RL.
- **Probabilistic Ensembles with Trajectory Sampling (PETS):** learns an ensemble of probabilistic dynamics models and uses sampling-based planning, often with the cross-entropy method. The ensemble represents epistemic uncertainty, which is important when evaluating unfamiliar treatment trajectories.
- **Model-Based Policy Optimization (MBPO):** learns a dynamics model and generates short synthetic rollouts that augment real data while training an off-policy policy, commonly a SAC-style policy.
- **World-model methods, such as PlaNet and Dreamer:** learn a compact latent dynamics model and train a policy or value function using imagined rollouts within that learned model.
- **Hybrid model-based RL:** uses a mechanistic or partially mechanistic hybrid model as the core world model, optionally learning patient-specific parameters, residual dynamics, event probabilities, reward models, and the treatment policy.
