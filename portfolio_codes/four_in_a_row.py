from pig_tv import *


def draw_fleche(x, y, add):

    x += add[0]

    y += add[1]

    width = 25

    height = 15

    rect1 = pygame.Rect(x, y, width, height)

    pygame.draw.rect(screen, GREEN, rect1)

    pygame.draw.polygon(screen, GREEN, ((x-5, y+height), (x+5+width, y+height), (x+width//2, y+height*2.5), (x-5, y+height)))



def aff_circles(winning_coors, grid):

    #winning_coors.reverse()#print(winning_coors)

    vecteur = winning_coors[1]

    actual_coor = winning_coors[0][1]

    while actual_coor != winning_coors[0][0]:

        pygame.draw.circle(screen, PURPLE, (actual_coor[0]*grid.square_size + grid.bordure_x+grid.square_size//2, actual_coor[1]*grid.square_size + grid.bordure_y+grid.square_size//2), grid.square_size//2)

        actual_coor[0] += vecteur[0]

        actual_coor[1] += vecteur[1]

    pygame.draw.circle(screen, PURPLE, (actual_coor[0]*grid.square_size + grid.bordure_x+grid.square_size//2, actual_coor[1]*grid.square_size + grid.bordure_y+grid.square_size//2), grid.square_size//2)


def aff_rect(winning_coors, grid):

    winning_coors.reverse()

    print(winning_coors)

    win_cor1 = winning_coors[0]

    win_cor2 = winning_coors[1]

    if win_cor1[0] == win_cor2[0]:

        x_pos = grid.bordure_x + win_cor1[0]*grid.square_size

        width = grid.square_size

        y_pos = grid.bordure_y + win_cor1[1]*grid.square_size

        height = grid.bordure_y + win_cor2[1]*grid.square_size - y_pos + grid.square_size

        pyg_rect = pygame.Rect(x_pos, y_pos, width, height)

        pygame.draw.rect(screen, PURPLE, pyg_rect, 5)

    elif win_cor1[1] == win_cor2[1]:

        y_pos = grid.bordure_y + win_cor1[1]*grid.square_size

        height = grid.square_size

        x_pos = grid.bordure_x + win_cor1[0]*grid.square_size

        width = grid.bordure_x + win_cor2[0]*grid.square_size - x_pos + grid.square_size

        pyg_rect = pygame.Rect(x_pos, y_pos, width, height)

        pygame.draw.rect(screen, PURPLE, pyg_rect, 5)        

    else:

        pos1 = [grid.bordure_x + winning_coors[0][0]*grid.square_size, grid.bordure_y + winning_coors[0][1]*grid.square_size + grid.square_size//2]

        pos2 = [grid.bordure_x + winning_coors[1][0]*grid.square_size + grid.square_size//2, grid.bordure_y + winning_coors[1][1]*grid.square_size]

        pos3 = [grid.bordure_x + winning_coors[1][0]*grid.square_size + grid.square_size//2, grid.bordure_y + winning_coors[1][1]*grid.square_size + grid.square_size//2]

        pos4 = [grid.bordure_x + winning_coors[0][0]*grid.square_size + grid.square_size//2, grid.bordure_y + winning_coors[0][1]*grid.square_size + grid.square_size//2]

        pygame.draw.polygon(screen, PURPLE, (pos1, pos2, pos3, pos4, pos1), 4)


class Grid:

    def __init__(self, rows=7, column=7, x_inrow=4, graphic=1):

        if graphic:

            self.bordure_y = 100

            self.place = screen_height-self.bordure_y

            self.square_size = self.place//rows

            self.bordure_x = (screen_width-self.square_size*column)//2

        self.rows = rows

        self.column = column

        self.grid_content = [[0 for x in range(self.column)] for x in range(self.rows)]

        self.x_inrow = x_inrow

    def print_grid(self):

        for row in self.grid_content:

            for lettre in row:

                if lettre == -1:

                    print("#", end=" ")

                else:

                    print(lettre, end=" ")

            print()

        print("\n")

    def update(self, case_index, color, graphic):

        full = Grid.append_case(self, case_index, color)

        if graphic:

            Grid.draw(self)

        return full

    def append_case(self, case_index, color):

        liste = []

        if color == 0:

            color = -1

        for x in self.grid_content:

            liste.append(x[case_index])

        new_index = len(liste)-1

        while liste[new_index] != 0:

            new_index -= 1

        self.grid_content[new_index][case_index] = color

        if new_index == 0:

            return True

    def draw(self):

        screen.fill(BROWN)

        for y in range(self.rows):

            for x in range(self.column):

                x_pos = self.bordure_x+x*self.square_size

                y_pos = self.square_size*y+self.bordure_y

                pyg_square = pygame.Rect(x_pos, y_pos, self.square_size, self.square_size)

                pygame.draw.rect(screen, GREY, pyg_square, 4)

                if self.grid_content[y][x] == 1:

                    pygame.draw.circle(screen, RED, (x_pos+self.square_size//2, y_pos+self.square_size//2), self.square_size//2)

                elif self.grid_content[y][x] == -1:

                    pygame.draw.circle(screen, YELLOW, (x_pos+self.square_size//2, y_pos+self.square_size//2), self.square_size//2)

    def is_over(self, color):

        if color == 0:

            color = -1

        for row in range(len(self.grid_content)):

            for col in range(len(self.grid_content[row])):

                if self.grid_content[row][col] == color:

                    winning_coors = Grid.four_inrow(self, row, col)

                    if winning_coors:

                        return winning_coors

    def in_grid(self, y, x):

        if (0 <= y < self.rows) and (0 <= x < self.column):

            return True

    def four_inrow(self, row, col):

        color = self.grid_content[row][col]

        directions = [[1, 0], [0, 1], [1, 1], [-1, 1]]

        sens = [1, -1]

        for x, y in directions:

            in_row = 1

            winning_coors = []

            for s in sens:

                temp_y = row+y*s

                temp_x = col+x*s

                while (Grid.in_grid(self, temp_y, temp_x)) and (self.grid_content[temp_y][temp_x] == color):

                    in_row += 1

                    temp_x += x*s

                    temp_y += y*s

                winning_coors.append([temp_x-x*s, temp_y-y*s])

            if in_row >= self.x_inrow:

                return [winning_coors, [x, y]]

def game_loop(x_inrow):

    graphic = 1

    if x_inrow == 5:

        grid = Grid(9, 9, 5)

        x_coor_fleche = 15

    else:

        grid = Grid()

        x_coor_fleche = 24

    play = True

    available_panneaux = [Panneau("", grid.bordure_x+x*grid.square_size, 0, grid.square_size, grid.bordure_y, GREEN, image=draw_fleche, image_coors=[x_coor_fleche, 30], index=x) for x in range(grid.column)]

    clickable_panneaux = [Panneau("", grid.bordure_x+x*grid.square_size, 0, grid.square_size, screen_height, index=x) for x in range(grid.column)]

    grid.draw()

    for pann in available_panneaux:

        pann.draw()

    pygame.display.update()

    compteur = 0

    while play:

        for event in pygame.event.get():

            # return to menu

            if event.type == pygame.QUIT:

                play = False

            # player click

            elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):

                mouse_pos = pygame.mouse.get_pos()

                # checks if the player has clicked in a zone where he could place a coin

                for click_panneau in clickable_panneaux:

                    panneau = available_panneaux[clickable_panneaux.index(click_panneau)]

                    # une zone a ete cliquee

                    if click_panneau.clicked(mouse_pos):

                        compteur += 1  # game moves forward

                        delete_pann = grid.update(panneau.index, compteur%2, graphic)

                        if delete_pann:

                            available_panneaux.remove(panneau)

                            pygame.display.update()

                        for pann in available_panneaux:

                            pann.draw()

                        pygame.display.update()

                        winning_coors = grid.is_over(compteur%2)

                        if winning_coors:

                            play = False

    aff_circles(winning_coors, grid)  # aff_rect(winning_coors, grid)

    pygame.display.update()

    wait()

    end_game(compteur)



def wait():

    click = 0

    while not click:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                click = 1

            elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):

                click = 1


def end_game(compteur):

    if (compteur % 2) == 1:

        gagnant = " Rouges "

    else:

        gagnant = " Jaunes "

    screen.fill(WHITE)

    aff_txt("Les"+gagnant+"ont gagné !", 100, 300, taille=50)

    pygame.display.update()

    wait()


def go_settings():

    four_button = Panneau("Four in a Row !", 200, 300, 400, 100, RED)

    five_button = Panneau("Five in a Row !", 200, 450, 400, 100, PURPLE)

    choix = 0

    while choix == 0:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                choix = 1

            elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):

                mouse_pos = pygame.mouse.get_pos()

                if four_button.clicked(mouse_pos):

                    return 4

                elif five_button.clicked(mouse_pos):

                    return 5

        screen.fill(BROWN)

        four_button.draw()

        five_button.draw()

        aff_txt("Fire & Fury Corp.", 250, 100)

        aff_txt("Four in a Row !", 200, 200, taille=50)

        pygame.display.update()

        clock.tick(10)


def main():

    settings_button = Panneau("Settings", 150, 350, 200, 100, YELLOW)

    play_button = Panneau("Play !", 400, 350, 150, 100, BLUE)

    exit_button = Panneau("Exit..", 300, 475, 150, 100, RED)

    x_in_a_row = 4

    choix = 0

    while choix == 0:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                choix = 1

            elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):

                mouse_pos = pygame.mouse.get_pos()

                if settings_button.clicked(mouse_pos):

                    choix_settings = go_settings()

                    if choix_settings:

                        x_in_a_row = choix_settings

                elif play_button.clicked(mouse_pos):

                    game_loop(x_in_a_row)

                elif exit_button.clicked(mouse_pos):

                    choix = 1

        screen.fill(BROWN)

        settings_button.draw()

        play_button.draw()

        exit_button.draw()

        aff_txt("Fire & Fury Corp.", 250, 100)

        aff_txt("Four in a Row !", 200, 200, taille=50)

        pygame.display.update()

        clock.tick(10)

if __name__ == "__main__":

    main()

