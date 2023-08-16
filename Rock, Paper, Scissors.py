from random import choice

wins={'rock':'scissors','paper':'rock','scissors':'paper'}
u_score, c_score=0,0

print('Welcome to Rock, Paper, Scissors.')
repeat=int(input('# Rounds:  '))

for x in range(0, repeat):
    c_play=choice(['rock','paper','scissors'])
    
    u_play=None
    while not u_play in ['rock','paper','scissors']:
        u_play=input('Play:  ')
        
    print('Rock, paper, scissors, shoot!  Your play: %s.  Computer play: %s.' %(u_play,c_play))

    #Decides who wins the round, then adds to either the u(user) or c(computer) score
    if u_play==c_play:
        print('Tie round.')
    elif wins[u_play]==c_play:
        print('You win that round.')
        u_score+=1
    else:
        print('The computer wins that round.')
        c_score+=1

#Who won?
if u_score>c_score:
    print('\nYou win. The score is %s to %s.' %(u_score, c_score))
elif c_score>u_score:
    print('\nYou lose. The score is %s to %s.' %(c_score, u_score))
else:
    print('\nTie with a score of %s to %s!' %(u_score, c_score))