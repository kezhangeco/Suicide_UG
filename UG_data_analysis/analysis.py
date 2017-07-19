import pandas as pd
import numpy as np


df = pd.read_csv("/Users/kezhang/ownCloud/Suicide_UG/UG_clean_data/all_data.csv", dtype={'Fairness_score': int})
print(df.dtypes)
def main_fairness():
    #check the main effect of fairness, whether people accept more fair offer.
    #5 levels of fairness for the offers (1 = 50/50; 2 = 60/40; 3 = 70/30; 4 = 8/2; 5 = 90/10);
    #fair = 5-5, 6-4;
    #unfair = 7-3, 8-2, 9 -1
    df['fairness']= np.where((df['Fairness_score'] == 1) | (df['Fairness_score'] == 2), 'fair', 'unfair')
    fairCount = df.groupby('fairness').count()
    fairCount.to_csv("/Users/kezhang/ownCloud/Suicide_UG/UG_clean_data/fairness.csv")
    print(fairCount)
main_fairness()


