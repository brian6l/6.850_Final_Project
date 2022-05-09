from fortunegraphics import f, Point #draw_points
from pointlocationgraphics import DecisionTree, EPSILON
import pygame, time

pygame.init()
HEIGHT = 600
WIDTH = 1000
EPSILON = 5*EPSILON
screen = pygame.display.set_mode([WIDTH, HEIGHT])
screen.fill((255, 255, 255))

def approx(points):
    p1, p2 = points[0], points[1]
    if p2[0] < p1[0]:
        p1, p2 = p2, p1
    slope = (p2[1]-p1[1])/(p2[0]-p1[0])
    normal_c = EPSILON/(1+slope**2)
    dx, dy = normal_c, normal_c*slope
    return ((p1[0]+dx, p1[1]+dy), (p2[0]-dx, p2[1]-dy), points[2], points[3])

def NearestNeighbor(sites, box = [(0,0),(1000,600)], speed = 0.01):
    x_min, y_min, x_max, y_max = box[0][0], box[0][1], box[1][0], box[1][1]
    points = [Point(site[0],site[1]) for site in sites]
    graph = f(points, speed, screen)
    time.sleep(2)
    edges = set()
    for site_edge in graph:
        p1, p2 = site_edge[0], site_edge[1]
        for point in graph[site_edge]:
            if point[0] < x_min:
                x_min = point[0]
            elif point[0] > x_max:
                x_max = point[0]
            if point[1] < y_min:
                y_min = point[1]
            elif point[1] > y_max:
                y_max = point[1]
    x_min -= EPSILON
    y_min -= EPSILON
    x_max -= EPSILON
    y_max -= EPSILON
    box = [(x_min-EPSILON,y_min-EPSILON), (x_max+EPSILON, y_max+EPSILON)]

    for site_edge in graph:
        p1, p2 = site_edge[0], site_edge[1]
        m_s = (p2[1]-p1[1])/(p2[0]-p1[0])
        b_s = p2[1] - m_s*p2[0]
        if len(graph[site_edge]) == 2:
            q1, q2 = graph[site_edge][0], graph[site_edge][1]
            m_v = (q2[1]-q1[1])/(q2[0]-q1[0])
            b_v = q2[1] - m_v*q2[0]
            if p1[1] > m_v*p1[0]+b_v: #p1 is on top, p0 is below
                edges.add(approx((q1, q2, p1, p2)))
            else:
                edges.add(approx((q1, q2, p2, p1)))
        else:
            q = graph[site_edge][0]
            m_v = -1/m_s
            b_v = q[1] - m_v*q[0]
            for diff_site in sites:
                if diff_site != p1 and diff_site != p2:
                    break
            if diff_site[1] > m_s*diff_site[0]+b_s:
                sign = -1
            else:
                sign = 1
            if p1[1] < m_v*p1[0]+b_v:
                p1, p2 = p2, p1
            
            left = (x_min, x_min*m_v+b_v)
            if y_min <= left[1] <= y_max and (left[1]-left[0]*m_s-b_s)*sign > 0:
                edges.add(approx((q, left, p1, p2)))
                continue
            right = (x_max, x_max*m_v+b_v)
            if y_min <= right[1] <= y_max and (right[1]-right[0]*m_s-b_s)*sign > 0:
                edges.add(approx((q, right, p1, p2)))
                continue
            bottom = ((y_min-b_v)/m_v, y_min)
            if x_min <= bottom[0] <= x_max and (bottom[1]-bottom[0]*m_s-b_s)*sign > 0:
                edges.add(approx((q, bottom, p1, p2)))
                continue
            top = ((y_max-b_v)/m_v, y_max)
            if x_min <= top[0] <= x_max and (top[1]-top[0]*m_s-b_s)*sign > 0:
                edges.add(approx((q, top, p1, p2)))
                continue
            raise Exception("Could not find a suitable border point")
    print([edge for edge in edges])
    trap_tree = DecisionTree([edge for edge in edges], box, screen)
    return trap_tree, graph

def query_NN(trap_tree, pos):
    region = trap_tree.search(pos).val
    for _ in range(2):
        if region.top.bottom:
            return region.top.bottom
        elif region.bottom.top:
            return region.bottom.top
        else:
            if region.rightneighbors:
                region = region.rightneighbors[0]
            elif region.leftneighbors:
                region = region.leftneighbors[0]

positions = []
x_coords = set()
y_coords = set()
def game(screen, running, calc_flag):
    trap_tree = None
    last_query = None
    computation_flag = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and not calc_flag:
                pos = pygame.mouse.get_pos()
                if not computation_flag and pos[0] not in x_coords and pos[1] not in y_coords:
                    pygame.draw.circle(screen, (0, 0, 0), pos, 2)
                    pygame.display.flip()
                    positions.append((pos[0],pos[1]))
                    x_coords.add(pos[0])
                    y_coords.add(pos[1])
                elif trap_tree:
                    pygame.draw.circle(screen, (0, 0, 0), pos, 1)
                    if last_query:
                        pygame.draw.circle(screen, (255,255,255), last_query, 1)
                    for site in positions:
                        pygame.draw.circle(screen, (0, 0, 0), site, 2)
                    nearest_neighbor = query_NN(trap_tree, pos)
                    pygame.draw.circle(screen, (0, 255, 0), nearest_neighbor, 2)
                    pygame.display.flip()
                    last_query = pos

        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE] and not calc_flag:
            calc_flag = True
            s = ""
            for point in positions:
                s += "("+str(point[0])+", "+str(point[1])+"),"
            print(s[:-1])
            try:
                trap_tree, voronoi = NearestNeighbor(positions, speed = 0.01)
                pygame.draw.rect(screen, (255, 255, 255), pygame.Rect((0,0),(1000,600)))
                trap_tree.draw((200,200,200))
                for point in positions:
                    pygame.draw.circle(screen, (0,0,0), (point[0], point[1]), 2)
                for edge in voronoi:
                    if len(voronoi[edge])==2:
                        pygame.draw.line(screen, (255,0,0), voronoi[edge][0], voronoi[edge][1],2)
                    else:
                        if not(0<=voronoi[edge][0][0]<=WIDTH and 0<=voronoi[edge][0][1]<=HEIGHT):
                            continue
                        m = (edge[1][1]-edge[0][1])/(edge[1][0]-edge[0][0])
                        b = edge[1][1] - m*edge[1][0]
                        for point in positions:
                            if (point[0], point[1]) != edge[0] and (point[0], point[1]) != edge[1]:
                                break
                        m1 = -1/m
                        b1 = voronoi[edge][0][1]-m1*voronoi[edge][0][0]
                        if b+m*point[0] > point[1]:
                            pygame.draw.line(screen, (255,0,0), voronoi[edge][0], ((HEIGHT-b1)/m1,HEIGHT),2)
                        else:
                            pygame.draw.line(screen, (255,0,0), voronoi[edge][0], (-b1/m1, 0),2)
            except:
                print(s)
            calc_flag = False
            computation_flag = True
            pass
        pygame.display.flip()
    pygame.quit()


game(screen, True, False)