"""

flappy bird : learning

"""

from pig_tv import *

from Neural_Network import Network

import numpy as np

import pickle


class Bird:

    def __init__(self, radius, jump_height, color, bird_x_pos, layer_nb, layer_size, brain=0):

        self.x = bird_x_pos

        self.y = screen_height//2

        self.radius = radius

        self.y_movement = 0

        self.color_index = color  # for children

        color_dict = {0:get_random_color(),
                      1:RED,
                      2:YELLOW,
                      3:GREEN,
                      4:BLUE}

        self.color = color_dict[color]

        self.jump_height = jump_height

        self.layer_nb = layer_nb

        self.layer_size = layer_size

        if brain:

            self.brain = brain

        else:

            self.brain = Network(2, layer_nb, layer_size, 1)  # creates a neural network with two inputs, some hidden inputs and an output (jump or not)

        self.points = 0

    def update(self, graphic, inputs):

        Bird.think(self, inputs)

        self.y_movement += .4

        self.y += self.y_movement

        if graphic:

            Bird.draw(self)

        if not Bird.in_borne(self):

            Bird.die(self)

            return 1

    def think(self, inputs):

        inputs = np.array(inputs)

        output = self.brain.feedforward(inputs)

        if output[0][0] > 0.5:

            Bird.jump(self)

    def die(self):

        self.color = RED

        Bird.draw(self)

    def in_borne(self):

        return ((self.y > 0) and (self.y < screen_height))

    def jump(self):

        self.y_movement = -self.jump_height

    def draw(self):

        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

    def copy(self):

        return Bird(self.radius, self.jump_height, self.color_index, self.x, self.layer_size, self.layer_nb, self.brain.copy())

    def mutate(self, ecart=1):

        self.brain.mutate(ecart)


class Pilier:

    def __init__(self, inter_ecart, pillar_speed):

        self.x = screen_width

        self.width = 50

        self.y1 = 0

        self.height1 = random.randint(screen_height//2-inter_ecart, screen_height//2+inter_ecart)

        self.inter_ecart = inter_ecart

        self.y2 = self.height1 + inter_ecart

        self.height2 = screen_height - self.y1

        self.color = GREEN

        self.pillar_speed = pillar_speed

    def update(self, graphic):

        self.x -= self.pillar_speed

        if (self.x+self.width) < 0:

            return 1

        if graphic:

            Pilier.draw(self)

    def draw(self):

        up_rect = pygame.Rect(self.x, self.y1, self.width, self.height1)

        low_rect = pygame.Rect(self.x, self.y2, self.width, self.height2)

        pygame.draw.rect(screen, self.color, up_rect)

        pygame.draw.rect(screen, self.color, low_rect)

    def get_middle(self):

        return self.height1+self.inter_ecart//2


def save_pop(pop_array):

    with open("flappy_bird_pop.txt", "ab") as file:

        pickled_array = pickle.dump(pop_array, file)


def load_pop():

    try:

        with open("flappy_bird_pop.txt", "rb") as file:

            pop_array = pickle.load(file)

        return pop_array

    except FileNotFoundError:

        print("No existing saved population")

        raise(SystemExit)

def main(inputs):

    # variables

    radius = 20

    jump_height = 10

    inter_ecart = 180

    pillar_speed = 5

    pillar_spawn_time = 80

    color = 0

    pop_len, mutation_rate, layer_nb, layr_size = inputs

    bird_x_pos = screen_width//6

    graphic = 1

    generation = 0

    keep_training = 1

    # Instances


    # defining start population

    if input("1) Start with random population\n2) Load existing population\n") == "1":

        birds = []

        for x in range(pop_len):

            birds.append(Bird(radius, jump_height, color, bird_x_pos, layer_nb, layr_size))

        bird_pop = Population(birds, 1, mutation_rate, lambda x:x**2)

        print("Random population generated")

    else:

        birds = load_pop()

        bird_pop = Population(birds, 1, mutation_rate, lambda x:x**2)

        print("Population succesfully loaded")

    # Training loop

    train_pop = True

    while train_pop:

        generation += 1

        # game stuff

        points = 0

        compteur = 0

        piliers = []

        new_pillar_time = 1

        # game loop

        play = True

        while play:

            compteur += 1

            new_pillar_time -= 1

            # creating a new pillar if need be

            if not new_pillar_time:

                piliers.append(Pilier(inter_ecart, pillar_speed))

                new_pillar_time = random.randint(pillar_spawn_time-pillar_spawn_time//8, pillar_spawn_time+pillar_spawn_time//8)

            # dealing with screen events

            for event in pygame.event.get():

                if event.type == pygame.QUIT:

                    play = False

            # drawing bg

            screen.fill(BLUE)

            aff_txt("points : "+str(points), 0, 0, color=YELLOW)

            aff_txt("generation : "+str(generation), 0, 50, color=YELLOW)

            # updates pillars

            for x in range(len(piliers)-1, -1, -1):

                pilier_out = piliers[x].update(graphic)

                if pilier_out:

                    del piliers[x]

                    points += 1

                # checks if birds are colliding pillars

                for index in range(len(birds)-1, -1, -1):

                    bird = birds[index]

                    if collide_circle_to_rect([bird.x, bird.y], bird.radius, [piliers[x].x, piliers[x].y1, piliers[x].width, piliers[x].height1]) or \
                       collide_circle_to_rect([bird.x, bird.y], bird.radius, [piliers[x].x, piliers[x].y2, piliers[x].width, piliers[x].height2]):

                           # bird might die because they collided with a pillar

                            bird.points = compteur

                            birds.remove(bird)

                            bird.die()

            # the x distance is the same for every bird
            pillar_x_distance = set_val_to_different_array([0, screen_width-bird_x_pos], [-1, 1], piliers[0].x-bird_x_pos)

            # updating the birds

            for index in range(len(birds)-1, -1, -1):

                bird = birds[index]

                # prepares the input for current bird

                pillar_y_distance = set_val_to_different_array([0, screen_height], [-1, 1], bird.y - piliers[0].get_middle())  # the y distance with middle of inter pillar space

                inputs = [[pillar_x_distance, pillar_y_distance]]

                # update bird, checks if out of screen
                dead = bird.update(graphic, inputs)

                if dead:  # bird might die because they went out screen (beyond screen edges)

                    bird.points = compteur

                    birds.remove(bird)

            play = (birds != [])

            pygame.display.update()

            #clock.tick(60)

        keep_training -= 1

        if not keep_training:

            train_pop = input("q = quitter\n")!="q"

            if train_pop:

                keep_training = int(input("generation number:\n"))

        if train_pop:

            bird_pop.evaluate()

            bird_pop.evolve()

            birds = bird_pop.pop.copy()

    if input("1) Save population\n") == "1":

        save_pop(bird_pop.pop)

        print("Population saved")

    else:

        print("Population not saved")


if __name__ == "__main__":

    pop_len = 100

    mutation_rate = 8

    layer_nb, layr_size = 2, 4

    main([pop_len, mutation_rate, layer_nb, layr_size])
