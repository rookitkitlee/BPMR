import json
import kit.IOKit as IOKit
from kit.NumberKit import NumberKit
import random
import numpy as np
import multiprocessing
from multiprocessing import Pool
from handle.HandleStepReadData import HandleStepReadData
from handle.HandleStepCreateEnum import HandleStepCreateEnum
from handle.HandleStepRecodeBehavior import HandleStepRecodeBehavior
from bean.BehaviorEnum import BehaviorEnumFactory
from multiprocessing import Array
import kit.EvaluatingIndicatorMultiProcess2 as EVM2

# Z-score normalization

class StepTNBZScore:

    @staticmethod
    def subTask1(processId, tasks, datadir, MAX, ie, be, PC, NC, LPN, SelectUser, SelectItem):


        Sample = [[] for _ in range(be.get_bs_size())]

        pc = [0 for _ in range(be.get_bs_size())]
        nc = [0 for _ in range(be.get_bs_size())]
        lpn = [0, 0]

        for taskid, subus in tasks:

            print('likehood '+str(taskid))

            data = IOKit.read_pkl("Data/" + datadir +
                                  "/IN_"+str(taskid)+".pkl")

            for u1 in range(len(subus)):

                uid = subus[u1]

                for i1 in range(len(ie.enum)):

                    iid = i1

                    d = data[u1][i1]
                    flag_index = be.get_flag_index()
                    flag = False
                    if d[flag_index] > 0:
                        flag = True
                        lpn[0] = lpn[0] + 1
                    else:
                        lpn[1] = lpn[1] + 1

                    for k in range(be.get_bs_size()):

                        if k == be.get_flag_index():
                            continue

                        v = d[k]

                        # 求比例 除不除 都一样
                        # v = v / MAX[k]

                        if flag == True:
                            pc[k] = pc[k] + v
                        else:
                            nc[k] = nc[k] + v


                    # 采样算标准差
                    if uid in SelectUser and iid in SelectItem:
                        for k in range(be.get_bs_size()):
                            Sample[k].append(d[k])

        for k in range(be.get_bs_size()):
            PC[k] = PC[k] + pc[k]
            NC[k] = NC[k] + nc[k]


        LPN[0] = LPN[0] + lpn[0]
        LPN[1] + LPN[1] + lpn[1]

        IOKit.write_pkl("Data/" + datadir + "/Sample_"+str(processId)+".pkl", Sample)

    @staticmethod
    def subTask2(tasks, datadir, MAX, be, ie, CH, Mean):

        for taskid, subus in tasks:

            print('posterior '+str(taskid))

            data = IOKit.read_pkl("Data/" + datadir + "/IN_"+str(taskid)+".pkl")
            R = []

            for u1 in range(len(subus)):

                r = [0 for _ in range(len(ie.enum))]
                for i1 in range(len(ie.enum)):
                    d = data[u1][i1]
                    bv = 1.0
                    for k in range(be.get_bs_size()):
                        if k == be.get_flag_index():
                            continue

                        v = d[k] - Mean[k]
                        v = v / MAX[k]
                        bv = bv * (CH[k] ** v)

                    r[i1] = bv

                R.append(r)

            IOKit.write_pkl("Data/" + datadir + "/RNBZScore_"+str(taskid)+".pkl", R)

    @staticmethod
    def execute(dataset):

        bbs = HandleStepReadData.read_train_test_facade(dataset)
        ue, ie = HandleStepCreateEnum.createUserAndItemEnum(bbs)
        tb = HandleStepReadData.read_target_facade(dataset)
        rtb = HandleStepRecodeBehavior.recode_behavior(ue, ie, tb)
        TestU, _, TestR = HandleStepReadData.read_test_facade(dataset, ue, ie)
        be = BehaviorEnumFactory.createEnumByDataSet(dataset)
        MAX = IOKit.read_pkl("Data/" + dataset + "/IN_MAX.pkl")

        u_len = len(ue.enum)
        batch_size = 50
        batch = int(u_len / batch_size) + 1
        us_totals = [i for i in range(u_len)]
        process_total = 20
        tasks = [[] for _ in range(process_total)]

        for i in range(batch):
            us = us_totals[i*batch_size: (i+1)*batch_size]
            process_id = i % process_total
            tasks[process_id].append((i, us))

        print('start subtasks')


        SelectUser = []
        SelectItem = []
        SelectUserLength = int(len(ue.enum) / 100)
        SelectItemLength = int(len(ie.enum) / 100)
        for u1 in range(len(ue.enum)):
            if u1 % SelectUserLength == 0:
                SelectUser.append(u1)
        for i1 in range(len(ie.enum)):
            if i1 % SelectItemLength == 0:
                SelectItem.append(i1)

        PC = Array('f', [0 for _ in range(be.get_bs_size())])
        NC = Array('f', [0 for _ in range(be.get_bs_size())])
        LPN = Array('f', [0 for _ in range(2)])

        ps = []
        for i in range(process_total):
            p = multiprocessing.Process(
                target=StepTNBZScore.subTask1, args=(i, tasks[i], dataset, MAX, ie, be, PC, NC, LPN, SelectUser, SelectItem))
            ps.append(p)

        for p in ps:
            p.start()
        for p in ps:
            p.join()

        
        PC = [PC[i] for i in range(be.get_bs_size())]
        NC = [NC[i] for i in range(be.get_bs_size())]
        PC = np.array(PC)
        NC = np.array(NC)
        Mean = [(PC[i] + NC[i]) / len(ue.enum) / len(ie.enum)  for i in range(be.get_bs_size())]
        PC = [PC[i] - Mean[i] * LPN[0] for i in range(be.get_bs_size())]
        NC = [NC[i] - Mean[i] * LPN[1] for i in range(be.get_bs_size())]
        PC = (PC) / np.sum(PC)
        NC = (NC) / np.sum(NC)
        CH = [PC[i] / (NC[i] + 0.0000001) for i in range(be.get_bs_size())]

        Sample = [[] for _ in range(be.get_bs_size())]
        for i in range(process_total):
            sa = IOKit.read_pkl("Data/" + dataset + "/Sample_"+str(i)+".pkl")
            for k in range(be.get_bs_size()):
                ssd = sa[k]
                for xd in ssd:
                    Sample[k].append(xd)

        Sigmoid = [0 for i in range(be.get_bs_size())]
        for k in range(be.get_bs_size()):
            dd = np.array(Sample[k])
            Sigmoid[k] = np.var(dd)

        ps = []
        for i in range(process_total):
            p = multiprocessing.Process(
                target=StepTNBZScore.subTask2, args=(tasks[i], dataset, MAX, be, ie, CH, Sigmoid))
            ps.append(p)

        for p in ps:
            p.start()
        for p in ps:
            p.join()

        R = []
        for i in range(batch):
            data = IOKit.read_pkl("Data/" + dataset + "/RNBZScore_"+str(i)+".pkl")
            for d in data:
                R.append(d)

        # 存储已选择的顶点
        for b in rtb.bs:
            u, v = b
            if u >= u_len:
                continue
            R[u][v] = 0

        recall10, mndcg10 = EVM2.Top_Recall_Ndcg2(TestU, TestR, R, 10)
        recall20, mndcg20 = EVM2.Top_Recall_Ndcg2(TestU, TestR, R, 20)
        recall50, mndcg50 = EVM2.Top_Recall_Ndcg2(TestU, TestR, R, 50)
        recall80, mndcg80 = EVM2.Top_Recall_Ndcg2(TestU, TestR, R, 80)

        print('结束了 就是这个结果')

        print("RECALL10:"+str(recall10))
        print("RECALL20:"+str(recall20))
        print("RECALL50:"+str(recall50))
        print("RECALL80:"+str(recall80))

        print("NDCG10:"+str(mndcg10))
        print("NDCG20:"+str(mndcg20))
        print("NDCG50:"+str(mndcg50))
        print("NDCG80:"+str(mndcg80))

        log = open("Data/"+ dataset +"/Z_RNBZScore.txt", mode='w')
        log.write("RECALL10:"+str(recall10) +'\n')
        log.write("RECALL20:"+str(recall20) +'\n')
        log.write("RECALL50:"+str(recall50) +'\n')
        log.write("RECALL80:"+str(recall80) +'\n')
        log.write("NDCG10:"+str(mndcg10) +'\n')
        log.write("NDCG20:"+str(mndcg20) +'\n')
        log.write("NDCG50:"+str(mndcg50) +'\n')
        log.write("NDCG80:"+str(mndcg80) +'\n')
        log.flush()
        log.close()
