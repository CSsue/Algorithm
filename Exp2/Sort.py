import random
import time
import copy
import tracemalloc
import pandas as pd


# -------------------- 排序算法实现 --------------------
def insertion_sort(arr):
    """插入排序 - IS"""
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr


def top_down_merge_sort(arr):
    """自顶向下归并排序 - TDM"""
    if len(arr) <= 1:
        return arr

    """合并两个有序数组"""
    def merge(left, right):
        result = []
        i = j = 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        # 添加剩余元素
        result.extend(left[i:])
        result.extend(right[j:])
        return result

    mid = len(arr) // 2
    left = top_down_merge_sort(arr[:mid])
    right = top_down_merge_sort(arr[mid:])
    return merge(left, right)


def bottom_up_merge_sort(arr):
    """自底向上归并排序 - BUM"""
    n = len(arr)
    if n <= 1:
        return arr

    # 创建临时数组
    temp = arr.copy()
    width = 1

    while width < n:
        for i in range(0, n, 2 * width):
            left = i
            mid = min(i + width, n)
            right = min(i + 2 * width, n)

            # 归并操作
            i1, i2, j = left, mid, left
            while i1 < mid and i2 < right:
                if arr[i1] <= arr[i2]:
                    temp[j] = arr[i1]
                    i1 += 1
                else:
                    temp[j] = arr[i2]
                    i2 += 1
                j += 1

            # 处理剩余元素
            while i1 < mid:
                temp[j] = arr[i1]
                i1 += 1
                j += 1

            while i2 < right:
                temp[j] = arr[i2]
                i2 += 1
                j += 1

            # 复制回原数组
            for k in range(left, right):
                arr[k] = temp[k]

        width *= 2
    return arr


def quick_sort_random(arr):
    """随机枢轴快速排序 - RQ"""

    def qsort(a, l, r):
        if l >= r:
            return
        # 随机选择枢轴
        pivot_idx = random.randint(l, r)
        pivot = a[pivot_idx]

        # 三路划分
        i, j, k = l, l, r
        while j <= k:
            if a[j] < pivot:
                a[i], a[j] = a[j], a[i]
                i += 1
                j += 1
            elif a[j] > pivot:
                a[j], a[k] = a[k], a[j]
                k -= 1
            else:
                j += 1

        qsort(a, l, i - 1)
        qsort(a, k + 1, r)

    qsort(arr, 0, len(arr) - 1)
    return arr


def quick_sort_3way(arr):
    """三路快速排序 - QD3P"""

    def qsort(a, l, r):
        if l >= r:
            return

        lt, i, gt = l, l + 1, r
        pivot = a[l]

        while i <= gt:
            if a[i] < pivot:
                a[lt], a[i] = a[i], a[lt]
                lt += 1
                i += 1
            elif a[i] > pivot:
                a[i], a[gt] = a[gt], a[i]
                gt -= 1
            else:
                i += 1

        qsort(a, l, lt - 1)
        qsort(a, gt + 1, r)

    qsort(arr, 0, len(arr) - 1)
    return arr


# -------------------- 单次测试函数 --------------------
def run_single_test(algorithm, data, run_number):
    """
    单次测试运行
    返回: (运行时间μs, 峰值内存KB)
    """
    # 深拷贝数据以避免修改原数组
    test_data = copy.deepcopy(data)

    # 开始内存跟踪
    tracemalloc.start()

    # 记录开始时间
    start_time = time.perf_counter()

    # 执行排序算法
    algorithm(test_data)

    # 记录结束时间
    end_time = time.perf_counter()

    # 获取内存使用情况
    current_memory, peak_memory = tracemalloc.get_traced_memory()

    # 停止内存跟踪
    tracemalloc.stop()

    # 计算运行时间（微秒）
    run_time = (end_time - start_time) * 1e6  # 转换为μs

    # 计算峰值内存（KB）
    peak_memory_kb = peak_memory / 1024  # 转换为KB

    # 输出单次运行结果
    print(f"      第{run_number:2d}次: 时间={run_time:8.2f}μs, 内存={peak_memory_kb:8.2f}KB")

    return run_time, peak_memory_kb


# -------------------- 验证排序正确性 --------------------
def verify_sorting(algorithm, data):
    """验证排序算法的正确性"""
    test_data = copy.deepcopy(data)
    sorted_data = sorted(test_data)  # Python内置排序作为基准

    algorithm_result = algorithm(copy.deepcopy(test_data))

    if algorithm_result is not None:
        algorithm_sorted = algorithm_result
    else:
        algorithm_sorted = test_data

    return algorithm_sorted == sorted_data


# -------------------- 主测试函数 --------------------
def main():
    """主测试函数"""
    # 定义算法字典
    algorithms = {
        'IS': insertion_sort,
        'TDM': top_down_merge_sort,
        'BUM': bottom_up_merge_sort,
        'RQ': quick_sort_random,
        'QD3P': quick_sort_3way
    }

    # 定义测试规模
    sizes = [100, 1000, 5000]

    # 每个算法运行次数
    runs = 10

    # 存储结果的列表
    time_results = []
    memory_results = []

    # 存储详细运行记录的列表
    detailed_records = []

    print("开始排序算法性能测试...")
    print("=" * 80)

    # 验证算法正确性
    print("验证算法正确性...")
    test_data_small = [random.randint(0, 1000) for _ in range(100)]
    for algo_name, algo_func in algorithms.items():
        is_correct = verify_sorting(algo_func, test_data_small)
        status = "✓ 正确" if is_correct else "✗ 错误"
        print(f"  {algo_name}: {status}")

    print("\n开始性能测试...")

    # 对每个规模进行测试
    for size in sizes:
        print(f"\n{'=' * 80}")
        print(f"测试规模: {size} 个元素")
        print(f"{'=' * 80}")

        # 生成测试数据（使用较大范围避免重复值过多）
        data = [random.randint(0, size * 10) for _ in range(size)]

        # 对每个算法进行测试
        for algo_name, algo_func in algorithms.items():
            print(f"\n算法 {algo_name}:")
            print(f"  {'-' * 60}")

            # 跳过在大数据量下过慢的插入排序
            if algo_name == 'IS' and size > 10000:
                print("  跳过测试（数据量过大，插入排序性能较差）")
                continue

            time_sum = 0.0
            memory_sum = 0.0
            run_times = []
            run_memories = []

            # 运行10次
            for run in range(1, runs + 1):
                run_time, peak_memory = run_single_test(algo_func, data, run)
                time_sum += run_time
                memory_sum += peak_memory
                run_times.append(run_time)
                run_memories.append(peak_memory)

                # 记录详细数据
                detailed_records.append({
                    '算法': algo_name,
                    '规模': size,
                    '运行次数': run,
                    '时间μs': round(run_time, 2),
                    '内存KB': round(peak_memory, 2)
                })

            # 计算平均值
            avg_time = time_sum / runs
            avg_memory = memory_sum / runs

            # 输出该算法的统计信息
            print(f"  {'-' * 60}")
            print(f"  统计信息:")
            print(f"    平均时间: {avg_time:8.2f}μs")
            print(f"    平均内存: {avg_memory:8.2f}KB")
            print(f"    时间范围: {min(run_times):8.2f}μs - {max(run_times):8.2f}μs")
            print(f"    内存范围: {min(run_memories):8.2f}KB - {max(run_memories):8.2f}KB")

            # 存储结果
            time_results.append({
                '算法': algo_name,
                '规模': size,
                '平均时间μs': round(avg_time, 2),
                '最小时间μs': round(min(run_times), 2),
                '最大时间μs': round(max(run_times), 2)
            })

            memory_results.append({
                '算法': algo_name,
                '规模': size,
                '平均内存KB': round(avg_memory, 2),
                '最小内存KB': round(min(run_memories), 2),
                '最大内存KB': round(max(run_memories), 2)
            })

    # 创建数据框
    time_df = pd.DataFrame(time_results)
    memory_df = pd.DataFrame(memory_results)
    detailed_df = pd.DataFrame(detailed_records)

    # 转换为透视表以便更好的显示
    time_pivot = time_df.pivot(index='算法', columns='规模', values='平均时间μs')
    memory_pivot = memory_df.pivot(index='算法', columns='规模', values='平均内存KB')

    # 输出详细运行记录
    print(f"\n{'=' * 80}")
    print("详细运行记录")
    print(f"{'=' * 80}")

    # 按算法和规模分组显示详细记录
    for size in sizes:
        print(f"\n规模 {size}:")
        size_data = detailed_df[detailed_df['规模'] == size]
        for algo_name in algorithms.keys():
            algo_data = size_data[size_data['算法'] == algo_name]
            if not algo_data.empty:
                print(f"\n  {algo_name}:")
                for _, row in algo_data.iterrows():
                    print(f"    第{row['运行次数']:2d}次: 时间={row['时间μs']:8.2f}μs, 内存={row['内存KB']:8.2f}KB")

    # 输出结果表格
    print(f"\n{'=' * 80}")
    print("平均运行时间表 (μs)")
    print(f"{'=' * 80}")
    print(time_pivot)

    print(f"\n{'=' * 80}")
    print("平均内存使用表 (KB)")
    print(f"{'=' * 80}")
    print(memory_pivot)

    # 输出包含范围的详细表格
    print(f"\n{'=' * 80}")
    print("详细时间性能表 (μs)")
    print(f"{'=' * 80}")
    time_detail_table = time_df.pivot(index='算法', columns='规模',
                                      values=['平均时间μs', '最小时间μs', '最大时间μs'])
    print(time_detail_table)

    print(f"\n{'=' * 80}")
    print("详细内存性能表 (KB)")
    print(f"{'=' * 80}")
    memory_detail_table = memory_df.pivot(index='算法', columns='规模',
                                          values=['平均内存KB', '最小内存KB', '最大内存KB'])
    print(memory_detail_table)

    # 保存结果到CSV文件
    time_pivot.to_csv('排序算法时间性能.csv', encoding='utf-8-sig')
    memory_pivot.to_csv('排序算法内存性能.csv', encoding='utf-8-sig')
    detailed_df.to_csv('排序算法详细运行记录.csv', encoding='utf-8-sig', index=False)

    print(f"\n{'=' * 80}")
    print("结果文件已保存:")
    print("  - 排序算法时间性能.csv")
    print("  - 排序算法内存性能.csv")
    print("  - 排序算法详细运行记录.csv")
    print(f"{'=' * 80}")


# -------------------- 程序入口 --------------------
if __name__ == '__main__':
    main()