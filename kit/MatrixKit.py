

class MatrixKit:

    @staticmethod
    def add(m1, m2):

        l1 = len(m1)
        l2 = len(m1[0])

        m = [[0 for _ in l2] for _ in l1]
        for i in range(l1):
            for j in range(l2):
                m[i][j] = m1[i][j] + m2[i][j]

        return m