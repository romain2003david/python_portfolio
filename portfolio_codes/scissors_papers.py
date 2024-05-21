from pig_tv import *


class Grid:

    def __init__(self):

        self.max_lifes = 4

        self.width = screen_width

        self.height = screen_height

        self.grid = [[0 for x in range(self.width)] for y in range(self.height)]

        self.square_width = min(screen_width//self.width, screen_height//self.height)

        self.color_dict = {0:RED,
                           1:GREEN,
                           2:BLUE}

    def update(self, clicking, graphic, chosen_color_index):

        if clicking:

            mouse_pos = pygame.mouse.get_pos()

            try:

                self.grid[mouse_pos[1]//self.square_width][mouse_pos[0]//self.square_width] = [chosen_color_index, self.max_lifes]

            except IndexError:

                pass

        Grid.update_grid(self)

        if graphic:

            Grid.draw(self)

    def update_grid(self):

        n_grid = self.grid.copy()

        for y in range(self.height):

            for x in range(self.width):

                pixel = self.grid[y][x]

                #n_grid[y][x] = pixel

                if (type(pixel) == list):

                    # serching for neighbor pixel

                    rand_list = []

                    for delta_x in [-1, 0, 1]:

                        for delta_y in [-1, 0, 1]:

                            if (delta_x or delta_y) and (not out_screen(x+delta_x, y+delta_y, self.width-1, self.height-1)):  # new pixel in screen and not pixel itself

                                n_pixel = n_grid[y+delta_y][x+delta_x]

                                if type(n_pixel) == list:
##
##                                    if (n_pixel[0] == pixel[0]) and (pixel[1]-1 > n_pixel[1]):  # new one is of same color and has less lifes
##
##                                        rand_list.append([y+delta_y, x+delta_x, 0])

                                    if (n_pixel[0]+1)%3 == pixel[0]:

                                        rand_list.append([y+delta_y, x+delta_x, 1])

                                elif (pixel[1] > 1):

                                    rand_list.append([y+delta_y, x+delta_x, 0])

                    if rand_list:

                        # chosing neighbor
                        neighbor = random.choice(rand_list)

                        # new pixel becomes of same color with one life less
                        n_grid[neighbor[0]][neighbor[1]] = n_grid[y][x].copy()

                        if neighbor[2]:

                            n_grid[neighbor[0]][neighbor[1]][1] = self.max_lifes

                        else:

                            n_grid[neighbor[0]][neighbor[1]][1] -= 1

        self.grid = n_grid

    def draw(self):

        for y in range(self.height):

            for x in range(self.width):

                pixel = self.grid[y][x]

                if type(pixel) == list:

                    color = self.color_dict[pixel[0]]

                else:

                    color = WHITE

                x_coor = x*self.square_width

                y_coor = y*self.square_width

                rect = pygame.Rect(x_coor, y_coor, self.square_width, self.square_width)

                pygame.draw.rect(screen, color, rect)


def main():

    play = True

    grid = Grid()

    clicking = 0

    graphic = 1

    chosen_color_index = 0

    button_size = 50

    red_panneau = Panneau("", screen_width-button_size, 0, button_size, button_size, color=RED)

    green_panneau = Panneau("", screen_width-button_size, button_size, button_size, button_size, color=GREEN)

    blue_panneau = Panneau("", screen_width-button_size, 2*button_size, button_size, button_size, color=BLUE)

    color_buttons = [red_panneau, green_panneau, blue_panneau]

    while play:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                play = False

            elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):

                mouse_pos = pygame.mouse.get_pos()

                clicking = 1

                for button in color_buttons:

                    if button.clicked(mouse_pos):

                        chosen_color_index = color_buttons.index(button)

                #print(clock.get_fps())

            elif (event.type == pygame.MOUSEBUTTONUP) and (event.button == 1):

                mouse_pos = pygame.mouse.get_pos()

                clicking = 0

            elif (event.type == pygame.MOUSEMOTION):

                translation = event.rel

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_LEFT:

                    pass

        grid.update(clicking, graphic, chosen_color_index)

        for button in color_buttons:

            button.draw()

        pygame.display.update()

        clock.tick(60)    

if __name__ == "__main__":

    main()
