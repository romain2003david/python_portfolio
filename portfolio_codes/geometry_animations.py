from pig_tv import *


def draw_lines(fps, progressive_color):

    play = True

    compteur = 0

    adding_rate = 1

    saved_line = get_random_line()

    draw_line(saved_line)

    screen.fill(WHITE)

    color = ColorManager(get_random_color())

    width = random.randint(1, 5)

    s_compteur = 0

    while play:

        compteur += 1

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                play = False

            elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):

                mouse_pos = pygame.mouse.get_pos()

            elif (event.type == pygame.MOUSEMOTION):

                translation = event.rel

        if compteur == adding_rate:

            s_compteur += 1

            if s_compteur == adding_rate*10:

                s_compteur = 0

                saved_line = get_random_line()

                if progressive_color:

                    for x in range(10):

                        color.update_color()

                    if progressive_color == 2:

                        for x in range(10):

                            color.update_color()

                        average = get_average(color.color)

                        color.color = [average for x in range(3)]

                else:

                    color.set_to_rand_color()

                width = random.randint(1, 5)

            compteur = 0

            n_point = [random.randint(0, screen_width), random.randint(0, screen_height)]

            n_droite = get_perpendiculaire_from_d(saved_line, n_point)

            draw_line(n_droite, color.color, width*4)

            saved_line = n_droite

        pygame.display.update()

        clock.tick(fps)


def draw_circles(fps, progressive_color):

    radius = 1

    color = ColorManager(get_random_color())

    signe = 1

    keep_displaying = 1

    x = 0

    diagonale = sqrt(screen_width**2+screen_height**2)

    while keep_displaying:

        x += 1

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                keep_displaying = False

            elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):

                mouse_pos = pygame.mouse.get_pos()

            elif (event.type == pygame.MOUSEMOTION):

                translation = event.rel

        if progressive_color:

            color.update_color()

            if progressive_color == 2:

                color.set_to_bw()

        elif (x % 10 == 0):

            color.set_to_rand_color()

        pygame.draw.circle(screen, color.color, (screen_width//2, screen_height//2), radius)

        radius += 1*signe

        if (radius > diagonale//2) or (radius < 2):

            signe *= -1

        clock.tick(fps)

        pygame.display.update()


class Figure:

    def __init__(self, progressive_color):

        self.increment = 30

        self.ecart = 50

        self.points = [[screen_width//2-self.ecart, screen_height//2-self.ecart],[screen_width//2+self.ecart, screen_height//2-self.ecart], [screen_width//2+self.ecart, screen_height//2+self.ecart], [screen_width//2-self.ecart, screen_height//2+self.ecart]]#[[0, 0], [10, 0], [10, 10], [0, 10]]#

        self.list_points = [self.points]

        self.signes = []

        self.pieton = 0

        self.color = ColorManager()

        self.colors_list = []

        self.progressive_color = progressive_color

        self.compteur = 0

        self.increasing = 1

        Figure.draw(self)

        pygame.display.update()

    def update(self):

        self.compteur += 1

        if self.compteur%40 < 20:

            n_points = []

            signes = [1, 1, -1, -1]

            for x in range(4):

                signe = signes[(x+self.pieton)%4]

                line = get_droite_from_pt(self.points[x], self.points[(x+1)%4])

                #pygame.draw.line(screen, YELLOW, self.points[x], self.points[(x+1)%4])

                n_points.append(get_line_steps(line, self.points[(x+1)%4], self.increment*signe))#, self.points[(x+1)%4][1]+bonus])

            self.list_points.append(n_points)

            self.points = n_points

            self.pieton += 1

        else:

            self.increasing = 0

            self.list_points.pop()

            if len(self.colors_list) > 0:

                self.colors_list.pop()

            if self.compteur%40 == 39:  # resets for a new tour

                self.points = [[screen_width//2-self.ecart, screen_height//2-self.ecart],[screen_width//2+self.ecart, screen_height//2-self.ecart], [screen_width//2+self.ecart, screen_height//2+self.ecart], [screen_width//2-self.ecart, screen_height//2+self.ecart]]

                self.list_points = [self.points]

                self.pieton = 0

                self.increasing = 1

                self.color.set_to_rand_color()

                self.colors_list = [self.color.color.copy()]

        Figure.draw(self)

    def draw(self):

        screen.fill(BLACK)

        for x in range(len(self.list_points)-1, -1, -1):

            if self.progressive_color == 1:

                if self.increasing:

                    self.colors_list.append(self.color.color.copy())

                    for c in range(20):

                        self.color.update_color()

                pygame.draw.polygon(screen, self.colors_list[x], self.list_points[x])

            elif self.progressive_color == 2:

                pygame.draw.polygon(screen, BLACK*(x%2) or WHITE, self.list_points[x])

            else:

                pygame.draw.polygon(screen, get_random_color(), self.list_points[x])

##        for x in self.points:
##
##            pygame.draw.circle(screen, RED, (int(x[0]), int(x[1])), 10)#



def draw_growing_squares(fps, progressive_color):

    play = True

    fig = Figure(progressive_color)

    compteur = 0

    rate = int((1/fps)*1000)

    while play:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                play = False

            elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):

                a = 0

        if not compteur%(rate):

            fig.update()

            pygame.display.update()

        compteur += 1

        clock.tick(fps)


class Star:

    def __init__(self, color_mode):

        self.x = random.randint(0, screen_width)

        self.y = random.randint(0, screen_height)

        self.target = [screen_width//2, screen_height//2]

        self.changing_color = color_mode

        if not(color_mode == 1):

            self.color1 = REAL_LIGHT_BLUE

            self.color2 = WHITE

        else:

            self.color1 = ColorManager()

            self.color2 = ColorManager()

    def goto(self, x, y):

        Star.stear(self, x, y)

        Star.get_speed(self, x, y)

        Star.move(self)

        if Star.out_born(self):

            Star.go_middle(self)

    def stear(self, x, y):
        """ Defines a new moving vector """

        self.vector = [x-self.x, y-self.y]

    def get_speed(self, x, y):

        self.speed = -10

    def move(self):

        total = abs(self.vector[0]) + abs(self.vector[1])

        if total:

            add_x = self.speed * (self.vector[0]/total)

            add_y = self.speed * (self.vector[1]/total)

        else:

            add_y = 0

            add_x = 0

        self.x += add_x

        self.y += add_y

    def update(self):

        Star.goto(self, self.target[0], self.target[1])

        Star.draw(self)

    def draw(self):

        if self.changing_color == 0:

            pygame.draw.circle(screen, get_random_color(), (int(self.x), int(self.y)), 3, 1)

            pygame.draw.circle(screen, get_random_color(), (int(self.x), int(self.y)), 2)

        elif self.changing_color == 1:

            self.color1.update_color()

            self.color2.update_color()

            pygame.draw.circle(screen, self.color1.color, (int(self.x), int(self.y)), 3, 1)

            pygame.draw.circle(screen, self.color2.color, (int(self.x), int(self.y)), 2)

        else:

            pygame.draw.circle(screen, self.color1, (int(self.x), int(self.y)), 3, 1)

            pygame.draw.circle(screen, self.color2, (int(self.x), int(self.y)), 2)

    def out_born(self):

        if (self.x < 0) or (self.y < 0) or (self.x > screen_width) or (self.y > screen_height):

            return True

        return False

    def go_middle(self):

        self.x = random.randint(screen_width//2-100, screen_width//2+100)

        self.y = random.randint(screen_height//2-100, screen_height//2+100)


def draw_stars(fps, progressive_color):

    play = True

    stars = [Star(progressive_color) for x in range(1000)]

    while play:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                play = False

        for star in stars:

            star.update()

        pygame.display.update()

        clock.tick(fps)


class Pyramid:

    def __init__(self, square_size, center):

        self.fast_center = 1

        self.square_size = square_size

        self.center = center

        self.corners = [[0, screen_width], [screen_height, screen_width], [screen_height, 0], [0, 0]]

        self.max_dist = max([get_distance(self.center, x) for x in self.corners])

        self.screen_content = []

        Pyramid.set_random_moving_vector(self)

        self.y_loops = screen_height//square_size

        self.x_loops = screen_width//square_size

        for y in range(self.y_loops):

            self.screen_content.append([])

            for x in range(self.x_loops):

                self.screen_content[-1].append(get_distance(center, (x*square_size, y*square_size)))

    def set_random_moving_vector(self):

        set_rand_vect = 0

        if set_rand_vect == 1:

            if random.randint(0, 1):  # 1 out of 2

                self.random_moving_vector = [0, 0]

                if random.randint(0, 1):

                    self.random_moving_vector[0] = 1

                else:

                    self.random_moving_vector[0] = -1

            else:  # 1 out of 2

                self.random_moving_vector = [0, 0]

                if random.randint(0, 1):

                    self.random_moving_vector[1] = 1

                else:

                    self.random_moving_vector[1] = -1

        else:

            self.random_moving_vector = sum_arrays(self.center, pygame.mouse.get_pos(), -1, 1)

            if self.fast_center == 0:

                self.random_moving_vector = get_normalized_vector(self.random_moving_vector, 10)

            apply_function_to_array(self.random_moving_vector, round)

    def set_screen_square(self, n_size):

        self.square_size = n_size

        old_y_loops = self.y_loops

        old_x_loops = self.x_loops

        self.y_loops = screen_height//self.square_size

        self.x_loops = screen_width//self.square_size

        x_diff = self.x_loops - old_x_loops

        if x_diff < 0:

            for x in range(abs(x_diff)):

                for row in self.screen_content:

                    del row[-1]

        elif x_diff > 0:

            for x in range(abs(x_diff)):

                for row in self.screen_content:

                   row.append(0)

        y_diff = self.y_loops - old_y_loops

        if y_diff < 0:

            for x in range(abs(y_diff)):

                del self.screen_content[-1]

        elif y_diff > 0:

            for x in range(abs(y_diff)):

                self.screen_content.append([0 for x in range(self.x_loops)])

    def update(self):

        new_update = 1

        # center's moved
        self.center = sum_arrays(self.center, self.random_moving_vector)

        if new_update == 0:

            # the screen_contents (each square) is moved
            n_screen_content = [[0 for x in range(self.x_loops)] for y in range(self.y_loops)]

            for y in range(self.y_loops):

                for x in range(self.x_loops):

                    n_x = x + self.random_moving_vector[0]

                    n_y = y + self.random_moving_vector[1]

                    if not out_screen(n_x, n_y, self.x_loops-1, self.y_loops-1):

                        n_screen_content[n_y][n_x] = self.screen_content[y][x]

            # fills the forgotten line (because of moving vector
            steady_index = self.random_moving_vector.index(0)

            forgotten_line_index = (steady_index-1)*-1

            to_fill_squares_nb = [self.y_loops, self.x_loops][forgotten_line_index]

            if self.random_moving_vector[forgotten_line_index] == -1:

                other_dimension_coor = [self.y_loops, self.x_loops][steady_index]-1

            else:

                other_dimension_coor = 0

            for v in range(to_fill_squares_nb):

                if forgotten_line_index == 0:

                    #print(1, [v, other_dimension_coor])

                    n_col = get_distance(self.center, (v*self.square_size, other_dimension_coor*self.square_size))

                    n_screen_content[v][other_dimension_coor] = n_col

                else:

                    #print(3, [v, other_dimension_coor])

                    n_col = get_distance(self.center, (other_dimension_coor*self.square_size, v*self.square_size))

                    n_screen_content[other_dimension_coor][v] = n_col
            ##
            # sets new screen content
            self.screen_content = n_screen_content

        else:

            for y in range(self.y_loops):

                for x in range(self.x_loops):

                    self.screen_content[y][x] = get_distance(self.center, (x*self.square_size, y*self.square_size))

        Pyramid.draw(self)

        Pyramid.set_random_moving_vector(self)

    def draw(self):

        max_dist = max([get_distance(self.center, x) for x in self.corners])

        for y in range(self.y_loops):

            for x in range(self.x_loops):

                col = set_val_to_different_array([0, self.max_dist], [0, 255], self.screen_content[y][x])

                if col < 0:

                    col = 0

                if col > 255:

                    col = 255

                pygame.draw.rect(screen, [col for x in range(3)], pygame.Rect(x*self.square_size, y*self.square_size, self.square_size, self.square_size))


def draw_pyramid(fps, progressive_color):

    lift = Lift(20, 30, min_borne=1, max_borne=100, afficher_echelle=0, float_vals=0, echelle=10)

    fast_center_button = BoolButton(300, 30, "Fast Center", 1)

    square_size = 10

    pyramid = Pyramid(square_size, screen_center)

    clicking = 0

    play = True

    while play:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                play = False

            elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):

                mouse_pos = pygame.mouse.get_pos()

                clicking = 1

                if fast_center_button.clicked(mouse_pos):

                    fast_center_button.bool_value = (fast_center_button.bool_value-1)*-1

                    pyramid.fast_center = fast_center_button.bool_value

            elif (event.type == pygame.MOUSEBUTTONUP) and (event.button == 1):

                clicking = 0

            elif (event.type == pygame.MOUSEMOTION):

                translation = event.rel

                if clicking:

                    lift.go(translation[0])

                    pyramid.set_screen_square(lift.echelle)

        # updating screen
        pyramid.update()

        fast_center_button.draw()

        lift.draw()

        pygame.display.update()

        clock.tick(fps)


def main(inputs):

    fps, anim_choice, progressive_color = inputs

    if anim_choice == 0:

        draw_lines(fps, progressive_color)

    elif anim_choice == 1:

        draw_circles(fps, progressive_color)

    elif anim_choice == 2:

        draw_growing_squares(fps, progressive_color)

    elif anim_choice == 3:

        draw_stars(fps, progressive_color)

    elif anim_choice == 4:

        draw_pyramid(fps, progressive_color)


if __name__ == "__main__":

    main([60, 4, 1])
