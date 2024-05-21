from typing import List
#import matplotlib.pyplot as plt 
#import networkx as nx 
#G = nx.DiGraph()
#H = nx.DiGraph()


def chemin_valide(n: int, dieux: List[str], m: int, passations: List[str]) -> None:
    """
    :param n: le nombre de dieux
    :param dieux: liste des prénoms et noms des dieux séparés par un espace
    :param m: nombre de passations du message
    :param passations: liste des échanges de message entre les dieux, les noms complets des deux dieux séparés par un espace
    """
    # TODO Si le message n'a pas été passé en respectant le protocole, afficher
    # sur une ligne le message `NON`. Sinon, afficher `OUI` sur une ligne,
    # puis, en affichant un nom par ligne, le nom de tous les dieux ayant pu
    # être dieu initial.

    arretes = [[0 for i in range(n)] for j in range(n)]
    sous_grph = [[0 for i in range(n)] for j in range(n)]

    sommets = [i for i in range(n)]

    dico_sommets = {}
    c = 0

    for dieu in dieux:
        prenom, nom = dieu.split()
        dico_sommets[(prenom, nom)] = c
        v = 0
        for dieu2 in dieux:
            if dieu2 != dieu:
                prenom2, nom2 = dieu2.split()
                if prenom == prenom2 or nom == nom2:
                    arretes[c][v] = 1
                    arretes[v][c] = 1
                    #G.add_edge(c, v)
            v += 1
        c += 1

    for duo in passations:
        pre1, nom1, pre2, nom2 =  duo.split()
        i, j = dico_sommets[(pre1, nom1)], dico_sommets[(pre2, nom2)]
        sous_grph[i][j] = 1
        sous_grph[j][i] = 1
        #H.add_edge(i, j)
    #nx.draw( G )
    #nx.draw( H )
    #plt.show()

    def is_arbre(sommets, arretes, indice_else=None, ask_connex=False):
        # faire parcours, voir si on retombe sur sommet deja visite
        indice = 0
        visited = []
        if indice_else != None:
            if indice_else == 0:
                indice = 1
        pile = [sommets[indice]]
        ancetre = [None]

        def voisins_except_ancetre(sommet, ancetre):
            return [i for i in range(n) if arretes[sommet][i] and i != ancetre]

        while pile != []:
            n_sommet = pile.pop()
            visited.append(n_sommet)
            voisins = voisins_except_ancetre(n_sommet, ancetre.pop())

            for vois in voisins:
                if vois in visited:
                    return False
                pile.append(vois)
                ancetre.append(n_sommet)

        if ask_connex:
            if len(visited) == len(sommets):
                return True
        return True

    def is_arbre_except_sommet(sommets, arretes, except_sommet, transmissions):
        arretes_cop = [x.copy() for x in arretes]  # arretes.copy()
        for j in range(n):
            if transmissions[except_sommet][j] == 0:
                arretes_cop[except_sommet][j] = 0
                arretes_cop[j][except_sommet] = 0
        return is_arbre(sommets, arretes_cop, indice_else=except_sommet)

    def is_arbre_connexe(sommets, arretes):
        return is_arbre(sommets, arretes, ask_connex=True)
    def parcours_par_transmission_disjoint(transmissions, n, sommet_initial, arretes):
        unvisited_vertices = list(range(n))
        pile = [sommet_initial]
        ancetre = [None]

        def voisins_except_ancetre_arr(sommet, ancetre):
            return [i for i in range(n) if arretes[sommet][i] and i != ancetre]


        def voisins_except_ancetre_trans(sommet, ancetre):
            return [i for i in range(n) if transmissions[sommet][i] and i != ancetre]

        while pile != []:
            n_sommet = pile.pop()
            visited.append(n_sommet)
            voisins = voisins_except_ancetre(n_sommet, ancetre.pop())

            for vois in voisins_trans:
                if vois in visited:
                    return False
                pile.append(vois)
                ancetre.append(n_sommet)

    found = False
    if is_arbre_connexe(sommets, sous_grph):
        for som in sommets:
            if is_arbre_except_sommet(sommets, arretes, som, sous_grph):
                if not found:
                    print("OUI")
                print(dieux[som])
                found = True

    if not found:
        print("NON")


if __name__ == "__main__":
    n = int(input())
    dieux = [input() for _ in range(n)]  # sommets du grph  # arretes
    m = int(input())
    passations = [input() for _ in range(m)]  # arretes du sous grph
    chemin_valide(n, dieux, m, passations)
