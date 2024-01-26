from bean.Behavior import Behavior
import kit.IOKit as IOKit
from bean.UserEnum import UserEnum
from bean.ItemEnum import ItemEnum
import random
import pickle
import numpy as np


class HandleStepReadData:

    @staticmethod
    def read_train_test_facade(dataset):

        if dataset.startswith("beibei"):
            return HandleStepReadData.read_beibei_train(dataset)
        if dataset.startswith("Taobao"):
            return HandleStepReadData.read_taobao_train(dataset)
        if dataset.startswith("IJCAI2"):
            return HandleStepReadData.read_IJCAI2_train(dataset)
        return None

    @staticmethod
    def read_target_facade(dataset):

        if dataset.startswith("beibei"):
            return HandleStepReadData.read_beibei_train(dataset)[2]
        if dataset.startswith("Taobao"):
            return HandleStepReadData.read_taobao_train(dataset)[2]
        if dataset.startswith("IJCAI2"):
            return HandleStepReadData.read_IJCAI2_train(dataset)[3]
        return None

    @staticmethod
    def read_test_facade(dataset, ue, ie, top=None):

        if dataset.startswith("beibei"):
            return HandleStepReadData.read_beibei_test(dataset, ue, ie, top)
        if dataset.startswith("Taobao"):
            return HandleStepReadData.read_taobao_test(dataset, ue, ie, top)
        if dataset.startswith("IJCAI2"):
            return HandleStepReadData.read_IJCAI2_test(dataset, ue, ie, top)
        return None



    @staticmethod
    def read_taobao_train(dataset):

        pb = Behavior()
        pb.name = "p"

        cb = Behavior()
        cb.name = "c"
        
        bb_train = Behavior()
        bb_train.name = "b"

        bb_test = Behavior()
        bb_test.name = "bt"


        for line in IOKit.read_txt("Data/"+str(dataset)+"/pv.txt")[1:]:     
            dd = line.split("	")
            pb.bs.append((int(dd[0]), int(dd[1])))
        # pb.create_index()

        for line in IOKit.read_txt("Data/"+str(dataset)+"/cart.txt")[1:]:     
            dd = line.split("	")
            cb.bs.append((int(dd[0]), int(dd[1])))
        # cb.create_index()

        for line in IOKit.read_txt("Data/"+str(dataset)+"/buy.train.txt")[1:]:    
            dd = line.replace("\n"," ").split("	")
            bb_train.bs.append((int(dd[0]), int(dd[1])))
        # bb_train.create_index()

        # 这个数据集有11条数据，用户或项目在训练集当中没有出现，所以统一编码的时候加上测试集
        # 这样会导致结果降低，但我也不知道没人是怎么处理的，但是降低这一点我们不是很在乎
        for line in IOKit.read_txt("Data/Taobao/buy.test.txt")[1:]:    
            dd = line.replace("\n"," ").split("	")
            bb_test.bs.append((int(dd[0]), int(dd[1])))

        return [pb, cb, bb_train, bb_test]


    @staticmethod
    def read_beibei_train(dataset):

        pb = Behavior()
        pb.name = "p"

        cb = Behavior()
        cb.name = "c"
        
        bb_train = Behavior()
        bb_train.name = "b"

        bb_test = Behavior()
        bb_test.name = "bt"

        for line in IOKit.read_txt("Data/"+str(dataset)+"/pv.txt")[:]:     
            # print(line)
            dd = line.replace("\n"," ").split(" ")
            # print(dd)
            uid = int(dd[0])
            for v in dd[1:]:
                if v == '':
                    continue
                vid = int(v)
                pb.bs.append((uid, vid))

        for line in IOKit.read_txt("Data/"+str(dataset)+"/cart.txt")[:]:     
            dd = line.replace("\n"," ").split(" ")
            uid = int(dd[0])
            for v in dd[1:]:
                if v == '':
                    continue
                vid = int(v)
                cb.bs.append((uid, vid))

        for line in IOKit.read_txt("Data/"+str(dataset)+"/train.txt")[:]:    
            dd = line.replace("\n"," ").split(" ")
            uid = int(dd[0])
            for v in dd[1:]:
                if v == '':
                    continue
                vid = int(v)
                bb_train.bs.append((uid, vid))

        for line in IOKit.read_txt("Data/"+str(dataset)+"/test.txt")[:]:    
            dd = line.replace("\n"," ").split(" ")
            uid = int(dd[0])
            for v in dd[1:]:
                if v == '':
                    continue
                vid = int(v)
                bb_test.bs.append((uid, vid))

        return [pb, cb, bb_train, bb_test]

    @staticmethod
    def read_IJCAI2_train(dataset):

        pb = Behavior()
        pb.name = "p"

        fb = Behavior()
        fb.name = "f"

        cb = Behavior()
        cb.name = "c"
        
        bb = Behavior()
        bb.name = "b"

        bt = Behavior()
        bt.name = "bt"

        for line in IOKit.read_txt("Data/"+str(dataset)+"/pv.txt"):     
            dd = line.split("	")
            pb.bs.append((int(dd[0]), int(dd[1])))

        for line in IOKit.read_txt("Data/"+str(dataset)+"/fav.txt"):     
            dd = line.split("	")
            fb.bs.append((int(dd[0]), int(dd[1])))

        for line in IOKit.read_txt("Data/"+str(dataset)+"/cart.txt"):     
            dd = line.split("	")
            cb.bs.append((int(dd[0]), int(dd[1])))

        for line in IOKit.read_txt("Data/"+str(dataset)+"/train.txt"):    
            dd = line.split("	")
            bb.bs.append((int(dd[0]), int(dd[1])))

        for line in IOKit.read_txt("Data/"+str(dataset)+"/test.txt"):    
            dd = line.split("	")
            bt.bs.append((int(dd[0]), int(dd[1])))

        return [pb, fb, cb, bb, bt]


    def read_taobao_test(dataset, ue:UserEnum, ie:ItemEnum, top=None):

        TestU = set()
        TestV = set()
        TestR = {}
        for line in IOKit.read_txt("Data/"+str(dataset)+"/buy.test.txt")[1:]:     
            dd = line.replace("\n"," ").split("	")

            u = ue.enum[int(dd[0])]
            v = ie.enum[int(dd[1])]

            TestV.add(v)

            if top!= None and u >= top:
                continue

            TestU.add(u)
            if TestR.get(u) is None:
                TestR[u] = {}
            TestR[u][v] = 1

        return TestU, TestV, TestR  

    def read_beibei_test(dataset, ue:UserEnum, ie:ItemEnum, top=None):

        TestU = set()
        TestV = set()
        TestR = {}
        for line in IOKit.read_txt("Data/"+str(dataset)+"/test.txt")[:]:     
            dd = line.replace("\n"," ").split(" ")
            # bb_test.bs.append((int(dd[0]), int(dd[1])))
            u = ue.enum[int(dd[0])]
            v = ie.enum[int(dd[1])]

            TestV.add(v)

            if top!= None and u >= top:
                continue

            TestU.add(u)
            if TestR.get(u) is None:
                TestR[u] = {}
            TestR[u][v] = 1

        return TestU, TestV, TestR  


    @staticmethod
    def read_IJCAI2_test(dataset, ue:UserEnum, ie:ItemEnum, u_len = None):

        TestU = set()
        TestV = set()
        TestR = {}
        for line in IOKit.read_txt("Data/"+str(dataset)+"/test.txt"):     

            try:

                dd = line.replace("\n"," ").split("	")
                u = int(dd[0])
                v = int(dd[1])

                if u_len != None and u > u_len:
                    continue

                if u not in ue.enum.keys():
                    continue

                if v not in ie.enum.keys():
                    continue

                iu = ue.enum[u]
                iv = ie.enum[v]

                TestU.add(iu)
                TestV.add(iv)
                if TestR.get(iu) is None:
                    TestR[iu] = {}
                TestR[iu][iv] = 1

            except:

                print(line)

            finally:
                
                continue

        return TestU, TestV, TestR






       