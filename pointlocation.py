import random

EPSILON = 0.0001

class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, P):
        return self.x == P.x and self.y == P.y

    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"

class Segment():
    def __init__(self, P, Q, top = None, bottom = None):
        self.P = P
        self.Q = Q
        self.top = top
        self.bottom = bottom
    
    def __str__(self):
        return str(self.P) + " to " + str(self.Q)

class Trapezoid():
    def __init__(self, bottom, top, leftp, rightp):
        self.top = top
        self.bottom = bottom
        self.leftp = leftp
        self.rightp = rightp

    def __str__(self):
        return "bottom: " + str(self.bottom) + ", top: " + str(self.top) + ", left: " + str(self.leftp) + ", right: " + str(self.rightp)

class Node():
    #for segments, we say that down is left and up is right
    def __init__(self, type, val, parents = None, left = None, right = None):
        self.type = type #T for trapezoid, P for point, S for segment
        self.val = val
        self.left = left
        if left:
            left.parents.append(self)
        self.right = right
        if right:
            right.parents.append(self)
        if parents:
            self.parents = parents
        else:
            self.parents = []
        if self.type == "T":
            self.leftneighbors = [] #store bottom up. can have at most 2
            self.rightneighbors = []

    def search(self, pos):
        if self.type == "T":
            return self
        if self.type == "P":
            if pos[0] < self.val.x:
                return self.left.search(pos)
            else:
                return self.right.search(pos)
        if self.type == "S":
            P, Q = self.val.P, self.val.Q
            m = (P.y-Q.y)/(P.x-Q.x)
            b = P.y-m*P.x
            if pos[1] < m*pos[0]+b:
                return self.left.search(pos)
            else:
                return self.right.search(pos)
    
    def replace(self, new_node):
        if not self.parents:
            raise Exception("Parent not found")
        for parent in self.parents:
            if parent.left == self:
                parent.left = new_node
                new_node.parents.append(parent)
            elif    parent.right == self:
                parent.right = new_node
                new_node.parents.append(parent)
            else:
                raise Exception("Node is not child of its parent")

def trap_sort(node):
    trap = node.val
    m = (trap.bottom.Q.y-trap.bottom.P.y)/(trap.bottom.Q.x-trap.bottom.P.x)
    b = trap.bottom.Q.y-m*trap.bottom.Q.x
    return m*trap.leftp.x+b

def DecisionTree(edges, box = [(0,0), (1000,600)]):
    random.shuffle(edges)
    print("EDGES: ",edges)
    bottom_left, bottom_right, top_left, top_right = Point(box[0][0], box[0][1]), Point(box[1][0], box[0][1]), Point(box[0][0], box[1][1]), Point(box[1][0], box[1][1])
    root = Node("T", Trapezoid(Segment(bottom_left,bottom_right),Segment(top_left,top_right),bottom_left,top_right))
    for n in range(len(edges)):
        e = edges[n]
        if e[1][0] < e[0][0]:
            if len(e) > 2:
                e = (e[1], e[0], e[2], e[3])
            else:
                e = (e[1], e[0])
        print("Adding edge",e)
        if len(e) > 2:
            segment = Segment(Point(e[0][0],e[0][1]),Point(e[1][0],e[1][1]), e[2], e[3])
        else:
            segment = Segment(Point(e[0][0],e[0][1]),Point(e[1][0],e[1][1]))
        m = (e[1][1]-e[0][1])/(e[1][0]-e[0][0])
        b = e[1][1]-e[1][0]*m
        normal_c = EPSILON/((1+m**2)**0.5)
        dx, dy = normal_c, m*normal_c
        print("Searching for points",(e[0][0]+dx, e[0][1]+dy),"and",(e[1][0]-dx,e[1][1]-dy))
        trap_start = root.search((e[0][0]+dx, e[0][1]+dy)) #this is to ensure that we get the right region even if they are endpoints
        trap_end = root.search((e[1][0]-dx,e[1][1]-dy))
        print("Starting trapezoid:", trap_start.val)
        print("Ending trapezoid:", trap_end.val)
        left_cap, right_cap = None, None #the "cap" trapezoid if the endpoint is within the interior of the left/right trapezoid
        left_end, right_end = Point(e[0][0], e[0][1]), Point(e[1][0], e[1][1])
        if e[0] != (trap_start.val.leftp.x, trap_start.val.leftp.y):
            left_cap = Trapezoid(trap_start.val.bottom, trap_start.val.top, trap_start.val.leftp, left_end)
            print("Got left cap", left_cap)
        if e[1] != (trap_end.val.rightp.x, trap_end.val.rightp.y):
            right_cap = Trapezoid(trap_end.val.bottom, trap_end.val.top, right_end, trap_end.val.rightp)
            print("Got right cap", right_cap)
        trap_list = [] #keep track of all trapezoids we hit
        top_traps, bottom_traps = [], [] #collection of the trapezoids formed above and below the added segment, respectively
        curr_leftp_top, curr_leftp_bottom = left_end, left_end
        curr_trap = trap_start
        while curr_trap != trap_end:
            trap_list.append(curr_trap)
            print("Passing trapezoid", curr_trap.val)
            rightx, righty = curr_trap.val.rightp.x, curr_trap.val.rightp.y
            print(righty, rightx, m, b)
            if righty > rightx*m+b:
                top_traps.append(Trapezoid(segment, curr_trap.val.top, curr_leftp_top, curr_trap.val.rightp))
                curr_leftp_top = curr_trap.val.rightp
            else:
                bottom_traps.append(Trapezoid(curr_trap.val.bottom, segment, curr_leftp_bottom, curr_trap.val.rightp))
                curr_leftp_bottom = curr_trap.val.rightp
            if len(curr_trap.rightneighbors) > 1:
                leftp_test = curr_trap.rightneighbors[0].val.leftp
                if leftp_test.y < m*leftp_test.x+b: #the left point is below, so we use the upper neighbor
                    curr_trap = curr_trap.rightneighbors[1]
                else:
                    curr_trap = curr_trap.rightneighbors[0]
            else: #only one right neighbor, we just take it
                curr_trap = curr_trap.rightneighbors[0]
        trap_list.append(trap_end)
        if right_cap:
            top_traps.append(Trapezoid(segment, trap_end.val.top, curr_leftp_top, right_end))
            bottom_traps.append(Trapezoid(trap_end.val.bottom, segment, curr_leftp_bottom, right_end))
        else:
            top_traps.append(Trapezoid(segment, trap_end.val.top, curr_leftp_top, trap_end.val.rightp))
            bottom_traps.append(Trapezoid(trap_end.val.bottom, segment, curr_leftp_bottom, trap_end.val.rightp))

        print("TOP TRAPS")
        for trap in top_traps:
            print(trap)
        print("\nBOTTOM TRAPS")
        for trap in bottom_traps:
            print(trap)
        top_traps = [Node("T",top_trap) for top_trap in top_traps]
        bottom_traps = [Node("T",bottom_trap) for bottom_trap in bottom_traps]

        if left_cap:
            left_cap = Node("T", left_cap)
            top_traps[0].leftneighbors.append(left_cap)
            bottom_traps[0].leftneighbors.append(left_cap)
            left_cap.rightneighbors.append(bottom_traps[0])
            left_cap.rightneighbors.append(top_traps[0])
            left_cap.leftneighbors = trap_start.leftneighbors
            new_trap = left_cap
        else:
            #if trap_start.val.top.P == trap_start.val.leftp:
                #new_trap = bottom_traps[0]
            #elif trap_start.val.bottom.P == trap_start.val.leftp:
                #new_trap = top_traps[0]
            #else:
                raise Exception
        for neighbor_trap in trap_start.leftneighbors:
            for i in range(len(neighbor_trap.rightneighbors)):
                if neighbor_trap.rightneighbors[i] == trap_start:
                    neighbor_trap.rightneighbors[i] = new_trap
                    break

        if right_cap:
            right_cap = Node("T", right_cap)
            top_traps[-1].rightneighbors.append(right_cap)
            bottom_traps[-1].rightneighbors.append(right_cap)
            right_cap.leftneighbors.append(bottom_traps[-1])
            right_cap.leftneighbors.append(top_traps[-1])
            right_cap.rightneighbors = trap_end.rightneighbors
            new_trap = right_cap
        else:
            #if trap_end.val.top.Q == trap_end.val.rightp:
                #new_trap = bottom_traps[-1]
            #elif trap_end.val.bottom.Q == trap_end.val.rightp:
                #new_trap = top_traps[-1]
            #else:
                raise Exception
        for neighbor_trap in trap_end.rightneighbors:
            for i in range(len(neighbor_trap.leftneighbors)):
                if neighbor_trap.leftneighbors[i] == trap_end:
                    neighbor_trap.leftneighbors[i] = new_trap
                    break
        
        for i in range(len(top_traps)-1):
            top_traps[i].rightneighbors.append(top_traps[i+1])
            top_traps[i+1].leftneighbors.append(top_traps[i])
        for i in range(len(bottom_traps)-1):
            bottom_traps[i].rightneighbors.append(bottom_traps[i+1])
            bottom_traps[i+1].leftneighbors.append(bottom_traps[i])
        if trap_start == trap_end: #this means we are in the starting case with only the bounding box
            if not(len(top_traps)==1 and len(bottom_traps)==1):
                raise Exception("If the line is in a single trapezoid, it should only have bottom and top")
            left_end_node, right_end_node = Node("P",left_end), Node("P",right_end)
            segment_node = Node("S", segment)
            segment_node.left, segment_node.right = bottom_traps[0], top_traps[0]
            bottom_traps[0].parents.append(segment_node)
            top_traps[0].parents.append(segment_node)
            if left_cap and right_cap:
                left_end_node.left, left_end_node.right = left_cap, right_end_node
                left_cap.parents.append(left_end_node)
                right_end_node.parents.append(left_end_node)
                right_end_node.left, right_end_node.right = segment_node, right_cap
                segment_node.parents.append(right_end_node)
                right_cap.parents.append(right_end_node)
                if not trap_start.parents:
                    root = left_end_node
                else:
                    trap_start.replace(left_end_node)
            elif left_cap:
                left_end_node.left, left_end_node.right = left_cap, segment_node
                left_cap.parents.append(left_end_node)
                segment_node.parents.append(left_end_node)
                trap_start.replace(left_end_node)
                #add the neighbors of the right trap which takes the side?
            elif right_cap:
                right_end_node.left, right_end_node.right = segment_node, right_cap
                segment_node.parents.append(right_end_node)
                right_cap.parents.append(right_end_node)
                trap_start.replace(right_end_node)
                #add the neighbors of the left trap which takes the side?
        else:
            curr_bottom_index, curr_top_index = 0, 0
            if left_cap:
                segment_node = Node("S", segment, [left_end], bottom_traps[0], top_traps[0])
                trap_start.replace(Node("P",left_end, None, left_cap, segment_node))
            else:
                trap_start.replace(Node("S", segment, None, bottom_traps[0], top_traps[0]))
            
            if right_cap:
                segment_node = Node("S", segment, [right_end], bottom_traps[-1], top_traps[-1])
                trap_end.replace(Node("P",right_end, None, segment_node, right_cap))
            else:
                trap_end.replace(Node("S", segment, None, bottom_traps[-1], top_traps[-1]))
            
            for i in range(0,len(trap_list)-1):
                if i > 0:
                    trap_list[i].replace(Node("S", segment, None, bottom_traps[curr_bottom_index], top_traps[curr_top_index]))
                left_new_neighbor = None
                right_new_neighbor = None
                for trap in trap_list[i+1].leftneighbors:
                    if trap != trap_list[i]:
                        left_new_neighbor = trap
                for trap in trap_list[i].rightneighbors:
                    if trap != trap_list[i+1]:
                        right_new_neighbor = trap
                if trap_list[i].val.rightp == top_traps[curr_top_index].val.rightp:
                    if right_new_neighbor:
                        for j in range(len(right_new_neighbor.leftneighbors)):
                            if right_new_neighbor.leftneighbors[j] == trap_list[i]:
                                right_new_neighbor.leftneighbors[j] = top_traps[curr_top_index]
                                top_traps[curr_top_index].rightneighbors.append(right_new_neighbor)
                                top_traps[curr_top_index].rightneighbors.sort(key = trap_sort)
                                print(right_new_neighbor.val,"has new neighbor",top_traps[curr_top_index].val)
                    curr_top_index += 1
                    if left_new_neighbor:
                        for j in range(len(left_new_neighbor.rightneighbors)):
                            if left_new_neighbor.rightneighbors[j] == trap_list[i+1]:
                                left_new_neighbor.rightneighbors[j] = top_traps[curr_top_index]
                                top_traps[curr_top_index].leftneighbors.append(left_new_neighbor)
                                top_traps[curr_top_index].leftneighbors.sort(key = trap_sort)
                                print(left_new_neighbor.val,"has new neighbor",top_traps[curr_top_index].val)

                elif trap_list[i].val.rightp == bottom_traps[curr_bottom_index].val.rightp:
                    if right_new_neighbor:
                        for j in range(len(right_new_neighbor.leftneighbors)):
                            if right_new_neighbor.leftneighbors[j] == trap_list[i]:
                                right_new_neighbor.leftneighbors[j] = bottom_traps[curr_bottom_index]
                                bottom_traps[curr_bottom_index].rightneighbors.append(right_new_neighbor)
                                bottom_traps[curr_bottom_index].rightneighbors.sort(key = trap_sort)
                                print(right_new_neighbor.val,"has new neighbor",bottom_traps[curr_bottom_index].val)
                    curr_bottom_index += 1
                    if left_new_neighbor:
                        for j in range(len(left_new_neighbor.rightneighbors)):
                            if left_new_neighbor.rightneighbors[j] == trap_list[i+1]:
                                left_new_neighbor.rightneighbors[j] = bottom_traps[curr_bottom_index]
                                bottom_traps[curr_bottom_index].leftneighbors.append(left_new_neighbor)
                                bottom_traps[curr_bottom_index].leftneighbors.sort(key = trap_sort)
                                print(left_new_neighbor.val,"has new neighbor",bottom_traps[curr_bottom_index].val)
                else:
                    raise Exception("Right point is not a left point of either constituent trapezoid")
    return root
            
            


        