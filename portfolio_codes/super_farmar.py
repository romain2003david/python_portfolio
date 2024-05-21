from pig_tv import *

import matplotlib.pyplot as plt


class Joueur:

    costs = Arr([1, 6, 12, 36, 72, 6, 36])

    kostky_seed = [('ovce', 'kralik'), ('vlk', 'ovce'), ('prase', 'kralik'), ('krava', 'ovce'), ('ovce', 'kralik'), ('krava', 'kralik'), ('kralik', 'prase'), ('ovce', 'ovce'), ('kralik', 'kralik'), ('ovce', 'ovce'), ('kralik', 'kralik'), ('ovce', 'kralik'), ('kralik', 'prase'), ('ovce', 'liska'), ('ovce', 'prase'), ('kralik', 'kralik'), ('krava', 'kralik'), ('kralik', 'kun'), ('kralik', 'kralik'), ('ovce', 'kralik'), ('ovce', 'kralik'), ('kralik', 'kralik'), ('kralik', 'kralik'), ('ovce', 'prase'), ('kralik', 'kun'), ('kralik', 'ovce'), ('kralik', 'ovce'), ('prase', 'prase'), ('kralik', 'prase'), ('kralik', 'kun'), ('ovce', 'kun'), ('prase', 'kralik'), ('kralik', 'kun'), ('prase', 'kralik'), ('kralik', 'liska'), ('prase', 'kun'), ('kralik', 'kralik'), ('kralik', 'liska'), ('ovce', 'kralik'), ('ovce', 'ovce'), ('kralik', 'kralik'), ('kralik', 'kralik'), ('ovce', 'kralik'), ('ovce', 'prase'), ('ovce', 'kralik'), ('krava', 'kralik'), ('ovce', 'kralik'), ('kralik', 'kralik'), ('prase', 'kralik'), ('prase', 'kralik'), ('vlk', 'kralik'), ('ovce', 'kralik'), ('kralik', 'liska'), ('prase', 'prase'), ('kralik', 'kralik'), ('kralik', 'liska'), ('krava', 'kralik'), ('ovce', 'kralik'), ('krava', 'prase'), ('vlk', 'ovce')]

    def __init__(self, borne, comportements, borne2=40):

        self.kralik = 0

        self.ovce = 0

        self.prase = 0

        self.krava = 0

        self.kun = 0

        self.maly_pes = 0

        self.velky_pes = 0

        self.zvirata = Arr([self.kralik, self.ovce, self.prase, self.krava, self.kun, self.maly_pes, self.velky_pes])

        self.victoire = sum(self.costs) - 6 - 36

        self.zvirata_names = ["kralik", "ovce", "prase", "krava", "kun"]

        self.zvirata_names_extended = self.zvirata_names+["maly pes", "velky pes"]

        self.colors = ["brown", "yellow", "pink", "orange", "red", "blue", "grey"]

        self.kolo = 0

        self.stavy = [self.zvirata]

        self.palier_maly_pes = borne

        self.palier_velky_pes = borne2

        self.comportements = comportements

    def update_zvirata(self, add_list):

        self.zvirata += add_list

        # updating animal tags

        self.kralik = self.zvirata[0]

        self.ovce = self.zvirata[1]

        self.prase = self.zvirata[2]

        self.krava = self.zvirata[3]

        self.kun = self.zvirata[4]

        self.maly_pes = self.zvirata[5]

        self.velky_pes = self.zvirata[6]

    def replace_zvirata(self, replace_list):

        self.zvirata = replace_list

        # updating animal tags

        self.kralik = self.zvirata[0]

        self.ovce = self.zvirata[1]

        self.prase = self.zvirata[2]

        self.krava = self.zvirata[3]

        self.kun = self.zvirata[4]

        self.maly_pes = self.zvirata[5]

        self.velky_pes = self.zvirata[6]

    def get_zvirata_nb(self):
        """ returns nb of animals with kralik unit """

        return Joueur.get_zvirata_nb_liste(self.zvirata)

    def get_zvirata_nb_liste(liste_zvirata):

        return sum(liste_zvirata*Joueur.costs)

    def print_stav(self):

        for x in rl(self.zvirata_names_extended):

            print("{} : {}".format(self.zvirata_names_extended[x], self.zvirata[x]))

    def has_won(self):

        return Joueur.get_zvirata_nb(self) >= self.victoire

    def step(self, kostky=None):

        self.kolo += 1

        if kostky == None:

            kostky = get_kostky()  #  Joueur.kostky_seed[self.kolo-1]  # 

        #print("kolo {} : {}".format(self.kolo, kostky))

        if "vlk" in kostky:

            if self.velky_pes >= 1:

                self.velky_pes -= 1

                self.zvirata[-1] -= 1

            else:

                Joueur.replace_zvirata(self, Arr([0, 0, 0, 0, self.kun, self.maly_pes, 0]))

        if "liska" in kostky:

            if self.maly_pes >= 1:

                self.maly_pes -= 1

                self.zvirata[-2] -= 1

            else:

                self.kralik = 0

                self.zvirata[0] = 0

        c = -1

        for string in self.zvirata_names:

            c += 1

            liste_add_zvirata = Arr.get_nul([7])

            if string in kostky:

                if kostky == (string, string):

                    bonus = 2

                else:

                    bonus = 1

                liste_add_zvirata[c] += (self.zvirata[c]+bonus) // 2

                Joueur.update_zvirata(self, liste_add_zvirata)

        return kostky

    def draw_stavy(self):

        xs = [x+1 for x in rl(self.stavy)]

        for y in rl(self.zvirata_names_extended):

            string = self.zvirata_names_extended[y]

            ys = [self.stavy[i][y] for i in rl(self.stavy)]

            plt.plot(xs, ys, linestyle=':', marker="o", label=string, color=self.colors[y])

        plt.legend()

        plt.show()

##        plt.clf()
##
##        xs = [x+1 for x in rl(self.stavy)]
##
##        ys = [Joueur.get_zvirata_nb_liste(self.stavy[i]) for i in rl(self.stavy)]
##
##        plt.plot(xs, ys, linestyle=':', marker="o")
##
##        plt.show()

    def romain_deal(self):

        # Current wealth

        money = Joueur.get_zvirata_nb(self)

        new_zvirata_list = Arr.get_nul([7])

        # Chosing dogs

        palier_maly_pes = 7

        palier_maly_pes_2 = 25

        palier_maly_pes_3 = 39

        palier_velky_pes = 67

        if money >= palier_velky_pes:

            new_zvirata_list[-2:] = [1, 1]

            money -= self.costs[-1]+self.costs[-2]

        elif money >= palier_maly_pes_3:

            new_zvirata_list[-2] = 3

            money -= self.costs[-2]*3

        elif money >= palier_maly_pes_2:

            new_zvirata_list[-2] = 2

            money -= self.costs[-2]*2

        elif money >= palier_maly_pes:

            new_zvirata_list[-2] = 1

            money -= self.costs[-2]

        # Managing other animals

##        all_repartitions = get_repartitions(money, [1, 6, 12])
##
##        best_repartitions = None
##
##        max_ = 0
##
##        for k_v_p in all_repartitions:
##
##            if esperance(k_v_p) > max_:
##
##                best_repartitions = k_v_p

        if money < 20:

            best_repartitions = [money, 0, 0]

        else:

            nb_mouton = (money-12)//6

            best_repartitions = [money-nb_mouton*6, nb_mouton, 0]

        new_zvirata_list[:3] = best_repartitions

        #print(best_repartitions)

        Joueur.replace_zvirata(self, new_zvirata_list)

        self.stavy.append(self.zvirata)

    def deal(self):
        """

        comportements:
        0 : rien
        1 : a partir de x lapins achete un petit chien (bornes optimales : 7, 10, 13)
        2 : exchanger : transforme tout en un type d'animal
        3 : a partir de x argent achete un grand chien

        """

        if 2 in self.comportements:

            Joueur.exchange_all_into(self, 1)

        if 1 in self.comportements:

            if (self.kralik >= self.palier_maly_pes) and self.maly_pes == 0:

                self.maly_pes = 1

                self.kralik -= 6

                self.zvirata[0] -= 6

                self.zvirata[5] += 1

        #Joueur.print_stav(self)

        if 3 in self.comportements:

            if self.velky_pes == 0 and Joueur.get_zvirata_nb(self) > self.palier_velky_pes:

                Joueur.buy_velky_pes(self)

        #Joueur.print_stav(self)

        self.stavy.append(self.zvirata)

    def exchange_all_into(self, type_animal):

        cost = self.costs[type_animal]

        for x in range(len(self.zvirata)-2):

            if x != type_animal:

                update_list = Arr.get_nul([7])

                nb = self.costs[x]*self.zvirata[x] // cost

                vendus = nb*cost//self.costs[x]

                update_list[type_animal] = nb

                update_list[x] = -vendus

                Joueur.update_zvirata(self, update_list)

    def buy_velky_pes(self, priorite_list=[4, 3, 2, 1, 0, 5]):

        self.velky_pes = 1

        self.zvirata[6] += 1

        cost = self.costs[6]

        indi = -1

        update_zvirata_list = Arr.get_nul([7])

        while cost > 0:

            indi += 1

            zvire_indx = priorite_list[indi]

            if self.costs[zvire_indx]*self.zvirata[zvire_indx] >= cost:  # there is enough of this type of animals to pay for the velky pes

                if cost//self.costs[zvire_indx] == self.zvirata[zvire_indx]:

                    enough_zvire_nb =  cost//self.costs[zvire_indx]

                else:

                    enough_zvire_nb = cost//self.costs[zvire_indx] + 1

                update_zvirata_list[zvire_indx] -= enough_zvire_nb

                update_zvirata_list[0] += self.costs[zvire_indx]*enough_zvire_nb - cost  # dostava zpet kraliky

                cost = 0

            else:

                 max_zvire_nb = self.zvirata[zvire_indx]

                 update_zvirata_list[zvire_indx] -= max_zvire_nb

                 cost -= self.costs[zvire_indx]*max_zvire_nb

        Joueur.update_zvirata(self, update_zvirata_list)


def get_kostky():

    zluta_kostka = ["kralik" for x in range(6)]+["vlk"]+["krava"]+["prase"]+["ovce" for x in range(3)]

    cervena_kostka = ["kralik" for x in range(6)]+["liska"]+["kun"]+["prase" for x in range(2)]+["ovce" for x in range(2)]

    return random.choice(zluta_kostka), random.choice(cervena_kostka)


def get_all_kostky():

    zluta_kostka = ["kralik" for x in range(6)]+["vlk"]+["krava"]+["prase"]+["ovce" for x in range(3)]

    cervena_kostka = ["kralik" for x in range(6)]+["liska"]+["kun"]+["prase" for x in range(2)]+["ovce" for x in range(2)]

    all_pos = []

    for x in zluta_kostka:

        for y in cervena_kostka:

            all_pos.append((x, y))

    return all_pos


#print(get_all_kostky(), len(get_all_kostky()))
##
##s = 0
##for x in get_all_kostky():
##
##    if 'prase' in x:
##
##        s += 1
##
##print(s)


def esperance(K_V_P):

    update_liste = Arr.get_nul([7])

    update_liste[0:3] = K_V_P

    #update_liste[-2:] = [1, 1]

    #kralik_nb, ovce_nb, prase_nb = K_V_P

    j = Joueur(0, [], 0)

    j.update_zvirata(update_liste)

    valeur = j.get_zvirata_nb()

    all_kostky = get_all_kostky()

    somme = 0

    for hod in all_kostky:

        j = Joueur(0, [], 0)

        j.update_zvirata(update_liste)

        j.step(hod)

##        replace_list = j.zvirata
##
##        replace_list[-2:] = [1, 1]
##
##        j.replace_zvirata(replace_list)

        valeur2 = j.get_zvirata_nb()

        surplus = valeur2-valeur

        somme += surplus

    return somme/len(all_kostky)

def get_repartitions(n, ponderations):
    """ returns all (a_1, a_2, ..., a_N) positive integers so that a_1*x_1 + a_2*x_2 + ... + a_N*x_N = n , where ponderations = [x_1, ..., x_N] """

    if len(ponderations) == 1:

        if n % ponderations[0] == 0:

            return [[n // ponderations[0]]]

        else:

            return [[]]

    else:

        possible_a1 = [a for a in range(n//ponderations[0]+1)]

        all_pos = []

        for a1 in possible_a1:

            for liste in get_repartitions(n-a1*ponderations[0], ponderations[1:]):

                if liste != []:

                    all_pos.append([a1]+liste)

        return all_pos


def possibilites(n):

    all_repartitions = get_repartitions(n, [1, 6, 12])

    for k_v_p in all_repartitions:

        print(k_v_p, esperance(k_v_p))


#possibilites(24)


def main():

    j = Joueur(7, [2, 3])

    while not j.has_won():

        j.step()

        j.romain_deal()

    j.draw_stavy()
    
    xs = [x for x in range(36, 60)]

    ys1 = []

    ys2 = []

    for borne in xs:

        kola1 = []

        kola2 = []

        for x in range(1000):

            j1 = Joueur(borne, [1])

            j2 = Joueur(7, [2, 3], borne)

##            kostky = []
##
##            for x in range(60):
##
##                kostky.append(j1.step())
##
##                j1.deal()
##
##            print(kostky)

            while not j2.has_won():

                j2.step()

                j2.romain_deal()

            #j1.draw_stavy()

            #j2.draw_stavy()

            kola1.append(j1.kolo)

            kola2.append(j2.kolo)

            #print(j.kolo)

        ys1.append(get_average(kola1))

        ys2.append(get_average(kola2))

        print(get_average(kola2))

        #print("palier : {}, score : {}".format(borne, ys[-1]))

    #plt.plot(xs, ys1)

    plt.plot(xs, ys2)

    plt.show()


main()




"""
full kralik exchanging : 61

full kralik exchanging + maly pes: 36

full ovce exchanging : 58

full prase exchanging : 83

full krava exchanging : 83

full kun exchanging : 50

full kralik exchanging + velky pes : 47

full ovce exchanging + velky pes : 41

full prase exchanging + velky pes : 47

full krava exchanging + velky pes : 45

full kun exchanging + velky pes : 43


Romix:

1 kr = 1 kralik unit (1 ovce = 6 kr...)

money >= 7 kr:

    maly pes

money >= x kr:




romix

chiens a paliers:
strategie calcul brut : 36.87 (100 essais)
full lapins : 34.7247
quelques moutons : 34.608
plus de moutons : 39.163
"""










