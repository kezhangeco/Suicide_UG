
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