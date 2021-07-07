# -*- coding: utf-8 -*-
"""
Created on Tue Jul  6 15:42:18 2021

@author: Manish.
"""

import random
import os
import glob
import time

# game contstants
noRunsRequired = -1
unlimitedOvers = -1
allOutWickets = 10 # can reduce this down for testing
balls = ["0", "1", "2", "3", "4", "6", "OUT"]
decisions = ["Not Out!","Bowled!","Caught!","LBW!","Run Out!","Stumped!","Not Out!"]

# match variables
oversPerTeam = 1
gameRate = 0.01 # seconds between balls
#Checking for teams data
os.chdir('./')
result = glob.glob( '*.csv' )
print('Avaliable teams: ',result)

for i in range(1):
    team1 = int(input("Enter team 1 index: "))
    team1 = result[team1 - 1].replace('.csv', '')
    team2 = int(input("Enter team 2 index: "))
    team2 = result[team2 - 1].replace('.csv', '')
print()
print('Team 1: ',team1)
print('Team 2: ',team2)
print()

def returnToMark():
    """ Function call to simulate the time taken 
        for the bowler to return to their mark """
    time.sleep(gameRate)

def makeDecision():
    """ Function call to simulate the time taken 
        for the umpire to make a decision and add tension to the game """
    time.sleep(gameRate * 2)

def roll(dice):
    """ Function call to simulate either the roll of a dice
        for either the bowl of a ball or an appeal decision """
    if (dice == "bowl"):
        return balls[random.randint(0,len(balls) - 1)]
    elif (dice == "decision"):
        makeDecision()
        return decisions[random.randint(0, len(decisions) - 1)]
    else:
        return "0"
    
def innings(battingTeam,maxOvers,runsRequired):
    """ Function call to simulate a single innings """

    wickets = 0
    score = 0
    bowled = 0
    overs = 0
    unfinishedOverBalls = 0

    while wickets < allOutWickets and \
        (not score > runsRequired or runsRequired == noRunsRequired) and \
        (overs < maxOvers or maxOvers == unlimitedOvers):
        ball = roll("bowl")
        event = ""
        if (ball == "OUT"):
            # print(ball)
            decision = roll("decision")
            event = decision
            if (decision != "Not Out!"):
                wickets = wickets + 1
        else:
            event = "{} run".format(ball)
            if (ball != "1"):
                event = event + "s"

            score = score + int(ball)
            
        bowled = bowled + 1
        unfinishedOverBalls = int(bowled % 10)
        overs = int((bowled - unfinishedOverBalls) / 10)
        # print("{} - {} {}/{} ({}.{} overs)".format(event,battingTeam,score,wickets,overs,unfinishedOverBalls))
        print("{}.{}    {}  {} {}/{} ".format(overs,unfinishedOverBalls,event,battingTeam,score,wickets))
        if unfinishedOverBalls == 0:
            print()
        returnToMark()


    return { "Runs": score, "Wickets": wickets, "Overs": overs, "Balls": unfinishedOverBalls }


#toss
toss = ['Heads','Tails']
tossChoice = random.choice(toss)
#2nd team toss call and generating random option
tossCall = ['Heads', 'Tails']
team2Call = random.choice(tossCall)
#Generating toss
print(team1+" spins the coin \n"+team2+" - "+team2Call+" is the call. And it's "+
      tossChoice)
#Setting up who wont the toss and what they want to choose first.
firstChoice = ['Bat','Bowl']
firstChoiceCall = random.choice(firstChoice)
#Checking if team 2 toss call is same with coin toss or not
if team2Call == tossChoice:
    print()
    print(team2+' won the toss and choose to '+firstChoiceCall+' first !')
    print()
    if firstChoiceCall == 'Bowl':
        team1, team2 = team1, team2
        firstInnings = innings(team1,oversPerTeam,noRunsRequired)
        print("{} score {}/{} in {}.{} overs".format(team1,firstInnings["Runs"],firstInnings["Wickets"],firstInnings["Overs"],firstInnings["Balls"]))
        secondInnings = innings(team2,oversPerTeam,firstInnings["Runs"])
        print("{} score {}/{} in {}.{} overs".format(team2,secondInnings["Runs"],secondInnings["Wickets"],secondInnings["Overs"],secondInnings["Balls"]))
    elif firstChoiceCall == 'Bat':
        team1, team2 = team2, team1
        firstInnings = innings(team1,oversPerTeam,noRunsRequired)
        print("{} score {}/{} in {}.{} overs".format(team1,firstInnings["Runs"],firstInnings["Wickets"],firstInnings["Overs"],firstInnings["Balls"]))
        secondInnings = innings(team2,oversPerTeam,firstInnings["Runs"])
        print("{} score {}/{} in {}.{} overs".format(team2,secondInnings["Runs"],secondInnings["Wickets"],secondInnings["Overs"],secondInnings["Balls"]))
else:
    print()
    print(team1+' won the toss and choose to '+firstChoiceCall+' first !')
    print()
    if firstChoiceCall == 'Bowl':
        team1, team2 = team2, team1
        print('%%%%% 1st Innings %%%%%')
        firstInnings = innings(team1,oversPerTeam,noRunsRequired)
        print("{} score {}/{} in {}.{} overs".format(team1,firstInnings["Runs"],firstInnings["Wickets"],firstInnings["Overs"],firstInnings["Balls"]))
        print()
        print('%%%%% 2nd Innings %%%%%')
        print()
        secondInnings = innings(team2,oversPerTeam,firstInnings["Runs"])
        print("{} score {}/{} in {}.{} overs".format(team2,secondInnings["Runs"],secondInnings["Wickets"],secondInnings["Overs"],secondInnings["Balls"]))
    elif firstChoiceCall == 'Bat':
        team1, team2 = team1, team2
        print('%%%%% 1st Innings %%%%%')
        firstInnings = innings(team1,oversPerTeam,noRunsRequired)
        print("{} score {}/{} in {}.{} overs".format(team1,firstInnings["Runs"],firstInnings["Wickets"],firstInnings["Overs"],firstInnings["Balls"]))
        print()
        print('%%%%% 2nd Innings %%%%%')
        print()
        secondInnings = innings(team2,oversPerTeam,firstInnings["Runs"])
        print("{} score {}/{} in {}.{} overs".format(team2,secondInnings["Runs"],secondInnings["Wickets"],secondInnings["Overs"],secondInnings["Balls"]))
        
if (firstInnings["Runs"] > secondInnings["Runs"]):
    print("{} win by {} runs!".format(team1,firstInnings["Runs"] - secondInnings["Runs"]))
elif (firstInnings["Runs"] < secondInnings["Runs"]):
    print("{} win by {} wickets!".format(team2,10 - secondInnings["Wickets"]))
else:
    print("Tied game!")