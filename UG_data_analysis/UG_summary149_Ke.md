# Main results

## How does $group$ interact with $fairness$, $total\, stake$, and $reappraisal\, direction$?

$$AcceptOffer = ReappraisalDirection * scale(fairLR) * scale(totalStake) + \\ReappraisalDirection * group4 + scale(fairLR) * group4 + scale(totalStake) * \\group4 + (1 | ID/block)$$

**The reference is $baseline$, $attempter$, and $attempterHL$.**

 ```*p<0.1; **p<0.05; ***p<0.01```

1. Main effect:

   - ReappraisalDirectionempathy                                          0.883***          
   - ReappraisalDirectionpunish                                             -1.814***         
   - scale(fairLR)                                                                          2.099***        
   - Participants accept more offers under empathy, and fewer under punishment, compared to baseline context.
   - The fairer offers, the more acceptance.  

2. $fairness * group$

   - scale(fairLR):group4depression                                        -0.169**   

   - As the offers are getting fairer, the depression becomes less likely to accept offers compared to the attempter.   

     ​                              ![Gfair*group](/Volumes/LAB/Suicide_UG/UG_data_analysis/outputs/main/NoIndividual/UGfair*group4.jpg)     

3. $ReappraisalDirection * group$

   - ReappraisalDirectionempathy:group4control                 0.850**   

   - Compared to the attempter, the control has a higher increasing tendency to accept offers under empathy relative to baseline.

     ![Gcontext*group](/Volumes/LAB/Suicide_UG/UG_data_analysis/outputs/main/NoIndividual/UGcontext*group4.jpg)

4. $total \, stake * group$

   - No interaction

     ![Gstake*group](/Volumes/LAB/Suicide_UG/UG_data_analysis/outputs/main/NoIndividual/UGstake*group4.jpg)

5. $ReappraisalDirection * fairness$

   - ReappraisalDirectionempathy:scale(fairLR)                      -1.275***         
   - ReappraisalDirectionpunish:scale(fairLR)                          -1.245***         

6. $ReappraisalDirection * totalStake$

   - ReappraisalDirectionpunish:scale(totalStake)                   0.191***          

7. $fairness * total\,stake$

   - scale(fairLR):scale(totalStake)                                                -0.136**       


​               

# Punishment Type

## How does the specific punishment type $resources$ and $reputation$ influence offer acceptance across groups?

$$AcceptOffer = AcceptOffer lag + ReappraisalDirectionResourcesRep * scale(fairLR) + \\ReappraisalDirectionResourcesRep * scale(totalStake) + ReappraisalDirectionResourcesRep *$$
  $$group4 + scale(fairLR) * group4 + (1 | ID/block)$$

**Reappraisal Direction:** $baseline, empathy, reputation, resources$

**Reference:** $basline, attempter$

1. Main effect:

   - ReappraisalDirectionResourcesRepempathy                               0.928***          
   - ReappraisalDirectionResourcesRepreputation                            -2.931***         
   - ReappraisalDirectionResourcesRepresources                             -0.504**      
   - scale(fairLR)                                                                                        2.089***  
   - Participants accept more offers under empathy, and fewer offers under resources and reputation relative to baseline.
   - The fairer offers, the more acceptance.             

2. $punishType * group$

   - ReappraisalDirectionResourcesRepempathy:group4control                 1.027***          

   - ReappraisalDirectionResourcesRepempathy:group4ideator                  0.917**   

   - Compared to the attempter, the increasing likelihood of accepting offers under empathy from baseline is higher in the control and ideator.

     ![roup4*Pu](/Volumes/LAB/Suicide_UG/UG_data_analysis/outputs/punishType/NoIndividual/group4*Pun.jpg)       

3. $fairness * group$

   - scale(fairLR):group4ideator                                                                           0.236**   

   - The ideator has higher increase in the tendency of acceptance as the offers are getting fairer, compared to the attempter.

     ![roup4*fai](/Volumes/LAB/Suicide_UG/UG_data_analysis/outputs/punishType/NoIndividual/group4*fair.jpg)       

4. $total\, stake * group$

   - No interaction

5. $punishType * fairness$

   - ReappraisalDirectionResourcesRepempathy:scale(fairLR)                 -1.256***         
   - ReappraisalDirectionResourcesRepreputation:scale(fairLR)              -1.226***         
   - ReappraisalDirectionResourcesRepresources:scale(fairLR)               -0.825***       

6. $punishType * total\,stake$

   - No interaction

   ​

# Emotional reactivity

## How emotionally reactive a group is under $punish$ and $empathy$ context?

$$scale(Rating) = PunishingType*group4 + (1|ID)$$ 

**Post survey: unfairness, sympathy, anger.**

#### Unfairness survey

$Reappraisal Direction: empathy, punish (reputation, resources)$

1. No main effect

2. $UG\, context * group$

   - 3 types: $empathy, reputation, resources$ 
     - PunishingTypereputation:group4control          -0.691***        
     - PunishingTyperesources:group4control           -0.440**    
     - PunishingTypereputation:group4ideator          -0.535***   
     - Compared to the attempter, the control becomes less likely to accept offers under punishment (resources and reputation) relative to empathy context.    
     - Compared to the attempter, the ideator becomes less likely to accept offers under reputation context relative to empathy context.     

   - 2 types: $empathy, punish$

     - ReappraisalDirectionpunish:group4control      -0.582***    

     ![1fairnes](/Volumes/LAB/Suicide_UG/UG_data_analysis/outputs/reactivity/NoIndividual/Q1fairness.jpg)

     ![fairnes](/Volumes/LAB/Suicide_UG/UG_data_analysis/outputs/reactivity/NoIndividual/Qfairness.jpg)

#### Sympathy survey 

1. Main effect:

   - 3 types
     - PunishingTypereputation                         -1.383 *** 
     - PunishingTyperesources                          -1.318 ***    
   - 2 types
     - ReappraisalDirectionpunish                   -1.355***    
     - Participants are less sympathetic under punishment context, in both reputation and resources.  

2. No interaction

   ![1sympath](/Volumes/LAB/Suicide_UG/UG_data_analysis/outputs/reactivity/NoIndividual/Q1sympathy.jpg)

   ![sympath](/Volumes/LAB/Suicide_UG/UG_data_analysis/outputs/reactivity/NoIndividual/Qsympathy.jpg)

#### Anger survey

1. Main effect:

   - 3 types
     - PunishingTypereputation                       1.663*** 
     - PunishingTyperesources                         0.520*** 
   - 2 types
     - ReappraisalDirectionpunish                   1.176***    
     - Participants have more anger under punishment context, in both reputation and resources.

2. No interaction effect

   ![1ange](/Volumes/LAB/Suicide_UG/UG_data_analysis/outputs/reactivity/NoIndividual/Q1anger.jpg)

   ![ange](/Volumes/LAB/Suicide_UG/UG_data_analysis/outputs/reactivity/NoIndividual/Qanger.jpg)





