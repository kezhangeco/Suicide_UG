import pandas as pd
import numpy as np

emo = pd.read_csv('/Users/kezhang/ownCloud/Suicide_UG/raw_data_backup/post_survey_master_data_frame.csv', encoding = "ISO-8859-1")
# emo = pd.read_csv('C:\\Users\\ke\\ownCloud\\Suicide_UG\\UG_clean_updated\\post_survey_master_data_frame.csv', encoding = "ISO-8859-1")

def avg_emotion():
    # take the average of ratings of empathy and anger and fairness for each subject
    emoAvg = emo.groupby(['ID','Q_type'], as_index=False)['Rating'].mean()
    # emoAvg = emoAvg.rename(columns = {'Rating': 'emoRating'})
    # emoAvg['Q_type1'] = np.where((emo['Q_type'] == "sympathy") | (emo['Q_type'] == "anger"), 'emoReactivity', 'fairness')
    print(emoAvg)


    emoAvg.to_csv('/Users/kezhang/ownCloud/Suicide_UG/UG_clean_updated/post_survey_avg.csv', index = False)



avg_emotion()
