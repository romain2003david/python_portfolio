from pig_tv import *


class Circle:

    def __init__(self, radius, modulo_nb, table, modulo_nb_increment, table_increment, changing_col=0):

        self.radius = radius

        self.x = radius+(screen_width-screen_height)//2

        self.y = radius

        self.modulo_nb = int(modulo_nb)

        self.table = table

        self.modulo_nb_increment = int(modulo_nb_increment)

        self.table_increment = table_increment

        self.color = [0, 0, 0]

        self.selected_color = [0, 1]

        self.changing_col = changing_col

    def update(self, graphic):

        # the two values to tweak

        self.modulo_nb += self.modulo_nb_increment

        self.table += self.table_increment

        ##

        if graphic:

            Circle.draw(self)

    def draw(self):

        pygame.draw.circle(screen, BLACK, (self.x, self.y), self.radius, 3)

        base_mesure = (2*pi)/self.modulo_nb

##        for x in range(self.modulo_nb):
##
##            pygame.draw.circle(screen, RED, round_list(get_pos_on_circle(base_mesure*x, self.radius, [300, 300])), 1)

        for x in range(self.modulo_nb):

            if self.changing_col:

                self.color, self.selected_color = update_colors(self.color, self.selected_color)

            pos1 = round_list(get_pos_on_circle(base_mesure*x, self.radius, screen_center))

            pos2 = round_list(get_pos_on_circle(base_mesure*(x*self.table)%self.modulo_nb, self.radius, screen_center))

            pygame.draw.line(screen, self.color, pos1, pos2, 1)


def main(inputs):

    modulo_nb, table, modulo_nb_increment, table_increment, fps = inputs

    circle = Circle(screen_height//2, modulo_nb, table, modulo_nb_increment, table_increment)

    play = True

    graphic = 1

    while play:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                play = False

            elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):

                circle.table += 1

                mouse_pos = pygame.mouse.get_pos()

            elif (event.type == pygame.MOUSEMOTION):

                translation = event.rel

        screen.fill(WHITE)

        circle.update(graphic)

        pygame.display.update()

        clock.tick(fps)

##        if not random.randint(0, 60):
##
##            print(clock.get_fps())


if __name__ == "__main__":

    modulo_nb = 20

    table = 2

    modulo_nb_increment, table_increment = 1, 0.01

    main([modulo_nb, table, modulo_nb_increment, table_increment, 60])
