
class NumberKit:

    @staticmethod
    def KeySetAddData(ks, k, d):

        if k in ks.keys():
            ks[k].add(d)
        else:
            ks[k] = set()
            ks[k].add(d)

    @staticmethod
    def KeySetAddDataValue(ks, k, d, v):

        # if k in ks.keys():
        #     ks[k].add(d)
        # else:
        #     ks[k] = set()
        #     ks[k].add(d)

        if k not in ks.keys():
            ks[k] = {}
        ks[k][d] = v



    @staticmethod
    def CalcTopKIndex(data, k):

        rs = []
        for i in range(k):
            b = data.index(max(data))
            rs.append(b)
            data[b] = -1

        return rs