import pandas as pd
import numpy as np
import glob
import shutil

def add_demo():
    baseline = pd.read_csv("/Users/kezhang/ownCloud/Suicide_UG/baseline_master_data_frame.csv", encoding = "ISO-8859-1")
    context = pd.read_csv('/Users/kezhang/ownCloud/Suicide_UG/context_master_data_frame.csv', encoding = "ISO-8859-1")
    demo = pd.read_csv('/Users/kezhang/ownCloud/Suicide_UG/ug_demos.csv')

    demo = demo.rename(columns={'ID':'id'})

    #combine demographic into task data
    baseline_demo = pd.merge(baseline, demo, how='left')
    context_demo = pd.merge(context,demo, how='left')

    #edit the trial number, context data follows baseline data
    baseline_demo['merge_trial'] = baseline_demo['Trial_Number']
    context_demo['merge_trial'] = context_demo['Trial_Number'] + 26

    baseline_demo.to_csv("/Users/kezhang/ownCloud/Suicide_UG/UG_clean_data/baseline_demo.csv")
    context_demo.to_csv('/Users/kezhang/ownCloud/Suicide_UG/UG_clean_data/context_demo.csv')

def all_data():
    files = glob.glob("/Users/kezhang/ownCloud/Suicide_UG/UG_clean_data/*.csv")
    all_data = pd.DataFrame()
    for f in files:
        df = pd.read_csv(f)
        all_data = all_data.append(df)[df.columns.tolist()]
    print(all_data.head())
    all_data.to_csv("/Users/kezhang/ownCloud/Suicide_UG/UG_clean_data/all_data.csv")

all_data()
