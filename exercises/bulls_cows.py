import random


def make_list(exclude=None):
    if exclude is None:
        exclude = []
    k = 0
    items = []
    while k < 4:
        r = random.randint(1, 9)
        if r not in items and r not in exclude:
            items.append(r)
            k += 1
    return items


class BullGetter():
    def __init__(self):
        self.current = make_list()
        self.bulls = {}  # a dict with index position as key and number 1-9 as the value
        self.avoid = []  # list of digits that are either asserted bulls or non-cows
        self.mem = [[self.current]]
        self.counts = []

    def __str__(self):
        return ''.join(str(a) for a in self.current)

    def pick_new(self):
        try:
            return random.choice([a for a in range(1, 9) if a not in self.avoid and a not in self.current])
        except IndexError:
            ind = [a for a in range(4) if a not in self.bulls.keys()]
            self.current[ind[0]], self.current[ind[1]] = self.current[ind[1]], self.current[ind[0]]

    @property
    def change(self):
        # to evaluate one digit changes, gives (a, b, c) where a is the index position, b is previous, c is new digit
        mem = self.mem[-1]
        new_dig = [a for a in self.current if a not in mem]
        if len(new_dig) == 1:
            ind = self.current.index(new_dig[0])
            return ind, mem[ind], new_dig[0]


bgt = BullGetter()


def evaluate(entry):
    if entry == [0, 0]:
        for a in bgt.current:
            bgt.avoid.append(a)
        bgt.current = make_list(bgt.avoid)
        bgt.mem.append(bgt.current)
        return
    try:
        if entry[0] < bgt.counts[-2][0]:  # if bulls -1
            bgt.bulls[bgt.change[0][0]] = bgt.change[0][1]
            bgt.avoid.append(bgt.change[0][1])
        elif entry[0] > bgt.counts[-2][0]:  # if bulls +1
            bgt.bulls[bgt.change[0][0]] = bgt.change[0][2]
            bgt.avoid.append(bgt.change[0][2])
        if entry[0] == bgt.counts[-2][0]:
            if entry[1] < bgt.counts[-2][1]:  # if cows -1
                bgt.avoid.append(bgt.change[0][2])
            elif entry[1] > bgt.counts[-2][1]:  # if cows +1
                bgt.avoid.append(bgt.change[0][1])
    except TypeError:
        pass


def make_choice():
    if bgt.bulls:
        ind = [a for a in range(4) if a not in bgt.bulls.keys()]
        bgt.current[random.choice(ind)] = bgt.pick_new()
    else:
        bgt.current[random.randint(0, 3)] = bgt.pick_new()
        bgt.mem.append(bgt.current)


n = 1
while True:
    print('Attempt #{}. My guess: {}'.format(n, bgt))
    user_input = input()
    if user_input == '' or user_input == '40':
        break
    entry = (int(user_input[0]), int(user_input[1]))
    bgt.counts.append((entry[0], entry[1]))
    evaluate(entry)
    make_choice()
    n += 1

if __name__ == '__main__':
    main()
