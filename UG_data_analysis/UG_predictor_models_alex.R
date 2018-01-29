## general predictor script
load(file = "~/code/Suicide_UG/UG1.Rdata")
setwd("~/code/Suicide_UG/predictor_plots")

# vars <- c("NEUROTICISM","EXTRAVERSION" , "CONSCIENTIOUSNESS", "AGREEABLENESS", "OPENNESS", "PAIBOR TOTAL" , "WTARSS", "EXIT_full", "IIP15AGRESS","IIP15INTAMBV", "IIP15INTSEN"  )
vars <- c( "Anxiety Lifetime" , "Substance Lifetime" ,"ARSTOTAL" ,"BIS_NONPLAN" ,"HouseholdIncome", 
           "IRI_EMPATHETIC_CONCERN" ,"IRI_FANTASY_SCALE",  "IRI_PERSONAL_DISTRESS","IRI_PERSPECTIVE_TAKING",
           "UPPSP LACK OF PERSEV" ,  "UPPSP LACK OF PREMED" ,  "urgency"  , "UPPSP POS URGENCY",
           "isela", "iselb", "iselse", "iselt")

for(i in 1:length(vars))
{varname <- vars[i]
print(varname)
allData$predictor <- as.numeric(as.matrix(allData[,varname]))

# control for ed
m_pred <-
  glmer(
    allData$AcceptOffer ~ ReappraisalDirection * scale(fairLR) * scale(totalStake) + ReappraisalDirection *
      group4 + scale(fairLR) * group4 + scale(totalStake) * group4 + 
      ReappraisalDirection*scale(predictor) + (1 |
                                                 ID/block),
    family = binomial,
    data = allData,
    nAGQ = 0,  
    control = glmerControl(optimizer = "bobyqa"))
summary(m_pred)
car::Anova(m_pred)
q <- quantile(allData$predictor, na.rm = TRUE,probs = seq(0,1,0.1))
filename <- paste0(varname,"_context_UG.pdf")
pdf(file = filename,width = 12, height = 6)
lsm <- lsmeans(m_pred, "ReappraisalDirection", by = "predictor", at = list(predictor = c(q[2],q[6],q[10])))
print(plot(lsm, horiz = F))
dev.off()
}
