import pandas as pd
import numpy as np

emo = pd.read_csv('/Users/kezhang/ownCloud/Suicide_UG/UG_clean_updated/post_survey_master_data_frame.csv',
                  encoding = "ISO-8859-1")
def avg_emotion():
    # take the average of ratings of empathy and anger and fairness for each subject
    emoAvg1 = emo.groupby(['id','Q_type'])['Rating'].mean()
    emoAvg1.to_csv('/Users/kezhang/ownCloud/Suicide_UG/UG_clean_updated/post_survey_avg.csv')

    print(emoAvg1)
    emo['Q_type1'] = np.where((emo['Q_type'] == "sympathy") | (emo['Q_type'] == "anger"), 'emoReactivity', 'fairness')
    emoAvg2 = emo.groupby(['id', 'Q_type1'])['Rating'].mean()


avg_emotion()
