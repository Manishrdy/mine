# -*- coding: utf-8 -*-
"""
Created on Tue Jul 27 14:29:14 2021

@author: Manish.
"""

import pandas as pd
import numpy as np
import random

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
battingPlayers = battingPlayers.values.tolist()

battingPlayerNames = []
battingPlayerRatings = []
for i in battingPlayers:
    battingPlayerNames.append(i[0])
    battingPlayerRatings.append(i[1:])



totalWickets = 0
totalScore = 0
batsmanStrike = battingPlayerNames[0]
batsmanOffStrike = battingPlayerNames[1]
bowlingStats = []
initialScore = 0
initialOut = 0
initialWide = 0
count = 0

inng1InningsBatting = {}
inng2InningsBowling = {}

bowler = random.choice(bowlingPlayers)
b = 0
playerOut = 0
bowlerPresent = bowler
batsman1 = battingPlayerNames[b]
batsman2 = battingPlayerNames[b+1]
batsman1Rating = battingPlayerRatings[b]
batsman2Rating = battingPlayerRatings[b+1]

for i in range(1,50):
    previousBowler = bowler
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
        else:
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
                print('     End of innings (Balls '+str(count)+')')
                rr = totalScore / (count / 10)
                print('     Chennai Super Kings     '+str(totalScore)+'/'+str(totalWickets)+'  (RR: {:.2f})'.format(rr))
                break
            
    if count % 10 == 0:
        print()
        print('     END of '+str(count)+' balls ('+str(initialScore)+' runs)')
        print('     Chennai Super Kings     '+str(totalScore)+'/'+str(totalWickets))
        rr = totalScore / (count / 10)
        print('     RR: {:.2f}'.format(rr))
        print()
        print('     {}     {}-{}-{}-{}'.format(bowlerPresent,'10','0',initialScore,initialOut))
        print()
        
        #Reseting over score before the begini of new over.
        initialScore = 0
        initialOut = 0
        #Change of bowler
        bowler = random.choice(bowlingPlayers)
        bowlerPresent = bowler
        
        
    
    #If out bring in next batsmen
    if ballOutcome == ['OUT']:
        playerOut = playerOut + 1
        batsman1Rating = battingPlayerRatings[b+playerOut+1]
        batsman1 = battingPlayerNames[b+playerOut+1]
 
    
    #Checking weather to rotate strike or not after the end of over and in between the innings
    if ballOutcome == [1]:
        if count % 10 == 0: #overend
            batsman1, batsman2 = batsman1, batsman2
            batsman1Rating, batsman2Rating = batsman1Rating, batsman2Rating
        else:
            batsman1, batsman2 = batsman2, batsman1
            batsman1Rating, batsman2Rating = batsman2Rating, batsman1Rating
    elif ballOutcome == [3]:
        if count % 10 == 0: #overend
            batsman1, batsman2 = batsman2, batsman1
            batsman1Rating, batsman2Rating = batsman2Rating, batsman1Rating
        else:
            batsman1, batsman2 = batsman2, batsman1
            batsman1Rating, batsman2Rating = batsman2Rating, batsman1Rating
    elif ballOutcome == [0]:
        if count % 10 == 0: #overend
            batsman1, batsman2 = batsman2, batsman1
            batsman1Rating, batsman2Rating = batsman2Rating, batsman1Rating
        else:
            batsman1, batsman2 = batsman1, batsman2
            batsman1Rating, batsman2Rating = batsman1Rating, batsman2Rating
    elif ballOutcome == [2]:
        if count % 10 == 0: #overend
            batsman1, batsman2 = batsman2, batsman1
            batsman1Rating, batsman2Rating = batsman2Rating, batsman1Rating
        else:
            batsman1, batsman2 = batsman1, batsman2
            batsman1Rating, batsman2Rating = batsman1Rating, batsman2Rating
    elif ballOutcome == [4]:
        if count % 10 == 0: #overend
            batsman1, batsman2 = batsman2, batsman1
            batsman1Rating, batsman2Rating = batsman2Rating, batsman1Rating
        else:
            batsman1, batsman2 = batsman1, batsman2
            batsman1Rating, batsman2Rating = batsman1Rating, batsman2Rating
    elif ballOutcome == [6]:
        if count % 10 == 0: #overend
            batsman1, batsman2 = batsman2, batsman1
            batsman1Rating, batsman2Rating = batsman2Rating, batsman1Rating
        else:
            batsman1, batsman2 = batsman1, batsman2
            batsman1Rating, batsman2Rating = batsman1Rating, batsman2Rating
    elif ballOutcome == ['Wide']:
        batsman1, batsman2 = batsman1, batsman2
        batsman1Rating, batsman2Rating = batsman2Rating, batsman1Rating
