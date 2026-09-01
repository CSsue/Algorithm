import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.io_utils import read_graph
from src.dijkstra import ShortestPath
import math

def test_small_graph():
    print("=== 小图测试 ===")
    
    # 读取图
    graph = read_graph('data/small.txt')
    print(f"顶点数: {len(graph.points)}")
    print(f"边数: {sum(len(adj) for adj in graph.adj) // 2}")
    
    # 打印顶点信息
    print("\n顶点信息:")
    for p in graph.points:
        print(f"顶点 {p.id}: ({p.x}, {p.y})")
    
    # 打印邻接关系
    print("\n邻接关系:")
    for i in range(len(graph.points)):
        neighbors = [edge.w.id for edge in graph.neighbors(i)]
        print(f"顶点 {i} 的邻居: {neighbors}")
    
    # 测试点之间的距离
    print("\n点之间距离:")
    p0 = graph.get_point(0)
    p1 = graph.get_point(1)
    p2 = graph.get_point(2)
    p5 = graph.get_point(5)
    print(f"0->1 距离: {p0.distance_to(p1):.2f}")
    print(f"1->2 距离: {p1.distance_to(p2):.2f}")
    print(f"2->5 距离: {p2.distance_to(p5):.2f}")
    
    return graph

def test_shortest_paths():
    print("\n=== 最短路径测试 ===")
    graph = read_graph('data/small.txt')
    sp = ShortestPath(graph)
    
    # 测试 0->5 的最短路径（题目中应该是 0-1-2-5）
    print("测试 0 -> 5 的最短路径:")
    
    # Dijkstra
    dist_dijkstra = sp.dijkstra(0, 5)
    path_dijkstra = sp.get_path(5)
    print(f"Dijkstra 结果: 距离={dist_dijkstra:.2f}, 路径={path_dijkstra}")
    
    # A*
    dist_astar = sp.astar(0, 5)
    path_astar = sp.get_path(5)
    print(f"A* 结果: 距离={dist_astar:.2f}, 路径={path_astar}")
    
    # 验证路径长度
    expected_path = [0, 1, 2, 5]
    manual_distance = 0
    for i in range(len(expected_path)-1):
        p1 = graph.get_point(expected_path[i])
        p2 = graph.get_point(expected_path[i+1])
        manual_distance += p1.distance_to(p2)
    
    print(f"手动计算路径 {expected_path} 的距离: {manual_distance:.2f}")
    
    # 测试其他路径
    test_cases = [(0, 3), (1, 4), (0, 4)]
    for start, goal in test_cases:
        dist = sp.astar(start, goal)
        path = sp.get_path(goal)
        print(f"{start}->{goal}: 距离={dist:.2f}, 路径={path}")

def validate_with_expected():
    """根据题目中给出的处理过程验证"""
    print("\n=== 与题目预期结果对比 ===")
    graph = read_graph('data/small.txt')
    sp = ShortestPath(graph)
    
    # 题目中给出的处理过程：
    # process (0.0)  
    #     lower 3 to 3841.9  
    #     lower 1 to 1897.4  
    # process 1 (1897.4)  
    #     lower 4 to 3776.2  
    #     lower 2 to 2537.7  
    # process 2 (2537.7)  
    #     lower 5 to 6274.0  
    
    # 计算 0->5
    dist = sp.astar(0, 5)
    path = sp.get_path(5)
    
    print(f"0->5 计算路径: {path}")
    print(f"0->5 计算距离: {dist:.2f}")
    print(f"题目预期距离: 6274.0")
    print(f"差异: {abs(dist - 6274.0):.2f}")
    
    # 验证中间距离
    print("\n验证中间顶点距离:")
    dist_to_1 = graph.get_point(0).distance_to(graph.get_point(1))
    dist_1_to_2 = graph.get_point(1).distance_to(graph.get_point(2)) 
    dist_2_to_5 = graph.get_point(2).distance_to(graph.get_point(5))
    
    print(f"0->1: {dist_to_1:.2f} (预期: ~1897.4)")
    print(f"1->2: {dist_1_to_2:.2f} (预期: ~640.3)")
    print(f"2->5: {dist_2_to_5:.2f}")
    print(f"累计: {(dist_to_1 + dist_1_to_2 + dist_2_to_5):.2f}")

if __name__ == "__main__":
    test_small_graph()
    test_shortest_paths()
    validate_with_expected()