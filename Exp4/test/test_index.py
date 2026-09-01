# 全量加载

import sys

def tokenize(text):
    """按空白符分割文本为单词列表"""
    return text.split()

def find_phrase_stats(words, phrase_words):
    """
    在单词列表 words 中查找短语 phrase_words
    返回 (first_position_1_based, count)
    """
    if not phrase_words:
        return -1, 0
    # 非法文本索引处理
    n = len(words)
    m = len(phrase_words)
    if m > n:
        return -1, 0

    first_pos = -1
    count = 0

    for i in range(n - m + 1):
        if words[i:i + m] == phrase_words:
            if count == 0:
                first_pos = i + 1  # 转为 1-based
            # 增加计数
            count += 1

    if count == 0:
        return -1, 0
    else:
        return first_pos, count

def main():
    if len(sys.argv) != 3:
        print("Usage: python word_index.py <corpus_file> <query_file>")
        sys.exit(1)

    # 读取语料库并分词
    with open(sys.argv[1], 'r', encoding='utf-8') as f:
        corpus = f.read()
    words = tokenize(corpus)

    # 读取查询（每行一个）
    with open(sys.argv[2], 'r', encoding='utf-8') as f:
        queries = [line.rstrip('\n') for line in f]

    # 处理每个查询
    for query in queries:
        phrase = query.split()
        pos, cnt = find_phrase_stats(words, phrase)
        if cnt == 0:
            print(f"-- 0 {query}")
        else:
            print(f"{pos} {cnt} {query}")

if __name__ == "__main__":
    main()