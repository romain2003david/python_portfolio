from pig_tv import *


def fact(n):

    if n == 0:

        return 1

    return n*fact(n-1)


def coef_bin(k, n):

    return fact(n)//(fact(k)*fact(n-k))


def berni(i, n, t):

    return coef_bin(i, n)*t**i*(1-t)**(n-i)


def plus(liste):

    if len(liste) == 1:

        return liste[0]

    else:

        return liste[0]+plus(liste[1:])

    
class Attache:

    def __init__(self, pt1, pt2, tile_width):

        self.color = BLACK

        self.pas = 0.01

        self.pts = []

        taille = random.randint(int(tile_width/5), int(tile_width/4))

        vect = (Arr(pt2)-Arr(pt1))

        deplace_vect = vect.copy()

        deplace_vect.normalize(taille)

        orth = vect.get_orth()

        self.orth = orth

        orth.normalize(taille)

        orth *= random.choice([-1, 1])

        fact_avant = (random.random()/2+1)/2

        fact_arrier = (random.random()/2+1)/2

        fact_rand = random.random()-0.5

        fact_length = 2

        half_vect = vect*(1/2)
        
        

        self.pts_controle = [Arr(pt1)+half_vect-deplace_vect*fact_avant, Arr(pt1)+half_vect-2*deplace_vect*fact_avant+orth*(2/5)*fact_length, Arr(pt1)+half_vect+deplace_vect*fact_rand+orth*(2/3)*fact_length, Arr(pt1)+half_vect+2*deplace_vect*fact_arrier+orth*(2/5)*fact_length, Arr(pt1)+half_vect+deplace_vect*fact_arrier]  # [Arr([100, 100]), Arr([200, 100]), Arr([200, 200]), Arr([100, 200]), Arr([100, 200])]

        Attache.generate_pts(self)

    def generate_pts(self):

        self.pts = []

        n = len(self.pts_controle)

        for t in [i*self.pas for i in range(int(1/self.pas))]:

            n_pt = plus([self.pts_controle[i]*berni(i, n-1, t) for i in range(n)])

            n_pt.apply_fun(round)

            self.pts.append(n_pt)

    def draw_controle(self):

        for pt in self.pts_controle:#[self.pts_controle[0], self.pts_controle[-1]]:

            pt.apply_fun(round)

            pygame.draw.circle(screen, LIGHT_BLUE, pt, 10)

    def draw(self):


##        self.orth.normalize(1)
##
##        if self.orth == Arr ( [1, 0] ) :
##
##            Attache.draw_controle(self)

        pygame.draw.line(screen, WHITE, self.pts_controle[0], self.pts_controle[-1], 4)

        for pt in self.pts:

           # print(pt)

            screen.set_at(pt.liste, self.color)


class Line:

    def __init__(self, width, pente=None, ord_orig=None):

##        if angle == None:
##
##            angle_reduit = random.random()
##
##            self.angle = set_val_to_different_array([0, 1], [-pi/2, pi/2], angle_reduit)
##
##        if ord_orig == None:
##
##            self.ord_orig = random.randint(0, screen_height)
##
##        print(self.ord_orig)
##
##        self.pente = tan(self.angle)

        if pente == None:

            pt1, pt2 = get_random_point_in_screen(), get_random_point_in_screen()

            self.droite = get_droite_from_pt(pt1, pt2)  # [self.pente, self.ord_orig]

            self.pente, self.ord_orig = self.droite

        else:

            self.pente, self.ord_orig = pente, ord_orig

            self.droite = [self.pente, self.ord_orig]

        self.start_pos = (0, self.ord_orig)

        self.end_pos = (width, width*self.pente+self.ord_orig)

        self.pt_intersections = []

        self.color = BLACK  # get_random_color()

    def draw(self):

        pygame.draw.line(screen, self.color, self.start_pos, self.end_pos)

        #for pt in self.pt_intersections:

        #    pygame.draw.circle(screen, BLUE, pt, 10)

    def add_pt_intersec(self, n_pt):

        c = 0

        apply_function_to_array(n_pt, round)

        while c < len(self.pt_intersections) and n_pt <= self.pt_intersections[c]:

            c += 1

        self.pt_intersections.insert(c, n_pt)




class Screen:

    def __init__(self, tile_width):

        self.color = BLACK

        self.width = screen_width

        self.height = screen_height

        self.taille = [self.width, self.height]

        self.lines = []

        self.tile_width = tile_width

    def in_screen(self, pt):

        return (0<=pt[0]<=self.width and 0<=pt[1]<=self.height)

    def add_line(self, pente=None, ord_orig=None):

        line = Line(self. width, pente, ord_orig)

        Screen.add_intersections(self, line)

        self.lines.append(line)

    def add_intersections(self, n_line):

        for line in self.lines:

            pt = get_inter_from_droite(line.droite, n_line.droite, 1)

            if pt != None and Screen.in_screen(self, pt):

                n_line.add_pt_intersec(pt)

                line.add_pt_intersec(pt)

    def draw_attaches(self):

        for line in self.lines:

            for i in range(len(line.pt_intersections)-1):

                pt1, pt2 = line.pt_intersections[i], line.pt_intersections[i+1]

                atta = Attache(pt1, pt2, self.tile_width)

                atta.draw()

                #draw_test_circle(pt1, get_random_color())

                #draw_test_circle(pt2, get_random_color())

                #pygame.display.update()

                #wait()

    def draw(self):

        screen.fill(WHITE)

        for line in self.lines:

            line.draw()


#collide_segment_to_segment()
def main2(inputs):
    
    tile_width = inputs[0]

    play = True

    clicking = 0

    scree = Screen(tile_width)

    for i in range(screen_height//tile_width):

        scree.add_line(0, i*tile_width+30)
    for j in range(screen_height//tile_width):
        scree.add_line(100, -(i*tile_width)*100)
        #screen.add_line(0, 200)
    scree.draw()

    scree.draw_attaches()
    pygame.display.update()

    wait()

    return

    while play:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                play = False

            elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):

                clicking = 1

            elif (event.type == pygame.MOUSEBUTTONUP) and (event.button == 1):

                clicking = 0


        screen.draw()
        pygame.display.update()

        clock.tick(60)


def main():

    play = True

    clicking = 0

    atta = Attache()

    sel = 0


    while play:

        for event in pygame.event.get():

            screen.fill(WHITE)

            if event.type == pygame.QUIT:

                play = False

            elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):

                clicking = 1

            elif (event.type == pygame.MOUSEBUTTONUP) and (event.button == 1):

                clicking = 0

            elif (event.type == pygame.MOUSEMOTION):

                translation = event.rel

                atta.pts_controle[sel] = Arr(pygame.mouse.get_pos())

                atta.generate_pts()

                atta.draw()

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_q:

                    print(1)

                    atta.generate_pts()

                    atta.draw()

                if event.key == pygame.K_1:

                    sel = 0

                if event.key == pygame.K_2:

                    sel = 1

                if event.key == pygame.K_3:

                    sel = 2

                if event.key == pygame.K_4:

                    sel = 3

                if event.key == pygame.K_5:

                    sel = 4

        atta.draw_controle()

        pygame.display.update()

        clock.tick(60)
    
    wait()




if __name__ == "__main__":
    
    tile_width = 50

    main2([tile_width])
