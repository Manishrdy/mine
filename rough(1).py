# -*- coding: utf-8 -*-
"""
Created on Tue Jul 27 14:29:14 2021
@author: Manish.
"""

import pandas as pd
import numpy as np
import random
import sys
from tabulate import tabulate

sys.setrecursionlimit(10**6)



outcomes = [0, 1, 2, 3, 4, 6, 'OUT', 'Wide']
outList = ['Stumped', 'Bowled', 'Caught']

battingTeam1 = pd.read_csv('Chennai Super Kings.csv')
bowlingTeam1 = pd.read_csv('Sunrisers Hyderabad.csv')

team1 = battingTeam1.replace('.csv','')
team2 = bowlingTeam1.replace('.csv','')

bowlingPlayers = bowlingTeam1[bowlingTeam1['role'] == "Bowler"]
bowlingPlayers = bowlingPlayers.player
bowlingPlayers = bowlingPlayers.to_list()

battingPlayers = battingTeam1
columns = ['role', 'type', 'total']
battingPlayers.drop(columns, inplace=True, axis=1)
#bowler names
battingPlayers = battingPlayers.values.tolist()

battingPlayerNames = []
battingPlayerRatings = []
for i in battingPlayers:
    battingPlayerNames.append(i[0])
    battingPlayerRatings.append(i[1:])

checkList = []

previousBowler = ''
totalWickets = 0
totalScore = 0
batsmanStrike = battingPlayerNames[0]
batsmanOffStrike = battingPlayerNames[1]
bowlingStats = []
initialScore = 0
initialOut = 0
initialWide = 0
count = 0
initialDotBalls = 0

initialStrikerRuns = 0
intialNonStrikerRuns = 0
initialStrikerBallsCount = 0
initialNonStrikerBallsCount = 0
initialStrikeFour = 0
initialNonStrikeFour = 0
initialStrikeSix = 0
initialNonStrikeSix = 0

batsmenScoreboard = []

def pickBowler():
    bowler = random.choice(bowlingPlayers)
    if bowler != checkList[-1] and checkList.count(bowler) < 2:
        checkList.append(bowler)
        return bowler
    else:
        return pickBowler()
    return bowler

bowlerPresent = random.choice(bowlingPlayers)
checkList.append(bowlerPresent)
bowlerStatsOnetemp = pd.DataFrame({"Bowler":[bowlerPresent],
                                   "Balls":[0],
                                   "Dots":[0],
                                   "Runs":[0],
                                   "Wickets":[0],
                                   "Economy":[0]
    })

b = 0
playerOut = 0
batsman1 = battingPlayerNames[b]
batsman2 = battingPlayerNames[b+1]
batsman1Rating = battingPlayerRatings[b]
batsman2Rating = battingPlayerRatings[b+1]

for i in range(1,101):
    
    if len(str(i)) == 1:
        ball = 'Ball 0'+str(i)+' : '
    else:
        ball = 'Ball '+str(i)+' : '
    
    ballOutcome = random.choices(outcomes, weights=(batsman1Rating), k=1)
    if ballOutcome == [1]:
        initialScore = initialScore + 1
        totalScore = totalScore + 1
    elif ballOutcome == [2]:
        initialScore = initialScore + 2
        totalScore = totalScore + 2
    elif ballOutcome == [3]:
        initialScore = initialScore + 3
        totalScore = totalScore + 3
    elif ballOutcome == [4]:
        initialScore = initialScore + 4
        totalScore = totalScore + 4
    elif ballOutcome == [6]:
        initialScore = initialScore + 6
        totalScore = totalScore + 6
    elif ballOutcome == ['Wide']:
        initialScore = initialScore + 1
        totalScore = totalScore + 1
        initialWide = initialWide + 1
    elif ballOutcome == ['OUT']:
        initialOut = initialOut + 1
        totalWickets = totalWickets + 1
        initialDotBalls = initialDotBalls + 1
    elif ballOutcome == [0]:
        initialDotBalls = initialDotBalls + 1
    else:
        pass
    
    if ballOutcome == ['OUT']:
        print('{} {} to {} : {}'.format(ball,bowlerPresent,batsman1,*ballOutcome))
    elif ballOutcome == ['Wide']:
        print('{} {} to {} : {}'.format(ball,bowlerPresent,batsman1,*ballOutcome))
    elif ballOutcome == [1]:
        print('{} {} to {} : {} {}'.format(ball,bowlerPresent,batsman1,*ballOutcome,'run'))
    else:
        print('{} {} to {} : {} {}'.format(ball,bowlerPresent,batsman1,*ballOutcome,'runs'))
    count = count + 1
    if totalWickets == 10:
        print('     End of innings (Balls '+str(count)+')')
        rr = totalScore / (count / 10)
        print('     Chennai Super Kings     '+str(totalScore)+'/'+str(totalWickets)+'  (RR: {:.2f})'.format(rr))
        break
        
    
    #wideball
    if ballOutcome == ['Wide']:
        wideBallNo = str(i)
        ballOutcome = random.choices(outcomes, weights=(batsman1Rating), k=1)
        
        #First over posibilities 'Ball 0X'
        if len(str(i)) == 1:
            ball = 'Ball 0'+str(i)+' : '
            if ballOutcome == [1]:
                initialScore = initialScore + 1
                totalScore = totalScore + 1
            elif ballOutcome == [2]:
                initialScore = initialScore + 2
                totalScore = totalScore + 2
            elif ballOutcome == [3]:
                initialScore = initialScore + 3
                totalScore = totalScore + 3
            elif ballOutcome == [4]:
                initialScore = initialScore + 4
                totalScore = totalScore + 4
            elif ballOutcome == [6]:
                initialScore = initialScore + 6
                totalScore = totalScore + 6
            elif ballOutcome == ['Wide']:
                initialWide = initialWide + 1
                initialScore = initialScore + 1
                totalScore = totalScore + 1
            elif ballOutcome == ['OUT']:
                initialOut = initialOut + 1
                totalWickets = totalWickets + 1
                initialDotBalls = initialDotBalls + 1
            elif ballOutcome == [0]:
                initialDotBalls = initialDotBalls + 1
            else:
                pass
            
            if ballOutcome == ['OUT']:
                print('{} {} to {} : {}'.format(ball,bowlerPresent,batsman1,*ballOutcome))
            elif ballOutcome == ['Wide']:
                print('{} {} to {} : {}'.format(ball,bowlerPresent,batsman1,*ballOutcome))
            elif ballOutcome == [1]:
                print('{} {} to {} : {}'.format(ball,bowlerPresent,batsman1,*ballOutcome))
            else:
                print('{} {} to {} : {} runs'.format(ball,bowlerPresent,batsman1,*ballOutcome))
            
            # print('{} {} to {} : {} runs'.format(ball,bowlerPresent,batsman1,*ballOutcome))
            if totalWickets == 10:
                print('     End of innings (Balls '+str(count)+')')
                rr = totalScore / (count / 10)
                print('     Chennai Super Kings     '+str(totalScore)+'/'+str(totalWickets)+'  (RR: {:.2f})'.format(rr))
                break
        else: #Rest 90 balls 'Ball 1X'
            ball = 'Ball '+str(i)+' : '
            if ballOutcome == [1]:
                initialScore = initialScore + 1
                totalScore = totalScore + 1
            elif ballOutcome == [2]:
                initialScore = initialScore + 2
                totalScore = totalScore + 2
            elif ballOutcome == [3]:
                initialScore = initialScore + 3
                totalScore = totalScore + 3
            elif ballOutcome == [4]:
                initialScore = initialScore + 4
                totalScore = totalScore + 4
            elif ballOutcome == [6]:
                initialScore = initialScore + 6
                totalScore = totalScore + 6
            elif ballOutcome == ['Wide']:
                initialWide = initialWide + 1
                initialScore = initialScore + 1
                totalScore = totalScore + 1
            elif ballOutcome == ['OUT']:
                initialOut = initialOut + 1
                totalWickets = totalWickets + 1
                initialDotBalls = initialDotBalls + 1
            elif ballOutcome == [0]:
                initialDotBalls = initialDotBalls + 1
            else:
                pass
            
            if ballOutcome == ['OUT']:
                print('{} {} to {} : {}'.format(ball,bowlerPresent,batsman1,*ballOutcome))
            elif ballOutcome == ['Wide']:
                print('{} {} to {} : {}'.format(ball,bowlerPresent,batsman1,*ballOutcome))
            elif ballOutcome == [1]:
                print('{} {} to {} : {} run'.format(ball,bowlerPresent,batsman1,*ballOutcome))
            else:
                print('{} {} to {} : {} runs'.format(ball,bowlerPresent,batsman1,*ballOutcome))
            
            # print('{} {} to {} : {} runs'.format(ball,bowlerPresent,batsman1,*ballOutcome))
            if totalWickets == 10:
                print()
                print('     {}     {}-{}-{}-{}'.format(bowlerPresent,'10',initialDotBalls,initialScore,initialOut))
                print()
                print('     End of innings (Balls '+str(count)+')')
                rr = totalScore / (count / 10)
                print('     Chennai Super Kings     '+str(totalScore)+'/'+str(totalWickets)+'  (RR: {:.2f})'.format(rr))
                break
            
    
    
    #End of every 10 balls presenting score  
    if count % 10 == 0:
        print()
        print('     END of '+str(count)+' balls ('+str(initialScore)+' runs)')
        print('     Chennai Super Kings     '+str(totalScore)+'/'+str(totalWickets))
        rr = totalScore / (count / 10)
        print('     RR: {:.2f}'.format(rr))
        print()
        
        
        if count == 100:
            print()
            print('     End of innings (Balls '+str(count)+')')
            rr = totalScore / (count / 10)
            print('     Chennai Super Kings     '+str(totalScore)+'/'+str(totalWickets)+'  (RR: {:.2f})'.format(rr))
        
        #Reseting over score before the begini of new over.
        initialScore = 0
        initialOut = 0
        initialDotBalls = 0
        #Change of bowler
        bowlerPresent = pickBowler() #bowler
        
        # bowler = random.choice(bowlingPlayers)
        # bowlerPresent = bowler
    
    #Checking weather to rotate strike or not after the end of over and in between the innings
    if ballOutcome == [1]:
        if count % 10 == 0: #overend
            batsman1, batsman2 = batsman1, batsman2
            batsman1Rating, batsman2Rating = batsman1Rating, batsman2Rating
            initialStrikeFour, initialNonStrikeFour = initialStrikeFour, initialNonStrikeFour
            initialStrikeSix, initialNonStrikeSix = initialStrikeSix, initialNonStrikeSix
        else:
            batsman1, batsman2 = batsman2, batsman1
            batsman1Rating, batsman2Rating = batsman2Rating, batsman1Rating
            initialStrikeFour, initialNonStrikeFour = initialNonStrikeFour, initialStrikeFour
            initialStrikeSix, initialNonStrikeSix = initialNonStrikeSix, initialStrikeSix
    elif ballOutcome == [3]:
        if count % 10 == 0: #overend
            batsman1, batsman2 = batsman2, batsman1
            batsman1Rating, batsman2Rating = batsman2Rating, batsman1Rating
            initialStrikeFour, initialNonStrikeFour = initialStrikeFour, initialNonStrikeFour
            initialStrikeSix, initialNonStrikeSix = initialStrikeSix, initialNonStrikeSix
        else:
            batsman1, batsman2 = batsman2, batsman1
            batsman1Rating, batsman2Rating = batsman2Rating, batsman1Rating
            initialStrikeFour, initialNonStrikeFour = initialNonStrikeFour, initialStrikeFour
            initialStrikeSix, initialNonStrikeSix = initialNonStrikeSix, initialStrikeSix
    elif ballOutcome == [0]:
        if count % 10 == 0: #overend
            batsman1, batsman2 = batsman2, batsman1
            batsman1Rating, batsman2Rating = batsman2Rating, batsman1Rating
            initialStrikeFour, initialNonStrikeFour = initialNonStrikeFour, initialStrikeFour
            initialStrikeSix, initialNonStrikeSix = initialNonStrikeSix, initialStrikeSix
        else:
            batsman1, batsman2 = batsman1, batsman2
            batsman1Rating, batsman2Rating = batsman1Rating, batsman2Rating
            initialStrikeFour, initialNonStrikeFour = initialStrikeFour, initialNonStrikeFour
            initialStrikeSix, initialNonStrikeSix = initialStrikeSix, initialNonStrikeSix
    elif ballOutcome == [2]:
        if count % 10 == 0: #overend
            batsman1, batsman2 = batsman2, batsman1
            batsman1Rating, batsman2Rating = batsman2Rating, batsman1Rating
            initialStrikeFour, initialNonStrikeFour = initialNonStrikeFour, initialStrikeFour
            initialStrikeSix, initialNonStrikeSix = initialNonStrikeSix, initialStrikeSix
        else:
            batsman1, batsman2 = batsman1, batsman2
            batsman1Rating, batsman2Rating = batsman1Rating, batsman2Rating
            initialStrikeFour, initialNonStrikeFour = initialStrikeFour, initialNonStrikeFour
            initialStrikeSix, initialNonStrikeSix = initialStrikeSix, initialNonStrikeSix
    elif ballOutcome == [4]:
        if count % 10 == 0: #overend
            initialStrikeFour = initialStrikeFour + 1
            batsman1, batsman2 = batsman2, batsman1
            batsman1Rating, batsman2Rating = batsman2Rating, batsman1Rating
            initialStrikeFour, initialNonStrikeFour = initialNonStrikeFour, initialStrikeFour
            initialStrikeSix, initialNonStrikeSix = initialNonStrikeSix, initialStrikeSix
        else:
            initialStrikeFour = initialStrikeFour + 1
            batsman1, batsman2 = batsman1, batsman2
            batsman1Rating, batsman2Rating = batsman1Rating, batsman2Rating
            initialStrikeFour, initialNonStrikeFour = initialStrikeFour, initialNonStrikeFour
            initialStrikeSix, initialNonStrikeSix = initialStrikeSix, initialNonStrikeSix
    elif ballOutcome == [6]:
        if count % 10 == 0: #overend
            initialStrikeSix = initialStrikeSix + 1
            batsman1, batsman2 = batsman2, batsman1
            batsman1Rating, batsman2Rating = batsman2Rating, batsman1Rating
            initialStrikeFour, initialNonStrikeFour = initialNonStrikeFour, initialStrikeFour
            initialStrikeSix, initialNonStrikeSix = initialNonStrikeSix, initialStrikeSix
        else:
            initialStrikeSix = initialStrikeSix + 1
            batsman1, batsman2 = batsman1, batsman2
            batsman1Rating, batsman2Rating = batsman1Rating, batsman2Rating
            initialStrikeFour, initialNonStrikeFour = initialStrikeFour, initialNonStrikeFour
            initialStrikeSix, initialNonStrikeSix = initialStrikeSix, initialNonStrikeSix
    elif ballOutcome == ['Wide']:
        batsman1, batsman2 = batsman1, batsman2
        batsman1Rating, batsman2Rating = batsman2Rating, batsman1Rating
        initialStrikeFour, initialNonStrikeFour = initialStrikeFour, initialNonStrikeFour
        initialStrikeSix, initialNonStrikeSix = initialStrikeSix, initialNonStrikeSix
       
        
    if ballOutcome == ['OUT']:
        if count % 10 == 0:
            #add runs to strike batsmen
            initialStrikerRuns = initialStrikerRuns + 0
            initialStrikerBallsCount = initialStrikerBallsCount + 1
            initialStrikerRuns, intialNonStrikerRuns = intialNonStrikerRuns, initialStrikerRuns
            initialStrikerBallsCount, initialNonStrikerBallsCount = initialNonStrikerBallsCount, initialStrikerBallsCount
        else:
            #add runs to strike batsmen
            initialStrikerRuns = initialStrikerRuns + 0
            initialStrikerBallsCount = initialStrikerBallsCount + 1
            initialStrikerRuns, intialNonStrikerRuns = initialStrikerRuns, intialNonStrikerRuns
            initialStrikerBallsCount, initialNonStrikerBallsCount = initialStrikerBallsCount, initialNonStrikerBallsCount
        # print(batsman1+'-> '+' Fours: '+str(initialStrikeFour)+' Sixes: '+str(initialStrikeSix))
        # print(batsman2+'-> '+' Fours: '+str(initialNonStrikeFour)+' Sixes: '+str(initialNonStrikeSix))
    if ballOutcome == [0]:
        if count % 10 == 0:
            #add runs to strike batsmen
            initialStrikerRuns = initialStrikerRuns + 0
            initialStrikerBallsCount = initialStrikerBallsCount + 1
            initialStrikerRuns, intialNonStrikerRuns = intialNonStrikerRuns, initialStrikerRuns
            initialStrikerBallsCount, initialNonStrikerBallsCount = initialNonStrikerBallsCount, initialStrikerBallsCount
        else:
            #add runs to strike batsmen
            initialStrikerRuns = initialStrikerRuns + 0
            initialStrikerBallsCount = initialStrikerBallsCount + 1
            initialStrikerRuns, intialNonStrikerRuns = initialStrikerRuns, intialNonStrikerRuns
            initialStrikerBallsCount, initialNonStrikerBallsCount = initialStrikerBallsCount, initialNonStrikerBallsCount
        # print(batsman1+'-> '+' Fours: '+str(initialStrikeFour)+' Sixes: '+str(initialStrikeSix))
        # print(batsman2+'-> '+' Fours: '+str(initialNonStrikeFour)+' Sixes: '+str(initialNonStrikeSix))
    if ballOutcome == [1]:
        if count % 10 == 0: #when outcome 1 on last ball of over, strike change.
            #add runs to strike batsmen
            initialStrikerRuns = initialStrikerRuns + 1
            initialStrikerBallsCount = initialStrikerBallsCount + 1
            initialStrikerRuns, intialNonStrikerRuns = initialStrikerRuns, intialNonStrikerRuns
            initialStrikerBallsCount, initialNonStrikerBallsCount = initialStrikerBallsCount, initialNonStrikerBallsCount
        else:
            #add runs to strike batsmen
            initialStrikerRuns = initialStrikerRuns + 1
            initialStrikerBallsCount = initialStrikerBallsCount + 1
            initialStrikerRuns, intialNonStrikerRuns = intialNonStrikerRuns, initialStrikerRuns
            initialStrikerBallsCount, initialNonStrikerBallsCount = initialNonStrikerBallsCount, initialStrikerBallsCount
        # print(batsman1+'-> '+' Fours: '+str(initialStrikeFour)+' Sixes: '+str(initialStrikeSix))
        # print(batsman2+'-> '+' Fours: '+str(initialNonStrikeFour)+' Sixes: '+str(initialNonStrikeSix))
    elif ballOutcome == [2]:
        if count % 10 == 0:
            #add runs to strike batsmen
            initialStrikerRuns = initialStrikerRuns + 2
            initialStrikerBallsCount = initialStrikerBallsCount + 1
            initialStrikerRuns, intialNonStrikerRuns = intialNonStrikerRuns, initialStrikerRuns
            initialStrikerBallsCount, initialNonStrikerBallsCount = initialNonStrikerBallsCount, initialStrikerBallsCount
        else:
            #add runs to strike batsmen
            initialStrikerRuns = initialStrikerRuns + 2
            initialStrikerBallsCount = initialStrikerBallsCount + 1
            initialStrikerRuns, intialNonStrikerRuns = initialStrikerRuns, intialNonStrikerRuns
            initialStrikerBallsCount, initialNonStrikerBallsCount = initialStrikerBallsCount, initialNonStrikerBallsCount
        # print(batsman1+'-> '+' Fours: '+str(initialStrikeFour)+' Sixes: '+str(initialStrikeSix))
        # print(batsman2+'-> '+' Fours: '+str(initialNonStrikeFour)+' Sixes: '+str(initialNonStrikeSix))
    elif ballOutcome == [3]:
        if count % 10 == 0:
             #add runs to strike batsmen
            initialStrikerRuns = initialStrikerRuns + 3
            initialStrikerBallsCount = initialStrikerBallsCount + 1
            initialStrikerRuns, intialNonStrikerRuns = initialStrikerRuns, intialNonStrikerRuns
            initialStrikerBallsCount, initialNonStrikerBallsCount = initialStrikerBallsCount, initialNonStrikerBallsCount
        else:
            #add runs to strike batsmen
            initialStrikerRuns = initialStrikerRuns + 3
            initialStrikerBallsCount = initialStrikerBallsCount + 1
            initialStrikerRuns, intialNonStrikerRuns = intialNonStrikerRuns, initialStrikerRuns
            initialStrikerBallsCount, initialNonStrikerBallsCount = initialNonStrikerBallsCount, initialStrikerBallsCount
        # print(batsman1+'-> '+' Fours: '+str(initialStrikeFour)+' Sixes: '+str(initialStrikeSix))
        # print(batsman2+'-> '+' Fours: '+str(initialNonStrikeFour)+' Sixes: '+str(initialNonStrikeSix))
    elif ballOutcome == [4]:
        if count % 10 == 0:
            #add runs to strike batsmen
            initialStrikerRuns = initialStrikerRuns + 4
            initialStrikerBallsCount = initialStrikerBallsCount + 1
            #Counting 4's and 6's
            initialStrikerRuns, intialNonStrikerRuns = intialNonStrikerRuns, initialStrikerRuns
            initialStrikerBallsCount, initialNonStrikerBallsCount = initialNonStrikerBallsCount, initialStrikerBallsCount
        else:
            #add runs to strike batsmen
            initialStrikerRuns = initialStrikerRuns + 4
            initialStrikerBallsCount = initialStrikerBallsCount + 1
            initialStrikerRuns, intialNonStrikerRuns = initialStrikerRuns, intialNonStrikerRuns
            initialStrikerBallsCount, initialNonStrikerBallsCount = initialStrikerBallsCount, initialNonStrikerBallsCount
        # print(batsman1+'-> '+' Fours: '+str(initialStrikeFour)+' Sixes: '+str(initialStrikeSix))
        # print(batsman2+'-> '+' Fours: '+str(initialNonStrikeFour)+' Sixes: '+str(initialNonStrikeSix))
    elif ballOutcome == [6]:
        if count % 10 == 0:
             #add runs to strike batsmen
            initialStrikerRuns = initialStrikerRuns + 6
            initialStrikerBallsCount = initialStrikerBallsCount + 1
            initialStrikerRuns, intialNonStrikerRuns = intialNonStrikerRuns, initialStrikerRuns
            initialStrikerBallsCount, initialNonStrikerBallsCount = initialNonStrikerBallsCount, initialStrikerBallsCount
        else:
            #add runs to strike batsmen
            initialStrikerRuns = initialStrikerRuns + 6
            initialStrikerBallsCount = initialStrikerBallsCount + 1
            initialStrikerRuns, intialNonStrikerRuns = initialStrikerRuns, intialNonStrikerRuns
            initialStrikerBallsCount, initialNonStrikerBallsCount = initialStrikerBallsCount, initialNonStrikerBallsCount
        # print(batsman1+'-> '+' Fours: '+str(initialStrikeFour)+' Sixes: '+str(initialStrikeSix))
        # print(batsman2+'-> '+' Fours: '+str(initialNonStrikeFour)+' Sixes: '+str(initialNonStrikeSix))
    

    if count % 10 == 0:
        print('     {}     ({}){} [{}x4 {}x6]'.format(batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour, initialStrikeSix))
        print('     {}     ({}){} [{}x4 {}x6]'.format(batsman2,intialNonStrikerRuns,initialNonStrikerBallsCount, initialNonStrikeFour, initialNonStrikeSix))
        print('     {}     {}-{}-{}-{}'.format(bowlerPresent,'10',initialDotBalls,initialScore,initialOut))
        print()
        
    
    #If out bring in next batsmen ['Batsman','Bowler','Runs','Balls','4s','6s','SR']
    if ballOutcome == ['OUT']:
        sr = initialStrikerRuns * 100 // initialStrikerBallsCount

        batsmenScoreboard.append([batsman1, bowlerPresent, initialStrikerRuns, initialStrikerBallsCount, 
               initialStrikeFour, initialStrikeSix, sr])

        
        print()
        print('     b. {}     {}({}){} [{}x4 {}x6]'.format(bowlerPresent,batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour,initialStrikeSix))
        initialStrikerRuns = 0
        initialStrikerBallsCount = 0
        initialStrikeFour = 0
        initialStrikeSix = 0
        print()
        playerOut = playerOut + 1
        batsman1Rating = battingPlayerRatings[b+playerOut+1]
        batsman1 = battingPlayerNames[b+playerOut+1]
        
print()
df = pd.DataFrame(batsmenScoreboard, columns =['Batsman','Bowler','Runs','Balls','4s','6s','SR'])
print(tabulate(df, showindex=False, headers=df.columns))
