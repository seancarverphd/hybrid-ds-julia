
## Test beds

The initial test beds should be scientifically recognizable, numerically demanding enough to demonstrate the value of hybrid methods, and small enough to support reproducible end-to-end workflows.

The purpose is not to claim immediate coverage of every QSP or PK/PD application. The purpose is to establish a sequence of examples in which event-aware simulation, variational equations, saltation updates, multiple shooting, and schedule-facing analysis can be validated and compared with simpler workflows.

The proposed sequence begins with a compact deterministic treatment model, expands to higher-dimensional biomedical systems, and then adds stochastic and Filippov-style benchmark problems.

### First biomedical target

The first flagship biomedical example should be an **immuno-oncology tumor–immune QSP model with pulsed dosing and toxicity-triggered treatment holds**.

A representative model can include states for:

\[
T(t) = \text{tumor burden},
\]

\[
E(t) = \text{effector immune-cell activity},
\]

\[
C(t) = \text{drug concentration},
\]

\[
B(t) = \text{toxicity or biomarker burden}.
\]

Between events, a compact model might have the form

\[
\dot{T}
=
r_T T
\left(
1-\frac{T}{K_T}
\right)
-
k_E E T,
\]

\[
\dot{E}
=
s_E
+
\alpha_E
\frac{T}{K_E+T}
-
d_E E
-
\gamma_E C E,
\]

\[
\dot{C}
=
-k_C C,
\]

\[
\dot{B}
=
\alpha_B C
+
\beta_B E
-
k_B B.
\]

This system is only illustrative. The specific biological components can be adjusted as the benchmark is refined. The key point is that the model should contain a treatment-control structure with clinically interpretable events.

For example, at planned dosing times \(t_k\),

\[
C(t_k^+)
=
C(t_k^-)
+
D_k,
\]

where \(D_k\) is the administered dose.

A toxicity hold may be triggered when

\[
B(t)
\geq
B_{\mathrm{hold}},
\]

causing a transition from an active-treatment mode to a hold mode. In the hold mode, scheduled doses are skipped until toxicity falls below a recovery threshold:

\[
B(t)
\leq
B_{\mathrm{restart}}.
\]

The system can therefore have modes such as:

- treatment active,
- treatment hold,
- recovery monitoring,
- reduced-dose rechallenge,
- or alternative therapy.

The scientific questions are straightforward and decision-relevant:

- Which schedules suppress tumor burden while avoiding prolonged toxicity?
- How sensitive are outcomes to dose interval, dose intensity, or hold thresholds?
- Does a small change in a threshold produce a large change in time on treatment or long-term tumor control?
- Are some treatment schedules robust across plausible parameter variation?
- Do different mechanisms of action produce distinct schedule-response regimes?

The numerical questions are equally important:

- Can the simulator locate threshold crossings reliably?
- Are event times and state resets reproducible under solver tolerances?
- Do sensitivities propagated through the hold and restart events agree with local perturbation experiments?
- Does multiple shooting improve conditioning for long-horizon schedule optimization?
- Where do grazing events or near-threshold trajectories produce ill-conditioned derivatives?

This first example should be intentionally compact. It should be understandable from the README and reproducible from a small number of scripts or notebooks. Its role is to demonstrate the full workflow: model specification, event handling, simulation, sensitivity propagation, and schedule-facing analysis.

### Next biomedical extensions

After the initial tumor–immune treatment-hold model, the next examples should increase biological and numerical complexity without changing the core message of the package.

Possible extensions include:

- **Combination therapy models** with separate dosing schedules, synergistic or antagonistic effects, and treatment rules that depend on multiple biomarkers.
- **Autoimmune or inflammatory disease models** with flare-remission dynamics, steroid tapering, rescue therapy, or biomarker-triggered treatment escalation.
- **Cell therapy models** with conditioning regimens, cell infusion events, delayed expansion phases, cytokine-release toxicity, and dose-adjustment logic.
- **PK/PD models with adaptive dosing** in which treatment changes depend on drug concentration, target engagement, toxicity, or efficacy biomarkers.
- **Longitudinal virtual-patient studies** in which parameter heterogeneity and decision rules are varied together to assess regimen robustness across plausible patient populations.

A useful second-stage benchmark may involve a higher-dimensional model with two or more treatment agents, a toxicity state, and a state-triggered decision policy. That would allow the package to demonstrate both scheduled impulses and state-dependent transitions in the same system.

For example, a combination-treatment model could include:

\[
C_1(t),
\qquad
C_2(t),
\]

for two drug exposures, along with tumor, immune, and toxicity states. A treatment rule might reduce or stop one agent when toxicity crosses a threshold while allowing the other to continue. Such a model naturally produces hybrid trajectories whose interpretation depends on the timing and ordering of events.

These extensions should be selected for their ability to demonstrate a practical progression:

1. A small deterministic event-driven model.
2. A higher-dimensional QSP-style model.
3. A model with multiple treatment modes and competing intervention rules.
4. A cohort or virtual-patient workflow.
5. A stochastic or uncertainty-aware extension.

### Mechanistic stochastic and Bayesian extensions

Once the deterministic hybrid core is stable, the package can expand toward stochastic and Bayesian workflows for systems in which uncertainty, heterogeneity, or random events materially affect the scientific question.

A first stochastic extension could add random effects, stochastic forcing, or event-time variability to an otherwise deterministic treatment model. For example, patient-level parameters may be sampled from a distribution:

\[
\theta_i
\sim
p(\theta \mid \eta_i),
\]

where \(i\) indexes a virtual patient and \(\eta_i\) represents patient-specific random effects.

This can be combined with deterministic treatment events and state-triggered treatment logic. The resulting workflow would allow users to ask not only whether a schedule works for a nominal trajectory, but also how robust the schedule is across a population.

A more advanced extension could represent uncertainty in unobserved biology through stochastic differential equations or jump processes:

\[
dX_t
=
f(X_t,t,\theta)\,dt
+
g(X_t,t,\theta)\,dW_t
+
J(X_{t^-},t,\theta)\,dN_t.
\]

The deterministic scheduled intervention structure remains explicit, while stochastic terms represent biological fluctuations, unobserved disturbances, variable adherence, or random clinical events.

Bayesian parameter inference is another natural extension. A modeler may specify priors over mechanistic parameters:

\[
p(\theta),
\]

combine those with a likelihood for longitudinal observations:

\[
p(y \mid \theta),
\]

and obtain a posterior distribution:

\[
p(\theta \mid y)
\propto
p(y \mid \theta)p(\theta).
\]

For hybrid models, the likelihood can depend strongly on event timing, treatment holds, threshold crossings, and reset states. Event-aware sensitivities can therefore be useful for gradient-based inference, Laplace approximations, variational methods, or Hamiltonian Monte Carlo workflows.

The main purpose of this stage is not to provide a complete Bayesian pharmacometrics platform. It is to demonstrate that hybrid event structure can be retained when uncertainty is introduced, rather than being simplified away before inference or population analysis begins.

### Filippov pseudo-Hopf normal form

A mathematically focused benchmark should accompany the biomedical examples. One useful candidate is a Filippov pseudo-Hopf normal form, which provides a compact test problem for switching surfaces, discontinuous vector fields, bifurcation structure, and hybrid sensitivity calculations.

A Filippov system has different vector fields on different sides of a switching surface. In two dimensions, one may write:

\[
\dot{x}
=
f^+(x,\mu)
\qquad \text{when } h(x)>0,
\]

\[
\dot{x}
=
f^-(x,\mu)
\qquad \text{when } h(x)<0,
\]

where \(h(x)=0\) defines the switching boundary and \(\mu\) is a bifurcation parameter.

A pseudo-Hopf bifurcation is a nonsmooth analogue of a Hopf-type transition, in which a periodic orbit or related oscillatory behavior arises through the interaction of the vector fields and the switching boundary rather than through the classical smooth-system eigenvalue crossing alone.

This benchmark is useful because it can expose numerical issues that are harder to see in a high-dimensional biomedical model:

- transverse crossing versus tangential contact with a switching surface,
- sensitivity growth near grazing events,
- discontinuous changes in the vector field,
- continuation of periodic orbits across parameter changes,
- and conditioning of shooting formulations near nonsmooth bifurcations.

The Filippov benchmark should not be positioned as a biomedical model. Its purpose is to validate the mathematical core of the package under controlled conditions where known hybrid behavior can be reproduced, visualized, and compared across numerical methods.

A complete benchmark workflow could include:

- direct simulation of trajectories on both sides of the switching surface,
- event detection and mode transitions,
- computation of periodic-orbit candidates,
- multiple-shooting refinement,
- variational and saltation-based sensitivities,
- parameter continuation,
- and comparison against finite-difference sensitivities.

Together, the biomedical and Filippov test beds create a complementary validation strategy. The biomedical models demonstrate translational relevance, while the normal-form benchmark demonstrates that the underlying hybrid numerical machinery behaves correctly in a setting where nonsmooth dynamics can be examined directly.