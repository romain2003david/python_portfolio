##
##def sur_les_ondes(n, freqs):
##    """
##    :param n: nombre de fréquences données
##    :type n: int
##    :param freqs: la liste des fréquences à vérifier
##    :type freqs: list[int]
##    """
##    freq3 = [x for x in freqs if x%3==0]
##
##    return min(freq3)
##
##
##if __name__ == '__main__':
##    n = int(input())
##    freqs = list(map(int, input().split()))
##    print(sur_les_ondes(n, freqs))

##def resoudre(ncouleurs, couleurs, ncotes, couleurscotes, npieces, pieces):
##    """
##    :param ncouleurs: le nombre de couleurs
##    :type ncouleurs: int
##    :param couleurs: les différentes couleurs possibles
##    :type couleurs: list[str]
##    :param ncotes: le nombre de côtés de la pièce manquante
##    :type ncotes: int
##    :param couleurscotes: les couleurs des pièces adjacentes à la pièce manquante
##    :type couleurscotes: list[str]
##    :param npieces: le nombre de pièces à trier
##    :type npieces: int
##    :param pieces: les pièces à trier
##    :type pieces: list[dict["nCotesPiece": int, "couleurPiece": str]]
##    """
##    # TODO Affiche sur la première ligne, pour chaque pièce un caractère 'O' si
##    # la pièce peut correspondre à celle recherchée, 'X' sinon. Affiche sur la
##    # ligne suivante le nombre de pièces qui peuvent correspondre.
##
##    string = ""
##
##    t = 0
##
##    for p in pieces:
##
##        cotes, color = p
##
##        if cotes == ncotes and (not color in couleurscotes):
##
##            string += "O"
##
##            t += 1
##
##        else:
##
##            string += "X"
##
##    print(string)
##    print(t)
##
##
##if __name__ == '__main__':
##    ncouleurs = int(input())
##    couleurs = [input() for _ in range(ncouleurs)]
##    ncotes = int(input())
##    couleurscotes = [input() for _ in range(ncotes)]
##    npieces = int(input())
##    pieces = [[
##        int(input()),
##        input()
##    ] for _ in range(npieces)]
##    resoudre(ncouleurs, couleurs, ncotes, couleurscotes, npieces, pieces)


##def print_result(liste, slice1, slice2):
##
##    print(*liste[slice1[0]:(slice1[0]+slice1[1])+1])
##
##    print(*liste[slice2[0]:(slice2[0]+slice2[1])+1])
##
##
##def resoudre(x, n, liste):
##    """
##    :param x: le nombre magique
##    :type x: int
##    :param n: la longueur du code la Matriks
##    :type n: int
##    :param l: le code de la Matriks
##    :type l: list[int]
##    """
##    # TODO Les deux clés (chacune sur une ligne) ou le message "IMPOSSIBLE".
##
####    liste_cles = []  # liste des nombres qu'on peut construire en sommant les termes de sous listes
####
####    liste_indics = []  # liste de couple index_first_element, len sous liste qui reperent la sous liste en question
##
##    cles_dict = {}
##
##    for i in range(n):
##
##        cle = 0
##
##        for j in range(i, n):
##
##            cle += liste[j]
##
##            if (x/cle) == int(x/cle):  # la cle divise x, donc est possiblement une solution
##
##                current_len = j-i
##
##                if cle in cles_dict.keys():  # la cle (en tant que somme) existe deja
##
##                    if cles_dict[cle][1] < current_len:  # on a trouve une sous liste plus longue
##
##                        cles_dict[cle] = [i, current_len]
##
##                else:  # new diviseur found
##
##                    cles_dict[cle] = [i, current_len]
##
##    # cherche le couple de diviseurs qui verifient d1*d2 = x et constitues des sous liste les plus grandes
##    best_couple = []
##
##    len_record = 0
##
##    diviseurs = list(cles_dict.keys())
##
##    while diviseurs != []:
##
##        not_the_same = True
##
##        div1 = diviseurs[0]
##
##        quotient = x//div1
##
##        if quotient in diviseurs:
##
##            indx = diviseurs.index(quotient)
##
##            if indx == 0:
##
##                not_the_same = False
##
##            div2 = diviseurs[indx]
##
##            tot_len = len(cles_dict[div2]) + len(cles_dict[div1])
##
##            if tot_len > len_record:
##
##                len_record = tot_len
##
##                best_couple = [cles_dict[div2], cles_dict[div1]]
##
##            del diviseurs[indx]
##
##        if not_the_same:
##
##            del diviseurs[0]
##
##    # printing results
##    if best_couple == []:
##
##        print("IMPOSSIBLE")
##
##    else:
##
##        if best_couple[0][1] > best_couple[1][1]:
##
##            print_result(liste, best_couple[0], best_couple[1])
##
##        elif best_couple[0][1] < best_couple[1][1]:
##
##            print_result(liste, best_couple[1], best_couple[0])
##
##        else:
##
##            slice1, slice2 = best_couple[0], best_couple[1]
##
##            if sum(liste[slice1[0]:(slice1[0]+slice1[1])+1]) > sum(liste[slice2[0]:(slice2[0]+slice2[1])+1]):
##
##                print_result(liste, best_couple[0], best_couple[1])
##
##            else:
##
##                print_result(liste, best_couple[1], best_couple[0])
##
##
##import random
##
##if __name__ == '__main__':
####    x = int(input())
####    n = int(input())
####    liste = list(map(int, input().split()))
####
####    resoudre(x, n, liste)
##
##    for x in range(10):
##
##        x = random.randint(1, 100000)
##        n = random.randint(1, 100000)
##
##        liste = [random.randint(1, x) for i in range(n)]
##
##        resoudre(x, n, liste)
##
##        print(x)
##
##        print()



def valid_password(chaine):

    valide = [0, 0, 0, 0]

    for char in chaine:

        if char.isupper():

            valide[0] = 1

        if char.islower():

            valide[1] = 1

        if char.isdigit():

            valide[3] = 1

        if char in "!#$%&'()*+,-./:;<=>?@[\]^_`{|}~" or char == '"':

            valide[2] = 1

    return valide == [1, 1, 1, 1]


def fuite_de_clavier(n, k, chaine):
    """
    :param n: taille de la chaîne
    :type n: int
    :param k: taille du mot de passe
    :type k: int
    :param chaine: la chaîne contenant le mot de passe
    :type chaine: list[str]
    """
    # TODO afficher le nombre de mots de passes possibles parmi la chaîne

    nb_chaine = 0

    for x in range(0, n-k+1):

        chain = chaine[x:x+k]

        if valid_password(chain):

            nb_chaine += 1

    return nb_chaine


if __name__ == '__main__':
    n = int(input())
    k = int(input())
    chaine = list(input())
    print(fuite_de_clavier(n, k, chaine))
