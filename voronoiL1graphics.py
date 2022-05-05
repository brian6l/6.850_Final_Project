from linkedavl import LAVLTree
import pygame

pygame.init()
HEIGHT = 600
WIDTH = 1000
screen = pygame.display.set_mode([WIDTH, HEIGHT])
screen.fill((255, 255, 255))

def d(p1, p2):
    return abs(p1[0]-p2[0])+abs(p1[1]-p2[1])

def SPM(points):
    curr_intervals = LAVLTree()
    root = None
    y_min, y_max = points[0][1], points[0][1]
    for (x,y) in points:
        if y < y_min:
            y_min = y
        if y > y_max:
            y_max = y
    root = curr_intervals.insert_node(root, (0,0)) #y_min doesn't matter because we have 0 as a lower bound
    pygame.draw.line(screen, (0,0,0), (points[0][0], 0), (points[0][0], HEIGHT))
    for i in range(1, len(points)):
        print("Looking at point",points[i])
        left = root
        while left.leftneighbor:
            left = left.leftneighbor
        while left:
            pygame.draw.line(screen, (0,0,0), (points[i-1][0], left.key[0]), (points[i][0], left.key[0]))
            left = left.rightneighbor
        #START HERE
        below_proj = None
        start = None
        curr = root
        while curr:
            if curr.key[0] >= points[i][1]:
                curr = curr.left
            else:
                below_proj = curr
                curr = curr.right
        P = (points[i][0], below_proj.key[0])
        if d(points[i], P) <= d(points[below_proj.key[1]], P):
            start = below_proj
        if not start and below_proj.rightneighbor:
            P = (points[i][0], below_proj.rightneighbor.key[0])
            if d(points[i], P) <= d(points[below_proj.rightneighbor.key[1]], P):
                start = below_proj.rightneighbor
        if not start:
            j = below_proj.key[1] #the entire interval must be above
            down = (points[i][1]+points[j][1]-points[i][0]+points[j][0])/2
            root = curr_intervals.insert_node(root, (down, i))
            pygame.draw.line(screen, (0,0,0), (points[i][0], down), (points[i][0],HEIGHT))
            continue
        temp = start.parent()
        print("temp start:",start.key)
        curr_intervals.printHelper(root,"",True)
        while temp:
            P = (points[i][0], temp.key[0])
            if d(points[i], P) <= d(points[temp.key[1]], P):
                start = temp
                print("using parent:",start.key)
                temp = temp.parent()
            else:
                break
        print("start:",start.key)
        #THE PROBLEM IS HERE. THE INTERVAL DOESN'T NECESSARILY LIE IN A SINGLE BIG SUBTREE
        curr_up, curr_down = start, start
        last_up, last_down = None, None
        while curr_up:
            j = curr_up.key[1]
            P = (points[i][0], curr_up.key[0])
            if d(points[i], P) <= d(points[j], P):
                last_up = curr_up
                curr_up = curr_up.right
            else:
                curr_up = curr_up.left
        while curr_down:
            j = curr_down.key[1]
            P = (points[i][0], curr_down.key[0])
            if d(points[i], P) <= d(points[j], P):
                last_down = curr_down
                curr_down = curr_down.left
            else:
                curr_down = curr_down.right
        #END HERE
        j = last_up.key[1]
        if points[j][1] >= points[i][1] and (points[i][0]-points[j][0]) <= (points[j][1]-points[i][1]):
            up = (points[j][1]+points[i][1]+points[i][0]-points[j][0])/2
        else:
            up = None
        if last_down.key[0] != 0:
            j = last_down.leftneighbor.key[1]
            down = max(0,(points[i][1]+points[j][1]-points[i][0]+points[j][0])/2)
        else:
            down = 0
        if down == 0:
            replaced = curr_intervals.getMinValueNode(root).key
            root = curr_intervals.delete_node(root, replaced)
        root = curr_intervals.insert_node(root, (down,i))
        print("last down:",last_down.key, "last up:",last_up.key)
        print("down:",down,"up:",up)
        if up is not None:
            pygame.draw.line(screen, (0,0,0), (points[i][0],down),(points[i][0],up))
        else:
            pygame.draw.line(screen, (0,0,0), (points[i][0],down),(points[i][0],HEIGHT))
        curr = root
        while curr.key != (down, i):
            if curr.key < (down, i):
                curr = curr.right
            else:
                curr = curr.left
        curr_above = curr.rightneighbor
        if up is not None:
            if not curr_above:
                root = curr_intervals.insert_node(root, (up, replaced[1]))
            elif curr_above.key[0] > up:
                if curr.leftneighbor:
                    root = curr_intervals.insert_node(root, (up, curr.leftneighbor.key[1]))
                else:
                    root = curr_intervals.insert_node(root, (up, replaced[1]))
            else:
                while curr_above:
                    temp = curr_above.rightneighbor
                    print("deleting",curr_above.key)
                    if not temp or temp.key[0] > up:
                        deleted_key = curr_above.key
                        root = curr_intervals.delete_node(root, curr_above.key)
                        if up is not None:
                            print("inserted",(up, deleted_key[1]))
                            root = curr_intervals.insert_node(root, (up, deleted_key[1]))
                        break
                    else:
                        root = curr_intervals.delete_node(root, curr_above.key)
                    curr_above = temp
        else:
            while curr_above:
                temp = curr_above.rightneighbor
                root = curr_intervals.delete_node(root, curr_above.key)
                curr_above = temp
        print(curr_intervals.__str__(root))
    left = root
    while left.leftneighbor:
        left = left.leftneighbor
    while left:
        pygame.draw.line(screen, (0,0,0), (points[-1][0], left.key[0]), (WIDTH, left.key[0]))
        left = left.rightneighbor
    return root, curr_intervals

positions = []
def game(screen, running, calc_flag):
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and not calc_flag:
                pos = pygame.mouse.get_pos()
                pygame.draw.circle(screen, (0, 0, 0), pos, 2)
                positions.append(pos)
                pygame.display.flip()
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE] and not calc_flag:
            calc_flag = True
            positions.sort()
            ans = SPM(positions)
            print(ans)
            pass
        pygame.display.flip()
    pygame.quit()

game(screen, True, False)