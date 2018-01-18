library(Matrix)
library(rJava)
library(lme4)
library(ggplot2)
library(GGally)
library(plyr)
library(readxl)
library(reshape2)
library(numDeriv)
library(MuMIn)
library(glmulti)

# import data
task <- read.csv("/home/kzhang5/scratch/cedar/interactive/ug_all_task_data.csv")
demo <- read_excel("/home/kzhang5/scratch/cedar/interactive/ug_demog.xlsx")
question <- read_excel("/home/kzhang5/scratch/cedar/interactive/ug_questionnaire.xlsx")

demoQuestion <- merge(demo, question, on = "ID")
allData <- merge(task, demoQuestion, on = "ID")
allData$totalStake <- allData$PlayerProposedAmount + allData$OpponentProposedAmount
allData <- rename(allData, c("HOUSEHOLD INCOME" = "HouseholdIncome", "HRSD NO SUI" = "HRSD_NO_SUI", "PER CAPITA INCOME" = "IncomePerCapita", "MMSE TOTAL" = "MMSE", "UPPSP NEG URGENCY" = "urgency"))
question <- rename(question, c("UPPSP NEG URGENCY" = "urgency"))
allData$Fairness_score <- as.factor(allData$Fairness_score)
allData$ID <- as.factor(allData$ID)
allData$AcceptOffer <- as.factor(allData$AcceptOffer)

# predictors:- Reappraisal Direction
## - total stake
## - Fairness score
## - clinical groups
## - education
## - household income
## - EXIT (4 missing values)
## - trial number (within block number)
## - block number
## - an impulsivity measure: BIS_NONPLAN (3 missing values)
## - an interpersonal function measure: IIP15INTAMBV (4 missing values)

# complete missing values
# check how many percentage of data is missing in the question dataframe
pMiss <- function(x){sum(is.na(x))/length(x)*100}
missingVar <- c('ID', 'BIS_NONPLAN', 'IIP15INTAMBV', 'EXIT', 'urgency')
missingDF <- question[, missingVar]
apply(question[missingVar], 2, pMiss)
print(md.pattern(question[missingVar]))

# impute data
missingDF_impute <- mice(missingDF, m = 5, meth = "pmm", maxit = 50)
print(summary(missingDF_impute))
missingVar_complete <- complete(missingDF_impute,1)

# merge the generated values to the df
missingVar_complete <- rename(missingVar_complete, c("BIS_NONPLAN" = "BIS_NONPLAN_full", "IIP15INTAMBV" = "IIP15INTAMBV_full", "EXIT" = "EXIT_full", "urgency" = "urgency_full"))
allData <- merge(allData, missingVar_complete, by = "ID")


# Level 1 model
## Random intercept and fixed slopes with random effect (1|ID)
m1 <- glmulti(allData$AcceptOffer ~ ReappraisalDirection * scale(totalStake) * Fairness_score, level = 1, fitfunction = glmer.glmulti, random = "+ (1|ID)", method = "g", data = allData, confsetsize = 8)

summary(m1)
# look at the models
m1_models <- weightable(m1)
m1_models <- m1_models[m1_models$aicc <= min(m1_models$aicc) + 2,]


# Level 1 model with $group$ predictor
#4 way interaction effect, and see if the model is significant. If not, drop this interaction
m2_4interaction <- glmer(allData$AcceptOffer ~ ReappraisalDirection * scale(totalStake) * Fairness_score * group4 + (1|ID), data = allData, family = binomial)

summary(m2_4interaction)

# Screening all alternative models of the level 1 + group models
m2 <- glmulti(allData$AcceptOffer ~ ReappraisalDirection * scale(totalStake) * Fairness_score * group4, level = 2, fitfunction = glmer.glmulti, random = "+ (1|ID)", method = "g", data = allData)

m2_1 <- glmulti(allData$AcceptOffer ~ ReappraisalDirection * scale(totalStake) * Fairness_score * group5, level = 2, fitfunction = glmer.glmulti, random = "+ (1|ID)", method = "g", data = allData)

# Correlation matrix of demographics

corrMatrix <- ggpairs(demoQuestion[, c("IncomePerCapita", "HRSD NO SUI", "DRS", "EDUCATION", "EXIT", "BIS_NONPLAN", "urgency", IIP15INTAMBV)])

save.image("basicModel.RData")
