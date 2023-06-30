import pandas as pd
import numpy as np
import networkx as nx
import re
import os
import json


class Edge:
    def __init__(self, content, from_user, to_user, foward_num, comment_num, like_num) -> None:
        """
        边的构造函数
        A转发B : from_user = A, to_user = B
        """
        self.content = content
        self.from_user = from_user
        self.to_user = to_user
        self.foward_num = foward_num
        self.comment_num = comment_num
        self.like_num = like_num

    def str_equal(self, edge):
        """
        通过content比较是否是同一条边。在边的去重时有用
        """
        return self.content == edge.content
    
    def __eq__(self, other) -> bool:
        """
        通过比较content+from_user+to_user比较是否是同一条边。边的去重时有用
        (注意：随时间变化转发链中的内容/点赞数可能会有不同(这应该是由于数据爬取过程中信息发生了变化)。去重时不可能考虑到所有情况，尽量使重复边比较少)
        """
        return self.content == other.content and self.from_user == other.from_user and self.to_user == other.to_user

    def print_edge(self):
        return "(" + str(self.from_user) + ", " + str(self.to_user) + ")"

class Node:
    def __init__(self, user_id) -> None:
        """
        节点构造函数。一个用户抽象为一个节点
        forward: 当前用户引用其他用户产生的边
        forward_by: 当前用户被其他用户引用产生的边。A-->B-->C中, (A, B)就是在B的forward_by中
        """
        self.user_id = user_id
        self.forward: list[Edge] = []
        self.forward_by: list[Edge] = []

    def add_forward(self, forward_edge: Edge):
        """
        添加边。已经考虑去重
        下同
        """
        if forward_edge not in self.forward:
            self.forward.append(forward_edge)

    def add_forward_by(self, forward_by_edge: Edge):
        if forward_by_edge not in self.forward_by:
            self.forward_by.append(forward_by_edge)

    def remove_forward(self, forward_edge: Edge):
        self.forward.remove(forward_edge)

    def remove_forward_by(self, forward_by_edge: Edge):
        self.forward_by.remove(forward_by_edge)

    def get_deg(self):
        """
        获取节点的度。即入度+出度
        """
        return len(self.forward) + len(self.forward_by)  # TODO: ?

    
class Graph:
    def __init__(self) -> None:
        """
        整张图的构造函数。图中只存储节点
        """
        self.known_users: list[Node] = []
        
    def add_known_user(self, known_user):
        self.known_users.append(known_user)

    def print_graph(self):
        """
        用邻接表(user_id:[edge1, edge2, ...])的形式打印图
        """
        print("print known user list")
        for known_user in self.known_users:
            print(f'{known_user.user_id}: {[edge.print_edge() for edge in known_user.forward]}')

    def get_nodes(self, n):
        """
        获取节点(只挑选度 >= n 的节点)。画图用
        """
        nodes = []
        nodes.extend([user.user_id for user in self.known_users if user.get_deg() >= n])
        return nodes
    
    def get_edges(self, n):
        """
        获取边。画图用
        """
        nodes = self.get_nodes(n)
        edges = []
        for user in self.known_users:
            for edge in user.forward:
                if edge.from_user in nodes or edge.to_user in nodes:
                    edges.append((edge.from_user, edge.to_user))
        return list(edges)
    
    def get_user_by_id(self, user_id):
        """
        通过user_id获取节点
        """
        for user in self.known_users:
            if user.user_id == user_id:
                return user
        return None
    
    
    def pruning(self, n):
        """
        剪枝。只保留度 > n 的那些节点.同时可以选择要不要把对应的边全部删除.
        TODO: 怎么剪枝比较重要，现在的剪枝方法剪掉的节点会影响其他节点的边数。最终的剪枝应该尽可能保留重要的节点，并且使画出来的图比较好看
        """
        for i in range(len(self.known_users) - 1, -1, -1):
            user = self.known_users[i]
            if user.get_deg() < n:
                self.remove_all_edges(user)  # 到底要不要删边？这个需要根据效果斟酌
                del self.known_users[i]

    def remove_all_edges(self, user: Node):  # 删除所有相关的边，主要是删除该边另一头节点边列表中的这条边
        for edge in user.forward:
            another_user = self.get_user_by_id(edge.to_user)
            if another_user is not None:
                another_user.remove_forward_by(edge)
        for edge in user.forward_by:
            another_user = self.get_user_by_id(edge.from_user)
            if another_user is not None:
                another_user.remove_forward(edge)

    def to_json(self):
        """
        转换为json格式，下同
        """
        top_dict = dict()
        nodes_dict = dict()
        for user in self.known_users:
            nodes_dict[user.user_id] = self.get_edge_info(user.user_id)
        top_dict["nodes"] = nodes_dict
        return top_dict
    
    def to_json_file(self, file_name):
        json_dict = self.to_json()
        with open(file=file_name, mode="w", encoding='utf-8') as f:
            json.dump(json_dict, f, indent=2, ensure_ascii=False)
        
    
    def get_edge_info(self, user_id):
        """
        获取边的属性dict
        """
        user = self.get_user_by_id(user_id)
        if user is None:
            return None
        forward_edges = []
        for edge in user.forward:
            edge_dict = dict()
            edge_dict['from_user'] = edge.from_user  # from_user == user.id
            edge_dict['to_user'] = edge.to_user
            edge_dict['content'] = edge.content
            edge_dict['comment_num'] = edge.comment_num
            edge_dict['likes_num'] = edge.like_num
            edge_dict['forward_num'] = edge.foward_num
            forward_edges.append(edge_dict)

        forward_by_edges = []
        for edge in user.forward_by:
            edge_dict = dict()
            edge_dict['from_user'] = edge.from_user  # to_user == user.id
            edge_dict['to_user'] = edge.to_user
            edge_dict['content'] = edge.content
            edge_dict['comment_num'] = edge.comment_num
            edge_dict['likes_num'] = edge.like_num
            edge_dict['forward_num'] = edge.foward_num
            forward_by_edges.append(edge_dict)
        return {'forward_edges':forward_edges, 'forward_by_edges':forward_by_edges}
    
    def profile(self):
        """
        返回图的最大度、节点数等信息，方便剪枝分析
        """
        max_deg = self.get_max_deg()
        num_nodes = len(self.get_nodes(0))  # 获取所有节点
        num_edges = len(self.get_edges(0))  # 获取所有边
        return {'max_deg':max_deg, 'num_nodes':num_nodes, 'num_edges':num_edges}


    def get_max_deg(self):
        """
        获取图中节点的最大度
        """
        max_deg = 0
        for user in self.known_users:
            max_deg = max(max_deg, user.get_deg())
        return max_deg