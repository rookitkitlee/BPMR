
class BehaviorEnum3:

    def __init__(self) -> None:
        
        self.base = ['p', 'c', 'b']
        self.bs = []
        self.enum = {}

        for b in self.base:
            self.enum[b] = len(self.bs)
            self.bs.append(b)

        for i in range(3):
            for j in range(3):
                for k in range(3):
                    mb = (self.base[i], self.base[j], self.base[k])
                    self.enum[mb] = len(self.bs)
                    self.bs.append(mb)
    

    def get_bs_size(self):
        return len(self.bs)

    def get_index(self, mb):
        return self.enum[mb]

    def get_flag_index(self):
        return 2

class BehaviorEnum4:

    def __init__(self) -> None:
        
        self.base = ['p', 'f', 'c', 'b']
        self.bs = []
        self.enum = {}

        for b in self.base:
            self.enum[b] = len(self.bs)
            self.bs.append(b)

        for i in range(4):
            for j in range(4):
                for k in range(4):
                    mb = (self.base[i], self.base[j], self.base[k])
                    self.enum[mb] = len(self.bs)
                    self.bs.append(mb)
    

    def get_bs_size(self):
        return len(self.bs)

    def get_index(self, mb):
        return self.enum[mb]

    def get_flag_index(self):
        return 3


class BehaviorEnumFactory:

    @staticmethod
    def createEnumByDataSet(dataset):

        if dataset.startswith("beibei") or dataset.startswith("Taobao"):
            return BehaviorEnum3()
        elif dataset.startswith("IJCAI2"):
            return BehaviorEnum4()
        else:
            return None