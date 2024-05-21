from pig_tv import *

from maze3 import main as maze_walls


class Terrain:

    def __init__(self, ray_nbr, taille3Drender, maze_size):

        #self.start_pos = [screen_width//2, screen_height//2]
        
        self.maze_size = maze_size

        self.all_lines = maze_walls([maze_size, maze_size, 0])

        self.lines = self.all_lines[0]

        start_end = self.all_lines[1]

        for v in range(2):

            rect = start_end[v]

            if v == 0:
                col = BLUE
                self.start_pos = get_rect_center(rect)

            else:
                col = GREEN

            x_side = rect[2]

            y_side = rect[3]

            n_rect = [rect[0]+x_side//4, rect[1]+y_side//4, x_side//2, y_side//2]

            for x in get_lines_of_rect(n_rect):

                self.lines.append([col, x])

            for indx in range(len(self.lines)):

                seg2 = self.lines[indx]

                if len(seg2[0]) == 3:

                    seg2 = seg2[1]

                    self.lines[indx] = [self.lines[indx][0], [[round(seg2[0][0], 2), round(seg2[0][1], 2)], [round(seg2[1][0], 2), round(seg2[1][1], 2)]]]

                else:

                    self.lines[indx] = [[round(seg2[0][0], 2), round(seg2[0][1], 2)], [round(seg2[1][0], 2), round(seg2[1][1], 2)]]
##        for x in range(4):
##
##            self.lines.append([GREEN, shrink_line(start_end[1][x])])

##        self.lines =  [
##            [[0, 0], [screen_width, 0]],
##            [[0, screen_height], [screen_width, screen_height]],
##            [[0, 0], [0, screen_height]],
##            [[screen_width, 0], [screen_width, screen_height]],
##
##            ]#, [[100, 0], [100, screen_height]]]#[[[500, 0], [500, screen_height]], [[100, 0], [100, screen_height]]]  # [get_random_point_in_screen(), get_random_point_in_screen()] for x in range(4)]

        rects = []#[0, 0, 100, 100]]

        for x in rects:

            self.lines += get_lines_of_rect(x)

        side = 100

        self.max_distance = sqrt(screen_width**2+screen_height**2)

        self.ray_number = ray_nbr  # screen_width//20

        self.taille3Drender = taille3Drender  # portion of screen dedicated to 3D rendering (1 means all, a 2 half, a 3 third..)

        #self.rects = [[(x%(screen_width//side)*side), (x//8)*side, side, side] for x in range((screen_width//side)**2)]

##        self.storage = [[[(x%(screen_width//side)*side), (x//(screen_height//side))*side, side, side], []] for x in range((screen_width//side)*(screen_height//side))]  # storage stores all rects index 0 and then all lines (index 1)
##
##        self.rects = [x[0] for x in self.storage]
##
##        Terrain.sub_divide(self)

    def sub_divide(self):

        for line in self.lines:

            for index in range(len(self.storage)):

                if segment_in_rect(line, self.storage[index][0]):

                    #print(self.storage[index][0])

                    self.storage[index][1].append(line)

    def update(self, joueur):

        # draws the floor and the ceiling

        x_start_3D = screen_width-screen_width*(1/self.taille3Drender)

        pygame.draw.rect(screen, BROWN, pygame.Rect(x_start_3D, screen_height//2, screen_width*(1/self.taille3Drender), screen_height//2))  # floor

        pygame.draw.rect(screen, DARK_BLUE, pygame.Rect(x_start_3D, 0, screen_width, screen_height//2))  # ceiling

        ##

        ray_nbr = self.ray_number

        ray_width = screen_width//(self.taille3Drender*ray_nbr)

        angle_step = joueur.view_angle/ray_nbr

        pos = [joueur.x, joueur.y]

        #pos_s = []

        for current_step in range(ray_nbr):

            chosen_color = GREY  # should be useless while there always is a wall in every direction

            vect = get_vect_from_angle(joueur.angle - joueur.view_angle/2 + angle_step*current_step)

            line = get_droite_from_pt(pos, [joueur.x+vect[0], joueur.y+vect[1]])

            seg1 = Terrain.get_ray_segment(vect, pos, line)

            seg1 = [[round(seg1[0][0], 2), round(seg1[0][1], 2)], [round(seg1[1][0], 2), round(seg1[1][1], 2)]]

            for seg2 in self.lines:

                # the segment has a special color (ex: target is green
                if len(seg2[0]) == 3:

                    color = seg2[0]

                    seg2 = seg2[1]

                # normal color
                else:

                    color = BLACK

                pt = collide_segment_to_segment(seg1, seg2)  # apply_function_to_array(seg1, int), apply_function_to_array(seg2, int))

##                if pt:
##
##                    pygame.draw.circle(screen, GREEN, [int(pt[0]), int(pt[1])], 10)

                if pt and Terrain.closer_to_pt1_of_seg(seg1, pt):  # get_distance(seg1[0], seg1[1])>get_distance(seg1[0], pt):  # 

                    seg1[1] = pt

                    chosen_color = color

            # upper view (2D)

            if self.taille3Drender != 1:

                pygame.draw.line(screen, RED, [seg1[0][0]//2, seg1[0][1]//2], [seg1[1][0]//2, seg1[1][1]//2])

            # 3D view
            ratio = get_distance(seg1[0], seg1[1])/(self.max_distance)  # ((seg1[0][0]-seg1[1][0])**2+(seg1[0][1]-seg1[1][1])**2)/(self.max_distance)**2

            if ratio > 1:

                ratio = 1

            if chosen_color == BLACK:

                chosen_color = [(ratio-1)*-255 for x in range(3)]

            takeoff_size = 400*ratio

            x_3D_pos = current_step*ray_width+x_start_3D

            #pos_s.append([x_3D_pos, screen_height-takeoff_size])

            pygame.draw.line(screen, chosen_color, [x_3D_pos, takeoff_size], [x_3D_pos, screen_height-takeoff_size], ray_width)

        #pygame.draw.polygon(screen, RED, [[screen_width-screen_width*(1/self.taille3Drender), screen_height]]+pos_s+[[screen_width, screen_height]])

    def get_ray_segment(vect, start_pos, line):

        if vect[0] == 0:

            if vect[1] > 0:

                return [start_pos, [start_pos[0], screen_height]]

            elif vect[1] < 0:

                return [start_pos, [start_pos[0], 0]]

        elif vect[0] > 0:

            return [start_pos, [screen_width, screen_width*line[0]+line[1]]]

        else:

            return [start_pos, [0, line[1]]]

    def closer_to_pt1_of_seg(seg, n_pt):

        tried_point = seg[1]

        seg_x_variation = seg[0][0] - tried_point[0]

        seg_y_variation = seg[0][1] - tried_point[1]

        if not seg_y_variation:

            return (((seg_x_variation < 0) and (n_pt[0] < tried_point[0])) or ((seg_x_variation > 0) and (n_pt[0] > tried_point[0])))
            
        elif not seg_x_variation:

            return  (((seg_y_variation < 0) and (n_pt[1] < tried_point[1])) or ((seg_y_variation > 0) and (n_pt[1] > tried_point[1])))

        return (((seg_x_variation < 0) and (n_pt[0] < tried_point[0])) or
                ((seg_x_variation > 0) and (n_pt[0] > tried_point[0]))
                and
                (((seg_y_variation < 0) and (n_pt[1] < tried_point[1])) or
                 ((seg_y_variation > 0) and (n_pt[1] > tried_point[1]))))


    def draw(self):

        for line in self.lines:

            if len(line[0]) == 3:

                color = line[0]

                line = line[1]

            else:

                color = BLACK

            pygame.draw.line(screen, color, [line[0][0]//2, line[0][1]//2], [line[1][0]//2, line[1][1]//2])

    def append_rect(self, rect):

        self.lines += get_lines_of_rect(rect)

##        for rect in self.storage:
##
##            pygame.draw.rect(screen, get_random_color(), get_pygame_rect(rect[0]))


class Joueur:

    def __init__(self, start_pos, view_angle):

        self.x = start_pos[0]

        self.y = start_pos[1]

        self.angle = 0

        self.vect = [1, 0]

        self.color = RED

        self.view_angle = view_angle

        self.vitesse = 4

    def update_vect_from_angle(self):

        self.vect = get_vect_from_angle(self.angle, rounding=0)

    def update(self, turning_right, turning_left, goin_forwad, goin_backwads, graphic, terrain):

        if turning_right:

            Joueur.rotate_vect(self, 1)

        elif turning_left:

            Joueur.rotate_vect(self, -1)

        if goin_forwad:

            Joueur.apply_vector(self, self.vitesse)

            wall = Joueur.colliding_wall(self, terrain.lines)

            if wall == 1:

                Joueur.apply_vector(self, -self.vitesse)

            elif wall == 2:  # reached the target

                return 1  # win

        elif goin_backwads:

            Joueur.apply_vector(self, -self.vitesse)

            wall = Joueur.colliding_wall(self, terrain.lines)

            if wall == 1:

                Joueur.apply_vector(self, self.vitesse)  # collides with a wall, goes back

            elif wall == 2:  # reached the target

                return 1  # win

        if turning_right or turning_left or goin_forwad or goin_backwads:

            screen.fill(WHITE, rect=pygame.Rect(0, 0, screen_width//2, screen_height))

            screen.fill(BLACK, rect=pygame.Rect(screen_width//2, 0, screen_width//2, screen_height))

            terrain.draw()

            terrain.update(self)

            if graphic:

                Joueur.draw(self)

            pygame.display.update()

    def colliding_wall(self, walls):

        wall_thickness = 3  # adding a thickness to the wall so that player can't pass through it, to x and y, so don't have to check if horizontal or vertical wall

        for wall in walls:

            if len(wall[0]) == 3:

                if wall[0] == GREEN:  # is the target

                    wall = wall[1]

                    if collide_point_to_rect([self.x, self.y], [wall[0][0]-wall_thickness, wall[0][1]-wall_thickness, wall[1][0]-wall[0][0]+wall_thickness*2, wall[1][1]-wall[0][1]+wall_thickness*2]):

                        return 2

            else:

                if collide_point_to_rect([self.x, self.y], [wall[0][0]-wall_thickness, wall[0][1]-wall_thickness, wall[1][0]-wall[0][0]+wall_thickness*2, wall[1][1]-wall[0][1]+wall_thickness*2]):

                    return 1

    def get_pos(self):

        return (int(self.x), int(self.y))

    def draw(self):

        self_pos = Joueur.get_pos(self)

        pygame.draw.circle(screen, self.color, [self_pos[0]//2, self_pos[1]//2] , 10)

##        left_line = get_vect_from_angle((-self.view_angle/2)+self.angle)
##
##        right_line = get_vect_from_angle((self.view_angle/2)+self.angle)
##
##        taille = 20
##
##        pygame.draw.line(screen, GREEN, self_pos, [self_pos[0]+self.vect[0]*taille, self_pos[1]+self.vect[1]*taille])
##
##        pygame.draw.line(screen, RED, self_pos, [self_pos[0]+left_line[0]*taille, self_pos[1]+left_line[1]*taille])
##
##        pygame.draw.line(screen, RED, self_pos, [self_pos[0]+right_line[0]*taille, self_pos[1]+right_line[1]*taille])

    def apply_vector(self, facteur=1):

        self.x += self.vect[0] * facteur

        self.y += self.vect[1] * facteur

    def rotate_vect(self, angle):

        self.angle = (self.angle+angle*0.1) % (2*pi)

        Joueur.update_vect_from_angle(self)



def main(inputs):

    ray_nbr, taille3Drender, view_angle, maze_size = inputs

    terrain = Terrain(ray_nbr, taille3Drender, maze_size)

    joueur = Joueur(terrain.start_pos, view_angle)

    turning_left = 0

    turning_right = 0

    goin_forwad = 0

    goin_backwads = 0

    play = True

    graphic = (taille3Drender != 1)

    start_time = time.time()

    while play:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                play = False

            elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):

                mouse_pos = pygame.mouse.get_pos()

                #terrain.append_rect([mouse_pos[0], mouse_pos[1], 100, 100])

            elif (event.type == KEYDOWN):

                if event.key == pygame.K_UP:

                    goin_forwad = 1

                if event.key == pygame.K_DOWN:

                    goin_backwads = 1

                if event.key == pygame.K_LEFT:

                    turning_left = 1

                if event.key == pygame.K_RIGHT:

                    turning_right = 1

            elif (event.type == KEYUP):

                if event.key == pygame.K_UP:

                    goin_forwad = 0

                if event.key == pygame.K_DOWN:

                    goin_backwads = 0

                if event.key == pygame.K_LEFT:

                    turning_left = 0

                if event.key == pygame.K_RIGHT:

                    turning_right = 0

        if play:

            play = not(joueur.update(turning_right, turning_left, goin_forwad, goin_backwads, graphic, terrain))

        clock.tick(60)

        print_fps = 0

        if print_fps and random.randint(0, 20) == 0:

            print(clock.get_fps())

    end_game(str(int(time.time()-start_time))+" sec")


if __name__ == "__main__":

    ray_nbr = 50

    view_angle = (3*pi)/5

    taille3Drender = 2
    
    maze_size = 10

    inputs = [ray_nbr, taille3Drender, view_angle, maze_size]

    main(inputs)
