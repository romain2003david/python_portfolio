from pig_tv import *

import numpy

from fractions import Fraction as frac


"""

code that should build a neural network almost from scratch (dealing with matrices, doing the logic of NN, visualising them



array([[ 1.04314163, -0.56480673],
       [ 1.17533508, -1.27912482],
       [-1.73280912, -1.36939963]])


[
[0.8685026406, -0.7689231296]
[-0.1846123059, -0.0529864924]
[0.4666603947, -0.2158118553]
]

"""

def sigmoid(x):

    return 1/(1+exp(-x))


def get_deriv_sigmoid(x):

    return exp(-x)/(1+exp(-x))**2


def test_sigmoids():

    a = [get_deriv_sigmoid(sigmoid(set_val_to_different_array([-300, 300], [-3, 3], x))) for x in range(-300, 300)]

    graph_array(a)

    a = [get_deriv_sigmoid(get_deriv_sigmoid(set_val_to_different_array([-300, 300], [-3, 3], x))) for x in range(-300, 300)]

    graph_array(a)


class Matrix:

    def __init__(self, rows, cols, content=0, randomize=1, mean_gauss=0, ecart_gauss=sqrt(3)/2, range_=1, precision=10, negatif=1, spe_type=None, spe_args=None):

        self.rows = rows

        self.cols = cols

        if content == 0:

            if spe_type == "Id":

                self.content = [[1*(x==y) for x in range(cols)] for y in range(rows)]

            elif spe_type == "Canonique":

                self.content = [[1*((x==spe_args[1]) and (y==spe_args[0])) for x in range(cols)] for y in range(rows)]

            else:

                if randomize == 1:

                    self.content = [[Matrix.get_rand_nbr(self, range_, precision, negatif) for x in range(cols)] for y in range(rows)]

                elif randomize == 2:

                    self.content = [[Matrix.get_rand_gauss(self, mean_gauss, ecart_gauss) for x in range(cols)] for y in range(rows)]

                elif randomize == 3:

                    self.content = [[random.randint(-9, 9) for x in range(cols)] for y in range(rows)]

                elif randomize == 0:

                    self.content = [[0 for x in range(cols)] for y in range(rows)]

        else:

            self.content = content

    def __repr__(self):

        return "Matrix with format {}x{}\n".format(self.rows, self.cols)

    def get_rand_nbr(self, range_, precision, negatif):

        if negatif:

            borne_inf = -range_

        else:

            borne_inf = 0

        return random.randint(borne_inf*10**precision, range_*10**precision)/10**precision

    def get_rand_gauss(mean=0, standard_deviation=1, x="a"):
        """ returns a “normal” (Gaussian) distribution of given mean and standard variation """

##        if x == "a":
##
##            x = random.randint(-5, 5)
##
##        return 1/(standard_deviation*sqrt(2*pi))*e**((-1/2)*((x-mean)/standard_deviation)**2)
        return numpy.random.normal()

    def print(self):

        print("\n[")

        for x in range(self.rows):

            print(self.content[x])

        print("]\n")

    def apply_function_between_matrices(matrix1, matrix2, function):

        if (matrix1.rows == matrix2.rows) and (matrix1.cols == matrix2.cols):

            n_matrix = Matrix(matrix1.rows, matrix1.cols, randomize=0)

            for y in range(n_matrix.rows):

                for x in range(n_matrix.cols):

                    n_matrix.content[y][x] = function(matrix1.content[y][x], matrix2.content[y][x])

            return n_matrix

        else:

            print("Applying function between matrices : Matrices with uncompatible format\n{}\nand\n{}".format(matrix1, matrix2))

    def dot_product(matrix1, matrix2):
        """ returns dot product of two given matrices ; the first matrice needs have same number of columns as the second one has rows ; resulting matrix has rows(m1) cols(m2) """

        if matrix1.cols == matrix2.rows:

            n_matrix = Matrix(matrix1.rows, matrix2.cols, randomize=0)

            for y1 in range(matrix1.rows):

                for y2 in range(matrix2.cols):

                    for x in range(matrix1.cols):

                        n_matrix.content[y1][y2] += matrix1.content[y1][x]*matrix2.content[x][y2]

            return n_matrix

        else:

            print("Dot Product : Matrices with uncompatible format\n{}\nand\n{}".format(matrix1, matrix2))

    def transpose(self):

        n_content = [[] for x in range(self.cols)]

        for nrow in range(self.cols):

            for y in range(self.rows):

                n_content[nrow].append(self.content[y][nrow])

        self.content = n_content

        save_cols = self.cols

        self.cols = self.rows

        self.rows = save_cols

    def apply_function_to_matrix(self, function):
        """ applies a given function to each element of the matrix """

        for y in range(self.rows):

            for x in range(self.cols):

                self.content[y][x] = function(self.content[y][x])

    def apply_function_arg_to_matrix(self, function, arg):
        """ applies a given function with an argument to each element of the matrix """

        for y in range(self.rows):

            for x in range(self.cols):

                self.content[y][x] = function(self.content[y][x], arg)

    def copy(self):

        n_matrix = Matrix(self.rows, self.cols, randomize=0)

        n_matrix.content = self.content

        return n_matrix

    def get_line_switcher(self, line1, line2):
        """ for square matrices only """

        if self.rows == self.cols:

            n_matrix = Matrix(self.cols, self.cols, spe_type="Id")

            mat1 = Matrix(self.cols, self.cols, spe_type="Canonique", spe_args=(line1, line2))

            mat2 = Matrix(self.cols, self.cols, spe_type="Canonique", spe_args=(line2, line1))

            mat3 = Matrix(self.cols, self.cols, spe_type="Canonique", spe_args=(line1, line1))

            mat4 = Matrix(self.cols, self.cols, spe_type="Canonique", spe_args=(line2, line2))

            n_matrix1 = Matrix.apply_function_between_matrices(n_matrix, mat1, lambda x, y:x+y)

            n_matrix2 = Matrix.apply_function_between_matrices(n_matrix1, mat2, lambda x, y:x+y)

            n_matrix3 = Matrix.apply_function_between_matrices(n_matrix2, mat3, lambda x, y:x-y)

            n_matrix4 = Matrix.apply_function_between_matrices(n_matrix3, mat4, lambda x, y:x-y)

            return n_matrix4

    def get_line_adder(self, line, factor):
        """ for square matrices only """

        if self.rows == self.cols:

            n_matrix = Matrix(self.cols, self.cols, spe_type="Id")

            mat1 = Matrix(self.cols, self.cols, spe_type="Canonique", spe_args=(line, line))

            mat1.apply_function_to_matrix(lambda x:x*(factor-1))

            n_matrix1 = Matrix.apply_function_between_matrices(n_matrix, mat1, lambda x, y:x+y)

            return n_matrix1

    def get_line_adder_multiplier(self, added_to_line, added_from_line, factor):
        """ returns the matrices that a square matrix should be multiplied by to add to a line (added_to_line) the content of an other line (added_from_line), multiplied by a constant (factor) """

        if self.rows == self.cols:

            n_matrix = Matrix(self.cols, self.cols, spe_type="Id")

            mat1 = Matrix(self.cols, self.cols, spe_type="Canonique", spe_args=(added_to_line, added_from_line))

            mat1.apply_function_to_matrix(lambda x:x*(factor))

            n_matrix1 = Matrix.apply_function_between_matrices(n_matrix, mat1, lambda x, y:x+y)

            return n_matrix1

    def switch_lines(self, line1, line2):
        """ function that exchanges two lines of a square matrix """

        if self.rows == self.cols:

            if (0 <= line1 <= self.cols) and (0 <= line2 <= self.cols):

                special_matrix = Matrix.get_line_switcher(self, line1, line2)

                new_matrix = Matrix.dot_product(special_matrix, self)

                self.content = new_matrix.content

    def multiply_line(self, line, factor):
        """ function that multiplies a line by a factor in a square matrix """

        if self.rows == self.cols:

            if (0 <= line <= self.cols):

                special_matrix = Matrix.get_line_adder(self, line, factor)

                new_matrix = Matrix.dot_product(special_matrix, self)

                self.content = new_matrix.content

    def add_multiply_lines(self, line1, line2, factor):
        """ function that [see get_line_adder_multiplier] in a square matrix """

        if self.rows == self.cols:

            if (0 <= line1 <= self.cols) and (0 <= line2 <= self.cols):

                special_matrix = Matrix.get_line_adder_multiplier(self, line1, line2, factor)

                new_matrix = Matrix.dot_product(special_matrix, self)

                self.content = new_matrix.content

    def get_inverse(self):
        """ for square matrices only """

        if self.rows == self.cols:

            stored_content = self.content.copy()

            inv_matrix = Matrix(self.cols, self.cols, spe_type="Id")

            for x in range(self.cols):

                # transforms diagonal nb into a 1 (except if 0)

                diag_nb = self.content[x][x]

                if diag_nb != 0:

                    Matrix.multiply_line(self, x, frac(1, diag_nb))

                    inv_matrix.multiply_line(x, frac(1, diag_nb))

                else:

                    print("Annoying 0")

                # getting rid of all other numbers (on top of it, and below it)

                for t in range(self.cols):

                    if t != x:

                        to_delete_content = self.content[t][x]

                        Matrix.add_multiply_lines(self, t, x, to_delete_content*(-1))

                        inv_matrix.add_multiply_lines(t, x, to_delete_content*(-1))

        self.content = stored_content

        return inv_matrix

    def max_index(self):

        if type(self.content[0]) == list:

            return self.content[0].index(max(self.content[0]))

        else:

            return self.content.index(max(self.content))


class Network:

    def __init__(self, input_nb, layer_nb, layer_size, output_nb, precision=-1):

        # network settings

        self.input_nb = input_nb

        self.layer_nb = layer_nb

        self.layer_size = layer_size

        self.output_nb = output_nb

        self.precision = precision

        # learning settings

        self.learning_rate = 10**1

        # initialising bias matrices

        self.biases = []

        for x in range(layer_nb):

            self.biases.append(Matrix(1, layer_size))

        # initialising weight matrices

        self.weights = []

        # input neurons
        self.weights.append(Matrix(input_nb, layer_size, randomize=2))

        self.weights[0].apply_function_to_matrix(lambda x:x*sqrt(2/input_nb))
        #

        #other layers of neurons
        for x in range(layer_nb-1):

            self.weights.append(Matrix(layer_size, layer_size, randomize=2))  # , randomize=2)):

            self.weights[-1].apply_function_to_matrix(lambda x:x*sqrt(2/layer_size))

        # outut_neurons
        self.weights.append(Matrix(layer_size, output_nb, randomize=2))

        self.weights[-1].apply_function_to_matrix(lambda x:x*sqrt(2/layer_size))

        # the activations of feed_forward need be stored for learning

        self.stored_activations = []  # activations when applying feedforward ; activation a = sigmoid(z)

        self.stored_zactivations = []  # zactivations when applying feedforward ; zactivation z(l) = w1*a1(l-1)+w2*a2(l-1)+...+wn*an(l-1)+b(l)

    def print_net(self):
        """ function that prints settings of the network """

        print("Printing Network\n")

        for x in range(self.layer_nb):

            print("Bias layer", x+1)

            self.biases[x].print()

            print("Weight layer", x+1)

            self.weights[x].print()

        print("Weight layer", self.layer_nb+1)

        self.weights[-1].print()

    def feed_forward(self, inputs, store_activations=0):
        """ input is a Matrix instance, and returns the output of a net given this input """

        #Network.print_net(self)

        if store_activations:

            self.stored_activations = [inputs.copy()]

            self.stored_zactivations = []

        if inputs.cols != self.input_nb:

            print("Bad dimension input")

            inputs.print()

            print(inputs.cols)

            return

        for x in range(self.layer_nb):

            #inputs.print()

            #self.weights[x].print()

            inputs = Matrix.dot_product(inputs, self.weights[x])

            #inputs.print()

            #self.biases[x].print()

            inputs = Matrix.apply_function_between_matrices(inputs, self.biases[x], lambda x, y:x+y)

            if store_activations:

                self.stored_zactivations.append(inputs.copy())

            inputs.apply_function_to_matrix(sigmoid)

            if store_activations:

                #inputs.print()

                #print("act")

                self.stored_activations.append(inputs.copy())

        inputs = Matrix.dot_product(inputs, self.weights[-1])

        if store_activations:

            self.stored_zactivations.append(inputs.copy())

        inputs.apply_function_to_matrix(sigmoid)

        if self.precision != -1:

            inputs.apply_function_arg_to_matrix(round, self.precision)

        return inputs  # in fact output

    def backpropagation_step(self, output, expected_output):
        """ tweaks the weights and biases by computing gradient of cost function """

##        #print("backprop")
##
##        # stores the errors of each layer
##        deltas = []
##
##        # computing error in the output layer
##        partil_dev_cost = Matrix.apply_function_between_matrices(output, expected_output, lambda x,y:x-y)
##
##        self.stored_zactivations[-1].apply_function_to_matrix(get_deriv_sigmoid)
##
##        deltas.append(Matrix.apply_function_between_matrices(partil_dev_cost, self.stored_zactivations[-1], lambda x,y:x*y))  # Hadamard product
##
##        # updating weights and biases according to the error
##
##        correcting_bias_matrix = deltas[0].copy()
##
##        correcting_bias_matrix.apply_function_to_matrix(lambda x:x*(-self.learning_rate))
##
##        self.stored_activations[-1].transpose()
##
##        correcting_weight_matrix = Matrix.dot_product(self.stored_activations[-1], correcting_bias_matrix)
##
##        self.weights[-1] = Matrix.apply_function_between_matrices(self.weights[-1], correcting_weight_matrix, lambda x,y:x+y)
##
####        correcting_weight_matrix.print()
####
####        self.stored_activations[-1].print()
####
####        partil_dev_cost.print()
####
####        self.stored_zactivations[-1].print()
##
##        # backpropagating the error
##        for x in range(self.layer_nb):
##
##            self.stored_zactivations[-(x+2)].apply_function_to_matrix(get_deriv_sigmoid)  # modifies the matrix
##
##            transposed_weights = self.weights[-(x+1)].copy()
##
##            #transposed_weights.transpose()
##
##            weight_delta_product = Matrix.dot_product(transposed_weights, deltas[-1])  # using last layer error to compute new one
##
##            self.stored_zactivations[-(x+2)].transpose()
##
##            deltas.append(Matrix.apply_function_between_matrices(weight_delta_product, self.stored_zactivations[-(x+2)], lambda x,y:x*y))  # Hadamard product
##
##            # updating weights and biases according to the error
##
##            correcting_bias_matrix = deltas[-1].copy()
##
##            correcting_bias_matrix.apply_function_to_matrix(lambda x:x*(-self.learning_rate))
##
##            correcting_bias_matrix.transpose()
##
##            self.biases[-(x+1)] = Matrix.apply_function_between_matrices(self.biases[-(x+1)], correcting_bias_matrix, lambda x,y:x+y)
##
##            self.stored_activations[-(x+2)].transpose()
##
##            #self.stored_activations[-(x+2)].print()
##
####            correcting_bias_matrix.print()
####
####            print("w")
####
####            Network.print_net(self)
####
####            self.biases[-(x+1)].print()
####
####            deltas[-1].print()
##            
##            correcting_weight_matrix = Matrix.dot_product(self.stored_activations[-(x+2)], correcting_bias_matrix)
##
##            self.weights[-(x+2)] = Matrix.apply_function_between_matrices(self.weights[-(x+2)], correcting_weight_matrix, lambda x,y:x+y)
##
##            #correcting_weight_matrix.print()

    def backpropagate(self, batch):
        """ input : a batch subdivided in multiple mini batches, each of these mini batches being composed of 1 to n learning examples,
            each example being an array composed of an input and it's expected output """

        print("Recommended mini batches lengths : 1\nYou using {} size".format(len(batch[0])))

        compteur = 0

        for mini_batch in batch:

            #summed_loss = Matrix(1, self.output_nb, randomize=0)

            for example in mini_batch:

                compteur += 1

                input_, expected_output = example

                output = Network.feed_forward(self, input_, store_activations=1)

                Network.backpropagation_step(self, output, expected_output)

                print("Entrainements termines : ", compteur)

##                cost = Matrix.apply_function_between_matrices(output, expected_output, lambda x,y:0.5*(x-y)**2)
##
##                summed_cost = Matrix.apply_function_between_matrices(summed_loss, loss, lambda x, y:x+y)
##
##            summed_cost.apply_function_to_matrix(lambda x:x/len(mini_batch))
##
##            Network.backpropagation_step(self, summed_loss)

    def draw(self):

        screen.fill(WHITE)

        pos = [[] for x in range(self.layer_nb+2)]

        x_place = screen_width/(self.layer_nb+2)

        neuron_radius = 30

        # drawing inputs

        y_place = screen_height/(self.input_nb)  # leaves a space up and down

        blank_space = y_place-neuron_radius

        for x in range(self.input_nb):

            pygame.draw.circle(screen, BLUE, (int(x_place//2), int(blank_space/2+(y_place)*x)), neuron_radius)

            pos[0].append((int(x_place//2), int(blank_space/2+(y_place)*x)))

        # drawing layers

        for l in range(self.layer_nb):

            y_place = screen_height/(self.layer_size)  # leaves a space up and down

            blank_space = y_place-neuron_radius

            for x in range(self.layer_size):

                neuron_color = set_val_to_different_array([-1, 1], [0, 255], self.biases[l].content[0][x])

                pygame.draw.circle(screen, [neuron_color, neuron_color, neuron_color], (int(x_place*(l+1.5)), int(blank_space/2+(y_place)*x)), neuron_radius)

                pos[l+1].append((int(x_place*(l+1.5)), int(blank_space/2+(y_place)*x)))

        # drawing outputs

        y_place = screen_height/(self.output_nb)  # leaves a space up and down

        blank_space = y_place-neuron_radius

        for x in range(self.output_nb):

            pygame.draw.circle(screen, RED, (screen_width-int(x_place//2), int(blank_space/2+(y_place)*x)), neuron_radius)

            pos[-1].append((screen_width-int(x_place//2), int(blank_space/2+(y_place)*x)))

        # drawing weights

        for m in range(len(self.weights)):

            matrix = self.weights[m]

            for y in range(matrix.rows):

                for x in range(matrix.cols):

                    weight_color = 0  # set_val_to_different_array([-1, 1], [0, 255], matrix.content[y][x])

                    start_neuron = pos[m][y]

                    end_neuron = pos[m+1][x]

                    pygame.draw.line(screen, [weight_color, weight_color, weight_color], start_neuron, end_neuron, 1)

        ##

        pygame.display.update()


def main():

    # test matrices

    n1 = Matrix(2, 2)

    print("First matrix")

    n1.print()

    #
    n2 = Matrix(2, 2)

    print("Second matrix")

    n2.print()

    # difference
    n = Matrix.apply_function_between_matrices(n1, n2, lambda x, y:x-y)

    print("Difference")

    n.print()

    # dot products
    n = Matrix.dot_product(n1, n2)

    print("Dot product")

    n.print()

    # different sizes of dot products

    n1 = Matrix(1, 4)

    n2 = Matrix(4, 1)

    print("Dot product 1x1")

    Matrix.dot_product(n1, n2).print()

    n1 = Matrix(5, 4)

    n2 = Matrix(4, 5)

    print("Dot product 5x5")

    n = Matrix.dot_product(n1, n2)

    print("Valid format : ", n.cols == 5, ", ", n.rows == 5)

    # transposition
    n = Matrix(2, 4)

    print("Normal matrix")

    n.print()

    n.transpose()

    print("to transposed matrix")

    n.print()

    # test on lines in square matrices

    m1 = Matrix(4, 4, randomize=3)

    print("Normal matrix:")

    m1.print()

    # line switching
    m1.switch_lines(1, 2)

    print("Switching lines 2 and 3")

    m1.print()

    # multiplying line by factor
    m1.multiply_line(0, 10)

    print("Multiplying lines 1 by a factor of 10")

    m1.print()

    # multiplying a line then adding to other line
    m1.add_multiply_lines(0, 1, -10)

    print("Substracting ten times line 2 from line 1")

    m1.print()

    # finding inverse

    matrix = Matrix(3, 3, [[1, 2, 1], [4, 0, -1], [-1, 2, 2]])

    matrix.print()

    print("Finding inverse")

    matrix.get_inverse().print()

    a
    
    ##
    ## networks test

    input_nb = 3

    net = Network(input_nb, 1, 2, 3, precision=4)

    net.print_net()

    net.draw()

    print("Feedforwarding network")

    for y in [-1, 0, 1]:

        for x in [-1, 0, 1]:

            inputs = [0 for g in range(input_nb)]

            inputs[0] = x

            inputs[1] = y

            net_input = Matrix(1, input_nb, content=[inputs])

            output = net.feed_forward(net_input)

            print("Input:\n", inputs, "\nOutput :\n")

            output.print()

    # testing backpropagation

    net = Network(1, 1, 1, 1)

    net.print_net()

    net.draw()

    # start tests
    print("Input:\n", 1, "\nOutput :\n")

    net_input = Matrix(1, 1, content=[[1]])

    output = net.feed_forward(net_input)

    output.print()

    print("Input:\n", 0, "\nOutput :\n")

    net_input = Matrix(1, 1, content=[[0]])

    output = net.feed_forward(net_input)

    output.print()

    # training network

    training_batch = [[[Matrix(1, 1, [[x%2]]), Matrix(1, 1, [[x%2]])]] for x in range(1)]

    net.backpropagate(training_batch)

    # testing how succesful net is at classification
    print("Input:\n", 1, "\nOutput :\n")

    net_input = Matrix(1, 1, content=[[1]])

    output = net.feed_forward(net_input)

    output.print()

    print("Input:\n", 0, "\nOutput :\n")

    net_input = Matrix(1, 1, content=[[0]])

    output = net.feed_forward(net_input)

    output.print()

    # overal network view

    net.print_net()


if __name__ == "__main__":

    main()


