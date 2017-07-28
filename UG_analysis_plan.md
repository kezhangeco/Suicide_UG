# UG analysis plan 

### Hypothesis 1: Participants in all groups punished their counterparts for unfair offer. However, low-lethality attempters, non-suicidal depression, ideators, and controls punished less as the cost of punishment increased, accepting more unfair offers as the stakes grew large. High-lethality attempters did not adjust their choices based on stake magnitude, punishing unfair offers without regard to the cost.

#### Binary logistic generalized mixed model (GLMM)

- Examines the acceptance of offer in HL attempters and other groups
- Nest each trials of binary values to the model

#### Multilevel structural equation modeling (MLSEM)

- examine effects of potential intervening variables (sensitivity of unfairness)
- We only included the eight moderately equitable and eight very unequitable trials in these analyses, as variance in rejection rates of the fair (equitable) trials was minimal

### Hypothesis 2: Groups have different judgment or sensitivity to fairness. It may explain a large proportion of the difference in acceptance. High-lethality attempters judged offers based on the inequality. The comparison groups judged offers based on the combination of inequality and magnitudes.



### data clean

1. Exclude those age under 50
2. group ideator-attempters as attempters

### data description

1. Demographic, clinical, and SES indicators, those continuous measure  are compared across the 5 groups by ANOVA.

   **groups:**

   - CONTROL-CONTROL
   - DEPRESSION-DEPRESSION(non-suicidal)
   - SUICIDAL-IDEATOR
   - SUICIDAL-ATTEMPTER: HL, LL
     - HL>=4
     - LL<4

   **Demographic and SES:**

   - age
   - education
   - gender (% men)
   - race(% white) 
   - marital status

   **Clinical:**

   - sensitivity to fairness

2. Categorical data are compared by chi-square tests across the groups (if there's any categorical data)

3. Percentage of acceptance:

   1) calculate the percentage of acceptance of unfair offer in aggregate level

   2) calculate the percentage of acceptance of unfair offer by groups





