from fortunegraphics import f, Point
import pygame
import time

pygame.init()
HEIGHT = 600
WIDTH = 1000
screen = pygame.display.set_mode([WIDTH, HEIGHT])
screen.fill((255, 255, 255))

class DSDS():
    def __init__(self, vals):
        self.parents = {val:val for val in vals}
        self.sizes = {val:1 for val in vals}
    def find(self, val):
        if self.parents[val] != val:
            self.parents[val] = self.find(self.parents[val])
            return self.parents[val]
        else:
            return val
    def merge(self, x, y):
        x = self.find(x)
        y = self.find(y)
        if x == y:
            return
        if self.sizes[x] < self.sizes[y]:
            x, y = y, x
        self.parents[y] = x
        self.sizes[x] += self.sizes[y]

def kruskal(graph, screen):
    CC = DSDS(graph["V"])
    ans = set()
    graph["E"].sort()
    for e in graph["E"]:
        u = e[1]
        v = e[2]
        if CC.find(u) != CC.find(v):
            ans.add((u,v))
            pygame.draw.line(screen, (0,0,0), u, v)
            CC.merge(u,v)
            pygame.display.flip()
            time.sleep(0.2)
    return ans

def dist(point1, point2):
    return ((point1[0]-point2[0])**2+(point1[1]-point2[1])**2)**0.5

def Delaunay(points, screen):
    graph = f(points, screen = screen)
    return {edge for edge in graph}


def EMST(points, screen):
    edges = list(Delaunay(points, screen))
    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect((0,0), (WIDTH, HEIGHT)))
    vertices = set()
    for edge in edges:
        vertices.add(edge[0])
        vertices.add(edge[1])
    for i in range(len(edges)):
        edges[i] = (dist(edges[i][0],edges[i][1]), edges[i][0], edges[i][1])
        pygame.draw.line(screen, (200, 200, 200), edges[i][1], edges[i][2])
    for pos in vertices:
        pygame.draw.circle(screen, (0, 0, 0), pos, 2)
    pygame.display.flip()
    time.sleep(1)
    return kruskal({"E":edges, "V":vertices}, screen)

positions = []
def game(screen, running, calc_flag):
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and not calc_flag:
                pos = pygame.mouse.get_pos()
                pygame.draw.circle(screen, (0, 0, 0), pos, 2)
                positions.append(Point(pos[0],pos[1]))
                pygame.display.flip()
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE] and not calc_flag:
            calc_flag = True
            emst = EMST(positions, screen)
        pygame.display.flip()
    pygame.quit()

game(screen, True, False)




    
