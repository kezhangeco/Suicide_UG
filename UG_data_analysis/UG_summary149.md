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

     ​                              ![Gfair*group](https://ws1.sinaimg.cn/large/006tKfTcgy1fpreoxxm1wj30dc0dcq3i.jpg)     

3. $ReappraisalDirection * group$

   - ReappraisalDirectionempathy:group4control                 0.850**   

   - Compared to the attempter, the control has a higher increasing tendency to accept offers under empathy relative to baseline.

     ![Gcontext*group](https://ws1.sinaimg.cn/large/006tKfTcgy1fprep2cy68j30dc0dcmxv.jpg)

4. $total \, stake * group$

   - No interaction

     ![Gstake*group](https://ws3.sinaimg.cn/large/006tKfTcgy1fprep4jp4wj30dc0dcmxv.jpg)

5. $ReappraisalDirection * fairness$

   - ReappraisalDirectionempathy:scale(fairLR)                      -1.275***         
   - ReappraisalDirectionpunish:scale(fairLR)                          -1.245***         

6. $ReappraisalDirection * totalStake$

   - ReappraisalDirectionpunish:scale(totalStake)                   0.191***          

7. $fairness * total\,stake$

   - scale(fairLR):scale(totalStake)                                                -0.136**       



   

## Whether the interaction of $fairness*total\,stake*group5$ exists? A replication of the previous study.

$$AcceptOffer = ReappraisalDirection * scale(fairLR) * scale(totalStake) + ReappraisalDirection * group5 + \\scale(fairLR) * group5 + scale(totalStake) * group5 + scale(fairLR) * scale(totalStake) * group5 + \\(1 | ID/block)$$

1. Main effect

   - ​

2. $ReappraisalDirection * group$

   - ​                                          

3. $fairness * group$

4. $total\, stake * group$

   - ​

     ​                 

     ​

5. $fairness * total\, stake * group$

   - ​

#### Comparison with the previous study

- The previous study shows $group * magnitude$ interaction. The control, depression, attempterLL accepted fewer high stake size offers. T
- The previous study did not find $fairness*magnitude$ and $fairness*magnitude*group$ interaction. The current study does not find $fairness*magnitude$, but $fairness*magnitude*group$. 

## Individual characteristics on the offer acceptance.

### MMSE $(MMSE *Reappraisal\,Direction)$

 

### IRI_EMPATHETIC_CONCERN $(IRI\,EMPATHETIC\,CONCERN*Reappraisal\,Direction*group)$

1. ​

### IIP15INTSEN $(IIP15INTSEN*Reappraisal\,Direction*group)$



### IIP15AGRESS$(IIP15AGRESS *Reappraisal\,Direction*group4)$



### Gender ($Reappraisal\,Direction*gender$)

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

     ![roup4*Pu](https://ws1.sinaimg.cn/large/006tKfTcgy1fprep5blrlj30dc0dct9i.jpg)       

3. $fairness * group$

   - scale(fairLR):group4ideator                                                                           0.236**   

   - The ideator has higher increase in the tendency of acceptance as the offers are getting fairer, compared to the attempter.

     ![roup4*fai](https://ws3.sinaimg.cn/large/006tKfTcgy1fprepbjskaj30dc0dcjrx.jpg)       

4. $total\, stake * group$

   - No interaction

5. $punishType * fairness$

   - ReappraisalDirectionResourcesRepempathy:scale(fairLR)                 -1.256***         
   - ReappraisalDirectionResourcesRepreputation:scale(fairLR)              -1.226***         
   - ReappraisalDirectionResourcesRepresources:scale(fairLR)               -0.825***       

6. $punishType * total\,stake$

   - No interaction

   ​

## Individual Characterstics

### Education($ punishType*education$)



### Gender ($ punishType*gender$)



### MMSE($ punishType*MMSE$)







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

     ![1fairnes](https://ws4.sinaimg.cn/large/006tKfTcgy1fprepdx7q2j30dc0dcjrx.jpg)

     ![fairnes](https://ws4.sinaimg.cn/large/006tKfTcgy1fprepg5oixj30dc0dcgmb.jpg)

#### Sympathy survey 

1. Main effect:

   - 3 types
     - PunishingTypereputation                         -1.383 *** 
     - PunishingTyperesources                          -1.318 ***    
   - 2 types
     - ReappraisalDirectionpunish                   -1.355***    
     - Participants are less sympathetic under punishment context, in both reputation and resources.  

2. No interaction

   ![1sympath](https://ws4.sinaimg.cn/large/006tKfTcgy1fpreph9oh2j30dc0dcwf4.jpg)

   ![sympath](https://ws1.sinaimg.cn/large/006tKfTcgy1fprepkrftmj30dc0dcaap.jpg)

#### Anger survey

1. Main effect:

   - 3 types
     - PunishingTypereputation                       1.663*** 
     - PunishingTyperesources                         0.520*** 
   - 2 types
     - ReappraisalDirectionpunish                   1.176***    
     - Participants have more anger under punishment context, in both reputation and resources.

2. No interaction effect

   ![1ange](https://ws3.sinaimg.cn/large/006tKfTcgy1fprepm6hquj30dc0dcdgd.jpg)

   ![ange](https://ws3.sinaimg.cn/large/006tKfTcgy1fprepmr8m3j30dc0dcdgh.jpg)





