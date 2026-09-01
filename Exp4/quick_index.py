# 指针索引报错

# query_indexed.py
import sys
import re
import bisect

class TextIndex:
    """文本索引类，使用后缀数组实现"""
    
    def __init__(self, text):
        """初始化索引，构建后缀数组"""
        self.text = text
        self.length = len(text)
        
        print(f"文本长度: {self.length} 字符")
        print("正在构建后缀数组...")
        
        # 构建后缀数组：存储所有后缀的起始位置
        self.suffix_array = list(range(self.length))
        
        # 按后缀的字典序排序
        self.suffix_array.sort(key=lambda i: text[i:])
        
        print("后缀数组构建完成！")
    
    def search(self, query):
        """在索引中搜索查询字符串，返回(首次出现位置, 出现次数)"""
        if not query:
            return -1, 0
        
        query_len = len(query)
        print(f"搜索查询: '{query}' (长度: {query_len})")
        
        # 自定义比较函数
        def get_suffix_prefix(i):
            return self.text[i:i+query_len]
        
        # 使用二分查找找到第一个匹配的后缀
        lo = bisect.bisect_left(self.suffix_array, query, key=get_suffix_prefix)
        
        # 如果没有找到
        if lo == self.length or not self.text[self.suffix_array[lo]:].startswith(query):
            print(f"未找到查询: '{query}'")
            return -1, 0
        
        # 找到最后一个匹配的后缀
        hi = bisect.bisect_right(self.suffix_array, query, key=get_suffix_prefix)
        
        # 计算首次出现位置（1-based）
        first_pos = self.suffix_array[lo] + 1  # 转换为1-based索引
        
        # 统计出现次数
        count = hi - lo
        
        print(f"找到查询 '{query}': 首次出现位置={first_pos}, 出现次数={count}")
        return first_pos, count
    
    @classmethod
    def from_file(cls, filename):
        """从文件创建文本索引"""
        print(f"正在读取文件: {filename}")
        with open(filename, 'r', encoding='utf-8') as f:
            # 读取整个文本，保留换行符
            text = f.read()
        
        print(f"文件读取完成，长度: {len(text)} 字符")
        # 显示前200个字符预览
        preview = text[:200].replace('\n', '\\n').replace('\r', '\\r')
        print(f"文本预览: {preview}...")
        
        return cls(text)

def clean_query(query):
    """清理查询字符串：只保留小写字母、空格和换行符"""
    print(f"原始查询: '{query}'")
    
    # 转换为小写
    query = query.lower()
    print(f"转换为小写: '{query}'")
    
    # 只保留字母和空格
    query = re.sub(r'[^a-z\s]', ' ', query)
    print(f"清理后: '{query}'")
    
    # 合并多个空格
    query = re.sub(r'\s+', ' ', query).strip()
    print(f"最终查询: '{query}'")
    
    return query

def main():
    # 检查命令行参数
    print("=" * 60)
    print("文本索引搜索程序")
    print("=" * 60)
    
    print(f"命令行参数: {sys.argv}")
    
    if len(sys.argv) != 3:
        print("用法错误!")
        print("正确用法: python query_indexed.py <语料库文件> <查询文件>")
        print("示例: python query_indexed.py corpus.txt queries.txt")
        print(f"当前参数个数: {len(sys.argv)}")
        for i, arg in enumerate(sys.argv):
            print(f"  参数[{i}]: {arg}")
        sys.exit(1)
    
    corpus_file = sys.argv[1]
    query_file = sys.argv[2]
    
    print(f"语料库文件: {corpus_file}")
    print(f"查询文件: {query_file}")
    
    try:
        # 检查文件是否存在
        import os
        if not os.path.exists(corpus_file):
            print(f"错误: 语料库文件 '{corpus_file}' 不存在!")
            sys.exit(1)
        if not os.path.exists(query_file):
            print(f"错误: 查询文件 '{query_file}' 不存在!")
            sys.exit(1)
        
        # 构建文本索引
        print("\n" + "=" * 60)
        print("开始构建索引...")
        index = TextIndex.from_file(corpus_file)
        
        # 读取查询
        print("\n" + "=" * 60)
        print(f"读取查询文件: {query_file}")
        with open(query_file, 'r', encoding='utf-8') as f:
            queries = [line.rstrip('\n') for line in f]
        
        print(f"找到 {len(queries)} 个查询:")
        for i, q in enumerate(queries):
            print(f"  查询[{i+1}]: '{q}'")
        
        # 处理每个查询
        print("\n" + "=" * 60)
        print("开始搜索查询...")
        print("-" * 60)
        
        results = []
        for query in queries:
            if not query.strip():
                print("跳过空查询")
                results.append((query, -1, 0))
                continue
                
            print(f"\n处理查询: '{query}'")
            # 清理查询
            clean_q = clean_query(query)
            
            if not clean_q:
                print("查询清理后为空")
                results.append((query, -1, 0))
                continue
            
            # 在索引中搜索
            first_pos, count = index.search(clean_q)
            results.append((query, first_pos, count))
        
        # 输出结果
        print("\n" + "=" * 60)
        print("搜索结果汇总:")
        print("-" * 60)
        
        for query, first_pos, count in results:
            if count == 0:
                print(f"-- 0 {query}")
            else:
                print(f"{first_pos} {count} {query}")
        
        print("\n" + "=" * 60)
        print("程序执行完成!")
        
    except FileNotFoundError as e:
        print(f"错误: 文件未找到 - {e}")
        sys.exit(1)
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()