## Example applications

The following examples illustrate the kinds of translational and decision-facing questions that `hybrid-ds-julia` is intended to support. They are not separate product claims; they are examples of how event-aware simulation, sensitivities, and trajectory analysis can be used when mechanistic models include real intervention logic.

### QSP and PK/PD

In QSP and PK/PD, many model outputs depend on more than continuous exposure-response relationships. Treatment schedules, dose holds, switches, biomarker thresholds, and protocol rules can determine whether a trajectory enters one long-term regime or another.

For example, an immuno-oncology model may include:

- tumor growth and immune-mediated killing,
- drug exposure and clearance,
- treatment-cycle dosing,
- toxicity accumulation,
- and a treatment-hold rule triggered by a toxicity biomarker.

A clinically relevant question is not only whether a nominal dose reduces tumor burden. It may also be whether a schedule produces sustained control, temporary response followed by relapse, prolonged treatment interruption, or unacceptable toxicity.

With event-aware simulation, the model can represent the full treatment logic directly:

\[
C(t_k^+)
=
C(t_k^-)
+
D_k
\]

at planned dose times, together with threshold-triggered treatment holds such as

\[
B(t)
\geq
B_{\mathrm{hold}}
\quad \Longrightarrow \quad
\text{hold treatment}.
\]

If toxicity subsequently recovers,

\[
B(t)
\leq
B_{\mathrm{restart}}
\quad \Longrightarrow \quad
\text{restart or reduce treatment}.
\]

The resulting trajectory can be analyzed with respect to dose size, dose interval, treatment-hold thresholds, restart thresholds, and patient-specific parameter variation.

Potential QSP and PK/PD applications include:

- schedule comparison for pulsed, cyclic, or intermittent dosing,
- toxicity-aware dose optimization,
- treatment-holiday and rechallenge analysis,
- adaptive dosing based on biomarker thresholds,
- combination-therapy sequencing,
- virtual-patient studies with heterogeneous event thresholds,
- and sensitivity analysis of clinically meaningful outcome metrics.

A major practical advantage is that the analysis can focus on questions that are already meaningful to pharmacologists and clinicians:

- How much time is spent on treatment?
- How often are doses held or reduced?
- What is the cumulative exposure before toxicity forces a switch?
- Which parameters determine whether recovery and rechallenge are possible?
- How sensitive is a proposed schedule to changes in patient biology or measurement thresholds?

### Translational pharmacology

The package is intended to support translational workflows in which mechanistic models are used to connect preclinical observations, biomarker dynamics, and treatment strategies to early clinical decisions.

A translational model may combine:

- pharmacokinetics,
- target engagement,
- pathway modulation,
- biomarker response,
- tumor or disease burden,
- toxicity,
- and treatment-management logic.

The hybrid structure arises because real treatment development involves decisions and interventions that are not continuously varying. Examples include:

- dose escalation or de-escalation,
- treatment delay,
- stopping rules,
- cohort transitions,
- rescue medication,
- biomarker-triggered enrichment,
- and protocol-defined dose modifications.

A useful workflow can therefore be framed as a sequence:

1. Specify a mechanistic model and a treatment-control policy.
2. Simulate the resulting hybrid trajectory.
3. Compute sensitivities of outcomes and event times to model parameters and schedule variables.
4. Compare candidate regimens or decision rules.
5. Identify robust regions of the design space rather than optimizing only for one nominal parameter set.
6. Examine whether the conclusions change near event boundaries, threshold crossings, or treatment-regime transitions.

This perspective is particularly relevant in early development, where uncertainty is high and the goal is often to distinguish between plausible mechanisms, identify useful biomarkers, and choose dose or schedule ranges that remain reasonable across uncertainty.

### SAR progression and mechanism differentiation

Structure–activity relationship work often focuses on potency, selectivity, exposure, and safety properties. Those measurements remain essential, but mechanistic models can add another layer of interpretation: whether compounds with different pharmacological profiles generate meaningfully different dynamical treatment regimes under realistic dosing and intervention constraints.

For example, two compounds may have similar short-term tumor-growth inhibition in vitro but differ in:

- target residence time,
- exposure persistence,
- immune activation,
- toxicity accumulation,
- feedback effects,
- or the ability to sustain a response after dosing is reduced or interrupted.

A hybrid QSP model can make those differences visible at the regimen level.

Suppose a compound-specific parameter vector is written as

\[
\theta_j,
\]

where \(j\) indexes candidate compounds. The model may then produce an outcome map

\[
\mathcal{O}(\theta_j, D, \tau, \pi),
\]

where:

- \(D\) represents dose,
- \(\tau\) represents schedule timing,
- and \(\pi\) represents a treatment policy, such as a toxicity-hold or restart rule.

The outcome may include tumor control, biomarker suppression, cumulative exposure, time in toxicity hold, relapse probability, or time to progression.

The goal is not to claim that a model can replace experimental SAR. Rather, the model can help organize mechanistic hypotheses and prioritize experiments by asking questions such as:

- Does a change in potency alter the optimal schedule, or only the dose scale?
- Does a longer-lived effect improve robustness to missed doses or treatment holidays?
- Does one mechanism produce a wider safe scheduling window than another?
- Are certain compound properties especially valuable because they reduce sensitivity to toxicity-driven holds?
- Which measurements would most reduce uncertainty in mechanism-dependent regimen predictions?

This provides a way to connect compound properties to decision-relevant dynamical behavior rather than treating each property as an isolated optimization target.

### Autoimmune and inflammatory disease

Autoimmune and inflammatory disease models often have flare-remission behavior, delayed response, treatment tapering, rescue therapy, and biomarker-based adjustment. These features make them natural applications for hybrid dynamical-systems methods.

A conceptual model might include inflammatory activity \(I\), regulatory immune activity \(R\), drug exposure \(C\), and a toxicity or adverse-effect burden \(B\):

\[
\dot{I}
=
\alpha_I I
-
k_R R I
-
k_C C I,
\]

\[
\dot{R}
=
s_R
-
d_R R
+
\eta_C C,
\]

\[
\dot{C}
=
-k_C^{\mathrm{elim}}C,
\]

\[
\dot{B}
=
\alpha_B C
-
k_B B.
\]

A treatment policy may initiate rescue therapy during a flare:

\[
I(t)
\geq
I_{\mathrm{flare}}
\quad \Longrightarrow \quad
\text{administer rescue treatment},
\]

or taper treatment when disease activity remains controlled:

\[
I(t)
\leq
I_{\mathrm{control}}
\quad \Longrightarrow \quad
\text{reduce maintenance treatment}.
\]

The model can then be used to study:

- when tapering produces sustained control versus relapse,
- whether rescue therapy should be triggered earlier or later,
- how biomarker noise affects threshold-based decisions,
- whether treatment holidays create beneficial recovery or destabilizing flare cycles,
- and how patient heterogeneity changes the balance between efficacy and adverse effects.

The same numerical issues appear as in oncology: event times may be central to the outcome, small changes in thresholds can alter the treatment path, and long-horizon simulation may become sensitive to repeated regime changes.

### Crop science and precision agriculture

The event-aware framework also applies to crop models, where continuous growth and environmental dynamics interact with discrete management actions.

A crop-growth system may include biomass, water availability, nutrient status, canopy development, and pest pressure. Interventions such as irrigation, fertilization, pesticide application, planting, harvest, and greenhouse climate changes occur at specific times or in response to sensor thresholds.

For example, a precision-irrigation policy could apply water when soil moisture falls below a threshold:

\[
M(t)
\leq
M_{\mathrm{threshold}}
\quad \Longrightarrow \quad
M(t^+)
=
M(t^-)
+
\Delta M.
\]

A nutrient-management policy could apply fertilizer after a sensor-derived nutrient variable falls below a specified level:

\[
N(t)
\leq
N_{\mathrm{threshold}}
\quad \Longrightarrow \quad
N(t^+)
=
N(t^-)
+
\Delta N.
\]

The hybrid model can then be used to compare:

- fixed-calendar and sensor-triggered irrigation,
- alternative fertilizer timing and dose strategies,
- pest-intervention thresholds,
- crop responses to heat or water-stress events,
- and robustness of management policies across weather and soil conditions.

In this setting, variational equations and event-aware sensitivities can help identify which thresholds, schedule variables, or biological parameters most affect final yield, water use, nutrient efficiency, or resilience to environmental stress.

The original crop-science motivation for this project is retained in the following section because it remains a meaningful example of how hybrid dynamical-systems methods can support decision-facing biological modeling outside pharmacology.
