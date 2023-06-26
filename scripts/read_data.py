# coding=gbk
import numpy as np
import pandas as pd
import os
import sys
import matplotlib.pyplot as plt
import seaborn as sns
import re

# Path: scripts\read_data.py

# 正则匹配第一个//@前的内容，如果没有//@，则返回全部内容
def get_first_comment(text):
    """
    正则匹配第一个//@前的内容，如果没有//@，则返回全部内容
    :param text: 评论内容
    :return: 第一个//@前的内容
    """
    # 正则匹配第一个//@前的内容，如果没有//@，则返回全部内容
    pattern = re.compile(r'//@.*')
    # 匹配结果
    result = pattern.findall(text)
    # 如果没有//@，则返回全部内容
    if len(result) == 0:
        return text
    # 如果有//@，则返回第一个//@前的内容
    else:
        # return result[0]
        text = re.split(r'//@', text)
        return text[0]
    
# 正则匹配每一个//@后面的内容到下一个//@前的内容，如果没有//@，则返回//后的内容
def get_comment(text):
    """
    正则匹配每一个//@后面的内容到下一个//@前的内容，如果没有//@，则返回//后的内容
    :param text: 评论内容
    :return: 每一个//@后面的内容到下一个//@前的内容
    """
    # 正则匹配每一个//@后面的内容到下一个//@前的内容，如果没有//@，则返回//后的内容
    pattern = re.compile(r'//@.*')
    # 匹配结果
    result = pattern.findall(text)
    # 如果没有//@，则返回//后的内容
    if len(result) == 0:
        return []
    # 如果有//@，则返回每一个//@后面的内容到下一个//@前的内容
    else:
        # 以//@为分隔符，分割字符串
        result = re.split(r'//@', text)
        # 去掉第一个//@前的内容
        result = result[1:]
        ans = {}
        # 遍历每一个result，按照:分割字符串，前面的为key，后面的为value
        for i in range(len(result)):
            # 按照:分割字符串
            tmp = result[i].split(':')
            # 第一个元素为key，后面的字符串用:连接为value
            ans[tmp[0]] = ':'.join(tmp[1:])
        return ans


def read_data(filename : str):
    """
    读取数据
    :param filename: 数据文件名
    :return: 数据
    """
    # 读取数据
    data = pd.read_csv(filename, encoding='gbk', nrows=10)
    # 提取全文内容
    df = data['全文内容']
    # 提取第一个//@前的内容
    df_context = df.apply(get_first_comment)
    # 提取每一个//@后面的内容到下一个//@前的内容
    df_comment = df.apply(get_comment)
    # 将df_comment、df_context、data['标题／微博内容']、data['评论数']、data['点赞数']、data['转发数']合并为一个DataFrame
    data = pd.concat([df_context, df_comment, data['标题／微博内容'], data['评论数'], data['点赞数'], data['转发数']], axis=1)
    # 重命名列名
    data.columns = ['context', 'comment', 'title', 'comment_num', 'like_num', 'forward_num']
    # 写入文件
    # data.to_csv('../data/2022年全国高考A平台数据/34918267_new.csv', index=False, encoding='gbk')
    # 将data按照字典形式返回
    data = data.to_dict(orient='records')
    # 返回数据
    return data

if __name__ == '__main__':
    filename = '../data/2022年全国高考A平台数据/34918267.csv'
    data = read_data(filename)
    print(data)

    # 返回参数形式
    # context: 此评论自身内容
    # comment: 此评论下的相关转发评论，字典形式，key为评论者，value为评论内容
    # title: 标题
    # comment_num: 评论数
    # like_num: 点赞数
    # forward_num: 转发数
    # 例如：{'context': '[猪头]', 'comment': {'小铃铛-霖霖': 'http://t.cn/A6xAcwv4。??', ' 
    # 长江国际十八楼团霸': '宝贝好久不见呀～祝我的宝贝新的一年万事胜意！高考加油！今年就要成年啦～真的过得好快～我们的小宝贝就要十八岁啦！我希望我的宝贝要一直开心下去呀！'}, 'title': '[猪头]//@小铃铛-霖霖:http://t.cn/A6xAcwv4。??//@长江国际十八楼团霸:宝贝好久不见呀～祝我的宝贝新的一年万事胜意！高考加油！今年就要成年啦～真的过得好快～ 
    # 我们的小宝贝就要十八岁啦！我希望我的宝贝要一直开心下去呀！', 'comment_num': 0, 'like_num': 0, 'forward_num': 0}