from pig_tv import *


def treat_formated_compute_array(array):

    open_parenthesis = 0

    opening_index = -1

    # deals with parenthesis : deals with each separated part by parenthesis first, by calling treat_formated_compute_array for each part

    still_parentheses = 1

    while still_parentheses:

        still_parentheses = 0

        if "(" in array:

            open_parenthesis = 1

            opening_index = array.index("(")

        if ")" in array:

            if not open_parenthesis:

                raise( "Error parenthesis" )

            closing_index = (list(reversed(array)).index(")")-(len(array)-1))*-1

            array[opening_index:closing_index+1] = [treat_formated_compute_array(array[opening_index+1:closing_index])]

            open_parenthesis = 0

    if open_parenthesis:

        raise( "Error parenthesis" )

    # converts all numbers
    for x in range(len(array)):

        if type(array[x]) == list:

            nombre = 0

            for indx in range(len(array[x])):

                nombre += array[x][indx]*10**(len(array[x])-indx-1)

            array[x] = nombre

    array = search_array_replace(array, ["."], [[-1, 2]], [convert_to_decimal])

    array = search_array_replace(array, ["sqrt"], [[0, 2]], [get_square_root])

    array = search_array_replace(array, ["(-)"], [[0, 2]], [negative_time])

    array = search_array_replace(array, ["^"], [[-1, 2]], [to_power])

    array = search_array_replace(array, ["!"], [[-1, 1]], [get_factoriel])

    array = search_array_replace(array, ["*", "/"], [[-1, 2], [-1, 2]], [multiplicate, divide])

    array = search_array_replace(array, ["+", "-"], [[-1, 2], [-1, 2]], [add, substract])

    return array
            

def search_array_replace(array, char, bornes, functions):

    in_array = 1

    while in_array:

        in_array = 0

        for character in range(len(char)):

            if char[character] in array:

                in_array = 1

                index = array.index(char[character])

                if bornes[character] == [0, 1]:

                    array[index] = functions[character](array[index])

                else:

                    array[index+bornes[character][0]:index+bornes[character][1]] = [functions[character](array[index+bornes[character][0]:index+bornes[character][1]])]

    return array


def negative_time(array):

    return array[1]*-1


def to_power(array):

    return array[0]**array[2]


def multiplicate(array):

    return array[0]*array[2]


def divide(array):

    return array[0]/array[2]


def add(array):

    return array[0]+array[2]


def substract(array):

    return array[0]-array[2]


def get_factoriel(array):

    return factoriel(array[0])


def convert_to_decimal(array):

    return array[0]+array[2]/10**(int(log(array[2], 10))+1)


def get_square_root(array):

    return sqrt(array[1])


class Calculette:

    def __init__(self):

        self.buttons = []

        self.width_button = 100

        self.height_button = 100

        self.nbr_cadre_y_add = 200

        self.operateurs = ["+", "-", "<", "/", "*", "!", "(", ")", "^", "ac", "sqrt", "="]

        self.full_operateurs = self.operateurs+[".", "0", "(-)"]

        Calculette.define_buttons(self)

        self.vitre = []

        self.pyg_vitre = Panneau("", 20, 60, 600, 120, BLACK, background=WHITE)

        self.last_calcul = [0, 0]

        Calculette.draw(self)

        self.result_screen = 0

        self.max_caracteres = 30

    def define_buttons(self):

        symboles_nbr = [".", "0", "(-)"]

        x_pad_operateur = 400

        for y in range(4):

            for x in range(3):

                if y < 3:

                    val = ((x-2)*-1+y*3-9)*-1

                else:

                    val = symboles_nbr[x]

                self.buttons.append(Panneau(str(val), x*self.width_button, y*self.height_button+self.nbr_cadre_y_add, largeur=self.width_button, hauteur=self.height_button))

        for y in range(4):

            for x in range(3):

                val = self.operateurs[y*3+x]

                self.buttons.append(Panneau(str(val), x*self.width_button+x_pad_operateur, y*self.height_button+self.nbr_cadre_y_add, largeur=self.width_button, hauteur=self.height_button))


    def update(self, mouse_pos):

        for index in range(len(self.buttons)):

            button = self.buttons[index]

            if button.clicked(mouse_pos):

                if (button.contenu in self.operateurs) and (button.contenu != "ac") and (button.contenu != "sqrt") and (button.contenu != "<") and (self.result_screen) and (self.last_calcul[1] != "Erreur"):

                  self.result_screen = 0

                  self.vitre = [self.last_calcul[1]]

                  self.last_calcul[0] = 0

                if self.result_screen:

                    self.vitre = []

                    self.result_screen = 0

                    self.last_calcul = [0, 0]

                if button.contenu == "<":

                    if self.vitre != []:

                        self.vitre.pop()

                elif button.contenu == "=":

                    Calculette.get_result(self)

                elif button.contenu == "ac":

                    self.vitre = []

                else:

                    self.vitre.append(button.contenu)

                self.pyg_vitre.contenu = "".join(self.vitre)

                if self.last_calcul[0]:

                    self.pyg_vitre.color = GREY

                else:

                    self.pyg_vitre.color = BLACK

                if len(self.pyg_vitre.contenu) > self.max_caracteres:

                    self.pyg_vitre.contenu = self.pyg_vitre.contenu[len(self.pyg_vitre.contenu)-self.max_caracteres:]

                self.pyg_vitre.draw()

                if self.last_calcul[0]:

                    if len(self.last_calcul[1]) > self.max_caracteres:

                        string = self.last_calcul[1][:self.max_caracteres-5]+"x10^"+str(len(self.last_calcul[1])-(self.max_caracteres-5))

                    else:

                        string = self.last_calcul[1]

                    aff_txt("".join(string), 40, 120, BLACK, 30)

                pygame.display.update()

    def draw(self):

        screen.fill(WHITE)

        aff_txt("Fire & Fury Corp.", 0, 0)

        aff_txt("Calculator", 500, 0)

        for bout in self.buttons:

            bout.draw()

        self.pyg_vitre.draw()

        pygame.display.update()

    def get_result(self):

        nbrs = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

        operateurs = ["+", "*", "-", "/", "^", "-", "(", ")", "(-)"]

        resultat = 0

        index = 0

        nbrs_array = [[]]

        nbr_index = 0

        compute_memory = self.vitre.copy()

        while len(self.vitre) > index:

            entity = self.vitre[index]

            if entity in nbrs:

                nbrs_array[nbr_index].append(int(entity))

                if (len(self.vitre)>index+1) and (not self.vitre[index+1] in nbrs):

                    nbr_index += 1

                    nbrs_array.append([])

            elif entity in self.full_operateurs:

                replace = 0

                if nbrs_array[-1] == []:

                    nbrs_array.pop()

                    nbr_index += 1

                    replace = 1

                nbrs_array.append(entity)

                if replace:

                    nbrs_array.append([])

            else:

                nbrs_array[nbr_index].append(int(entity))

                if (len(self.vitre)>index+1) and (not self.vitre[index+1] in nbrs):

                    nbr_index += 1

                    nbrs_array.append([])

            index += 1

        if nbrs_array[-1] == []:

            nbrs_array.pop()

        try:

            resultat = treat_formated_compute_array(nbrs_array)

        except:

            resultat = ["Erreur"]

        self.last_calcul[0], self.last_calcul[1] = 1, str(resultat[0])

        self.pyg_vitre.contenu = "".join(self.vitre)

        if len(self.pyg_vitre.contenu) > self.max_caracteres:

            self.pyg_vitre.contenu = self.pyg_vitre.contenu[len(self.pyg_vitre.contenu)-self.max_caracteres:]

        self.pyg_vitre.draw()

        pygame.display.update()

        self.result_screen = 1

def main():

    aff = 0

    calculette = Calculette()

    while aff == 0:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                aff = 1

            elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):

                mouse_pos = pygame.mouse.get_pos()

                calculette.update(mouse_pos)

        clock.tick(10)


if __name__ == "__main__":

    main()
