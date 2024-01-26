from pip import main
from torch.utils.data import DataLoader
from torch.utils.data.dataset import Dataset
import numpy as np
import os
import torch
from torch import nn
import math
import torch.optim as optim
import torch.nn.functional as F
from sklearn import preprocessing
import numpy as np
import operator
import heapq
import time
from multiprocessing import Array
from multiprocessing import Value
from multiprocessing import Manager
import multiprocessing
from multiprocessing import Pool
import kit.IOKit as IOKit
import heapq

def nDCG(ranked_list, ground_truth):  # 评价指标
    dcg = 0
    idcg = IDCG(len(ground_truth))
    for i in range(len(ranked_list)):
        id = ranked_list[i]
        if id not in ground_truth:
            continue
        rank = i+1
        dcg += 1 / math.log(rank+1, 2)
    return dcg / idcg


def IDCG(n):
    idcg = 0
    for i in range(n):
        idcg += 1 / math.log(i+2, 2)
    return idcg


def AP(ranked_list, ground_truth):
    hits, sum_precs = 0, 0.0
    for i in range(len(ranked_list)):
        id = ranked_list[i]
        if id in ground_truth:
            hits += 1
            sum_precs += hits / (i+1.0)
    if hits > 0:
        return sum_precs / len(ground_truth)
    else:
        return 0.0


def RR(ranked_list, ground_list):

    for i in range(len(ranked_list)):
        id = ranked_list[i]
        if id in ground_list:
            return 1 / (i + 1.0)
    return 0


# 计算预测 和召回率 ranked_list   ground_list真实列表
def Precision_and_Recall(ranked_list, ground_list):
    hits = 0
    for i in range(len(ranked_list)):
        id = ranked_list[i]
        if id in ground_list:
            hits += 1
    pre = hits/(1.0 * len(ranked_list))  # 命中次数/预测列表长度
    rec = hits/(1.0 * len(ground_list))  # 命中次数/真实列表长度

    # print('pre:'+str(pre) + ' rec:'+str(rec))
    return pre, rec


# https://codeleading.com/article/37464926651/

def subTask_Top_Recall_Ndcg2(taskid, SAS, SAL, subus, testScore, predictionScore, top_n):
    
    recall_list = []
    ndcg_list = []


    for u in subus:

        # tmp_r = sorted(predictionScore[u], key=lambda x: x[1], reverse=True)[0:top_n]
        tmp_r = heapq.nlargest(top_n, range(len(predictionScore[u])), predictionScore[u].__getitem__)
        tmp_t = sorted(testScore[u].items(), key=lambda x: x[1], reverse=True)[0:min(len(testScore[u]), top_n)]


        # print('********************')
        # print(tmp_r)

        tmp_r_list = []
        tmp_t_list = []

        for item in tmp_r:  # 读取预测topn中的item的名称
            tmp_r_list.append(item)

        for (item, rate) in tmp_t:  # 读取测试集中topn中的item的名称
            tmp_t_list.append(item)

        pre, rec = Precision_and_Recall(tmp_r_list, tmp_t_list)  # 计算预测 和召回率
        ndcg = nDCG(tmp_r_list, tmp_t_list)
        recall_list.append(rec)
        ndcg_list.append(ndcg)
        
    # 0:recall_list 1:ndcg_list
    SAS[0] = SAS[0] + sum(recall_list)
    SAS[1] = SAS[1] + sum(ndcg_list)

    SAL[0] = SAL[0] + len(recall_list)
    SAL[1] = SAL[1] + len(ndcg_list)
       


def Top_Recall_Ndcg2(test_u, testScore, predictionScore, top_n, multiprocess=20):

    u_len = len(test_u)
    list_u = list(test_u)
    batch = int(u_len / multiprocess + 1)

    SAS = Array('f', [0.0 for _ in range(2)])
    SAL = Array('f', [0.0 for _ in range(2)])

    ps = []
    valid_s_len = 0
    for i in range(multiprocess):

        us = list_u[i*batch : (i+1)*batch] 
        if len(us) > 0:
            p = multiprocessing.Process(target = subTask_Top_Recall_Ndcg2 ,args=(i, SAS, SAL, us, testScore, predictionScore, top_n))
            ps.append(p)
            valid_s_len = valid_s_len + 1
  
    for p in ps:
        p.start()
    for p in ps:
        p.join()

    recall = SAS[0] / SAL[0]
    mndcg = SAS[1] / SAL[1]
    return recall, mndcg

