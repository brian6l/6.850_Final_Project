from fortune import f, Point

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

def kruskal(graph):
    CC = DSDS(graph["V"])
    ans = set()
    graph["E"].sort()
    for (u, v) in graph["E"]:
        if CC.find(u) != CC.find(v):
            ans.add((u,v))
            CC.merge(u,v)
    return ans

def dist(point1, point2):
    return ((point1[0]-point2[0])**2+(point1[1]-point2[1])**2)**0.5

def Delaunay(points):
    graph = f(points)
    return {edge for edge in graph}


def EMST(points):
    edges = list(Delaunay(points))
    vertices = set()
    for edge in edges:
        vertices.add(edge[0])
        vertices.add(edge[1])
    for i in range(len(edges)):
        edges[i] = (dist(edges[i][0],edges[i][1]), edges[i][0], edges[i][1])
    return kruskal({"E":edges, "V":vertices})
    
