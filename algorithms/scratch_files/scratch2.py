class Node:
    def __init__(self,initdata):
        self.data = initdata
        self.next = None


class UnorderedList:

    def __init__(self):
        self.head = None

    # only the first node created (the end) has next set to None;
    def add(self, item):
        temp = Node(item)
        temp.next = self.head
        self.head = temp

    def search(self, item):
        current = self.head
        found = False
        while current is not None and not found:
            if current.data == item:
                found = True
            else:
                current = current.next
        return found

mylist = UnorderedList()

for i in [31, 77, 17, 93, 26]:
    mylist.add(i)

print(mylist.search(17))
