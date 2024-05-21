#from pig_tv import *
import pickle
#import matplotlib.pyplot as plt


class Caracteristique:

    def __init__(self, code, name, ajr):

        self.code = code
        self.name = name
        self.ajr = ajr

    def __repr__(self):
        return "\nfeature: "+self.code+" : "+self.name+"\n"


class Food:
    info_essentielles = ["Energie", "Eau", "Protéines", "Glucides", "Sucres", "Fibres", "Lipides", "saturés", "Cholestérol"]
    metaux = ["Sodium", "Magnésium", "Phosphore", "Chlorure", "Potassium", "Calcium", "Manganèse", "Fer", "Cuivre", "Zinc", "Sélénium", "Iode"]

    def __init__(self, name, dico_code_car, code_grps, code_ss_grps, reader):

        self.name = name
        self.code_grps = code_grps
        self.code_ss_grps = code_ss_grps

        self.dico_caracteristiques = {}

        self.dico_code_car = dico_code_car

        self.reader = reader
        self.groupe = ""
        self.ss_groupe = ""
        self.ss_ss_groupe = ""
        self.init_groupes()

    def init_groupes(self):
        self.groupe = self.reader.get_grp(self.code_grps)
        self.ss_groupe = self.reader.get_ss_grp(self.code_grps)
        self.ss_ss_groupe = self.reader.get_ss_ss_grp(self.code_ss_grps)

    def add_caracteristique(self, code_cst, value_cst):

        nom_cst = self.dico_code_car[code_cst].name
        self.dico_caracteristiques[nom_cst] = value_cst

    def get_car_value(self, nom_cst):
        try:
            val = self.dico_caracteristiques[nom_cst]
            if val in ["-", "<", "traces"]:
                return 0
            n_val = val.replace(",", ".")
            return float(n_val)
        except KeyError:
            print("The feature ({}) is not in {}".format(nom_cst, self.name))
            return 0

    def str_name_and_car(self, car):
        return "{}: {} : {}".format(self.name, car, self.dico_caracteristiques[car])

    def str_of_car(self, car):
        return "{}: {}".format(self.name, self.dico_caracteristiques[car])

    def print_name_and_car(self, car):
        print(self.str_name_and_car(car))

    def print_grp(self):
        print("{} in {} < {} < {}".format(self.name, self.ss_ss_groupe, self.ss_ss_groupe, self.groupe))

    def __repr__(self):
        return "food : {}\n".format(self.name)

    def print(self):
        print(self.name)
        self.print_info_essentielle()
        self.print_vitamines()
        self.print_metaux()

    def print_all(self):
        print( "food : {}\ncaracteristiques :\n".format(self.name))
        for key in self.dico_caracteristiques.keys():
            print(key)

    def get_vitamines(self):
        liste_vita = []
        for carac in self.dico_caracteristiques.keys():
            if "Vitamine" in carac:
                val = self.dico_caracteristiques[carac]
                if not val in ["0", "<", "-"]:
                    liste_vita.append(carac)
        return liste_vita        

    def print_vitamines(self):
        print("\nVitamines:")

        for carac in self.get_vitamines():
            print("{} : {}".format(carac, self.dico_caracteristiques[carac]))
        print()

    def print_info_essentielle(self):
        print("\nInfos de base:")
        for carac in self.dico_caracteristiques.keys():
            for word in carac.split():
                for word2 in Food.info_essentielles:
                    if word2 in word:
                        val = self.dico_caracteristiques[carac]
                        if val in ["0", "<", "-"]:
                            print("No information on ", carac)
                        else:
                            print("{} : {}".format(carac, val))
        print()

    def print_metaux(self):
        print("\nMetaux:")
        for carac in self.dico_caracteristiques.keys():
            for word in carac.split():
                for word2 in Food.metaux:
                    if word2 in word:
                        val = self.dico_caracteristiques[carac]
                        if not val in ["0", "<", "-"]:
                            print("{} : {}".format(carac, val))
        print()

    def draw_vitamines(self):

        fig, ax = plt.subplots()

        vitas = self.get_vitamines()
        vitas_str = [vit[:13] for vit in vitas]
        counts = [self.dico_caracteristiques[key] for key in vitas]

        ax.bar(vitas_str, counts)

        ax.set_ylabel('apport sur ajr (apports journaliers recommandes)')

        plt.show()


def construct_dico_caracteristiques_ajr():# -> dico_caracs: Dict[str, Caracteristique]
    """ dict links feature code and Feature """

    dico_caracs = {}

    with open("data_aliment/const_2020_07_07_test.xml") as file:
        c = -3
        key = None
        for line in file.readlines():
            c += 1
            if c >= 0:
                print(line.split(), c)
                words = line.split()
                if c%6 == 1:
                    key = words[1]
                elif c%6 == 2:
##                    print(len(words))
##                    key = words[1]
##                    if len(words) >3:
##                        key += words[-3]+words[-2]
                    value = ""
                    for i in range(1, len(words)-1):
                        value+=words[i]+ " "
                    
                elif c%6 == 5:
                    dico_caracs[key] = Caracteristique(key, value, words[0])

    return dico_caracs
    

def construct_dico_caracteristiques():# -> dico_caracs: Dict[str, Caracteristique]

    dico_caracs = {}

    with open("data_aliment/const_2020_07_07.xml") as file:
        c = -3
        key = None
        for line in file.readlines():
            c += 1
            if c >= 0:
                words = line.split()
                if c%5 == 1:
                    key = words[1]
                elif c%5 == 2:
##                    print(len(words))
##                    key = words[1]
##                    if len(words) >3:
##                        key += words[-3]+words[-2]
                    value = ""
                    for i in range(1, len(words)-1):
                        value+=words[i]+ " "
                    
                elif c%5 == 4:
                    dico_caracs[value] = Caracteristique(key, value, 0)
    return dico_caracs


class CodeGrpReader:
    """ reconstructs the suclasses of each food """

    def __init__(self):

        self.dico = {}

        with open("data_aliment/alim_grp_2020_07_07.xml") as file:
            c = -3
            key = None
            for line in file.readlines():
                c += 1
                if c < 0:
                    continue
                k = c % 11
                no_info_idx = [0, 10, 3, 6, 9]
                info_idx = [i for i in range(11) if not i in no_info_idx]
                if k in no_info_idx:
                    continue

                parity = info_idx.index(k)%2

                words = line.split()
                if parity == 0:
                    key = words[1]
                elif parity == 1:
##                    print(len(words))
##                    key = words[1]
##                    if len(words) >3:
##                        key += words[-3]+words[-2]
                    value = ""
                    for i in range(1, len(words)-1):
                        value+=words[i]+ " "

                    if value != "- ":
                        self.dico[key] = value

    def get_grp(self, string):
        try:
            return self.dico[string[0:2]]
        except KeyError:
            return "no group"

    def get_ss_grp(self, string):
        try:
            return self.dico[string[0:4]]
        except KeyError:
            return "no group"

    def get_ss_ss_grp(self, string):
        if string[0:6] == "000000":
            return "no group"
        try:
            return self.dico[string[0:6]]
        except KeyError:
            return "no group"  

def construct_dico_foods():
    dico_names = {}
    dico_code_grps = {}
    dico_code_ss_grps = {}

    with open("data_aliment/alim_2020_07_07.xml") as file:
        c = -3
        key = None
        for line in file.readlines():
            c += 1
            if c >= 0:
                words = line.split()
                if c%9 == 1:
                    key = words[1]
                elif c%9 == 2:
##                    print(len(words))
##                    key = words[1]
##                    if len(words) >3:
##                        key += words[-3]+words[-2]
                    value = ""
                    for i in range(1, len(words)-1):
                        value+=words[i]+ " "
                    
                    dico_names[key] = value
                elif c%9 == 6:
                    dico_code_grps[key] = words[1]
                elif c%9 == 7:
                    dico_code_ss_grps[key] = words[1]

    return dico_names, dico_code_grps, dico_code_ss_grps


def construct_foods(reader):
    dico_caracs = construct_dico_caracteristiques()
    dico_food_code, dico_code_grps, dico_code_ss_grps = construct_dico_foods()
    dico_food = {}

    c = 1
    for code in dico_food_code.keys():
        c += 1
        val = dico_food_code[code]
        code_grps = dico_code_grps[code]
        code_ss_grps = dico_code_ss_grps[code]
        n_food = Food(val, dico_caracs, code_grps, code_ss_grps, reader)
        dico_food[code] = n_food

        #if c == 10:
         #   break


    with open("data_aliment/compo_2020_07_07.xml") as file:
        c = -3

        alim_code = None
        cst_code = None
        value = None

        for line in file.readlines():
            c += 1
            if c >= 0:
                words = line.split()
                if c%9 == 1:
                    alim_code = words[1]
                elif c%9 == 2:
                    cst_code = words[1]
                elif c%9 == 3:
                    value = words[1]
                    #print(alim_code, cst_code, value)
                    
                    dico_food[alim_code].add_caracteristique(cst_code, value)

            #if c >= 100:

             #   break

    with open("dico_food.txt", "wb") as file:
        pickle.dump(dico_food, file)

    return dico_food


def levenshteinDistance(s1, s2):
    if len(s1) > len(s2):
        s1, s2 = s2, s1

    distances = range(len(s1) + 1)
    for i2, c2 in enumerate(s2):
        distances_ = [i2+1]
        for i1, c1 in enumerate(s1):
            if c1 == c2:
                distances_.append(distances[i1])
            else:
                distances_.append(1 + min((distances[i1], distances[i1 + 1], distances_[-1])))
        distances = distances_
    return distances[-1]



def lower(str_):
    str_ = str_.lower()
    return str_


def load_dico():
    with open('dico_food.txt', 'rb') as file:
        return pickle.load(file)


def user_choice(search_string, str_liste):
    """ returns best_str """
    type_choix = 2

    if type_choix == 1:
        best = [string for string in str_liste if levenshteinDistance(string, search_string) < 6]
    else:
        best = [string for string in str_liste if lower(search_string) in lower(string)]

    for i in range(len(best)):
        print("{}) {}".format(i, best[i]))

    try:
        idx = int(input())
        if 0<= idx < len(best):
            return best[idx]
        else:
            print("bad input")
            user_choice(search_string, str_liste)
    except:
        print("bad input")
        user_choice(search_string, str_liste)



def user_choice_obj(string, obj_liste):
    str_liste = [objet.name for objet in obj_liste]
    return user_choice(string, str_liste)


def print_format(to_print_list):
    for line in to_print_list:
        line_txt, val = line.split(":")
        m = len(line_txt)//text_formatting_width
        j = len(line_txt)%text_formatting_width
        for n in range(m):
            print(line_txt[n*text_formatting_width:(n+1)*text_formatting_width])
        print(line_txt[(m)*text_formatting_width:]+" "*(text_formatting_width-j)+" : "+val)
            


construct = False
text_formatting_width = 30

def main():
    dico_caracs = construct_dico_caracteristiques()

    reader = CodeGrpReader()

    if construct:
        dico_food = construct_foods(reader)
    else:
        dico_food = load_dico()

    foods = list(dico_food.values())
    names = [food.name for food in foods]

    #nutri_features_names = [val.name for val in list(dico_caracs.values())]

    quitt = False

    while not quitt:
        
        string = input("Entrez le nom d'un aliment ou d'un element de nutrition (n <element>):\n")

        if string == "q":
            quitt = True

        elif string == "cd":
            dico_food = construct_foods()

        elif string[:2] == "n ":
            caracteristique = user_choice_obj(string[2:], list(dico_caracs.values()))

            leaderboard = sorted(foods, key=lambda food:food.get_car_value(caracteristique), reverse=True)

            to_print_list = []

            for food in leaderboard[:30]:
                to_print_list.append(food.str_of_car(caracteristique))

            print_format(to_print_list)

        else:

            name = user_choice(string, names)
            food_choice = foods[names.index(name)]

            food_choice.print_grp()
            food_choice.print_info_essentielle()
            food_choice.print_metaux()
            food_choice.print_vitamines()



main()








