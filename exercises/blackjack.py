import random

card_labels = ['Ace'] + [str(i) for i in range(2, 11)] + ['Jack', 'Queen', 'King']
suits = ['Hearts', 'Diamonds', 'Spades', 'Clubs']
cards = [[a, b] for a in card_labels for b in suits]


def get_card_value(hand_values):
    card_values = ['11'] + [str(i) for i in range(2, 11)] + ['10'] * 3
    return [int(card_values[card_labels.index(a)]) for a in hand_values]


class Player:
    def __init__(self, role):
        self.role = role
        self.hand = [random.choice(cards)] + [random.choice(cards)]
        self.card_values = get_card_value([a[0] for a in self.hand])
        self.score = sum(self.card_values)
        self.bust = False

    def __str__(self):
        return str(['{} of {}'.format(a[0], a[1]) for a in self.hand])


def take_or_stick(player):
    if player.score < 16:
        print("Hit enter to take a card")
        input('> ')
        return ''
    else:
        print("Hit enter to take a card or type 'S' to stick")
        move = input('> ')
        return move.upper()


def receive_card(player):
    player.hand += [random.choice(cards)]
    player.score = sum(get_card_value([a[0] for a in player.hand]))
    if player is gambler:
        print('Your cards: {}'.format(player))
    if bust(player):
        return True
    elif player is dealer:
        return


def bust(player):
    if player.score <= 21:
        return False
    if 'Ace' in [a[0] for a in player.hand] and player.score - 10 <= 21:
        return False
    if player.role == 'dealer':
        print("Dealer's hand: {}".format(dealer))
        print('Dealer Bust! You win')
        print('\n' * 2)
        return True
    else:
        print('Bust! You lose')
        print('\n' * 2)
        return True


print('Lets play Blackjack!')

while True:
    gambler = Player(role='player')
    dealer = Player(role='dealer')
    print("Hit enter to get your cards or enter 'quit' to exit")
    choice = input("> ")
    if choice.upper() == 'QUIT':
        break
    print('Your cards: {}'.format(gambler))
    print("Dealer's hand: {}".format(dealer.hand[0]))
    while take_or_stick(gambler) != 'S':
        if receive_card(gambler):
            gambler.bust = True
            break
        else:
            continue
    if gambler.bust is False:
        while dealer.bust is False:
            if dealer.score >= 16 and dealer.score >= gambler.score or gambler.bust:
                if not gambler.bust:
                    print("Dealer's hand: {}".format(dealer))
                print('Dealer wins')
                print('\n' * 2)
                break
            else:
                print("Hit enter")
                input('> ')
                if receive_card(dealer) is True:
                    break
                else:
                    print("Dealer's hand: {}".format(dealer))
                    continue
print('Thanks for playing')

"""
Suggested improvements:

* Create a class for the deck of cards and move functions inside classes

1) Enable the ability to save the number of wins/losses, cash in hand or top scores to a file. Add a name attribute to
   Player along with e.g. win/loss record and save and load the object using the pickle module. A context manager should
   be invoked through a 'with statement' containing the file object passed into the open() function. The open() function
   returns a file object having the __enter__ and __exit__ methods and the context manager will then open the file and
   automatically close the file.

2) Write unit tests. Check that the Person model is instantiated with the correct data. Test the functions which depend
   on data state of arguments (the Player model instances) with a setUp method similar to as follows:

    class PlayerMovesTest(TestCase):
        def setUp(self):
            self.player = Player(.....)

3) Refactoring. Once the application works satisfactorily, restructure and rewrite the code to make it more obvious to a
   new reader. Use docstrings for class/method/function definitions so that calling help() on it will
   return the docstring explaining any details. Refactoring should also be considered with regards to making the code
   easier to test, to make it more 'DRY', and make it more robust in relation to unexpected actions or conditions.
"""