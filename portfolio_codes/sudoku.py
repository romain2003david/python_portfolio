# -*- coding: utf-8 -*-
"""
Created on Fri Dec 11 14:13:18 2020
@author: rdavid
"""
import random

from pig_tv import *


class Square:

    def __init__(self, x, y, size, content=None, thickness=2, fill_color=0):

        self.x = x

        self.y = y

        self.size = size

        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)

        self.content = content

        self.thickness = thickness

        self.color = BLACK

        self.fill_color = fill_color

    def draw(self):

        if self.fill_color:

            pygame.draw.rect(screen, self.fill_color, self.rect)

        else:

            pygame.draw.rect(screen, BLACK, self.rect, self.thickness)

        if self.content != None:

            facteur = 1/3

            aff_txt(self.content, self.x+int(self.size*facteur), self.y+int(self.size*facteur)-5, taille=1, font=nb_font, color=self.color)

    def in_square(self, pos):

        x, y = pos

        return self.rect.collidepoint((x, y))

    def emphasize(self):

        self.color = GREEN

        self.thickness = 6

    def unemphasize(self):

        self.color = BLACK

        self.thickness = 2

    def warn_flag(self):

        self.color = RED

        self.thickness = 6

    def player_fill(self):

        self.color = GREY

        self.thickness = 2

    def empty(self):

        self.content = None

        self.thickness = 2





class Grid:
   
    def __init__(self, size):
       
        self.size = size
       
        self.grid = [[-1 for x in range(size*size)] for y in range(size*size)]
       
        self.given_squares = []

        self.valid_grid = []

        self.grid_saved_pos = None
       
        self.possibilities = [[[v for v in range(size*size)] for x in range(size*size)] for y in range(size*size)]

        ## creating visual features

        self.margin = 5

        # left area for sudoku grid

        area_size = min(int(screen_width*2/3), screen_height)

        square_size = area_size // (self.size**2)

        self.squares = [[] for y in range(size**2)]

        for y in range(size**2):

            for x in range(size**2):

                x_cor = square_size*x

                y_cor = square_size*y

                self.squares[y].append(Square(self.margin+x_cor, self.margin+y_cor, square_size))

        # grid that's on top of the squares to emphasize the big square delimitations

        self.emphasizing_grid = []

        for y in range(size):

            for x in range(size):

                x_cor = square_size*x*size

                y_cor = square_size*y*size

                self.emphasizing_grid.append(Square(self.margin+x_cor, self.margin+y_cor, square_size*size, thickness=6))

        # number buttons

        self.interactive_buttons = []

        self.user_digit = -1

        buttons_size = (screen_height-2*self.margin)/(self.size**2)

        button_x = screen_width-buttons_size-self.margin

        for y in range(self.size**2):

            square = Square(button_x, self.margin+y*buttons_size, buttons_size, content=str(y+1))

            self.interactive_buttons.append(square)

        # option buttons

        button_size = screen_height//10

        self.del_button = Square(self.margin, screen_height-self.margin-button_size, button_size, fill_color=RED)

        ##

        ## player options

        self.error_warning = 1

        self.blunders = 0

        self.error_warning_button = Square(screen_width*(2/3), screen_height-self.margin-button_size, button_size, fill_color=PURPLE)

        ##

        # initialising a new random grid

        Grid.create_partial_grid(self)

    def get_empty_squares(self):
       
        empty_squares = []
       
        for y in range(len(self.grid)):
           
            for x in range(len(self.grid[y])):
               
                if self.grid[y][x] == -1:
                   
                    empty_squares.append([y, x])
       
        return empty_squares
               
    def create_partial_grid(self):

        print("\nGeneration du Sudoku ! \n")

        empty_squares = Grid.get_empty_squares(self)  # [[0, 0]]
       
        while empty_squares != []:

            erreur = Grid.fill_square(self, empty_squares)

            empty_squares = Grid.get_empty_squares(self)

            if erreur == 1:  # invalid grid, preparing to reset grid

                empty_squares = []

        if erreur == 1:

            Grid.__init__(self, self.size)

        else:

            print("\nSudoku genere ! \n")
   
    def fill_square(self, empty_squares):
       
        new_square = random.choice(empty_squares)
       
        y_cor, x_cor = new_square

##        print(new_square, self.possibilities[y_cor][x_cor], self.grid[y_cor][x_cor])
##        print()
##
##        for x in self.possibilities:
##
##            print(*x)

        if self.possibilities[y_cor][x_cor] == []:

            print("Erreur : Sudoku invalide ...")

            return 1

        else:

            new_value = random.choice(self.possibilities[y_cor][x_cor])

            Grid.add_square(self, y_cor, x_cor, new_value)

    def update_possibilities(self, y_cor, x_cor, new_value):
        # deletes poss of newly occupied square

        self.possibilities[y_cor][x_cor] = []

        # dels poss in given col
       
        for delta_y in range(self.size*self.size):

            if y_cor != delta_y:
           
                if (self.possibilities[delta_y][x_cor] == []) and (self.grid[delta_y][x_cor] == new_value):

                    if error_display:
                   
                        print("Erreur : valeur interdite affectee (1)")
           
                elif new_value in self.possibilities[delta_y][x_cor]:
                   
                    self.possibilities[delta_y][x_cor].remove(new_value)
        
        # dels poss in given row
       
        for delta_x in range(self.size*self.size):

            if x_cor != delta_x:

                if (self.possibilities[y_cor][delta_x] == []) and (self.grid[y_cor][delta_x] == new_value):

                    if error_display:
                   
                        print("Erreur : valeur interdite affectee (2) ; row: {}, pos {}".format(y_cor, delta_x))
           
                elif new_value in self.possibilities[y_cor][delta_x]:
                   
                    self.possibilities[y_cor][delta_x].remove(new_value)
           
        # dels poss in big square
       
        big_square_pos_x = x_cor//self.size
       
        big_square_pos_y = y_cor//self.size
       
        for delta_x in range(size):
           
            for delta_y in range(self.size):

                pos_x, pos_y = big_square_pos_x*self.size+delta_x, big_square_pos_y*self.size+delta_y

                if (pos_x != x_cor) or (pos_y != y_cor):
                   
                    if (self.possibilities[pos_y][pos_x] == []) and (self.grid[pos_y][pos_x] == new_value):

                        if error_display:
                   
                            print("Erreur : valeur interdite affectee (3) ; gros carre {} {}, pos : {} {}".format(big_square_pos_x, big_square_pos_y, pos_x, pos_y))
           
                    elif new_value in self.possibilities[pos_y][pos_x]:
                   
                        self.possibilities[pos_y][pos_x].remove(new_value)

    def get_free_row_nb(self, y_cor):

        nbs = [n for n in range(len(self.grid[y_cor]))]

        for x in range(len(self.grid[y_cor])):

            if self.grid[y_cor][x] != -1:

                nbs.remove(self.grid[y_cor][x])

        return nbs

    def get_free_col_nb(self, x_cor):

        nbs = [n for n in range(len(self.grid))]

        for y in range(len(self.grid)):

            if self.grid[y][x_cor] != -1:

                nbs.remove(self.grid[y][x_cor])

        return nbs

    def get_free_big_square_nb(self, y_cor, x_cor):

        nbs = [n for n in range(len(self.grid))]

        for y in range(size):

            for x in range(size):

                if self.grid[y+y_cor][x+x_cor] != -1:

                    nbs.remove(self.grid[y+y_cor][x+x_cor])

        return nbs 

    def check_have_to(self):

        test = 0

        if not test:
       
            for y in range(len(self.possibilities)):
               
                for x in range(len(self.possibilities[y])):
                   
                    if len(self.possibilities[y][x]) == 1:

                        #print("added through", 0)

                        Grid.add_square(self, y, x, self.possibilities[y][x][0], auto_add=1)

                        return

        ## checks if a number has only one spot left in a body

        ## checks in rows

        if not test:

            for y in range(len(self.grid)):

                free_nbs = Grid.get_free_row_nb(self, y)

                for nb in free_nbs:

                    available_spots = []

                    for x in range(len(self.grid[y])):

                        if nb in self.possibilities[y][x]:

                            available_spots.append(x)

                    if len(available_spots) == 0:

                        if error_display:

                            print("ERREUR! Nombre non affecte n'a plus de place ... valeur = {}, ligne = {}".format(nb, y))

                    elif len(available_spots) == 1:  # find the sole place for this number

                        #print("added through", 1)

                        Grid.add_square(self, y, available_spots[0], nb, auto_add=1)

                        return

        ## checks in cols

        if not test == 2:

            for x in range(len(self.grid[0])):

                free_nbs = Grid.get_free_col_nb(self, x)

                for nb in free_nbs:

                    available_spots = []

                    for y in range(len(self.grid)):

                        if nb in self.possibilities[y][x]:

                            available_spots.append(y)

                    if len(available_spots) == 0:

                        if error_display:

                            print("ERREUR! Nombre non affecte n'a plus de place ... valeur = {}, colonne = {}".format(nb, x))

                    elif len(available_spots) == 1:  # find the sole place for this number

                        #print("added through", 2)

                        Grid.add_square(self, available_spots[0], x, nb, auto_add=1)

                        return

        ## checks in big squares

        if not test == 3:

            for x in range(size):

                for y in range(size):

                    big_x_cor = x*size

                    big_y_cor = y*size

                    free_nbs = Grid.get_free_big_square_nb(self, big_y_cor, big_x_cor)

                for nb in free_nbs:

                    available_spots = []

                    for delta_y in range(size):

                        for delta_x in range(size):

                            if nb in self.possibilities[big_y_cor+delta_y][big_x_cor+delta_x]:

                                available_spots.append([big_y_cor+delta_y, big_x_cor+delta_x])

                    if len(available_spots) == 0:

                        if error_display:

                            print("ERREUR! Nombre non affecte n'a plus de place ... valeur = {}, grand carre = {}".format(nb, [x, y]))

                    elif len(available_spots) == 1:  # find the sole place for this number

                        #print("added through", 3)

                        Grid.add_square(self, available_spots[0][0], available_spots[0][1], nb, auto_add=1)

                        return

    def add_square(self, y_cor, x_cor, value, auto_add=0):

        self.grid[y_cor][x_cor] = value

        self.squares[y_cor][x_cor].content = str(value+1)  # +1

        if auto_add:

            self.squares[y_cor][x_cor].color = GREEN

        else:
       
            self.given_squares.append([y_cor, x_cor])
       
        Grid.update_possibilities(self, y_cor, x_cor, value)

##        print()
##
##        for x in self.possibilities:
##
##            print(*x)
##
##        Grid.update(self)
##
##        pygame.display.update()

        #clock.tick(10)

        #wait()

        Grid.check_have_to(self)

    def draw(self, interactive=1, clicked=0):

        temp_var = 0

        won = 0

        if clicked:

            self.interactive_buttons[self.user_digit].unemphasize()

        screen.fill(WHITE)

        if interactive:

            mouse_pos = pygame.mouse.get_pos()

        for y_pos in range(len(self.squares)):

            for x_pos in range(len(self.squares)):

                square = self.squares[y_pos][x_pos]

                square.draw()

                if interactive:

                    if clicked and square.in_square(mouse_pos):

                        if (self.user_digit != -1) and (square.content == None):

                            won = Grid.player_add(self, y_pos, x_pos)

                        else:  # not empty square

                            if self.squares[y_pos][x_pos].color != BLACK:  # can't erase the default squares

                                self.grid_saved_pos = [x_pos, y_pos]

                                temp_var = 1

        for square in self.emphasizing_grid:

            square.draw()

        if interactive:

            if self.error_warning:

                aff_txt("Blunders : {}".format(self.blunders), self.margin, screen_height-120)

            for indx in range(len(self.interactive_buttons)):

                square = self.interactive_buttons[indx]

                square.draw()

                # checks if user has clicked on a digit to place in grid

                if clicked and square.in_square(mouse_pos):  # user has chosen a digit

                    self.user_digit = indx

                    self.interactive_buttons[self.user_digit].emphasize()

            self.error_warning_button.draw()

            if clicked:

                if self.error_warning_button.in_square(mouse_pos):  # user wants to change help on burdens options

                    if self.error_warning == 1:

                        self.error_warning = 0

                        for row in self.squares:

                            for square in row:

                                if square.color == RED:

                                    square.player_fill()

                    else:

                        self.error_warning = 1

                        Grid.check_for_burdens(self)

            if self.grid_saved_pos != None:

                self.del_button.draw()

                if clicked:

                    if self.del_button.in_square(mouse_pos):  # user wants to delete a square he's filled

                        x, y = self.grid_saved_pos

                        self.squares[y][x].empty()

                        self.grid[y][x] = -1

                        self.grid_saved_pos = None

                    elif not temp_var:

                        self.grid_saved_pos = None

        return won

    def check_for_burdens(self):

        for y in range(len(self.grid)):

            for x in range(len(self.grid[y])):

                if (self.grid[y][x] != self.valid_grid[y][x]) and (self.grid[y][x] != -1):

                   self.squares[y][x].warn_flag()

    def player_add(self, y_pos, x_pos):

        self.grid[y_pos][x_pos] = self.user_digit

        self.squares[y_pos][x_pos].content = str(self.grid[y_pos][x_pos]+1)

        self.squares[y_pos][x_pos].player_fill()

        if self.grid[y_pos][x_pos] != self.valid_grid[y_pos][x_pos]:  # player's a fool

            self.blunders += 1

            if self.error_warning:

                self.squares[y_pos][x_pos].warn_flag()

        if Grid.full(self):

            if Grid.correct(self):

                Grid.player_won(self)

                return 1

    def full(self):

        for row in self.grid:

            for square in row:

                if square == -1:

                    return False

        return True

    def correct(self):

        for y in range(len(self.grid)):

            for x in range(len(self.grid[y])):

                if self.grid[y][x] != self.valid_grid[y][x]:

                    return False

        return True

    def player_won(self):

        for y in range(len(self.grid)):

            for x in range(len(self.grid[y])):

                self.squares[y][x].unemphasize()

        Grid.draw(self, 0, 0)

        aff_txt("Blunders : {}".format(self.blunders), self.margin, screen_height-120)

        aff_txt("Well Done !", self.margin, screen_height-70, color=YELLOW)

        pygame.display.update()

        wait()

    def modify_grid(self):

        self.valid_grid = self.grid.copy()

        self.grid = [[-1 for x in range(size*size)] for y in range(size*size)]

        for row in self.squares:

            for square in row:

                square.content = None

                square.color = BLACK

        for coor in self.given_squares:

            y, x = coor

            self.grid[y][x] = self.valid_grid[y][x]

            self.squares[y][x].content = str(self.valid_grid[y][x]+1)

            


def main(size):

    keep_playin = 1

    while keep_playin:

        grid = Grid(size)

        play = True

        clicked = 0

        clicking = 0

        game_mode = 2#int(input("Game mode:\n1) Generer grille completee\n2) Jouer au Sudoku\n"))

        options = [0, 0]  # options for player : display digits in grid, display errors

        if game_mode == 1:

            grid.update(interactive=0)

            pygame.display.update()

            wait()

        else:

            grid.modify_grid()

            while play:

                clicked = 0

                for event in pygame.event.get():

                    if event.type == pygame.QUIT:

                        play = False

                    elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):

                        clicking = 1

                        clicked = 1

                    elif (event.type == pygame.MOUSEBUTTONUP) and (event.button == 1):

                        clicking = 0

                    elif (event.type == pygame.MOUSEMOTION):

                        translation = event.rel

                    elif event.type == pygame.KEYDOWN:

                        if event.key == pygame.K_LEFT:

                            pass

                won = grid.draw(clicked=clicked)

                if won:

                    play = False

                pygame.display.update()

                clock.tick(60)

        keep_playin = int(input("Keep playing ?\n0 to quit, else type number\n"))


if __name__ == "__main__":

    error_display = 0

    size = 3  #  int(input("Grid size (classical mode = 3)\n"))

    if size == 2:

        nb_font = pygame.font.SysFont("monospace", 60, True)

    elif size == 3:

        nb_font = pygame.font.SysFont("monospace", 40, True)

    else:

        nb_font = pygame.font.SysFont("monospace", 30, True)

   
    main(size)
