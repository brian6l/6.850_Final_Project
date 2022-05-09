from math import inf, sqrt, atan, atan2, floor
from heapq import heappush, heappop
import pygame
import time

pygame.init()
HEIGHT = 600
WIDTH = 1000
screen = pygame.display.set_mode([WIDTH, HEIGHT])
screen.fill((255, 255, 255))

class Point(object): 
    def __init__(self, x, y): 
        self.x = x
        self.y = y
    def __eq__(self, point): 
        return self.x==point.x and self.y==point.y
    def __str__(self): 
        return str(self.x)+','+str(self.y)
class TreeNode(object):
    def copy(self): 
        tempnode = self
        tempnodecopy = TreeNode(tempnode.point)
        tempnodecopy.left = tempnode.left
        tempnodecopy.right = tempnode.right
        tempnodecopy.leftx = tempnode.leftx
        tempnodecopy.rightx = tempnodecopy.rightx
        tempnodecopy.directrix = tempnode.directrix
        tempnodecopy.lneighbor = tempnode.lneighbor
        tempnodecopy.rneighbor = tempnode.rneighbor
        tempnodecopy.height = tempnode.height
        return tempnodecopy
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
    def __str__(self): 
        return str(self.point)+'|'+str(self.leftx)+','+str(self.rightx)+'|'+str(self.height)+'|'+str(id(self))
    def __eq__(self, node): 
        return self.point==node.point and self.leftx==node.leftx and self.rightx==node.rightx
    def computerightx(self): 
        if(self.directrix==self.point.y): 
            return self.point.x
        parabola1coeffs = [1/(2*(self.point.y-self.directrix)), -1/((self.point.y-self.directrix))*self.point.x, 1/(2*(self.point.y-self.directrix))*self.point.x**2+(self.point.y+self.directrix)/2]
        if self.rneighbor: 
            focusr = self.rneighbor.point
            parabolarcoeffs = [1/(2*(focusr.y-self.directrix)), -1/((focusr.y-self.directrix))*focusr.x, 1/(2*(focusr.y-self.directrix))*focusr.x**2+(focusr.y+self.directrix)/2]
            a, b, c = tuple(parabola1coeffs[i]-parabolarcoeffs[i] for i in range(3))
            # print(a, b, c)
            # print(parabola1coeffs)
            # print(parabolarcoeffs)
            # print(a, b, c, self, self.lneighbor, self.rneighbor, self.directrix, parabola1coeffs, parabolarcoeffs)
            # print(self)
            if(a==0): 
                rightx = -c/b
            else: 
                u = (-b+sqrt(b*b-4*a*c))/(2*a)
                v = (-b-sqrt(b*b-4*a*c))/(2*a)
                return v
                if(False): 
                # if(self.leftx<=u<=self.rightx and self.rneighbor.leftx<=u<=self.rneighbor.rightx): 
                    rightx = u
                else: 
                    rightx = v
        else: 
            rightx = inf
        return rightx
    def computeleftx(self): 
        if(self.directrix==self.point.y): 
            return self.point.x
        parabola1coeffs = [1/(2*(self.point.y-self.directrix)), -1/((self.point.y-self.directrix))*self.point.x, 1/(2*(self.point.y-self.directrix))*self.point.x**2+(self.point.y+self.directrix)/2]
        if self.lneighbor: 
            focusl = self.lneighbor.point
            parabolalcoeffs = [1/(2*(focusl.y-self.directrix)), -1/((focusl.y-self.directrix))*focusl.x, 1/(2*(focusl.y-self.directrix))*focusl.x**2+(focusl.y+self.directrix)/2]
            a, b, c = tuple(parabola1coeffs[i]-parabolalcoeffs[i] for i in range(3))
            # print(a, b, c, self, self.lneighbor, self.rneighbor, self.directrix, parabola1coeffs, parabolalcoeffs)
            if(a==0): 
                # print(a, b, c)
                leftx = -c/b
            else: 
                u = (-b+sqrt(b*b-4*a*c))/(2*a)
                v = (-b-sqrt(b*b-4*a*c))/(2*a)
                return u
                if(True): 
                # if(self.leftx<=u<=self.rightx and self.lneighbor.leftx<=u<=self.lneighbor.rightx): 
                    leftx = u
                else: 
                    leftx = v
        else: 
            leftx = -inf
        # print(self, leftx)
        return leftx
    def __lt__(self, point): 
        # returns self<point, ie point going straight up is to the right of parabola
        if(self.rightx<point.x): 
            return True
        if(self.leftx>=point.x): 
            return False
        leftx = self.computeleftx()
        rightx = self.computerightx()
        return rightx<point.x or (rightx<=point.x+0.0000001 and leftx<point.x)
    def __gt__(self, point): 
        if(self.leftx>point.x): 
            return True
        if(self.rightx<=point.x): 
            return False
        leftx = self.computeleftx()
        rightx = self.computerightx()
        # print(leftx, rightx, point.x)
        return leftx>point.x or (leftx>=point.x-0.0000001 and rightx>point.x)
class Event(object): 
    def __init__(self, node, point, directrix, isinsertion): 
        self.node = node
        self.point = point
        self.directrix = directrix
        self.isinsertion = isinsertion
    def __lt__(self, event): 
        return self.directrix<event.directrix
    def __rt__(self, event): 
        return self.directrix>event.directrix
    def __eq__(self, event): 
        return self.directrix==event.directrix
    def __str__(self): 
        return str(self.node)+'||'+str(self.point)+'||'+str(self.directrix)+'||'+str(self.isinsertion)+('' if self.isinsertion else '||'+str(self.nodepoint)+" "+str(self.lneighborpoint)+" "+str(self.rneighborpoint))
class Beachline(object): 
    def __init__(self): 
        self.y = -inf
    def find_node(self, root, node, eventx=None): 
        if not root:
            return False
        if(eventx is None): 
            root.directrix = node.directrix
            # print(self, root, node)
            if(node==root): 
                # event.node.point==root.point and root.leftx<=event.point<=root.rightx
                return root
            elif(root.lneighbor and node==root.lneighbor): 
                return root.lneighbor
            elif(root.rneighbor and node==root.rneighbor): 
                return root.rneighbor
            # if root>node.point:
            if(root.computeleftx()>node.computeleftx()): 
                return self.find_node(root.left, node)
            if(root.computeleftx()<node.computeleftx()): 
            # elif root<node.point:
                return self.find_node(root.right, node)
            else:
                return None
        root.directrix = node.directrix
        # print(root, node, eventx, 'find delete')
        if(node.point==root.point and root.leftx<=eventx<=root.rightx): 
            # event.node.point==root.point and root.leftx<=event.point<=root.rightx
            return root
        elif(root.lneighbor and node.point==root.lneighbor.point and root.lneighbor.leftx<=eventx<=root.lneighbor.rightx): 
            return root.lneighbor
        elif(root.rneighbor and node.point==root.rneighbor.point and root.rneighbor.leftx<=eventx<=root.rneighbor.rightx): 
            return root.rneighbor
        # if root>node.point:
        # print(root.computeleftx(), root.computerightx())
        if(root.computeleftx()>eventx or (root.computeleftx()>=eventx-0.0000001 and root.computerightx()>eventx)): 
            return self.find_node(root.left, node, eventx=eventx)
        elif(root.computerightx()<eventx or (root.computerightx()<=eventx+0.0000001 and root.computeleftx()<eventx)): 
            # print('hi', root.right)
        # elif root<node.point:
            return self.find_node(root.right, node, eventx=eventx)
        else:
            return None
    def delete_left_node(self, root): 
        if(root.left is None): 
            return root.right
        root.left = self.delete_left_node(root.left)
        root.height = 1 + max(self.getHeight(root.left),
                              self.getHeight(root.right))

        # Update the balance factor and balance the tree
        balanceFactor = self.getBalance(root)
        if balanceFactor < -1:
            return self.leftRotate(root)

        return root
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
        root.left = self.insert_left_node(root.left, node)
        root.height = 1 + max(self.getHeight(root.left),
                              self.getHeight(root.right))

        # Update the balance factor and balance the tree
        balanceFactor = self.getBalance(root)
        if balanceFactor > 1:
            return self.rightRotate(root)

        return root

    def insert_node(self, root, point):
        # print(root, point)
        # Find the correct location and insert the node
        if not root:
            return TreeNode(point)
        root.directrix = point.y
        if root>point:
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
            lroot.rneighbor = root
            rroot.lneighbor = root
            root.left = self.insert_right_node(root.left, lroot)
            root.right = self.insert_left_node(root.right, rroot)
            root.leftx = -inf
            root.rightx = inf
        root.height = 1 + max(self.getHeight(root.left),
                              self.getHeight(root.right))
        # print('b', root, root.left, root.right, self.getHeight(root.left), self.getHeight(root.right), root.height)
        # Update the balance factor and balance the tree
        balanceFactor = self.getBalance(root)
        # print(balanceFactor)
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
        # print(root, event, 'delete', [root])
        # print(root.computeleftx(), root.computerightx())
        root.directrix = event.directrix
        # Find the node to be deleted and remove it
        boolean = False
        if not root:
            return root
        elif(event.node.point==root.point and root.leftx-0.0000001<=event.point.x<=root.rightx+0.0000001): 
            # print('hi')
            # print('a', root, root.lneighbor, root.rneighbor, root.left, root.right)
            # if root.left is None:
            #     if root.lneighbor: 
            #         root.lneighbor.rneighbor = root.rneighbor
            #     if root.rneighbor: 
            #         root.rneighbor.lneighbor = root.lneighbor
            #     temp = root.right
            #     root = None
            #     print('left')
            #     return temp
            # elif root.right is None:
            #     temp = root.left
            #     if root.lneighbor: 
            #         root.lneighbor.rneighbor = root.rneighbor
            #     if root.rneighbor: 
            #         root.rneighbor.lneighbor = temp
            #     root = None
            #     print('right')
            #     return temp
            # # print(root, 'neither')
            # temp = self.getMinValueNode(root.right)
            # root.point = temp.point
            # root.leftx = temp.leftx
            # root.rightx = temp.rightx
            # root.right = self.delete_left_node(root.right)
            # if(root.rneighbor and root.rneighbor.rneighbor): 
            #     root.rneighbor.rneighbor.lneigbor = root
            #     root.rneighbor = root.rneighbor.rneighbor
            # print(root, root.left, root.right)
            # print(root.lneighbor.rneighbor, root.rneighbor.lneighbor)
            if root.left is None:
                temp = root.right
            elif root.right is None:
                temp = root.left
            else:
                temp = root.rneighbor
                # temp = self.getMinValueNode(root.right)
            if not root.left or not root.right:
                if root.rneighbor:
                    if root.lneighbor:
                        root.rneighbor.lneighbor = root.lneighbor
                        root.lneighbor.rneighbor = root.rneighbor
                    else:
                        root.rightneighbor.leftneighbor = None
                elif root.leftneighbor:
                    root.leftneighbor.rightneighbor = None
                return temp
            boolean = False
            # if(root.point==Point(307, 206)): 
            #     boolean = True
            #     print(root.lneighbor)
            root.point = temp.point
            root.leftx = temp.leftx
            root.rightx = temp.rightx
            if root.rneighbor:
                if(root.rneighbor.rneighbor): 
                    root.rneighbor.rneighbor.lneighbor = root
                root.rneighbor = root.rneighbor.rneighbor
            root.right = self.delete_left_node(root.right)
            # if(boolean): 
            #     print(root, root.right.left, root.right.left.lneighbor, root.right.left.lneighbor.lneighbor, 'b')
            # assert str([root])==str([root.rneighbor.lneighbor])
        elif root>event.point:
            # print('g')
            # print(root, event.point, 'g')
            root.left = self.delete_node(root.left, event)
        elif root<event.point:
            # print('l')
            # print(root, event.point, 'l')
            root.right = self.delete_node(root.right, event)
        else:
            print('not found')
            # print('hi')
            return root
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
            root.point = temp.point
            root.leftx = temp.leftx
            root.rightx = temp.rightx
            root.right = self.delete_left_node(root.right)
            
        # if root is None:
        #     return root
        # print(root)
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
        if(boolean): 
            print(root, root.lneighbor, root.right.left.lneighbor.lneighbor, root.right.left.lneighbor.lneighbor.lneighbor)
        return root
    def leftRotate(self, z):
        # print(z)
        # leftmost = self.getMinValueNode(z)
        # rightmost = z
        # while(rightmost is not None and rightmost.right is not None): 
        #     rightmost = rightmost.right
        # print(leftmost)
        # while(True): 
        #     leftmost = leftmost.rneighbor
        #     print(leftmost)
        #     if(leftmost==rightmost): 
        #         break
        # print()
        # return z
        y = z.right
        T2 = y.left
        y.left = z
        z.right = T2
        z.height = 1 + max(self.getHeight(z.left),
                           self.getHeight(z.right))
        y.height = 1 + max(self.getHeight(y.left),
                           self.getHeight(y.right))
        # leftmost = self.getMinValueNode(y)
        # rightmost = y
        # while(rightmost is not None and rightmost.right is not None): 
        #     rightmost = rightmost.right
        # print(leftmost)
        # while(True): 
        #     leftmost = leftmost.rneighbor
        #     print(leftmost)
        #     if(leftmost==rightmost): 
        #         break
        # print()
        # print()
        return y

    # Function to perform right rotation
    def rightRotate(self, z):
        # print(z, 'right', z.left, z.right)
        # print(self.getBalance(z))
        # leftmost = self.getMinValueNode(z)
        # rightmost = z
        # while(rightmost is not None and rightmost.right is not None): 
        #     rightmost = rightmost.right
        # print(leftmost)
        # while(True): 
        #     leftmost = leftmost.rneighbor
        #     print(leftmost)
        #     if(leftmost==rightmost): 
        #         break
        # print()
        # return z
        y = z.left
        T3 = y.right
        y.right = z
        z.left = T3
        z.height = 1 + max(self.getHeight(z.left),
                           self.getHeight(z.right))
        y.height = 1 + max(self.getHeight(y.left),
                           self.getHeight(y.right))
        # leftmost = self.getMinValueNode(y)
        # rightmost = y
        # while(rightmost is not None and rightmost.right is not None): 
        #     rightmost = rightmost.right
        # print(leftmost)
        # while(True): 
        #     leftmost = leftmost.rneighbor
        #     print(leftmost)
        #     if(leftmost==rightmost): 
        #         break
        # print()
        # print()
        return y

    # Get the height of the node
    def getHeight(self, root):
        if not root:
            return 0
        return root.height

    # Get balance factor of the node
    def getBalance(self, root):
        # return 0
        if not root:
            return 0
        return self.getHeight(root.left) - self.getHeight(root.right)
    def getMinValueNode(self, root):
        if root is None or root.left is None:
            return root
        return self.getMinValueNode(root.left)
    def draw(self, root, precision = 100, screen = screen):
        if root.directrix == -inf:
            return
        curr = self.getMinValueNode(root)
        right = None
        while curr:
            curr.directrix, temp = root.directrix, curr.directrix
            try:
                left = curr.computeleftx()
            except:
                left = 0
            try:
                right = curr.computerightx()
            except:
                right = WIDTH
            curr.directrix = temp
            t = 2*(curr.point.y-root.directrix)
            if t != 0:
                a, b, c = 1/t, -2*curr.point.x/t, (curr.point.x**2+curr.point.y**2-root.directrix**2)/t
                #print(left, right)
                prev_p = (left, a*left*left+b*left+c)
                for k in range(1, precision+1):
                    x = left + (right-left)*k/precision
                    curr_p = (x, a*x*x+b*x+c)
                    pygame.draw.line(screen, (0,0,0), prev_p, curr_p)
                    prev_p = curr_p
            curr = curr.rneighbor

def draw_points(positions, screen = screen):
    pygame.draw.rect(screen, (255,255,255), pygame.Rect((0,0), (WIDTH, HEIGHT)))
    for point in positions:
        pygame.draw.circle(screen, (0,0,0), (point.x, point.y), 2)

def circumcenter(point1, point2, point3): 
    z12 = point1.x**2+point1.y**2
    z22 = point2.x**2+point2.y**2
    z32 = point3.x**2+point3.y**2
    return Point(-(point1.y*z22+point2.y*z32+point3.y*z12-point1.y*z32-point2.y*z12-point3.y*z22)/area(point1, point2, point3)/2, (point1.x*z22+point2.x*z32+point3.x*z12-point1.x*z32-point2.x*z12-point3.x*z22)/area(point1, point2, point3)/2)
def circumradius(point1, point2, point3): 
    d1 = sqrt((point2.x-point3.x)**2+(point2.y-point3.y)**2)
    d2 = sqrt((point3.x-point1.x)**2+(point3.y-point1.y)**2)
    d3 = sqrt((point1.x-point2.x)**2+(point1.y-point2.y)**2)
    return d1*d2*d3/(2*abs(area(point1, point2, point3)))
def area(point1, point2, point3): 
    return point1.x*point2.y+point2.x*point3.y+point3.x*point1.y-point1.y*point2.x-point2.y*point3.x-point3.y*point1.x
    
def f(points, speed = 0.005, screen = None):
    if not screen:
        screen = pygame.display.set_mode([WIDTH, HEIGHT])
    points.sort(key=lambda point: point.y)
    beachlineroot = None
    beachline = Beachline()
    events = []
    # eventsroot = None
    # events = AVLTree()
    for point in points: 
        node = TreeNode(point)
        node.directrix = point.y
        heappush(events, Event(node, point, point.y, True))
    graph = {}
    prev_directrix = 0
    while(events): 
        # print([i.__str__() for i in events])
        nextevent = heappop(events)
        if beachlineroot:
            root_directrix = beachlineroot.directrix
            if root_directrix <= HEIGHT:
                N = floor(nextevent.directrix - prev_directrix)
                for i in range(0,N):
                    beachlineroot.directrix = prev_directrix + (nextevent.directrix-prev_directrix)*i/N
                    draw_points(points, screen)
                    for edge in graph:
                        if len(graph[edge]) == 2:
                            pygame.draw.line(screen, (0,0,0), graph[edge][0], graph[edge][1])
                    pygame.draw.line(screen, (0,0,0), (0, beachlineroot.directrix), (WIDTH, beachlineroot.directrix))
                    beachline.draw(beachlineroot, screen = screen)
                    pygame.display.flip()
                    time.sleep(speed)
                    if beachlineroot.directrix > HEIGHT:
                        break
                beachlineroot.directrix = root_directrix
        else:
            N = floor(nextevent.directrix - prev_directrix)
            for i in range(0, N):
                y = prev_directrix + (nextevent.directrix - prev_directrix)*i/N
                draw_points(points, screen)
                pygame.draw.line(screen, (0,0,0), (0, y), (WIDTH, y))
                pygame.display.flip()
                time.sleep(speed)
        if(nextevent.isinsertion): 
            # print()
            # event is new site
            beachlineroot = beachline.insert_node(beachlineroot, nextevent.point)
            # print('a')
            # print(beachlineroot)
            # leftmost = beachlineroot
            # while(leftmost.left is not None): 
            #     leftmost = leftmost.left
            # print(leftmost)
            # while(leftmost): 
                # print(leftmost, leftmost.height, leftmost.left, leftmost.right, leftmost.lneighbor, leftmost.rneighbor)
                # leftmost = leftmost.rneighbor
            # print()
            # print(nextevent.node, beachlineroot)
            node = beachline.find_node(beachlineroot, nextevent.node)
            # print(node.lneighbor)
            if(node.lneighbor and node.lneighbor.lneighbor): 
                # print('asdfgh')
                # if(area(node.point, node.lneighbor.point, node.lneighbor.lneighbor.point)<0): 
                    circumx = circumcenter(node.point, node.lneighbor.point, node.lneighbor.lneighbor.point).x
                    circumy = circumcenter(node.point, node.lneighbor.point, node.lneighbor.lneighbor.point).y
                    arcy = circumy+circumradius(node.point, node.lneighbor.point, node.lneighbor.lneighbor.point)
                    if(atan((node.point.x-circumx)/(arcy-node.point.y))>atan((node.lneighbor.point.x-circumx)/(arcy-node.lneighbor.point.y))>atan((node.lneighbor.lneighbor.point.x-circumx)/(arcy-node.lneighbor.lneighbor.point.y))): 
                        tempnode = node.lneighbor.copy()
                        if(tempnode.left is not None): 
                            tempnode.left = tempnode.left.copy()
                        if(tempnode.right is not None): 
                            tempnode.right = tempnode.right.copy()
                        if(tempnode.lneighbor is not None): 
                            tempnode.lneighbor = tempnode.lneighbor.copy()
                        if(tempnode.rneighbor is not None): 
                            tempnode.rneighbor = tempnode.rneighbor.copy()
                        tempevent = Event(tempnode, Point(circumx, circumy), arcy, False)
                        tempevent.lneighborpoint = tempnode.lneighbor.point
                        tempevent.rneighborpoint = tempnode.rneighbor.point
                        heappush(events, tempevent)
            if(node.rneighbor and node.rneighbor.rneighbor): 
                # print('asdfghr')
                # print(node)
                # print(node.rneighbor)
                # print(node.rneighbor.rneighbor)
                # if(area(node.point, node.rneighbor.point, node.rneighbor.rneighbor.point)>0): 
                    circumx = circumcenter(node.point, node.rneighbor.point, node.rneighbor.rneighbor.point).x
                    circumy = circumcenter(node.point, node.rneighbor.point, node.rneighbor.rneighbor.point).y
                    arcy = circumy+circumradius(node.point, node.rneighbor.point, node.rneighbor.rneighbor.point)
                    if(atan((node.point.x-circumx)/(arcy-node.point.y))<atan((node.rneighbor.point.x-circumx)/(arcy-node.rneighbor.point.y))<atan((node.rneighbor.rneighbor.point.x-circumx)/(arcy-node.rneighbor.rneighbor.point.y))): 
                        tempnode = node.rneighbor.copy()
                        if(tempnode.left is not None): 
                            tempnode.left = tempnode.left.copy()
                        if(tempnode.right is not None): 
                            tempnode.right = tempnode.right.copy()
                        if(tempnode.lneighbor is not None): 
                            tempnode.lneighbor = tempnode.lneighbor.copy()
                        if(tempnode.rneighbor is not None): 
                            tempnode.rneighbor = tempnode.rneighbor.copy()
                        tempevent = Event(tempnode, Point(circumx, circumy), arcy, False)
                        tempevent.lneighborpoint = tempnode.lneighbor.point
                        tempevent.rneighborpoint = tempnode.rneighbor.point
                        heappush(events, tempevent)
            # heappush(events, events)
        else: 
            # event is popping smth
            # print(nextevent)
            # print(nextevent.node)
            nextevent.node.directrix = nextevent.directrix
            node = beachline.find_node(beachlineroot, nextevent.node, eventx=nextevent.point.x)
            # print(nextevent.node, node)
            if(node): 
                point1 = nextevent.node.point.x, nextevent.node.point.y
                point2 = nextevent.lneighborpoint.x, nextevent.lneighborpoint.y
                point3 = nextevent.rneighborpoint.x, nextevent.rneighborpoint.y
                # print('AAAAAA', point1, point2, point3, nextevent.point, nextevent.node)
                edge12 = (point1, point2) if point1[0]<point2[0] or (point1[0]==point2[0] and point1[1]<point2[1]) else (point2, point1)
                edge23 = (point2, point3) if point2[0]<point3[0] or (point2[0]==point3[0] and point2[1]<point3[1]) else (point3, point2)
                edge31 = (point3, point1) if point3[0]<point1[0] or (point3[0]==point1[0] and point3[1]<point1[1]) else (point1, point3)
                if(edge12 in graph): 
                    graph[edge12].append((nextevent.point.x, nextevent.point.y))
                else: 
                    graph[edge12] = [(nextevent.point.x, nextevent.point.y)]
                if(edge23 in graph): 
                    graph[edge23].append((nextevent.point.x, nextevent.point.y))
                else: 
                    graph[edge23] = [(nextevent.point.x, nextevent.point.y)]
                if(edge31 in graph): 
                    graph[edge31].append((nextevent.point.x, nextevent.point.y))
                else: 
                    graph[edge31] = [(nextevent.point.x, nextevent.point.y)]
                # print(node, set(graph))
            if(node): 
                # print('success', nextevent.directrix)
                # print(nextevent)
                # print(nextevent.node.lneighbor)
                # print(nextevent.node.rneighbor)
                if(node.lneighbor and node.rneighbor and node.lneighbor.lneighbor): 
                    # if(area(node.rneighbor.point, node.lneighbor.point, node.lneighbor.lneighbor.point)>0): 
                        circumx = circumcenter(node.rneighbor.point, node.lneighbor.point, node.lneighbor.lneighbor.point).x
                        circumy = circumcenter(node.rneighbor.point, node.lneighbor.point, node.lneighbor.lneighbor.point).y
                        arcy = circumy+circumradius(node.rneighbor.point, node.lneighbor.point, node.lneighbor.lneighbor.point)
                        if(atan((node.rneighbor.point.x-circumx)/(arcy-node.rneighbor.point.y))>atan((node.lneighbor.point.x-circumx)/(arcy-node.lneighbor.point.y))>atan((node.lneighbor.lneighbor.point.x-circumx)/(arcy-node.lneighbor.lneighbor.point.y))): 
                            tempnode = node.lneighbor.copy()
                            if(tempnode.left is not None): 
                                tempnode.left = tempnode.left.copy()
                            if(tempnode.right is not None): 
                                tempnode.right = tempnode.right.copy()
                            if(tempnode.lneighbor is not None): 
                                tempnode.lneighbor = tempnode.lneighbor.copy()
                            if(tempnode.rneighbor is not None): 
                                tempnode.rneighbor = tempnode.rneighbor.copy()
                            tempevent = Event(tempnode, Point(circumx, circumy), arcy, False)
                            tempevent.lneighborpoint = tempnode.lneighbor.point
                            tempevent.rneighborpoint = tempnode.rneighbor.rneighbor.point
                            heappush(events, tempevent)
                if(node.lneighbor and node.rneighbor and node.rneighbor.rneighbor): 
                    # if(area(node.lneighbor.point, node.rneighbor.point, node.rneighbor.rneighbor.point)<0): 
                        circumx = circumcenter(node.lneighbor.point, node.rneighbor.point, node.rneighbor.rneighbor.point).x
                        circumy = circumcenter(node.lneighbor.point, node.rneighbor.point, node.rneighbor.rneighbor.point).y
                        arcy = circumy+circumradius(node.lneighbor.point, node.rneighbor.point, node.rneighbor.rneighbor.point)
                        # print(node)
                        # print(node.lneighbor)
                        # print(node.rneighbor)
                        # print(node.rneighbor.rneighbor)
                        # print(arcy)
                        if(atan((node.lneighbor.point.x-circumx)/(arcy-node.lneighbor.point.y))<atan((node.rneighbor.point.x-circumx)/(arcy-node.rneighbor.point.y))<atan((node.rneighbor.rneighbor.point.x-circumx)/(arcy-node.rneighbor.rneighbor.point.y))): 
                            tempnode = node.rneighbor.copy()
                            if(tempnode.left is not None): 
                                tempnode.left = tempnode.left.copy()
                            if(tempnode.right is not None): 
                                tempnode.right = tempnode.right.copy()
                            if(tempnode.lneighbor is not None): 
                                tempnode.lneighbor = tempnode.lneighbor.copy()
                            if(tempnode.rneighbor is not None): 
                                tempnode.rneighbor = tempnode.rneighbor.copy()
                            tempevent = Event(tempnode, Point(circumx, circumy), arcy, False)
                            tempevent.lneighborpoint = tempnode.lneighbor.lneighbor.point
                            tempevent.rneighborpoint = tempnode.rneighbor.point
                            heappush(events, tempevent)
                beachlineroot = beachline.delete_node(beachlineroot, nextevent)
        prev_directrix = nextevent.directrix
        # print()
        # print([i.__str__() for i in events])
        # leftmost = beachlineroot
        # while(leftmost.left is not None): 
        #     leftmost = leftmost.left
        # # print(leftmost)
        # while(leftmost): 
        #     print(leftmost, leftmost.height, leftmost.left, leftmost.right, leftmost.lneighbor, leftmost.rneighbor)
        #     leftmost = leftmost.rneighbor
        # print()
    draw_points(points)
    for edge in graph:
        #pygame.draw.line(screen, (0,0,0), edge[0], edge[1])
        if len(graph[edge])==2:
            pygame.draw.line(screen, (0,0,0), graph[edge][0], graph[edge][1])
        else:
            if not(0<=graph[edge][0][0]<=WIDTH and 0<=graph[edge][0][1]<=HEIGHT):
                continue
            m = (edge[1][1]-edge[0][1])/(edge[1][0]-edge[0][0])
            b = edge[1][1] - m*edge[1][0]
            for point in points:
                if (point.x, point.y) != edge[0] and (point.x, point.y) != edge[1]:
                    break
            m1 = -1/m
            b1 = graph[edge][0][1]-m1*graph[edge][0][0]
            if b+m*point.x > point.y:
                pygame.draw.line(screen, (0,0,0), graph[edge][0], ((HEIGHT-b1)/m1,HEIGHT))
            else:
                pygame.draw.line(screen, (0,0,0), graph[edge][0], (-b1/m1, 0))
    pygame.display.flip()
    return graph

positions = []
x_coords = set()
y_coords = set()
def game(screen, running, calc_flag):
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and not calc_flag:
                pos = pygame.mouse.get_pos()
                if pos[0] not in x_coords and pos[1] not in y_coords:
                    pygame.draw.circle(screen, (0, 0, 0), pos, 2)
                    positions.append(Point(pos[0],pos[1]))
                    x_coords.add(pos[0])
                    y_coords.add(pos[1])
                    pygame.display.flip()
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE] and not calc_flag:
            calc_flag = True
            s = ""
            for point in positions:
                s += "Point("+str(point.x)+", "+str(point.y)+"),"
            print(s[:-1])
            ans = f(positions, 0.01)
            print(ans)
            pass
        pygame.display.flip()
    pygame.quit()

if __name__ == '__main__':
    game(screen, True, False)
