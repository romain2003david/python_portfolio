from pig_tv import *


class Electron:

    def __init__(self, draw_cloud):

        self.x = random.randint(0, screen_width)

        self.y = random.randint(0, screen_height)

        self.radius = 10

        self.cloud_radius = self.radius*10

        self.vector = get_random_vector()

        self.color = get_random_color()

        self.draw_cloud = draw_cloud

    def update(self, graphic):

        self.vector[0] += random.randint(-10, 10)/100

        self.vector[1] += random.randint(-10, 10)/100

        repulsion = set_array_to_different_array([-700, 700], [-1, 1], stear_of_screen(self.x, self.y, screen_width, screen_height))

        self.vector = [self.vector[0]+repulsion[0], self.vector[1]+repulsion[1]]

        if not out_screen(self.x+self.vector[0], self.y+self.vector[1], screen_width, screen_height):

            self.x += self.vector[0]

            self.y += self.vector[1]

        if graphic:

            Electron.draw(self)

    def draw(self):

        if self.draw_cloud:

            pygame.draw.circle(screen, GREY, (int(self.x), int(self.y)), self.cloud_radius)

        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)


def main(inputs):

    entity_nb, draw_cloud = inputs

    play = True

    electrons = [Electron(draw_cloud) for x in range(int(entity_nb))]

    graphic = 1

    while play:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                play = False

            elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):

                mouse_pos = pygame.mouse.get_pos()

            elif (event.type == pygame.MOUSEMOTION):

                translation = event.rel

        screen.fill(BLACK)

        for electron in electrons:

            electron.update(graphic)

        pygame.display.update()

        clock.tick(150)


if __name__ == "__main__":

    main([50, 0])
