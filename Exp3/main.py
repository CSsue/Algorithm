import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.io_utils import read_graph
from src.dijkstra import ShortestPath

def main():
    if len(sys.argv) < 2:
        print("用法: python main.py <图文件> [起点 终点]")
        return

    graph_file = sys.argv[1]
    graph = read_graph(graph_file)

    sp = ShortestPath(graph)

    if len(sys.argv) == 4:
        start, goal = int(sys.argv[2]), int(sys.argv[3])
        dist = sp.astar(start, goal)
        path = sp.get_path(goal)
        print(f"最短路径长度: {dist}")
        print(f"路径: {path}")
    else:
        print("进入交互模式，输入 'q' 退出")
        while True:
            try:
                line = input("输入起点和终点: ").strip()
                if line == 'q':
                    break
                start, goal = map(int, line.split())
                dist = sp.astar(start, goal)
                path = sp.get_path(goal)
                print(f"最短路径长度: {dist}")
                print(f"路径: {path}")
            except Exception as e:
                print("错误:", e)

if __name__ == "__main__":
    main()