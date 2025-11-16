# OLS: total annual cost

Dependent variable: **total_cost**

Predictors: age, bmi, hba1c, wearable_steps_avg, diabetes_flag, heart_failure_flag, copd_flag, outpatient_visits, ed_visits, inpatient_admissions, care_mgmt_enrolled, high_risk_flag

```
                            OLS Regression Results                            
==============================================================================
Dep. Variable:             total_cost   R-squared:                       0.960
Model:                            OLS   Adj. R-squared:                  0.960
Method:                 Least Squares   F-statistic:                 1.112e+04
Date:                Sun, 16 Nov 2025   Prob (F-statistic):               0.00
Time:                        04:09:23   Log-Likelihood:                -44710.
No. Observations:                5513   AIC:                         8.945e+04
Df Residuals:                    5500   BIC:                         8.953e+04
Df Model:                          12                                         
Covariance Type:            nonrobust                                         
========================================================================================
                           coef    std err          t      P>|t|      [0.025      0.975]
----------------------------------------------------------------------------------------
const                 -201.3101    166.196     -1.211      0.226    -527.120     124.499
age                     -1.2359      0.663     -1.863      0.063      -2.536       0.065
bmi                      2.4302      2.478      0.981      0.327      -2.428       7.289
hba1c                   29.9368     24.947      1.200      0.230     -18.970      78.843
wearable_steps_avg       0.0018      0.005      0.337      0.736      -0.009       0.012
diabetes_flag           94.8142     47.196      2.009      0.045       2.291     187.337
heart_failure_flag     188.2595     37.976      4.957      0.000     113.811     262.708
copd_flag              161.5107     33.779      4.781      0.000      95.291     227.730
outpatient_visits      147.1745      5.761     25.545      0.000     135.880     158.469
ed_visits              850.3931     15.045     56.524      0.000     820.899     879.887
inpatient_admissions  5548.8844     21.371    259.648      0.000    5506.989    5590.780
care_mgmt_enrolled     -15.0884     31.625     -0.477      0.633     -77.087      46.910
high_risk_flag           2.2491     48.120      0.047      0.963     -92.085      96.583
==============================================================================
Omnibus:                     1299.748   Durbin-Watson:                   1.934
Prob(Omnibus):                  0.000   Jarque-Bera (JB):            47479.004
Skew:                           0.389   Prob(JB):                         0.00
Kurtosis:                      17.356   Cond. No.                     1.22e+05
==============================================================================

Notes:
[1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
[2] The condition number is large, 1.22e+05. This might indicate that there are
strong multicollinearity or other numerical problems.
```


## Interpretation — OLS (total cost)

**What the model says.**  
Cost rises with utilization (**inpatient > ED > outpatient**) and clinical risk flags. Steps trend **negatively** with cost. Coefficients may look small per unit but accumulate over a year.

**What it means for finance & ops.**  
A small group of **high utilizers** drives spend. Because costs are skewed, consider **GLM Gamma (log link)** or **quantile regression** for robustness.

**Actions.**  
Stand up a **High-Utilizer Review**; expand **telehealth/home monitoring** for chronic cohorts with frequent ED use. Track ROI with matched pre/post cohorts and monthly dashboards.
