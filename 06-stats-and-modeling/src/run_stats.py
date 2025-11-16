# Re-create figures and tables from the CSV in docs/
import os, pandas as pd, numpy as np, matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm
from scipy import stats

HERE = os.path.dirname(__file__)
docs = os.path.abspath(os.path.join(HERE, "../../docs"))
figs = os.path.join(docs, "figs")
os.makedirs(figs, exist_ok=True)
csv_path = os.path.join(docs, "healthcare_2015_2024_patient_year.csv")
df = pd.read_csv(csv_path)

def save_fig(p):
    plt.tight_layout(); plt.savefig(p, dpi=160, bbox_inches="tight"); plt.close()

agg = df.groupby("year").agg(
    admissions=("inpatient_admissions", "sum"),
    ed_visits=("ed_visits","sum"),
    mean_hba1c=("hba1c","mean"),
    readmit_rate=("any_30d_readmit","mean"),
    total_cost=("total_cost","sum"),
).reset_index()

plt.figure(figsize=(9,5)); plt.plot(agg['year'], agg['admissions'], marker='o')
plt.title('Inpatient admissions, 2015–2024'); plt.xlabel('Year'); plt.ylabel('Admissions')
save_fig(os.path.join(figs,'admissions_trend.png'))

plt.figure(figsize=(9,5)); plt.plot(agg['year'], agg['ed_visits'], marker='o')
plt.title('ED visits, 2015–2024'); plt.xlabel('Year'); plt.ylabel('ED visits')
save_fig(os.path.join(figs,'ed_visits_trend.png'))

plt.figure(figsize=(9,5)); plt.plot(agg['year'], agg['mean_hba1c'], marker='o')
plt.title('Average HbA1c, 2015–2024'); plt.xlabel('Year'); plt.ylabel('HbA1c')
save_fig(os.path.join(figs,'hba1c_trend.png'))

plt.figure(figsize=(9,5)); plt.plot(agg['year'], agg['readmit_rate'], marker='o')
plt.title('30-day readmission rate, 2015–2024'); plt.xlabel('Year'); plt.ylabel('Readmission rate')
save_fig(os.path.join(figs,'readmit_rate_trend.png'))

plt.figure(figsize=(9,5)); plt.plot(agg['year'], agg['total_cost'], marker='o')
plt.title('Total cost (sum), 2015–2024'); plt.xlabel('Year'); plt.ylabel('Total cost')
save_fig(os.path.join(figs,'total_cost_trend.png'))

plt.figure(figsize=(9,5))
groups = [g['total_cost'].values for _, g in df.groupby('insurance_type')]
plt.boxplot(groups, labels=[k for k,_ in df.groupby('insurance_type')])
plt.title('Total cost by insurance type'); plt.xlabel('Insurance type'); plt.ylabel('Total cost')
save_fig(os.path.join(figs,'cost_by_insurance.png'))

plt.figure(figsize=(9,5))
plt.scatter(df['wearable_steps_avg'], df['total_cost'], alpha=0.5)
plt.title('Wearable steps vs total cost'); plt.xlabel('Avg steps'); plt.ylabel('Total cost')
save_fig(os.path.join(figs,'steps_vs_cost.png'))

bins = pd.cut(df['hba1c'], bins=10); prob = df.groupby(bins)['any_30d_readmit'].mean()
centers = [c.mid for c in prob.index.categories]
plt.figure(figsize=(9,5)); plt.plot(centers, prob.values, marker='o')
plt.title('HbA1c vs readmission rate'); plt.xlabel('HbA1c (binned)'); plt.ylabel('Readmission rate')
save_fig(os.path.join(figs,'hba1c_vs_readmit.png'))

num = df.select_dtypes(include=[np.number]).drop(columns=['patient_id'], errors='ignore')
# --- Descriptives (nice table) ---
desc = num.describe().T
desc.to_csv(os.path.join(docs, 'desc_stats.csv'))
with open(os.path.join(docs, 'desc_stats.md'), 'w') as f:
    f.write("# Descriptive statistics\n\n")
    f.write(desc.round(3).to_markdown())
    f.write("\n")

# --- Correlation matrix (nice table) ---
corr = num.corr()
corr.to_csv(os.path.join(docs, 'corr_matrix.csv'))
with open(os.path.join(docs, 'corr_matrix.md'), 'w') as f:
    f.write("# Correlation matrix\n\n")
    f.write(corr.round(3).to_markdown())
    f.write("\n")
num.describe().T.to_csv(os.path.join(docs,'desc_stats.csv'))
num.corr().to_csv(os.path.join(docs,'corr_matrix.csv'))

plt.figure(figsize=(10,8)); c = num.corr()
plt.imshow(c, interpolation='nearest'); plt.xticks(range(len(c.columns)), c.columns, rotation=90)
plt.yticks(range(len(c.columns)), c.columns); plt.colorbar(); plt.title('Correlation heatmap')
save_fig(os.path.join(docs,'corr_heatmap.png'))

log_vars = ['age','diabetes_flag','heart_failure_flag','copd_flag','bmi','hba1c','outpatient_visits','ed_visits','inpatient_admissions','care_mgmt_enrolled','wearable_steps_avg','genai_triage_flag','high_risk_flag']
m = df.dropna(subset=['any_30d_readmit']+log_vars).copy()
y = m['any_30d_readmit']; X = sm.add_constant(m[log_vars])
log_summary = sm.Logit(y, X).fit(disp=False).summary().as_text()
open(os.path.join(docs,'regression_logit_readmission.md'),'w').write(log_summary)

ols_vars = log_vars
m2 = df.dropna(subset=['total_cost']+ols_vars).copy()
y2 = m2['total_cost']; X2 = sm.add_constant(m2[ols_vars])
ols_summary = sm.OLS(y2,X2).fit().summary().as_text()
open(os.path.join(docs,'regression_ols_total_cost.md'),'w').write(ols_summary)

anova_table = anova_lm(ols('total_cost ~ C(insurance_type)', data=df).fit())
anova_table.to_csv(os.path.join(docs,'anova_total_cost_by_insurance.csv'))

sub = df[df['diabetes_flag']==1]
g1 = sub[sub['care_mgmt_enrolled']==1]['hba1c'].dropna()
g0 = sub[sub['care_mgmt_enrolled']==0]['hba1c'].dropna()
t,p = stats.ttest_ind(g1,g0, equal_var=False)
open(os.path.join(docs,'ttest_hba1c_care_mgmt_diabetes.md'),'w').write(f't={{t:.3f}}, p={{p:.3g}}, n1={{len(g1)}}, n0={{len(g0)}}')
