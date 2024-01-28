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
import os


class Step2CreateFeatures:

    @staticmethod
    def subTask(tasks, datadir, base, behaviors, IIIndex, IIIndex_C, ie, be, MAX, MIN):

        max = [0.0 for _ in range(be.get_bs_size())]
        min = [100.0 for _ in range(be.get_bs_size())]

        for taskid, subus in tasks:

            if os.path.exists("Data/"+ datadir +"/IN_"+str(taskid)+".pkl"):
                continue

            result = []

            xx = 0
            for u1 in subus:

                xx = xx + 1
                if xx % 20 == 1:
                    print('TaskId: '+str(taskid)+': ' +  str(xx) + '/' + str(len(subus)))

                u_result = []

                for i1 in range(len(ie.enum)):

                    i_result = [0 for _ in range(be.get_bs_size())]

                    for ind in range(len(base)):
        
                        id_index = be.get_index(base[ind])
                        beh = behaviors[ind]

                        if u1 not in beh.ui_index.keys():
                            continue

                        if i1 in beh.ui_index[u1]:
                            i_result[id_index] = 1
                            max[id_index] = 1


                    for ti in range(len(base)):

                        uiindex = behaviors[ti].ui_index
                        if u1 not in uiindex.keys():
                            continue

                        for tj in range(len(base)):
                            for tk in range(len(base)):
                                t_name = base[tk] + "_" + base[tj]

                                iiindex = IIIndex[t_name]
                                iiindex_c = IIIndex_C[t_name]

                                if i1 not in iiindex.keys():
                                    continue

                                set1 = uiindex[u1]
                                set2 = iiindex[i1]
                                ins = set1.intersection(set2)

                                if len(ins) == 0:
                                    continue

                                sum = 0
                                for i2 in ins:
                                    sum = sum + iiindex_c[i1][i2]

                                xxx = be.get_index((base[ti], base[tj], base[tk]))
                                i_result[xxx] = sum

                                if max[xxx] < sum:
                                    max[xxx] = sum
                                if min[xxx] > sum:
                                    min[xxx] = sum

                    u_result.append(i_result)

                result.append(u_result)

            IOKit.write_pkl("Data/"+ datadir +"/IN_"+str(taskid)+".pkl", result)

        for i in range(be.get_bs_size()):
            if MAX[i] < max[i]:
                MAX[i] = max[i]
            if MIN[i] > min[i]:
                MIN[i] = min[i]

    @staticmethod
    def execute(dataset, top=None):

        bbs = HandleStepReadData.read_train_test_facade(dataset)
        ue, ie = HandleStepCreateEnum.createUserAndItemEnum(bbs)
        rbbs = HandleStepRecodeBehavior.recode_behaviors(ue, ie, bbs)
        be = BehaviorEnumFactory.createEnumByDataSet(dataset)
        base = be.base
        behaviors = rbbs[0: len(base)]

        IIIndex = {}
        IIIndex_C = {}

        for i in range(len(base)):
            for j in range(len(base)):
                name = base[i] + "_" + base[j]
                index = IOKit.read_pkl("Data/"+ dataset +"/IIIndex_"+name+".pkl")
                index_c = IOKit.read_pkl("Data/"+ dataset +"/IIIndex_C_"+name+".pkl")
                IIIndex[name] = index
                IIIndex_C[name] = index_c


        if top == None:
            u_len = len(ue.enum)
        else:
            u_len = top
        
        batch_size = 50
        batch = int(u_len / batch_size) + 1
        us_totals = [i for i in range(u_len)]
        process_total = 20
        tasks = [[] for _ in range(process_total)]

        for i in range(batch):
            us = us_totals[i*batch_size: (i+1)*batch_size]
            process_id = i % process_total
            tasks[process_id].append((i, us))

        # print(tasks)

        print('start subtasks')

        MAX = Array('f', [0.0 for _ in range(be.get_bs_size())])
        MIN = Array('f', [0.0 for _ in range(be.get_bs_size())])

        ps = []
        for i in range(process_total):
            p = multiprocessing.Process(target=Step2CreateFeatures.subTask, args=(
                tasks[i], dataset, base, behaviors, IIIndex, IIIndex_C, ie, be, MAX, MIN))
            ps.append(p)

        for p in ps:
            p.start()
        for p in ps:
            p.join()

        max = [MAX[i] for i in range(be.get_bs_size())]
        min = [MIN[i] for i in range(be.get_bs_size())]

        IOKit.write_pkl("Data/"+ dataset +"/IN_MAX.pkl", max)
        IOKit.write_pkl("Data/"+ dataset +"/IN_MIN.pkl", min)
