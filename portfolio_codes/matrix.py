from random import *


class Matrix:

    def __init__(self, rows, cols, randomize=1):

        self.rows = rows

        self.cols = cols

        if randomize:

            self.data = [[0 for x in range(cols)] for y in range(rows)]

        else:

            self.data = [[randint(-100, 100)/100 for x in range(cols)] for y in range(rows)]

    def matrix_product(a, b):

        """ Apply the matrix product on two matrixes a and b
            C(m,k) = A(m,n) * B(n,k)
            a are the weigths, b the values of the last layer"""

        n_matrix = Matrix(a.rows, b.cols)  # rows of weight matrix ; columns of input neurons

        # a.cols == b.rows

##        print("MATRIX PRODUCT")
##        a.print()
##        b.print()

        for row1 in range(a.rows):

            for row2 in range(b.rows):

                n_matrix.data[row1][0] += a.data[row1][row2] * b.data[row2][0]  # weight * neuron

        #n_matrix.print()

        return n_matrix

##    def matrix_product_back_prop(self, error_matrix):
##        """ Function called with the weights matrix or the biases matrix, to which the error matrix is applied """
##
##        for row in range(error_matrix.rows):
##
##            for col in range(self.cols):
##
##                self.data[row][col] += error_matrix[row][0]

    def weight_add_cost(self, cost, rate):
        """ Fonction ajoutant cost a self (-> la matrix de poids)
            col_self = row_cost"""
##        print("comp")
##        Matrix.print(self)
##        cost.print()

        for x in range(cost.rows):

            for y in range(self.rows):

                self.data[y][x] += cost.data[x][0] * rate
        

    def add(self, matrix, rate=1):
        """Ads a matrix to another (index to index), with optional weight(for the learning rate)"""

##        print("add")
##        Matrix.print(self)
##        matrix.print()

        for x in range(self.rows):

            for y in range(self.cols):

                self.data[x][y] += matrix.data[x][y] * rate

    def scale(self, scaler):
        """ Scales the matrix according to the scaler """

        for row in range(self.rows):
            
            for col in range(self.cols):

                self.data[row][col] *= scaler

    def print(self):

        #print(self.data)

        print("[")

        for x in self.data:

            print(*x)

        print("]")

    def apply(self, function):

        for row in range(len(self.data)):
            for col in range(len(self.data[row])):

                self.data[row][col] = function(self.data[row][col])

    def randomize(self):

        for row in range(self.rows):

            for col in range(self.cols):

                self.data[row][col] = randint(-10, 10)/10

    def transpose(matrix):
        """ Change a matrix's rows into it's columns and inversely """

        n_matrix = Matrix(matrix.cols, matrix.rows)

        for row in range(matrix.rows):

            for col in range(matrix.cols):

                n_matrix.data[col][row] = matrix.data[row][col]

        return n_matrix

    def transpose(self):
        """ Change self's rows into self's columns and inversely """

        n_matrix = Matrix(self.cols, self.rows)

        for row in range(self.rows):

            for col in range(self.cols):

                n_matrix.data[col][row] = self.data[row][col]

        self.cols, self.rows = self.rows, self.cols

        self.data = n_matrix.data

    def from_array(array):

        rows = len(array)

        if type(array[0]) == list:

            cols = len(array[0])

        else:

            cols = 1

        n_matrix = Matrix(rows, cols)

        for row in range(rows):

            if not cols == 1:

                n_matrix.data[row] = array[row]

            else:

                n_matrix.data[row][0] = array[row]

        return n_matrix

    def to_array(matrix):

        array = []

        for row in range(matrix.rows):

            if len(matrix.data[row]) == 1:

                array.append(matrix.data[row][0])

            else:

                array.append(matrix.data[row])

        return array


class Test:

    def __init__(self):

        a = Matrix(3, 2)
        a.randomize()
        a.print()

        a.scale(2)
        a.print()

        b = Matrix(2, 1)
        b.randomize()
        b.print()

        a.weight_add_cost(b, 1)
        a.print()

##        arr = [0, 1]
##        m_a = Matrix.from_array(arr)
##        m_a.print()
##
##        c = Matrix(3, 2)
##        #c.randomize()
##        c.print()
##
##        d = Matrix.matrix_product(c, m_a)
##        d.print()
##
##        a.print()
##        a_prime = Matrix.transpose(a)
##        a_prime.print()
##
##        c.print()
##        c_prime = Matrix.transpose(c)
##        c_prime.print()

##        arr = [4, 2]
##        m_a = Matrix.from_array(arr)
##        m_a.print()
##        m_a = Matrix.to_array(m_a)
##        print(m_a)
##        arr = [[4, 2], [8, 9]]
##        m_a = Matrix.from_array(arr)
##        m_a.print()
##
##        m_a = Matrix.to_array(m_a)
##        print(m_a)


if __name__ == "__main__":      

    t=Test()
