from pig_tv import *


class Marcheur:

    def __init__(self):

        self.pos = Arr([random.randint(0, screen_width), random.randint(0, screen_height)])

        self.norme_vitesse = 8  # px.s^-1

        self.vitesse = Arr([random.randint(0, 100), random.randint(0, 100)])

        self.vitesse.normalize(self.norme_vitesse)

        self.bordure = 50

    def update(self):

        self.norme_vitesse += (random.random()-0.5)

        if self.norme_vitesse < 3:

            self.norme_vitesse += 0.1

        self.vitesse = self.vitesse + Arr.get_random()

        self.vitesse.normalize(self.norme_vitesse)

        self.pos = self.pos + self.vitesse

        Marcheur.stay_in_screen(self)

    def stay_in_screen(self):

        if self.pos[0] < self.bordure:

            if self.vitesse[0] < 0:

                self.vitesse[0] *= -1

        if self.pos[0] > screen_width-self.bordure:

            if self.vitesse[0] > 0:

                self.vitesse[0] *= -1

        if self.pos[1] < self.bordure:

            if self.vitesse[1] < 0:

                self.vitesse[1] *= -1

        if self.pos[1] > screen_height-self.bordure:

            if self.vitesse[1] > 0:

                self.vitesse[1] *= -1

    def draw(self):

        pygame.draw.circle(screen, RED, self.pos.with_fun_applied(round), 10)

        
class Plan:

    def __init__(self, unite=30):

        self.unite = unite

        self.x_coors = [x*self.unite for x in range(screen_width//self.unite)]

        self.y_coors = [y*self.unite for y in range(screen_height//self.unite)]

        self.cont = [[Arr([0, 0]) for x in self.x_coors] for y in self.y_coors]

        self.poles = [Marcheur() for x in range(4)]

        self.intensites = [[0 for x in self.x_coors] for y in self.y_coors]

    def update(self, mouse_pos):

        for pole in self.poles:

            pole.update()

        for y in range(len(self.cont)):

            for x in range(len(self.cont[y])):

                tot_intensite = 0

                force = Arr.get_nul()

                coor = Arr([self.x_coors[x], self.y_coors[y]])

                #self.poles[0].pos = Arr(mouse_pos)

                for pol in self.poles:

                    force_pol = pol.pos - coor

                    dist = force_pol.norme_eucli()

                    if dist < 0.1:

                        intensite = 10

                    else:

                        intensite = 1/dist

                    tot_intensite += intensite

                    force_pol.normalize(intensite)

                    force = force + force_pol

                tot_intensite *= 200

                if tot_intensite > 15:

                    tot_intensite = 15

                self.intensites[y][x] = tot_intensite

                force.normalize(norme=4+tot_intensite)

                self.cont[y][x] = force

    def draw(self):

        screen.fill(WHITE)

        for pole in self.poles:

            pass#pole.draw()

        for y in range(len(self.cont)):

            for x in range(len(self.cont[y])):

                vect = self.cont[y][x]

                coor = Arr([self.x_coors[x], self.y_coors[y]])

                indic = self.intensites[y][x]

                if indic > 6:

                    indic = 6

                red = set_val_to_different_array([0, 6], [0, 255], indic)

                color = [red, 255-red, 0]

                pygame.draw.line(screen, color, coor.liste, (coor+vect).liste)


def main():

    plan = Plan()

    play = True

    clicking = 0

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

        plan.update(pygame.mouse.get_pos())

        plan.draw()

        pygame.display.update()

        clock.tick(60)


main()









