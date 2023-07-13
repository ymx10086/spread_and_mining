import pandas as pd
import numpy as np
import networkx as nx
import re
import os
import json

from graph import *
from read_data import *


def add_csv_to_graph(cur_graph: Graph, filename: str):
    """
    把一个csv文件中的关系添加到图中
    """
    cur_data = read_data(filename)
    print(f'read file {filename}')
    for record in cur_data:
        add_edges_from_comment_dict(cur_graph, record['comment'], record['context'], record['comment_num'], record['like_num'], record['forward_num'])


def check_user_in_known_list(graph: Graph, user: Node) -> bool:  # TODO: if use {id:Node} as the data structure, then we don't need to use these two functions.
    """
    查看user是否已经在图的节点集合中
    """
    for known_user in graph.known_users:
        if known_user.user_id == user.user_id:
            return True
    return False

def get_user_in_known_list(graph: Graph, user: Node) -> Node:
    """
    获取节点集合中已经存在的对应节点
    """
    for known_user in graph.known_users:
        if known_user.user_id == user.user_id:
            return known_user

def add_edges_from_comment_dict(graph: Graph, comment_chain: dict, context: str, comment_num, like_num, forward_num):
    """
    根据转发链字典添加边
    :param comment_chain: 转发链
    """
    if comment_chain is None:
        return
    key_list = list(comment_chain.keys())
    for i in range(1, len(key_list)):  # TODO: 如果转发链只有unknown-->user，这个user将直接被舍弃
        # print(f'add relation {key_list[i-1]} -> {key_list[i]}')
        edge = Edge(comment_chain[key_list[i-1]], key_list[i-1], key_list[i], forward_num, comment_num, like_num)
        user1 = Node(key_list[i-1])
        user2 = Node(key_list[i])
        if check_user_in_known_list(graph, user1) and check_user_in_known_list(graph, user2):
            user_known1 = get_user_in_known_list(graph, user1)
            user_known2 = get_user_in_known_list(graph, user2)
            user_known1.add_forward(edge)
            user_known2.add_forward_by(edge)
        elif check_user_in_known_list(graph, user1):
            user_known1 = get_user_in_known_list(graph, user1)
            user_known1.add_forward(edge)
            user2.add_forward_by(edge)
            graph.add_known_user(user2)
        elif check_user_in_known_list(graph, user2):
            user_known2 = get_user_in_known_list(graph, user2)
            user_known2.add_forward_by(edge)
            user1.add_forward(edge)
            graph.add_known_user(user1)
        else:
            user1.add_forward(edge)
            user2.add_forward_by(edge)
            graph.add_known_user(user1)
            graph.add_known_user(user2)


if __name__ == '__main__':
    graph = Graph()
    add_csv_to_graph(graph, "../data/2022年全国高考A平台数据/34918267.csv")
    print('=' * 100)
    graph.print_graph()
    graph.to_json_file('../data/json/graph.json')

    # nodes: {节点名：{出边:[{}， {}，...], 入边：[{}, ...]}, 节点名：{出边:[{}， {}，...], 入边：[{}, ...]}, ...}