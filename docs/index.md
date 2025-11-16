---
title: Healthcare Analytics Portfolio (Anonymized)
---

# Healthcare Analytics Portfolio (Anonymized)

**Data Analyst** specializing in end-to-end analytics, survey & operational insights, and reproducible reporting.
This portfolio demonstrates a 10-year (2015–2024) chronic-care dataset with descriptive analytics, correlations,
**logistic regression for readmissions**, **OLS for total cost**, **ANOVA**, and reproducible charts via GitHub Actions.

<style>
.port-btn{
  display:inline-block;
  padding:.6rem 1rem;
  margin:.25rem .4rem 0 0;
  border-radius:8px;
  background:#0366d6;
  color:#fff !important;
  text-decoration:none !important;
  border:1px solid rgba(0,0,0,.08);
  box-shadow:0 1px 2px rgba(0,0,0,.05);
  font-weight:600;
}
.port-btn:hover{ filter:brightness(0.95); }
</style>

<p class="btn-row">
  <a class="port-btn port-btn--light" href="...">View on GitHub</a>
  <a class="port-btn port-btn--light" href="#projects">Explore My Projects</a>
  <a class="port-btn port-btn--light" href="resume.pdf">Résumé</a>
  <a class="port-btn port-btn--light" href="https://www.linkedin.com/in/derrick-dzormeku-mba-75288644">LinkedIn</a>
</p>

---

## Featured visuals

- Admissions trend — *utilization over time*  
  ![](./figs/admissions_trend.png)

- ED visits trend — *front-door demand*  
  ![](./figs/ed_visits_trend.png)

- Average HbA1c — *clinical control signal*  
  ![](./figs/hba1c_trend.png)

- Readmission rate (30d) — *outcome metric*  
  ![](./figs/readmit_rate_trend.png)

- Total cost — *budget signal*  
  ![](./figs/total_cost_trend.png)

- Cost by insurance — *variation*  
  ![](./figs/cost_by_insurance.png)

- Steps vs cost — *behavior vs spend*  
  ![](./figs/steps_vs_cost.png)

- HbA1c vs readmission — *clinical driver*  
  ![](./figs/hba1c_vs_readmit.png)

---

## <a name="dataset"></a>Dataset
- File: [`healthcare_2015_2024_patient_year.csv`](./healthcare_2015_2024_patient_year.csv)  
- Unit: patient-year records with demographics, conditions, utilization, outcomes, cost, and program flags.

---

## <a name="analysis"></a>Statistical analysis
- **Descriptive statistics (table):** [desc_stats.md](desc_stats.md)
- **Correlation matrix:** [corr_matrix.md](corr_matrix.md)
- **Logistic regression:** (readmit): [summary + interpretation](regression_logit_readmission.md)
- **OLS (total cost):** [summary + interpretation](regression_ols_total_cost.md)
- **ANOVA (year):** [anova_total_cost_by_year.md](anova_total_cost_by_year.md)
- **t-test (HbA1c):** [ttest_hba1c_care_mgmt_diabetes.md](ttest_hba1c_care_mgmt_diabetes.md)

---

## Case studies & trends
See **[case studies & future trends](./case_studies.html)** for a concise briefing on analytics types, operational wins,
AI adoption, and implementation challenges in healthcare analytics.
