## Imports

from pig_tv import *

import random

import math

import time


# tests (used during coding)

def draw_circle(x=screen_width//2, y=screen_height//2, radius=20):

    pygame.draw.circle(screen, RED, (x, y), radius)


## Functions

def draw_check(x, y, add):

    thickness = 4

    x += add[0]

    y += add[1]

    pygame.draw.line(screen, GREEN, (x-10, y-10), (x, y), thickness)

    pygame.draw.line(screen, GREEN, (x, y), (x+20, y-30), thickness)


def draw_cross(x, y, add):

    thickness = 4

    x += add[0]

    y += add[1]

    pygame.draw.line(screen, RED, (x-20, y-20), (x+20, y+20), thickness)

    pygame.draw.line(screen, RED, (x-20, y+20), (x+20, y-20), thickness)


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


def switch_values(file_name, seeked_line, replacement):
    """ gets a file name (eg "file.txt") et switches a value at a line"""

    with open(file_name, "r+") as file:

        new_file = file.readlines()

        file.seek(0)

        for line in new_file:

            if line != (seeked_line):  # rewrites the normal lines

                file.write(line)

            else:  # changes the incorrect line

                file.write(replacement)

        file.truncate()


def get_bonus():

    array = []

    products = []

    bornes = [0, 3, 5, 8, 10, 11]

    array_int = [0, 1, 2, 2, 1]  # 0 to do the max, 1 to keep the array and 2 to do the sum

    with open("products.txt", "r") as file:

        for line in file:

            if not int(line[len(line)-3:len(line)-2]) == 0:

                products.append(int(line[1:len(line)-4]))

    for indx in range(len(bornes)-1):

        array.append([x for x in products if bornes[indx]<=x<bornes[indx+1]])

    last_array = []

    for nbr in range(len(array_int)):

        if array_int[nbr] == 0:

            if array[nbr] == []:

                last_array.append(0)

            else:

                last_array.append(max(array[nbr]))

        elif array_int[nbr] == 2:

            if array[nbr] == []:

                last_array.append(0)

            else:

                last_array.append(len(array[nbr]))

        else:

            last_array.append(array[nbr])
        

    return last_array


def get_randomized_normalized_vector(norme=1, up=0):

    vect = [random.randint(-100, 100), random.randint(-100, (1*up or 100))]

    if vect == [0, 0]:

        vect = [1, 1]

    total = abs(vect[0])+abs(vect[1])

    return [vect[0]/total, vect[1]/total]


## Classes


class Balle:

    def __init__(self, vague, allowed, purple, ground, speed):
        """ Constructor of the ball instance. The type of the ball (good/bad) is defined here """

        ## Defines the ball type

        self.type = random.randint(0, 1)

        if random.randint(0, 20) == 0:

            if random.randint(0, 1) == 0:

                self.type = 2

            else:

                self.type = 3

        if allowed != []:  # might create special balls if they are bought

            if random.randint(0, 30) == 0:

                self.type = random.choice(allowed)+4  # will create a special ball

##        if (self.type == 4) or (self.type == 5):
##
##            if not (random.randint(0, 2) == 0):
##
##                self.type = 1  # the purple and rainbow balls are very rare

        ## the more the game is advanced, the more likely it is for black balls to appear instead of the green and the red balls

        if (self.type == 2) or (self.type == 0):  # red or green ball

            max_vague = 100

            if max_vague > vague:  # before max_vague, color swithes sometimes (the more you approach max_vague, the more likely you are to switch)

                prob = (vague-max_vague) * -1

                if random.randint(0, prob) == 0:

                    self.type = 3

            elif max_vague*2 > vague:

                prob = (vague-max_vague)

                if random.randint(0, prob) != 0:

                    self.type = 3

            else:  # After max_vague*2, color switches everytime

                self.type = 3

        # the purple ball disables bad balls

        if (purple) and ((self.type == 0) or (self.type == 3)):

            if random.randint(0, 20) == 0:

                self.type = 2

            else:

                self.type = 1

        # set color

        if self.type == 1:

            self.color = [0, 0, random.randint(100, 255)]

        elif self.type == 2:

            self.color = [0, random.randint(100, 255), 0]

        elif self.type == 3:

            self.color = [0, 0, 0]

        elif self.type == 0:

            self.color = [random.randint(100, 255), 0, 0]

        elif self.type == 4:  # purple

            self.color = [100, 0, 100]

        elif self.type == 5:  # rainbow

            self.color = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 150)]

        elif self.type == 6:  # yellow

            self.color = [random.randint(220, 255), random.randint(220, 255), 0]

        self.radius = 30 - vague // 5

        if self.radius < 10:

            self.radius = 10

        self.vecteur = [random.randint(-10, 10), random.randint(50, 100)]

        total = abs(self.vecteur[0]) + abs(self.vecteur[1])

        self.vecteur[0] /= total

        self.vecteur[1] /= total

        self.x = random.randint(1*(self.vecteur[0]>0) or screen_width//2, screen_width//2*(self.vecteur[0]>0) or screen_width)

        self.y = random.randint(-screen_height//2, 0)

        self.ground = ground

        self.speed = speed

    def update(self, bowl_mask):

        #pygame.draw.circle(screen, BROWN, (int(self.x), int(self.y)), rad)

        # goes forward by vector
        self.x += self.vecteur[0] * self.speed

        self.y += self.vecteur[1] * self.speed

        out = Balle.collision(self, bowl_mask)

        if out:  # out of screen (ball has fallen) or in the bowl

            return out

        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

        pygame.draw.circle(screen, (0, 0, 0), (int(self.x), int(self.y)), self.radius, 3)

        if self.type == 5:

            col = random.randint(0, 2)

            self.color[col] += 2*((self.color[col]<127) or -1)


    def collision(self, pyg_bowl):

        if self.y >= (self.ground - self.radius):  # might collide
            # end screen

            if self.y > screen_height:  # ball has "fallen" from the screen

                return 1

            pyg_balle_mask = pygame.Rect(self.x-self.radius//2, self.y-self.radius//2, self.radius, self.radius)

            if pyg_balle_mask.colliderect(pyg_bowl):

                return 2

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


class Particle:
    """ A bunch particle is launched whenever an important ball is caught """

    def __init__(self, x, y):

        self.x = x

        self.y = y

        self.vect = get_randomized_normalized_vector(up=1)

        self.radius = 15

    def update(self):

        speed = 3

        self.x += self.vect[0] * speed

        self.y += self.vect[1] * speed

        self.vect[1] += 0.03

    def out(self):

        return (self.y > screen_height)




class Coin(Particle):

    def __init__(self, x, y, color=(255, 255, 0)):

        Particle.__init__(self, x, y)

        self.color = color

    def update(self):

        Particle.update(self)

        Coin.draw(self)

        return Coin.out(self)

    def draw(self):

        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

        pygame.draw.circle(screen, BLACK, (int(self.x), int(self.y)), self.radius, 3)


class Heart(Particle):

    def update(self):

        Particle.update(self)

        Heart.draw(self)

        return Heart.out(self)

    def draw(self):
        """ Draws an approximative heart """

        taille = 18

        heart_coors = ((self.x, self.y), (self.x-taille, self.y-taille), (self.x-taille*(2/5), self.y-taille*(4/3)), (self.x, self.y-taille), (self.x+taille*(2/5), self.y-taille*(4/3)), (self.x+taille, self.y-taille), (self.x, self.y))

        pygame.draw.polygon(screen, RED, heart_coors)

        pygame.draw.polygon(screen, BLACK, heart_coors, 3)


class Shield(Particle):

    def update(self):

        Particle.update(self)

        Shield.draw(self)

        return Shield.out(self)

    def draw(self):
        """ Draws an approximative heart """

        taille = 18

        heart_coors = ((self.x, self.y), (self.x-taille, self.y-taille),(self.x, self.y-2*taille), (self.x+taille, self.y-taille), (self.x, self.y))

        pygame.draw.polygon(screen, PURPLE, heart_coors)

        pygame.draw.polygon(screen, BLACK, heart_coors, 3)


class Bowl:

    def __init__(self, hide, green_lifes, ground):

        self.x = pygame.mouse.get_pos()[0]

        self.y = ground

        self.eat = 0

        self.hurt = 0

        self.hide = hide

        self.eat_coin = 0

        self.eat_heart = 0

        self.eat_purple = 0

        self.eat_rainbow = 0

        self.dollar_coor = [550, 50]

        self.children = []

        self.green_lifes = green_lifes

    def move(self, add_x):

        self.x += add_x

    def draw(self):

        if self.eat:

            color = GREEN

            self.eat -= 1

        else:

            color = YELLOW

        if self.hurt:

            color = RED

            self.hurt -= 1

        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), 50)

        pyg_hide = pygame.Rect(self.x-50, self.y-50, 100, 50)

        pygame.draw.rect(screen, self.hide, pyg_hide)

        if self.eat_coin:

            self.eat_coin = 0

            for x in range(5):

                self.children.append(Coin(self.x, self.y))

        if self.eat_heart:

            self.eat_heart = 0

            for x in range(self.green_lifes):

                self.children.append(Heart(self.x, self.y))

        if self.eat_purple:

            self.eat_purple = 0

            for x in range(5):

                self.children.append(Shield(self.x, self.y))

        if self.eat_rainbow:

            self.eat_rainbow = 0

            for x in range(5):

                self.children.append(Coin(self.x, self.y, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))))

        for child in range(len(self.children)-1, -1, -1):  # takes it in reverse to be able to remove the coins once the're out of the square

            out = self.children[child].update()

            if out:

                del self.children[child]


class BackGround:

    def __init__(self, nbr, ground):

        self.nbr = nbr

        if nbr == 0:

            self.color = BROWN

        elif nbr == 1:

            self.color = [0, 0, 130]  # dusk

            self.sun_coor = ((screen_width//3)*2, ground-100)

        else:

            self.color = [0, 0, 0]  # dégradé

        self.ground = ground

    def draw(self):

        screen.fill(self.color)

        if self.nbr == 1:

            pygame.draw.rect(screen, [0, 0, 40], pygame.Rect(0, 0, screen_width, self.sun_coor[1]))

            sun_radius = 50

            pygame.draw.circle(screen, DARK_ORANGE, self.sun_coor, sun_radius)

            pygame.draw.rect(screen, [0, 0, 130], pygame.Rect(self.sun_coor[0]-sun_radius, self.sun_coor[1], sun_radius*2, sun_radius))


        
## Game loop functions


def menu(inputs):

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

                    game_loop(inputs)

                elif exit_button.clicked(mouse_pos):

                    choix = 1

                    return  # goes back to main, saves file then quit


        screen.fill(BROWN)

        shop_button.draw()

        play_button.draw()

        exit_button.draw()

        aff_txt("Fire & Fury Corp.", 250, 100)

        aff_txt("Capture the ball !", 125, 200, taille=50)

        pygame.display.update()

        clock.tick(10)


def check_sell(button, argent):

    list_str = ["You are about", "to buy :", "Confirm purchase ?"]

    for x in reversed(button):

        list_str.insert(2, x)

    warning_button = Panneau(list_str, 250, 250, 300, 200)

    money_button = Panneau("Gold : ", 550, 50, 200, 50, YELLOW, 15)

    box_size = 70

    yes_button = Panneau("", 250, 500, box_size, box_size, BLACK, image=draw_check, image_coors=[30, 50])  # gives a function to draw the picture

    no_button = Panneau("", 450, 500, box_size, box_size, BLACK, image=draw_cross, image_coors=[35, 30])

    choix = 0

    while choix == 0:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                raise(SystemExit)

            elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):

                mouse_pos = pygame.mouse.get_pos()

                if yes_button.clicked(mouse_pos):

                    choix = 1

                    return choix

                elif no_button.clicked(mouse_pos):

                    choix = 0

                    return choix

        screen.fill(BROWN)

        money_button.draw(argent)

        warning_button.draw(several_lines=2+len(button))

        yes_button.draw()

        no_button.draw()

        aff_txt("Shop !", 300, 50, taille=60)

        pygame.display.update()

        clock.tick(10)





def go_shop():

    with open("file.txt", "r") as file:

        argent = 0

        for line in file:

            if line[0] == ">":

                argent += int(line[1:len(line)-2])  # between the two arrows, each transaction is stored ; have to take two before (the back arrow and the \n")

    hauteur_slot_buttons = 200

    slot_picture_coors = [90, 120]

    slot_button_1 = Panneau("", 0, 150, 200, hauteur_slot_buttons, GREY, image_coors=slot_picture_coors)

    slot_button_2 = Panneau("", 200, 150, 200, hauteur_slot_buttons, GREY, image_coors=slot_picture_coors)

    slot_button_3 = Panneau("", 400, 150, 200, hauteur_slot_buttons, GREY, image_coors=slot_picture_coors)

    slot_button_4 = Panneau("", 600, 150, 200, hauteur_slot_buttons, GREY, image_coors=slot_picture_coors)

    slot_buttons = [slot_button_1, slot_button_2, slot_button_3, slot_button_4]

    money_button = Panneau("Gold : ", 550, 50, 200, 50, YELLOW, 15)

    exit_button = Panneau("Back to menu", 40, 40, 150, 90, RED, 15)

    choix = 0

    too_expensive = Panneau("This product is too expensive !", 200, 400, 400, 100, RED, 20)

    expense_active = 0

    index_list_product = 0  # index of the list of the available products

    # array of arrays composed of a description and a price (["product name", price])
    product_list = [[["Normal", "background", "> 0$"], 1],  # already bought (default bg)
                    [["Dusk", "background", "> 500$"], 500],
                    [["Background", "\"dégradé\"", "> 1000$"], 1000],
                    [["Purple", "ball", "> 1500$"], 1500],
                    [["Rainbow", "ball", "> 1500$"], 1500],
                    [["Green ball", "enhacement 1",  "> 500$"], 500],
                    [["Green ball", "enhacement 2",  "> 1000$"], 1000],
                    [["Green ball", "enhacement 3",  "> 1500$"], 1500],
                    [["Blue ball", "enhacement 1",  "> 1000$"], 1000],
                    [["Blue ball", "enhacement 2",  "> 2000$"], 2000],
                    [["Surprise",  "> 2000$"], 2000],
                    
                    ]

    #only_one = [[0, 1]]  # array of arrays : each array contains a list of indexes that can't be activated in the same time

    with open("products.txt", "r") as file:

        for line in file:

            del product_list[int(line[1:len(line)-4])][0][-1]  # deletes the price : the product was already bought

            product_list[int(line[1:len(line)-4])][1] = int(line[len(line)-3:len(line)-2])  # -4 : [";+{active/not}+<+\n] ; [1] : not the price, but {active/not} -> if it's selected for the game {0/1}

    while choix == 0:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                raise(SystemExit)

            elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):

                mouse_pos = pygame.mouse.get_pos()

                for button in slot_buttons:

                    if button.clicked(mouse_pos):

                        prix = product_list[slot_buttons.index(button)+index_list_product][1]

                        if prix < 2:  # already bought product

                            product_list[slot_buttons.index(button)+index_list_product][1] = (product_list[slot_buttons.index(button)+index_list_product][1]-1)*-1

                            switch_values("products.txt", ">"+str(slot_buttons.index(button)+index_list_product)+";"+str(prix)+"<\n", ">"+str(slot_buttons.index(button)+index_list_product)+";"+str(product_list[slot_buttons.index(button)+index_list_product][1])+"<\n")


                        elif argent > prix:

                            sell = check_sell(button.contenu, argent)

                            if sell:

                                with open("file.txt", "a") as file:

                                    file.write(">"+str(prix*-1)+"<\n")

                                with open("products.txt", "a") as file:

                                    file.write(">"+str(slot_buttons.index(button)+index_list_product)+";1"+"<\n")  # is set to active

                                argent -= prix

                                del product_list[slot_buttons.index(button)+index_list_product][0][-1]  # product bought

                                product_list[slot_buttons.index(button)+index_list_product][1] = 1  # -4 : [";+{active/not}+<+\n] ; [1] : not the price, but {active/not} -> if it's selected for the game {0/1}

                        else:

                            expense_active = 20

                if exit_button.clicked(mouse_pos):

                    choix = 1

                    return  # leave the shop (goes back to menu)

            elif event.type == pygame.KEYDOWN:

                if event.key == K_LEFT:

                    if index_list_product > 0:  # The beginning of the list have to contain enough products to display, else useless to go left

                        index_list_product -= 1

                elif event.key == K_RIGHT:

                    if index_list_product < len(product_list)-4:  # The end of the list have to contain enough products to display, else useless to go right

                        index_list_product += 1

        screen.fill(BROWN)

        for index in range(4):  # len(slot_buttons[index_list_product:])

            slot_buttons[index].contenu = product_list[index+index_list_product][0]

            if product_list[index+index_list_product][1] < 2:

                if product_list[index+index_list_product][1]:

                    slot_buttons[index].image = draw_check

                else:

                    slot_buttons[index].image = draw_cross

                slot_buttons[index].draw(several_lines=-1)  # will draw several lines, but no yellow lines

            else:

                slot_buttons[index].image = None

                slot_buttons[index].draw(several_lines=len(product_list[index+index_list_product][0]))  # the argument explicits which line is drawn in YELLOW

        exit_button.draw()

        money_button.draw(argent)

        aff_txt("Shop !", 300, 50, taille=60)

        if expense_active > 0:

            too_expensive.draw()

            expense_active -= 1

        pygame.display.update()

        clock.tick(10)


def set_pause(last_coors):

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

                    pygame.mouse.set_pos(last_coors)

                    choix = 1

                    return

                if panneau_quit.clicked(mouse_pos):

                    choix = 1

                    return 1

            screen.fill(BROWN)

            panneau_play.draw()

            panneau_quit.draw()

            pygame.display.update()


def game_loop(inputs):

    fps, speed, ground = inputs

    ## checking the bought bonuses
    bonuses = get_bonus()

    selected_bg = bonuses[0]

    allowed = []

    if bonuses[1] != []:

        if bonuses[1][0] == 3:

            allowed.append(0)  # purple ball

            if len(bonuses[1]) == 2:

                allowed.append(1)  # rainbow ball


        else:

            allowed.append(1)

    bonus_vie_vert = bonuses[2] + 1

    if bonus_vie_vert == 4:

        bonus_vie_vert = 5

    bonus_point_bleu = bonuses[3] + 1

    if bonuses[4]:

        allowed.append(2)

    ## Variables

    play = True

    trajectoire = [0, 0]

    compteur = 0

    mouse_lock = 0

    balles = []

    vies = 5

    points = 0

    purple = 0  # purple ball caught

    reset_fps = -1

    vague = 0

    message_stay = [0, 0]

    # Class Instances

    bg = BackGround(selected_bg, ground)

    bowl = Bowl(bg.color, bonus_vie_vert, ground)

    panneau_vie = Panneau("Vies : ", 0, 0, color=RED)

    panneau_point = Panneau("Points : ", screen_width-200, 0, color=YELLOW)

    panneau_pause = Panneau("", screen_width//2-50, 0, 100, 100, color=GREY, image=draw_pause, image_coors=[43, 40])

    next_time = random.randint(120, 300)

    while play:

        compteur += 1

        if reset_fps >= 0:

            reset_fps -= 1

            if not reset_fps:

                fps *= 2

        if compteur % next_time == 0:

            balles.append(Balle(vague, allowed, purple, ground, speed))

            compteur = 0

            next_time = random.randint(30-vague//5, 60-vague//5)

            if next_time < 10:

                next_time = 10

            vague += 1

            if vague == 1:

                message_stay = [20, 0]

            if vague == 100:

                message_stay = [20, 1]

            elif vague == 200:

                message_stay = [20, 2]

        if purple:

            purple -= 1

        # Choosing the balls trajectory

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                play = False  # goes back to main, saves file then quit

            elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):

                mouse_pos = pygame.mouse.get_pos()

                if panneau_pause.clicked(mouse_pos):

                    mouse_lock = 1

                    leave = set_pause([bowl.x, bowl.y])

                    if leave:

                        save_points(points)

                        play = False

            elif (event.type == pygame.MOUSEBUTTONUP) and (event.button == 1):

                mouse_lock = 0

            elif (event.type == pygame.MOUSEMOTION):

                if not mouse_lock:

                    translation_x = event.rel[0]

                    bowl.move(translation_x)

                else:

                    mouse_lock = 0

        # Graphic

        bg.draw()

        bowl.draw()

        bowl_mask = pygame.Rect(bowl.x-50, bowl.y, 100, 50)

        panneau_vie.draw(vies)

        panneau_point.draw(points)

        if message_stay[0]:

            message_stay[0] -= 1

            if not message_stay[1]:

                col = GREEN

            elif not message_stay[1] == 1:

                col = RED

            else:

                col = BLUE

            aff_txt("Vague "+str(message_stay[1])+" !", 100, 250, col, 70)
##
        panneau_pause.draw()

        for bal in balles:

            event = bal.update(bowl_mask)

            if event == 1:

                if bal.type == 1:  # une balle bleue est tombee sans avoir ete rattrapee

                    vies -= 1

                    bowl.hurt = 40

                balles.remove(bal)

            elif event == 2:  # Une balle a ete rattrapee

                if bal.type == 1:  # balle bleue

                    points += bonus_point_bleu

                    bowl.eat += 20

                elif bal.type == 2:  # balle verte

                    vies += bonus_vie_vert

                    bowl.eat += 20

                    bowl.eat_heart = 1

                elif bal.type == 3:  # balle noire

                    vies = 0

                elif bal.type == 0:  # balle rouge

                    vies -= 1

                    bowl.hurt = 40

                elif bal.type == 4:  # balle violette

                    purple = fps * 4  # disables bad balls for 4 (?) seconds

                    bowl.eat_purple = 1

                elif bal.type == 5:  # balle arc-en-ciel

                    reset_fps = fps * 3

                    fps = fps // 2

                    bowl.eat_rainbow = 1

                elif bal.type == 6:  # balle jaune

                    points += bonus_point_bleu * 10

                    bowl.eat_coin = 1

                    bowl.eat += 20

                balles.remove(bal)

        if vies == 0:

            play = False

            print_end(points, vague)

        pygame.display.update()

        clock.tick(fps)

    menu(inputs)


def set_file():

    global file

    with open("file.txt", "a") as file:

        file.write("#"+time.asctime(time.localtime(time.time()))+"#\n")

    file = open("products.txt", "a")

    file.close()

    with open("products.txt", "r+") as file:

        if (file.readline() == ""):

            file.write(">0;1<\n")


def print_end(points, vague):

    screen.fill(BLACK)

    aff_txt("Perdu", 200, 100, WHITE, 70)

    aff_txt("Points : "+str(points), 100, 300, WHITE, 70)

    aff_txt("Vague : "+str(vague), 100, 500, WHITE, 70)

    save_points(points)

    pygame.display.update()

    wait()


def save_points(points):

    with open("file.txt", "a") as file:

        file.write(">"+str(points)+"<\n")

## Main loop

def main(inputs):

    ground = screen_height-100

    set_file()

    menu(inputs+[ground])

    #close_file()  useless since using "with" statement


#ground = screen_height-100

#file = 0  # defined later, here to be accessible at global -> local level (in several functions easily)

#panneau = Panneau("SHOOT !", screen_width//2-100, ground)

#panneau_balles = Panneau("Balles : ", 500, ground)


if __name__ == "__main__":

    fps = 60

    speed = 10

    inputs = [fps, speed]

    main(inputs)
