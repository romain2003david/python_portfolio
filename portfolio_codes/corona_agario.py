from pig_tv import *

import pickle

import os


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

        self.color = GREEN

        self.sick = 0

        self.speed = 5

        self.area = self.radius * pi**2

        self.neighbors = []

        self.sick_radius = self.radius*3

        self.healthy = random.randint(180, 300)

    def think(self):

        if not random.randint(0, 5/self.universe.mesure_de_confinement):

            self.vector = get_random_vector()

    def make_sick(self):

        self.sick = 1

        self.color = RED

    def check_pos_in_screen(self):

        if self.x < 0:

            self.x = self.universe.width

        elif self.x > self.universe.width:

            self.x = 0

        if self.y < 0:

            self.y = self.universe.height

        elif self.y > self.universe.height:

            self.y = 0

        self.coor = [self.x, self.y]

    def update_area(self):

        if self.area > 1000:

            self.area -= .1

            self.radius = int(self.area/pi**2)

    def update_sickness(self):

        if self.sick == 1:

            if not random.randint(0, self.universe.sick_time):

                if random.random() < self.universe.kill_rate:

                    self.sick = -1

                    self.color = BLUE

                else:

                    return -1

    def update(self):

        MovingEntity.update_area(self)

        MovingEntity.think(self)

        MovingEntity.update_coor(self)

        MovingEntity.check_pos_in_screen(self)

        return MovingEntity.update_sickness(self)

    def draw(self, move_vect):

        x, y = int(self.x), int(self.y)

        pygame.draw.circle(screen, self.color, sum_arrays([x, y], move_vect), self.radius)

        if self.sick == 1:

            pygame.draw.circle(screen, RED, sum_arrays([x, y], move_vect), self.sick_radius, 3)

    def update_coor(self):

        self.coor = sum_arrays(self.coor, self.vector)

        self.x = self.coor[0]

        self.y = self.coor[1]

    def get_infected(self):

        if not random.randint(0, self.universe.infection_rate):

            MovingEntity.make_sick(self)


class PlayerEntity(MovingEntity):

    def __init__(self, universe, camera):

        self.camera = camera

        MovingEntity.__init__(self, universe, screen_center)

        #self.coor = [100, 100]  # for debugging

        self.color = YELLOW

    def update(self):

        self.vector = get_normalized_vector(sum_arrays(sum_arrays(self.coor, self.camera.off_set), pygame.mouse.get_pos(), -1), self.speed)

        MovingEntity.update_coor(self)

        MovingEntity.update_area(self)

        MovingEntity.check_pos_in_screen(self)

        return MovingEntity.update_sickness(self)


class Universe:

    def __init__(self, width, height):

        # sickness stats

        self.kill_rate = .4

        self.infection_rate = 100

        self.sick_time = 1800

        self.intervall_check = 60  # checks sick ents each sec

        self.mesure_de_confinement = 1

        self.sick_list = []
        ##

        self.width = width

        self.height = height

        self.camera = Camera(self)

        self.player = PlayerEntity(self, self.camera)

        self.entities = []

        pop_size = 80

        for x in range(pop_size):

            self.entities.append(MovingEntity(self))

        self.clock = 0

        player_playing = 0

        if player_playing:

            self.entities.append(self.player)

            self.entities[-1].make_sick()

        else:

            self.entities[0].make_sick()

    def update(self, graphic):

        # updating entities vector, and coors

        to_del = []

        for ent in self.entities:

            if not isinstance(ent, StaticEntity):

                dead = ent.update()

                if dead:

                    to_del.append(ent)

        for x in to_del:

            self.entities.remove(x)

        self.clock += 1

        if self.clock == self.intervall_check:

            self.clock = 0

            sum_sick = 0

            for ent in self.entities:

                if ent.sick == 1:

                    sum_sick += 1

            self.sick_list.append(sum_sick)

            if sum_sick == 0:

                if max(self.sick_list) > 10:

                    file_name = str(random.randint(0, 9))+str(random.randint(0, 9))+str(random.randint(0, 9))+str(random.randint(0, 9))+str(random.randint(0, 9))+str(random.randint(0, 9))

                    file = open("corona_graphs/"+str(file_name)+".txt", "wb")

                    pickle.dump(self.sick_list, file)

                    file.close()

                return -1

        # drawing, updating screen

        if graphic:

            self.camera.draw()

        Universe.check_collisions(self)

        pygame.display.update()

    def check_collisions(self):

        # checking collisions (might draw again some entities that are colliding)

        ent_size = self.entities[0].radius  # size of smaller square of quad tree created, so that it can be at most in four squares of quadtree

        # creating tree that shan't have too big or small squares

        rect_size = min(self.width, self.height)  # shouldn't spread even on the smallest side

        max_subd = 0

        left_over = []

        while rect_size > ent_size:

            rect_size /= 2

            max_subd += 1

        rect_size *= 2

        max_subd -= 1

        terrain_tree = QuadTree(0, 0, self.width, self.height, max_subd, 4)

        # adding most entities in tree (not too big, that could be in more than four squares at a time)
        for x in range(len(self.entities)):

            ent = self.entities[x]

            terrain_tree.add_entity(ent)

        # quad tree returns colliding colliding entites, faster detection collision than n!
        colliding = terrain_tree.agario_collisions_and_closest(couple=1, colliding_func=2)

        # dealing with colliding entities : biggest one eats smallest one
        for couple in colliding:

            if couple[0].sick == 1:

                couple[1].get_infected()

            else:

                couple[0].get_infected()

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

        rect = pygame.Rect(self.off_set[0], self.off_set[1], self.universe.width, self.universe.height)  # rect = pygame.Rect(offset[0], offset[1], self.universe.width, self.universe.height)

        pygame.draw.rect(screen, PURPLE, rect, 1)


def graph_corona_array():

    arrays = []

    for x in os.listdir("corona_graphs"):

        arrays.append(pickle.load(open("corona_graphs/"+x, "rb")))

    if arrays != []:

        graph_arrays(arrays)


def main(inputs):

    # instances

    universe = Universe(800, 700)

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

                if event.key == pygame.K_SPACE:

                    graph_array(universe.sick_list)

                elif event.key == pygame.K_s:

                    graph_corona_array()


        play = not(universe.update(graphic))

        #clock.tick(60)


if __name__ == "__main__":

    inputs = []

    main(inputs)
