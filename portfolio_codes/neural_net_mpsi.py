import numpy as np

import random

def creer_liste_1_dim(moy,écart_type,lg):
    u=np.random.normal(moy,écart_type,lg)
    L=[]
    for i in range(lg):
        L.append(u[i])
    return L

def creer_liste_2_dim(moy,écart_type,ligne,colone):
    L=[]
    for i in range(ligne):
        L.append(creer_liste_1_dim(moy, écart_type,colone))
    return L

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
        


class Matrix:
    
    def __init__(self, row, col, contenu=None, auto_init=False):
        
        self.row = row
        
        self.col = col

        if contenu == None:
        
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

                n_mat.contenu[i][j] = self.contenu[i][j]+mat.contenu[i][j]

        return n_mat

    def __len__(self):
        """  returns row nb  """

        return len(self.contenu)

    def col_nb(self):

        """  returns col nb  """

        return self.col

    def dot_product(mat1, mat2):

        if mat1.col != mat2.row:

            print("Bad format for dot product")

        else:

            n_mat = Matrix(mat1.row, mat2.col)

            for i in range(mat1.row):

                for j in range(mat2.col):

                    n_mat.contenu[i][j] = sum(mat1.contenu[i][k]*mat2.contenu[k][j] for k in range(mat1.col))

            return n_mat

    def apply_function_to(self, function):
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


class Net:
    
    def __init__(self, nb_input, nb_output, nb_layer, layer_size):
        
        self.nb_input = nb_input
        
        self.nb_output = nb_output
        
        self.nb_layer = nb_layer
        
        self.layer_size = layer_size
        
        self.z_activations = []
        
        ## creer les weight
        
        self.cost_function = [0 for x in range(nb_output)]
        
        self.weights = [Matrix(layer_size, nb_input, auto_init=True)]
        
        for x in range(nb_layer-1):
            
            self.weights.append(Matrix(layer_size, layer_size, auto_init=True))
        
        self.weights.append(Matrix(nb_output, layer_size, auto_init=True))

    def __repr__(self):

        rep_string = "\n## Printing Network\n"

        for x in range(self.nb_layer):

##            print("Bias layer", x+1)
##
##            self.biases[x].print()

            rep_string += "Weight layer " + str(x+1)

            rep_string += self.weights[x].__repr__()

        rep_string += "Weight layer" + str(self.nb_layer+1)

        rep_string += self.weights[-1].__repr__()

        rep_string += "\n## End Network\n"

        return rep_string

    def feedforward(self, input_mat):
        
        last_activation = input_mat

        self.z_activations.append(input_mat)
        
        for x in range(self.nb_layer+1):

            print(self.weights[x], "x", last_activation)
            
            Z = Matrix.dot_product(self.weights[x], last_activation)
            
            last_activation = Matrix.apply_function_to_matrix(Z, sigmoid)
            
            self.z_activations.append(Z)
        
        return last_activation
    
    def learn(self, inputs, expected_outputs):
        
        for input_ in inputs:
            
            gotten_output = Net.feedforward(self, input_)
            
            self.cost_function = apply_fun_betw_lists(gotten_output, expected_output, lambda x, y:0.5*(x-y)**2)
            
            Net.back_propagate(self, gotten_output, expected_output)
    
    def back_propagate(self, output, expected_output):

        ## defining vars

        #defines matrices where deltas (tweaks that are to be applied) are stored
        # weight deltas
        delta_matrix_weights = [Matrix(self.nb_output, self.layer_size)]
        
        for x in range(self.nb_layer-1):
            
            delta_matrix_weights.append(Matrix(self.layer_size, self.layer_size))
            
        delta_matrix_weights.append(Matrix(self.layer_size, self.nb_input))

        # activation deltas (used to compute most weight deltas (except first one, at the right)
        
        delta_matrix_activations = [Matrix(self.layer_size, 1) for x in range(self.nb_layer)]

        # allege le code
        ZS = [self.z_activations[x].contenu for x in range(len(self.z_activations))]

        WS = [self.weights[x].contenu for x in range(len(self.weights))]

        # Computing deltas

        # rectifications pour la derniere matrice de weight
        
        for i in range(self.nb_output):  # loops on output layer size
            
            for j in range(self.layer_size):  # loops on last hidden layer size

                deriv_cost = (output.contenu[i][0]-expected_output.contenu[i][0])
                
                delta_matrix_weights[0].contenu[i][j] = deriv_cost*sigmoid_prime(ZS[-1][i][0])*sigmoid(ZS[-2][j][0])
        
        
        # rectifications pour la derniere couche d'activations
        
        for i in range(self.layer_size):  # loops on hidden layer size : each "activation neuron" will get modified, on the sum of tweaks due to every connection that it has
            
            for j in range(self.nb_output):  # loops on every connection (ouput layer size)

                print(output)

                deriv_cost = (output.contenu[j][0]-expected_output.contenu[j][0])

                delta_matrix_activations[0].contenu[i][0] += deriv_cost*sigmoid_prime(ZS[-1][j][0])*WS[-1][j][i]
        
        
        # rectifications pour les couches d'activations précédentes
        
        for x in range(1, self.nb_layer):
            
            # uses the delta of the activation computed previously (that is more at the right in the net

            last_AC = delta_matrix_activations[x-1].contenu
                    
            for i in range(self.layer_size):
                
                for j in range(self.layer_size):

                   delta_matrix_activations[x].contenu[i][0] += last_AC[j][0]*sigmoid_prime(ZS[-x-1][j][0])*WS[-x-1][j][i]

        # rectifications pour les matrices de weight précédentes

        for x in range(1, self.nb_layer+1):  # computes the tweaks backwards (although not necessary, activations were already computed...) ; loops on every weight matrix except the last one that has been done before

            # delta activations that have been computed are used to change the weights

            delta_AC = delta_matrix_activations[x-1].contenu

            for i in range(len(delta_matrix_weights[x])):  # loops on size of hidden layer that's at the right (should always be hidden layer size)

                for j in range(delta_matrix_weights[x].col_nb()):  # loops on size of hidden layer that's at the right (should always be hidden layer size, expect for last one comuted, linked to inputs)
                    print(len(delta_matrix_weights[x]), delta_matrix_weights[x].col_nb(), len(ZS[x]), len(ZS[x-1]))
                    delta_matrix_weights[x].contenu[i][j] = delta_AC[i][0]*sigmoid_prime(ZS[-1-x][i][0])*sigmoid(ZS[-x-2][j][0])
            

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

    nb_layers, layer_size = 2, 5

    nb_o = 1

    net = Net(nb_i, nb_o, nb_layers, layer_size)

    print(net)

    test_input = [0.2, 0.9, .1]

    test_mat_input = Matrix(len(test_input), 1, contenu=test_input)

    expected_output = Matrix(1, 1, [0.2])

    print("Feeding forward")

    output = net.feedforward(test_mat_input)

    print(output)

    print("Back propagating")

    net.back_propagate(output, expected_output)

if __name__ == "__main__":

    main()
        




