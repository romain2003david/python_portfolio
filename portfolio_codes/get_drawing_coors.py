""" Return the coordinates of whatever drawing """

import pygame

from pygame.locals import *


class Drawing:

    def __init__(self, screen, screen_width, screen_height):

        self.screen = screen

        self.screen_width = screen_width

        self.screen_height = screen_height

        self.list = []

    def get_coor(self, drawing_color):

        for y in range(self.screen_height):

            for x in range(self.screen_width):

                pix_color = self.screen.get_at((x, y))

                if pix_color == drawing_color:

                    self.list.append((x, y))

class Test:

    def __init__(self):

        draw = Drawing(screen, largeur_screen, hauteur_screen)
        draw.get_coor((255, 255, 255))

        time.sleep(0.1)

        for coor in draw.list:

            screen.set_at((coor[0], coor[1]), (255, 0, 0))

        pygame.display.update()



if __name__== "__main__":

    def aff_txt(contenu, x, y, color=(0, 0, 0), taille=20):
        """ Permet d'afficher un texte """
        myfont = pygame.font.SysFont("monospace", taille, True)
        label = myfont.render(contenu, 1, color)
        screen.blit(label, (x, y))

    import time

    largeur_screen, hauteur_screen = 700, 700
    largeur_barriere = 21

    pygame.init()

    screen = pygame.display.set_mode((largeur_screen, hauteur_screen))#, FULLSCREEN)
    pygame.display.set_caption("Jeu")

    screen.fill((0, 0, 0))

    pygame.draw.circle(screen, (255, 255, 255), (350, 350), 30)

    pygame.display.update()

    test = Test()

    screen.fill((0, 0, 0))

    aff_txt("romain", 100, 200, (255, 255, 255), taille=150)

    pygame.display.update()

    test = Test()

