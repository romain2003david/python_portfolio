from matrix import Matrix

import numpy as np

import random


def sigmoid(x):

    if x < -10:

        return 0

    elif x > 10:

        return 1

    return 1 / (1 + math.exp(-x))


def np_sigmoid(x):

    return 1/(1+np.exp(-x))

class Network:

    def __init__(self, input_nb, layer_nb, layer_size, output_nb, weights=0):

        self.input_nb = input_nb

        self.layer_nb = layer_nb

        self.layer_size = layer_size

        self.output_nb = output_nb

        if weights:  # weights given in input (is a copy of an other neural network)

            self.weights = weights

        else:  # defines random weights

            if layer_size > 0:

                self.weights = [Network.create_reandom_matrix(input_nb, layer_size)]  # layer_size = rows (= 3) ; nbr_input = column (= 2)

                for layer in range(self.layer_nb-1):  # Couche inter hidden layer

                    self.weights.append(Network.create_reandom_matrix(layer_size, layer_size))

                self.weights.append(Network.create_reandom_matrix(layer_size, output_nb))  # derniere hidden layer -> output

            else:

                self.weights = [Network.create_reandom_matrix(input_nb, output_nb)]

    def create_reandom_matrix(row, col):
        """ creates a matrix with random numbers betweeen -1 and 1 """

        return 2*np.random.random((row, col)) - 1

    def print_net(self):
        """ prints the net in a clear way """

        print("Network :\n\nWeights:")

        for weight in self.weights:

            print("weight {} : {}".format(self.weights.index(weight), weight))

        print("\nEnd net\n")

    def feedforward(self, np_input, is_np=True):
        """ The neural Network guess what the answer is given some input """

        for layer_index in range(len(self.weights)):  # does this for every layer of weights

            # does the matrix product between input and layers

            np_input = np.dot(np_input, self.weights[layer_index])  # Matrix.matrix_product(self.weights[layer_index], matrix_input)

            #print(np_input)

            # applies sigmoid function to resulting matrix

            np_input = np_sigmoid(np_input)

        return np_input  # en fait couche des outputs

    def copy(self):
        """ returns a copy of this neural network, as an other instance """

        # creates a copy that can be modified without altering the original

        personal_data = []

        for x in self.weights:

            personal_data.append(x.copy())

        # returns net copy

        return Network(self.input_nb, self.layer_nb, self.layer_size, self.output_nb, personal_data)

    def mutate(self, ecart=1):
        """ tweaks a parameter of the network """

        first_rand = random.randint(0, len(self.weights)-1)

        second_rand = random.randint(0, len(self.weights[first_rand])-1)

        #print(ecart, first_rand, second_rand, self.weights[first_rand][second_rand])

        self.weights[first_rand][second_rand] += ((2*random.random())-1) * ecart  # random.randint(-ecart, ecart)

        #print(self.weights[first_rand][second_rand])

        limited_weights = 0

        if limited_weights:

            if self.weights[first_rand][second_rand] > 1:

                self.weights[first_rand][second_rand] = 1

            elif self.weights[first_rand][second_rand] < -1:

                self.weights[first_rand][second_rand] = -1            


def main():

    n = Network(2, 0, 0, 1)

    n.print_net()

    c = 0

    for x in range(-1, 2):

        for y in range(-1, 2):

            c += 1

            net_input = np.array([[x, y]])

            print("Input {} : {}".format(c, net_input))

            print(n.feedforward(net_input))


if __name__ == "__main__":

    main()
