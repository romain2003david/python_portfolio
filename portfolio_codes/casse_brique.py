## Imports

from pig_tv import *

import random

import math

import time


# tests (used during coding)

def draw_circle(x=screen_width//2, y=screen_height//2, radius=20):

    pygame.draw.circle(screen, RED, (x, y), radius)


## Functions

def val_abs(nbr):

    if nbr < 0:

        return -nbr

    return nbr



def aff_txt(contenu, x, y, color=(0, 0, 0), taille=30):
    """ Permet d'afficher un texte """
    myfont = pygame.font.SysFont("monospace", taille, True)
    label = myfont.render(contenu, 1, color)
    screen.blit(label, (x, y))


def collide_circle_to_circle(pos1, rad1, pos2, rad2):

    dist = math.sqrt((pos2[0]-pos1[0])**2 + (pos2[1]-pos1[1])**2)

    max_dist_to_touch = (rad1 + rad2)

    if dist < max_dist_to_touch:  # distance between the two circles lesser than their combined radius

        return True

def collide_circle_to_rect(pos, rad, rect):  # pos[x, y]
    """ detects if a circle collides a rectangle; returns 1 if collides on xline, 2 if collides on yline, 3 if a mix of the txo (arriving in corner), None else """

    # puts rectangle to normal format

    if rect[2] < 0:  # width < 0; x coor is x-width

        rect[0] = rect[0]-rect[2]

        rect[2] = -rect[2]

    if rect[3] < 0:  # height < 0; y coor is y-height

        rect[1] = rect[1]-rect[3]

        rect[3] = -rect[3]

    if pos[0] < rect[0]:  # The x coordinate of the circle is lesser than the left side of the rectangle -> closest x of rect from pos[0] (x centre of circle) is rect[0]
        # now searching closest y
        if pos[1] < rect[1]:  # rect[1] is closest in y to pos[1]

            dist = math.sqrt((rect[0]-pos[0])**2 + (rect[1]-pos[1])**2)

            if dist < rad:

                return 3  # ball arriving in a corner (in that case left low corner)

        elif pos[1] > rect[1]+rect[3]:  # rect[1]+rect[3] (y coor of rect + its width) is closest in y

            dist = math.sqrt((rect[0]-pos[0])**2 + (rect[1]+rect[3]-pos[1])**2)

            if dist < rad:

                return 3  # left up corner

        else:  # closest is pos[1] : don't have to substract in y

            dist = val_abs(rect[0]-pos[0])

            if dist < rad:

                return 1  # ball ariving in the retangle from the left -> should switch (*-1) the x coor of the vector

    elif pos[0] > rect[0]+rect[2]:  # x coor of circle is bigger than x coor of rect + its width
        # now searching closest y
        if pos[1] < rect[1]:  # rect[1] is closest in y

            dist = math.sqrt((rect[0]+rect[2]-pos[0])**2 + (rect[1]-pos[1])**2)

            if dist < rad:

                return 3

        elif pos[1] > rect[1]+rect[3]:  # rect[1]+rect[3] (y coor of rect + its width) is closest in y

            dist = math.sqrt((rect[0]+rect[2]-pos[0])**2 + (rect[1]+rect[3]-pos[1])**2)

            if dist < rad:

                return 3

        else:  # closest is pos[1] : don't have to substract in y

            dist = val_abs(rect[0]+rect[2]-pos[0])

            if dist < rad:

                return 1

    else:  # pos x of circle is in rect

        if pos[1] < rect[1]:  # the ball in under the rect (same x coordinates, y coors of ball < rect's one) -> rect[1] (lowest point of rect (y without the height) is closest in y

            dist = val_abs(rect[1]-pos[1])

            if dist < rad:

                return 2

        elif pos[1] > rect[1]+rect[3]:  # rect[1]+rect[3] (y coor of rect + its width) is closest in y

            dist = val_abs(rect[1]+rect[3]-pos[1])

            if dist < rad:

                return 2

        else:  # the ball is in rect (left_rect<x_ball<right_rect, down_rect<y_ball<up_rect)

            if min((pos[0]-rect[0])/rect[2], 1-(pos[0]-rect[0])/rect[2]) < min((pos[1]-rect[1])/rect[3], 1-(pos[1]-rect[1])/rect[3]):

                return 1

            else:

                return 2


def set_rect_color(tour, y, vie):

    total = tour - (y*tour_add)

    #print(total , tour , y,vie)

    if total % 10 == 0:

        life_proportion = (vie//2 / total)

        if life_proportion > 0.5:

            red = (life_proportion*2-1)*255

            green = 255-red

            blue = 0

        else:

            red = 0

            green = (life_proportion*2)*255

            blue = 255-red

        #print([red, green, blue])

        #return [255, 0, 0]

    else:

        ## first half blue turns into green

        life_proportion = (vie / total)

        if life_proportion > 0.5:

            blue = (life_proportion*2-1)*255

            green = 255-blue

            red = 0

        else:

            blue = 0

            green = (life_proportion*2)*255

            red = 255-green
    #print([red, green, blue])

    return [red, green, blue]


## Classes

class Robot:

    def __init__(self):

        ## coors, dimensions

        self.x = 100

        self.y = ground

        self.largeur = 100

        self.hauteur = screen_height - self.y

        ## colors

        self.color = DARK_BLUE#[random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]

        self.color_arm = self.color.copy()

        for x in range(3):

            self.color_arm[x] += 15

            if self.color_arm[x] > 255:

                self.color_arm[x] = 255

        self.format_color_ball = random.randint(0, 1)

        self.nbr_balles = 1

        self.grid = Board()

        self.last_trajectoire = [(0, 0), (0, 0)]

    def get_membre(self):

        
        if self.x > screen_width // 2:

            side = -1

        else:

            side = 1

        x_middle_body = self.x+self.largeur//2

        y_middle_body = self.y+self.hauteur//2

        arm_width = self.largeur // 4

        arm_height = self.hauteur//2 * -1

        return side, x_middle_body, y_middle_body, arm_width, arm_height

    def draw(self):

        pyg_body = pygame.Rect(self.x, self.y, self.largeur, self.hauteur)

        pygame.draw.rect(screen, self.color, pyg_body)


        # Draws the robot's arm

        side, x_middle_body, y_middle_body, arm_width, arm_height = Robot.get_membre(self)

        pygame.draw.polygon(screen, self.color_arm, ((x_middle_body, y_middle_body), (x_middle_body+self.largeur*side*(2/3), y_middle_body+arm_height), (x_middle_body+self.largeur*side*(2/3), y_middle_body+arm_height-arm_width), (x_middle_body, y_middle_body-arm_width), (x_middle_body, y_middle_body)))

        # Draws the walls..
        self.grid.draw()

    def update_trajectoire(self, trajectoire):
        # Draws the players trajectory

        if trajectoire != [0, 0]:

            taille_voulue = 50

            side, x_middle_body, y_middle_body, arm_width, arm_height = Robot.get_membre(self)

            pygame.draw.line(screen, BROWN, self.last_trajectoire[0], self.last_trajectoire[1])

            taille_ligne = math.sqrt((trajectoire[0])**2+(trajectoire[1])**2)

            facteur = taille_voulue / taille_ligne

            pygame.draw.line(screen, WHITE, (x_middle_body+self.largeur*side*(2/3), y_middle_body+arm_height-arm_width), (x_middle_body+self.largeur*side*(2/3)+trajectoire[0]*facteur, y_middle_body-arm_width+arm_height+trajectoire[1]*facteur))

            self.last_trajectoire = [(x_middle_body+self.largeur*side*(2/3), y_middle_body+arm_height-arm_width), (x_middle_body+self.largeur*side*(2/3)+trajectoire[0]*facteur, y_middle_body-arm_width+arm_height+trajectoire[1]*facteur)]


    def shoot(self, trajectoire, panneau1, panneau2):
        
        global speed

        to_delete = []

        to_draw = []

        screen.fill(BROWN)

        panneau.draw(BLACK)

        panneau_balles.draw(BLUE, self.nbr_balles)

        Robot.draw(self)

        # defines the vector for the balls

        total_trajectoire = val_abs(trajectoire[0])+val_abs(trajectoire[1])

        vecteur = [trajectoire[0]/total_trajectoire, trajectoire[1]/total_trajectoire]

        # defines the starting points for the balls

        side, x_middle_body, y_middle_body, arm_width, arm_height = Robot.get_membre(self)

        default_coors = [x_middle_body+self.largeur*side*(2/3), y_middle_body+arm_height-arm_width]

        # creates the ball array

        balles = [0 for x in range(self.nbr_balles)]

        facteur = 50

        for bal in range(self.nbr_balles):

            these_coors = [default_coors[0]-(bal*vecteur[0]*facteur), default_coors[1]-(bal*vecteur[1]*facteur)]

            balles[bal] = Balle((WHITE*self.format_color_ball or [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]), these_coors[0], these_coors[1], vecteur.copy(), default_coors[1])

        # runs till all balls are out
        while balles != []:

            ## two arrays are used: one (last) to draw the rects where a ball have been, but to do have to wait one tour in the storage array : the balls draw their shadow..

            last_to_draw = to_draw.copy()  # copy the storage

            to_draw = []  # vide[?] the storage

            for event in pygame.event.get():

                if event.type == pygame.QUIT:

                    return

                elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 3):

                    #translation_x = event.rel[0]
                    x_mouse_pos = pygame.mouse.get_pos()[0]

                    speed = int(x_mouse_pos/screen_width * 25)

            #for obj in [self, panneau1, panneau2]:

                #obj.draw()

            for bal in range(len(balles)-1, -1, -1):  # updates (= moves and draws) each ball

                out = balles[bal].update()

                unlock = 1  # if the ball didn't hit any bonus, unlock will stay at one, thus resetting the ball's lock

                if out == 1:

                    balles.remove(balles[bal])

                    unlock = 0  # avoids errors

                elif out:  # checking if not colliding squares in zone

                    for square in out:  # every "suspect"

                        if type(self.grid.board[square[1]][square[0]]) == str:  # is bonus  // the indexes are inversed because if fact x, the columns, are put behind in indexes ## Errors here are probably due to the ball being too far

                            pos1, pos2, rad1, rad2 = [balles[bal].x, balles[bal].y], [square[0]*brick_width+brick_width//2, square[1]*brick_height+brick_height//2], balles[bal].radius, self.grid.radius_bonus

                            if collide_circle_to_circle(pos1, rad1, pos2, rad2):

                                ## deals with the several possible effects

                                if self.grid.board[square[1]][square[0]] == "+":

                                    self.nbr_balles += 1

                                    self.grid.board[square[1]][square[0]] = 0

                                    pygame.draw.rect(screen, BROWN, pygame.Rect(square[0]*brick_width, square[1]*brick_height, brick_width, brick_height))  # bonus disapears

                                    panneau2.draw((0, 0, 255), self.nbr_balles)

                                else:  # bonus that last to the end of the tour

                                    ## put the bonuses to be drawn again

                                    unlock = 0  # the ball won't be unlocked cause it's on a bonus

                                    to_draw.append(square)

                                    if not square in to_delete:

                                        to_delete.append(square)

                                    # part activated only if the ball just landed on the bonus, not if it was already there last tour
                                    if not balles[bal].lock:

                                        balles[bal].lock = 1

                                        if self.grid.board[square[1]][square[0]] == "*":

                                            vectx = random.randint(-100, 100)

                                            vecty = random.randint(-100, 0)

                                            total_trajectoire = val_abs(vectx)+val_abs(vecty)

                                            balles[bal].vecteur[0] = vectx/total_trajectoire

                                            balles[bal].vecteur[1] = vecty/total_trajectoire

                                        elif self.grid.board[square[1]][square[0]] == "-":  # horizontal beam

                                            for x in range(len(self.grid.board[square[1]])):

                                                if (type(self.grid.board[square[1]][x]) == int) and (self.grid.board[square[1]][x] > 0):

                                                    self.grid.board[square[1]][x] -= 1

                                                    ## Draws the updated rect

                                                    if self.grid.board[square[1]][x] > 0:

                                                        self.grid.aff_brique(x, square[1], self.grid.board[square[1]][x])  # draws the new lifes of the rect

                                                        self.grid.aff_bonus(x, square[1], self.grid.board[square[1]][x], 1)  # draws white lifes on a red circle

                                                    else:

                                                        pygame.draw.rect(screen, BROWN, pygame.Rect(x*brick_width, square[1]*brick_height, brick_width, brick_height))

                                        elif self.grid.board[square[1]][square[0]] == "|":  # vetrical beam

                                            for x in range(len(self.grid.board)):

                                                if (type(self.grid.board[x][square[0]]) == int) and (self.grid.board[x][square[0]] > 0):

                                                    self.grid.board[x][square[0]] -= 1

                                                    ## Draws the updated rect

                                                    if self.grid.board[x][square[0]] > 0:

                                                        self.grid.aff_brique(square[0], x, self.grid.board[x][square[0]])  # draws the new lifes of the rect

                                                        self.grid.aff_bonus(x, square[1], self.grid.board[square[1]][x], 1)  # draws white lifes on a red circle

                                                    else:

                                                        pygame.draw.rect(screen, BROWN, pygame.Rect(square[0]*brick_width, x*brick_height, brick_width, brick_height))

                                        elif self.grid.board[square[1]][square[0]] == "!":  # giant / mini ball

                                            balles[bal].last_radius = balles[bal].radius

                                            balles[bal].radius = random.randint(5, 25)

                        elif self.grid.board[square[1]][square[0]] > 0:  # is a brick

                            pos, rad, rect = [balles[bal].x, balles[bal].y], balles[bal].radius, [square[0]*brick_width, square[1]*brick_height, brick_width, brick_height]

                            rect_collision = collide_circle_to_rect(pos, rad, rect)

                            if rect_collision:

                                self.grid.board[square[1]][square[0]] -= 1

                                if self.grid.board[square[1]][square[0]]:  # draws the brick again (the screen is not entirely refreshed, just the balls, therefore, have to redraw what the balls have erased

                                    if not square in to_draw:

                                        to_draw.append(square)  # draws the brick at the end of the tour, to avoid drawing a single brick multiple times

                                else:  # draws an empty place

                                    pygame.draw.rect(screen, BROWN, pygame.Rect(square[0]*brick_width, square[1]*brick_height, brick_width, brick_height))
    
                                if rect_collision == 1:

                                    balles[bal].vecteur[0] *= -1

                                elif rect_collision == 2:

                                    balles[bal].vecteur[1] *= -1

                                else:  # ball collided on a corner

                                    balles[bal].vecteur[1], balles[bal].vecteur[0] = balles[bal].vecteur[0], balles[bal].vecteur[1]

                if unlock:

                    balles[bal].lock = 0

            for square in last_to_draw:

                if self.grid.board[square[1]][square[0]] != 0:

                    if type(self.grid.board[square[1]][square[0]]) == int:  #brick

                        self.grid.aff_brique(square[0], square[1], self.grid.board[square[1]][square[0]])  # draws the new lifes of the rect

                    else:  # bonus

                        self.grid.aff_bonus(square[0], square[1], self.grid.board[square[1]][square[0]])

            pygame.display.update()

            clock.tick(fps_jeu)

        if random.randint(0, 2) == 0:

            self.x = random.randint(100, screen_width-100)

        for square in to_delete:  # deletes the bonuses when the're used

            pygame.draw.rect(screen, BROWN, pygame.Rect(square[0]*brick_width, square[1]*brick_height, brick_width, brick_height))  # bonus disapears

            self.grid.board[square[1]][square[0]] = 0

        return self.grid.create_line()


class Balle:

    def __init__(self, color, x, y, vecteur, default_coor):

        self.color = color

        self.radius = 10

        self.last_radius = 10  # when radius is changed, to draw a fitting shadow

        self.x = x

        self.y = y

        self.vecteur = vecteur

        self.fresh = 1  # the ball has just been created : fresh equals to null when ball pops from the hand, thus can be seen

        self.default_coor = default_coor  # to see when the balls have reached the point when they leave the hand of the robot; they become visible

        self.lock = 0  # lock equals to one when ball on a bonus, is disabled only when the ball leave the bonus, avoid to use it several times

    def update(self):

        if not self.fresh:

            # hides last move

            if self.radius != self.last_radius:

                rad = self.last_radius

                self.last_radius = self.radius

            else:

                rad = self.radius

            pygame.draw.circle(screen, BROWN, (int(self.x), int(self.y)), rad)

        # goes forward by vector
        self.x += self.vecteur[0] * speed

        self.y += self.vecteur[1] * speed

        if self.fresh:

            if self.y < self.default_coor:  # check y coors is sufficient (ball further than robots hand)

                self.fresh = 0  # now ball can be drawn

        else:

            out = Balle.collision(self)

            if out == 1:  # out of screen (ball has fallen)

                return 1

            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

            return out  # None or 2, which means it touched a square

    def collision(self):

        # end screen

        if self.y > screen_height:  # ball has "fallen" from the screen

            return 1

        elif ((self.x < 0) and (self.vecteur[0] < 0)) or ((self.x > screen_width) and (self.vecteur[0] > 0)):

            self.vecteur[0] *= -1

        elif (self.y < 0) and (self.vecteur[1] < 0):  # in case vector has already been inversed but ball still up, which shouldn't arrive but anyway

            self.vecteur[1] *= -1

        # squares

        # roughly locating in the board

        x_loc = int(self.x // brick_width)  # in which grid it is

        y_loc = int(self.y // brick_height)

        x_rest = int(self.x % brick_width)  # is close to another cell of the grid

        y_rest = int(self.y % brick_height)

        if (x_loc == -1):

            x_loc = 0  # case when ball is out of screen
            x_rest = brick_width / 2  # disables x_rest

        elif x_loc == nb_column:

            x_loc -= 1
            x_rest = brick_width / 2

        if y_loc == -1:

            y_loc = 0
            y_rest = brick_height / 2

        elif y_loc == nb_row:

            y_loc -= 1
            y_rest = brick_height / 2

        to_check = [[x_loc, y_loc]]

        if (x_rest < self.radius):

            if not x_loc-1 < 0:

                to_check.append([x_loc-1, y_loc])  # checking if that suspect is not out of the screen

        elif (brick_width-x_rest < self.radius):

            if not x_loc+1 > nb_column-1:

                to_check.append([x_loc+1, y_loc])

        if (y_rest < self.radius):

            if not y_loc-1 < 0:

                to_check.append([x_loc, y_loc-1])

        elif (brick_height-y_rest < self.radius):

            if not y_loc+1 > nb_row-1:

                to_check.append([x_loc, y_loc+1])

        if len(to_check) == 3:

            to_check.append([to_check[1][0], to_check[2][1]])

        return to_check  # returns the cell where the ball is, can't check for itself cause don-t have access to board

class Panneau:

    def __init__(self, contenu, x, y):

        self.largeur = 200

        self.x = x

        self.hauteur = 50

        self.y = y

        self.pyg_rect = pygame.Rect(self.x, self.y, self.largeur, self.hauteur)

        bordure = 5

        self.pyg_cadre = pygame.Rect(self.x+bordure, self.y+bordure, self.largeur-2*bordure, self.hauteur-2*bordure)

        self.contenu = contenu

    def draw(self, color, contenu_special=None):

        pygame.draw.rect(screen, BLACK, self.pyg_rect)

        pygame.draw.rect(screen, color, self.pyg_cadre, 3)

        if contenu_special == None:

            aff_txt(self.contenu, self.x+47, self.y+10, color)

        else:

            aff_txt(self.contenu+str(contenu_special), self.x+15, self.y+10, color, taille=20)


class Board:

    def __init__(self):

        self.nb_column = nb_column

        self.nb_row = nb_row

        self.tour = 0

        self.board = [[0 for x in range(self.nb_column)] for x in range(self.nb_row)]

        Board.create_line(self)

        self.largeur_brique = brick_width

        self.hauteur_brique = brick_height  #+2  devrait se finir quand des briques touchent le bas, pas apres..

        self.radius_bonus = 15

    def get_coor(unite_x, unite_y):

        return unite_x*brick_width, unite_y*brick_height

    def create_line(self):

        self.tour += tour_add

        if self.tour % 10 == 0:

            vie_brick = self.tour * 2

        else:

            vie_brick = self.tour

        perdu = Board.decale_line(self)

        nline = [0 for x in range(nb_column)]

        if random.randint(0, 2) == 0:  # 1 chance out of three

            if random.randint(0, 1) == 0:  # a star or a 

                nline[random.randint(0, nb_column-1)] = "*"

            elif random.randint(0, 1) == 0:  # laser beam

                nline[random.randint(0, nb_column-1)] = "-"  # horizontally

            else:

                nline[random.randint(0, nb_column-1)] = "|"  # vertically

        if random.randint(0, 5) == 0:  # 1 chance out of three

            nline[random.randint(0, nb_column-1)] = "!"

        nline[random.randint(0, nb_column-1)] = "+"

        for x in range(self.nb_column):

            if nline[x] == 0:

                if random.randint(0, 5) > 2:

                    nline[x] = vie_brick  # adds a square to destroy, with "tour" lifes

        self.board.insert(0, nline)

        return perdu

    def decale_line(self):

        a = 0

        for x in self.board[-1]:

            if (type(x) == int) and (x != 0):

                a = 1

        del self.board[-1]

        return a

    def draw(self):
        """ dessine l'echiquier de self.board : briques, vides, bonus """

        for y in range(self.nb_row):

            for x in range(self.nb_column):

                piece = self.board[y][x]

                if piece:

##                    x_coor = 10 + self.largeur_brique*x
##
##                    y_coor = 10 + self.hauteur_brique*y

                    if type(piece) == int:

                        Board.aff_brique(self, x, y, piece)

                    else:

                        Board.aff_bonus(self, x, y, piece)

    def aff_brique(self, x_coor, y_coor, piece):

        y_level = y_coor

        x_coor, y_coor = Board.get_coor(x_coor, y_coor)

        pyg_brique = pygame.Rect(x_coor, y_coor, self.largeur_brique, self.hauteur_brique)

        pyg_cadre = pygame.Rect(x_coor+2, y_coor+2, self.largeur_brique-4, self.hauteur_brique-4)

        color = set_rect_color(self.tour, y_level, piece)

        pygame.draw.rect(screen, color, pyg_brique)

        pygame.draw.rect(screen, BLACK, pyg_cadre, 2) 

        aff_txt(str(piece), x_coor+self.largeur_brique//3+10, y_coor+self.hauteur_brique//3, taille=30)

    def aff_bonus(self, x_coor, y_coor, piece, special=0):

        x_coor, y_coor = Board.get_coor(x_coor, y_coor)

        bonuses = ["*", "+", "-", "|", "!"]

        bonus_coors = [[-10, -13], [-9, -16], [-10, -18], [-10, -13], [-10, -15]]

        bonus_colors = [PURPLE, GREEN, RED, BLUE, YELLOW]

        pos = [int(x_coor+self.largeur_brique//2), int(y_coor+self.hauteur_brique//2)]

        if special:

            pygame.draw.circle(screen, (0, 0, 100), pos, self.radius_bonus+10)

            aff_txt(str(piece), x_coor+self.largeur_brique//2-15, y_coor+self.hauteur_brique//2-15, color=WHITE, taille=30)
 
        else:

            pygame.draw.circle(screen, bonus_colors[bonuses.index(piece)], pos, self.radius_bonus)

            aff_txt(piece, x_coor+self.largeur_brique//2+bonus_coors[bonuses.index(piece)][0], y_coor+self.hauteur_brique//2+bonus_coors[bonuses.index(piece)][1], taille=30)


## Main loop

def main():

    # Variables

    play = True

    mouse_lock = 0

    trajectoire = [0, 0]

    compteur = 0

    # Class Instances

    robot = Robot()

    while play:

        # Choosing the balls trajectory

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                return  # raise(SystemExit)

            elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):

                mouse_pos = pygame.mouse.get_pos()

                mouse_lock = 1

            elif (event.type == pygame.MOUSEBUTTONUP) and (event.button == 1):

                mouse_lock = 0

                if trajectoire != [0, 0]:

                    play = not(robot.shoot(trajectoire, panneau, panneau_balles))

                    trajectoire = [0, 0]

                    compteur = 0

                mouse_pos = pygame.mouse.get_pos()

            elif (event.type == pygame.MOUSEMOTION):

                translation = event.rel

                if mouse_lock:

                    trajectoire[0], trajectoire[1] = trajectoire[0]-translation[0], trajectoire[1]-translation[1]

                    if trajectoire[1] > -10:

                        trajectoire[1] = -10

        # Graphic

        if compteur == 0:

            screen.fill(BROWN)

            panneau.draw(RED)

            panneau_balles.draw(BLUE, robot.nbr_balles)

            robot.draw()

            compteur = 1

        else:

            robot.update_trajectoire(trajectoire)

        pygame.display.update()

        clock.tick(fps)

    screen.fill(BLACK)

    aff_txt("Perdu", 300, 300, WHITE, 70)

    pygame.display.update()


ground = screen_height-100

speed = 3

tour_add = 2

nb_column = 7

nb_row = 8

fps = 60

fps_jeu = 300#int(input("How much fps ?\n"))

brick_width = (screen_width) // nb_column

brick_height = (screen_height) // nb_row

panneau = Panneau("SHOOT !", screen_width//2-100, ground)

panneau_balles = Panneau("Balles : ", 500, ground)

if __name__ == "__main__":

    main()
