import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import chisquare

def main_fairness():
    #check the main effect of fairness, whether people accept more fair offer in terms of percentage.
    #5 levels of fairness for the offers (1 = 50/50; 2 = 60/40; 3 = 70/30; 4 = 8/2; 5 = 90/10);
    #fair = 5-5, 6-4;
    #unfair = 7-3, 8-2, 9 -1

    # df = pd.read_csv('/Users/kezhang/ownCloud/Suicide_UG/UG_clean_data/all_data.csv', encoding="ISO-8859-1")
    df = pd.read_csv('C:\\Users\\ke\\ownCloud\\Suicide_UG\\UG_clean_data\\all_data.csv', encoding="ISO-8859-1")
    df['fairness']= np.where((df['Fairness_score'] == 1) | (df['Fairness_score'] == 2), 'fair', 'unfair')
    df.to_csv('C:\\Users\\ke\\ownCloud\\Suicide_UG\\UG_clean_data\\all_data.csv', index=False)

    fairCount = df.groupby(['fairness', 'AcceptOffer']).size().unstack(fill_value=0)
    print(fairCount)
    fairCount.to_csv("/Users/kezhang/ownCloud/Suicide_UG/UG_clean_data/fairness.csv")

    #bar graph
    reject_fair = fairCount.iat[0,0]/(fairCount.iat[0,0]+fairCount.iat[0,1])
    reject_unfair = fairCount.iat[1,0]/(fairCount.iat[1,0]+fairCount.iat[1,1])
    y = [reject_fair, reject_unfair]
    print('percentage of fairness trial vs unfair trial',y)
    groups = ['reject_fair', 'reject_unfair']
    x_pos = np.arange(len(groups))
    plt.bar(x_pos,y,align='center')
    plt.xticks(x_pos,groups)

    ax = plt.gca()
    ax.set_ylim([0, 1])
    plt.show()

def ttest_offer_acceptance():
    #Are people significantly accepting more fair offers than unfair offers?
    #in total population
    df = pd.read_csv('C:\\Users\\ke\\ownCloud\\Suicide_UG\\UG_clean_data\\all_data.csv', encoding="ISO-8859-1")
    fair_accept = df.groupby(['id', 'AcceptOffer', 'fairness']).size()
    fair_accept.to_csv('C:\\Users\\ke\\ownCloud\\Suicide_UG\\UG_clean_data\\acceptance_describe.csv')


def byGroup():
    # new var identifies the subject's group: control, depressed_control, ideator, AttempterHL, AttempterLL

    df = pd.read_csv('/Users/kezhang/ownCloud/Suicide_UG/UG_clean_data/all_data.csv', encoding = "ISO-8859-1")
    df["group"] = np.where(df['PATTYPE'] == 'CONTROL', 'control', np.where(df['PATTYPE'] == 'DEPRESSION', 'depression',
                                                                           np.where(df['COMMENT'] == 'IDEATOR', 'ideator',
                                                                                    np.where(df['COMMENT'] == 'IDEATOR-ATTEMPTER', np.where(df['MAXLETHALITY'] < 4, 'AttempterLL', 'AttempterHL'),
                                                                                             np.where(df['COMMENT'] == 'ATTEMPTER', np.where(df['MAXLETHALITY'] < 4, 'AttempterLL', 'AttempterHL'), 'NA')))))
    df.to_csv('/Users/kezhang/ownCloud/Suicide_UG/UG_clean_data/all_data.csv', encoding = "ISO-8859-1", index = False)

def demo_description():
    # add 'group' variable into demographic data
    # describe demographic info, mean, median, sd...

    df = pd.read_csv('/Users/kezhang/ownCloud/Suicide_UG/new_data/ug_demos.csv', encoding = "ISO-8859-1")
    df["group"] = np.where(df['PATTYPE'] == 'CONTROL', 'control', np.where(df['PATTYPE'] == 'DEPRESSION', 'depression',
                                                                           np.where(df['COMMENT'] == 'IDEATOR',
                                                                                    'ideator',
                                                                                    np.where(df[
                                                                                                 'COMMENT'] == 'IDEATOR-ATTEMPTER',
                                                                                             np.where(
                                                                                                 df['MAXLETHALITY'] < 4,
                                                                                                 'AttempterLL',
                                                                                                 'AttempterHL'),
                                                                                             np.where(df[
                                                                                                          'COMMENT'] == 'ATTEMPTER',
                                                                                                      np.where(df[
                                                                                                                   'MAXLETHALITY'] < 4,
                                                                                                               'AttempterLL',
                                                                                                               'AttempterHL'),
                                                                                                      'NA')))))
    df.to_csv('/Users/kezhang/ownCloud/Suicide_UG/UG_clean_data/ug_demos.csv', index = False)

    var_ls = ['group','BASELINEAGE', "SUICIDEAGE", 'SUICID2AGE', 'MAXLETHALITY', 'EDUCATION', 'GENDERTEXT', 'MARITALTEXT']

    df_demo_groups = df.groupby('group')[var_ls].groups

    print(df_demo_groups)

    attempterHL = df[var_ls][df_demo_groups['AttempterHL']]
    attempterLL = df[var_ls][df_demo_groups['AttempterLL']]
    depression = df[var_ls][df_demo_groups['depression']]
    ideator = df[var_ls][df_demo_groups['ideator']]


demo_description()

def questionnaires_description():
    # add 'group' to distinguish LL and HL
    # describe questionnaires information, such as depression, MMSE and others

    df = pd.read_excel('C:\\Users\\ke\\ownCloud\\Suicide_UG\\raw_data_backup\\questionnaires.xlsx', sheetname='July 2017 UG DATA')
    df['group'] = np.where(df['COMMENT'] == 'ATTEMPTER', np.where(df['MAX LETHALITY'] < 4, 'AttempterLL', 'AttempterHL'), df['COMMENT'])
    df.to_csv('C:\\Users\\ke\\ownCloud\\Suicide_UG\\questionnaires.csv', index = False)

    question_bygroup = df.groupby('group').describe()
    question_bygroup.to_csv('C:\\Users\\ke\\ownCloud\\Suicide_UG\\UG_clean_data\\questionnaire_describe.csv')


def punishType():
    ###code baseline as punishType condition 0###

    df = pd.read_csv('C:\\Users\\ke\\ownCloud\\Suicide_UG\\UG_clean_data\\all_data.csv', encoding = "ISO-8859-1")
    df['PunishingType'] = np.where(df['PunishingType'].isnull(), 0, df['PunishingType'])
    print(df['PunishingType'])
    # df.to_csv('C:\\Users\\ke\\ownCloud\\Suicide_UG\\UG_clean_data\\UG_clean_data\\all_data.csv', index = False)





