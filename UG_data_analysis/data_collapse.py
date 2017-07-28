import pandas as pd
import numpy as np
import glob

def add_demo():
    ####merge demo data to the task data.###

    baseline = pd.read_csv('C:\\Users\\ke\ownCloud\\Suicide_UG\\new_data\\baseline_master_data_frame.csv',  encoding = "ISO-8859-1")
    context = pd.read_csv('C:\\Users\\ke\\ownCloud\\Suicide_UG\\new_data\\context_master_data_frame.csv',  encoding = "ISO-8859-1")
    demo = pd.read_csv('C:\\Users\\ke\ownCloud\\Suicide_UG\\new_data\\ug_demos.csv', encoding = "ISO-8859-1")

    # baseline = pd.read_csv('/Users/kezhang/ownCloud/Suicide_UG/new_data/baseline_master_data_frame.csv', encoding = "ISO-8859-1")
    # context = pd.read_csv('/Users/kezhang/ownCloud/Suicide_UG/new_data/context_master_data_frame.csv', encoding = "ISO-8859-1")
    # demo = pd.read_csv('/Users/kezhang/ownCloud/Suicide_UG/new_data/ug_demos.csv', encoding = "ISO-8859-1")

    demo = demo.rename(columns={'ID':'id'})

    #combine demographic into task data
    baseline_demo = pd.merge(baseline, demo, how='left')
    context_demo = pd.merge(context,demo, how='left')

    #edit the trial number, context data follows baseline data
    baseline_demo['merge_trial'] = baseline_demo['Trial_Number']
    context_demo['merge_trial'] = context_demo['Trial_Number'] + 26

    # baseline_demo.to_csv("/Users/kezhang/ownCloud/Suicide_UG/baseline_demo.csv", index=False)
    # context_demo.to_csv("/Users/kezhang/ownCloud/Suicide_UG/context_demo.csv", index=False)

    baseline_demo.to_csv('C:\\Users\\ke\\ownCloud\\Suicide_UG\\baseline_demo.csv', index = False)
    context_demo.to_csv('C:\\Users\\ke\\ownCloud\\Suicide_UG\\context_demo.csv', index = False)


def all_data():
    #merge context data and baseline data into one file.###

    # files = glob.glob("/Users/kezhang/ownCloud/Suicide_UG/*.csv")
    files = glob.glob("C:\\Users\\ke\\ownCloud\\Suicide_UG\\*.csv")
    all_data = pd.DataFrame()
    for f in files:
        df = pd.read_csv(f,encoding = "ISO-8859-1")
        all_data = all_data.append(df)[df.columns.tolist()]
    print(all_data.head())
    # all_data.to_csv("/Users/kezhang/ownCloud/Suicide_UG/UG_clean_data/all_data.csv")
    all_data.to_csv("C:\\Users\\ke\\ownCloud\\Suicide_UG\\UG_clean_data\\all_data.csv", index=False)


