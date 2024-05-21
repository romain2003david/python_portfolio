from pig_tv import *


class Brush:

    def __init__(self, thickness, color, symetry_function, in_allocated_space, color_change, sym):

        # variables

        self.thickness = thickness

        # color

        self.color = color

        self.color_change = color_change

        self.selected_color = [1, 1]

        # instance functions

        self.in_allocated_space = in_allocated_space

        self.symetry_function = symetry_function

        # graphic

        self.lines = [[(screen_width//2, 0), (screen_width//2, screen_height)]]

        if sym:

            self.lines.append([(0, screen_height//2), (screen_width, screen_height//2)])

    def draw(self):

        for line in self.lines:

            pygame.draw.line(screen, WHITE, line[0], line[1])

        pygame.display.update()

    def update_color(self):

        for x in range(self.color_change):

            self.color, self.selected_color = update_colors(self.color, self.selected_color)

    def paint(self, last_pos):

        m_pos = pygame.mouse.get_pos()

        if (self.in_allocated_space(m_pos)) and (self.in_allocated_space(last_pos)):

            Brush.update_color(self)

            pygame.draw.line(screen, self.color, last_pos, m_pos, self.thickness)#, [m_pos[0]+translation[0], m_pos[1]+translation[1]])

            self.symetry_function(m_pos, last_pos, self.thickness, self.color)

            pygame.display.update()

        return m_pos


def draw_4_sym(pos1, pos2, thickness, color):

    for x, y in [[1, 0], [0, 1], [1, 1]]:

        pos1p = [(screen_width//2 + (screen_width//2-pos1[0]))*x or pos1[0], (screen_height//2 + (screen_height//2-pos1[1]))*y or pos1[1]]

        pos2p = [(screen_width//2 + (screen_width//2-pos2[0]))*x or pos2[0], (screen_height//2 + (screen_height//2-pos2[1]))*y or pos2[1]]  # try fuck ?

        pygame.draw.line(screen, color, pos1p, pos2p, thickness)


def draw_2_sym(pos1, pos2, thickness, color):

    for x, y in [[1, 0]]:

        pos1p = [(screen_width//2 + (screen_width//2-pos1[0]))*x or pos1[0], (screen_height//2 + (screen_height//2-pos1[1]))*y or pos1[1]]

        pos2p = [(screen_width//2 + (screen_width//2-pos2[0]))*x or pos2[0], (screen_height//2 + (screen_height//2-pos2[1]))*y or pos2[1]]

        pygame.draw.line(screen, color, pos1p, pos2p, thickness)


def in_allocated_space_4(pos):

    return (pos[0] < screen_width//2) and (pos[1] < screen_height//2)


def in_allocated_space_2(pos):

    return (pos[0] < screen_width//2)


##    while (color[selected_color[0]]+selected_color[1] < 50) or (color[selected_color[0]]+selected_color[1] > 255):
##
##            selected_color[0] = random.randint(0, 2)
##
##            if random.randint(0, 1) == 0:
##
##                selected_color[1] = -color_change
##
##            else:
##
##                selected_color[1] = color_change
##
##    color[selected_color[0]] += selected_color[1]
##
##    return color, selected_color

def main(inputs):

    # symetry stuff

    thickness, color_change, sym = inputs

    if sym == 1:

        function_sym = draw_4_sym

        in_allocated_space = in_allocated_space_4

    elif sym == 0:

        function_sym = draw_2_sym

        in_allocated_space = in_allocated_space_2

    brush = Brush(thickness, [255, 255, 255], function_sym, in_allocated_space, color_change, sym)


    # tool vars

    play = True

    m_pos = pygame.mouse.get_pos()

    lock = 0

    brush.draw()

    # painting loop
    while play:

        #update_color()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                play = False

            elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):

                lock = 1

                m_pos = pygame.mouse.get_pos()

            elif (event.type == pygame.MOUSEBUTTONUP) and (event.button == 1):

               lock = 0

            elif (event.type == pygame.MOUSEMOTION):

                if lock:

                    m_pos = brush.paint(m_pos)

        clock.tick(60)


if __name__ == "__main__":

    sym = 0

    main([3, 5, sym])
