import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import ggplot
from openpyxl import load_workbook
from scipy import stats


def byGroup():
    # new var identifies the subject's group: control, depressed_control, ideator, AttempterHL, AttempterLL
    # group 5: split attempter into HL and LL
    # group 4: does not split attempters
    df = pd.read_csv('/Users/kezhang/ownCloud/Suicide_UG/UG_clean_updated/merged_panels/all_task_data.csv',  encoding="ISO-8859-1",
                     dtype={'StakeImg': object, 'ReappraisalText': object, 'ReappraisalDirection': object,
                            'PunishingType': object})


    df["group5"] = np.where(df['PATTYPE'] == 'CONTROL', 'control', np.where(df['PATTYPE'] == 'DEPRESSION', 'depression',
                                                                           np.where(df['COMMENT'] == 'IDEATOR', 'ideator',
                                                                                    np.where(df['COMMENT'] == 'IDEATOR-ATTEMPTER',
                                                                                             np.where(df['MAXLETHALITY'] < 4, 'AttempterLL', 'AttempterHL'),
                                                                                             np.where(df['COMMENT'] == 'ATTEMPTER',
                                                                                                      np.where(df['MAXLETHALITY'] < 4, 'AttempterLL', 'AttempterHL'), 'NA')))))

    df['group4'] = np.where((df['group5'] == 'AttempterLL') | (df['group5'] == 'AttempterHL'), 'attempter', df['group5'])
    df.to_csv('/Users/kezhang/ownCloud/Suicide_UG/UG_clean_updated/merged_panels/ug_all_task_data.csv', encoding = "ISO-8859-1", index = False)


def demo_description():
    # add 'group' variable into demographic data: 5 levels group and 4 levels group. HH and LL attempters
    # describe demographic info, mean, median, sd...

    df1 = pd.read_excel('/Users/kezhang/ownCloud/Suicide_UG/UG_clean_updated/ug_demog.xlsx')
    # print(df1)

    group5_demo = df1.groupby(['group5'])['PROTECT2AGE', 'MARITALTEXT', 'GENDERTEXT',
                                          'EDUCATION', 'RACETEXT'].describe(percentiles=None, include = 'all')
    group4_demo = df1.groupby(['group4'])['PROTECT2AGE', 'MARITALTEXT', 'GENDERTEXT',
                                          'EDUCATION'].describe(percentiles=None, include = 'all')

    # attempter = df1[df1['group4'] == 'attempter'].dropna()
    # attempterHL = df1[df1['group5'] == 'AttempterHL'].dropna()
    # attempterLL = df1[df1['group5'] == 'AttempterLL'].dropna()
    # ideator = df1[df1['group4'] == 'ideator'].dropna()
    # control = df1[df1['group4'] == 'control'].dropna()
    # depression = df1[df1['group4'] == 'depression'].dropna()
    #
    # demo = df1.groupby(['group4'])['PROTECT2AGE']
    # # demo = demo.reset_index()
    # print(demo)


    # writer = pd.ExcelWriter("/Users/kezhang/ownCloud/Suicide_UG/UG_clean_updated/demo_summary.xlsx")
    # group5_demo.to_excel(writer, 'group5_demo')
    # group4_demo.to_excel(writer, 'group4_demo')
    # writer.save()
    # writer.close()

    mar = df1[df1['EDUCATION'].isnull()]
    print(list(mar['ID']))


def questionnaires_description():
    # describe questionnaires information, such as depression, MMSE and others

    df = pd.read_excel('/Users/kezhang/ownCloud/Suicide_UG/UG_clean_updated/ug_questionnaire.xlsx')
    book = load_workbook("/Users/kezhang/ownCloud/Suicide_UG/UG_clean_updated/demo_summary.xlsx")
    writer = pd.ExcelWriter("/Users/kezhang/ownCloud/Suicide_UG/UG_clean_updated/demo_summary.xlsx", engine = 'openpyxl')
    writer.book = book

    question_bygroup5 = df.groupby('group5')['DEP ONSET AGE', 'HOUSEHOLD INCOME', 'HRSD NO SUI', 'MMSE TOTAL',
    'PER CAPITA INCOME', 'SSI BL CURRENT', 'DRS'].describe(include='all')
    question_bygroup4 = df.groupby('group4')['DEP ONSET AGE', 'HOUSEHOLD INCOME', 'HRSD NO SUI', 'MMSE TOTAL',
    'PER CAPITA INCOME', 'SSI BL CURRENT', 'DRS'].describe(include='all')

    question_bygroup5.to_excel(writer, 'group5_questionnaires')
    question_bygroup4.to_excel(writer, 'group4_questionnaired')
    writer.save()
    writer.close()


def demo_summ_clean():
    summ5 = pd.read_excel('/Users/kezhang/ownCloud/Suicide_UG/UG_clean_updated/UG_summary.xlsx', sheetname='group5')
    summ4 = pd.read_excel('/Users/kezhang/ownCloud/Suicide_UG/UG_clean_updated/UG_summary.xlsx', sheetname='group4')

    rows = ['min', 'max', '25%', '50%', '75%', 'max', 'unique', 'top', 'freq']

    summ_g5 = ~summ5.stats.isin(rows)
    summ_g5 = summ5[summ_g5]

    summ_g4 = ~summ4.stats.isin(rows)
    summ_g4 = summ4[summ_g4]


    book = load_workbook('/Users/kezhang/ownCloud/Suicide_UG/UG_clean_updated/UG_summary_py.xlsx')
    writer = pd.ExcelWriter('/Users/kezhang/ownCloud/Suicide_UG/UG_clean_updated/UG_summary_py.xlsx', engine='openpyxl')
    writer.book = book

    summ_g5.to_excel(writer, 'group5', index = False)
    summ_g4.to_excel(writer, 'group4', index = False)
    writer.save()
    writer.close()


def summ_gender():
    summ = pd.read_csv('/Users/kezhang/ownCloud/Suicide_UG/UG_clean_updated/ug_demog.csv')
    summ = summ[['ID', 'GENDERTEXT', 'RACETEXT', 'MARITALTEXT', 'group5', 'group4']]
    summ.to_excel('/Users/kezhang/ownCloud/Suicide_UG/UG_clean_updated/ug_gender.xlsx')

