from pig_tv import *


def init_grid(index, grid, rows, cols, sand_pile_height):

    if index >= 1:

        grid[rows//2+10][cols//2] = sand_pile_height

        grid[rows//2][cols//2+10] = sand_pile_height

    if index >= 2:

        grid[rows//2-10][cols//2] = sand_pile_height

        grid[rows//2][cols//2-10] = sand_pile_height

    if index >= 3:

        grid[rows//2][cols//4*3] = sand_pile_height

        grid[rows//4*3][cols//2] = sand_pile_height

    if index >= 4:

        grid[rows//2][cols//4] = sand_pile_height

        grid[rows//4][cols//2] = sand_pile_height

        grid[rows//3][cols//3] = sand_pile_height

        grid[rows//3][cols//3] = sand_pile_height

        grid[rows//3*2][cols//3*2] = sand_pile_height

        grid[rows//3*2][cols//3*2] = sand_pile_height

    return grid


class Grid:

    def __init__(self, graphic, index, all_sand_piles, main_sand_pile, auxiliary_sand_piles):

        self.rows = 150

        self.cols = 150

        self.grid_ = [[all_sand_piles for col in range(self.cols)] for row in range(self.rows)]

        self.grid_[self.rows//2][self.cols//2] = main_sand_pile

        self.grid_[0][0] = 0

        self.grid_ = init_grid(index, self.grid_, self.rows, self.cols, auxiliary_sand_piles)

        self.colors_dict = {0:get_random_color(), 1:get_random_color(), 2:get_random_color(), 3:get_random_color(), 4:get_random_color(), 5:get_random_color(), 6:get_random_color()}  # {0:BLACK, 1:BLUE, 2:YELLOW, 3:RED, 4:PURPLE, 5:PINK, 6:GREEN}

        if graphic:

            Grid.draw(self)

    def print_grid(self):

        for x in self.grid_:

            print(*x)

        print()

    def in_grid(self, row, col):

        return not((row < 0) or (col < 0) or (row > len(self.grid_)-1) or (col > len(self.grid_[0])-1))

    def update(self, graphic):

        n_grid = [self.grid_[x].copy() for x in range(self.rows)]

        #a=b

        for row in range(self.rows):

            for col in range(self.cols):

                if self.grid_[row][col] > 3:

                    n_grid[row][col] -= 4

                    for x, y in [[-1, 0], [1, 0], [0, -1], [0, 1]]:

                        if Grid.in_grid(self, row+x, col+y):

                            n_grid[row+x][col+y] += 1

        self.grid_ = n_grid

        if graphic:

            #Grid.print_grid(self)

            Grid.draw(self)


    def draw(self):

        screen.fill(BLACK)

        for row in range(len(self.grid_)):

            for col in range(len(self.grid_[row])):

                if self.grid_[row][col] > 6:

                    radius = 4

                    color = ORANGE

                else:

                    color = self.colors_dict[self.grid_[row][col]]

                    radius = self.grid_[row][col]

                pygame.draw.circle(screen, color, (row*4, col*4), radius)

        pygame.display.update()
            
def main(inputs):

    all_sand_piles, main_sand_pile, auxiliary_sand_piles, index = inputs

    aff = True

    graphic = 1

    grid = Grid(graphic, index, all_sand_piles, main_sand_pile, auxiliary_sand_piles)

    index = 0

    while aff:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                aff = False

            elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):

                grid.update(graphic)

        grid.update(graphic)

        clock.tick(60)


if __name__ == "__main__":

    index = 4

    all_sand_piles = 3

    main_sand_pile = 100

    auxiliary_sand_piles = 50

    main([all_sand_piles, main_sand_pile, auxiliary_sand_piles, index])
