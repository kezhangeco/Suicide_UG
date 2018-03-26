import pandas as pd
import numpy as np
import glob
import demo_question_describe
import os.path

def add_demo_task():
    #### merge demo data to the task data.###
    # recode empty reappraisal cells(null values) to "baseline"

    demo = pd.read_csv('/Users/kezhang/ownCloud/Suicide_UG/UG_clean_updated/ug_demog.csv', encoding = "ISO-8859-1")
    task = pd.read_csv('/Users/kezhang/ownCloud/Suicide_UG/UG_clean_updated/ug_all_task_data.csv', encoding = "ISO-8859-1")

    variables = ['ID', 'PROTECT2 AGE', 'GENDER TEXT', 'MARITAL TEXT', 'RACE TEXT', 'ETHNICITY TEXT']

    task_demo = pd.merge(task, demo[variables], on = 'ID')

    task_demo['PunishingType'].fillna('baseline', inplace = True)
    task_demo['ReappraisalDirection'].fillna('baseline', inplace=True)
    task_demo['ReappraisalDirection'] = np.where(task_demo['ReappraisalDirection'] == 1, 'punish',
                                          np.where(task_demo['ReappraisalDirection'] == 2, 'empathy',
                                                   task_demo['ReappraisalDirection']))

    task_demo['fairness'] = np.where((task_demo['Fairness_score'] == 1) | (task_demo['Fairness_score'] == 2),
                                     'fair', 'unfair')

    task_demo = task_demo.rename(columns = {'PROTECT2 AGE':'PROTECT2AGE', 'GENDER TEXT':'GENDERTEXT',
                                            'MARITAL TEXT':'MARITALTEXT', 'RACE TEXT':'RACETEXT',
                                            'ETHNICITY TEXT':'ETHNICITYTEXT'})
    task_demo.to_csv('/Users/kezhang/ownCloud/Suicide_UG/UG_clean_updated/ug_all_task_data.csv')

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
    demo = pd.read_csv('/Users/kezhang/ownCloud/Suicide_UG/UG_clean_updated/ug_demog.csv')
    baseline = pd.read_csv('/Users/kezhang/ownCloud/Suicide_UG/UG_clean_updated/trials/baselineID155.csv')
    context = pd.read_csv('/Users/kezhang/ownCloud/Suicide_UG/UG_clean_updated/trials/contextID155.csv')
    files = glob.glob('/Users/kezhang/ownCloud/Suicide_UG/UG_clean_updated/trials/*.csv')
    cols_to_use = context.columns.difference(baseline.columns)
    print(cols_to_use)
    print(context[cols_to_use])
    all_data = pd.concat([baseline, context], ignore_index=True)
    # all_data = pd.DataFrame()
    # for f in files:
    #     df = pd.read_csv(f, encoding = "ISO-8859-1")
    #     all_data = all_data.append(df)[df.columns.tolist()]

    print(all_data['ID'].nunique())
    print(demo['ID'].nunique())
    print(list(set(demo.ID.tolist()) - set(all_data.ID.tolist())))
    all_data.to_csv('/Users/kezhang/ownCloud/Suicide_UG/UG_clean_updated/ug_all_task_data.csv', index = False)


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


def add_groupType():
    # take the original 121 participants' data from the current larger 155 data set.
    # ID120 = pd.read_csv("/Users/kezhang/ownCloud/Suicide_UG/UG_clean_updated/wrongData/ug_all_task_data.csv",
    #                     encoding = "ISO-8859-1")
    # ug_demog = pd.read_excel("/Users/kezhang/ownCloud/Suicide_UG/UG_clean_updated/wrongData/ug_demog.xlsx")
    demoID155 = pd.read_csv("/Users/kezhang/ownCloud/Suicide_UG/raw_data_backup/03-22-18 UG DEMO.csv"
                            , encoding="ISO-8859-1")
    baselineID155 = pd.read_csv("/Users/kezhang/ownCloud/Suicide_UG/raw_data_backup/baseline_master_data_frame.csv"
                                , encoding="ISO-8859-1")
    contextID155 = pd.read_csv("/Users/kezhang/ownCloud/Suicide_UG/raw_data_backup/context_master_data_frame.csv"
                               , encoding="ISO-8859-1")
    postID155 = pd.read_csv("/Users/kezhang/ownCloud/Suicide_UG/raw_data_backup/post_survey_master_data_frame.csv"
                            , encoding="ISO-8859-1")
    question = pd.read_excel("/Users/kezhang/ownCloud/Suicide_UG/raw_data_backup/questionnaires.xlsx",
                             sheetname = "July 2017 UG DATA")

    # categorize group
    demoID155["group5"] = np.where(demoID155['PATTYPE'] == 'CONTROL', 'control', np.where(demoID155['PATTYPE'] == 'DEPRESSION', 'depression',
                                                                            np.where(demoID155['COMMENT'] == 'IDEATOR',
                                                                                     'ideator',
                                                                                     np.where(demoID155[
                                                                                                  'COMMENT'] == 'IDEATOR-ATTEMPTER',
                                                                                              np.where(demoID155[
                                                                                                           'MAX LETHALITY'] < 4,
                                                                                                       'AttempterLL',
                                                                                                       'AttempterHL'),
                                                                                              np.where(demoID155[
                                                                                                           'COMMENT'] == 'ATTEMPTER',
                                                                                                       np.where(demoID155[
                                                                                                                    'MAX LETHALITY'] < 4,
                                                                                                                'AttempterLL',
                                                                                                                'AttempterHL'),
                                                                                                       'NA')))))

    demoID155['group4'] = np.where((demoID155['group5'] == 'AttempterLL') | (demoID155['group5'] == 'AttempterHL'), 'attempter',
                            demoID155['group5'])


    subjectType = demoID155[['ID', 'group5', 'group4']]

    baselineID155 = baselineID155.rename(columns={'id':'ID'})
    contextID155 = contextID155.rename(columns={'id':'ID'})
    postID155 = postID155.rename(columns={'id':'ID'})

    baselineID155 = baselineID155.merge(subjectType, on = 'ID')
    contextID155 = contextID155.merge(subjectType, on = 'ID')
    postID155 = postID155.merge(subjectType, on = 'ID')
    question = question.merge(subjectType, on = 'ID')

    demoID155.to_csv("/Users/kezhang/ownCloud/Suicide_UG/UG_clean_updated/ug_demog.csv")
    baselineID155.to_csv('/Users/kezhang/ownCloud/Suicide_UG/UG_clean_updated/trials/baselineID155.csv')
    contextID155.to_csv('/Users/kezhang/ownCloud/Suicide_UG/UG_clean_updated/trials/contextID155.csv')
    postID155.to_csv('/Users/kezhang/ownCloud/Suicide_UG/UG_clean_updated/ug_reactivity.csv')
    question.to_csv('/Users/kezhang/ownCloud/Suicide_UG/UG_clean_updated/ug_questionnaires.csv')


def extract120():
    # extract the original 120 participants from the larger 155.
    ug_all_taskID155 = pd.read_csv('/Users/kezhang/ownCloud/Suicide_UG/UG_clean_updated/ug_all_task_data155.csv')
    demoID155 = pd.read_csv('/Users/kezhang/ownCloud/Suicide_UG/UG_clean_updated/ug_demog155.csv')
    postID155 = pd.read_csv('/Users/kezhang/ownCloud/Suicide_UG/UG_clean_updated/ug_reactivity155.csv')
    ID120 = pd.read_csv("/Users/kezhang/ownCloud/Suicide_UG/UG_clean_updated/wrongData/ug_all_task_data.csv",
                        encoding = "ISO-8859-1")
    olddemo = pd.read_excel("/Users/kezhang/ownCloud/Suicide_UG/UG_clean_updated/wrongData/ug_demog.xlsx")

    ug_all_taskID155['ID'] = ug_all_taskID155['ID'].astype('category')
    demoID155['ID'] = demoID155['ID'].astype('category')
    ug_all_taskID155['ID'] = ug_all_taskID155['ID'].astype('category')
    demoID155['ID'] = demoID155['ID'].astype('category')
    ID120['ID'] = ID120['ID'].astype('category')

    ID120N = np.unique(ID120['ID'])
    print(len(ID120N))

    demoID120 = demoID155.loc[demoID155['ID'].isin(ID120N)]
    ug_all_taskID120 = ug_all_taskID155.loc[ug_all_taskID155['ID'].isin(ID120N)]
    postID120 = postID155.loc[postID155['ID'].isin(ID120N)]

    # check if the past ID120 and current ID120 slice from ID155 have the same group for partcipants
    dold120 = olddemo[['ID', 'group4', 'group5']].reset_index(drop=True)
    dnew120 = demoID120[['ID', 'group4','group5']].reset_index(drop=True)
    newtask120 = ug_all_taskID120[['ID', 'group4', 'group5']].reset_index(drop=True)
    oldtask120 = ID120[['ID', 'group4', 'group5']].reset_index(drop=True)

    ogroup5_demo = dold120.groupby(['group5'])['ID'].describe(percentiles=None, include='all')
    ngroup5_demo = dnew120.groupby(['group5'])['ID'].describe()
    ngroup5_task = newtask120.groupby(['group5'])['ID'].describe()
    ogroup5_task = oldtask120.groupby(['group5'])['ID'].describe()
    print('old demo', ogroup5_demo)
    print('new demo', ngroup5_demo)
    print('old task', ogroup5_task)
    print('new task', ngroup5_task)

    # old demo group and task group are not the same, check which ones are different
    compareDemoGroup = pd.merge(dold120, oldtask120, on='ID')
    compareDemoGroup['differ4'] = np.where(compareDemoGroup['group4_x'] == compareDemoGroup['group4_y'], 'same', 'NO')
    compareDemoGroup['differ5'] = np.where(compareDemoGroup['group5_x'] == compareDemoGroup['group5_y'], 'same', 'NO')
    differ = compareDemoGroup.loc[compareDemoGroup['differ5'] == 'NO']

    # groups in the old data are different from the new data, check which ones are different

    dold120 = dold120.drop_duplicates(subset = ['ID']).set_index('ID')
    dnew120 = dnew120.drop_duplicates(subset = ['ID']).set_index('ID')
    newtask120 = newtask120.drop_duplicates(subset = ['ID']).set_index('ID')
    dold120 = dold120.rename(columns = {'group5':'old'})
    dnew120 = dnew120.rename(columns = {'group5': 'newDemo'})
    newtask120 = newtask120.rename(columns = {'group5': 'newTask'})
    compareGroup = pd.concat([dold120, dnew120, newtask120], axis=1)
    compareGroup['differ5'] = np.where((compareGroup['old'] == compareGroup['newDemo']) |
                                       (compareGroup['old'] == compareGroup['newTask']),
                                       'same', 'NO')
    differ1 = compareGroup.loc[compareGroup['differ5'] == 'NO']
    print(differ1)

    # print(differ.drop_duplicates(subset = ['ID']))

    # demoID120.to_csv('/Users/kezhang/ownCloud/Suicide_UG/UG_clean_updated/ug_demog.csv')
    # ug_all_taskID120.to_csv('/Users/kezhang/ownCloud/Suicide_UG/UG_clean_updated/ug_all_task_data.csv')
    # postID120.to_csv('/Users/kezhang/ownCloud/Suicide_UG/UG_clean_updated/ug_reactivity.csv')

def rmID():
    # rm ID who are under age 50
    demo155 = pd.read_csv('/Users/kezhang/ownCloud/Suicide_UG/UG_clean_updated/ug_demog155.csv')
    task155 = pd.read_csv('/Users/kezhang/ownCloud/Suicide_UG/UG_clean_updated/ug_all_task_data155.csv')
    emo155 = pd.read_csv('/Users/kezhang/ownCloud/Suicide_UG/UG_clean_updated/ug_reactivity155.csv')
    demo = pd.read_csv('/Users/kezhang/ownCloud/Suicide_UG/UG_clean_updated/ug_demog.csv')
    task = pd.read_csv('/Users/kezhang/ownCloud/Suicide_UG/UG_clean_updated/ug_all_task_data.csv')
    emo = pd.read_csv('/Users/kezhang/ownCloud/Suicide_UG/UG_clean_updated/ug_reactivity.csv')

    print(emo155.drop_duplicates(subset = ['ID']).shape)
    print(emo.drop_duplicates(subset = ['ID']).shape)

    demo155 = demo155.loc[demo155['PROTECT2AGE'] >= 50]
    task155 = task155.loc[task155['PROTECT2AGE'] >= 50]
    demo = demo.loc[demo['PROTECT2AGE'] >= 50]
    task = task.loc[task['PROTECT2AGE'] >= 50]

    ID = np.unique(demo155['ID'])
    emo155 = emo155.loc[emo155['ID'].isin(ID)]
    emo = emo.loc[emo['ID'].isin(ID)]

    print(min(demo155['PROTECT2AGE']), min(task155['PROTECT2AGE']))
    print('demo155', demo155.shape,
          'task155', task155.drop_duplicates(subset = 'ID').shape,
          'demo', demo.shape,
          'task', task.drop_duplicates(subset = 'ID').shape,
          'emo155', emo155.drop_duplicates(subset = 'ID').shape,
          'emo', emo.drop_duplicates(subset = 'ID').shape)

    demo155.to_csv('/Users/kezhang/ownCloud/Suicide_UG/UG_clean_updated/ug_demog155.csv')
    task155.to_csv('/Users/kezhang/ownCloud/Suicide_UG/UG_clean_updated/ug_all_task_data155.csv')
    emo155.to_csv('/Users/kezhang/ownCloud/Suicide_UG/UG_clean_updated/ug_reactivity155.csv')
    demo.to_csv('/Users/kezhang/ownCloud/Suicide_UG/UG_clean_updated/ug_demog.csv')
    task.to_csv('/Users/kezhang/ownCloud/Suicide_UG/UG_clean_updated/ug_all_task_data.csv')
    emo.to_csv('/Users/kezhang/ownCloud/Suicide_UG/UG_clean_updated/ug_reactivity.csv')





rmID()