from .graph import Graph, Point

def read_graph(filename):
    graph = Graph()
    with open(filename, 'r') as f:
        # 顶点数 边数
        first_line = f.readline().strip().split()
        V = int(first_line[0])
        E = int(first_line[1])
        
        print(f"读取图中: {V} 个顶点, {E} 条边")
        
        # 读顶点
        for i in range(V):
            parts = f.readline().strip().split()
            if len(parts) < 3:
                continue
            idx, x, y = int(parts[0]), int(parts[1]), int(parts[2])
            graph.add_point(Point(idx, x, y))
        
        # 读边
        edges_read = 0
        for line in f:
            parts = line.strip().split()
            if len(parts) < 2:
                continue
            v, w = int(parts[0]), int(parts[1])
            graph.add_edge(v, w)
            edges_read += 1
        
        print(f"成功读取: {len(graph.points)} 个顶点, {edges_read} 条边")
        
    return graph