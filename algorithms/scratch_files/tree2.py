
class TreeThree:
    def __init__(self, obj, left=None, middle=None, right=None):
        self.key = obj
        self.left_child = left
        self.middle_child = middle
        self.right_child = right

    def insert(self, position, obj):
        child = getattr(self, position + '_child')
        if child is None:
            setattr(self, position + '_child', TreeThree(obj))
        else:
            new_node = TreeThree(obj, **{position: child})
            setattr(self, position + '_child', new_node)


bt = TreeThree('a')
bt.insert('left', 'b')
bt.insert('middle', 'c')
bt.insert('right', 'c')
bt.insert('left', 'l')
bt.insert('middle', 'm')
bt.insert('right', 'n')
bt.insert('left', 'p')



def inorder(tree):
    if tree is not None:
        print(tree.key)
        inorder(tree.left_child)
        inorder(tree.middle_child)
        inorder(tree.right_child)


def preorder(tree):
    if tree:
        print(tree.key)
        inorder(tree.left_child)
        inorder(tree.middle_child)

        inorder(tree.right_child)




print(inorder(bt))
print('\n')
print(preorder(bt))
