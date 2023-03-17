from QuantumComputerSimulator.mods.MatrixFrame import MatrixFrame

import copy
import numpy as np

class LazyMatrix(MatrixFrame):

    def __init__(self, Type, *args):
        '''
        Set up the lazy gates using lambda functions.
        <b>param Type<\b> Gate to be initialised
        <b>param args<\b>
        '''
        if Type == 'I':
            self.matrix = [lambda x: x[0], lambda x: x[1]]
        if Type == 'H':
            self.matrix = [lambda x: (x[0] + x[1]) / np.sqrt(2), lambda x: (x[0] - x[1]) / np.sqrt(2)]
        if Type == 'P':
            self.matrix = [lambda x: x[0], lambda x: np.exp(1j * args[0]) * x[1]]

        if Type == 'X':
            self.matrix = [lambda x: x[1], lambda x: x[0]]
        if Type == 'Y':
            self.matrix = [lambda x: 1j * x[1], lambda x: -1j * x[0]]
        if Type == 'Z':
            self.matrix = [lambda x: x[0], lambda x: -1 * x[1]]

        if Type == 'TP' or Type == 'MM' or Type == "General":
            self.matrix = args[0]

        if Type == 'CNOT':
            self.matrix = self.cnot(args[0], args[1], args[2])
        if Type == 'CV':
            self.matrix = self.cv(args[0], args[1], args[2])
        if Type == 'CZ':
            self.matrix = self.cz(args[0], args[1], args[2])

        if Type == 'M0':
            self.matrix = [lambda x: x[0], lambda x: 0]
        if Type == 'M1':
            self.matrix = [lambda x: 0, lambda x: x[1]]

        if Type == 'zerocol':
            pass
        if Type == 'onecol':
            pass

        self.dim = len(self.matrix)

    @classmethod
    def quantum_register(cls, qnum):
        pass

    @classmethod
    def tensor_prod(cls, m1, m2):
        '''
        Lazy tensor product
        <b>param m1<\b> Gate 1
        <b>param m2<\b> Gate 2
        <b>return<\b> Tensor product of Gate 1 with Gate 2
        '''
        tp = []
        for i in range(0, m1.dim):
            for j in range(0, m2.dim):
                tp.append(lambda x, y=i, z=j: m1.matrix[y](
                    [m2.matrix[z]([x[m2.dim * k + l] for l in range(0, m2.dim)]) for k in range(0, m1.dim)]))

        new_matrix = LazyMatrix('TP', tp)
        return new_matrix

    @classmethod
    def matrix_multiply(cls, m1, m2):
        '''
        Use list comprehension to preform a matrix multiplication between two 'matrices'
        <b>param m1<\b> Gate 1
        <b>param m2<\b> Gate 2
        <b>return<\b> Multiplication of gate 1 and gate 2
        '''
        mm = []
        for i in range(0, m1.dim):
            mm.append(
                lambda x, y=i: m1.matrix[y]([m2.matrix[k]([x[l] for l in range(0, m2.dim)]) for k in range(0, m1.dim)]))

        new_matrix = LazyMatrix('MM', mm)
        return new_matrix

    @classmethod
    def inner_product(cls, M):
        pass

    @classmethod
    def trace(cls, M):
        pass

    @classmethod
    def conjugate(cls, M):
        pass

    def cnot(self, d, c, t):
        digits = copy.deepcopy(d)
        cn = []

        index = super().CNOT_logic(digits, c, t)

        for i in range(0, len(index)):
            cn.append(lambda x, y=i: x[index[y]])

        return cn

    def cv(self, d, c, t):
        digits = copy.deepcopy(d)
        cv = []

        index = super().CV_logic(digits, c, t)

        for i in range(0, len(digits)):
            if index[i] == 1:
                cv.append(lambda x, y=i: 1j * x[y])
            else:
                cv.append(lambda x, y=i: x[y])

        return cv

    def cz(self, d, c, t):
        pass

    def output(self,inputs):
        new_in = []
        for i in range(0,len(inputs)):
            new_in.append(inputs[i][0])
        out = []
        for i in range(0,self.dim):
            out.append(self.matrix[i](new_in))

        return out

    def apply_register(self, input_vector: list) -> list:
        '''Returns the output state vector.'''
        #amplitudes = np.dot(self.matrix, input_vector)
        amplitudes = self.output([[v] for v in input_vector])
        return [amp[0]*np.conjugate(amp)[0] for amp in amplitudes.matrix]


class LazyMatrixSingle(MatrixFrame):
    def __init__(self, Type, *args):
        pass
