"""
encore une fois je retente de faire un agario correct
romain david
15/11/2019
"""


from pig_tv import *

from Neural_Network import Network

import numpy as np


def eating_circle(pos1, pos2, big_rad):

    if get_distance(pos1, pos2) < big_rad:

        return 1


def get_speed_of_area(nb):

    speed = set_val_to_different_array([3.1, 4.8], [8, 1], log(nb, 5))

    if speed < 1:

        speed = 1

    return speed


class StaticEntity:

    def __init__(self, universe, coor=0):

        self.radius = 10

        self.area = self.radius * pi**2

        self.color = WHITE

        if coor:

            self.x, self.y = coor

            self.coor = coor

        else:

            self.x, self.y = random.randint(self.radius, universe.width-self.radius), random.randint(self.radius, universe.height-self.radius)

            self.coor = [self.x, self.y]

    def draw(self, move_vect):

        x, y = int(self.x), int(self.y)

        pygame.draw.circle(screen, self.color, sum_arrays([x, y], move_vect), self.radius)

    def eat(self):

        print("Impossible happened!\nFood actually ate a player -_-")


class MovingEntity:

    def __init__(self, universe, coor=0):

        self.universe = universe

        self.vector = [0, 0]

        self.radius = 15

        if coor:

            self.x, self.y = coor

        else:

            self.x, self.y = random.randint(self.radius, universe.width-self.radius), random.randint(self.radius, universe.height-self.radius)

        self.coor = [self.x, self.y]

        self.color = get_random_color()

        self.speed = 5

        self.area = self.radius * pi**2

        self.neighbors = []

        layer_nb, layer_size = 1, 1

        self.brain = Network(3, layer_nb, layer_size, 2)

        self.neural_input = [0, 0, 0]  # diff in x pos, diff in y pos, diff in size

    def think(self):

        self.vector = set_array_to_different_array([0, 1], [-1, 1], self.brain.feedforward(self.neural_input))

        apply_function_to_array(self.vector, lambda x:x*self.speed)

        #print(self.vector, self.neural_input)

##        if not random.randint(0, 100):
##
##            self.vector = get_normalized_vector(sum_arrays(self.coor, [self.universe.width//2, self.universe.height//2], -1), self.speed)

##        vectors = []
##
##        for neighbor in self.neighbors:
##
##            if isinstance(neighbor, MovingEntity):
##
##                if neighbor.radius < self.radius:
##
##                    eatable = 1
##
##                else:
##
##                    eatable = 0
##
##            else:
##
##                eatable = 1
##
##            vectors = self.brain.feedforward(neighbor.x, neighbor.y, eatable)  # neural network takes as input a 3 by 1 matrix (coors + can eat entity) and returns vector
##
##        if vectors != []:
##
##            self.vector = [sum([x[0] for x in vectors]), sum([x[1] for x in vectors])]

    def eat(self, eaten_entity):
        """ the entity eats an other entity; half it's area is added to this ; area = pi*radius**2 """

        self.area += eaten_entity.area/10

        self.radius = int(self.area/pi**2)

        self.speed = get_speed_of_area(self.area)

    def check_pos_in_screen(self):

        if self.x < 0:

            self.x -= self.vector[0]

        elif self.x > self.universe.width:

            self.x -= self.vector[0]

        if self.y < 0:

            self.y -= self.vector[1]

        elif self.y > self.universe.height:

            self.y -= self.vector[1]

        self.coor = [self.x, self.y]

    def update_area(self):

        if self.area > 1000:

            self.area -= .1

            self.radius = int(self.area/pi**2)

    def update(self):

        MovingEntity.update_area(self)

        MovingEntity.think(self)

        MovingEntity.update_coor(self)

        MovingEntity.check_pos_in_screen(self)

    def draw(self, move_vect):

        x, y = int(self.x), int(self.y)

        pygame.draw.circle(screen, self.color, sum_arrays([x, y], move_vect), self.radius)

    def update_coor(self):

        self.coor = sum_arrays(self.coor, self.vector)

        self.x = self.coor[0]

        self.y = self.coor[1]


class PlayerEntity(MovingEntity):

    def __init__(self, universe, camera):

        self.camera = camera

        MovingEntity.__init__(self, universe)

        #self.coor = [100, 100]  # for debugging

        self.color = YELLOW

    def update(self):

        self.vector = get_normalized_vector(sum_arrays(sum_arrays(self.coor, self.camera.off_set), pygame.mouse.get_pos(), -1), self.speed)

        MovingEntity.update_coor(self)

        MovingEntity.update_area(self)

        MovingEntity.check_pos_in_screen(self)


class Universe:

    def __init__(self, width, height):

        self.width = width

        self.height = height

        self.camera = Camera(self)

        self.player = PlayerEntity(self, self.camera)

        self.entities = []

        pop_size = 40

        for x in range(pop_size):

            self.entities.append(MovingEntity(self))

        for x in range(pop_size*2):

            self.entities.append(StaticEntity(self))

        self.entities.append(self.player)

    def update(self, graphic):

        # updating entities vector, and coors

        for ent in self.entities:

            if not isinstance(ent, StaticEntity):

                ent.update()

        # drawing, updating screen

        if graphic:

            self.camera.draw()

            aff_txt(str(int(self.player.area)), 0, 0, WHITE)

        Universe.check_collisions(self)

        pygame.display.update()

    def check_collisions(self):

        # checking collisions (might draw again some entities that are colliding)

        self.entities.sort(key=lambda x:x.radius)

        troi_quartil_size = self.entities[int(len(self.entities)/4*3)].radius  # size of smaller square of quad tree created, so that it can be at most in four squares of quadtree

        # creating tree that shan't have too big or small squares

        rect_size = min(self.width, self.height)  # shouldn't spread even on the smallest side

        max_subd = 0

        left_over = []

        while rect_size > troi_quartil_size:

            rect_size /= 2

            max_subd += 1

        rect_size *= 2

        max_subd -= 1

        terrain_tree = QuadTree(0, 0, self.width, self.height, max_subd, 4)

        # adding most entities in tree (not too big, that could be in more than four squares at a time)
        for x in range(len(self.entities)):

            ent = self.entities[x]

            if ent.radius < rect_size:

                terrain_tree.add_entity(ent)

            else:

                left_over.append(ent)

        # quad tree returns colliding colliding entites, faster detection collision than n!
        colliding = terrain_tree.agario_collisions_and_closest(couple=1, colliding_func=1)

##        # adding inputs to entities
##
##        groups = terrain_tree.get_branches_content()

        # the biggest entities are checked "by hand"
        for to_check_ent in left_over:

            for ent in self.entities:

                if eating_circle(to_check_ent.coor, ent.coor, max(to_check_ent.radius, ent.radius)):  # collide_circle_to_circle(to_check_ent.coor, to_check_ent.radius, ent.coor, ent.radius):

                    colliding.append([to_check_ent, ent])

        # dealing with colliding entities : biggest one eats smallest one
        for couple in colliding:

            if couple[0].radius > couple[1].radius:

                couple[0].eat(couple[1])

                Universe.remove_entity(self, couple[1])

            elif couple[0].radius < couple[1].radius:

                couple[1].eat(couple[0])

                Universe.remove_entity(self, couple[0])

        #terrain_tree.draw(RED, sum_arrays(screen_center, self.player.coor, 1, -1))

    def remove_entity(self, entity):

        if entity in self.entities:  # usually true, except if one eating entity was eaten at the same time..

            if isinstance(entity, StaticEntity):

                self.entities.append(StaticEntity(self))

            else:

                self.entities.append(MovingEntity(self))

            self.entities.remove(entity)


class Camera:

    def __init__(self, universe):

        self.universe = universe

        self.off_set = [0, 0]

        #self.universe_edge = pygame.Rect(0, 0, universe.width, universe.height)

    def draw(self):

        self.off_set = sum_arrays(screen_center, self.universe.player.coor, 1, -1)

        apply_function_to_array(self.off_set, int)

        screen.fill(DARK_BLUE)

        for ent in self.universe.entities:

            ent.draw(self.off_set)

##        offset = sum_arrays([self.universe.width/2, self.universe.height/2], self.universe.player.coor, 1, -1)
##
##        print(offset, self.universe.player.coor)
##
        rect = pygame.Rect(self.off_set[0], self.off_set[1], self.universe.width, self.universe.height)  # rect = pygame.Rect(offset[0], offset[1], self.universe.width, self.universe.height)

        pygame.draw.rect(screen, PURPLE, rect, 1)


def main(inputs):

    # instances

    universe = Universe(1000, 1000)

    # variables

    play = True

    clicking = 0

    graphic = 1

    # main playing loop

    while play:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                play = False

            elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):

                clicking = 1

            elif (event.type == pygame.MOUSEBUTTONUP) and (event.button == 1):

                clicking = 0

            elif (event.type == pygame.MOUSEMOTION):

                translation = event.rel

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_LEFT:

                    pass

        universe.update(graphic)

        clock.tick(60)


if __name__ == "__main__":

    inputs = []

    main(inputs)
