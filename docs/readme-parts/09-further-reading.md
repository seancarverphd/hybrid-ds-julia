## `docs/readme-parts/09-further-reading.md`

```md
## Further reading

This list is intended as a starting point rather than a comprehensive bibliography. It includes foundational hybrid-systems references, QSP and PK/PD context, sensitivity and automatic-differentiation methods, AI-enabled mechanistic modeling, and application areas relevant to the package.

### Related hybrid-systems papers in other domains

- Carver, S., Guckenheimer, J., & Cowan, N. J. (2009). *Lateral stability of the spring-loaded inverted pendulum model of running and the influence of step-to-step transition dynamics*. Chaos. A preprint is available through [the LIMBS website](https://limbs.lcsr.jhu.edu/wp-content/papercite-data/pdf/carverlateral2009.pdf). This paper is relevant because it uses hybrid-system computations in which accurate event handling, boundary-value methods, and structured sensitivity propagation are essential.
- di Bernardo, M., Budd, C. J., Champneys, A. R., & Kowalczyk, P. (2008). *Piecewise-smooth Dynamical Systems: Theory and Applications*. Springer. A broad introduction to discontinuity-induced bifurcations, switching systems, and piecewise-smooth dynamics.
- Goebel, R., Sanfelice, R. G., & Teel, A. R. (2012). *Hybrid Dynamical Systems: Modeling, Stability, and Robustness*. Princeton University Press. A foundational treatment of hybrid-system modeling and analysis.
- van der Schaft, A. J., & Schumacher, H. (2000). *An Introduction to Hybrid Dynamical Systems*. Springer. A useful reference for systems that combine continuous dynamics and discrete transitions.

### Core dynamical systems / hybrid methods

- Guckenheimer, J., & Holmes, P. (1983). *Nonlinear Oscillations, Dynamical Systems, and Bifurcations of Vector Fields*. Springer. Foundational material on dynamical systems, periodic orbits, bifurcations, and stability.
- Kuznetsov, Y. A. (2004). *Elements of Applied Bifurcation Theory* (3rd ed.). Springer. A standard reference for local bifurcations and continuation-oriented analysis.
- Leine, R. I., & Nijmeijer, H. (2013). *Dynamics and Bifurcations of Non-Smooth Mechanical Systems*. Springer. Relevant to piecewise-smooth systems, impacts, switching, and discontinuity-induced bifurcations.
- Nordmark, A. B. (1991). Non-periodic motion caused by grazing incidence in an impact oscillator. *Journal of Sound and Vibration*, 145(2), 279–297. A classic treatment of grazing events and their dynamical consequences.
- Filippov, A. F. (1988). *Differential Equations with Discontinuous Righthand Sides*. Springer. A foundational source for differential equations with discontinuous vector fields and sliding dynamics.

### QSP / PK–PD concepts and practice

- van der Graaf, P. H., & Benson, N. (2011). Systems pharmacology: Bridging systems biology and pharmacokinetics-pharmacodynamics (PKPD) in drug discovery and development. *Pharmaceutical Research*, 28, 1460–1464. A concise early statement of the systems-pharmacology perspective.
- Peterson, M. C., & Riggs, M. M. (2015). A physiologically based pharmacokinetic model of a monoclonal antibody against interleukin 6 in mice: A platform for translational model-based drug development. *Drug Metabolism and Disposition*, 43(8), 1143–1154. An example of mechanistic modeling in translational pharmacology.
- Agoram, B. M., Martin, S. W., & van der Graaf, P. H. (2007). The role of mechanism-based pharmacokinetic-pharmacodynamic models in translational research. *CPT: Pharmacometrics & Systems Pharmacology* and related systems-pharmacology literature. Useful background on mechanism-based translational modeling.
- Sorger, P. K., Allerheiligen, S. R. B., Abernethy, D. R., Altman, R. B., Brouwer, K. L. R., Califano, A., D’Argenio, D. Z., Iyengar, R., Jusko, W. J., Lalonde, R., et al. (2011). *Quantitative and Systems Pharmacology in the Post-genomic Era: New Approaches to Discovering Drugs and Understanding Therapeutic Mechanisms*. NIH White Paper. A major framing document for QSP.
- van der Graaf, P. H., Benson, N., & related authors. QSP and model-informed drug development literature. QSP provides a framework for mechanistic models that combine drug exposure, biological pathways, disease state, and quantitative data to support in silico experiments and translational decisions. [QSP overview](https://www.mathworks.com/discovery/quantitative-systems-pharmacology.html)

### Sensitivity, adjoint, and automatic differentiation

- Rackauckas, C., Ma, Y., Dixit, V., Guo, X., Innes, M., Revels, J., Nyberg, J., & Ivaturi, V. (2020). Universal differential equations for scientific machine learning. *arXiv:2001.04385*. Relevant to combining mechanistic differential equations, machine learning, and differentiable simulation.
- Rackauckas, C., & Nie, Q. (2017). DifferentialEquations.jl – A performant and feature-rich ecosystem for solving differential equations in Julia. *Journal of Open Research Software*, 5(1), 15. Background on the Julia differential-equation ecosystem on which `hybrid-ds-julia` is intended to build.
- Rackauckas, C., et al. (2019). DiffEqFlux.jl — A Julia library for neural differential equations. *arXiv:1902.02376*. Relevant to differentiable simulation and scientific machine learning in Julia.
- Cao, Y., Li, S., Petzold, L., & Serban, R. (2003). Adjoint sensitivity analysis for differential-algebraic equations: The adjoint DAE system and its numerical solution. *SIAM Journal on Scientific Computing*, 24(3), 1076–1089. Relevant background for gradient-based estimation and optimization.
- Walther, A., & Griewank, A. (2012). *Getting Started with ADOL-C*. In *Combinatorial Scientific Computing*. Chapman and Hall/CRC. A useful introduction to automatic differentiation concepts and implementation.

### Mechanistic stochastic and Bayesian methods

- Wilkinson, D. J. (2011). *Stochastic Modelling for Systems Biology* (2nd ed.). Chapman and Hall/CRC. A broad introduction to stochastic models for biological systems.
- Gillespie, D. T. (1977). Exact stochastic simulation of coupled chemical reactions. *The Journal of Physical Chemistry*, 81(25), 2340–2361. The classic stochastic simulation algorithm for reaction systems.
- Allen, L. J. S. (2017). *A Primer on Stochastic Epidemics*. Springer. A useful introduction to stochastic epidemic modeling and uncertainty in compartmental systems.
- Gelman, A., Carlin, J. B., Stern, H. S., Dunson, D. B., Vehtari, A., & Rubin, D. B. (2013). *Bayesian Data Analysis* (3rd ed.). CRC Press. General Bayesian methodology relevant to parameter inference and uncertainty quantification.
- Carpenter, B., Gelman, A., Hoffman, M. D., Lee, D., Goodrich, B., Betancourt, M., Brubaker, M., Guo, J., Li, P., & Riddell, A. (2017). Stan: A probabilistic programming language. *Journal of Statistical Software*, 76(1), 1–32. Relevant to Bayesian inference workflows and gradient-based posterior computation.

### Mechanistic--neural hybrid systems

- Mann, J., et al. (2024). Mechanism-based organization of neural networks to emulate biological and pharmacological processes. This work is relevant because it reorganizes neural-network layers to reflect biological and pharmacological process structure rather than treating the model as an unconstrained black box. [Article](https://pmc.ncbi.nlm.nih.gov/articles/PMC11130269/)
- Moutik, M., et al. Review of hybrid quantitative systems pharmacology and machine-learning approaches. See also [AI/ML mathematical extensions](#aiml-mathematical-extensions), especially [Mechanistic--neural hybrid systems](#mechanistic--neural-hybrid-systems). This literature is relevant to combining structured mechanistic models with learned components while preserving interpretation of pharmacological and biological state variables.
- Fochesato, A., et al. (2025). Building hybrid pharmacometric–machine-learning models in practice. This tutorial reviews hybrid pharmacometric and machine-learning model considerations, including reporting and validation issues. [Article](https://pmc.ncbi.nlm.nih.gov/articles/PMC12823305/)
- Coupling quantitative systems pharmacology modelling to machine learning. *Frontiers in Systems Biology* (2024). Discusses how QSP and ML can be combined, including biology-informed neural-network approaches. [Article](https://www.frontiersin.org/journals/systems-biology/articles/10.3389/fsysb.2024.1380685/full)
- Pinto, A., Ramos, et al. A general hybrid modeling framework for systems biology. Relevant to combining mechanistic models and deep neural networks while retaining structured biological representations.

Further work enabled by `hybrid-ds-julia` would be to combine these mechanistic–neural architectures with explicit event surfaces, dose maps, toxicity holds, and therapy-switch transitions. This would allow learned model-discrepancy terms to improve prediction while preserving known treatment and biological logic.

### Physics-informed neural networks

- Raissi, M., Perdikaris, P., & Karniadakis, G. E. (2019). Physics-informed neural networks: A deep learning framework for solving forward and inverse problems involving nonlinear partial differential equations. *Journal of Computational Physics*, 378, 686–707. The foundational PINN reference.
- Karniadakis, G. E., Kevrekidis, I. G., Lu, L., Perdikaris, P., Wang, S., & Yang, L. (2021). Physics-informed machine learning. *Nature Reviews Physics*, 3, 422–440. A broad review of physics-informed machine learning.
- Erdem, D., et al. (2024). Learning chemotherapy drug action via universal physics-informed neural networks. This work applies a physics-informed approach to QSP models to identify hidden drug-action terms from synthetic and in-vitro data. [Preprint](https://arxiv.org/html/2404.08019v1)
- A current landscape of integrating QSP and machine learning. *CPT: Pharmacometrics & Systems Pharmacology* (2022). Discusses PINNs and biologically informed neural networks as methods for combining mechanistic ODE structure with data-driven learning in QSP. [Article](https://pmc.ncbi.nlm.nih.gov/articles/PMC8837505/)
- Rackauckas, C., et al. (2020). Universal differential equations for scientific machine learning. *arXiv:2001.04385*. Relevant to using neural components inside structured differential-equation models.

For `hybrid-ds-julia`, the important extension would be hybrid PINNs that enforce not only continuous ODE residuals but also scheduled-dose jump maps, state-triggered guard conditions, reset maps, and continuity or discontinuity constraints at event times. Such tools could support latent-state reconstruction and parameter estimation from sparse, irregular, event-rich longitudinal data.

### Neural hybrid automata

- Goebel, R., Sanfelice, R. G., & Teel, A. R. (2012). *Hybrid Dynamical Systems: Modeling, Stability, and Robustness*. Princeton University Press. A foundation for explicit representations of modes, guards, and reset maps.
- van der Schaft, A. J., & Schumacher, H. (2000). *An Introduction to Hybrid Dynamical Systems*. Springer. A foundational treatment of hybrid automata and continuous-discrete system structure.
- Pinto, A., Ramos, et al. A general hybrid modeling framework for systems biology. Relevant to machine-learning components combined with structured biological dynamics and interoperable systems-biology representations.
- Moutik, M., et al. Review of QSP and machine-learning integration. See also [AI/ML mathematical extensions](#aiml-mathematical-extensions). This literature is relevant to identifying where learned components can complement, rather than replace, explicit mechanistic structure.
- di Bernardo, M., Budd, C. J., Champneys, A. R., & Kowalczyk, P. (2008). *Piecewise-smooth Dynamical Systems: Theory and Applications*. Springer. Relevant to switching boundaries, mode transitions, and regime-dependent dynamics.

A neural-hybrid-automaton direction for `hybrid-ds-julia` would retain known clinical modes—such as active treatment, reduced dose, hold, recovery, and rescue therapy—while using data-driven components only where latent mode structure, mode-dependent dynamics, or transition conditions are genuinely uncertain.

### Neural jump SDEs

- Jia, J., & Benson, A. R. (2019). Neural jump stochastic differential equations. *Advances in Neural Information Processing Systems*. [Paper](https://proceedings.neurips.cc/paper_files/paper/9177-neural-jump-stochastic-differential-equations.pdf)
- Jia, J., & Benson, A. R. (2019). Neural jump stochastic differential equations. [arXiv:1905.10403](https://arxiv.org/abs/1905.10403). The paper introduces a data-driven framework that learns continuous latent dynamics together with discrete stochastic events.
- Baili, et al. Neural jump SDE-related work. See also [AI/ML mathematical extensions](#ai/ml-mathematical-extensions), especially [Neural jump SDEs](#neural-jump-sdes). This reference should be used alongside the final verified bibliographic citation for the Baili paper before release.
- Krystul, J. (2006). Stochastic differential equations on hybrid state spaces. Relevant background for jump diffusion and hybrid stochastic-system formulations.
- Wilkinson, D. J. (2011). *Stochastic Modelling for Systems Biology* (2nd ed.). Chapman and Hall/CRC. Background for stochastic biological dynamics and simulation.

Within `hybrid-ds-julia`, a neural-jump-SDE extension would distinguish known scheduled clinical interventions from uncertain or latent stochastic events. It could support uncertainty-aware virtual-patient simulations, models of treatment interruptions or adherence variation, and estimation of stochastic biological perturbations without obscuring the explicit treatment policy.

### Epidemiology, adaptive intervention, and public-health policy

- Hethcote, H. W. (2000). The mathematics of infectious diseases. *SIAM Review*, 42(4), 599–653. A classic review of compartmental epidemic models and their mathematical analysis.
- Brauer, F., Castillo-Chavez, C., & Feng, Z. (2019). *Mathematical Models in Epidemiology*. Springer. A broad reference for deterministic and stochastic epidemic modeling.
- Funk, S., Salathé, M., & Jansen, V. A. A. (2010). Modelling the influence of human behaviour on the spread of infectious diseases: A review. *Journal of the Royal Society Interface*, 7(50), 1247–1256. Relevant to feedback between epidemic state, behavior, and intervention responses.
- Ferguson, N. M., et al. (2020). Impact of non-pharmaceutical interventions (NPIs) to reduce COVID-19 mortality and healthcare demand. Imperial College COVID-19 Response Team Report 9. An example of intervention timing and policy structure affecting epidemic outcomes.
- Kissler, S. M., Tedijanto, C., Goldstein, E., Grad, Y. H., & Lipsitch, M. (2020). Projecting the transmission dynamics of SARS-CoV-2 through the postpandemic period. *Science*, 368(6493), 860–868. Relevant to intervention cycles, seasonality, and long-term epidemic-policy dynamics.

These references motivate work in which `hybrid-ds-julia` represents threshold-triggered interventions, vaccination pulses, testing and treatment rules, capacity constraints, and hysteretic reopening policies directly inside epidemiological models. Event-aware sensitivities could help identify policy thresholds at which small changes in timing, reporting delay, or intervention strength produce qualitatively different epidemic trajectories.

### Mechanistic crop models and trait optimization

- Thornley, J. H. M., & France, J. (2007). *Mathematical Models in Agriculture: Quantitative Methods for the Plant, Animal and Ecological Sciences* (2nd ed.). CABI. A broad resource for mechanistic agricultural models.
- Yin, X., & Struik, P. C. (2010). Modelling the crop: From system dynamics to systems biology. *Journal of Experimental Botany*, 61(8), 2171–2183. Relevant to linking crop physiological models with systems-level analysis.
- Hammer, G. L., Messina, C., van Oosterom, E., & Chapman, S. (2019). Crop design for adaptation to the drought and high-temperature risks anticipated in future climates. *Crop Science*, 59(5), 2093–2110. Relevant to trait-by-environment interactions and crop-design questions.
- APSIM Initiative. APSIM: Agricultural Production Systems sIMulator. A widely used platform for crop, soil, and management simulation.
- Jones, J. W., et al. (2003). The DSSAT cropping system model. *European Journal of Agronomy*, 18(3–4), 235–265. A foundational reference for crop-system simulation.

These references provide context for using hybrid event-aware methods in crop growth, irrigation, fertilization, canopy competition, and trait-optimization problems where the timing of discrete management actions can be as important as the continuous biological dynamics.
```