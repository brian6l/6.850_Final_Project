# AVL tree implementation in Python


import sys

# Create a tree node
class TreeNode(object):
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.leftneighbor = None
        self.rightneighbor = None
        self.height = 1
    def parent(self):
        if self.leftneighbor and self.leftneighbor.right is self:
            return self.leftneighbor
        elif self.rightneighbor and self.rightneighbor.left is self:
            return self.rightneighbor
        else:
            return None
from math import inf
class LAVLTree(object):
    def __init__(self): 
        self.y = -inf

    def __str__(self, root):
        left_node = self.getMinValueNode(root)
        ans = ""
        while left_node:
            ans += str(left_node.key)
            ans += " "
            left_node = left_node.rightneighbor
        return ans
    # Function to insert a node
    def insert_node(self, root, key):

        # Find the correct location and insert the node
        if not root:
            return TreeNode(key)
        elif key < root.key:
            left = self.insert_node(root.left, key)
            if not root.left:
                left.rightneighbor, left.leftneighbor = root, root.leftneighbor
                if root.leftneighbor:
                    root.leftneighbor.rightneighbor = left
                root.leftneighbor = left
            root.left = left
        else:
            right = self.insert_node(root.right, key)
            if not root.right:
                right.leftneighbor, right.rightneighbor = root, root.rightneighbor
                if root.rightneighbor:
                    root.rightneighbor.leftneighbor = right
                root.rightneighbor = right
            root.right = right

        root.height = 1 + max(self.getHeight(root.left),
                              self.getHeight(root.right))

        # Update the balance factor and balance the tree
        balanceFactor = self.getBalance(root)
        if balanceFactor > 1:
            if key < root.left.key:
                return self.rightRotate(root)
            else:
                root.left = self.leftRotate(root.left)
                return self.rightRotate(root)

        if balanceFactor < -1:
            if key > root.right.key:
                return self.leftRotate(root)
            else:
                root.right = self.rightRotate(root.right)
                return self.leftRotate(root)

        return root

    # Function to delete a node
    def delete_node(self, root, key):

        # Find the node to be deleted and remove it
        if not root:
            return root
        elif key < root.key:
            root.left = self.delete_node(root.left, key)
        elif key > root.key:
            root.right = self.delete_node(root.right, key)
        else:
            if root.left is None:
                temp = root.right
            elif root.right is None:
                temp = root.left
            else:
                temp = self.getMinValueNode(root.right)
            if not root.left or not root.right:
                if root.rightneighbor:
                    if root.leftneighbor:
                        root.rightneighbor.leftneighbor = root.leftneighbor
                        root.leftneighbor.rightneighbor = root.rightneighbor
                    else:
                        root.rightneighbor.leftneighbor = None
                elif root.leftneighbor:
                    root.leftneighbor.rightneighbor = None
                return temp
            root.key = temp.key
            if root.rightneighbor:
                root.rightneighbor = root.rightneighbor.rightneighbor
            root.right = self.delete_node(root.right,
                                          temp.key)
        if root is None:
            return root

        # Update the balance factor of nodes
        root.height = 1 + max(self.getHeight(root.left),
                              self.getHeight(root.right))

        balanceFactor = self.getBalance(root)

        # Balance the tree
        if balanceFactor > 1:
            if self.getBalance(root.left) >= 0:
                return self.rightRotate(root)
            else:
                root.left = self.leftRotate(root.left)
                return self.rightRotate(root)
        if balanceFactor < -1:
            if self.getBalance(root.right) <= 0:
                return self.leftRotate(root)
            else:
                root.right = self.rightRotate(root.right)
                return self.leftRotate(root)
        return root

    # Function to perform left rotation
    def leftRotate(self, z):
        y = z.right
        T2 = y.left
        y.left = z
        z.right = T2
        z.height = 1 + max(self.getHeight(z.left),
                           self.getHeight(z.right))
        y.height = 1 + max(self.getHeight(y.left),
                           self.getHeight(y.right))
        return y

    # Function to perform right rotation
    def rightRotate(self, z):
        y = z.left
        T3 = y.right
        y.right = z
        z.left = T3
        z.height = 1 + max(self.getHeight(z.left),
                           self.getHeight(z.right))
        y.height = 1 + max(self.getHeight(y.left),
                           self.getHeight(y.right))
        return y

    # Get the height of the node
    def getHeight(self, root):
        if not root:
            return 0
        return root.height

    # Get balance factore of the node
    def getBalance(self, root):
        if not root:
            return 0
        return self.getHeight(root.left) - self.getHeight(root.right)

    def getMinValueNode(self, root):
        if root is None or root.left is None:
            return root
        return self.getMinValueNode(root.left)

    def preOrder(self, root):
        if not root:
            return
        print("{0} ".format(root.key), end="")
        self.preOrder(root.left)
        self.preOrder(root.right)

    # Print the tree
    def printHelper(self, currPtr, indent, last):
        if currPtr != None:
            sys.stdout.write(indent)
            if last:
                sys.stdout.write("R----")
                indent += "     "
            else:
                sys.stdout.write("L----")
                indent += "|    "
            print(currPtr.key)
            self.printHelper(currPtr.left, indent, False)
            self.printHelper(currPtr.right, indent, True)

myTree = LAVLTree()
root = None
nums = [i for i in range(10)]
for num in nums:
    root = myTree.insert_node(root, num)
myTree.printHelper(root, "", True)
print(myTree.__str__(root))
key = 13
root = myTree.delete_node(root, 3)
myTree.printHelper(root,"",True)
print(myTree.__str__(root))
root = myTree.delete_node(root, 4)
myTree.printHelper(root,"",True)
print(myTree.__str__(root))
root = myTree.delete_node(root, 6)
myTree.printHelper(root, "", True)
print(myTree.__str__(root))
root = myTree.insert_node(root, 6)
myTree.printHelper(root, "", True)
print(myTree.__str__(root))