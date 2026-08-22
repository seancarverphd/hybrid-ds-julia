## Further reading

This section is organized to mirror the mathematical, computational, application, and limitation sections of this README. It is intentionally a curated starting point rather than a comprehensive bibliography. Readers should consult original papers, authoritative guidelines, maintained software documentation, and domain experts before relying on a model for scientific, engineering, clinical, or operational decisions.

### Hybrid-systems foundations, events, and sensitivity analysis

#### Hybrid transitions, saltation matrices, and event-aware derivatives

- Goebel, R., Sanfelice, R. G., and Teel, A. R. (2012). *Hybrid Dynamical Systems: Modeling, Stability, and Robustness*. Princeton University Press.

  This textbook develops a general framework for hybrid inclusions, including flow and jump sets, stability, robustness, and well-posedness. It is a foundational reference for formalizing continuous dynamics and discrete transitions rather than treating events as informal simulation callbacks.

- di Bernardo, M., Budd, C. J., Champneys, A. R., and Kowalczyk, P. (2008). *Piecewise-Smooth Dynamical Systems: Theory and Applications*. Springer.

  This textbook covers discontinuity-induced bifurcations, switching systems, impacts, grazing, and other phenomena that arise when a trajectory encounters a nonsmooth boundary. It is especially useful for interpreting threshold crossings, event-order changes, and numerical fragility near grazing events.

- Henzinger, T. A. (1996). The theory of hybrid automata. In *Proceedings of the 11th Annual IEEE Symposium on Logic in Computer Science*, 278–292. https://doi.org/10.1109/LICS.1996.561342

  A foundational formalism for systems with discrete modes, continuous flows, invariants, guards, and transitions. It provides useful conceptual vocabulary for specifying the mode logic and event semantics that `hybrid-ds-julia` aims to make explicit.

- Kong, N. J., Payne, J. J., Zhu, J., and Johnson, A. M. (2024). Saltation matrices: The essential tool for linearizing hybrid dynamical systems. *Proceedings of the IEEE*, 112(2), 161–196. https://doi.org/10.1109/JPROC.2023.3339933

  This review explains saltation matrices and their role in first-order linearization across hybrid events, including event-time variation, reset maps, and mode changes. It is a direct mathematical reference for the package’s planned event-aware sensitivity layer.

- Saccon, A., van de Wouw, N., and Nijmeijer, H. (2014). Sensitivity analysis of hybrid systems with state jumps with application to trajectory tracking. *Proceedings of the IEEE Conference on Decision and Control*.

  This paper develops sensitivity analysis for hybrid trajectories with state jumps, including the effect of event timing on trajectory perturbations. It is directly relevant to verifying how event-aware derivatives should propagate through resets and mode changes.

- Galvanetto, U., and Magri, L. (2020). Modeling and sensitivity analysis methodology for hybrid dynamical systems. *Journal of Computational and Nonlinear Dynamics*, 15(2). https://doi.org/10.1115/1.4045066

  This paper presents a modeling and sensitivity-analysis methodology for hybrid systems with discontinuities and transitions. It provides practical context for structuring event logic and interpreting sensitivity results when the trajectory is only piecewise smooth.

- Esposito, J. M., and Kumar, V. (2000). A state event detection algorithm for numerically simulating hybrid systems. *Proceedings of the 2000 IEEE International Conference on Robotics and Automation*, 154–160. https://doi.org/10.1109/ROBOT.2000.844068

  This paper addresses numerical detection and localization of state events in hybrid simulation. It is directly relevant to treating guard crossings, rather than merely sampled-time branches, as reproducible numerical objects.

#### Identifiability, validation, and uncertainty

- Raue, A., Kreutz, C., Maiwald, T., Bachmann, J., Schilling, M., Klingmüller, U., and Timmer, J. (2009). Structural and practical identifiability analysis of partially observed dynamical models by exploiting the profile likelihood. *Bioinformatics*, 25(15), 1923–1929. https://doi.org/10.1093/bioinformatics/btp358

  This paper distinguishes structural from practical parameter identifiability and presents profile likelihoods for partially observed dynamical models. It is relevant when calibrating event-rich PK/PD or QSP models whose latent mechanisms, thresholds, and parameters may not be uniquely supported by available data.

- Villaverde, A. F., and Banga, J. R. (2014). Reverse engineering and identification in systems biology: Strategies, perspectives and challenges. *Journal of the Royal Society Interface*, 11(91), 20130505. https://doi.org/10.1098/rsif.2013.0505

  This review surveys parameter estimation, model selection, experimental design, identifiability, and related inverse-problem challenges in systems biology. Its scope is useful for situating calibration and validation as part of model development rather than post hoc fitting.

- Saltelli, A., Ratto, M., Andres, T., et al. (2008). *Global Sensitivity Analysis: The Primer*. Wiley. https://doi.org/10.1002/9780470725184

  This textbook introduces global sensitivity-analysis concepts and methods for evaluating how uncertainty in model inputs affects outputs. It is useful for parameter, intervention, and policy studies, while event probabilities and event-sequence changes should be treated as explicit outputs in hybrid applications.

#### Multiple shooting, optimization, and parallel simulation

- Bock, H. G., and Plitt, K. J. (1984). A multiple shooting algorithm for direct solution of optimal control problems. *Proceedings of the IFAC World Congress*.

  This foundational paper introduces multiple shooting for the direct numerical solution of optimal-control problems. Its interval-based formulation motivates the planned use of event-aware continuity constraints for long, sensitive, or unstable hybrid trajectories.

- Diehl, M., Bock, H. G., Diedam, H., and Wieber, P.-B. (2006). Fast direct multiple shooting algorithms for optimal robot control. In *Fast Motions in Biomechanics and Robotics*.

  This chapter develops efficient direct multiple-shooting methods for optimal-control problems in robotics. Its computational ideas are transferable to event-aware trajectory optimization, although hybrid treatment and pharmacology models require their own handling of guards, resets, and changing event sequences.

- Betts, J. T. (2010). *Practical Methods for Optimal Control and Estimation Using Nonlinear Programming* (2nd ed.). SIAM.

  This textbook covers direct transcription, shooting methods, nonlinear programming, estimation, and optimal-control implementation. It provides broad practical context for the package’s planned multiple-shooting, calibration, and constrained policy-optimization workflows.

- Rackauckas, C., and Nie, Q. (2017). DifferentialEquations.jl—A performant and feature-rich ecosystem for solving differential equations in Julia. *Journal of Open Research Software*, 5(1), 15. https://doi.org/10.5334/jors.151

  This paper describes the Julia differential-equations ecosystem that supplies the solver, callback, and composable numerical infrastructure on which `hybrid-ds-julia` can build. It is an implementation foundation rather than a substitute for explicit hybrid-event sensitivity theory.

- Rackauckas, C., Ma, Y., Dixit, V., et al. (2020). Universal differential equations for scientific machine learning. *arXiv:2001.04385*. https://arxiv.org/abs/2001.04385

  This paper introduces universal differential equations, which combine mechanistic differential-equation structure with learned components. It is relevant to learning limited unknown interactions or model discrepancies while retaining explicit interventions, modes, and event logic.

- SciML. SciMLSensitivity.jl documentation: sensitivity algorithms for differential equations, including hybrid equations with events and callbacks. Consult the versioned documentation matching the installed package.

- SciML. DifferentialEquations.jl and SciMLBase ensemble-simulation documentation. Consult the versioned documentation matching the installed package.

#### Stochastic hybrid systems, multistate models, and event processes

- Bujorianu, M. L., and Lygeros, J. (2006). Toward a general theory of stochastic hybrid systems. In *Stochastic Hybrid Systems*, 3–30. Springer. https://doi.org/10.1007/978-3-540-37228-5_1

  This chapter develops a broad theoretical perspective on stochastic hybrid systems, where continuous evolution, discrete modes, and uncertainty coexist. It supplies background for distinguishing the package’s deterministic event-aware core from later uncertainty-aware extensions.

- Andersen, P. K., and Keiding, N. (2002). Multi-state models for event history analysis. *Statistical Methods in Medical Research*, 11(2), 91–115. https://doi.org/10.1191/0962280202sm276ra

  This review introduces multistate event-history models, including transition intensities and the representation of changing subject states over time. It is relevant to treatment-active, treatment-hold, hospitalized, progressed, and related clinical modes.

- Andersen, P. K., Abildstrom, S. Z., and Rosthøj, S. (2002). Competing risks as a multi-state model. *Statistical Methods in Medical Research*, 11(2), 203–215. https://doi.org/10.1191/0962280202sm281ra

  This review treats competing risks as a special case of multistate modeling and discusses cumulative-incidence and regression perspectives. It is useful when a hybrid clinical model includes mutually exclusive endpoints or competing transition types.

- Andersen, P. K., and Ravn, H. (2020). *Models for Multi-State Survival Data: Rates, Risks, and Pseudo-Values*. CRC Press.

  This textbook covers intensity-based and marginal approaches to competing risks, multistate models, and recurrent events. It is a practical reference for connecting state-dependent event rates to longitudinal clinical trajectories.

- Jia, J., and Benson, A. R. (2019). Neural jump stochastic differential equations. *Advances in Neural Information Processing Systems*, 32. https://arxiv.org/abs/1905.10403

  This paper introduces a learned framework for continuous latent dynamics with stochastic events and jump updates, coupled to temporal point-process intensities. For `hybrid-ds-julia`, it is a research-facing extension reference: known doses and protocol rules should remain explicit deterministic events, while uncertain interruptions or latent biological events may eventually motivate stochastic learned components.

### AI/ML extensions for mechanistic hybrid models

#### Mechanistic–neural models and physics-informed learning

- Brunton, S. L., and Kutz, J. N. (2019). *Data-Driven Science and Engineering: Machine Learning, Dynamical Systems, and Control*. Cambridge University Press. https://doi.org/10.1017/9781108380690

  This textbook connects machine learning, dynamical systems, scientific computing, and control. It provides broad scope for using learned representations or residual models without losing the role of mechanistic structure and decision objectives.

- Rackauckas, C., Ma, Y., Dixit, V., et al. (2020). Universal differential equations for scientific machine learning. *arXiv:2001.04385*. https://arxiv.org/abs/2001.04385

  This paper introduces universal differential equations, which combine mechanistic differential-equation structure with learned components. For this repository, the central extension principle is to learn limited unknown interactions or discrepancies while preserving interpretable dynamics, interventions, guards, and reset logic.

- Raissi, M., Perdikaris, P., and Karniadakis, G. E. (2019). Physics-informed neural networks: A deep learning framework for solving forward and inverse problems involving nonlinear partial differential equations. *Journal of Computational Physics*, 378, 686–707. https://doi.org/10.1016/j.jcp.2018.10.045

  This foundational PINN paper introduces training with both data and differential-equation residuals for forward and inverse problems. Hybrid uses require additional care because discontinuities, reset conditions, and unknown event times cannot safely be represented by a single smooth trajectory approximation.

- Poli, M., Massaroli, S., Scimeca, L., et al. (2021). Neural hybrid automata: Learning dynamics with multiple modes and stochastic transitions. *Advances in Neural Information Processing Systems*, 34. https://arxiv.org/abs/2106.04165

  This paper studies learning multi-mode continuous dynamics and stochastic transitions without assuming the modes or transition dynamics are known in advance. It is relevant to the longer-term possibility of learned latent modes, but also illustrates why known clinical protocols and scientifically defined guards should remain explicit rather than being indiscriminately inferred.

#### Reinforcement learning and decision policies

- Sutton, R. S., and Barto, A. G. (2018). *Reinforcement Learning: An Introduction* (2nd ed.). MIT Press.

  This textbook introduces the core reinforcement-learning framework, including value functions, policy learning, model-free methods, and planning concepts. It is useful background for distinguishing learned treatment policies from the mechanistic hybrid model that predicts the consequences of actions.

- Levine, S. (2018). Reinforcement learning and control as probabilistic inference: Tutorial and review. *arXiv:1805.00909*. https://arxiv.org/abs/1805.00909

  This review connects reinforcement learning, control, and probabilistic inference, with emphasis on policy optimization and model-based reasoning. It is useful for understanding algorithmic framing, but clinical policy use still requires causal assumptions, constraint handling, uncertainty assessment, and external validation.

- Chua, K., Calandra, R., McAllister, R., and Levine, S. (2018). Deep reinforcement learning in a handful of trials using probabilistic dynamics models. *Advances in Neural Information Processing Systems*, 31. https://arxiv.org/abs/1805.12114

  This paper presents PETS, a model-based RL approach that uses probabilistic dynamics ensembles and trajectory sampling for planning. It is a relevant algorithmic exemplar for a future hybrid-model-based policy layer, where the predictive model, event semantics, uncertainty, and safety constraints remain inspectable.

- Janner, M., Fu, J., Zhang, M., and Levine, S. (2019). When to trust your model: Model-based policy optimization. *Advances in Neural Information Processing Systems*, 32. https://arxiv.org/abs/1906.08253

  This paper introduces MBPO, which combines learned dynamics with short synthetic rollouts to improve sample efficiency. It is a future comparison point rather than a clinical decision template; model error and event-sequence error can be especially consequential in hybrid treatment settings.

### Pharmaceutical development and translational medicine

#### Tuberculosis and HIV

- Perelson, A. S., Neumann, A. U., Markowitz, M., Leonard, J. M., and Ho, D. D. (1996). HIV-1 dynamics in vivo: Virion clearance rate, infected cell life-span, and viral generation time. *Science*, 271(5255), 1582–1586.

  This influential within-host HIV modeling study used viral-load dynamics during treatment to estimate key kinetic quantities, including virion clearance and infected-cell lifespan. It is a foundational example of mechanistic viral-dynamics modeling linked to treatment data.

- Rong, L., and Perelson, A. S. (2009). Modeling HIV persistence, the latent reservoir, and viral blips. *Journal of Theoretical Biology*, 260(2), 308–331.

  This study models HIV persistence, latent reservoirs, and transient viral-load elevations under therapy. It provides a mechanistic example in which latent states, treatment effects, and intermittent observable events must be distinguished carefully.

- Hill, A. L., Rosenbloom, D. I. S., Fu, F., Nowak, M. A., and Siliciano, R. F. (2014). Predicting the outcomes of treatment to eradicate the latent reservoir for HIV-1. *Proceedings of the National Academy of Sciences*, 111(37), 13475–13480.

  This paper uses a stochastic model to assess how reservoir-reduction interventions could affect the chance and timing of HIV rebound. It is a useful example of connecting mechanistic uncertainty to probabilistic outcome predictions.

- World Health Organization. Consolidated guidelines on the use of antiretroviral drugs for treating and preventing HIV infection. Consult the current edition and associated viral-load-monitoring guidance.

- World Health Organization. Consolidated guidelines on tuberculosis: Module 4: Treatment. Consult the current edition and regimen-specific updates.

- Shibata, M., et al. (2024). Pharmacokinetic–pharmacodynamic modeling of tuberculosis time-to-positivity and colony-forming-unit data to compare linezolid dosing regimens. *Antimicrobial Agents and Chemotherapy*.

  This PK/PD study compares linezolid dosing regimens using tuberculosis time-to-positivity and colony-forming-unit data. It illustrates how multiple microbiological endpoints can be integrated into regimen-comparison models.

#### Oncology and adaptive cancer therapy

- Gatenby, R. A., Silva, A. S., Gillies, R. J., and Frieden, B. R. (2009). Adaptive therapy. *Cancer Research*, 69(11), 4894–4903.

  This article introduces adaptive therapy as an evolutionary treatment strategy that seeks to manage, rather than only eliminate, resistant tumor populations. It supplies the conceptual basis for threshold-based dose modulation and treatment-holiday models.

- Zhang, J., Cunningham, J. J., Brown, J. S., and Gatenby, R. A. (2017). Integrating evolutionary dynamics into treatment of metastatic castrate-resistant prostate cancer. *Nature Communications*, 8, 1816.

  This study applies evolutionary principles and patient-specific modeling to treatment scheduling in metastatic castrate-resistant prostate cancer. It is a prominent translational example of using modeled competition between sensitive and resistant cells to motivate adaptive dosing strategies.

- West, J. B., et al. (2020). A survey of open questions in adaptive therapy: Bridging mathematics and clinical translation. *eLife*, 9, e84263.

  This review surveys unresolved mathematical, biological, and translational questions in adaptive cancer therapy. It is useful for framing treatment scheduling as a hypothesis and model-validation problem rather than as a direct clinical recommendation.

- Enriquez-Navas, P. M., et al. (2016). Exploiting evolutionary principles to prolong tumor control in preclinical models of breast cancer. *Science Translational Medicine*, 8(327), 327ra24.

  This preclinical study tests evolution-informed treatment scheduling in breast-cancer models and reports prolonged tumor control relative to conventional approaches in the studied setting. It provides experimental context for mathematical work on adaptive therapy while not establishing a general clinical rule.

- Anderson, A. R. A., Quaranta, V., and collaborators. Mathematical oncology reviews and primary studies on tumor ecology, resistance, and treatment scheduling. Consult indication-specific literature.

#### Immunology, inflammation, and autoimmune disease

- Eftimie, R., Bramson, J. L., and Earn, D. J. D. (2011). Interactions between the immune system and cancer: A brief review of non-spatial mathematical models. *Bulletin of Mathematical Biology*, 73, 2–32.

  This review maps non-spatial mathematical models of tumor–immune interactions, including common state variables, mechanisms, and modeling objectives. It is useful for locating reduced-order immuno-oncology test beds and understanding the assumptions behind them.

- Iwami, S., Takeuchi, Y., and others. Mathematical models of autoimmune-disease dynamics, tolerance, flare-up, and dormancy. Consult disease-specific primary literature.

- Kuhlmann, T., et al. (2024). Mathematical modeling in autoimmune diseases: A review of onset, progression, and treatment-effect models. *Frontiers in Immunology*.

  This review surveys mathematical models of autoimmune-disease onset, progression, and treatment effects. Its scope helps readers identify where mechanistic state variables and discrete flare, treatment, or monitoring events may be scientifically meaningful.

- Germain, R. N. (2012). Maintaining system homeostasis: The third law of Newtonian immunology. *Nature Immunology*, 13, 902–906.

  This perspective discusses immune homeostasis as a systems-level balance maintained through interacting regulatory processes. It provides conceptual context for mechanistic models of inflammatory feedback, tolerance, recovery, and perturbation responses.

- Consult disease-specific guidance, mechanistic studies, and pharmacometric literature for the intended autoimmune or inflammatory indication.

#### PK/PD and quantitative systems pharmacology

- Mager, D. E., and Jusko, W. J. (2001). General pharmacokinetic model for drugs exhibiting target-mediated drug disposition. *Journal of Pharmacokinetics and Pharmacodynamics*, 28, 507–532.

  This paper develops a general PK model for target-mediated drug disposition, in which binding, target turnover, and drug–target interactions can create nonlinear exposure behavior. It is a useful mechanistic template for PK models whose dynamics change with target abundance and treatment state.

- Danhof, M., de Jongh, J., De Lange, E. C. M., Della Pasqua, O., Ploeger, B. A., and Voskuyl, R. A. (2007). Mechanism-based pharmacokinetic-pharmacodynamic modeling: Biophase distribution, receptor theory, and dynamical systems analysis. *Annual Review of Pharmacology and Toxicology*, 47, 357–400.

  This review covers mechanism-based PK/PD modeling from biophase distribution and receptor theory through dynamical-systems analysis. It is a broad foundation for representing drug exposure and biological response before introducing explicit dosing, holds, switches, and other hybrid event logic.

- Marshall, S. F., Burghaus, R., Cosson, V. F., et al. (2016). Good practices in model-informed drug discovery and development: Practice, application, and documentation. *CPT: Pharmacometrics & Systems Pharmacology*, 5, 93–122.

  This review discusses good practice for model-informed drug discovery and development, including model purpose, documentation, evaluation, and communication. It is relevant to the repository’s emphasis on transparent assumptions, validation, and defined contexts of use.

- Sorger, P. K., et al. (2011). Quantitative and systems pharmacology in the post-genomic era: New approaches to discovering drugs and understanding therapeutic mechanisms. *NIH White Paper*.

  This white paper outlines the scope of quantitative and systems pharmacology, including multiscale mechanistic modeling, data integration, and drug-development applications.

#### Hybrid and stochastic-hybrid drug-effect modeling

- Li, X., Qian, L., and Dougherty, E. R. (2012). *Dynamical modeling of drug effect using hybrid systems.* *EURASIP Journal on Bioinformatics and Systems Biology*, 2012, Article 19. https://doi.org/10.1186/1687-4153-2012-19

  A directly relevant early application of hybrid-systems theory to drug-effect modeling. The paper couples periodic dosing, pharmacokinetic concentration profiles, and thresholded pharmacodynamic effects with gene-regulatory-network dynamics. Its hybrid domains encode clinically recognizable concentration regimes—ineffective exposure, concentration-dependent effect, and saturation—and demonstrate that dose amount and dosing interval can produce different outcomes even under comparable total drug intake. For `hybrid-ds-julia`, this paper is a conceptual and mathematical precedent rather than an implementation template: the package generalizes the same continuous-plus-discrete modeling principle to explicit treatment modes, guards, reset maps, scheduled interventions, state-triggered clinical decisions, and event-aware computational workflows.

- Oduola, W. O., and Li, X. (2018). *Multiscale tumor modeling with drug pharmacokinetic and pharmacodynamic profile using stochastic hybrid system.* *Cancer Informatics*, 17, 1176935118790262. https://doi.org/10.1177/1176935118790262

  A directly relevant multiscale precedent for the stochastic-hybrid extension of `hybrid-ds-julia`. The paper integrates drug PK/PD profiles with molecular, cellular, and multicellular tumor dynamics using a stochastic hybrid-system framework. Differential equations represent gene-regulatory pathways, cellular automata represent tumor behavior across cellular scales, and Markov chains represent stochastic cell behaviors conditional on gene expression, cell-cycle state, and microenvironment. Its relevance is conceptual rather than a first-implementation template: `hybrid-ds-julia` is initially focused on transparent event-aware ODE models, but this work demonstrates a longer-term path toward linking mechanistic PK/PD dynamics, discrete biological transitions, and stochastic multiscale tumor evolution when the intended question and data support that added complexity.

- Baran, S. W., and Gaburro, S. (2026). *Hybrid mechanistic–machine learning PK/PD models with digital biomarkers: from cage to clinic.* *Frontiers in Pharmacology*, 17, 1815118. https://doi.org/10.3389/fphar.2026.1815118

  A directly relevant review for the AI/ML extension of `hybrid-ds-julia`. It considers how mechanistic PK/PD models can be combined with machine-learning components and digital biomarkers from continuous monitoring, imaging, omics, home-cage systems, telemetry, wearables, and remote patient monitoring. The review is especially relevant to hybrid models because such data may support observation models, latent-state estimation, individual parameter calibration, covariate discovery, cross-species translation, event detection, and assessment of dosing or monitoring policies. It also emphasizes that additional ML complexity is not automatically beneficial: missingness, device drift, data leakage, poor generalizability, weak identifiability, and misalignment between sensor streams, dosing history, clinical decisions, and physiological state require explicit mitigation. The paper supports a disciplined approach in which ML augments a structurally sound mechanistic model, is evaluated against a relevant baseline, and is documented for a defined context of use.

- U.S. Food and Drug Administration. Model-informed drug development and population pharmacokinetic guidance and related regulatory materials. Consult current guidance.
