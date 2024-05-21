from pig_tv import *

from random import *

from matrix import Matrix


class Network:

    def __init__(self, nbr_input, layer_nb=0, layer_size=0, nb_output=0, visuel=0, training_data=0):

        self.visuel = visuel

        # defines the network shape

        if type(nbr_input) == list:

            self.nbr_input = nbr_input[0]

            self.layer_nb = nbr_input[1]  # Nombre de hidden

            self.layer_size = nbr_input[2]

            self.nb_output = nbr_input[3]

        else:

            self.nbr_input = nbr_input

            self.layer_nb = layer_nb  # Nombre de hidden

            self.layer_size = layer_size

            self.nb_output = nb_output

        # creates random values for network weights

        self.layers = []

        self.learning_rate = 0.5

        if training_data:

            self.training_data = training_data

        for k in range(self.layer_nb):

            self.layers.append(Matrix(self.layer_size, 1))  # Biases

            self.layers[-1].randomize()

        # Every matrix of weights has i number of in_neuron rows and o number of out_neurons columns

        # weight input -> premiere hidden layer
        self.weights = [Matrix(self.layer_size, self.nbr_input)]  # layer_size = rows (= 3) ; nbr_input = column (= 2)
        self.weights[-1].randomize()

        for layer in range(self.layer_nb-1):  # Couche inter hidden layer

            self.weights.append(Matrix(self.layer_size, self.layer_size))
            self.weights[-1].randomize()

        self.weights.append(Matrix(self.nb_output, self.layer_size))  # derniere hidden layer -> output
        self.weights[-1].randomize()

        #Network.print_net(self)

        if visuel:

            screen.fill((255, 255, 255))

            layer_space = 100

            taille_neurone = 20

            for x in range(layer_nb+2):

                if not x:  # input

                    for y in range(nbr_input):

                        color = (0, 0, 0)

                        pygame.draw.circle(screen, color, (layer_space, (y+1)*100), taille_neurone)

                elif layer_nb+1 == x:  # output

                    for y in range(nb_output):

                        color = (0, 0, 0)

                        pygame.draw.circle(screen, color, ((x+1)*layer_space, (y+1)*100), taille_neurone)

                else:

                    for ya in range(len(self.layers[x-1].data)):
                        
                        y = self.layers[x-1].data[ya]

                        if y[0] > 0:

                            color = (0, y[0]*255, 0)

                        else:

                            color = (y[0]*-255, 0, 0)

                        pygame.draw.circle(screen, color, ((x+1)*layer_space, (ya+1)*100), taille_neurone)

                        #aff_txt(str(y[0]), (x+1)*layer_space, (ya+1)*120, color=(0, 0, 0), taille=15)

            for w in range(len(self.weights)):

                for x in range(len(self.weights[w].data)):  #row

                    for y in range(len(self.weights[w].data[x])):

                        # w definit la couche a laquelle on se situe (abscisse)
                        # x definit l'ordonne de la deuxieme coor
                        # y definit l'ordonne de la premiere coor

                        abs1 = (w+1) * layer_space
                        abs2 = abs1 + layer_space

                        ord1 = (y+1) * layer_space
                        ord2 = (x+1) * layer_space

                        col_factor = self.weights[w].data[x][y]

                        if col_factor > 0:

                            color = (0, col_factor*255, 0)

                        else:

                            color = (col_factor*-255, 0, 0)

                        pygame.draw.line(screen, color, (abs1, ord1), (abs2, ord2), 3)

                        #aff_txt(str(col_factor), (abs1+abs2)//2, (ord1+ord2)//2, color=(0, 0, 0), taille=15)
                        

            pygame.display.update()

    def print_net(self):

        print("Layers :\n")
        for matrix in self.layers:
            print("Hidden Layer {}:".format(self.layers.index(matrix)+1))
            matrix.print()

        print("Weights :\n")
        for matrix in self.weights:
            print("Weight {}:".format(self.weights.index(matrix)+1))
            matrix.print()
        
    def train(self):

        """ Permet d'entrainer le reseau a determiner si un point est de classe a ou b, avec a > fct(x), et b!=a """

        # Create random points and classify them NOPE
        train_range = len(self.training_data)
        batch_range = 1  # taille des "lots" de training qu'on fait (donc de cost) avant la back propagation

        for k in range(train_range//batch_range):  # Normalement devrait toujours etre entier (100 div 10 par ex)

            #Network.print_net(self)

            batch_cost = Matrix(self.nb_output, 1)

            for l in range(batch_range):

                if self.learning_rate > 0.1:

                    self.learning_rate -= 0.01

                outputs = Network.feedforward(self, self.training_data[k][0])

                #outputs.print()

                cost = Network.get_cost(outputs, self.training_data[k][1])  # Computes the "error"

                batch_cost.add(cost)

            batch_cost.scale(1/batch_range)  # Get the average cost / error of the training batch

            #print("ERROR")
            #batch_cost.print()

            Network.back_propagation(self, batch_cost)

    def copy(self):

        return self.layers, self.weights


    def feedforward(self, inputs):
        """ The neural Network guess what the answer is given some input """

        matrix_input = Matrix.from_array(inputs)

        matrix_input.print()

        for layer in range(self.layer_nb+1):

            matrix_input = Matrix.matrix_product(self.weights[layer], matrix_input)

            if not layer == self.layer_nb:  # On rajoute le biais ( layers[layer] ) a chaque couche a part la derniere

                matrix_input.add(self.layers[layer])

            matrix_input.apply(sigmoid)  # On apply a chaque neurone de la couche

            if self.visuel:

                taille_neurone = 20
                layer_space = 100

                for row in range(len(matrix_input.data)):

                    col_fact = matrix_input.data[row][0]

                    if col_fact > 0:

                        color = (0, col_fact*255, 0)

                    else:

                        color = (col_fact*-255, 0, 0)

                    pygame.draw.circle(screen, color, ((layer+2)*layer_space, (row+1)*100), taille_neurone)

                    aff_txt(str(round(col_fact, 2)), (layer+2)*layer_space, (row+1)*120, color=(0, 0, 0), taille=15)
                pygame.display.update()

        

        return matrix_input  # en fait couche des outputs

    def get_cost(output, desired_output):

        output = Matrix.to_array(output)

        cost = [(desired_output[k]-output[k]) for k in range(len(output))]  # **2

        return Matrix.from_array(cost)

    def back_propagation(self, cost):
        """ The neurons of the network are being changed according to the cost = error
            calculate a gradient descent
            should do a stochastic = sum of group of " errors " """

        # A calculer : weights, biases, activation -> (weights, biases) previous layer

        # Calcul des masses last_hidden_layer -> output + last_hidden_layer, puis layer_nbr fois dans hidden layer, avec la derniere fois pas les activations (input pas modifiable : pas de weight/bias derriere)

        n_cost = Network.cost_propagate(self, self.weights[-1], 0, 0, 0, cost)  # On a deja le cost (celui des outputs)

        for layer in range(self.layer_nb):

            n_cost = Network.cost_propagate(self, self.weights[-layer-2], n_cost, self.layers[-layer-1], self.weights[-layer-1])

        self.weights[0].transpose()

    def cost_propagate(self, w_matrix, last_cost, layer, last_weight, err=0):
        """ Should compute one step of the propagation

            Last weight sert a calculer la n_cost_matrix"""

        w_matrix.transpose()

        if err:

            cost_matrix = err

        else:  # compute cost_matrix

            # Not for ouputs (last/first in backprop) layer

            cost_matrix = Matrix.matrix_product(last_weight, last_cost)

            last_weight.transpose()

            layer.add(cost_matrix, self.learning_rate)  # applies the error matrix to the biases (=layer) matrix (est effectue une fois de moins : derniere layer a pas de biais)

        w_matrix.weight_add_cost(cost_matrix, self.learning_rate)  # applies the error(/cost) matrix to the weights matrix

        return cost_matrix


def sigmoid(x):

    if x < -10:

        return 0

    elif x > 10:

        return 1

    return 1 / (1 + math.exp(-x))


def main():

    nbr_input = 2

    layer_nb = 1

    layer_size = 1

    nb_output = 2

    train_range = 10

    training_data = [[[1 for x in range(nbr_input)], [0.5, 0.5]] for x in range(train_range)]  # The input and the expected output

    reseau = Network(nbr_input, layer_nb, layer_size, nb_output, 1, training_data)

    reseau.train()


if __name__ == "__main__":

    # main()

    n = Network(1, 0, 0, 1)

    n.print_net()

    print(Matrix.to_array(n.feedforward([0])))
