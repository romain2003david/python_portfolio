import numpy as np

ar = np.array

from pig_tv import *


def sgn(x):
    if x>=0:
        return 1
    return -1


def sigmoid(x):
   return 1 / (1 + np.exp(-x))


def sigmoid_prime(x):
    s = sigmoid(x)
    return np.multiply(np.exp(-x), np.multiply(s, s))


class Network:

    def __init__(self, input_nb, neuron_nb, output_nb, loss=None, max_parameter_val=10, redu_learning_rate=1):
        self.input_nb = input_nb
        self.neuron_nb = neuron_nb
        self.output_nb = output_nb

        self.weights = Network.rd_initializer_mat((self.neuron_nb, input_nb))
        self.weights_out = Network.rd_initializer_mat((output_nb, self.neuron_nb))
        self.bias = Network.rd_initializers(self.neuron_nb)

        self.activations = np.zeros(self.neuron_nb)
        self.outputs = np.zeros(self.output_nb)

        if loss == None:
            loss = lambda label,output:sum(np.multiply(label-output, label-output))
        self.loss = loss

        self.labels = []

        self.max_parameter_val = max_parameter_val
        self.redu_learning_rate = redu_learning_rate

    def set(self, weights=None, weights_out=None, bias=None):
        if weights != None:
            self.weights = np.array(weights)
        if weights_out != None:
            self.weights_out = np.array(weights_out)
        if bias != None:
            self.bias = np.array(bias)

    def rd_initializer():
        return np.random.random(1)[0]

    def rd_initializers(n):
        return np.array([Network.rd_initializer() for i in range(n)])

    def rd_initializer_mat(shape):
        return np.array([[Network.rd_initializer() for j in range(shape[1])] for i in range(shape[0])])
            

    def feedforward(self, input_):
        assert(len(input_)==self.input_nb)

        self.activations = self.bias+self.weights.dot(input_)
        
        self.outputs = self.weights_out.dot(self.activations)  # sum(np.multiply(self.activations, self.weights_out))

        if np.isnan(self.outputs).any():
            print("Problem with feedforward")
            print(self.bias,self.weights, input_)
            self.print()
            exit(-1)

        return sigmoid(self.outputs)

    def print(self):
        print("first weights : {}, scd w : {}, bias: {}".format(self.weights, self.weights_out, self.bias))

    def center_data(self, xs):
        """ centers and reducts every feature of the matrix (individuals x features) """
        return
        xs -= xs.mean(axis=0)
        xs /= np.std(xs, axis=0)

    def backpropagate(self, xs, ys, learning_rate=0.1, call_back_fct=None, test=True):
        assert(len(ys[0])==self.output_nb)
        if test:
            print("BACKPROPAGATION")

        batch_size = len(xs)
        #

        losses = np.zeros(batch_size)
        errors = 0

        for i in range(batch_size):

            x, y = xs[i], ys[i]
            y_guess = self.feedforward(x)
            difference = y-y_guess
            losses[i] = difference.dot(difference)

            # gradient of quadratic loss

            activat_sigm_diff = sigmoid_prime(self.outputs)
            minus_dl_on_df = 2*learning_rate*difference
            relative_to_output = np.multiply(minus_dl_on_df, activat_sigm_diff)

            activation_deriv = self.weights_out.transpose().dot(relative_to_output)

            self.weights_out += relative_to_output.reshape((self.output_nb, 1)).dot(self.activations.reshape((1, self.neuron_nb)))  # + bcs two minuses are combined (we descend the gradient)
            if np.isnan(self.weights_out).any() or np.isinf(self.weights_out).any():
                print(learning_rate,difference,self.activations,self.bias, self.weights.dot(x), self.bias+self.weights.dot(x))
                exit(-1)

            self.bias += activation_deriv
            if np.isnan(self.bias).any() or np.isinf(self.bias).any():
                print(learning_rate,difference,self.activations,self.bias, self.weights.dot(x), self.bias+self.weights.dot(x))
                exit(-1)

            self.weights += x.reshape((self.input_nb, 1)).dot(activation_deriv.reshape(1, self.neuron_nb)).transpose()
            if np.isnan(self.weights).any() or np.isinf(self.weights).any():
                print(learning_rate,difference,self.activations,self.bias, self.weights.dot(x), self.bias+self.weights.dot(x))
                exit(-1)

            if call_back_fct:
                call_back_fct(xs, ys)

            if not self.right_prediction(x, ys[i]):  # sgn(y_guess) != sgn(ys[i]):
                errors += 1

        self.limit_parameter_size()

        

        print(100*errors/batch_size, "% of errors in training")

    def learn(self, xs, ys, n_train=4, center_data=False, call_back_fct=None, learning_rate=0.6):

        if center_data:
            self.center_data(xs)

        for n in range(n_train):
            print("training layer nb {}, learning rate is {}".format(n, learning_rate))
            self.compare_prediction(xs, ys)
            self.backpropagate(xs, ys, learning_rate, call_back_fct=call_back_fct)
            learning_rate *= self.redu_learning_rate

    def guess_label(self, guess):
        return np.argmax(guess)

        dists = abs(self.labels-guess)
        return self.labels[np.argmin(dists)]

    def compare_prediction(self, xs, ys, center_data=False, test=False):
        if test:
            print("ACCURACY")

        if center_data:
            self.center_data(xs)

        batch_size = len(xs)

        losses = np.zeros(batch_size)
        errors = 0

        for i in range(batch_size):
            x = xs[i]
            y_guess = self.feedforward(x)
            diff=(y_guess-ys[i])
            losses[i] = np.multiply(diff, diff).mean()
            if not self.right_prediction(x, ys[i]):#sgn(y_guess) != sgn(ys[i]):
                errors += 1

        tot_loss = losses.mean()#axis=0)
        print("mse : ", tot_loss)
        error_freq = errors/batch_size
        print(100*error_freq, "% of errors in validating")
        #self.print()
        return error_freq

    def right_prediction(self, x, y, test=False):
        label = self.guess_label(self.feedforward(x))
        if test:
            print(label, y, x, self.feedforward(x))
        return y[label]==1

    def split_data(xs, ys):
        n = len(xs)
        x_test, x_validate = xs[:n//2], xs[n//2:]
        y_test, y_validate = ys[:n//2], ys[n//2:]

        return x_test, x_validate, y_test, y_validate

    def learn_and_validate(self, xs, ys, call_back_fct=None, n_train=4, learning_rate=0.1):

        self.center_data(xs)
        n=len(xs)

        x_test, x_validate, y_test, y_validate = Network.split_data(xs, ys)

        self.learn(x_test, y_test, center_data=False, call_back_fct=call_back_fct, n_train=n_train, learning_rate=learning_rate)
        self.compare_prediction(x_validate, y_validate, center_data=False)

    def limit_parameter_size(self):

        self.weights.clip(-self.max_parameter_val, self.max_parameter_val)
        self.weights_out.clip(-self.max_parameter_val, self.max_parameter_val)
        self.bias.clip(-self.max_parameter_val, self.max_parameter_val)


class DotClassifier(Network):

    def __init__(self, neuron_nb, output_nb, learning_rate=0.1):

        Network.__init__(self, 2, neuron_nb, output_nb)

        self.colors = [BLACK, RED, GREEN]

        self.n_train = 7

        self.learning_rate = learning_rate

    def draw_separation(self):
        return

        ord1 = -self.bias/self.weights[1]
        ord2 = ord1-screen_width*self.weights[0]/self.weights[1]

        pygame.draw.line(screen, BLUE, (0, ord1), (screen_width, ord2))

    def draw_points(self, xs, ys):
        dist = max(max(xs[:,0])-min(xs[:,0]), max(xs[:,1])-min(xs[:,1]))
        small = abs(min(min(xs[:,0]), min(xs[:,1])))
        batch_size = len(xs)
        for i in range(batch_size):
            x, y = xs[i], ys[i]
            pos_x=(x+np.array([small, small]))*screen_height/dist

            col = [int((np.argmax(y)+1)*255/self.output_nb) for i in range(3)]  # self.colors[ys[i]]  # 
            pygame.draw.circle(screen, col, pos_x, 5)
            if self.right_prediction(x, y):
                pygame.draw.circle(screen, GREEN, pos_x, 7, 2)
            else:
                pygame.draw.circle(screen, RED, pos_x, 7, 2)

        abs1 = -small
        abs2 = dist

        # draws the separating hyperplane

        for n in range(self.neuron_nb):

            bi = self.bias[n]
            wi = self.weights[n]
            ord1 = -bi/wi[1]-abs1*wi[0]/wi[1]
            ord2 = -bi/wi[1]-abs2*wi[0]/wi[1]
            pt1 = (np.array([abs1, ord1])+np.array([small, small]))*screen_height/dist
            pt2 = (np.array([abs2, ord2])+np.array([small, small]))*screen_height/dist
            pygame.draw.line(screen, BLUE, pt1, pt2)

    def draw_situation(self, xs, ys):

        screen.fill(WHITE)

        self.draw_points(xs, ys)
        self.draw_separation()
        pygame.display.update()

        #time.sleep(.1)

    def learn_and_validate(self, xs, ys, niter=None):
        if niter == None:
            niter=self.n_train
        x_learn = xs.copy()
        call_back_fct = self.draw_situation
        Network.learn_and_validate(self, x_learn, ys, call_back_fct=call_back_fct, n_train=niter, learning_rate=self.learning_rate)
        #self.draw_situation(xs, ys)
        

        

def rand_gauss(n=100, mu=[1, 1], sigmas=[0.1, 0.1]):
    """Sample  points from a Gaussian variable.
    Parameters
    ----------
    n : number of samples
    mu : centered
    sigma : standard deviation
    """
    d = len(mu)
    res = np.random.randn(n, d)
    return np.array(mu + res * sigmas)

def rand_bi_gauss(n1=100, n2=100, mu1=[1, 1], mu2=[-1, -1], sigmas1=[0.1, 0.1],
                  sigmas2=[0.1, 0.1]):
    """Sample points from two Gaussian distributions.
    Parameters
    ----------
    n1 : number of sample from first distribution
    n2 : number of sample from second distribution
    mu1 : center for first distribution
    mu2 : center for second distribution
    sigma1: std deviation for first distribution
    sigma2: std deviation for second distribution
    """
    ex1 = rand_gauss(n1, mu1, sigmas1)
    ex2 = rand_gauss(n2, mu2, sigmas2)
    y = np.hstack([np.ones(n1), -1 * np.ones(n2)])
    y = y.astype('int')
    X = np.vstack([ex1, ex2])
    ind = np.random.permutation(n1 + n2)
    return X[ind, :], y[ind]


def rand_tri_gauss(n1=100, n2=100, n3=100, mu1=[1, 1], mu2=[-1, -1], mu3=[0, 0], sigmas1=[0.1, 0.1],
                  sigmas2=[0.1, 0.1], sigmas3=[0.1, 0.1]):
    """Sample points from two Gaussian distributions.
    Parameters
    ----------
    n1 : number of sample from first distribution
    n2 : number of sample from second distribution
    mu1 : center for first distribution
    mu2 : center for second distribution
    sigma1: std deviation for first distribution
    sigma2: std deviation for second distribution
    """
    ex1 = rand_gauss(n1, mu1, sigmas1)
    ex2 = rand_gauss(n2, mu2, sigmas2)
    ex3 = rand_gauss(n3, mu3, sigmas3)
    y = np.hstack([np.ones(n1), -1 * np.ones(n2), np.zeros(n3)])
    y = y.astype('int')
    X = np.vstack([ex1, ex2, ex3])
    ind = np.random.permutation(n1 + n2+n3)
    return X[ind, :], y[ind]

def rand_n_gauss(ns, mus, sigmass):
    """Sample points from two Gaussian distributions.
    Parameters
    ----------
    n1 : number of sample from first distribution
    n2 : number of sample from second distribution
    mu1 : center for first distribution
    mu2 : center for second distribution
    sigma1: std deviation for first distribution
    sigma2: std deviation for second distribution
    """
    m = len(mus)
    exs = [rand_gauss(ns, mus[i], sigmass[i]) for i in range(m)]
    y = np.hstack([np.ones(ns)*i for i in range(m)]).astype(int)
    X = np.vstack(exs)
    y_vects = np.zeros((m*ns, m))
    for i in range(len(y)):
        y_vects[i, y[i]] = 1
    ind = np.random.permutation(ns*m)
    return X[ind, :], y_vects[ind]


def in_circle(n):
    X = np.zeros((n, 2))
    y = np.zeros((n, 2))
    for i in range(n):
        X[i] = ar([random.random(), random.random()])
        if np.linalg.norm(X[i]-ar([0.5, 0.5])) < 0.4:
            y[i][0] = 1
        else:
            y[i][1] = 1
        
    return X, y


class GeneticNetworks:

    def __init__(self, neuron_nb, X, y, pool_size=50):

        self.neuron_nb = neuron_nb

        self.X, self.y = X, y

        self.input_nb = len(self.X[0])
        self.output_nb = len(self.y[0])

        self.pool_size = pool_size

        self.nets = [DotClassifier(neuron_nb, self.output_nb) for i in range(pool_size)]

    def train_nets(self):

        x_test, x_validate, y_test, y_validate = Network.split_data(self.X, self.y)

        for net in self.nets:
            net.learn(x_test, y_test, n_train=4, learning_rate=0.6)

        results = [self.nets[i].compare_prediction(x_validate, y_validate) for i in range(self.pool_size)]
        best_net = self.nets[np.argmin(results)]
        best_net.learning_rate = 0.1
        best_net.redu_learning_rate = 0.8

        best_net.learn_and_validate(self.X, self.y, 30)

        
        


def classify_normals():
    #X, y = rand_bi_gauss(5, 5, mu1=[200, 100], mu2=[100, 200], sigmas1=[20, 10], sigmas2=[10, 10])
    n=500
    X, y = rand_bi_gauss(n, n, mu1=[1, 1], mu2=[-1, -2], sigmas1=[1, 1], sigmas2=[3, 1])
    #X, y = rand_tri_gauss(n, n, n, mu1=[1, 1], mu2=[-1, -2], mu3=[0, 0], sigmas1=[1, 1], sigmas2=[3, 1], sigmas3=[1, 1])
    #X, y = rand_tri_gauss(n, n, n, mu1=[1, 1], mu2=[-1, -2], mu3=[0, 0], sigmas1=[.1, .1], sigmas2=[.3, .1], sigmas3=[.1, .1])
    X, y = rand_n_gauss(n, mus=[[-1, 1], [0, 1], [-2, -3], [1, -1]], sigmass=[[.2, .1], [.1, .1], [.1, .1], [.3, .4]])
    #X, y = rand_n_gauss(3, mus=[[-1, 1], [1, 1], [-2, -1], [1, -1]], sigmass=[[.2, .1], [.1, .1], [.1, .1], [.3, .4]])
    X, y = in_circle(n)

    gen_net = GeneticNetworks(3, X, y)
    gen_net.train_nets()

    return

    for i in range(1):
        net = DotClassifier(3, 2)
        #net.set(weights = [[0.28485409, 0.44165848], [0.08903234, 0.33591097]], weights_out= [0.78150545, 0.31539767], bias= [0.21191161, 0.46077893])

        net.learn_and_validate(X, y, 30)






classify_normals()






        
            

            
