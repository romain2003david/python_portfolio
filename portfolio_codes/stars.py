"""
stars
"""

from pig_tv import *

import random

def val_abs(nbr):

    if nbr < 0:

        return -nbr

    return nbr


class Star:

    def __init__(self):

        self.x = random.randint(0, screen_width)

        self.y = random.randint(0, screen_height)

        self.target = [screen_width//2, screen_height//2]

    def goto(self, x, y):

        Star.stear(self, x, y)

        Star.get_speed(self, x, y)

        Star.move(self)

        if Star.out_born(self):

            Star.go_middle(self)

    def stear(self, x, y):
        """ Defines a new moving vector """

        self.vector = [x-self.x, y-self.y]

    def get_speed(self, x, y):

        self.speed = -10

##        dist_target = math.sqrt((self.vector[0])**2+((self.vector[1])**2))  # int(val_abs(self.vector[0]) + val_abs(self.vector[1]) * 0.8)
##
##        if dist_target:
##
##            max_speed = 3
##
##            if dist_target > 100:
##
##                self.speed = max_speed
##
##            else:
##
##                self.speed = max_speed / (1/(dist_target / 100))  # dist_target != 0


    def move(self):

        total = val_abs(self.vector[0]) + val_abs(self.vector[1])

        if total:

            add_x = self.speed * (self.vector[0]/total)

            add_y = self.speed * (self.vector[1]/total)

        else:

            add_y = 0

            add_x = 0

       # print(add_x, self.vector[0], total, self.speed, self.target[0], self.target[1])

        self.x += add_x

        self.y += add_y

    def update(self):

        #print(self.target[0], self.target[1])

        Star.goto(self, self.target[0], self.target[1])

        Star.draw(self)

    def draw(self):

        pygame.draw.circle(screen, (200, 200, 255), (int(self.x), int(self.y)), 3, 1)

        pygame.draw.circle(screen, (255, 255, 255), (int(self.x), int(self.y)), 2)

    def out_born(self):

        if (self.x < 0) or (self.y < 0) or (self.x > screen_width) or (self.y > screen_height):

            return True

        return False

    def go_middle(self):

        self.x = random.randint(screen_width//2-100, screen_width//2+100)

        self.y = random.randint(screen_height//2-100, screen_height//2+100)


def main():

    play = True

    stars = [Star() for x in range(1000)]

    while play:

        #screen.fill((0, 0, 0))

        for star in stars:

            star.update()

        pygame.display.update()

main()
