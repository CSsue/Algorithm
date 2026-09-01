"""
    处理大规模文本，删除非法字符和标点

"""
# preprocess.py
import sys
import re

def clean_and_tokenize(input_path, output_word_file):
    with open(input_path, 'r', encoding='utf-8', errors='ignore') as fin, \
         open(output_word_file, 'w', encoding='utf-8') as fout:

        word_count = 0
        buffer = ''

        # 流式读取文件
        while True:
            chunk = fin.read(65536)  # 64KB
            if not chunk:
                break
            # 缓冲区
            # 防止分块影响数据
            buffer += chunk

            # 按行分割，保留最后一段不完整行
            lines = buffer.split('\n')
            buffer = lines[-1]

            for line in lines[:-1]:
                # 正则处理
                cleaned = re.sub(r'[^a-z\s]', ' ', line.lower())
                words = cleaned.split()
                # 单词分行处理
                for word in words:
                    if word:
                        fout.write(word + '\n')
                        word_count += 1

        # 处理剩余 buffer
        if buffer:
            cleaned = re.sub(r'[^a-z\s]', ' ', buffer.lower())
            words = cleaned.split()
            for word in words:
                if word:
                    fout.write(word + '\n')
                    word_count += 1

    print(f"Preprocessing done. Total words: {word_count}", file=sys.stderr)

def main():
    if len(sys.argv) != 3:
        print("Usage: python preprocess.py <raw_corpus.txt> <clean_words.txt>")
        sys.exit(1)
    clean_and_tokenize(sys.argv[1], sys.argv[2])

if __name__ == "__main__":
    main()