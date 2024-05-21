def get_expr(filename):

    with open(filename, "r") as file:

        for line in file:

            name, expr_str = line

            n_expr = ExpressionNommee(name, expr_str)


class Operateur:

    priority = 0

    def __le__(op2):

        return priority <= op2.priority


class Power(Operateur):

    self.symbole = "^"

    self.priority = 1

class Multiplication(Operateur):

    self.symbole = "*"

    self.priority = 2


class Division(Operateur):

    self.symbole = "/"

    self.priority = 2


class Sum(Operateur):

    self.symbole = "+"

    self.priority = 3


class Substraction(Operateur):

    self.symbole = "-"

    self.priority = 3







class ExpressionReguliere:

    operateurs_reguliers = [Or, Etoile, 

    operateurs = [Sum, Substraction, Division, Multiplication, Power]

    operateurs.sort()

    operateurs.reverse()

    operateurs_str = [op.symbole for op in operateurs]

    def __init__(self, expr_str):

        self.expr = expr_str

    def decoupe(self):

        if self.expr[0] == "(" and self.expr[-1] == ")":

            return Expression(self.expr[1:-1])

        else:

            for x in operateurs_str:  # based on priority of operation

                if x in self.expr:

                    

            

    def eval(self):

        


class ExpressionCarac(ExpressionReguliere):

    def  __init__(self, carac):

        self.carac = carac

    def get_automate(self):

        etat1 = Etat("1", init=True)

        etat2 = Etat("2", final=True)

        transitions = {}

        transitions[etat1] = {carac:etat2}

        return Automate(etats, transitions)



class EtoileExpression(ExpressionReguliere):

    def  __init__(self, expr):

        self.expr1 = expr1

    def get_automate(self):

        automate = expr1.get_automate()

        etat1 = Etat(1, init=True)

        etat2 = Etat(2, final=True)

        transitions = {}

        transitions[etat1] = {carac:etat2}

        return Automate(etats, transitions)

class OuExpression(ExpressionReguliere):

    def  __init__(self, expr1, expr2):

        self.expr1 = expr1

        self.expr2 = expr2

    def get_automate(self):

        # automates deterministes

        automate1 = expr1.get_automate()

        automate2 = expr2.get_automate()

        etat1 = Etat(1, init=True)

        etats = [etat1]

        automate1.rename_states(first_state=2)

        automate2.rename_states(first_state=2+len(automate1.etats))

        transitions = {}

        transitions[etat1] = {carac:etat2}

        return Automate(etats, transitions)


class ExpressionNommee:

    def __init__(self, name, expr_str):

        self.expr = expr

        self.expr = ExpressionReguliere(expr_str)



class Etat:

    def __init__(self, name, init=False, final=False):

        self.initial = init

        self.final = final

        self.state_name = name


class Automate:

    def __init__(self, etats, transitions):

        self.etats = etats

        self.transitions = transitions

        self.etat_init = [etat for etat in etats if etat.init]

        self.etat_final = [etat for etat in etats if etat.init]

        self.deterministe = len(self.etat_init) == 1

    def update_init_final(self):

        self.etat_init = [etat for etat in etats if etat.init]

        self.etat_final = [etat for etat in etats if etat.init]

        self.deterministe = len(self.etat_init) == 1

    def create_from_expr(expr):

        return expr.get_automate()

    def est_reconnu(self, mot):

        if self.deterministe:

            etat = self.etat_init

            for carac in mot:

                try:

                    etat = self.transitions[etat][carac]

                except KeyError:

                    return False

            return etat.final

        else:

            Automate.determiniser(self)

                

    def determiniser():
        """ cree l'automate deterministe des parties"""

        pass

    def rename_states(self, first_state=1):

        name_change = {self.etats[x].name:x+first_state for x in range(len(self.etats))}

    def rename_state(self, last_state, n_state):

        name_change = {self.etats[x].name:x+first_state for x in range(len(self.etats))}

        def rename_dico_values(dico, rename_dico):

            {x:rename_dico[dico[x]] for x in dico.keys()}

        def rename_dico_keys(dico, rename_dico):

            return {rename_dico[x]:dico[x] for x in dico.keys()}

        def rename_dico_transitions(dico, rename_dico):

            return {rename_dico[x]:rename_dico_values(dico[x], rename_dico) for x in dico.keys()}

        name_change = {self.etats[x].name:x+first_state for x in range(len(self.etats))}

        n_transitions = rename_dico_transitions(self.transitions, name_change)

        for state in self.etats:

            state.name = name_change[state.name]

    

    def replace_state(state_name, n_state):

        index = [x.name for x in self.etats].index(state_name)

        self.etats[index] = n_state

        


if __name__ == "__main__":

    get_expr("expr_reguliere_calculette.txt")


