#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
内存架构性能评估脚本
用于评估DDR3、DDR4和HBM2三种内存架构的性能指标
包括带宽、延迟和能耗等关键性能参数
"""

import os
import sys
import json
import subprocess
import time
import csv
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

# 定义内存配置文件路径
CONFIGS = {
    "DDR3": "/home/ubuntu/DRAMsim3/configs/DDR3_4Gb_x4_1600.ini",
    "DDR4": "/home/ubuntu/DRAMsim3/configs/DDR4_4Gb_x4_1866.ini",
    "HBM2": "/home/ubuntu/DRAMsim3/configs/HBM2_4Gb_x128.ini"
}

# 定义负载类型
WORKLOADS = {
    "random": "随机访问模式",
    "stream": "流式访问模式",
    "matrix": "矩阵运算模式",
    "sort": "排序算法模式",
    "ai": "AI训练模式"
}

# 定义仿真参数
SIM_CYCLES = {
    "short": 10000,    # 短时仿真
    "medium": 100000,  # 中等时长仿真
    "long": 1000000    # 长时仿真
}

# 定义结果输出目录
OUTPUT_DIR = "/home/ubuntu/memory_benchmark_results"
DRAMSIM3_EXEC = "/home/ubuntu/DRAMsim3/build/dramsim3main"

# 创建输出目录
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 创建结果CSV文件
results_file = os.path.join(OUTPUT_DIR, f"memory_benchmark_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
with open(results_file, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow([
        "内存类型", "负载类型", "仿真周期数", "平均带宽(GB/s)", 
        "平均读延迟(ns)", "平均功耗(mW)", "总能耗(nJ)", 
        "读命令数", "写命令数", "行命中率(%)"
    ])

def generate_trace_file(workload_type, trace_file, size=1000):
    """
    生成不同类型的访问模式的trace文件
    
    参数:
    workload_type: 负载类型
    trace_file: 输出的trace文件路径
    size: trace大小
    """
    with open(trace_file, 'w') as f:
        if workload_type == "matrix":
            # 矩阵运算模式: 模拟矩阵乘法的内存访问模式
            # 假设两个NxN矩阵相乘，每个元素4字节
            N = 32  # 矩阵大小
            base_addr = 0x10000000
            
            # 模拟矩阵A的行访问和矩阵B的列访问
            for i in range(N):
                for j in range(N):
                    # 读取矩阵A的一行
                    for k in range(N):
                        addr_a = base_addr + (i * N + k) * 4
                        f.write(f"0 READ 0x{addr_a:x}\n")
                    
                    # 读取矩阵B的一列
                    for k in range(N):
                        addr_b = base_addr + 0x10000 + (k * N + j) * 4
                        f.write(f"{k+1} READ 0x{addr_b:x}\n")
                    
                    # 写入结果矩阵C
                    addr_c = base_addr + 0x20000 + (i * N + j) * 4
                    f.write(f"{N+1} WRITE 0x{addr_c:x}\n")
        
        elif workload_type == "sort":
            # 排序算法模式: 模拟快速排序的内存访问模式
            # 随机访问数组元素，然后写回
            base_addr = 0x20000000
            array_size = 1000
            
            # 模拟快速排序的分区过程
            for i in range(size):
                # 随机读取数组元素
                idx1 = np.random.randint(0, array_size)
                idx2 = np.random.randint(0, array_size)
                
                # 读取两个元素
                f.write(f"{i*3} READ 0x{base_addr + idx1*4:x}\n")
                f.write(f"{i*3+1} READ 0x{base_addr + idx2*4:x}\n")
                
                # 写回交换后的元素
                f.write(f"{i*3+2} WRITE 0x{base_addr + idx1*4:x}\n")
                f.write(f"{i*3+3} WRITE 0x{base_addr + idx2*4:x}\n")
        
        elif workload_type == "ai":
            # AI训练模式: 模拟神经网络训练的内存访问模式
            # 前向传播: 读取权重和输入
            # 反向传播: 读取梯度，更新权重
            base_addr = 0x30000000
            layer_size = 1024  # 每层神经元数量
            batch_size = 32    # 批处理大小
            
            for batch in range(min(batch_size, size // 100)):
                # 前向传播
                for layer in range(3):  # 假设3层网络
                    weight_addr = base_addr + layer * layer_size * 4
                    input_addr = base_addr + 0x100000 + batch * layer_size * 4
                    output_addr = base_addr + 0x200000 + batch * layer_size * 4
                    
                    # 读取权重和输入
                    for i in range(min(layer_size, 100)):
                        time_offset = batch * 1000 + layer * 100 + i
                        f.write(f"{time_offset} READ 0x{weight_addr + i*4:x}\n")
                        f.write(f"{time_offset+1} READ 0x{input_addr + i*4:x}\n")
                    
                    # 写入输出
                    for i in range(min(layer_size, 50)):
                        time_offset = batch * 1000 + layer * 100 + 50 + i
                        f.write(f"{time_offset} WRITE 0x{output_addr + i*4:x}\n")
                
                # 反向传播
                for layer in range(2, -1, -1):
                    grad_addr = base_addr + 0x300000 + layer * layer_size * 4
                    weight_addr = base_addr + layer * layer_size * 4
                    
                    # 读取梯度
                    for i in range(min(layer_size, 100)):
                        time_offset = batch * 1000 + 500 + (2-layer) * 100 + i
                        f.write(f"{time_offset} READ 0x{grad_addr + i*4:x}\n")
                    
                    # 更新权重
                    for i in range(min(layer_size, 50)):
                        time_offset = batch * 1000 + 500 + (2-layer) * 100 + 50 + i
                        f.write(f"{time_offset} READ 0x{weight_addr + i*4:x}\n")
                        f.write(f"{time_offset+1} WRITE 0x{weight_addr + i*4:x}\n")
        else:
            # 默认随机访问模式
            for i in range(size):
                # 随机地址
                addr = np.random.randint(0x10000000, 0x20000000)
                # 随机读写
                op = "READ" if np.random.random() < 0.7 else "WRITE"  # 70%读，30%写
                f.write(f"{i} {op} 0x{addr:x}\n")

def run_simulation(memory_type, workload_type, cycles, output_dir=OUTPUT_DIR):
    """
    运行内存架构仿真
    
    参数:
    memory_type: 内存类型 (DDR3, DDR4, HBM2)
    workload_type: 负载类型 (random, stream, matrix, sort, ai)
    cycles: 仿真周期数
    output_dir: 输出目录
    
    返回:
    性能指标字典
    """
    print(f"运行仿真: {memory_type}, {workload_type}, {cycles} 周期")
    
    # 创建特定内存类型和负载的输出目录
    sim_output_dir = os.path.join(output_dir, f"{memory_type}_{workload_type}_{cycles}")
    os.makedirs(sim_output_dir, exist_ok=True)
    
    # 构建命令
    cmd = [DRAMSIM3_EXEC, CONFIGS[memory_type], "-c", str(cycles), "-o", sim_output_dir]
    
    # 对于内置的random和stream负载，直接使用-s参数
    if workload_type in ["random", "stream"]:
        cmd.extend(["-s", workload_type])
    else:
        # 对于自定义负载，生成trace文件并使用-t参数
        trace_file = os.path.join(sim_output_dir, f"{workload_type}_trace.txt")
        generate_trace_file(workload_type, trace_file)
        cmd.extend(["-t", trace_file])
    
    # 运行仿真
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # 解析结果
        json_file = os.path.join(sim_output_dir, "dramsim3.json")
        if os.path.exists(json_file):
            with open(json_file, 'r') as f:
                data = json.load(f)
                
                # 提取关键性能指标
                channel_data = data.get("0", {})  # 假设只有一个通道
                
                # 计算性能指标
                bandwidth = channel_data.get("average_bandwidth", 0)  # GB/s
                read_latency = channel_data.get("average_read_latency", 0)  # 周期数
                power = channel_data.get("average_power", 0)  # mW
                energy = channel_data.get("total_energy", 0)  # nJ
                
                # 命令统计
                read_cmds = channel_data.get("num_read_cmds", 0)
                write_cmds = channel_data.get("num_write_cmds", 0)
                
                # 计算行命中率
                read_row_hits = channel_data.get("num_read_row_hits", 0)
                write_row_hits = channel_data.get("num_write_row_hits", 0)
                total_cmds = read_cmds + write_cmds
                row_hit_rate = 0
                if total_cmds > 0:
                    row_hit_rate = (read_row_hits + write_row_hits) / total_cmds * 100
                
                # 转换延迟从周期数到纳秒
                # 根据不同内存类型的tCK值转换
                tCK = 1.25  # DDR3默认值 (ns)
                if memory_type == "DDR4":
                    tCK = 1.07  # DDR4默认值 (ns)
                elif memory_type == "HBM2":
                    tCK = 1.0   # HBM2默认值 (ns)
                
                read_latency_ns = read_latency * tCK
                
                # 返回性能指标
                return {
                    "memory_type": memory_type,
                    "workload_type": workload_type,
                    "cycles": cycles,
                    "bandwidth": bandwidth,
                    "read_latency": read_latency_ns,
                    "power": power,
                    "energy": energy,
                    "read_cmds": read_cmds,
                    "write_cmds": write_cmds,
                    "row_hit_rate": row_hit_rate
                }
        else:
            print(f"错误: 未找到结果文件 {json_file}")
            return None
    except subprocess.CalledProcessError as e:
        print(f"仿真运行错误: {e}")
        return None
    except Exception as e:
        print(f"处理结果时出错: {e}")
        return None

def plot_results(results, output_dir=OUTPUT_DIR):
    """
    绘制性能对比图表
    
    参数:
    results: 性能结果列表
    output_dir: 输出目录
    """
    # 按内存类型分组
    memory_types = set(r["memory_type"] for r in results)
    workload_types = set(r["workload_type"] for r in results)
    
    # 带宽对比图
    plt.figure(figsize=(12, 8))
    bar_width = 0.2
    index = np.arange(len(workload_types))
    
    for i, mem_type in enumerate(sorted(memory_types)):
        bandwidths = [r["bandwidth"] for r in results if r["memory_type"] == mem_type]
        workloads = [r["workload_type"] for r in results if r["memory_type"] == mem_type]
        
        # 确保顺序一致
        sorted_data = []
        for wl in sorted(workload_types):
            for j, w in enumerate(workloads):
                if w == wl:
                    sorted_data.append(bandwidths[j])
                    break
            else:
                sorted_data.append(0)
        
        plt.bar(index + i*bar_width, sorted_data, bar_width, label=mem_type)
    
    plt.xlabel('负载类型')
    plt.ylabel('带宽 (GB/s)')
    plt.title('不同内存架构在各种负载下的带宽对比')
    plt.xticks(index + bar_width, sorted(workload_types))
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'bandwidth_comparison.png'))
    
    # 延迟对比图
    plt.figure(figsize=(12, 8))
    
    for i, mem_type in enumerate(sorted(memory_types)):
        latencies = [r["read_latency"] for r in results if r["memory_type"] == mem_type]
        workloads = [r["workload_type"] for r in results if r["memory_type"] == mem_type]
        
        # 确保顺序一致
        sorted_data = []
        for wl in sorted(workload_types):
            for j, w in enumerate(workloads):
                if w == wl:
                    sorted_data.append(latencies[j])
                    break
            else:
                sorted_data.append(0)
        
        plt.bar(index + i*bar_width, sorted_data, bar_width, label=mem_type)
    
    plt.xlabel('负载类型')
    plt.ylabel('读延迟 (ns)')
    plt.title('不同内存架构在各种负载下的读延迟对比')
    plt.xticks(index + bar_width, sorted(workload_types))
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'latency_comparison.png'))
    
    # 能耗对比图
    plt.figure(figsize=(12, 8))
    
    for i, mem_type in enumerate(sorted(memory_types)):
        power_values = [r["power"] for r in results if r["memory_type"] == mem_type]
        workloads = [r["workload_type"] for r in results if r["memory_type"] == mem_type]
        
        # 确保顺序一致
        sorted_data = []
        for wl in sorted(workload_types):
            for j, w in enumerate(workloads):
                if w == wl:
                    sorted_data.append(power_values[j])
                    break
            else:
                sorted_data.append(0)
        
        plt.bar(index + i*bar_width, sorted_data, bar_width, label=mem_type)
    
    plt.xlabel('负载类型')
    plt.ylabel('功耗 (mW)')
    plt.title('不同内存架构在各种负载下的功耗对比')
    plt.xticks(index + bar_width, sorted(workload_types))
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'power_comparison.png'))
    
    # 行命中率对比图
    plt.figure(figsize=(12, 8))
    
    for i, mem_type in enumerate(sorted(memory_types)):
        hit_rates = [r["row_hit_rate"] for r in results if r["memory_type"] == mem_type]
        workloads = [r["workload_type"] for r in results if r["memory_type"] == mem_type]
        
        # 确保顺序一致
        sorted_data = []
        for wl in sorted(workload_types):
            for j, w in enumerate(workloads):
                if w == wl:
                    sorted_data.append(hit_rates[j])
                    break
            else:
                sorted_data.append(0)
        
        plt.bar(index + i*bar_width, sorted_data, bar_width, label=mem_type)
    
    plt.xlabel('负载类型')
    plt.ylabel('行命中率 (%)')
    plt.title('不同内存架构在各种负载下的行命中率对比')
    plt.xticks(index + bar_width, sorted(workload_types))
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'row_hit_rate_comparison.png'))

def main():
    """主函数，运行所有仿真并生成报告"""
    print("开始内存架构性能评估...")
    
    # 存储所有结果
    all_results = []
    
    # 运行所有仿真组合
    for memory_type in CONFIGS.keys():
        for workload_type in ["random", "stream", "matrix", "sort", "ai"]:
            # 使用中等长度的仿真周期
            cycles = SIM_CYCLES["medium"]
            
            # 运行仿真
            result = run_simulation(memory_type, workload_type, cycles)
            
            if result:
                all_results.append(result)
                
                # 将结果写入CSV
                with open(results_file, 'a', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow([
                        result["memory_type"],
                        result["workload_type"],
                        result["cycles"],
                        result["bandwidth"],
                        result["read_latency"],
                        result["power"],
                        result["energy"],
                        result["read_cmds"],
                        result["write_cmds"],
                        result["row_hit_rate"]
                    ])
    
    # 绘制结果图表
    if all_results:
        plot_results(all_results)
        print(f"结果已保存到 {OUTPUT_DIR}")
    else:
        print("没有有效的仿真结果")

if __name__ == "__main__":
    main()
