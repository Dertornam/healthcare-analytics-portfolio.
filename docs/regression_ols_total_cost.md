# OLS regression: total cost

Dependent variable: `total_cost`

```
                            OLS Regression Results                            
==============================================================================
Dep. Variable:             total_cost   R-squared:                       0.961
Model:                            OLS   Adj. R-squared:                  0.961
Method:                 Least Squares   F-statistic:                 1.031e+04
Date:                Sun, 16 Nov 2025   Prob (F-statistic):               0.00
Time:                        03:28:21   Log-Likelihood:                -44697.
No. Observations:                5513   AIC:                         8.942e+04
Df Residuals:                    5499   BIC:                         8.952e+04
Df Model:                          13                                         
Covariance Type:            nonrobust                                         
========================================================================================
                           coef    std err          t      P>|t|      [0.025      0.975]
----------------------------------------------------------------------------------------
const                 -188.8557    165.861     -1.139      0.255    -514.009     136.297
age                     -1.1127      0.662     -1.680      0.093      -2.411       0.186
diabetes_flag           97.7809     47.099      2.076      0.038       5.448     190.114
heart_failure_flag     188.2330     37.896      4.967      0.000     113.943     262.523
copd_flag              160.7740     33.707      4.770      0.000      94.695     226.853
bmi                      2.4720      2.473      1.000      0.318      -2.376       7.320
hba1c                   29.7452     24.894      1.195      0.232     -19.057      78.548
outpatient_visits      147.0980      5.749     25.586      0.000     135.827     158.369
ed_visits              849.9331     15.013     56.612      0.000     820.501     879.365
inpatient_admissions  5549.6517     21.326    260.231      0.000    5507.845    5591.459
care_mgmt_enrolled     -14.6226     31.558     -0.463      0.643     -76.489      47.244
wearable_steps_avg       0.0016      0.005      0.299      0.765      -0.009       0.012
genai_triage_flag     -172.1081     34.768     -4.950      0.000    -240.267    -103.949
high_risk_flag          -1.3041     48.023     -0.027      0.978     -95.448      92.840
==============================================================================
Omnibus:                     1301.323   Durbin-Watson:                   1.953
Prob(Omnibus):                  0.000   Jarque-Bera (JB):            47320.397
Skew:                           0.393   Prob(JB):                         0.00
Kurtosis:                      17.331   Cond. No.                     1.22e+05
==============================================================================

Notes:
[1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
[2] The condition number is large, 1.22e+05. This might indicate that there are
strong multicollinearity or other numerical problems.
```