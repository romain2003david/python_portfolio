import random


#from pig_tv import *

class Word:

    classes_equivalence = [["e", "é", "è", "ê"], ["a", "à"], ["u", "ù"]]

    def __init__(self, string):

        self.string = string

        self.normalized_string = list(self.string.lower())

        for x in range(len(self.normalized_string)-1, -1, -1):

            car = self.normalized_string[x]

            if car == " " or car == "\n":

                del self.normalized_string[x]

            for classe in Word.classes_equivalence:

                if car in classe:

                    self.normalized_string[x] = classe[0]

        self.normalized_string = "".join(self.normalized_string)

    def __eq__(self, word2):

        if isinstance(word2, Word):

            return self.normalized_string == word2.normalized_string

        elif isinstance(word2, str):

            return self.string == word2

    def __repr__(self):

        return self.string

    def __hash__(self):

        return hash(self.string)



def liste_to_str(liste):

    string = ""

    for x in liste:

        string = string+x

    return string


def create_dico():

    with open("dico_ang.txt", "r", encoding="utf_8") as file:

        lines = []

        for line in file:

            if len(line) > 3:

                lines.append(line)

        dico = {}

        def dico_append(chunk):

            try:

                key, val = chunk.split(":")

            except ValueError:

                print(chunk)

            vals = val.split(",")

            dico[Word(key)] = tuple([Word(v) for v in vals])

            return key

        for line in lines:

            parts = line.split(";")

            key = dico_append(parts[0])

            if len(parts) > 1:

                for x in range(1, len(parts)):

                    temp_part = parts[x].split(":")

                    if "." in temp_part[0]:

                        indx = temp_part[0].index(".")

                        debut = temp_part[0][:indx-1]

                        fin = temp_part[0][indx+2:]

                        temp_part[0] = debut+key+fin

                    string = temp_part[0]+ ":" + temp_part[1]

                    dico_append(string)

        return dico


def test_word_engl(dico):

    word = random.choice(list(dico.keys()))

    print(word, end=" ")

    answers = dico[word]  # list of words

    user_guess = Word(input(" = ? (q to quit)\n- "))

    if user_guess == "q":

        return False

    else:

        found = False

        for mot in answers:

            if user_guess == mot:

                found = True

        print("{} : solutions were :".format(found))

        for x in answers:

            print(x)

        return True


def english_translate(dico):

    while test_word_engl(dico):

        pass


def menu(dico):

    invite = "Tap e if you want to translate english words into french, f if you want to translate french words into english and q to quit"

    answer = None

    while answer != "q":

        print(invite)

        answer = input("- ")

        if answer == "e":

            english_translate(dico)


def main():

    dico = create_dico()

    menu(dico)


main()

    
