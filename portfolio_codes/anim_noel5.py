from pig_tv import *

import random

import math

import time

from get_drawing_coors import Drawing


def list_add(add_thing, added_list):

    to_return = []

    for thing in added_list:

        if type(add_thing) == int:

            if type(thing) == int:

                return [x+add_thing for x in added_list]

            elif type(thing) == list:

                to_return.append([x+add_thing for x in thing])

            else:

                print("Invalid stuff in added_list")

        elif type(add_thing) == list:

            if (len(thing) == len(add_thing)) and (all(isinstance(x, (int, float)) for x in thing)):  # if the sub_lists (thing) of added_list are the same as add_thing, which means the're meant to be added

                to_return.append([thing[index]+add_thing[index] for index in range(len(thing))])

            else:

                to_return.append(list_add(add_thing, thing))

        else:

            print("add_thing is invalid stuff")

    return to_return


def val_abs(nbr):

    if nbr > 0:

        return nbr

    return -nbr

class Particule:

    def __init__(self, largeur, hauteur, forme, vitesse):

        self.gravite = 1
        self.acceleration = 0.08
        self.vitesse = vitesse  # pluie different de neige (+ rapide)

        self.y = random.randint(int(-(screen_height)), 0)

        self.x = random.randint(-(screen_width//2), screen_width*1.5)
        # distance de la camera : plus la particule est proche, plus elle est grosse et va vite

        self.distance = random.randint(60, 180)/100

        self.largeur = largeur / self.distance
        self.hauteur = hauteur / self.distance

        self.forme = forme

        if self.forme:
            self.element = pygame.Rect(self.x, self.y, self.largeur, self.hauteur)
        else:
            self.element = [(int(self.x), int(self.y)), self.hauteur]

        self.vent = 0

    def update(self, vent):

        """ Moves the particle """

        self.gravite += self.acceleration

        self.y += self.gravite * self.distance * self.vitesse

        if self.y > 0:

            trans_x = vent

            self.x += (trans_x/4) * self.distance * self.vitesse

        if self.forme:

            self.element = pygame.Rect(self.x, self.y, self.largeur, self.hauteur)

        else:

            self.element = [(int(self.x), int(self.y)), self.hauteur]

    def off_screen(self):
        """ Checks if the entity is off_screen ; if it is, gets it above the screen """

        if self.y > screen_height:

            self.x = random.randint(-(screen_width//2), screen_width*1.5)

            self.gravite = 1

            self.y = random.randint(int(-(screen_height/6)), 0)


class Snow:

    def __init__(self):

        self.flocons = [Particule(2, 2, 0, 0.6) for x in range(NBR_FLOCON)]

        self.color = (255, 255, 255)

    def update(self, vent, graphic=1):

        """ Moves each particle of snow """

        for flocon in self.flocons:

            flocon.off_screen()

            flocon.update(vent)

            if (flocon.y >= 0) and (0 < flocon.x < screen_width) and graphic:

                pygame.draw.circle(screen, self.color, flocon.element[0], int(flocon.element[1]))


class Lune:

    def __init__(self):

        self.x = int(screen_width*0.7)

        self.y = int(screen_height/4)

        self.rayon = 50

    def draw(self):
        """ Draws the moon """

        pygame.draw.circle(screen, (255, 255, 255), (self.x, self.y), self.rayon)

        pygame.draw.circle(screen, BG, (self.x-30, self.y), self.rayon)        


class StearingObject:

    def __init__(self, precision=2):

        self.round = precision

    def stear(self, x, y, x_obj, y_obj):
        """ Defines a new moving vector """

        self.vector = [x-x_obj, y-y_obj]

    def get_speed(self, x, y, attraction, min_max_distance, max_speed):

        dist_target = math.sqrt((self.vector[0])**2+((self.vector[1])**2))  #int(val_abs(self.vector[0]) + val_abs(self.vector[1]) * 0.8)

        # magnet
        if dist_target:

            if dist_target > min_max_distance:

                self.speed = max_speed

            else:

                self.speed = (dist_target/min_max_distance) * max_speed

        # repulsion : maps the results so as to get the opposite and invert of the "magnet"/attraction case (20 out of 100 -> -80)
        if not attraction:

            self.speed = (self.speed-max_speed)  # times *-1 (repulsion)* -1(mapping) = *1, useless

    def move(self):

        total = val_abs(self.vector[0]) + val_abs(self.vector[1])

        if total:

            add_x = self.speed * (self.vector[0]/total)

            add_y = self.speed * (self.vector[1]/total)

        else:

            add_y = 0

            add_x = 0

        mini = 1/10**self.round  # sth like 0.01 or 0.001 ..

        if (val_abs(add_x) < mini) and (val_abs(add_y) < mini):  # evite les ajouts inutiles

            add_y = 0

            add_x = 0

        self.x += add_x

        self.y += add_y

        return add_x, add_y


class Cadeau(StearingObject):

    def __init__(self, side, is_move):

        StearingObject.__init__(self)

        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

        self.color_bar = []

        self.x = 0

        self.y = 0

        for x in range(3):

            self.color_bar.append((self.color[x]-255)*-1)

        self.cote = random.randint(10, 20)

        self.cote_ruban = self.cote // 5

        self.side = side * -1

        self.target = 0

        self.is_move = is_move

        self.active_repulsion = 1

    def draw(self, x, y):

        if x == None:

            x = self.x

            y = self.y

        pyg_cadeau = pygame.Rect(x, y, self.cote*self.side, self.cote)

        pygame.draw.rect(screen, self.color, pyg_cadeau)

        milieu_x = x+(self.cote//2)*self.side - (self.cote_ruban//2)*self.side

        pyg_ruban_vertical = pygame.Rect(milieu_x, y, self.cote_ruban*self.side, self.cote)

        pygame.draw.rect(screen, self.color_bar, pyg_ruban_vertical)

        milieu_y = y+(self.cote//2) - (self.cote_ruban//2)

        pyg_ruban_horizontal = pygame.Rect(x, milieu_y, self.cote*self.side, self.cote_ruban)

        pygame.draw.rect(screen, self.color_bar, pyg_ruban_horizontal)

    def activate(self, x, y):

        self.x = x
        self.y = y

        self.target = [int(self.x) + random.randint(-100, 100), screen_height-100]

    def go_down(self):

        if self.y > screen_height-100-self.cote:

            return 1

        self.y += 5

    def stear(self, x, y):

        milieu_x = self.x + self.cote//2

        milieu_y = self.y + self.cote//2

        StearingObject.stear(self, x, y, milieu_x, milieu_y)

    def goto(self, x, y, attraction, min_max_distance, max_speed):

        Cadeau.stear(self, x, y)

        Cadeau.get_speed(self, x, y, attraction, min_max_distance, max_speed)

        add_x, add_y = Cadeau.move(self)

        return [add_x, add_y]

    def update(self, bas_traineau):

        min_max_distance_rep = 400

        max_speed_rep = 30

        min_max_distance_atr = 800

        max_speed_atr = 20

        if self.active_repulsion:

            add_ = Cadeau.goto(self, bas_traineau[0], bas_traineau[1], 0, min_max_distance_rep, max_speed_rep)

            if (val_abs(add_[0]) < 1) and (val_abs(add_[1]) < 1):

                self.active_repulsion = 0

                return 1  # kdo going down again

        else:

            kdo_fin = Cadeau.go_down(self)#Cadeau.goto(self, self.target[0], self.target[1], 1, min_max_distance_atr, max_speed_atr)

            if kdo_fin:#(val_abs(kdo_fin[0]) < 1) and (val_abs(kdo_fin[1]) < 1):

                return 2  # almost fallen


class Renne:

    def __init__(self, side, position):

        self.color = BROWN

        self.first_height = 30

        self.hauteur_rel = self.first_height

        self.longueur_laisse = 100*side*-1/2

        self.side = side * -1

        self.largeur = 90

        if position == 0:

            self.longueur_laisse += self.largeur*1.4*self.side

        self.largeur_feet = self.largeur // 10

        self.hauteur = self.largeur * 0.4

        self.basic_saut = -4

        self.saut = self.basic_saut

        self.jump = 1

        self.ready_to_stop = 0

        self.bois = []

        for x in range(2):

            self.bois.append(Renne.create_bois(self))

    def create_bois(self):

        norme = 18

        first_trans = [-norme*self.side, -norme//2]

        scd_trans = [(-norme-norme//5)*self.side, -norme*1.8]

        rapport1 = first_trans[0] / first_trans[1]

        rapport2 = scd_trans[0] / scd_trans[1]

        lines = [[[0, 0], first_trans], [first_trans, scd_trans]]  # structure principale du bois

        # ajoute des ramifications
        for x in range(random.randint(3, 6)):

            len_bois = 10

            if (-norme-norme//5)*self.side < 0:

                pos_x = random.randint((-norme-norme//5)*self.side, 0)

            else:

                pos_x = random.randint(0, (-norme-norme//5)*self.side)

            if norme > val_abs(pos_x):  # la structure principale est compose de deux droites, on verifie sur laquelle se trouve la ramification

                pos_y = pos_x/rapport1

            else:

                pos_y = (-norme)*self.side/rapport1 + (pos_x-(-norme)*self.side)/rapport2

            lines.append([[pos_x, pos_y], [pos_x-random.randint(len_bois-len_bois//2, len_bois+len_bois//2)*self.side, pos_y-random.randint(len_bois-len_bois//2, len_bois+len_bois//2)]])

        return lines

    def draw(self, xy):

        if self.hauteur_rel == self.first_height:

            self.saut = self.basic_saut

            if not self.jump:

                self.ready_to_stop = 1

                self.saut = 0

        if not self.ready_to_stop:

            self.saut += 0.1

        self.hauteur_rel = round(self.saut+self.hauteur_rel, 2)

        x, y = xy

        n_x = x+self.longueur_laisse

        n_y = y+self.hauteur_rel

        pygame.draw.line(screen, RED, (x, y), (n_x, n_y), 3)

        pyg_body = pygame.Rect(n_x, n_y, self.largeur*self.side, self.hauteur)

        pygame.draw.rect(screen, self.color, pyg_body)

        # la queue
        pygame.draw.line(screen, BROWN, (n_x, n_y), (n_x+self.largeur//3*self.side*-1, n_y+self.hauteur), 4)

        x_addin = n_x

        # Draws the reindeer's feets
        for index in range(4):

            if index == 2:

                x_addin = n_x+self.largeur*self.side - self.largeur_feet*self.side

            pyg_jambe = pygame.Rect(x_addin, n_y+self.hauteur, self.largeur_feet*self.side, self.hauteur*0.8)

            pyg_sabot = pygame.Rect(x_addin, n_y+self.hauteur*1.8, self.largeur_feet*self.side, self.hauteur*0.2)

            pygame.draw.rect(screen, BROWN, pyg_jambe)

            pygame.draw.rect(screen, GREY, pyg_sabot)

        # Draws the neck
        pygame.draw.polygon(screen, BROWN, ((x_addin, n_y), (x_addin+(self.largeur//8)*self.side, n_y-self.hauteur//4), (x_addin+(self.largeur//8)*self.side, n_y-self.hauteur//4+10), (x_addin, n_y+14), (x_addin, n_y)))

        # Draws the head
        pyg_head = pygame.Rect(x_addin+(self.largeur//8)*self.side, n_y-self.hauteur//4+9, self.largeur//3*self.side, -20)
        pygame.draw.rect(screen, BROWN, pyg_head)

        # dessine les bois
        x_bois = x_addin+(self.largeur//8)*self.side
        y_bois = n_y-self.hauteur//4+9-20  # top of the head

        for bois in self.bois:

            for line in bois:

                if bois.index(line) > 1:

                    width_pen = 2

                else:

                    width_pen = 3

                coors = list_add([x_bois, y_bois], line)

                pygame.draw.line(screen, GREY, coors[0], coors[1], width_pen)

            x_bois += self.largeur//9*self.side

        # Draws the eye
        pygame.draw.circle(screen, WHITE, (int(x_addin+(self.largeur//8+self.largeur//3-5)*self.side), int(n_y-self.hauteur//4-4)), 3, 2)
        pygame.draw.circle(screen, GREEN, (int(x_addin+(self.largeur//8+self.largeur//3-5)*self.side), int(n_y-self.hauteur//4-4)), 2)

        # smile
        pygame.draw.line(screen, RED, (int(x_addin+(self.largeur//8+self.largeur//3)*self.side), int(n_y-self.hauteur//4+4)), (int(x_addin+(self.largeur//4)*self.side), int(n_y-self.hauteur//4)), 2)

    def activate(self):

        self.jump = 0


class PereNoel:

    def __init__(self, side):

        self.side = side * -1

        self.active_arm = 0

        self.color = RED

        self.largeur = 35

        self.hauteur = -self.largeur*1.7

        self.rennes = [Renne(side, 0), Renne(side, 1)]

    def draw(self, x, y, c):
        """ Draws the pere noel, gets coordinates of high point of \traineau and middle of it """

        # Draws body
        milieu_corps = x + self.side * 10

        bar_side = self.side*-1

        pyg_corps = pygame.Rect(milieu_corps, y, self.largeur*self.side, self.hauteur)
        pygame.draw.rect(screen, self.color, pyg_corps)

        # Draws arms
        if c%50 == 0:  # disabled right now

            self.active_arm = 0#(self.active_arm+1)%2  # exchanges which arm is drawn first

        hauteur = self.hauteur*0.5
        x_arm = 1.4  # to tweak the values easily
        y_arm = 2.8

        y_mult1 = 0.7  # those too.. XD
        y_mult2 = 0.6

        bras = [((milieu_corps+self.largeur*self.side, y+hauteur*y_mult1), (milieu_corps+self.largeur*self.side*1.5*x_arm, y+hauteur*(y_mult1-0.1)), (milieu_corps+self.largeur*self.side*1.5*x_arm, y+hauteur*(y_mult1-0.2*y_arm)), (milieu_corps+self.largeur*self.side, y+hauteur*(y_mult1-0.1*y_arm)), (milieu_corps+self.largeur*self.side, y+hauteur*y_mult1)),
                ((milieu_corps+self.largeur*self.side, y+hauteur*y_mult2), (milieu_corps+self.largeur*self.side*1.5*x_arm, y+hauteur*(y_mult2+0.1)), (milieu_corps+self.largeur*self.side*1.5*x_arm, y+hauteur*(y_mult2+0.2*y_arm)), (milieu_corps+self.largeur*self.side, y+hauteur*(y_mult2+0.1*y_arm)), (milieu_corps+self.largeur*self.side, y+hauteur*0.7))]

        for loop in range(2):

            pygame.draw.polygon(screen, (self.color*loop) or DARK_RED, bras[(self.active_arm+loop)%2])

            self.rennes[loop].draw(bras[(self.active_arm+loop)%2][2])

        mid_x = milieu_corps + self.largeur//2*self.side

        pyg_tete = pygame.Rect(mid_x, y+self.hauteur//1.5, self.largeur//2*self.side, self.hauteur//3.4)

        pygame.draw.rect(screen, BEIGE, pyg_tete)

        pyg_barbe = pygame.Rect(mid_x, y+self.hauteur//1.5, self.largeur//2*self.side, -self.hauteur//4)

        pygame.draw.rect(screen, WHITE, pyg_barbe)

        pygame.draw.line(screen, RED, (mid_x+(self.largeur//6)*self.side, y+self.hauteur//1.3), (mid_x+(self.largeur//2)*self.side, y+self.hauteur//1.6), 3)

        pyg_oeil = pygame.Rect(mid_x+(self.largeur//2-6)*self.side, y+self.hauteur//1.1, 4*self.side, 4)

        pygame.draw.rect(screen, LIGHT_BLUE, pyg_oeil)

    def activate(self):

        for renn in self.rennes:

            renn.activate()


class Paillette:

    def __init__(self, xy):

        self.x, self.y = int(xy[0]), int(xy[1])

        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

        self.radius = random.randint(1, 4)

    def draw(self):

        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)


class Particle(StearingObject):

    def __init__(self, target, attraction=1, couleur=(189, 0, 0)):

        self.target = target

        self.x = 0  # will be activated when needed

        self.y = 0

        self.radius = 3

        if not couleur == (189, 0, 0):

            self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

        else:

            self.color = couleur

        self.attraction = attraction

        StearingObject.__init__(self)

        self.amount = random.randint(0, 180)

        self.ready_to = 0

    def activate(self, x, y):
        """ Particle should probably be created at that precise moment """

        self.x = x

        self.y = y

    def update(self):

        Particle.goto(self)

        return Particle.draw(self)

    def go_down(self):

        self.y += 6

    def goto(self):

        min_max_distance_rep = 100

        max_speed_rep = 30

        min_max_distance_atr = 1000

        max_speed_atr = 15

        Particle.stear(self, self.target[0], self.target[1], self.x, self.y)

        if self.attraction == 0:  # already exploded particle

            Particle.get_speed(self, self.target[0], self.target[1], self.attraction, min_max_distance_rep, max_speed_rep)

            Particle.move(self)

            Particle.go_down(self)

        else:

            Particle.get_speed(self, self.target[0], self.target[1], self.attraction, min_max_distance_atr, max_speed_atr)

            add_x, add_y = Particle.move(self)

            if (add_x == 0) and (add_y == 0):

                self.ready_to = 1

    def out_borne(self):

        if (self.x < 0) or (self.y < 0) or (self.x > screen_width) or(self.y > screen_height):

            return True

    def draw(self):

        if Particle.out_borne(self):

            return 1

        if self.ready_to:

            if self.amount == 0:

                return 2

            self.amount -= 1


        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

class Traineau(StearingObject):

    def __init__(self, side, target, gift_coors):

        StearingObject.__init__(self)

        if side:

            self.x = screen_width+400

            andere_x = -400

        else:

            self.x = -400

            andere_x = screen_width+400

        self.end_target = [andere_x, screen_height // 3.5]

        self.side = ((side*1) or -1)

        self.y = screen_height // 3.5 # Il sera un peu plus bas au global, ca c'est son point en haut

        self.largeur = 150

        self.hauteur = self.largeur // 3

        self.papa_n = PereNoel(self.side)

        self.speed = 3

        self.target = target

        self.target[1] += 3

        self.largeur_dorure = 5

        self.paillettes = []

        nbr_cadeaux = 40

        self.particles = []

        for x in range(len(gift_coors)):

            self.particles.append(Particle(gift_coors[x]))

        self.merry_message = 0  # is activated when particles form the message

        self.cadeaux = []

        for x in range(nbr_cadeaux):  # creates the array of presents in the sleigh

            if x < 20:

                moving = 1

            else:

                moving = 0

            self.cadeaux.append(Cadeau(self.side, moving))

        self.cadeaux_coors_bonus = [(random.randint(-20, 20), random.randint(-15, 15)) for x in range(nbr_cadeaux)]

        self.active_cadeaux = 0

        self.dones = 0

    def draw(self, c):

        milieu_traineau = self.x + self.largeur//2

        for index in range(len(self.cadeaux)):  # draws the presents

            if (not self.active_cadeaux) or (not self.cadeaux[index].is_move):

                pos_y = self.y - 20 + self.cadeaux_coors_bonus[index][1]

                pos_x = milieu_traineau + self.side*self.largeur//3 + self.cadeaux_coors_bonus[index][0]

                self.cadeaux[index].draw(pos_x, pos_y)

            else:

                self.cadeaux[index].draw(None, None)

        pyg_traineau = pygame.Rect(self.x, self.y, self.largeur, self.hauteur)

        pygame.draw.rect(screen, RED, pyg_traineau)

        pygame.draw.rect(screen, YELLOW, pyg_traineau, self.largeur_dorure)

        arriere_x = milieu_traineau + self.side*(self.largeur//2)  # can come from the left or the right

        pygame.draw.polygon(screen, RED, ((arriere_x, self.y), (arriere_x, self.y-self.hauteur), (arriere_x+(self.largeur//3*self.side*-1), self.y), (arriere_x, self.y)))

        pygame.draw.polygon(screen, YELLOW, ((arriere_x, self.y), (arriere_x, self.y-self.hauteur), (arriere_x+(self.largeur//3*self.side*-1), self.y), (arriere_x, self.y)), self.largeur_dorure)

        # le dessous de la luge (pour qu'elle "glisse"
        dessous_traineau = pygame.Rect(self.x, self.y+self.hauteur+self.hauteur//8, self.largeur, self.hauteur//8)

        pygame.draw.rect(screen, LIGHT_GREY, dessous_traineau)

        # le bout incurve du dessus de la luge
        pygame.draw.polygon(screen, LIGHT_GREY, ((milieu_traineau-self.side*(self.largeur//2), self.y+self.hauteur+self.hauteur//8), (milieu_traineau-self.side*(self.largeur//2+self.hauteur//5), self.y+self.hauteur+self.hauteur//8-self.hauteur//4), (milieu_traineau-self.side*(self.largeur//2+self.hauteur//5+self.hauteur//8), self.y+self.hauteur+self.hauteur//8-self.hauteur//4+self.hauteur//8), (milieu_traineau-self.side*(self.largeur//2), self.y+self.hauteur+self.hauteur//4), (milieu_traineau-self.side*(self.largeur//2), self.y+self.hauteur+self.hauteur//8)))                                    # mettre que traineau donne leur coordonnes a chacun ds cadeaux a partir de scoor de coor_init                               

        # les rattaches du dessous au traineau
        for dist in [self.largeur//3, self.largeur*2//3]:

            rattache_pyg = pygame.Rect(self.x+dist, self.y+self.hauteur, 5, self.hauteur//8)

            pygame.draw.rect(screen, LIGHT_GREY, rattache_pyg)

        self.papa_n.draw(milieu_traineau+15*self.side, self.y, c)

        Traineau.draw_paillettes(self, milieu_traineau)

        #pygame.draw.circle(screen, BLACK, (int(milieu_traineau + self.side*(self.largeur//3)), int(self.y+40)), 10)

    def draw_paillettes(self, milieu_x):
        """ Dessine des paillettes autour du traineau """

        mid_x = self.x + self.largeur//2

        mid_y = self.y + self.hauteur//2

        ecart_x = self.largeur//1.5
        ecart_y = self.hauteur//1

##        for zx in range(random.randint(5, 15)):
##
##            for zy in range(random.randint(5, 15)):

        for zx in range(4):

            #zx = random.randint(0, 1)
            zy = random.randint(0, 1)

            # parfois dans les parties gauche-droite, parfois haut-bas, et parfois a droite(bas), parfois a gauche(haut)
            if zx%2 == 0:

                expr1 = int(mid_x-2*ecart_x)
                expr2 = int(mid_x+2*ecart_x)

                expr3 = int(mid_y+2*ecart_y*((zy%2) or -1))
                expr4 = int(mid_y+ecart_y*((zy%2) or -1))

            else:

                expr1 = int(mid_x+2*ecart_x*((zy%2) or -1))
                expr2 = int(mid_x+ecart_x*((zy%2) or -1))

                expr3 = int(mid_y-2*ecart_y)
                expr4 = int(mid_y+2*ecart_y)

            if expr1 > expr2:

                expr1, expr2 = expr2, expr1

            if expr3 > expr4:

                expr4, expr3 = expr3, expr4

            #pygame.draw.rect(screen, RED, pygame.Rect(expr1, expr3, expr2-expr1, expr4-expr3))

            pix_coor = [random.randint(expr1, expr2), random.randint(expr3, expr4)]

            self.paillettes.append(Paillette(pix_coor))

        if len(self.paillettes) > 100:

            self.paillettes = self.paillettes[len(self.paillettes)-100:]

        for paille in self.paillettes:

            paille.draw()

    def create_cadeau(self):

        self.cadeaux.append(Cadeau(self.side, 1))

    def goto(self, x, y, attraction, min_max_distance, max_speed):

        Traineau.stear(self, x, y)

        Traineau.get_speed(self, x, y, attraction, min_max_distance, max_speed)

        Traineau.move(self)

    def move(self):

        add_x, add_y = StearingObject.move(self)

        if ((add_x == 0) and (add_y == 0)) or (self.target == self.end_target):  # quand le traineau est a l'arret, ou est reparti

            milieu_traineau = self.x + self.largeur//2

            if not self.active_cadeaux:  # active les cadeaux, et les reines, qui arretent de sauter

                for index in range(len(self.cadeaux)):

                    if self.cadeaux[index].is_move:

                        pos_x = (milieu_traineau + self.side*self.largeur//3) + self.cadeaux_coors_bonus[index][0]  # (basic pos) + (rel pos of each present)

                        pos_y = self.y - 20 + self.cadeaux_coors_bonus[index][1]

                        self.cadeaux[index].activate(pos_x, pos_y)

                self.papa_n.activate()

                self.active_cadeaux = 1

            for kdo in self.cadeaux:

                if  (kdo.is_move):

                    bas_traineau = (milieu_traineau + self.side*self.largeur//3, self.y+40)

                    done = kdo.update(bas_traineau)

                    if done == 1:  # Presents beginning to fall down : time to send the rockets

                        if not self.merry_message:

                            Traineau.activate_paillettes(self)

                    elif done == 2:  # presents on the ground

                        self.dones += 1

                        if self.dones == 20:

                            self.target = self.end_target  # changes the sleigh targets cause presents are delivered

        if self.merry_message:

            Traineau.update_merry(self)


    def stear(self, x, y):
        """ Defines a new moving vector """

        milieu_traineau = self.x + self.largeur//2

        devant_x = milieu_traineau - self.side*(self.largeur//2+self.hauteur//5)  # can come from the left or the right

        devant_y = self.y + self.hauteur + self.hauteur//4

        self.vector = [x-devant_x, y-devant_y]

    def update(self, c):

        Traineau.goto(self, self.target[0], self.target[1], 1, 100, 3)

        Traineau.draw(self, c)

    def update_merry(self):

        for x in range(len(self.particles)-1, -1, -1):

            explode = self.particles[x].update()

            if explode == 2:  # only 2

                for n in range(20):

                    self.particles.append(Particle(self.particles[x].target, 0, 1))

                    self.particles[-1].x = self.particles[x].x + random.randint(-200, 200)/100

                    self.particles[-1].y = self.particles[x].y + random.randint(-1000, -500)/100

            if explode:  # 1 or 2

                self.particles.remove(self.particles[x])

    def activate_paillettes(self):

        self.merry_message = 1

        for x in self.particles:

            x.activate(self.x, self.y)


def draw_triangle(x, y, add_x, add_y, color, width=0):
    """ Draws a simple triangle with two equal sides, symetric, at given coordinates .. """

    pygame.draw.polygon(screen, set_color(color), ((x, y), (x+add_x//2, y+add_y), (x+add_x, y), (x, y)), width)

class Sapin:

    def __init__(self, x, y):

        self.x = x

        self.y = y

        self.width = 15

        self.height = self.width * -20

        self.sapin = pygame.Rect(self.x, self.y, self.width, self.height)

        self.couleur = DARK_GREEN

        self.wood_color = BROWN

        self.nbr_boules = random.randint(10, 25)

        limites_x = (self.x-20, self.x+self.width+20)  # y area for the baubles

        limites_y = (self.y+self.height//4, self.y+self.height+self.height//16)  # x area for the baubles

        self.boules = [(random.randint(limites_x[0], limites_x[1]), random.randint(limites_y[1], limites_y[0]), (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), random.randint(6, 12)) for x in range(self.nbr_boules)]

    def draw(self):

        # Drawing the trunk

        pygame.draw.rect(screen, self.wood_color, self.sapin)

        #pygame.draw.circle(screen, RED, (self.x+self.width//2, self.y), 10)

        # Drawing the branches

        degrade = 0

        default_size = 70

        bonus_size = 25

        x_coor = self.x+self.width//2

        nbr_triangle = 6

        color = [20+nbr_triangle*6, 60+nbr_triangle*10, 25+nbr_triangle*6]

        y_coor = self.y + self.height

        for triangle in range(nbr_triangle):

            width_triangle = default_size + bonus_size*triangle

            height_triangle = width_triangle // 2.5

            draw_triangle(x_coor-width_triangle//2, y_coor, width_triangle, -height_triangle, color)

            y_coor += height_triangle

            if degrade:

                for c in range(len(color)):

                    if c == 1:

                        color[c] -= 10

                    else:

                        color[c] -= 6
        for boule in range(self.nbr_boules):

            color = self.boules[boule][2]

            posx = self.boules[boule][0]

            posy = self.boules[boule][1]

            radius = self.boules[boule][3]

            pygame.draw.circle(screen, color, (posx, posy), radius)

        #draws a star on top of the tree
        max_y = self.y + self.height - 20
        pos_x = self.x + self.width//2

        norme = 20

        pygame.draw.polygon(screen, REAL_YELLOW, ((pos_x, max_y), (pos_x+norme//1.2, max_y+norme//2), (pos_x, max_y-2*norme), (pos_x-norme//1.2, max_y+norme//2), (pos_x, max_y)))

        pygame.draw.polygon(screen, REAL_YELLOW, ((pos_x, max_y), (pos_x+norme*1.2, max_y-norme), (pos_x-norme*1.2, max_y-norme), (pos_x, max_y)))


class Lampadaire:

    def __init__(self, y):

        self.couleur = GREY

        self.x = random.randint(100, screen_width-100)

        self.y = y

        self.largeur_poto = 15

        self.hauteur_poto = -150

        self.largeur_tete = 35

        self.hauteur_tete = -50

        self.side = (2*(self.x>screen_width//2) or 1) -1

        self.pyg_poto = pygame.Rect(self.x, self.y, self.largeur_poto, self.hauteur_poto)

        self.pyg_poto_tete = pygame.Rect(self.x-10, self.y+self.hauteur_poto, self.largeur_tete, self.hauteur_tete)

        self.pyg_lampe = pygame.Rect(self.x-7, self.y+self.hauteur_poto-3, self.largeur_tete-6, self.hauteur_tete//2)

    def draw(self):

        # Draws the street light

        pygame.draw.rect(screen, self.couleur, self.pyg_poto)

        pygame.draw.rect(screen, self.couleur, self.pyg_poto_tete)

        pygame.draw.rect(screen, YELLOW, self.pyg_lampe)

        # Draw the light around the light

        light_around = 1

        if light_around:

            pixel = [self.x-7, self.y+self.hauteur_poto-3]

            # Draws pixels close to the light brighter -> every pixel in a rectangle of x+100, with x the side of the square of light (+ fifty on each side, (doesn't light above) and below), is brighter, according to it's distance to the central square of light

            brightness = 51

            for side in range(2):  # on each side

                for x in range(1, brightness+1):  # 50 = brightness

                    for y in range(val_abs(self.hauteur_tete//2)):

                        x_abs = side*x or -x

                        if x_abs > 0:

                            x_abs += self.largeur_tete-6

                        pix = pixel.copy()

                        pix[0] += x_abs

                        pix[1] -= y

                        pix_color = screen.get_at(pix)

                        #valide = 1

                        dist = (val_abs(x) - brightness) * -1

                        for col in range(3):

                            if dist + pix_color[col] < 256:

                                pix_color[col] += dist

                            else:

                                pix_color[col] = 255

                        screen.set_at(pix, pix_color)

        

    def get_x_sap(self):

        if self.x > screen_width//2:

            return random.randint(50, screen_width//2-100)

        return random.randint(screen_width//2+100, screen_width-50)


class Colline:

    def __init__(self, x, y, radius):

        self.x = x

        self.y = y

        self.radius = radius

    def draw(self):

        pygame.draw.circle(screen, WHITE, (self.x, self.y), self.radius)

        #pygame.draw.rect(screen, RED, Rect(self.x - self.radius*2, 400, self.radius*4, 20)) # -> surface occupied by the hill

        # Edge at least a little smooth

        dis_x = self.radius

        dis_moins_x = -dis_x // 1.5

        dis_y = -dis_x // 1.15

        for sens in [-1, 1]:

            pygame.draw.polygon(screen, WHITE, ((self.x + self.radius*sens, self.y), (self.x + (self.radius+dis_x)*sens, self.y), (self.x + (self.radius+dis_moins_x)*sens, self.y+dis_y), (self.x + self.radius*sens, self.y)))

    def get_ter(self):

        return [self.x - self.radius*2, self.x + self.radius*2]


class BackGround:

    def __init__(self, y):

        self.y = y

        self.nbr_collines = random.randint(1, 3)  # Le nombre de collines dans le decor

        self.collines = []

        for _ in range(self.nbr_collines):

            self.collines.append(Colline(random.randint(0, screen_width), self.y, random.randint(50, 150)))  # pos x de la colline = abscisse ; radius colline = rayon

    def draw(self):

        pygame.draw.rect(screen, WHITE, pygame.Rect(0, self.y, screen_width, screen_height-self.y))

        for col in self.collines:

            col.draw()
##
##    def get_free_terrain(self):
##
##        free_terrain = [0, screen_width]
##
##        for col in self.collines:
##
##             occ_ter = col.get_ter()

    def update(self):

        pass


def aff_txt(contenu, x, y, color=(0, 0, 0), taille=20):
    """ Permet d'afficher un texte """
    myfont = pygame.font.SysFont("monospace", taille, True)
    label = myfont.render(contenu, 1, color)
    screen.blit(label, (x, y))


def init_coor_cible():

    screen.fill((0, 0, 0))

    aff_txt("Joyeux", 10, 100, (255, 255, 255), taille=170)

    aff_txt("Noël", 120, 300, (255, 255, 255), taille=200)


    draw = Drawing(screen, screen_width, screen_height)

    draw.get_coor((255, 255, 255))

    liste = draw.list

    for x in range(len(liste)-1, 0, -1):

        if not x%100 == 0:

            del liste[x]

    return liste


def main():

    # Variables

    play = True

    compteur = 0

    vent = 0

    vent2 = vent

    ground = screen_height-100

    temps_depart = time.time()

    cibles = init_coor_cible()

    ##
    # Instances

    snow = Snow()

    bg = BackGround(ground)

    lampe = Lampadaire(ground)

    x_sapin = lampe.get_x_sap()

    sapin = Sapin(x_sapin, ground)

    lune = Lune()

    traineau = Traineau(lampe.side, [sapin.x+10, sapin.y], cibles)
    ##

    # runs the snow to dispatch it

    for x in range(100):

        snow.update(int(vent), 0)

    while play:

        compteur += 1

##        if compteur % 60 == 0:
##
##            print(compteur/60, " : ", time.time()-temps_depart)

        if compteur % 800 == 0:  # De temps en temps le vent change

            vent2 = random.randint(-15, 15)

        if vent != vent2:   # Le vent change pas d'un coup : c'est progressif

            if vent2 > vent:

                vent += 0.02

            else:

                vent -= 0.02

        ## GUI (graphic user interphace
        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                raise(SystemExit)

            elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):

                mouse_pos = pygame.mouse.get_pos()

            elif (event.type == pygame.MOUSEBUTTONUP) and (event.button == 1):

                mouse_pos = pygame.mouse.get_pos()

            elif (event.type == pygame.MOUSEMOTION):

                translation = event.rel

        ##
        ## Graphic

        graphic = 1

        if (graphic) or (compteur == 1):

            screen.fill(BG)

            bg.draw()

            lune.draw()

            snow.update(int(vent))

            lampe.draw()

            sapin.draw()

        else:

            snow.update(int(vent))

        if compteur > 40:

            traineau.update(compteur)

        pygame.display.update()

        clock.tick(FPS)


def set_color(col):

    rand = 0

    if rand:

        return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    return col
# Constantes

BG = set_color((0, 0, 50))

WHITE = set_color((255, 255, 255))

BLACK = set_color((0, 0, 0))

RED = set_color((255, 0, 0))

DARK_RED = set_color((150, 0, 0))

YELLOW = set_color((255, 255, 180))

REAL_YELLOW = set_color((255, 255, 0))

BEIGE = set_color((210, 210, 150))

GREEN = set_color((20, 255, 25))

DARK_GREEN = set_color((20, 60, 25))

BROWN = set_color((50, 30, 40))

DARK_BROWN = set_color((20, 0, 10))

GREY = set_color((150, 150, 150))

LIGHT_GREY = set_color((200, 200, 200))

LIGHT_BLUE = set_color((0, 0, 255))

#colors = [WHITE,BLACK,RED,DARK_RED,YELLOW,REAL_YELLOW,BEIGE,GREEN,DARK_GREEN,BROWN,DARK_BROWN,GREY,LIGHT_GREY,LIGHT_BLUE]

NBR_FLOCON = 1000

FPS = 60

##

if __name__ == "__main__":

    main()
