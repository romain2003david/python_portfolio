import numpy as np

import random

import time

from pig_tv import *


def sigmoid(x):
    
    return 1/(1+np.exp(-x))


def sigmoid_prime(x):  # check
    
    return sigmoid(x) * (1-sigmoid(x))


def random_normal():
    # pour les matrices, repartition normale, centree reduite
    
    return random.normalvariate(0, 1)



def apply_fun_betw_lists(list1, list2, fun):
    
    res_list = [0 for x in range(len(list1))]
    
    if len(list1) == len(list2):
    
        for x in range(len(list1)):
         
            res_list[x] = fun(list1, list2)
     
        return res_list
    
    else:
     
        print("erreur taille listes")


##def concaténation_colone(mat1, mat2):#même nombre de lignes
##  
##    mat_f=Matrix(len(mat1), len(mat2[0])+len(mat1[0]))
##    
##    for i in range(len(mat1)):
##        
##        for j in range(len(mat1.contenu[0])):
##            
##            mat_f.contenu[i][j]=mat1.contenu[i][j]
##    
##    for i in range(len(mat1)):
##        
##        for j in range(len(mat2.contenu[0])):
##            
##            mat_f.contenu[i][j+len(mat1[0])]=mat2.contenu[i][j]
##    
##    return mat_f 
##
##def concaténation_ligne(mat1, mat2):#même nombre de colonne
##    
##    mat_f=Matrix(len(mat1)+len(mat2),len(mat1.contenu[0]))
##
##    for i in range(len(mat1)):
##        
##        for j in range(len(mat1.contenu[0])):
##            
##            mat_f.contenu[i][j]=mat1.contenu[i][j]
##    
##    for i in range(len(mat2)):
##        
##        for j in range(len(mat1.contenu[0])):
##            
##            mat_f.contenu[i+len(mat1)][j]=mat2.contenu[i][j]
##    
##    return mat_f



class Matrix:
    
    def __init__(self, row, col, contenu=None, auto_init=False, is_identite=False):
     
        self.row = row
     
        self.col = col

        if contenu == None:  # matrice nulle
     
            self.contenu = [[0 for x in range(col)] for z in range(row)]

        else: # la matrice a deja une valeur fixee

            # Les matrices sont des vecteurs (colonne/ligne) : facilite l'ecriture

            if row == 1:  # matrice ligne

                self.contenu = [contenu]

            elif col == 1:  # matrice colonne

                self.contenu = [[contenu[x]] for x in range(len(contenu))]

            else:

                self.contenu = contenu
     
        if auto_init:
         
            Matrix.init_random_weights(self)

        if is_identite:

            Matrix.set_identite(self)

    def __repr__(self):

        string = "\n\n"

        car_space = 4

        for i in range(self.row):

            string += "["

            for j in range(self.col-1):

                string += str(self.contenu[i][j])+" "*max((4-len(str(self.contenu[i][j]))), 1)

            string += str(self.contenu[i][self.col-1])

            string += "]\n"

        string += "\n"

        return string
          
    def __add__(self, mat):

        n_mat = Matrix(self.row, self.col)

        for i in range(self.row):

            for j in range(self.col):

                n_mat.contenu[i][j] = self.contenu[i][j] + mat.contenu[i][j]

        return n_mat

    def __sub__(self, mat):

        n_mat = Matrix(self.row, self.col)

        for i in range(self.row):

            for j in range(self.col):

                n_mat.contenu[i][j] = self.contenu[i][j] - mat.contenu[i][j]

        return n_mat

    def __mul__(self, scalaire):

        n_mat = Matrix(self.row, self.col)

        for i in range(self.row):

            for j in range(self.col):

                n_mat.contenu[i][j] = self.contenu[i][j] * scalaire

        return n_mat

    def __len__(self):
        """  returns row nb  """

        return len(self.contenu)

    def format(self):

        return (self.row, self.col)

    def col_nb(self):

        """  returns col nb  """

        return self.col

    def dot_product(mat1, mat2):

        if mat1.col != mat2.row:

            print("Bad format for dot product")

            print(mat1, mat2)

            raise("error")

        else:

            n_mat = Matrix(mat1.row, mat2.col)

            for i in range(mat1.row):

                for j in range(mat2.col):

                    n_mat.contenu[i][j] = sum(mat1.contenu[i][k]*mat2.contenu[k][j] for k in range(mat1.col))

            return n_mat

    def apply_function(self, function):
        """ applies a given function to each element of the matrix """

        for y in range(self.row):

            for x in range(self.col):

                self.contenu[y][x] = function(self.contenu[y][x])

    def apply_function_to_matrix(mat, function):

        n_mat = Matrix(mat.row, mat.col)

        for y in range(mat.row):

            for x in range(mat.col):

                n_mat.contenu[y][x] = function(mat.contenu[y][x])

        return n_mat

    def init_random_weights(self):
     
        for i in range(self.row):
         
            for j in range(self.col):
             
                self.contenu[i][j] = random_normal()

    def set_identite(self):

        if self.row == self.col:

            self.contenu = [[0 for x in range(self.col)] for z in range(self.row)]

            for x in range(self.col):

                self.contenu[x][x] = 1

        else:

            print("Matrice pas carree..")

    def concatene_one(self, x=1):

        if self.col == 1:

            self.row += 1

            self.contenu.append([x])

        else:

            print("Attention la matrice n'est pas une colonne")

    def get_transposed(self):

        n_mat = Matrix(self.col, self.row)

        for y in range(self.row):

            for x in range(self.col):

                n_mat.contenu[x][y] = self.contenu[y][x]

        return n_mat

    def take_out_col(self, col_nb):
        """ takes col between 0 and self.col-1 """

        self.col -= 1

        for i in range(self.row):

            del self.contenu[i][col_nb]

    def with_take_out_col(self, col_nb):
        """ takes col between 0 and self.col-1 """

        n_matrix = Matrix(self.row, self.col-1)

        for i in range(self.row):

            for j in range(self.col):

                if j != col_nb:

                    n_matrix.contenu[i][j] = self.contenu[i][j]

        return n_matrix


class Net:
    
    def __init__(self, nb_input, nb_output, nb_layer, layer_size, particulier=0):

        # csts

        self.big_nb = 1000

        self.learn_rate = 1#0**(-2)

        self.batch_size = 2

        self.backprop_step = 0

        # parametres
     
        self.nb_input = nb_input
     
        self.nb_output = nb_output
     
        self.nb_layer = nb_layer
     
        self.layer_size = layer_size
     
        Net.init_z_activations(self)

        self.cost_function = [0 for x in range(nb_output)]

        ## creer les weight

        if particulier:

            self.weights = [Matrix(2, 3, contenu=[[1, 2, 3], [-2, 5, -1]]), Matrix(2, 3, contenu=[[1, 2, 3], [-2, 5, -1]])]

        else:

            if self.nb_layer > 0:  # complex net
             
                self.weights = [Matrix(layer_size, nb_input+1, auto_init=True)]  # +1 colonne pour definir les bias
             
                for x in range(nb_layer-1):
                 
                    self.weights.append(Matrix(layer_size, layer_size+1, auto_init=True))  # de meme
             
                self.weights.append(Matrix(nb_output, layer_size+1, auto_init=True))  # de meme

            else: # perceptron

                self.weights = [Matrix(nb_output, nb_input+1, auto_init=True)]  # +1 colonne pour definir les bias

    def draw(self):

        #screen.fill(WHITE)

        pos = [[] for x in range(self.nb_layer+2)]

        x_place = screen_width/(self.nb_layer+2)

        # drawing cst

        neuron_radius = 30

        weight_width = 5

        # drawing inputs

        y_place = screen_height/(self.nb_input+1)  # leaves a space up and down

        blank_space = y_place-neuron_radius

        for x in range(self.nb_input+1):

            pygame.draw.circle(screen, BLUE, (int(x_place//2), int(blank_space/2+(y_place)*x)), neuron_radius)

            pos[0].append((int(x_place//2), int(blank_space/2+(y_place)*x)))

        # drawing layers

        for l in range(self.nb_layer):

            y_place = screen_height/(self.layer_size+1)  # leaves a space up and down

            #biases = self.weights[l].get_transposed().contenu[-1]  # les biais sont dans la derniere colonne de la matrice weight, donc dans la derniere ligne de sa transposee

            blank_space = y_place-neuron_radius

            for x in range(self.layer_size+1):

                neuron_color = 0  # set_val_to_different_array([-3, 3], [0, 255], biases[x], mustbe_inborne=True)

                pygame.draw.circle(screen, [neuron_color, neuron_color, neuron_color], (int(x_place*(l+1.5)), int(blank_space/2+(y_place)*x)), neuron_radius)

                pos[l+1].append((int(x_place*(l+1.5)), int(blank_space/2+(y_place)*x)))

        # drawing outputs

        y_place = screen_height/(self.nb_output)  # leaves a space up and down

        blank_space = y_place-neuron_radius

        for x in range(self.nb_output):

            pygame.draw.circle(screen, RED, (screen_width-int(x_place//2), int(blank_space/2+(y_place)*x)), neuron_radius)

            pos[-1].append((screen_width-int(x_place//2), int(blank_space/2+(y_place)*x)))

        # drawing weights

        for m in range(len(self.weights)):

            matrix = self.weights[m].contenu
##
##            matrix = matrix.with_take_out_col(matrix.col-1)
##
##            matrix = matrix.contenu

            for y in range(len(matrix)):

                for x in range(len(matrix[0])):

                    weight_size = 10

                    weight_color = set_val_to_different_array([-weight_size, weight_size], [0, 255], matrix[y][x], mustbe_inborne=True)

                    start_neuron = pos[m][x]

                    end_neuron = pos[m+1][y]

                    pygame.draw.line(screen, [weight_color, weight_color, weight_color], start_neuron, end_neuron, weight_width)

        ##

        pygame.display.update()

    def init_z_activations(self):

        self.z_activations = [Matrix(self.layer_size+1, 1) for x in range(self.nb_layer)]  # +1 for biases

        self.z_activations.insert(0, Matrix(self.nb_input+1, 1))  # +1 for biases

        self.z_activations.append(Matrix(self.nb_output, 1))

    def __repr__(self):

        rep_string = "\n## Printing Network\n"

        rep_string += "network with {} inputs, {} hidden layers of size {}, and {} output(s).\n\n".format(self.nb_input, self.nb_layer, self.layer_size, self.nb_output)

        for x in range(self.nb_layer):

##          print("Bias layer", x+1)
##
##          self.biases[x].print()

            rep_string += "Weight layer " + str(x+1)

            rep_string += self.weights[x].__repr__()

        rep_string += "Weight layer" + str(self.nb_layer+1)

        rep_string += self.weights[-1].__repr__()

        rep_string += "\n## End Network\n"

        return rep_string

    def feedforward(self, input_mat, intensive_print=False):
     
        last_activation = input_mat

        last_activation.concatene_one(self.big_nb)

        self.z_activations[0] += last_activation

        last_activation = Matrix.apply_function_to_matrix(last_activation, sigmoid)

        if intensive_print:

            print("sigmoised input")

            print(last_activation)
     
        for x in range(self.nb_layer+1):

            if intensive_print:

                print("\nlayer ", x, self.weights[x], "x", last_activation)
                        
            Z = Matrix.dot_product(self.weights[x], last_activation)

            if intensive_print:

                print("result of dot product", Z)

            if x != self.nb_layer:  # we don't add bias to output layer

                Z.concatene_one(self.big_nb)

            self.z_activations[x+1] += Z

            last_activation = Matrix.apply_function_to_matrix(Z, sigmoid)

        if intensive_print:

            print("zs", self.z_activations)

        return last_activation
    
    def learn(self, inputs, expected_outputs, test_print=False):

        print_user = (len(inputs) < 100) and test_print

        if test_print:

            print("starting learning process")

        start_chrono = time.time()

        if len(inputs) % self.batch_size != 0:

            print("Warning : example batch not adapted to batch size")
     
        for i in range(len(inputs)//self.batch_size):

            # initialises settings for new batch

            Net.init_z_activations(self)

            output_difference = Matrix(1, self.nb_output)

            mean_expected_output = Matrix(1, self.nb_output)

            # feedforwards

            for j in range(self.batch_size):

                x = i*self.batch_size + j

                if print_user:

                    print("batch ", i, "learning step ", x)

                input_x = inputs[x]

                gotten_output = Net.feedforward(self, input_x, intensive_print=test_print)

                output_difference += (gotten_output - expected_outputs[x])

                mean_expected_output += expected_outputs[x]

            # computes mean of z activations

            for k in range(len(self.z_activations)):

                self.z_activations[k] *= (1/self.batch_size)

            mean_expected_output *= (1/self.batch_size)

            # computes mean cost of training examples
             
            self.cost_function = output_difference.apply_function(lambda x:0.5*x**2)

            # backpropagation
             
            delta_weight_matrices = Net.back_propagate(self, Matrix.apply_function_to_matrix(self.z_activations[-1], sigmoid), mean_expected_output, intensive_print=test_print)

            for w in range(len(delta_weight_matrices)):

                self.learn_rate = np.log10(self.backprop_step)

                delta_weight_matrices[w] *= self.learn_rate

##                if self.weights[w].format() != delta_weight_matrices[w].format():
##
##                    print(self.weights[w].format() , delta_weight_matrices[w].format(), i, k, w)

                self.weights[w] += delta_weight_matrices[-w-1]

        if test_print:

            print("learning ended")

            print(time.time()-start_chrono)
    
    def back_propagate(self, output, expected_output, test_print=False, intensive_print=False):

        self.backprop_step += 1

        ## defining vars

        #defines matrices where deltas (tweaks that are to be applied) are stored
        # weight deltas

        if self.layer_size > 0:  # complex net

            delta_matrix_weights = [Matrix(self.nb_output, self.layer_size+1)]
         
            for x in range(self.nb_layer-1):
             
                delta_matrix_weights.append(Matrix(self.layer_size, self.layer_size+1))  # There is a +1 because of the bias indeed we directly implemented the bias inside of the weight matrice
             
            delta_matrix_weights.append(Matrix(self.layer_size, self.nb_input+1))  # +1 for bias

        else:  # perceptron

            delta_matrix_weights = [Matrix(self.nb_output, self.nb_input+1)]

        # activation deltas (used to compute most weight deltas (except first one, at the right)
     
        delta_matrix_activations = [Matrix(self.layer_size, 1) for x in range(self.nb_layer)]  # there is one for each hidden layer

        # allege le code
        ZS = [self.z_activations[x].contenu for x in range(len(self.z_activations))]

        if test_print or intensive_print:

            print("zs", ZS)

            if intensive_print:

                print("deltas containers:")

                print("activations\n", delta_matrix_activations, "weights\n", delta_matrix_weights)

        WS = [self.weights[x].contenu for x in range(len(self.weights))]

        # Computing deltas

        # rectifications pour la derniere matrice de weight

        if intensive_print:

            print("computation of first delta weight matrix")

        last_delta_w_matrix = delta_matrix_weights[0]  # the more to the right in the net
     
        for i in range(len(last_delta_w_matrix)):  # loops on output layer size
         
            for j in range(len(last_delta_w_matrix.contenu[0])):  # loops on last hidden layer size, there is a +1 because of the bias

                deriv_cost = -(output.contenu[i][0] - expected_output.contenu[i][0])

                last_delta_w_matrix.contenu[i][j] = deriv_cost*sigmoid_prime(ZS[-1][i][0])*sigmoid(ZS[-2][j][0])

                if test_print or intensive_print:

                    print(i, j, last_delta_w_matrix.contenu[i][j], deriv_cost, sigmoid_prime(ZS[-1][i][0]),sigmoid(ZS[-2][j][0]),output.contenu[i][0],expected_output.contenu[i][0], ZS[-1][i][0])

        if intensive_print:

            print("computation of first delta activation matrix")

        # rectifications pour la derniere couche d'activations
     
        for i in range(self.layer_size):  # loops on hidden layer size : each "activation neuron" will get modified, on the sum of tweaks due to every connection that it has
         
            for j in range(self.nb_output):  # loops on every connection (ouput layer size)

                deriv_cost = -(output.contenu[j][0]-expected_output.contenu[j][0])

                delta_matrix_activations[0].contenu[i][0] += deriv_cost*sigmoid_prime(ZS[-1][j][0])*WS[-1][j][i]

                if intensive_print:

                    print(i, j)
     
        if intensive_print:

            print("computation of other delta activation matrices")

        # rectifications pour les couches d'activations précédentes
     
        for x in range(1, self.nb_layer):
         
            # uses the delta of the activation computed previously (that is at the right of the weight matrix in the net)

            last_AC = delta_matrix_activations[x-1].contenu

            for i in range(self.layer_size):
             
                for j in range(self.layer_size):

                    delta_matrix_activations[x].contenu[i][0] += last_AC[j][0]*sigmoid_prime(ZS[-x-1][j][0])*WS[-x-1][j][i]

                    if intensive_print:

                        print(x, i, j)

        if intensive_print:

            print("computation of other delta weight matrices")

        # rectifications pour les matrices de weight précédentes

        for x in range(1, self.nb_layer+1):  # computes the tweaks backwards (although not necessary, activations were already computed...) ; loops on every weight matrix except the "last" (closest to outputs) one that has been done before;

            # delta activations that have been computed are used to change the weights

            delta_AC = delta_matrix_activations[x-1].contenu

            for i in range(len(delta_matrix_weights[x])):  # loops on size of hidden layer that's at the right (should always be hidden layer size)

                for j in range(delta_matrix_weights[x].col_nb()):  # loops on size of hidden layer that's at the right (should always be hidden layer size, expect for last one comuted, linked to inputs)

                    delta_matrix_weights[x].contenu[i][j] = delta_AC[i][0]*sigmoid_prime(ZS[-1-x][i][0])*sigmoid(ZS[-x-2][j][0])

                    if intensive_print:

                        print(x, i, j)

        if intensive_print:

            print("final deltas")

            print("activations")

            print(delta_matrix_activations)

            print("weights")

            print(delta_matrix_weights)

            print("##")

        return delta_matrix_weights




##def backpropagate_généralisé(self,outpouts,exp_outpouts):
##    l=len(outpouts)
##    assert l==len(exp_outpouts),"pas compatible"
##    Delta=backpropagate_simple(self,outpouts.[0],exp_outpouts.[0])
##    for i in range(1,l):
##        Delta=Delta.__add__(Delta,backpropagate_simple(self,outpouts[i],exp_outpouts[i]))
##    Delta.multiplication_par_scalaire(1/l)  #On fait une moyenne
##    return Delta



def main():

    print("TESTS BASIQUES MATRICES")

    print("defining matrices")

    test_mat1 = Matrix(3, 3, contenu=[[1, 2, 3], [4, 5, 6], [7, 8, 9]])

    test_mat2 = Matrix(3, 1, contenu=[1, 2, 3])

    test_mat3 = Matrix(3, 3, auto_init=True)

    test_mat4 = Matrix(1, 7, auto_init=True)

    test_mat6 = Matrix(3, 3)

    test_mat6.set_identite()

    print(test_mat1, test_mat2, test_mat3, test_mat4, test_mat6)

    ##

    print("adding up matrices")

    print(test_mat1+test_mat3)

    ##

    print("multiplying matrices")

    test_mat5 = Matrix(1, 3, contenu=[1, 2, 3])

    print(Matrix.dot_product(test_mat5, test_mat2))

    print(Matrix.dot_product(test_mat2, test_mat5))

    print(Matrix.dot_product(test_mat6, test_mat1))

    print("####")

    print("TESTS BASIQUES RESEAUX")

    nb_i = 3

    nb_layers, layer_size = 3, 4

    nb_o = 1

    net = Net(nb_i, nb_o, nb_layers, layer_size)

    print(net)

    test_input = [0.2, 0.9, .1]

    test_mat_input = Matrix(len(test_input), 1, contenu=test_input)

    expected_output = Matrix(1, 1, [0.2])

    print("Feeding forward")

    output = net.feedforward(test_mat_input)

    print("output", output)

    print("Back propagating")

    net.back_propagate(output, expected_output)

    # test avec reseau particulier

    net = Net(2, 2, 1, 2, particulier=1)

    print("With arbitrary net")

    print(net)

    test_input = [0, 1]

    test_mat_input = Matrix(len(test_input), 1, contenu=test_input)

    output = net.feedforward(test_mat_input)

    print("With input [0, 1], output", output)

    test_input = [1, 0]

    test_mat_input = Matrix(len(test_input), 1, contenu=test_input)

    output = net.feedforward(test_mat_input)

    print("With input [1, 0], output", output)

    expected_output = Matrix(2, 1, [1, .2])

    net.back_propagate(output, expected_output)

    screen.fill(LIGHT_BLUE)

##    # first problem : AND with perceptron
##
##    print("first problem : AND")
##
##    nb_i = 2
##
##    nb_layers, layer_size = 0, 0
##
##    nb_o = 1
##
##    net = Net(nb_i, nb_o, nb_layers, layer_size)
##
##    print(net)
##
##    for x in range(2):
##
##        for y in range(2):
##
##            test_input = [x, y]
##
##            print(x, y, "output", net.feedforward(Matrix(len(test_input), 1, contenu=test_input)))
##
##    for y in range(10):
##
##        net.draw()
##
##        wait()
##
##        #creating inputs and expected outputs
##
##        inputs = []
##
##        expected_outputs = []
##
##        for x in range(2000):
##
##            test_input = [random.randint(0, 1), random.randint(0, 1)]
##
##            expected_outputs.append(Matrix(1, 1, [test_input[0]*test_input[1]]))
##
##            inputs.append(Matrix(len(test_input), 1, contenu=test_input))
##
##        net.learn(inputs, expected_outputs)
##
##        print(net)
##
##        for x in range(2):
##
##            for y in range(2):
##
##                test_input = [x, y]
##
##                print(x, y, "output", net.feedforward(Matrix(len(test_input), 1, contenu=test_input)))

    ##

    # second problem : AND with bigger network

##    print("second problem : AND")
##
##    nb_i = 2
##
##    nb_layers, layer_size = 1, 1
##
##    nb_o = 1
##
##    net = Net(nb_i, nb_o, nb_layers, layer_size)
##
##    print(net)
##
##    #creating inputs and expected outputs
##
##    inputs = []
##
##    expected_outputs = []
##
##    for x in range(2):
##
##        for y in range(2):
##
##            test_input = [x, y]
##
##            print(x, y, "output", net.feedforward(Matrix(len(test_input), 1, contenu=test_input)))
##
##    for x in range(200000):
##
##        test_input = [random.randint(0, 1), random.randint(0, 1)]
##
##        expected_outputs.append(Matrix(1, 1, [test_input[0]*test_input[1]]))
##
##        inputs.append(Matrix(len(test_input), 1, contenu=test_input))
##
##
##    net.learn(inputs, expected_outputs, test_print=False)
##
##    print(net)
##
##    for x in range(2):
##
##        for y in range(2):
##
##            test_input = [x, y]
##
##            print(x, y, "output", net.feedforward(Matrix(len(test_input), 1, contenu=test_input)))

    # third problem : points higher than a line

##    print("third problem : LINE")
##
##    nb_i = 2
##
##    nb_layers, layer_size = 1, 1
##
##    nb_o = 1
##
##    net = Net(nb_i, nb_o, nb_layers, layer_size)
##
##    print(net)
##
##    #creating inputs and expected outputs
##
##    inputs = []
##
##    expected_outputs = []
##
##    test_line = [0.5, 100]  # sous la forme y = ax+b, on donne a et b
##
##    for x in range(100000):
##
##        test_input = [random.randint(0, 800), random.randint(0, 700)]
##
##        test_input_changed = [set_val_to_different_array([0, 800], [-3, 3], test_input[0]), set_val_to_different_array([0, 700], [-3, 3], test_input[1])]
##
##        higher = (test_input[0]*test_line[0]+test_input[1]) < test_input[1]
##
##        expected_outputs.append(Matrix(1, 1, [higher]))
##
##        inputs.append(Matrix(len(test_input), 1, contenu=test_input_changed))
##
##    net.learn(inputs, expected_outputs, test_print=False)
##
##    # screen displaying
##
##    screen.fill(WHITE)
##
##    pygame.draw.line(screen, RED, (0, 100), (800, 500), 5)
##
##    pygame.display.update()
##
##    for x in range(200):
##
##        test_input = [random.randint(0, 800), random.randint(0, 700)]
##
##        test_input_changed = [set_val_to_different_array([0, 800], [-3, 3], test_input[0]), set_val_to_different_array([0, 700], [-3, 3], test_input[1])]
##
##        test_input_mat = Matrix(len(test_input), 1, contenu=test_input_changed)
##
##        higher_net = net.feedforward(test_input_mat)
##
##        if higher_net.contenu[0][0] > 0.5:
##
##            color = GREEN
##
##        else:
##
##            color = BLUE
##
##        pygame.draw.circle(screen, color, (test_input[0], test_input[1]), 5)
##
##    pygame.display.update()
##
##    print(net)

    # fourth problem : points higher than a line


##    print("fourth problem : PROGRESSIVE LINE")
##
##    nb_i = 2
##
##    nb_layers, layer_size = 0, 0
##
##    nb_o = 1
##
##    net = Net(nb_i, nb_o, nb_layers, layer_size)
##
##    print(net)
##
##    upd = True
##
##    screen.fill(WHITE)
##
##    test_line = [-0.5, 500]  # sous la forme y = ax+b, on donne a et b
##
##    pygame.draw.line(screen, RED, (0, test_line[1]), (screen_width, screen_width*test_line[0]+test_line[1]), 5)
##
##    c = 0
##
##    while upd:
##
##        c += 1
##
##        if c%100 == 0:
##
##            print(c*10)
##
##        #creating inputs and expected outputs
##
##        inputs = []
##
##        expected_outputs = []
##
##        for x in range(10):
##
##            test_input = [random.randint(0, 800), random.randint(0, 700)]
##
##            test_input_changed = [set_val_to_different_array([0, 800], [-3, 3], test_input[0]), set_val_to_different_array([0, 700], [-3, 3], test_input[1])]
##
##            higher = test_input[0]*(test_line[0])+test_line[1] < test_input[1]
##
##            expected_outputs.append(Matrix(1, 1, [higher]))
##
##            inputs.append(Matrix(len(test_input), 1, contenu=test_input_changed))
##
##        net.learn(inputs, expected_outputs, test_print=False)
##
##        # screen displaying
##
##        for x in range(1000):
##
##            test_input = [random.randint(0, 800), random.randint(0, 700)]
##
##            test_input_changed = [set_val_to_different_array([0, 800], [-3, 3], test_input[0]), set_val_to_different_array([0, 700], [-3, 3], test_input[1])]
##
##            test_input_mat = Matrix(len(test_input), 1, contenu=test_input_changed)
##
##            higher_net = net.feedforward(test_input_mat)
##
##            degr = set_val_to_different_array([0, 1], [0, 255], higher_net.contenu[0][0])
##
##            color = [degr, degr, 0]
##
####            if higher_net.contenu[0][0] > 0.5:
####
####                color = GREEN
####
####            else:
####
####                color = BLUE
##
##            pygame.draw.circle(screen, color, (test_input[0], test_input[1]), 5)
##
##        net.draw()


    print("fifth problem : PROGRESSIVE CIRCLE")

    nb_i = 2

    nb_layers, layer_size = 1, 3

    nb_o = 1

    net = Net(nb_i, nb_o, nb_layers, layer_size)

    print(net)

    upd = True

    screen.fill(WHITE)

    test_circle = [400, 350, 280]  # sous la forme [pos_x, pos_y, radius]

    pygame.draw.circle(screen, RED, test_circle[:2], test_circle[2], 5)

    correct = 0

    incorrect = 0

    screen.fill(LIGHT_BLUE)

    while upd:

        #creating inputs and expected outputs

        inputs = []

        expected_outputs = []

        for x in range(200):

            rand_rad, rand_angle = set_val_to_different_array([0, 1], [0, test_circle[2]], random.random()), set_val_to_different_array([0, 1], [0, 2*np.pi], random.random())

            test_input = [test_circle[0]+rand_rad*cos(rand_angle), test_circle[1]+rand_rad*sin(rand_angle)]

            test_input_changed = [set_val_to_different_array([0, 800], [-3, 3], test_input[0]), set_val_to_different_array([0, 700], [-3, 3], test_input[1])]

            in_circle = (get_distance(test_input, test_circle[:2]) < test_circle[2])

            expected_outputs.append(Matrix(1, 1, [in_circle]))

            inputs.append(Matrix(len(test_input), 1, contenu=test_input_changed))

        net.learn(inputs, expected_outputs, test_print=False)

        inputs = []

        expected_outputs = []

        for x in range(200):

            test_input = [random.randint(0, 800), random.randint(0, 700)]

            test_input_changed = [set_val_to_different_array([0, 800], [-3, 3], test_input[0]), set_val_to_different_array([0, 700], [-3, 3], test_input[1])]

            in_circle = (get_distance(test_input, test_circle[:2]) < test_circle[2])

            expected_outputs.append(Matrix(1, 1, [in_circle]))

            inputs.append(Matrix(len(test_input), 1, contenu=test_input_changed))

        net.learn(inputs, expected_outputs, test_print=False)#True)

        ##
        # screen displaying

##        for x in range(100):
##
##            test_input = [random.randint(0, 800), random.randint(0, 700)]
##
##            test_input_changed = [set_val_to_different_array([0, 800], [-3, 3], test_input[0]), set_val_to_different_array([0, 700], [-3, 3], test_input[1])]
##
##            test_input_mat = Matrix(len(test_input), 1, contenu=test_input_changed)
##
##            in_circle_net = net.feedforward(test_input_mat).contenu[0][0]
##
##            in_circle = (get_distance(test_input, test_circle[:2]) < test_circle[2])
##
##            if round(in_circle_net) == in_circle:
##
##                correct += 1
##
##            else:
##
##                incorrect += 1
##
##            if not random.randint(0, 500):
##
##                print(correct/(incorrect+correct))
##
##                correct = 0
##
##                incorrect = 0
##
##            if in_circle_net > 0.5:
##
##                color = GREEN
##
##            else:
##
##                color = BLUE
##
##            pygame.draw.circle(screen, color, (test_input[0], test_input[1]), 5)

        net.draw()

        pygame.display.update()

    print(net)

##    print("sixth problem : PROGRESSIVE LINE IN THE MIDDLE")
##
##    nb_i = 2
##
##    nb_layers, layer_size = 1, 2
##
##    nb_o = 1
##
##    net = Net(nb_i, nb_o, nb_layers, layer_size)
##
##    print(net)
##
##    upd = True
##
##    screen.fill(WHITE)
##
##    c = 0
##
##    while upd:
##
##        c += 1
##
##        if c%100 == 0:
##
##            print(c*10)
##
##        #creating inputs and expected outputs
##
##        inputs = []
##
##        expected_outputs = []
##
##        for x in range(100):
##
##            test_input = [random.randint(0, 800), random.randint(0, 700)]
##
##            test_input_changed = [set_val_to_different_array([0, 800], [-3, 3], test_input[0]), set_val_to_different_array([0, 700], [-3, 3], test_input[1])]
##
##            between = 300 < test_input[0] < 600 #*(test_line[0])+test_line[1] < test_input[1]
##
##            expected_outputs.append(Matrix(1, 1, [between]))
##
##            inputs.append(Matrix(len(test_input), 1, contenu=test_input_changed))
##
##        net.learn(inputs, expected_outputs, test_print=False)
##
##        # screen displaying
##
##        for x in range(1000):
##
##            test_input = [random.randint(0, 800), random.randint(0, 700)]
##
##            test_input_changed = [set_val_to_different_array([0, 800], [-3, 3], test_input[0]), set_val_to_different_array([0, 700], [-3, 3], test_input[1])]
##
##            test_input_mat = Matrix(len(test_input), 1, contenu=test_input_changed)
##
##            higher_net = net.feedforward(test_input_mat)
##
##            if higher_net.contenu[0][0] > 0.5:
##
##                color = GREEN
##
##            else:
##
##                color = BLUE
##
##            pygame.draw.circle(screen, color, (test_input[0], test_input[1]), 5)
##
##        net.draw()
##
##        #wait()    

    # seventh problem : XOR

##    print("seventh problem : XOR")
##
##    nb_i = 2
##
##    nb_layers, layer_size = 1, 2
##
##    nb_o = 1
##
##    net = Net(nb_i, nb_o, nb_layers, layer_size)
##
##    print(net)
##
##    for x in range(2):
##
##        for y in range(2):
##
##            test_input = [x, y]
##
##            print(x, y, "output", net.feedforward(Matrix(len(test_input), 1, contenu=test_input)))
##
##    for y in range(1000):
##
##        net.draw()
##
##        #creating inputs and expected outputs
##
##        inputs = []
##
##        expected_outputs = []
##
##        for x in range(20000):
##
##            test_input = [random.randint(0, 1), random.randint(0, 1)]
##
##            xor_test = (test_input[1] or test_input[0])-(test_input[1] and test_input[0])
##
##            expected_outputs.append(Matrix(1, 1, [xor_test]))
##
##            inputs.append(Matrix(len(test_input), 1, contenu=test_input))
##
##        net.learn(inputs, expected_outputs)#, test_print=y>100)
##
##        print(net)
##
##        if not random.randint(0, 0):
##
##            for x in range(2):
##
##                for y in range(2):
##
##                    test_input = [x, y]
##
##                    print(x, y, "output", net.feedforward(Matrix(len(test_input), 1, contenu=test_input)))


if __name__ == "__main__":

    main()
     



"""



"""



