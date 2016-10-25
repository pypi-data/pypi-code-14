import random
import math

random.seed()
K = 16

# what is the expectation of Ra wins Rb
def expected(ra, rb):
    return 1.0 / (1 + math.pow(10, float(rb - ra)/400))

# Ra' = Ra + K(Sa - Ea)
# Ra is A's score
# Rb is B's score
# Sa (win: 1, draw: 0.5, lose: 0)
def win(ra, rb):
    ra = ra + K * (1 - expected(ra, rb))
    return ra

def draw(ra, rb):
    ra = ra + K * (0.5 - expected(ra, rb))
    return ra

def lose(ra, rb):
    ra = ra + K * (0 - expected(ra, rb))
    return ra


def match(player1, player2):
    while True:
        r = input("Which one wins? (0: draw, 1: 1 wins, 2: 2 wins)\n1. %s\n2. %s\n[0/1/2]:" % (player1, player2))
        r = int(r)
        if r == 0:
            player1["score"] = draw(player1["score"], player2["score"])
            player2["score"] = draw(player2["score"], player1["score"])
            break
        elif r == 1:
            player1["score"] = win(player1["score"], player2["score"])
            player2["score"] = lose(player2["score"], player1["score"])
            break
        elif r == 2:
            player1["score"] = lose(player1["score"], player2["score"])
            player2["score"] = win(player2["score"], player1["score"])
            break
        else:
            print("Invalid answer: %s\n" % r)

def sort(items):
    length = len(items)
    n = length
    if n < 2:
        return items

    array = []
    for item in items:
        bucket = { "score": 0, "item": item }
        array.append(bucket)

    for i in range(n):
        player1 = random.choice(array)
        player2 = random.choice(array)
        while player1 == player2:
            player2 = random.choice(array)
        match(player1, player2)

    array = sorted(array, key=lambda x: x["score"], reverse=True)
    #print("elo sorted array: ", array)

    res = []
    for bucket in array:
        res.append(bucket["item"])

    return res

