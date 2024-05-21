from neural_network2 import Matrix

from pig_tv import *

from fractions import Fraction as frac



def get_nbr(string):

    print(string, "\n")

    choice = input()

    try:

        return int(choice)

    except ValueError:

        return get_nbr(string)


def nbr_input(string):

    print(string)

    print("type a number, or f if u wanna enter a fraction")

    choice = input()

    if choice == "f":

        num = get_nbr("numerateur:")

        deno = get_nbr("denominateur:")

        return frac(num, deno)

    else:

        try:

            return int(choice)

        except ValueError:

            return nbr_input(string)


class VisMatrix:

    def __init__(self, rows, cols):

        self.rows = rows

        self.cols = cols

        self.matrix = Matrix(rows, cols, randomize=3)

        self.stored_line = None

        VisMatrix.init_grid(self)

    def init_grid(self):

        x_margin = 100

        y_margin = 80

        tile_width = (screen_width-x_margin)//self.cols

        tile_height = (screen_height-y_margin)//self.rows

        self.grid = [[Panneau(str(self.matrix.content[y][x]), x_margin+tile_width*x, y_margin+tile_height*y, largeur=tile_width, hauteur=tile_height, color=BLACK, background=WHITE) for x in range(self.cols)] for y in range(self.rows)]

    def modify_content(self, n_content):

        if n_content == "Id":

            self.matrix = Matrix(self.rows, self.cols, spe_type="Id")

        elif n_content == "Spe":

            self.matrix.content =  [[2, 4, 3], [0, 1, 1], [2, 2, -1]]  # [[1, 0, -1], [0, 2, 1], [1, 1, 0]] # [[1, 2, 1], [4, 0, -1], [-1, 2, 2]]  # 

        else:

            self.matrix.content = n_content

        VisMatrix.init_grid(self)

    def update(self, clicked, active_mouse):

        to_return = None

        if clicked:

            clicked_coors = None

            mouse_pos = pygame.mouse.get_pos()

            for y in range(len(self.grid)):

                for x in range(len(self.grid[y])):

                    if self.grid[y][x].clicked(mouse_pos):

                        clicked_coors = [y, x]

            if clicked_coors:

                y, x = clicked_coors

                if active_mouse[1] == 1:

                    factor = nbr_input("factor:\n")

                    self.matrix.multiply_line(y, factor)

                    VisMatrix.init_grid(self)

                    to_return = [1, y, factor]

                elif active_mouse[0] == 1:

                    if self.stored_line == None:

                        self.stored_line = y

                    else:

                        self.matrix.switch_lines(self.stored_line, y)

                        VisMatrix.init_grid(self)

                        to_return = [2, self.stored_line, y]

                        self.stored_line = None

                elif active_mouse[2] == 1:

                    if self.stored_line == None:

                        self.stored_line = y

                    else:

                        factor = nbr_input("factor:\n")

                        self.matrix.add_multiply_lines(self.stored_line, y, factor)

                        VisMatrix.init_grid(self)

                        to_return = [3, self.stored_line, y, factor]

                        self.stored_line = None

                else:

                    self.matrix.content[y][x] = nbr_input("new value:\n")

                    VisMatrix.init_grid(self)

        VisMatrix.draw(self)

        return to_return

    def draw(self):

        for line in self.grid:

            for tile in line:

                tile.draw()


def main():

    play = True

    clicking = 0

    rows, cols = 3, 3

    matri = VisMatrix(rows, cols)

    #matri.modify_content("Spe")

    result_matrix = VisMatrix(rows, cols)

    result_matrix.modify_content("Id")

    switch_button = Panneau("swi", 0, 0, 100, 100)

    multiply_button = Panneau("pro", 0, 100, 100, 100)

    add_multiply_button = Panneau("add", 0, 200, 100, 100)

    active_mouse = [0, 0, 0]

    buttons = [switch_button, multiply_button, add_multiply_button]

    result_button = Panneau("see", 0, 500, 100, 100, RED)

    while play:

        clicked = 0

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                play = False

            elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):

                clicking = 1

                clicked = 1

                mouse_pos = pygame.mouse.get_pos()

                if switch_button.clicked(mouse_pos):

                    active_mouse = [1, 0, 0]

                elif multiply_button.clicked(mouse_pos):

                    active_mouse = [0, 1, 0]

                elif add_multiply_button.clicked(mouse_pos):

                    active_mouse = [0, 0, 1]

                elif result_button.clicked(mouse_pos):

                    result_matrix.draw()

                    pygame.display.update()

                    wait()

                for x in range(len(buttons)):

                    if active_mouse[x]:

                        buttons[x].color = GREEN

                    else:

                        buttons[x].color = WHITE

            elif (event.type == pygame.MOUSEBUTTONUP) and (event.button == 1):

                clicking = 0

            elif (event.type == pygame.MOUSEMOTION):

                translation = event.rel

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_LEFT:

                    pass

        screen.fill(WHITE)

        switch_button.draw()

        multiply_button.draw()

        add_multiply_button.draw()

        result_button.draw()

        acted = matri.update(clicked, active_mouse)

        if acted != None:

            if acted[0] == 1:

                result_matrix.matrix.multiply_line(acted[1], acted[2])

                result_matrix.init_grid()

            if acted[0] == 2:

                result_matrix.matrix.switch_lines(acted[1], acted[2])

                result_matrix.init_grid()

            if acted[0] == 3:

                result_matrix.matrix.add_multiply_lines(acted[1], acted[2], acted[3])

                result_matrix.init_grid()

        pygame.display.update()

        clock.tick(60)


if __name__ == "__main__":

    main()
