import random

uns_cards = [5, 13, 47, 17, 53, 2, 7, 29, 41, 11, 23]
uns_cards2 = [5, 13, 47, 17, 53, 2, 7, 29, 41, 11, 23, 101 ]
uns_cards3 = [5, 13, 47, 17, 53, 2, 7, 29, 41, 11, 23, 101, 77]
uns_cards4 = [5, 13, 47, 17, 53, 2, 7, 29, 41, 11, 23, 101, 77, 99, 222, 344, 232, 122, 122, 111, 122, 145, 234, 544, 343, 23, 2, 43]

class CardSort:
    """ simulate a human strategy to list of number cards, i.e. no sort or min/max methods """
    def __init__(self, unsorted):
        self.unsorted = unsorted
        self.sorted1 = []
        self.sorted2 = []
        self.min_ind = None
        self.min_val = None
        self.max_ind = None
        self.max_val = None
        self.total_checks = 0
        self._initial = True
        self._first = True
        self.unsorted_len = 2

    def check_min_max(self, index, value):
        # get a count of the unordered list
        if self._initial and index + 1 > self.unsorted_len:
            self.unsorted_len = index + 1
        if self._first:
            self.min_val, self.max_val = value, value
        if value <= self.min_val:
            self.min_ind, self.min_val = index, value
        if value >= self.max_val:
            self.max_ind, self.max_val = index, value

    def loop_over_unsorted(self):
        self._first = True
        for i, num in enumerate(self.unsorted):
            self.check_min_max(i, num)
            self._first = False
            self.total_checks += 1
        self._initial = False
        unsort_min = self.unsorted.pop(self.min_ind)
        if self.max_ind > self.min_ind:
            self.max_ind -= 1
        unsort_max = self.unsorted.pop(self.max_ind)
        self.sorted1.append(unsort_min)
        self.sorted2.insert(0, unsort_max)
        self.unsorted_len -= 2

    def run(self):
        while self.unsorted_len > 1:
            self.loop_over_unsorted()
        if self.unsorted:
            self.sorted1.append(self.unsorted[0])
        return 'Sorted list: {} \nTotal cards checked: {} \nn = {}'.format(
            self.sorted1 + self.sorted2, self.total_checks, len(self.sorted1 + self.sorted2))


c = CardSort(uns_cards)
print(c.run())
c2 = CardSort(uns_cards2)
print(c2.run())
c = CardSort(uns_cards3)
print(c.run())
c = CardSort(uns_cards4)
print(c.run())
