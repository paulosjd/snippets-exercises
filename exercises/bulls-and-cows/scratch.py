import random
import logging


def make_choice(exclude=None):
    if exclude is None:
        exclude = {}
    n = 0
    items = {}
    while n < 4:
        r = random.randint(1,9)
        if r not in items.values() and r not in exclude:
            items[n] = r
            n += 1
    return items

sec = make_choice()
sec


class BullGetter():
    def __init__(self, bc):
        self.current = [1, 2, 4, 8]  # make_list()
        # gets dicts with index position as key and number 1-9 as the value
        self.bulls = {}
        self.cows = {}

    def __str__(self):
        return ''.join(str(a) for a in self.current)

    def pick_new(self, avoid):
        return random.choice([a for a in range(1, 9) if a != avoid])