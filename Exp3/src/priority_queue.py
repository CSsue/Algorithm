"""
Algorithm.Exp3.src.priority_queue 的 Docstring
    通过最小堆的逻辑构建优先队列

"""

import heapq

class IndexedMinHeap:
    def __init__(self):
        self.heap = []
        self.index_map = {}  # 元素的内容，索引（确定位置）

    def push(self, item, key):
        if item in self.index_map:
            self.update(item, key)
        else:
            entry = [key, item]
            self.index_map[item] = entry
            heapq.heappush(self.heap, entry)

    def pop(self):
        while self.heap:
            key, item = heapq.heappop(self.heap)
            if item is not None:
                del self.index_map[item]
                return item, key
        raise IndexError("pop from empty heap")

    def update(self, item, new_key):
        entry = self.index_map[item]
        entry[0] = new_key
        heapq.heapify(self.heap)  # 简单实现，可优化

    def is_empty(self):
        return len(self.heap) == 0