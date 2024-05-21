from pig_tv import *


class Brief:

    def __init__(self):

        self.x_border = screen_width//8

        self.y_border = screen_height//8

        self.pyg_rect = pygame.Rect(self.x_border, 2*self.y_border, screen_width-2*self.x_border, screen_height-4*self.y_border)

        self.metronome = 0

        self.opened = 0

        self.pulled = 0

    def draw(self, not_yet_step2):

        self.metronome = (self.metronome+1)%100

        pygame.draw.rect(screen, YELLOW, self.pyg_rect)

        A = [self.pyg_rect[0], self.pyg_rect[1]]

        B = [self.pyg_rect[0]+self.pyg_rect[2], self.pyg_rect[1]]

        C = [self.pyg_rect[0], self.pyg_rect[1]+self.pyg_rect[3]]

        D = [self.pyg_rect[0]+self.pyg_rect[2], self.pyg_rect[1]+self.pyg_rect[3]]

        E = [self.pyg_rect[0]+self.pyg_rect[2]//2, self.pyg_rect[1]+self.pyg_rect[3]//2]

        F = [E[0]-self.x_border, E[0]-self.x_border]

        G = [E[0]+self.x_border, E[0]-self.x_border]

        V = [self.pyg_rect[0]+self.pyg_rect[2]//2, self.pyg_rect[1]-self.pyg_rect[3]//2+10]

        E2 = [self.pyg_rect[0]+self.pyg_rect[2]//2, self.pyg_rect[1]+self.pyg_rect[3]//6]

        pygame.draw.line(screen, BLACK, A, B)

        pygame.draw.line(screen, BLACK, A, C)

        pygame.draw.line(screen, BLACK, C, D)

        pygame.draw.line(screen, BLACK, B, D)

        if (not self.opened) or not_yet_step2:

            pygame.draw.line(screen, BLACK, A, E)

            pygame.draw.line(screen, BLACK, E, B)

            pygame.draw.line(screen, BLACK, C, F)

            pygame.draw.line(screen, BLACK, D, G)

            aff_txt("Papa", 350, screen_height//2+50, taille=44)

            if (not self.opened) and ((self.metronome % 100) < 50):

                aff_txt("Click to open !", 260, screen_height-100)

        else:

            pygame.draw.polygon(screen, YELLOW, [A, V, B])

            pygame.draw.line(screen, BLACK, A, E2)

            pygame.draw.line(screen, BLACK, E2, B)

            pygame.draw.line(screen, BLACK, A, V)

            pygame.draw.line(screen, BLACK, V, B)

            pygame.draw.polygon(screen, WHITE, [A, E2, B])

            if self.pyg_rect[1] < 280:

                self.pyg_rect[1] += 1

            norme = 15

            if self.pulled == -1:

                M = [A[0]-2*norme, A[1]-2*norme]

                N = [B[0]-2*norme, B[1]-norme]

                pygame.draw.polygon(screen, WHITE, [A, B, N, M])

            elif self.pulled == 1:

                M = [A[0]+2*norme, A[1]-norme]

                N = [B[0]+2*norme, B[1]-2*norme]

                pygame.draw.polygon(screen, WHITE, [A, B, N, M])

    def read(self):

        pygame.draw.rect(screen, WHITE, self.pyg_rect)

        aff_txt("Joyeuse fête", 260, 350, taille=40)

        aff_txt("des pères !", 265, 450, taille=40)

        self.metronome = (self.metronome+1)%100

        if (self.metronome % 100) < 50:

            aff_txt("Click to turn !", 260, screen_height-60)

    def turn(self):

        pygame.draw.rect(screen, WHITE, self.pyg_rect)

        if self.pyg_rect[0] < screen_width-self.x_border:

            vitesse = 5

            self.pyg_rect[0] += vitesse

            self.pyg_rect[2] -= 2*vitesse

        else:

            return 1


class Heart(Particule):

    def __init__(self, x, y, size):

        Particule.__init__(self, x, y)

        self.size = size

    def update(self):

        if out_screen(self.x, self.y, screen_width, screen_height):

            return 1

        Particule.stear_off_screen(self)

        Particule.apply_vect(self)

        Heart.draw(self)

    def draw(self):

        draw_heart(self.x, self.y, self.size)


class Polygon(Particule):

    def __init__(self, x, y, size, vertices_nb):

        self.size = size

        self.vertices_nb = vertices_nb

        Particule.__init__(self, x, y)

        self.colors = [get_random_color() for x in range(self.size//2)]

        self.vitesse = random.randint(1, 5)/4

        self.compteur = 0

        rand_index = random.randint(0, 2)

        rand_index2 = random.randint(0, 2)

        self.color = [255 for x in range(3)]  #get_random_color()

        self.color[rand_index] = 0

        self.color[rand_index2] = 127

    def update(self):

        if out_screen(self.x, self.y, screen_width+3*self.size, screen_height+3*self.size, min_x=-3*self.size, min_y=-3*self.size):

            return 1

        Particule.stear_off_screen(self)

        Particule.apply_vect(self, self.vitesse)

        Polygon.draw(self)

    def draw(self):

        self.compteur += 1

        vertices = []

        steps = (2*pi)/self.vertices_nb

        for x in range(self.vertices_nb):

            vertices.append([self.x+self.size*cos(self.compteur+x*steps), self.y+self.size*sin(self.compteur+x*steps)])

        pygame.draw.polygon(screen, self.color, vertices)


class Flower(Particule):

    def __init__(self, x, y, size):

        self.size = size

        Particule.__init__(self, x, y)

        self.colors = [get_random_color() for x in range(self.size//2)]

        self.vitesse = random.randint(1, 5)/4

        self.compteur = 0

        rand_index = random.randint(0, 2)

        self.color = [255 for x in range(3)]  #get_random_color()

        self.color[rand_index] = 0

    def draw(self):

        petal_nb = self.size // 4

        draw_flower(self.x, self.y, self.size, YELLOW, self.colors, petal_nb, self.compteur)

        self.compteur -= 0.01

    def update(self):

        if out_screen(self.x, self.y, screen_width+3*self.size, screen_height+3*self.size, min_x=-3*self.size, min_y=-3*self.size):

            return 1

        Particule.stear_off_screen(self)

        Particule.apply_vect(self, self.vitesse)

        Flower.draw_babe(self)

    def draw_babe(self):

        petal_nb = self.size // 2

        draw_flower(self.x, self.y, self.size, self.color, self.colors, petal_nb, self.compteur)

        self.compteur += 0.01  # pygame.draw.circle(screen, RED, [int(self.x), int(self.y)], self.size)
      

class Arrow(Particule):

    def __init__(self):

        self.size = 10

        Particule.__init__(self, screen_center[0]-self.size//2, screen_center[1]+50)

        self.color = GREEN

        self.show = 0

    def draw(self):

        if self.show:

            draw_fleche(self.x, self.y, self.size, self.color)

            self.y -= .6

            self.size += .3

            self.x = screen_center[0]-self.size//2

            if self.y < screen_center[1]:

                self.y = screen_center[1]+50

                self.size = 10

                self.x = screen_center[0]-self.size//2


def main():

    hearts = []

    brief = Brief()

    arrow = Arrow()

    flower = Flower(screen_center[0], screen_center[1], 30)

    flower_babes = [Flower(screen_center[0]+random.randint(-100, 100)/100, screen_center[1]+random.randint(-100, 100)/100, random.randint(10, 20)) for x in range(10)]

    step = 0

    play = True

    heart_append = 0

    clicking = 0

    a = time.time()

    saved_pos = screen_center

    while play:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                play = False

            elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):

                clicking = 1

                mouse_pos = pygame.mouse.get_pos()

                if not brief.opened:

                    heart_append = 10

                    brief.opened = 1

                elif step == 1:

                    saved_pos = mouse_pos

                elif step == 2:

                    step = 3

            elif (event.type == pygame.MOUSEBUTTONUP) and (event.button == 1):

                clicking = 0

                if step == 1:

                    mouse_pos = pygame.mouse.get_pos()

                    if saved_pos[1]-100 > mouse_pos[1]:

                        step = 2

            elif (event.type == pygame.MOUSEMOTION):

                translation = event.rel

                if clicking and (step == 1) and (translation[1] < 0):

                    if pygame.mouse.get_pos()[0] < screen_center[0]:

                        brief.pulled = -1

                    else:

                        brief.pulled = 1

        screen.fill(LIGHT_RED)

        if step < 2:

            brief.draw(heart_append)

            arrow.draw()

            if heart_append and random.randint(0, 5) == 0:

                hearts += [Heart(screen_center[0]+random.randint(-100, 100)/100, screen_center[1]+random.randint(-100, 100)/100, random.randint(5, 25)) for x in range(5)]

                heart_append -= 1

            for x in range(len(hearts)-1, -1, -1):

                out = hearts[x].update()

                if out:

                    del hearts[x]

                    if hearts == []:

                        arrow.show = 1

                        step = 1

        elif step == 2:

            brief.read()

        elif step == 3:

            done = brief.turn()

            if done:

                step = 4

                flower_append = 15

        if step == 4:

            flower.draw()

            if flower_append and (random.randint(0, 30) == 0):

                for x in range(5):

                    if not random.randint(0, 5):

                        flower_babes.append(Flower(screen_center[0]+random.randint(-100, 100)/100, screen_center[1]+random.randint(-100, 100)/100, random.randint(8, 16)))

                    else:

                        flower_babes.append(Polygon(screen_center[0]+random.randint(-100, 100)/100, screen_center[1]+random.randint(-100, 100)/100, random.randint(30, 50), random.randint(3, 8)))

                flower_append -= 1

            for x in range(len(flower_babes)-1, -1, -1):

                out = flower_babes[x].update()

                if out:

                    del flower_babes[x]

                    if (flower_babes == []) and (flower_append == 0):

                        step = 5

                        compteur = screen_width//2

        if step == 5:

            flower.draw()

            compteur -= 40

            if not compteur < 0:

                for y in range(screen_height):

                    for x in range(screen_width):

                        if (y-screen_center[1])**2+(x-screen_center[0])**2 > compteur**2:

                            screen.set_at((x, y), BLACK)

            else:

                screen.fill(BLACK)

                aff_txt("Bisous !", screen_width//2-50, screen_height//2-30, RED)

                play = False

        pygame.display.update()

        clock.tick(60)

if __name__ == "__main__":

    main()
