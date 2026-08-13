## Other disease applications

Although the initial focus is QSP and PK/PD, the same event-aware numerical framework can apply to a broad range of mechanistic disease models.

Examples include:

- **Autoimmune disease** — flare-remission dynamics, tapering schedules, rescue therapy, and biomarker-triggered escalation or de-escalation.
- **Inflammatory disease** — treatment holidays, adaptive biologic dosing, threshold-based switching, and toxicity management.
- **Infectious disease** — pulsed antimicrobial therapy, adherence interruptions, resistance thresholds, treatment switching, and pathogen-load triggers.
- **Metabolic disease** — intermittent interventions, glucose-triggered dosing rules, meal events, and state-dependent control policies.
- **Neurological disease** — stimulation protocols, medication cycling, threshold-triggered intervention, and episodic symptom dynamics.
- **Cell and gene therapy** — conditioning regimens, infusion events, expansion phases, delayed toxicity, and intervention rules based on cytokine or biomarker dynamics.
- **Cardiovascular disease** — intermittent treatment, device-triggered interventions, threshold-based alarms, and adaptive control of physiological states.

The common feature is not any particular disease area. It is the coexistence of continuous biological dynamics and discrete intervention logic.

In all of these settings, the central questions are similar:

- How does timing affect long-term outcome?
- Which thresholds or intervention rules are responsible for a qualitative change in behavior?
- How robust is a schedule across plausible parameter variation?
- Can model sensitivities identify leverage points for safer or more effective treatment strategies?
- Do different treatment policies create distinct dynamical regimes that should be analyzed separately?

## Other computational biology applications

The same hybrid dynamical-systems methods can also support computational-biology applications outside human disease modeling. In each case, the continuous state dynamics may be governed by differential equations, while interventions, environmental changes, threshold rules, or experimental protocols introduce discrete events and regime transitions.

### Predator--prey, pest management, and adaptive harvesting

Ecological models often include continuous population dynamics together with discrete harvesting, stocking, pesticide application, predator release, seasonal transitions, or threshold-based management decisions.

A simple predator--prey system might be represented as

\[
\dot{N}
=
rN
\left(
1-\frac{N}{K}
\right)
-
\frac{aNP}{1+bN},
\]

\[
\dot{P}
=
c\frac{aNP}{1+bN}
-
dP,
\]

where \(N\) is prey or pest abundance and \(P\) is predator abundance.

A management intervention can be represented by a pulse or reset map. For example, pesticide application at time \(t_k\) might produce

\[
N(t_k^+)
=
(1-\rho_k)N(t_k^-),
\]

while periodic predator release could produce

\[
P(t_k^+)
=
P(t_k^-)
+
R_k.
\]

State-triggered intervention rules are also common. A pest-management policy may apply control only when pest abundance exceeds a threshold:

\[
N(t)
\geq
N_{\mathrm{threshold}}.
\]

This naturally creates a hybrid system in which management actions depend on the evolving ecological state.

Potential uses of `hybrid-ds-julia` include:

- comparing the timing and intensity of pesticide or biological-control pulses,
- optimizing harvesting or stocking schedules,
- identifying threshold policies that avoid pest outbreaks,
- studying resilience and recovery after interventions,
- and analyzing how uncertainty in growth or predation rates affects management outcomes.

### Crop growth, canopy competition, and precision agriculture

Crop and plant-growth models combine continuous developmental and physiological processes with discrete management events such as planting, irrigation, fertilization, pesticide application, pruning, harvest, and abrupt weather changes.

A stylized crop-growth model may include biomass \(W\), soil-water availability \(M\), nutrient availability \(N\), and canopy state \(L\):

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
\ell_N(N),
\]

where \(I(t)\) and \(F(t)\) represent irrigation and fertilizer inputs.

Discrete management events may be represented by impulsive updates such as

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

A state-dependent precision-agriculture policy might trigger irrigation when soil moisture falls below a threshold:

\[
M(t)
\leq
M_{\mathrm{irrigation}}.
\]

Similarly, fertilization, pest intervention, or canopy management may be activated only when one or more sensor-derived variables enter a specified range.

Hybrid methods are relevant because the timing of those interventions can strongly affect cumulative growth, resource use, and final yield. A small change in irrigation timing, for example, may matter much more during a sensitive growth stage than at another point in the season.

Potential uses include:

- optimizing irrigation and fertilization schedules,
- comparing threshold-based versus fixed-calendar interventions,
- quantifying sensitivity of yield to timing and dose of inputs,
- analyzing crop-response regimes under different environmental conditions,
- and incorporating weather, sensor, or management events into a coherent dynamical model.

### Gene regulatory networks, cell-cycle control, and synthetic biology

Gene regulatory networks often exhibit thresholding, switching, pulses, feedback, and state-dependent transitions. These features arise naturally from transcriptional regulation, bistability, cell-cycle checkpoints, inducible expression systems, optogenetic stimulation, and experimental interventions.

A simple regulatory interaction can be represented using a Hill-function response:

\[
\dot{x}
=
\frac{\alpha}{1+\left(\frac{y}{K}\right)^n}
-
\delta_x x,
\]

\[
\dot{y}
=
\frac{\beta x^m}{L^m+x^m}
-
\delta_y y.
\]

Depending on parameters, such systems can display switch-like behavior, oscillations, or multiple stable states.

Hybrid structure enters when a regulatory program changes at a threshold or when an experiment applies a pulse. For example, an inducible expression experiment might update an input state at selected times:

\[
u(t_k^+)
=
u(t_k^-)
+
A_k.
\]

A cell-cycle checkpoint may activate when a damage variable exceeds a threshold, changing the active regulatory dynamics:

\[
D(t)
\geq
D_{\mathrm{checkpoint}}.
\]

Synthetic-biology control systems can also contain explicit mode changes, such as light-on/light-off stimulation protocols, nutrient shifts, temperature changes, or feedback controllers that switch based on fluorescent reporter levels.

Potential uses include:

- optimizing pulse timing for gene-expression control,
- studying sensitivity of switching behavior to parameter uncertainty,
- identifying interventions that move a system between stable phenotypic states,
- designing feedback rules for synthetic circuits,
- and estimating event-aware sensitivities in models with checkpoint or threshold logic.

### Microbial communities, bioreactors, and pulsed interventions

Microbial communities and bioreactor systems often involve continuous growth, substrate consumption, metabolite production, competition, and feedback together with pulsed feeding, dilution, inoculation, antibiotic exposure, environmental shifts, and threshold-based control.

A simple chemostat-style model may include microbial biomass \(X\), substrate \(S\), and product \(P\):

\[
\dot{X}
=
\mu(S)X
-
D X,
\]

\[
\dot{S}
=
D(S_{\mathrm{in}}-S)
-
\frac{1}{Y}\mu(S)X,
\]

\[
\dot{P}
=
q_P(S)X
-
D P,
\]

where \(D\) is a dilution rate, \(Y\) is a yield coefficient, and \(\mu(S)\) describes substrate-limited growth.

A pulsed feeding event can be represented by

\[
S(t_k^+)
=
S(t_k^-)
+
F_k.
\]

A contamination, inhibition, or oxygen-limitation event may trigger a change in the governing dynamics when a metabolite or process variable crosses a threshold.

In microbial ecology, similar structures arise through antibiotic pulses, nutrient switching, periodic disturbance, inoculation, or host-mediated environmental changes. These events can alter community composition, drive transitions between ecological states, or create history-dependent responses that are not captured well by purely smooth models.

Potential uses include:

- optimizing feed schedules and dilution policies in bioreactors,
- analyzing resilience of microbial communities after pulsed perturbations,
- studying antibiotic scheduling and resistance dynamics,
- comparing threshold-based versus periodic control rules,
- and using event-aware sensitivities to identify parameters that control transitions between productive and unproductive regimes.

### Epidemiology, public-health policy, and adaptive intervention

Epidemiological systems have continuous transmission, progression, recovery, and immunity dynamics, but policy and care pathways routinely introduce hybrid structure. Vaccination campaigns, school or workplace closures, antiviral treatment starts, isolation protocols, testing thresholds, hospital-capacity triggers, and changes in public-health guidance can all change the effective dynamics at specific times or when surveillance indicators cross a threshold.

A basic susceptible–infectious–recovered model can be written as

\[
\dot{S}
=
-\beta(t)\frac{SI}{N},
\]

\[
\dot{I}
=
\beta(t)\frac{SI}{N}
-
\gamma I,
\]

\[
\dot{R}
=
\gamma I.
\]

Hybrid policy structure enters when the transmission rate, testing intensity, treatment availability, or intervention state changes. For example, a threshold-triggered intervention may reduce effective transmission when infections exceed a policy threshold:

\[
I(t)
\geq
I_{\mathrm{trigger}}
\quad \Longrightarrow \quad
\beta(t)
=
\beta_{\mathrm{restricted}}.
\]

When cases fall below a reopening threshold,

\[
I(t)
\leq
I_{\mathrm{release}}
\quad \Longrightarrow \quad
\beta(t)
=
\beta_{\mathrm{baseline}}.
\]

Vaccination or prophylaxis campaigns can be represented by jump maps such as

\[
S(t_k^+)
=
S(t_k^-)
-
V_k,
\]

\[
R(t_k^+)
=
R(t_k^-)
+
V_k,
\]

where \(V_k\) is the number or proportion effectively vaccinated at the event time.

More detailed models can include exposed, hospitalized, intensive-care, treated, isolated, or age-stratified compartments. They can also represent delayed test results, treatment eligibility rules, limited hospital capacity, supply constraints, and region-specific intervention policies.

Potential uses of `hybrid-ds-julia` include:

- comparing fixed-calendar and threshold-triggered nonpharmaceutical interventions,
- optimizing the timing of vaccination, testing, treatment, or prophylaxis campaigns,
- studying hysteresis in policy rules, such as distinct intervention and reopening thresholds,
- quantifying sensitivity of epidemic outcomes to trigger thresholds, reporting delays, and intervention timing,
- evaluating robustness of adaptive policies across uncertainty in transmission, behavior, and adherence,
- and representing inequities in access to testing, treatment, vaccination, or timely intervention as explicit differences in event timing and policy structure.

This application area is especially well suited to hybrid sensitivity analysis because policy conclusions can depend sharply on when a threshold is crossed. Small changes in transmission, surveillance delay, intervention timing, or available capacity may change whether a region experiences a short outbreak, repeated intervention cycles, or sustained healthcare-system stress. Event-aware derivatives and multiple shooting can help distinguish genuine policy-regime boundaries from numerical artifacts.
