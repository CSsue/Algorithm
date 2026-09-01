"""
Algorithm.Exp3.src.dijkstra 的 Docstring
    迪杰斯特拉算法的优化 --> 添加导航索引

"""


from .priority_queue import IndexedMinHeap
import math

class ShortestPath:
    def __init__(self, graph):
        # 无穷大
        self.graph = graph
        self.dist = [float('inf')] * len(graph.points)
        self.prev = [-1] * len(graph.points)
        self.visited = [False] * len(graph.points)

    def reset(self):
        for i in range(len(self.dist)):
            self.dist[i] = float('inf')
            self.prev[i] = -1
            self.visited[i] = False

    def dijkstra(self, start, goal=None):
        self.reset()
        pq = IndexedMinHeap()
        self.dist[start] = 0.0
        pq.push(start, 0.0)

        while not pq.is_empty():
            v, _ = pq.pop()     # 取最近的顶点
            if self.visited[v]:     # 处理过的点跳过
                continue
            self.visited[v] = True

            if goal is not None and v == goal:
                break

            # 遍历临近节点
            for edge in self.graph.neighbors(v):
                w = edge.w.id
                new_dist = self.dist[v] + edge.distance
                if new_dist < self.dist[w]:
                    self.dist[w] = new_dist
                    self.prev[w] = v
                    pq.push(w, new_dist)

        return self.dist[goal] if goal is not None else self.dist

    # A*算法优化
    def astar(self, start, goal):
        self.reset()
        pq = IndexedMinHeap()
        self.dist[start] = 0.0
        start_point = self.graph.get_point(start)
        goal_point = self.graph.get_point(goal)

        def heuristic(v):
            p = self.graph.get_point(v)
            return p.distance_to(goal_point)

        pq.push(start, 0.0 + heuristic(start))

        while not pq.is_empty():
            v, _ = pq.pop()
            if self.visited[v]:
                continue
            self.visited[v] = True

            if v == goal:
                break

            for edge in self.graph.neighbors(v):
                w = edge.w.id
                new_dist = self.dist[v] + edge.distance
                if new_dist < self.dist[w]:
                    self.dist[w] = new_dist
                    self.prev[w] = v
                    pq.push(w, new_dist + heuristic(w))

        return self.dist[goal]

    def get_path(self, goal):
        path = []
        curr = goal
        while curr != -1:
            path.append(curr)
            curr = self.prev[curr]
        return path[::-1]