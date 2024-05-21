import pygame
import random

from pygame.locals import *

# Constantes
couleur_oiseau = (0, 255, 0)
largeur_fen, hauteur_fen = 700, 700

# Screen settings
pygame.init()
screen = pygame.display.set_mode((largeur_fen, hauteur_fen))#, FULLSCREEN)
pygame.display.set_caption("Snake")


class Ver:

    def __init__(self, screen):
        """ Constructeur d'une instance de Ver """

        self.screen = screen

        self.pas = 5
        self.taille_membre = 20

        # coordonnes de la tete
        self.x = int(largeur_fen / 2)
        self.y = int(hauteur_fen / 2)

        # Le corps commence avec une longueur de 3
        self.direction = "right"
        self.corps = [[self.x, self.y, self.direction, None], [int(largeur_fen/2 - self.taille_membre), int(hauteur_fen/2) , "right", None], [int(largeur_fen/2 - 2*self.taille_membre), int(hauteur_fen/2), "right", None]]  # chaque partie du corps de ver porte sa direction, qu'elle passe au suivant apres avoir avance
        self.tete = self.corps[0]

    def manger(self):
        """ Ajoute une partie au corps du ver """
        self.corps.append(self.corps[-1].copy())
        self.corps[-1][3] = None
        dico_deplace = {"right" : [0, -1], "left" : [0, 1], "up" : [1, 1], "down" : [1, -1]}
        index, balance = dico_deplace[self.corps[-1][2]]
        self.corps[-1][index] += self.taille_membre * balance

    def avancer(self):
        """ Fais avancer le corps du ver """

##        for x in range(len(self.corps)-1, 0, -1):
##            self.corps[x][2] = self.corps[x-1][2]
        #print(self.corps)

        self.tete[2] = self.direction

        def assign_xy(x, y, direction):

            if direction == "right":
                x += self.pas
            elif direction == "left":
                x += self.pas * -1
            elif direction == "up":
                y += self.pas * -1
            elif direction == "down":
                y += self.pas

            return x, y

        self.x, self.y = assign_xy(self.x, self.y, self.direction)
        self.corps[0][0], self.corps[0][1] = self.x, self.y
        pygame.draw.rect(self.screen, (100, 200, 20), pygame.Rect(self.x, self.y, self.taille_membre, self.taille_membre))

        for v in range(1, len(self.corps)):
            self.corps[v][0], self.corps[v][1] = assign_xy(self.corps[v][0], self.corps[v][1], self.corps[v][2])
            pygame.draw.rect(self.screen, (100, 200, 20), pygame.Rect(self.corps[v][0], self.corps[v][1], self.taille_membre, self.taille_membre))

            #repere
            if self.corps[v][3] != None:
                if (self.corps[v][0] == self.corps[v][3][0]) and (self.corps[v][1] == self.corps[v][3][1]):
                    self.corps[v][2] = self.corps[v][3][2]
                    if not v == len(self.corps)-1:
                        self.corps[v+1][3] = self.corps[v][3]
                    self.corps[v][3] = None
            

    def in_borne(self):
        return in_borne(self.x, self.y, self.taille_membre, self.taille_membre)


class Nourriture:

    def __init__(self, xy, screen):

        self.x = xy[0]
        self.y = xy[1]

        self.taille_cote = 20
        self.screen = screen

    def placer(self):
        pygame.draw.rect(self.screen, (200, 100, 120), pygame.Rect(self.x, self.y, self.taille_cote, self.taille_cote))
        

def aff_txt(contenu, x, y, color=(0, 0, 0), taille=30):
    """ Permet d'afficher un texte """
    myfont = pygame.font.SysFont("monospace", taille, True)
    label = myfont.render(contenu, 1, color)
    screen.blit(label, (x, y))


def in_borne(x, y, hauteur_item, largeur_item):
    if x<0:
        return ["x",0]
    elif x>(largeur_fen-largeur_item):
        return ["x",1520-largeur_item]
    elif y>(hauteur_fen-hauteur_item):
        return ["y",800-hauteur_item]
    elif y<0:
        return ["y",0]
    else:
        return False


def poser_repere(ver, vtisk, rappel):
    """pose un repere pour les autres parties du corps(qd tourner)"""

    ver.corps[0][2] = vtisk
    ver.direction = vtisk
    if ver.corps[1][3] == None:
        ver.corps[1][3] = ver.corps[0].copy()
    else:
        rappel = ver.corps[0].copy()

    return rappel

def jeu(screen):
    """ Fonction contenant la boucle principale de jeu """

    jeu = True
    rappel = None

    xy_nourriture = [largeur_fen //2 - 60, hauteur_fen //2]
    point = 0

    ver = Ver(screen)
    nourriture = Nourriture(xy_nourriture, screen)

    wait = True
    aff_txt("Tap whatever you wish to", 120, hauteur_fen//2, (255, 0, 100))
    pygame.display.update()

    while wait:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                wait = False

    while jeu:

        screen.fill((0, 50, 255))
        #print(ver.corps)
        for event in pygame.event.get():
            if event.type == QUIT:
                aff_txt("au revoir", 250, 300, color=(255, 0, 0))
                jeu = False

            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_LEFT) and (ver.direction != "right"):
                    rappel = poser_repere(ver, "left", rappel)

                if (event.key == pygame.K_RIGHT) and (ver.direction != "left"):
                    rappel = poser_repere(ver, "right", rappel)

                if (event.key == pygame.K_UP) and (ver.direction != "down"):
                    rappel = poser_repere(ver, "up", rappel)

                if (event.key == pygame.K_DOWN) and (ver.direction != "up"):
                    rappel = poser_repere(ver, "down", rappel)

        if ver.in_borne():  # in fact /not/ in born
            aff_txt("hors zone !", 250, 300, color=(255, 0, 0))
            jeu = False

        if rappel != None:

            if ver.corps[1][3] == None:
                ver.corps[1][3] = rappel
                rappel = None

        rect_tete, rect_nourriture = pygame.Rect(ver.corps[0][0], ver.corps[0][1], ver.taille_membre, ver.taille_membre), pygame.Rect(xy_nourriture[0], xy_nourriture[1], nourriture.taille_cote, nourriture.taille_cote)
        if rect_tete.colliderect(rect_nourriture):
            ver.manger()
            point += 1
            xy_nourriture = [random.randint(0, largeur_fen-20), random.randint(0, hauteur_fen-20)]
            nourriture = Nourriture(xy_nourriture, screen)

        for membre in range(2, len(ver.corps)):
            rect_partie_ver = pygame.Rect(ver.corps[membre][0], ver.corps[membre][1], ver.taille_membre, ver.taille_membre)
            if rect_tete.colliderect(rect_partie_ver):
                aff_txt("Touché !", 250, 300, color=(255, 0, 0))
                jeu = False

        nourriture.placer()
        aff_txt("Points : {}".format(point), 0, 0, color=(20, 200, 20))

        ver.avancer()
        pygame.display.update()

        pygame.time.Clock().tick(100)

jeu(screen)
