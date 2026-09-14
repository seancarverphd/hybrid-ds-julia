### Clinical operations and treatment delivery

This section covers modeling and evidence relevant to treatment delivery, adherence, therapeutic monitoring, critical-care workflows, digital health, and clinical decision support. These references support research and evaluation workflows; they do not establish that a model, algorithm, or software system is suitable for autonomous clinical decision-making.

#### Dose scheduling, adherence, and therapeutic monitoring

- Sheiner, L. B., and Steimer, J.-L. (2000). Pharmacokinetic/pharmacodynamic modeling in drug development. *Annual Review of Pharmacology and Toxicology*, 40, 67–95. https://doi.org/10.1146/annurev.pharmtox.40.1.67

  This review explains the role of PK/PD modeling in drug development, linking exposure, response, variability, and study design. It provides foundational context for representing dose schedules and observed responses, before adding explicit adherence, treatment-hold, or monitoring-event logic.

- Mould, D. R., and Upton, R. N. (2012). Basic concepts in population modeling, simulation, and model-based drug development. *CPT: Pharmacometrics & Systems Pharmacology*, 1, e6. https://doi.org/10.1038/psp.2012.4

  This tutorial review introduces population modeling, simulation, covariates, variability, and model-based drug-development concepts. Its scope is useful for distinguishing population-level parameter distributions from individual longitudinal states and event histories.

- Kang, J. S., and Lee, M. H. (2009). Overview of therapeutic drug monitoring. *The Korean Journal of Internal Medicine*, 24(1), 1–10. https://doi.org/10.3904/kjim.2009.24.1.1

  This review outlines the rationale, indications, sampling considerations, and interpretation issues for therapeutic drug monitoring. It is relevant to observation models in which measured concentration data inform dose adjustment but do not directly reveal all latent PK/PD states.

- Nieuwlaat, R., Wilczynski, N., Navarro, T., et al. (2014). Interventions for enhancing medication adherence. *Cochrane Database of Systematic Reviews*, 2014(11), CD000011. https://doi.org/10.1002/14651858.CD000011.pub4

  This systematic review evaluates interventions intended to improve adherence to prescribed medication. It provides a cautionary evidence base for adherence scenarios: behavioral interventions, measurement methods, and outcomes vary substantially, so missed-dose processes should not be treated as universally predictable or easily corrected.

- Vrijens, B., De Geest, S., Hughes, D. A., et al. (2012). A new taxonomy for describing and defining adherence to medications. *British Journal of Clinical Pharmacology*, 73(5), 691–705. https://doi.org/10.1111/j.1365-2125.2012.04167.x

  This consensus paper distinguishes medication initiation, implementation, and persistence. It is useful for translating adherence into explicit event semantics—for example, delayed or omitted administrations, changing dose implementation, and treatment discontinuation—rather than representing all nonadherence as a single scalar parameter.

- Berg, M. J., et al. (2017). How can we assess adherence to antiepileptic drug therapy? *Epilepsia*, 58(11), 1919–1929. https://doi.org/10.1111/epi.13910

  This review compares adherence-assessment approaches, including self-report, pharmacy records, electronic monitoring, and drug concentrations. It is a useful reminder that observed adherence signals are imperfect measurements and should be modeled separately from the latent medication-taking process when possible.

#### Dose adjustment, monitoring policies, and closed-loop care

- Holford, N. H. G., Kimko, H. C., Monteleone, J. P. R., and Peck, C. C. (2000). Simulation of clinical trials. *Annual Review of Pharmacology and Toxicology*, 40, 209–234. https://doi.org/10.1146/annurev.pharmtox.40.1.209

  This review describes clinical-trial simulation as a way to combine PK/PD models, variability, study design, and decision questions. It is relevant to virtual-patient studies comparing dose, monitoring, and threshold-policy scenarios before any prospective evaluation.

- Proost, J. H., and Meijer, D. K. F. (1992). MW/Pharm, an integrated software package for drug dosage regimen calculation and therapeutical drug monitoring. *Computers in Biology and Medicine*, 22(3), 155–163. https://doi.org/10.1016/0010-4825(92)90004-8

  This paper describes an early integrated approach to dosage-regimen calculation and therapeutic drug monitoring. It provides historical context for the practical link between PK models, observed concentrations, and clinician-directed dose adjustment.

- Tannenbaum, S. J., and Mager, D. E. (2017). A pharmacokinetic-pharmacodynamic model-based approach to the design of improved pediatric dosing regimens. *Clinical Pharmacology & Therapeutics*, 102(4), 593–601. https://doi.org/10.1002/cpt.698

  This paper illustrates how PK/PD modeling can inform dosing-regimen design in a population with distinctive physiological constraints. It is relevant as an example of model-informed schedule design, not as a generic rule for transferring a model to a different population or indication.

- Dalla Man, C., Rizza, R. A., and Cobelli, C. (2007). Meal simulation model of the glucose-insulin system. *IEEE Transactions on Biomedical Engineering*, 54(10), 1740–1749. https://doi.org/10.1109/TBME.2007.893506

  This mechanistic glucose–insulin model represents meal disturbances and physiological dynamics relevant to closed-loop control research. It offers a non-oncology example of continuous physiology coupled to scheduled inputs, measurement timing, and control decisions.

- Kovatchev, B. P., Renard, E., Cobelli, C., et al. (2013). Safety of outpatient closed-loop control for overnight glucose control in adults with type 1 diabetes: A randomized crossover trial. *The Lancet Diabetes & Endocrinology*, 1(1), 30–37. https://doi.org/10.1016/S2213-8587(13)70010-1

  This clinical study evaluates overnight closed-loop glucose control in adults with type 1 diabetes. It is a useful example of how a control-oriented physiological model and monitoring system require prospective safety evaluation rather than simulation evidence alone.

#### Hospital, critical care, and digital health

- Clermont, G., Angus, D. C., DiRusso, S. M., Griffin, M., and Linde-Zwirble, W. T. (2004). Predicting hospital mortality for patients in the intensive care unit: A comparison of artificial neural networks with logistic regression models. *Critical Care Medicine*, 29, 291–296.

  This study compares neural-network and logistic-regression approaches to ICU mortality prediction. It is an early reminder that predictive performance depends on the intended population, data representation, and evaluation setting, and that prediction alone does not define a treatment policy.

- Johnson, A. E. W., Pollard, T. J., Shen, L., et al. (2016). MIMIC-III, a freely accessible critical care database. *Scientific Data*, 3, 160035. https://doi.org/10.1038/sdata.2016.35

  This paper describes MIMIC-III, a deidentified single-center critical-care database containing vital signs, medications, laboratory measurements, clinical observations, and notes. It is a useful resource for methods development and retrospective validation, while its setting, data-generating processes, and missingness patterns limit direct transportability to other hospitals.

- Heldt, T., et al. Physiological modeling, monitoring, and control literature for intensive-care and clinical decision-support systems. Consult condition-specific literature.

- Behar, J. A., et al. (2018). Remote health monitoring and wearable physiological sensing: Methods and applications. Consult current reviews and validation studies.

- Steinhubl, S. R., Muse, E. D., and Topol, E. J. (2015). The emerging field of mobile health. *Science Translational Medicine*, 7(283), 283rv3. https://doi.org/10.1126/scitranslmed.aaa3487

  This review surveys mobile-health technologies and their potential roles in longitudinal measurement, engagement, and care delivery. It provides broad context for using wearable or remote-monitoring data as observations, while emphasizing that sensing availability does not by itself establish clinical validity or actionability.

- Goldsack, J. C., Coravos, A., Bakker, J. P., et al. (2020). Verification, analytical validation, and clinical validation (V3): The foundation of determining fit-for-purpose for biometric monitoring technologies. *npj Digital Medicine*, 3, 55. https://doi.org/10.1038/s41746-020-0260-4

  This paper defines verification, analytical validation, and clinical validation for biometric-monitoring technologies. It is directly relevant to treating wearable and digital-biomarker streams as measurement systems with device error, context dependence, and a defined intended use—not as interchangeable ground truth.

- Shah, N. H., and Tenenbaum, J. D. (2012). The coming age of data-driven medicine: Translational bioinformatics' next frontier. *Journal of the American Medical Informatics Association*, 19(e1), e2–e4. https://doi.org/10.1136/amiajnl-2012-000969

  This perspective discusses the opportunities and translational challenges of data-driven medicine. It is useful background for integrating longitudinal clinical data with mechanistic models, while preserving attention to data quality, causal interpretation, and workflow context.

#### Clinical decision support, validation, and governance

- Collins, G. S., Moons, K. G. M., Dhiman, P., et al. (2024). TRIPOD+AI statement: Updated guidance for reporting clinical prediction models that use regression or machine learning methods. *BMJ*, 385, e078378. https://doi.org/10.1136/bmj-2023-078378

  This reporting guideline covers clinical prediction models developed with regression or machine-learning methods and supersedes the original TRIPOD statement. It is relevant when documenting a model’s predictors, outcomes, validation, performance, and intended use, including any learned components attached to a hybrid mechanistic workflow.

- Vasey, B., Nagendran, M., Campbell, B., et al. (2022). Reporting guideline for the early stage clinical evaluation of decision support systems driven by artificial intelligence: DECIDE-AI. *Nature Medicine*, 28, 924–933. https://doi.org/10.1038/s41591-022-01772-9

  This consensus reporting guideline addresses early live clinical evaluation of AI-based decision-support systems. It emphasizes real-world workflow, human factors, safety, and intended use—considerations that remain necessary even when a system is built on an interpretable mechanistic model.

- Liu, X., Cruz Rivera, S., Moher, D., et al. (2020). Reporting guidelines for clinical trial reports for interventions involving artificial intelligence: The CONSORT-AI extension. *Nature Medicine*, 26, 1364–1374. https://doi.org/10.1038/s41591-020-1034-x

  This guideline extends CONSORT reporting for clinical trials involving AI interventions. Its scope is useful if a model-supported intervention proceeds beyond retrospective analysis toward prospective comparative evaluation.

- Sutton, R. T., Pincock, D., Baumgart, D. C., et al. (2020). An overview of clinical decision support systems: Benefits, risks, and strategies for success. *npj Digital Medicine*, 3, 17. https://doi.org/10.1038/s41746-020-0221-y

  This review covers clinical decision-support-system functions, potential benefits, implementation barriers, and safety risks. It is useful for distinguishing a technically accurate predictive or mechanistic model from a decision-support tool that must fit clinical workflow and preserve appropriate clinician oversight.

- U.S. Food and Drug Administration. Clinical Decision Support Software: Guidance for Industry and Food and Drug Administration Staff. Consult the current guidance.

- U.S. Food and Drug Administration. Software as a Medical Device (SaMD) and related digital-health regulatory materials. Consult current guidance.
