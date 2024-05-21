from pig_tv import *
##
##from screen_filters2 import *
##
##
##def ease_image(colors, screen_format, largeur_carre=4):
##
##    x_max, y_max = screen_format
##
##    for y1 in range(0, (y_max-2)//largeur_carre):
##
##        for x1 in range(0, (x_max-2)//largeur_carre):
##
##            y, x = y1*largeur_carre+1, x1*largeur_carre+1
##
##            cur_color = Arr(list(screen.get_at((x, y))[:3]))
##
##            distances = []
##
##            for color in colors:
##
##                distances.append((cur_color-color).norme_eucli())
##
##            index = distances.index(min(distances))
##
##            #screen.set_at((x, y), colors[index])
##
##            rect = pygame.Rect(x-largeur_carre//2, y-largeur_carre//2, largeur_carre, largeur_carre)
##
##            pygame.draw.rect(screen, colors[index], rect)
##
##        pygame.display.update()
##
##
##def chose_colors(nb_colors=1):
##
##    play = True
##
##    clicking = 0
##
##    colors = []
##
##    while len(colors) < nb_colors:
##
##        for event in pygame.event.get():
##
##            if event.type == pygame.QUIT:
##
##                play = False
##
##            elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):
##
##                colors.append(Arr(screen.get_at(pygame.mouse.get_pos())[:3]))
##
##                print(colors[-1])
##
##        pygame.display.update()
##
##        clock.tick(60)
##
##    return colors
##
##
##def main():
##
##    picture_path = "D:\photos\\05.10.2019\IMG_20190713_132708758.jpg"
##
##    img = pygame.image.load(picture_path)
##
##    frame = img.get_rect()
##
##    im_width, im_height = frame[2], frame[3]
##
##    ratio_pb = max(im_width/screen_width, im_height/screen_height)
##
##    if ratio_pb > 1:
##
##        n_format = (int(im_width/ratio_pb), int(im_height/ratio_pb))
##
##    else:
##
##        n_format = (im_width, im_height)
##
##    screen = pygame.display.set_mode(n_format)
##
##    img = pygame.transform.scale(img, n_format)
##
##    screen.blit(img, (0, 0))
##
##    pygame.display.update()
##
##    colors = [Arr ((132, 119, 110))]+[Arr( (190, 122, 73)), Arr( (35, 18, 11)), Arr ((220, 175, 142)), Arr( (103, 68, 46)), Arr ((88, 54, 45)), Arr ((75, 100, 68))]
##
##    ease_image(colors, n_format)
##
##    set_fast_blur(n_format[0], n_format[1], 3)
##
##    
##main()
##


class Dent:

    def __init__(self, index, speed, size, color=None):

        self.index = index

        self.pos = Arr([[0, screen_width][self.index%2], [0, screen_height][self.index//2]])

        #self.orginin_pos = self.pos.copy()

        self.speed = Arr(screen_center)-self.pos

        self.speed.normalize(1)

        mvmt_orth = self.speed.get_orth()

        self.size = size

        proportion = 0.2

        self.sommets = [self.pos + self.size*(-1*self.speed+(proportion*x)*mvmt_orth) for x in [-1, 1]]

        self.speed.normalize(speed)

        self.sommets.append(self.pos)

        if color == None:

            self.color = get_random_color()

        else:

            self.color = color

        self.origin_color = self.color.copy()

        self.activated = 0

    def update(self):

        for x in rl(self.sommets):

            self.sommets[x] += self.speed

        self.pos = self.sommets[2]

    def draw(self):

        pygame.draw.polygon(screen, self.color, self.sommets)

    def change_color(self):

        self.color = get_random_color()

    def collide(self, pos):

        return collide_point_polygon(pos, [x.liste for x in self.sommets])

    def activate(self):

        self.color = RED

        self.activated = 1

    def unactivate(self):

        self.color = self.origin_color.copy()

        self.activated = 0

    def move_pos(self, add):

        self.pos += add

        self.sommets[2] = self.pos

    def is_aside(self):

        return (self.pos-Arr(screen_center)).norme_eucli() > screen_height/2-30

        
def dents_centre():

    dents = [Dent(x, 10, 250) for x in range(4)]

    play = True

    clicking = 0

    while dents[0].pos[0] < screen_width+dents[0].size*2:

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

        screen.fill(YELLOW)

        for dent in dents:

            dent.update()

            dent.draw()

        pygame.display.update()

        clock.tick(60)

    return [dent.color for dent in dents]


def dents_centre2(colors):

    dents = [Dent(x, 6, 600, colors[x]) for x in range(4)]

    play = True

    clicking = 0

    while play:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                play = False

            elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):

                clicking = 1

                for dent in dents:

                    mouse_pos = pygame.mouse.get_pos()

                    if dent.collide(mouse_pos):

                        dent.change_color()

            elif (event.type == pygame.MOUSEBUTTONUP) and (event.button == 1):

                clicking = 0

            elif (event.type == pygame.MOUSEMOTION):

                translation = event.rel

        screen.fill(YELLOW)

        if dents[0].pos[0] < screen_center[0]:

            for dent in dents:

                dent.update()

        for dent in dents:

            dent.draw()

        if dents[0].pos[0] > screen_center[0]:

            play = False

        pygame.display.update()

        clock.tick(60)

    return dents


##class EventDealer:
##
##    def __init__(self):
##
##        pass
##
##    
def dents_sides(dents):

    play = True

    clicking = 1

    pressing = 0

    active_dent = None

    aside_dents = []

    while play:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                play = False

            elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):

                clicking = 1

                active_dent = None

                for dent in dents:

                    dent.unactivate()

                    mouse_pos = pygame.mouse.get_pos()

                    if dent.collide(mouse_pos):

                        dent.activate()

                        active_dent = dent

            elif (event.type == pygame.MOUSEBUTTONUP) and (event.button == 1):

                clicking = 0

            elif (event.type == pygame.MOUSEMOTION):

                translation = event.rel

            elif event.type == pygame.KEYDOWN:

                pressing = 1

            elif event.type == pygame.KEYUP:

                pressing = 0

        # moving teeths
        if pressing and active_dent != None:

            speed = 5

            if event.key == pygame.K_LEFT:

                active_dent.move_pos(Arr([-speed, 0]))

            if event.key == pygame.K_RIGHT:

                active_dent.move_pos(Arr([speed, 0]))

            if event.key == pygame.K_UP:

                active_dent.move_pos(Arr([0, -speed]))

            if event.key == pygame.K_DOWN:

                active_dent.move_pos(Arr([0, speed]))

            if active_dent.is_aside():

                if not active_dent in aside_dents:

                    aside_dents.append(active_dent)

                    if len(aside_dents) == 4:

                        play = False

        screen.fill(YELLOW)

        for dent in dents:

            dent.draw()

        pygame.display.update()

        clock.tick(60)


def txt_clignotant(string, c, lines=1):

    if c % 60 < 35:

        if lines == 1:

            aff_txt(string, 100, 350)

        else:

            y = 350

            for str_ in string:

                aff_txt(str_, 100, y)

                y += 30

    pygame.display.update()


def dessiner_invite(c):

    screen.fill(YELLOW)

    txt_clignotant("Click whatever you want to start", c)


def dessiner_invite2(c):

    rect = pygame.Rect(100, 350, 650, 80)

    pygame.draw.rect(screen, RED, rect)

    txt_clignotant(["Click on the teeths and", "use the arrows to move them aside !"], c, 2)


def dessiner_invite3(c):

    screen.fill(YELLOW)

    txt_clignotant("Now we can move on !", c)


class Figure:

    def __init__(self, nb_pt, pos=Arr.get_nul([2]), size=100):

        self.pos = pos

        self.pts_relatif = [Arr.get_random(norme=random.randint(size//2, size)) for n in range(nb_pt)]

        self.real_pts = [pt_pos+self.pos for pt_pos in self.pts_relatif]

        self.rotation_speed = random.random()

        self.color = get_random_color()

    def update_pos(self, add):

        self.pos += add

        self.real_pts = [pt_pos+self.pos for pt_pos in self.pts_relatif]

    def draw(self):

        pygame.draw.polygon(screen, self.color, self.real_pts)

    def rotate(self):

        mat_rota = Arr.get_mat_rot2D(self.rotation_speed)

        for x in rl(self.pts_relatif):

            #print(mat_rota, self.pts_relatif[x] , mat_rota*x)

            self.pts_relatif[x] = mat_rota*self.pts_relatif[x]  # dot product

            print(self.pts_relatif[x], self.pos)

        self.real_pts = [pt_pos+self.pos for pt_pos in self.pts_relatif]


def geometrie_vole():

    play = True

    clicking = 0

    figures = [Figure(random.randint(3, 7), random_pt_in_screen()) for x in range(10)]

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

        screen.fill(YELLOW)

        for fig in figures:

            fig.rotate()

            fig.draw()

        pygame.display.update()

        clock.tick(60)


def main():

    affichage_while_condition(dessiner_invite, 1, 1)
##
##    dents = dents_centre()
##
##    dents = dents_centre2(dents)
##
##    affichage_while_condition(dessiner_invite2, 1, 1)
##
##    dents_sides(dents)
##
##    affichage_while_condition(dessiner_invite3, 1, 1)

    geometrie_vole()

    

    
main()

    
