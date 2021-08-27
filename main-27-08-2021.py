# -*- coding: utf-8 -*-
"""
Created on Wed Jul 28 21:42:15 2021
@author: Manish.
"""

import random
import os
import glob
import time
import pandas as pd
import sys
import io
from tabulate import tabulate

sys.setrecursionlimit(10**9)

outcomes = [0, 1, 2, 3, 4, 6, 'OUT', 'Wide', 'Leg Bye']
outList = ['Stumped', 'Bowled', 'Caught']
gameRate = 0.05 # seconds between balls

# def endSaveScript():
#     sys.stdout.close()
#     sys.stdout=stdoutOrigin

#Creating arrays for 4's and 6's
zeroComm = []
oneComm = []
twoComm = []
threeComm = []
fourComm = []
sixComm = []
outComm = []
batsmenScoreboard1 = []
batsmenScoreboard2 = []

file = io.open('./commentry/0.txt','r',encoding="utf8")
for i in file.readlines():
    zeroComm.append(i)

for i in range(len(zeroComm)):
    zeroComm[i] = zeroComm[i].replace('\n','')
    
file = io.open('./commentry/1.txt','r',encoding="utf8")
for i in file.readlines():
    oneComm.append(i)

for i in range(len(oneComm)):
    oneComm[i] = oneComm[i].replace('\n','')

file = io.open('./commentry/2.txt','r',encoding="utf8")
for i in file.readlines():
    twoComm.append(i)

for i in range(len(twoComm)):
    twoComm[i] = twoComm[i].replace('\n','')
    
file = io.open('./commentry/3.txt','r',encoding="utf8")
for i in file.readlines():
    threeComm.append(i)

for i in range(len(threeComm)):
    threeComm[i] = threeComm[i].replace('\n','')

file = io.open('./commentry/4.txt','r',encoding="utf8")
for i in file.readlines():
    fourComm.append(i)

for i in range(len(fourComm)):
    fourComm[i] = fourComm[i].replace('\n','')
    
file = io.open('./commentry/6.txt','r',encoding="utf8")
for i in file.readlines():
    sixComm.append(i)

for i in range(len(sixComm)):
    sixComm[i] = sixComm[i].replace('\n','')
    
file = io.open('./commentry/out.txt','r',encoding="utf8")
for i in file.readlines():
    outComm.append(i)

for i in range(len(outComm)):
    outComm[i] = outComm[i].replace('\n','')
    
    
def prepInnings2(team1, team2, target):
    
    team2BowlerRatings = pd.read_csv(team2+' Bowling.manish')
    team2FastBowlersRatings = team2BowlerRatings[team2BowlerRatings['type'] == 'fast']
    team2SpinBowlersRatings = team2BowlerRatings[team2BowlerRatings['type'] == 'spin']
    
    player_name = team2FastBowlersRatings['player'].to_list()
    team2FastBowlersRatingsValues = team2FastBowlersRatings['rating'].to_list()
    
    player_name2 = team2SpinBowlersRatings['player'].to_list()
    team2SpinBowlersRatingsValues = team2SpinBowlersRatings['rating'].to_list()
    
    fastBowlers = []
    spinBowlers = []
    
    for i in range(len(player_name)):
        fastBowlers.append([player_name[i], team2FastBowlersRatingsValues[i]])
    fastBowlers.sort(key=lambda fastBowlers:fastBowlers[1], reverse=True)
    
    for i in range(len(player_name2)):
        spinBowlers.append([player_name2[i], team2SpinBowlersRatingsValues[i]])
    spinBowlers.sort(key=lambda spinBowlers:spinBowlers[1], reverse=True)
    
    bowlers = fastBowlers + spinBowlers
    
    sortedBowlers = []
    for i in bowlers:
        sortedBowlers.append(i[0])
    
    checkList = []
    
    battingTeam1 = pd.read_csv(team1+'.csv')
    bowlingTeam1 = pd.read_csv(team2+'.csv')
    
    oppTeam = pd.read_csv(team2+'.csv')
    keeper = oppTeam[oppTeam['role'] == 'Keeper']['player']
    keeper = keeper.values
    
    oppTeam = oppTeam.player
    oppTeam = oppTeam.to_list()
    
    bowlingPlayers = bowlingTeam1[bowlingTeam1['role'] == "Bowler"]
    bowlingPlayers = bowlingPlayers.player
    bowlingPlayers = bowlingPlayers.to_list()
    
    if set(bowlingPlayers) == set(sortedBowlers):
        pass
    else:
        print('Bowlers ratings data not matching with playing 11 data !!')
        print('Check '+team2+'.csv and '+team2+' Bowling.manish')
        sys.exit()
    
    battingPlayers = battingTeam1
    columns = ['role', 'type', 'total']
    battingPlayers.drop(columns, inplace=True, axis=1)
    battingPlayers = battingPlayers.values.tolist()
    
    battingPlayerNames = []
    battingPlayerRatings = []
    
    for i in battingPlayers:
        battingPlayerNames.append(i[0])
        battingPlayerRatings.append(i[1:])
    
    
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
    totalExtras = 0
    
    
    inng1InningsBatting = {}
    inng2InningsBowling = {}
    
    print(team1+' - ',battingPlayerNames)
    print(team2+' - ',bowlingPlayers)
    print()
    
    def pickBowler():
        bowler = random.choice(sortedBowlers)
        if bowler != checkList[-1] and checkList.count(bowler) < 2:
            checkList.append(bowler)
            return bowler
        else:
            return pickBowler()
        return bowler
    
    b = 0
    playerOut = 0
    
    bowlerPresent = sortedBowlers[0]
    checkList.append(bowlerPresent)
    sortedBowlerIndex = sortedBowlers.index(bowlerPresent)
    bowlerPresentRating = bowlers[sortedBowlerIndex][1]
    
    batsman1 = battingPlayerNames[b]
    batsman2 = battingPlayerNames[b+1]
    batsman1Rating = battingPlayerRatings[b]
    batsman2Rating = battingPlayerRatings[b+1]
    
    #Name, Balls, Dots, Runs, Wickets, Economy
    bowlersScoreboardTwo = []
    for i in range(len(bowlingPlayers)):
        bowlersScoreboardTwo.append([bowlingPlayers[i],0,0,0,0,0])
    
    print('%%%%%  Second Innings  %%%%%')
    print()
    
    for i in range(1,101):
        # time.sleep(gameRate)
        iBall = i
        if len(str(i)) == 1:
            ball = 'Ball 0'+str(i)+' : '
        else:
            ball = 'Ball '+str(i)+' : '
        
        def callBatsman1Rating():
           if bowlerPresentRating in range(71, 76):
               #increase
               batsman1Rating[0] = batsman1Rating[0] - 3
               batsman1Rating[1] = batsman1Rating[1] - 3
               batsman1Rating[2] = batsman1Rating[2] - 1
               batsman1Rating[6] = batsman1Rating[6] - 0
               #decrease
               batsman1Rating[3] = batsman1Rating[3] + 0.3
               batsman1Rating[4] = batsman1Rating[4] + 1.3
               batsman1Rating[5] = batsman1Rating[5] + 0.7
           elif bowlerPresentRating in range(76, 81):
               #increase
               batsman1Rating[0] = batsman1Rating[0] - 5
               batsman1Rating[1] = batsman1Rating[1] - 5
               batsman1Rating[2] = batsman1Rating[2] - 3
               batsman1Rating[6] = batsman1Rating[6] - 1
               #decrease
               batsman1Rating[3] = batsman1Rating[3] + 0.7
               batsman1Rating[4] = batsman1Rating[4] + 2
               batsman1Rating[5] = batsman1Rating[5] + 1.5
           elif bowlerPresentRating in range(81, 86):
               #increase
               batsman1Rating[0] = batsman1Rating[0] - 6
               batsman1Rating[1] = batsman1Rating[1] - 6
               batsman1Rating[2] = batsman1Rating[2] - 4
               batsman1Rating[6] = batsman1Rating[6] - 2
               #decrease
               batsman1Rating[3] = batsman1Rating[3] + 1
               batsman1Rating[4] = batsman1Rating[4] + 3
               batsman1Rating[5] = batsman1Rating[5] + 2
           elif bowlerPresentRating in range(86, 91):
               #increase
               batsman1Rating[0] = batsman1Rating[0] - 7
               batsman1Rating[1] = batsman1Rating[1] - 7
               batsman1Rating[2] = batsman1Rating[2] - 5
               batsman1Rating[6] = batsman1Rating[6] - 3
               #decrease
               batsman1Rating[3] = batsman1Rating[3] + 2
               batsman1Rating[4] = batsman1Rating[4] + 4
               batsman1Rating[5] = batsman1Rating[5] + 3
           elif bowlerPresentRating in range(91, 96):
               #increase
               batsman1Rating[0] = batsman1Rating[0] - 8
               batsman1Rating[1] = batsman1Rating[1] - 8
               batsman1Rating[2] = batsman1Rating[2] - 6
               batsman1Rating[6] = batsman1Rating[6] - 7
               #decrease
               batsman1Rating[3] = batsman1Rating[3] + 3
               batsman1Rating[4] = batsman1Rating[4] + 5
               batsman1Rating[5] = batsman1Rating[5] + 4
           elif bowlerPresentRating in range(0,55):
               #increase
               batsman1Rating[0] = batsman1Rating[0] + 25
               batsman1Rating[1] = batsman1Rating[1] - 15
               batsman1Rating[2] = batsman1Rating[2] - 15
               batsman1Rating[6] = batsman1Rating[6] + 7
               #decrease
               batsman1Rating[3] = batsman1Rating[3] - 3
               batsman1Rating[4] = batsman1Rating[4] - 6
               batsman1Rating[5] = batsman1Rating[5] - 6
           elif bowlerPresentRating in range(55,61):
               #increase
               batsman1Rating[0] = batsman1Rating[0] - 0.5
               batsman1Rating[1] = batsman1Rating[1] - 0.5
               batsman1Rating[2] = batsman1Rating[2] - 0.5
               batsman1Rating[6] = batsman1Rating[6] - 0.5
               #decrease
               batsman1Rating[3] = batsman1Rating[3] + 0.5
               batsman1Rating[4] = batsman1Rating[4] + 0.5
               batsman1Rating[5] = batsman1Rating[5] + 0.5
           elif bowlerPresentRating in range(61,66):
               #increase
               batsman1Rating[0] = batsman1Rating[0] - 1
               batsman1Rating[1] = batsman1Rating[1] - 1
               batsman1Rating[2] = batsman1Rating[2] - 1
               batsman1Rating[6] = batsman1Rating[6] - 1
               #decrease
               batsman1Rating[3] = batsman1Rating[3] + 0.5
               batsman1Rating[4] = batsman1Rating[4] + 0.5
               batsman1Rating[5] = batsman1Rating[5] + 0.5
           elif bowlerPresentRating in range(66,71):
               #increase
               batsman1Rating[0] = batsman1Rating[0] - 2
               batsman1Rating[1] = batsman1Rating[1] - 2
               batsman1Rating[2] = batsman1Rating[2] - 2
               batsman1Rating[6] = batsman1Rating[6] - 2
               #decrease
               batsman1Rating[3] = batsman1Rating[3] + 1
               batsman1Rating[4] = batsman1Rating[4] + 1
               batsman1Rating[5] = batsman1Rating[5] + 1
        
        if bowlerPresentRating in range(71, 76):
            #increase
            batsman1Rating[0] = batsman1Rating[0] + 3
            batsman1Rating[1] = batsman1Rating[1] + 3
            batsman1Rating[2] = batsman1Rating[2] + 1
            #decrease
            batsman1Rating[3] = batsman1Rating[3] - 0.3
            batsman1Rating[4] = batsman1Rating[4] - 1.3
            batsman1Rating[5] = batsman1Rating[5] - 0.7
        elif bowlerPresentRating in range(76, 81):
            #increase
            batsman1Rating[0] = batsman1Rating[0] + 5
            batsman1Rating[1] = batsman1Rating[1] + 5
            batsman1Rating[2] = batsman1Rating[2] + 3
            batsman1Rating[6] = batsman1Rating[6] + 1
            #decrease
            batsman1Rating[3] = batsman1Rating[3] - 0.7
            batsman1Rating[4] = batsman1Rating[4] - 2
            batsman1Rating[5] = batsman1Rating[5] - 1.5
        elif bowlerPresentRating in range(81, 86):
            #increase
            batsman1Rating[0] = batsman1Rating[0] + 6
            batsman1Rating[1] = batsman1Rating[1] + 6
            batsman1Rating[2] = batsman1Rating[2] + 4
            batsman1Rating[6] = batsman1Rating[6] + 2
            #decrease
            batsman1Rating[3] = batsman1Rating[3] - 1
            batsman1Rating[4] = batsman1Rating[4] - 3
            batsman1Rating[5] = batsman1Rating[5] - 2
        elif bowlerPresentRating in range(86, 91):
            #increase
            batsman1Rating[0] = batsman1Rating[0] + 7
            batsman1Rating[1] = batsman1Rating[1] + 7
            batsman1Rating[2] = batsman1Rating[2] + 5
            batsman1Rating[6] = batsman1Rating[6] + 3
            #decrease
            batsman1Rating[3] = batsman1Rating[3] - 2
            batsman1Rating[4] = batsman1Rating[4] - 4
            batsman1Rating[5] = batsman1Rating[5] - 3
        elif bowlerPresentRating in range(91, 96):
            #increase
            batsman1Rating[0] = batsman1Rating[0] + 8
            batsman1Rating[1] = batsman1Rating[1] + 8
            batsman1Rating[2] = batsman1Rating[2] + 6
            batsman1Rating[6] = batsman1Rating[6] + 7
            #decrease
            batsman1Rating[3] = batsman1Rating[3] - 3
            batsman1Rating[4] = batsman1Rating[4] - 5
            batsman1Rating[5] = batsman1Rating[5] - 4
        elif bowlerPresentRating in range(0,55):
            #increase
            batsman1Rating[0] = batsman1Rating[0] - 25
            batsman1Rating[1] = batsman1Rating[1] + 15
            batsman1Rating[2] = batsman1Rating[2] + 15
            batsman1Rating[6] = batsman1Rating[6] - 7
            #decrease
            batsman1Rating[3] = batsman1Rating[3] + 3
            batsman1Rating[4] = batsman1Rating[4] + 6
            batsman1Rating[5] = batsman1Rating[5] + 6
        elif bowlerPresentRating in range(55,61):
            #increase
            batsman1Rating[0] = batsman1Rating[0] + 0.5
            batsman1Rating[1] = batsman1Rating[1] + 0.5
            batsman1Rating[2] = batsman1Rating[2] + 0.5
            batsman1Rating[6] = batsman1Rating[6] + 0.5
            #decrease
            batsman1Rating[3] = batsman1Rating[3] - 0.5
            batsman1Rating[4] = batsman1Rating[4] - 0.5
            batsman1Rating[5] = batsman1Rating[5] - 0.5
        elif bowlerPresentRating in range(61,66):
            #increase
            batsman1Rating[0] = batsman1Rating[0] + 1
            batsman1Rating[1] = batsman1Rating[1] + 1
            batsman1Rating[2] = batsman1Rating[2] + 1
            batsman1Rating[6] = batsman1Rating[6] + 1
            #decrease
            batsman1Rating[3] = batsman1Rating[3] - 0.5
            batsman1Rating[4] = batsman1Rating[4] - 0.5
            batsman1Rating[5] = batsman1Rating[5] - 0.5
        elif bowlerPresentRating in range(66,71):
            #increase
            batsman1Rating[0] = batsman1Rating[0] + 2
            batsman1Rating[1] = batsman1Rating[1] + 2
            batsman1Rating[2] = batsman1Rating[2] + 2
            batsman1Rating[6] = batsman1Rating[6] + 2
            #decrease
            batsman1Rating[3] = batsman1Rating[3] - 1
            batsman1Rating[4] = batsman1Rating[4] - 1
            batsman1Rating[5] = batsman1Rating[5] - 1
        
        ballOutcome = random.choices(outcomes, weights=(batsman1Rating), k=1)
        callBatsman1Rating()
        
        if ballOutcome == [1] or ballOutcome == ['Leg Bye']:
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
            totalExtras = totalExtras + 1
        elif ballOutcome == ['OUT']:
            initialOut = initialOut + 1
            totalWickets = totalWickets + 1
            initialDotBalls = initialDotBalls + 1
        elif ballOutcome == [0]:
            initialDotBalls = initialDotBalls + 1
        elif ballOutcome == ['Leg Bye']:
            totalExtras = totalExtras + 1
        else:
            pass
        
        if ballOutcome == ['OUT']:
            outType = random.choice(outList)
            if outType == 'Caught':
                cPlayer = random.choice(oppTeam)
                print('{} {} to {}, {} by {}, {}'.format(ball,bowlerPresent,batsman1,outType,cPlayer,random.choice(outComm)))
            elif outType == 'Bowled':
                print('{} {} to {}, {}, {}'.format(ball,bowlerPresent,batsman1,outType,random.choice(outComm)))
            elif outType == 'Stumped':
                print('{} {} to {}, {} by {}, {}'.format(ball,bowlerPresent,batsman1,outType,*keeper,random.choice(outComm)))
        elif ballOutcome == ['Wide']:
            print('{} {} to {},{}, {}'.format(ball,bowlerPresent,batsman1,*ballOutcome,'Thats a wide ball from '+bowlerPresent))
        elif ballOutcome == [1]:
            print('{} {} to {}, one {}, {}'.format(ball,bowlerPresent,batsman1,'run',random.choice(oneComm).replace('batsman', batsman1)))
        elif ballOutcome == [2]:
            print('{} {} to {}, two {}, {}'.format(ball,bowlerPresent,batsman1,'runs',random.choice(twoComm).replace('batsman', batsman1)))
        elif ballOutcome == [3]:
            print('{} {} to {}, three {}, {}'.format(ball,bowlerPresent,batsman1,'runs',random.choice(threeComm).replace('batsman', batsman1)))
        elif ballOutcome == [4]:
            print('{} {} to {}, FOUR {}, {}'.format(ball,bowlerPresent,batsman1,'runs',random.choice(fourComm).replace('batsman', batsman1)))
        elif ballOutcome == [0]:
            print('{} {} to {}, dot {}, {}'.format(ball,bowlerPresent,batsman1,'',random.choice(zeroComm).replace('batsman', batsman1)))
        elif ballOutcome == ['Leg Bye']:
            print('{} {} to {}, Leg Bye , {}'.format(ball,bowlerPresent,batsman1,random.choice(oneComm).replace('batsman', batsman1)))
        elif ballOutcome == [6]:
            print('{} {} to {}, SIX ! {}, {}'.format(ball,bowlerPresent,batsman1,'runs',random.choice(sixComm).replace('batsman', batsman1)))
        
        count = count + 1
        if ballOutcome == ['OUT']:
            if count % 10 == 0:
                initialStrikerRuns, intialNonStrikerRuns = intialNonStrikerRuns, initialStrikerRuns
                initialStrikerBallsCount, initialNonStrikerBallsCount = initialNonStrikerBallsCount, initialStrikerBallsCount
                
        
        #Checking for winner after every ball
        if totalScore >= target:
            if initialStrikerBallsCount == 0:
                sr1 = 0
            else:
                sr1 = initialStrikerRuns * 100 // initialStrikerBallsCount
            sr2 = intialNonStrikerRuns * 100 // initialNonStrikerBallsCount
            batsmenScoreboard2.append([batsman1, "Not Out",'','', initialStrikerRuns, initialStrikerBallsCount, 
            initialStrikeFour, initialStrikeSix, sr1])
            batsmenScoreboard2.append([batsman2, "Not Out",'','', intialNonStrikerRuns, initialNonStrikerBallsCount, 
            initialNonStrikeFour, initialNonStrikeSix, sr2])
            print()
            for i in bowlingPlayers:
                if i == bowlerPresent:
                    index = bowlingPlayers.index(i)
                    if bowlersScoreboardTwo[index][1] == 0:
                        if iBall == 100:
                            bowlersScoreboardTwo[index][1] = bowlersScoreboardTwo[index][1] + 10
                            bowlersScoreboardTwo[index][2] = bowlersScoreboardTwo[index][2] + initialDotBalls
                            bowlersScoreboardTwo[index][3] = bowlersScoreboardTwo[index][3] + initialScore
                            bowlersScoreboardTwo[index][4] = bowlersScoreboardTwo[index][4] + initialOut
                            bowlersScoreboardTwo[index][5] = bowlersScoreboardTwo[index][3] / 20
                            initialBowlerBallsCount = 20
                            # print('     b. {}     {}({}){} [{}x4 {}x6]'.format(bowlerPresent,batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour,initialStrikeSix))
                            print('     {}     ({}){} [{}x4 {}x6]'.format(batsman1,initialStrikerRuns,initialStrikerBallsCount, initialStrikeFour, initialStrikeSix))
                            print('     {}     ({}){} [{}x4 {}x6]'.format(batsman2,intialNonStrikerRuns,initialNonStrikerBallsCount, initialNonStrikeFour, initialNonStrikeSix))
                            print('     {}     {}-{}-{}-{}'.format(bowlerPresent,initialBowlerBallsCount,bowlersScoreboardTwo[index][2],bowlersScoreboardTwo[index][3],bowlersScoreboardTwo[index][4]))
                            print()
                        else:
                            iBall = str(iBall)
                            tempBalls = iBall[1:]
                            tempBalls = int(tempBalls)
                            bowlersScoreboardTwo[index][1] = bowlersScoreboardTwo[index][1] + tempBalls
                            bowlersScoreboardTwo[index][2] = bowlersScoreboardTwo[index][2] + initialDotBalls
                            bowlersScoreboardTwo[index][3] = bowlersScoreboardTwo[index][3] + initialScore
                            bowlersScoreboardTwo[index][4] = bowlersScoreboardTwo[index][4] + initialOut
                            bowlersScoreboardTwo[index][5] = bowlersScoreboardTwo[index][3] / bowlersScoreboardTwo[index][1]
                            initialBowlerBallsCount = 10 + tempBalls

                            # print('     b. {}     {}({}){} [{}x4 {}x6]'.format(bowlerPresent,batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour,initialStrikeSix))
                            print('     {}     ({}){} [{}x4 {}x6]'.format(batsman1,initialStrikerRuns,initialStrikerBallsCount, initialStrikeFour, initialStrikeSix))
                            print('     {}     ({}){} [{}x4 {}x6]'.format(batsman2,intialNonStrikerRuns,initialNonStrikerBallsCount, initialNonStrikeFour, initialNonStrikeSix))
                            print('     {}     {}-{}-{}-{}'.format(bowlerPresent,initialBowlerBallsCount,bowlersScoreboardTwo[index][2],bowlersScoreboardTwo[index][3],bowlersScoreboardTwo[index][4]))
                            print()
                    elif bowlersScoreboardTwo[index][1] == 10:
                        if iBall == 100:
                            bowlersScoreboardTwo[index][1] = bowlersScoreboardTwo[index][1] + 10
                            bowlersScoreboardTwo[index][2] = bowlersScoreboardTwo[index][2] + initialDotBalls
                            bowlersScoreboardTwo[index][3] = bowlersScoreboardTwo[index][3] + initialScore
                            bowlersScoreboardTwo[index][4] = bowlersScoreboardTwo[index][4] + initialOut
                            bowlersScoreboardTwo[index][5] = bowlersScoreboardTwo[index][3] / 20
                            initialBowlerBallsCount = 20
                            # print('     {}     ({}){} [{}x4 {}x6]'.format(batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour, initialStrikeSix))
                            print('     b. {}     {}({}){} [{}x4 {}x6]'.format(bowlerPresent,batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour,initialStrikeSix))
                            print('     {}     ({}){} [{}x4 {}x6]'.format(batsman2,intialNonStrikerRuns,initialNonStrikerBallsCount, initialNonStrikeFour, initialNonStrikeSix))
                            print('     {}     {}-{}-{}-{}'.format(bowlerPresent,initialBowlerBallsCount,bowlersScoreboardTwo[index][2],bowlersScoreboardTwo[index][3],bowlersScoreboardTwo[index][4]))
                            print()
                        else:
                            iBall = str(iBall)
                            tempBalls = iBall[1:]
                            tempBalls = int(tempBalls)
                            bowlersScoreboardTwo[index][1] = bowlersScoreboardTwo[index][1] + tempBalls
                            bowlersScoreboardTwo[index][2] = bowlersScoreboardTwo[index][2] + initialDotBalls
                            bowlersScoreboardTwo[index][3] = bowlersScoreboardTwo[index][3] + initialScore
                            bowlersScoreboardTwo[index][4] = bowlersScoreboardTwo[index][4] + initialOut
                            bowlersScoreboardTwo[index][5] = bowlersScoreboardTwo[index][3] / bowlersScoreboardTwo[index][1]
                            initialBowlerBallsCount = 10 + tempBalls
                            # print('     b. {}     {}({}){} [{}x4 {}x6]'.format(bowlerPresent,batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour,initialStrikeSix))
                            print('     {}     ({}){} [{}x4 {}x6]'.format(batsman1,initialStrikerRuns,initialStrikerBallsCount, initialStrikeFour, initialStrikeSix))
                            print('     {}     ({}){} [{}x4 {}x6]'.format(batsman2,intialNonStrikerRuns,initialNonStrikerBallsCount, initialNonStrikeFour, initialNonStrikeSix))
                            print('     {}     {}-{}-{}-{}'.format(bowlerPresent,initialBowlerBallsCount,bowlersScoreboardTwo[index][2],bowlersScoreboardTwo[index][3],bowlersScoreboardTwo[index][4]))
                            print()
            # print('     {}     {}-{}-{}-{}'.format(bowlerPresent,'10',initialDotBalls,initialScore,initialOut))
            print()
            wicketsDiffer = 10 - totalWickets
            print()
            print('     End of innings (Balls '+str(count)+')')
            rr = totalScore / (count / 10)
            print('     '+team1+'     '+str(totalScore)+'/'+str(totalWickets)+'  (RR: {:.2f})'.format(rr))
            print()
            print('     '+team1+' win by '+str(wicketsDiffer)+' wickets.')
            break
        
        if totalWickets == 10:
            print()
            for i in bowlingPlayers:
                if i == bowlerPresent:
                    index = bowlingPlayers.index(i)
                    if bowlersScoreboardTwo[index][1] == 0:
                        if iBall == 100:
                            bowlersScoreboardTwo[index][1] = bowlersScoreboardTwo[index][1] + 10
                            bowlersScoreboardTwo[index][2] = bowlersScoreboardTwo[index][2] + initialDotBalls
                            bowlersScoreboardTwo[index][3] = bowlersScoreboardTwo[index][3] + initialScore
                            bowlersScoreboardTwo[index][4] = bowlersScoreboardTwo[index][4] + initialOut
                            bowlersScoreboardTwo[index][5] = bowlersScoreboardTwo[index][3] / 20
                            initialBowlerBallsCount = 20
                            # print('     {}     ({}){} [{}x4 {}x6]'.format(batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour, initialStrikeSix))
                            if outType == 'Bowled':
                                print('     b. {}     {}({}){} [{}x4 {}x6]'.format(bowlerPresent,batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour,initialStrikeSix))
                            elif outType == 'Stumped':
                                print('     st. {}     b. {}     {}({}){} [{}x4 {}x6]'.format(*keeper,bowlerPresent,batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour,initialStrikeSix))
                            elif outType == 'Caught':
                                print('     c. {}     b. {}     {}({}){} [{}x4 {}x6]'.format(cPlayer,bowlerPresent,batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour,initialStrikeSix))
                             
                            # print('     b. {}     {}({}){} [{}x4 {}x6]'.format(bowlerPresent,batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour,initialStrikeSix))
                            print('     {}     ({}){} [{}x4 {}x6]'.format(batsman2,intialNonStrikerRuns,initialNonStrikerBallsCount, initialNonStrikeFour, initialNonStrikeSix))
                            print('     {}     {}-{}-{}-{}'.format(bowlerPresent,initialBowlerBallsCount,bowlersScoreboardTwo[index][2],bowlersScoreboardTwo[index][3],bowlersScoreboardTwo[index][4]))
                            print()
                        else:
                            iBall = str(iBall)
                            tempBalls = iBall[1:]
                            tempBalls = int(tempBalls)
                            bowlersScoreboardTwo[index][1] = bowlersScoreboardTwo[index][1] + tempBalls
                            bowlersScoreboardTwo[index][2] = bowlersScoreboardTwo[index][2] + initialDotBalls
                            bowlersScoreboardTwo[index][3] = bowlersScoreboardTwo[index][3] + initialScore
                            bowlersScoreboardTwo[index][4] = bowlersScoreboardTwo[index][4] + initialOut
                            bowlersScoreboardTwo[index][5] = bowlersScoreboardTwo[index][3] / bowlersScoreboardTwo[index][1]
                            initialBowlerBallsCount = 10 + tempBalls
                            # print('     {}     ({}){} [{}x4 {}x6]'.format(batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour, initialStrikeSix))
                            if outType == 'Bowled':
                                print('     b. {}     {}({}){} [{}x4 {}x6]'.format(bowlerPresent,batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour,initialStrikeSix))
                            elif outType == 'Stumped':
                                print('     st. {}     b. {}     {}({}){} [{}x4 {}x6]'.format(*keeper,bowlerPresent,batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour,initialStrikeSix))
                            elif outType == 'Caught':
                                print('     c. {}     b. {}     {}({}){} [{}x4 {}x6]'.format(cPlayer,bowlerPresent,batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour,initialStrikeSix))
                             
                            # print('     b. {}     {}({}){} [{}x4 {}x6]'.format(bowlerPresent,batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour,initialStrikeSix))
                            print('     {}     ({}){} [{}x4 {}x6]'.format(batsman2,intialNonStrikerRuns,initialNonStrikerBallsCount, initialNonStrikeFour, initialNonStrikeSix))
                            print('     {}     {}-{}-{}-{}'.format(bowlerPresent,initialBowlerBallsCount,bowlersScoreboardTwo[index][2],bowlersScoreboardTwo[index][3],bowlersScoreboardTwo[index][4]))
                            print()
                    elif bowlersScoreboardTwo[index][1] == 10:
                        if iBall == 100:
                            bowlersScoreboardTwo[index][1] = bowlersScoreboardTwo[index][1] + 10
                            bowlersScoreboardTwo[index][2] = bowlersScoreboardTwo[index][2] + initialDotBalls
                            bowlersScoreboardTwo[index][3] = bowlersScoreboardTwo[index][3] + initialScore
                            bowlersScoreboardTwo[index][4] = bowlersScoreboardTwo[index][4] + initialOut
                            bowlersScoreboardTwo[index][5] = bowlersScoreboardTwo[index][3] / 20
                            initialBowlerBallsCount = 20
                            # print('     {}     ({}){} [{}x4 {}x6]'.format(batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour, initialStrikeSix))
                            if outType == 'Bowled':
                                print('     b. {}     {}({}){} [{}x4 {}x6]'.format(bowlerPresent,batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour,initialStrikeSix))
                            elif outType == 'Stumped':
                                print('     st. {}     b. {}     {}({}){} [{}x4 {}x6]'.format(*keeper,bowlerPresent,batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour,initialStrikeSix))
                            elif outType == 'Caught':
                                print('     c. {}     b. {}     {}({}){} [{}x4 {}x6]'.format(cPlayer,bowlerPresent,batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour,initialStrikeSix))
                             
                            # print('     b. {}     {}({}){} [{}x4 {}x6]'.format(bowlerPresent,batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour,initialStrikeSix))
                            print('     {}     ({}){} [{}x4 {}x6]'.format(batsman2,intialNonStrikerRuns,initialNonStrikerBallsCount, initialNonStrikeFour, initialNonStrikeSix))
                            print('     {}     {}-{}-{}-{}'.format(bowlerPresent,initialBowlerBallsCount,bowlersScoreboardTwo[index][2],bowlersScoreboardTwo[index][3],bowlersScoreboardTwo[index][4]))
                            print()
                        else:
                            iBall = str(iBall)
                            tempBalls = iBall[1:]
                            tempBalls = int(tempBalls)
                            bowlersScoreboardTwo[index][1] = bowlersScoreboardTwo[index][1] + tempBalls
                            bowlersScoreboardTwo[index][2] = bowlersScoreboardTwo[index][2] + initialDotBalls
                            bowlersScoreboardTwo[index][3] = bowlersScoreboardTwo[index][3] + initialScore
                            bowlersScoreboardTwo[index][4] = bowlersScoreboardTwo[index][4] + initialOut
                            bowlersScoreboardTwo[index][5] = bowlersScoreboardTwo[index][3] / bowlersScoreboardTwo[index][1]
                            initialBowlerBallsCount = 10 + tempBalls
                            # print('     {}     ({}){} [{}x4 {}x6]'.format(batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour, initialStrikeSix))
                            print('     b. {}     {}({}){} [{}x4 {}x6]'.format(bowlerPresent,batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour,initialStrikeSix))
                            print('     {}     ({}){} [{}x4 {}x6]'.format(batsman2,intialNonStrikerRuns,initialNonStrikerBallsCount, initialNonStrikeFour, initialNonStrikeSix))
                            print('     {}     {}-{}-{}-{}'.format(bowlerPresent,initialBowlerBallsCount,bowlersScoreboardTwo[index][2],bowlersScoreboardTwo[index][3],bowlersScoreboardTwo[index][4]))
                            print()
            # print('     {}     {}-{}-{}-{}'.format(bowlerPresent,'10',initialDotBalls,initialScore,initialOut))
            print()
            if totalScore < target:
                print('     END of '+str(count)+' balls ('+str(initialScore)+' runs)')
                print('     '+team1+'     '+str(totalScore)+'/'+str(totalWickets))
                rr = totalScore / (count / 10)
                rrr = (target - totalScore) / ((100 - count) / 10)
                
                print('     RR: {:.2f}     RRR: {:.2f}'.format(rr, rrr))
                print()
            print('     End of innings (Balls '+str(count)+')')
            rr = totalScore / (count / 10)
            print('     '+team1+'     '+str(totalScore)+'/'+str(totalWickets)+'  (RR: {:.2f})'.format(rr))
            
            print()
            if totalScore < target:
                if initialStrikerBallsCount == 0:
                    sr1 = 0
                else:
                    sr1 = initialStrikerRuns * 100 // initialStrikerBallsCount
                sr2 = intialNonStrikerRuns * 100 // initialNonStrikerBallsCount
                
                if outType == 'Bowled':
                    batsmenScoreboard2.append([batsman1, 'b. ','', bowlerPresent, initialStrikerRuns, initialStrikerBallsCount, 
                   initialStrikeFour, initialStrikeSix, sr1])
                elif outType == 'Caught':
                    batsmenScoreboard2.append([batsman1, 'c. ',cPlayer, bowlerPresent, initialStrikerRuns, initialStrikerBallsCount, 
                   initialStrikeFour, initialStrikeSix, sr1])
                elif outType == 'Stumped':
                    batsmenScoreboard2.append([batsman1, 'st. ',*keeper, bowlerPresent, initialStrikerRuns, initialStrikerBallsCount, 
                   initialStrikeFour, initialStrikeSix, sr1])
                # batsmenScoreboard2.append([batsman1, bowlerPresent, initialStrikerRuns, initialStrikerBallsCount, 
                #    initialStrikeFour, initialStrikeSix, sr1])
                batsmenScoreboard2.append([batsman2, "Not Out",'','', intialNonStrikerRuns, initialNonStrikerBallsCount, 
                initialNonStrikeFour, initialNonStrikeSix, sr2])
                print()
                diff = target - totalScore - 1
                print('     '+team2+' win by '+str(diff)+' runs.')
                break
            
        
        #wideball
        if ballOutcome == ['Wide']:
            wideBallNo = str(i)
            
            if bowlerPresentRating in range(71, 76):
                #increase
                batsman1Rating[0] = batsman1Rating[0] + 3
                batsman1Rating[1] = batsman1Rating[1] + 3
                batsman1Rating[2] = batsman1Rating[2] + 1
                #decrease
                batsman1Rating[3] = batsman1Rating[3] - 0.3
                batsman1Rating[4] = batsman1Rating[4] - 1.3
                batsman1Rating[5] = batsman1Rating[5] - 0.7
            elif bowlerPresentRating in range(76, 81):
                #increase
                batsman1Rating[0] = batsman1Rating[0] + 5
                batsman1Rating[1] = batsman1Rating[1] + 5
                batsman1Rating[2] = batsman1Rating[2] + 3
                batsman1Rating[6] = batsman1Rating[6] + 1
                #decrease
                batsman1Rating[3] = batsman1Rating[3] - 0.7
                batsman1Rating[4] = batsman1Rating[4] - 2
                batsman1Rating[5] = batsman1Rating[5] - 1.5
            elif bowlerPresentRating in range(81, 86):
                #increase
                batsman1Rating[0] = batsman1Rating[0] + 6
                batsman1Rating[1] = batsman1Rating[1] + 6
                batsman1Rating[2] = batsman1Rating[2] + 4
                batsman1Rating[6] = batsman1Rating[6] + 2
                #decrease
                batsman1Rating[3] = batsman1Rating[3] - 1
                batsman1Rating[4] = batsman1Rating[4] - 3
                batsman1Rating[5] = batsman1Rating[5] - 2
            elif bowlerPresentRating in range(86, 91):
                #increase
                batsman1Rating[0] = batsman1Rating[0] + 7
                batsman1Rating[1] = batsman1Rating[1] + 7
                batsman1Rating[2] = batsman1Rating[2] + 5
                batsman1Rating[6] = batsman1Rating[6] + 3
                #decrease
                batsman1Rating[3] = batsman1Rating[3] - 2
                batsman1Rating[4] = batsman1Rating[4] - 4
                batsman1Rating[5] = batsman1Rating[5] - 3
            elif bowlerPresentRating in range(91, 96):
                #increase
                batsman1Rating[0] = batsman1Rating[0] + 8
                batsman1Rating[1] = batsman1Rating[1] + 8
                batsman1Rating[2] = batsman1Rating[2] + 6
                batsman1Rating[6] = batsman1Rating[6] + 7
                #decrease
                batsman1Rating[3] = batsman1Rating[3] - 3
                batsman1Rating[4] = batsman1Rating[4] - 5
                batsman1Rating[5] = batsman1Rating[5] - 4
            elif bowlerPresentRating in range(0,55):
                #increase
                batsman1Rating[0] = batsman1Rating[0] - 25
                batsman1Rating[1] = batsman1Rating[1] + 15
                batsman1Rating[2] = batsman1Rating[2] + 15
                batsman1Rating[6] = batsman1Rating[6] - 7
                #decrease
                batsman1Rating[3] = batsman1Rating[3] + 3
                batsman1Rating[4] = batsman1Rating[4] + 6
                batsman1Rating[5] = batsman1Rating[5] + 6
            elif bowlerPresentRating in range(55,61):
                #increase
                batsman1Rating[0] = batsman1Rating[0] + 0.5
                batsman1Rating[1] = batsman1Rating[1] + 0.5
                batsman1Rating[2] = batsman1Rating[2] + 0.5
                batsman1Rating[6] = batsman1Rating[6] + 0.5
                #decrease
                batsman1Rating[3] = batsman1Rating[3] - 0.5
                batsman1Rating[4] = batsman1Rating[4] - 0.5
                batsman1Rating[5] = batsman1Rating[5] - 0.5
            elif bowlerPresentRating in range(61,66):
                #increase
                batsman1Rating[0] = batsman1Rating[0] + 1
                batsman1Rating[1] = batsman1Rating[1] + 1
                batsman1Rating[2] = batsman1Rating[2] + 1
                batsman1Rating[6] = batsman1Rating[6] + 1
                #decrease
                batsman1Rating[3] = batsman1Rating[3] - 0.5
                batsman1Rating[4] = batsman1Rating[4] - 0.5
                batsman1Rating[5] = batsman1Rating[5] - 0.5
            elif bowlerPresentRating in range(66,71):
                #increase
                batsman1Rating[0] = batsman1Rating[0] + 2
                batsman1Rating[1] = batsman1Rating[1] + 2
                batsman1Rating[2] = batsman1Rating[2] + 2
                batsman1Rating[6] = batsman1Rating[6] + 2
                #decrease
                batsman1Rating[3] = batsman1Rating[3] - 1
                batsman1Rating[4] = batsman1Rating[4] - 1
                batsman1Rating[5] = batsman1Rating[5] - 1
            
            ballOutcome = random.choices(outcomes, weights=(batsman1Rating), k=1)
            callBatsman1Rating()
            
            #First over posibilities 'Ball 0X'
            if len(str(i)) == 1:
                ball = 'Ball 0'+str(i)+' : '
                if ballOutcome == [1] or ballOutcome == ['Leg Bye']:
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
                    totalExtras = totalExtras + 1
                elif ballOutcome == ['OUT']:
                    initialOut = initialOut + 1
                    totalWickets = totalWickets + 1
                    initialDotBalls = initialDotBalls + 1
                elif ballOutcome == [0]:
                    initialDotBalls = initialDotBalls + 1
                elif ballOutcome == ['Leg Bye']:
                    totalExtras = totalExtras + 1
                else:
                    pass
                
                if ballOutcome == ['OUT']:
                    outType = random.choice(outList)
                    if outType == 'Caught':
                        cPlayer = random.choice(oppTeam)
                        print('{} {} to {}, {} by {}, {}'.format(ball,bowlerPresent,batsman1,outType,cPlayer,random.choice(outComm)))
                    elif outType == 'Bowled':
                        print('{} {} to {}, {}, {}'.format(ball,bowlerPresent,batsman1,outType,random.choice(outComm)))
                    elif outType == 'Stumped':
                        print('{} {} to {}, {} by {}, {}'.format(ball,bowlerPresent,batsman1,outType,*keeper,random.choice(outComm)))
                            # print('{} {} to {}, {}, {}'.format(ball,bowlerPresent,batsman1,*ballOutcome,random.choice(outComm)))
                elif ballOutcome == ['Wide']:
                    print('{} {} to {},{}, {}'.format(ball,bowlerPresent,batsman1,*ballOutcome,'Thats a wide ball from '+bowlerPresent))
                elif ballOutcome == [1]:
                    print('{} {} to {}, one {}, {}'.format(ball,bowlerPresent,batsman1,'run',random.choice(oneComm).replace('batsman', batsman1)))
                elif ballOutcome == [2]:
                    print('{} {} to {}, two {}, {}'.format(ball,bowlerPresent,batsman1,'runs',random.choice(twoComm).replace('batsman', batsman1)))
                elif ballOutcome == [3]:
                    print('{} {} to {}, three {}, {}'.format(ball,bowlerPresent,batsman1,'runs',random.choice(threeComm).replace('batsman', batsman1)))
                elif ballOutcome == [4]:
                    print('{} {} to {}, FOUR {}, {}'.format(ball,bowlerPresent,batsman1,'runs',random.choice(fourComm).replace('batsman', batsman1)))
                elif ballOutcome == [6]:
                    print('{} {} to {}, SIX ! {}, {}'.format(ball,bowlerPresent,batsman1,'runs',random.choice(sixComm).replace('batsman', batsman1)))
                elif ballOutcome == [0]:
                    print('{} {} to {}, dot {}, {}'.format(ball,bowlerPresent,batsman1,'',random.choice(zeroComm).replace('batsman', batsman1)))
                elif ballOutcome == ['Leg Bye']:
                    print('{} {} to {}, Leg Bye , {}'.format(ball,bowlerPresent,batsman1,random.choice(oneComm).replace('batsman', batsman1)))
        
                #Checking for winner after every ball
                if totalScore >= target:
                    sr1 = initialStrikerRuns * 100 // initialStrikerBallsCount
                    sr2 = intialNonStrikerRuns * 100 // initialNonStrikerBallsCount
                    batsmenScoreboard2.append([batsman1, "Not Out",'','', initialStrikerRuns, initialStrikerBallsCount, 
                   initialStrikeFour, initialStrikeSix, sr1])
                    batsmenScoreboard2.append([batsman2, "Not Out",'','', intialNonStrikerRuns, initialNonStrikerBallsCount, 
                   initialNonStrikeFour, initialNonStrikeSix, sr2])
                    print()
                    for i in bowlingPlayers:
                        if i == bowlerPresent:
                            index = bowlingPlayers.index(i)
                            if bowlersScoreboardTwo[index][1] == 0:
                                if iBall == 100:
                                    bowlersScoreboardTwo[index][1] = bowlersScoreboardTwo[index][1] + 10
                                    bowlersScoreboardTwo[index][2] = bowlersScoreboardTwo[index][2] + initialDotBalls
                                    bowlersScoreboardTwo[index][3] = bowlersScoreboardTwo[index][3] + initialScore
                                    bowlersScoreboardTwo[index][4] = bowlersScoreboardTwo[index][4] + initialOut
                                    bowlersScoreboardTwo[index][5] = bowlersScoreboardTwo[index][3] / 20
                                    initialBowlerBallsCount = 20
                                    # print('     {}     ({}){} [{}x4 {}x6]'.format(batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour, initialStrikeSix))
                                    if outType == 'Bowled':
                                        print('     b. {}     {}({}){} [{}x4 {}x6]'.format(bowlerPresent,batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour,initialStrikeSix))
                                    elif outType == 'Stumped':
                                        print('     st. {}     b. {}     {}({}){} [{}x4 {}x6]'.format(*keeper,bowlerPresent,batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour,initialStrikeSix))
                                    elif outType == 'Caught':
                                        print('     c. {}     b. {}     {}({}){} [{}x4 {}x6]'.format(cPlayer,bowlerPresent,batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour,initialStrikeSix))
                                     
                                    # print('     b. {}     {}({}){} [{}x4 {}x6]'.format(bowlerPresent,batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour,initialStrikeSix))
                                    print('     {}     ({}){} [{}x4 {}x6]'.format(batsman2,intialNonStrikerRuns,initialNonStrikerBallsCount, initialNonStrikeFour, initialNonStrikeSix))
                                    print('     {}     {}-{}-{}-{}'.format(bowlerPresent,initialBowlerBallsCount,bowlersScoreboardTwo[index][2],bowlersScoreboardTwo[index][3],bowlersScoreboardTwo[index][4]))
                                    print()
                                else:
                                    iBall = str(iBall)
                                    tempBalls = iBall[1:]
                                    tempBalls = int(tempBalls)
                                    bowlersScoreboardTwo[index][1] = bowlersScoreboardTwo[index][1] + tempBalls
                                    bowlersScoreboardTwo[index][2] = bowlersScoreboardTwo[index][2] + initialDotBalls
                                    bowlersScoreboardTwo[index][3] = bowlersScoreboardTwo[index][3] + initialScore
                                    bowlersScoreboardTwo[index][4] = bowlersScoreboardTwo[index][4] + initialOut
                                    bowlersScoreboardTwo[index][5] = bowlersScoreboardTwo[index][3] / bowlersScoreboardTwo[index][1]
                                    initialBowlerBallsCount = 10 + tempBalls
                                    # print('     {}     ({}){} [{}x4 {}x6]'.format(batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour, initialStrikeSix))
                                    print('     b. {}     {}({}){} [{}x4 {}x6]'.format(bowlerPresent,batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour,initialStrikeSix))
                                    print('     {}     ({}){} [{}x4 {}x6]'.format(batsman2,intialNonStrikerRuns,initialNonStrikerBallsCount, initialNonStrikeFour, initialNonStrikeSix))
                                    print('     {}     {}-{}-{}-{}'.format(bowlerPresent,initialBowlerBallsCount,bowlersScoreboardTwo[index][2],bowlersScoreboardTwo[index][3],bowlersScoreboardTwo[index][4]))
                                    print()
                            elif bowlersScoreboardTwo[index][1] == 10:
                                if iBall == 100:
                                    bowlersScoreboardTwo[index][1] = bowlersScoreboardTwo[index][1] + 10
                                    bowlersScoreboardTwo[index][2] = bowlersScoreboardTwo[index][2] + initialDotBalls
                                    bowlersScoreboardTwo[index][3] = bowlersScoreboardTwo[index][3] + initialScore
                                    bowlersScoreboardTwo[index][4] = bowlersScoreboardTwo[index][4] + initialOut
                                    bowlersScoreboardTwo[index][5] = bowlersScoreboardTwo[index][3] / 20
                                    initialBowlerBallsCount = 20
                                    # print('     {}     ({}){} [{}x4 {}x6]'.format(batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour, initialStrikeSix))
                                    if outType == 'Bowled':
                                        print('     b. {}     {}({}){} [{}x4 {}x6]'.format(bowlerPresent,batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour,initialStrikeSix))
                                    elif outType == 'Stumped':
                                        print('     st. {}     b. {}     {}({}){} [{}x4 {}x6]'.format(*keeper,bowlerPresent,batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour,initialStrikeSix))
                                    elif outType == 'Caught':
                                        print('     c. {}     b. {}     {}({}){} [{}x4 {}x6]'.format(cPlayer,bowlerPresent,batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour,initialStrikeSix))
                                     
                                    # print('     b. {}     {}({}){} [{}x4 {}x6]'.format(bowlerPresent,batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour,initialStrikeSix))
                                    print('     {}     ({}){} [{}x4 {}x6]'.format(batsman2,intialNonStrikerRuns,initialNonStrikerBallsCount, initialNonStrikeFour, initialNonStrikeSix))
                                    print('     {}     {}-{}-{}-{}'.format(bowlerPresent,initialBowlerBallsCount,bowlersScoreboardTwo[index][2],bowlersScoreboardTwo[index][3],bowlersScoreboardTwo[index][4]))
                                    print()
                                else:
                                    iBall = str(iBall)
                                    tempBalls = iBall[1:]
                                    tempBalls = int(tempBalls)
                                    bowlersScoreboardTwo[index][1] = bowlersScoreboardTwo[index][1] + tempBalls
                                    bowlersScoreboardTwo[index][2] = bowlersScoreboardTwo[index][2] + initialDotBalls
                                    bowlersScoreboardTwo[index][3] = bowlersScoreboardTwo[index][3] + initialScore
                                    bowlersScoreboardTwo[index][4] = bowlersScoreboardTwo[index][4] + initialOut
                                    bowlersScoreboardTwo[index][5] = bowlersScoreboardTwo[index][3] / bowlersScoreboardTwo[index][1]
                                    initialBowlerBallsCount = 10 + tempBalls
                                    # print('     {}     ({}){} [{}x4 {}x6]'.format(batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour, initialStrikeSix))
                                    if outType == 'Bowled':
                                        print('     b. {}     {}({}){} [{}x4 {}x6]'.format(bowlerPresent,batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour,initialStrikeSix))
                                    elif outType == 'Stumped':
                                        print('     st. {}     b. {}     {}({}){} [{}x4 {}x6]'.format(*keeper,bowlerPresent,batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour,initialStrikeSix))
                                    elif outType == 'Caught':
                                        print('     c. {}     b. {}     {}({}){} [{}x4 {}x6]'.format(cPlayer,bowlerPresent,batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour,initialStrikeSix))
                                     
                                    # print('     b. {}     {}({}){} [{}x4 {}x6]'.format(bowlerPresent,batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour,initialStrikeSix))
                                    print('     {}     ({}){} [{}x4 {}x6]'.format(batsman2,intialNonStrikerRuns,initialNonStrikerBallsCount, initialNonStrikeFour, initialNonStrikeSix))
                                    print('     {}     {}-{}-{}-{}'.format(bowlerPresent,initialBowlerBallsCount,bowlersScoreboardTwo[index][2],bowlersScoreboardTwo[index][3],bowlersScoreboardTwo[index][4]))
                                    print()
                    # print('     {}     {}-{}-{}-{}'.format(bowlerPresent,'10',initialDotBalls,initialScore,initialOut))
                    print()
                    print('     END of '+str(count)+' balls ('+str(initialScore)+' runs)')
                    print('     '+team1+'     '+str(totalScore)+'/'+str(totalWickets))
                    rr = totalScore / (count / 10)
                    rrr = (target - totalScore) / ((100 - count) / 10)
                    print('     RR: {:.2f}     RRR: {:.2f}'.format(rr, rrr))
                    print()
                    wicketsDiffer = 10 - totalWickets
                    print('     '+team1+' win by '+str(wicketsDiffer)+' wickets.')
                    break
            
                # print('{} {} to {} : {} runs'.format(ball,bowlerPresent,batsman1,*ballOutcome))
                if totalWickets == 10:
                    sr1 = initialStrikerRuns * 100 // initialStrikerBallsCount
                    sr2 = intialNonStrikerRuns * 100 // initialNonStrikerBallsCount
                    if outType == 'Bowled':
                        batsmenScoreboard2.append([batsman1, 'b. ','', bowlerPresent, initialStrikerRuns, initialStrikerBallsCount, 
                       initialStrikeFour, initialStrikeSix, sr1])
                    elif outType == 'Caught':
                        batsmenScoreboard2.append([batsman1, 'c. ',cPlayer, bowlerPresent, initialStrikerRuns, initialStrikerBallsCount, 
                       initialStrikeFour, initialStrikeSix, sr1])
                    elif outType == 'Stumped':
                        batsmenScoreboard2.append([batsman1, 'st. ',*keeper, bowlerPresent, initialStrikerRuns, initialStrikerBallsCount, 
                       initialStrikeFour, initialStrikeSix, sr1])
                   #  batsmenScoreboard2.append([batsman1, bowlerPresent, initialStrikerRuns, initialStrikerBallsCount, 
                   # initialStrikeFour, initialStrikeSix, sr1])
                    batsmenScoreboard2.append([batsman2, "Not Out",'','', intialNonStrikerRuns, initialNonStrikerBallsCount, 
                   initialNonStrikeFour, initialNonStrikeSix, sr2])
                    print()
                    for i in bowlingPlayers:
                        if i == bowlerPresent:
                            index = bowlingPlayers.index(i)
                            if bowlersScoreboardTwo[index][1] == 0:
                                if iBall == 100:
                                    bowlersScoreboardTwo[index][1] = bowlersScoreboardTwo[index][1] + 10
                                    bowlersScoreboardTwo[index][2] = bowlersScoreboardTwo[index][2] + initialDotBalls
                                    bowlersScoreboardTwo[index][3] = bowlersScoreboardTwo[index][3] + initialScore
                                    bowlersScoreboardTwo[index][4] = bowlersScoreboardTwo[index][4] + initialOut
                                    bowlersScoreboardTwo[index][5] = bowlersScoreboardTwo[index][3] / 20
                                    initialBowlerBallsCount = 20
                                    # print('     {}     ({}){} [{}x4 {}x6]'.format(batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour, initialStrikeSix))
                                    if outType == 'Bowled':
                                        print('     b. {}     {}({}){} [{}x4 {}x6]'.format(bowlerPresent,batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour,initialStrikeSix))
                                    elif outType == 'Stumped':
                                        print('     st. {}     b. {}     {}({}){} [{}x4 {}x6]'.format(*keeper,bowlerPresent,batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour,initialStrikeSix))
                                    elif outType == 'Caught':
                                        print('     c. {}     b. {}     {}({}){} [{}x4 {}x6]'.format(cPlayer,bowlerPresent,batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour,initialStrikeSix))
                                    # print('     b. {}     {}({}){} [{}x4 {}x6]'.format(bowlerPresent,batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour,initialStrikeSix))
                                    print('     {}     ({}){} [{}x4 {}x6]'.format(batsman2,intialNonStrikerRuns,initialNonStrikerBallsCount, initialNonStrikeFour, initialNonStrikeSix))
                                    print('     {}     {}-{}-{}-{}'.format(bowlerPresent,initialBowlerBallsCount,bowlersScoreboardTwo[index][2],bowlersScoreboardTwo[index][3],bowlersScoreboardTwo[index][4]))
                                    print()
                                else:
                                    iBall = str(iBall)
                                    tempBalls = iBall[1:]
                                    tempBalls = int(tempBalls)
                                    bowlersScoreboardTwo[index][1] = bowlersScoreboardTwo[index][1] + tempBalls
                                    bowlersScoreboardTwo[index][2] = bowlersScoreboardTwo[index][2] + initialDotBalls
                                    bowlersScoreboardTwo[index][3] = bowlersScoreboardTwo[index][3] + initialScore
                                    bowlersScoreboardTwo[index][4] = bowlersScoreboardTwo[index][4] + initialOut
                                    bowlersScoreboardTwo[index][5] = bowlersScoreboardTwo[index][3] / bowlersScoreboardTwo[index][1]
                                    initialBowlerBallsCount = 10 + tempBalls
                                    # print('     {}     ({}){} [{}x4 {}x6]'.format(batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour, initialStrikeSix))
                                    if outType == 'Bowled':
                                        print('     b. {}     {}({}){} [{}x4 {}x6]'.format(bowlerPresent,batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour,initialStrikeSix))
                                    elif outType == 'Stumped':
                                        print('     st. {}     b. {}     {}({}){} [{}x4 {}x6]'.format(*keeper,bowlerPresent,batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour,initialStrikeSix))
                                    elif outType == 'Caught':
                                        print('     c. {}     b. {}     {}({}){} [{}x4 {}x6]'.format(cPlayer,bowlerPresent,batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour,initialStrikeSix))
                                     
                                    # print('     b. {}     {}({}){} [{}x4 {}x6]'.format(bowlerPresent,batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour,initialStrikeSix))
                                    print('     {}     ({}){} [{}x4 {}x6]'.format(batsman2,intialNonStrikerRuns,initialNonStrikerBallsCount, initialNonStrikeFour, initialNonStrikeSix))
                                    print('     {}     {}-{}-{}-{}'.format(bowlerPresent,initialBowlerBallsCount,bowlersScoreboardTwo[index][2],bowlersScoreboardTwo[index][3],bowlersScoreboardTwo[index][4]))
                                    print()
                            elif bowlersScoreboardTwo[index][1] == 10:
                                if iBall == 100:
                                    bowlersScoreboardTwo[index][1] = bowlersScoreboardTwo[index][1] + 10
                                    bowlersScoreboardTwo[index][2] = bowlersScoreboardTwo[index][2] + initialDotBalls
                                    bowlersScoreboardTwo[index][3] = bowlersScoreboardTwo[index][3] + initialScore
                                    bowlersScoreboardTwo[index][4] = bowlersScoreboardTwo[index][4] + initialOut
                                    bowlersScoreboardTwo[index][5] = bowlersScoreboardTwo[index][3] / 20
                                    initialBowlerBallsCount = 20
                                    # print('     {}     ({}){} [{}x4 {}x6]'.format(batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour, initialStrikeSix))
                                    if outType == 'Bowled':
                                        print('     b. {}     {}({}){} [{}x4 {}x6]'.format(bowlerPresent,batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour,initialStrikeSix))
                                    elif outType == 'Stumped':
                                        print('     st. {}     b. {}     {}({}){} [{}x4 {}x6]'.format(*keeper,bowlerPresent,batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour,initialStrikeSix))
                                    elif outType == 'Caught':
                                        print('     c. {}     b. {}     {}({}){} [{}x4 {}x6]'.format(cPlayer,bowlerPresent,batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour,initialStrikeSix))
                                     
                                    # print('     b. {}     {}({}){} [{}x4 {}x6]'.format(bowlerPresent,batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour,initialStrikeSix))
                                    print('     {}     ({}){} [{}x4 {}x6]'.format(batsman2,intialNonStrikerRuns,initialNonStrikerBallsCount, initialNonStrikeFour, initialNonStrikeSix))
                                    print('     {}     {}-{}-{}-{}'.format(bowlerPresent,initialBowlerBallsCount,bowlersScoreboardTwo[index][2],bowlersScoreboardTwo[index][3],bowlersScoreboardTwo[index][4]))
                                    print()
                                else:
                                    iBall = str(iBall)
                                    tempBalls = iBall[1:]
                                    tempBalls = int(tempBalls)
                                    bowlersScoreboardTwo[index][1] = bowlersScoreboardTwo[index][1] + tempBalls
                                    bowlersScoreboardTwo[index][2] = bowlersScoreboardTwo[index][2] + initialDotBalls
                                    bowlersScoreboardTwo[index][3] = bowlersScoreboardTwo[index][3] + initialScore
                                    bowlersScoreboardTwo[index][4] = bowlersScoreboardTwo[index][4] + initialOut
                                    bowlersScoreboardTwo[index][5] = bowlersScoreboardTwo[index][3] / bowlersScoreboardTwo[index][1]
                                    initialBowlerBallsCount = 10 + tempBalls
                                    # print('     {}     ({}){} [{}x4 {}x6]'.format(batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour, initialStrikeSix))
                                    print('     b. {}     {}({}){} [{}x4 {}x6]'.format(bowlerPresent,batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour,initialStrikeSix))
                                    print('     {}     ({}){} [{}x4 {}x6]'.format(batsman2,intialNonStrikerRuns,initialNonStrikerBallsCount, initialNonStrikeFour, initialNonStrikeSix))
                                    print('     {}     {}-{}-{}-{}'.format(bowlerPresent,initialBowlerBallsCount,bowlersScoreboardTwo[index][2],bowlersScoreboardTwo[index][3],bowlersScoreboardTwo[index][4]))
                                    print()
                    # print('     {}     {}-{}-{}-{}'.format(bowlerPresent,'10',initialDotBalls,initialScore,initialOut))
                    print()
                    if totalScore < target:
                        diff = target - totalScore - 1
                        print(team2+' win by '+str(diff)+' runs.')

                    print('     End of innings (Balls '+str(count)+')')
                    rr = totalScore / (count / 10)
                    print('     '+team1+'     '+str(totalScore)+'/'+str(totalWickets)+'  (RR: {:.2f})'.format(rr))
                    print()
                    # if totalScore < target:
                    #     diff = target - totalScore - 1
                    #     print(team2+' win by '+str(diff)+' runs.')
                    #     break
            else: #Rest 90 balls 'Ball 1X'
                ball = 'Ball '+str(i)+' : '
                if ballOutcome == [1] or ballOutcome == ['Leg Bye']:
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
                    totalExtras = totalExtras + 1
                elif ballOutcome == ['OUT']:
                    initialOut = initialOut + 1
                    totalWickets = totalWickets + 1
                    initialDotBalls = initialDotBalls + 1
                elif ballOutcome == [0]:
                    initialDotBalls = initialDotBalls + 1
                elif ballOutcome == ['Leg Bye']:
                    totalExtras = totalExtras + 1
                else:
                    pass
                
                if ballOutcome == ['OUT']:
                    outType = random.choice(outList)
                    if outType == 'Caught':
                        cPlayer = random.choice(oppTeam)
                        print('{} {} to {}, {} by {}, {}'.format(ball,bowlerPresent,batsman1,outType,cPlayer,random.choice(outComm)))
                    elif outType == 'Bowled':
                        print('{} {} to {}, {}, {}'.format(ball,bowlerPresent,batsman1,outType,random.choice(outComm)))
                    elif outType == 'Stumped':
                        print('{} {} to {}, {} by {}, {}'.format(ball,bowlerPresent,batsman1,outType,*keeper,random.choice(outComm)))
                    # print('{} {} to {}, {}, {}'.format(ball,bowlerPresent,batsman1,*ballOutcome,random.choice(outComm)))
                elif ballOutcome == ['Wide']:
                    print('{} {} to {},{}, {}'.format(ball,bowlerPresent,batsman1,*ballOutcome,'Thats a wide ball from '+bowlerPresent))
                elif ballOutcome == [1]:
                    print('{} {} to {}, one {}, {}'.format(ball,bowlerPresent,batsman1,'run',random.choice(oneComm).replace('batsman', batsman1)))
                elif ballOutcome == [2]:
                    print('{} {} to {}, two {}, {}'.format(ball,bowlerPresent,batsman1,'runs',random.choice(twoComm).replace('batsman', batsman1)))
                elif ballOutcome == [3]:
                    print('{} {} to {}, three {}, {}'.format(ball,bowlerPresent,batsman1,'runs',random.choice(threeComm).replace('batsman', batsman1)))
                elif ballOutcome == [4]:
                    print('{} {} to {}, FOUR {}, {}'.format(ball,bowlerPresent,batsman1,'runs',random.choice(fourComm).replace('batsman', batsman1)))
                elif ballOutcome == [6]:
                    print('{} {} to {}, SIX ! {}, {}'.format(ball,bowlerPresent,batsman1,'runs',random.choice(sixComm).replace('batsman', batsman1)))
                elif ballOutcome == [0]:
                    print('{} {} to {}, dot {}, {}'.format(ball,bowlerPresent,batsman1,'',random.choice(zeroComm).replace('batsman', batsman1)))
                elif ballOutcome == ['Leg Bye']:
                    print('{} {} to {}, Leg Bye , {}'.format(ball,bowlerPresent,batsman1,random.choice(oneComm).replace('batsman', batsman1)))
        
                
                #Checking for winner after every ball
                if totalScore >= target:
                    if initialStrikerBallsCount == 0:
                        sr1 = 0
                    else:
                        sr1 = initialStrikerRuns * 100 // initialStrikerBallsCount
                    sr2 = intialNonStrikerRuns * 100 // initialNonStrikerBallsCount
                    batsmenScoreboard2.append([batsman1, "Not Out",'','', initialStrikerRuns, initialStrikerBallsCount, 
                   initialStrikeFour, initialStrikeSix, sr1])
                    batsmenScoreboard2.append([batsman2, "Not Out",'','', intialNonStrikerRuns, initialNonStrikerBallsCount, 
                   initialNonStrikeFour, initialNonStrikeSix, sr2])
                    print()
                    for i in bowlingPlayers:
                        if i == bowlerPresent:
                            index = bowlingPlayers.index(i)
                            if bowlersScoreboardTwo[index][1] == 0:
                                if iBall == 100:
                                    bowlersScoreboardTwo[index][1] = bowlersScoreboardTwo[index][1] + 10
                                    bowlersScoreboardTwo[index][2] = bowlersScoreboardTwo[index][2] + initialDotBalls
                                    bowlersScoreboardTwo[index][3] = bowlersScoreboardTwo[index][3] + initialScore
                                    bowlersScoreboardTwo[index][4] = bowlersScoreboardTwo[index][4] + initialOut
                                    bowlersScoreboardTwo[index][5] = bowlersScoreboardTwo[index][3] / 20
                                    initialBowlerBallsCount = 20
                                    # print('     b. {}     {}({}){} [{}x4 {}x6]'.format(bowlerPresent,batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour,initialStrikeSix))
                                    print('     {}     ({}){} [{}x4 {}x6]'.format(batsman1,initialStrikerRuns,initialStrikerBallsCount, initialStrikeFour, initialStrikeSix))
                                    print('     {}     ({}){} [{}x4 {}x6]'.format(batsman2,intialNonStrikerRuns,initialNonStrikerBallsCount, initialNonStrikeFour, initialNonStrikeSix))
                                    print('     {}     {}-{}-{}-{}'.format(bowlerPresent,initialBowlerBallsCount,bowlersScoreboardTwo[index][2],bowlersScoreboardTwo[index][3],bowlersScoreboardTwo[index][4]))
                                    print()
                                else:
                                    iBall = str(iBall)
                                    tempBalls = iBall[1:]
                                    tempBalls = int(tempBalls)
                                    bowlersScoreboardTwo[index][1] = bowlersScoreboardTwo[index][1] + tempBalls
                                    bowlersScoreboardTwo[index][2] = bowlersScoreboardTwo[index][2] + initialDotBalls
                                    bowlersScoreboardTwo[index][3] = bowlersScoreboardTwo[index][3] + initialScore
                                    bowlersScoreboardTwo[index][4] = bowlersScoreboardTwo[index][4] + initialOut
                                    bowlersScoreboardTwo[index][5] = bowlersScoreboardTwo[index][3] / bowlersScoreboardTwo[index][1]
                                    initialBowlerBallsCount = 10 + tempBalls
   
                                    # print('     b. {}     {}({}){} [{}x4 {}x6]'.format(bowlerPresent,batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour,initialStrikeSix))
                                    print('     {}     ({}){} [{}x4 {}x6]'.format(batsman1,initialStrikerRuns,initialStrikerBallsCount, initialStrikeFour, initialStrikeSix))
                                    print('     {}     ({}){} [{}x4 {}x6]'.format(batsman2,intialNonStrikerRuns,initialNonStrikerBallsCount, initialNonStrikeFour, initialNonStrikeSix))
                                    print('     {}     {}-{}-{}-{}'.format(bowlerPresent,initialBowlerBallsCount,bowlersScoreboardTwo[index][2],bowlersScoreboardTwo[index][3],bowlersScoreboardTwo[index][4]))
                                    print()
                            elif bowlersScoreboardTwo[index][1] == 10:
                                if iBall == 100:
                                    bowlersScoreboardTwo[index][1] = bowlersScoreboardTwo[index][1] + 10
                                    bowlersScoreboardTwo[index][2] = bowlersScoreboardTwo[index][2] + initialDotBalls
                                    bowlersScoreboardTwo[index][3] = bowlersScoreboardTwo[index][3] + initialScore
                                    bowlersScoreboardTwo[index][4] = bowlersScoreboardTwo[index][4] + initialOut
                                    bowlersScoreboardTwo[index][5] = bowlersScoreboardTwo[index][3] / 20
                                    initialBowlerBallsCount = 20
         
                                    # print('     b. {}     {}({}){} [{}x4 {}x6]'.format(bowlerPresent,batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour,initialStrikeSix))
                                    print('     {}     ({}){} [{}x4 {}x6]'.format(batsman1,initialStrikerRuns,initialStrikerBallsCount, initialStrikeFour, initialStrikeSix))
                                    print('     {}     ({}){} [{}x4 {}x6]'.format(batsman2,intialNonStrikerRuns,initialNonStrikerBallsCount, initialNonStrikeFour, initialNonStrikeSix))
                                    print('     {}     {}-{}-{}-{}'.format(bowlerPresent,initialBowlerBallsCount,bowlersScoreboardTwo[index][2],bowlersScoreboardTwo[index][3],bowlersScoreboardTwo[index][4]))
                                    print()
                                else:
                                    iBall = str(iBall)
                                    tempBalls = iBall[1:]
                                    tempBalls = int(tempBalls)
                                    bowlersScoreboardTwo[index][1] = bowlersScoreboardTwo[index][1] + tempBalls
                                    bowlersScoreboardTwo[index][2] = bowlersScoreboardTwo[index][2] + initialDotBalls
                                    bowlersScoreboardTwo[index][3] = bowlersScoreboardTwo[index][3] + initialScore
                                    bowlersScoreboardTwo[index][4] = bowlersScoreboardTwo[index][4] + initialOut
                                    bowlersScoreboardTwo[index][5] = bowlersScoreboardTwo[index][3] / bowlersScoreboardTwo[index][1]
                                    initialBowlerBallsCount = 10 + tempBalls
                                    # print('     b. {}     {}({}){} [{}x4 {}x6]'.format(bowlerPresent,batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour,initialStrikeSix))
                                    print('     {}     ({}){} [{}x4 {}x6]'.format(batsman1,initialStrikerRuns,initialStrikerBallsCount, initialStrikeFour, initialStrikeSix))
                                    print('     {}     ({}){} [{}x4 {}x6]'.format(batsman2,intialNonStrikerRuns,initialNonStrikerBallsCount, initialNonStrikeFour, initialNonStrikeSix))
                                    print('     {}     {}-{}-{}-{}'.format(bowlerPresent,initialBowlerBallsCount,bowlersScoreboardTwo[index][2],bowlersScoreboardTwo[index][3],bowlersScoreboardTwo[index][4]))
                                    print()
                    # print('     {}     {}-{}-{}-{}'.format(bowlerPresent,'10',initialDotBalls,initialScore,initialOut))
                    print()
                    print('     END of '+str(count)+' balls ('+str(initialScore)+' runs)')
                    print('     '+team1+'     '+str(totalScore)+'/'+str(totalWickets))
                    rr = totalScore / (count / 10)
                    rrr = (target - totalScore) / ((100 - count) / 10)      
                    print('     RR: {:.2f}     RRR: {:.2f}'.format(rr, rrr))
                    print()
                    wicketsDiffer = 10 - totalWickets
                    print('     '+team1+' win by '+str(wicketsDiffer)+' wickets.')
                    break
                
                # print('{} {} to {} : {} runs'.format(ball,bowlerPresent,batsman1,*ballOutcome))
                if totalWickets == 10:
                    sr2 = intialNonStrikerRuns * 100 // initialNonStrikerBallsCount
                    batsmenScoreboard2.append([batsman2, "Not Out",'','', intialNonStrikerRuns, initialNonStrikerBallsCount, 
                   initialNonStrikeFour, initialNonStrikeSix, sr2])
                    print()
                    for i in bowlingPlayers:
                        if i == bowlerPresent:
                            index = bowlingPlayers.index(i)
                            if bowlersScoreboardTwo[index][1] == 0:
                                if iBall == 100:
                                    bowlersScoreboardTwo[index][1] = bowlersScoreboardTwo[index][1] + 10
                                    bowlersScoreboardTwo[index][2] = bowlersScoreboardTwo[index][2] + initialDotBalls
                                    bowlersScoreboardTwo[index][3] = bowlersScoreboardTwo[index][3] + initialScore
                                    bowlersScoreboardTwo[index][4] = bowlersScoreboardTwo[index][4] + initialOut
                                    bowlersScoreboardTwo[index][5] = bowlersScoreboardTwo[index][3] / 20
                                    initialBowlerBallsCount = 20
                                    # print('     {}     ({}){} [{}x4 {}x6]'.format(batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour, initialStrikeSix))
                                    if outType == 'Bowled':
                                        print('     b. {}     {}({}){} [{}x4 {}x6]'.format(bowlerPresent,batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour,initialStrikeSix))
                                    elif outType == 'Stumped':
                                        print('     st. {}     b. {}     {}({}){} [{}x4 {}x6]'.format(*keeper,bowlerPresent,batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour,initialStrikeSix))
                                    elif outType == 'Caught':
                                        print('     c. {}     b. {}     {}({}){} [{}x4 {}x6]'.format(cPlayer,bowlerPresent,batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour,initialStrikeSix))
                                     
                                    # print('     b. {}     {}({}){} [{}x4 {}x6]'.format(bowlerPresent,batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour,initialStrikeSix))
                                    print('     {}     ({}){} [{}x4 {}x6]'.format(batsman2,intialNonStrikerRuns,initialNonStrikerBallsCount, initialNonStrikeFour, initialNonStrikeSix))
                                    print('     {}     {}-{}-{}-{}'.format(bowlerPresent,initialBowlerBallsCount,bowlersScoreboardTwo[index][2],bowlersScoreboardTwo[index][3],bowlersScoreboardTwo[index][4]))
                                    print()
                                else:
                                    iBall = str(iBall)
                                    tempBalls = iBall[1:]
                                    tempBalls = int(tempBalls)
                                    bowlersScoreboardTwo[index][1] = bowlersScoreboardTwo[index][1] + tempBalls
                                    bowlersScoreboardTwo[index][2] = bowlersScoreboardTwo[index][2] + initialDotBalls
                                    bowlersScoreboardTwo[index][3] = bowlersScoreboardTwo[index][3] + initialScore
                                    bowlersScoreboardTwo[index][4] = bowlersScoreboardTwo[index][4] + initialOut
                                    bowlersScoreboardTwo[index][5] = bowlersScoreboardTwo[index][3] / bowlersScoreboardTwo[index][1]
                                    initialBowlerBallsCount = 10 + tempBalls
                                    # print('     {}     ({}){} [{}x4 {}x6]'.format(batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour, initialStrikeSix))
                                    print('     b. {}     {}({}){} [{}x4 {}x6]'.format(bowlerPresent,batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour,initialStrikeSix))
                                    print('     {}     ({}){} [{}x4 {}x6]'.format(batsman2,intialNonStrikerRuns,initialNonStrikerBallsCount, initialNonStrikeFour, initialNonStrikeSix))
                                    print('     {}     {}-{}-{}-{}'.format(bowlerPresent,initialBowlerBallsCount,bowlersScoreboardTwo[index][2],bowlersScoreboardTwo[index][3],bowlersScoreboardTwo[index][4]))
                                    print()
                            elif bowlersScoreboardTwo[index][1] == 10:
                                if iBall == 100:
                                    bowlersScoreboardTwo[index][1] = bowlersScoreboardTwo[index][1] + 10
                                    bowlersScoreboardTwo[index][2] = bowlersScoreboardTwo[index][2] + initialDotBalls
                                    bowlersScoreboardTwo[index][3] = bowlersScoreboardTwo[index][3] + initialScore
                                    bowlersScoreboardTwo[index][4] = bowlersScoreboardTwo[index][4] + initialOut
                                    bowlersScoreboardTwo[index][5] = bowlersScoreboardTwo[index][3] / 20
                                    initialBowlerBallsCount = 20
                                    # print('     {}     ({}){} [{}x4 {}x6]'.format(batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour, initialStrikeSix))
                                    if outType == 'Bowled':
                                        print('     b. {}     {}({}){} [{}x4 {}x6]'.format(bowlerPresent,batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour,initialStrikeSix))
                                    elif outType == 'Stumped':
                                        print('     st. {}     b. {}     {}({}){} [{}x4 {}x6]'.format(*keeper,bowlerPresent,batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour,initialStrikeSix))
                                    elif outType == 'Caught':
                                        print('     c. {}     b. {}     {}({}){} [{}x4 {}x6]'.format(cPlayer,bowlerPresent,batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour,initialStrikeSix))
                                     
                                    # print('     b. {}     {}({}){} [{}x4 {}x6]'.format(bowlerPresent,batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour,initialStrikeSix))
                                    print('     {}     ({}){} [{}x4 {}x6]'.format(batsman2,intialNonStrikerRuns,initialNonStrikerBallsCount, initialNonStrikeFour, initialNonStrikeSix))
                                    print('     {}     {}-{}-{}-{}'.format(bowlerPresent,initialBowlerBallsCount,bowlersScoreboardTwo[index][2],bowlersScoreboardTwo[index][3],bowlersScoreboardTwo[index][4]))
                                    print()
                                else:
                                    iBall = str(iBall)
                                    tempBalls = iBall[1:]
                                    tempBalls = int(tempBalls)
                                    bowlersScoreboardTwo[index][1] = bowlersScoreboardTwo[index][1] + tempBalls
                                    bowlersScoreboardTwo[index][2] = bowlersScoreboardTwo[index][2] + initialDotBalls
                                    bowlersScoreboardTwo[index][3] = bowlersScoreboardTwo[index][3] + initialScore
                                    bowlersScoreboardTwo[index][4] = bowlersScoreboardTwo[index][4] + initialOut
                                    bowlersScoreboardTwo[index][5] = bowlersScoreboardTwo[index][3] / bowlersScoreboardTwo[index][1]
                                    initialBowlerBallsCount = 10 + tempBalls
                                    # print('     {}     ({}){} [{}x4 {}x6]'.format(batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour, initialStrikeSix))
                                    print('     b. {}     {}({}){} [{}x4 {}x6]'.format(bowlerPresent,batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour,initialStrikeSix))
                                    print('     {}     ({}){} [{}x4 {}x6]'.format(batsman2,intialNonStrikerRuns,initialNonStrikerBallsCount, initialNonStrikeFour, initialNonStrikeSix))
                                    print('     {}     {}-{}-{}-{}'.format(bowlerPresent,initialBowlerBallsCount,bowlersScoreboardTwo[index][2],bowlersScoreboardTwo[index][3],bowlersScoreboardTwo[index][4]))
                                    print()
                    # print('     {}     {}-{}-{}-{}'.format(bowlerPresent,'10',initialDotBalls,initialScore,initialOut))
                    print()
                    print('     End of innings (Balls '+str(count)+')')
                    rr = totalScore / (count / 10)
                    print('     '+team1+'     '+str(totalScore)+'/'+str(totalWickets)+'  (RR: {:.2f})'.format(rr))
                    print()
                    if totalScore < target:
                        diff = target - totalScore - 1
                        print(team2+' win by '+str(diff)+' runs.')
                        break

        #End of every 10 balls presenting score  
        if count % 10 == 0:
            print()
            print('     END of '+str(count)+' balls ('+str(initialScore)+' runs)')
            print('     '+team1+'     '+str(totalScore)+'/'+str(totalWickets))
            rr = totalScore / (count / 10)
            rrr = (target - totalScore) / ((100 - count) / 10)
            print('     RR: {:.2f}     RRR: {:.2f}'.format(rr, rrr))
            print()
            # print('     {}     {}-{}-{}-{}'.format(bowlerPresent,'10',initialDotBalls,initialScore,initialOut))
            # print()
            
            
            
            #Checking for winner after every ball
            if count == 100:
                print()
                print('     End of innings (Balls '+str(count)+')')
                rr = totalScore / (count / 10)
                print('     '+team1+'     '+str(totalScore)+'/'+str(totalWickets)+'  (RR: {:.2f})'.format(rr))
                if totalScore < target:
                    if initialStrikerBallsCount == 0:
                        sr1 = 0
                    else:
                        sr1 = initialStrikerRuns * 100 // initialStrikerBallsCount
                    sr2 = intialNonStrikerRuns * 100 // initialNonStrikerBallsCount
                    
                    batsmenScoreboard2.append([batsman1, "Not Out",'','', initialStrikerRuns, initialStrikerBallsCount, 
                   initialStrikeFour, initialStrikeSix, sr1])
                    batsmenScoreboard2.append([batsman2, "Not Out",'','', intialNonStrikerRuns, initialNonStrikerBallsCount, 
                   initialNonStrikeFour, initialNonStrikeSix, sr2])
                    print()
                    for i in bowlingPlayers:
                        if i == bowlerPresent:
                            index = bowlingPlayers.index(i)
                            if bowlersScoreboardTwo[index][1] == 0:
                                if iBall == 100:
                                    bowlersScoreboardTwo[index][1] = bowlersScoreboardTwo[index][1] + 10
                                    bowlersScoreboardTwo[index][2] = bowlersScoreboardTwo[index][2] + initialDotBalls
                                    bowlersScoreboardTwo[index][3] = bowlersScoreboardTwo[index][3] + initialScore
                                    bowlersScoreboardTwo[index][4] = bowlersScoreboardTwo[index][4] + initialOut
                                    bowlersScoreboardTwo[index][5] = bowlersScoreboardTwo[index][3] / 20
                                    initialBowlerBallsCount = 20
                                    # print('     {}     ({}){} [{}x4 {}x6]'.format(batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour, initialStrikeSix))
                                    if ballOutcome == ['OUT']:
                                        if outType == 'Bowled':
                                            print('     b. {}     {}({}){} [{}x4 {}x6]'.format(bowlerPresent,batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour,initialStrikeSix))
                                        elif outType == 'Stumped':
                                            print('     st. {}     b. {}     {}({}){} [{}x4 {}x6]'.format(*keeper,bowlerPresent,batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour,initialStrikeSix))
                                        elif outType == 'Caught':
                                            print('     c. {}     b. {}     {}({}){} [{}x4 {}x6]'.format(cPlayer,bowlerPresent,batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour,initialStrikeSix))
                                    else:  
                                    # print('     b. {}     {}({}){} [{}x4 {}x6]'.format(bowlerPresent,batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour,initialStrikeSix))
                                        print('     {}     ({}){} [{}x4 {}x6]'.format(batsman1,initialStrikerRuns,initialStrikerBallsCount, initialStrikeFour, initialStrikeSix))
                                        print('     {}     ({}){} [{}x4 {}x6]'.format(batsman2,intialNonStrikerRuns,initialNonStrikerBallsCount, initialNonStrikeFour, initialNonStrikeSix))
                                        print('     {}     {}-{}-{}-{}'.format(bowlerPresent,initialBowlerBallsCount,bowlersScoreboardTwo[index][2],bowlersScoreboardTwo[index][3],bowlersScoreboardTwo[index][4]))
                                    print()
                                else:
                                    iBall = str(iBall)
                                    tempBalls = iBall[1:]
                                    tempBalls = int(tempBalls)
                                    bowlersScoreboardTwo[index][1] = bowlersScoreboardTwo[index][1] + tempBalls
                                    bowlersScoreboardTwo[index][2] = bowlersScoreboardTwo[index][2] + initialDotBalls
                                    bowlersScoreboardTwo[index][3] = bowlersScoreboardTwo[index][3] + initialScore
                                    bowlersScoreboardTwo[index][4] = bowlersScoreboardTwo[index][4] + initialOut
                                    bowlersScoreboardTwo[index][5] = bowlersScoreboardTwo[index][3] / bowlersScoreboardTwo[index][1]
                                    initialBowlerBallsCount = 10 + tempBalls
                                    # print('     {}     ({}){} [{}x4 {}x6]'.format(batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour, initialStrikeSix))
                                    if ballOutcome == ['OUT']:
                                        if outType == 'Bowled':
                                            print('     b. {}     {}({}){} [{}x4 {}x6]'.format(bowlerPresent,batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour,initialStrikeSix))
                                        elif outType == 'Stumped':
                                            print('     st. {}     b. {}     {}({}){} [{}x4 {}x6]'.format(*keeper,bowlerPresent,batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour,initialStrikeSix))
                                        elif outType == 'Caught':
                                            print('     c. {}     b. {}     {}({}){} [{}x4 {}x6]'.format(cPlayer,bowlerPresent,batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour,initialStrikeSix))
                                    else:  
                                    # print('     b. {}     {}({}){} [{}x4 {}x6]'.format(bowlerPresent,batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour,initialStrikeSix))
                                        print('     {}     ({}){} [{}x4 {}x6]'.format(batsman1,initialStrikerRuns,initialStrikerBallsCount, initialStrikeFour, initialStrikeSix))
                                        print('     {}     ({}){} [{}x4 {}x6]'.format(batsman2,intialNonStrikerRuns,initialNonStrikerBallsCount, initialNonStrikeFour, initialNonStrikeSix))
                                        print('     {}     {}-{}-{}-{}'.format(bowlerPresent,initialBowlerBallsCount,bowlersScoreboardTwo[index][2],bowlersScoreboardTwo[index][3],bowlersScoreboardTwo[index][4]))
                                    print()
                            elif bowlersScoreboardTwo[index][1] == 10:
                                if iBall == 100:
                                    bowlersScoreboardTwo[index][1] = bowlersScoreboardTwo[index][1] + 10
                                    bowlersScoreboardTwo[index][2] = bowlersScoreboardTwo[index][2] + initialDotBalls
                                    bowlersScoreboardTwo[index][3] = bowlersScoreboardTwo[index][3] + initialScore
                                    bowlersScoreboardTwo[index][4] = bowlersScoreboardTwo[index][4] + initialOut
                                    bowlersScoreboardTwo[index][5] = bowlersScoreboardTwo[index][3] / 20
                                    initialBowlerBallsCount = 20
                                    # print('     {}     ({}){} [{}x4 {}x6]'.format(batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour, initialStrikeSix))
                                    if ballOutcome == ['OUT']:
                                        if outType == 'Bowled':
                                            print('     b. {}     {}({}){} [{}x4 {}x6]'.format(bowlerPresent,batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour,initialStrikeSix))
                                        elif outType == 'Stumped':
                                            print('     st. {}     b. {}     {}({}){} [{}x4 {}x6]'.format(*keeper,bowlerPresent,batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour,initialStrikeSix))
                                        elif outType == 'Caught':
                                            print('     c. {}     b. {}     {}({}){} [{}x4 {}x6]'.format(cPlayer,bowlerPresent,batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour,initialStrikeSix))
                                    else:  
                                    # print('     b. {}     {}({}){} [{}x4 {}x6]'.format(bowlerPresent,batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour,initialStrikeSix))
                                        print('     {}     ({}){} [{}x4 {}x6]'.format(batsman1,initialStrikerRuns,initialStrikerBallsCount, initialStrikeFour, initialStrikeSix))
                                        print('     {}     ({}){} [{}x4 {}x6]'.format(batsman2,intialNonStrikerRuns,initialNonStrikerBallsCount, initialNonStrikeFour, initialNonStrikeSix))
                                        print('     {}     {}-{}-{}-{}'.format(bowlerPresent,initialBowlerBallsCount,bowlersScoreboardTwo[index][2],bowlersScoreboardTwo[index][3],bowlersScoreboardTwo[index][4]))
                                    print()
                                else:
                                    iBall = str(iBall)
                                    tempBalls = iBall[1:]
                                    tempBalls = int(tempBalls)
                                    bowlersScoreboardTwo[index][1] = bowlersScoreboardTwo[index][1] + tempBalls
                                    bowlersScoreboardTwo[index][2] = bowlersScoreboardTwo[index][2] + initialDotBalls
                                    bowlersScoreboardTwo[index][3] = bowlersScoreboardTwo[index][3] + initialScore
                                    bowlersScoreboardTwo[index][4] = bowlersScoreboardTwo[index][4] + initialOut
                                    bowlersScoreboardTwo[index][5] = bowlersScoreboardTwo[index][3] / bowlersScoreboardTwo[index][1]
                                    initialBowlerBallsCount = 10 + tempBalls
                                    # print('     {}     ({}){} [{}x4 {}x6]'.format(batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour, initialStrikeSix))
                                    if outType == 'Bowled':
                                        print('     b. {}     {}({}){} [{}x4 {}x6]'.format(bowlerPresent,batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour,initialStrikeSix))
                                    elif outType == 'Stumped':
                                        print('     st. {}     b. {}     {}({}){} [{}x4 {}x6]'.format(*keeper,bowlerPresent,batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour,initialStrikeSix))
                                    elif outType == 'Caught':
                                        print('     c. {}     b. {}     {}({}){} [{}x4 {}x6]'.format(cPlayer,bowlerPresent,batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour,initialStrikeSix))
                                     
                                    # print('     b. {}     {}({}){} [{}x4 {}x6]'.format(bowlerPresent,batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour,initialStrikeSix))
                                    print('     {}     ({}){} [{}x4 {}x6]'.format(batsman2,intialNonStrikerRuns,initialNonStrikerBallsCount, initialNonStrikeFour, initialNonStrikeSix))
                                    print('     {}     {}-{}-{}-{}'.format(bowlerPresent,initialBowlerBallsCount,bowlersScoreboardTwo[index][2],bowlersScoreboardTwo[index][3],bowlersScoreboardTwo[index][4]))
                                    print()
                    # print('     {}     {}-{}-{}-{}'.format(bowlerPresent,'10',initialDotBalls,initialScore,initialOut))
                    print()
                    diff = target - totalScore
                    print(team2+' win by '+str(diff)+' runs.')
                    break
            elif count == 100:
                if totalScore >= target:
                    sr1 = initialStrikerRuns * 100 // initialStrikerBallsCount
                    sr2 = intialNonStrikerRuns * 100 // initialNonStrikerBallsCount
                    batsmenScoreboard2.append([batsman1, "Not Out",'','', initialStrikerRuns, initialStrikerBallsCount, 
                   initialStrikeFour, initialStrikeSix, sr1])
                    batsmenScoreboard2.append([batsman2, "Not Out",'','', intialNonStrikerRuns, initialNonStrikerBallsCount, 
                   initialNonStrikeFour, initialNonStrikeSix, sr2])
                    print()
                    for i in bowlingPlayers:
                        if i == bowlerPresent:
                            index = bowlingPlayers.index(i)
                            if bowlersScoreboardTwo[index][1] == 0:
                                if iBall == 100:
                                    bowlersScoreboardTwo[index][1] = bowlersScoreboardTwo[index][1] + 10
                                    bowlersScoreboardTwo[index][2] = bowlersScoreboardTwo[index][2] + initialDotBalls
                                    bowlersScoreboardTwo[index][3] = bowlersScoreboardTwo[index][3] + initialScore
                                    bowlersScoreboardTwo[index][4] = bowlersScoreboardTwo[index][4] + initialOut
                                    bowlersScoreboardTwo[index][5] = bowlersScoreboardTwo[index][3] / 20
                                    initialBowlerBallsCount = 20

                                    # print('     b. {}     {}({}){} [{}x4 {}x6]'.format(bowlerPresent,batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour,initialStrikeSix))
                                    print('     {}     ({}){} [{}x4 {}x6]'.format(batsman1,initialStrikerRuns,initialStrikerBallsCount, initialStrikeFour, initialStrikeSix))
                                    print('     {}     ({}){} [{}x4 {}x6]'.format(batsman2,intialNonStrikerRuns,initialNonStrikerBallsCount, initialNonStrikeFour, initialNonStrikeSix))
                                    print('     {}     {}-{}-{}-{}'.format(bowlerPresent,initialBowlerBallsCount,bowlersScoreboardTwo[index][2],bowlersScoreboardTwo[index][3],bowlersScoreboardTwo[index][4]))
                                    print()
                                else:
                                    iBall = str(iBall)
                                    tempBalls = iBall[1:]
                                    tempBalls = int(tempBalls)
                                    bowlersScoreboardTwo[index][1] = bowlersScoreboardTwo[index][1] + tempBalls
                                    bowlersScoreboardTwo[index][2] = bowlersScoreboardTwo[index][2] + initialDotBalls
                                    bowlersScoreboardTwo[index][3] = bowlersScoreboardTwo[index][3] + initialScore
                                    bowlersScoreboardTwo[index][4] = bowlersScoreboardTwo[index][4] + initialOut
                                    bowlersScoreboardTwo[index][5] = bowlersScoreboardTwo[index][3] / bowlersScoreboardTwo[index][1]
                                    initialBowlerBallsCount = 10 + tempBalls

                                    # print('     b. {}     {}({}){} [{}x4 {}x6]'.format(bowlerPresent,batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour,initialStrikeSix))
                                    print('     {}     ({}){} [{}x4 {}x6]'.format(batsman1,initialStrikerRuns,initialStrikerBallsCount, initialStrikeFour, initialStrikeSix))
                                    print('     {}     ({}){} [{}x4 {}x6]'.format(batsman2,intialNonStrikerRuns,initialNonStrikerBallsCount, initialNonStrikeFour, initialNonStrikeSix))
                                    print('     {}     {}-{}-{}-{}'.format(bowlerPresent,initialBowlerBallsCount,bowlersScoreboardTwo[index][2],bowlersScoreboardTwo[index][3],bowlersScoreboardTwo[index][4]))
                                    print()
                            elif bowlersScoreboardTwo[index][1] == 10:
                                if iBall == 100:
                                    bowlersScoreboardTwo[index][1] = bowlersScoreboardTwo[index][1] + 10
                                    bowlersScoreboardTwo[index][2] = bowlersScoreboardTwo[index][2] + initialDotBalls
                                    bowlersScoreboardTwo[index][3] = bowlersScoreboardTwo[index][3] + initialScore
                                    bowlersScoreboardTwo[index][4] = bowlersScoreboardTwo[index][4] + initialOut
                                    bowlersScoreboardTwo[index][5] = bowlersScoreboardTwo[index][3] / 20
                                    initialBowlerBallsCount = 20
 
                                    # print('     b. {}     {}({}){} [{}x4 {}x6]'.format(bowlerPresent,batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour,initialStrikeSix))
                                    print('     {}     ({}){} [{}x4 {}x6]'.format(batsman1,initialStrikerRuns,initialStrikerBallsCount, initialStrikeFour, initialStrikeSix))
                                    print('     {}     ({}){} [{}x4 {}x6]'.format(batsman2,intialNonStrikerRuns,initialNonStrikerBallsCount, initialNonStrikeFour, initialNonStrikeSix))
                                    print('     {}     {}-{}-{}-{}'.format(bowlerPresent,initialBowlerBallsCount,bowlersScoreboardTwo[index][2],bowlersScoreboardTwo[index][3],bowlersScoreboardTwo[index][4]))
                                    print()
                                else:
                                    iBall = str(iBall)
                                    tempBalls = iBall[1:]
                                    tempBalls = int(tempBalls)
                                    bowlersScoreboardTwo[index][1] = bowlersScoreboardTwo[index][1] + tempBalls
                                    bowlersScoreboardTwo[index][2] = bowlersScoreboardTwo[index][2] + initialDotBalls
                                    bowlersScoreboardTwo[index][3] = bowlersScoreboardTwo[index][3] + initialScore
                                    bowlersScoreboardTwo[index][4] = bowlersScoreboardTwo[index][4] + initialOut
                                    bowlersScoreboardTwo[index][5] = bowlersScoreboardTwo[index][3] / bowlersScoreboardTwo[index][1]
                                    initialBowlerBallsCount = 10 + tempBalls

                                    # print('     b. {}     {}({}){} [{}x4 {}x6]'.format(bowlerPresent,batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour,initialStrikeSix))
                                    print('     {}     ({}){} [{}x4 {}x6]'.format(batsman1,initialStrikerRuns,initialStrikerBallsCount, initialStrikeFour, initialStrikeSix))
                                    print('     {}     ({}){} [{}x4 {}x6]'.format(batsman2,intialNonStrikerRuns,initialNonStrikerBallsCount, initialNonStrikeFour, initialNonStrikeSix))
                                    print('     {}     {}-{}-{}-{}'.format(bowlerPresent,initialBowlerBallsCount,bowlersScoreboardTwo[index][2],bowlersScoreboardTwo[index][3],bowlersScoreboardTwo[index][4]))
                                    print()
                    # print('     {}     {}-{}-{}-{}'.format(bowlerPresent,'10',initialDotBalls,initialScore,initialOut))
                    print()
                    wicketsDiffer = 10 - totalWickets
                    print(team1+' win by '+str(wicketsDiffer)+' wickets.')
                    break
        
        #If out bring in next batsmen
        # if ballOutcome == ['OUT']:
        #     playerOut = playerOut + 1
        #     batsman1Rating = battingPlayerRatings[b+playerOut+1]
        #     batsman1 = battingPlayerNames[b+playerOut+1]
            
        
        #Checking weather to rotate strike or not after the end of over and in between the innings
        if ballOutcome == [1]:
            if count % 10 == 0 or ballOutcome == ['Leg Bye']: #overend
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
        elif ballOutcome == ['Leg Bye']:
            if count % 10 == 0: #when outcome 1 on last ball of over, strike change.
                #add runs to strike batsmen
                initialStrikerRuns = initialStrikerRuns + 0
                initialStrikerBallsCount = initialStrikerBallsCount + 1
                initialStrikerRuns, intialNonStrikerRuns = initialStrikerRuns, intialNonStrikerRuns
                initialStrikerBallsCount, initialNonStrikerBallsCount = initialStrikerBallsCount, initialNonStrikerBallsCount
            else:
                #add runs to strike batsmen
                initialStrikerRuns = initialStrikerRuns + 0
                initialStrikerBallsCount = initialStrikerBallsCount + 1
                initialStrikerRuns, intialNonStrikerRuns = intialNonStrikerRuns, initialStrikerRuns
                initialStrikerBallsCount, initialNonStrikerBallsCount = initialNonStrikerBallsCount, initialStrikerBallsCount
            # print(batsman1+'-> '+' Fours: '+str(initialStrikeFour)+' Sixes: '+str(initialStrikeSix))
            # print(batsman2+'-> '+' Fours: '+str(initialNonStrikeFour)+' Sixes: '+str(initialNonStrikeSix))
        
    
        if count % 10 == 0:
            for i in bowlingPlayers:
                if i == bowlerPresent:
                    index = bowlingPlayers.index(i)
                    if bowlersScoreboardTwo[index][1] == 0:
                        bowlersScoreboardTwo[index][1] = 10
                        bowlersScoreboardTwo[index][2] = initialDotBalls
                        bowlersScoreboardTwo[index][3] = initialScore
                        bowlersScoreboardTwo[index][4] = initialOut
                        bowlersScoreboardTwo[index][5] = initialScore / 10
                        initialBowlerBallsCount = 10
                        print('     {}     ({}){} [{}x4 {}x6]'.format(batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour, initialStrikeSix))
                        print('     {}     ({}){} [{}x4 {}x6]'.format(batsman2,intialNonStrikerRuns,initialNonStrikerBallsCount, initialNonStrikeFour, initialNonStrikeSix))
                        print('     {}     {}-{}-{}-{}'.format(bowlerPresent,initialBowlerBallsCount,initialDotBalls,initialScore,initialOut))
                        print()
                    elif bowlersScoreboardTwo[index][1] == 10:
                        bowlersScoreboardTwo[index][1] = bowlersScoreboardTwo[index][1] + 10
                        bowlersScoreboardTwo[index][2] = bowlersScoreboardTwo[index][2] + initialDotBalls
                        bowlersScoreboardTwo[index][3] = bowlersScoreboardTwo[index][3] + initialScore
                        bowlersScoreboardTwo[index][4] = bowlersScoreboardTwo[index][4] + initialOut
                        bowlersScoreboardTwo[index][5] = bowlersScoreboardTwo[index][3] / 20
                        initialBowlerBallsCount = 20
                        print('     {}     ({}){} [{}x4 {}x6]'.format(batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour, initialStrikeSix))
                        print('     {}     ({}){} [{}x4 {}x6]'.format(batsman2,intialNonStrikerRuns,initialNonStrikerBallsCount, initialNonStrikeFour, initialNonStrikeSix))
                        print('     {}     {}-{}-{}-{}'.format(bowlerPresent,initialBowlerBallsCount,bowlersScoreboardTwo[index][2],bowlersScoreboardTwo[index][3],bowlersScoreboardTwo[index][4]))
                        print()
            # print('     {}     ({}){} [{}x4 {}x6]'.format(batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour, initialStrikeSix))
            # print('     {}     ({}){} [{}x4 {}x6]'.format(batsman2,intialNonStrikerRuns,initialNonStrikerBallsCount, initialNonStrikeFour, initialNonStrikeSix))
            # print('     {}     {}-{}-{}-{}'.format(bowlerPresent,'10',initialDotBalls,initialScore,initialOut))
            # print()
            
            if ballOutcome == ['OUT']:
                sr = initialStrikerRuns * 100 // initialStrikerBallsCount
                if outType == 'Bowled':
                    batsmenScoreboard2.append([batsman1, 'b. ','', bowlerPresent, initialStrikerRuns, initialStrikerBallsCount, 
                   initialStrikeFour, initialStrikeSix, sr])
                elif outType == 'Caught':
                    batsmenScoreboard2.append([batsman1, 'c. ',cPlayer, bowlerPresent, initialStrikerRuns, initialStrikerBallsCount, 
                   initialStrikeFour, initialStrikeSix, sr])
                elif outType == 'Stumped':
                    batsmenScoreboard2.append([batsman1, 'st. ',*keeper, bowlerPresent, initialStrikerRuns, initialStrikerBallsCount, 
                   initialStrikeFour, initialStrikeSix, sr])
                print()
                if outType == 'Bowled':
                    print('     b. {}     {}({}){} [{}x4 {}x6]'.format(bowlerPresent,batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour,initialStrikeSix))
                elif outType == 'Stumped':
                    print('     st. {}     b. {}     {}({}){} [{}x4 {}x6]'.format(*keeper,bowlerPresent,batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour,initialStrikeSix))
                elif outType == 'Caught':
                    print('     c. {}     b. {}     {}({}){} [{}x4 {}x6]'.format(cPlayer,bowlerPresent,batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour,initialStrikeSix))
                 
                # print('     b. {}     {}({}){} [{}x4 {}x6]'.format(bowlerPresent,batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour,initialStrikeSix))
                
                initialStrikerRuns = 0
                initialStrikerBallsCount = 0
                initialStrikeFour = 0
                initialStrikeSix = 0
                print()
                playerOut = playerOut + 1
                batsman1Rating = battingPlayerRatings[b+playerOut+1]
                batsman1 = battingPlayerNames[b+playerOut+1]
            #Reseting over score before the begini of new over.
            initialScore = 0
            initialOut = 0
            
            #Change of bowler
            bowlerPresent = pickBowler() #bowler
            
            # bowler = random.choice(bowlingPlayers)
            # bowlerPresent = bowler
            
            initialDotBalls = 0
        
        #If out bring in next batsmen
        if ballOutcome == ['OUT'] and count % 10 != 0:
            sr = initialStrikerRuns * 100 // initialStrikerBallsCount
            if outType == 'Bowled':
                batsmenScoreboard2.append([batsman1, 'b. ','', bowlerPresent, initialStrikerRuns, initialStrikerBallsCount, 
               initialStrikeFour, initialStrikeSix, sr])
            elif outType == 'Caught':
                batsmenScoreboard2.append([batsman1, 'c. ',cPlayer, bowlerPresent, initialStrikerRuns, initialStrikerBallsCount, 
               initialStrikeFour, initialStrikeSix, sr])
            elif outType == 'Stumped':
                batsmenScoreboard2.append([batsman1, 'st. ',*keeper, bowlerPresent, initialStrikerRuns, initialStrikerBallsCount, 
               initialStrikeFour, initialStrikeSix, sr])
            print()
            if outType == 'Bowled':
                print('     b. {}     {}({}){} [{}x4 {}x6]'.format(bowlerPresent,batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour,initialStrikeSix))
            elif outType == 'Stumped':
                print('     st. {}     b. {}     {}({}){} [{}x4 {}x6]'.format(*keeper,bowlerPresent,batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour,initialStrikeSix))
            elif outType == 'Caught':
                print('     c. {}     b. {}     {}({}){} [{}x4 {}x6]'.format(cPlayer,bowlerPresent,batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour,initialStrikeSix))
             
            # print('     b. {}     {}({}){} [{}x4 {}x6]'.format(bowlerPresent,batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour,initialStrikeSix))
            
            initialStrikerRuns = 0
            initialStrikerBallsCount = 0
            initialStrikeFour = 0
            initialStrikeSix = 0
            print()
            playerOut = playerOut + 1
            batsman1Rating = battingPlayerRatings[b+playerOut+1]
            batsman1 = battingPlayerNames[b+playerOut+1]
    
    
    if count == 100:
        if totalWickets != 10:
            if initialStrikerBallsCount == 0:
                sr1 = 0
            else:
                sr1 = initialStrikerRuns * 100 // initialStrikerBallsCount
            sr2 = intialNonStrikerRuns * 100 // initialNonStrikerBallsCount
           #  batsmenScoreboard2.append([batsman1, "Not Out",'','', initialStrikerRuns, initialStrikerBallsCount, 
           # initialStrikeFour, initialStrikeSix, sr1])
           #  batsmenScoreboard2.append([batsman2, "Not Out",'','', intialNonStrikerRuns, initialNonStrikerBallsCount, 
           # initialNonStrikeFour, initialNonStrikeSix, sr2])
        if totalWickets == 10:
            sr2 = intialNonStrikerRuns * 100 // initialNonStrikerBallsCount
            batsmenScoreboard2.append([batsman2, "Not Out",'','', intialNonStrikerRuns, initialNonStrikerBallsCount, 
           initialNonStrikeFour, initialNonStrikeSix, sr2])
    print()
    
    
    print(team1+' 2nd Innings Scoreboard')
    print()
    batsmenScoreboardTwo = pd.DataFrame(batsmenScoreboard2, columns =['Batsman','','Fielder','Bowler','Runs','Balls','4s','6s','SR'])
    # print(batsmenScoreboardTwo)
    print(tabulate(batsmenScoreboardTwo, showindex=False, headers=batsmenScoreboardTwo.columns))
    print()
    print('  Total:   {}/{}     Balls: {}     Run Rate: {}     Extras: {}'.format(totalScore,totalWickets,count,round(rr,2),totalExtras))
    dnb = batsmenScoreboardTwo['Batsman'].to_list()
    dnb = list(set(battingPlayerNames) - set(dnb))
    print()
    if len(dnb) == 0:
        print('  DNB : Nil')
    else: 
        print()
        print('  DNB : ',dnb)
    print()

    
    # timestr = time.strftime("%Y%m%d-%H%M%S")
    # bat = path+team1+'-batting'+timestr+'.csv'
    # batsmenScoreboardTwo.to_csv(bat)
    print(team2+' Bowling Scorecard')
    print()
    bowlersScoreboard2 = pd.DataFrame(bowlersScoreboardTwo, columns=['Bowler','Balls','Dots','Runs','Wickets','Economy'])
    bowlersScoreboard2.round({"Economy":2})
    print(tabulate(bowlersScoreboard2, showindex=False, headers=bowlersScoreboard2.columns))
    # timestr = time.strftime("%Y%m%d-%H%M%S")
    # ball = path+team2+'-bowling'+timestr+'.csv'
    # bowlersScoreboard2.to_csv(ball)
    


def prepInnings(team1, team2):
    
    team2BowlerRatings = pd.read_csv(team2+' Bowling.manish')
    team2FastBowlersRatings = team2BowlerRatings[team2BowlerRatings['type'] == 'fast']
    team2SpinBowlersRatings = team2BowlerRatings[team2BowlerRatings['type'] == 'spin']
    
    player_name = team2FastBowlersRatings['player'].to_list()
    team2FastBowlersRatingsValues = team2FastBowlersRatings['rating'].to_list()
    
    player_name2 = team2SpinBowlersRatings['player'].to_list()
    team2SpinBowlersRatingsValues = team2SpinBowlersRatings['rating'].to_list()
    
    fastBowlers = []
    spinBowlers = []
    
    for i in range(len(player_name)):
        fastBowlers.append([player_name[i], team2FastBowlersRatingsValues[i]])
    fastBowlers.sort(key=lambda fastBowlers:fastBowlers[1], reverse=True)
    
    for i in range(len(player_name2)):
        spinBowlers.append([player_name2[i], team2SpinBowlersRatingsValues[i]])
    spinBowlers.sort(key=lambda spinBowlers:spinBowlers[1], reverse=True)
    
    bowlers = fastBowlers + spinBowlers
    
    sortedBowlers = []
    for i in bowlers:
        sortedBowlers.append(i[0])
    
    checkList = []
    
    battingTeam1 = pd.read_csv(team1+'.csv')
    bowlingTeam1 = pd.read_csv(team2+'.csv')
    
    oppTeam = pd.read_csv(team2+'.csv')
    keeper = oppTeam[oppTeam['role'] == 'Keeper']['player']
    keeper = keeper.values
    
    oppTeam = oppTeam.player
    oppTeam = oppTeam.to_list()
    
    bowlingPlayers = bowlingTeam1[bowlingTeam1['role'] == "Bowler"]
    bowlingPlayers = bowlingPlayers.player
    bowlingPlayers = bowlingPlayers.to_list()
    
    if set(bowlingPlayers) == set(sortedBowlers):
        pass
    else:
        print('Bowlers ratings data not matching with playing 11 data !!')
        print('Check '+team2+'.csv and '+team2+' Bowling.manish')
        sys.exit()
    
    battingPlayers = battingTeam1
    columns = ['role', 'type', 'total']
    battingPlayers.drop(columns, inplace=True, axis=1)
    battingPlayers = battingPlayers.values.tolist()
    
    battingPlayerNames = []
    battingPlayerRatings = []
    
    for i in battingPlayers:
        battingPlayerNames.append(i[0])
        battingPlayerRatings.append(i[1:])
        
    print(team1+' - ',battingPlayerNames)
    print(team2+' - ',bowlingPlayers)
    print()
    
    #Name, Balls, Dots, Runs, Wickets, Economy
    bowlersScoreboardOne = []
    for i in range(len(bowlingPlayers)):
        bowlersScoreboardOne.append([bowlingPlayers[i],0,0,0,0,0])
    
    totalWickets = 0
    totalScore = 0
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
    totalExtras = 0
    
    
    
    def pickBowler():
        bowler = random.choice(sortedBowlers)
        if bowler != checkList[-1] and checkList.count(bowler) < 2:
            checkList.append(bowler)
            return bowler
        else:
            return pickBowler()
        return bowler
    
    b = 0
    playerOut = 0
    
    bowlerPresent = sortedBowlers[0]
    checkList.append(bowlerPresent)
    sortedBowlerIndex = sortedBowlers.index(bowlerPresent)
    bowlerPresentRating = bowlers[sortedBowlerIndex][1]
    
    batsman1 = battingPlayerNames[b]
    batsman2 = battingPlayerNames[b+1]
    batsman1Rating = battingPlayerRatings[b]
    batsman2Rating = battingPlayerRatings[b+1]
    
    print('%%%%%  First Innings  %%%%%')
    print()
    
    for i in range(1,101):
        iBall = i
        # time.sleep(gameRate)
        if len(str(i)) == 1:
            ball = 'Ball 0'+str(i)+' : '
        else:
            ball = 'Ball '+str(i)+' : '
        
        def callBatsman1Rating():
           if bowlerPresentRating in range(71, 76):
               #increase
               batsman1Rating[0] = batsman1Rating[0] - 3
               batsman1Rating[1] = batsman1Rating[1] - 3
               batsman1Rating[2] = batsman1Rating[2] - 1
               batsman1Rating[6] = batsman1Rating[6] - 0
               #decrease
               batsman1Rating[3] = batsman1Rating[3] + 0.3
               batsman1Rating[4] = batsman1Rating[4] + 1.3
               batsman1Rating[5] = batsman1Rating[5] + 0.7
           elif bowlerPresentRating in range(76, 81):
               #increase
               batsman1Rating[0] = batsman1Rating[0] - 5
               batsman1Rating[1] = batsman1Rating[1] - 5
               batsman1Rating[2] = batsman1Rating[2] - 3
               batsman1Rating[6] = batsman1Rating[6] - 1
               #decrease
               batsman1Rating[3] = batsman1Rating[3] + 0.7
               batsman1Rating[4] = batsman1Rating[4] + 2
               batsman1Rating[5] = batsman1Rating[5] + 1.5
           elif bowlerPresentRating in range(81, 86):
               #increase
               batsman1Rating[0] = batsman1Rating[0] - 6
               batsman1Rating[1] = batsman1Rating[1] - 6
               batsman1Rating[2] = batsman1Rating[2] - 4
               batsman1Rating[6] = batsman1Rating[6] - 2
               #decrease
               batsman1Rating[3] = batsman1Rating[3] + 1
               batsman1Rating[4] = batsman1Rating[4] + 3
               batsman1Rating[5] = batsman1Rating[5] + 2
           elif bowlerPresentRating in range(86, 91):
               #increase
               batsman1Rating[0] = batsman1Rating[0] - 7
               batsman1Rating[1] = batsman1Rating[1] - 7
               batsman1Rating[2] = batsman1Rating[2] - 5
               batsman1Rating[6] = batsman1Rating[6] - 3
               #decrease
               batsman1Rating[3] = batsman1Rating[3] + 2
               batsman1Rating[4] = batsman1Rating[4] + 4
               batsman1Rating[5] = batsman1Rating[5] + 3
           elif bowlerPresentRating in range(91, 96):
               #increase
               batsman1Rating[0] = batsman1Rating[0] - 8
               batsman1Rating[1] = batsman1Rating[1] - 8
               batsman1Rating[2] = batsman1Rating[2] - 6
               batsman1Rating[6] = batsman1Rating[6] - 7
               #decrease
               batsman1Rating[3] = batsman1Rating[3] + 3
               batsman1Rating[4] = batsman1Rating[4] + 5
               batsman1Rating[5] = batsman1Rating[5] + 4
           elif bowlerPresentRating in range(0,55):
               #increase
               batsman1Rating[0] = batsman1Rating[0] + 25
               batsman1Rating[1] = batsman1Rating[1] - 15
               batsman1Rating[2] = batsman1Rating[2] - 15
               batsman1Rating[6] = batsman1Rating[6] + 7
               #decrease
               batsman1Rating[3] = batsman1Rating[3] - 3
               batsman1Rating[4] = batsman1Rating[4] - 6
               batsman1Rating[5] = batsman1Rating[5] - 6
           elif bowlerPresentRating in range(55,61):
               #increase
               batsman1Rating[0] = batsman1Rating[0] - 0.5
               batsman1Rating[1] = batsman1Rating[1] - 0.5
               batsman1Rating[2] = batsman1Rating[2] - 0.5
               batsman1Rating[6] = batsman1Rating[6] - 0.5
               #decrease
               batsman1Rating[3] = batsman1Rating[3] + 0.5
               batsman1Rating[4] = batsman1Rating[4] + 0.5
               batsman1Rating[5] = batsman1Rating[5] + 0.5
           elif bowlerPresentRating in range(61,66):
               #increase
               batsman1Rating[0] = batsman1Rating[0] - 1
               batsman1Rating[1] = batsman1Rating[1] - 1
               batsman1Rating[2] = batsman1Rating[2] - 1
               batsman1Rating[6] = batsman1Rating[6] - 1
               #decrease
               batsman1Rating[3] = batsman1Rating[3] + 0.5
               batsman1Rating[4] = batsman1Rating[4] + 0.5
               batsman1Rating[5] = batsman1Rating[5] + 0.5
           elif bowlerPresentRating in range(66,71):
               #increase
               batsman1Rating[0] = batsman1Rating[0] - 2
               batsman1Rating[1] = batsman1Rating[1] - 2
               batsman1Rating[2] = batsman1Rating[2] - 2
               batsman1Rating[6] = batsman1Rating[6] - 2
               #decrease
               batsman1Rating[3] = batsman1Rating[3] + 1
               batsman1Rating[4] = batsman1Rating[4] + 1
               batsman1Rating[5] = batsman1Rating[5] + 1
               
              
        
        if bowlerPresentRating in range(71, 76):
            #increase
            batsman1Rating[0] = batsman1Rating[0] + 3
            batsman1Rating[1] = batsman1Rating[1] + 3
            batsman1Rating[2] = batsman1Rating[2] + 1
            #decrease
            batsman1Rating[3] = batsman1Rating[3] - 0.3
            batsman1Rating[4] = batsman1Rating[4] - 1.3
            batsman1Rating[5] = batsman1Rating[5] - 0.7
        elif bowlerPresentRating in range(76, 81):
            #increase
            batsman1Rating[0] = batsman1Rating[0] + 5
            batsman1Rating[1] = batsman1Rating[1] + 5
            batsman1Rating[2] = batsman1Rating[2] + 3
            batsman1Rating[6] = batsman1Rating[6] + 1
            #decrease
            batsman1Rating[3] = batsman1Rating[3] - 0.7
            batsman1Rating[4] = batsman1Rating[4] - 2
            batsman1Rating[5] = batsman1Rating[5] - 1.5
        elif bowlerPresentRating in range(81, 86):
            #increase
            batsman1Rating[0] = batsman1Rating[0] + 6
            batsman1Rating[1] = batsman1Rating[1] + 6
            batsman1Rating[2] = batsman1Rating[2] + 4
            batsman1Rating[6] = batsman1Rating[6] + 2
            #decrease
            batsman1Rating[3] = batsman1Rating[3] - 1
            batsman1Rating[4] = batsman1Rating[4] - 3
            batsman1Rating[5] = batsman1Rating[5] - 2
        elif bowlerPresentRating in range(86, 91):
            #increase
            batsman1Rating[0] = batsman1Rating[0] + 7
            batsman1Rating[1] = batsman1Rating[1] + 7
            batsman1Rating[2] = batsman1Rating[2] + 5
            batsman1Rating[6] = batsman1Rating[6] + 3
            #decrease
            batsman1Rating[3] = batsman1Rating[3] - 2
            batsman1Rating[4] = batsman1Rating[4] - 4
            batsman1Rating[5] = batsman1Rating[5] - 3
        elif bowlerPresentRating in range(91, 96):
            #increase
            batsman1Rating[0] = batsman1Rating[0] + 8
            batsman1Rating[1] = batsman1Rating[1] + 8
            batsman1Rating[2] = batsman1Rating[2] + 6
            batsman1Rating[6] = batsman1Rating[6] + 7
            #decrease
            batsman1Rating[3] = batsman1Rating[3] - 3
            batsman1Rating[4] = batsman1Rating[4] - 5
            batsman1Rating[5] = batsman1Rating[5] - 4
        elif bowlerPresentRating in range(0,55):
            #increase
            batsman1Rating[0] = batsman1Rating[0] - 25
            batsman1Rating[1] = batsman1Rating[1] + 15
            batsman1Rating[2] = batsman1Rating[2] + 15
            batsman1Rating[6] = batsman1Rating[6] - 7
            #decrease
            batsman1Rating[3] = batsman1Rating[3] + 3
            batsman1Rating[4] = batsman1Rating[4] + 6
            batsman1Rating[5] = batsman1Rating[5] + 6
        elif bowlerPresentRating in range(55,61):
            #increase
            batsman1Rating[0] = batsman1Rating[0] + 0.5
            batsman1Rating[1] = batsman1Rating[1] + 0.5
            batsman1Rating[2] = batsman1Rating[2] + 0.5
            batsman1Rating[6] = batsman1Rating[6] + 0.5
            #decrease
            batsman1Rating[3] = batsman1Rating[3] - 0.5
            batsman1Rating[4] = batsman1Rating[4] - 0.5
            batsman1Rating[5] = batsman1Rating[5] - 0.5
        elif bowlerPresentRating in range(61,66):
            #increase
            batsman1Rating[0] = batsman1Rating[0] + 1
            batsman1Rating[1] = batsman1Rating[1] + 1
            batsman1Rating[2] = batsman1Rating[2] + 1
            batsman1Rating[6] = batsman1Rating[6] + 1
            #decrease
            batsman1Rating[3] = batsman1Rating[3] - 0.5
            batsman1Rating[4] = batsman1Rating[4] - 0.5
            batsman1Rating[5] = batsman1Rating[5] - 0.5
        elif bowlerPresentRating in range(66,71):
            #increase
            batsman1Rating[0] = batsman1Rating[0] + 2
            batsman1Rating[1] = batsman1Rating[1] + 2
            batsman1Rating[2] = batsman1Rating[2] + 2
            batsman1Rating[6] = batsman1Rating[6] + 2
            #decrease
            batsman1Rating[3] = batsman1Rating[3] - 1
            batsman1Rating[4] = batsman1Rating[4] - 1
            batsman1Rating[5] = batsman1Rating[5] - 1
            
            
        
        ballOutcome = random.choices(outcomes, weights=(batsman1Rating), k=1)
        callBatsman1Rating()
        
        if ballOutcome == [1] or ballOutcome == ['Leg Bye']:
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
            totalExtras = totalExtras + 1
        elif ballOutcome == ['OUT']:
            initialOut = initialOut + 1
            totalWickets = totalWickets + 1
            initialDotBalls = initialDotBalls + 1
            
        elif ballOutcome == [0]:
            initialDotBalls = initialDotBalls + 1
        elif ballOutcome == ['Leg Bye']:
            totalExtras = totalExtras + 1
        else:
            pass
        
        if ballOutcome == ['OUT']:
            outType = random.choice(outList)
            if outType == 'Caught':
                cPlayer = random.choice(oppTeam)
                print('{} {} to {}, {} by {}, {}'.format(ball,bowlerPresent,batsman1,outType,cPlayer,random.choice(outComm)))
            elif outType == 'Bowled':
                print('{} {} to {}, {}, {}'.format(ball,bowlerPresent,batsman1,outType,random.choice(outComm)))
            elif outType == 'Stumped':
                print('{} {} to {}, {} by {}, {}'.format(ball,bowlerPresent,batsman1,outType,*keeper,random.choice(outComm)))
        elif ballOutcome == ['Wide']:
            print('{} {} to {}, {}, {}'.format(ball,bowlerPresent,batsman1,*ballOutcome,'Thats a wide ball from '+bowlerPresent))
        elif ballOutcome == [1]:
            print('{} {} to {}, one {}, {}'.format(ball,bowlerPresent,batsman1,'run',random.choice(oneComm).replace('batsman', batsman1)))
        elif ballOutcome == [2]:
            print('{} {} to {}, two {}, {}'.format(ball,bowlerPresent,batsman1,'runs',random.choice(twoComm).replace('batsman', batsman1)))
        elif ballOutcome == [3]:
            print('{} {} to {}, three {}, {}'.format(ball,bowlerPresent,batsman1,'runs',random.choice(threeComm).replace('batsman', batsman1)))
        elif ballOutcome == [4]:
            print('{} {} to {}, FOUR {}, {}'.format(ball,bowlerPresent,batsman1,'runs',random.choice(fourComm).replace('batsman', batsman1)))
        elif ballOutcome == [6]:
            print('{} {} to {}, SIX ! {}, {}'.format(ball,bowlerPresent,batsman1,'runs',random.choice(sixComm).replace('batsman', batsman1)))
        elif ballOutcome == [0]:
            print('{} {} to {}, dot {}, {}'.format(ball,bowlerPresent,batsman1,'',random.choice(zeroComm).replace('batsman', batsman1)))
        elif ballOutcome == ['Leg Bye']:
            print('{} {} to {}, Leg Bye , {}'.format(ball,bowlerPresent,batsman1,random.choice(oneComm).replace('batsman', batsman1)))
        
        count = count + 1
        if ballOutcome == ['OUT']:
            if count % 10 == 0:
                initialStrikerRuns, intialNonStrikerRuns = intialNonStrikerRuns, initialStrikerRuns
                initialStrikerBallsCount, initialNonStrikerBallsCount = initialNonStrikerBallsCount, initialStrikerBallsCount
                
        if totalWickets == 10:
            print()
            for i in bowlingPlayers:
                if i == bowlerPresent:
                    index = bowlingPlayers.index(i)
                    if bowlersScoreboardOne[index][1] == 0:
                        if iBall == 100:
                            bowlersScoreboardOne[index][1] = bowlersScoreboardOne[index][1] + 10
                            bowlersScoreboardOne[index][2] = bowlersScoreboardOne[index][2] + initialDotBalls
                            bowlersScoreboardOne[index][3] = bowlersScoreboardOne[index][3] + initialScore
                            bowlersScoreboardOne[index][4] = bowlersScoreboardOne[index][4] + initialOut
                            bowlersScoreboardOne[index][5] = bowlersScoreboardOne[index][3] / 20
                            initialBowlerBallsCount = 20
                            # print('     {}     ({}){} [{}x4 {}x6]'.format(batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour, initialStrikeSix))
                            print('     b. {}     {}({}){} [{}x4 {}x6]'.format(bowlerPresent,batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour,initialStrikeSix))
                            print('     {}     ({}){} [{}x4 {}x6]'.format(batsman2,intialNonStrikerRuns,initialNonStrikerBallsCount, initialNonStrikeFour, initialNonStrikeSix))
                            print('     {}     {}-{}-{}-{}'.format(bowlerPresent,initialBowlerBallsCount,bowlersScoreboardOne[index][2],bowlersScoreboardOne[index][3],bowlersScoreboardOne[index][4]))
                            print()
                        else:
                            iBall = str(iBall)
                            tempBalls = iBall[1:]
                            tempBalls = int(tempBalls)
                            bowlersScoreboardOne[index][1] = bowlersScoreboardOne[index][1] + tempBalls
                            bowlersScoreboardOne[index][2] = bowlersScoreboardOne[index][2] + initialDotBalls
                            bowlersScoreboardOne[index][3] = bowlersScoreboardOne[index][3] + initialScore
                            bowlersScoreboardOne[index][4] = bowlersScoreboardOne[index][4] + initialOut
                            if bowlersScoreboardOne[index][1] == 0:
                                bowlersScoreboardOne[index][5] = 0
                            else:
                                bowlersScoreboardOne[index][5] = bowlersScoreboardOne[index][3] / bowlersScoreboardOne[index][1]
                            initialBowlerBallsCount = 10 + tempBalls
                            # print('     {}     ({}){} [{}x4 {}x6]'.format(batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour, initialStrikeSix))
                            print('     b. {}     {}({}){} [{}x4 {}x6]'.format(bowlerPresent,batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour,initialStrikeSix))
                            print('     {}     ({}){} [{}x4 {}x6]'.format(batsman2,intialNonStrikerRuns,initialNonStrikerBallsCount, initialNonStrikeFour, initialNonStrikeSix))
                            print('     {}     {}-{}-{}-{}'.format(bowlerPresent,initialBowlerBallsCount,bowlersScoreboardOne[index][2],bowlersScoreboardOne[index][3],bowlersScoreboardOne[index][4]))
                            print()
                    elif bowlersScoreboardOne[index][1] == 10:
                        if iBall == 100:
                            bowlersScoreboardOne[index][1] = bowlersScoreboardOne[index][1] + 10
                            bowlersScoreboardOne[index][2] = bowlersScoreboardOne[index][2] + initialDotBalls
                            bowlersScoreboardOne[index][3] = bowlersScoreboardOne[index][3] + initialScore
                            bowlersScoreboardOne[index][4] = bowlersScoreboardOne[index][4] + initialOut
                            bowlersScoreboardOne[index][5] = bowlersScoreboardOne[index][3] / 20
                            initialBowlerBallsCount = 20
                            # print('     {}     ({}){} [{}x4 {}x6]'.format(batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour, initialStrikeSix))
                            print('     b. {}     {}({}){} [{}x4 {}x6]'.format(bowlerPresent,batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour,initialStrikeSix))
                            print('     {}     ({}){} [{}x4 {}x6]'.format(batsman2,intialNonStrikerRuns,initialNonStrikerBallsCount, initialNonStrikeFour, initialNonStrikeSix))
                            print('     {}     {}-{}-{}-{}'.format(bowlerPresent,initialBowlerBallsCount,bowlersScoreboardOne[index][2],bowlersScoreboardOne[index][3],bowlersScoreboardOne[index][4]))
                            print()
                        else:
                            iBall = str(iBall)
                            tempBalls = iBall[1:]
                            tempBalls = int(tempBalls)
                            bowlersScoreboardOne[index][1] = bowlersScoreboardOne[index][1] + tempBalls
                            bowlersScoreboardOne[index][2] = bowlersScoreboardOne[index][2] + initialDotBalls
                            bowlersScoreboardOne[index][3] = bowlersScoreboardOne[index][3] + initialScore
                            bowlersScoreboardOne[index][4] = bowlersScoreboardOne[index][4] + initialOut
                            bowlersScoreboardOne[index][5] = bowlersScoreboardOne[index][3] / bowlersScoreboardOne[index][1]
                            initialBowlerBallsCount = 10 + tempBalls
                            # print('     {}     ({}){} [{}x4 {}x6]'.format(batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour, initialStrikeSix))
                            print('     b. {}     {}({}){} [{}x4 {}x6]'.format(bowlerPresent,batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour,initialStrikeSix))
                            print('     {}     ({}){} [{}x4 {}x6]'.format(batsman2,intialNonStrikerRuns,initialNonStrikerBallsCount, initialNonStrikeFour, initialNonStrikeSix))
                            print('     {}     {}-{}-{}-{}'.format(bowlerPresent,initialBowlerBallsCount,bowlersScoreboardOne[index][2],bowlersScoreboardOne[index][3],bowlersScoreboardOne[index][4]))
                            print()
            # print('     {}     {}-{}-{}-{}'.format(bowlerPresent,'10',initialDotBalls,initialScore,initialOut))
            print()
            print('     End of innings (Balls '+str(count)+')')
            rr = totalScore / (count / 10)
            print('     '+team1+'     '+str(totalScore)+'/'+str(totalWickets)+'  (RR: {:.2f})'.format(rr))
            break
            
        
        #wideball
        if ballOutcome == ['Wide']:
            wideBallNo = str(i)
            if bowlerPresentRating in range(71, 76):
                #increase
                batsman1Rating[0] = batsman1Rating[0] + 3
                batsman1Rating[1] = batsman1Rating[1] + 3
                batsman1Rating[2] = batsman1Rating[2] + 1
                #decrease
                batsman1Rating[3] = batsman1Rating[3] - 0.3
                batsman1Rating[4] = batsman1Rating[4] - 1.3
                batsman1Rating[5] = batsman1Rating[5] - 0.7
            elif bowlerPresentRating in range(76, 81):
                #increase
                batsman1Rating[0] = batsman1Rating[0] + 5
                batsman1Rating[1] = batsman1Rating[1] + 5
                batsman1Rating[2] = batsman1Rating[2] + 3
                batsman1Rating[6] = batsman1Rating[6] + 1
                #decrease
                batsman1Rating[3] = batsman1Rating[3] - 0.7
                batsman1Rating[4] = batsman1Rating[4] - 2
                batsman1Rating[5] = batsman1Rating[5] - 1.5
            elif bowlerPresentRating in range(81, 86):
                #increase
                batsman1Rating[0] = batsman1Rating[0] + 6
                batsman1Rating[1] = batsman1Rating[1] + 6
                batsman1Rating[2] = batsman1Rating[2] + 4
                batsman1Rating[6] = batsman1Rating[6] + 2
                #decrease
                batsman1Rating[3] = batsman1Rating[3] - 1
                batsman1Rating[4] = batsman1Rating[4] - 3
                batsman1Rating[5] = batsman1Rating[5] - 2
            elif bowlerPresentRating in range(86, 91):
                #increase
                batsman1Rating[0] = batsman1Rating[0] + 7
                batsman1Rating[1] = batsman1Rating[1] + 7
                batsman1Rating[2] = batsman1Rating[2] + 5
                batsman1Rating[6] = batsman1Rating[6] + 3
                #decrease
                batsman1Rating[3] = batsman1Rating[3] - 2
                batsman1Rating[4] = batsman1Rating[4] - 4
                batsman1Rating[5] = batsman1Rating[5] - 3
            elif bowlerPresentRating in range(91, 96):
                #increase
                batsman1Rating[0] = batsman1Rating[0] + 8
                batsman1Rating[1] = batsman1Rating[1] + 8
                batsman1Rating[2] = batsman1Rating[2] + 6
                batsman1Rating[6] = batsman1Rating[6] + 7
                #decrease
                batsman1Rating[3] = batsman1Rating[3] - 3
                batsman1Rating[4] = batsman1Rating[4] - 5
                batsman1Rating[5] = batsman1Rating[5] - 4
            elif bowlerPresentRating in range(0,55):
                #increase
                batsman1Rating[0] = batsman1Rating[0] - 25
                batsman1Rating[1] = batsman1Rating[1] + 15
                batsman1Rating[2] = batsman1Rating[2] + 15
                batsman1Rating[6] = batsman1Rating[6] - 7
                #decrease
                batsman1Rating[3] = batsman1Rating[3] + 3
                batsman1Rating[4] = batsman1Rating[4] + 6
                batsman1Rating[5] = batsman1Rating[5] + 6
            elif bowlerPresentRating in range(55,61):
                #increase
                batsman1Rating[0] = batsman1Rating[0] + 0.5
                batsman1Rating[1] = batsman1Rating[1] + 0.5
                batsman1Rating[2] = batsman1Rating[2] + 0.5
                batsman1Rating[6] = batsman1Rating[6] + 0.5
                #decrease
                batsman1Rating[3] = batsman1Rating[3] - 0.5
                batsman1Rating[4] = batsman1Rating[4] - 0.5
                batsman1Rating[5] = batsman1Rating[5] - 0.5
            elif bowlerPresentRating in range(61,66):
                #increase
                batsman1Rating[0] = batsman1Rating[0] + 1
                batsman1Rating[1] = batsman1Rating[1] + 1
                batsman1Rating[2] = batsman1Rating[2] + 1
                batsman1Rating[6] = batsman1Rating[6] + 1
                #decrease
                batsman1Rating[3] = batsman1Rating[3] - 0.5
                batsman1Rating[4] = batsman1Rating[4] - 0.5
                batsman1Rating[5] = batsman1Rating[5] - 0.5
            elif bowlerPresentRating in range(66,71):
                #increase
                batsman1Rating[0] = batsman1Rating[0] + 2
                batsman1Rating[1] = batsman1Rating[1] + 2
                batsman1Rating[2] = batsman1Rating[2] + 2
                batsman1Rating[6] = batsman1Rating[6] + 2
                #decrease
                batsman1Rating[3] = batsman1Rating[3] - 1
                batsman1Rating[4] = batsman1Rating[4] - 1
                batsman1Rating[5] = batsman1Rating[5] - 1
                
            ballOutcome = random.choices(outcomes, weights=(batsman1Rating), k=1)
            callBatsman1Rating()
            
            #First over posibilities 'Ball 0X'
            if len(str(i)) == 1:
                ball = 'Ball 0'+str(i)+' : '
                if ballOutcome == [1] or ballOutcome == ['Leg Bye']:
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
                    totalExtras = totalExtras + 1
                elif ballOutcome == ['OUT']:
                    initialOut = initialOut + 1
                    totalWickets = totalWickets + 1
                    initialDotBalls = initialDotBalls + 1
                elif ballOutcome == [0]:
                    initialDotBalls = initialDotBalls + 1
                elif ballOutcome == ['Leg Bye']:
                    totalExtras = totalExtras + 1
                else:
                    pass
                
                if ballOutcome == ['OUT']:
                    outType = random.choice(outList)
                    if outType == 'Caught':
                        cPlayer = random.choice(oppTeam)
                        print('{} {} to {}, {} by {}, {}'.format(ball,bowlerPresent,batsman1,outType,cPlayer,random.choice(outComm)))
                    elif outType == 'Bowled':
                        print('{} {} to {}, {}, {}'.format(ball,bowlerPresent,batsman1,outType,random.choice(outComm)))
                    elif outType == 'Stumped':
                        print('{} {} to {}, {} by {}, {}'.format(ball,bowlerPresent,batsman1,outType,*keeper,random.choice(outComm)))
                    # print('{} {} to {}, {}, {}'.format(ball,bowlerPresent,batsman1,*ballOutcome,random.choice(outComm)))
                elif ballOutcome == ['Wide']:
                    print('{} {} to {},{}, {}'.format(ball,bowlerPresent,batsman1,*ballOutcome,'Thats a wide ball from '+bowlerPresent))
                elif ballOutcome == [1]:
                    print('{} {} to {}, one {}, {}'.format(ball,bowlerPresent,batsman1,'run',random.choice(oneComm).replace('batsman', batsman1)))
                elif ballOutcome == [2]:
                    print('{} {} to {}, two {}, {}'.format(ball,bowlerPresent,batsman1,'runs',random.choice(twoComm).replace('batsman', batsman1)))
                elif ballOutcome == [3]:
                    print('{} {} to {}, three {}, {}'.format(ball,bowlerPresent,batsman1,'runs',random.choice(threeComm).replace('batsman', batsman1)))
                elif ballOutcome == [4]:
                    print('{} {} to {}, FOUR {}, {}'.format(ball,bowlerPresent,batsman1,'runs',random.choice(fourComm).replace('batsman', batsman1)))
                elif ballOutcome == [6]:
                    print('{} {} to {}, SIX ! {}, {}'.format(ball,bowlerPresent,batsman1,'runs',random.choice(sixComm).replace('batsman', batsman1)))
                elif ballOutcome == [0]:
                    print('{} {} to {}, dot {}, {}'.format(ball,bowlerPresent,batsman1,'',random.choice(zeroComm).replace('batsman', batsman1)))
                elif ballOutcome == ['Leg Bye']:
                    print('{} {} to {}, Leg Bye , {}'.format(ball,bowlerPresent,batsman1,random.choice(oneComm).replace('batsman', batsman1)))
        
                # print('{} {} to {} : {} runs'.format(ball,bowlerPresent,batsman1,*ballOutcome))
                if totalWickets == 10:
                    print()
                    for i in bowlingPlayers:
                        if i == bowlerPresent:
                            index = bowlingPlayers.index(i)
                            if bowlersScoreboardOne[index][1] == 0:
                                if iBall == 100:
                                    bowlersScoreboardOne[index][1] = bowlersScoreboardOne[index][1] + 10
                                    bowlersScoreboardOne[index][2] = bowlersScoreboardOne[index][2] + initialDotBalls
                                    bowlersScoreboardOne[index][3] = bowlersScoreboardOne[index][3] + initialScore
                                    bowlersScoreboardOne[index][4] = bowlersScoreboardOne[index][4] + initialOut
                                    bowlersScoreboardOne[index][5] = bowlersScoreboardOne[index][3] / 20
                                    initialBowlerBallsCount = 20
                                    # print('     {}     ({}){} [{}x4 {}x6]'.format(batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour, initialStrikeSix))
                                    print('     b. {}     {}({}){} [{}x4 {}x6]'.format(bowlerPresent,batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour,initialStrikeSix))
                                    print('     {}     ({}){} [{}x4 {}x6]'.format(batsman2,intialNonStrikerRuns,initialNonStrikerBallsCount, initialNonStrikeFour, initialNonStrikeSix))
                                    print('     {}     {}-{}-{}-{}'.format(bowlerPresent,initialBowlerBallsCount,bowlersScoreboardOne[index][2],bowlersScoreboardOne[index][3],bowlersScoreboardOne[index][4]))
                                    print()
                                else:
                                    iBall = str(iBall)
                                    tempBalls = iBall[1:]
                                    tempBalls = int(tempBalls)
                                    bowlersScoreboardOne[index][1] = bowlersScoreboardOne[index][1] + tempBalls
                                    bowlersScoreboardOne[index][2] = bowlersScoreboardOne[index][2] + initialDotBalls
                                    bowlersScoreboardOne[index][3] = bowlersScoreboardOne[index][3] + initialScore
                                    bowlersScoreboardOne[index][4] = bowlersScoreboardOne[index][4] + initialOut
                                    bowlersScoreboardOne[index][5] = bowlersScoreboardOne[index][3] / bowlersScoreboardOne[index][1]
                                    initialBowlerBallsCount = 10 + tempBalls
                                    # print('     {}     ({}){} [{}x4 {}x6]'.format(batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour, initialStrikeSix))
                                    print('     b. {}     {}({}){} [{}x4 {}x6]'.format(bowlerPresent,batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour,initialStrikeSix))
                                    print('     {}     ({}){} [{}x4 {}x6]'.format(batsman2,intialNonStrikerRuns,initialNonStrikerBallsCount, initialNonStrikeFour, initialNonStrikeSix))
                                    print('     {}     {}-{}-{}-{}'.format(bowlerPresent,initialBowlerBallsCount,bowlersScoreboardOne[index][2],bowlersScoreboardOne[index][3],bowlersScoreboardOne[index][4]))
                                    print()
                            elif bowlersScoreboardOne[index][1] == 10:
                                if iBall == 100:
                                    bowlersScoreboardOne[index][1] = bowlersScoreboardOne[index][1] + 10
                                    bowlersScoreboardOne[index][2] = bowlersScoreboardOne[index][2] + initialDotBalls
                                    bowlersScoreboardOne[index][3] = bowlersScoreboardOne[index][3] + initialScore
                                    bowlersScoreboardOne[index][4] = bowlersScoreboardOne[index][4] + initialOut
                                    bowlersScoreboardOne[index][5] = bowlersScoreboardOne[index][3] / 20
                                    initialBowlerBallsCount = 20
                                    # print('     {}     ({}){} [{}x4 {}x6]'.format(batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour, initialStrikeSix))
                                    print('     b. {}     {}({}){} [{}x4 {}x6]'.format(bowlerPresent,batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour,initialStrikeSix))
                                    print('     {}     ({}){} [{}x4 {}x6]'.format(batsman2,intialNonStrikerRuns,initialNonStrikerBallsCount, initialNonStrikeFour, initialNonStrikeSix))
                                    print('     {}     {}-{}-{}-{}'.format(bowlerPresent,initialBowlerBallsCount,bowlersScoreboardOne[index][2],bowlersScoreboardOne[index][3],bowlersScoreboardOne[index][4]))
                                    print()
                                else:
                                    iBall = str(iBall)
                                    tempBalls = iBall[1:]
                                    tempBalls = int(tempBalls)
                                    bowlersScoreboardOne[index][1] = bowlersScoreboardOne[index][1] + tempBalls
                                    bowlersScoreboardOne[index][2] = bowlersScoreboardOne[index][2] + initialDotBalls
                                    bowlersScoreboardOne[index][3] = bowlersScoreboardOne[index][3] + initialScore
                                    bowlersScoreboardOne[index][4] = bowlersScoreboardOne[index][4] + initialOut
                                    bowlersScoreboardOne[index][5] = bowlersScoreboardOne[index][3] / bowlersScoreboardOne[index][1]
                                    initialBowlerBallsCount = 10 + tempBalls
                                    # print('     {}     ({}){} [{}x4 {}x6]'.format(batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour, initialStrikeSix))
                                    print('     b. {}     {}({}){} [{}x4 {}x6]'.format(bowlerPresent,batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour,initialStrikeSix))
                                    print('     {}     ({}){} [{}x4 {}x6]'.format(batsman2,intialNonStrikerRuns,initialNonStrikerBallsCount, initialNonStrikeFour, initialNonStrikeSix))
                                    print('     {}     {}-{}-{}-{}'.format(bowlerPresent,initialBowlerBallsCount,bowlersScoreboardOne[index][2],bowlersScoreboardOne[index][3],bowlersScoreboardOne[index][4]))
                                    print()
                    # print('     {}     {}-{}-{}-{}'.format(bowlerPresent,'10',initialDotBalls,initialScore,initialOut))
                    print()
                    print('     End of innings (Balls '+str(count)+')')
                    rr = totalScore / (count / 10)
                    print('     '+team1+'     '+str(totalScore)+'/'+str(totalWickets)+'  (RR: {:.2f})'.format(rr))
                    break
            else: #Rest 90 balls 'Ball 1X'
                ball = 'Ball '+str(i)+' : '
                if ballOutcome == [1] or ballOutcome == ['Leg Bye']:
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
                    totalExtras = totalExtras + 1
                elif ballOutcome == ['OUT']:
                    initialOut = initialOut + 1
                    totalWickets = totalWickets + 1
                    initialDotBalls =  initialDotBalls + 1
                elif ballOutcome == [0]:
                     initialDotBalls = initialDotBalls + 1
                elif ballOutcome == ['Leg Bye']:
                    totalExtras = totalExtras + 1
                else:
                    pass
                
                if ballOutcome == ['OUT']:
                    outType = random.choice(outList)
                    if outType == 'Caught':
                        cPlayer = random.choice(oppTeam)
                        print('{} {} to {}, {} by {}, {}'.format(ball,bowlerPresent,batsman1,outType,cPlayer,random.choice(outComm)))
                    elif outType == 'Bowled':
                        print('{} {} to {}, {}, {}'.format(ball,bowlerPresent,batsman1,outType,random.choice(outComm)))
                    elif outType == 'Stumped':
                        print('{} {} to {}, {} by {}, {}'.format(ball,bowlerPresent,batsman1,outType,*keeper,random.choice(outComm)))
                    # print('{} {} to {}, {}, {}'.format(ball,bowlerPresent,batsman1,*ballOutcome,random.choice(outComm)))
                elif ballOutcome == ['Wide']:
                    print('{} {} to {},{}, {}'.format(ball,bowlerPresent,batsman1,*ballOutcome,'Thats a wide ball from '+bowlerPresent))
                elif ballOutcome == [1]:
                    print('{} {} to {}, one {}, {}'.format(ball,bowlerPresent,batsman1,'run',random.choice(oneComm).replace('batsman', batsman1)))
                elif ballOutcome == [2]:
                    print('{} {} to {}, two {}, {}'.format(ball,bowlerPresent,batsman1,'runs',random.choice(twoComm).replace('batsman', batsman1)))
                elif ballOutcome == [3]:
                    print('{} {} to {}, three {}, {}'.format(ball,bowlerPresent,batsman1,'runs',random.choice(threeComm).replace('batsman', batsman1)))
                elif ballOutcome == [4]:
                    print('{} {} to {}, FOUR {}, {}'.format(ball,bowlerPresent,batsman1,'runs',random.choice(fourComm).replace('batsman', batsman1)))
                elif ballOutcome == [6]:
                    print('{} {} to {}, SIX ! {}, {}'.format(ball,bowlerPresent,batsman1,'runs',random.choice(sixComm).replace('batsman', batsman1)))
                elif ballOutcome == [0]:
                    print('{} {} to {}, dot {}, {}'.format(ball,bowlerPresent,batsman1,'',random.choice(zeroComm).replace('batsman', batsman1)))
                elif ballOutcome == ['Leg Bye']:
                    print('{} {} to {}, Leg Bye , {}'.format(ball,bowlerPresent,batsman1,random.choice(oneComm).replace('batsman', batsman1)))
        
                # print('{} {} to {} : {} runs'.format(ball,bowlerPresent,batsman1,*ballOutcome))
                if totalWickets == 10:
                    print()
                    for i in bowlingPlayers:
                        if i == bowlerPresent:
                            index = bowlingPlayers.index(i)
                            if bowlersScoreboardOne[index][1] == 0:
                                if iBall == 100:
                                    bowlersScoreboardOne[index][1] = bowlersScoreboardOne[index][1] + 10
                                    bowlersScoreboardOne[index][2] = bowlersScoreboardOne[index][2] + initialDotBalls
                                    bowlersScoreboardOne[index][3] = bowlersScoreboardOne[index][3] + initialScore
                                    bowlersScoreboardOne[index][4] = bowlersScoreboardOne[index][4] + initialOut
                                    bowlersScoreboardOne[index][5] = bowlersScoreboardOne[index][3] / 20
                                    initialBowlerBallsCount = 20
                                    # print('     {}     ({}){} [{}x4 {}x6]'.format(batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour, initialStrikeSix))
                                    print('     b. {}     {}({}){} [{}x4 {}x6]'.format(bowlerPresent,batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour,initialStrikeSix))
                                    print('     {}     ({}){} [{}x4 {}x6]'.format(batsman2,intialNonStrikerRuns,initialNonStrikerBallsCount, initialNonStrikeFour, initialNonStrikeSix))
                                    print('     {}     {}-{}-{}-{}'.format(bowlerPresent,initialBowlerBallsCount,bowlersScoreboardOne[index][2],bowlersScoreboardOne[index][3],bowlersScoreboardOne[index][4]))
                                    print()
                                else:
                                    iBall = str(iBall)
                                    tempBalls = iBall[1:]
                                    tempBalls = int(tempBalls)
                                    bowlersScoreboardOne[index][1] = bowlersScoreboardOne[index][1] + tempBalls
                                    bowlersScoreboardOne[index][2] = bowlersScoreboardOne[index][2] + initialDotBalls
                                    bowlersScoreboardOne[index][3] = bowlersScoreboardOne[index][3] + initialScore
                                    bowlersScoreboardOne[index][4] = bowlersScoreboardOne[index][4] + initialOut
                                    bowlersScoreboardOne[index][5] = bowlersScoreboardOne[index][3] / bowlersScoreboardOne[index][1]
                                    initialBowlerBallsCount = 10 + tempBalls
                                    # print('     {}     ({}){} [{}x4 {}x6]'.format(batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour, initialStrikeSix))
                                    print('     b. {}     {}({}){} [{}x4 {}x6]'.format(bowlerPresent,batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour,initialStrikeSix))
                                    print('     {}     ({}){} [{}x4 {}x6]'.format(batsman2,intialNonStrikerRuns,initialNonStrikerBallsCount, initialNonStrikeFour, initialNonStrikeSix))
                                    print('     {}     {}-{}-{}-{}'.format(bowlerPresent,initialBowlerBallsCount,bowlersScoreboardOne[index][2],bowlersScoreboardOne[index][3],bowlersScoreboardOne[index][4]))
                                    print()
                            elif bowlersScoreboardOne[index][1] == 10:
                                if iBall == 100:
                                    bowlersScoreboardOne[index][1] = bowlersScoreboardOne[index][1] + 10
                                    bowlersScoreboardOne[index][2] = bowlersScoreboardOne[index][2] + initialDotBalls
                                    bowlersScoreboardOne[index][3] = bowlersScoreboardOne[index][3] + initialScore
                                    bowlersScoreboardOne[index][4] = bowlersScoreboardOne[index][4] + initialOut
                                    bowlersScoreboardOne[index][5] = bowlersScoreboardOne[index][3] / 20
                                    initialBowlerBallsCount = 20
                                    # print('     {}     ({}){} [{}x4 {}x6]'.format(batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour, initialStrikeSix))
                                    print('     b. {}     {}({}){} [{}x4 {}x6]'.format(bowlerPresent,batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour,initialStrikeSix))
                                    print('     {}     ({}){} [{}x4 {}x6]'.format(batsman2,intialNonStrikerRuns,initialNonStrikerBallsCount, initialNonStrikeFour, initialNonStrikeSix))
                                    print('     {}     {}-{}-{}-{}'.format(bowlerPresent,initialBowlerBallsCount,bowlersScoreboardOne[index][2],bowlersScoreboardOne[index][3],bowlersScoreboardOne[index][4]))
                                    print()
                                else:
                                    iBall = str(iBall)
                                    tempBalls = iBall[1:]
                                    tempBalls = int(tempBalls)
                                    bowlersScoreboardOne[index][1] = bowlersScoreboardOne[index][1] + tempBalls
                                    bowlersScoreboardOne[index][2] = bowlersScoreboardOne[index][2] + initialDotBalls
                                    bowlersScoreboardOne[index][3] = bowlersScoreboardOne[index][3] + initialScore
                                    bowlersScoreboardOne[index][4] = bowlersScoreboardOne[index][4] + initialOut
                                    bowlersScoreboardOne[index][5] = bowlersScoreboardOne[index][3] / bowlersScoreboardOne[index][1]
                                    initialBowlerBallsCount = 10 + tempBalls
                                    # print('     {}     ({}){} [{}x4 {}x6]'.format(batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour, initialStrikeSix))
                                    print('     b. {}     {}({}){} [{}x4 {}x6]'.format(bowlerPresent,batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour,initialStrikeSix))
                                    print('     {}     ({}){} [{}x4 {}x6]'.format(batsman2,intialNonStrikerRuns,initialNonStrikerBallsCount, initialNonStrikeFour, initialNonStrikeSix))
                                    print('     {}     {}-{}-{}-{}'.format(bowlerPresent,initialBowlerBallsCount,bowlersScoreboardOne[index][2],bowlersScoreboardOne[index][3],bowlersScoreboardOne[index][4]))
                                    print()
                                    
                                    
                                # print('     {}     ({}){} [{}x4 {}x6]'.format(batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour, initialStrikeSix))
                                # print('     b. {}     {}({}){} [{}x4 {}x6]'.format(bowlerPresent,batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour,initialStrikeSix))
                                # print('     {}     ({}){} [{}x4 {}x6]'.format(batsman2,intialNonStrikerRuns,initialNonStrikerBallsCount, initialNonStrikeFour, initialNonStrikeSix))
                                # print('     {}     {}-{}-{}-{}'.format(bowlerPresent,initialBowlerBallsCount,bowlersScoreboardOne[index][2],bowlersScoreboardOne[index][3],bowlersScoreboardOne[index][4]))
                                # print()
                    # print('     {}     {}-{}-{}-{}'.format(bowlerPresent,'10',initialDotBalls,initialScore,initialOut))
                    print()
                    print('     End of innings (Balls '+str(count)+')')
                    rr = totalScore / (count / 10)
                    print('     '+team1+'     '+str(totalScore)+'/'+str(totalWickets)+'  (RR: {:.2f})'.format(rr))
                    break

        #End of every 10 balls presenting score  
        if count % 10 == 0:
            print()
            print('     END of '+str(count)+' balls ('+str(initialScore)+' runs)')
            print('     '+team1+'     '+str(totalScore)+'/'+str(totalWickets))
            rr = totalScore / (count / 10)

            
            print('     RR: {:.2f}'.format(rr))
            print()
            # print('     {}     {}-{}-{}-{}'.format(bowlerPresent,'10',initialDotBalls,initialScore,initialOut))
            # print()
            
            if count == 100:
                print()
                print('     End of innings (Balls '+str(count)+')')
                rr = totalScore / (count / 10)
                print('     '+team1+'     '+str(totalScore)+'/'+str(totalWickets)+'  (RR: {:.2f})'.format(rr))
                
            # #Reseting over score before the begini of new over.
            # initialScore = 0
            # initialOut = 0
            # initialDotBalls = 0
            # #Change of bowler
            # bowlerPresent = pickBowler() #bowler
            
            # # bowler = random.choice(bowlingPlayers)
            # # bowlerPresent = bowler
            
            
            
        #If out bring in next batsmen
        # if ballOutcome == ['OUT']:
        #     playerOut = playerOut + 1
        #     batsman1Rating = battingPlayerRatings[b+playerOut+1]
        #     batsman1 = battingPlayerNames[b+playerOut+1]
            
        
        #Checking weather to rotate strike or not after the end of over and in between the innings
        if ballOutcome == [1] or ballOutcome == ['Leg Bye']:
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
                batsman1, batsman2 = batsman1, batsman2
                batsman1Rating, batsman2Rating = batsman1Rating, batsman2Rating
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
        elif ballOutcome == ['Leg Bye']:
            if count % 10 == 0: #when outcome 1 on last ball of over, strike change.
                #add runs to strike batsmen
                initialStrikerRuns = initialStrikerRuns + 0
                initialStrikerBallsCount = initialStrikerBallsCount + 1
                initialStrikerRuns, intialNonStrikerRuns = initialStrikerRuns, intialNonStrikerRuns
                initialStrikerBallsCount, initialNonStrikerBallsCount = initialStrikerBallsCount, initialNonStrikerBallsCount
            else:
                #add runs to strike batsmen
                initialStrikerRuns = initialStrikerRuns + 0
                initialStrikerBallsCount = initialStrikerBallsCount + 1
                initialStrikerRuns, intialNonStrikerRuns = intialNonStrikerRuns, initialStrikerRuns
                initialStrikerBallsCount, initialNonStrikerBallsCount = initialNonStrikerBallsCount, initialStrikerBallsCount
            # print(batsman1+'-> '+' Fours: '+str(initialStrikeFour)+' Sixes: '+str(initialStrikeSix))
            # print(batsman2+'-> '+' Fours: '+str(initialNonStrikeFour)+' Sixes: '+str(initialNonStrikeSix))
        
        
        #Name. Balls, Dots, Runs, Wickets, Economy
        if count % 10 == 0:
    
            for i in bowlingPlayers:
                if i == bowlerPresent:
                    index = bowlingPlayers.index(i)
                    if bowlersScoreboardOne[index][1] == 0:
                        bowlersScoreboardOne[index][1] = 10
                        bowlersScoreboardOne[index][2] = initialDotBalls
                        bowlersScoreboardOne[index][3] = initialScore
                        bowlersScoreboardOne[index][4] = initialOut
                        bowlersScoreboardOne[index][5] = initialScore / 10
                        initialBowlerBallsCount = 10
                        print('     {}     ({}){} [{}x4 {}x6]'.format(batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour, initialStrikeSix))
                        print('     {}     ({}){} [{}x4 {}x6]'.format(batsman2,intialNonStrikerRuns,initialNonStrikerBallsCount, initialNonStrikeFour, initialNonStrikeSix))
                        print('     {}     {}-{}-{}-{}'.format(bowlerPresent,initialBowlerBallsCount,initialDotBalls,initialScore,initialOut))
                        print()
                    elif bowlersScoreboardOne[index][1] == 10:
                        bowlersScoreboardOne[index][1] = bowlersScoreboardOne[index][1] + 10
                        bowlersScoreboardOne[index][2] = bowlersScoreboardOne[index][2] + initialDotBalls
                        bowlersScoreboardOne[index][3] = bowlersScoreboardOne[index][3] + initialScore
                        bowlersScoreboardOne[index][4] = bowlersScoreboardOne[index][4] + initialOut
                        bowlersScoreboardOne[index][5] = bowlersScoreboardOne[index][3] / 20
                        initialBowlerBallsCount = 20
                        print('     {}     ({}){} [{}x4 {}x6]'.format(batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour, initialStrikeSix))
                        print('     {}     ({}){} [{}x4 {}x6]'.format(batsman2,intialNonStrikerRuns,initialNonStrikerBallsCount, initialNonStrikeFour, initialNonStrikeSix))
                        print('     {}     {}-{}-{}-{}'.format(bowlerPresent,initialBowlerBallsCount,bowlersScoreboardOne[index][2],bowlersScoreboardOne[index][3],bowlersScoreboardOne[index][4]))
                        print()
            
            # print('     {}     ({}){} [{}x4 {}x6]'.format(batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour, initialStrikeSix))
            # print('     {}     ({}){} [{}x4 {}x6]'.format(batsman2,intialNonStrikerRuns,initialNonStrikerBallsCount, initialNonStrikeFour, initialNonStrikeSix))
            # print('     {}     {}-{}-{}-{}'.format(bowlerPresent,'10',initialDotBalls,initialScore,initialOut))
            # print()
            

            
            #Reseting over score before the begini of new over.
            initialScore = 0
            initialOut = 0
            #Change of bowler
            if ballOutcome == ['OUT']:
                sr = initialStrikerRuns * 100 // initialStrikerBallsCount
                if outType == 'Bowled':
                    batsmenScoreboard1.append([batsman1, 'b. ','', bowlerPresent, initialStrikerRuns, initialStrikerBallsCount, 
                   initialStrikeFour, initialStrikeSix, sr])
                elif outType == 'Caught':
                    batsmenScoreboard1.append([batsman1, 'c. ',cPlayer, bowlerPresent, initialStrikerRuns, initialStrikerBallsCount, 
                   initialStrikeFour, initialStrikeSix, sr])
                elif outType == 'Stumped':
                    batsmenScoreboard1.append([batsman1, 'st. ',*keeper, bowlerPresent, initialStrikerRuns, initialStrikerBallsCount, 
                   initialStrikeFour, initialStrikeSix, sr])
                
                if outType == 'Bowled':
                    print('     b. {}     {}({}){} [{}x4 {}x6]'.format(bowlerPresent,batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour,initialStrikeSix))
                elif outType == 'Stumped':
                    print('     st. {}     b. {}     {}({}){} [{}x4 {}x6]'.format(*keeper,bowlerPresent,batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour,initialStrikeSix))
                elif outType == 'Caught':
                    print('     c. {}     b. {}     {}({}){} [{}x4 {}x6]'.format(cPlayer,bowlerPresent,batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour,initialStrikeSix))
                initialStrikerRuns = 0
                initialStrikerBallsCount = 0
                initialStrikeFour = 0
                initialStrikeSix = 0
                print()
                playerOut = playerOut + 1
                batsman1Rating = battingPlayerRatings[b+playerOut+1]
                batsman1 = battingPlayerNames[b+playerOut+1]
                
            
            bowlerPresent = pickBowler() #bowler
            
            # bowler = random.choice(bowlingPlayers)
            # bowlerPresent = bowler
            
            initialDotBalls = 0
        
        #If out bring in next batsmen
        if count % 10 != 0 and  ballOutcome == ['OUT']:
            sr = initialStrikerRuns * 100 // initialStrikerBallsCount
            if outType == 'Bowled':
                batsmenScoreboard1.append([batsman1, 'b. ','', bowlerPresent, initialStrikerRuns, initialStrikerBallsCount, 
               initialStrikeFour, initialStrikeSix, sr])
            elif outType == 'Caught':
                batsmenScoreboard1.append([batsman1, 'c. ',cPlayer, bowlerPresent, initialStrikerRuns, initialStrikerBallsCount, 
               initialStrikeFour, initialStrikeSix, sr])
            elif outType == 'Stumped':
                batsmenScoreboard1.append([batsman1, 'st. ',*keeper, bowlerPresent, initialStrikerRuns, initialStrikerBallsCount, 
               initialStrikeFour, initialStrikeSix, sr])
                    
            # batsmenScoreboard1.append([batsman1, bowlerPresent, initialStrikerRuns, initialStrikerBallsCount, 
            #        initialStrikeFour, initialStrikeSix, sr])
            
            print()
            if outType == 'Bowled':
                print('     b. {}     {}({}){} [{}x4 {}x6]'.format(bowlerPresent,batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour,initialStrikeSix))
            elif outType == 'Stumped':
                print('     st. {}     b. {}     {}({}){} [{}x4 {}x6]'.format(*keeper,bowlerPresent,batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour,initialStrikeSix))
            elif outType == 'Caught':
                print('     c. {}     b. {}     {}({}){} [{}x4 {}x6]'.format(cPlayer,bowlerPresent,batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour,initialStrikeSix))
            # print('     b. {}     {}({}){} [{}x4 {}x6]'.format(bowlerPresent,batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour,initialStrikeSix))
            initialStrikerRuns = 0
            initialStrikerBallsCount = 0
            initialStrikeFour = 0
            initialStrikeSix = 0
            print()
            playerOut = playerOut + 1
            batsman1Rating = battingPlayerRatings[b+playerOut+1]
            batsman1 = battingPlayerNames[b+playerOut+1]
    
    if count == 100:
        if totalWickets != 10:
            if initialStrikerBallsCount == 0:
                sr1 = 0
            else:
                sr1 = initialStrikerRuns * 100 // initialStrikerBallsCount
            sr2 = intialNonStrikerRuns * 100 // initialNonStrikerBallsCount
            batsmenScoreboard1.append([batsman1, "Not Out",'','', initialStrikerRuns, initialStrikerBallsCount, 
           initialStrikeFour, initialStrikeSix, sr1])
            batsmenScoreboard1.append([batsman2, "Not Out",'','', intialNonStrikerRuns, initialNonStrikerBallsCount, 
           initialNonStrikeFour, initialNonStrikeSix, sr2])
        if totalWickets == 10:
            sr2 = intialNonStrikerRuns * 100 // initialNonStrikerBallsCount
            batsmenScoreboard1.append([batsman2, "Not Out",'','', intialNonStrikerRuns, initialNonStrikerBallsCount, 
           initialNonStrikeFour, initialNonStrikeSix, sr2])
            
    if count != 100 and totalWickets == 10:
        if initialStrikerBallsCount == 0:
            sr1 = 0
        else:
            sr1 = initialStrikerRuns * 100 // initialStrikerBallsCount
            if outType == 'Bowled':
                batsmenScoreboard1.append([batsman1, 'b. ','', bowlerPresent, initialStrikerRuns, initialStrikerBallsCount, 
               initialStrikeFour, initialStrikeSix, sr1])
            elif outType == 'Caught':
                batsmenScoreboard1.append([batsman1, 'c. ',cPlayer, bowlerPresent, initialStrikerRuns, initialStrikerBallsCount, 
               initialStrikeFour, initialStrikeSix, sr1])
            elif outType == 'Stumped':
                batsmenScoreboard1.append([batsman1, 'st. ',*keeper, bowlerPresent, initialStrikerRuns, initialStrikerBallsCount, 
               initialStrikeFour, initialStrikeSix, sr1])
                    
            sr2 = intialNonStrikerRuns * 100 // initialNonStrikerBallsCount
            batsmenScoreboard1.append([batsman2, "Not Out",'','', intialNonStrikerRuns, initialNonStrikerBallsCount, 
           initialNonStrikeFour, initialNonStrikeSix, sr2])
        
    
    print()
    print(team1+' 1st Innings Scoreboard')
    print()
    batsmenScoreboardOne = pd.DataFrame(batsmenScoreboard1, columns =['Batsman','','Fielder','Bowler','Runs','Balls','4s','6s','SR'])
    # print(batsmenScoreboardOne)
    print(tabulate(batsmenScoreboardOne, showindex=False, headers=batsmenScoreboardOne.columns))
    dnb = batsmenScoreboardOne['Batsman'].to_list()
    dnb = list(set(battingPlayerNames) - set(dnb))
    print()
    print('   Total:   {}/{}        Balls: {}        Run Rate: {}        Extras: {}'.format(totalScore,totalWickets,count,round(rr,2),totalExtras))
    print()
    if len(dnb) == 0:
        print('DNB : Nil')
    else: 
        print('DNB : ',dnb)
    print()
    
    # timestr = time.strftime("%Y%m%d-%H%M%S")
    # bat = path+team1+'-batting'+timestr+'.csv'
    # batsmenScoreboardOne.to_csv(bat)
    
    bowlersScoreboard1 = pd.DataFrame(bowlersScoreboardOne, columns=['Bowler','Balls','Dots','Runs','Wickets','Economy'])
    bowlersScoreboard1.round({"Economy":2})
    print(team2+' Bowling Scoreboard')
    print()
    print(tabulate(bowlersScoreboard1, showindex=False, headers=bowlersScoreboard1.columns))
    # timestr = time.strftime("%Y%m%d-%H%M%S")
    # ball = path+team2+'-bowling'+timestr+'.csv'
    # bowlersScoreboard1.to_csv(ball)
    
    target = totalScore + 1
    rrr = target / 100
    print()
    print(team2+' need '+str(target)+' runs in 100 balls at '+str(round(rrr,2))+' run/s per ball.')
    
    team1, team2 = team2, team1
    prepInnings2(team1, team2, target)
    # endSaveScript()


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
print('     '+team1+'   vs   '+team2)
print()

#saving output to file opening
# parent_dir = "./"
# timestr = time.strftime("%Y%m%d-%H%M%S")
# directory = team1+' vs '+team2+'-'+timestr
# path = os.path.join(parent_dir, directory) 
# os.mkdir(path)
 
# stdoutOrigin = sys.stdout
# path = './'+path+'/'
# filename = team1+' vs '+team2+'-'+timestr+'.txt' 
# sys.stdout = open(path+filename, "w")

#toss options
toss = ['Heads','Tails']
tossChoice = random.choice(toss)

#2nd team toss call and generating random option (Away team choice)
#Dhoni spins the coin "Williamson choose tails".
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
        prepInnings(team1, team2)

    elif firstChoiceCall == 'Bat':
        team1, team2 = team2, team1
        prepInnings(team1, team2)    
else:
    print()
    print(team1+' won the toss and choose to '+firstChoiceCall+' first !')
    print()
    if firstChoiceCall == 'Bowl':
        team1, team2 = team2, team1
        prepInnings(team1, team2)

    elif firstChoiceCall == 'Bat':
        team1, team2 = team1, team2
        prepInnings(team1, team2)
