"""
    文本索引：
    在一个大型的单词列表文件（每行一个单词）中，高效地查找多个查询短语（来自另一个文件）出现的位置和次数。
    采用流式读取，避免内存爆炸

"""
# query_large.py
import sys
from collections import deque

def count_phrase_in_word_file(word_file, phrase_words):
    """
    流式读取 word_file，查找 phrase_words 的出现情况
    返回 (first_position_1_based, total_count)
    """
    k = len(phrase_words)
    if k == 0:
        return -1, 0

    # 使用双端队列实现窗口的滑动
    window = deque(maxlen=k)

    pos = 0  # 当前单词位置（1-based）
    first_pos = -1
    count = 0

    with open(word_file, 'r', encoding='utf-8') as f:
        for line in f:
            # 处理空字符串
            word = line.strip()
            if not word:
                continue
            pos += 1
            # 窗口滑动
            window.append(word)

            if len(window) == k:
                if list(window) == phrase_words:
                    # 首次出现
                    if count == 0:
                        first_pos = pos - k + 1
                    # 计数加1
                    count += 1

    return (first_pos, count)

def main():
    # 终端命令
    if len(sys.argv) != 3:
        print("Usage: python query_large.py <clean_words.txt> <query.txt>")
        sys.exit(1)

    word_file = sys.argv[1]
    query_file = sys.argv[2]

    # 读取每一行作为原始字符串
    with open(query_file, 'r', encoding='utf-8') as f:
        queries = [line.rstrip('\n') for line in f]

    # 处理查询文件中的非法字符
    for query in queries:
        # 清理查询：只保留 a-z 和空格，并转小写
        import re
        clean_query = re.sub(r'[^a-z\s]', ' ', query.lower()).strip()
        # 空文件处理
        if not clean_query:
            print(f"-- 0 {query}")
            continue

        phrase = clean_query.split()

        # 调用文本索引函数
        first, cnt = count_phrase_in_word_file(word_file, phrase)

        if cnt == 0:
            print(f"-- 0 {query}")
        else:
            print(f"{first} {cnt} {query}")
# 程序入口
if __name__ == "__main__":
    main()