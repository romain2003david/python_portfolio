from pig_tv import *


def draw_test_circle(pos):

    x, y = pos

    pygame.draw.circle(screen, RED, [int(x), int(y)], 10)


class Joint:

    def __init__(self, x, y, orientation, length):

        self.x = x

        self.y = y

        self.orientation = orientation

        self.length = length

    def get_end(self):

        return Joint(self.x+self.length*sin(self.orientation), self.y+self.length*cos(self.orientation), 0, 0)

    def fill_data(self, x=None, y=None, orientation=None, length=None):

        if x != None:

            self.x = x

        if y != None:

            self.y = y

        if orientation != None:

            self.orientation = orientation

        if length != None:

            self.length = length

    def get_pos(self):

        return [self.x, self.y]


class StickMan:

    def __init__(self, x, y, height=100):

        ## body data

        # head coors

        self.x = x

        self.y = y
        #

        # data about limbs lenghts

        self.height = height

        self.head_radius = height//4

        self.arm_length = height//2

        self.leg_length = int(height//1.7)

        self.shoulder_to_body_fract = 1/4

        self.forearms_to_biceps_fract = 0.6

        self.thig_to_calf_fract = 0.5

        # limb orientation

        StickMan.set_standing_posture(self)

        # each main point of body has a specific pos

        self.head = [self.x, self.y]

        # the other points will be defined thx to the position of the stickman (sitting, standing, lying..)

        self.shoulders = []

        self.elbows = [[], []]

        self.hands = [[], []]

        self.hips = []

        self.knees = [[], []]

        self.feets = [[], []]

        StickMan.build_posture(self)

    def set_standing_posture(self):
        """ sets limb orientation for standing position """

        self.body_orientation = 0  # -pi/2

        # shoulders

        self.r_shoulder_orientation = 2*pi/3

        self.l_shoulder_orientation = -self.r_shoulder_orientation

        # elbows
        self.r_elbow_orientation = pi/3

        self.l_elbow_orientation = -self.r_elbow_orientation

        # hips
        self.r_hip_orientation = pi/3

        self.l_hip_orientation = -self.r_hip_orientation

        # knees
        self.r_knee_orientation = 0

        self.l_knee_orientation = -self.r_knee_orientation

    def build_posture(self):
        """ sets the coors of the main points of the body thanks to the orientation data """

        x, y = self.x, self.y

        # creates the head, starting point
        self.head = Joint(x, y, self.body_orientation, self.head_radius)

        # creates neck
        self.neck = self.head.get_end()

        # creates shoulders
        self.neck.fill_data(orientation=self.body_orientation, length=self.arm_length*self.shoulder_to_body_fract)

        self.shoulders = self.neck.get_end()

        # creates biceps (well like I mean upper arm Ig?) (down to the elbows)

        self.shoulders.fill_data(orientation=self.r_shoulder_orientation, length=self.height*(1-self.forearms_to_biceps_fract))

        self.elbows[0] = self.shoulders.get_end()

        self.shoulders.fill_data(orientation=self.l_shoulder_orientation)

        self.elbows[1] = self.shoulders.get_end()

        # creates forearms (down to the hands)

        self.elbows[0].fill_data(orientation=self.r_elbow_orientation, length=self.height*self.forearms_to_biceps_fract)

        self.hands[0] = self.elbows[0].get_end()

        self.elbows[1].fill_data(orientation=self.l_elbow_orientation, length=self.height*self.forearms_to_biceps_fract)

        self.hands[1] = self.elbows[1].get_end()

        # creates core (down to the hips)
        self.neck.fill_data(orientation=self.body_orientation, length=self.height)

        self.hips = self.neck.get_end()

        # creates thighs (down to the knees)
        self.hips.fill_data(orientation=self.r_hip_orientation, length=self.height*(1-self.thig_to_calf_fract))

        self.knees[0] = self.hips.get_end()

        self.hips.fill_data(orientation=self.l_hip_orientation)

        self.knees[1] = self.hips.get_end()

        # creates calfs (down to the feets)

        self.knees[0].fill_data(orientation=self.r_knee_orientation, length=self.height*self.thig_to_calf_fract)

        self.feets[0] = self.knees[0].get_end()

        self.knees[1].fill_data(orientation=self.l_knee_orientation, length=self.height*self.thig_to_calf_fract)

        self.feets[1] = self.knees[1].get_end()

    def draw(self):
        """ easy part : just links the limbs with lines """

        thickness = 3

        # head

        pygame.draw.circle(screen, BLACK, self.head.get_pos(), self.head_radius, thickness)  # draws the head

        pygame.draw.line(screen, BLACK, self.neck.get_pos(), self.shoulders.get_pos(), thickness)

        # first arm

        pygame.draw.line(screen, BLACK, self.shoulders.get_pos(), self.elbows[0].get_pos(), thickness)

        pygame.draw.line(screen, BLACK, self.elbows[0].get_pos(), self.hands[0].get_pos(), thickness)

        # second arm

        pygame.draw.line(screen, BLACK, self.shoulders.get_pos(), self.elbows[1].get_pos(), thickness)

        pygame.draw.line(screen, BLACK, self.elbows[1].get_pos(), self.hands[1].get_pos(), thickness)

        # core

        pygame.draw.line(screen, BLACK, self.shoulders.get_pos(), self.hips.get_pos(), thickness)

        # first leg

        pygame.draw.line(screen, BLACK, self.hips.get_pos(), self.knees[0].get_pos(), thickness)

        pygame.draw.line(screen, BLACK, self.knees[0].get_pos(), self.feets[0].get_pos(), thickness)

        # second leg

        pygame.draw.line(screen, BLACK, self.hips.get_pos(), self.knees[1].get_pos(), thickness)

        pygame.draw.line(screen, BLACK, self.knees[1].get_pos(), self.feets[1].get_pos(), thickness)



##def main():
##
##    not_done = True
##
##    clicking = 0
##
##    string = ""
##
##    while not_done:
##
##        for event in pygame.event.get():
##
##            if event.type == pygame.QUIT:
##
##                not_done = False
##
##            elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):
##
##                clicking = 1
##
##            elif (event.type == pygame.MOUSEBUTTONUP) and (event.button == 1):
##
##                clicking = 0
##
##            elif (event.type == pygame.MOUSEMOTION):
##
##                translation = event.rel
##
##            elif event.type == pygame.KEYDOWN:
##
##                print(event.key)
##
##                if event.key == K_RETURN:
##
##                    not_done = False
##
##                elif event.key == 8:
##
##                    print(string)
##
##                    string = string[:-1]
##
##                    print(string)
##
##                else:
##
##                    string += event.unicode
##
##        screen.fill(WHITE)
##
##        aff_txt(string, 0, 0, BLACK)
##
##        pygame.display.update()
##
##        clock.tick(60)

def main():

    play = True

    clicking = 0

    stick_man = StickMan(400, 400)

    sens = 1

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

        screen.fill(WHITE)

        stick_man.draw()

        pygame.display.update()

        clock.tick(60)

main()
