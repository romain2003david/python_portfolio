from pig_tv import *


class Balle:

    def __init__(self, start_pos, end_pos):

        self.x = start_pos[0]

        self.y = start_pos[1]

        self.start_pos = start_pos

        self.end_pos = end_pos

        self.vect = [self.start_pos[0]-self.end_pos[0], self.start_pos[1]-self.end_pos[1]]

        self.vect = get_normalized_vector(self.vect, 10)

        self.width = random.randint(5, 20)

        self.long_vect = get_normalized_vector(self.vect.copy(), self.width*5)

        self.color = get_random_color()

    def update(self):

        Balle.draw(self)

        Balle.update_coor(self)

    def reset_vect(self):

        self.long_vect = get_normalized_vector(self.vect.copy(), self.width*5)

    def update_coor(self):

        self.x += self.vect[0]

        self.y += self.vect[1]

        if self.x < 0:

            self.vect[0] *= -1

            Balle.reset_vect(self)

        elif self.x > screen_width:

            self.vect[0] *= -1

            Balle.reset_vect(self)

        if self.y < 0:

            self.vect[1] *= -1

            Balle.reset_vect(self)

        elif self.y > screen_height:

            self.vect[1] *= -1

            Balle.reset_vect(self)

    def draw(self):

        pygame.draw.line(screen, self.color, [self.x, self.y], sum_arrays(self.long_vect, [self.x, self.y]), self.width)


def main(inputs):

    play = True

    clicking = 0

    start_shooting_pos = []

    balles = []

    # main playing loop

    while play:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                play = False

            elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):

                start_shooting_pos = pygame.mouse.get_pos()

                clicking = 1

            elif (event.type == pygame.MOUSEBUTTONUP) and (event.button == 1):

                balles.append(Balle(start_shooting_pos, pygame.mouse.get_pos()))

                clicking = 0

            elif (event.type == pygame.MOUSEMOTION):

                translation = event.rel

        screen.fill(BLACK)

        for ball in balles:

            ball.update()

        pygame.display.update()

        clock.tick(60)


if __name__ == "__main__":

    inputs = []

    main(inputs)
