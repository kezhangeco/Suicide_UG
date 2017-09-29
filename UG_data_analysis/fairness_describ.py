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
