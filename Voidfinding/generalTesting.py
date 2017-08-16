import math as m
import random as r
import time as t

r.seed(t.ctime())

chips = 100
bet = 1
won = True
for i in range(1,200):
    print("betting on even. Chips:" + str(chips))
    if(bet > 100):
        bet = 100
    chips -= bet
    print("Betting " + str(bet) + " chips. Total Chips:" + str(chips))
    roll = r.randint(0,37)
    print("Rolling.. " + str(roll))
    if (roll == 0) or (roll == 37) or (roll%2 == 1):
        #0 and 00 + odds -> we loose!
        print("Lost! Chips:" + str(chips))
        if chips < 0:
            print("GAME OVER")
            break
        #double the bet!
        bet *= 2
    else:
        chips += (2*bet)
        print("Won! Chips:" + str(chips))
        bet = 1





