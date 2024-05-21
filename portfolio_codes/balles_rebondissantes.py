from pig_tv import *


class Terrain:

    def __init__(self, ground):

        self.rectangles = [[0, screen_height-ground, screen_width, ground], [screen_width//2+30, 200, 40, screen_height]]

        self.objects = [RotatingRectangle(70, [470, 100], 200, [0, 10, 100, 110], color=BLACK),
                        RotatingRectangle(70, [470, 100], 200, [50, 60, 150, 160], color=BLACK)
                        ]

    def update(self, graphic):

        for obj in self.objects:

            obj.update()

        if graphic:

            Terrain.draw(self)

    def draw(self):

        for rect in self.rectangles:

            pygame.draw.rect(screen, BLACK, pygame.Rect(rect[0], rect[1], rect[2], rect[3]))

        for obj in self.objects:

            obj.draw()


class Balle:

    def __init__(self, radius, x, y, ground, gravity_constant):

        self.ground = ground

        self.radius = 20#random.randint(5, 50)

        self.x = random.randint(0, screen_width//2)

        self.y = y

        self.vector = [0, 0]

        self.gravite = gravity_constant

        self.color = get_random_color()

        self.frottements = 0.02

    def update(self, graphic, rectangles, mouse):

        Balle.update_vector(self, rectangles, mouse)
##
##        repulsion = set_array_to_different_array([-700, 700], [-1, 1], stear_of_screen(self.x, self.y, screen_width, screen_height))
##
##        self.vector = [self.vector[0]+repulsion[0], self.vector[1]+repulsion[1]]

        #if not out_screen(self.x+self.vector[0], self.y+self.vector[1], screen_width, screen_height):

        self.x += self.vector[0]

        self.y += self.vector[1]

        if graphic:

            Balle.draw(self)

    def down_scale_vector(self, facteur=1):

        for x in range(len(self.vector)):

            if x == 1:

                frottements = self.frottements*4

            else:

                frottements = self.frottements

            if self.vector[x] < 0:

                self.vector[x] += frottements*facteur

            elif not self.vector[x] == 0:

                self.vector[x] -= frottements*facteur

    def update_vector(self, rectangles, mouse):

        collision = deal_with_collisions(self.x, self.y, self.radius, rectangles)  # list with all collisions

        if 2 in collision:

            self.vector[1] *= -1

        else:

            self.vector[1] += self.gravite

        if 1 in collision:

            self.vector[0] *= -1

            self.x += self.vector[0]*2

            Balle.down_scale_vector(self, 10)

        if mouse.click:

            if collide_circle_to_circle((self.x, self.y), self.radius, pygame.mouse.get_pos(), mouse.radius):

                n_vector = get_vector_to_point(pygame.mouse.get_pos(), (self.x, self.y), 3)

                self.vector = add_arrays(self.vector, n_vector)

        Balle.down_scale_vector(self)

        if (self.x < 0):

            self.x = 0

            self.vector[0] *= -1

            Balle.down_scale_vector(self, 10)

        elif (self.x > screen_width):

            self.x = screen_width

            self.vector[0] *= -1

            Balle.down_scale_vector(self, 10)

        if abs(self.vector[1]) < self.frottements*8:

           self.vector[1] = 0

        if self.y < 0:

            self.y = 0

            self.vector[1] = 0.1

        elif self.y > screen_height-self.ground-self.radius+1:

            self.y = screen_height-self.ground-self.radius

        if self.vector[0] > 20:

            self.vector[0] = 20

        elif self.vector[0] < -20:

            self.vector[0] = -20

    def draw(self):

        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)


class Mouse:

    def __init__(self):

        self.radius = 60

        self.click = 0

    def update(self, graphic):

        if graphic:

            Mouse.draw(self)

    def draw(self):

        if self.click == 1:

            color = RED

        else:

            color = GREY

        pygame.draw.circle(screen, color, pygame.mouse.get_pos(), self.radius)


def main(inputs):

    radius, gravity_constant = inputs

    ground = 40

    balles = [Balle(radius, random.randint(50, screen_width-50), random.randint(50, screen_height-50), ground, gravity_constant) for x in range(100)]

    play = True

    graphic = 1

    terrain = Terrain(ground)

    mouse = Mouse()

    while play:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                play = False

            elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):

                mouse.click = 1

            elif (event.type == pygame.MOUSEBUTTONUP) and (event.button == 1):

                mouse.click = 0

            elif (event.type == pygame.MOUSEMOTION):

                translation = event.rel

        screen.fill(WHITE)

        mouse.update(graphic)

        terrain.update(graphic)

        for bal in balles:

            bal.update(graphic, terrain.rectangles, mouse)

        pygame.display.update()

        clock.tick(60)


if __name__ == "__main__":

    radius = 10

    gravity_constant = 0.3

    inputs = [radius, gravity_constant]

    main(inputs)
