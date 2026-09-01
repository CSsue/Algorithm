import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.io_utils import read_graph
from src.dijkstra import ShortestPath

def test_small():
    graph = read_graph('data/small.txt')  # 你可以构造一个小图测试
    sp = ShortestPath(graph)
    dist = sp.astar(0, 5)
    print(f"0 -> 5 最短路径: {dist}")
    print(f"路径: {sp.get_path(5)}")

def test_usa():
    graph = read_graph('data/usa.txt')
    sp = ShortestPath(graph)
    # 测试几个查询
    test_pairs = [(0, 100), (500, 1000), (1000, 2000)]
    for start, goal in test_pairs:
        dist = sp.astar(start, goal)
        print(f"{start} -> {goal} : {dist}")

if __name__ == "__main__":
    test_small()
    # test_usa()