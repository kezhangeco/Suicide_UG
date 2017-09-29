import pandas as pd
import numpy as np
import glob

def add_demo():
    #### merge demo data to the task data.###

    baseline = pd.read_csv('/Users/kezhang/ownCloud/Suicide_UG/raw_data_backup/baseline_master_data_frame.csv',  encoding = "ISO-8859-1")
    context = pd.read_csv('/Users/kezhang/ownCloud/Suicide_UG/raw_data_backup/context_master_data_frame.csv',  encoding = "ISO-8859-1")
    demo = pd.read_csv('/Users/kezhang/ownCloud/Suicide_UG/raw_data_backup/UG_CON_DEMOS_UPDATED.csv', encoding = "ISO-8859-1")

    baseline = baseline.rename(columns={'id': 'ID'})
    context = context.rename(columns={'id': 'ID'})

    #combine demographic into task data
    baseline_demo = pd.merge(baseline, demo, how='left')
    context_demo = pd.merge(context,demo, how='left')

    #edit the trial number, context data follows baseline data
    baseline_demo['merge_trial'] = baseline_demo['Trial_Number']
    context_demo['merge_trial'] = context_demo['Trial_Number'] + 26

    baseline_demo.to_csv('/Users/kezhang/ownCloud/Suicide_UG/UG_clean_updated/merged_panels/baseline_demo.csv', index = False)
    context_demo.to_csv('/Users/kezhang/ownCloud/Suicide_UG/UG_clean_updated/merged_panels/context_demo.csv', index = False)


def all_task_data():
    #merge context data and baseline data into one file.###

    files = glob.glob("/Users/kezhang/ownCloud/Suicide_UG/UG_clean_updated/merged_panels/*.csv")
    all_data = pd.DataFrame()
    for f in files:
        df = pd.read_csv(f,encoding = "ISO-8859-1")
        all_data = all_data.append(df)[df.columns.tolist()]
    print(all_data.head())
    all_data.to_csv("/Users/kezhang/ownCloud/Suicide_UG/UG_clean_updated/merged_panels/all_task_data.csv", index=False)



add_demo()
all_task_data()