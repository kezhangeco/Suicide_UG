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

    files = glob.glob("/Users/kezhang/ownCloud/Suicide_UG/UG_clean_updated/try/*.csv")
    all_data = pd.DataFrame()
    for f in files:
        df = pd.read_csv(f,encoding = "ISO-8859-1")
        all_data = all_data.append(df)[df.columns.tolist()]
        # all_data = all_data.append(df)
        # return all_data1, all_data2
    print(all_data)


    # all_data1.to_csv("/Users/kezhang/ownCloud/Suicide_UG/UG_clean_updated/try/all_try1.csv", index=False)
    # all_data2.to_csv("/Users/kezhang/ownCloud/Suicide_UG/UG_clean_updated/try/all_try2.csv", index=False)

def try_data():
    f1 = pd.read_excel("/Users/kezhang/ownCloud/Suicide_UG/UG_clean_updated/try/try.xlsx")
    f2 = pd.read_excel("/Users/kezhang/ownCloud/Suicide_UG/UG_clean_updated/try/try2.xlsx")
    print(f1)
    print(f2)
    all_data = pd.DataFrame()

    # frames = [f1, f2]
    # df = pd.concat(frames,axis=0)
    # df = all_data.append(frames,ignore_index=True)
    f1 = f1.append(f2)[f2.columns.tolist()]

    print(f1)
try_data()



def control():
    # extra all HC data
    all_data = pd.read_csv('/Users/kezhang/ownCloud/Suicide_UG/UG_clean_updated/ug_all_task_data.csv', encoding="ISO-8859-1")
    HC = all_data[all_data.group5 == 'control']
    # # HC.to_excel('/Users/kezhang/ownCloud/Suicide_UG/UG_clean_updated/controls_data.xlsx', index=False)
    # for row in range(0:HC.length):
    #     excel.writerow(HC["pid"][row],)
