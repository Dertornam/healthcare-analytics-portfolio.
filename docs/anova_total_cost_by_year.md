<h1>ANOVA — total cost by year</h1>
<div style='max-width:100%; overflow-x:auto; padding:6px; border:1px solid #e5e7eb; border-radius:8px;'>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>k_groups</th>
      <th>N_total</th>
      <th>F_stat</th>
      <th>p_value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>10</td>
      <td>30000</td>
      <td>8.2567</td>
      <td>2.245662e-12</td>
    </tr>
  </tbody>
</table>
</div>
## Interpretation — ANOVA (total cost by year)

**What the test says.**  
Mean annual cost differs **across years**—consistent with shifts in care patterns, pricing, and case mix.

**What it means.**  
Year effects blend clinical need and macro factors (rates, coding, policy). Don’t infer quality solely from year-to-year change.

**Actions.**  
Follow with **post-hoc** comparisons (e.g., Tukey) and then a **multivariate GLM** including utilization and risk flags to isolate year effects.
