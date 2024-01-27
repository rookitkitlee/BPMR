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
import os

class Step1CreateIIndex:

    @staticmethod
    def subTask(name, datadir, ie, b1, b2):

        if os.path.exists("Data/"+ datadir +"/IIIndex_C_"+name+".pkl"):
            return

        IIIndex = {}
        IIIndex_C = {} 

        for m in range(len(ie.enum)):

            if m % 100 == 1:
                print('TaskId: '+str(name)+': ' + str(m)+ '/'+ str(len(ie.enum)))

            if m not in b1.iu_index.keys():
                continue

            for n in range(len(ie.enum)):

                if n not in b2.iu_index.keys():
                    continue

                set1 = b1.iu_index[m]
                set2 = b2.iu_index[n]    
                ins = set1.intersection(set2)

                if len(ins) > 0:
                    NumberKit.KeySetAddData(IIIndex, m, n)
                    NumberKit.KeySetAddDataValue(IIIndex_C, m, n, len(ins))

        IOKit.write_pkl("Data/"+ datadir +"/IIIndex_"+name+".pkl", IIIndex)
        IOKit.write_pkl("Data/"+ datadir +"/IIIndex_C_"+name+".pkl", IIIndex_C)


    @staticmethod
    def execute(dataset):

        bbs = HandleStepReadData.read_train_test_facade(dataset)
        ue, ie = HandleStepCreateEnum.createUserAndItemEnum(bbs)
        rbbs = HandleStepRecodeBehavior.recode_behaviors(ue, ie, bbs)
        be = BehaviorEnumFactory.createEnumByDataSet(dataset)
        base = be.base
        behaviors = rbbs[0: len(base)]

        ps = []

        for i in range(len(base)):
            b1 = behaviors[i]
            for j in range(len(base)):
                b2 = behaviors[j]
                name = base[i] + "_" + base[j]

                p = multiprocessing.Process(target = Step1CreateIIndex.subTask ,args = (name, dataset, ie, b1, b2))
                ps.append(p)

        for p in ps:
            p.start()
        for p in ps:
            p.join()

        print('end ----------------------------------------------')



                

                    





