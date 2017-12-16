import pandas as pd
import numpy as np
import glob

def add_demo_task():
    #### merge demo data to the task data.###
    # recode empty reappraisal cells(null values) to "baseline"

    demo = pd.read_excel('C:\\Users\\ke\\ownCloud\\Suicide_UG\\UG_clean_updated\\ug_demog.xlsx')
    task = pd.read_csv('C:\\Users\\ke\\ownCloud\\Suicide_UG\\UG_clean_updated\\ug_all_task_data.csv', encoding = "ISO-8859-1")

    demo = demo.rename(columns = {'ID' : 'id'})
    variables = ['id', 'PROTECT2AGE', 'GENDERTEXT', 'MARITALTEXT', 'RACETEXT', 'ETHNICITYTEXT', 'group5', 'group4']

    task_demo = pd.merge(task, demo[variables], on = 'id')

    task_demo['PunishingType'].fillna('baseline', inplace = True)
    task_demo['ReappraisalDirection'].fillna('baseline', inplace=True)
    task_demo['ReappraisalDirection'] = np.where(task_demo['ReappraisalDirection'] == 1, 'punish',
                                          np.where(task_demo['ReappraisalDirection'] == 2, 'empathy',
                                                   task_demo['ReappraisalDirection']))

    task_demo.to_csv('C:\\Users\\ke\\ownCloud\\Suicide_UG\\UG_clean_updated\\ug_all_task_data.csv')

def mergeTwoBatch_demog():
    oldContext = pd.read_csv('/Users/kezhang/ownCloud/Suicide_UG/raw_data_backup/context_master_data_frame.csv',  encoding = "ISO-8859-1")
    oldBase = pd.read_csv('/Users/kezhang/ownCloud/Suicide_UG/raw_data_backup/baseline_master_data_frame.csv',  encoding = "ISO-8859-1")
    newContext = pd.read_csv('/Users/kezhang/ownCloud/Suicide_UG/raw_data_backup/data_batch2_raw/new_ug_context_n18.csv',  encoding = "ISO-8859-1")
    newBase = pd.read_csv('/Users/kezhang/ownCloud/Suicide_UG/raw_data_backup/data_batch2_raw/new_ug_baseline_n18.csv',  encoding = "ISO-8859-1")
    newQuestion = pd.read_excel('/Users/kezhang/ownCloud/Suicide_UG/raw_data_backup/data_batch2_raw/new_baseline_demo.xlsx', encoding = "ISO-8859-1")
    oldQuestion = pd.read_excel('/Users/kezhang/ownCloud/Suicide_UG/raw_data_backup/questionnaires.xlsx', sheetname='July 2017 UG DATA' )
    newDemo = pd.read_csv('/Users/kezhang/ownCloud/Suicide_UG/raw_data_backup/data_batch2_raw/UG_CON_new_n18_demos.csv')
    oldDemo = pd.read_csv('/Users/kezhang/ownCloud/Suicide_UG/raw_data_backup/UG_CON_DEMOS_UPDATED.csv')

    contextls = [oldContext, newContext]
    basels = [oldBase, newBase]
    questionls = [newQuestion, oldQuestion]
    demols = [newDemo, oldDemo]
    context = pd.concat(contextls).drop_duplicates().reset_index(drop=True)
    base = pd.concat(basels).drop_duplicates().reset_index(drop=True)
    question = pd.concat(questionls).drop_duplicates().reset_index(drop=True)
    demo = pd.concat(demols).drop_duplicates().reset_index(drop=True)

    print("len of PID context", context['id'].nunique())
    print("len of PID base", base['id'].nunique())

    print('N of PID old/new context', oldContext['id'].nunique(), newContext['id'].nunique())
    print('N of PID old/new base', oldBase['id'].nunique(), newBase['id'].nunique())

    print('N of demo', demo['ID'].nunique())

    # context.to_csv("/Users/kezhang/ownCloud/Suicide_UG/raw_data_backup/context_master_data_frame_withBatch2.csv")
    # base.to_csv("/Users/kezhang/ownCloud/Suicide_UG/raw_data_backup/baseline_master_data_frame_withBatch2.csv")
    # question.to_excel('/Users/kezhang/ownCloud/Suicide_UG/UG_clean_updated/ug_questionnaire.xlsx', index = False)
    demo.to_excel('/Users/kezhang/ownCloud/Suicide_UG/UG_clean_updated/ug_demog.xlsx', index = False)


def demo_group():
    # identify participant type in demo and questionnaire spreadsheets.
    # PID 220989, 220927 are "AttempterHL". They are incorrectly identified in the raw data. Hence changes made here

    df = pd.read_excel("/Users/kezhang/ownCloud/Suicide_UG/UG_clean_updated/ug_demog.xlsx")
    question = pd.read_excel('/Users/kezhang/ownCloud/Suicide_UG/UG_clean_updated/ug_questionnaire.xlsx')

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

    df['group4'] = np.where((df['group5'] == 'AttempterLL') | (df['group5'] == 'AttempterHL'), 'attempter', df['group5'])

    df['group5'] = np.where((df['ID'] == 220989) | (df['ID'] == 220927), "AttempterHL", df['group5'])

    subjectType = df[['ID', 'group5', 'group4']]
    question = question.merge(subjectType, on = 'ID')

    df.to_excel('/Users/kezhang/ownCloud/Suicide_UG/UG_clean_updated/ug_demog.xlsx', index=False)
    question.to_excel('/Users/kezhang/ownCloud/Suicide_UG/UG_clean_updated/ug_questionnaire.xlsx', index=False)



def all_task_data():
    #merge context data and baseline data into one file.###
    demo = pd.read_excel('C:\\Users\\ke\ownCloud\\Suicide_UG\\UG_clean_updated\\ug_demog.xlsx')
    files = glob.glob('C:\\Users\\ke\\ownCloud\\Suicide_UG\\raw_data_backup\\trials\\*.csv')
    all_data = pd.DataFrame()
    for f in files:
        df = pd.read_csv(f, encoding = "ISO-8859-1")
        all_data = all_data.append(df)[df.columns.tolist()]

    print(all_data['id'].nunique())
    print(demo['ID'].nunique())
    print(list(set(demo.ID.tolist()) - set(all_data.id.tolist())))
    all_data.to_csv('C:\\Users\\ke\\ownCloud\\Suicide_UG\\UG_clean_updated\\ug_all_task_data.csv', index = False)

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

