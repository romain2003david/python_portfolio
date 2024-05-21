def rl(liste):

    return range(len(liste))


import math


from pig_tv import *

class Graphe:

    def __init__(self, mat_adj=None, distances=None, liste_vois=None):


        if mat_adj == None:

            pass

##            self.liste_vois = liste_vois  # liste_vois[i] contains all his neighbors, a neighbor being a distance and a point : (dist, pt)
##
##            self.mat_adj = [[0 for j in range(self.nb_pt)] for i in range(self.nb_pt)]
##
##            for i in range(self.nb_pt):
##
##                for couple_vois in self.liste_vois[i]:
##
##                    dist, pt = couple_vois  # dist =! 0
##
##                    self.mat_adj[i][pt] = dist

        else:

            self.nb_pt = len(mat_adj)

            self.mat_adj = mat_adj

            self.distances = {}

            for i in range(self.nb_pt):

                for j in range(self.nb_pt):

                    self.distances[(i, j)] = self.mat_adj[i][j]

            self.arretes = [arrete for arrete in self.distances.keys() if not self.distances[arrete] == 0]

            self.liste_vois = [[j for j in range(self.nb_pt) if self.mat_adj[i][j] != 0] for i in range(self.nb_pt)]

        self.current_curseur_topologique = 0

        self.tri_topo = [-1 for k in range(self.nb_pt)]

    def get_neighbors(self, i):

        return self.liste_vois[i]

    def parcours_profondeur(self, pt, liste_visites=[], tri_topo=False):

        liste_visites.append(pt)

        if tri_topo:

            self.tri_topo[pt] = self.current_curseur_topologique

            self.current_curseur_topologique += 1

        for voisin in Graphe.get_neighbors(self, pt):

            if not voisin in liste_visites:

                Graphe.parcours_profondeur(self, voisin, liste_visites, tri_topo)

        return liste_visites

    def parcours_largeur(self, pt):

        liste_visites = []

        file = [pt]

        while file != []:

            n_pt = file[0]

            del file[0]

            liste_visites.append(n_pt)

            for voisin in Graphe.get_neighbors(self, n_pt):

                if not (voisin in file or voisin in liste_visites):

                    file.append(voisin)

        return liste_visites

    def arbre_couvrant_kruskal(self):
        """ pour les GNO (graphe non oriente)connexe, selectionne des arretes (n-1) tq elle forme un arbre couvrant du graphe et que la somme de leur poids est minimale """

        arretes_dist = [(self.distances[arrete], arrete) for arrete in self.arretes]

        arretes_dist.sort()

        composantes_connexes = [i for i in range(self.nb_pt)]

        arretes_choisies = []

        while len(arretes_choisies) <= self.nb_pt-2:

            min_dist, min_arrete = arretes_dist[0]

            pt1, pt2 = min_arrete

            del arretes_dist[0]

            if composantes_connexes[pt1] != composantes_connexes[pt2]:  # ne sont pas dans la meme composante connexe

                arretes_choisies.append(min_arrete)

                for x in rl(composantes_connexes):

                    if composantes_connexes[x] == composantes_connexes[pt1]:

                        composantes_connexes[x] = composantes_connexes[pt2]

        return arretes_choisies

    def dijkstra(self, pt):
        """ plus courts chemins dans un graphe a ponderation positive en partant d'un pt"""

        distances  = [math.inf for x in range(self.nb_pt)]

        predecesseurs = [None for x in range(self.nb_pt)]

        visited = [False for x in range(self.nb_pt)]

        predecesseurs[pt] = pt

        distances[pt] = 0

        for x in range(self.nb_pt-1):  # on officialise les distances 1 par 1

            # estime les distances

            min_dist = math.inf

            chosen = None

            for k in range(self.nb_pt):

                if not visited[k] and distances[k] < min_dist:

                    chosen = k

                    min_dist = distances[k]

            visited[chosen] = True

            for vois in Graphe.get_neighbors(self, chosen):

                if distances[chosen] + self.distances[(chosen, vois)] < distances[vois]:

                    distances[vois] = distances[chosen] + self.distances[(chosen, vois)]

                    predecesseurs[vois] = chosen

        return distances, predecesseurs

    def bellman_ford(self, origine):
        """ retourn plus courtes distances en partant d'un pt ds un graphe sans cycles absorbants (somme de poids negatifs) """

        distances = [math.inf for x in range(self.nb_pt)]

        predecesseurs = [None for x in range(self.nb_pt)]

        distances[origine] = 0

        predecesseurs[origine] = origine

        for k in range(self.nb_pt):

            for arrete in self.arretes:

                start, end = arrete

                if distances[start]+self.distances[arrete] < distances[end]:

                    distances[end] = distances[start]+self.distances[arrete]

                    predecesseurs[end] = start

        return distances, predecesseurs

    def warshall_floyd(self):
        """ trouver les plus courts chemins entre tout couples de points """

        distances = self.mat_adj.copy()  # distances matrix contains the distances to go from each point to each point : distances[i][j] is the distance to go from j to i

        predecesseurs = [[None for j in range(self.nb_pt)] for i in range(self.nb_pt)]

        for i in range(self.nb_pt):

            for j in range(self.nb_pt):

                if distances[i][j] < math.inf:

                    predecesseurs[i][j] = j  # predecessor of j, to go from j to i

        replace_liste(distances, 0, math.inf)

        for intermediaire in range(self.nb_pt):  # at each loop allows the paths to travel through one more point of the graph

            for start in range(self.nb_pt):

                for end in range(self.nb_pt):

                    if distances[start][intermediaire]+distances[intermediaire][end] < distances[start][end]:

                        distances[start][end] = distances[start][intermediaire]+distances[intermediaire][end]

                        predecesseurs[start][end] = intermediaire

        return distances, predecesseurs

    def get_comp_cnx(self):
        """ retourne les composantes connexes d'un GNO """

        comp_cnx = []

        for i in range(self.nb_pt):

            print(comp_cnx, i)

            if not in_deep(comp_cnx, i):

                comp_cnx.append(Graphe.parcours_largeur(self, i))

        return comp_cnx

    def set_tri_topo(self, racine=0):

        self.tri_topo = [-1 for k in range(self.nb_pt)]

        self.current_curseur_topologique = 0

        liste_visite = Graphe.parcours_profondeur(self, racine, [], True)

        while -1 in self.tri_topo:

            indx = self.tri_topo.index(-1)

            liste_visite2 = Graphe.parcours_profondeur(self, indx, liste_visite, True)

            liste_visite.extend(liste_visite2)

    def get_comp_frtm_cnx(self):
        """ retourne les composantes fortement connexes d'un GO """

        comp_frtmt_cnx = []

        Graphe.set_tri_topo(self)

        mat_inv = [[self.mat_adj[j][i] for j in range(self.nb_pt)]for i in range(self.nb_pt)]

        grph_inverse = Graphe(mat_inv)

        for n in range(self.nb_pt-1, -1, -1):

            pt = self.tri_topo.index(n)

            if not in_deep(comp_frtmt_cnx, pt):

                comp = grph_inverse.parcours_profondeur(pt)

                comp_frtmt_cnx.append(comp)

        return comp_frtmt_cnx


## tests

mat_adj = [[0, 1, 1, 0], [0, 0, 0, 1], [0, 0, 0, 0], [0, 0, 0, 0]]

grph = Graphe(mat_adj)

print(grph.get_neighbors(0))

print(grph.get_neighbors(1))

print(grph.parcours_profondeur(0))

print(grph.parcours_largeur(0))

grph.set_tri_topo(1)

print("t", grph.tri_topo)

grph.set_tri_topo(0)

print(grph.tri_topo)

# kruskal

mat_adj2 = [[0, 1, 0, 1.5], [1, 0, 2, 3], [0, 2, 0, 2], [1.5, 3, 2, 0]]

grph2 = Graphe(mat_adj2)

print(grph2.arbre_couvrant_kruskal())

##img = pygame.image.load('pictures/alz.png')
##
##frame = img.get_rect()
##print(frame[2]*frame[3])
##math_adj_img = [[0 for x in range(frame[2]*frame[3])] for y in range(frame[2]*frame[3])]
##
##for x in range(frame[2]):
##
##    for y in range(frame[3]):
##
##        pt = img.get_at((x, y))
##
##        index = x+y*frame[2]
##
##        neighbors = []
##
##        for i in range(-1, 2):
##
##            for j in range(-1, 2):
##
##                if not((i+x) < 0 or (i+x >= frame[2]) or (j+y) < 0 or (j+y >= frame[3]) or (i, j) == (0, 0) or abs(i)+abs(j) > 1):
##
##                    neighbors.append((x+i, y+j))
##
##        for (w, z) in neighbors:
##
##            index2 = w+z*frame[2]
##
##            pt2 = img.get_at((w, z))
##
##            dist = get_distance(pt1, pt2)
##
##            math_adj_img[index1][index2] = dist
##
##print(math_adj_img[:10][:10])
##
##grph_img = Graphe(math_adj_img)
##
##arretes = grph_img.arbre_couvrant_kruskal()
##
##n_grph

# dijkstra

mat_adj3 = [[0, 1, 3], [1, 0, 1], [0, 0, 0]]

grph3 = Graphe(mat_adj3)

print("plus courtes dist", grph3.dijkstra(0))

mat_adj4 = [[0, 1, 5, 5], [0, 0, 1, 0], [0, 0, 0, 1], [0, 0, 0, 0]]

grph4 = Graphe(mat_adj4)

print("plus courtes dist", grph4.dijkstra(0))

# bellman ford

mat_adj5 = [[0, 3, 3], [0, 0, -1], [0, 0, 0]]

grph5 = Graphe(mat_adj5)

print("plus courtes dist", grph5.bellman_ford(0))

# warshall floyd

mat_adj6 = [[0, 1, 5], [0, 0, 2], [3, 0, 0]]

grph6 = Graphe(mat_adj6)

print("toutes plus courtes dist", grph6.warshall_floyd())

# composantes connexes GNO

mat_adj7 = [[0, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 0]]

grph7 = Graphe(mat_adj7)

print("composantes connexes", grph7.get_comp_cnx())


# composantes fortement connexes GO


mat_adj8 = [[0, 1, 1, 0], [0, 0, 1, 0], [0, 1, 0, 1], [0, 0, 0, 0]]

grph8 = Graphe(mat_adj8)

print("composantes fortement connexes", grph8.get_comp_frtm_cnx())

















