### Specific labs and authors

The examples in this section identify research programs whose published work is potentially relevant to the scientific and technical scope of `hybrid-ds-julia`. They are included as invitations to technical scrutiny, not as endorsements or claims of collaboration. In each case, the relevant question is whether the package's combination of continuous-time ODE models, explicit events, threshold rules, reset maps, sensitivity analysis, and constrained optimization would usefully complement existing domain-specific theory, software, experiments, and analysis workflows.

These research programs already use sophisticated modeling, estimation, control, simulation, and experimental methods. `hybrid-ds-julia` is not intended to replace established specialized tools. Its potential value is as a transparent Julia-native environment for reduced-order or mechanistic hybrid models in which the researcher directly specifies continuous dynamics and the discrete events that alter them.

#### Jeka and Kiemel: human postural control and locomotion

John Jeka and Tim Kiemel's work on human upright posture, multisensory integration, multijoint coordination, balance, locomotion, and system identification provides an especially direct scientific motivation for interpretable hybrid sensorimotor models.

Their research combines structured perturbation experiments, sensory manipulation, feedback-control models, biomechanical plant models, state estimation, and system-identification approaches. This body of work illustrates how a model can be meaningfully tied to experimental data rather than used only as a generic simulation.

A reduced postural-control model may contain continuous states for body-segment position and velocity, center-of-mass motion, muscle activation, sensory estimates, controller states, or sensory weights. Events may include perturbation onset and offset, sensory-reference changes, foot contact, stepping thresholds, recovery steps, changes in visual or support-surface conditions, and controller-mode transitions.

A generic formulation might be:

$$
\dot{x}(t)=f_{q(t)}(x(t),u(t),\theta),
$$

where the state includes biomechanical and neural-control variables, the input includes visual, vestibular, proprioceptive, tactile, or platform-perturbation signals, and the mode represents stance, stepping, recovery, sensory context, or controller configuration.

The potential role of `hybrid-ds-julia` would be to implement reduced-order models transparently. For example, it could support an inverted-pendulum or multi-segment plant coupled to a sensory estimator and feedback controller, with explicit delayed feedback, perturbation events, state-dependent stepping thresholds, and reset maps associated with contact or recovery.

Potential uses include:

- Simulating sensory perturbation experiments with explicit event timing
- Comparing sensory reweighting, state-estimation, and controller-gain hypotheses
- Modeling stance-to-step transitions or balance-recovery actions
- Studying how delays, noise, and sensory availability affect stability
- Performing sensitivity analysis for sensory gains, mechanical parameters, thresholds, and delays
- Comparing control policies subject to realistic force, stepping, or stability constraints
- Designing perturbation protocols that discriminate among competing hypotheses

The package should not be assumed to replace the laboratory's existing experimental, theoretical, and identification methods. The relevant question is whether its explicit event, reset, and sensitivity semantics would make particular lower-dimensional models easier to reproduce, compare, or extend.

#### Ahrens Lab: whole-brain zebrafish sensorimotor behavior

The Ahrens Lab at HHMI Janelia Research Campus studies how large neuronal populations support flexible behavior in larval zebrafish. Its experimental approach combines whole-brain imaging, virtual-reality behavioral paradigms, fictive locomotor recordings, computational analysis, genetics, anatomy, and targeted perturbation. The laboratory's work on motor adaptation, sensorimotor transformations, behavioral-state switching, and positional homeostasis is particularly relevant to reduced-order hybrid dynamical models.

The potential fit is not that whole-brain neural data should be replaced by a low-dimensional ODE model. Rather, a hybrid model could provide a compact and falsifiable representation of a specific mechanistic hypothesis: a small number of neural, sensory, behavioral, or internal-estimate variables evolve continuously; experimentally imposed perturbations and behavioral actions occur as discrete events; and explicit feedback links motor output to the subsequent sensory environment.

For example, in closed-loop virtual-reality paradigms, fictive swim output changes visual feedback, which changes sensory input and then changes later neural activity and motor output. A model might include continuous states for sensory evidence, motor-vigor drive, estimated self-location, accumulated prediction error, neural-population activity, or glial state. It could include discrete events for swim bouts, stimulus onset or offset, changes in visuomotor gain, externally imposed displacement, action-outcome mismatch, behavioral-state transitions, and experimental perturbations.

A general state-and-event representation could be written as:

$$
\dot{x}(t)=f_{q(t)}\bigl(x(t),u(t),\theta\bigr),
$$

where $x(t)$ represents a reduced neural-behavioral state, $u(t)$ represents sensory input or experimental drive, $\theta$ contains physiological and control parameters, and $q(t)$ identifies an active behavioral or experimental mode. At an event condition $g_i(x,t)=0$, the mode and state could change through:

$$
x^+=R_i(x^-,\theta),
\qquad
q^+=T_i(q^-,x^-).
$$

The important scientific question is whether a proposed state, guard, or reset corresponds to experimentally observable quantities and predicts data not used for fitting.

Motor-adaptation experiments with altered visual feedback in a closed-loop virtual environment provide one useful target. In a hybrid formulation, a visual-gain manipulation is an experimental mode switch; fictive swim bouts are discrete motor events; neural and adaptation variables may evolve continuously between bouts; and predictions can be compared with neural activity, behavioral output, and the time course of recalibration. Sensitivity analysis could ask whether predicted adaptation depends most strongly on feedback gain, sensory delay, adaptation time constant, or an internal prediction-error gain.

Brain-wide sensorimotor-transformation experiments suggest a modular architecture that separates sensory encoding, intermediate sensorimotor transformation, motor command, and locomotor output. A reduced hybrid model should not equate correlation with instantaneous motor output to causal motor command. It could instead compare feedforward sensory-to-motor mapping, recurrent state estimation, or state-dependent action-selection architectures against data obtained under multiple visual-feedback conditions.

Behavioral-state switching after unsuccessful action is an especially direct candidate for a threshold model. A stylized hypothesis could include a continuous variable $e(t)$ representing accumulated evidence that action is futile:

$$
\dot{e}(t)=-\lambda e(t)
$$

between swimming events, with a discrete update after an unsuccessful bout:

$$
e^+=e^-+\alpha.
$$

A threshold condition could define a transition from an active mode to a suppressed or passive behavioral mode:

$$
q^+=\mathrm{passive}
\quad\text{when}\quad
e(t)\geq\vartheta.
$$

This is a stylized hypothesis, not a claim that the biological system follows this exact equation. Its value would be to make assumptions about integration, decay, thresholding, and recovery explicit and quantitatively testable against behavioral and neural/glial data. Competing models could use nonlinear accumulation, state-dependent thresholds, stochastic event effects, adaptation of $\alpha$, or an additional latent arousal state.

Work on self-location memory and positional homeostasis provides another natural control-theoretic example. A model could include an internal self-location estimate:

$$
\dot{\hat{p}}(t)=v_{\mathrm{self}}(t),
\qquad
e_p(t)=p_{\mathrm{reference}}-\hat{p}(t),
$$

where $\hat{p}(t)$ is an internal position estimate and $e_p(t)$ is a position error. An imposed displacement can be represented as a reset or perturbation to physical position, sensory input, internal estimate, or some combination, depending on the mechanistic hypothesis. Corrective swim-bout probability, direction, vigor, or termination could be modeled as a state-dependent event policy.

Potential uses of `hybrid-ds-julia` in this setting include:

- Simulation of closed-loop virtual-environment protocols with explicit sensory delay and visuomotor gain changes
- Reduced-order models of motor adaptation, sensory prediction error, and behavioral-state switching
- Event-aware estimation of parameters from neural, glial, fictive-swim, and behavioral data
- Comparison of alternative reset maps for imposed displacement, failed action, sensory perturbation, or behavioral transition
- Sensitivity analysis for feedback gain, delay, evidence accumulation, state decay, threshold location, and controller gain
- Simulation-based comparison of competing mechanistic hypotheses
- Constrained optimization of perturbation timing or gain schedules to distinguish between competing models

The limitation is equally important. Whole-brain neural data are high dimensional, experimentally rich, and shaped by circuitry that cannot in general be reduced to a small number of ODE states without strong assumptions. Any use of `hybrid-ds-julia` would therefore need a deliberately limited scientific target, biologically interpretable reduced states, a clear measurement model, alternative-hypothesis comparison, and tests using held-out perturbation conditions.

The package would complement—not replace—whole-brain imaging pipelines, statistical neural-population analysis, machine learning, circuit mapping, or causal perturbation experiments.

#### Cowan and the LIMBS Laboratory: locomotion, active sensing, system identification, and hybrid mechanics

The Locomotion in Mechanical and Biological Systems (LIMBS) Laboratory, directed by Noah J. Cowan at Johns Hopkins University, studies how animals and robots move, sense, navigate, adapt, and control behavior. Its work spans control theory, nonlinear and geometric mechanics, system identification, robotics, active sensing, neuromechanics, animal locomotion, and experimental analysis of biological control systems.

This research program is already deeply connected to the mathematical territory of hybrid dynamical systems. Contacts, impacts, gait transitions, task changes, mode switches, sensory perturbations, actuator saturation, threshold-triggered behaviors, and intermittent control can all introduce discontinuous changes into otherwise continuous mechanical and neural dynamics.

The relevant question is therefore not whether the LIMBS Laboratory needs a generic claim that hybrid systems are important. The specific question is whether `hybrid-ds-julia` could provide a useful and technically correct implementation environment for a particular class of reduced-order models, experimental protocols, sensitivity calculations, or optimization problems.

The intended role for `hybrid-ds-julia` would be complementary to established robotics, control, identification, and simulation tools. It would not replace multibody simulators, geometric-mechanics formulations, experiment-specific identification methods, robot middleware, or mature optimal-control workflows. Its possible niche is a transparent Julia-native workflow in which a researcher directly specifies:

- A continuous-time plant, controller, estimator, or sensory-state model
- Guard conditions defining contact, behavioral, measurement, or protocol events
- Reset maps, parameter changes, or mode transitions at those events
- A schedule of externally imposed perturbations or sensory manipulations
- Objectives, constraints, and parameter sets for sensitivity analysis or policy comparison

A generic reduced-order formulation might be:

$$
\dot{x}(t)=f_{q(t)}\bigl(x(t),u(t),\theta\bigr),
$$

where $x(t)$ contains mechanical, sensory, neural, controller, or estimator states; $u(t)$ denotes external forcing or measured sensory input; $\theta$ contains plant, controller, and measurement parameters; and $q(t)$ denotes an active contact, gait, behavioral, or controller mode. An event may be defined by:

$$
g_i(x,t,\theta)=0,
$$

with a state and mode update:

$$
x^+=R_i(x^-,\theta),
\qquad
q^+=T_i(q^-,x^-).
$$

The technical value of this representation is that event conditions and event maps are first-class model components rather than informal post-processing logic. It permits a modeler to ask how conclusions change when an impact occurs earlier or later, when a sensory threshold is crossed, when an actuator saturates, when a controller switches, or when an experiment introduces a perturbation.

The LIMBS Laboratory's work on animal locomotion and active sensing provides several plausible test cases. In mechanical locomotion, continuous state may include position, velocity, body orientation, joint configuration, internal compliance, actuator state, and controller state. Discrete events may include foot contact, lift-off, collision, stick-slip transition, takeoff, landing, gait-phase change, or perturbation-triggered recovery step. In active sensing, the state may additionally include a sensory reference, internal estimate, or policy variable; discrete events may include probe movements, sensory sampling, abrupt stimulus changes, or switches between tracking and exploratory behavior.

The laboratory's research on the relation between mechanics and sensory decoding is especially relevant. Work on refuge tracking in weakly electric knifefish emphasizes that locomotor mechanics shape sensory information, and that understanding the sensory system requires modeling the closed loop between the animal, its plant, its movement, and its sensory input. A hybrid extension becomes appropriate when the experiment or hypothesized controller involves discrete sensory movements, abrupt perturbations, mode changes, contact events, or thresholded behavioral decisions.

Potential uses of `hybrid-ds-julia` in this research area include:

- Reduced-order models of locomotor plants coupled to neural feedback controllers
- Simulation of stance, stepping, contact, lift-off, and perturbation-recovery transitions
- Explicit experimental-protocol models with visual, vestibular, tactile, mechanical, or electrosensory stimuli that change at scheduled or state-dependent times
- Active-sensing models with intermittent measurements, sampling actions, state-dependent probing, or mode-dependent sensory gains
- Closed-loop system-identification studies comparing plant, controller, estimator, delay, noise, and event assumptions
- Sensitivity analysis for feedback gain, mechanical stiffness, damping, sensory delay, threshold placement, reset-map parameters, and event-time variation
- Optimization of constrained controller, sensing, or perturbation policies
- Reproducible compact examples that expose equations, events, assumptions, and diagnostics directly

Hybrid sensitivity requires special care. In a smooth ODE model, sensitivities can be obtained by integrating variational equations. In a hybrid model, a parameter perturbation can also change the time at which an event occurs and the post-event state. A correct first-order calculation must therefore account for both continuous evolution and event-induced variation, for example through a saltation-matrix or equivalent reset-aware update. The most important questions for the LIMBS Laboratory are concrete:

1. Which research models would benefit from an explicit ODE-plus-guard-plus-reset interface rather than an existing multibody, control, or identification workflow?
2. Are there scientifically useful reduced-order examples in locomotion, active sensing, or experimental perturbation for which event-time sensitivity is central?
3. What event semantics, differentiation behavior, optimization interface, or numerical diagnostics would be required for the package to be technically trustworthy in this setting?
4. Which existing workflows should the package interoperate with, rather than attempt to reproduce?
5. Can one identify a compact benchmark in which the package adds reproducibility, interpretable event logic, or sensitivity analysis beyond what present tools already provide?

The package should be judged useful only if it addresses a real gap in those questions. It should not be described as a replacement for established expertise in nonlinear mechanics, closed-loop identification, control, or robotic experimentation.

#### Fortune: feedback control, locomotor variability, and active sensing in weakly electric fish

Eric S. Fortune studies mechanisms and evolution of animal behavior, with important work on sensorimotor control, active sensing, locomotion, electrosensory behavior, refuge tracking, behavioral variability, and feedback control in weakly electric fish. He is currently an Associate Professor of Biological Sciences at the New Jersey Institute of Technology.

The potential relevance of `hybrid-ds-julia` is strongest where a model must represent continuous closed-loop locomotor and sensory dynamics together with explicitly discrete actions, manipulations, or behavioral modes. It is not that refuge tracking or active sensing must be treated as hybrid by default. Many experimental tasks can be analyzed well with smooth linear, nonlinear, frequency-domain, or system-identification methods. A hybrid representation becomes worthwhile only when the scientific question depends on transitions, intermittent actions, state-dependent sensing, abrupt environmental changes, trial-protocol events, or mode-dependent control.

A generic closed-loop formulation might separate plant, controller, and sensory dynamics:

$$
\dot{x}_p=f_p(x_p,u,\theta_p),
$$

$$
\dot{x}_c=f_c(x_c,y,\theta_c),
$$

$$
u=\pi_{q(t)}(x_c,y,\theta_\pi),
$$

where $x_p$ represents locomotor plant state, $x_c$ represents internal controller or estimator state, $y$ represents sensory input, and $q(t)$ represents a behavioral or experimental mode. The sensory signal may depend on both animal motion and environment:

$$
y(t)=h\bigl(x_p(t),r(t),\theta_s\bigr)+\eta(t),
$$

where $r(t)$ is refuge or environmental motion and $\eta(t)$ represents sensory or measurement noise.

A hybrid extension can represent events such as:

- Onset, offset, or abrupt phase changes of refuge motion
- Transitions between predictable and unpredictable stimulus regimes
- Changes in refuge dynamics or destabilizing feedback
- Discrete probe movements or active-sensing actions
- Sensory perturbation, temporary occlusion, jamming, or social electrosensory events
- Threshold-triggered changes in tracking gain, body position, swimming direction, or control strategy
- Trial boundaries, conditioning events, or changes in sensory context
- Switching between locomotor, exploratory, stationary, or recovery modes

Research on the critical role of locomotion mechanics in decoding sensory systems provides a key conceptual basis. Refuge tracking in *Eigenmannia* is useful for sensorimotor-control research precisely because locomotor mechanics and sensory encoding must be understood together in closed loop. The package could support a reduced-order implementation in which fish mechanics, sensory-image dynamics, neural control, and experimental forcing are explicit components.

This would allow investigators to test which conclusions depend on plant dynamics, controller dynamics, sensory delay, feedback gain, or stimulus structure. An experiment could compare modes such as:

$$
q\in\{
\mathrm{predictable},
\mathrm{unpredictable},
\mathrm{sensory\ cue\ available},
\mathrm{sensory\ cue\ absent}
\},
$$

with each mode selecting a different controller gain, estimator gain, delay, noise level, or active-sensing policy.

The point would not be to infer an unobserved controller from a small dataset without constraint. Rather, the model would formalize competing hypotheses and ask whether they make distinguishable predictions under carefully designed perturbation experiments.

Work on sensorimotor adaptation to destabilizing dynamics is particularly suitable for this kind of model. A gradual or abrupt change in the relation between fish movement and sensory consequences can be represented as a parameter change in the plant, sensory environment, or closed-loop feedback pathway. The model could compare competing explanations:

$$
\text{plant adaptation},
\qquad
\text{controller-gain adaptation},
\qquad
\text{state-estimator adaptation},
\qquad
\text{mode switching},
$$

or combinations of these mechanisms.

Potential uses of `hybrid-ds-julia` in this setting include:

- Event-aware closed-loop simulations of refuge tracking and active-sensing tasks
- Joint plant-controller-estimator models with explicit feedback and perturbation protocols
- Comparison of smooth versus switching control laws under predictable, destabilizing, or noisy conditions
- Sensitivity analysis for plant parameters, sensory delay, feedback gain, internal-model parameters, noise level, and transition thresholds
- Analysis of how trial timing or stimulus structure affects identifiability of plant and controller parameters
- Optimization of perturbation schedules or stimulus designs that distinguish competing feedback-control hypotheses
- Simulation of individual variability in locomotor plant dynamics and robustness to controller/plant mismatch
- Explicit representation of trial boundaries and intervention times as part of the model

The relationship between individual variability and feedback control is especially important. If different animals have different locomotor plants but performance remains robust, a model can ask whether the controller is individualized, whether feedback compensates for mismatch, or whether multiple plant/controller pairs produce similarly effective closed-loop behavior.

The central technical challenge is closed-loop identification. Because the animal's action changes the sensory stimulus later used to infer the controller, open-loop assumptions can produce biased or misleading estimates. A hybrid model adds another requirement: if events change the stimulus, controller, or state, parameter sensitivities must include changed event timing and reset maps.

Questions for Dr. Fortune and collaborators include:

1. Which experimental phenomena genuinely require a discrete mode, event, or reset model rather than a smooth closed-loop representation?
2. Are stimulus-predictability changes, active-sensing actions, trial events, or destabilizing perturbations best modeled as externally scheduled inputs, state-triggered events, or changes in controller architecture?
3. Would reset-aware sensitivity analysis add scientific value in designing experiments or testing robustness of closed-loop hypotheses?
4. What quantities are observable well enough to constrain a reduced-order hybrid model?
5. Which results would demonstrate that the package adds value beyond established frequency-domain, system-identification, and control-theoretic tools?

`hybrid-ds-julia` should be useful here only as a transparent hypothesis-testing and simulation environment. It should not be presented as a replacement for detailed experimental analysis, closed-loop system identification, or the biological insight that comes from the fish model itself.

#### Hines and the NEURON ecosystem: neural and network simulation with events, discontinuities, and multiscale control

Michael L. Hines has made foundational contributions to computational neuroscience through the NEURON simulation environment and related work on numerical methods, variable-step integration, parallel neural-network simulation, event-driven mechanisms, interoperability, and reproducible modeling. NEURON is a mature and extensively validated environment for simulating biophysically detailed neurons and neural networks, including compartmental morphology, cable equations, membrane mechanisms, ion channels, synapses, stochastic processes, stimulation, and distributed network computation.

The relationship between `hybrid-ds-julia` and NEURON must therefore be stated with particular care. `hybrid-ds-julia` is not intended to compete with, replace, or reproduce NEURON. A general ODE-and-event package would not provide NEURON's mature infrastructure for morphologically detailed cable models, domain-specific model descriptions, synaptic event handling, mechanism libraries, network simulation, variable-step solvers, parallel execution, validation history, ModelDB ecosystem, or broad community expertise.

The possible role for `hybrid-ds-julia` is instead at a different modeling layer: reduced-order, system-level, experimental-protocol, control, optimization, or cross-domain models in which neural or cellular dynamics interact with externally defined discrete interventions, policies, thresholds, and non-neural states.

In that role, the package might serve as:

- A compact environment for low-dimensional neural mass, neural population, conductance-based, oscillator, or state-space surrogate models
- A systems-level wrapper around a reduced neural model coupled to behavior, biomechanics, pharmacology, stimulation, or experimental control
- A tool for explicit intervention schedules, threshold-triggered stimulation, adaptive closed-loop control, dosing events, and experimental-protocol logic
- A platform for sensitivity analysis and constrained optimization of systems that include neural states but are not principally compartmental-neuron simulations
- A possible pre- or post-processing companion to detailed NEURON simulations, if a scientifically and technically sound coupling interface can be defined

A reduced-order hybrid neural system could be written as:

$$
\dot{x}(t)=f_{q(t)}\bigl(x(t),I(t),p(t),\theta\bigr),
$$

where $x(t)$ includes neural, synaptic, network, cellular, behavioral, or physiological states; $I(t)$ is stimulation or synaptic drive; $p(t)$ represents intervention or protocol state; $\theta$ contains biophysical or phenomenological parameters; and $q(t)$ selects an active treatment, stimulation, behavioral, or experimental mode. Events might include:

- Current-pulse onset, offset, amplitude change, or waveform change
- Synaptic input, spike detection, or network event
- State-dependent stimulation triggered by a measured neural or behavioral variable
- Electrode, recording, or stimulation artifact events
- Seizure-like threshold crossing, burst termination, or mode transition
- Closed-loop neuromodulation action
- Drug administration, concentration threshold, receptor-blockade change, or washout protocol
- Trial onset, sensory stimulus transition, task phase, reinforcement signal, or behavioral action
- A coupling event between a detailed neuronal simulator and a reduced external system

At cellular and network levels, NEURON already treats several of these problems as first-class concerns. It supports variable-order and variable-step integration, event delivery, parallel networks, and detailed biophysical mechanisms. The existing sophistication has two implications for `hybrid-ds-julia`.

First, the package should not make generic claims such as “NEURON cannot model events” or “hybrid event support is missing from neural simulators.” Such claims would be false or misleading. Event-driven synaptic mechanisms and network simulation are central to modern computational-neuroscience tools.

Second, any proposed complementarity must identify a genuinely distinct use case. A plausible distinction is between an event internal to a detailed neural-network simulation and an event that changes the governing model at the system or experimental-policy level:

$$
\text{neural dynamics}
\longrightarrow
\text{estimated biomarker}
\longrightarrow
\text{stimulation decision}
\longrightarrow
\text{changed stimulation protocol}
\longrightarrow
\text{future neural and behavioral dynamics}.
$$

A model of this form might combine a low-dimensional neural state, a behavioral state, a measurement process, an estimator, and a thresholded controller. The hybrid framework would make a decision rule explicit:

$$
\text{apply stimulation if }\hat{z}(t)\geq z_{\mathrm{threshold}},
$$

or:

$$
\text{change mode if}
\int_{t-T}^{t}\phi(x(s))\,ds
\geq\Theta.
$$

Such a model could be useful for studying assumptions in adaptive stimulation, experimental design, neuroprosthetic control, pharmacological intervention, or neural-behavioral coupling. It is not a substitute for detailed cellular simulation when morphology, spatial ion dynamics, dendritic integration, channel kinetics, or network connectivity are essential to the scientific question.

Potential uses of `hybrid-ds-julia` in a NEURON-adjacent context include:

- Reduced-order neural or neural-mass models coupled to discrete stimulation, recording, behavioral, or treatment events
- Simulation of adaptive closed-loop stimulation policies with explicit safety thresholds, delays, measurement noise, and control constraints
- Comparison of open-loop, scheduled, threshold-triggered, and estimator-based stimulation protocols
- Sensitivity analysis for stimulation amplitude, timing, delay, measurement noise, state-estimator parameters, and intervention thresholds
- Constrained optimization of stimulation schedules or control policies in low-dimensional surrogate models
- Neural-behavioral or neural-pharmacological systems in which external subsystems are naturally represented by ODEs and discrete events
- Experimental-design simulation that compares which stimulation or measurement schedules distinguish competing hypotheses
- Development of reduced-order surrogates for use when a full multicompartment network simulation would be too costly inside a policy-optimization loop

The numerical requirements are demanding. State-triggered events can cause discontinuities in parameters, inputs, modes, or states. When estimating gradients or sensitivities, a correct method must include the dependence of event timing on parameters and state, not merely differentiate the smooth intervals between events. If an external decision rule depends on a threshold crossing, then both threshold-crossing time and state transition must be handled consistently.

A possible future interoperability direction would be deliberately modest: use detailed NEURON simulations to generate data or reduced-order surrogates, then use `hybrid-ds-julia` for system-level policy exploration; or use a reduced-order external model to determine stimulation or intervention protocols subsequently evaluated in NEURON. Direct co-simulation would require explicit agreement about time stepping, event ordering, state transfer, units, reproducibility, and numerical error control. It should not be claimed until demonstrated on a concrete benchmark.

Questions for Dr. Hines and the NEURON community include:

1. What system-level hybrid problems are not already adequately handled by NEURON, CoreNEURON, Python control scripts, or existing co-simulation workflows?
2. Would a Julia-native reduced-order ODE-and-event environment be useful for adaptive stimulation, neural-behavioral coupling, pharmacological protocols, or multiscale policy modeling?
3. What would a scientifically meaningful NEURON-adjacent benchmark look like?
4. Which event semantics, solver guarantees, sensitivity methods, and numerical diagnostics would be necessary before using such a workflow for neural applications?
5. Is one-way model exchange, surrogate fitting, protocol export, or direct co-simulation the most realistic interoperability target?
6. Which capabilities should remain explicitly outside project scope because NEURON and related neuroscience ecosystems already address them more effectively?

The most credible position is one of complementarity. `hybrid-ds-julia` may become useful for transparent low-dimensional systems models and event-aware intervention policies that sit around, above, or alongside detailed neural simulation. It should not present itself as an alternative implementation of NEURON's core scientific and computational mission.

## Domains where `hybrid-ds-julia` would be less helpful

### Why these settings are difficult

Hybrid dynamical systems become difficult to use responsibly when recorded events do not identify the continuous state that is meant to drive the model.

A dataset may record appointments, prescriptions, diagnostic codes, symptom questionnaires, hospitalizations, medication changes, and changes in function. These observations can establish that a person’s symptoms or care pathway changed. They may not establish whether the dominant driver was one disease-specific biological process, multiple interacting processes, a co-occurring condition, medication effects, behavior, environmental exposures, changing access to care, or a combination of these factors.

In such settings, a model can often represent observable parts of the chain:

- Timing of documented clinical events
- Medication and treatment exposure
- Healthcare utilization
- Symptom and functional-status documentation
- Selected physiological measurements
- Monitoring and care-pathway decisions

The difficult step is causal identification: determining which latent continuous state generated the observations, how that state changes over time, and whether an intervention caused a subsequent change. A model may fit observed trajectories while assigning them to the wrong mechanism.

More formally, if $y(t)$ is an observed symptom or function score, it may depend on several partially unobserved processes:

$$
y(t)=f_1(x_1(t))+f_2(x_2(t))+\cdots+f_k(x_k(t))+\epsilon(t).
$$

When the relevant $x_i(t)$ are poorly measured, nonunique, or causally confounded, fitting a model to $y(t)$ does not establish which process is responsible. This is a limitation of measurement and causal identifiability, not a judgment about the legitimacy or severity of any illness.

### Some infectious and post-infectious conditions

Infection itself is not a limitation. Tuberculosis and HIV, for example, can be suitable applications when pathogen burden, drug exposure, treatment schedules, resistance, and relevant biomarkers are sufficiently defined and measured.

Challenges arise in some infectious and post-infectious settings when persistent symptoms have multiple possible contributors and available observations do not identify the biological process that should form the model’s continuous state. In these settings, event history may be useful for descriptive or care-pathway analysis but insufficient for disease-specific mechanistic inference.

#### Long COVID

Long COVID can involve discrete, timestamped events such as acute infection, reinfection, hospitalization, medication changes, diagnostic testing, rehabilitation, work-disability transitions, and follow-up visits. These events can support carefully scoped monitoring, care-pathway, utilization, or organ-specific models.

The central difficulty is that long COVID is heterogeneous, its mechanisms remain incompletely resolved, and routine laboratory results do not reliably distinguish it from other illnesses. Persistent symptoms may reflect multiple possible and potentially interacting processes, including immune dysregulation, tissue injury, altered autonomic function, post-intensive-care effects, concurrent conditions, medication effects, and contextual factors.

`hybrid-ds-julia` may be useful for explicitly limited questions, such as rehabilitation scheduling, monitoring policies, longitudinal function tracking, or a well-defined organ-specific complication. It should not be presented as a validated model that identifies a single cause of an individual’s persistent symptoms or selects individualized treatment on that basis.

#### Persistent symptoms following Lyme disease treatment

Lyme disease can be a suitable target for carefully scoped models of tick exposure, early infection, antimicrobial PK/PD, treatment scheduling, and objectively documented manifestations such as arthritis, neurologic disease, or carditis.

Persistent nonspecific symptoms following appropriate treatment are a more difficult modeling target. Fatigue, pain, cognitive complaints, and reduced function may have several possible contributors, including reinfection, delayed or incomplete diagnosis, immune or tissue effects, co-occurring illness, sleep disturbance, medication effects, other infections, and causes unrelated to active *Borrelia* infection.

A model may represent treatment timing, diagnostic testing, antibiotic exposure, symptom documentation, and follow-up care. Those events alone do not establish whether a persistent symptom trajectory represents ongoing infection, treatment failure, a post-infectious process, or another contributor. Models in this setting should remain carefully scoped and should not be used to infer an individual’s unmeasured mechanism or justify individualized treatment without strong external validation.

### ME/CFS

Myalgic encephalomyelitis/chronic fatigue syndrome (ME/CFS) is a particularly clear example of a setting in which clinically meaningful events can be recorded without providing an identified disease-specific continuous state.

Potentially modelable observations include symptom and function tracking, healthcare encounters, medication events, orthostatic measurements where available, activity and rest records, work or school participation, and patient-reported post-exertional symptom worsening. Such information may support descriptive longitudinal analysis, monitoring workflows, and explicitly limited care-pathway questions.

The central challenge is that there is no confirmatory diagnostic test or validated biomarker that identifies ME/CFS as a single measurable biological state. Fatigue, post-exertional symptom worsening, pain, sleep disturbance, cognitive difficulty, autonomic symptoms, and functional limitation can coexist with other conditions or be influenced by multiple processes. Alternative explanations, comorbidities, medication effects, sleep disorders, activity patterns, and time-varying illness severity can confound relationships between recorded interventions and subsequent outcomes.

For example, a treatment change may occur because a person was already worsening. An observational model could then associate the treatment with worse later symptoms even when worsening, rather than treatment, caused both the intervention and the later outcome.

`hybrid-ds-julia` should therefore not be framed as identifying an individual’s ME/CFS mechanism or selecting treatment from sparse symptom and event records. It may still support descriptive symptom/function trajectories, monitoring systems, care-delivery operations, and sensitivity analyses that make competing assumptions explicit.

### Mental health and complex behavioral care

Mental health, substance use, and other forms of complex behavioral care can contain rich event histories: medication changes, therapy sessions, emergency visits, admissions, discharges, symptom-scale measurements, relapse episodes, substance-use treatment events, housing changes, employment changes, and social-service interventions.

These events can support operational models of access, scheduling, continuity of care, monitoring, crisis response, capacity planning, and service delivery. Validated symptom scales may also support carefully defined descriptive or predictive tasks.

However, mechanistic individual-level disease models can be difficult because symptoms and outcomes depend on many interacting, time-varying influences. These can include social and economic conditions, therapeutic relationship, trauma exposure, family and community support, concurrent physical illness, substance use, medication adherence, treatment availability, clinician selection, and patient preferences.

Treatment-selection confounding is especially important. A medication change, hospitalization, or intensive intervention often occurs because symptoms, risk, or social circumstances were already worsening. A model trained only on observational event histories can mistake this association for a causal treatment effect.

In these settings, `hybrid-ds-julia` may be useful for care-pathway simulation, resource planning, monitoring workflows, and sensitivity analysis. It should not be assumed to recover a single latent disease mechanism from routine records or to make unvalidated individualized treatment recommendations.

### What remains appropriate in difficult settings

A setting being less suitable for a mechanistic hybrid model does not make it unsuitable for all modeling. In the difficult domains above, `hybrid-ds-julia` may still be useful when the model’s purpose and limitations are explicit.

Appropriate uses may include:

- Descriptive models of symptom, function, or care trajectories
- Monitoring and measurement workflows
- Simulation of care pathways, referral rules, service capacity, and follow-up schedules
- Cohort-level hypothesis generation
- Sensitivity analyses across multiple explicitly stated causal assumptions
- Analyses of missingness, delay, monitoring frequency, and measurement uncertainty
- Operational studies that do not claim to identify disease-specific biology
- Educational simulations that distinguish observed events from hypothesized latent mechanisms

Such models should state clearly which states are directly measured, which are inferred, which assumptions are uncertain, and which decisions the model is not validated to support. They should not be used as a substitute for diagnosis, clinical judgment, informed consent, or external validation in the population and setting where they would be applied.
