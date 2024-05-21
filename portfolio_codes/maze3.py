from pig_tv import *


class Grid:

    def __init__(self, rows, cols):

        self.rows = rows

        self.cols = cols

        self.cell_size = min((screen_height-20)/rows, (screen_width-20)/cols)

        self.maze_grid = [[0 for x in range(cols)] for y in range(rows)]

        self.pyg_grid_rect = pygame.Rect(0, 0, (self.cell_size*cols), (self.cell_size*rows))

        self.stack = []

        self.compteur_stack = []

        self.cell_compteur = 0

        self.max_cell_compteur = 0

        self.best_finish_spot = []

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

        self.start_pos = self.current_pos.copy()

        self.paths = []

        self.start_end = []

        fucking_recursion_limit_fuck_u = 1

        while fucking_recursion_limit_fuck_u:  # avoid recursive functions (for big mazes : RecursionError: maximum recursion depth exceeded in comparison)

             self.current_pos = Grid.next_(self, self.current_pos[0], self.current_pos[1])

             fucking_recursion_limit_fuck_u = (self.current_pos != None)

        Grid.draw(self)

    def next_(self, x_pos, y_pos):

        neighbors = Grid.get_neighbors(self, x_pos, y_pos)

        if neighbors != []:

            self.cell_compteur += 1

            if len(neighbors) > 1:

                self.stack.append([x_pos, y_pos])

                self.compteur_stack.append(self.cell_compteur)

            next_neighbor = random.choice(neighbors)

            # to chose the finish : takes the one further away from start (not necessarily the harder but anyway..)

            if self.cell_compteur > self.max_cell_compteur:

                self.max_cell_compteur = self.cell_compteur

                self.best_finish_spot = next_neighbor.copy()

            self.maze_grid[next_neighbor[1]][next_neighbor[0]] = 1

            self.paths.append([[x_pos, y_pos], next_neighbor])

            return next_neighbor #  Grid.next_(self, next_neighbor[0], next_neighbor[1])

        elif self.stack != []:

            n_to_do = self.stack[-1]

            self.cell_compteur = self.compteur_stack[-1]

            self.stack.pop()

            self.compteur_stack.pop()

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

        # draws start and end spots
        start_cell = pygame.Rect((self.start_pos[0]+0.5)*self.cell_size, (self.start_pos[1]+0.5)*self.cell_size, self.cell_size//2, self.cell_size//2)

        end_cell = pygame.Rect((self.best_finish_spot[0]+0.5)*self.cell_size, (self.best_finish_spot[1]+0.5)*self.cell_size, self.cell_size//2, self.cell_size//2)

        pygame.draw.rect(screen, GREEN, start_cell)

        pygame.draw.rect(screen, BLUE, end_cell)

        pygame.display.update()

        self.start_end.append([start_cell[0], start_cell[1], start_cell[2], start_cell[3]])

        self.start_end.append([end_cell[0], end_cell[1], end_cell[2], end_cell[3]])

    def get_walls(self):

        outer_walls = list(get_lines_of_rect(self.pyg_grid_rect))

        inner_walls = []

        for y in range(self.rows-1):

            for x in range(self.cols-1):

                inner_walls.append([[(x+1)*self.cell_size, (y)*self.cell_size], [(x+1)*self.cell_size, (y+1)*self.cell_size]])

                inner_walls.append([[(x)*self.cell_size, (y+1)*self.cell_size], [(x+1)*self.cell_size, (y+1)*self.cell_size]])

            inner_walls.append([[(x+1)*self.cell_size, (y+1)*self.cell_size], [(x+2)*self.cell_size, (y+1)*self.cell_size]])

        for x in range(self.cols-1):

            inner_walls.append([[(x+1)*self.cell_size, (self.rows-1)*self.cell_size], [(x+1)*self.cell_size, self.rows*self.cell_size]])

        add_val_to_array(outer_walls, 0.125*self.cell_size)

        add_val_to_array(inner_walls, 0.25*self.cell_size)

        for wall_index in range(len(inner_walls)-1, -1, -1):

            wall = inner_walls[wall_index]

            clean = 1

            for path in self.paths:

                if collide_segment_to_segment(apply_function_to_array(path, int), apply_function_to_array(wall, int)):

                    clean = 0

            if clean:

                pygame.draw.line(screen, PINK, wall[0], wall[1])

            else:

                del inner_walls[wall_index]

        for wall in outer_walls:

            pygame.draw.line(screen, PINK, wall[0], wall[1])

        pygame.display.update()

        return outer_walls+inner_walls

    def draw_traditional_maze(self, walls):

        pygame.draw.rect(screen, BLACK, self.pyg_grid_rect)

        wall_thickness = int(100/self.cols)+1

        for wall in walls:

            pygame.draw.line(screen, WHITE, wall[0], wall[1], wall_thickness)

        # draws start and end spots
        start_cell = pygame.Rect((self.start_pos[0]+0.5)*self.cell_size, (self.start_pos[1]+0.5)*self.cell_size, self.cell_size//2, self.cell_size//2)

        end_cell = pygame.Rect((self.best_finish_spot[0]+0.5)*self.cell_size, (self.best_finish_spot[1]+0.5)*self.cell_size, self.cell_size//2, self.cell_size//2)

        pygame.draw.rect(screen, GREEN, start_cell)

        pygame.draw.rect(screen, BLUE, end_cell)

        pygame.display.update()


def main(inputs):

    rows, cols, style = inputs

    maze = Grid(rows, cols)

    #wait()

    walls = maze.get_walls()

    wait()

    if style:

        maze.draw_traditional_maze(walls)

    wait()

    return walls, maze.start_end


if __name__ == "__main__":

    var = 10

    rows, cols = var, var #  screen_height//10, screen_width//10

    style = 1

    main([rows, cols, style])
