from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd 
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score,confusion_matrix


def home(request):
    return render(request,'main.html')
def home1(request):
    return render(request,'index.html')
def home2(request):
    return render(request,'predict.html')
def result1(request):
    data1=pd.read_csv(r"C:\Users\POOJA.K\Documents\dsp(assignment)\ipl\matches.csv")
    data2=pd.read_csv(r"C:\Users\POOJA.K\Documents\dsp(assignment)\ipl\deliveries.csv")
    total_score=data2.groupby(["match_id","inning"]).sum()["total_runs"].reset_index()
    total_score=total_score[total_score["inning"]==1]
    data1=data1.merge(total_score[["match_id","total_runs"]],left_on='id',right_on='match_id')

    match_data=data1[["match_id",'city','total_runs','winner']]
    match_data=match_data.merge(data2,on='match_id')
    match_data=match_data[match_data["inning"]==2]
    match_data["current_Score"]=match_data.groupby('match_id').cumsum()['total_runs_y']
    match_data["runs_left"]=match_data["total_runs_x"]-match_data["current_Score"]
    match_data["batting_team"]=match_data["batting_team"].replace(to_replace="Delhi Daredevils", value="Delhi Capitals")
    match_data["batting_team"]=match_data["batting_team"].replace(to_replace="Deccan Chargers", value="Sunrisers Hyderabad")
    match_data["batting_team"]=match_data["batting_team"].replace(to_replace="Pune Warriors", value="Rising Pune Supergiants")
    match_data["batting_team"]=match_data["batting_team"].replace(to_replace="Rising Pune Supergiant", value="Rising Pune Supergiants")
    match_data["bowling_team"]=match_data["bowling_team"].replace(to_replace="Delhi Daredevils", value="Delhi Capitals")
    match_data["bowling_team"]=match_data["bowling_team"].replace(to_replace="Deccan Chargers", value="Sunrisers Hyderabad")
    match_data["bowling_team"]=match_data["bowling_team"].replace(to_replace="Pune Warriors", value="Rising Pune Supergiants")
    match_data["bowling_team"]=match_data["bowling_team"].replace(to_replace="Rising Pune Supergiant", value="Rising Pune Supergiants")
    match_data["winner"]=match_data["winner"].replace(to_replace="Delhi Daredevils", value="Delhi Capitals")
    match_data["winner"]=match_data["winner"].replace(to_replace="Deccan Chargers", value="Sunrisers Hyderabad")
    match_data["winner"]=match_data["winner"].replace(to_replace="Pune Warriors", value="Rising Pune Supergiants")
    match_data["winner"]=match_data["winner"].replace(to_replace="Rising Pune Supergiant", value="Rising Pune Supergiants")
    match_data["balls_left"]=120-(match_data['over']*6+match_data['ball'])
    match_data['player_dismissed']=match_data['player_dismissed'].fillna("0")
    match_data['player_dismissed']=match_data['player_dismissed'].apply(lambda x:"0" if x=="0" else "1")
    match_data['player_dismissed']=match_data['player_dismissed'].astype(int)
    wickets=match_data.groupby("match_id").cumsum()['player_dismissed'].values
    match_data['wickets']=10-wickets
    match_data["crr"]=(match_data["current_Score"]*6)/(120-match_data["balls_left"])
    match_data["rrr"]=(match_data["runs_left"]*6)/match_data["balls_left"]
    def result(row):
        return 1 if row['batting_team']==row['winner'] else 0
    match_data['result']=match_data.apply(result, axis=1)
    data=match_data[["batting_team","bowling_team","city","runs_left","balls_left","wickets","total_runs_x","crr","rrr","result"]]
    label1=data["batting_team"].value_counts().reset_index()
    label3=data["city"].value_counts().reset_index()
    data.dropna(inplace=True)
    data=data[data['balls_left']!=0]
    labelencoder_x=LabelEncoder()
    data["batting_team"]=labelencoder_x.fit_transform(data["batting_team"])
    data["bowling_team"]=labelencoder_x.fit_transform(data["bowling_team"])
    data["city"]=labelencoder_x.fit_transform(data["city"])
    x=data.iloc[:,:-1]
    y=data.iloc[:,-1]
    x_train,x_test,y_train,y_test=train_test_split(x,y, test_size=0.3, random_state=1)
    tree_model=DecisionTreeClassifier(criterion="entropy")
    tree_model.fit(x_train,y_train)
    label2=x["batting_team"].value_counts().reset_index()
    label4=x["city"].value_counts().reset_index()
    team_label=pd.DataFrame({'index':label1['index'],'INDEX':label2['index']})
    city_label=pd.DataFrame({'index':label3['index'],'INDEX':label4['index']})
    
    bat_team=str(request.GET['t1'])
    bowl_team=str(request.GET['t2'])
    city=str(request.GET['t3'])
    target=int(request.GET['t4'])
    present_score=int(request.GET['t5'])
    wickets=int(request.GET['t6'])
    overs_compleated=int(request.GET['t7'])
    ball=float(request.GET['t8'])
    
    citi=city_label["INDEX"][city_label[city_label["index"]==city].index]
    team1=team_label["INDEX"][team_label[team_label["index"]==bat_team].index]
    team2=team_label["INDEX"][team_label[team_label["index"]==bowl_team].index]
    runs_left=target-present_score
    balls_left=120-((overs_compleated*6)+ball)
    rrr=(runs_left*6)/balls_left
    crr=(present_score*6)/((overs_compleated*6)+ball)
    output=tree_model.predict([[citi,team1,team2,runs_left,balls_left,wickets,target,crr,rrr]])
    if(output==any(team1)):
        a=bat_team
    else:
        a=bowl_team
    
    return render(request,'index.html',{"result":a})

def result2(request):
    matches=pd.read_csv(r"C:\Users\POOJA.K\Documents\dsp(assignment)\ipl\matches.csv")
    teams=pd.read_csv(r"C:\Users\POOJA.K\Documents\dsp(assignment)\ipl\teamwise_home_and_away.csv")
    matches.drop(["Season","date","result","win_by_runs","win_by_wickets","player_of_match","venue","umpire1","umpire2","umpire3"], axis=1, inplace=True)
    matches=matches.merge(teams,left_on="team1", right_on="team")
    matches["winner"]=matches["winner"].fillna("tie")
    matches["team1"]=matches["team1"].replace(to_replace="Delhi Daredevils", value="Delhi Capitals")
    matches["team1"]=matches["team1"].replace(to_replace="Deccan Chargers", value="Sunrisers Hyderabad")
    matches["team1"]=matches["team1"].replace(to_replace="Pune Warriors", value="Rising Pune Supergiants")
    matches["team1"]=matches["team1"].replace(to_replace="Rising Pune Supergiant", value="Rising Pune Supergiants")
    matches["team2"]=matches["team2"].replace(to_replace="Delhi Daredevils", value="Delhi Capitals")
    matches["team2"]=matches["team2"].replace(to_replace="Deccan Chargers", value="Sunrisers Hyderabad")
    matches["team2"]=matches["team2"].replace(to_replace="Pune Warriors", value="Rising Pune Supergiants")
    matches["team2"]=matches["team2"].replace(to_replace="Rising Pune Supergiant", value="Rising Pune Supergiants")
    matches["winner"]=matches["winner"].replace(to_replace="Delhi Daredevils", value="Delhi Capitals")
    matches["winner"]=matches["winner"].replace(to_replace="Deccan Chargers", value="Sunrisers Hyderabad")
    matches["winner"]=matches["winner"].replace(to_replace="Pune Warriors", value="Rising Pune Supergiants")
    matches["winner"]=matches["winner"].replace(to_replace="Rising Pune Supergiant", value="Rising Pune Supergiants")
    matches["winner"]=matches["toss_winner"].replace(to_replace="Delhi Daredevils", value="Delhi Capitals")
    matches["winner"]=matches["toss_winner"].replace(to_replace="Deccan Chargers", value="Sunrisers Hyderabad")
    matches["winner"]=matches["toss_winner"].replace(to_replace="Pune Warriors", value="Rising Pune Supergiants")
    matches["winner"]=matches["toss_winner"].replace(to_replace="Rising Pune Supergiant", value="Rising Pune Supergiants")
    matches.drop(matches[matches["city"].isna()].index, axis=0, inplace=True)
    x=matches.drop(["winner","id","team"],axis=1)
    y=matches.iloc[:,7]
    label1=matches["team1"].value_counts().reset_index()
    label5=matches["city"].value_counts().reset_index()
    label=LabelEncoder()
    x["city"]=label.fit_transform(x["city"])
    x["team1"]=label.fit_transform(x["team1"])
    x["team2"]=label.fit_transform(x["team2"])
    x["toss_winner"]=label.fit_transform(x["toss_winner"])
    x["toss_decision"]=label.fit_transform(x["toss_decision"])
    y[:]=label.fit_transform(y[:])
    y=y.astype(int)
    x_train,x_test,y_train,y_test=train_test_split(x,y, test_size=0.3, random_state=1)
    tree_model=DecisionTreeClassifier(criterion="entropy")
    tree_model.fit(x_train,y_train)
    label2=x["team1"].value_counts().reset_index()
    label6=x["city"].value_counts().reset_index()
    label6=label6.merge(label5,on="city")
    label6.drop("city",axis=1,inplace=True)
    label6.rename(columns={"index_x":"team","index_y":"city_label"},inplace=True)
    labels=label1.merge(label2, on="team1")
    labels.drop("team1",axis=1,inplace=True)
    labels.rename(columns={"index_x":"team","index_y":"team_label"},inplace=True)

    city=str(request.GET['t1'])
    batting_team=str(request.GET['t2'])
    bowling_team=str(request.GET['t3'])
    toss_winner=str(request.GET['t4'])
    toss_decision=str(request.GET['t5'])
    dl_applied=int(request.GET['t6'])
    home_matches=int(request.GET['t7'])
    home_wins=int(request.GET['t8'])
    away_matches=int(request.GET['t9'])
    away_wins=int(request.GET['t10'])

    citi=label6["team"][label6[label6["city_label"]==city].index]
    team1=labels["team_label"][labels[labels["team"]==batting_team].index]
    team2=labels["team_label"][labels[labels["team"]==bowling_team].index]
    tosswinner=labels["team_label"][labels[labels["team"]==toss_winner].index]
    tossdecision=("0" if toss_decision=="field" else "1")
    home_win_percentage=(home_wins/home_matches)*100
    away_win_percentage=(away_wins/away_matches)*100
    output=tree_model.predict([[citi,team1,team2,tosswinner,tossdecision,dl_applied,home_wins,away_wins,home_matches,away_matches,home_win_percentage,away_win_percentage]])
    a=labels["team"][labels[labels["team_label"]==output[0]].index].values
    return render(request,'predict.html',{"result":a[0]})
# Create your views here.
