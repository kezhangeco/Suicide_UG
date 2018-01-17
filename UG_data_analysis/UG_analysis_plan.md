

# UG analysis plan 

### **Hypothesis 1**: Participants in all groups punished their counterparts for unfair offer. However, low-lethality attempters, non-suicidal depression, ideators, and controls punished less as the cost of punishment increased, accepting more unfair offers as the stakes grew large. High-lethality attempters did not adjust their choices based on stake magnitude, punishing unfair offers without regard to the cost.

#### Binary logistic generalized mixed model (GLMM)

- Examines the acceptance of offer in HL attempters and other groups
- Nest each trials of binary values to the model

#### Multilevel structural equation modeling (MLSEM)

- examine effects of potential intervening variables (sensitivity of unfairness)
- We only included the eight moderately equitable and eight very unequitable trials in these analyses, as variance in rejection rates of the fair (equitable) trials was minimal

### **Hypothesis 2**: Groups have different judgment or sensitivity to fairness. It may explain a large proportion of the difference in acceptance. High-lethality attempters judged offers based on the inequality. The comparison groups judged offers based on the combination of inequality and magnitudes.



## Data clean:

1. One person changed from LL attempter to ideator
2. Exclude those age under 50
3. group ideator-attempters as attempters

Steps: 

1. Merge context, baseline data into 1 panel sheet ('data_collapse.py').

2. add participants type into task spreadsheet

3. reorder trial number: baseline 1-26, context from 27 on

4. identify whether trials are fair or unfair: fair = 5-5, 6-4; unfair = others (fairness_describe.py)

   ​

   ​

##Data description:

1. Demographic, clinical, and SES indicators, those continuous measure  are compared across the 4/5 groups by ANOVA.

   **groups:**

   - CONTROL-CONTROL
   - DEPRESSION-DEPRESSION(non-suicidal)
   - SUICIDAL-IDEATOR
   - SUICIDAL-ATTEMPTER: HL, LL
     - HL>=4 (max lethality)
     - LL<4

   **Demographic and SES:**

   - age
   - education
   - gender (% men)
   - race(% white) 
   - marital status

   **Clinical:**

   - rest of variables in the questionnaires

2. Categorical data are compared by chi-square tests across the groups: gender & race

3. ANOVA test:

   - Depression variables tested without controls:
     - HRSD NO SUI
     - SSI BL CURRENT
     - DEP ONSET AGE
   - Variables tested only with attempters:
     - AGE AT FIRST ATTEMPT
     - SIS ML TOTAL
     - SIS ML PLAN

4. Fairness description

   - how each group accept fairness offer under different reappraisal condition: baseline, punish, empathy. 



# GLMM 

- **Goal**: whether suicide attempters responded differently to unfaireness and stake during UG.
- Binary logistic generalized mixed model (GLMM)
- Parameter estimates were derived using MLE based on adaptive Gauss-Hermite quadrature rule.

## Research question

what types of context and groups influence one's offer acceptance?

##Hypotheses:

1. social context influence offer acceptance
2. psychiatric group influence offer acceptance, after controlling for social context
3. psychiatric group moderates the social context-offer acceptance relationship. 



## Model hierarchy

###HLM1

| Level   | Hierarchy    | variables                   |
| ------- | ------------ | --------------------------- |
| Level 2 | Participants | Participants Type(clinical) |
|         |              | **age***                    |
|         |              | **Depression(HRSD NO SUI)** |
|         |              | **Household Income***       |
|         |              | **Cognitive ability(DRS)**  |
|         |              | **Gender**                  |
|         |              | **Race**                    |
|         |              | **marriage**                |
|         |              | **MMSE**                    |
|         |              | **Education**               |
|         |              |                             |
|         |              |                             |
|         |              |                             |
| Level 1 | Trials       | Trial number                |
|         |              | total stake size            |
|         |              | Fairness ratio              |
|         |              | Social framing context      |
|         |              |                             |
|         |              | **Offer Acceptance (DV)**   |

### HLM2

| Level   | Hierarchy    | Variables                   |
| ------- | ------------ | --------------------------- |
| Level 3 | Participants | Participants Type(clinical) |
|         |              | age*                        |
|         |              | Depression(HRSD NO SUI)     |
|         |              | Household Income*           |
|         |              | Cognitive ability(DRS)      |
|         |              | Gender                      |
|         |              | Race                        |
|         |              | MMSE                        |
|         |              | Education                   |
|         |              | marriage                    |
| Level 2 | Framing      | Social context              |
| Level 1 | Trials       | Fairness ratio              |
|         |              | total stake size            |
|         |              | **Offer Acceptance (DV)**   |



##Alternative models

1. **Manipulate social framing context**:

   Only input "empathy" and "punish" context, and excludes "Baseline" into the model. To see if timing matters in offer acceptance. Because baseline always the first, then empathy and punish are randomized, the order of the trials may influence the behaviour. 

2. **Manipulate participant type**:

   Remove "controls". Look at how the variable of depression influence the offer acceptance. It is meaningless to leave controls in the group. 

3. **Longitudinal model:**

   Add "ReappraisalDirection" as the "time" variable. Whether the framing treatment leads to different acceptance than the baseline.

   - "Baseline": $T$ = 0

   - "punish" & "empathy": $T$ = 1

   - $T_{it}$: dedicated time predictor; $X_{it}$: time-varying predictors (level 1 variables); $Z_{i}$: time-invariant predictors (level 2 variables)

   - $$
     Level\ 1:\,Y_{it} = \pi_{0i} + \pi_{1i}(T_{it}) + \pi_{2i}(X_{it}) +\epsilon_{it} \\
     \pi_{0i} = \beta_{00} + \beta_{01} (Z_i) + r_{0i}\\
     $$

     $$
     Level\ 2:\, \pi_{1i} = \beta_{10} + r_{1i} \\
     \pi_{2i} = \beta_{20} + r_{2i}
     $$

     ​


## Steps in R

### 1. Intraclass correlation (ICC)

- Determine if multi-level modeling is the correct choice for our analysis.
- The ICC measures the degree of clustering in our data and answers the question, “How much does my Level 2 predict the total variance of my study?” If your ICC is greater than 0, you have a multi-level study.

### 2. Test continous IVs correlation

Prepare for potential collinearity

### 3. Handle with categorical IVs

- Encode "control" as the comparison group
- Fairness_score <- as.factor(Fairness_score): emphasize it is a categorical rather than a continuous IV.


### 4. Test collinearity

### 5. Choose global models and run

### 6. Test model fit

### 7. Model selection

use model averaging.

### 8. Final model assumption




# MLSEM



- Goal: whether the effect of stake on acceptance was influenced by income, implusivity, exective control, interpersonal dysfunction.
- Each participant contribute 16 trials.
- decomposes the data into within-subject and between-subjects components, allow models for each level.






  
