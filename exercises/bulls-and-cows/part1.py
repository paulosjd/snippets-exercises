
guess = '3254'

def bc_count(secret, gs):
    """ expects secret as a list of four ints, guess as a four digit string """
    bulls = 0
    cows = 0
    ges = [int(a) for a in gs]
    for a in ges:
        if a in secret:
            cows += 1
        if a == secret[ges.index(a)]:
            bulls += 1
            cows -= 1
    return bulls, cows

def player_turn():
    return '{} => bulls {}, cows {}'.format(guess, *bc_count(sec, guess))

player_turn()