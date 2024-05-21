""" events loop with pause

panneau_pause = Panneau("", screen_width//2-50, 0, 100, 100, color=GREY, image=draw_pause, image_coors=[43, 40])

for event in pygame.event.get():

    if event.type == pygame.QUIT:

        raise(SystemExit)

    elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):

        mouse_pos = pygame.mouse.get_pos()

        if panneau_pause.clicked(mouse_pos):

            leave = set_pause()

            if leave:

                save_points(points)

                play = False

    elif (event.type == pygame.MOUSEBUTTONUP) and (event.button == 1):

        mouse_pos = pygame.mouse.get_pos()


    elif (event.type == pygame.MOUSEMOTION):

        translation = event.rel

    panneau_pause.draw()
"""
from pig_tv import *


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


def draw_cross(x, y, add):

    thickness = 4

    x += add[0]

    y += add[1]

    pygame.draw.line(screen, RED, (x-20, y-20), (x+20, y+20), thickness)

    pygame.draw.line(screen, RED, (x-20, y+20), (x+20, y-20), thickness)


def aff_txt(contenu, x, y, color=(0, 0, 0), taille=30):

    """ Permet d'afficher un texte """
    myfont = pygame.font.SysFont("monospace", taille, True)
    label = myfont.render(contenu, 1, color)
    screen.blit(label, (x, y))


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


def set_color(col):

    rand = 0

    if rand:

        return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    return col

WHITE = set_color((255, 255, 255))

BLACK = set_color((0, 0, 0))

RED = set_color((255, 0, 0))

DARK_RED = set_color((150, 0, 0))

YELLOW = set_color((255, 255, 0))

BEIGE = set_color((210, 210, 150))

GREEN = set_color((20, 255, 25))

DARK_GREEN = set_color((20, 60, 25))

BROWN = set_color((60, 30, 20))

DARK_BROWN = set_color((20, 0, 10))

GREY = set_color((150, 150, 150))

LIGHT_GREY = set_color((200, 200, 200))

BLUE = set_color((0, 0, 150))

LIGHT_BLUE = set_color((0, 0, 255))

DARK_BLUE = set_color([0, 0, 60])

PURPLE = set_color([200, 10, 190])

DARK_ORANGE = set_color([160, 40, 40])



from math import *

def get_speed(m1, v1, m2, v2):

    a = -m2**2-m2*m1

    b = 2*v1*m1*m2 + 2*v2*m2**2

    c = v2**2*m1*m2 - 2*m1*v1*m2*v2 - m2**2*v2**2

    delta = (b**2) - 4*a*c

    # a, b, c and delta seem to be correct

    if delta > 0:

        v4_1 = (-b -sqrt(delta))/ (2*a)

        v4_2 = (-b +sqrt(delta))/ (2*a)

        v3_1 = (m1*v1 + m2*v2 - m2*v4_1) / m1

        v3_2 =(m1*v1 + m2*v2 - m2*v4_2) / m1

        liste_4 = [v4_1, v4_2]

        liste_3 = [v3_1, v3_2]

        good_index = max(liste_3, key=lambda x:abs(v1-x))

        to_return = [liste_4[liste_3.index(good_index)], good_index]

        return to_return

    elif delta == 0:

        v4 = -b / (2*a)

        v3 = (m1*v1 + m2*v2 - m2*v4) / m1

        return v3, v4

    else:

        print("error : non resolvable equation :a : {}, b : {}, c : {}, delta : {}, m1 : {}, v1 : {}, m2 : {}, v2 : {}".format(a, b, c, delta, m1, v1, m2, v2))
        return [0, 0]


def add_square(x):

    return Square(x=x, vector=[0, 0])

def add_moving_square(vect_x, masse):

    return Square(0, vector=[vect_x, 0], color=BLACK, masse=masse)


def signe(nbr):

    if nbr > 0:

        return 1

    elif nbr < 0:

        return -1

    else:

        #print("Non moving stuff is colliding.\nSounds quite strange, doesn't it?")
        return 0


class Square:

    def __init__(self, x=screen_width//2, y=500-50, vector=[0, 0], cote=50, color=(200, 60, 130), masse=1):

        self.x = x

        self.y = y

        self.vector = vector

        self.cote = cote  # negative, to be on top of the ground, and not in/under it

        self.masse = masse

        self.color = color

        self.points = None

        if self.color == (200, 60, 130):

            self.points = 0

        #self.new = 0  # oups

    def update(self, graphic):

        facteur = 1

##        if self.new:
##
##            facteur = 2
##
##            self.new = 1

        self.x += self.vector[0] * facteur

        self.y += self.vector[1] * facteur

        if graphic:

            Square.draw(self)

    def get_color(self):

        if (abs(self.vector[0]) > 2):

            green = 255

        else:

            green = abs(self.vector[0])*120

        return (200, green, 130)

    def draw(self):

        if self.color != (0, 0, 0):

            self.color = Square.get_color(self)

        pyg_rect = pygame.Rect(self.x, self.y, self.cote, self.cote)

        pygame.draw.rect(screen, self.color, pyg_rect)

##        if self.points != None:
##
##            aff_txt(str(self.points), 100, 100)


class Universe:

    def __init__(self, ground):

        self.x = 0

        self.y = ground

        self.pyg_sky = pygame.Rect(self.x, self.y, screen_width, -ground//3)

        self.pyg_earth = pygame.Rect(self.x, self.y, screen_width, screen_height-ground)

        self.ground = ground

    def update(self, squares, graphic, panneaux=0, panneaux2=0):

        if graphic:

            Universe.draw(self, panneaux, panneaux2)

        Universe.deal_collisions(squares)

    def draw(self, panneaux, panneaux2):

        pygame.draw.rect(screen, GREEN, self.pyg_earth)

        if panneaux:

            pygame.draw.rect(screen, BLUE, pygame.Rect(self.x, self.y, screen_width, -self.ground))

            for x in range(len(panneaux)):

                panneaux[x].draw()

            for x in range(len(panneaux2)):

                panneaux2[x].draw()

        else:

            pygame.draw.rect(screen, BLUE, self.pyg_sky)

    def deal_collisions(squares):

        for x in range(len(squares)-1, 0, -1):  # does it inversely, doesn't check last cause already done by the others

            if squares[x].x < 0:

##                if squares[x].points != None:
##
##                    print(squares[x].points)

                squares.remove(squares[x])

                if squares != []:

                    for sq in squares:

                        if sq.points != None:

                            pass#rint(sq.points)

            else:

                if squares[x].x > screen_width:

                    squares[x].vector[0] *= -1

                    if squares[x].points != None:

                        squares[x].points += 1

                for y in range(x-1, -1, -1):

                    pyg_square_1 = pygame.Rect(squares[x].x, squares[x].y, squares[x].cote, squares[x].cote)

                    pyg_square_2 = pygame.Rect(squares[y].x, squares[y].y, squares[y].cote, squares[y].cote)

                    if pyg_square_1.colliderect(pyg_square_2):

                        # Should reset the two square coors so that they don't collide anymore (in real life, as the time is linear, this is not needed, but because the animation is made of frames, it's necessary)

                        xs = [squares[x].x, squares[y].x]

                        vs = [squares[x].vector[0], squares[y].vector[0]]

                        up_x = xs.index(min(xs))

                        down_x = (up_x-1) * -1

                        actor = vs.index(max(vs, key=lambda x: abs(x)))

                        if actor == 0:

                            squares[x].x -= (xs[actor]+(50*(actor==up_x)) - xs[(actor-1)*-1]+(50*(actor==down_x))*signe(vs[actor]))

                        else:

                            squares[y].x -= (xs[actor]+(50*(actor==up_x)) - xs[(actor-1)*-1]+(50*(actor==down_x))*signe(vs[actor]))

##                        if (abs((xs[actor]+(50*(actor==up_x)) - xs[(actor-1)*-1]+(50*(actor==down_x))*signe(vs[actor]))) > 2):

##                            print(squares[x].color, squares[y].color, xs, vs, actor, up_x, vs[actor])

                        squares[y].vector[0], squares[x].vector[0] = get_speed(squares[x].masse, squares[x].vector[0], squares[y].masse, squares[y].vector[0])

                        if squares[x].points != None:

                            squares[x].points += 1

                        elif squares[y].points != None:

                            squares[y].points += 1

        if len(squares) > 0:

            # for the first one have to check out of the loop
            if squares[0].x < 0:

##                if squares[0].points != None:
##
##                    print(squares[0].points)

                squares.remove(squares[0])

                if squares != []:

                    for sq in squares:

                        if sq.points != None:

                            pass#rint(sq.points)

            elif squares[0].x > screen_width:

                squares[0].vector[0] *= -1

                if squares[0].points != None:

                    squares[0].points += 1      


def main():

    ground = screen_height - 200

    compteur = 0

    point = 0

    graphic = 1

    play = True

    universe = Universe(ground)

    squares = []

    panneaux = []

    if graphic:

        valeurs_panneaux = [1, 2, 5, 10, 100, 1000]

        largeur_panneau = screen_width/(len(valeurs_panneaux)+1)

        delete_panneau = Panneau("", largeur_panneau*len(valeurs_panneaux), 0, largeur_panneau, 100, color=RED, image=draw_cross, image_coors=[55, 50])

        selected = 0

        for x in valeurs_panneaux:

            panneaux.append(Panneau(str(x), valeurs_panneaux.index(x)*largeur_panneau, 0, largeur_panneau, 100))

        panneaux[selected].color = GREEN

        refresh = 1

        panneaux2 = []

        valeurs_panneaux2 = [.01, .1, 0.6, 1, 2, 3]

        selected2 = 3

        for x in valeurs_panneaux2:

            panneaux2.append(Panneau(str(x), (valeurs_panneaux2.index(x)+0.5)*largeur_panneau, 100, largeur_panneau, 100))

        panneaux2[selected2].color = GREEN

    else:

        squares.append(add_square(60))

        squares.append(add_moving_square(.001, 100000000))

    while play:

##        test = 0
##
##        compteur += 1
##
##        if test:
##
##            compteur += 1
##
##            if (compteur % 100) == 0:
##
##                print(len(squares))
##
##                for sq in squares:
##
##                    print(sq.x, sq.vector[0])

        if graphic:

            for event in pygame.event.get():

                if event.type == pygame.QUIT:

                    play = False

                elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):

                    mouse_pos = pygame.mouse.get_pos()

                    if mouse_pos[1] > screen_height//2:

                        squares.append(add_square(mouse_pos[0]))  # screen_width-100

                    else:

                        if delete_panneau.clicked(mouse_pos):

                            squares = []

                        for pann in panneaux:

                            if pann.clicked(mouse_pos):

                                panneaux[selected].color = WHITE

                                selected = panneaux.index(pann)

                                pann.color = GREEN

                                refresh = 1

                        for pann in panneaux2:

                            if pann.clicked(mouse_pos):

                                panneaux2[selected2].color = WHITE

                                selected2 = panneaux2.index(pann)

                                pann.color = GREEN

                                refresh = 1

                elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 3):

                    vect_x = float(panneaux2[selected2].contenu)

                    masse = float(panneaux[selected].contenu)

                    squares.append(add_moving_square(vect_x, masse))

                elif (event.type == pygame.MOUSEMOTION):

                    translation = event.rel

        if graphic and refresh:

            refresh = universe.update(squares, graphic, panneaux, panneaux2)  # always resets to 0

            delete_panneau.draw()

        else:

            universe.update(squares, graphic)

        for indx in range(len(squares)-1, -1, -1):

            squares[indx].update(graphic)

        if graphic:

            pygame.display.update()

            clock.tick(300)


if __name__ == "__main__":

    main()
