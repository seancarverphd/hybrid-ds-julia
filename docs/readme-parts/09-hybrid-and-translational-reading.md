## Further reading

This section is organized to mirror the mathematical, computational, application, and limitation sections of this README. It is intentionally a curated starting point rather than a comprehensive bibliography. Readers should consult original papers, authoritative guidelines, maintained software documentation, and domain experts before relying on a model for scientific, engineering, clinical, or operational decisions.

### Hybrid-systems foundations, events, and sensitivity analysis

#### Hybrid transitions, saltation matrices, and event-aware derivatives

- Goebel, R., Sanfelice, R. G., and Teel, A. R. (2012). *Hybrid Dynamical Systems: Modeling, Stability, and Robustness*. Princeton University Press.

- di Bernardo, M., Budd, C. J., Champneys, A. R., and Kowalczyk, P. (2008). *Piecewise-Smooth Dynamical Systems: Theory and Applications*. Springer.

- Kong, N. J., Payne, J. J., Zhu, J., and Johnson, A. M. (2024). Saltation matrices: The essential tool for linearizing hybrid dynamical systems. *Proceedings of the IEEE*, 112(2), 161–196.

- Saccon, A., van de Wouw, N., and Nijmeijer, H. (2014). Sensitivity analysis of hybrid systems with state jumps with application to trajectory tracking. *Proceedings of the IEEE Conference on Decision and Control*.

- Galvanetto, U., and Magri, L. (2020). Modeling and sensitivity analysis methodology for hybrid dynamical systems. *Journal of Computational and Nonlinear Dynamics*, 15(2).

#### Multiple shooting, optimization, and parallel simulation

- Bock, H. G., and Plitt, K. J. (1984). A multiple shooting algorithm for direct solution of optimal control problems. *Proceedings of the IFAC World Congress*.

- Diehl, M., Bock, H. G., Diedam, H., and Wieber, P.-B. (2006). Fast direct multiple shooting algorithms for optimal robot control. In *Fast Motions in Biomechanics and Robotics*.

- Betts, J. T. (2010). *Practical Methods for Optimal Control and Estimation Using Nonlinear Programming* (2nd ed.). SIAM.

- Rackauckas, C., and Nie, Q. (2017). DifferentialEquations.jl—A performant and feature-rich ecosystem for solving differential equations in Julia. *Journal of Open Research Software*, 5(1), 15.

- Rackauckas, C., Ma, Y., Dixit, V., et al. (2020). Universal differential equations for scientific machine learning. *arXiv:2001.04385*.

- SciML. SciMLSensitivity.jl documentation: sensitivity algorithms for differential equations, including hybrid equations with events and callbacks. Consult the versioned documentation matching the installed package.

- SciML. DifferentialEquations.jl and SciMLBase ensemble-simulation documentation. Consult the versioned documentation matching the installed package.

### Pharmaceutical development and translational medicine

#### Tuberculosis and HIV

- Perelson, A. S., Neumann, A. U., Markowitz, M., Leonard, J. M., and Ho, D. D. (1996). HIV-1 dynamics in vivo: Virion clearance rate, infected cell life-span, and viral generation time. *Science*, 271(5255), 1582–1586.

- Rong, L., and Perelson, A. S. (2009). Modeling HIV persistence, the latent reservoir, and viral blips. *Journal of Theoretical Biology*, 260(2), 308–331.

- Hill, A. L., Rosenbloom, D. I. S., Fu, F., Nowak, M. A., and Siliciano, R. F. (2014). Predicting the outcomes of treatment to eradicate the latent reservoir for HIV-1. *Proceedings of the National Academy of Sciences*, 111(37), 13475–13480.

- World Health Organization. Consolidated guidelines on the use of antiretroviral drugs for treating and preventing HIV infection. Consult the current edition and associated viral-load-monitoring guidance.

- World Health Organization. Consolidated guidelines on tuberculosis: Module 4: Treatment. Consult the current edition and regimen-specific updates.

- Shibata, M., et al. (2024). Pharmacokinetic–pharmacodynamic modeling of tuberculosis time-to-positivity and colony-forming-unit data to compare linezolid dosing regimens. *Antimicrobial Agents and Chemotherapy*.

#### Oncology and adaptive cancer therapy

- Gatenby, R. A., Silva, A. S., Gillies, R. J., and Frieden, B. R. (2009). Adaptive therapy. *Cancer Research*, 69(11), 4894–4903.

- Zhang, J., Cunningham, J. J., Brown, J. S., and Gatenby, R. A. (2017). Integrating evolutionary dynamics into treatment of metastatic castrate-resistant prostate cancer. *Nature Communications*, 8, 1816.

- West, J. B., et al. (2020). A survey of open questions in adaptive therapy: Bridging mathematics and clinical translation. *eLife*, 9, e84263.

- Enriquez-Navas, P. M., et al. (2016). Exploiting evolutionary principles to prolong tumor control in preclinical models of breast cancer. *Science Translational Medicine*, 8(327), 327ra24.

- Anderson, A. R. A., Quaranta, V., and collaborators. Mathematical oncology reviews and primary studies on tumor ecology, resistance, and treatment scheduling. Consult indication-specific literature.

#### Immunology, inflammation, and autoimmune disease

- Eftimie, R., Bramson, J. L., and Earn, D. J. D. (2011). Interactions between the immune system and cancer: A brief review of non-spatial mathematical models. *Bulletin of Mathematical Biology*, 73, 2–32.

- Iwami, S., Takeuchi, Y., and others. Mathematical models of autoimmune-disease dynamics, tolerance, flare-up, and dormancy. Consult disease-specific primary literature.

- Kuhlmann, T., et al. (2024). Mathematical modeling in autoimmune diseases: A review of onset, progression, and treatment-effect models. *Frontiers in Immunology*.

- Germain, R. N. (2012). Maintaining system homeostasis: The third law of Newtonian immunology. *Nature Immunology*, 13, 902–906.

- Consult disease-specific guidance, mechanistic studies, and pharmacometric literature for the intended autoimmune or inflammatory indication.

#### PK/PD and quantitative systems pharmacology

- Mager, D. E., and Jusko, W. J. (2001). General pharmacokinetic model for drugs exhibiting target-mediated drug disposition. *Journal of Pharmacokinetics and Pharmacodynamics*, 28, 507–532.

- Danhof, M., de Jongh, J., De Lange, E. C. M., Della Pasqua, O., Ploeger, B. A., and Voskuyl, R. A. (2007). Mechanism-based pharmacokinetic-pharmacodynamic modeling: Biophase distribution, receptor theory, and dynamical systems analysis. *Annual Review of Pharmacology and Toxicology*, 47, 357–400.

- Marshall, S. F., Burghaus, R., Cosson, V. F., et al. (2016). Good practices in model-informed drug discovery and development: Practice, application, and documentation. *CPT: Pharmacometrics & Systems Pharmacology*, 5, 93–122.

- Sorger, P. K., et al. (2011). Quantitative and systems pharmacology in the post-genomic era: New approaches to discovering drugs and understanding therapeutic mechanisms. *NIH White Paper*.

#### Hybrid and stochastic-hybrid drug-effect modeling

- Li, X., Qian, L., and Dougherty, E. R. (2012). *Dynamical modeling of drug effect using hybrid systems.* *EURASIP Journal on Bioinformatics and Systems Biology*, 2012, Article 19. https://doi.org/10.1186/1687-4153-2012-19

  A directly relevant early application of hybrid-systems theory to drug-effect modeling. The paper couples periodic dosing, pharmacokinetic concentration profiles, and thresholded pharmacodynamic effects with gene-regulatory-network dynamics. Its hybrid domains encode clinically recognizable concentration regimes—ineffective exposure, concentration-dependent effect, and saturation—and demonstrate that dose amount and dosing interval can produce different outcomes even under comparable total drug intake. For `hybrid-ds-julia`, this paper is a conceptual and mathematical precedent rather than an implementation template: the package generalizes the same continuous-plus-discrete modeling principle to explicit treatment modes, guards, reset maps, scheduled interventions, state-triggered clinical decisions, and event-aware computational workflows.

- Oduola, W. O., and Li, X. (2018). *Multiscale tumor modeling with drug pharmacokinetic and pharmacodynamic profile using stochastic hybrid system.* *Cancer Informatics*, 17, 1176935118790262. https://doi.org/10.1177/1176935118790262

  A directly relevant multiscale precedent for the stochastic-hybrid extension of `hybrid-ds-julia`. The paper integrates drug PK/PD profiles with molecular, cellular, and multicellular tumor dynamics using a stochastic hybrid-system framework. Differential equations represent gene-regulatory pathways, cellular automata represent tumor behavior across cellular scales, and Markov chains represent stochastic cell behaviors conditional on gene expression, cell-cycle state, and microenvironment. Its relevance is conceptual rather than a first-implementation template: `hybrid-ds-julia` is initially focused on transparent event-aware ODE models, but this work demonstrates a longer-term path toward linking mechanistic PK/PD dynamics, discrete biological transitions, and stochastic multiscale tumor evolution when the intended question and data support that added complexity.

- Baran, S. W., and Gaburro, S. (2026). *Hybrid mechanistic–machine learning PK/PD models with digital biomarkers: from cage to clinic.* *Frontiers in Pharmacology*, 17, 1815118. https://doi.org/10.3389/fphar.2026.1815118

  A directly relevant review for the AI/ML extension of `hybrid-ds-julia`. It considers how mechanistic PK/PD models can be combined with machine-learning components and digital biomarkers from continuous monitoring, imaging, omics, home-cage systems, telemetry, wearables, and remote patient monitoring. The review is especially relevant to hybrid models because such data may support observation models, latent-state estimation, individual parameter calibration, covariate discovery, cross-species translation, event detection, and assessment of dosing or monitoring policies. It also emphasizes that additional ML complexity is not automatically beneficial: missingness, device drift, data leakage, poor generalizability, weak identifiability, and misalignment between sensor streams, dosing history, clinical decisions, and physiological state require explicit mitigation. The paper supports a disciplined approach in which ML augments a structurally sound mechanistic model, is evaluated against a relevant baseline, and is documented for a defined context of use.

- U.S. Food and Drug Administration. Model-informed drug development and population pharmacokinetic guidance and related regulatory materials. Consult current guidance.
