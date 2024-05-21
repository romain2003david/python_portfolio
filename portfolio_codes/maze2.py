from pig_tv import *


class Grid:

    def __init__(self, rows, cols):

        self.rows = rows

        self.cols = cols

        self.cell_size = min((screen_height-20)/rows, (screen_width-20)/cols)

        self.maze_grid = [[0 for x in range(cols)] for y in range(rows)]

        self.pyg_grid_rect = pygame.Rect(0, 0, (self.cell_size*cols), (self.cell_size*rows))

        self.stack = []

        # defines a random starting pos on the edge of the maze
        if random.randint(0, 1):

            if random.randint(0, 1):

                self.current_pos = [0, random.randint(0, self.rows-1)]

            else:

                self.current_pos = [self.cols-1, random.randint(0, self.rows-1)]

        else:

            if random.randint(0, 1):

                self.current_pos = [random.randint(0, self.cols-1), 0]

            else:

                self.current_pos = [random.randint(0, self.cols-1), self.rows-1]

        self.paths = []

        fucking_recursion_limit_fuck_u = 1

        while fucking_recursion_limit_fuck_u:

             self.current_pos = Grid.next_(self, self.current_pos[0], self.current_pos[1])

             fucking_recursion_limit_fuck_u = (self.current_pos != None)

        Grid.draw(self)

    def next_(self, x_pos, y_pos):

        neighbors = Grid.get_neighbors(self, x_pos, y_pos)

        if neighbors != []:

            if len(neighbors) > 1:

                self.stack.append([x_pos, y_pos])

            next_neighbor = random.choice(neighbors)

            self.maze_grid[next_neighbor[1]][next_neighbor[0]] = 1

            self.paths.append([[x_pos, y_pos], next_neighbor])

            return next_neighbor #  Grid.next_(self, next_neighbor[0], next_neighbor[1])

        elif self.stack != []:

            n_to_do = self.stack[-1]

            self.stack.pop()

            return n_to_do #  Grid.next_(self, n_to_do[0], n_to_do[1])

    def get_neighbors(self, x_pos, y_pos):

        neighbors = []

        for y in range(-1, 2):

            for x in range(-1, 2):

                if (bool(y) != bool(x)):  # not [0, 0] -> means the same one and not diagonale line -> just one zero

                    n_x_pos, n_y_pos = x_pos+x, y_pos+y

                    if not out_screen(n_x_pos, n_y_pos, self.cols-1, self.rows-1):  # inside the grid

                        if not self.maze_grid[n_y_pos][n_x_pos]:  # the cell has not been visited yet

                            neighbors.append([n_x_pos, n_y_pos])

        return neighbors

    def draw(self):

        pygame.draw.rect(screen, BLACK, self.pyg_grid_rect)

        for y in range(self.rows):

            for x in range(self.cols):

                pyg_cell = pygame.Rect((x+0.5)*self.cell_size, (y+0.5)*self.cell_size, self.cell_size//2, self.cell_size//2)

                pygame.draw.rect(screen, WHITE, pyg_cell)

        for path in self.paths:

            n_pt1 = times_array_by_val(add_val_to_array(path[0], 0.75), self.cell_size)

            n_pt2 = times_array_by_val(add_val_to_array(path[1], 0.75), self.cell_size)

            pygame.draw.line(screen, WHITE, n_pt1, n_pt2, int(self.cell_size//8))#pyg_path = pygame.Rect(path[0][0]+self.cell_size, selfself.cell_size, self.cell_size//2)

        pygame.display.update()


def main(inputs):

    rows, cols = inputs

    maze = Grid(rows, cols)



if __name__ == "__main__":

    rows, cols = screen_height//10, screen_width//10

    main([rows, cols])
