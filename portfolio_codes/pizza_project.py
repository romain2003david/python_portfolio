class User:

    def __init__(self, name, age, taille, masse):

        self.name = name

        self.age = age

        self.taille = taille

        self.masse = masse

        self.imc = get_imc(self.taille, self.masse)

        self.objectif = 0

        User.define_objectif(self)

        print("Vos objectifs ont bien ete definis")

        self.programme = 0

        self.regime = 0

    def menu(self):

        entree = input("Bonjour {}.\nQue voulez vous faire ?\n1) Choisir un programme de musculation\n2) Choisir un regime\n3) Se deconnecter\n".format(self.name))

        if entree == "1":

            User.set_programme(self)

        elif entree == "2":

            User.set_regime(self)

        elif entree == "3":

            pass

        else:

            print("Mauvaise entree")

            User.define_objectif(self)
        

    def define_objectif(self):

        entree = input("Que veux-tu ?\n1) Secher\n2) Prendre de la masse violemment\n3) Se muscler globalement\n")

        if entree == "1":

            self.objectif = 0

        elif entree == "2":

            self.objectif = 1

        elif entree == "3":

            self.objectif = 2

        else:

            print("Mauvaise entree")

            User.define_objectif(self)

        
    def print_imc(self):

        print(self.imc)

    def presenter_user(self):

        print("L'utilisateur {} a {} ans et voudrait {}.\nAvec les mensurations suivantes, {} m, {} kg.\nMaintenant il faut que tu {}".format(self.name, self.age, self.objectif, self.taille, self.masse, self.programme))

    def set_programme(self):

        if self.objectif == 0:

            self.programme = "fais du cardio"

        elif self.objectif == 1:

            self.programme = "va a la salle"

        elif self.objectif == 2:

            self.programme = "va au street"

        print("Votre programme a ete selectionne")

    def set_regime(self):

        # fonction a completer
        print("Votre regime a ete selectionne")

def get_imc(height, weight):

    imc = weight/(height)**2

    return imc

        

    

    
    
"""    if imc < 18.5:
return("vous ètes en stade de magreur")

    elif 18.5 < imc < 24.9:

        return("votre poids est normal fragile va !!!!!")
    
    elif 25 < imc < 29.9 :

        return("vous etes en """
        


def create_user():

    user_name = input("name\n")

    age = int(input("age\n"))

    height = int(input("entre ta taille pd\n"))

    weight = int(input("entre ton poids de gros lard stp\n"))

    user = User(user_name, age, height, weight)

    print("Bonjour {}, votre compte a ete cree".format(user_name))

    return user


def main():

##    hatime = User("hatime", 19, 1.64, 57)
##
##    hatime.print_imc()

    romèx = User("romèx", 17, 1.78, 64)

    romèx.presenter_user()

    user = create_user()

    user.presenter_user()





if __name__ == "__main__":

    main()
