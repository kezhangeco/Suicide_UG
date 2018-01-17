library(lme4)
library(ggplot2)
library(GGally)
library(plyr)
library(Matrix)
library(readxl)
library(reshape2)
library(numDeriv)
library(MuMIn)
library(glmulti)
library(rJava)

# import data
task <- read.csv("/home/kzhang5/scratch/ug_all_task_data.csv")
demo <- read_excel("/home/kzhang5/scratch/ug_demog.xlsx")
question <- read_excel("/home/kzhang5/scratch/ug_questionnaire.xlsx")

demoQuestion <- merge(demo, question, on = "ID")
allData <- merge(task, demoQuestion, on = "ID")
allData$totalStake <- allData$PlayerProposedAmount + allData$OpponentProposedAmount
allData <- rename(allData, c("HOUSEHOLD INCOME" = "HouseholdIncome", "HRSD NO SUI" = "HRSD_NO_SUI", "PER CAPITA INCOME" = "IncomePerCapita", "MMSE TOTAL" = "MMSE"))
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

# non interaction effect 

