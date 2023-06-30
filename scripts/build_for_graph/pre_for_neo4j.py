# coding=gbk
import pandas as pd
import numpy as np
import re
import os
import json

# 读取json文件，导出结点csv文件和边csv文件
def main(filename: str):
    # 读取json文件filename
    data = json.load(open(filename, 'r', encoding='utf-8'))
    data = data['nodes']
    # 生成结点csv文件的列名
    colomn = ["entity:ID", "name", ":LABEL"]
    entity = {}
    cnt = 0
    for keys in data.keys():
        entity[keys] = "entity" + str(cnt)
        cnt += 1
    # 将结点信息写入结点csv文件
    entity_df = pd.DataFrame(columns=colomn)
    for keys in data.keys():
        entity_df = pd.concat([entity_df, pd.DataFrame([[entity[keys], keys, "User"]], columns=colomn)], axis = 0)
    entity_df.to_csv("../../data/csv/entity.csv", index=False, encoding='utf-8')

    # 生成边csv文件的列名
    colomn = [":START_ID", ":END_ID", ":TYPE", "content", "forward_num", "comment_num", "like_num"]
    # 将边信息写入边csv文件
    edge_df = pd.DataFrame(columns=colomn)
    for keys in data.keys():
        for items in data[keys]['forward_edges']:
            edge_df = pd.concat([edge_df, pd.DataFrame([[entity[items["from_user"]], entity[items['to_user']], "forward", items['content'], items['forward_num'], items['comment_num'], items['likes_num']]], columns=colomn)], axis = 0)
        for items in data[keys]['forward_by_edges']:
            edge_df = pd.concat([edge_df, pd.DataFrame([[entity[items["from_user"]], entity[items['to_user']], "backward", items['content'], items['forward_num'], items['comment_num'], items['likes_num']]], columns=colomn)], axis = 0)
    edge_df.to_csv("../../data/csv/edge.csv", index=False, encoding='utf-8')

if __name__ == '__main__':
    filename = '../../data/json/graph.json'
    main(filename=filename)