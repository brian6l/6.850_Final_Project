from curses.panel import top_panel
import random
from subprocess import ABOVE_NORMAL_PRIORITY_CLASS

EPSILON = 0.0001

class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, P):
        return self.x == P.x and self.y == P.y

class Segment():
    def __init__(self, P, Q, top = None, bottom = None):
        self.P = P
        self.Q = Q
        self.top = top
        self.bottom = bottom

class Trapezoid():
    def __init__(self, bottom, top, leftp, rightp):
        self.top = top
        self.bottom = bottom
        self.leftp = leftp
        self.rightp = rightp

class Node():
    #for segments, we say that down is left and up is right
    def __init__(self, type, val, parent = None, left = None, right = None):
        self.type = type #T for trapezoid, P for point, S for segment
        self.val = val
        self.left = left
        self.right = right
        self.parent = parent
        if self.val == "T":
            self.leftneighbors = [] #store bottom up. can have at most 2
            self.rightneighbors = []

    def search(self, pos):
        if type == "T":
            return self
        if type == "P":
            if pos[0] < self.val.x:
                return self.left.search(pos)
            else:
                return self.right.search(pos)
        if type == "S":
            P, Q = self.val.P, self.val.Q
            m = (P.y-Q.y)/(P.x-Q.x)
            b = P.y-m*P.x
            if pos[1] < m*pos[0]+b:
                return self.left.search(pos)
            else:
                return self.right.search(pos)
    
    def replace(self, new_node):
        if not self.parent:
            raise Exception("Parent not found")
        if self.parent.left == self:
            self.parent.left = new_node
            new_node.parent = self.parent
        elif self.parent.right == self:
            self.parent.right = new_node
            new_node.parent = self.parent
        else:
            raise Exception("Node is not child of its parent")

def DecisionTree(edges, box = [(0,0), (1000,600)]):
    random.shuffle(edges)
    bottom_left, bottom_right, top_left, top_right = Point(box[0][0], box[0][1]), Point(box[1][0], box[0][1]), Point(box[0][0], box[1][1]), Point(box[1][0], box[1][1])
    root = Node("T", Trapezoid(Segment(bottom_left,bottom_right),Segment(top_left,top_right),bottom_left,top_right))
    for e in edges:
        if e[1][0] < e[0][0]:
            e = (e[1], e[0])
        segment = Segment(Point(e[0][0],e[0][1]),Point(e[1][0],e[1][1]))
        m = (e[1][1]-e[0][1])/(e[1][0]-e[0][0])
        b = e[1][1]*m-e[1][0]
        normal_c = EPSILON/((1+m**2)**0.5)
        dx, dy = normal_c, m*normal_c
        trap_start = root.search((e[0][0]+dx, e[0][1]+dy)) #this is to ensure that we get the right region even if they are endpoints
        trap_end = root.search((e[1][0]-dx,e[1][1]-dy))
        left_cap, right_cap = None, None #the "cap" trapezoid if the endpoint is within the interior of the left/right trapezoid
        left_end, right_end = Point(e[0][0], e[0][1]), Point(e[1][0], e[1][1])
        if e[0] != (trap_start.leftp.x, trap_start.rightp.y):
            left_cap = Trapezoid(trap_start.bottom, trap_start.top, trap_start.leftp, left_end)
        if e[1] != (trap_end.rightp.x, trap_end.rightp.y):
            right_cap = Trapezoid(trap_end.bottom, trap_end.top, right_end, trap_end.rightp)
        trap_list = [] #keep track of all trapezoids we hit
        top_traps, bottom_traps = [], [] #collection of the trapezoids formed above and below the added segment, respectively
        curr_leftp_top, curr_leftp_bottom = left_end, left_end
        curr_trap = trap_start
        while curr_trap != trap_end:
            trap_list.append(curr_trap)
            rightx, righty = curr_trap.rightp.x, curr_trap.rightp.y
            if righty > rightx*m+b:
                top_traps.append(Trapezoid(segment, curr_trap.top, curr_leftp_top, curr_trap.rightp))
                curr_leftp_top = curr_trap.rightp
            else:
                bottom_traps.append(Trapezoid(curr_trap.bottom, segment, curr_leftp_bottom, curr_trap.rightp))
                curr_leftp_bottom = curr_trap.rightp
            if len(curr_trap.rightneighbors) > 1:
                leftp_test = curr_trap.rightneighbors[0].leftp
                if leftp_test.y < m*leftp_test.x+b: #the left point is below, so we use the upper neighbor
                    curr_trap = curr_trap.rightneighbors[1]
                else:
                    curr_trap = curr_trap.rightneighbors[0]
            else: #only one right neighbor, we just take it
                curr_trap = curr_trap.rightneighbors[0]
        trap_list.append(trap_end)
        if right_cap:
            top_traps.append(Trapezoid(segment, trap_end.top, curr_leftp_top, right_end))
            bottom_traps.append(Trapezoid(trap_end.bottom, segment, curr_leftp_bottom, right_end))
        else:
            top_traps.append(Trapezoid(segment, trap_end.top, curr_leftp_top, trap_end.rightp))
            bottom_traps.append(Trapezoid(trap_end.bottom, segment, curr_leftp_bottom, trap_end.rightp))

        top_traps = [Node("T",top_trap) for top_trap in top_traps]
        bottom_traps = [Node("T",bottom_trap) for bottom_trap in bottom_traps]

        if left_cap:
            left_cap = Node("T", left_cap)
            top_traps[0].leftneighbors.append(left_cap)
            bottom_traps[0].leftneighbors.append(left_cap)
            left_cap.rightneighbors.append(bottom_traps[0])
            left_cap.rightneighbors.append(top_traps[0])
        if right_cap:
            right_cap = Node("T", right_cap)
            top_traps[-1].rightneighbors.append(right_cap)
            bottom_traps[-1].rightneighbors.append(right_cap)
            right_cap.leftneighbors.append(bottom_traps[-1])
            right_cap.leftneighbors.append(top_traps[-1])
        
        for i in range(len(top_traps)-1):
            top_traps[i].rightneighbors.append(top_traps[i+1])
            top_traps[i+1].leftneighbors.append(top_traps[i])
        for i in range(len(bottom_traps)-1):
            bottom_traps[i].rightneighbors.append(bottom_traps[i+1])
            bottom_traps[i+1].leftneighbors.append(bottom_traps[i])
        if not trap_start.parent: #this means we are in the starting case with only the bounding box
            if not(len(top_traps)==1 and len(bottom_traps)==1 and left_cap and right_cap):
                raise Exception("Incorrect base case computation")
            left_end_node, right_end_node = Node("P",left_end), Node("P",right_end)
            segment_node = Node("S", segment)
            left_end_node.left, left_cap.parent = left_cap, left_end_node
            left_end_node.right, right_end_node.parent = right_end_node, left_end_node
            right_end_node.left, segment_node.parent = segment_node, right_end_node
            right_end_node.right, right_cap.parent = right_cap, right_end_node
            segment_node.left, bottom_traps[0].parent = bottom_traps[0], segment_node
            segment_node.right, top_traps[0].parent = top_traps[0], segment_node
            root = left_end_node
        else:
            curr_bottom_index, curr_top_index = 0
            if left_cap:
                segment_node = Node("S", segment,left_end, bottom_traps[0], top_traps[0])
                trap_start.replace(Node("P",left_end, trap_start.parent, left_cap, segment_node))
            else:
                trap_start.replace(Node("S", segment, trap_start.parent, bottom_traps[0], top_traps[0]))
            if trap_start.val.rightp == top_traps[0].leftp:
                curr_top_index += 1
            elif trap_start.val.rightp == bottom_traps[0].leftp:
                curr_bottom_index += 1
            else:
                raise Exception("Right point is not a left point of either constituent trapezoid")
            
            if right_cap:
                segment_node = Node("S", segment, right_end, bottom_traps[-1], top_traps[-1])
                trap_end.replace(Node("P",right_end, trap_end.parent, right_cap, segment_node))
            else:
                trap_end.replace(Node("S", segment, trap_end.parent, bottom_traps[-1], top_traps[-1]))
            
            for i in range(1,len(trap_list)-1):
                trap_list[i].replace(Node("S", segment, trap_list[i].parent, bottom_traps[curr_bottom_index], top_traps[curr_top_index]))
                if trap_list[i].val.rightp == top_traps[curr_top_index].leftp:
                    curr_top_index += 1
                elif trap_list[i].val.rightp == bottom_traps[curr_bottom_index].leftp:
                    curr_bottom_index += 1
                else:
                    raise Exception("Right point is not a left point of either constituent trapezoid")
    return root
            
            


        