from pig_tv import *

from Neural_Network import Network

import numpy as np

import pickle


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

        self.tile_side = screen_height//self.rows

        self.body_color = YELLOW  # get_random_color()

        self.head_color = RED  # get_random_color()

        self.bg_color = LIGHT_BLUE  # get_random_color()

        self.food_size = food_size

        self.dir_vect = [1, 0]

        self.vects = [[-1, 0], [0, -1], [1, 0], [0, 1]]

        self.vect_index = 2

        Grid.set_n_food(self)

    def get_nearest(self):

        vect = self.dir_vect

        pos = self.head.copy()  # checks if no body part in our way

        x, y = sum_arrays(pos.copy(), vect)

        # too long

##        while not(out_screen(x, y, self.cols-1, self.rows-1)):
##
##            for b in self.body:
##
##                if b == [x, y]:
##
##                    if vect[0]:
##
##                        return x-pos[0]
##
##                    return y-pos[1]
##
##            x, y = sum_arrays([x, y], vect)
##
##        if vect[0]:
##
##            return x-pos[0]
##
##        return y-pos[1]

        dist = self.cols

        if not vect[0]:

            for b in self.body:

                if b[0] == x:

                    if vect[1] > 0:

                        if b[1] >= y:

                            if dist > abs(b[1]-y):

                                dist = abs(b[1]-y)

                    else:

                        if b[1] <= y:

                            if dist > abs(b[1]-y):

                                dist = abs(b[1]-y)
        else:

            for b in self.body:

                if b[1] == y:

                    if vect[0] > 0:

                        if b[0] >= x:

                            if dist > abs(b[0]-x):

                                dist = abs(b[0]-x)

                    else:

                        if b[0] <= x:

                            if dist > abs(b[0]-x):

                                dist = abs(b[0]-x)

        if vect[0]:

            dist2 = x-pos[0]

        else:

            dist2 = y-pos[1]

        return min(dist, dist2)

    def turn_vect(self, val):

        self.vect_index = (self.vect_index+val)%len(self.vects)

        self.dir_vect = self.vects[self.vect_index]

    def set_n_food(self):

        n_x, n_y = random.randint(1, self.rows-1), random.randint(1, self.cols-1)

        self.food = Food(n_x*self.tile_side, n_y*self.tile_side, self.food_size)

        Grid.draw(self)

    def get_rel_dist_food(self):
        """ returns the difference in x and y between player and food instance """

        return [self.head[0]-self.food.x/self.tile_side, self.head[1]-self.food.y/self.tile_side]

    def food_near(self, y, x):

        for y_ind in range(-self.food_size, self.food_size+1):

            for x_ind in range(-self.food_size, self.food_size+1):

                Grid.draw_pix(self, y+y_ind, x+x_ind, 1)

                if not(out_screen(x+x_ind, y+y_ind, self.cols-1, self.rows-1)) and (self.grid[y+y_ind][x+x_ind] == 2):

                    return 1

    def grow_snake(self):

        self.body.append(1)

    def update(self):

        food_found = 0

        self.head = sum_arrays(self.head, list(reversed(self.dir_vect)))

        # snake is out of screen
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

            if val == 1:

                color = self.body_color

            elif val == 3:

                color = self.head_color

            else:

                color = self.bg_color

            tile_rect = pygame.Rect(x*self.tile_side, y*self.tile_side, self.tile_side, self.tile_side)

            pygame.draw.rect(screen, color, tile_rect)



def game_loop(rows, fps, food_rad, snake, generation, running_time):

    cols = rows

    points = 0

    play = True

    screen.fill(BLACK)

    grid = Grid(rows, cols, food_rad)

    compteur = 0

    while play:

        compteur += 1

        if compteur == running_time:

            play = False

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                play = False

        # draws point stats

        aff_txt("points : "+str(points), 0, 0, PURPLE)

        aff_txt("generation : "+str(generation), 0, 50, color=PURPLE)

        # defining snake input, updating snake AI

        nearest_wall = set_val_to_different_array([0, cols], [-1, 1], grid.get_nearest())

        x_food_diff_pos, y_food_diff_pos = grid.get_rel_dist_food()

        x_food_diff_pos = set_val_to_different_array([0, cols], [-1, 1], x_food_diff_pos)

        y_food_diff_pos = set_val_to_different_array([0, rows], [-1, 1], y_food_diff_pos)

        snake_input = np.array([nearest_wall, x_food_diff_pos, y_food_diff_pos])

        snake_output = snake.feedforward(snake_input)

        if snake_output[0] > 0.5:  # AI wants to turn left

            if snake_output[0] < snake_output[1]:  # AI wants to turn right even more

                grid.turn_vect(1)

            else:

                grid.turn_vect(-1)

        elif snake_output[1] > 0.5:  # AI wants to turn right

            grid.turn_vect(1)

        # updating grid (eats food, is out screen..)

        output = grid.update()

        if output == 2:

            snake.points = points

            play = False

        elif output == 1:

            points += 1

        pygame.display.update()

        #clock.tick(fps)

    return points


def main(inputs):

    # Variables

    rows, fps, food_rad, pop_len, layer_nb, layer_size, mutation_rate = inputs

    generation = 0

    keep_training = 1

    running_time = 300

    # defining start population

    if 1:#input("1) Start with random population\n2) Load existing population\n") == "1":

        snakes = []

        for x in range(pop_len):

            snakes.append(Network(3, layer_nb, layer_size, 2))

        snake_pop = Population(snakes, 1, mutation_rate, lambda x:x**2)

        print("Random population generated")

    else:

        snakes = load_pop()

        snake_pop = Population(snakes, 1, mutation_rate, lambda x:x**2)

        print("Population succesfully loaded")

    # Training loop

    train_pop = True

    while train_pop:

        generation += 1

        start_time = time.time()

        for snake in snakes:

            snake.points = game_loop(rows, fps, food_rad, snake, generation, running_time)

        print("temps :", round(time.time()-start_time, 2))

        keep_training -= 1

        running_time += 10

        rows += 1

        if not keep_training:

            train_pop = input("q = quitter\n")!="q"

            if train_pop:

                keep_training = int(input("generation number:\n"))

        if train_pop:

            if snake_pop.evaluate() == -1:  # empty generation (all entities have 0)

                snakes = []

                for x in range(pop_len):

                    snakes.append(Network(3, layer_nb, layer_size, 2))

                snake_pop = Population(snakes, 1, mutation_rate, lambda x:x**2)

            else:

                snake_pop.evolve()

                snakes = snake_pop.pop.copy()

    if input("1) Save population\n") == "1":

        save_pop(snake_pop.pop)

        print("Population saved")

    else:

        print("Population not saved")


if __name__ == "__main__":

    pop_len = 40

    layer_nb, layer_size, mutation_rate = 1, 2, 8

    rows = 6#screen_height//10

    main([rows, 6, 10, pop_len, layer_nb, layer_size, mutation_rate])
