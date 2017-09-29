import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import chisquare
import ggplot
from openpyxl import load_workbook


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
    df.to_csv('/Users/kezhang/ownCloud/Suicide_UG/UG_clean_updated/all_task_data_demo.csv', encoding = "ISO-8859-1", index = False)


def demo_description():
    # add 'group' variable into demographic data: 5 levels group and 4 levels group. HH and LL attempters
    # describe demographic info, mean, median, sd...

    # df = pd.read_csv('/Users/kezhang/ownCloud/Suicide_UG/raw_data_backup/UG_CON_DEMOS_UPDATED.csv', encoding = "ISO-8859-1")
    # df["group5"] = np.where(df['PATTYPE'] == 'CONTROL', 'control', np.where(df['PATTYPE'] == 'DEPRESSION', 'depression',
    #                                                                        np.where(df['COMMENT'] == 'IDEATOR',
    #                                                                                 'ideator',
    #                                                                                 np.where(df[
    #                                                                                              'COMMENT'] == 'IDEATOR-ATTEMPTER',
    #                                                                                          np.where(
    #                                                                                              df['MAXLETHALITY'] < 4,
    #                                                                                              'AttempterLL',
    #                                                                                              'AttempterHL'),
    #                                                                                          np.where(df[
    #                                                                                                       'COMMENT'] == 'ATTEMPTER',
    #                                                                                                   np.where(df[
    #                                                                                                                'MAXLETHALITY'] < 4,
    #                                                                                                            'AttempterLL',
    #                                                                                                            'AttempterHL'),
    #                                                                                                   'NA')))))
    #
    # df['group4'] = np.where((df['group5'] == 'AttempterLL') | (df['group5'] == 'AttempterHL'), 'attempter', df['group5'])
    # df.to_csv('/Users/kezhang/ownCloud/Suicide_UG/UG_clean_updated/ug_demog.csv', index=False)
    #
    df1 = pd.read_csv("/Users/kezhang/ownCloud/Suicide_UG/UG_clean_updated/ug_demog.csv", encoding = "ISO-8859-1")
    group5_demo = df1.groupby(['group5'])['BASELINEAGE', 'PROTECT2AGE', 'AGETODAY', 'MAXLETHALITY', 'EDUCATION'].describe()
    group4_demo = df1.groupby(['group4'])['BASELINEAGE', 'PROTECT2AGE', 'AGETODAY', 'MAXLETHALITY', 'EDUCATION'].describe()
    print(group5_demo)
    print(group4_demo)

    writer = pd.ExcelWriter("/Users/kezhang/ownCloud/Suicide_UG/UG_clean_updated/demo_summary.xlsx")
    group5_demo.to_excel(writer, 'group5_age')
    group4_demo.to_excel(writer, 'group4_age')
    writer.save()
    writer.close()


def questionnaires_description():
    # add 'group5' to distinguish LL and HL
    # add 'group4' to have only 4 groups
    # describe questionnaires information, such as depression, MMSE and others

    df = pd.read_excel('/Users/kezhang/ownCloud/Suicide_UG/raw_data_backup/questionnaires.xlsx', sheetname='July 2017 UG DATA')
    df['group5'] = np.where(df['COMMENT'] == 'ATTEMPTER', np.where(df['MAX LETHALITY'] < 4, 'AttempterLL', 'AttempterHL'), df['COMMENT'])
    df['group4'] = df['COMMENT']
    df.to_csv('/Users/kezhang/ownCloud/Suicide_UG/UG_clean_updated/questionnaires.csv', index = False)



    book = load_workbook("/Users/kezhang/ownCloud/Suicide_UG/UG_clean_updated/demo_summary.xlsx")
    writer = pd.ExcelWriter("/Users/kezhang/ownCloud/Suicide_UG/UG_clean_updated/demo_summary.xlsx", engine = 'openpyxl')
    writer.book = book

    question_bygroup5 = df.groupby('group5').describe(include='all')
    question_bygroup4 = df.groupby('group4').describe(include='all')

    question_bygroup5.to_excel(writer, 'group5_questionnaires')
    question_bygroup4.to_excel(writer, 'group4_questionnaired')
    writer.save()
    writer.close()


def punishType():
    ###code baseline as punishType condition 0###

    df = pd.read_csv('C:\\Users\\ke\\ownCloud\\Suicide_UG\\UG_clean_data\\all_data.csv', encoding = "ISO-8859-1")
    df['PunishingType'] = np.where(df['PunishingType'].isnull(), 0, df['PunishingType'])
    print(df['PunishingType'])
    # df.to_csv('C:\\Users\\ke\\ownCloud\\Suicide_UG\\UG_clean_data\\UG_clean_data\\all_data.csv', index = False)



def byGroup_condition_accept():
    df = pd.read_csv('/Users/kezhang/ownCloud/Suicide_UG/UG_clean_data/all_data.csv', encoding = "ISO-8859-1")
    df['ReappraisalDirection'].fillna(0, inplace = True)
    ct = pd.crosstab([df.group5, df.ReappraisalDirection, df.fairness], df.AcceptOffer)
    ct1 = pd.crosstab([df.group4, df.ReappraisalDirection, df.fairness], df.AcceptOffer)
    ct.to_excel('/Users/kezhang/ownCloud/Suicide_UG/UG_clean_data/group5.xlsx')
    ct1.to_excel('/Users/kezhang/ownCloud/Suicide_UG/UG_clean_data/group4.xlsx')

    df_byGroup = df.groupby('id')
    print(df_byGroup)

