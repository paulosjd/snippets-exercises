# itertools.islice
# def islice(iterable, *args):
    # islice('ABCDEFG', 2) --> A B
    # islice('ABCDEFG', 2, 4) --> C D
    # islice('ABCDEFG', 2, None) --> C D E F G
    # islice('ABCDEFG', 0, None, 2) --> A C E G

def pascal(n):
    if n == 1:
        return [1]
    line = [1]
    previous_line = pascal(n - 1)
    inner = []
    if n > 3:
        inner = [previous_line[a] + previous_line[a + 1] for a in range(int(n / 2 - 1))]
        inner = inner + inner[::-1]
    for i in inner:
        line.append(i)
    if n % 2 != 0:
        ind = int(n / 2)
        line.insert(ind, previous_line[ind] + previous_line[ind - 1])
    line.append(1)
    return line

