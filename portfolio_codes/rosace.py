from pig_tv import *


class Circle:

    def __init__(self, x, y, radius, thickness):

        self.x = x

        self.y = y

        self.radius = radius

        self.color = get_random_color()

        self.thickness = thickness

    def draw(self):

        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius, self.thickness)

    def spread(self, babe_nb, start_angle=0):

        n_circles = []

        angle_move = 2*pi / babe_nb

        for x in range(babe_nb):

            n_x = self.x+(cos(x*angle_move)*self.radius)

            n_y = self.y+(sin(x*angle_move)*self.radius)

            n_circle_inst = Circle(n_x, n_y, self.radius, self.thickness)

            n_circles.append(n_circle_inst)

        return n_circles

        
        
def main(inputs):

    radius, spread_nb, thickness, circle_pos_choice = inputs

    if circle_pos_choice == 2:

        current_circles = []
        aff_txt("press any key to begin", 100, screen_height//2-50, color=WHITE)
        aff_txt("right click to place circles", 100, screen_height//2, color=WHITE)
        aff_txt("left click to update", 100, screen_height//2+50, color=WHITE)
        pygame.display.update()
        wait()
        screen.fill(BLACK)

    else:

        current_circles = [Circle(screen_center[0], screen_center[1], radius, thickness)]

        if circle_pos_choice == 1:

            for x in [0.5, 1.5]:

                for y in [0.5, 1.5]:

                    current_circles.append(Circle(screen_center[0]*x, screen_center[1]*y, radius, thickness))

    play = True

    while play:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                play = False

            elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 3):

                mouse_pos = pygame.mouse.get_pos()

                current_circles.append(Circle(mouse_pos[0], mouse_pos[1], radius, thickness))

            elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):

                n_circles = []

                for circle in current_circles:

                    n_circles += circle.spread(spread_nb)

                current_circles = n_circles

            elif (event.type == pygame.MOUSEMOTION):

                translation = event.rel

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_LEFT:

                    pass

        for circle in current_circles:

            circle.draw()

        pygame.display.update()

        clock.tick(60)

if __name__ == "__main__":

    inputs = [30, 4, 1, 0]

    main(inputs)
