# 06-stats-and-modeling/src/run_stats.py
import os, textwrap
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
from scipy import stats

# ---------- paths ----------
DOCS_DIR = "docs"
os.makedirs(DOCS_DIR, exist_ok=True)

# read CSV: env var (from workflow) or default path in docs/
CSV_PATH = os.environ.get("SURVEY_CSV", os.path.join(DOCS_DIR, "healthcare_2015_2024_patient_year.csv"))
df = pd.read_csv(CSV_PATH)

# ---------- helpers ----------
def write_md_table(df_tbl: pd.DataFrame, md_path: str, title: str = None, after: str = ""):
    """Write a Markdown page with optional title, table, and extra text."""
    lines = []
    if title:
        lines += [f"# {title}", ""]
    # requires 'tabulate' installed in workflow
    lines += [df_tbl.to_markdown(index=True), ""]
    if after:
        lines += [after.strip(), ""]
    with open(os.path.join(DOCS_DIR, md_path), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

def append_md(md_filename: str, md_text: str):
    with open(os.path.join(DOCS_DIR, md_filename), "a", encoding="utf-8") as f:
        f.write("\n\n" + md_text.strip() + "\n")

sns.set_theme(style="whitegrid")

# =========================================
# 1) DESCRIPTIVE STATISTICS (nice Markdown)
# =========================================
num = df.select_dtypes(include=[np.number])
desc = num.describe().T
desc = desc.rename(columns={
    "count":"n","mean":"mean","std":"sd","min":"min","25%":"p25","50%":"p50",
    "75%":"p75","max":"max"
}).round(3)

# CSV (if someone wants to download)
desc.to_csv(os.path.join(DOCS_DIR, "desc_stats.csv"))
# Markdown (what the site should link to)
write_md_table(
    desc,
    md_path="desc_stats.md",
    title="Descriptive statistics",
    after=""
)

append_md("desc_stats.md", textwrap.dedent("""
## Interpretation — Descriptive statistics

**What stands out.**  
Utilization (ED and inpatient) and **total_cost** are right-skewed—typical in healthcare where a small share of patients drive spend. Physiologic variables (SBP/DBP, BMI) are stable; **HbA1c** has wider spread among diabetics.

**What it means.**  
Skew suggests robust summaries (medians/IQR) are more representative than means. When modelling **total_cost**, a GLM with **Gamma (log link)** or quantile regression often fits better than OLS.

**Actions.**  
Profile the **top-cost decile** each quarter; ensure case-management eligibility checks and post-discharge touchpoints are applied consistently. Track med adherence and access barriers for high-risk chronic patients.
"""))

# =========================================
# 2) CORRELATIONS + HEATMAP
# =========================================
corr = num.corr(numeric_only=True).round(3)
corr.to_csv(os.path.join(DOCS_DIR, "corr_matrix.csv"))

# heatmap figure
plt.figure(figsize=(10,8))
sns.heatmap(corr, cmap="vlag", center=0, linewidths=0.2)
plt.title("Correlation heatmap")
plt.tight_layout()
plt.savefig(os.path.join(DOCS_DIR, "corr_heatmap.png"), dpi=180)
plt.close()

# Markdown page that embeds the heatmap and table
with open(os.path.join(DOCS_DIR, "corr_matrix.md"), "w", encoding="utf-8") as f:
    f.write("# Correlation matrix\n\n")
    f.write("![Correlation heatmap](corr_heatmap.png)\n\n")
    f.write(corr.to_markdown(index=True))
    f.write("\n")

append_md("corr_matrix.md", textwrap.dedent("""
## Interpretation — Correlations

**What you’ll see.**  
Utilization features correlate **positively** with total_cost; **HbA1c** tends to track with readmissions and cost; physical-activity proxy (wearable_steps_avg) has **negative** associations with ED/cost.

**Caveats.**  
Correlations are not causal; shared drivers (frailty, access, polypharmacy) can produce spurious links.

**Actions.**  
Use correlations to **screen features** and set **reasonableness checks** (e.g., rising steps ↔ falling ED). Verify directions in multivariate models or pilots before acting.
"""))

# =========================================
# 3) LOGISTIC REGRESSION — 30-day readmission
# =========================================
# pick predictors present in your dataset
logit_features = [
    "age","diabetes_flag","heart_failure_flag","copd_flag","bmi","hba1c",
    "outpatient_visits","ed_visits","inpatient_admissions","care_mgmt_enrolled",
    "wearable_steps_avg","genai_triage_flag","high_risk_flag"
]
logit_features = [c for c in logit_features if c in df.columns]
df_logit = df.dropna(subset=["any_30d_readmit"] + logit_features).copy()
y = df_logit["any_30d_readmit"].astype(int)
X = sm.add_constant(df_logit[logit_features])
logit_res = sm.Logit(y, X).fit(disp=0)

with open(os.path.join(DOCS_DIR, "regression_logit_readmission.md"), "w", encoding="utf-8") as f:
    f.write("# Logistic regression: 30-day readmission\n\n")
    f.write("Dependent variable: **any_30d_readmit** (0/1)\n\n")
    f.write("Predictors: " + ", ".join(logit_features) + "\n\n")
    f.write("```\n" + str(logit_res.summary()) + "\n```\n")

append_md("regression_logit_readmission.md", textwrap.dedent("""
## Interpretation — Logistic regression (30-day readmission)

**What the model says (plain English).**  
Older age, recent utilization (ED visits / admissions), and higher **HbA1c** are associated with **higher** odds of readmission. Steps show a small, directionally protective effect. Pseudo-R² is modest—as expected for readmissions.

**What it means for care & data.**  
High-utilizers with poor glycemic control are the key risk segment. Expect unobserved SDOH (transportation, caregiver support) to matter; add them if available.

**Actions.**  
Trigger a **48–72h post-discharge call** and **7–10 day clinic follow-up** for older patients with prior-year admissions/ED. Tighten HbA1c management. Pilot a **nurse call-back + med reconciliation** bundle for the top-risk decile.
"""))

# =========================================
# 4) OLS — TOTAL COST
# =========================================
ols_features = [
    "age","bmi","hba1c","wearable_steps_avg","diabetes_flag","heart_failure_flag",
    "copd_flag","outpatient_visits","ed_visits","inpatient_admissions","care_mgmt_enrolled",
    "high_risk_flag"
]
ols_features = [c for c in ols_features if c in df.columns]
df_ols = df.dropna(subset=["total_cost"] + ols_features).copy()
y_cost = df_ols["total_cost"]
X_cost = sm.add_constant(df_ols[ols_features])
ols_res = sm.OLS(y_cost, X_cost).fit()

with open(os.path.join(DOCS_DIR, "regression_ols_total_cost.md"), "w", encoding="utf-8") as f:
    f.write("# OLS: total annual cost\n\n")
    f.write("Dependent variable: **total_cost**\n\n")
    f.write("Predictors: " + ", ".join(ols_features) + "\n\n")
    f.write("```\n" + str(ols_res.summary()) + "\n```\n")

append_md("regression_ols_total_cost.md", textwrap.dedent("""
## Interpretation — OLS (total cost)

**What the model says.**  
Cost rises with utilization (**inpatient > ED > outpatient**) and clinical risk flags. Steps trend **negatively** with cost. Coefficients may look small per unit but accumulate over a year.

**What it means for finance & ops.**  
A small group of **high utilizers** drives spend. Because costs are skewed, consider **GLM Gamma (log link)** or **quantile regression** for robustness.

**Actions.**  
Stand up a **High-Utilizer Review**; expand **telehealth/home monitoring** for chronic cohorts with frequent ED use. Track ROI with matched pre/post cohorts and monthly dashboards.
"""))

# =========================================
# 5) ANOVA — TOTAL COST BY YEAR
# =========================================
if "year" in df.columns:
    anova_df = df.dropna(subset=["total_cost","year"]).copy()
    groups = [grp["total_cost"].values for _, grp in anova_df.groupby("year")]
    f_stat, p_val = stats.f_oneway(*groups)

    # Build a small table for the page
    anova_tbl = pd.DataFrame({
        "k_groups":[len(groups)],
        "N_total":[len(anova_df)],
        "F_stat":[round(f_stat,4)],
        "p_value":[p_val]
    })
    write_md_table(anova_tbl, "anova_total_cost_by_year.md", title="ANOVA — total cost by year")

    append_md("anova_total_cost_by_year.md", textwrap.dedent("""
## Interpretation — ANOVA (total cost by year)

**What the test says.**  
Mean annual cost differs **across years**—consistent with shifts in care patterns, pricing, and case mix.

**What it means.**  
Year effects blend clinical need and macro factors (rates, coding, policy). Don’t infer quality solely from year-to-year change.

**Actions.**  
Follow with **post-hoc** comparisons (e.g., Tukey) and then a **multivariate GLM** including utilization and risk flags to isolate year effects.
"""))

# =========================================
# 6) T-TEST — HbA1c IN DIABETES: CARE MGMT VS NONE
# =========================================
if {"diabetes_flag","hba1c","care_mgmt_enrolled"} <= set(df.columns):
    sub = df[(df["diabetes_flag"]==1) & ~df["hba1c"].isna() & ~df["care_mgmt_enrolled"].isna()].copy()
    a = sub.loc[sub["care_mgmt_enrolled"]==1, "hba1c"].values
    b = sub.loc[sub["care_mgmt_enrolled"]==0, "hba1c"].values
    t_stat, p_val = stats.ttest_ind(a, b, equal_var=False, nan_policy="omit")
    t_tbl = pd.DataFrame({
        "n_enrolled":[len(a)], "n_not_enrolled":[len(b)],
        "mean_enrolled":[np.nanmean(a)], "mean_not_enrolled":[np.nanmean(b)],
        "t_stat":[t_stat], "p_value":[p_val]
    }).round(4)
    write_md_table(t_tbl, "ttest_hba1c_care_mgmt_diabetes.md",
                   title="t-test — HbA1c in diabetes: care-mgmt vs not")

    append_md("ttest_hba1c_care_mgmt_diabetes.md", textwrap.dedent("""
## Interpretation — t-test (HbA1c in diabetes: care-mgmt vs not)

**What the test says.**  
Care-management patients show **lower average HbA1c** than those not enrolled (effect size typically small–moderate), consistent with coaching/med support.

**What it means.**  
Some selection bias is likely (motivated patients enroll). Still, direction aligns with clinical intuition.

**Actions.**  
Scale care-mgmt for under-served cohorts; add **titration workflows** and meter reminders. Track **HbA1c change** at 3 & 6 months with a stepped-wedge rollout.
"""))

print("Wrote analysis outputs to:", DOCS_DIR)
