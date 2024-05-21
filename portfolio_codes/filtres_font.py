import os

from pig_tv import *

import numpy as np

import string


def see():

    for filename in os.listdir("font/"):
        #print(filename)

        if len(filename) == 7 and filename[1] == "2":

            os.remove("font/"+filename)

     
def closest_in(element, liste):

    return np.argmin([abs(x-element) for x in liste])


def no_extension(filename):

    c = len(filename)-1

    while filename[c] != ".":

        c -= 1

    return filename[:c]


class Lettre:

    def __init__(self, file_name, rep="font/"):

        self.img = pygame.image.load(rep+file_name)

        self.rect = self.img.get_rect()

        self.name = no_extension(file_name)

        self.this_width, self.this_height = self.rect[2], self.rect[3]

        print(self.this_width, self.this_height, self.name)

        if self.name in ["g", "j", "p", "q", "z", "y", "f"]:

            self.low = 1

        else:

            self.low = 0

    def scale(self):

        width = [50, 100]

        height = [50, 100, 150]

        self.this_width, self.this_height = width[closest_in(self.rect[2], width)], height[closest_in(self.rect[3], height)]

        self.img = pygame.transform.scale(self.img, (self.this_width, self.this_height))

    def filter(self, see_diff = True):

        global screen

        screen = pygame.display.set_mode((self.this_width, self.this_height))

        screen.blit(self.img, (0, 0))

        if see_diff:

            print("original image")

            pygame.display.update()

            wait()

        # takes out the lines

        for x in range(self.this_width):

            for y in range(self.this_height):

                pix = screen.get_at((x, y))

                mean = round(sum(pix[:3])/3)

                if mean > 205:

                    screen.set_at((x,y), [255, 255, 255])

        # thickens the letters

        def nearby_pix(x, y):

            indices = get_flattened_list([[(i, j) for i in range(-1, 2)] for j in range(-1, 2)], reduc_nb=1)

            #random.shuffle(indices)

            #print([(x+i, y+j) for (i, j) in indices if ((i, j) != (0, 0) and (0 <= x+i < self.this_width) and (0 <= y+j < self.this_height))])

            return [screen.get_at((x+i, y+j)) for (i, j) in indices if ((i, j) != (0, 0) and (0 <= x+i < self.this_width) and (0 <= y+j < self.this_height))]

        nb = 2

        for n in range(nb):

            screen_copy = [[screen.get_at((x, y)) for x in range(self.this_width)] for y in range(self.this_height)]

            for x in range(self.this_width):

                for y in range(self.this_height):

                    pix = screen.get_at((x, y))

                    if list(pix[:3]) == WHITE:

                        for oth_pix in nearby_pix(x, y):

                            if oth_pix != WHITE:

                                screen_copy[y][x] = oth_pix

                                #print(oth_pix)

                                break

            for x in range(self.this_width):

                for y in range(self.this_height):

                    screen.set_at((x, y), screen_copy[y][x])

        pygame.image.save(screen, "filtered_font/"+self.name+".jpeg")

        self.img = pygame.image.load('filtered_font/'+self.name+".jpeg")

        if see_diff:

            print("filtered image")

            screen.blit(self.img, (0, 0))

            pygame.display.update()

            wait()

    def draw(self, coor, size=50):

        n_img = self.img.copy()

        if size != 50:

            facteur = size/50

            n_img = pygame.transform.scale(self.img, (int(self.this_width*facteur), int(self.this_height*facteur)))

        screen.blit(n_img, coor)


class BlankLetter:

    def __init__(self):

        self.this_width, self.this_height = 50, 50

        self.low = 0

    def draw(self, coor, size):

        rect = pygame.Rect(coor[0], coor[1], size, size)

        pygame.draw.rect(screen, WHITE, rect)


class Font:

    repertory = "filtered_font/"

    special_character = "\\"

    def __init__(self):

        self.dico_lettres = {}

    def download(self):

        for filename in os.list_dir(repertory):

        #for lettre in string.ascii_lowercase:

            self.dico_filename_to_lettres[lettre] = Lettre(filename, rep=Font.repertory)

    def add_lettre(self, lettre):

        self.dico_lettres[lettre.name] = lettre

    def write(self, texte, x, y, size=50):

        olds_news = [(s+s, s.upper()) for s in string.ascii_lowercase]

        #olds_news.append(("\c", "\coeur"))

        olds_news.append((":", "\dbl_pt\\"))

        olds_news.append((".", "\pt\\"))

        olds_news.append(("?", "\intero\\"))

        olds_news.append(("\s1", "\smiley1\\"))

        olds_news.append(("\s2", "\smiley2\\"))

        olds_news.append(("\c", "\coeur\\"))

        for (old, new) in olds_news:

            texte = texte.replace(old, new)

        accentuees_aigu = [["é"], "\acc1\\", ["e"]]

        accentuees_grave = [["è", "à"], "\acc2\\", ["e", "a"]]

        accentuees_trema = [["ï", "ö", "ë"], "\acc3\\", ["i", "o", "e"]]

        accentuees_circon = [["î", "ê", "û", "ô"], "\acc4\\", ["i", "e", "u", "o"]]

        accents = [accentuees_aigu, accentuees_grave, accentuees_circon, accentuees_trema]

        for (liste_lettres, accent, lettres) in accents:

            for spe_lettre in liste_lettres:

                new = accent+lettres[liste_lettres.index(spe_lettre)]

                texte = texte.replace(spe_lettre, new)

        facteur = size/50

        coor = [x, y]

        dico_lettre = {}

        def next_read(texte):

            if texte[0] == Font.special_character:

                c = 1

                while c < len(texte) and texte[c] != Font.special_character:

                    c += 1

                return texte[1:c-1], texte[c:]  # takes out special character

            else:

                return texte[0], texte[1:]

        while texte != "":

            symbole, texte = next_read(texte)

            try:

                filename = dico_symbol_to_filename[symbole]

                lettre = self.dico_filename_to_lettres[filename]

            except KeyError:

                lettre = BlankLetter()

            coor[1] -= lettre.this_height*facteur - size*(1+lettre.low)

            lettre.draw(coor, size)

            coor[0] += lettre.this_width*facteur

            coor[1] += lettre.this_height*facteur - size*(1+lettre.low)

            if coor[0]+2*size > screen_width:

                coor[0] = x

                coor[1] += 2.2*size

        pygame.display.update()

    


def main():

    global screen

    font = Font()

    create_font = True

    if create_font:

        for file_name in os.listdir("font"):

            #if not "2" in file_name:

            lettre = Lettre(file_name)

            lettre.scale()

            lettre.filter(see_diff=False)

            font.add_lettre(lettre)

        screen = pygame.display.set_mode((screen_width, screen_height))

    else:

        font.download()

    screen.fill(WHITE)

    font.write("romix", 100, 100, 20)

    #font.write("hello my love i write to you in a new font that i have drawn by myself", 0, 200, 20)

    font.write("Bonjour je m'appelle Romain; mais pas Rômàïn", 0, 200, 20)

    #font.write("Hmm. We’re having trouble finding that site.We can’t connect to the server at www.google.com.If you entered the right address, you can:Try again laterCheck your network connectionCheck that Firefox has permission to access the web (you might be connected but behind a firewall)", 50, 200, 20)



##        screen.blit(img, (0, 0))
##
##        pygame.display.update()
##
##        wait()

        #for x in range(


main()
