### Specific labs and authors

This section identifies research programs and software ecosystems that are especially relevant to sensorimotor control, active sensing, whole-brain dynamics, system identification, hybrid mechanics, and event-driven neural simulation. These readings are intended as entry points to primary literature, maintained software documentation, public datasets, and domain expertise.

#### Jeka and Kiemel: postural control, multisensory integration, and locomotion

- Jeka, J. J., Kiemel, T., Creath, R., Horak, F., and Peterka, R. J. (2004). Controlling human upright posture: Velocity information is more accurate than position or acceleration. *Journal of Neurophysiology*, 92(4), 2368–2379. https://doi.org/10.1152/jn.00935.2003

  This study examines the sensory information used to control upright human posture, with emphasis on velocity-related information. It is relevant to reduced-order postural-control models that combine continuous body dynamics with sensory feedback and corrective actions.

- Kiemel, T., Oie, K. S., and Jeka, J. J. (2002). Multisensory fusion and the stochastic structure of postural sway. *Biological Cybernetics*, 87, 262–277. https://doi.org/10.1007/s00422-002-0333-2

  This paper studies multisensory integration and stochastic structure in postural sway. It provides an example of how sensory uncertainty and feedback can shape observable movement variability.

- Creath, R., Kiemel, T., Horak, F., and Jeka, J. J. (2008). The role of vestibular and somatosensory systems in intersegmental dynamics during stance. *Experimental Brain Research*, 183, 509–517. https://doi.org/10.1007/s00221-007-1168-3

  This study investigates vestibular and somatosensory contributions to coordination across body segments during stance. It is useful for identifying candidate state variables, sensory inputs, and coupling mechanisms in postural models.

- Hsu, W.-L., Scholz, J. P., Schöner, G., Jeka, J. J., and Kiemel, T. (2007). Control and estimation of posture during quiet stance depends on multijoint coordination. *Journal of Neurophysiology*, 97(4), 3024–3035. https://doi.org/10.1152/jn.01142.2006

  This paper examines posture control and state estimation in the presence of multijoint coordination. It provides relevant context for observation models and reduced-order descriptions of sensorimotor state.

- Kiemel, T., Elahi, A. J., and Jeka, J. J. (2008). Identification of the plant for upright stance in humans: Multiple movement patterns from a single neural strategy. *Journal of Neurophysiology*, 100, 3394–3406. https://doi.org/10.1152/jn.90673.2008

  This paper uses system-identification approaches to characterize the mechanical plant of human upright stance. It is a useful example of separating physical dynamics from neural control hypotheses.

- Logan, D., Kiemel, T., and Jeka, J. J. (2016). Using a system identification approach to investigate subtask control during human locomotion. *Frontiers in Computational Neuroscience*, 10, 146. https://doi.org/10.3389/fncom.2016.00146

  This study applies system identification to investigate subtask control during human locomotion. It is relevant to decomposing complex behavior into experimentally grounded continuous processes and event- or phase-related control components.

#### Ahrens Lab: zebrafish sensorimotor behavior and whole-brain dynamics

- Ahrens, M. B., Li, J. M., Orger, M. B., Robson, D. N., Schier, A. F., Engert, F., and Portugues, R. (2012). Brain-wide neuronal dynamics during motor adaptation in zebrafish. *Nature*, 485, 471–477. https://doi.org/10.1038/nature11057

  This study links whole-brain neural activity to motor adaptation in larval zebrafish. It provides a rich example of connecting high-dimensional observations to behavioral state transitions and adaptation dynamics.

- Chen, X., Mu, Y., Hu, Y., Kuan, A. T., Nikitchenko, M., Randlett, O., Chen, A. B., Gavornik, J. P., Sompolinsky, H., Engert, F., and Ahrens, M. B. (2018). Brain-wide organization of neuronal activity and convergent sensorimotor transformations in larval zebrafish. *Neuron*, 100, 876–890.e5. https://doi.org/10.1016/j.neuron.2018.09.042

  This paper examines brain-wide organization and sensorimotor transformations in larval zebrafish. It is useful background for linking latent neural states, sensory signals, and behavioral outputs without assuming that a low-dimensional mechanistic model is uniquely identifiable.

- Mu, Y., Bennett, D. V., Rubinov, M., Narayan, S., Yang, C.-T., Tanimoto, M., Mensh, B. D., Looger, L. L., and Ahrens, M. B. (2019). Glia accumulate evidence that actions are futile and suppress unsuccessful behavior. *Cell*, 178, 27–43.e19. https://doi.org/10.1016/j.cell.2019.05.050

  This study links glial activity, evidence accumulation, and behavioral suppression in zebrafish. It is relevant to models in which latent evidence or internal state influences discrete behavioral policy changes.

- Yang, E., Zwart, M. F., James, B., Rubinov, M., Wei, Z., Narayan, S., Vladimirov, N., Mensh, B. D., Fitzgerald, J. E., and Ahrens, M. B. (2022). A brainstem integrator for self-location memory and positional homeostasis in zebrafish. *Cell*, 185, 5011–5027.e20. https://doi.org/10.1016/j.cell.2022.11.014

  This paper identifies a brainstem integrator associated with self-location memory and positional homeostasis. It is a useful example of a candidate mechanistic state variable connecting neural dynamics to behavioral regulation.

- Ahrens Lab, HHMI Janelia Research Campus. Laboratory website, publications, and public datasets. Consult current laboratory materials.

#### Cowan and the LIMBS Laboratory: mechanics, active sensing, and system identification

- Cowan, N. J., and Fortune, E. S. (2007). The critical role of locomotion mechanics in decoding sensory systems. *Journal of Neuroscience*, 27(5), 1123–1128. https://doi.org/10.1523/JNEUROSCI.4195-06.2007

  This perspective argues that locomotor mechanics can be essential for interpreting sensory-system function. It provides conceptual support for modeling sensing, action, mechanics, and feedback as a coupled dynamical system rather than as isolated modules.

- Sefati, S., Neveln, I. D., Roth, E., Mitchell, T. R. T., Snyder, J. B., MacIver, M. A., Fortune, E. S., and Cowan, N. J. (2013). Mutually opposing forces during locomotion can eliminate the tradeoff between maneuverability and stability. *Proceedings of the National Academy of Sciences*, 110(47), 18798–18803. https://doi.org/10.1073/pnas.1305598110

  This study analyzes how opposing locomotor forces can alter the relationship between maneuverability and stability. It is an example of using mechanics and control analysis to test biologically meaningful performance tradeoffs.

- Cowan, N. J., Ankarali, M. M., Dyhr, J. P., Madhav, M. S., Roth, E., Sefati, S., Sponberg, S., Stamper, S. A., Fortune, E. S., and Daniel, T. L. (2014). Feedback control as a framework for understanding tradeoffs in biology. *Integrative and Comparative Biology*, 54(2), 223–237. https://doi.org/10.1093/icb/icu050

  This review presents feedback control as a framework for studying biological tradeoffs among stability, responsiveness, sensing, and energetic cost. It provides a broad conceptual bridge between mechanistic biology and control-theoretic modeling.

- LIMBS Laboratory, Johns Hopkins University. Research materials and publication list. Consult current laboratory materials.

#### Fortune: weakly electric fish, active sensing, and feedback control

- Cowan, N. J., and Fortune, E. S. (2007). The critical role of locomotion mechanics in decoding sensory systems. *Journal of Neuroscience*, 27(5), 1123–1128. https://doi.org/10.1523/JNEUROSCI.4195-06.2007

  See the annotated entry in [Cowan and the LIMBS Laboratory: mechanics, active sensing, and system identification](#cowan-and-the-limbs-laboratory-mechanics-active-sensing-and-system-identification).

- Roth, E., Zhuang, K., Stamper, S. A., Fortune, E. S., and Cowan, N. J. (2011). Stimulus predictability mediates a switch in locomotor smooth-pursuit performance for *Eigenmannia virescens*. *Journal of Experimental Biology*, 214, 1170–1180. https://doi.org/10.1242/jeb.052043

  This study examines how stimulus predictability alters smooth-pursuit behavior in weakly electric fish. It is useful for models in which sensory context changes the active feedback strategy or behavioral regime.

- Madhav, M. S., Stamper, S. A., Fortune, E. S., and Cowan, N. J. (2013). Closed-loop stabilization of the jamming avoidance response reveals its locally unstable and globally nonlinear dynamics. *Journal of Experimental Biology*, 216, 4272–4284. https://doi.org/10.1242/jeb.088914

  This paper uses closed-loop experiments to characterize locally unstable and globally nonlinear dynamics in the jamming-avoidance response. It is a close example of event- and feedback-aware system identification in a biological behavior.

- Yang, Y., Yared, D. G., Fortune, E. S., and Cowan, N. J. (2024). Sensorimotor adaptation to destabilizing dynamics in weakly electric fish. *Current Biology*.

  This study examines sensorimotor adaptation in weakly electric fish exposed to destabilizing dynamics. It provides a contemporary example of experimentally probing feedback adaptation and behavioral stability.

- Fortune, E. S. and collaborators. Primary research on locomotion, active sensing, sensory feedback, and behavioral variability in weakly electric fish. Consult current publication lists.

#### Hines and the NEURON ecosystem: neural and network simulation

- Hines, M. L., and Carnevale, N. T. (1997). The NEURON simulation environment. *Neural Computation*, 9(6), 1179–1209. https://doi.org/10.1162/neco.1997.9.6.1179

  This paper introduces the NEURON simulation environment for biophysically detailed neuronal modeling. It provides historical and conceptual context for simulator architectures that combine continuous membrane dynamics with discrete synaptic and network events.

- Hines, M. L., and Carnevale, N. T. (2001). NEURON: A tool for neuroscientists. *The Neuroscientist*, 7(2), 123–135. https://doi.org/10.1177/107385840100700207

  This review describes NEURON’s modeling scope, including cellular and network simulation for neuroscience. It is useful background for choosing a specialized neural simulator when biological and numerical detail exceed the intended scope of `hybrid-ds-julia`.

- Hines, M. L., and Carnevale, N. T. (2004). Discrete event simulation in the NEURON environment. *Neurocomputing*, 58–60, 1117–1122. https://doi.org/10.1016/j.neucom.2004.01.183

  This paper addresses discrete-event simulation in the NEURON environment. It is directly relevant as a domain-specific precedent for combining continuous neural dynamics with discontinuous synaptic, stimulation, and network events.

- Migliore, M., Cannia, C., Lytton, W. W., Markram, H., and Hines, M. L. (2006). Parallel network simulations with NEURON. *Journal of Computational Neuroscience*, 21, 119–129. https://doi.org/10.1007/s10827-006-7949-5

  This paper describes parallel simulation of neuronal networks with NEURON. It provides practical context for scaling independent or distributed neural simulations, while communication and event scheduling can limit ideal parallelism.

- Hines, M. L., Davison, A. P., and Muller, E. (2009). NEURON and Python. *Frontiers in Neuroinformatics*, 3, 1. https://doi.org/10.3389/neuro.11.001.2009

  This paper describes Python interoperability for NEURON, illustrating how a specialized simulator can be integrated into a broader scientific-computing workflow.

- Carnevale, N. T., and Hines, M. L. (2006). *The NEURON Book*. Cambridge University Press.

  This textbook covers biophysical neuron and network modeling with NEURON, including morphology, membrane mechanisms, synapses, numerical simulation, and model construction. It is a foundational reference for applications requiring detailed neuronal simulation rather than reduced-order hybrid ODE models.

- NEURON and CoreNEURON documentation; ModelDB. Consult current documentation and model repositories.

### Domains where mechanistic hybrid modeling is more limited

The following readings are included to support careful treatment of causal identification, diagnostic uncertainty, symptom heterogeneity, alternative explanations, comorbidity, treatment-selection confounding, and appropriate limits on individualized mechanistic inference. In these domains, mechanistic hybrid models may remain useful for transparent, limited research questions, but they should not be presented as validated individualized diagnostic, prognostic, or treatment-selection tools without strong condition-specific evidence.

#### ME/CFS

- National Academy of Medicine. (2015). *Beyond Myalgic Encephalomyelitis/Chronic Fatigue Syndrome: Redefining an Illness*. National Academies Press. https://doi.org/10.17226/19012

  This consensus report reviews the clinical evidence, diagnostic challenges, symptom burden, and research needs associated with ME/CFS. It is useful for understanding why heterogeneity, uncertain mechanisms, and limited biomarkers constrain individualized mechanistic inference.

- U.S. Centers for Disease Control and Prevention. ME/CFS clinical overview, diagnostic guidance, and diagnostic criteria. Consult current guidance.

- National Institute for Health and Care Excellence. (2021). *Myalgic encephalomyelitis (or encephalopathy)/chronic fatigue syndrome: Diagnosis and management* (NG206). Consult current guidance.

- Nacul, L., et al. (2020). How myalgic encephalomyelitis/chronic fatigue syndrome is diagnosed and managed in primary care. Consult current systematic reviews and guidance.

#### Long COVID and persistent post-infectious symptoms

- World Health Organization. A clinical case definition of post COVID-19 condition by a Delphi consensus. Consult current WHO materials.

- U.S. Centers for Disease Control and Prevention. Long COVID clinical overview and clinical guidance. Consult current guidance.

- RECOVER Initiative. Publications, cohort resources, and current evidence on post-acute sequelae of SARS-CoV-2 infection. Consult current materials.

- Davis, H. E., McCorkell, L., Vogel, J. M., and Topol, E. J. (2023). Long COVID: Major findings, mechanisms, and recommendations. *Nature Reviews Microbiology*, 21, 133–146. https://doi.org/10.1038/s41579-022-00846-2

  This review summarizes evidence on Long COVID manifestations, proposed mechanisms, and research priorities. Its breadth underscores the limits of attributing persistent symptoms to a single mechanism or using an unvalidated mechanistic model for individual treatment decisions.

- Thaweethai, T., et al. (2023). Development of a definition of postacute sequelae of SARS-CoV-2 infection. *JAMA*, 329(22), 1934–1946. https://doi.org/10.1001/jama.2023.8823

  This study develops an empirical research definition for postacute sequelae of SARS-CoV-2 infection. It is relevant to outcome-definition uncertainty and to the distinction between research phenotyping and individual clinical diagnosis.

#### Persistent symptoms following Lyme disease treatment

- Lantos, P. M., Rumbaugh, J., Bockenstedt, L. K., et al. (2021). Clinical practice guidelines by the Infectious Diseases Society of America, American Academy of Neurology, and American College of Rheumatology: 2020 guidelines for the prevention, diagnosis, and treatment of Lyme disease. *Clinical Infectious Diseases*, 72(1), e1–e48. https://doi.org/10.1093/cid/ciaa1215

  This guideline addresses prevention, diagnosis, and treatment of Lyme disease using a systematic evidence-review process. It is an authoritative clinical reference for delimiting what a model should not override or extrapolate beyond evidence-based care.

- U.S. Centers for Disease Control and Prevention. Lyme disease and prolonged symptoms following Lyme disease. Consult current guidance.

- National Academies of Sciences, Engineering, and Medicine. (2025). *Charting a Path Toward New Treatments for Lyme Infection-Associated Chronic Illnesses*. National Academies Press.

  This consensus report addresses research needs and therapeutic-development challenges for Lyme infection-associated chronic illnesses. It provides scope on clinical heterogeneity and unresolved mechanisms rather than a basis for a single validated causal model.

- Bobe, J. R., Jutras, B. L., Horn, E. J., et al. (2021). Recent progress in Lyme disease and remaining challenges. *Frontiers in Medicine*, 8, 666554. https://doi.org/10.3389/fmed.2021.666554

  This review surveys progress and remaining challenges in Lyme disease research. It is useful for understanding the unresolved biological, diagnostic, and treatment questions that constrain mechanistic modeling claims.

#### Mental health and complex behavioral care

- Hernán, M. A., and Robins, J. M. (2020). *Causal Inference: What If*. Chapman and Hall/CRC. https://www.hsph.harvard.edu/miguel-hernan/causal-inference-book/

  This textbook develops causal-inference concepts and methods for observational and experimental data, including confounding, counterfactuals, and target-trial reasoning. It is essential background when considering whether observed treatment and outcome trajectories support causal or policy claims.

- Shadish, W. R., Cook, T. D., and Campbell, D. T. (2002). *Experimental and Quasi-Experimental Designs for Generalized Causal Inference*. Houghton Mifflin.

  This textbook covers experimental and quasi-experimental design, validity threats, and causal interpretation. It provides foundational scope for evaluating evidence when randomized experiments are unavailable or difficult.

- Greenland, S., Pearl, J., and Robins, J. M. (1999). Causal diagrams for epidemiologic research. *Epidemiology*, 10(1), 37–48. https://doi.org/10.1097/00001648-199901000-00008

  This paper introduces causal diagrams as tools for expressing assumptions about confounding, selection, and causal pathways. It is useful for making explicit the assumptions required before using observational behavioral or clinical data to support intervention claims.

- National Institute of Mental Health. Research Domain Criteria and current research resources. Consult current materials.

- Consult disorder-specific clinical guidelines, epidemiological studies, treatment-trial literature, and implementation-science research for the intended mental-health or behavioral-care application.
