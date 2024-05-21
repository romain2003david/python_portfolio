from pig_tv import *


def in_borne(y, x, nbr_row, nbr_col):

    if ((x < 0) or (x > nbr_col-1)) or ((y < 0) or (y > nbr_row-1)):

        return False

    return True


class Grille:

    def __init__(self, nbr_col, nbr_row, cell_size):

        self.nbr_col = nbr_col

        self.nbr_row = nbr_row

        self.cell_size = cell_size

        self.tab = []

        self.ancien = 0

        for row in range(nbr_row):

            self.tab.append([])

            for col in range(nbr_col):

                if (col%2) ==(row%2):

                    walls = [True for x in range(4)]

                else:

                    walls = 0

                self.tab[row].append(Cell(cell_size, col*cell_size, row*cell_size,  walls))

        self.current_index = [0, 0]
        self.current = self.tab[0][0]

        self.stack = []

        self.done_color = [0, 0, 0]
        self.color_vector = []

        Grille.pick_ncolor(self, self.done_color)

        self.last_cut_line = 0

    def aff(self):

        for x in self.tab:

            for y in x:

                y.aff()

        pygame.display.update()

    def process(self):

        next_square = Grille.choose_neighbor(self)

        if next_square:

            if type(self.ancien) == list:  # self ancien et la paire de coordonnees
                
                Grille.find_color(self, self.ancien)
                #print(self.color_vector)

            Grille.cut_wall(self, self.current_index, next_square)
            #print(self.color_vector)

            self.stack.append(next_square)
            #print(self.color_vector)

            self.current_index = next_square
            #print(self.color_vector)

            self.current = self.tab[self.current_index[0]][self.current_index[1]]
            #print(self.color_vect)

            self.current.highlight(self.done_color, self.color_vector, self)

            self.ancien = 1

        else:

            try:

                self.current_index = self.stack[-1]

                self.stack.pop()

            except:

                #aff_txt("Fini", 0, 600)
                pygame.display.update()
                
                return 1

            self.current = self.tab[self.current_index[0]][self.current_index[1]]
        

    def choose_neighbor(self):

        index = self.current_index

        neighbors = []

        #visited = 0

        for k, l in [[-1, 0], [1, 0], [0, 1], [0, -1]]:  # abs et ord

            if in_borne(k+index[0], l+index[1], self.nbr_row, self.nbr_col):  # row puis col

                if not self.tab[k+index[0]][l+index[1]].visited:

                    neighbors.append([k+index[0], l+index[1]])

                #else:

                    #visited += 1

        if len(neighbors) > 0:

            return random.choice(neighbors)#, visited

    def cut_wall(self, index_a, index_b):

        cell_a = self.current

        cell_b = self.tab[index_b[0]][index_b[1]]

        cell_b.visited = True

        if cell_a.walls:

            cell = cell_a

        else:

            cell = cell_b

        diff_x = index_a[0] - index_b[0]  # Row en fait y

        diff_y = index_a[1] - index_b[1]

        if diff_x == 0:

            if diff_y > 0:

                index1 = index_a[1]

            else:

                index1 = index_b[1]

            indexs = [[index1*self.cell_size+1, index_a[0]*self.cell_size+1], [index1*self.cell_size-1, index_a[0]*self.cell_size+self.cell_size-1]]

        else:

            if diff_x > 0:

                index1 = index_a[0]

            else:

                index1 = index_b[0]

            indexs = [[index_a[1]*self.cell_size+1, index1*self.cell_size+1], [index_a[1]*self.cell_size+self.cell_size-1, index1*self.cell_size-1]]

        pygame.draw.line(screen, self.done_color, indexs[0], indexs[1], 5)

        self.last_cut_wall = indexs

    def pick_ncolor(self, color):

        #print("cc pick")

        index_color = random.randint(0, 2)

        if color[index_color] == 255:

            vect = -1

        else:

            vect = 1

        self.color_vector = [index_color, vect]

    def find_color(self, last_coor):

        first_coor = [self.current_index[0]*self.cell_size+int(self.cell_size/2), self.current_index[1]*self.cell_size+int(self.cell_size/2)]

        second_coor = [last_coor[0]*self.cell_size+int(self.cell_size/2), last_coor[1]*self.cell_size+int(self.cell_size/2)]

        first_coor.reverse()

        second_coor.reverse()

        first = screen.get_at((first_coor[0], first_coor[1]))[:3]

        second = screen.get_at((second_coor[0], second_coor[1]))[:3]

##        pygame.draw.rect(screen, (255, 255, 100), pygame.Rect(first_coor[0]-3, first_coor[1]-3, 6, 6))
##        pygame.draw.rect(screen, (255, 255, 100), pygame.Rect(second_coor[0]-3, second_coor[1]-3, 6, 6))
##
##        pygame.display.update()

        for x in range(3):

            diff = second[x] - first[x]

            if diff:

                self.color_vector = [x, diff]
                self.done_color = list(first)
                #print("col", self.color_vect, self.done_color, first, second)


class Cell:

    def __init__(self, cell_size, x, y, walls):

        self.size = cell_size

        self.x = x
        self.y = y

        self.rectangle = pygame.Rect(x+1, y+1, self.size-1, self.size-1)
        self.color = [0, 0, 0]

        self.walls = walls
        self.wall_color = (255, 255, 255)

        self.anti_wall_color = (255, 255, 0)

        self.visited = False

        self.wall_width = 2

    def aff(self):

        pygame.draw.rect(screen, self.color, self.rectangle)

        if self.walls:

            if self.walls[0]:  # haut : a droite

                pygame.draw.line(screen, self.wall_color, (self.x, self.y), (self.x+self.size, self.y), self.wall_width)

            else:
                
                pygame.draw.line(screen, self.anti_wall_color, (self.x, self.y), (self.x+self.size, self.y), self.wall_width)

            if self.walls[1]:  # droite : en bas

                pygame.draw.line(screen, self.wall_color, (self.x+self.size, self.y), (self.x+self.size, self.y+self.size), self.wall_width)

            else:
                
                pygame.draw.line(screen, self.anti_wall_color, (self.x+self.size, self.y), (self.x+self.size, self.y+self.size), self.wall_width)

            if self.walls[2]:  # bas : a gauche

                pygame.draw.line(screen, self.wall_color, (self.x+self.size, self.y+self.size), (self.x, self.y+self.size), self.wall_width)                    

            else:
                
                pygame.draw.line(screen, self.anti_wall_color, (self.x+self.size, self.y+self.size), (self.x, self.y+self.size), self.wall_width)


            if self.walls[3]:  # gauche : en haut

                pygame.draw.line(screen, self.wall_color, (self.x, self.y+self.size), (self.x, self.y) ,self.wall_width)

            else:
                
                pygame.draw.line(screen, self.anti_wall_color, (self.x, self.y+self.size), (self.x, self.y))

    def highlight(self, done_color, color_vector, grille):

        #print(done_color, color_vector)
        done_color[color_vector[0]] += color_vector[1]

        if (done_color[color_vector[0]] == 0) or (done_color[color_vector[0]] == 255):

            Grille.pick_ncolor(grille, done_color)

        pygame.draw.rect(screen, done_color, self.rectangle)


def end():

    pass

##    for x in range(2):
##
##        end_coor = [random.randint(0, nbr_col*cell_size), random.randint(0, nbr_row*cell_size)]
##
##        color_end = screen.get_at((end_coor[0], end_coor[1]))[:3]
##
##        anti_color = []
##
##        for x in range(3):
##
##            anti_color.append((color_end[x]-255)*-1)
##
##        print(anti_color)
##        pygame.draw.rect(screen, anti_color, pygame.Rect(end_coor[1]-end_coor[1]%cell_size+2, end_coor[0]-end_coor[0]%cell_size+2, cell_size-2, cell_size-2))
##
##    pygame.display.update()


def main(inputs):

    rows, show_continually = inputs

    cols = rows

    cell_size = screen_height // rows

    grille = Grille(cols, rows, cell_size)

    grille.aff()

    continu = True

    while continu:

##        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(grille.current_index[1]*cell_size, grille.current_index[0]*cell_size, 10, 10))
##        pygame.display.update()

        continu = not(grille.process())

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                continu = False

        if show_continually:

            pygame.display.update()

        #time.sleep(1)

    wait()

if __name__ == "__main__":

    pygame.display.set_caption("Maze")

    nbr_row = 20

    main([nbr_row, 1])

