"""
Algorithm.Exp3.src.graph 的 Docstring
    构建地图的拓扑结构，存储点、边、邻接边信息。
    
"""

import math

class Point:
    def __init__(self, idx, x, y):
        self.id = idx
        self.x = x
        self.y = y

    def distance_to(self, other):
        # 预期直线距离
        return math.hypot(self.x - other.x, self.y - other.y)

class Edge:
    def __init__(self, v, w):
        self.v = v
        self.w = w
        self.distance = v.distance_to(w)

class Graph:
    def __init__(self):
        self.points = []    # 存储定点
        self.adj = []   # 相邻边的存储

    def add_point(self, p):
        self.points.append(p)
        self.adj.append([])

    def add_edge(self, v, w):
        self.adj[v].append(Edge(self.points[v], self.points[w]))
        self.adj[w].append(Edge(self.points[w], self.points[v]))

    def get_point(self, idx):
        return self.points[idx]

    def neighbors(self, idx):
        return self.adj[idx]