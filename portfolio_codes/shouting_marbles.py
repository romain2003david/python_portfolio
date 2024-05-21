from pig_tv import *

import time

from visual_neural_network import *


class Population:

    def __init__(self, taille_population):

        self.taille_population = taille_population

        self.pop = Population.generate_random_pop(self)

        self.chosen = []

    def generate_random_pop(self):

        return [[Player(100, 0), Player(600, 0)] for x in range(self.taille_population)]

    def save(self, name):
        """ Fonction qui sauve les caracteristiques des instances de la population avant de quitter """

        save_path = os.getcwd()

        complete_name = save_path + "\\populations\\" + name + ".txt"

        with open(complete_name, "wb") as file:

            pickle.dump(list(self.pop), file, -1)

    def print_results(fitness_list):

        sum_fit = 0

        for x in fitness_list:

            sum_fit += x

        print(sum_fit/len(fitness_list))

    def run(self, graphic, max_frame=600):

        for index in range(self.taille_population):

            win = game_loop(self.pop[index], max_frame, graphic)

            self.pop[index][0].points = self.pop[index][1].degat - self.pop[index][0].degat

            self.pop[index][1].points = self.pop[index][0].degat - self.pop[index][1].degat

    def evolve(self):

        fitnesses = []

        npop = []

        for couple in self.pop:

            for entit in couple:

                fitnesses.append(entit.points)

        for x in range(len(fitnesses)):

            fitnesses[x] += abs(min(fitnesses))

        fitnesses = set_list_to(fitnesses)

        if type(random_weighted_choice(fitnesses)) == str:

            self.pop = Population.generate_random_pop(self)

        else:

            for couple in range(len(self.pop)):

                npop.append([])

                for x in range(2):

                    if (x%2) == 0:

                        coor = 100

                    else:

                        coor = 600

                    chosen_index = random_weighted_choice(fitnesses)

                    n_IA = Player(coor, 0)

                    n_IA.brain.net.layers, n_IA.brain.net.weights = self.pop[chosen_index//2][chosen_index%2].brain.net.copy()

                    npop[-1].append(n_IA)

            self.pop = npop

            Population.mutate(self, 1)  # mutation rate : 1 out of rate+1

##        #  fills the empty space with new randomly generated entities
##        for x in range(self.taille_population-len(self.pop)):
##
##            self.pop.append([Player(100, 0), Player(600, 0)])

    def mutate(self, mutation_rate):

        for ents in self.pop:

            for ent in ents:

                if random.randint(0, mutation_rate) == 0:

                    rand1 = random.randint(0, len(ent.brain.net.weights)-1)

                    rand2 = random.randint(0, len(ent.brain.net.weights[rand1].data)-1)

                    rand3 = random.randint(0, len(ent.brain.net.weights[rand1].data[rand2])-1)

                    ent.brain.net.weights[rand1].data[rand2][rand3] = random.randint(-10, 10)/10


class Universe:
    """ A quite light class, just to check collisions between the players and the missiles """

    def __init__(self, players):

        self.zero_entities = []

        self.zero_entity = players[1]

        self.one_entities = []

        self.one_entity = players[0]

    def append_balle(self, balle):

        if not ((balle[1][0] == 0) and (balle[1][1] == 0)):

            if balle[0] == 0:

                self.zero_entities.append(Entity(balle[1], balle[2]))

            else:

                self.one_entities.append(Entity(balle[1], balle[2]))

    def update(self, graphic):

        for index in range(len(self.zero_entities)-1, -1, -1):

            entity = self.zero_entities[index]

            if Universe.deal_with_entity(self, entity, self.zero_entity, graphic):  # ball has touched player

                self.zero_entities.remove(entity)

        for index in range(len(self.one_entities)-1, -1, -1):

            entity = self.one_entities[index]

            if Universe.deal_with_entity(self, entity, self.one_entity, graphic):  # ball has touched player

                self.one_entities.remove(entity)

    def deal_with_entity(self, entity, to_check_object, graphic):

        collision = entity.update(to_check_object, graphic)

        if collision == 1:  # touched player

            to_check_object.degat += 1

            return 1

        elif collision == 2:  # out

            return 1

            

class Entity:

    def __init__(self, vector, xy):

        self.vector = vector

        self.x = xy[0]

        self.y = xy[1]

        self.color = RED

        self.radius = 10

    def out_screen(self):

        return (self.x < 0) or (self.y < 0) or (self.x > screen_width) or (self.y > screen_height)

    def update(self, to_check_circle, graphic):

        self.x += self.vector[0]*2

        self.y += self.vector[1]*2

        if collide_circle_to_circle((self.x, self.y), self.radius, (to_check_circle.x, to_check_circle.y), to_check_circle.radius):

            return 1

        elif Entity.out_screen(self):

            return 2

        if graphic:

            Entity.draw(self)

    def draw(self):

        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)


class Brain:

    def __init__(self):

        nbr_input = 6  # vectors and distance of other ball and possibly existing bullet

        hiddens = 4

        nbr_output = 4  # vector of view, moving (True/False), shooting (True/False)

        self.net = Network(nbr_input, hiddens, hiddens, nbr_output)

    def guess(self, universe, index, color):
        """should return an orientation, a speed (moving or not) and a Shoot order (True/False) """

        dist = round(abs(universe.zero_entity.x-universe.one_entity.x) + abs(universe.zero_entity.y-universe.one_entity.y), 2)

        vector = [round(universe.zero_entity.x-universe.one_entity.x, 2), round(universe.zero_entity.y-universe.one_entity.y, 2)]

        if index == 1:

            vector[0] *= -1

            vector[1] *= -1

            if universe.zero_entities != []:

                bullet_dist = round(abs(universe.zero_entities[0].x-universe.zero_entity.x) + abs(universe.zero_entities[0].y-universe.zero_entity.y), 2)

                bullet_vect = [round(universe.zero_entities[0].x-universe.zero_entity.x, 2), round(universe.zero_entities[0].y-universe.zero_entity.y, 2)]

            else:

                bullet_dist = 1000

                bullet_vect = [0, 0]

        else:

            if universe.one_entities != []:

                bullet_dist = round(abs(universe.one_entities[0].x-universe.one_entity.x) + abs(universe.one_entities[0].y-universe.one_entity.y), 2)

                bullet_vect = [round(universe.one_entities[0].x-universe.one_entity.x, 2), round(universe.one_entities[0].y-universe.one_entity.y, 2)]

            else:

                bullet_dist = 1000

                bullet_vect = [0, 0]

        inputs = [vector[0], vector[1], dist, bullet_vect[0], bullet_vect[1], bullet_dist]

        for x in range(len(inputs)):

            if (x == 2) or (x == 5):

                bornes = [0, 800]

            else:

                bornes = [-800, 800]

            inputs[x] = round_between(inputs[x], bornes)

        print(inputs)

        resultat = self.net.feedforward(inputs)

        print(round_list(resultat.to_array(), 2))

        return resultat


class Player:

    def __init__(self, x, human=1):

        self.x = x

        self.y = x

        self.index = ((x==600)*2 or 1) - 1

        self.human = human

        if not self.human:

            self.brain = Brain()

        self.radius = player_radius

        self.vector = [0, 0]

        self.tir = 0

        self.moving = 0

        self.color = get_random_color()

        self.recharge = 0

        self.degat = 0

        self.points = 0

    def update(self, graphic, universe):

        if self.recharge: # loads the gun

            self.recharge -= 1

        if self.human:  # controlled by player

            self.vector = get_vector_to_point((self.x, self.y), pygame.mouse.get_pos(), speed, 3)

        else:  # controlled by AI

            resultat = self.brain.guess(universe, self.index, self.color).to_array()

            #print("AI feedforward result :", resultat)

            self.vector = get_normalized_vector(resultat[:2], speed)

            self.tir, self.moving = resultat[2:]

            if self.tir > 0.5:

                if self.recharge == 0:

                    self.tir = 1

                    self.recharge = recharge_needed

            if self.moving > 0.5:

                self.moving = 1

        if self.tir == 1:  # is activated for a player when clicked, for an AI in update function

            self.tir = 0

            if self.human:

                vector_tir = get_vector_to_point((self.x, self.y), pygame.mouse.get_pos(), speed, 0)

            else:

                vector_tir = self.vector

            return [self.index, vector_tir, [self.x, self.y]]  # a ball is created, with the actual player's vector, and his id

        if (self.moving) and (not Player.out_screen(self)):

            self.x += self.vector[0]

            self.y += self.vector[1]

        if graphic:

            Player.draw(self)

    def out_screen(self):

        return (self.x < 0) or (self.y < 0) or (self.x > screen_width) or (self.y > screen_height)

    def draw(self):

        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

        dist = (self.radius-5)/4

        obj_cote = 28

        pos_obj = [self.x + self.vector[0]*dist, self.y + self.vector[1]*dist]

        pygame.draw.circle(screen, self.color, (int(pos_obj[0]), int(pos_obj[1])), obj_cote)


def go_shop():

    print("Welcome to shop !")


def game_loop(players, max_frame, graphic=1):

    play = True

    universe = Universe(players)

    human_ingame = (players[0].human or players[1].human)

    if (human_ingame) and (players[0].human):

        hplayer_index = 0

    elif (human_ingame):

        hplayer_index = 1

    compteur = 0

    while play:

        compteur += 1

        if compteur > max_frame:

            play = False

        if human_ingame:  # a human player is there (have to check clicks ..

            for event in pygame.event.get():

                if event.type == pygame.QUIT:

                    choix = 1

                elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 3):

                    if not players[hplayer_index].recharge:

                        players[hplayer_index].tir = 1

                        player.recharge = recharge_needed  # gun ain't available for 30 frames

                elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):

                    players[hplayer_index].moving = 1

                elif (event.type == pygame.MOUSEBUTTONUP) and (event.button == 1):

                    players[hplayer_index].moving = 0

        else:

            for event in pygame.event.get():

                if event.type == pygame.QUIT:

                    play = False

        if graphic:

            screen.fill(BLACK)

        for player in players:

            balle = player.update(graphic, universe)

            if balle:

                universe.append_balle(balle)

        universe.update(graphic)

        if graphic:

            pygame.display.update()

        if human_ingame:

            clock.tick(60)

    if (players[0].degat == 0) and (players[1].degat == 0):

        return -1

    else:

        return players.index(min(players, key=lambda x:x.degat))


def main():

    shop_button = Panneau("Shop $", 200, 350, 150, 100, YELLOW)

    play_button = Panneau("Play !", 400, 350, 150, 100, BLUE)

    exit_button = Panneau("Exit..", 300, 475, 150, 100, RED)

    choix = 0

    while choix == 0:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                choix = 1

            elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):

                mouse_pos = pygame.mouse.get_pos()

                if shop_button.clicked(mouse_pos):

                    go_shop()

                elif play_button.clicked(mouse_pos):

                    players = [Player(100), Player(600, 0)]

                    graphic = 1

                    game_time = 6000

                    print("winner :", game_loop(players, game_time, graphic))

                elif exit_button.clicked(mouse_pos):

                    choix = 1

        screen.fill(BROWN)

        shop_button.draw()

        play_button.draw()

        exit_button.draw()

        aff_txt("Fire & Fury Corp.", 250, 100)

        aff_txt("Circle Dash !", 200, 200, taille=50)

        pygame.display.update()

        clock.tick(10)


def train_ai():

    pop = Population(280)

    graphic = 1

    training_time = 450

    choix = 1

    training_loops = 0

    for x in range(training_loops):

        a = time.time()

        pop.run(0, training_time)

        pop.evolve()

        print(time.time()-a, " secondes\n")

    while choix:

        choix_inp = input("quitter : \"q\"\ngraphic : \"v\"\n")

        if choix_inp == "v":

            graphic = 1

        else:

            graphic = 0

        choix = (choix_inp != "q")

        if choix:

            a = time.time()

            pop.run(graphic, training_time)

            pop.evolve()

            print(time.time()-a, " secondes\n")


if __name__ == "__main__":

    player_radius = 30

    speed = 4

    recharge_needed = 60

    main()

    #train_ai()
