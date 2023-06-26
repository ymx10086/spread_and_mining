# coding=gbk
import numpy as np
import pandas as pd
import os
import sys
import matplotlib.pyplot as plt
import seaborn as sns
import re

# Path: scripts\read_data.py

# ����ƥ���һ��//@ǰ�����ݣ����û��//@���򷵻�ȫ������
def get_first_comment(text):
    """
    ����ƥ���һ��//@ǰ�����ݣ����û��//@���򷵻�ȫ������
    :param text: ��������
    :return: ��һ��//@ǰ������
    """
    # ����ƥ���һ��//@ǰ�����ݣ����û��//@���򷵻�ȫ������
    pattern = re.compile(r'//@.*')
    # ƥ����
    result = pattern.findall(text)
    # ���û��//@���򷵻�ȫ������
    if len(result) == 0:
        return text
    # �����//@���򷵻ص�һ��//@ǰ������
    else:
        # return result[0]
        text = re.split(r'//@', text)
        return text[0]
    
# ����ƥ��ÿһ��//@��������ݵ���һ��//@ǰ�����ݣ����û��//@���򷵻�//�������
def get_comment(text):
    """
    ����ƥ��ÿһ��//@��������ݵ���һ��//@ǰ�����ݣ����û��//@���򷵻�//�������
    :param text: ��������
    :return: ÿһ��//@��������ݵ���һ��//@ǰ������
    """
    # ����ƥ��ÿһ��//@��������ݵ���һ��//@ǰ�����ݣ����û��//@���򷵻�//�������
    pattern = re.compile(r'//@.*')
    # ƥ����
    result = pattern.findall(text)
    # ���û��//@���򷵻�//�������
    if len(result) == 0:
        return []
    # �����//@���򷵻�ÿһ��//@��������ݵ���һ��//@ǰ������
    else:
        # ��//@Ϊ�ָ������ָ��ַ���
        result = re.split(r'//@', text)
        # ȥ����һ��//@ǰ������
        result = result[1:]
        ans = {}
        # ����ÿһ��result������:�ָ��ַ�����ǰ���Ϊkey�������Ϊvalue
        for i in range(len(result)):
            # ����:�ָ��ַ���
            tmp = result[i].split(':')
            # ��һ��Ԫ��Ϊkey��������ַ�����:����Ϊvalue
            ans[tmp[0]] = ':'.join(tmp[1:])
        return ans


def read_data(filename : str):
    """
    ��ȡ����
    :param filename: �����ļ���
    :return: ����
    """
    # ��ȡ����
    data = pd.read_csv(filename, encoding='gbk', nrows=10)
    # ��ȡȫ������
    df = data['ȫ������']
    # ��ȡ��һ��//@ǰ������
    df_context = df.apply(get_first_comment)
    # ��ȡÿһ��//@��������ݵ���һ��//@ǰ������
    df_comment = df.apply(get_comment)
    # ��df_comment��df_context��data['���⣯΢������']��data['������']��data['������']��data['ת����']�ϲ�Ϊһ��DataFrame
    data = pd.concat([df_context, df_comment, data['���⣯΢������'], data['������'], data['������'], data['ת����']], axis=1)
    # ����������
    data.columns = ['context', 'comment', 'title', 'comment_num', 'like_num', 'forward_num']
    # д���ļ�
    # data.to_csv('../data/2022��ȫ���߿�Aƽ̨����/34918267_new.csv', index=False, encoding='gbk')
    # ��data�����ֵ���ʽ����
    data = data.to_dict(orient='records')
    # ��������
    return data

if __name__ == '__main__':
    filename = '../data/2022��ȫ���߿�Aƽ̨����/34918267.csv'
    data = read_data(filename)
    print(data)

    # ���ز�����ʽ
    # context: ��������������
    # comment: �������µ����ת�����ۣ��ֵ���ʽ��keyΪ�����ߣ�valueΪ��������
    # title: ����
    # comment_num: ������
    # like_num: ������
    # forward_num: ת����
    # ���磺{'context': '[��ͷ]', 'comment': {'С����-����': 'http://t.cn/A6xAcwv4��??', ' 
    # ��������ʮ��¥�Ű�': '�����þò���ѽ��ף�ҵı����µ�һ������ʤ�⣡�߿����ͣ������Ҫ����������Ĺ��úÿ졫���ǵ�С������Ҫʮ����������ϣ���ҵı���Ҫһֱ������ȥѽ��'}, 'title': '[��ͷ]//@С����-����:http://t.cn/A6xAcwv4��??//@��������ʮ��¥�Ű�:�����þò���ѽ��ף�ҵı����µ�һ������ʤ�⣡�߿����ͣ������Ҫ����������Ĺ��úÿ졫 
    # ���ǵ�С������Ҫʮ����������ϣ���ҵı���Ҫһֱ������ȥѽ��', 'comment_num': 0, 'like_num': 0, 'forward_num': 0}