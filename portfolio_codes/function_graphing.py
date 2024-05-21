from pig_tv import *


def get_ycoor_of_xcoor(x_coor, polynom, print_=0):

    y_coor = polynom[0]

    for degree in range(1, len(polynom)):

        y_coor += polynom[degree] * x_coor**degree

        if print_:

            print(y_coor , polynom[degree] , x_coor,degree)

    return y_coor


def draw_fct(fct, translation, tangent_x_coor, add=0):
    """ draws a polynom """

    last_point = None

    for x_coor in range(screen_width):

        y_coor = get_ycoor_of_xcoor(x_coor+translation[0], fct)

        pos = [x_coor, y_coor]

        pos[1] -= translation[1]

        apply_function_to_array(pos, round)

        screen.set_at(pos, GREEN)

        if last_point:

            pygame.draw.line(screen, GREEN, pos, last_point)

        last_point = pos

    if not tangent_x_coor == None:

        tangent_x_coor += add

        y_coor = get_ycoor_of_xcoor(tangent_x_coor, fct)

        draw_tangent(tangent_x_coor, y_coor, fct, translation)


def get_derive_poly(x_coor, polynom):

    if len(polynom) > 1:

        sum_deriv_of_x = polynom[1]

        for x in range(2, len(polynom)):
            # x is power

            sum_deriv_of_x += (x*polynom[x]) * (x_coor**(x-1))

        return sum_deriv_of_x

    return 0

        
def draw_tangent(x, y_coor, polynom, translation):

    # draws circle at tangent location
    center = apply_function_to_array(sum_arrays((x, y_coor), translation, 1, -1), round)

    pygame.draw.circle(screen, PURPLE, center, 10)

    # computes the function tangent in x
    derive = get_derive_poly(x, polynom)

    m = derive

    p = -derive*x + y_coor

    droite = [m, p]

    p1 = sum_arrays([0, p], translation, 1, -1)

    p2 = sum_arrays([screen_width, m*screen_width+p], translation, 1, -1)

##    droite = [derive, (derive*x)+(y_coor)]  # [derive, (derive*a-(derive*x)+(y_coor))]
##
##    m, p = droite
##
##    p1 = sum_arrays([0, p], translation, 1, -1)
##
##    p2 = sum_arrays([screen_width, m*screen_width+p], translation, 1, -1)

    #p2 = sum_arrays([0, -(y_coor+derive*x)], translation, 1, -1)

    #print(y_coor, derive, x)

    draw_line(get_droite_from_pt(p1, p2), RED)

    #pygame.draw.line(screen, RED, p1, p2, 3)


def get_nbr(string):

    try:

        nb = float(input(string+"\n"))

        return nb

    except ValueError:

        print("bad input")

        get_nbr(string)


def get_user_function():
    """ returns a polynom of n degrees """

    test = 0

    if test:

        return [0, 0, .1]

    nbr_degre = int(get_nbr("nombre de degres:"))

    degres = [0 for x in range(nbr_degre+1)]

    for x in range(nbr_degre+1):

        degres[x] = get_nbr("facteur x de degre {} :".format(x))

    return degres


class BG:

    def __init__(self):

        self.x_lift = Lift(550, 30, min_borne=-400, max_borne=0, echelle=-100, afficher_echelle=0)

        self.y_lift = Lift(screen_width-30, 10, width=10, height=170, min_borne=-400, max_borne=0, echelle=-100, vertical=1, afficher_echelle=0)

        self.x_line_pos = [[0, 0], [screen_width, 0]]

        self.y_line_pos = [[0, 0], [0, screen_height]]

        self.x_lift_clicked = 0

        self.y_lift_clicked = 0

        self.upper_box = pygame.Rect(0, 0, screen_width, 200)

        #self.right_box = pygame.Rect(screen_width-100, 0, 100, 250)

        self.color = BLUE

    def check_click(self, mouse_pos):

        if self.x_lift.clicked(mouse_pos):

            self.x_lift_clicked = 1

        if self.y_lift.clicked(mouse_pos):

            self.y_lift_clicked = 1

    def cancel_click(self):

        self.x_lift_clicked = 0

        self.y_lift_clicked = 0

    def update(self, mouse_pos, clicking, translation):

        change = 0

        if self.x_lift_clicked:

            self.x_lift.go(translation[0])

            change = 1

        if self.y_lift_clicked:

            self.y_lift.go(translation[1])

            change = 1

        if not change:

            BG.draw(self)

        return change

    def get_translation(self):

        return [self.x_lift.echelle, self.y_lift.echelle]

    def draw(self):

        translation = BG.get_translation(self)

        # dessine le repere
        pygame.draw.line(screen, BLACK, sum_arrays(self.x_line_pos[0], translation, 1, -1), sum_arrays(self.x_line_pos[1], translation, 1, -1), 3)

        pygame.draw.line(screen, BLACK, sum_arrays(self.y_line_pos[0], translation, 1, -1), sum_arrays(self.y_line_pos[1], translation, 1, -1), 3)

        # draws upper part of screen
        pygame.draw.rect(screen, self.color, self.upper_box)

        #pygame.draw.rect(screen, self.color, self.right_box)

        self.x_lift.draw()

        self.y_lift.draw()


def main():

    type_box = Panneau("Set function", 0, 0, largeur=250, y_focus=-20, color=RED)

    tangent_box = Panneau("Draw tangente", 250, 0, largeur=300, y_focus=-20, color=RED)

    derive_lift = Lift(0, 80, min_borne=-200, max_borne=200, echelle=0, afficher_echelle=0)

    derive_lift_clicked = 0

    bg = BG()

    screen.fill(WHITE)

    play = True

    clicking = 0

    fct = None

    tangent_x_coor = None

    while play:

        change_too = 0

        translation = [0, 0]

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                play = False

            elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):

                clicking = 1

                mouse_pos = pygame.mouse.get_pos()

                if type_box.clicked(mouse_pos):

                    translation = bg.get_translation()

                    screen.fill(WHITE)

                    fct = get_user_function()

                    tangent_x_coor = None

                    draw_fct(fct, translation, tangent_x_coor)

                elif tangent_box.clicked(mouse_pos):

                    tangent_x_coor = get_nbr("x coor of the tangent")

                    screen.fill(WHITE)

                    if fct:

                        draw_fct(fct, bg.get_translation(), tangent_x_coor, derive_lift.echelle)

                    bg.draw()

                elif derive_lift.clicked(mouse_pos):

                    derive_lift_clicked = 1

                else:

                    change = bg.check_click(mouse_pos)

            elif (event.type == pygame.MOUSEBUTTONUP) and (event.button == 1):

                clicking = 0

                bg.cancel_click()

                derive_lift_clicked = 0

            elif (event.type == pygame.MOUSEMOTION):

                translation = event.rel

                if derive_lift_clicked and (tangent_x_coor != None):

                    derive_lift.go(translation[0])

                    change_too = 1

        change = bg.update(pygame.mouse.get_pos(), clicking, translation)

        if change or change_too:

            screen.fill(WHITE)

            if fct:

                draw_fct(fct, bg.get_translation(), tangent_x_coor, derive_lift.echelle)

            bg.draw()

        type_box.draw()

        tangent_box.draw()

        if (tangent_x_coor != None):

            derive_lift.draw()

        pygame.display.update()

        clock.tick(60)

        test = 0

        if test and (not random.randint(0, 120)):

            print(clock.get_fps())


if __name__ == "__main__":

    main()
