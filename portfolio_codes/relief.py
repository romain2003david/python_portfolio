from pig_tv import *

class Grid:

    def __init__(self, rows, cols, basic_fill, growing_rate, draw_lines):

        self.rows = rows

        self.columns = cols

        self.grid_contents = [[basic_fill for x in range(self.columns)] for x in range(self.rows)]

        self.mountain = [random.randint(0, self.rows-1), random.randint(0, self.rows-1)]

        self.growing_rate = growing_rate

        self.deplacement = self.rows // 10

        self.cote = (screen_height // self.rows) or 1  # shoud never be zero

        self.draw_lines = draw_lines

    def update(self, graphic):

        print_active = 0

        if print_active:

            print("loading update")


        if graphic:

            Grid.draw(self)

            if print_active:

                print("Drawing done")

        else:

            active_print_grid = 1

            if active_print_grid:

                Grid.print_grid(self)

        n_grid = self.grid_contents.copy()

        for y in range(self.rows):

            for x in range(self.columns):

                if random.randint(0, 3) == 0:

                    n_grid = Grid.update_case(self, x, y, n_grid)

        self.grid_contents = n_grid

        Grid.move_mountain(self)

        if print_active:

            print("Maths done")


            print("loading finished")

    def print_grid(self):

        for x in self.grid_contents:

            print(*x)

    def move_mountain(self):

        last_mountain = self.mountain.copy()

        self.mountain[0] += random.randint(-self.deplacement, self.deplacement)

        self.mountain[1] += random.randint(-self.deplacement, self.deplacement)

        for x in range(len(self.mountain)):

            if self.mountain[x] < 0:

                self.mountain[x] = 0

            elif self.mountain[x] > self.rows-1:

                self.mountain[x] = self.rows-1

        self.grid_contents[self.mountain[1]][self.mountain[0]], self.grid_contents[last_mountain[1]][last_mountain[0]] = self.grid_contents[last_mountain[1]][last_mountain[0]], self.grid_contents[self.mountain[1]][self.mountain[0]]


    def update_case(self, x, y, n_grid):

        content = self.grid_contents[y][x]

        if content > self.growing_rate:

            slide_vector = round_list([(self.mountain[0]-x)/2, (self.mountain[1]-y)/2])#get_sign_of_array(round_list([self.mountain[0]-x, self.mountain[1]-y]))

            if (self.draw_lines) and (random.randint(0, 400//self.cote) == 0):

                pygame.draw.line(screen, RED, (x*self.cote, y*self.cote), ((x+slide_vector[0])*self.cote, (y+slide_vector[1])*self.cote))

                pygame.draw.line(screen, GREEN, ((x+slide_vector[0])*self.cote, (y+slide_vector[1])*self.cote), ((x+slide_vector[0]*2)*self.cote, (y+slide_vector[1]*2)*self.cote))

            n_grid[y][x] -= self.growing_rate

            n_grid[y+slide_vector[1]][x+slide_vector[0]] += self.growing_rate

            if n_grid[y+slide_vector[1]][x+slide_vector[0]] > 255:

                n_grid = Grid.dispatch(self, y+slide_vector[1], x+slide_vector[0], n_grid)

        return n_grid

    def dispatch(self, y, x, grid):

        to_take_out = self.grid_contents[y][x]-255

        liste_x = [-1, 0, 1]

        liste_y = [-1, 0, 1]

        if (x == 0):

            liste_x = [0, 1]

        elif (x == self.rows-1):

            liste_x = [-1, 0]

        if (y == 0):

            liste_y = [0, 1]

        elif (y == self.rows-1):

            liste_y = [-1, 0]

        nbr_neighbor = len(liste_x)*len(liste_y) - 1

        #print("dispatched", to_take_out, nbr_neighbor)

        for y_ in liste_y:

            for x_ in liste_x:

                if (x_ or y_):

                    if not out_screen(x_+x, y_+y, self.columns, self.rows):

                        grid[y_+y][x_+x] += to_take_out/nbr_neighbor

                        if grid[y_+y][x_+x] > 255:

                            sys_ferme = 0

                            if sys_ferme:

                                ind_x = random.randint(0, self.rows-1)

                                ind_y = random.randint(0, self.rows-1)

                                grid[ind_x][ind_y] += grid[y_+y][x_+x]-255

                                if grid[ind_x][ind_y] > 255:

                                    grid = Grid.dispatch(self, ind_x, ind_y, grid)

                            grid[y_+y][x_+x] = 255


        grid[y][x] = 255

        return grid

    def draw(self):

        for y in range(self.rows):

            for x in range(self.columns):

                teinte_grise = (self.grid_contents[y][x]-255) *-1#self.grid_contents[y][x]#

                color = [teinte_grise, teinte_grise, teinte_grise]#[127, 127, 127]

                #index = random.randint(0, 2)

                #color[index] = teinte_grise

                try:

                    pygame.draw.rect(screen, color, pygame.Rect(x*self.cote, y*self.cote, self.cote, self.cote))  #screen.set_at((x, y), (teinte_grise, teinte_grise, teinte_grise))

                except:

                    print(teinte_grise)
                    Grid.print_grid(self)

        pygame.draw.rect(screen, RED, pygame.Rect(0, 0, self.cote*self.rows, self.cote*self.rows), 3)

        pygame.draw.rect(screen, (255, teinte_grise, teinte_grise), pygame.Rect(self.mountain[0]*self.cote, self.mountain[1]*self.cote, self.cote, self.cote))


def main(inputs):

    rows, cols, basic_fill, growing_rate, draw_lines = inputs

    grid = Grid(rows, cols, basic_fill, growing_rate, draw_lines)

    play = True

    graphic = 1

    grid.update(graphic)

    while play:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                play = False

            elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):

                mouse_pos = pygame.mouse.get_pos()

                grid.update(graphic)

            elif (event.type == pygame.MOUSEMOTION):

                translation = event.rel

        grid.update(graphic)

        pygame.display.update()

        clock.tick(60)


if __name__ == "__main__":

    inputs = [100, 100, 127, 10, 0]

    main(inputs)
