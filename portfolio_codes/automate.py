class Automat:

    def __init__(self, states, liste_dico_transition, init_states, final_states):

        self.states = states  # list of integers normally

        self.liste_dico_transition = liste_dico_transition

        self.init_states = init_states  

        self.final_states = final_states

        ##

        self.cur_states = []

        # computes the alphabet, all the allowed symbols

        self.alphabet = []

        for dico in self.liste_dico_transition:

            self.alphabet = [lettre for lettre in dico.keys() if not lettre in self.alphabet]
        ##

    def get_nexts(self, lettre, states):

        next_states = []

        for state in states:

            dico = self.liste_dico_transition[state]

            if lettre in dico.keys():

                next_states.extend(dico[lettre])

        return next_states

    def get_determined_automat(self):

        def name_states(n_states, all_states):
            # returns if its a new group of state, and the group name

            #n_states.sort()

            if n_states in all_states:

                return False, all_states.index(n_states)

            else:

                return True, len(n_states)

        pile_to_do = [self.init_states]

        states_equivalency = [self.init_states]

        new_states = [0]  # how the groups of states will be called in the new automat

        new_liste_dico_transition = {}

        n_final_states = []

        while still:

            cur_states = pile_to_do.pop  # next group of states to deal with

            this_name = states_equivalency.index(cur_states)

            final_state = False

            for state in cur_states:

                if state in self.final_states:

                    final_state = True

            if final_state:

                n_final_states.append(this_name)

            n_dico = {}  # self.new_liste_dico_transition[cur_states]

            for lettre in self.alphabet:

                n_states = self.get_nexts(lettre, cur_states)

                n_states.sort()

                new, name = name_states(n_states, states_equivalency)

                if new:

                    states_equivalency.append(n_states)

                    new_states.append(name)

                    pile_to_do.append(n_states)

                n_dico[lettre] = name

            new_liste_dico_transition[this_name] = n_dico

        liste_dico = [new_liste_dico_transition[i] for i in range(new_states)]

        return DeterministAutomat(new_states, liste_dico, 0, n_final_states)


class DeterministAutomat(Automat):

    def __init__(self, states, liste_dico_transition, init_state, final_states):

        self.init_state = init_state

        Automat.__init__(self, states, liste_dico_transition, None, final_states)

    def read_next(self, lettre):

        dico = self.liste_dico_transition[self.cur_state]

        if lettre in dico.keys():

            self.cur_state = dico[lettre]

        else:

            self.cur_state = None

            return False

    def read_word(self, word):

        self.cur_state = self.init_state

        for lettre in word:

            if not self.read_next(lettre)

            return False

    def automate_disjonction(auto1, auto2):

        pass



def main():

    states = [0, 1, 2]

    auto_indet = Automat(states, [{"a":[0, 1], "b":[2]}, {}, {"a":0, "b":2}], [0], [1])




if __name__ == "__main__":

    main()












