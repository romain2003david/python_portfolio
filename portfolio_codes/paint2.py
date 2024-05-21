from pig_tv import *


class Bomb:

    def __init__(self):

        self.intensite_rad_fact = 40

        self.drop_nb = 250

    def activate(self, color, intensite):

        mouse_pos = pygame.mouse.get_pos()

        screen.set_at(mouse_pos, color)

        for x in range(int(intensite*self.intensite_rad_fact)):

            rand = random.randint(self.intensite_rad_fact-10, self.intensite_rad_fact+10)

            rand_add = [random.randint(-rand, rand) for l in range(2)]

            pos = sum_arrays(mouse_pos, rand_add)

            if not out_screen(pos[0], pos[1], screen_width-1, screen_height):

                col = list(screen.get_at(pos)[:3])

                col = sum_arrays(col, color)

                apply_function_to_array(col, lambda x:x/2)

                screen.set_at(pos, col)


class Brush:

    def __init__(self):

        self.intensite_rad_fact = 10

    def activate(self, color, intensite):

        mouse_pos = pygame.mouse.get_pos()

        pygame.draw.circle(screen, color, mouse_pos, int(intensite*self.intensite_rad_fact))


class Marker:
    """ can be a rubber if the set color is white """

    def __init__(self):

        #self.erase_color = WHITE

        self.size_fac = 50

    def activate(self, color, intensite):

        x, y = pygame.mouse.get_pos()

        pyg_rect = pygame.Rect(x-(self.size_fac*intensite)//2, y-(self.size_fac*intensite)//2, (self.size_fac*intensite), (self.size_fac*intensite))

        pygame.draw.rect(screen, color, pyg_rect)


class Pencil:

    def __init__(self):

        self.intensite_thickness_fact = 3

        self.last_pos = None

    def activate(self, color, intensite):

        mouse_pos = pygame.mouse.get_pos()

        if self.last_pos == None:

            screen.set_at(mouse_pos, color)

        else:

            pygame.draw.line(screen, color, self.last_pos, mouse_pos, int(intensite*self.intensite_thickness_fact))

        self.last_pos = mouse_pos


class Fill:

    def __init__(self, y_min, y_max):

        self.y_min = y_min

        self.y_max = y_max

    def activate(self, color, intensite):

        mouse_pos = pygame.mouse.get_pos()

        searched_col = screen.get_at(mouse_pos)

        if color == list(searched_col[:3]):  # would turn into an infinte loop

            return

        all_vects = [[1, 0], [0, 1], [-1, 0], [0, -1]]  # [[x, y] for x in [-1, 1] for y in [-1, 1]]

        searching_pixels = [[mouse_pos, []]]

        while searching_pixels != []:

            n_searching_pixels = []

            for pix in searching_pixels:

                pix_pos, origin_vects = pix

                pix_vects = [x for x in all_vects if not x in origin_vects]

                for vect in pix_vects:

                    n_pos = sum_arrays(pix_pos, vect)

                    if (not n_pos in n_searching_pixels) and not(out_screen(n_pos[0], n_pos[1], screen_width-1, self.y_max, min_y=self.y_min)) and (screen.get_at(n_pos) == searched_col):

                        opposite_vect = [x*-1 for x in  vect]  # 0 unaffected, 1 or -1 becomes opposite

                        n_searching_pixels.append([n_pos, opposite_vect])

                        screen.set_at(n_pos, color)

            pygame.display.update()

            searching_pixels = n_searching_pixels

##        for y in range(self.y_min, self.y_max):
##
##            for x in range(screen_width):
##
##                if screen.get_at((x, y)) == searched_col:
##
##                    screen.set_at((x, y), color)
##
##            draw_barre_vie((y-self.y_min)/(self.y_max-self.y_min), screen_width-100, screen_height-80, 80)
##
##            pygame.display.update()


class Window:

    def __init__(self, min_y, max_y):

        self.upper_y = min_y

        self.upper_rect = pygame.Rect(0, 0, screen_width, self.upper_y)

        self.lower_y = max_y

        lower_height = screen_height-self.lower_y

        self.lower_rect = pygame.Rect(0, self.lower_y, screen_width, lower_height)

    def draw(self):

        pygame.draw.rect(screen, WHITE, self.upper_rect)

        pygame.draw.rect(screen, BLACK, self.upper_rect, 5)

        pygame.draw.rect(screen, WHITE, self.lower_rect)

        pygame.draw.rect(screen, BLACK, self.lower_rect, 5)

    def in_canvas(self):

        pos = pygame.mouse.get_pos()

        return (not self.upper_rect.collidepoint(pos)) and (not self.lower_rect.collidepoint(pos))


def main():

    play = True

    clicking = 0

    index = 0

    screen.fill(WHITE)

    # instanes

    min_y, max_y = 200, screen_height-100

    window = Window(min_y, max_y)

    tools = [Brush(), Bomb(), Marker(), Pencil(), Fill(min_y, max_y)]

    tool_choice = RadioButtons(10, screen_height-80, ["Brush", "Bomb", "Marker", "Pencil", "Fill"], color=WHITE)

    x_margin = 400

    y_margin = 50

    y_spot = 20

    red_lift = Lift(x_margin, y_spot, min_borne=0, max_borne=255, color1=RED, float_vals=0)

    green_lift = Lift(x_margin, y_spot+y_margin, min_borne=0, max_borne=255, color1=GREEN, float_vals=0)

    blue_lift = Lift(x_margin, y_spot+2*y_margin, min_borne=0, max_borne=255, color1=BLUE, float_vals=0)

    intensite_lift = Lift(100, 20, min_borne=0.01)

    lifts = [intensite_lift, blue_lift, green_lift, red_lift]

    lift_clicked_index = -1

    while play:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                play = False

            elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):

                mouse_pos = pygame.mouse.get_pos()

                clicking = 1

                for x in range(len(lifts)):

                    if lifts[x].clicked(mouse_pos):

                       lift_clicked_index = x 

            elif (event.type == pygame.MOUSEBUTTONUP) and (event.button == 1):

                clicking = 0

                lift_clicked_index = -1

                if isinstance(tools[tool_choice.bool_value], Pencil):

                    tools[tool_choice.bool_value].last_pos = None

            elif (event.type == pygame.MOUSEMOTION):

                translation = event.rel

                if lift_clicked_index >= 0:

                    lifts[lift_clicked_index].go(translation[0])

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_LEFT:

                    pass

        window.draw()

        for lift in lifts:

            lift.draw()

        if clicking and window.in_canvas():

            tools[tool_choice.bool_value].activate([red_lift.echelle, green_lift.echelle, blue_lift.echelle], intensite_lift.echelle)

        tool_choice.update(pygame.mouse.get_pos(), clicking)

        tool_choice.draw()

        pygame.display.update()

        clock.tick(60)


if __name__ == "__main__":

    main()
