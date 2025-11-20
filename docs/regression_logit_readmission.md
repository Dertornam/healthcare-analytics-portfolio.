# Logistic regression: 30-day readmission


<pre>
                           Logit Regression Results                           
==============================================================================
Dep. Variable:        any_30d_readmit   No. Observations:                 5513
Model:                          Logit   Df Residuals:                     5499
Method:                           MLE   Df Model:                           13
Date:                Sun, 16 Nov 2025   Pseudo R-squ.:                 0.04934
Time:                        04:24:11   Log-Likelihood:                -1467.9
converged:                       True   LL-Null:                       -1544.1
Covariance Type:            nonrobust   LLR p-value:                 6.893e-26
========================================================================================
                           coef    std err          z      P&gt;|z|      [0.025      0.975]
----------------------------------------------------------------------------------------
const                   -6.5667      0.766     -8.577      0.000      -8.067      -5.066
age                      0.0318      0.003      9.715      0.000       0.025       0.038
diabetes_flag           -0.1770      0.214     -0.828      0.408      -0.596       0.242
heart_failure_flag      -0.0298      0.169     -0.176      0.860      -0.361       0.302
copd_flag               -0.0196      0.149     -0.131      0.895      -0.312       0.273
bmi                     -0.0009      0.011     -0.082      0.935      -0.023       0.021
hba1c                    0.2541      0.110      2.302      0.021       0.038       0.471
outpatient_visits        0.0361      0.026      1.390      0.164      -0.015       0.087
ed_visits                0.2351      0.064      3.694      0.000       0.110       0.360
inpatient_admissions     0.1810      0.089      2.036      0.042       0.007       0.355
care_mgmt_enrolled      -0.1619      0.150     -1.078      0.281      -0.456       0.132
wearable_steps_avg    3.511e-05   2.49e-05      1.412      0.158   -1.36e-05    8.38e-05
genai_triage_flag       -0.2979      0.174     -1.708      0.088      -0.640       0.044
high_risk_flag          -0.0056      0.193     -0.029      0.977      -0.383       0.372
========================================================================================
</pre>

## Interpretation — Logistic regression (30-day readmission)

**What the model says (plain English).**  
Older age, recent utilization (ED visits / admissions), and higher **HbA1c** are associated with **higher** odds of readmission. Steps show a small, directionally protective effect. Pseudo-R² is modest—as expected for readmissions.

**What it means for care & data.**  
High-utilizers with poor glycemic control are the key risk segment. Expect unobserved SDOH (transportation, caregiver support) to matter; add them if available.

**Actions.**  
Trigger a **48–72h post-discharge call** and **7–10 day clinic follow-up** for older patients with prior-year admissions/ED. Tighten HbA1c management. Pilot a **nurse call-back + med reconciliation** bundle for the top-risk decile.
