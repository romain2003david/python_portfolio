from pig_tv import *


class Circle:

    def __init__(self):

        self.x, self.y = screen_center

        self.radius = 250

        self.color = WHITE

        # animation steps

        self.step = 0

        # about the animation length

        self.advance_time = 0

        self.step_time = 300

        # about the small circles

        self.small_circle_nb = 24

        self.small_circle_radius = int((pi*self.radius)/(self.small_circle_nb-pi))

        self.small_circles_angles = [0]

        self.angle_increment = int(self.step_time / self.small_circle_nb)

        # about the lines

        self.line_angles = [pi/2, 7*pi/6, 11*pi/6]

        # storage

        self.points = []

    def get_small_circle_pos(self, angle):

        x = self.x+(self.radius+self.small_circle_radius)*cos(angle)

        y = self.y+(self.radius+self.small_circle_radius)*sin(angle)

        return [int(x), int(y)]

    def get_pos_on_circle(self, angle, radius = None):

        if radius == None:

            radius = self.radius

        x = self.x+(radius)*cos(angle)

        y = self.y+(radius)*sin(angle)

        return [int(x), int(y)]

    def update(self):

        self.advance_time += 1

        if self.advance_time % self.angle_increment == 0:

            max_ = 2*pi

            if (self.step%4)>1:  # left to right, or opposite direction : it changes

                max_ *= -1

            n_angle = set_val_to_different_array([0, self.step_time], [0, max_], self.advance_time)

            if self.step % 2 == 0:

                self.small_circles_angles.append(get_trigo_sole_angle(n_angle))

            else:

                self.small_circles_angles.remove(get_trigo_sole_angle(n_angle))

        if self.advance_time == self.step_time:

            self.step += 1

            self.advance_time = 0

        Circle.draw(self)

    def draw(self):

        # draws big circle
        pygame.draw.circle(screen, self.color, [self.x, self.y], self.radius)

        # draws small circles
        for angle in self.small_circles_angles:

            pygame.draw.circle(screen, self.color, Circle.get_small_circle_pos(self, angle), self.small_circle_radius)

        if self.step == 0:

            # draws lines into circle

            line_advance = set_val_to_different_array([0, self.step_time], [0, self.radius], self.advance_time)

            for angle in self.line_angles:

                pygame.draw.line(screen, get_inv_color(self.color), Circle.get_pos_on_circle(self, angle), Circle.get_pos_on_circle(self, angle, self.radius-line_advance), 3)

        elif self.step == 1:

            pts = []

            for indx in range(len(self.line_angles)):

                delta_angle = set_val_to_different_array([0, self.step_time], [0, -pi/3], self.advance_time)

                pts.append(Circle.get_pos_on_circle(self, self.line_angles[indx]+delta_angle))

            # draws rotating triangle into circle

            pygame.draw.polygon(screen, get_inv_color(self.color), pts)

        elif self.step == 2:

            # draws steady triangle into circle
            pts = [Circle.get_pos_on_circle(self, self.line_angles[x]-pi/3) for x in range(3)]

            pygame.draw.polygon(screen, get_inv_color(self.color), pts)

            # draws lines into circle

            line_advance = set_val_to_different_array([0, self.step_time], [0, self.radius//2], self.advance_time)

            for angle in self.line_angles:

                pygame.draw.line(screen, self.color, Circle.get_pos_on_circle(self, angle), Circle.get_pos_on_circle(self, angle, line_advance), 5)

        elif self.step == 3:

            # computing for middle of traingle segments to be changed

            sommets_triangle = [Circle.get_pos_on_circle(self, self.line_angles[x]-pi/3) for x in range(3)]

            milieux = [get_milieu_droite(sommets_triangle[0], sommets_triangle[1]), get_milieu_droite(sommets_triangle[1], sommets_triangle[2]), get_milieu_droite(sommets_triangle[2], sommets_triangle[0])]

            n_coors = []

            for indx in range(len(milieux)):

                x, y = milieux[indx]

                n_x = set_val_to_different_array([0, self.step_time], [x, self.x], self.advance_time)

                n_y = set_val_to_different_array([0, self.step_time], [y, self.y], self.advance_time)

                n_coors.append([n_x, n_y])

            pygame.draw.polygon(screen, get_inv_color(self.color), [sommets_triangle[0], n_coors[0], sommets_triangle[1], n_coors[1], sommets_triangle[2], n_coors[2]])

        elif self.step == 4:

            sommets_triangle = [Circle.get_pos_on_circle(self, self.line_angles[x]-pi/3) for x in range(3)]

            milieux = [get_milieu_droite(sommets_triangle[0], sommets_triangle[1]), get_milieu_droite(sommets_triangle[1], sommets_triangle[2]), get_milieu_droite(sommets_triangle[2], sommets_triangle[0])]

            for indx in range(len(milieux)):

                x, y = milieux[indx]

                n_x = set_val_to_different_array([1, 5], [x, self.x], 4)

                n_y = set_val_to_different_array([1, 5], [y, self.y], 4)

                milieux[indx] = [n_x, n_y]

            # designing the steady pts around teh moving middles
            milieux_on_sides = []

            for m in range(len(milieux)):

                for side in range(2):

                    ref_pt1 = milieux[m]

                    ref_pt2 = sommets_triangle[(m+side)%3]

                    ratio = 4/5

                    x = ref_pt1[0]*ratio+ref_pt2[0]*(1-ratio)

                    y = ref_pt1[1]*ratio+ref_pt2[1]*(1-ratio)

                    milieux_on_sides.append([x, y])

            vects_milieux_centre = [sum_arrays(milieux[x], [self.x, self.y], 1, -1) for x in range(len(milieux))]

            n_coors = milieux

            n_coors = []

            for indx in range(len(milieux)):

                facteur_vect = set_val_to_different_array([0, self.step_time], [1, 8], self.advance_time)

                n_coors.append(sum_arrays([self.x, self.y], vects_milieux_centre[indx], 1, facteur_vect))

            points = []

            for x in range(len(sommets_triangle)):

                points.append(sommets_triangle[x])

                points.append(milieux_on_sides[x*2])

                points.append(n_coors[x])

                points.append(milieux_on_sides[x*2+1])

            pygame.draw.polygon(screen, get_inv_color(self.color), points)

            self.points = points

        elif self.step == 5:

            sommets = []

            for x in range(len(self.points)//4):

                sommets.append(self.points[x*4])

            vects = [sum_arrays(sommets[x], [self.x, self.y], -1) for x in range(len(sommets))]

            points = self.points.copy()

            for x in range(len(sommets)):

                delta = set_val_to_different_array([0, self.step_time], [0, 1], self.advance_time)

                apply_function_to_array(vects[x], lambda x:x*delta)

                sommets[x] = sum_arrays(vects[x], sommets[x])

                points[x*4] = sommets[x]

            pygame.draw.polygon(screen, get_inv_color(self.color), points)

        elif self.step == 6:

            sommets = []

            for x in range(len(self.points)//4):

                sommets.append(self.points[x*4])

            vects = [sum_arrays(sommets[x], [self.x, self.y], -1) for x in range(len(sommets))]

            points = self.points.copy()

            for x in range(len(sommets)):

                delta = set_val_to_different_array([0, self.step_time], [1, 0], self.advance_time)

                apply_function_to_array(vects[x], lambda x:x*delta)

                sommets[x] = sum_arrays(vects[x], sommets[x])

                points[x*4] = sommets[x]

            pygame.draw.polygon(screen, get_inv_color(self.color), points)

        elif self.step == 7:

            sommets = []

            for x in range(len(self.points)//4):

                sommets.append(self.points[x*4+1])

                sommets.append(self.points[x*4+3])

            main_sommets = []

            for x in range(len(self.points)//4):

                main_sommets.append(self.points[x*4+2])

            vects = [sum_arrays(sommets[x], main_sommets[x//2], -1) for x in range(len(sommets))]

            points = self.points.copy()

            for x in range(len(sommets)):

                delta = set_val_to_different_array([0, self.step_time], [1, 0], self.advance_time)

                apply_function_to_array(vects[x], lambda x:x*delta)

                sommets[x] = sum_arrays(vects[x], sommets[x])

                points[x*2+1] = sommets[x]

            pygame.draw.polygon(screen, get_inv_color(self.color), points)

        elif self.step == 8:

            for indx in range(len(self.line_angles)):

                delta_angle = set_val_to_different_array([0, self.step_time], [0, -pi/3], self.advance_time)

                self.line_angles[indx] += delta_angle

            # draws triangle into circle

            pygame.draw.polygon(screen, get_inv_color(self.color), [Circle.get_pos_on_circle(self, ang) for ang in self.line_angles])

        elif self.step == 9:

            screen.fill(WHITE)

            pygame.draw.circle(screen, get_inv_color(self.color), [self.x, self.y], self.radius)

            pygame.draw.polygon(screen, self.color, self.points)

            pygame.display.update()

            SystemExit()

def main():

    play = True

    clicking = 0

    circle = Circle()

    while play:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                play = False

            elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):

                clicking = 1

            elif (event.type == pygame.MOUSEBUTTONUP) and (event.button == 1):

                clicking = 0

            elif (event.type == pygame.MOUSEMOTION):

                translation = event.rel

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_LEFT:

                    pass

        screen.fill(BLACK)

        circle.update()

        pygame.display.update()

        clock.tick(60)


if __name__ == "__main__":

    main()
