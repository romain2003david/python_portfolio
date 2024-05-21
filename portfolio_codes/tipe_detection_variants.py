# imports

import random

from pig_tv import *

import matplotlib.pyplot as plt

import numpy as np

from mpl_toolkits import mplot3d

from matplotlib import cm

### Classification hiérarchique: l. 49
### Neighbor Joining: l. 610
### Inertie : l. 1270
### Elements graphiques : l. 1462
### Tests : l. 1758
### Tests base de donnee Covid : l. 2727

def get_random_dendrogramme(nb_feuille):
    """ returns a random binary tree """

    points = [k for k in range(nb_feuille)]

    for k in range(nb_feuille-1):  # n-1 etapes de rassemblage

        # choses the two 'to be merged' pts
        index1 = random.randint(0, len(points)-1)

        index2 = random.randint(0, len(points)-2)

        if index2 == index1:

            index2 += 1

        # merging in the pts list

        points.append([points[index1], points[index2]])

        del points[max(index1, index2)]

        del points[min(index1, index2)]

    return points[0]


### Classification hiérarchique
###

def get_new_dist(dist1, dist2, meth, tailles):
    """ computes new distance depending on methode aggregative ;
        tailles is only used in ward'd method ; it contains size of the first cluster (linked to dist1), the second one and the other one whose distance to we're computing ;
        it also contains distance bewteen the two to_be_merged clusters"""

    if meth == 0:  # average

        return round((dist1+dist2)/2, 1)

    elif meth == 1:  # minimum

        return round(min(dist1, dist2), 1)

    elif meth == 2:  # maximum

        return round(max(dist1, dist2), 1)

    elif meth == 3:  # ward

        taille1, taille2, taille_other, dist_to_be_merged = tailles

        n_dist = ((taille1+taille_other)*dist1 + (taille2+taille_other)*dist2 - taille_other*dist_to_be_merged) / (taille1+taille2+taille_other)

        return round(n_dist, 1)


def merge_distance_matrix_centre(distance_matrix, to_merge_pos, methode_aggregative, liste_tailles):
    """ the lines and columns relative to the to_be_merged elements are deleted, and replaced by a point that's the mean of the distances to the two points """

    k, l = to_merge_pos  # k always smaller than l

    dist_kl = distance_matrix[k][l-k-1]

    n = len(distance_matrix)

    #print(len(distance_matrix), len(liste_tailles))

    # computing the new distances, varying on the aggregative method
    # the new point will be added to the bottom

    for x in range(n):

        if (x != k) and (x != l):

            # a line of the distance matrix only contains the distance if the line is smaller than the column
            if k > x:

                old_dist1 = distance_matrix[x][k-x-1]

            else:

                old_dist1 = distance_matrix[k][x-k-1]

            if l > x:

                old_dist2 = distance_matrix[x][l-x-1]

            else:

                old_dist2 = distance_matrix[l][x-l-1]

            if methode_aggregative == 3:

                tailles = [liste_tailles[k], liste_tailles[l], liste_tailles[x], dist_kl]

            else:

                tailles = None

            new_dist = get_new_dist(old_dist1, old_dist2, methode_aggregative, tailles)

            # all the distances get added in the other lines' columns cause it will be placed last line, so it's line is never smaller than its column ; it's also placed at the end of the column
            distance_matrix[x].append(new_dist)

            # deleted the old distances if they were stored
            if x < l:  # first deleting biggest index

                del distance_matrix[x][l-x-1]

            if x < k:

                del distance_matrix[x][k-x-1]

    # adding a line with the new distances ; it will be the last line of the matrix
    # deleting the lines
    if l < n:

        old_dist1 = distance_matrix[k][n-k-1]

        old_dist2 = distance_matrix[l][n-l-1]

        if methode_aggregative == 3:

                tailles = [liste_tailles[k], liste_tailles[l], liste_tailles[n], dist_kl]

        else:

            tailles = None

        new_dist = get_new_dist(old_dist1, old_dist2, methode_aggregative, tailles)  # round((old_dist1+old_dist2)/2, 1)

        distance_matrix.append([new_dist])

        del distance_matrix[l]

    del distance_matrix[k]

    if methode_aggregative == 3:
        # updates the sizes of the clusters
        liste_tailles.append(liste_tailles[k]+liste_tailles[l])

        del liste_tailles[l]

        del liste_tailles[k]


def hierarchical_clustering(points, distance, nb_clusters=1, methode_aggregative=0):
    """ applies the hierarchical clustering method to a set of points with a distance function (pt1, pt2) -> d (float) """

    n = len(points)

    distance_matrix = [[distance(points[x], points[y]) for x in range(y+1, n)] for y in range(n-1)]  # triangular matrix, because distance(x, y) = distance(y, x)

    return hierarchical_clustering_mat(distance_matrix, nb_clusters, methode_aggregative)


def hierarchical_clustering_mat(distance_matrix, nb_clusters=1, methode_aggregative=0):
    """ applies the hierarchical clustering method to a set of points with a distance matrix M[pt1, pt2] = d (float)
        returns the cluster structure, which stores the links between the points,
        and a dictionnary with the distances between each new created cluster

        methode_aggregative:
        0 for average
        1 for minimum
        2 for maximum
        3 for ward
    """

    n = len(distance_matrix)+1

    liste_significations = [k for k in range(n)]  # repere les clusters

    dictionnaire_distances = {}

    dendrite = []

    if methode_aggregative == 3:

        liste_tailles = [1 for x in range(n)]

    else:

        liste_tailles = []

    for x in range(n-nb_clusters):  # at each step finds the two closest elements/clusters

        # searches minimum in distance matrix

        min_dist = distance_matrix[0][0]

        min_pos = [0, 1]

        for k in range(len(distance_matrix)):

            for j in range(len(distance_matrix[k])):

                if distance_matrix[k][j] < min_dist:

                    min_dist = distance_matrix[k][j]

                    min_pos = [k, k+j+1]

        # merges the two elements in the matrix
        merge_distance_matrix_centre(distance_matrix, min_pos, methode_aggregative, liste_tailles)

        # updates calculated branches lenghts
        n_distance = min_dist/2

        couple1 = (str(liste_significations[min_pos[1]]), str([liste_significations[min_pos[0]], liste_significations[min_pos[1]]]))

        couple2 = (str(liste_significations[min_pos[0]]), str([liste_significations[min_pos[0]], liste_significations[min_pos[1]]]))

        dictionnaire_distances[couple1] = n_distance

        dictionnaire_distances[couple2] = n_distance

        # updates the clusters left
        liste_significations.append([liste_significations[min_pos[0]], liste_significations[min_pos[1]]])

        #print(liste_significations, dictionnaire_distances)
        # see ->
# [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, [5, 7]] {('7', '[5, 7]'): 15.25, ('5', '[5, 7]'): 15.25}
# [0, 1, 2, 3, 4, 6, 8, 9, 10, 11, 12, 13, 14, 15, [5, 7], [6, [5, 7]]] {('7', '[5, 7]'): 15.25, ('5', '[5, 7]'): 15.25, ('[5, 7]', '[6, [5, 7]]'): 23.0, ('6', '[6, [5, 7]]'): 23.0}
        # works well

        del liste_significations[min_pos[1]]

        del liste_significations[min_pos[0]]
        

    return liste_significations[0], dictionnaire_distances


def total_dist_from_dict(dictionnary):

    return sum(dictionnary.values())

class Dendogramme:
    """ structure that implements a dendrogramme, either with distances between clusters or not, and enables to draw it"""

    def __init__(self, dendrogram_list, dictionnaire=None, mots=None, dico_color=None):

        self.dendrogram_list = dendrogram_list

        self.dico_color = dico_color

        self.dictionnaire = dictionnaire

        self.font = 15

        self.width = 1

        self.mots = mots

        self.mot_font = 20

    def draw(self):

        screen.fill(WHITE)

        if self.mots == None:

            Dendogramme.rec_draw(self.dendrogram_list, self.font, self.width, self.dictionnaire, mots=None)

        else:

            Dendogramme.rec_draw(self.dendrogram_list, self.mot_font, self.width, self.dictionnaire, mots=self.mots, x_right_coor=screen_width-50, dico_col=self.dico_color)

        pygame.display.update()

        wait()

    def rec_draw(dendo_list, font=20, f_width=1, dictionnaire=None, x_left_coor=0, x_right_coor=screen_width, y_up_coor=100, y_down_coor=screen_height, mots=None, dico_col=None):
        """ recursively draws the dendogram , starting from the top (the most global cluster) """

        middle_x = (x_left_coor+x_right_coor)/2

        x_length = middle_x-x_left_coor

        y_height = (y_down_coor-y_up_coor)/10

        decal = 0#random.randint(40, 70)

        if len(dendo_list) == 1:

            if mots == None:

                aff_txt(str(dendo_list[0]), middle_x, y_up_coor, taille=font)

            else:

                print(dendo_list)

                aff_txt(mots[dendo_list[0]], middle_x, y_up_coor, GREEN, taille=font)

        else:  # len 2

            low_y = y_up_coor+y_height

            new_left_base = [middle_x-x_length/2, low_y+decal/3]

            new_right_base = [middle_x+x_length/2, low_y+decal]

            pygame.draw.line(screen, BLACK, [middle_x, y_up_coor], new_left_base, f_width)

            pygame.draw.line(screen, BLACK, [middle_x, y_up_coor], new_right_base, f_width)

            if dictionnaire != None:  # there are distances on the branches

                middle_left_branch = get_scaled_vecteur(sum_arrays([middle_x, y_up_coor], new_left_base), 0.5)

                middle_right_branch = get_scaled_vecteur(sum_arrays([middle_x, y_up_coor], new_right_base), 0.5)

                str1 = str(dictionnaire[str(dendo_list[0]), str(dendo_list)])

                str2 = str(dictionnaire[str(dendo_list[1]), str(dendo_list)])

                aff_txt(str1, middle_left_branch[0], middle_left_branch[1], BLUE, taille=font)

                aff_txt(str2, middle_right_branch[0]+10, middle_right_branch[1], RED, taille=font)

            if type(dendo_list[0]) == list:# or type(dendo_list[0]) == tuple:

                Dendogramme.rec_draw(dendo_list[0], font, f_width, dictionnaire, x_left_coor, middle_x, low_y+decal/3, y_down_coor, mots, dico_col=dico_col)

            else:

                if mots == None:

                    aff_txt(str(dendo_list[0]), new_left_base[0]-14, new_left_base[1], taille=font)

                else:

                    if dico_col == None:

                        color = RED

                    else:

                        color = dico_col[mots[dendo_list[0]]]

                    aff_txt(mots[dendo_list[0]], new_left_base[0]-60, new_left_base[1], color, taille=font)

            if type(dendo_list[1]) == list:  # or type(dendo_list[1]) == tuple:

                Dendogramme.rec_draw(dendo_list[1], font, f_width, dictionnaire, middle_x, x_right_coor, low_y+decal, y_down_coor, mots, dico_col=dico_col)

            else:

                if mots == None:

                    aff_txt(str(dendo_list[1]), new_right_base[0], new_right_base[1], taille=font)

                else:

                    if dico_col == None:

                        color = BLUE

                    else:

                        color = dico_col[mots[dendo_list[1]]]

                    aff_txt(mots[dendo_list[1]], new_right_base[0], new_right_base[1], color, taille=font)

                

        

def distance_euclidienne(vect1, vect2):

    x, y = vect1

    z, w = vect2

    return round(sqrt((x-z)**2 + (y-w)**2), 1)


def test_hierarchical_clustering(pts=None, nb_clusters=1):

    # Graphic csts

    radius = 15

    # creating the set of points to cluster

    if pts == None:

        nb_pt = 12

        nb_clusters = 1

        compteur = 0

        type_repartition = 3

        x_len = screen_width/2

        y_len = screen_height/2

        if type_repartition == 1:

            pts = [[random.randint(0, 2*x_len), random.randint(0, 2*y_len)] for v in range(nb_pt)]  # []

            #print(pts)

        elif type_repartition == 2:

            pts = []

            for x in range(2):

                for y in range(2):

                    pts += [[random.randint(x_len*x, (x+1)*x_len-100), random.randint(y_len*y, (y+1)*y_len-100)] for v in range(nb_pt//4)]

        else:

            pts = [[580, 237], [740, 540], [687, 498], [659, 89], [655, 286], [140, 511], [400, 460], [224, 27], [587, 130], [302, 361], [312, 613], [5, 520]]

    # gets the clustering
    dendrite, dictionnaire = hierarchical_clustering(pts, distance_euclidienne, nb_clusters)

    #print(len(dendrite))

    #print(dictionnaire)

    def aff_pts(liste, color):

        nonlocal compteur

        if type(liste) == int:

            pygame.draw.circle(screen, color, pts[liste], radius)

            #pygame.display.update()

            #time.sleep(.01)

            #compteur += 1

        else:

            aff_pts(liste[0], color)

            if len(liste) > 1:

                aff_pts(liste[1:], color)

    def uncluster(dendrogramme):

        clusters = []

        points = []

        if type(dendrogramme[0]) == int:

            points.append(dendrogramme[0])

        else:

            clusters.append(dendrogramme[0])

        if type(dendrogramme[1]) == int:

            points.append(dendrogramme[1])

        else:

            clusters.append(dendrogramme[1])

        return clusters, points

    #print(dendrite)

    screen.fill(WHITE)

    dendro = Dendogramme(dendrite, dictionnaire)

    dendro.draw()

    screen.fill(BLACK)

    for pos in pts:

        pygame.draw.circle(screen, WHITE, pos, radius)

        print(pos)

    pygame.display.update()

    wait()

    clusters = [dendrite]

    points = []

    while clusters != []:

        n_clusters = []

        for clus in clusters:

            n_clus, n_points = uncluster(clus)

            if len(n_clus) == 1:

                n_clusters.append(n_clus[0])

                n_points.append(n_points[0])

            elif len(n_clus) == 2:

                n_clusters.append(n_clus[0])

                n_clusters.append(n_clus[1])

            else:

                n_points.append(n_points[0])

                n_points.append(n_points[1])

        clusters = n_clusters

        for clust in clusters:

            color = get_random_color()

            aff_pts(clust, color)

        for point in points:

            color = get_random_color()

            aff_pts(point, color)

        pygame.display.update()

        #print(compteur)  <---------------------

        wait()


#test_hierarchical_clustering()


def distance_edition(seq1, seq2):
    """ Implementation de l'algorithme de recherche de plus courte distance entre deux mots (distance d'edition), en programmation dynamique ;
        utilise principe de memoïzation, entre les mots plus ou moins construit, et la relation:
        d(mot1+"a", mot2+"b") = min( d(mot1, mot2+"b")+1, d(mot1+"a", mot2)+1, d(mot1, mot2)+(1 sauf si a=b)
        complexité temporelle : O(n*m)
        complexité spatiale : O(n*m)
    """

    # pour comprendre addition, soustraction, on fait comme si on voulait transformer seq2 en seq1 (...)

    n, m = len(seq1), len(seq2)

    tableau = [[0 for x in range(m)] for y in range(n)]

    # cas triviaux (initialisation) pour le mot construit sur les colonnes
    for x in range(m):

        tableau[0][x] = x+1 - int(seq1[0] in seq2[:x+1])

    # cas triviaux (initialisation) pour le mot construit sur les lignes
    for y in range(n):

        tableau[y][0] = y+1 - int(seq2[0] in seq1[:y+1])

    #bouclage sur le tableau

    for y in range(1, n):

        for x in range(1, m):

            echange = tableau[y-1][x-1] + (seq1[y] != seq2[x])  # on doit echanger la derniere lettre si elle est differente

            addition = tableau[y][x-1] + 1  # addition : on regarde la distance minimale pour seq2 un peu plus petite, et ajoute la lettre qu'il faut...

            soustraction = tableau[y-1][x] + 1  # soustraction / suppression : on regarde la distance avec le mot objectifun peu plus court, on enleve pour cela la lettre en trop du mot

            # utilisation du principe de récurrence pour remplir la nouvelle case

            tableau[y][x] = min(echange, addition, soustraction)


### Neighbor Joining
###

def get_dist(dictionaire_distance, nbr1, nbr2):

    if nbr1 == nbr2:

        return 0

    if plus_petit(nbr1, nbr2):

        return dictionaire_distance[(nbr1, nbr2)]

    else:

        return dictionaire_distance[(nbr2, nbr1)]




def plus_petit(nbr1, nbr2):
    """ the etiquettes, so called nbr, are actually often lists """

    dim1, dim2 = dim(nbr1), dim(nbr2)

    if dim1 != dim2:

        return dim1 <= dim2

    if dim1 <= 1:

        return nbr1 < nbr2  # lexicographique ou classique

    len1, len2 = len(nbr1), len(nbr2)

    if len1 != len2:

        return len1 <= len2

    c = 0

    while (nbr1[c] == nbr2[c]) and (c < len1-1):

        c += 1

    if c == len1-1:

        print("erreur, les deux etiquettes sont egales...")
        True

    else:

        return plus_petit(nbr1[c], nbr2[c])


def set_dist(dictionaire_distance, nbr1, nbr2, value):

    if plus_petit(nbr1, nbr2):

        dictionaire_distance[(nbr1, nbr2)] = value

    else:

        dictionaire_distance[(nbr2, nbr1)] = value


def branch_len_associating_ij(dictionaire_distance, current_noeuds, i, j):

    nb_noeuds = len(current_noeuds)

    ci = current_noeuds[i]

    cj = current_noeuds[j]

    s = (nb_noeuds-2)*get_dist(dictionaire_distance, ci, cj)

    #print(dictionaire_distance, current_noeuds)

    for k in range(nb_noeuds):

        ck = current_noeuds[k]

        s -= (get_dist(dictionaire_distance, ci, ck) + get_dist(dictionaire_distance, cj, ck))

    return s


def next_pair(dictionaire_distance, current_noeuds):

    nb_noeuds = len(current_noeuds)

    record = 0  # criterion always negative

    best_couple = [-1, -1]

    for i in range(nb_noeuds):

        for j in range(i+1, nb_noeuds):

            score = branch_len_associating_ij(dictionaire_distance, current_noeuds, i, j)

            #print(score)

            if score <= record:

                record = score

                best_couple = [i, j]

    return best_couple


def new_branch_lengths(dictionaire_distance, current_noeuds, i, j):
    """ Problem : creates weird distances, that can be negative """
    nb_noeuds = len(current_noeuds)

    ci = current_noeuds[i]

    cj = current_noeuds[j]

    len_branch_i = 0.5*get_dist(dictionaire_distance, cj, ci)

    len_branch_j = len_branch_i

    change = 0

    # some kind of weird shit
    for k in range(nb_noeuds):

        ck = current_noeuds[k]

        change += (get_dist(dictionaire_distance, ci, ck) - get_dist(dictionaire_distance, cj, ck))

    len_branch_i += change

    len_branch_j -= change

    return (len_branch_i, len_branch_j)


def update_dictionaire_distance_and_noeuds(dictionaire_distance, current_noeuds, i, j, branche_i, branche_j, n_nbr):
    """ computes the new distance from each old point to the new cluster (except for the involved points i and j) """

    #print(current_noeuds, current_noeuds[j], current_noeuds[i], i, j)

    nb_noeuds = len(current_noeuds)

    ci = current_noeuds[i]

    cj = current_noeuds[j]

    for k in range(nb_noeuds):

        if k != i and k != j:

            ck = current_noeuds[k]

            new_branch_len = 0.5 * (get_dist(dictionaire_distance, ci, ck)-branche_i) + 0.5 * (get_dist(dictionaire_distance, cj, ck)-branche_j)

            set_dist(dictionaire_distance, ck, n_nbr, new_branch_len)

            #print(ck, n_nbr, get_dist(dictionaire_distance, ck, n_nbr))

    set_dist(dictionaire_distance, ci, n_nbr, branche_i)

    set_dist(dictionaire_distance, cj, n_nbr, branche_j)

    current_noeuds.remove(ci)

    current_noeuds.remove(cj)

    current_noeuds.append(n_nbr)


def concatene(n1, n2):

    if n1 > n2:

        n1, n2 = n2, n1

    if n1 == 0:

        power = 1

    else:

        power = int(log10(n1)) + 1

    return n2*10**power+n1


class Tree:

    def __init__(self, distance_matrix, scale_fact=1):

        self.distance_matrix = distance_matrix

        self.central_noeud_pos = screen_center

        self.nb_noeud = len(distance_matrix)

        self.noeud_radius = 5

        self.etiquettes = [k for k in range(self.nb_noeud)]

        self.nb_unassigned = len(self.etiquettes)

        self.angles = [2*pi*i/self.nb_noeud for i in range(self.nb_noeud)]

        self.vectors = [get_normalized_vector_eucli([cos(ang), sin(ang)], norme=1) for ang in self.angles]

        self.associated = {}

        self.change_angle = pi/4

        self.scale_fact = scale_fact

        self.index_lettre = 65

        self.dico_name = {}

    def draw_noeud(self, pos, noeud_name):

        pygame.draw.circle(screen, BLACK, pos, self.noeud_radius)

        aff_txt(noeud_name, pos[0], pos[1], BLACK, taille=22)

    def step(self, i, j, dist_i, dist_j, n_cluster):

        self.nb_unassigned -= 1

        dist_i, dist_j = random.randint(300, 500), random.randint(300, 500)

        self.associated[n_cluster] = [[i, dist_i], [j, dist_j]]

        self.etiquettes.remove(i)

        self.etiquettes.remove(j)

        self.etiquettes.append(n_cluster)

    def draw_associated(self, nom, pos, vector):

        #print(vector)

        if nom in self.associated.keys():

            noeud1, noeud2 = self.associated[nom]

            nom1, dist1 = noeud1

            nom2, dist2 = noeud2

            if type(nom1) == tuple:

                nom_graph1 = self.dico_name[nom1]

            else:

                nom_graph1 = str(nom1)

            if type(nom2) == tuple:

                nom_graph2 = self.dico_name[nom2]

            else:

                nom_graph2 = str(nom2)

            normale = get_scaled_vecteur(get_normale_2D(vector), 1)

            vect1 = add_vectors(vector, normale, 1, 1)

            vect2 = add_vectors(vector, normale, 1, -1)

            #print(dist1, dist2)

            vect1 = get_normalized_vector_eucli(vect1, norme=abs(dist1)*self.scale_fact)

            vect2 = get_normalized_vector_eucli(vect2, norme=abs(dist2)*self.scale_fact)

            pos1 = apply_function_to_array(add_vectors(pos, vect1, 1, 1), int)

            pos2 = apply_function_to_array(add_vectors(pos, vect2, 1, 1), int)

            Tree.draw_noeud(self, pos1, nom_graph1)

            Tree.draw_noeud(self, pos2, nom_graph2)

            pygame.draw.line(screen, BLUE, pos, pos1)

            pygame.draw.line(screen, RED, pos, pos2)

            Tree.draw_associated(self, nom1, pos1, get_normalized_vector_eucli(vect1, norme=1))

            try:

                Tree.draw_associated(self, nom2, pos2, get_normalized_vector_eucli(vect2, norme=1))

            except:

                print(vector, normale, vect2)

    def draw(self):

        screen.fill(WHITE)

        Tree.draw_noeud(self, self.central_noeud_pos, "X")

        # draws the noeuds that we ai'nt sure of yet

        for k in range(self.nb_unassigned):

            pos = apply_function_to_array(add_vectors(self.central_noeud_pos, self.vectors[k], 1, 100), int)

            if type(self.etiquettes[k]) == tuple:

                if not self.etiquettes[k] in self.dico_name.keys():

                    self.dico_name[self.etiquettes[k]] = chr(self.index_lettre)

                    self.index_lettre += 1

                name = self.dico_name[self.etiquettes[k]]

            else:

                name = str(self.etiquettes[k])

            Tree.draw_noeud(self, pos, name)

            Tree.draw_associated(self, self.etiquettes[k], pos, self.vectors[k])

            pygame.draw.line(screen, GREY, self.central_noeud_pos, pos)

        pygame.display.update()

        wait()


def update_dict_affinites(dict_affinites, n1, n2, bound):

    if n1 in dict_affinites.keys():

        dict_affinites[n1].append(bound)

    else:

        dict_affinites[n1] = [bound]

    if n2 in dict_affinites.keys():

        dict_affinites[n2].append(bound)

    else:

        dict_affinites[n2] = [bound]

    if bound in dict_affinites.keys():

        dict_affinites[bound].append(n1)

        dict_affinites[bound].append(n2)

    else:

        dict_affinites[bound] = [n1, n2]


def neighbor_joining(distance_matrix, scale_fact=1, visual=1):
    """ applies the neighbor joining algorithm to a set of point whose mutual distances are stored in a distance matrix, scale fact is just used to draw the unroooted tree """

    nb_noeuds = len(distance_matrix)

    current_noeuds = [k for k in range(nb_noeuds)]  # stores the points (or clusters) that are still to be united into clusters

    dictionaire_distance = {}  # distances between two points, the first one is the smallest index ; (or clusters, a cluster is just the concatenation of the points that belong to it

    dict_affinites = {}  # stores the relatives (three at the most, two sons and a father, when the tree gets rooted) of each points / cluster

    tree = Tree(distance_matrix, scale_fact)

    screen.fill(WHITE)

    if visual:

        tree.draw()

    # initialises the distances that are already known (real distances)
    for i in range(nb_noeuds):

        for j in range(i, nb_noeuds):

            dictionaire_distance[(i, j)] = distance_matrix[i][j]

    # loops that finds next cluster (two points that are to be associated into a cluster, which is more or less the point in the middle) at each step
    for k in range(nb_noeuds-1):

        # points that minimise the criterion
        i, j = next_pair(dictionaire_distance, current_noeuds)

        # finds new distance according to nj algo
        branche_i, branche_j = new_branch_lengths(dictionaire_distance, current_noeuds, i, j)

        ci, cj = current_noeuds[i], current_noeuds[j]

        n_nbr = (ci, cj)  # concatene(ci, cj)

        update_dictionaire_distance_and_noeuds(dictionaire_distance, current_noeuds, i, j, branche_i, branche_j, n_nbr)

        update_dict_affinites(dict_affinites, ci, cj, n_nbr)

        tree.step(ci, cj, branche_i, branche_j, n_nbr)

        if visual:

            tree.draw()

    if visual:

        tree.draw()

    return dictionaire_distance, dict_affinites


def tuple_liste(liste):

    if dim(liste) == 0:

        return liste

    elif dim(liste) == 1:

        return tuple(liste)

    else:

        return tuple([tuple_liste(x) for x in liste])


def tuple_dico(dico):

    for x in dico.keys():

        dico[x] = tuple_liste(dico[x])

def total_dictionaire_distance(dico_dist, dico_affin):

    print(dico_affin)

    tuple_dico(dico_affin)

    print(dico_dist)

    print(dico_affin)

    racine_qqconque = 0  # d'ou on commence le parcours de l'arbre ne modifie pas sa longueur

    seen = [0]

    to_see = list(dico_affin[racine_qqconque])

    total_dist = 0

    print(to_see)

    while to_see != []:

        next_to_see = to_see.pop()

        seen.append(next_to_see)

        vois = dico_affin[next_to_see]

        print(to_see, seen, vois)

        for x in vois:

            if not x in seen:

                to_see.append(x)

                total_dist += get_dist(dico_dist, x, next_to_see)

    return total_dist


def matrix_from_pts(points, distance):

    n = len(points)

    return [[distance(points[x], points[y]) for x in range(n)] for y in range(n)]


def enraciner(dict_affinites, racine, affected_clust=None):
    """ retourne un dendrogramme a partir du dictionnaire qui regroupe les liens de parenté """

    def replace_by_neighbors(dict_affinites, to_replace, ancestor):

        neighbors = dict_affinites[to_replace]

        neighbors_cop = neighbors.copy()

        neighbors_cop.remove(ancestor)

        for indx in range(len(neighbors_cop)):

            nei = neighbors_cop[indx]

            if len(dict_affinites[nei]) > 1:

                neighbors_cop[indx] = replace_by_neighbors(dict_affinites, nei, to_replace)

        if len(neighbors_cop) == 1:

            return neighbors_cop[0]

        return neighbors_cop

    neighbors = dict_affinites[racine]

    to_add = []

    for indx in range(len(neighbors)):

        nei = neighbors[indx]

        second_ngb = dict_affinites[nei]

        for nei2 in second_ngb:

            #print(nei2, to_add)

            if not nei2 == racine:

                if len(dict_affinites[nei2]) == 1:  # c'est une feuille

                    to_add.append(nei2)

                else:  # noeud

                    to_add.append(replace_by_neighbors(dict_affinites, nei2, nei))

    dendrogramme = [racine, to_add]

    if to_add == [to_add[0]]:

        dendrogramme = [racine, to_add[0]]

    return dendrogramme


    
def test_neighbor_joining():

##    mat = [[],
##[36.67 ],
##[38.33, 38.33 ,],
##[39.00, 39.00, 38.67, ],
##[40.33 ,40.33 ,40.00 ,39.67 ],
##[40.33 ,40.33, 40.00 ,39.67 ,37.00 ],
##[40.17 ,40.17 ,39.83 ,39.50 ,38.83, 38.83 ],
##[40.17 ,40.17 ,39.83, 39.50 ,38.83, 38.83, 37.67 ]]
##
##    test_matrix = [[0 for x in range(8)] for x in range(8)]
##
##    for k in range(8):
##
##        for l in range(8):
##
##            if l != k:
##
##                try:
##
##                    test_matrix[k][l] = mat[k][l]
##
##                except:
##
##                    test_matrix[k][l] = mat[l][k]
##
##    print(test_matrix)

    matrix = [[0, 7, 8, 11, 13, 16, 13, 17], [7, 0, 5, 8, 10, 13, 10, 14], [8, 5, 0, 5, 7, 10, 7, 11], [11, 8, 5, 0, 8, 11, 8, 12], [13, 10, 7, 8, 0, 5, 6, 10], [16, 13, 10, 11, 5, 0, 9, 13], [13, 10, 7, 8, 6, 9, 0, 8], [17, 14, 11, 12, 10, 13, 8, 0]]

    matrix2 = [[0, 36.67, 38.33, 39.0, 40.33, 40.33, 40.17, 40.17], [36.67, 0, 38.33, 39.0, 40.33, 40.33, 40.17, 40.17], [38.33, 38.33, 0, 38.67, 40.0, 40.0, 39.83, 39.83], [39.0, 39.0, 38.67, 0, 39.67, 39.67, 39.5, 39.5], [40.33, 40.33, 40.0, 39.67, 0, 37.0, 38.83, 38.83], [40.33, 40.33, 40.0, 39.67, 37.0, 0, 38.83, 38.83], [40.17, 40.17, 39.83, 39.5, 38.83, 38.83, 0, 37.67], [40.17, 40.17, 39.83, 39.5, 38.83, 38.83, 37.67, 0]]

    matrix3 = [[0, 5, 9, 9, 8], [5, 0, 10, 10, 9], [9, 10, 0, 8, 7], [9, 10, 8, 0, 3], [8, 9, 7, 3, 0]]

    dict_dist = neighbor_joining(matrix)

    print(dict_dist)
"""
>>> for x in a :
	print("[", end ="")

	for y in x:
		if y == 0:
			print("0.0 ", end ="|")
		elif y<10:
			print(round(y), end ="   |")
		else:
			print(round(y), end ="  |")
	print("]")

	
[0.0 |7   |8   |11  |13  |16  |13  |17  |]
[7   |0.0 |5   |8   |10  |13  |10  |14  |]
[8   |5   |0.0 |5   |7   |10  |7   |11  |]
[11  |8   |5   |0.0 |8   |11  |8   |12  |]
[13  |10  |7   |8   |0.0 |5   |6   |10  |]
[16  |13  |10  |11  |5   |0.0 |9   |13  |]
[13  |10  |7   |8   |6   |9   |0.0 |8   |]
[17  |14  |11  |12  |10  |13  |8   |0.0 |]
"""

def test_nj_shuffle_resistant():

    def shuffle(liste):

        n = len(liste)

        indices = [x for x in range(n)]

        permutation =  []

        for x in range(n):

            ind = random.choice(indices)

            permutation.append(ind)

            indices.remove(ind)

        return [liste[x] for x in permutation]

    pts = [[random.randint(0, screen_width), random.randint(0, screen_height)] for v in range(5)]#[[10, 203], [14, 158], [165, 237], [143, 531], [184, 417], [120, 548], [601, 43], [560, 159], [502, 21], [634, 478], [421, 428], [621, 415]]

    plan = Plan(pts)

    plan.draw()

    for x in range(100):

        pts = shuffle(pts)
        plan = Plan(pts)

        matrix = matrix_from_pts(pts, get_distance)

        dict_dist, dict_affinites = neighbor_joining(matrix, scale_fact=0.16, visual=0)

        dendrite = enraciner(dict_affinites, 1)

        plan.add_cluster(dendrite)

        plan.draw()


#test_nj_shuffle_resistant()


### Inertie
###

def dim(liste):

    if type(liste) == int or type(liste) == float:

        return 0

    listes = []

    for x in liste:

        if type(x) == list or type(x) == tuple:

            listes.append(x)

    if listes == []:

        return 1

    else:

        return 1 + max([dim(x) for x in listes])


def get_reduced_dim_list(liste):

    n_liste = []

    for x in liste:

        if type(x) == list:

            n_liste.extend(x)

        else:

            n_liste.append(x)

    return n_liste


def taille_cluster(liste):

    if type(liste) == int:

        return 1

    else:

        s = 0

        for x in liste:

            s += taille_cluster(x)

        return s

def get_barycentre(pts):

    g = pts[0]

    for x in pts[1:]:

        g = sum_arrays(g, x)

    return get_scaled_vecteur(g, 1/len(pts))


def inertie_grp_pt(pts, ponderation, distance):

    g = get_barycentre(pts)

    inertie = 0

    for x in pts:

        inertie += distance(g, x)**2

    return inertie/len(pts)


def get_flattened_list(liste):

    if type(liste) == int:

        return liste

    n_liste = []

    for x in liste:

        if type(x) == int:

            n_liste.append(x)

        else:

            n_liste.extend(get_flattened_list(x))

    return n_liste


def get_inertie_dendrogramme(dendr, pts):
    """ retourne l'inertie interclasse du dendogramme"""

    nbr_clust = len(dendr)

    nbr_pt = taille_cluster(dendr)

    inertie_inter_classe = 0

    bary = get_barycentre(pts)

    for x in range(nbr_clust):

        clust = dendr[x]

        nx = taille_cluster(clust)

        if nx == 1:  # le cluster est un point

            bary_x = pts[clust]

        else:

            indexs_in = get_flattened_list(clust)

            pts_in = [pts[x] for x in indexs_in]

            bary_x = get_barycentre(pts_in)

        inertie_inter_classe += nx*get_distance(bary, bary_x)**2

    return inertie_inter_classe/nbr_pt


def get_inertie_dendrogramme2(dendr, pts):
    """ retourne l'inertie intraclasse du dendogramme"""

    nbr_clust = len(dendr)

    nbr_pt = taille_cluster(dendr)

    inertie_intra_classe = 0

    for x in range(nbr_clust):

        clust = dendr[x]

        gain_inertie = 0

        if not type(clust) == int:  # le cluster n'est pas un point (sinon son inertie est nulle)

            indexs_in = get_flattened_list(clust)

            pts_in = [pts[x] for x in indexs_in]

            bary_x = get_barycentre(pts_in)

            for e in pts_in:

                gain_inertie += get_distance(e, bary_x)**2

        inertie_intra_classe += gain_inertie

    return inertie_intra_classe/nbr_pt


def get_inertie_totale_dendrogramme(dendrogramme, pts):

    indexs = get_flattened_list(dendrogramme)

    elements = [pts[idx] for idx in indexs]

    bary = get_barycentre(elements)

    return sum([get_distance(e, bary)**2 for e in elements])/len(elements)


def get_inertie_expliquee(dendrogramme, pts):

    inertie_inter = get_inertie_dendrogramme(dendrogramme, pts)

    inertie_tot = get_inertie_totale_dendrogramme(dendrogramme, pts)

    inertie_intra = get_inertie_dendrogramme2(dendrogramme, pts)

    return inertie_inter/inertie_tot


### Elements graphiques
###

def print_matrix(matrix):

    for x in matrix:

        print("[", end ="")

        for y in x:

            if y == 0:

                print("0.0 ", end ="|")

            elif y < 10:

                print(round(y), end ="   |")

            elif y < 100:

                print(round(y), end ="  |")

            else:

                print(round(y), end =" |")

        print("]")


class Noeud:

    def __init__(self, pos, fils, rad, type_noeud, nom=None):

        self.pos = pos

        self.pere = None

        self.fils = fils

        self.type_noeud = type_noeud  # 0 pour racine, 1 pour noeud, 2 pour feuille

        self.nom = str(nom)

        # draw csts
        self.color = [BLUE, BLUE, BLACK][self.type_noeud]

        if self.type_noeud != 2:

            rad /= 2

        self.radius = int(rad)

        self.thickness = 3

    def set_pere(self, pere):

        self.pere = pere

    def get_pos(self):

        return self.pos

    def get_pere(self):

        return self.pere

    def get_fils(self):

        return self.fils

    def dist_aux_fils(self):

        if self.fils != None:

            #print(distance_euclidienne(self.fils[0].get_pos(), self.pos))

            if type(self.pos) == str:

                return distance_edition(self.fils[0].get_pos(), self.pos)+distance_edition(self.fils[1].get_pos(), self.pos)

            if len(self.pos) == 2:

                return distance_euclidienne(self.fils[0].get_pos(), self.pos)+distance_euclidienne(self.fils[1].get_pos(), self.pos)

            else:

                return get_distance_eucli_rn(self.fils[0].get_pos(), self.pos)+get_distance_eucli_rn(self.fils[1].get_pos(), self.pos)

        else:

            return 0

    def draw(self):

        pygame.draw.circle(screen, self.color, self.pos, self.radius)

##        if self.nom != None:
##
##            aff_txt(screen, self.pos[0], self.pos[1], BLACK)

        if self.fils != None:

            f1, f2 = self.fils

            pygame.draw.line(screen, RED, self.pos, f1.pos, self.thickness)

            pygame.draw.line(screen, RED, self.pos, f2.pos, self.thickness)


def get_intermediates(clust, pts, rad):
    """ fonction to enable to draw a dendrogramme """

    liste_noeuds = []

    #visited = []

    def rec_find_interm(clust, racine=False):

        if type(clust) == list:

            noeud1 = rec_find_interm(clust[0])

            noeud2 = rec_find_interm(clust[1])

            pos1, pos2 = noeud1.pos, noeud2.pos

            pos = sum_arrays(pos1, pos2, 0.5, 0.5)

            if racine:

                noeud_type = 0

            else:

                noeud_type = 1

            n_noeud = Noeud(pos, [noeud1, noeud2], rad, noeud_type)

            liste_noeuds.append(n_noeud)

            noeud1.set_pere(n_noeud)

            noeud2.set_pere(n_noeud)

            apply_function_to_array(pos, int)

            return n_noeud

        else:

            pos = pts[clust]

            if not type(pos) == str:

                apply_function_to_array(pos, int)

            n_noeud = Noeud(pos, None, rad, 2, clust)

            liste_noeuds.append(n_noeud)

            return n_noeud

    rec_find_interm(clust, racine=True)

    return liste_noeuds


class Plan:

    def __init__(self, pts, mots=0):

        # structures

        self.pts = pts  # listes des points significatifs

        self.clusters = []

        self.cluster_visuels = []

        self.den_partiels = []

        self.dend_actif = -1  # cluster that gets drawn

        self.mots = mots

        #self.clusters_parties

        # graphic csts

        self.den_partiel_active = False

        self.color = WHITE

        self.noeud_radius = 15

        self.noeud_color = BLACK

    def draw(self, all_clus=False):

        screen.fill(self.color)

        c = 0

        for pt in self.pts:

            c += 1

            pygame.draw.circle(screen, self.noeud_color, pt, self.noeud_radius)

            # option pour afficher l'index des points
            aff_txt(str(c-1), pt[0]+20, pt[1], BLACK, 24)

        if self.dend_actif != -1:

            if self.den_partiel_active == True:

                for cluster in self.dend_partiels:

                    for noeud in cluster:

                        noeud.draw()

            else:

                for noeud in self.cluster_visuels[self.dend_actif]:

                    noeud.draw()

        if all_clus:

            for x in range(len(self.cluster_visuels)):

                for noeud in self.cluster_visuels[x]:

                    noeud.draw()

        pygame.display.update()

        print("plan drawn")

        wait()

    def add_cluster(self, n_clust, not_complete=False):

        self.clusters.append(n_clust)

        Plan.create_cluster_visuel(self, not_complete)

        self.dend_actif = len(self.clusters)-1

    def create_cluster_visuel(self, not_complete):
        """ creates structure with all intermediate intesections of branches, that are the centre of the created clusters;
            For visualisation, and also to compute total branch length for instance """

        #try:

        clust = self.clusters[-1]

        if not_complete:

            self.den_partiel_active = True

            self.dend_partiels = [get_intermediates(clust[x], self.pts, self.noeud_radius) for x in range(len(clust))]

        else:

            intermediates = get_intermediates(clust, self.pts, self.noeud_radius)

            self.cluster_visuels.append(intermediates)

##        except:
##
##            print("attention", clust, self.pts)

    def len_branches_cluster(self, index):

        total_len = 0

        racine = self.cluster_visuels[index][-1]

        def dist(noeud):

            fils = noeud.get_fils()

            if fils == None:

                return 0

            else:

                return noeud.dist_aux_fils()+dist(fils[0])+dist(fils[1])

        return dist(racine)


### Tests
###

def comparaison_clusterings():

    compteur = 0

    ### defines the set of points that are to be clustered

    nb_pt = 30

    nb_clusters = 1

    repartition_points = 11

    draw_active = 1

    if repartition_points == 0:

        pts = [[random.randint(0, screen_width), random.randint(0, screen_height)] for v in range(nb_pt)]

        print("generated pts", pts)

    elif repartition_points == 1:

        x_len = screen_width/2

        y_len = screen_height/2

        pts = []  #[[random.randint(0, 2*x_len), random.randint(0, 2*y_len)] for v in range(nb_pt)]  # []

        for x in range(2):

            for y in range(2):

                pts += [[random.randint(x_len*x, (x+1)*x_len-100), random.randint(y_len*y, (y+1)*y_len-100)] for v in range(nb_pt//4)]

        for x in range(nb_pt-(nb_pt//4)*4):

                pts.append([random.randint(0, screen_width), random.randint(0, screen_height)])

        print("generated pts", pts)

    elif repartition_points == 2:

        nb_pt = 16

        pts = [[295, 143], [113, 115], [252, 125], [49, 149], [159, 491], [21, 463], [217, 444], [3, 520], [684, 184], [683, 198], [565, 9], [566, 87], [543, 593], [428, 538], [615, 415], [681, 461]]

    elif repartition_points == 3:

        nb_pt = 16

        pts = [[223, 17], [147, 11], [202, 186], [40, 134], [200, 406], [235, 510], [135, 372], [51, 357], [426, 242], [579, 31], [603, 45], [457, 6], [483, 588], [480, 519], [569, 585], [649, 473]]

    elif repartition_points == 4:

        nb_pt = 6

        pts = [[0, 0], [100, 0], [0, 100], [200, 200], [200, 300], [200, 350]]

    elif repartition_points == 5:

        nb_pt = 20

        pts = [[181, 37], [125, 30], [276, 247], [118, 195], [170, 115], [116, 429], [137, 560], [275, 519], [53, 499], [35, 535], [572, 229], [460, 172], [535, 214], [431, 216], [579, 142], [512, 393], [458, 386], [609, 402], [507, 593], [489, 490]]

    elif repartition_points == 6:

        nb_pt = 12

        pts = [[10, 203], [14, 158], [165, 237], [143, 531], [184, 417], [120, 548], [601, 43], [560, 159], [502, 21], [634, 478], [421, 428], [621, 415]]

    elif repartition_points == 7:

        nb_pt = 3

        pts = [[264, 643], [764, 392], [468, 538]]

    elif repartition_points == 8:

        nb_pt = 9

        pts = [[408, 131], [610, 657], [600, 330], [103, 219], [444, 259], [542, 180], [699, 137], [222, 665], [340, 287]]

    elif repartition_points == 9:

        nb_pt = 5

        pts = [[82, 36], [171, 449], [411, 46], [572, 387], [368, 55]]

    elif repartition_points == 10:

        nb_pt = 12

        pts = [[14, 158], [601, 43], [143, 531], [184, 417], [165, 237], [120, 548], [560, 159], [10, 203], [621, 415], [502, 21], [634, 478], [421, 428]]

    elif repartition_points == 11:

        nb_pt = 5

        pts = [[0, 100], [100, 0], [411, 400], [500, 500], [510, 510]]

    matrix = matrix_from_pts(pts, get_distance)

    print_matrix(matrix)

    ### graphical structure

    plan = Plan(pts)

    plan.draw()

    ### random tree

    dendrite = get_random_dendrogramme(nb_pt)

    #print(dendrite)

    plan.add_cluster(dendrite)

    dendrogramme = Dendogramme(dendrite)#, dictionnaire)

    print("longueur branches arbre alea", plan.len_branches_cluster(-1))

    inertie = get_inertie_dendrogramme(dendrite, pts)#

    print("inertie arbre alea", inertie)

    ### drawing results

    if draw_active:

        plan.draw()

        dendrogramme.draw()

    ### hierarchical clustering
    ## average
    dendrite, dictionnaire = hierarchical_clustering(pts, distance_euclidienne, nb_clusters)

    print("A", dendrite)

    plan.add_cluster(dendrite)

    dendrogramme = Dendogramme(dendrite)#, dictionnaire)

    ### drawing results

    if draw_active:

        plan.draw()

        dendrogramme.draw()

    print("longueur branches arbre avg", plan.len_branches_cluster(-1), total_dist_from_dict(dictionnaire))

    inertie = get_inertie_dendrogramme(dendrite, pts)

    print("inertie arbre avg", inertie)

    ## min
    dendrite, dictionnaire = hierarchical_clustering(pts, distance_euclidienne, nb_clusters, methode_aggregative=1)

    plan.add_cluster(dendrite)

    dendrogramme = Dendogramme(dendrite)#, dictionnaire)

    ### drawing results
    if draw_active:

        plan.draw()

        dendrogramme.draw()

    print("longueur branches arbre min", plan.len_branches_cluster(-1), total_dist_from_dict(dictionnaire))

    inertie = get_inertie_dendrogramme(dendrite, pts)

    print("inertie arbre min", inertie)

    ## max
    dendrite_x, dictionnaire = hierarchical_clustering(pts, distance_euclidienne, nb_clusters, methode_aggregative=2)

    plan.add_cluster(dendrite_x)

    dendrogramme = Dendogramme(dendrite_x)#, dictionnaire)

    ### drawing results
    if draw_active:

        plan.draw()

    print("longueur branches arbre max", plan.len_branches_cluster(-1), total_dist_from_dict(dictionnaire))

    inertie = get_inertie_dendrogramme(dendrite_x, pts)

    print("inertie arbre max", inertie)
    if draw_active:

        dendrogramme.draw()

    ## ward
    dendrite_w, dictionnaire = hierarchical_clustering(pts, distance_euclidienne, nb_clusters, methode_aggregative=3)

    plan.add_cluster(dendrite_w)

    dendrogramme = Dendogramme(dendrite_w)#, dictionnaire)

    ### drawing results
    if draw_active:

        plan.draw()

    print("longueur branches arbre ward", plan.len_branches_cluster(-1), total_dist_from_dict(dictionnaire))

    inertie = get_inertie_dendrogramme(dendrite_w, pts)

    print("inertie arbre ward", inertie)

    if draw_active:

        dendrogramme.draw()


    ### neighbor joining

    dict_dist, dict_affinites = neighbor_joining(matrix, scale_fact=0.16, visual=1)

    #print("A", dict_affinites)

    dendrite2 = enraciner(dict_affinites, 1)

    plan.add_cluster(dendrite2)

    print(dendrite2)

    dendrogramme2 = Dendogramme(dendrite2)#, dictionnaire)

    ### drawing results

    plan.draw()

    print("longueur branches arbre nj", plan.len_branches_cluster(-1))#, total_dictionaire_distance(dict_dist, dict_affinites))

    inertie = get_inertie_dendrogramme(dendrite2, pts)

    print("inertie arbre nj", inertie)

    dendrogramme2.draw()

comparaison_clusterings()

def comparaison_taille():

    tailles = [x for x in range(10, 40, 1)]

    essais = 30

    ys = []

    test = 0  # 0 for len total branche, 1 for inertie expliquee

    #a = extraire_mots("mots")

    #print(a[:100])

    #suppr_doublons(a)

    a = time.time()

    fct_distance = get_distance  # distance_edition  # )

    for taill in tailles:

        cs = [0 for x in range(4)]

        for x in range(essais):

            x_len = screen_width/2

            y_len = screen_height/2

            pts = []  #[[random.randint(0, 2*x_len), random.randint(0, 2*y_len)] for v in range(nb_pt)]  # []

            for x in range(2):

                for y in range(2):

                    pts += [[random.randint(x_len*x, (x+1)*x_len-100), random.randint(y_len*y, (y+1)*y_len-100)] for v in range(taill//4)]

            for x in range(taill-(taill//4)*4):

                pts.append([random.randint(0, screen_width), random.randint(0, screen_height)])

            #pts = [[random.randint(0, screen_width), random.randint(0, screen_height)] for v in range(taill)]  # [random.choice(a) for x in range(taill)]  # 

            matrix = matrix_from_pts(pts, fct_distance)
##
            ### random tree

            #dendrite = get_random_dendrogramme(taill)

            # hc
            # avg
            dendrite_avg, dictionnaire = hierarchical_clustering(pts, fct_distance, 1)

##
##            # ward
##            dendrite_ward, dictionnaire = hierarchical_clustering(pts, fct_distance, 1, 3)
##
            # min
            dendrite_min, dictionnaire = hierarchical_clustering(pts, fct_distance, 1, 1)

            # max
            dendrite_max, dictionnaire = hierarchical_clustering(pts, fct_distance, 1, 2)

            # nj
            dict_dist, dict_affinites = neighbor_joining(matrix, scale_fact=0.5, visual=0)

            dendrite_nj = enraciner(dict_affinites, 1)

            if test == 0:

                plan = Plan(pts)

##                plan.add_cluster(dendrite)
##
                plan.add_cluster(dendrite_avg)
##
                plan.add_cluster(dendrite_min)

                plan.add_cluster(dendrite_max)
##
##                plan.add_cluster(dendrite_ward)

                #n0 = plan.len_branches_cluster(0)

                n1 = plan.len_branches_cluster(0)
##
                n2 = plan.len_branches_cluster(1)
##
                n3 = plan.len_branches_cluster(2)
##
##                n4 = plan.len_branches_cluster(4)
##
                plan.add_cluster(dendrite_nj)
##
                n5 = plan.len_branches_cluster(-1)

            elif test == 1:

                #print(dendrite_avg, get_inertie_expliquee(dendrite_avg, pts), get_inertie_dendrogramme(dendrite_avg, pts))

                for x in range(3):

                    dendrite = get_reduced_dim_list(dendrite)

                    dendrite_avg = get_reduced_dim_list(dendrite_avg)

                    dendrite_min = get_reduced_dim_list(dendrite_min)

                    dendrite_max = get_reduced_dim_list(dendrite_max)

                    dendrite_ward = get_reduced_dim_list(dendrite_ward)

                    dendrite_nj = get_reduced_dim_list(dendrite_nj)

                #n0 = get_inertie_dendrogramme(dendrite, pts)

                n1 = get_inertie_dendrogramme(dendrite_avg, pts)

                n2 = get_inertie_dendrogramme(dendrite_min, pts)

                n3 = get_inertie_dendrogramme(dendrite_max, pts)

                n4 = get_inertie_dendrogramme(dendrite_ward, pts)

                n5 = get_inertie_dendrogramme(dendrite_nj, pts)

            ns = [n1, n2, n3, n5]#, n4, n5]  #n0, 

            cs = [cs[x]+ns[x] for x in range(len(cs))]

        if test == 0:

            ys.append([round(c/essais) for c in cs])

        else:

            ys.append([c/essais for c in cs])

        #print("N", taill, ms)

    ys = np.array(ys)

    labels = ["hc average", "hc min", "hc max", "neighbor j"]  #"random", "hc ward", 

    print(time.time()-a)

    for n in range(len(ys[0])):

        plt.plot(tailles, ys[:, n], linestyle=':', marker="o", label=labels[n])

    plt.legend()

    plt.show()

    print(tailles, ys)


def evolution_entropie():

    pts = [[random.randint(0, screen_width), random.randint(0, screen_height)] for v in range(40)]

    plan = Plan(pts)

    print("genereated pts", pts)

    matrix = matrix_from_pts(pts, get_distance_eucli_rn)

    dendrite_nj, dictionnaire = hierarchical_clustering(pts, get_distance_eucli_rn, 1)

    dict_dist, dict_affinites = neighbor_joining(matrix, scale_fact=0.5, visual=0)

    #dendrite_nj = enraciner(dict_affinites, 1)

    dend_alea = get_random_dendrogramme(50)

    min_dim = dim(dendrite_nj)  # min(dim(dendrite_nj), dim(dendrite), dim(dend_alea))

    dimensions = [x for x in range(min_dim, 1, -1)]

    inerties = [[], [], []]

    plan.add_cluster(dendrite_nj)

    plan.draw()

    for x in range(min_dim-1):

        plan.add_cluster(dendrite_nj, not_complete=True)

        plan.draw()

        #inerties[0].append(get_inertie_expliquee(dendrite, pts))

        inerties[1].append(get_inertie_expliquee(dendrite_nj, pts))

        print(inerties[1][-1])

        #inerties[2].append(get_inertie_expliquee(dend_alea, pts))

        #dendrite = get_reduced_dim_list(dendrite)

        dendrite_nj = get_reduced_dim_list(dendrite_nj)

        #dend_alea = get_reduced_dim_list(dend_alea)

    #plt.plot(dimensions, inerties[0], linestyle=':', marker="o", label="hc")

    plt.plot(dimensions, inerties[1], linestyle=':', marker="o", label="nj")

    #plt.plot(dimensions, inerties[2], linestyle=':', marker="o", label="random")

    plt.legend()

    plt.xlabel("dimension du dendrogramme")

    plt.ylabel("inertie expliquée du dendrogramme")

    plt.show()


#evolution_entropie()


def simulation_progressive():

    pts = [[100, 150], [150, 110], [310, 200], [205, 300], [220, 350]]

    ### graphical structure

    plan = Plan(pts)

    plan.draw()

    ###

    dendrite, dictionnaire = hierarchical_clustering(pts, distance_euclidienne, 1)

    clus1 = [3, 4]

    clus2 = [0, 1]

    clus3 = [2, [3, 4]]

    clus4 = [[0, 1], [2, [3, 4]]]

    cluss = [clus1, clus2, clus3, clus4]

    for x in range(len(cluss)):

        plan.add_cluster(cluss[x])

        plan.draw(all_clus=True)

    #print(dendrite)


#simulation_progressive()


def test_inertie():

    nb_pt = 5

    pts = [[random.randint(0, screen_width), random.randint(0, screen_height)] for v in range(nb_pt)]
##    x_len = screen_width/2
##
##    y_len = screen_height/2
##
##    pts = []  #[[random.randint(0, 2*x_len), random.randint(0, 2*y_len)] for v in range(nb_pt)]  # []
##
##    for x in range(2):
##
##        for y in range(2):
##
##            pts += [[random.randint(x_len*x, (x+1)*x_len-100), random.randint(y_len*y, (y+1)*y_len-100)] for v in range(nb_pt//4)]

    print("generated pts", pts)

    mat = matrix_from_pts(pts, get_distance_eucli_rn)

    dendrite, dictionnaire = hierarchical_clustering(pts, distance_euclidienne, 1)

    dic_dist, dic_affini = neighbor_joining(mat, visual=0)

    dendrite2 = enraciner(dic_affini, 1)

    inerties = []

    dimensions = [dim(dendrite)-x for x in range(dim(dendrite))]

    for x in range(dim(dendrite)):

        new_inertie = get_inertie_expliquee(dendrite, pts)

        print(new_inertie, dim(dendrite), dendrite)

        inerties.append(new_inertie)

        dendrite = get_reduced_dim_list(dendrite)

    plt.plot(dimensions, inerties, linestyle=':', marker="o")

    #plt.legend()

    plt.show()

#test_inertie()


def simulation_progressive2():

    pts = [[100, 150], [150, 110], [310, 200]]#, [205, 300], [220, 350]]

    matrix = matrix_from_pts(pts, get_distance)

    ### graphical structure

    plan = Plan(pts)

    plan.draw()

    ###

    dendrite, dictionnaire = neighbor_joining(matrix)

##    clus1 = [3, 4]
##
##    clus2 = [0, 1]
##
##    clus3 = [2, [3, 4]]
##
##    clus4 = [[0, 1], [2, [3, 4]]]
##
##    cluss = [clus1, clus2, clus3, clus4]
##
##    for x in range(len(cluss)):
##
##        plan.add_cluster(cluss[x])
##
##        plan.draw(all_clus=True)

    #print(dendrite)


#simulation_progressive2()


def extraire_mots(doc_name):

    with open(doc_name+".txt", "r", encoding='utf-8') as file:

        txt = []

        for x in file:

            txt += x.split()

    return txt



def remplacer_in_dendrite(dendrite, mots):

    n_dendr = []

    for x in dendrite:

        if type(x) == int:

            n_dendr.append(mots[x])

        else:

            n_dendr.append(remplacer_in_dendrite(x, mots))

    return n_dendr

def suppr_doublons(txt):

    n = len(txt)

    for x in range(len(txt)):

        mot = txt[n-1-x]

        if mot in txt[1:len(txt)-1-x]:

            del txt[len(txt)-1-x]


def test_arbre_mot():

    a = extraire_mots("mots")

    print(a)

    suppr_doublons(a)

    print(a)

    nb_pt = 100

    pts = ["correct", "cor", "corps", "machine", "copie", "coquille", "crabe", "cogne", "bouteille", "faucon"]

    dendrite, dictionnaire = hierarchical_clustering(pts, distance_edition, 1)

    dendrogramme = Dendogramme(dendrite, mots=pts)#, dictionnaire)

    dendrogramme.draw()

    matrix = matrix_from_pts(pts, distance_edition)

    dict_dist, dict_affinites = neighbor_joining(matrix, visual=0)

    for x in range(len(pts)):

            dendrite = enraciner(dict_affinites, x)

            dendrogramme = Dendogramme(dendrite, mots=pts)#, dictionnaire)

            dendrogramme.draw()


#test_arbre_mot()

def comparaison_taille2():
    """ avec tests dans R^n au lieu de R^2 : on plot la taille des arbres pour quelques méthodes en fonction du nombre de points, et de la dimensions dans laquelle ceux-ci vivent """

    tailles = [x for x in range(10, 12)]

    all_essais = [d for d in range(1, 15, 4)]#dimensions  # all_essais

    #essais = 5

    zs_random = []

    zs_hc_avg = []

    zs_hc_ward = []

    zs_nj = []

    zss = [zs_random, zs_hc_avg, zs_nj] # , , zs_hc_ward, 

    for taill in tailles:

        for zs in zss:

            zs.append([])

        for essais in all_essais:  # dimension in dimensions:  #

            cs = [0 for x in range(len(zss))]

            for x in range(essais):

##                taille = 1000
##
##                moitie = taille/2
##
##                pts = []
##
##                for x in range(2):
##
##                    #for y in range(2):
##
##                    pts += [[random.randint(moitie*x, (x+1)*moitie) for d in range(dimension)] for v in range(taill//2)]

                pts = [[random.randint(0, 1000) for d in range(2)] for v in range(taill)]#dimensions

                plan = Plan(pts)

                matrix = matrix_from_pts(pts, get_distance_eucli_rn)

                ### random tree

                dendrite = get_random_dendrogramme(taill)

                plan.add_cluster(dendrite)

                n0 = plan.len_branches_cluster(-1)

                # hc
                # avg
                dendrite, dictionnaire = hierarchical_clustering(pts, get_distance_eucli_rn, 1)

                plan.add_cluster(dendrite)

##                # ward
##                dendrite, dictionnaire = hierarchical_clustering(pts, get_distance_eucli_rn, 1, 3)
##
##                plan.add_cluster(dendrite)
##
                n1 = plan.len_branches_cluster(-1)
##
##                n2 = plan.len_branches_cluster(2)

                # nj
                dict_dist, dict_affinites = neighbor_joining(matrix, scale_fact=0.5, visual=0)

                dendrite2 = enraciner(dict_affinites, 1)

                plan.add_cluster(dendrite2)

                n3 = plan.len_branches_cluster(-1)

                ns = [n0, n1, n3]  # , n2, 

                cs = [cs[x]+ns[x] for x in range(len(cs))]

            for x in range(len(cs)):

                zss[x][-1].append(round(cs[x]/essais))

        #print("N", taill, ms)

    zss = np.array(zss)

    #labels = ["hc average", "hc ward", "neighbor j"]  # "random", 

    fig = plt.figure()

    ax = plt.axes(projection='3d')

    #ax.plot_surface(x, y, z, cmap='viridis', edgecolor='none')

    tailles_x = np.outer(tailles, np.ones(len(all_essais)))

    dimensions_y = np.outer(all_essais, np.ones(len(tailles))).T

    for n in range(len(zss)):

        if n == 0:

            print(tailles_x, dimensions_y, np.array(zss[n]))

            print(tailles_x.shape, dimensions_y.shape, np.array(zss[n]).shape)

            ax.plot_surface(tailles_x, dimensions_y, np.array(zss[n]), edgecolor='none', cmap='viridis')

        else:

            ax.plot_surface(tailles_x, dimensions_y, np.array(zss[n]), edgecolor='none')#, cmap='viridis')  # , linestyle=':', marker="o"

    #ax.plot_surface(tailles_x, dimensions_y, np.array(zss[3]), edgecolor='none')

    #ax.legend()

    plt.show()

    #print(tailles, ys)

#comparaison_taille()

#comparaison_taille2()


def comparaison_taille3():
    """ avec tests dans R^n au lieu de R^2 : on plot la taille des arbres pour quelques méthodes en fonction du nombre de points, et de la dimensions dans laquelle ceux-ci vivent """

    tailles = [x for x in range(10, 30)]

    nb_dim = [x for x in range(2, 11)]  # dimensions prises par le dendrogramme

    essais = 20

    zs_random = [[[] for x in range(len(nb_dim))] for y in range(len(tailles))]

    zs_hc_avg = [[[] for x in range(len(nb_dim))] for y in range(len(tailles))]

    zs_hc_ward = [[[] for x in range(len(nb_dim))] for y in range(len(tailles))]

    zs_nj = [[[] for x in range(len(nb_dim))] for y in range(len(tailles))]

    zss = [zs_random, zs_hc_avg, zs_nj] # , , zs_hc_ward,

    t = -1

    for taill in tailles:

        t += 1

        for x in range(essais):

            pts = [[random.randint(0, 1000) for d in range(2)] for v in range(taill)]#dimensions

            matrix = matrix_from_pts(pts, get_distance_eucli_rn)

            ### random tree

            dendrite_rd = get_random_dendrogramme(taill)

            # hc
            # avg

            dendrite_rd, dictionnaire = hierarchical_clustering(pts, get_distance_eucli_rn, 1, 3)
            dendrite_avg, dictionnaire = hierarchical_clustering(pts, get_distance_eucli_rn, 1)

            # nj
            dict_dist, dict_affinites = neighbor_joining(matrix, scale_fact=0.5, visual=0)

            dendrite_nj = enraciner(dict_affinites, 1)

            min_dim = min(dim(dendrite_nj), dim(dendrite_rd), dim(dendrite_avg))

            #nb_dim.append(min_dim-1)

            d = len(nb_dim)

            for dimens in nb_dim:  # dimension in dimensions:  #

                d -= 1

                #cs = [0 for x in range(len(zss))]

                if dim(dendrite_rd) > 1:

                    #print(taill, get_inertie_dendrogramme(dendrite_rd, pts))

                    zss[0][t][d].append(get_inertie_dendrogramme(dendrite_rd, pts))

                    dendrite_rd = get_reduced_dim_list(dendrite_rd)

                else:

                    zss[0][t][d].append(None)

                if dim(dendrite_rd) > 1:

                    zss[1][t][d].append(get_inertie_dendrogramme2(dendrite_avg, pts))

                    dendrite_avg = get_reduced_dim_list(dendrite_avg)

                else:

                    zss[1][t][d].append(None)

                if dim(dendrite_nj) > 1:

                    zss[2][t][d].append(get_inertie_dendrogramme(dendrite_nj, pts))

                    dendrite_nj = get_reduced_dim_list(dendrite_nj)

                else:

                    zss[2][t][d].append(None)

        for n in range(len(zss)):

            for d in range(len(nb_dim)):

                s = 0

                c = 0

                for e in zss[n][t][d]:

                    if e != None:

                        c += 1

                        s += e

                if c == 0:

                   zss[n][t][d] = 1  # np.nan

                else:

                    zss[n][t][d] = s/c

                        

        #print("N", taill, ms)

    zss = np.array(zss)

    #print(zss.shape, zss)

    #labels = ["hc average", "hc ward", "neighbor j"]  # "random", 

    fig = plt.figure()

    ax = plt.axes(projection='3d')

    #ax.plot_surface(x, y, z, cmap='viridis', edgecolor='none')

    tailles_x = np.outer(tailles, np.ones(len(nb_dim)))

    dimensions_y = np.outer(nb_dim, np.ones(len(tailles))).T

    ax.plot_surface(tailles_x, dimensions_y, np.array(zss[2]), cmap=cm.coolwarm, linewidth=0)  # , antialiased=False, vmin=-1, vmax=1)

    ax.plot_surface(tailles_x, dimensions_y, np.array(zss[0]), cmap='viridis', linewidth=0)  # , antialiased=False, vmin=-1, vmax=1)
##    for n in [0, 1]:
##
##        if n == 0:
##
##            #print(np.array(zss[n]).shape, tailles_x.shape, dimensions_y.shape)
##
##            #print("z", zss[n], "x", tailles_x, dimensions_y)
##
##            ax.plot_surface(tailles_x, dimensions_y, np.array(zss[n]), rstride=1, cstride=1, cmap=cm.coolwarm, linewidth=0, antialiased=False, vmin=-1, vmax=1)  #cmap='viridis'
##
##        if n == 1:
##
##            ax.plot_surface(tailles_x, dimensions_y, np.array(zss[n]), rstride=1, cstride=1, cmap='viridis', linewidth=0, antialiased=False, vmin=-1, vmax=1)
##
##        else:
##
##            ax.plot_surface(tailles_x, dimensions_y, np.array(zss[n]))#, rstride=1, cstride=1, edgecolor='none', linewidth=0, antialiased=False, vmin=-1, vmax=1)#, cmap='viridis')  # , linestyle=':', marker="o"

    #ax.plot_surface(tailles_x, dimensions_y, np.array(zss[3]), edgecolor='none')

    #ax.legend()

    plt.show()

    #print(tailles, ys)

#comparaison_taille3()


### Tests base de donnee Covid
###

def distance_seq(seq1, seq2):

    dist = 0

    for y in range(len(seq1)):

        string = seq1[y]

        string2 = seq2[y]

        for x in range(len(string)):

            if string[x] != string2[x]:

                dist += 1

    return dist

            
def extraire_alignment():

    alignements = []

    noms = []

    with open("align21.fasta", "r") as file:

        c = 0

        for line in file:

            if line[0] == ">":

                c += 1

                alignements.append([])

                noms.append(str(c)+"_"+line[1:])

            else:

                alignements[-1].append(line[:-1])

    matrix_dist = [[0 for x in range(len(alignements))] for y in range(len(alignements))]

    for y in range(len(alignements)):

        for x in range(y+1, len(alignements)):

            matrix_dist[y][x] = distance_seq(alignements[y], alignements[x])

            #matrix_dist[x][y] = distance_seq(alignements[y], alignements[x])

    print_matrix(matrix_dist)
    for y in matrix_dist:

        print(*y)

    dict_dist, dict_affin = neighbor_joining(matrix_dist, 0.05, 0)

    dendrite_nj = enraciner(dict_affin, 0)

    print(dendrite_nj)

    dendro = Dendogramme(dendrite_nj)

    dendro.draw()

    modified_matrix = [[matrix_dist[x][y] for x in range(y+1, len(matrix_dist))] for y in range(len(matrix_dist)-1)]

    dendr_hc, dico = hierarchical_clustering_mat(modified_matrix)

    print(dendr_hc)

    dendro = Dendogramme(dendr_hc)

    dendro.draw()


#extraire_alignment()


def appliquer_fct(liste, fct):

    for idx in range(len(liste)):

        x = liste[idx]

        if type(x) == list:

            appliquer_fct(x, fct)

        else:

            liste[idx] = fct(x)


def arbre_site():

    def get_liste(liste, profondeur):

        if profondeur == 0:

            return liste

        else:

            return get_liste(liste[-1], profondeur-1)

    arbre = []

    location = 0

    active_profondeur = 0

    double_pt = False

    start = True

    with open("arbre_50_hc.txt", "r") as file:

        for line in file:

            for x in range(len(line)):

                car = line[x]

                if car == "(":

                    active_liste = get_liste(arbre, active_profondeur)

                    active_profondeur += 1

                    active_liste.append([])

                elif car == ")":

                    active_profondeur -= 1

                    double_pt = False

                elif car == ":":

                    active_liste = get_liste(arbre, active_profondeur)

##                    if not line[x+1]:
##
##                        active_liste.append([])

                    double_pt = True

                elif car == ",":

                    double_pt = False

                    start = True

                    active_liste = get_liste(arbre, active_profondeur)

                    active_liste.append("#")

                elif not double_pt and car != "\n" and start == True:

                    if car == "_":

                        start = False
                    else:

                        active_liste = get_liste(arbre, active_profondeur)

                        active_liste.append(car)

    def transformer_liste(liste):

        index_to_add = -1

        to_remove_indxs = []

        for x in range(len(liste)):

            ele = liste[x]

            if type(ele) == list:

                transformer_liste(ele)

            elif ele == "#":

                index_to_add = x+1

                to_remove_indxs.append(x)

            else:

                if index_to_add == -1:

                    index_to_add = x

                    liste[x] = int(ele)

                elif x == index_to_add:

                    liste[x] = int(ele)

                else:

                    liste[index_to_add] *= 10

                    liste[index_to_add] += int(ele)

                    to_remove_indxs.append(x)

        for x in range(len(to_remove_indxs)-1, -1, -1):

            del liste[to_remove_indxs[x]]

    transformer_liste(arbre)

    arbre = arbre[0]

    appliquer_fct(arbre, lambda x:x-1)

    print(arbre)

    dendro = Dendogramme(arbre)

    dendro.draw()


#arbre_site()

"""
[0, [29, [42, [[[7, 10], [[3, 19], [[11, [1, [[39, [25, [13, 35]]], [26, [2, [23, 48]]]]]], [30, 32]]]], [12, [16, [[[36, [[22, 33], [45, [41, 46]]]], [31, 34]], [[6, 20], [[28, 40], [[37, [17, [21, [38, [43, [5, [15, [18, 24]]]]]]]], [14, [27, [[9, 44], [[4, 8], [47, 49]]]]]]]]]]]]]]]

"""



def nom_variant():

    dico_color = {}

    variants = ["A", "B.1"]

    with open("names_and_classification.txt", "r") as file:

        for line in file:

            #print(line.split())

            variants.append(line.split()[8])

    del variants[2]

    c = -1

    colors = [RED, BLUE, GREEN, BROWN, BLACK, YELLOW, ORANGE, GREY]

    for string in variants:

        if not string in dico_color.keys():

            c += 1

            dico_color[string] = colors[c]  # get_random_color()
    print(variants)
    dend_me_hc = [[[43, [[21, 38], [5, [24, [15, 18]]]]], [44, [[41, [[34, [36, [22, 33]]], [45, 46]]], [6, [9, [[27, [[17, 37], [[14, 28], [20, [31, 40]]]]], [[47, 49], [4, 8]]]]]]]], [[[35, [[48, [23, 26]], [39, [13, 25]]]], [1, 2]], [42, [[11, [[7, 10], [[3, 19], [30, 32]]]], [[0, 29], [12, 16]]]]]]

    dend_me_nj = [0, [29, [42, [[[7, 10], [[3, 19], [[11, [1, [[39, [25, [13, 35]]], [26, [2, [23, 48]]]]]], [30, 32]]]], [12, [16, [[[36, [[22, 33], [45, [41, 46]]]], [31, 34]], [[6, 20], [[28, 40], [[37, [17, [21, [38, [43, [5, [15, [18, 24]]]]]]]], [14, [27, [[9, 44], [[4, 8], [47, 49]]]]]]]]]]]]]]]

##    dend_site_hc = [[[[[[[0, [29, 41]], 9], [[3, 6], [4, [7, 8]]]], [[[[[[[[14, 38], 16], [17, 21]], [15, 20]], [28, [31, 40]]], [[22, [33, 36]], [27, 37]]], 34], 45]], [12, [[46, 47], 49]]], [[42, 44], 43]], [[[[[1, [[[5, 26], [19, [23, 24]]], 18]], 30], 39], [[10, 11], [[[13, [25, 32]], 48], 35]]], 2]]
##
##    dend_site_nj = [[[[[[[[[[[[[[[0, [[[29, 41], 35], [[42, 44], 43]]], 9], [10, 45]], 2], [[[[1, 5], 7], [11, 13]], [[3, [12, [[[46, 49], 47], 48]]], [4, 8]]]], 6], 14], 15], 20], 38], [[16, [[[[[28, 31], 32], 34], 39], 40]], 21]], [19, 24]], [25, 26]], [30, 36]], [[17, [[18, 22], 27]], 23], [33, 37]]

##    dend_me_hc = [0, [13, [2, [1, [[12, [10, [[6, 7], [9, [3, [5, [8, 11]]]]]]], 4]]]]]
##    dend_me_nj = [[[12, 13], [[0, 1], [2, 3]]], [[[4, 5], [6, 7]], [[8, 9], [10, 11]]]]
#    dend_me_hc = [0, [[[12, [16, [5, [13, [[7, [6, [10, 11]]], [3, 15]]]]]], [14, [9, [17, 18]]]], [[1, 8], [4, 2]]]]
#    dend_me_nj = [[[[6, 7], [8, 9]], [[10, 11], [12, 13]]], [[[14, 15], [16, 17]], [[18, [0, 1]], [[2, 3], [4, 5]]]]]
    dendo1 = Dendogramme(dend_me_hc, mots = variants, dico_color=dico_color)

    dendo1.draw()

    dendo2 = Dendogramme(dend_me_nj, mots = variants, dico_color=dico_color)

    dendo2.draw()
##
##    dend_partiel = [[[7, 10], [[3, 19], [[11, [1, [[39, [25, [13, 35]]], [26, [2, [23, 48]]]]]], [30, 32]]]], [12, [16, [[[36, [[22, 33], [45, [41, 46]]]], [31, 34]], [[6, 20], [[28, 40], [[37, [17, [21, [38, [43, [5, [15, [18, 24]]]]]]]], [14, [27, [[9, 44], [[4, 8], [47, 49]]]]]]]]]]]]
##
##    dendo3 = Dendogramme(dend_partiel, mots = variants, dico_color=dico_color)
##
##    dendo3.draw()
##
##    dend_partiel2 = [[3, 19], [[11, [1, [[39, [25, [13, 35]]], [26, [2, [23, 48]]]]]], [30, 32]]]
##
##    dendo4 = Dendogramme(dend_partiel2, mots = variants, dico_color=dico_color)
##
##    dendo4.draw()
##
##    dend_partiel3 = [[[36, [[22, 33], [45, [41, 46]]]], [31, 34]], [[6, 20], [[28, 40], [[37, [17, [21, [38, [43, [5, [15, [18, 24]]]]]]]], [14, [27, [[9, 44], [[4, 8], [47, 49]]]]]]]]]
##
##    dendo5 = Dendogramme(dend_partiel3, mots = variants, dico_color=dico_color)
##
##    dendo5.draw()

##    dendo3 = Dendogramme(dend_site_hc, mots = variants, dico_color=dico_color)
##
##    dendo3.draw()
##
##    dendo4 = Dendogramme(dend_site_nj, mots = variants, dico_color=dico_color)
##
##    dendo4.draw()

    def get_proportions(liste_ins, names):

        if type(liste_ins) == int:

            return [1], [names[liste_ins]]

        dico = {}

        for x in liste_ins:

            elem = names[x]

            if elem in dico.keys():

                dico[elem] += 1

            else:

                dico[elem] = 1

        labels = [l for l in dico.keys()]

        tot = sum([x for x in dico.values()])

        props = [dico[l]/tot for l in labels]

        return props, labels

    dendrite = dend_me_nj

    for x in range(dim(dendrite)):

        print(dendrite)

        nb_partition = len(dendrite)

        partitions = [get_flattened_list(dendrite[x]) for x in range(nb_partition)]

        proportions = []

        c = 0

        for part in partitions:

            print(part)

            c += 1

            fig, ax = plt.subplots(figsize =(10, 7))

            values, labels = get_proportions(part, variants)

            wedges, texts = ax.pie(values, labels=labels)  # plt.pie(values, labels=labels)

            ax.set_title("dimension {}, partie {}".format(dim(dendrite)-x, c))

        plt.show()

        dendrite = get_reduced_dim_list(dendrite)


#nom_variant()
