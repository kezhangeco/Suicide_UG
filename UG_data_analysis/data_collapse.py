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

    files = glob.glob("C:\\Users\\ke\\ownCloud\\Suicide_UG\\UG_clean_updated\\merged_panels\\*.csv")
    all_data = pd.DataFrame()
    for f in files:
        df = pd.read_csv(f,encoding = "ISO-8859-1")
        all_data = all_data.append(df)[df.columns.tolist()]

    print(all_data)

    all_data.to_csv('C:\\Users\\ke\\ownCloud\\Suicide_UG\\UG_clean_updated\\merged_panels\\*.csv')

def all_task_data_recode():
    # insert recoded values
    # new var identifies the subject's group: control, depressed_control, ideator, AttempterHL, AttempterLL
    # group 5: split attempter into HL and LL
    # group 4: does not split attempters
    df = pd.read_csv('/Users/kezhang/ownCloud/Suicide_UG/UG_clean_updated/ug_all_task_data.csv',
                     encoding="ISO-8859-1",
                     dtype={'StakeImg': object, 'ReappraisalText': object, 'ReappraisalDirection': object,
                            'PunishingType': object})

    df["group5"] = np.where(df['PATTYPE'] == 'CONTROL', 'control', np.where(df['PATTYPE'] == 'DEPRESSION', 'depression',
                                                                            np.where(df['COMMENT'] == 'IDEATOR',
                                                                                     'ideator',
                                                                                     np.where(df[
                                                                                                  'COMMENT'] == 'IDEATOR-ATTEMPTER',
                                                                                              np.where(df[
                                                                                                           'MAXLETHALITY'] < 4,
                                                                                                       'AttempterLL',
                                                                                                       'AttempterHL'),
                                                                                              np.where(df[
                                                                                                           'COMMENT'] == 'ATTEMPTER',
                                                                                                       np.where(df[
                                                                                                                    'MAXLETHALITY'] < 4,
                                                                                                                'AttempterLL',
                                                                                                                'AttempterHL'),
                                                                                                       'NA')))))

    df['group4'] = np.where((df['group5'] == 'AttempterLL') | (df['group5'] == 'AttempterHL'), 'attempter',
                            df['group5'])

    # check the main effect of fairness, whether people accept more fair offer in terms of percentage.
    # 5 levels of fairness for the offers (1 = 50/50; 2 = 60/40; 3 = 70/30; 4 = 8/2; 5 = 90/10);
    # fair = 5-5, 6-4;
    # unfair = 7-3, 8-2, 9 -1

    df['fairness'] = np.where((df['Fairness_score'] == 1) | (df['Fairness_score'] == 2), 'fair', 'unfair')
    df.to_csv('/Users/kezhang/ownCloud/Suicide_UG/UG_clean_updated/ug_all_task_data_groupissue.csv', index=False)

def demo_group():
    df = pd.read_excel("C:\\Users\\ke\\ownCloud\\Suicide_UG\\raw_data_backup\\questionnaires_withBatch2.xlsx",
                        sheetname = "July 2017 UG DATA")
    df["group5"] = np.where(df['COMMENT'] == 'CONTROL', 'control', np.where(df['COMMENT'] == 'DEPRESSION', 'depression',
                                                                            np.where(df['COMMENT'] == 'IDEATOR',
                                                                                     'ideator',
                                                                                     np.where(df[
                                                                                                  'COMMENT'] == 'IDEATOR-ATTEMPTER',
                                                                                              np.where(df[
                                                                                                           'MAX LETHALITY'] < 4,
                                                                                                       'AttempterLL',
                                                                                                       'AttempterHL'),
                                                                                              np.where(df[
                                                                                                           'COMMENT'] == 'ATTEMPTER',
                                                                                                       np.where(df[
                                                                                                                    'MAX LETHALITY'] < 4,
                                                                                                                'AttempterLL',
                                                                                                                'AttempterHL'),
                                                                                                       'NA')))))

    df['group4'] = np.where((df['group5'] == 'AttempterLL') | (df['group5'] == 'AttempterHL'), 'attempter',
                            df['group5'])

    df.to_excel('C:\\Users\\ke\\ownCloud\\Suicide_UG\\UG_clean_updated\\questionnaire.xlsx', index=False)

demo_group()

def reappra():
    df = pd.read_csv('C:\\Users\\ke\\ownCloud\\Suicide_UG\\UG_clean_updated\\ug_all_task_data.csv')
    df['PunishingType'].fillna('baseline', inplace=True)
    df['ReappraisalDirection'].fillna('baseline', inplace=True)
    df['ReappraisalDirection'] = np.where(df['ReappraisalDirection'] == 1, 'punish',
                                          np.where(df['ReappraisalDirection'] == 2, 'empathy',
                                                   df['ReappraisalDirection']))
    print(df['ReappraisalDirection'])
    df.to_csv('C:\\Users\\ke\\ownCloud\\Suicide_UG\\UG_clean_updated\\ug_all_task_data.csv', index=False)


def control():
    # extra all HC data
    all_data = pd.read_csv('/Users/kezhang/ownCloud/Suicide_UG/UG_clean_updated/ug_all_task_data.csv',
                           encoding="ISO-8859-1")
    HC = all_data[all_data.group5 == 'control']
    HC.to_excel('/Users/kezhang/ownCloud/Suicide_UG/UG_clean_updated/controls_data.xlsx')

def bind_demoQuestionnaire_groups():
    question = pd.read_csv('/Users/kezhang/ownCloud/Suicide_UG/UG_clean_updated/ug_questionnaires.csv')
    demo = pd.read_csv('/Users/kezhang/ownCloud/Suicide_UG/UG_clean_updated/ug_demog.csv')
    merged = question.join(demo, on='ID')
    print(merged)

