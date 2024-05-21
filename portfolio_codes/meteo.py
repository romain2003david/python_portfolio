"""
Programme pour enfin avoir un temps souhaitable et souhaité
09/2018
1280 : 2561
"""

from pig_tv import *


class Sun:

    def __init__(self, y_move):

        self.radius = 100

        self.x = screen_width/2

        self.y = screen_height

        self.y_move = y_move

    def update(self):

        self.y -= self.y_move

        Sun.draw(self)

        if self.y + self.radius < 0:

            self.y_move *= -1

        if self.y - self.radius > screen_height:  # sun's down again

            return 1

    def draw(self):

        pygame.draw.circle(screen, (255, 255, 0), (int(self.x), int(self.y)), self.radius)


class Lune:

    def __init__(self):

        self.x = int(screen_width*0.7)

        self.y = int(screen_height/4)

        self.rayon = 50

    def draw(self, sky_color):

        pygame.draw.circle(screen, (255, 255, 255), (self.x, self.y), self.rayon)

        pygame.draw.circle(screen, sky_color, (self.x-30, self.y), self.rayon)        


class Lift:
    """ Le petit ascenseur avec lequel l'utilisateur choisit une valeur numerique """
    def __init__(self, x, y):

        self.x = x

        self.y = y

        self.largeur = 200

        self.hauteur = 10

        self.cote_carre = 16

        self.rail = pygame.Rect(x, y, self.largeur, self.hauteur)

        self.carre = pygame.Rect(x+self.largeur/2-self.cote_carre/2, y - (self.cote_carre-self.hauteur)/2, self.cote_carre, self.cote_carre)

        self.echelle = 0  # puissance du vent, de -x a x

    def draw(self):

        pygame.draw.rect(screen, (50, 150, 50), self.rail)

        pygame.draw.rect(screen, (215, 50, 50), self.carre)

        self.echelle

    def get_vent(self):

        return int(self.echelle / (self.largeur/2)*10)

    def clicked(self, pos):

        return (self.carre.collidepoint(pos))

    def go(self, translation):

        self.carre[0] += translation[0]

        if self.carre[0] > self.x+self.largeur:

            self.carre[0] = self.x+self.largeur

        elif self.carre[0] < self.x:

            self.carre[0] = self.x

        self.echelle = self.carre[0] - (self.x+self.largeur/2)


class Particule:

    def __init__(self, largeur, hauteur, forme, vitesse):

        self.gravite = 1

        self.acceleration = 0.08

        self.vitesse = vitesse  # pluie different de neige (+ rapide)

        self.y = random.randint(int(-(screen_height)), 0)

        self.x = random.randint(0, screen_width)

        # distance de la camera : plus la particule est proche, plus elle est grosse et va vite
        self.distance = random.randint(60, 180)/100

        self.largeur = largeur / self.distance

        self.hauteur = hauteur / self.distance

        self.forme = forme

        if self.forme:
            self.element = pygame.Rect(self.x, self.y, self.largeur, self.hauteur)
        else:
            self.element = [(int(self.x), int(self.y)), self.hauteur]

    def update(self, vent):

        self.gravite += self.acceleration
        self.y += self.gravite * self.distance * self.vitesse

        if self.y > 0:

            trans_x = vent

            self.x += (trans_x/4) * self.distance * self.vitesse

        if self.forme:

            self.element = pygame.Rect(self.x, self.y, self.largeur, self.hauteur)
        else:

            self.element = [(int(self.x), int(self.y)), self.hauteur]

    def off_screen(self):

        if self.y > screen_height:

            self.x = random.randint(0, screen_width)
            self.gravite = 1
            self.y = random.randint(int(-(screen_height/6)), 0)


class Eclair:

    def __init__(self):

        embranchement = random.randint(3, 5)

        self.parties = []

        for x in range(embranchement+1):
            if x == 0:
                n_x = random.randint(100, screen_width-100)
                n_line = [[n_x, 0], [n_x + random.randint(-60, -10), int(screen_height/embranchement)], random.randint(4, 7)]
            else:
                if x%2 == 1:
                    n_line = [[self.parties[x-1][1][0], self.parties[x-1][1][1]], [n_x + random.randint(10, 60), int(screen_height/embranchement)*(x+1)], random.randint(x*-1 + embranchement+1, x*-1 + (embranchement+1)*2)]

                else:
                    n_line = [[self.parties[x-1][1][0], self.parties[x-1][1][1]], [n_x + random.randint(-60, -10), int(screen_height/embranchement)*(x+1)], random.randint(x*-1 + embranchement+1, x*-1 + (embranchement+1)*2)]

            self.parties.append(n_line)

    def draw(self):

        for partie in self.parties:

            pygame.draw.line(screen, (255, 255, 255), partie[0], partie[1], partie[2])
                    

class Rain:

    def __init__(self, intens1, intens2):

        self.intensite = random.randint(intens1, intens2)

        self.gouttes = [Particule(1, 4, 1, 1) for x in range(self.intensite)]

        self.color = (0, 0, 255)

    def update(self, vent):

        for goutte in self.gouttes:

            goutte.off_screen()

            goutte.update(vent)

            if goutte.y >= 0:
                pygame.draw.rect(screen, self.color, goutte.element)


class Snow:

    def __init__(self, intens1, intens2):

        self.intensite = random.randint(intens1, intens2)

        self.flocons = [Particule(2, 2, 0, 0.6) for x in range(self.intensite)]

        self.color = (255, 255, 255)

    def update(self, vent):

        for flocon in self.flocons:

            flocon.off_screen()

            flocon.update(vent)

            if flocon.y >= 0:

                pygame.draw.circle(screen, self.color, flocon.element[0], int(flocon.element[1]))


class Storm:

    def __init__(self):
        
        self.pluie = Rain(400, 600)

        self.duree = 0

        self.eclair = 0

    def update(self, vent):

        self.pluie.update(vent)

        if self.duree > 0:

            self.eclair.draw()

            self.duree -= 1

        elif random.randint(0, 70) == 0:

            self.eclair = Eclair()

            self.duree = 10


class Cloud:

    def __init__(self, inputs):

        color, rad = inputs

        self.width = 120

        self.y = random.randint(-20, 400)

        self.height = 60


        if not random.randint(0, 1):

            self.x = -self.width

            self.x_move = 1

        else:

            self.x = screen_width

            self.x_move = -1

        self.circles = [[random.randint(self.x, self.x+self.width), random.randint(self.y, self.y+self.height)] for x in range(8)]

        self.circles.append([self.x, self.y+self.height//2])

        self.circles.append([self.x+self.width, self.y+self.height//2])

        self.radius = rad

        self.color = color

    def update(self, vent, weather_infos):

        for circ in self.circles:

            circ[0] += self.x_move+vent/9

        Cloud.draw(self)

        stearing_speed = 100

        color, rad = weather_infos

        if color != self.color:

            self.color = [self.color[x]+(color[x]-self.color[x])/stearing_speed for x in range(3)]  # stears towards ideal

            self.color = [color[x]*(abs(self.color[x]-color[x]) < 1) or (self.color[x]) for x in range(3)]  # if almost good then alright

        if rad != self.radius:

            self.radius += (rad-self.radius) / stearing_speed  # stears towards ideal

            if abs(self.radius-rad) < 1:  # if almost good then alright

               self.radius = rad 

    def draw(self):

        for x in self.circles:

            pygame.draw.circle(screen, self.color, [int(x[0]), int(x[1])], int(self.radius))  # get_random_color()


class BG:

    def __init__(self, night_color):

        self.color = night_color

        self.dream_color = [255-self.color[2], 255-self.color[2], 255]

        self.vector_speed_change = 1000  # the smaller the faster

        BG.define_vector(self)

    def update_dream(self, n_dream):

        self.dream_color = n_dream

        BG.define_vector(self)

    def define_vector(self):

        self.color_vector = [(self.dream_color[x]-self.color[x])/1000 for x in range(3)]

        self.vector_compteur = self.vector_speed_change

    def update(self):

        BG.update_color(self)

        BG.draw(self)

    def update_color(self):

        if self.vector_compteur:

            self.color = sum_arrays(self.color, self.color_vector)

            self.vector_compteur -= 1

        for x in range(3):

            if self.color[x] < 0:

                self.color[x] = 0

                self.color_vector = [0 for x in range(3)]

            elif self.color[x] > 255:

                self.color[x] = 255

                self.color_vector = [0 for x in range(3)]

    def draw(self):

##        if not random.randint(0, 200):
##
##            print(self.color, self.color_vector)

        screen.fill(self.color)


def main(inputs):

    time_speed = inputs[0]

    night_color = [0, 0, 40]

    sun = Sun(time_speed)

    lift = Lift(int(screen_height/20), screen_height - int(screen_height/5))

    moon = Lune()

    night = 0

    bg = BG(night_color)

    clouds = []

    weather_list = [["Sun", (255, 255, 255)], ["Rain", (150, 150, 150)], ["Storm", (80, 80, 100)], ["Snow", (200, 208, 215)]]

    current_weather = 0
 
    weather_buttons = [Panneau(weather_list[x][0], 0+x*210, screen_height-100, color=get_random_color(), y_focus=-18) for x in range(len(weather_list))]

    aff = True

    lift_clicked = 0

    clicking = 0

    stars = [[random.randint(0, screen_width), random.randint(0, screen_height*0.8)] for k in range(75)]  # , random.randint(1, 2)

    cloud_infos = {0:[300, WHITE, 30],
                     1:[300, GREY, 50],
                     2:[120, DARK_GREY, 90],
                     3:[300, LIGHT_GREY, 30]}

    active_weather = 0

    while aff:

        for event in pygame.event.get():

            if event.type == QUIT:

                aff_txt("bye", 250, 300, color=(255, 0, 0))

                aff = False

            if event.type == pygame.KEYDOWN:

                if (event.key == K_SPACE) and (njour == 1):

                    pass

            if (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):

                mouse_pos = pygame.mouse.get_pos()

                if not clicking:  # just clicked, is not clicked for several frames, which could end up calling a button's effect several times

                    for button in weather_buttons:

                        if button.clicked(mouse_pos):

                            current_weather = weather_buttons.index(button)

                            bg.update_dream(weather_list[current_weather][1])

                            if current_weather == 0:

                                active_weather = 0

                            elif current_weather == 1:

                                active_weather = Rain(200, 300)

                            elif current_weather == 2:

                                active_weather = Storm()

                            elif current_weather == 3:

                                active_weather = Snow(200, 300)


                if lift.clicked(mouse_pos):

                    lift_clicked = 1

                clicking = 1

            if (event.type == pygame.MOUSEMOTION):

                translation = event.rel

                if lift_clicked:

                    lift.go(translation)

            if (event.type == pygame.MOUSEBUTTONUP) and (event.button == 1):

                clicking = 0

                lift_clicked = 0

        if not random.randint(0, cloud_infos[current_weather][0]):  # chances of cloud vary depending on weather

            clouds.append(Cloud(cloud_infos[current_weather][1:]))

        vent = lift.get_vent()

        # draws what needs to be drawn

        bg.update()

        if not night:

            night = sun.update()

            if night:

                bg.update_dream(night_color)

        else:

            moon.draw(bg.color)

            for star in stars:

                pygame.draw.circle(screen, WHITE, star, random.randint(1, 3))

        for cloud in clouds:

            cloud.update(vent, cloud_infos[current_weather][1:])

        for button in weather_buttons:

            button.draw()

        if active_weather:

            active_weather.update(vent)

        lift.draw()

        pygame.display.update()

        clock.tick(60)


if __name__ == "__main__":

    pygame.display.set_caption("Meteo")

    main([1])
