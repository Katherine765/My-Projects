import random

def create_code():
    random.shuffle(colors)
    return colors[:4]

def guess_valid(guess):
    if len(guess) != 4:
        return False
    for x in range(4):
        if not guess[x] in colors:
            return False
    return True

def main():
    code = create_code()
    print(code)

    tries = 0
    while True:
        tries += 1
        guess = 'put random stuff here'
        while not guess_valid(guess):
            guess = list(input('Guess:  ').upper())

        cpos, ipos = 0, 0
        for i in range(4):
            if guess[i] == code[i]:
                cpos += 1
            elif guess[i] in code:
                ipos += 1
                
        if cpos == 4:
            break
        else:
            print(f'Correct spot: {cpos}')
            print(f'Incorrect spot: {ipos}')
            print()

    print(f'Win in {tries} tries!\n')


main()
