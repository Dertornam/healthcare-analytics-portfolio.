# ANOVA — total cost by year

|    |   k_groups |   N_total |   F_stat |     p_value |
|---:|-----------:|----------:|---------:|------------:|
|  0 |         10 |     30000 |   8.2567 | 2.24566e-12 |


## Interpretation — ANOVA (total cost by year)

**What the test says.**  
Mean annual cost differs **across years**—consistent with shifts in care patterns, pricing, and case mix.

**What it means.**  
Year effects blend clinical need and macro factors (rates, coding, policy). Don’t infer quality solely from year-to-year change.

**Actions.**  
Follow with **post-hoc** comparisons (e.g., Tukey) and then a **multivariate GLM** including utilization and risk flags to isolate year effects.
