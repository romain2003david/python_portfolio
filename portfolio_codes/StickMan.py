from pig_tv import *


def draw_test_circle(pos):

    x, y = pos

    pygame.draw.circle(screen, RED, [int(x), int(y)], 10)


def polar_to_cartesian_coors(angle, radius):

    return [radius*cos(angle), radius*sin(angle)]


def cartesian_to_polar_coors(x, y):

    dist = sqrt(x**2+y**2)

    if x == 0:

        if y > 0:

            angle = pi/2

        else:

            angle = -pi/2

    else:

        angle = atan(y/x)

    return [angle, dist]


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

    def set_pos(self, pos):

        self.x, self.y = pos


class StickMan:

    def __init__(self, x, y, index, height=100):

        self.ground = screen_height-100

        self.y_readjustment = 0  # when the body should be moved so as for it to be on the ground

        self.index = index

        ## body data

        self.body_pts = []  # is filled in build_posture

        # head coors

        self.x = x

        self.y = y
        #

        # data about limbs lenghts

        self.height = height

        self.head_radius = height//4

        self.arm_length = int(height*(.9))

        self.leg_length = int(height*(1.2))

        self.shoulder_to_body_fract = 1/4

        self.forearms_to_biceps_fract = 0.6

        self.thig_to_calf_fract = 0.5

        #

        self.on_ground_limbs = []

        ## data about positions

        self.positions_list = ["standing_front",
                               "needs_a_piss",
                               "standing_profile",
                               "sumo_squat_front",
                               "lying",
                               "hollow_body",
                               "plank",
                               ]

        # disctionnary that associates a position name with the list of joints orientations (neck, body, 2 shoulders, 2 elbow, 2 hips, 2 knees)
        self.positions = {"standing_front":[0, 0, pi/3, -pi/3, 0, 0, 0.4, -0.4, 0.4, -0.4],  # pi/2, 0, pi/3, -pi/3, 0, 0, 0.4, 0.4, 0.4, 0.4
                          "needs_a_piss":[0, 0, pi/3, -pi/3, 0, 0, 0.4, 0.4, 0.4, -0.4],
                          "standing_profile":[0, 0, .2, -.25, .4, 0.1, 0.3, 0, -0.15, -0.3],
                          "sumo_squat_front":[0, 0, pi/3, -pi/3, 0, 0, 1, -1, 0, 0],
                          "lying":[-pi/2, -pi/2, -pi/2+0.1, -pi/2-0.1, -pi/2+0.1, -pi/2-0.1, -pi/2+0.1, -pi/2-0.1, -pi/2+0.1, -pi/2-0.1],
                          "hollow_body":[-pi/2+0.3, -pi/2+0.3, pi+.2, pi/2-.3, pi+.2, pi/2-.3, -pi/2-.3, -pi/2-.4, -pi/2-.3, -pi/2-.4],
                          "plank":[-pi/2+0.3, -pi/2+0.3, 0, 0.1, 0, 0.1, -pi/2+.3, -pi/2+.4, -pi/2+.3, -pi/2+.4]
                          }

        for x in self.positions.values():

            if len(x) != 10:

                print("too many or too few joint orientations")

        # limb orientation

        StickMan.set_position(self, 2)  # standing position

        # enables to move a single joint in create movement
        self.joints = [self.neck_orientation, self.body_orientation, self.r_shoulder_orientation, self.l_shoulder_orientation, self.r_elbow_orientation, self.l_elbow_orientation, self.r_hip_orientation, self.l_hip_orientation, self.r_knee_orientation, self.l_knee_orientation,]

        # each main point of body has a specific pos

        # the other points will be defined thx to the position of the stickman (sitting, standing, lying..)

        self.elbows = [[], []]

        self.hands = [[], []]

        self.knees = [[], []]

        self.feets = [[], []]

        StickMan.build_posture(self)

        self.global_movements = []

        self.movements = []

        self.exercises = {"s":StickMan.squat,
                          "g":StickMan.pistol_squat,
                          "q":StickMan.stop_movements,
                          "e":StickMan.split,
                          "p":StickMan.push_up,
                          "i":StickMan.inverse_horizontally,
                          "m":StickMan.morning_routine,
                          "t":StickMan.rond_epaule_profil,
                          }

    def set_position(self, index):

        # gets orientations

        str_position = self.positions_list[index]

        joint_orientation_list = self.positions[str_position]

        # body
        self.neck_orientation = joint_orientation_list[0]

        self.body_orientation = joint_orientation_list[1]

        # shoulders

        self.r_shoulder_orientation = joint_orientation_list[2]

        self.l_shoulder_orientation = joint_orientation_list[3]

        # elbows
        self.r_elbow_orientation = joint_orientation_list[4]

        self.l_elbow_orientation = joint_orientation_list[5]

        # hips
        self.r_hip_orientation = joint_orientation_list[6]

        self.l_hip_orientation = joint_orientation_list[7]

        # knees
        self.r_knee_orientation = joint_orientation_list[8]

        self.l_knee_orientation = joint_orientation_list[9]

        StickMan.update_joints(self)

    def update_joints(self):

        self.joints = [self.neck_orientation, self.body_orientation, self.r_shoulder_orientation, self.l_shoulder_orientation, self.r_elbow_orientation, self.l_elbow_orientation, self.r_hip_orientation, self.l_hip_orientation, self.r_knee_orientation, self.l_knee_orientation,]

    def inverse_horizontally(self):

        for x in range(len(self.joints)):

            joint = self.joints[x]

            if joint >= 0:

                self.joints[x] = set_val_to_different_array([0, pi], [pi, 0], joint)

            else:

                self.joints[x] = set_val_to_different_array([0, -pi], [-pi, 0], joint)

        StickMan.build_posture(self)

    def update_body_points_coor(self):
        """ when self.body_pts has been modified """

        # unpacks pody_pts
        self.head, self.neck, self.shoulders, self.elbows[0], self.elbows[1], self.hands[0], self.hands[1], self.hips, self.knees[0], self.knees[1], self.feets[0], self.feets[1] = self.body_pts

        # chains of body joints
        self.upper_chain = [self.neck, self.shoulders, self.hips]

        self.r_arm_chain = [self.shoulders, self.elbows[0], self.hands[0]]

        self.l_arm_chain = [self.shoulders, self.elbows[1], self.hands[1]]

        self.r_leg_chain = [self.hips, self.knees[0], self.feets[0]]

        self.l_leg_chain = [self.hips, self.knees[1], self.feets[1]]

        self.body_chains = [self.upper_chain, self.r_arm_chain, self.l_arm_chain, self.r_leg_chain, self.l_leg_chain]

    def build_posture(self):
        """ sets the coors of the main points of the body thanks to the orientation data ; also checks if some limbs have to be on the ground, if yes returns the y diff that should be applied

        body pts (mainly joints)

        0:self.head,
        1:self.neck,
        2:self.shoulders,
        3:self.elbows[0],
        4:self.elbows[1],
        5:self.hands[0],
        6:self.hands[1],
        7:self.neck,
        8:self.hips,
        9:self.knees[0],
        10:self.knees[1],
        11:self.feets[0],
        12:self.feets[1]]

        """

        self.y_readjustment = 0

        # unpacks joints orientations
        self.neck_orientation, self.body_orientation, self.r_shoulder_orientation, self.l_shoulder_orientation, self.r_elbow_orientation, self.l_elbow_orientation, self.r_hip_orientation, self.l_hip_orientation, self.r_knee_orientation, self.l_knee_orientation = self.joints

        x, y = self.x, self.y

        # creates the head, starting point
        self.head = Joint(x, y, self.neck_orientation, self.head_radius)

        # creates neck
        self.neck = self.head.get_end()

        # creates shoulders
        self.neck.fill_data(orientation=self.neck_orientation, length=self.arm_length*self.shoulder_to_body_fract)

        self.shoulders = self.neck.get_end()

        # creates biceps (well like I mean upper arm Ig?) (down to the elbows)

        self.shoulders.fill_data(orientation=self.r_shoulder_orientation, length=self.arm_length*(1-self.forearms_to_biceps_fract))

        self.elbows[0] = self.shoulders.get_end()

        self.shoulders.fill_data(orientation=self.l_shoulder_orientation)

        self.elbows[1] = self.shoulders.get_end()

        # creates forearms (down to the hands)

        self.elbows[0].fill_data(orientation=self.r_elbow_orientation, length=self.arm_length*self.forearms_to_biceps_fract)

        self.hands[0] = self.elbows[0].get_end()

        self.elbows[1].fill_data(orientation=self.l_elbow_orientation, length=self.arm_length*self.forearms_to_biceps_fract)

        self.hands[1] = self.elbows[1].get_end()

        # creates core (down to the hips)
        self.neck.fill_data(orientation=self.body_orientation, length=self.height)

        self.hips = self.neck.get_end()

        # creates thighs (down to the knees)
        self.hips.fill_data(orientation=self.r_hip_orientation, length=self.leg_length*(1-self.thig_to_calf_fract))

        self.knees[0] = self.hips.get_end()

        self.hips.fill_data(orientation=self.l_hip_orientation)

        self.knees[1] = self.hips.get_end()

        # creates calfs (down to the feets)

        self.knees[0].fill_data(orientation=self.r_knee_orientation, length=self.leg_length*self.thig_to_calf_fract)

        self.feets[0] = self.knees[0].get_end()

        self.knees[1].fill_data(orientation=self.l_knee_orientation, length=self.leg_length*self.thig_to_calf_fract)

        self.feets[1] = self.knees[1].get_end()

        self.body_pts = [self.head, self.neck, self.shoulders, self.elbows[0], self.elbows[1], self.hands[0], self.hands[1], self.hips, self.knees[0], self.knees[1], self.feets[0], self.feets[1]]

        StickMan.update_body_points_coor(self)

        # checking if body's on the ground

        # translates the body on y axis (up or down)
        if len(self.on_ground_limbs) > 0:

            diff_ground = self.ground-self.body_pts[self.on_ground_limbs[0]].get_pos()[1]

            if abs(diff_ground) > self.y_readjustment:

                self.y_readjustment = diff_ground

        # rotates the body so that the second pt is also on the ground
        if len(self.on_ground_limbs) > 1:

            # defining circle where rotation takes place
            center_coor = self.body_pts[self.on_ground_limbs[0]].get_pos()

            other_point = self.body_pts[self.on_ground_limbs[1]].get_pos()

            # computing the variation angle (we know cartesian coordinates, radius, we miss angle)
            translated_pt = sum_arrays(other_point, center_coor, 1, -1)

            change_angle, radius = cartesian_to_polar_coors(translated_pt[0], translated_pt[1])

            # applying rotation angle to the other points of the body

            for x in range(len(self.body_pts)):

                if not x == self.on_ground_limbs[0]:  # pt that doesn't get rotated (that's already on the ground)

                    coors = self.body_pts[x].get_pos()

                    translated_coors = sum_arrays(coors.copy(), center_coor.copy(), 1, -1)

                    angle, dist = cartesian_to_polar_coors(translated_coors[0], translated_coors[1])

                    n_coors = polar_to_cartesian_coors(angle-change_angle, dist)

                    self.body_pts[x].set_pos(sum_arrays(n_coors.copy(), center_coor.copy(), 1, 1))

            StickMan.update_body_points_coor(self)

        #wait()
    def update(self, index):

        StickMan.update_movements(self)

        if index == self.index:

            StickMan.draw(self, BLUE)

        else:

            StickMan.draw(self)

    def draw(self, color=None):
        """ easy part : just links the limbs with lines """

        if color == None:

            color = BLACK

        pygame.draw.line(screen, color, [0, self.ground], [screen_width, self.ground])

        thickness = 3

        # head

        head_pos = self.head.get_pos()

        head_pos[1] += self.y_readjustment

        apply_function_to_array(head_pos, int)

        pygame.draw.circle(screen, color, head_pos, self.head_radius, thickness)  # draws the head

        for chain in self.body_chains:

            for x in range(len(chain)-1):

                pos = chain[x].get_pos()

                pos[1] += self.y_readjustment

                pos2 = chain[x+1].get_pos()

                pos2[1] += self.y_readjustment

                pygame.draw.line(screen, color, pos, pos2, thickness)

##        pygame.draw.line(screen, BLACK, self.neck.get_pos(special_y_focus), self.shoulders.get_pos(), thickness)
##
##        # first arm
##
##        pygame.draw.line(screen, BLACK, self.shoulders.get_pos(special_y_focus), self.elbows[0].get_pos(), thickness)
##
##        pygame.draw.line(screen, BLACK, self.elbows[0].get_pos(special_y_focus), self.hands[0].get_pos(), thickness)
##
##        # second arm
##
##        pygame.draw.line(screen, BLACK, self.shoulders.get_pos(special_y_focus), self.elbows[1].get_pos(), thickness)
##
##        pygame.draw.line(screen, BLACK, self.elbows[1].get_pos(special_y_focus), self.hands[1].get_pos(), thickness)
##
##        # core
##
##        pygame.draw.line(screen, BLACK, self.shoulders.get_pos(special_y_focus), self.hips.get_pos(), thickness)
##
##        # first leg
##
##        pygame.draw.line(screen, BLACK, self.hips.get_pos(special_y_focus), self.knees[0].get_pos(), thickness)
##
##        pygame.draw.line(screen, BLACK, self.knees[0].get_pos(special_y_focus), self.feets[0].get_pos(), thickness)
##
##        # second leg
##
##        pygame.draw.line(screen, BLACK, self.hips.get_pos(special_y_focus), self.knees[1].get_pos(), thickness)
##
##        pygame.draw.line(screen, BLACK, self.knees[1].get_pos(special_y_focus), self.feets[1].get_pos(), thickness)

    def create_movement(self, joint, move_range, rel_move=0, start_range="current", speed=.05, sens_inverse=0):
        """ creates a movement in chosen joint ;
            [0:self.neck_orientation,
             1:self.body_orientation,
             2:self.r_shoulder_orientation,
             3:self.l_shoulder_orientation,
             4:self.r_elbow_orientation,
             5:self.l_elbow_orientation,
             6:self.r_hip_orientation,
             7:self.l_hip_orientation,
             8:self.r_knee_orientation,
             9:self.l_knee_orientation,]

        """

        if rel_move:

            move_range = [self.joints[joint]+move_range[0], self.joints[joint]+move_range[1]]

        else:

            move_range.sort()

        if start_range != "current":

            self.joints[joint] = start_range

        if sens_inverse:

            sens = -1

        else:

            sens = 1

        self.movements.append([joint, move_range, sens, speed])

    def del_movement(self, index=0):

        if len(self.movement) > index:

            del self.movement[index]

        else:

            print("This movement doesn't exist.")

    def stop_movements(self):

        self.movements = []

    def update_movements(self):
        """ enables to move single joints ; the whole body needs however to be recreated """

        if self.global_movements != []:

            self.global_movements[0][1] -= 1  # takes out one tick of movement lifes span

            if self.global_movements[0][1] == 0:  # movement finished

                del self.global_movements[0]

                StickMan.stop_movements(self)

                if self.global_movements != []:

                    self.global_movements[0][0](self)

        if self.movements != []:

            for x in range(len(self.movements)):

                joint_ori = self.joints[self.movements[x][0]]

                move_range = self.movements[x][1]

                if (joint_ori > move_range[1]) or (joint_ori < move_range[0]):

                    self.movements[x][2] *= -1  # changes the growth direction

                self.joints[self.movements[x][0]] += self.movements[x][2]*self.movements[x][3]

            StickMan.build_posture(self)

    def squat(self):

        self.on_ground_limbs = []

        self.on_ground_limbs.append(11)

        StickMan.set_position(self, 2)

        self.r_elbow_orientation = 1.6

        self.l_elbow_orientation = 1.4

        self.r_shoulder_orientation = 1.6

        self.l_shoulder_orientation = 1.4

        StickMan.update_joints(self)
        
        StickMan.build_posture(self)

        speed = .02

        StickMan.create_movement(self, 6, [0, 1], 1, speed=speed)

        StickMan.create_movement(self, 7, [0, 1], 1, speed=speed)

        StickMan.create_movement(self, 8, [-1, 0], 1, speed=speed)

        StickMan.create_movement(self, 9, [-1, 0], 1, speed=speed)

    def pistol_squat(self):

        self.on_ground_limbs = []

        self.on_ground_limbs.append(10)

        StickMan.set_position(self, 2)

        self.r_elbow_orientation = 1.6

        self.l_elbow_orientation = 1.4

        self.r_shoulder_orientation = 1.6

        self.l_shoulder_orientation = 1.4

        self.l_hip_orientation = pi/2

        self.l_knee_orientation = pi/2-0.2

        StickMan.update_joints(self)
        
        StickMan.build_posture(self)

        speed = .01

        StickMan.create_movement(self, 6, [0, 1], 1, speed=speed)

        StickMan.create_movement(self, 8, [-1, 0], 1, speed=speed)

    def split(self):

        self.on_ground_limbs = []

        self.on_ground_limbs.append(11)

        StickMan.set_position(self, 0)

        #StickMan.update_joints(self)
        
        StickMan.build_posture(self)

        speed = .002

        end_move = 1.15

        StickMan.create_movement(self, 7, [-end_move, 0], 1, speed=speed)

        StickMan.create_movement(self, 6, [0, end_move], 1, speed=speed)

        StickMan.create_movement(self, 9, [-end_move, 0], 1, speed=speed)

        StickMan.create_movement(self, 8, [0, end_move], 1, speed=speed)

    def push_up(self):

        self.on_ground_limbs = []

        self.on_ground_limbs.append(10)

        self.on_ground_limbs.append(5)

        StickMan.set_position(self, 6)

        #StickMan.inverse_horizontally(self)

        self.l_shoulder_orientation = -.1

        self.l_elbow_orientation = -.1

        StickMan.update_joints(self)

        StickMan.build_posture(self)

        speed = .04

        end_move = pi/2-.2

        StickMan.create_movement(self, 4, [0, end_move], 1, speed=speed)

        StickMan.create_movement(self, 5, [0, end_move], 1, speed=speed)

        StickMan.create_movement(self, 2, [-end_move, 0], 1, speed=speed)

        StickMan.create_movement(self, 3, [-end_move, 0], 1, speed=speed)

    def morning_routine(self):

        StickMan.rotation_epaule(self)

        self.global_movements.append([StickMan.rotation_epaule, 300])  # movement added to list of to do movements, when gets finished (in 300 frames), next one gats called)

        self.global_movements.append([StickMan.rond_epaule_profil, 300])

        self.global_movements.append([StickMan.split, 150])

    def rotation_epaule(self):

        self.on_ground_limbs = []

        self.on_ground_limbs.append(10)

        StickMan.set_position(self, 0)

        self.l_elbow_orientation = self.l_shoulder_orientation

        self.r_elbow_orientation = self.r_shoulder_orientation

        StickMan.update_joints(self)

        StickMan.build_posture(self)

        # a movement is created in elbows and shoulders, both are moved cause the arms are straight
        end_move = pi/4

        speed = 0.02

        StickMan.create_movement(self, 2, [-end_move, end_move], 1, speed=speed)

        StickMan.create_movement(self, 3, [-end_move, end_move], 1, speed=speed, sens_inverse=1)

        StickMan.create_movement(self, 4, [-end_move, end_move], 1, speed=speed)

        StickMan.create_movement(self, 5, [-end_move, end_move], 1, speed=speed, sens_inverse=1)

    def rond_epaule_profil(self):

        self.on_ground_limbs = []

        self.on_ground_limbs.append(10)

        self.on_ground_limbs.append(11)

        StickMan.set_position(self, 2)

        self.l_elbow_orientation = self.l_shoulder_orientation

        self.r_elbow_orientation = self.r_shoulder_orientation

        StickMan.update_joints(self)

        StickMan.build_posture(self)

##        # a movement is created in elbows and shoulders, both are moved cause the arms are straight
##        end_move = pi/4
##
##        speed = 0.02
##
##        StickMan.create_movement(self, 2, [-end_move, end_move], 1, speed=speed)
##
##        StickMan.create_movement(self, 3, [-end_move, end_move], 1, speed=speed)
##
##        StickMan.create_movement(self, 4, [-end_move, end_move], 1, speed=speed)
##
##        StickMan.create_movement(self, 5, [-end_move, end_move], 1, speed=speed)
##
##        #StickMan.create_movement(self, 6, [0, end_move], 1, speed=speed)
##
##        #StickMan.create_movement(self, 7, [0, end_move], 1, speed=speed)

    #    def handstand


def main():

    play = True

    clicking = 0

    stick_men = [StickMan(150*x+300, 400, x) for x in range(2)]

    stick_man_index = 0

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

                if event.key == pygame.K_SPACE:

                    stick_man.create_movement(4, [-.8, .8], 1)

                elif event.key == pygame.K_LEFT:

                    stick_man_index = (stick_man_index-1)%len(stick_men)

                elif event.key == pygame.K_RIGHT:

                    stick_man_index = (stick_man_index+1)%len(stick_men)

                else:

                    try:

                        nbr = int(event.unicode)

                        stick_men[stick_man_index].set_position(nbr)

                        stick_men[stick_man_index].build_posture()

                    except ValueError:

                        if event.unicode in stick_men[stick_man_index].exercises.keys():

                            stick_men[stick_man_index].exercises[event.unicode](stick_men[stick_man_index])

        screen.fill(WHITE)

        for man in stick_men:

            man.update(stick_man_index)

        pygame.display.update()

        clock.tick(60)


if __name__ == "__main__":

    main()
