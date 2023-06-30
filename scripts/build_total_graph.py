import pandas as pd
import numpy as np
import networkx as nx
import re
import os
import json

from graph import *
from csv2graph import *

if __name__ == '__main__':

    # 跑整个文件夹文件的思路：分batch进行构图逐步添加关系，每添加几个文件后就进行剪枝。目前尝试batch=5还是太慢了。可能是剪枝的度还没控制好()，也可能和剪枝算法还有关系
    # 剪枝的度是需要尝试的。TODO：也可以维护一个变量 max_deg 存储最大的度。 n 就设置为 max_deg * 70%
    # 可以使用graph.profile函数对图的情况进行分析，方便选取剪枝参数n。具体见profile函数

    filename_list = os.listdir('../data/2022年全国高考A平台数据')
    # filename_list  # len = 49, 选择batch = 5
    graph = Graph()

    # batch 1
    for csv_file in filename_list[0:5]:
        add_csv_to_graph(graph, 'data/2022年全国高考A平台数据/' + csv_file)
        print('finish read ' + csv_file)
    graph.pruning(7)
    print('=' * 100)
    graph.print_graph()

    # batch 2
    for csv_file in filename_list[5:10]:
        add_csv_to_graph(graph, 'data/2022年全国高考A平台数据/' + csv_file)
        print('finish read ' + csv_file)
    graph.pruning(50)
    print('=' * 100)
    graph.print_graph()

    # batch 3
    for csv_file in filename_list[10:15]:
        add_csv_to_graph(graph, 'data/2022年全国高考A平台数据/' + csv_file)
        print('finish read ' + csv_file)
    print('=' * 100)
    graph.print_graph()