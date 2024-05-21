from pig_tv import *


class Horloge:

    def __init__(self):

        self.radius = int(screen_height//2.5)

        self.x = screen_width//2

        self.y = screen_height//2

        self.color = BLACK

    def update(self):

        Horloge.draw(self)

    def draw(self):

        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius, 5)

        angle_depart = -pi/2

        angle_step = (2*pi)/12

        for x in range(1, 13):

            angle_depart += angle_step

            pos = [self.x+cos(angle_depart)*(self.radius*0.9), self.y+sin(angle_depart)*(self.radius*0.9)]

            #pygame.draw.circle(screen, RED, (int(pos[0]), int(pos[1])), 15)

##            if x < 6:
##
##                pos[0] -= 35
##
##            elif 7 < x < 12:
##
##                pos[0] += 35
##
            if 4 < x < 8:

                pos[1] -= 25

            if (4 == x) or (x == 8):

                pos[0] += 10*((x==8) or -1)

                pos[1] -= 10
##
##            elif x == 12:
##
##                pos[0] += 35

            aff_txt(str(x), pos[0], pos[1], self.color, centre=1)

        cur_time = 0

        angle_depart = -pi/2

        lens_aiguille = [(1/2)*self.radius, (2/3)*self.radius, (4/5)*self.radius]

        valeurs_temps = Horloge.get_time(self)

        for x in range(3):

            len_aiguille = lens_aiguille[x]

            width = ((x-3)*-1)*3

            nombre = valeurs_temps[x]

            n_x = set_val_to_different_array([-1, 1], [self.x-len_aiguille, self.x+len_aiguille], (cos(angle_depart+angle_step*nombre)))

            n_y = set_val_to_different_array([-1, 1], [self.y-len_aiguille, self.y+len_aiguille], (sin(angle_depart+angle_step*nombre)))

            pygame.draw.line(screen, self.color, (self.x, self.y), (n_x, n_y), width)

    def get_time(self):

        array = [time.localtime().tm_hour % 12, time.localtime().tm_min, time.localtime().tm_sec]

        array[1] += array[2]/60

        array[0] += array[1]/60

        array[2] /= 5

        array[1] /= 5

        return array

def main():

    horloge = Horloge()

    play = True

    while play:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                play = False

            elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):

                mouse_pos = pygame.mouse.get_pos()


        screen.fill(WHITE)

        horloge.update()

        pygame.display.update()

        clock.tick(60)
    
if __name__ == "__main__":

    main()
