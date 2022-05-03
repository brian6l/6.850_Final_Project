from avl import AVLTree
from math import inf, sqrt
from heapq import heappush, heappop
class Point(object): 
    def __init__(self, x, y): 
        self.x = x
        self.y = y
    def __eq__(self, point): 
        return self.x==point.x and self.y==point.y
class TreeNode(object):
    def __init__(self, point):
        self.point = point
        self.left = None
        self.right = None
        self.height = 1
        self.lneighbor = None
        self.rneighbor = None
        self.leftx = -inf
        self.rightx = inf
        self.directrix = -inf
    def __eq__(self, node): 
        return self.point==node.point and self.leftx==node.leftx and self.rightx==node.rightx
    def __lt__(self, point): 
        # returns self<point, ie point going straight up is to the right of parabola
        if(self.rightx<point.x): 
            return True
        if(self.leftx>=point.x): 
            return False
        parabola1coeffs = [1/(2*(self.point.y-self.directrix)), -1/((self.point.y-self.directrix))*self.point.x, 1/(2*(self.point.y-self.directrix))*self.point.x**2+(self.point.y+self.directrix)//2]
        if self.rneighbor: 
            focusr = self.rneighbor.point
            parabolarcoeffs = [1/(2*(focusr.y-self.directrix)), -1/((focusr.y-self.directrix))*focusr.x, 1/(2*(focusr.y-self.directrix))*focusr.x**2+(focusr.y+self.directrix)//2]
            a, b, c = tuple(parabola1coeffs[i]-parabolarcoeffs[i] for i in range(3))
            if(a==0): 
                rightx = -c/b
            else: 
                u = (-b+sqrt(b*b-4*a*c))/(2*a)
                v = (-b-sqrt(b*b-4*a*c))/(2*a)
                if(self.leftx<=u<=self.rightx and self.rneighbor.leftx<=u<=self.rneighbor.rightx): 
                    rightx = u
                else: 
                    rightx = v
        else: 
            rightx = inf
        return rightx<point.x
    def __gt__(self, point): 
        if(self.leftx>point.x): 
            return True
        if(self.rightx<=point.x): 
            return False
        parabola1coeffs = [1/(2*(self.point.y-self.directrix)), -1/((self.point.y-self.directrix))*self.point.x, 1/(2*(self.point.y-self.directrix))*self.point.x**2+(self.point.y+self.directrix)//2]
        if self.lneighbor: 
            focusl = self.lneighbor.point
            parabolalcoeffs = [1/(2*(focusl.y-self.directrix)), -1/((focusl.y-self.directrix))*focusl.x, 1/(2*(focusl.y-self.directrix))*focusl.x**2+(focusl.y+self.directrix)//2]
            a, b, c = tuple(parabola1coeffs[i]-parabolalcoeffs[i] for i in range(3))
            if(a==0): 
                leftx = -c/b
            else: 
                u = (-b+sqrt(b*b-4*a*c))/(2*a)
                v = (-b-sqrt(b*b-4*a*c))/(2*a)
                if(self.leftx<=u<=self.rightx and self.rneighbor.leftx<=u<=self.rneighbor.rightx): 
                    leftx = u
                else: 
                    leftx = v
        else: 
            leftx = -inf
        return leftx>point.x
class Event(object): 
    def __init__(self, node, point, directrix, isinsertion): 
        self.node = node
        self.point = point
        self.directrix = directrix
        self.isinsertion = isinsertion
class Beachline(object): 
    def __init__(self): 
        self.y = -inf
    def find_node(self, root, event): 
        root.directrix = event.directrix
        # Find the node to be deleted and remove it
        if not root:
            return root
        elif(event.node==root): 
            return root
        elif(root.lneighbor and event.node==root.lneighbor): 
            return root.lneighbor
        elif(root.rneighbor and event.node==root.rneighbor): 
            return root.rneighbor
        elif root > event.point:
            return self.find_node(root.left, event)
        elif root < event.point:
            return self.find_node(root.right, event)
        else:
            return None
    def insert_right_node(self, root, node): 
        if(not root): 
            return node
        root.right = self.insert_right_node(root.right, node)
        root.height = 1 + max(self.getHeight(root.left),
                              self.getHeight(root.right))

        # Update the balance factor and balance the tree
        balanceFactor = self.getBalance(root)
        if balanceFactor < -1:
            return self.leftRotate(root)

        return root
    def insert_left_node(self, root, node): 
        if(not root): 
            return node
        root.left = self.insert_right_node(root.left, node)
        root.height = 1 + max(self.getHeight(root.left),
                              self.getHeight(root.right))

        # Update the balance factor and balance the tree
        balanceFactor = self.getBalance(root)
        if balanceFactor > 1:
            return self.rightRotate(root)

        return root

    def insert_node(self, root, point):

        # Find the correct location and insert the node
        root.directrix = point.y
        if not root:
            return TreeNode(point)
        elif root>point:
            root.left = self.insert_node(root.left, point)
        elif root<point:
            root.right = self.insert_node(root.right, point)
        else: 
            lroot = TreeNode(root.point)
            if root.lneighbor: 
                root.lneighbor.rneighbor = lroot
                lroot.lneighbor = root.lneighbor
            lroot.leftx = root.leftx
            lroot.rightx = point.x            
            rroot = TreeNode(root.point)
            if root.rneighbor: 
                root.rneighbor.lneighbor = rroot
                rroot.rneighbor = root.rneighbor
            rroot.leftx = point.x
            rroot.rightx = root.rightx
            root.point = point
            root.lneighbor = lroot  
            root.rneighbor = rroot
            root.left = self.insert_right_node(lroot)
            root.right = self.insert_left_node(rroot)
        root.height = 1 + max(self.getHeight(root.left),
                              self.getHeight(root.right))

        # Update the balance factor and balance the tree
        balanceFactor = self.getBalance(root)
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
    
    # Function to delete a node
    def delete_node(self, root, event):
        root.directrix = event.directrix
        # Find the node to be deleted and remove it
        if not root:
            return root
        elif(event.node==root.node): 
            if root.lneighbor: 
                root.lneighbor.rneighbor = root.rneighbor
            if root.rneighbor: 
                root.rneighbor.lneighbor = root.lneighbor
            if root.left is None:
                temp = root.right
                root = None
                return temp
            elif root.right is None:
                temp = root.left
                root = None
                return temp
            temp = self.getMinValueNode(root.right)
            root.key = temp.key
            root.right = self.delete_node(root.right,
                                          temp.key)
        elif(root.lneighbor and event.node==root.lneighbor.node): 
            root.lneighbor = self.delete_node(root.lneighbor, event)
        elif(root.rneighbor and event.node==root.rneighbor.node): 
            root.rneighbor = self.delete_node(root.rneighbor, event)
        elif root > event.point:
            root.left = self.delete_node(root.left, event)
        elif root < event.point:
            root.right = self.delete_node(root.right, event)
        else:
            if root.lneighbor: 
                root.lneighbor.rneighbor = root.rneighbor
            if root.rneighbor: 
                root.rneighbor.lneighbor = root.lneighbor
            if root.left is None:
                temp = root.right
                root = None
                return temp
            elif root.right is None:
                temp = root.left
                root = None
                return temp
            temp = self.getMinValueNode(root.right)
            root.key = temp.key
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
    def getMinValueNode(self, root):
        if root is None or root.left is None:
            return root
        return self.getMinValueNode(root.left)

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

    # Get balance factor of the node
    def getBalance(self, root):
        if not root:
            return 0
        return self.getHeight(root.left) - self.getHeight(root.right)

def f(points): 
    points.sort(key=lambda point: point.y)
    beachlineroot = None
    beachline = Beachline()
    events = []
    # eventsroot = None
    # events = AVLTree()
    for point in points: 
        heappush(events, Event(TreeNode(point), point, -inf, True))
    while(events): 
    # while(eventsroot!=None): 
        # nextevent = events.getMinValueNode(eventsroot)
        # eventsroot = events.delete_node(eventsroot, nextevent)
        nextevent = heappop(events)
        if(nextevent.isinsertion): 
            # event is new site
            beachlineroot = beachline.insert_node(beachlineroot, nextevent.point)
            node = beachline.find_node(beachlineroot, nextevent.node)
            heappush(events, events)
        else: 
            # event is popping smth
            beachlineroot = beachline.delete_node(beachlineroot, nextevent)
            heappush(events, events)