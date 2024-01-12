import random

deck = list(range(60))
random.shuffle(deck)
discard = []

p1 = [deck.pop(-1) for _ in range(10)]
p2 = [deck.pop(-1) for _ in range(10)]

ok=[(i,card) for i, card in enumerate(p2) if i == card//6]
gaps = []

def display(player):
    for i in range(9,-1,-1):
        value = player[i]
        print(f' {i}|    {value} '+'.'*(value//3) if value < 10 else f' {i}|    {value}'+'.'*(value//3))

def p1_turn():
    display(p1)
    if discard:
        seen = discard[-1]
        card = seen if input(f'{seen} or deck?  ')==str(seen) else deck.pop(-1)
    else:
        card = deck.pop(-1)

    place = input(f'placement of {card}:  ')
    
    if place.isdigit(): #otherwise just discard
        place = int(place)
        discard.append(p1[place])
        p1[place] = card
    else:
        discard.append(card)
        
    print()
          
def define_gaps(ok):
    gaps = []
    if ok:
        for i, pair in enumerate(ok[:-1]):
            indexes = range(pair[0]+1,ok[i+1][0])
            values  = range(pair[1]+1,ok[i+1][1])
            if len(indexes) > 0:
                gaps.append((indexes,values))
        #first gap 
        if ok[0][0] > 0:
            gaps.append((range(0, ok[0][0]), range(0, ok[0][1])))
        #last gap
        if ok[-1][0] < 9:
            gaps.append((range(ok[-1][0] +1, 10), range(ok[-1][1] +1, 60)))
    else:
        gaps.append((range(10),range(60)))
                                                
    return gaps

def get_gap(card, gaps):
    for i, pair in enumerate(gaps):
        if card in pair[1]:
            return pair
    return False

def p2_turn(ok):
    ok.sort(key = lambda x : x[0])
    gaps = define_gaps(ok)
    
    seen = discard[-1]
    gap = get_gap(seen, gaps)
    if gap:
        card = seen
    else:
        card = deck.pop(-1)
        gap = get_gap(card, gaps)

    if gap:
        # the lens act as if we are starting at zero, then the index of the start is added at the end
        relative_num = card - gap[1][0]
        spacing = len(gap[1])/len(gap[0])
        place = int(relative_num//spacing + gap[0][0])
        discard.append(p2[place])
        p2[place] = card
        ok.append((place, card))
    else:
        #for now
        discard.append(card)    
            
    print('computer')
    display(p2)
    print()
 
while True:
    p1_turn()
    if p1 == sorted(p1):
        break
    p2_turn(ok)
    if p2 == sorted(p2):
        break
