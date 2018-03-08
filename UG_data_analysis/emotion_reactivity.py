import pandas as pd
import numpy as np

# emo = pd.read_csv('/Users/kezhang/ownCloud/Suicide_UG/UG_clean_updated/post_survey_master_data_frame.csv', encoding = "ISO-8859-1")
emo = pd.read_csv('C:\\Users\\ke\\ownCloud\\Suicide_UG\\UG_clean_updated\\post_survey_master_data_frame.csv', encoding = "ISO-8859-1")

def avg_emotion():
    # take the average of ratings of empathy and anger and fairness for each subject
    emoAvg1 = emo.groupby(['id','Q_type'], as_index=False)['Rating'].mean()
    emoAvg1 = emoAvg1.rename(columns = {'Rating': 'RatingBy3'})
    print(emoAvg1)
    emo['Q_type1'] = np.where((emo['Q_type'] == "sympathy") | (emo['Q_type'] == "anger"), 'emoReactivity', 'fairness')
    emoAvg2 = emo.groupby(['id', 'Q_type1'], as_index=False)['Rating'].mean()
    emoAvg2 = emoAvg2.rename(columns = {'Rating': 'RatingBy2'})
    print(emoAvg2)

    emoAvg = pd.merge(emoAvg1, emoAvg2, on = 'id')
    print(emoAvg)

    emoAvg.to_csv('C:\\Users\\ke\\ownCloud\\Suicide_UG\\UG_clean_updated\\post_survey_avg.csv', index = False)



avg_emotion()
