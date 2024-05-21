from pig_tv import *


dico = {}

def fill_dico():

    def dico_add(key, value):

        if key in dico.keys():

            if not value in dico[key]:

                dico[key].append(value)

        else:

            dico[key] = [value]

    dico = {}

    nature = None

    c = -1

    with open("dico_francais.txt", "r", encoding="utf-8") as file:

        for line in file:

            #print(c)

            c += 1

            if c > 15:

                if line[:9] == ";;;;;;;;;":  # flexion d'un lemme (ex: avions et fléchis de avion

                    mots = line[10:].split(";")

                    #print(mots)

                    dico_add(mots[0], nature)

                else:  # lemme

                    mots = line.split(";")
                    #print(mots)

                    lemme = mots[0]

                    nature = mots[2]

                    if mots[3] != "":

                        print(mots[3])

                    dico_add(lemme, nature)

                    if nature == "Verbe":

                        nature = "Verbe conjugué"

                    premiere_flexion = mots[9]

                    dico_add(premiere_flexion, nature)

##            if c == 60:
##
##                break

    return dico


dico = fill_dico()




def get_indexs(liste, element):

    indexs = []

    for x in rl(liste):

        a = liste[x]

        if a == element:

            indexs.append(x)

    return indexs



class Phrase:

    def __init__(self, string):

        self.string = string

        self.liste_mots = phrase.split()

        self.verb_indexs = get_indexs(liste_natures, "Verbe Conjugué")

        ## Premier decoupage
        self.phrase_simple = -1  # -1 for unknown, 0 for simple, 1 for complex

        # Si la phrase est simple, elle est decoupee en deux parties : la phrase sujet et la phrase verbale sont deux sous parties de la phrase, une associee au sujet, l'autre au verbe

        self.phrase_sujet = None

        self.phrase_verbale = None

        # sinon elle est decoupee en sous phrases coordinees quasi independantes

        self.sous_phrases = None

        Phrase.decouper_phrase(self)
        ##


    def string_from_liste(liste_mots):

        return "".join(liste_mots)

    def decouper_phrase(self):
    """ finds two groups of words : the subject and the verbal phrase """


        def phrase_decoupee(liste_mot, sepa):

            return "sujet : {} ; phrase verbale : {}\n".format(get_phrase(liste_mots[:cassure]), get_phrase(liste_mots[cassure:]))

        liste_natures = [dico[mot] for mot in self.liste_mots]

        if len(self.index_verbes) == 1:  # phrase simple

            self.phrase_simple = 0

            cassure = index_verbes[0]

        else:  # besoin de plus d'indices

            indexs_coord = get_indexs(liste_natures, "Conjonction")

            for index in indexs_coord:

                if liste_mots[index].plus_precis == "Coordination":  # la phrase est decoupee en deux morceaux +/- independants

                    if  index+1 in index_verbes:# omission de repetition du sujet (ex : Le chat joue de la guitare et (! le chat) mange du fromage.)

                        pass

                


    return 























