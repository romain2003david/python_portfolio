from pig_tv import *


def cross_pattern(x_pos, y_pos, creation_vect):

    rects = [pygame.Rect(x_pos, y_pos, pattern_size, pattern_size), pygame.Rect(x_pos+pattern_size, y_pos, pattern_size, pattern_size)]

    if (creation_vect == []) or not(7 in creation_vect):

        paths = []

        for x, y in [[-1, -1], [-1, 0], [0, -1], [0, 0], [0, 1], [1, 0], [1, 1], [2, 1]]:

            paths.append([x_pos+pattern_size*x, y_pos+pattern_size*y, [x, y]])

##        for x, y in [[-2, 0], [-1, -2], [1, -2], [2, 0], [1, 2], [-1, 2]]:
##
##            paths.append([x_pos+pattern_size*x, y_pos+pattern_size*y, [x, y]])

    else:

        index = creation_vect.index(0)

        anti_index = (index-1)*-1

        paths = []

        for x in [-1, 0, 1]:

            paths.append([x_pos, y_pos, creation_vect.copy()])

            paths[-1][2][index] = x

            paths[-1][anti_index] += creation_vect[anti_index]*pattern_size

            paths[-1][index] += x*pattern_size

    for x in paths:

        if out_screen(x[0], x[1], screen_width, screen_height):

            paths.remove(x)

    return rects, paths


class Pattern:

    def __init__(self, start_x_pos, start_y_pos, function, color, creation_vect):

        self.start_x_pos = start_x_pos

        self.start_y_pos = start_y_pos

        self.color = color

##        if creation_vect == []:
##
##            self.color = BLACK
##
##        elif 0 in creation_vect:
##
##            self.color = GREEN
##
##        else:
##
##            self.color = RED

        self.rects, self.continue_paths = function(start_x_pos, start_y_pos, creation_vect)

    def draw(self):

        for rect in self.rects:

            pygame.draw.rect(screen, self.color, rect)

            pygame.draw.rect(screen, BLACK, rect, 1)

        polygon_shape = 0

        if polygon_shape:

            pygame.draw.polygon(screen, self.color, ((self.rects[0][0], self.rects[0][1]), (self.rects[1][0], self.rects[1][1]-pattern_size), (self.rects[1][0]+pattern_size, self.rects[1][1])))

            pygame.draw.polygon(screen, self.color, ((self.rects[0][0], self.rects[0][1]+pattern_size), (self.rects[1][0], self.rects[1][1]+2*pattern_size), (self.rects[1][0]+pattern_size, self.rects[1][1]+pattern_size)))

            pygame.draw.polygon(screen, BLACK, ((self.rects[0][0], self.rects[0][1]), (self.rects[1][0], self.rects[1][1]-pattern_size), (self.rects[1][0]+pattern_size, self.rects[1][1])), 1)

            pygame.draw.polygon(screen, BLACK, ((self.rects[0][0], self.rects[0][1]+pattern_size), (self.rects[1][0], self.rects[1][1]+2*pattern_size), (self.rects[1][0]+pattern_size, self.rects[1][1]+pattern_size)), 1)


def create_and_draw_patt(start_coors, color):

    if len(start_coors) == 2:

        creation_vect = []

    else:

        creation_vect = start_coors[2]

    patt = Pattern(start_coors[0], start_coors[1], cross_pattern, color, creation_vect)

    patt.draw()

    return patt.continue_paths


def do_step_pattern(current_pattern_coors):

    n_version = []

    color = get_random_color()  #selects a random color for this pattern wave

    for coor in current_pattern_coors:  # takes all current coors, draws the pattern in these coors

        n_version += create_and_draw_patt(coor, color)

    return n_version


def main(inputs):

    pattern_size, pattern_type = inputs

    play = True

    pattern_coors = [[screen_width//2, screen_height//2]]#[[0, 0]]#

    while play:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                play = False

            elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):

                pattern_coors = do_step_pattern(pattern_coors)

        pygame.display.update()

        clock.tick(5)


if __name__ == "__main__":

    pattern_size = 25

    pattern_type = 0

    inputs = [pattern_size, pattern_type]

    main(inputs)
