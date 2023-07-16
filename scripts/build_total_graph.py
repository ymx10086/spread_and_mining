import pandas as pd
import numpy as np
import networkx as nx
import re
import os
import json
import pickle
import argparse
import time

from graph import *
from csv2graph import *

def parse_args():
    parser = argparse.ArgumentParser(description="set parameters for build total graph")
    parser.add_argument("--mode", default='generate', help="generate: generate graph from raw csv files; profile: profile graphs; prune: prune graphs")
    parser.add_argument("--file_dir", default="../data/央视春晚D平台数据", help="which root file to build graph for")  # TODO: change this for reading different data
    parser.add_argument("--graph_bin_path", default='../graph_bin_data', help="save graph binary file")
    parser.add_argument("--batch_size", default=5, help="output a sub graph every `batch_size` csv files")
    parser.add_argument("--json_path", default='', help="json file output dir, if not: won't save json file")
    parser.add_argument("--prune_rate", default=0.7, help="prune ratio")
    parser.add_argument("--profile_result_path", default='./profile_result')
    parser.add_argument("--prune_result_path", default='./prune_result')
    
    
    args = parser.parse_args()
    return args

def read_one_batch(args, filename_list, start_idx, end_idx, output=True):
    graph = Graph()
    for csv_file in filename_list[start_idx:end_idx]:
        add_csv_to_graph(graph, os.path.join(args.file_dir, csv_file))
        print(f'finish read {os.path.join(args.file_dir, csv_file)}')
    bin_file_name = csv_file.split('.')[0] + '_checkpoint.graph'
    with open(os.path.join(args.graph_bin_path, bin_file_name), "wb") as f:
        pickle.dump(graph, f)
    if output and args.json_path is not None:
        graph.to_json_file(os.path.join(args.json_path, csv_file.split('.')[0] + '.json'))

if __name__ == '__main__':
    # 跑整个文件夹文件的思路：分batch进行构图逐步添加关系，每添加几个文件后就进行剪枝。目前尝试batch=5还是太慢了。可能是剪枝的度还没控制好()，也可能和剪枝算法还有关系
    # 剪枝的度是需要尝试的。TODO：也可以维护一个变量 max_deg 存储最大的度。 n 就设置为 max_deg * 70%
    # 可以使用graph.profile函数对图的情况进行分析，方便选取剪枝参数n。具体见profile函数
    args = parse_args()
    if args.json_path is not None:
        args.json_path = os.path.join(args.json_path, args.file_dir.split('/')[-1])
        if not os.path.exists(args.json_path):
            os.makedirs(args.json_path)
    if args.mode == 'generate':
        file_dir = args.file_dir
        batch_size = int(args.batch_size)
        bin_path = os.path.join(args.graph_bin_path, file_dir.split('/')[-1])
        if not os.path.exists(bin_path):
            os.makedirs(bin_path)
        args.graph_bin_path = bin_path
        print(f'generate graph from raw csv files under {file_dir}, batch size = {batch_size}, graph will be saved under {bin_path}')
        
        filename_list = os.listdir(file_dir)
        # filename_list  # len = 49
        for batch_num in range(1, (len(filename_list) - 1) // batch_size + 2):
            if batch_size * batch_num > len(filename_list):
                start_idx, end_idx = (batch_num - 1) * batch_size, len(filename_list)
            else:
                start_idx, end_idx = (batch_num - 1) * batch_size, batch_num * batch_size
            print(f'read batch {batch_num}')
            start = time.time()
            read_one_batch(args, filename_list, start_idx, end_idx)
            spend_time = time.time() - start
            print(f'finish read batch {batch_num}, spend {spend_time} s')
        print(f'finish generate.')
              
              
    elif args.mode == 'profile':
        if not os.path.exists(args.profile_result_path):
            os.makedirs(args.rofile_result_path)
        bin_path = args.graph_bin_path
        print(f'profile graphs under {bin_path}')
        filename_list = os.listdir(bin_path)
        for i in range(len(filename_list)):
            with open(filename_list[i], "rb") as f:
                graph = pickle.load(f)
                print(f'{filename_list[i]} : {graph.profile()}')
        print(f'finish profile.')
    
    
    if args.mode == 'prune':
        if not os.path.exists(args.prune_result_path):
            os.makedirs(args.prune_result_path)
        bin_path = args.graph_bin_path
        prune_result_path = args.prune_result_path
        prune_rate = args.prune_rate
        print(f'prune graphs under {bin_path}, prune ratio {prune_rate}, result will be saved under {prune_result_path}')
        filename_list = os.listdir(bin_path)
        for i in range(len(filename_list)):
            with open(filename_list[i], "rb") as f:
                graph = pickle.load(f)
                graph.pruning(graph.get_max_deg() * prune_rate)
                print(f'{filename_list[i]} after pruning: {graph.profile()}')
                with open(prune_result_path + filename_list[i].split()[0] + '.graph', "wb") as f1:
                    pickle.dump(graph, f1)
        print(f'finish pruning.')
        
