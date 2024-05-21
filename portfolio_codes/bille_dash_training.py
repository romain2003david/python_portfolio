from pig_tv import *

from Neural_Network import Network

import numpy as np

import pickle

## Functions

def get_coef(universe, move_x, index1=1):

    #x_loc1 = universe.universe_entities[index1].x

    while not(universe.universe_entities[index1].of_importance):  #(x_loc1 == universe.universe_entities[index1+1].x:

        index1 += 1

    index2 = index1+1

    #x_loc2 = universe.universe_entities[index2].x

    while not(universe.universe_entities[index2].of_importance):  #while x_loc2 == universe.universe_entities[index2+1].x:

        index2 += 1

    #print(index1, index2, ((universe.universe_entities[index1].y - universe.universe_entities[index2].y)/cote_bloc) * -move_x)

    return ((universe.universe_entities[index1].y - universe.universe_entities[index2].y)/cote_bloc) * -move_x


def set_terrain():

    terrain = [Rectangle(0, ground, [0, 0], cote_bloc, cote_bloc)]  # to initiate the terrain, needs a starting point

    terrain += create_highway(10, terrain[-1])

    return terrain


def create_path(terrain):

    print_path = 0

    rand_nb = random.randint(0, 7)

    strings = ["highway", "obstacle highway", "up_and_down", "create_piege", "create_platefomes", "hole_highway", "high stairs", "high fast up_and_down"]

    if print_path:

        print(strings[rand_nb])

    if rand_nb == 0:

        return create_highway(random.randint(1, 6), terrain[-1])

    elif rand_nb == 1:

        return obstacle_higway(random.randint(1, 6), terrain[-1])

    elif rand_nb == 2:

        return up_and_down(random.randint(1, 2), terrain[-1])

    elif rand_nb == 3:

        nbr = random.randint(1, 4)

        if random.randint(0, 2) == 0:

            return create_piege(nbr, terrain[-1], -1)

        return create_piege(nbr, terrain[-1])

    elif rand_nb == 4:

        return create_platefomes(random.randint(2, 5), terrain[-1], height=random.randint(1, 3))

    elif rand_nb == 5:

        return hole_highway(random.randint(3, 10), terrain[-1])

    elif rand_nb == 6:

        return create_stairs(random.randint(1, 3), terrain[-1], height=1)

    elif rand_nb == 7:

        return fast_up_and_down(random.randint(1, 3), terrain[-1])


def create_platefomes(length, last, height=2):

    terrain = [last]

    if length > 5:

        terrain += obstacle_higway(length, terrain[-1], intervalle=length//2)

    else:

        terrain += create_highway(length, terrain[-1])

    terrain.append(add_block(terrain[-1], [1, height], of_var_importance=1))

    if length > 5:

        terrain += obstacle_higway(length, terrain[-1], intervalle=length//2)

    else:

        terrain += create_highway(length-1, terrain[-1])

    return terrain[1:]



def hole_highway(length, last):

    terrain = [last]

    nex = random.randint(3, 5)

    for x in range(length):

        nex -= 1

        if nex == 0:

            for b in range(random.randint(1, 3)):

                terrain.append(add_block(terrain[-1], [1, 0], 1))  # collide_safe == 1 : invisible block

            nex = random.randint(3, 5)

        else:

            terrain.append(add_block(terrain[-1], [1, 0]))

    # to make sure doesn't make a hole next to some other stuff
    for x in range(2):

        terrain.append(add_block(terrain[-1], [1, 0]))

    return terrain[1:]


def update_terrain(universe):

    while len(universe.universe_entities) < 80:

        universe.universe_entities += create_path(universe.universe_entities)

    
def add_block(last_block, vecteur, collide_safe=0, of_var_importance=1):
    """ adds a new block to the terrain according to the vector, and the last block """

    return Rectangle(last_block.x+cote_bloc*vecteur[0], last_block.y+cote_bloc*vecteur[1], [0, 0], cote_bloc, cote_bloc, collide_safe=collide_safe, of_var_importance=of_var_importance)


def up_and_down(length, last):

    terrain = [last]

    terrain += create_highway(2, terrain[-1])

    for x in range(length):

        nbr = random.randint(2, 4)

        terrain += create_stairs(nbr, terrain[-1], up=1, height=1)

        terrain += create_highway(2, terrain[-1])

        terrain += create_stairs(nbr, terrain[-1], up=-1, height=1)

    terrain += create_highway(2, terrain[-1])

    return terrain[1:]


def fast_up_and_down(length, last):

    terrain = [last]

    terrain += create_highway(2, terrain[-1])

    for x in range(length):

        terrain += create_stairs(2, terrain[-1], up=1, height=1)

        terrain += create_stairs(2, terrain[-1], up=-1, height=1)

    terrain += create_highway(2, terrain[-1])

    return terrain[1:]


def obstacle(last):

    terrain = [last]

    terrain.append(add_block(terrain[-1], [0, -1], of_var_importance=0))

    terrain.append(add_block(terrain[-1], [1, 1]))

    return terrain[1:]


def create_piege(length, last, height=1):

    terrain = [last]

    for y in range(length*2):

        if y % 2 == 1:

            liste = [height*-1, 0]

        else:

            liste = [height*-1]

        for x in liste:  # creates a block with each item of list (when odd number, create block with h*-1, and block with 0)

            terrain.append(add_block(terrain[-1], [1, x], (y%2==0)))

    terrain.append(add_block(terrain[-1], [2, -5], of_var_importance=0))#terrain.append(add_block(terrain[-1], [2, -4], (y%2==0), 0))

    terrain.append(add_block(terrain[-1], [0, 1], of_var_importance=0))#terrain.append(add_block(terrain[-1], [0, 1], (y%2==0), 0))

    terrain.append(add_block(terrain[-1], [0, 1], of_var_importance=0))

    terrain.append(add_block(terrain[-1], [0, 5], (y%2==0)))

    terrain += create_highway(5, terrain[-1])

    return terrain[1:]


def obstacle_higway(length, last, intervalle=5):

    terrain = [last]

    for x in range(1, length+1):

        if (x%intervalle) == 0:

            terrain += obstacle(terrain[-1])

        terrain.append(add_block(terrain[-1], [1, 0]))

    return terrain[1:]


def create_highway(length, last):

    terrain = [last]

    for x in range(length):

        terrain.append(add_block(terrain[-1], [1, 0]))

    return terrain[1:]


def create_cut_road(length, last):

    terrain = [last]

    for x in range(length):

        terrain.append(add_block(terrain[-1], [1, 0], not(x%3)))

    return terrain[1:]


def create_stairs(length, last, up=1, height=0.5):

    terrain = [last]

    for y in range(length*2):

        if y % 2 == 1:

            liste = [height*up*-1, 0]

        else:

            liste = [height*up*-1]

        for x in liste:

            terrain.append(add_block(terrain[-1], [1, x], (y%2==0)))

    return terrain[1:]


# classes


class Universe:

    def __init__(self):

        self.up_color = [random.randint(50, 255), random.randint(50, 255), random.randint(50, 255)]

        self.low_color = [x-50 for x in self.up_color]

        self.universe_entities = set_terrain()

        self.particules = []

        self.selected_color = [random.randint(0, 2), 1]

        #Universe.print_var_terrain(self)

    def print_terrain(self):

        print(len(self.universe_entities))

        print("start")

        for x in range(len(self.universe_entities)):

            print(self.universe_entities[x].y)

        print("end")

    def print_var_terrain(self):

        print(len(self.universe_entities))

        print("start")

        for x in range(len(self.universe_entities)-1):

            print(self.universe_entities[x+1].y-self.universe_entities[x].y)

        print("end")

    def update(self, graphic, move):
        """ takes the vector that should be compensated by the universe entities """

        dead = 0

        for entity_index in range(len(self.universe_entities)-1, -1, -1):

            entity = self.universe_entities[entity_index]

            dead = entity.update(move)

            #print(dead)

            if dead:

                dead = 1

                self.universe_entities.remove(entity)

        for entity in self.particules:

            entity.update(move)

        if graphic:

            Universe.draw(self)

        return dead

    def draw(self):

        # background

        pyg_down = pygame.Rect(0, ground, screen_width, screen_height-ground)

        pyg_up = pygame.Rect(0, 0, screen_width, ground)

        pygame.draw.rect(screen, self.low_color, pyg_down)

        pygame.draw.rect(screen, self.up_color, pyg_up)

        Universe.update_colors(self)

        for entity in self.universe_entities:

            if not entity.collide_safe:

                entity.draw()

        for partic in self.particules:

            partic.draw()

    def update_colors(self):

        if (self.up_color[self.selected_color[0]]+self.selected_color[1] < 50) or (self.up_color[self.selected_color[0]]+self.selected_color[1] > 255):

            self.selected_color[0] = random.randint(0, 2)

            if random.randint(0, 1) == 0:

                self.selected_color[1] = -1

            else:

                self.selected_color[1] = 1

        else:

            facteur = 1

            self.up_color[self.selected_color[0]] = round(self.up_color[self.selected_color[0]]+self.selected_color[1]/facteur, 2)

            self.low_color[self.selected_color[0]] = round(self.low_color[self.selected_color[0]]+self.selected_color[1]/facteur, 2)

    def collides_with(self, player):

        #self.universe_entities.append(Particule(player.x, player.x, [0, 0], RED))

        to_return = []

        for entity in self.universe_entities:

            if (not entity.collide_safe) and (entity.x < 200):

                collision = entity.collides_with(player)

                if collision == 2:  # rect_circle collision : 1 x_line (dead), 2 y_line -> normal case (ball falling on block)

                    to_return.append(entity)

                elif collision == 1:  # dead

                    to_return.append(2)

        return to_return


class Entity:

    def __init__(self, x, y, vector, shape, static=0, deadly=0, of_importance=1):

        self.x = x

        self.y = y

        self.vector = vector

        self.shape = shape  # 0 stands for circle, 1 for rectangle

        self.static = static  # doesn't mean it's not moving (vector [0, 0]) but that it's a terrain entity that we don't care if it's moving in (collision dealing) or (out check)...

        self.deadly = deadly

        self.collide_safe = 0

        self.of_importance = of_importance

    def update(self, bonus_vector=0):

        Entity.update_coors(self, bonus_vector)

    def update_coors(self, bonus_vector):
        """ updates the coors of the enity """

        self.x += self.vector[0]-bonus_vector[0]

        self.y += self.vector[1]-bonus_vector[1]

    def is_out(self):

        if not self.static:

            if (self.y > screen_height):

                return True                


class Rectangle(Entity):
    """ An entity in cicrle shape, for example the players """

    def __init__(self, x, y, vector, width, height, static=0, collide_safe=0, of_var_importance=1):

        Entity.__init__(self, x, y, vector, 1, static=static, of_importance=of_var_importance)  # shape one is a rect

        self.height = height

        self.width = width

        if random.randint(0, 40) == 0:

            self.color = get_random_color()

        else:

            self.color = [0, 0, 0]

        self.bordure_color = [255, 255, 255]

        self.collide_safe = collide_safe

    def collides_with(self, entity):
        """ Checks if the circle is colliding with a given entity """

        if entity.shape == 0:  # circle and rectangle colliding

            collision = collide_circle_to_rect((entity.x, entity.y), entity.radius, [self.x, self.y, self.width, self.height])

            if (collision == 2):

                return 2

            elif collision != None:  # dead

                return 1

        elif entity.shape == 1:  # two rectangles colliding

            return collide_rect_to_rect([self.x, self.y, self.width, self.height], [entity.x, entity.y, entity.width, entity.height])

    def update(self, bonus_vector=0):

        Entity.update_coors(self, bonus_vector)

        return Rectangle.is_out_left(self)

    def is_out_left(self):

        return (self.x+self.width) < 0

    def draw(self):

        pygame.draw.rect(screen, self.color, pygame.Rect(self.x, self.y, self.width, self.height))

        pygame.draw.rect(screen, self.bordure_color, pygame.Rect(self.x, self.y, self.width, self.height), 3)


class Bille:

    def __init__(self, x, y, vector, static, gravity, jump, layer_nb, layr_size, brain=0):

        Entity.__init__(self, x, y, vector, 0, static=static)  # shape zero is a circle

        self.radius = player_radius

        self.color = get_random_color()

        self.jump_amount = jump

        self.gravity = gravity  # 10**-6 so that it doesn't pass by zero on the jump maxima, which would enable to spam auto-jump  # -20 and 1.2 fit well

        self.layer_nb = layer_nb

        self.layer_size = layer_size

        if brain:

            self.brain = brain

        else:

            self.brain = Network(1, layer_nb, layer_size, 1)  # creates a neural network with two inputs, some hidden inputs and an output (jump or not)

        self.points = 0

    def draw(self):

        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

    def update(self, graphic, universe, y_move, inputs):

        Bille.think(self, inputs)

        # first updates coors to correct them if colliding in update_vector
        self.y += self.vector[1] - y_move

        dead = Bille.update_vector(self, universe)

        if not dead:  # if already dead, useless to check

            dead = Entity.is_out(self)

        if graphic:

            Bille.draw(self)

        if dead:

            return -1

    def think(self, inputs):

        inputs = np.array(inputs)

        output = self.brain.feedforward(inputs)

        if output[0] > 0.5:

            Bille.jump(self)

    def update_vector(self, universe):
        # linked to the jump function, and to collisions with other entities (mainly terrain)

        collision = universe.collides_with(self)

        for stuff in collision:

            if stuff == 2:  # dead

                return 1

            else:

                if self.y != stuff.y-self.radius:

                    self.y = stuff.y-self.radius

                if self.vector[1] > 0:

                    self.vector[1] = 0

        if collision == []:

            self.vector[1] += self.gravity

    def jump(self):

        if (self.vector[1] == 0):

            self.vector[1] = -self.jump_amount

    def collides_with(self, entity):
        """ Checks if the circle is colliding with a given entity """

        if entity.shape == 0:  # two circles colliding

            return collide_circle_to_circle((self.x, self.y), self.radius, (entity.x, entity.y), entity.radius)

        elif entity.shape == 1:  # circle and rectangle colliding

            return collide_circle_to_rect((self.x, self.y), self.radius, [entity.x, entity.y, entity.width, entity.height])

        elif entity.shape == 2:  # circle and triangle colliding

            return collide_circle_to_triangle((self.x, self.y), self.radius, [entity.point1, entity.point2, entity.point3])

    def copy(self):

        return Bille(start_pos, ground-player_radius, [vitesse, 0], 0, self.gravity, self.jump_amount, self.layer_nb, self.layer_size, self.brain)

    def mutate(self, ecart=1):

        self.brain.mutate(ecart)


class Triangle(Entity):

    def __init__(self, point1, point2, point3, vector, color):

        Entity.__init__(self, point1[0], point1[1], vector, 2, 1)

        self.color = color

        self.point1 = point1

        self.point2 = point2

        self.point3 = point3

    def collides_with(self, entity):

        if entity.shape == 0:  # circle and triangle colliding

            return ((self.x, self.y), self.radius, [entity.point1, entity.point2, entity.point3])


def main(inputs):

    global player

    # Variables

    gravity, jump, pop_len, layer_nb, layer_size, mutation_rate = inputs

    generation = 0

    keep_training = 1

    # defining start population

    if input("1) Start with random population\n2) Load existing population\n") == "1":

        billes = []

        for x in range(pop_len):

            billes.append(Bille(start_pos, ground-player_radius, [vitesse, 0], 0, gravity, jump, layer_nb, layer_size))

        players_pop = Population(billes, 1, mutation_rate, lambda x:x**2)

        print("Random population generated")

    else:

        billes = load_pop()

        players_pop = Population(birds, 1, mutation_rate, lambda x:x**2)

        print("Population succesfully loaded")

    # Training loop

    train_pop = True

    while train_pop:

        generation += 1

        # game loop

        # class instances

        universe = Universe()

        # variables

        play = True

        graphic = 1

        compteur = 0

        points = 0

        #y_compensated = 0

        y_compensation = get_coef(universe, billes[0].vector[0])

        print("Génération : ", generation, end=" ; ")

        start_time = time.time()

        while play:

            compteur += 1

            update_terrain(universe)

            for event in pygame.event.get():

                if event.type == pygame.QUIT:

                    play = False

            # updating terrain (universe)

            move = [billes[0].vector[0], y_compensation]

            move[0] += compteur/100

            if move[0] > max_speed:

                move[0] = max_speed

            destroyed_block = universe.update(graphic, move)

            if destroyed_block:

                points += 1

                y_compensation = get_coef(universe, move[0])

            # draws stats

            aff_txt("points : "+str(points), 0, 0, color=YELLOW)

            aff_txt("generation : "+str(generation), 0, 50, color=YELLOW)

            # updating players (billes)

            # defining input for the neural network

            current_index = 3

            current_y_block = universe.universe_entities[current_index].y

            index = 1

            next_block = universe.universe_entities[current_index+index]

            while not(next_block.of_importance):

                index += 1

                next_block = universe.universe_entities[current_index+index]

            if next_block.collide_safe:  # if it's a hole

                next_y = next_block.y-cote_bloc

            # if there is an obstacle
            elif universe.universe_entities[current_index+index].x == universe.universe_entities[current_index+index+1].x:

                next_y = next_block.y-cote_bloc

            else:

                next_y = next_block.y

            diff_y = current_y_block-next_y

            inputs = [round(set_val_to_different_array([-50, 50], [-1, 1], diff_y), 3)]

            for index in range(len(billes)-1, -1, -1):

                player = billes[index]

                if player.update(1, universe, y_compensation, inputs) == -1:

                    player.points = compteur

                    billes.remove(player)

            # stoping game if need be

            if billes == []:

                play = False

    ##        if compteur % 60 == 0:
    ##
    ##            print(clock.get_fps())

            pygame.display.update()

            #clock.tick(60)

        # learning settings (like keep going or not..)

        print("temps :", round(time.time()-start_time, 2))

        keep_training -= 1

        if not keep_training:

            train_pop = input("q = quitter\n")!="q"

            if train_pop:

                keep_training = int(input("generation number:\n"))

        if train_pop:

            players_pop.evaluate()

            players_pop.evolve()

            billes = players_pop.pop.copy()

    if input("1) Save population\n") == "1":

        save_pop(bird_pop.pop)

        print("Population saved")

    else:

        print("Population not saved")


start_pos = 100

player = 0

player_radius = 30

cote_bloc = 50

vitesse = 6

max_speed = vitesse

ground = screen_height-200


if __name__ == "__main__":

    # gravity and jump shouldn't be too high else creates bugs (collision might be detected later because of bigger numbers being involved

    gravity = 0.7+10**-6

    jump = 12

    pop_len = 100

    layer_nb, layer_size = 1, 2

    mutation_rate = 8

    main([gravity, jump, pop_len, layer_nb, layer_size, mutation_rate])
