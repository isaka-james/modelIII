import pandas as pd
import os
from tabulate import tabulate
import requests

    
# The  INTROS 
# Check if the USER is enterested in TZ or UK
choice=input("\n\n   CHOOSE LEAGUE\n    1. Tanzania Premier League \n    2. England Premier League\n    3. Egypt Premier League\n    4. France Ligue1 \n\n     => ") 

# Taking different Leagues
if choice=='1':
    url=requests.get("https://www.soccerstats.com/latest.asp?league=tanzania#")
    teams_no=16
    # Converts to Pandas DataFrame
    data=url.text
    df1=pd.read_html(data)
    table_a=df1[15]
    # tOH => Have the standings of Home
    tOH=df1[41].iloc[:,[1,2,3]]
    # tOA => Have the standings of away
    tOA=df1[42].iloc[:,[1,2,3]]
if choice=='2':
    url=requests.get("https://www.soccerstats.com/latest.asp?league=england#")
    teams_no=20
    # Converts to Pandas DataFrame
    data=url.text
    df1=pd.read_html(data)
    table_a=df1[23]
    # tOH => Have the standings of Home
    tOH=df1[53].iloc[:,[1,2,3]]
    # tOA => Have the standings of away
    tOA=df1[54].iloc[:,[1,2,3]]
elif choice=='3':
    url=requests.get("https://www.soccerstats.com/latest.asp?league=egypt#")
    teams_no=18
    # Converts to Pandas DataFrame
    data=url.text
    df1=pd.read_html(data)
    table_a=df1[22]
    # tOH => Have the standings of Home
    tOH=df1[49].iloc[:,[1,2,3]]
    # tOA => Have the standings of away
    tOA=df1[50].iloc[:,[1,2,3]]

elif choice=='4':
    url=requests.get("https://www.soccerstats.com/latest.asp?league=france#")
    teams_no=20
    # Converts to Pandas DataFrame
    data=url.text
    df1=pd.read_html(data)
    table_a=df1[23]
    # tOH => Have the standings of Home
    tOH=df1[53].iloc[:,[1,2,3]]
    # tOA => Have the standings of away
    tOA=df1[54].iloc[:,[1,2,3]]
else:
    print("Invalid choice!!!")




# These are the GLOBAL variables that we'll use through out'
# Soup => Have the standings table filtered
soap=table_a.iloc[:,[1,2,3,4,5,6,7,8,9,11,12,13,14]]


class display:
    def __init__(self,soup):
        self.soup=soup
    # The logic behind I want to find both,
    # from the main table,
    # And the HOME and AWAY table.
    # The reason is that the Teams are not,
    # Proper oriented from the scrapted page.
    def tableOfModel_iii(data,name,teamA,teamB):
        print("")
        print("            MODEL III ")
        if data[1]>0.5:
            x=True
            xv=data[1]
        else:
            x=False
            xv=data[1]
        if data[2]>0.5:
            y=True
            yv=data[2]
        else:
            y=False
            yv=data[2]            
        if data[3]>0.5:
            z=True
            zv=data[3]
        else:
            z=False
            zv=data[3]
        team=name["normals"]["team_name"]
        table1=[["CODE","STATE"],
                     ["PPG",x],
                     ["G",y],
                     ["R",z]]
        table2=[["CODE","VALUE"],
                       ["PPG",xv],
                       ["G",yv],
                       ["R",zv],
                       ["SUM",data[4]]]  
        winner=(data[4])/3
        if winner>0.52:
            nameOfWinner=teamA["normals"]["team_name"]
        elif winner<0.48:
            nameOfWinner=teamB["normals"]["team_name"]
        else:
            nameOfWinner="DRAW"
        print(f"  For the {team} \n") 
        print(" The State table")  
        print(tabulate(table1,headers="firstrow")) 
        print("") 
         
        print(" The Probability Table ") 
        print(tabulate(table2,headers="firstrow"))
        print("")
        print(f"     Winner = {nameOfWinner}")
        print("")
        
    def teamsListMain(soap):
        theList=dict(soap[1])
        for i in range(teams_no):
            print(f"      {i+1}. {theList[i+1]}")
    def teamsListHome(soap):
        theList=dict(soap[1])
        init=2
        for i in range(teams_no):
            print(f"      {i+1}. {theList[init+i]}")
    def teamsListAway(soap):
        theList=dict(soap[1])
        init=2
        for i in range(teams_no):
            print(f"      {i+1}. {theList[init+i]}")
        
    def tableOfModel_ii(table,teamA,teamB,status):
        nameOfA=teamA["normals"]["team_name"]
        nameOfB=teamB["normals"]["team_name"]
        sum=table[1]+table[2]+table[3]+table[4]+table[5]+table[6]
        if sum<0.5:
            R1="Lose"
            R2="Win"
        elif sum>0.5:
            R1="Win"
            R2="Lose"
        else:
            R1="Draw"
            R2="Draw"
         
        tbl={nameOfA:{R1},nameOfB:{R2}}
        print("                     MODEL II \n         The Results of the MODEL!! \n")
        print(tabulate(tbl,headers="keys"))
        print("")
        print(f" The chance {nameOfA} to win is {sum}.")
        
        print("\n\n")
        tbl2=[["CODE","STATE"],
              ["PPG",status[5]["ppg"]],
              ["G", status[5]["goals"]],
              ["L8", status[5]["last"]],
              ["RTO", status[5]["rto"]]]
        print(f"The OTHER DATAS generated by the MODEL II for {nameOfA} .")
        print(tabulate(tbl2,headers="firstrow"))

        
class test:
    def convertToInt(x):
        try:
            y=int(x)
        except:
            raise Exception("   Expected integer type!!!")
        return y
        
        
        
        
class algorithm:
    def __init__(self,soap,choices):
        self.soap,self.choices=soap,choices
    def getProbability_iii(data):
        sum=data[1]+data[2]+data[4]
        ppg_r=data[1]
        kufunga_r=data[2]
        ratio_r=data[4]
        dict={1:ppg_r,2:kufunga_r,3:ratio_r,4:sum}
        return dict
    def extractDataMain(soap,choices):
        dataPurified=soap.iloc[choices]
        output1=dict(dataPurified)
        results={ "team_name": output1[1],
                         "game_played": int(output1[2]),
                         "win": int(output1[3]),
                         "draw": int(output1[4]),
                         "lose":int(output1[5]),
                         "goal_for": int(output1[6]),
                         "goal_against": int(output1[7]),
                         "goal_difference": int(output1[8]),
                         "points": int(output1[9]),
                         "point_per_game": float(output1[11]),
                         "last_8_ppg": float(output1[12]),
                         "clean_sheet": output1[13],
                         "failed_to_score": output1[14]
        }
        return results
    def extractDataHome(soap,choices):
        soup=soap.iloc[choices+1]
        home=dict(soup)
        results={ "team_name": home[1],
                  "ratio": float(home[3])/float(home[2]),
        }
        return results
        
    def extractDataAway(soap,choices):
        soup=soap.iloc[choices+1]
        away=dict(soup)
        results={ "team_name": away[1],
                  "ratio": float(away[3])/float(away[2]),
        }
        return results
        
    def check_ratios(data,tA_g,tB_g):
     ## The status (scrapted[5]) will be used to the model III +
      if data[1]>0:
         ppg= data[1]
         ppg_status=True
      else:
         ppg=data[1]
         ppg_status=False
      if tA_g>=0 and tB_g>=0:
         if tA_g>tB_g:
             team_goal_diff=tA_g - tB_g
             team_goal_diff_status=True
         else:
             team_goal_diff=tB_g - tA_g
             team_goal_diff_status=False
      elif tA_g>=0 and tB_g<0:
         team_goal_diff=1
         team_goal_diff_status=True
      elif tA_g<0 and tB_g>=0:
         team_goal_diff=-1
         team_goal_diff_status=False
      elif tA_g<0 and tB_g<0:
         if tA_g>tB_g:
             team_goal_diff=1
             team_goal_diff_status=True
         elif tA_g<tB_g:
             team_goal_diff=-1
             team_goal_diff_status=False
         else:
             raise Exception(f" Model Stopped")
      else:
         raise Exception (" Model stopped")
      if data[3]>0:
         last=data[3]
         last_status=True
      else:
         last=data[3]
         last_status=False
      if data[4]>0:
         rto=data[4]
         rto_status=True
      else:
         rto=data[4]
         rto_status=False 
      status={"ppg":ppg_status,"goals":team_goal_diff_status,"last":last_status,"rto":rto_status}
      scrapted={1:ppg,2:team_goal_diff,3:last,4:rto,5:status}
      return scrapted


    def getProbability(abc,a,b,r):
      if abc[1]>1:
          ppg_prob=0.2
      elif abc[1]==0:
          ppg_prob=0.1
      else:
         ppg_prob=0
      if abc[2]>0:
          goals_diff=0.05
      elif abc[2]==0:
          goals_diff=0.025
      else:
          goals_diff=0
      if abc[3]>0:
         last=0.2
      elif abc[3]==0:
          last=0.1
      else:
         last=0
      if abc[4]>0:
          ratio=0.05
      elif abc[4]==0:
          ratio=0.025
      else:
          ratio=0
      total=a+b
      prob_a=(a/total)*0.2
      last_3=r*0.3
      finalize={1:ppg_prob,2:goals_diff,3:last,4:ratio,5:prob_a,6:last_3}
      return finalize


def main():
    os.system("clear")
    soup=dict(soap)
    
    # The Animations of taking the desired,
    # Teams
    print("\n    CHOOSE YOUR TEAM:: standings-home")
    display.teamsListMain(soap)
    choose1=input("\n   => ")
    ch1=test.convertToInt(choose1)
    os.system("clear")
    print("\n    CHOOSE YOUR TEAM:: standings-away")
    display.teamsListMain(soap)
    choose4=input("\n   => ")
    ch4=test.convertToInt(choose4)
    os.system("clear")    
    print("\n    CHOOSE YOUR TEAM:: home")
    display.teamsListHome(tOH)
    choose2=input("\n   => ")
    ch2=test.convertToInt(choose2)
    os.system("clear")
    print("\n    CHOOSE YOUR TEAM:: away")
    display.teamsListAway(tOA)
    choose3=input("\n   => ")
    ch3=test.convertToInt(choose3)
    os.system("clear")
    
    # Making the dictionary full of data
    theMainA=algorithm.extractDataMain(soap,ch1)
    theMainB=algorithm.extractDataMain(soap,ch4)
    theHome=algorithm.extractDataHome(tOH,ch2)
    theAway=algorithm.extractDataAway(tOA,ch3)
    
    #Grouping data into two dictionaries
    teamA={"normals":theMainA,
             "home": theHome
            }
    teamB={ "normals": theMainB,
             "away": theAway
            }
            
    # Start getting the differences Model II
    ppg_d=teamA["normals"]["point_per_game"] - teamB["normals"]["point_per_game"]
    goal_d=teamA["normals"]["goal_difference"] - teamB["normals"]["goal_difference"]
    last_8_d=teamA["normals"]["last_8_ppg"] - teamB["normals"]["last_8_ppg"]
    ratio=teamA["home"]["ratio"] - teamB["away"]["ratio"]
    
    # Get the Probability ratios model iii
    ppg_ratio=(teamA["normals"]["point_per_game"])/(teamA["normals"]["point_per_game"] + teamB["normals"]["point_per_game"])
    kufunga=(teamA["normals"]["goal_for"])/(teamA["normals"]["goal_for"] + teamB["normals"]["goal_for"])
    kufungwa=(teamA["normals"]["goal_against"])/(teamA["normals"]["goal_against"] + teamB["normals"]["goal_against"])
    ratio_ratio=(teamA["normals"]["last_8_ppg"])/(teamA["normals"]["last_8_ppg"] + teamB["normals"]["last_8_ppg"])
    
    
    # We're going to take The odds'
    print("    Enter the odds:: \n ")
    oddsA=input(f" Odds for {teamA['normals']['team_name']} ::  ")
    oddsB=input(f" Odds for {teamB['normals']['team_name']} :: ")
    os.system("clear")
    
    
    # We're going to take the last 3 games
    print(" The last 3 games ( Points) ")
    last3={}
    last_3={}
    for i in range(3):
        last3[i]=input("  For Team A :: ")
        if last3[i]=='w':
           last_3[i]=3
        elif last3[i]=='l':
           last_3[i]=0
        else:
           last_3[i]=1
    last_3_ratio=(last_3[0]+last_3[1]+last_3[2])/3
    
    # Put the difference into a dictionary
    # For model II
    scrap={1:ppg_d,2:goal_d,3:last_8_d,4:ratio}
    
    # Put Probability into dictionary
    # For model III
    scrap_prob={1:ppg_ratio,2:kufunga,3:kufungwa,4:ratio_ratio}
    
    # Interpretation of Model iii
    model_iii=algorithm.getProbability_iii(scrap_prob)
    display.tableOfModel_iii(model_iii,teamA,teamA,teamB)
          
    
    # Interpretation of Model ii
    abc1=1/(float(oddsA))
    abc2=1/(float(oddsB))
    print("\n\n\n")
    answr=algorithm.check_ratios(scrap,teamA["normals"]["goal_difference"],teamB["normals"]["goal_difference"])
    model1=algorithm.getProbability(answr,abc1,abc2,last_3_ratio)
    display.tableOfModel_ii(model1,teamA,teamB,answr)
    
main()
   
         
