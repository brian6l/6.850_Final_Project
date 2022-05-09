from fortunegraphics import f, Point
from pointlocationgraphics import DecisionTree, EPSILON

def approx(points):
    p1, p2 = points[0], points[1]
    if p2[0] < p1[0]:
        p1, p2 = p2, p1
    slope = (p2[1]-p1[1])/(p2[0]-p1[0])
    normal_c = EPSILON/(1+slope**2)
    dx, dy = normal_c, normal_c*slope
    return ((p1[0]+dx, p1[1]+dy), (p2[0]-dx, p2[1]-dy), points[2], points[3])

def NearestNeighbor(sites, query, box = [(0,0),(1000,600)]):
    x_min, y_min, x_max, y_max = box[0][0], box[0][1], box[1][0], box[1][1]
    points = [Point(site[0],site[1]) for site in sites]
    graph = f(points)
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
                edges.add(approx(q1, q2, p1, p2))
            else:
                edges.add(approx(q1, q2, p2, p1))
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
    trap_tree = DecisionTree([edge for edge in edges])
    region = trap_tree.search(query).val
    if region.top.bottom:
        return region.top.bottom
    elif region.bottom.top:
        return region.bottom.top
    else:
        print("oops!")

print(NearestNeighbor([(0,0),(1,1),(2,4)],(3,3)))

            

            
            
        
