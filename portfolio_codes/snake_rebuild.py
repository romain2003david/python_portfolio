from pig_tv import *


class Food:

    def __init__(self, x, y, size):

        self.color = BROWN  # get_random_color()

        self.size = size

        self.x = x

        self.y = y

    def draw(self):

        pygame.draw.circle(screen, self.color, (self.x, self.y), self.size)

class Grid:

    def __init__(self, rows, cols, food_size):

        self.rows = rows

        self.cols = cols

        self.grid = [[0 for x in range(self.cols)] for y in range(self.rows)]

        self.head = [self.rows//2, self.cols//2]

        self.body = [self.head]

##        self.tile_width = screen_width//self.cols
##
##        self.tile_height = 

        self.tile_side = screen_height//self.rows

        self.body_color = YELLOW  # get_random_color()

        self.head_color = RED  # get_random_color()

        self.bg_color = LIGHT_BLUE  # get_random_color()

        self.food_size = food_size

        Grid.set_n_food(self)

        self.dir_vect = [1, 0]

    def set_n_food(self):

        n_x, n_y = random.randint(1, self.rows-1), random.randint(1, self.cols-1)

        self.food = Food(n_x*self.tile_side, n_y*self.tile_side, self.food_size)

        Grid.draw(self)

    def food_near(self, y, x):

        for y_ind in range(-self.food_size, self.food_size+1):

            for x_ind in range(-self.food_size, self.food_size+1):

                Grid.draw_pix(self, y+y_ind, x+x_ind, 1)

                if not(out_screen(x+x_ind, y+y_ind, self.cols-1, self.rows-1)) and (self.grid[y+y_ind][x+x_ind] == 2):

                    return 1

    def grow_snake(self):

#        new_part = [self.body[-1][0]-self.dir_vect[0], self.body[-1][1]-self.dir_vect[1]  ]     

        self.body.append(1)  #new_part)

##        self.grid[new_part[0]][new_part[1]] = 1
##
##        Grid.draw_pix(self, new_part[0], new_part[1], 1)

    def update(self):

        food_found = 0

        self.head = sum_arrays(self.head, list(reversed(self.dir_vect)))

        if out_screen(self.head[0], self.head[1], self.rows-1, self.cols-1):

            return 2

        # checks wether the head is colliding with other part of the body

        for part in self.body[2:]:  # else than head itself and neck

            if self.head == part:  # collide_rect_to_rect([self.head[1]*self.tile_side, self.head[0]*self.tile_side, self.tile_side, self.tile_side], [part[1]*self.tile_side, part[0]*self.tile_side, self.tile_side, self.tile_side]):

                return 2

        self.body.insert(0, self.head)

        if collide_circle_to_rect((self.food.x, self.food.y), self.food.size, [self.head[1]*self.tile_side, self.head[0]*self.tile_side, self.tile_side, self.tile_side]):

            food_found = 1

            Grid.set_n_food(self)

            Grid.grow_snake(self)

        self.grid[self.head[0]][self.head[1]] = 1

        Grid.draw_pix(self, self.head[0], self.head[1], 1)

        if self.body[-1] != 1:

            self.grid[self.body[-1][0]][self.body[-1][1]] = 0

            Grid.draw_pix(self, self.body[-1][0], self.body[-1][1], 0)

        self.body.pop()

        self.food.draw()

        return food_found

    def draw(self):

        for y in range(self.rows):

            for x in range(self.cols):

                Grid.draw_pix(self, y, x, self.grid[y][x])

        self.food.draw()

        pygame.display.update()

    def draw_pix(self, y, x, val):

        if not val == 2:

            if val == 1:  # snake's body

                color = self.body_color

            elif val == 3:  # snake's head

                color = self.head_color

            else:   # background pixel

                color = self.bg_color

            tile_rect = pygame.Rect(x*self.tile_side, y*self.tile_side, self.tile_side, self.tile_side)

            pygame.draw.rect(screen, color, tile_rect)

def main(inputs):

    rows, fps, food_rad = inputs

    cols = rows

    points = 0

    play = True

    screen.fill(BLACK)

    aff_txt("Press whatever you like", 60, 200, color=RED, taille=50)

    pygame.display.update()

    wait()

    screen.fill(BLACK)

    grid = Grid(rows, cols, food_rad)

    while play:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                play = False

            elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):

                mouse_pos = pygame.mouse.get_pos()

            elif (event.type == pygame.MOUSEMOTION):

                translation = event.rel

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_LEFT:

                    if grid.dir_vect != [1, 0]:

                        grid.dir_vect = [-1, 0]

                if event.key == pygame.K_RIGHT:

                    if grid.dir_vect != [-1, 0]:

                        grid.dir_vect = [1, 0]

                if event.key == pygame.K_UP:

                    if grid.dir_vect != [0, 1]:

                        grid.dir_vect = [0, -1]

                if event.key == pygame.K_DOWN:

                    if grid.dir_vect != [0, -1]:

                        grid.dir_vect = [0, 1]

        aff_txt("points : "+str(points), 0, 0, PURPLE)

        output = grid.update()

        if output == 2:

            play = False

        elif output == 1:

            points += 1

        pygame.display.update()

        clock.tick(fps)

    end_game(points)


if __name__ == "__main__":

    main([screen_height//10, 6, 10])
