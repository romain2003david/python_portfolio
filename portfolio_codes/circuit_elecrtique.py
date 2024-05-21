from pig_tv import *


class Branche:

    def __init__(self, noeud1, noeud2):

        # summits of graph

        self.noeud1 = noeud1

        self.noeud2 = noeud2

        # electrical variables

        self.composants = []

        self.nb_composant = 0

        self.tension = None  # en Volt

        self.courant = None  # en Ampere

        # drawing variables

        self.color = BLACK

        self.pos1 = self.noeud1.pos

        self.pos2 = self.noeud2.pos

        self.size = Arr.norme_eucli(self.pos2-self.pos1)

        self.vecteur_directeur = get_vect_unitaire_dim2(add_vectors(self.pos1, self.pos2, 1, -1))

        self.indiv_space = self.size

    def add_composant(self, composant):

        self.nb_composant += 1

        self.composants.append(composant)

        self.indiv_space = self.size / self.nb_composant

        # updates pos of each component
        for k in range(self.nb_composant):

            self.composants[k].update_centre(add_vectors(self.pos1, self.vecteur_directeur, 1, (k+0.5)*self.indiv_space))

    def draw(self):

        pygame.draw.line(screen, self.color, self.pos1, self.pos2)

        for k in range(self.nb_composant):

            self.composants[k].draw()

    def mouse_au_voisinage(self, pos, radius=5):

        return collide_segment_to_circle(pos, radius, [self.pos1, self.pos2])

    def select(self):

        self.color = GREEN

    def unselect(self):

        self.color = BLACK
        

class Resistance:

    def __init__(self, resistance, centre=[0, 0], vect_directeur=[1, 0], size=10, propo_height_to_width=0.25):
        """ vect_directeur est unitaire """ 

        self.resistance = resistance  # en ohms

        # drawing variables

        self.vect_directeur = vect_directeur

        self.size = size

        self.propo_height_to_width = propo_height_to_width

        Resistance.update_centre(centre)

    def update_centre(self, n_centre):

        self.centre = n_centre

        Resistance.update_points(self)

    def get_tension(self, courant):

        return self.resistance*courant

    def get_courant(self, tension):

        if self.resistance != 0:

            return tension/self.resistance

        else:

            print("resistance nulle..")

    def update_points(self):

        self.points = []

        horizontal = get_scaled_vector(vect_directeur, size/2)

        left_pt = add_vectors(self.centre, horizontal, 1, -1)

        right_pt = add_vectors(self.centre, horizontal, 1, -1)

        vertical = get_scaled_vector(get_normale_2D(self.vect_directeur), size/2*self.propo_height_to_width)

        self.points.append(add_vectors(left_pt, vertical, 1, -1))

        self.points.append(add_vectors(left_pt, vertical, 1, 1))

        self.points.append(add_vectors(right_pt, vertical, 1, 1))

        self.points.append(add_vectors(right_pt, vertical, 1, -1))

    def draw(self):

        pygame.draw.polygon(screen, BLACK, self.points)




class Noeud:

    def __init__(self, rang, name, pos=Arr([0, 0]), radius=10):

        self.rang = rang  # id of point

        self.name = name

        self.pos = pos

        self.color = BLUE

        self.radius = radius

        self.selected = 0

    def draw(self):

        pygame.draw.circle(screen, self.color, self.pos, self.radius)

    def mouse_au_voisinage(self, pos):

        if get_distance(self.pos, pos) < self.radius:

            return True

    def signal(self):

        if not self.selected == 1:

            self.color = RED

    def unsignal(self):

        if not self.selected == 1:

            self.color = BLUE

    def select(self):

        self.selected = 1

        self.color = GREEN

    def unselect(self):

        self.selected = 0

        self.color = BLUE


class Graph:

    def __init__(self, points, voisins):
        """ Le cicuit electrique est modélisé par un graphe, chaque sommet etant un noeud du circuit ; voisins is a list of lists, each sub list of indx i containing all the neighbors of pt of id i """

        self.points = points  # list of Noeud instances

        self.nb_points = len(self.points)

        # list of all list, each sub_list of index i containing the neighbors of index i, and their branch
        #[[Noeud(), Noeud()], ...]
        self.voisins = [[] for x in range(self.nb_points)]

        for couple in voisins:

            Graph.add_arrete(self, couple[0], couple[1])

    def add_pt(self, pos=Arr([0, 0]), pt_name=None, voisins=[]):
        """ receives voisin, list of Neoud instances """

        rang = self.nb_points

        self.nb_points += 1

        if pt_name == None:

            pt_name = rang

        n_pt = Noeud(rang, pt_name, pos)

        self.points.append(n_pt)

        self.voisins.append([])

        for vois in voisins:

            Graph.add_arrete(self, n_pt, vois)

    def add_branch(self, pt1, pt2):
        """ receives two Neoud instances """

        n_branch = Branche(pt1, pt2)

        self.voisins[pt1.rang].append([pt2, n_branch])

        self.voisins[pt2.rang].append([pt1, n_branch])

            
        
class Board:

    def __init__(self):

        self.graph = Graph([], [])

        #0 -> doing nothing
        #1 -> creating new branch ; already chose one summit
        #2 -> placing items on branch
        #3 -> 
        #4 -> 
        self.action = 0

        self.selected_summit = None

        self.selected_branch = None

        self.voisinage = []

        # visual menu

        self.items = [Resistance]

        self.item_str = ["Resistance", "Bobine", "Condensateur", "Generateur"]

        hauteur = 100

        self.buttons = [Panneau(self.item_str[x], x*200, screen_height-hauteur, hauteur=hauteur) for x in rl(self.item_str)]

    def main_loop(self):

        play = True

        clicking = 0

        while play:

            self.voisinage = []

            mouse_pos = pygame.mouse.get_pos()
            
            ## checking if user wants to select an already existing object
            # checking graph summits
            for pt in self.graph.points:

                if pt.mouse_au_voisinage(mouse_pos):

                    self.voisinage.append(pt)

                    pt.signal()

                else:

                    pt.unsignal()

            # checking graph vertices
            for id_pt in rl(self.graph.voisins):  # looping on each point

                pt = self.graph.points[id_pt]

                voisins = self.graph.voisins[id_pt]

                for voisin in voisins:  # looping on each neighbor, to find each verticy

                    vois, branche = voisin

                    if branche.mouse_au_voisinage(mouse_pos):

                        self.voisinage.append(branche)

            ##
            # dealing with user events
            for event in pygame.event.get():

                if event.type == pygame.QUIT:

                    play = False

                elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):

                    clicking = 1

                    if self.action == 2:

                        objet = Board.update_menu(self, mouse_pos)

                        Board.draw_menu(self)

                        if objet != None:

                            self.selected_branch.add_composant(objet)

                    elif self.voisinage == []:  # nothing around, player wants to create new summit of graph

                        self.graph.add_pt(Arr(mouse_pos))

                        self.action = 0

                        if self.selected_branch != None:

                            self.selected_branch.unselect()

                        self.selected_summit = None

                        self.selected_branch = None

                    elif self.action == 1: # creating a new branch, the second summit might just have been chosen

                        for x in self.voisinage:

                            if isinstance(x, Noeud):

                                if x != self.selected_summit:

                                    self.graph.add_branch(x, self.selected_summit)

                                self.selected_summit.unselect()

                                self.selected_summit = None

                                self.action = 0

                    else:

                        for x in self.voisinage:

                            if isinstance(x, Noeud):  # selecting a point

                                print("point selected")

                                self.selected_summit = x

                                x.select()

                                self.action = 1

                            elif isinstance(x, Branche):

                                print("branch selected")

                                self.selected_branch = x

                                x.select()

                                self.action = 2

                elif (event.type == pygame.MOUSEBUTTONUP) and (event.button == 1):

                    clicking = 0

                elif (event.type == pygame.MOUSEMOTION):

                    translation = event.rel

                elif event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_LEFT:

                        pass

                    if event.key == K_ESCAPE:

                        self.action = 0

            Board.draw(self)

            if self.action == 2:

                Board.draw_menu(self)

            pygame.display.update()

            clock.tick(60)

    def update_menu(self, mouse_pos):

        for x in rl(self.buttons):

            button = self.buttons[x]

            if button.clicked(mouse_pos):

                return self.items[x]  # retourne l'objet dont on veut creer l'instance

    def draw_menu(self):

        for x in rl(self.buttons):

            button = self.buttons[x]

            button.draw()

    def draw(self):

        screen.fill(WHITE)

        # drawing graph summits

        for pt in self.graph.points:

            pt.draw()

        # drawing graph vertices

        for pt in self.graph.voisins:

            for couple in pt:

                couple[1].draw()




if __name__ == "__main__":

    board = Board()

    board.main_loop()










