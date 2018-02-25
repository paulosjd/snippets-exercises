import random


def make_list(exclude=None):
    if exclude is None:
        exclude = []
    k = 0
    items = []
    while k < 4:
        r = random.randint(1,9)
        if r not in items and r not in exclude:
            items.append(r)
            k += 1
    return items


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


def player_turn(secret, guess):
    return '{} => bulls {}, cows {}'.format(guess, *bc_count(secret, guess))

#player_turn(make_list(), '2315')


class BullTracker():
    def __init__(self):
        self.current = make_list()
        self.digits = list(range(1, 10))
        self.bulls = {}
        self.mem = [self.current[:]]
        self.counts = []

    @property
    def single_change(self):
        """ returns (a, b, c) where a is index position of the digit, b is previous digit, c is the new digit """
        mem = self.mem[-2]
        new_digits = [a for a in self.current if a not in self.mem[-2]]
        if len(new_digits) == 1:
            ind = self.current.index(new_digits[0])
            return ind, mem[ind], new_digits[0]

    @property
    def non_bull_indexes(self):
        return [a for a in range(4) if a not in self.bulls.keys()]

    def __str__(self):
        return ''.join(str(a) for a in self.current)

    def pick_new(self):
        try:
            self.current[random.choice(self.non_bull_indexes)] = random.choice(
                [a for a in self.digits if a not in self.current])
        except IndexError:
            self.shuffle()

    def exclude(self, digit):
        self.digits = [a for a in self.digits if a is not digit]

    def shuffle(self):
        while True:
            ind1, ind2 = random.sample(self.non_bull_indexes, 2)
            self.current[ind1], self.current[ind2] = self.current[ind2], self.current[ind1]
            if self.current not in self.mem:
                break

    def check_entry(self, entry):
        if entry == (0, 0):
            for a in self.current:
                self.digits.remove(a)
            self.current = make_list(exclude=self.current)
            return
        if entry == (1,3) or entry == (2, 2):
            self.digits = self.current
        if len(self.counts) > 2:
            new = {self.current.index(a): a for a in self.current if a != self.mem[-2][self.current.index(a)]}
            if self.counts[-1][0] - self.counts[-2][0] == 2 and len(new) == 2:
                self.bulls.update(new)

tracker = BullTracker()


def eval_single_change(entry):
    change = tracker.single_change
    if entry[0] < tracker.counts[-2][0]:  # if bulls -1
        tracker.bulls[change[0]] = change[1]
    elif entry[0] > tracker.counts[-2][0]:  # if bulls +1
        tracker.bulls[change[0]] = change[2]
        if entry[1] > tracker.counts[-2][1]:  # if cows -1
            tracker.exclude(change[1])
    else:  # if bulls no change
        if entry[1] < tracker.counts[-2][1]:  # if cows -1
            tracker.exclude(change[2])
        elif entry[1] > tracker.counts[-2][1]:  # if cows +1
            tracker.exclude(change[1])
            
def run():
    n = 0
    while True:
        n += 1
        print('Attempt #{}. My guess: {}'.format(n, tracker))
        user_input = input('Bulls and cows: ')
        if user_input == '' or user_input == '40':
            break
        try:
            entry = (int(user_input[0]), int(user_input[1]))
        except ValueError:
            # flask flash with error?
            continue
        tracker.counts.append((entry[0], entry[1]))
        tracker.mem.append(tracker.current[:])
        if tracker.check_entry(entry):
            continue
        if tracker.single_change:
            eval_single_change(entry)
        for k, v in tracker.bulls.items():
            tracker.current[k] = v
        if entry == (2, 2) and len(tracker.bulls) >= 2:
            tracker.shuffle()
            continue
        tracker.pick_new()

run()