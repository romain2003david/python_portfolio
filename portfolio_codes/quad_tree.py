"""

Quad Tree algorithm with visual

Romain David 10/04/2019

"""

from pig_tv import *


class Spectre:

    def __init__(self, x, y, radius):

        self.x = x

        self.y = y

        self.radius = radius


class SpeMovingDot:

    def __init__(self, x, y, radius=1):

        self.x = x

        self.y = y

        self.radius = radius

        self.vector = [0, 0]

        self.color = BLUE

        self.compteur = 0

    def update(self, vector=[0, 0]):

        self.compteur += 1

        self.color = BLUE

        #if random.randint(0, 100) == 0:

        if vector == [0, 0]:

            if self.compteur % 40 == 0:

                if get_distance([self.x, self.y], [screen_width//2, screen_height//2]) > 400:

                    self.vector = get_vector_to_point([self.x, self.y], [screen_width//2, screen_height//2], 1)

                else:

                    self.vector = get_random_vector()

        else:

            self.vector = vector

        self.x += self.vector[0]

        self.y += self.vector[1]

    def draw(self):#, color=(0, 0, 0)):

        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)


class QuadTree:

    def __init__(self, rect, max_recursion=5, recursion=0, max_bille_square=3):

        self.rect = rect

        self.elements = []

        self.sub_divided = 0

        self.recursion = recursion

        self.max_recursion = max_recursion

        self.pyg_rect = pygame.Rect(rect[0], rect[1], rect[2], rect[3])

        self.max_bille_square = max_bille_square

    def print_content(self):

        if self.sub_divided:

            print(self.recursion, ">")

            for x in self.elements:

                x.print_content()

        else:

            print(self.recursion, self.rect)

            for x in self.elements:

                print(x)  # self.elements.index(x), ")", x.x, x.y)

    def get_len_tree(self):

        if self.sub_divided:

            total_len = 0

            for x in self.elements:

                total_len += x.get_len_tree()

            return total_len

        else:

            return len(self.elements)

    def append_element(self, element, spectre=0):

        if self.sub_divided:

            QuadTree.child_append_element(self, element, spectre)

        elif len(self.elements) > self.max_bille_square-1:

            if self.recursion < self.max_recursion:

                QuadTree.sub_divide(self)

                QuadTree.child_append_element(self, element, spectre)

            else:

                QuadTree.real_append(self, element, spectre)

        else:

            QuadTree.real_append(self, element, spectre)

    def real_append(self, element, spectre):

        if spectre:

            if not (spectre in self.elements):

                self.elements.append(spectre)

        else:

            if not (element in self.elements):

                self.elements.append(element)

    def get_element_in_child_location(self, element):

        if self.rect[0] <= element.x <= (self.rect[0]+self.rect[2]/2):

            if self.rect[1] <= element.y <= self.rect[1]+self.rect[3]/2:

                return 0

            elif self.rect[1]+self.rect[3]/2 <= element.y <= self.rect[1]+self.rect[3]:

                return 2

        elif (self.rect[0]+self.rect[2]/2) <= element.x <= self.rect[0]+self.rect[2]:

            if self.rect[1] <= element.y <= self.rect[1]+self.rect[3]/2:

                return 1

            elif self.rect[1]+self.rect[3]/2 <= element.y <= self.rect[1]+self.rect[3]:

                return 3

        return 4  # means it's out of parent quadtree, thus should be deleted (or else..)

    def child_append_element(self, element, spectre=0):

        child_index = QuadTree.get_element_in_child_location(self, element)

        if not child_index == 4:  # not in this tree

            self.elements[child_index].append_element(element, spectre)

    def child_remove_element(self, element):

        child_index = QuadTree.get_element_in_child_location(self, element)

        # ? if not child_index == 4:

        self.elements[child_index].remove_element(element)

    def sub_divide(self):

        self.sub_divided = 1

        old_elements = self.elements.copy()

        rects = [Rect(self.rect[0], self.rect[1], self.rect[2]/2, self.rect[3]/2),
                 Rect(self.rect[0]+self.rect[2]/2, self.rect[1], self.rect[2]/2, self.rect[3]/2),
                 Rect(self.rect[0], self.rect[1]+self.rect[3]/2, self.rect[2]/2, self.rect[3]/2),
                 Rect(self.rect[0]+self.rect[2]/2, self.rect[1]+self.rect[3]/2, self.rect[2]/2, self.rect[3]/2)]

        self.elements = [QuadTree(rects[0], self.max_recursion, self.recursion+1),
                         QuadTree(rects[1], self.max_recursion, self.recursion+1),
                         QuadTree(rects[2], self.max_recursion, self.recursion+1),
                         QuadTree(rects[3], self.max_recursion, self.recursion+1)]

        for ent in old_elements:

            QuadTree.child_append_element(self, ent)

    def unite(self):

        all_elements = QuadTree.get_elements(self)  # self.elements[0].get_elements()+self.elements[1].get_elements()+self.elements[2].get_elements()+self.elements[3].get_elements()

        self.elements = []

        for x in all_elements:

            if not x in self.elements:

                self.elements.append(x)

        self.sub_divided = 0

    def get_elements(self):
        """ returns elements (not quadtree) of a quadtree, useful during a unification when several layers of the tree get united at once """

        if self.sub_divided:

            return self.elements[0].get_elements() + self.elements[1].get_elements() + self.elements[2].get_elements() + self.elements[3].get_elements()

        return self.elements

    def remove_element(self, element):

        if self.sub_divided:

            QuadTree.child_remove_element(self, element)

            if QuadTree.get_len_children(self) < self.max_bille_square:

                QuadTree.unite(self)

        else:

            self.elements.remove(element)

    def get_len_children(self, entites=1):

        sum_children = 0

        if self.sub_divided:

            for x in range(4):

                sum_children += self.elements[x].get_len_children()

        else:

            sum_children += len(self.elements)

        return sum_children

    def update(self):

        if self.sub_divided:

            if QuadTree.get_len_children(self) < self.max_bille_square:

                QuadTree.unite(self)

        if self.sub_divided:  # every father tree gathers the to_add entities to pass to its own parents

            to_update_points = []

            for x in self.elements:

                possible_points = x.update()

                if possible_points:

                    to_update_points += possible_points

            if self.recursion == 0:  # first father tree

                #print("len tree", QuadTree.get_len_tree(self))

                for x in to_update_points:

                    if type(x) == list:  # adds a "spectre" : means that it will add a dot that is not really in the square, just collinding it.

                        QuadTree.append_element(self, x[0], x[1])

                    else:

                        QuadTree.append_element(self, x)

                QuadTree.deal_with_collisions(self)

            else:

                return to_update_points

        else:

            to_update_points = []

            for index in range(len(self.elements)-1, -1, -1):

                dot = self.elements[index]

                collide_ext_lines = circle_out_rect(dot, self.rect)

                #print(dot, collide_ext_lines)

                if 1 in collide_ext_lines:

                    to_update_points.append([Dot(self.rect[0]+self.rect[2]//2-self.rect[2], self.rect[1]+self.rect[3]//2), dot])  # to_update_points.append([Dot(dot.x-dot.radius, dot.y, radius), dot])#Spectre(dot.x, dot.y, dot.radius)])  # ? might create an error if border line and if perfectly just touching the other rectangle might add an infinity of rects in this square ...

                elif 2 in collide_ext_lines:

                    to_update_points.append([Dot(self.rect[0]+self.rect[2]//2+self.rect[2], self.rect[1]+self.rect[3]//2), dot])  # to_update_points.append([Dot(dot.x+dot.radius, dot.y, radius), dot])  # also have to be careful when adding radius to be sure that's it's on the other side that itt's not too be big and already in another square (but in that case probably wouldn't work anyway)

                if 3 in collide_ext_lines:

                    to_update_points.append([Dot(self.rect[0]+self.rect[2]//2, self.rect[1]+self.rect[3]//2-self.rect[3]), dot])  # to_update_points.append([Dot(dot.x, dot.y-dot.radius, radius), dot])#Spectre(dot.x, dot.y, dot.radius)])

                elif 4 in collide_ext_lines:

                    to_update_points.append([Dot(self.rect[0]+self.rect[2]//2, self.rect[1]+self.rect[3]//2+self.rect[3]), dot])  # to_update_points.append([Dot(dot.x, dot.y+dot.radius, radius), dot])#Spectre(dot.x, dot.y, dot.radius)])

                if not self.pyg_rect.collidepoint([dot.x, dot.y]):  # collide_circle_to_rect([dot.x, dot.y], 1, self.rect):

                    to_update_points.append(dot)
##
##                    try:
##
##                        print(to_update_points[-1] == dot)
##
##                    except:
##
##                        print(dot.x, dot.y, self.rect, dot.vector)

                    self.elements.remove(dot)  # QuadTree.remove_element(self, dot)

            return to_update_points

    def deal_with_collisions(self):

        if self.sub_divided:

            for x in self.elements:

                x.deal_with_collisions()

        else:

            for index1 in range(len(self.elements)-1, 0, -1):

                for index2 in range(index1-1, -1, -1):

                    element1 = self.elements[index1]

                    element2 = self.elements[index2]

                    if collide_circle_to_circle((element1.x, element1.y), element1.radius, (element2.x, element2.y), element2.radius):

                        self.elements[index1].color = RED

                        self.elements[index2].color = RED

    def draw(self):

        if self.sub_divided:

            for tree in self.elements:

                tree.draw()
        else:

            pygame.draw.rect(screen, BLACK, self.pyg_rect, 5)


def test():

    tree = QuadTree(Rect(0, 0, screen_width, screen_height), quad_tree_size)

    points = [SpeMovingDot(random.randint(0, screen_width), random.randint(0, screen_width), radius) for x in range(40)]

    for x in points:

        tree.append_element(x)

    play = True

    #sizes = []

    while play:

        #sizes.append(tree.get_len_tree())

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                play = False

            elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):

                x, y = pygame.mouse.get_pos()

                points.append(MovingDot(x, y, radius))

                tree.append_element(points[-1])

            elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 3):

                print("tree content :")

                print(tree.get_len_tree())

                print("stop tree content")

                #graph_array(sizes)

                print(sizes)

        screen.fill(WHITE)



        for pt in points:

            pt.update(get_vector_to_point([pt.x, pt.y], pygame.mouse.get_pos(), 1))

        tree.update()

        tree.draw()

        for pt in points:

            pt.draw()

        pygame.display.update()

        clock.tick(60)


if __name__ == "__main__":

    radius = 10

    quad_tree_size = 5

    test()
