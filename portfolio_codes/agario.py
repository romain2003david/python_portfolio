# Imports


from pig_tv import *

import random

import math

import time


# Functions


# files

def save_points(points):

    with open("points_agario.txt", "a") as file:

        file.write(">"+str(points)+"<\n")


def set_file():

    with open("points_agario.txt", "a") as file:

        file.write("#"+time.asctime(time.localtime(time.time()))+"#\n")

    file = open("products_agario.txt", "a")

    file.close()


# else
def steer(x, y, target):

    distance_x = target[0] - x

    distance_y = target[1] - y

    total = abs(distance_x) + abs(distance_y)

    if total:

        distance_x /= total

        distance_y /= total

    else:

        distance_x = 0

        distance_y = 0

    return [distance_x, distance_y]


def get_dist(x1, x2, y1, y2):

    return math.sqrt((x2-x1)**2 + (y2-y1)**2)


def follow(x, y, target):

    n_vector = [(x-target[0])*-1, (y-target[1])*-1]
    return n_vector


def get_randomized_normalized_vector(norme=1, up=0):

    vect = [random.randint(-100, 100), random.randint(-100, (1*up or 100))]

    if vect == [0, 0]:

        vect = [1, 1]

    total = abs(vect[0])+abs(vect[1])

    return [vect[0]/total, vect[1]/total]


def set_pause():

    panneau_play = Panneau("", screen_width//2-300, 300, 200, 200, color=GREY, image=draw_play, image_coors=[100, 100])

    panneau_quit = Panneau("", screen_width//2+100, 300, 200, 200, color=GREY, image=draw_quit, image_coors=[72, 70])

    choix = 0

    while choix == 0:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                choix = 1

                return 1

            elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):

                mouse_pos = pygame.mouse.get_pos()

                if panneau_play.clicked(mouse_pos):

                    choix = 1

                    return

                if panneau_quit.clicked(mouse_pos):

                    choix = 1

                    return 1

            screen.fill(BROWN)

            panneau_play.draw()

            panneau_quit.draw()

            pygame.display.update()


def draw_play(x, y, add):

    thickness = 0

    x += add[0]

    y += add[1]

    size = 30

    pygame.draw.polygon(screen, GREEN, ((x-size, y-size), (x+size, y), (x-size, y+size), (x-size, y-size)), thickness)


def draw_pause(x, y, add):

    x += add[0]

    y += add[1]

    rect1 = pygame.Rect(x, y, 5, 20)

    rect2 = pygame.Rect(x+10, y, 5, 20)

    pygame.draw.rect(screen, WHITE, rect1)

    pygame.draw.rect(screen, WHITE, rect2)



def draw_quit(x, y, add):

    thickness = 0

    x += add[0]

    y += add[1]

    size = 66  # divisible par 3

    rect = pygame.Rect(x, y, size, size)

    pygame.draw.rect(screen, RED, rect)

    door = pygame.Rect(x+size//3, y+size, size//3, -size//3)

    pygame.draw.rect(screen, BLACK, door)

    pygame.draw.polygon(screen, RED, ((x, y), (x+size//2, y-size//2), (x+size, y), (x, y)), thickness)


# Classes


class Panneau:

    def __init__(self, contenu, x, y, largeur=200, hauteur=50, color=(255, 255, 255), font_size=30, image=0, image_coors=[0, 0]):

        self.largeur = largeur

        self.x = x

        self.hauteur = hauteur

        self.y = y

        self.pyg_rect = pygame.Rect(self.x, self.y, self.largeur, self.hauteur)

        bordure = 5

        self.pyg_cadre = pygame.Rect(self.x+bordure, self.y+bordure, self.largeur-2*bordure, self.hauteur-2*bordure)

        self.contenu = contenu

        self.color = color

        self.font_size = font_size

        self.image = image

        self.image_coors = image_coors

    def draw(self, contenu_special=None, several_lines=None):

        pygame.draw.rect(screen, BLACK, self.pyg_rect)

        pygame.draw.rect(screen, self.color, self.pyg_cadre, 3)

        if contenu_special != None:

            txt = self.contenu+str(contenu_special)

            aff_txt(txt, self.x+15, self.y+10, self.color, taille=20)

        elif several_lines != None:

            for line in range(len(self.contenu)):

                if line == several_lines-1:

                    aff_txt(self.contenu[line], self.x+15, self.y+10+line*15, YELLOW, taille=20)

                else:

                    aff_txt(self.contenu[line], self.x+15, self.y+10+line*15, self.color, taille=20)

        else:

            txt = self.contenu

            aff_txt(txt, self.x+20, self.y+30, self.color, self.font_size)

        if self.image:

            self.image(self.x, self.y, self.image_coors)

    def clicked(self, pos):
        """ Si le bouton est appuye, active la fonction """

        return (self.pyg_rect.collidepoint(pos))


class Brain:

    def __init__(self):

        self.Network = 0

        self.vector = get_randomized_normalized_vector()

    def get_vect(self):

##        value = 0.01
##
##        nbr = random.randint(0, 1)
##
##        anti_nbr = (nbr-1) * -1
##
##        self.vector[nbr] += value
##
##        self.vector[anti_nbr] -= value

        return self.vector
        

class UniverseEntity:

    def __init__(self, player=0):

        if not player:

            self.x = random.randint(0, size*un_square_size)

            self.y = random.randint(0, size*un_square_size)

        else:

            self.x = int(screen_width/2)

            self.y = int(screen_height/2)

        self.player = player

        self.masse = self.radius*math.pi*2

    def adapt_to_player(self, vector):

        self.x += vector[0]

        self.y += vector[1]

    def collides_with(self, entit):

        dist = get_dist(self.x, entit.x, self.y, entit.y)

        concerned = [self, entit]

        if concerned[0].radius == concerned[1].radius:  # does nothing

            return

        min_ball = min(concerned, key=lambda x: x.radius)

        min_indx = concerned.index(min_ball)

        max_indx = (min_indx-1) * -1

        sum_rads = self.radius + entit.radius

        if dist < sum_rads:  # the two circles are colliding

            if dist <= (sum_rads - min_ball.radius):  # The smaller ball is absorbed

                concerned[max_indx].eat(concerned[min_indx].masse)  # the biggest entity eats the smallest one

                return concerned[min_indx]  # the smallest one will be destroyed

            else:  # just draws the biggest circle on top of the other

                concerned[max_indx].draw()

    def update(self):

        UniverseEntity.off_space(self)

        return UniverseEntity.locate_ingrid(self)

    def off_space(self):

        if self.x < 0:

            self.x = 0

        elif self.x > size*un_square_size:

            self.x = size*un_square_size

        if self.y < 0:

            self.y = 0

        elif self.y > size*un_square_size:

            self.y = size*un_square_size

    def locate_ingrid(self):

        squares = []

        #  roughly in which squares the circle might be

        look_at = self.radius // un_square_size  # how many square to check each side (numbre to check = (x*2)**2)

        #  loop that will take a look in which grid squares the circle is, by comparing distance to radius

        for x in [-look_at, look_at]:

            for y in [-look_at, look_at]:

                #if get_dist(

                n_square = [int(self.x + self.radius*x)//un_square_size, int(self.y + self.radius*y)//un_square_size]

                if (0 < n_square[0] < size) and (0 < n_square[1] < size) and (not n_square in squares):  # the square is in the grid and is not already in the saved squares (adding the radius does not necessarily change the circle of square)

                    squares.append(n_square)

        return squares


class Entity(UniverseEntity):

    def __init__(self, player=0):

        self.constante_speed = 20

        self.radius = 10

        UniverseEntity.__init__(self, player)

        self.brain = 0

        self.color = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]

        if not player:

            self.brain = Brain()

        else:

            self.color = RED

        self.speed = Entity.get_speed(self)

        self.vecteur = [0, 0]

    def update(self, shared_vect, shared_speed):

        if self.player:  # Returns the ball's vector

            self.vecteur = steer(self.x, self.y, pygame.mouse.get_pos())  # the whole universe will move instead of the ball, because it's the player

        else:

            vector = self.brain.get_vect()

            self.x += (vector[0]*self.speed)  # reacts to its brain

            self.y += (vector[1]*self.speed)

            self.x -= (shared_vect[0]*shared_speed)  # reacts to the player's movement (if player goes up, then whole universe goes down instead)

            self.y -= (shared_vect[1]*shared_speed)

        Entity.draw(self)

        return UniverseEntity.update(self)  # return the location in the universe grid

    def get_rad(self):

        return self.masse/(math.pi*2)

    def get_speed(self):

        return -math.sqrt(self.masse) + self.constante_speed

    def eat(self, nmasse):

        if self.player:

            print(nmasse)

        self.masse += nmasse

        self.radius = Entity.get_rad(self)

        self.speed = Entity.get_speed(self)

    def draw(self):

        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(self.radius))
        


class Food(UniverseEntity):

    def __init__(self):

        self.radius = 4

        UniverseEntity.__init__(self)

        self.color = WHITE        

    def update(self, shared_vect, shared_speed):

        self.x -= (shared_vect[0]*shared_speed)  # reacts to the player's movement (if player goes up, then whole universe goes down instead)

        self.y -= (shared_vect[1]*shared_speed)

        Food.draw(self)

        return UniverseEntity.update(self)

    def draw(self):

        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), self.radius)


class Univers:

    def __init__(self, player):

        # Universe 2D grid

        self.un_dimensions = [un_square_size*size, un_square_size*size]  # in pixels, un stands for universe

        self.grid = [[[] for x in range(int(self.un_dimensions[0]/un_square_size))] for y in range(int(self.un_dimensions[1]/un_square_size))]

        # Universe population

        self.pop_inventory = [player]

        taille_pop = 40

        for x in range(taille_pop):

            n_entit = Entity()

            self.pop_inventory.append(n_entit)

        taille_food = taille_pop * 5

        for x in range(taille_food):

            n_entit = Food()

            self.pop_inventory.append(n_entit)

        self.player = player

        self.common_vect = player.vecteur

    def add_to_grid(self, coors, thing):

        for coor in coors:

            if not thing in self.grid[coor[0]][coor[1]]:

                self.grid[coor[0]][coor[1]].append(thing)

    def print_grid(self):

        for row in self.grid:

            for column in row:

                print(column, end=" ")

            print()

    def draw_grid(self):

        for y in range(size):

            for x in range(size):

                pass

    def update(self):
        """ Updates each entity in the universe inventory (the whole pop), and puts each of them in the universe grid in order to check collisions """

        aff_txt("masse : {}".format(int(self.player.masse)), 0, 0, (80, 255, 80), 30)

        aff_txt("rayon : {}".format(int(self.player.radius)), 0, 50, (80, 255, 80), 30)

        self.grid = [[[] for x in range(int(self.un_dimensions[0]/un_square_size))] for y in range(int(self.un_dimensions[1]/un_square_size))]  # sets grid anew : better way to deal with it?

        for entit in self.pop_inventory:

            grid_coors = entit.update(self.player.vecteur, self.player.speed)  # updates the entity vector (to the player) and checks if it hasn't switched grid ; shared are player's vector adn speed, shared by the whole universe's pop

            Univers.add_to_grid(self, grid_coors, entit)

        Univers.draw_grid(self)

        return Univers.collision(self)  # if player is eaten

    def collision(self):
        """ chaud ; well four nested loops isn't that much, or is it? """

##        for row in range(len(self.grid)):
##
##            for col in range(len(self.grid[row])):
##
##                for square_1 in range(len(self.grid[row][col])-1, 0, -1):  # takes is backward, to avoid index_errors following a delete in the list ; tests all circle except the last, which will have been tested with every other circle by then
##
##                    deleted = 0
##
##                    for square_2 in range(square_1-1, -1, -1):  # tests circle with the circles that are after (in that case before, because of the inversed loop) it (those before have already been tested with it)
##
##                        if not deleted:
##
##                            eaten = self.grid[row][col][square_1].collides_with(self.grid[row][col][square_2])  # the function tests if colliding, if one slightly on the other, draws the bigger on top, if one on the other, returns the one eaten, calls bigger.eat 
##
##                            if eaten:
##
##                                if eaten == self.player:
##
##                                    return 1
##
##                                else:
##
##                                    if eaten == self.grid[row][col][square_1]:
##
##                                        deleted = 1
##
##                                    self.grid[row][col].remove(eaten)
##
##                                    if eaten in self.pop_inventory:  # might already have been deleted
##
##                                        self.pop_inventory.remove(eaten)


## Games functions


def end_game(masse):

    screen.fill(BLACK)

    aff_txt("Perdu", 200, 100, WHITE, 70)

    aff_txt("Masse : "+str(masse), 100, 300, WHITE, 70)

    save_points(masse)

    pygame.display.update()

    time.sleep(3)


def game_loop():

    univers = Univers(Entity(1))

    panneau_pause = Panneau("", screen_width//2-50, 0, 100, 100, color=GREY, image=draw_pause, image_coors=[43, 40])

    dead = 0

    compteur = 0

    while not(dead):

        compteur += 1

        for event in pygame.event.get():

            if event.type == QUIT:

                dead = True

            elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):

                mouse_pos = pygame.mouse.get_pos()

                if panneau_pause.clicked(mouse_pos):

                    leave = set_pause()

                    if leave:

                        save_points(univers.player.masse)

                        dead = 1

                        return

        screen.fill((0, 0, 0))

        panneau_pause.draw()

        dead = univers.update()

        pygame.display.update()

        pygame.time.Clock().tick(60)

    end_game(univers.player.masse)


def go_shop():

    print("shop")


def menu():

    shop_button = Panneau("Shop $", 200, 350, 150, 100, YELLOW)

    play_button = Panneau("Play !", 400, 350, 150, 100, BLUE)

    exit_button = Panneau("Exit..", 300, 475, 150, 100, RED)

    choix = 0

    while choix == 0:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                choix = 1

                return

            elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):

                mouse_pos = pygame.mouse.get_pos()

                if shop_button.clicked(mouse_pos):

                    go_shop()

                elif play_button.clicked(mouse_pos):

                    game_loop()

                elif exit_button.clicked(mouse_pos):

                    choix = 1

                    return  # goes back to main, saves file then quit


        screen.fill(BROWN)

        shop_button.draw()

        play_button.draw()

        exit_button.draw()

        aff_txt("Fire & Fury Corp.", 250, 100)

        aff_txt("Nebulous !", 250, 200, taille=50)

        pygame.display.update()

        clock.tick(10)


def main():

    jeu = True

    set_file()

    while jeu:

        jeu = menu()


if __name__ == "__main__":

    size = 14

    un_square_size = 150

    main()
