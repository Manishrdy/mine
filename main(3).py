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
import numpy as np
import sys
import time
import io

outcomes = [0, 1, 2, 3, 4, 6, 'OUT', 'Wide']
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
    print()
    
    battingTeam1 = pd.read_csv(team1+'.csv')
    bowlingTeam1 = pd.read_csv(team2+'.csv')
    
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
    
    
    inng1InningsBatting = {}
    inng2InningsBowling = {}
    
    print(team1+' - ',battingPlayerNames)
    print(team2+' - ',bowlingPlayers)
    print()
    
    def pickBowler():
        bowler = random.choice(bowlingPlayers)
        return bowler
    
    b = 0
    playerOut = 0
    bowlerPresent = pickBowler()
    batsman1 = battingPlayerNames[b]
    batsman2 = battingPlayerNames[b+1]
    batsman1Rating = battingPlayerRatings[b]
    batsman2Rating = battingPlayerRatings[b+1]
    
    print('%%%%%  Second Innings  %%%%%')
    print()
    
    for i in range(1,101):
        # time.sleep(gameRate)
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
            print('{} {} to {}, {}, {}'.format(ball,bowlerPresent,batsman1,*ballOutcome,random.choice(outComm)))
        elif ballOutcome == ['Wide']:
            print('{} {} to {},{}, {}'.format(ball,bowlerPresent,batsman1,*ballOutcome,'Thats a wide ball from '+bowlerPresent))
        elif ballOutcome == [1]:
            print('{} {} to {}, one {}, {}'.format(ball,bowlerPresent,batsman1,'run',random.choice(oneComm)))
        elif ballOutcome == [2]:
            print('{} {} to {}, two {}, {}'.format(ball,bowlerPresent,batsman1,'runs',random.choice(twoComm)))
        elif ballOutcome == [3]:
            print('{} {} to {}, three {}, {}'.format(ball,bowlerPresent,batsman1,'runs',random.choice(threeComm)))
        elif ballOutcome == [4]:
            print('{} {} to {}, FOUR {}, {}'.format(ball,bowlerPresent,batsman1,'runs',random.choice(fourComm)))
        elif ballOutcome == [6]:
            print('{} {} to {}, SIX ! {}, {}'.format(ball,bowlerPresent,batsman1,'runs',random.choice(sixComm)))
        else:
            print('{} {} to {}, dot ball, {}'.format(ball,bowlerPresent,batsman1,random.choice(zeroComm)))
        
        count = count + 1
        
        #Checking for winner after every ball
        if totalScore >= target:
            sr1 = initialStrikerRuns * 100 // initialStrikerBallsCount
            sr2 = intialNonStrikerRuns * 100 // initialNonStrikerBallsCount
            batsmenScoreboard2.append([batsman1, "Not Out", initialStrikerRuns, initialStrikerBallsCount, 
            initialStrikeFour, initialStrikeSix, sr1])
            batsmenScoreboard2.append([batsman2, "Not Out", intialNonStrikerRuns, initialNonStrikerBallsCount, 
            initialNonStrikeFour, initialNonStrikeSix, sr2])
            print()
            print('     {}     {}-{}-{}-{}'.format(bowlerPresent,'10',initialDotBalls,initialScore,initialOut))
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
            print('     {}     {}-{}-{}-{}'.format(bowlerPresent,'10',initialDotBalls,initialScore,initialOut))
            print()
            if totalScore < target:
                print('     END of '+str(count)+' balls ('+str(initialScore)+' runs)')
                print('     '+team1+'     '+str(totalScore)+'/'+str(totalWickets))
                rr = totalScore / (count / 10)
                print('     RR: {:.2f}'.format(rr))
                print()
            print('     End of innings (Balls '+str(count)+')')
            rr = totalScore / (count / 10)
            print('     '+team1+'     '+str(totalScore)+'/'+str(totalWickets)+'  (RR: {:.2f})'.format(rr))
            
            print()
            if totalScore < target:
                sr2 = intialNonStrikerRuns * 100 // initialNonStrikerBallsCount
                batsmenScoreboard2.append([batsman2, "Not Out", intialNonStrikerRuns, initialNonStrikerBallsCount, 
                initialNonStrikeFour, initialNonStrikeSix, sr2])
                print()
                diff = target - totalScore - 1
                print('     '+team2+' win by '+str(diff)+' runs.')
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
                    print('{} {} to {}, {}, {}'.format(ball,bowlerPresent,batsman1,*ballOutcome,random.choice(outComm)))
                elif ballOutcome == ['Wide']:
                    print('{} {} to {},{}, {}'.format(ball,bowlerPresent,batsman1,*ballOutcome,'Thats a wide ball from '+bowlerPresent))
                elif ballOutcome == [1]:
                    print('{} {} to {}, one {}, {}'.format(ball,bowlerPresent,batsman1,'run',random.choice(oneComm)))
                elif ballOutcome == [2]:
                    print('{} {} to {}, two {}, {}'.format(ball,bowlerPresent,batsman1,'runs',random.choice(twoComm)))
                elif ballOutcome == [3]:
                    print('{} {} to {}, three {}, {}'.format(ball,bowlerPresent,batsman1,'runs',random.choice(threeComm)))
                elif ballOutcome == [4]:
                    print('{} {} to {}, FOUR {}, {}'.format(ball,bowlerPresent,batsman1,'runs',random.choice(fourComm)))
                elif ballOutcome == [6]:
                    print('{} {} to {}, SIX ! {}, {}'.format(ball,bowlerPresent,batsman1,'runs',random.choice(sixComm)))
                elif ballOutcome == [0]:
                    print('{} {} to {}, dot {}, {}'.format(ball,bowlerPresent,batsman1,'',random.choice(zeroComm)))
            
                #Checking for winner after every ball
                if totalScore >= target:
                    sr1 = initialStrikerRuns * 100 // initialStrikerBallsCount
                    sr2 = intialNonStrikerRuns * 100 // initialNonStrikerBallsCount
                    batsmenScoreboard2.append([batsman1, "Not Out", initialStrikerRuns, initialStrikerBallsCount, 
                   initialStrikeFour, initialStrikeSix, sr1])
                    batsmenScoreboard2.append([batsman2, "Not Out", intialNonStrikerRuns, initialNonStrikerBallsCount, 
                   initialNonStrikeFour, initialNonStrikeSix, sr2])
                    print()
                    print('     {}     {}-{}-{}-{}'.format(bowlerPresent,'10',initialDotBalls,initialScore,initialOut))
                    print()
                    print('     END of '+str(count)+' balls ('+str(initialScore)+' runs)')
                    print('     '+team1+'     '+str(totalScore)+'/'+str(totalWickets))
                    rr = totalScore / (count / 10)
                    print('     RR: {:.2f}'.format(rr))
                    print()
                    wicketsDiffer = 10 - totalWickets
                    print('     '+team1+' win by '+str(wicketsDiffer)+' wickets.')
                    break
            
                # print('{} {} to {} : {} runs'.format(ball,bowlerPresent,batsman1,*ballOutcome))
                if totalWickets == 10:
                    sr2 = intialNonStrikerRuns * 100 // initialNonStrikerBallsCount
                    batsmenScoreboard2.append([batsman2, "Not Out", intialNonStrikerRuns, initialNonStrikerBallsCount, 
                   initialNonStrikeFour, initialNonStrikeSix, sr2])
                    print()
                    print('     {}     {}-{}-{}-{}'.format(bowlerPresent,'10',initialDotBalls,initialScore,initialOut))
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
                    print('{} {} to {}, {}, {}'.format(ball,bowlerPresent,batsman1,*ballOutcome,random.choice(outComm)))
                elif ballOutcome == ['Wide']:
                    print('{} {} to {},{}, {}'.format(ball,bowlerPresent,batsman1,*ballOutcome,'Thats a wide ball from '+bowlerPresent))
                elif ballOutcome == [1]:
                    print('{} {} to {}, one {}, {}'.format(ball,bowlerPresent,batsman1,'run',random.choice(oneComm)))
                elif ballOutcome == [2]:
                    print('{} {} to {}, two {}, {}'.format(ball,bowlerPresent,batsman1,'runs',random.choice(twoComm)))
                elif ballOutcome == [3]:
                    print('{} {} to {}, three {}, {}'.format(ball,bowlerPresent,batsman1,'runs',random.choice(threeComm)))
                elif ballOutcome == [4]:
                    print('{} {} to {}, FOUR {}, {}'.format(ball,bowlerPresent,batsman1,'runs',random.choice(fourComm)))
                elif ballOutcome == [6]:
                    print('{} {} to {}, SIX ! {}, {}'.format(ball,bowlerPresent,batsman1,'runs',random.choice(sixComm)))
                elif ballOutcome == [0]:
                    print('{} {} to {}, dot {}, {}'.format(ball,bowlerPresent,batsman1,'',random.choice(zeroComm)))
                
                #Checking for winner after every ball
                if totalScore >= target:
                    sr1 = initialStrikerRuns * 100 // initialStrikerBallsCount
                    sr2 = intialNonStrikerRuns * 100 // initialNonStrikerBallsCount
                    batsmenScoreboard2.append([batsman1, "Not Out", initialStrikerRuns, initialStrikerBallsCount, 
                   initialStrikeFour, initialStrikeSix, sr1])
                    batsmenScoreboard2.append([batsman2, "Not Out", intialNonStrikerRuns, initialNonStrikerBallsCount, 
                   initialNonStrikeFour, initialNonStrikeSix, sr2])
                    print()
                    print('     {}     {}-{}-{}-{}'.format(bowlerPresent,'10',initialDotBalls,initialScore,initialOut))
                    print()
                    print('     END of '+str(count)+' balls ('+str(initialScore)+' runs)')
                    print('     '+team1+'     '+str(totalScore)+'/'+str(totalWickets))
                    rr = totalScore / (count / 10)
                    print('     RR: {:.2f}'.format(rr))
                    print()
                    wicketsDiffer = 10 - totalWickets
                    print('     '+team1+' win by '+str(wicketsDiffer)+' wickets.')
                    break
                
                # print('{} {} to {} : {} runs'.format(ball,bowlerPresent,batsman1,*ballOutcome))
                if totalWickets == 10:
                    sr2 = intialNonStrikerRuns * 100 // initialNonStrikerBallsCount
                    batsmenScoreboard2.append([batsman2, "Not Out", intialNonStrikerRuns, initialNonStrikerBallsCount, 
                   initialNonStrikeFour, initialNonStrikeSix, sr2])
                    print()
                    print('     {}     {}-{}-{}-{}'.format(bowlerPresent,'10',initialDotBalls,initialScore,initialOut))
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
            print('     RR: {:.2f}'.format(rr))
            print()
            # print('     {}     {}-{}-{}-{}'.format(bowlerPresent,'10',initialDotBalls,initialScore,initialOut))
            # print()
            
            
            
            #Checking for winner after every ball
            if count == 100:
                print()
                print('     End of innings (Balls '+str(count)+')')
                rr = totalScore / (count / 10)
                print('     '+team1+str(totalScore)+'/'+str(totalWickets)+'  (RR: {:.2f})'.format(rr))
                if totalScore < target:
                    if initialStrikerBallsCount == 0:
                        sr1 = 0
                    else:
                        sr1 = initialStrikerRuns * 100 // initialStrikerBallsCount
                    sr2 = intialNonStrikerRuns * 100 // initialNonStrikerBallsCount
                    
                    batsmenScoreboard2.append([batsman1, "Not Out", initialStrikerRuns, initialStrikerBallsCount, 
                   initialStrikeFour, initialStrikeSix, sr1])
                    batsmenScoreboard2.append([batsman2, "Not Out", intialNonStrikerRuns, initialNonStrikerBallsCount, 
                   initialNonStrikeFour, initialNonStrikeSix, sr2])
                    print()
                    print('     {}     {}-{}-{}-{}'.format(bowlerPresent,'10',initialDotBalls,initialScore,initialOut))
                    print()
                    diff = target - totalScore
                    print(team2+' win by '+str(diff)+' runs.')
                    break
            elif count == 100:
                if totalScore >= target:
                    sr1 = initialStrikerRuns * 100 // initialStrikerBallsCount
                    sr2 = intialNonStrikerRuns * 100 // initialNonStrikerBallsCount
                    batsmenScoreboard2.append([batsman1, "Not Out", initialStrikerRuns, initialStrikerBallsCount, 
                   initialStrikeFour, initialStrikeSix, sr1])
                    batsmenScoreboard2.append([batsman2, "Not Out", intialNonStrikerRuns, initialNonStrikerBallsCount, 
                   initialNonStrikeFour, initialNonStrikeSix, sr2])
                    print()
                    print('     {}     {}-{}-{}-{}'.format(bowlerPresent,'10',initialDotBalls,initialScore,initialOut))
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
            
            #Reseting over score before the begini of new over.
            initialScore = 0
            initialOut = 0
            #Change of bowler
            bowlerPresent = pickBowler() #bowler
            
            # bowler = random.choice(bowlingPlayers)
            # bowlerPresent = bowler
            
            initialDotBalls = 0
        
        #If out bring in next batsmen
        if ballOutcome == ['OUT']:
            sr = initialStrikerRuns * 100 // initialStrikerBallsCount
            batsmenScoreboard2.append([batsman1, bowlerPresent, initialStrikerRuns, initialStrikerBallsCount, 
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
    
    
    if count == 100:
        if totalWickets != 10:
            sr1 = initialStrikerRuns * 100 // initialStrikerBallsCount
            sr2 = intialNonStrikerRuns * 100 // initialNonStrikerBallsCount
            batsmenScoreboard2.append([batsman1, "Not Out", initialStrikerRuns, initialStrikerBallsCount, 
           initialStrikeFour, initialStrikeSix, sr1])
            batsmenScoreboard2.append([batsman2, "Not Out", intialNonStrikerRuns, initialNonStrikerBallsCount, 
           initialNonStrikeFour, initialNonStrikeSix, sr2])
        if totalWickets == 10:
            sr2 = intialNonStrikerRuns * 100 // initialNonStrikerBallsCount
            batsmenScoreboard2.append([batsman2, "Not Out", intialNonStrikerRuns, initialNonStrikerBallsCount, 
           initialNonStrikeFour, initialNonStrikeSix, sr2])
    print()
    
    
    print('2nd Innings Scoreboard')
    batsmenScoreboardTwo = pd.DataFrame(batsmenScoreboard2, columns =['Batsman','Bowler','Runs','Balls','4s','6s','SR'])
    print(batsmenScoreboardTwo)
    


def prepInnings(team1, team2):
    
    battingTeam1 = pd.read_csv(team1+'.csv')
    bowlingTeam1 = pd.read_csv(team2+'.csv')
    
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
        
    print(team1+' - ',battingPlayerNames)
    print(team2+' - ',bowlingPlayers)
    print()
    
    
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
    
    inng1InningsBatting = {}
    inng2InningsBowling = {}
    
    def pickBowler():
        bowler = random.choice(bowlingPlayers)
        return bowler
    
    b = 0
    playerOut = 0
    bowlerPresent = pickBowler()
    batsman1 = battingPlayerNames[b]
    batsman2 = battingPlayerNames[b+1]
    batsman1Rating = battingPlayerRatings[b]
    batsman2Rating = battingPlayerRatings[b+1]
    
    print('%%%%%  First Innings  %%%%%')
    print()
    
    for i in range(1,101):
        # time.sleep(gameRate)
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
            print('{} {} to {}, {}, {}'.format(ball,bowlerPresent,batsman1,*ballOutcome,random.choice(outComm)))
        elif ballOutcome == ['Wide']:
            print('{} {} to {},{}, {}'.format(ball,bowlerPresent,batsman1,*ballOutcome,'Thats a wide ball from '+bowlerPresent))
        elif ballOutcome == [1]:
            print('{} {} to {}, one {}, {}'.format(ball,bowlerPresent,batsman1,'run',random.choice(oneComm)))
        elif ballOutcome == [2]:
            print('{} {} to {}, two {}, {}'.format(ball,bowlerPresent,batsman1,'runs',random.choice(twoComm)))
        elif ballOutcome == [3]:
            print('{} {} to {}, three {}, {}'.format(ball,bowlerPresent,batsman1,'runs',random.choice(threeComm)))
        elif ballOutcome == [4]:
            print('{} {} to {}, FOUR {}, {}'.format(ball,bowlerPresent,batsman1,'runs',random.choice(fourComm)))
        elif ballOutcome == [6]:
            print('{} {} to {}, SIX ! {}, {}'.format(ball,bowlerPresent,batsman1,'runs',random.choice(sixComm)))
        elif ballOutcome == [0]:
            print('{} {} to {}, dot {}, {}'.format(ball,bowlerPresent,batsman1,'',random.choice(zeroComm)))
            
        count = count + 1
        if totalWickets == 10:
            print()
            print('     {}     {}-{}-{}-{}'.format(bowlerPresent,'10',initialDotBalls,initialScore,initialOut))
            print()
            print('     End of innings (Balls '+str(count)+')')
            rr = totalScore / (count / 10)
            print('     '+team1+'     '+str(totalScore)+'/'+str(totalWickets)+'  (RR: {:.2f})'.format(rr))
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
                    print('{} {} to {}, {}, {}'.format(ball,bowlerPresent,batsman1,*ballOutcome,random.choice(outComm)))
                elif ballOutcome == ['Wide']:
                    print('{} {} to {},{}, {}'.format(ball,bowlerPresent,batsman1,*ballOutcome,'Thats a wide ball from '+bowlerPresent))
                elif ballOutcome == [1]:
                    print('{} {} to {}, one {}, {}'.format(ball,bowlerPresent,batsman1,'run',random.choice(oneComm)))
                elif ballOutcome == [2]:
                    print('{} {} to {}, two {}, {}'.format(ball,bowlerPresent,batsman1,'runs',random.choice(twoComm)))
                elif ballOutcome == [3]:
                    print('{} {} to {}, three {}, {}'.format(ball,bowlerPresent,batsman1,'runs',random.choice(threeComm)))
                elif ballOutcome == [4]:
                    print('{} {} to {}, FOUR {}, {}'.format(ball,bowlerPresent,batsman1,'runs',random.choice(fourComm)))
                elif ballOutcome == [6]:
                    print('{} {} to {}, SIX ! {}, {}'.format(ball,bowlerPresent,batsman1,'runs',random.choice(sixComm)))
                elif ballOutcome == [0]:
                    print('{} {} to {}, dot {}, {}'.format(ball,bowlerPresent,batsman1,'',random.choice(zeroComm)))
            
                # print('{} {} to {} : {} runs'.format(ball,bowlerPresent,batsman1,*ballOutcome))
                if totalWickets == 10:
                    print()
                    print('     {}     {}-{}-{}-{}'.format(bowlerPresent,'10',initialDotBalls,initialScore,initialOut))
                    print()
                    print('     End of innings (Balls '+str(count)+')')
                    rr = totalScore / (count / 10)
                    print('     '+team1+'     '+str(totalScore)+'/'+str(totalWickets)+'  (RR: {:.2f})'.format(rr))
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
                    initialDotBalls =  initialDotBalls + 1
                elif ballOutcome == [0]:
                     initialDotBalls = initialDotBalls + 1
                else:
                    pass
                
                if ballOutcome == ['OUT']:
                    print('{} {} to {}, {}, {}'.format(ball,bowlerPresent,batsman1,*ballOutcome,random.choice(outComm)))
                elif ballOutcome == ['Wide']:
                    print('{} {} to {},{}, {}'.format(ball,bowlerPresent,batsman1,*ballOutcome,'Thats a wide ball from '+bowlerPresent))
                elif ballOutcome == [1]:
                    print('{} {} to {}, one {}, {}'.format(ball,bowlerPresent,batsman1,'run',random.choice(oneComm)))
                elif ballOutcome == [2]:
                    print('{} {} to {}, two {}, {}'.format(ball,bowlerPresent,batsman1,'runs',random.choice(twoComm)))
                elif ballOutcome == [3]:
                    print('{} {} to {}, three {}, {}'.format(ball,bowlerPresent,batsman1,'runs',random.choice(threeComm)))
                elif ballOutcome == [4]:
                    print('{} {} to {}, FOUR {}, {}'.format(ball,bowlerPresent,batsman1,'runs',random.choice(fourComm)))
                elif ballOutcome == [6]:
                    print('{} {} to {}, SIX ! {}, {}'.format(ball,bowlerPresent,batsman1,'runs',random.choice(sixComm)))
                elif ballOutcome == [0]:
                    print('{} {} to {}, dot {}, {}'.format(ball,bowlerPresent,batsman1,'',random.choice(zeroComm)))
            
                # print('{} {} to {} : {} runs'.format(ball,bowlerPresent,batsman1,*ballOutcome))
                if totalWickets == 10:
                    print()
                    print('     {}     {}-{}-{}-{}'.format(bowlerPresent,'10',initialDotBalls,initialScore,initialOut))
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
        
        
        
        if count % 10 == 0:
            print('     {}     ({}){} [{}x4 {}x6]'.format(batsman1,initialStrikerRuns,initialStrikerBallsCount,initialStrikeFour, initialStrikeSix))
            print('     {}     ({}){} [{}x4 {}x6]'.format(batsman2,intialNonStrikerRuns,initialNonStrikerBallsCount, initialNonStrikeFour, initialNonStrikeSix))
            print('     {}     {}-{}-{}-{}'.format(bowlerPresent,'10',initialDotBalls,initialScore,initialOut))
            print()
            
            #Reseting over score before the begini of new over.
            initialScore = 0
            initialOut = 0
            #Change of bowler
            bowlerPresent = pickBowler() #bowler
            
            # bowler = random.choice(bowlingPlayers)
            # bowlerPresent = bowler
            
            initialDotBalls = 0
        
        #If out bring in next batsmen
        if ballOutcome == ['OUT']:
            sr = initialStrikerRuns * 100 // initialStrikerBallsCount
            batsmenScoreboard1.append([batsman1, bowlerPresent, initialStrikerRuns, initialStrikerBallsCount, 
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
    
    if count == 100:
        if totalWickets != 10:
            sr1 = initialStrikerRuns * 100 // initialStrikerBallsCount
            sr2 = intialNonStrikerRuns * 100 // initialNonStrikerBallsCount
            batsmenScoreboard1.append([batsman1, "Not Out", initialStrikerRuns, initialStrikerBallsCount, 
           initialStrikeFour, initialStrikeSix, sr1])
            batsmenScoreboard1.append([batsman2, "Not Out", intialNonStrikerRuns, initialNonStrikerBallsCount, 
           initialNonStrikeFour, initialNonStrikeSix, sr2])
        if totalWickets == 10:
            sr2 = intialNonStrikerRuns * 100 // initialNonStrikerBallsCount
            batsmenScoreboard1.append([batsman2, "Not Out", intialNonStrikerRuns, initialNonStrikerBallsCount, 
           initialNonStrikeFour, initialNonStrikeSix, sr2])
            
    print('1st Innings Scoreboard')
    batsmenScoreboardOne = pd.DataFrame(batsmenScoreboard1, columns =['Batsman','Bowler','Runs','Balls','4s','6s','SR'])
    print(batsmenScoreboardOne)
    print()
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
print('Team 1: ',team1)
print('Team 2: ',team2)
print()

#saving output to file opening
# stdoutOrigin = sys.stdout
# timestr = time.strftime("%Y%m%d-%H%M%S")
# filename = team1+' vs '+team2+'-'+timestr+'.txt' 
# sys.stdout = open(filename, "w")

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

    
