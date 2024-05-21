from pig_tv import *

from generateur_terrain import terrain3D


class Point3D:

    def __init__(self, coor):

        self.coor = coor

    def nul():

        return Point3D(Arr.get_nul([3]))

    def add_vect(self, vect):

        self.coor += vect

    def plus_vect(self, vect):

        return Point3D(self.coor+vect)

    def __repr__(self):

        return self.coor.__repr__()

    def add_x(self, x):

        self.coor[0] += x

    def add_y(self, y):

        self.coor[1] += y

    def add_z(self, z):

        self.coor[2] += z




class Cube:

    def __init__(self, coor, size):

        self.coor = coor
        self.size = size

        self.faces = []

        x_vect = Arr([size, 0, 0])
        y_vect = Arr([0, size, 0])
        z_vect = Arr([0, 0, size])

        vects = [[x_vect, y_vect], [y_vect, z_vect], [z_vect, x_vect]]

        c = -1

        for start_pt in [self.coor, self.coor.plus_vect(z_vect), self.coor, self.coor.plus_vect(x_vect), self.coor, self.coor.plus_vect(y_vect)]:

            c += 1

            vect1, vect2 = vects[c//2]
            
            pts = [start_pt, start_pt.plus_vect(vect1), start_pt.plus_vect(vect1+vect2), start_pt.plus_vect(vect2)]

            self.faces.append(Objet3D(pts))


def test_cube():

    coor = Point3D(Arr([10, 10, 10]))

    cube = Cube(coor, 20)

    print(cube.faces)



class Objet3D:
    """ polygone dans R3 """

    def __init__(self, pts, face_color=BLACK, edge_color=RED, vertex_color=BLUE):

        self.pts = pts

        self.face_color = get_random_color()  # face_color

        self.edge_color = edge_color

        self.vertex_color = vertex_color

        #

        self.stored_pts = []

        self.pts2D = []

    def store_translated_coors(self, vector):

        self.stored_pts = [pt.plus_vect(vector) for pt in self.pts]

    def project_on_screen(self, project_screen):

        u, v = project_screen

        #print(u, v)#, self.pts2D)

        #print(self.stored_pts)

        #print([Arr([Arr.p_s(pt.coor, u), Arr.p_s(pt.coor, v)]) for pt in self.stored_pts])

        self.pts2D = [Arr([Arr.p_s(pt.coor, u), Arr.p_s(pt.coor, v)]) for pt in self.stored_pts]

    def translate2D(self, vect):

        self.pts2D = [pt+vect for pt in self.pts2D]

    def draw(self):

        pygame.draw.polygon(screen, self.face_color, self.pts2D)

        for i in range(len(self.pts2D)):

            pygame.draw.line(screen, self.edge_color, self.pts2D[i], self.pts2D[i%(len(self.pts2D)-1)])

        for vertex in self.pts2D:

            pygame.draw.circle(screen, self.vertex_color, vertex.with_fun_applied(int), 3)

        #pygame.display.update()

        #wait()

    def __repr__(self):

        return str([pt.__repr__() for pt in self.pts])


class Space3D:

    def __init__(self, basic_objects, complex_objects):

        self.basic_objects = basic_objects

        self.complex_objects = complex_objects

    def add_cmplx_obj(self, complex_object):

        self.complex_objects.append(complex_object)

    def draw(self, camera_pos, project_screen):

        for c_obj in self.complex_objects:

            for face in c_obj.faces:

                face.store_translated_coors(-camera_pos.coor)

                face.project_on_screen(project_screen)

                face.translate2D(Arr(screen_center))

                face.draw()


                


class Camera:

    def __init__(self, space):

        self.pos = Point3D.nul()

        self.orientation = Arr([1, 0, 0])

        self.space = space

        self.project_screen = None

        self.move_ori_speed = 0.01

        # directions to walk

        self.update_directions_vects()

    def update_directions_vects(self):

        self.forward_vect = Arr([Arr.p_s(self.orientation, Arr([1, 0, 0])), Arr.p_s(self.orientation, Arr([0, 1, 0]))])

        self.forward_vect.normalize()

        self.left_vect = Arr.get_mat_rot2D(pi/2)*self.forward_vect  # still normalized

        self.forward_vect.append(0)

        self.left_vect.append(0)

    def update_ori(self, translation):

        u, v = self.orientation.normal_vects3D()  # gives us two normalized vectors, on which we'll project the objects
        #print("av", self.orientation)

        add_vector = self.move_ori_speed*(u*translation[0]+v*translation[1])

        #print(add_vector, translation)
        self.orientation += add_vector

        self.orientation.normalize()
        #print("ap", self.orientation)
        #print("uv", u, v, "uv")

        #self.orientation.apply_fun(lambda x:round(x, 3))

        # directions to walk

        self.update_directions_vects()

    def view(self):

        project_screen = self.orientation.normal_vects3D()  # gives us normalized two vectors, on which we'll project the objects

        self.space.draw(self.pos, project_screen)

    def add_x(self, x):

        self.pos.add_x(x)

    def add_y(self, y):

        self.pos.add_y(y)

    def add_z(self, z):

        self.pos.add_z(z)

    def up(self, translat):

        self.add_z(translat)

    def forward(self, translat):

        self.pos.add_vect(self.forward_vect*translat)

    def backward(self, translat):

        self.pos.add_vect(-self.forward_vect*translat)

    def right(self, translat):

        print(self.left_vect)

        self.pos.add_vect(-self.left_vect*translat)

    def left(self, translat):

        self.pos.add_vect(self.left_vect*translat)
        


def main():

    terrain_square_nb_width=1
    terrain_square_nb_height=1

    alti = terrain3D(terrain_square_nb_width, terrain_square_nb_height)

    cube_size = 50

    space = Space3D([], [])

    for i in range(terrain_square_nb_height):

        for j in range(terrain_square_nb_width):

            coor = Point3D(Arr([10+j*cube_size, 10+i*cube_size, 10+alti[i][j]*100]))

            #print(coor)

            obj = Cube(coor, cube_size)

            space.add_cmplx_obj(obj)


    cam = Camera(space)

    clicking = 0

    pressed = Arr.get_nul([5])

    play = True

    while play:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                play = False

            elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):

                clicking = 1

            elif (event.type == pygame.MOUSEBUTTONUP) and (event.button == 1):

                clicking = 0

            elif (event.type == pygame.MOUSEMOTION):

                mode_ori = 2

                if mode_ori == 2:

                    translation = pygame.mouse.get_rel()

                    cam.update_ori(translation)

                else:

                    translation = pygame.mouse.get_pos()

                    cam.update_ori(translation)

                    pygame.mouse.set_pos(screen_center)


            elif event.type == pygame.KEYDOWN:

                translat = 5

                if event.key == pygame.K_LEFT:

                    pressed[0] = 1

                if event.key == pygame.K_RIGHT:

                    pressed[1] = 1

                if event.key == pygame.K_UP:

                    pressed[2] = 1

                if event.key == pygame.K_DOWN:

                    pressed[3] = 1

                if event.key == pygame.K_LSHIFT:

                    pressed[4] = 1

                if event.key == pygame.K_a:

                    cam.update_ori([10, 10])

            elif event.type == pygame.KEYUP:

                pressed = Arr.get_nul([5])

        if pressed.norme_eucli() != 0:

            if pressed[2] == 1:

                cam.forward(translat)

            if pressed[3] == 1:

                cam.backward(translat)

            if pressed[0] == 1:

                cam.left(translat)

            if pressed[1] == 1:

                cam.right(translat)

            if pressed[4] == 1:

                cam.up(translat)

        screen.fill(WHITE)

        cam.view()

        pygame.display.update()

        #print(cam.orientation)

        clock.tick(60)



if __name__ == "__main__":

    main()











