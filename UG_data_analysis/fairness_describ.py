import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from openpyxl import load_workbook
import xlsxwriter



def main_fairness():
    #check the main effect of fairness, whether people accept more fair offer in terms of percentage.
    #5 levels of fairness for the offers (1 = 50/50; 2 = 60/40; 3 = 70/30; 4 = 8/2; 5 = 90/10);
    #fair = 5-5, 6-4;
    #unfair = 7-3, 8-2, 9 -1

    df = pd.read_csv('/Users/kezhang/ownCloud/Suicide_UG/UG_clean_updated/ug_all_task_data.csv', encoding="ISO-8859-1")
    df['fairness']= np.where((df['Fairness_score'] == 1) | (df['Fairness_score'] == 2), 'fair', 'unfair')
    df.to_csv('/Users/kezhang/ownCloud/Suicide_UG/UG_clean_updated/ug_all_task_data.csv', index=False)

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


def punishType():
    ##recode punishing type
    ##recode empty cell as the baseline

    df = pd.read_csv('/Users/kezhang/ownCloud/Suicide_UG/UG_clean_updated/merged_panels/all_task_data.csv',
                     encoding = "ISO-8859-1")
    df['PunishingType'] = np.where(df['PunishingType'].isnull(), 'baseline', df['PunishingType'])
    print(df['PunishingType'])
    df.to_csv('/Users/kezhang/ownCloud/Suicide_UG/UG_clean_updated/ug_all_task_data.csv', index = False)

def byGroup_reappraisal_fair():
    ##How each group accept fairness offer under different reapprisal condition: baseline, punish, empathy.

    df = pd.read_csv('/Users/kezhang/ownCloud/Suicide_UG/UG_clean_updated/ug_all_task_data.csv', encoding = "ISO-8859-1")
    df['ReappraisalDirection'].fillna('baseline', inplace = True)
    df['ReappraisalDirection'] = np.where(df['ReappraisalDirection'] == 1, 'punish',
                                          np.where(df['ReappraisalDirection'] == 2, 'empathy', df['ReappraisalDirection']))
    ct_group5_reappraisal = pd.crosstab([df.group5, df.ReappraisalDirection, df.fairness], df.AcceptOffer, normalize='index')
    ct_group4_reappraisal = pd.crosstab([df.group4, df.ReappraisalDirection, df.fairness], df.AcceptOffer, normalize='index')

    ct_group5 = pd.crosstab([df.group5, df.fairness], df.AcceptOffer, normalize='index')
    ct_group4 = pd.crosstab([df.group4, df.fairness], df.AcceptOffer, normalize='index')

    workbook = xlsxwriter.Workbook('/Users/kezhang/ownCloud/Suicide_UG/UG_clean_updated/fair_reappraisal.xlsx')
    workbook.close()

    book = load_workbook('/Users/kezhang/ownCloud/Suicide_UG/UG_clean_updated/fair_reappraisal.xlsx')
    writer = pd.ExcelWriter('/Users/kezhang/ownCloud/Suicide_UG/UG_clean_updated/fair_reappraisal.xlsx', engine='openpyxl')
    writer.book = book

    ct_group5_reappraisal.to_excel(writer, 'group5_reappraisal')
    ct_group4_reappraisal.to_excel(writer, 'group4_reappraisal')
    ct_group5.to_excel(writer, 'group5')
    ct_group4.to_excel(writer, 'group4')
    writer.save()
    writer.close()


byGroup_reappraisal_fair()