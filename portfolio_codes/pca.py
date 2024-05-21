from numpy import *


class PCA:

    def __init__(self, liste_individus, liste_caracteristiques, matrices_inds_cars):
        """ each matrix line contains a different individual (a specific car for instance), whereas the columns contain the features (weight for ex) """

        self.liste_individus = liste_individus
        self.liste_caracteristiques = liste_caracteristiques
        self.matrices_inds_cars = matrices_inds_cars
        self.matrices_centre_reduit = zeros(self.matrices_inds_cars.shape)

        self.ind_nb = len(self.liste_individus)
        self.car_nb = len(self.liste_caracteristiques)

        self.init_centre_reduit()

        self.pca = None
        self.compute_principal_components()

    def pca_from_feature_dicts(list_dicts):
        list_features = []
        matrix = []
        for dico in list_dicts:
            for feature in list(dico.keys()):
                if not feature in list_features:
                    list_features.append(feature)

        matrix = zeros((len(list_dicts), len(list_features)))

        for idx_f in range(len(list_features)):
            for idx_d in range(len(list_dicts)):
                try:
                    matrix[idx_d][idx_f] = list_dicts[idx_d][list_features[idx_f]]
                except:
                    pass
                #else 0

        return PCA(list_dicts, array(list_features), matrix)

    def get_car(self, ind_idx, car_idx):
        return self.matrices_inds_cars[ind_idx, car_idx]

    def get_cars(self, car_idx):
        return self.matrices_inds_cars[:, car_idx]

    def get_ind(self, ind_idx):
        return self.matrices_inds_cars[ind_idx, :]

    def init_centre_reduit(self):

        mean_cars = [mean(self.get_cars(k)) for k in range(self.car_nb)]

        var_cars = [cov(self.get_cars(k)) for k in range(self.car_nb)]  # [mean(multiply(self.get_cars(k), self.get_cars(k))-mean_cars[k]**2*ones(self.ind_nb)) for k in range(self.car_nb)]

        for ind_idx in range(self.ind_nb):
           for car_idx in range(self.car_nb):
               self.matrices_centre_reduit[ind_idx, car_idx] = (self.matrices_inds_cars[ind_idx, car_idx]-mean_cars[car_idx])
               if var_cars[car_idx]:
                   self.matrices_centre_reduit[ind_idx, car_idx] /= sqrt(var_cars[car_idx])

    def get_covariance_mat(self):
        return self.matrices_centre_reduit.transpose().dot(self.matrices_centre_reduit)

    def compute_principal_components(self):
        cov_mat = self.get_covariance_mat()
        eigen_vals, eigen_vects = linalg.eig(cov_mat)

        epsilon = 0.0001

        dict_eigs = {}

        c = 0
        for lambd in eigen_vals:
            affected=False
            for key in list(dict_eigs.keys()):
                if abs(key-lambd) < epsilon:
                    dict_eigs[key].append(eigen_vects[:,c])
                    affected = True
            if not affected:
                dict_eigs[round(lambd, 3)] = [eigen_vects[:,c]]
            c += 1

        self.pca = dict_eigs
        #print(self.pca)

    def best_comp(self):
        eigen_vals = list(self.pca.keys())

        max_val = max(eigen_vals)

        best_vect = self.pca[max_val][0]

        max_coef = max(abs(best_vect))

        print("principal component :\n")

        print("max_coef : ", max_coef)
        for i in range(len(best_vect)):
            if abs(best_vect[i]) >= max_coef/10:
                print(self.liste_caracteristiques[i], " : ", best_vect[i])

        for i in range(self.ind_nb):
            print(i, " : ", self.get_ind(i).dot(best_vect))


class Texte:

    def __init__(self, name):

        self.name = name

        self.dico_words = {}

        self.dico_word_type = {}

        self.load_text()

        self.sentences = []

        #print(self.dico_words)

    def add_to_dico(self, word):
        try:
            self.dico_words[word] += 1
        except KeyError:
            self.dico_words[word] = 1

    def load_sentences(self):
        with open("recueil_romans/"+self.name+".txt", encoding="utf-8") as texte:
            for line in texte.readlines():

                for sentence in line.split("."):
                    self.sentences.append(sentence.split())

    def classify_words(self):

        self.dico_word_type = {ke:[0 for i in range(self.model.nb_hidden_states)]}
        
        for sentence in self.sentences:
            likely_states = self.model.guess_hidden_states(sentence)
            for i in range(len(sentence)):
                word = sentence[i]
                self.dico_word_type[word][likely_states[i]] += 1

##        for word in list(self.dico_word_type.keys()):
##            

            

    def load_text(self):

        def delete_weird(word):
            deleted=False
            for idx in range(len(word)):
                lettre = word[idx]
                if ord(lettre) > 1000 or ord(lettre) <= 32:
                    idx = word.index(lettre)
                    if idx > len(word)/2:
                        word = word[:idx]
                    else:
                        word = word[idx+1:]
                    return word

        with open("recueil_romans/"+self.name+".txt", encoding="utf-8") as texte:
            for line in texte.readlines():
                words = line.split()
                for word in words:

                    if word.isdecimal():
                        continue

                    word = word.lower()                    
                    delete = True
                    while delete:
                        a = delete_weird(word)
                        if a == None:
                            delete=False
                        else:
                            word=a

                    if word == "":
                        break
                    if word[0] == "(":
                        self.add_to_dico(word[0])
                        word = word[1:]
                    if len(word) > 1 and word[1] == "'":
                        word = word[2:]
                    if word[-3:] == "...":
                        self.add_to_dico(word[-3:])
                        word = word[:-3]
                    while word != "" and word[-1] in [".", ",", ";", "!", "?", ")"]:
                        self.add_to_dico(word[-1])
                        word = word[:-1]

                    self.add_to_dico(word)


class LikelinessWord:

    def __init__(self, B, init_states, final_states):
        self.B = B
        self.init_states = init_states  # likeliness of a state to be the initial state
        self.final_states = final_states  # likeliness of a state to be the final state

    def likelinesses(self, word):
        return np.ones(

    def likeliness(self, word, state):
        return 1
    

class SentenceModel:

    def __init__(self, A, B, init_states, final_states):
        self.A = A
        self.hidden_state_nb = len(A)  # there exists nouns, verbs, adjectives...
        self.B = B  # class equivalent to matrix of size hidden_state_nb*state_nb (type of words, and types of letters)
        self.init_states = init_states  # likeliness of a state to be the initial state
        self.final_states = final_states  # likeliness of a state to be the final state

        self.cum_sumsA = [np.cumsum(A[i]) for i in range(len(A))]
        self.cum_sumsB = [np.cumsum(B[:, i]) for i in range(len(A))]

        self.states = []
        self.observations = []

        self.col_nb = 28
    
    def etat_suivant(self):
        if len(self.states) == 0:
            n_st = rd_cumsum(self.pi)
        else:
            st = self.states[-1]
            n_st = rd_cumsum(self.cum_sumsA[st])
        self.states.append(n_st)
    
    def create_observations(self):
        for st in self.states:
            observ = rd_cumsum(self.cum_sumsB[st])
            self.observations.append(observ)
    
    def create_seq(self):
        for i in range(self.col_nb):
            self.etat_suivant()
        self.create_observations()
    
    def get_seq(self):
        
        self.states = []
        self.observations = []
        
        self.create_seq()
        
        return self.observations

    def guess_hidden_states(self, seq):
        """ seq is a list of words """
        n = len(seq)
        A, B = self.A, self.B
        hstate_nb = class_model.hidden_state_nb
        likeliness_table = np.zeros((n+2, hstate_nb))
        ancestor_table = np.zeros((n+2, hstate_nb))
        
        likeliness_table[0] = self.init_states.copy()  # mul(self.init_states, B.likelinesses(seq[0]))

        for i in range(1, n):
            for j in range(hstate_nb):
                new_likes = mul(mul(likeliness_table[i-1,:],A[:, j]), B.likeliness(seq[i],j])
                ancestor_table[i, j] = np.argmax(new_likes)
                likeliness_table[i, j] = new_likes[ancestor[i, j]]

        for j in range(hstate_nb):
            new_likes = self.init_states[j]*mul(likeliness_table[-2,:],A[:, j])
            ancestor_table[-1, j] = np.argmax(new_likes)
            likeliness_table[-1, j] = new_likes[ancestor_table[-1, j]]

        best_seq = []  # will contain the hidden states the sequence is the most likely to be made of (according to the Markov model)
        best_seq.append(np.argmax(likeliness_table[-1]))  # the last state that's the likeliest

        for i in range(n):
            best_seq.append(ancestor_table[best_seq[-1]])
        r
        return best_seq.reverse()


def get_english_hidden_transitions():
    return np.load("grammar/grammar_markov_english_model.txt")


def main():

    test = True
    if not test:
        txt1 = Texte("chartreuse_de_parme")
        txt2 = Texte("rouge_et_noir")
        txt3 = Texte("therese_raquin")
        txt4 = Texte("peau_de_chagrin")

        txts = [txt1, txt2, txt3, txt4]

        dicos = [txt.dico_words for txt in txts]
        pca = PCA.pca_from_feature_dicts(dicos)

    else:
        txt1 = Texte("roman_test")
        txt2 = Texte("roman_test2")
        txt3 = Texte("roman_test3")
        txt4 = Texte("roman_test_english")

        pca = PCA.pca_from_feature_dicts([txt1.dico_words, txt2.dico_words, txt3.dico_words])

    #pca.best_comp()

    sentence_markov = [[]]
    B = LikelinessWord()
    init_sta, final_sta = np.zeros(len(sentence_markov)), np.zeros(len(sentence_markov))
    init_sta[0] = 1
    final_sta[-1] = 1

    sentence_model = SentenceModel(sentence_markov, B, init_sta, final_sta)
        

main()












