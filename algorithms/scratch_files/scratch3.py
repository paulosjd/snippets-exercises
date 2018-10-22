# def is_palindrome(word):
#     if word[0] != word[-1]:
#         return False
#     try:
#         return is_palindrome(word[1:-1])
#     except IndexError:
#         return True
#
# print(is_palindrome('bttaatb'))


class BinaryTree:
    def __init__(self, obj, left=None, right=None):
        self.key = obj
        self.left_child = left
        self.right_child = right

    def insert(self, position, obj):
        child = getattr(self, position + '_child')
        if child is None:
            setattr(self, position + '_child', BinaryTree(obj))
        else:
            new_node = BinaryTree(obj, **{position: child})
            setattr(self, position + '_child', new_node)


bt = BinaryTree('a')
bt.insert('left', 'b')
bt.insert('right', 'c')
bt.insert('left', 'd')



def inorder(tree):
    if tree is not None:
        inorder(tree.left_child)
        print(tree.key)
        inorder(tree.right_child)

def preorder(tree):
    if tree:
        print(tree.key)
        inorder(tree.left_child)
        inorder(tree.right_child)


bt = BinaryTree('a')
bt.insert('left', 'b')
bt.insert('right', 'c')
bt.insert('right', 'k')
bt.insert('left', 'd')

print(inorder(bt))
print('\n')
print(preorder(bt))
