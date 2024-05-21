from pig_tv import *

from neural_network2 import Network, Matrix


class IA2:

    def __init__(self, grid, skin):

        self.skin = skin

        self.grid = grid

        layer_nb, layer_size = 2, 2

        self.net = Network(grid.grid_size_width*grid.grid_size_height+2, layer_nb, layer_size, 3)  # outputs should be left, right or do nothing

    def decision(self):

        res = self.net.feed_forward(self.grid.get_matrix(self.skin.vecteur))

        #print(res.max_index(), res.content, self)

        if res.max_index() == 1:

            self.skin.turn_left()

        elif res.max_index() == 2:

            self.skin.turn_right()

        #print( self.net.feed_forward(self.grid.get_matrix()) )

        


class Grid:

    def __init__(self, size_width):

        self.grid_size_width = size_width

        self.square_size = screen_width // self.grid_size_width

        self.grid_size_height = screen_height // self.square_size

        self.grid = [[0 for i in range(self.grid_size_width)] for j in range(self.grid_size_height)]

        self.dic_id_index = {}

        self.players = []

        a = Player(self, 1)  # bin variable

    def screen_pos_into_grid(self, pos):

        x, y = pos

        grid_pos = x // self.square_size, y // self.square_size

        return grid_pos

    def get_matrix(self, vecteur):

        return Matrix(1, self.grid_size_height*self.grid_size_width+2, [get_flattened_list(self.grid)+list(vecteur)])

    def initialise_player(self, player):

        screen_pos, id_ = player.get_center_pos(), player.id

        self.players.append(player)

        player.index = len(self.players)-1

        Grid.assign_to_player(self, screen_pos, id_)

        self.dic_id_index[id_] = player.index

    def assign_to_player(self, screen_pos, id_):

        x_index, y_index = Grid.screen_pos_into_grid(self, screen_pos)

        self.grid[y_index][x_index] = id_

    def update_tile(self, grid_pos, id_):

        x_index, y_index = grid_pos

        old_tile = self.grid[y_index][x_index]

        idx = self.dic_id_index[id_]

        if old_tile == id_:  # home

            if self.players[idx].invading == 1:  # back home : claiming territory

                Grid.fill_player(self, id_)

                self.players[idx].invading = 0

        elif old_tile == 0:  # invading blank territory

            self.grid[y_index][x_index] = -id_

            self.players[idx].invading = 1

        elif old_tile == -id_:  # stumbled on his own path

            Grid.kill_player(self, self.dic_id_index[id_])

        elif type(old_tile) == list:

            if old_tile[0] == -id_:  # stumbled on his own path

                Grid.kill_player(self, self.dic_id_index[id_])

            elif old_tile[1] == id_:  # back home and also killed some adventurer

                if self.players[idx].invading == 1:  # claiming territory

                    Grid.fill_player(self, id_)

                    self.players[idx].invading = 0

                Grid.kill_player(self, self.dic_id_index[-old_tile[0]])  # killing the adventurer

            else:  # invading ennemy space while killing other ennemy

                Grid.kill_player(self, self.dic_id_index[-old_tile[0]])  # killing precedent adventurer

                self.grid[y_index][x_index] = [-id_, old_tile[1]]  # in case invader dies, invaded players claims his territory back

        elif old_tile < 0:  # killed an other player

            idx_killed = self.dic_id_index[-old_tile]

            Grid.kill_player(self, idx_killed)

            self.grid[y_index][x_index] = -id_

            self.players[idx].invading = 1

        elif old_tile > 0:  # invading an other's territory

            self.players[idx].invading = 1

            self.grid[y_index][x_index] = [-id_, self.grid[y_index][x_index]]  # in case invader dies, invaded players claims his territory back

    def fill_player(self, id_):

        first_try_indx = list(reversed(get_list_indexs_deep(self.grid, 0)[0]))  # finds an arbitrary blank tile coordinate

        Grid.try_fill_area(self, first_try_indx, id_)

    def try_fill_area(self, try_indx, id_):

        pile_coor = [try_indx]

        visited = []

        good_try = True

        try_grid = complete_copy_list(self.grid)

        while pile_coor != []:

            new = pile_coor.pop()

            if not new in visited:

                visited.append(new)

                try_grid[new[1]][new[0]] = "a"

                neighbors = [[new[0]+1, new[1]], [new[0]-1, new[1]], [new[0], new[1]+1], [new[0], new[1]-1]]

                for coor in neighbors:

                    x, y = coor

                    if Grid.out_bound(self, coor):

                        good_try = False

                    else:

                        val = try_grid[y][x]

                        if val == 0:

                            pile_coor.append(coor)

                        elif not (val in [id_, -id_] or val == "a" or (type(val) == list and (val[0] == -id_ or val[1] == id_))):

                            #good_try = False

                            #if annexion:

                            pile_coor.append(coor)

        if good_try == True:

            #if annexion == 0:

            self.grid = try_grid.copy()

            replace_liste(self.grid, "a", id_)

            for y in rl(self.grid):

                lgn = self.grid[y]

                for x in rl(lgn):

                    elemnt = lgn[x]

                    if type(elemnt) == list:

                        if elemnt[0] == -id_:  # player has conquered ennemy territory

                            self.grid[y][x] = elemnt[0]

            replace_liste(self.grid, -id_, id_)

        else:

            left_zeros = get_list_indexs_deep(try_grid, 0)

            if left_zeros != []:

                other_area_index = list(reversed(left_zeros[0]))

                Grid.try_fill_area(self, other_area_index, id_)

            else:

                found = False

                other_player_ids = [player.id for player in self.players if not player == None]

                other_player_ids.remove(id_)

                for other_id in other_player_ids:

                    non_invaded_tiles = get_list_indexs_deep(try_grid, other_id, max_depth=1)

                    if non_invaded_tiles != []:

                        found = True

                        other_area_index = list(reversed(non_invaded_tiles[0]))

                        Grid.try_fill_area(self, other_area_index, id_)

                if not found:

                    for y in rl(self.grid):

                        lgn = self.grid[y]

                        for x in rl(lgn):

                            elemnt = lgn[x]

                            if type(elemnt) == list:

                                if elemnt[0] == -id_:  # player has conquered ennemy territory

                                    self.grid[y][x] = elemnt[0]

                    replace_liste(self.grid, -id_, id_)

    def out_bound(self, coor):

        x, y = coor

        if x < 0 or y < 0 or x >= self.grid_size_width or y >= self.grid_size_height:

            return True

    def update(self):

        for indx in range(len(self.players)-1, -1, -1):

            player = self.players[indx]

            if player != None:

                event = player.update()

                if event == "dead":

                    Grid.kill_player(self, indx)

    def kill_player(self, indx):

        print("player {} died".format(self.players[indx].id))

        player = self.players[indx]

        id_ = player.id

        self.players[indx] = None

        # takes out his tiles from the grid

        for y in rl(self.grid):

            lgn = self.grid[y]

            for x in rl(lgn):

                elemnt = lgn[x]

                if type(elemnt) == list:

                    if elemnt[0] == -id_:  # killed player had invaded some territory

                        self.grid[y][x] = elemnt[1]

                    elif elemnt[1] == id_:  # killed player had been invaded

                        self.grid[y][x] = elemnt[0]

        replace_liste(self.grid, -id_, 0)

        replace_liste(self.grid, id_, 0)

    def draw(self):

        screen.fill(WHITE)

        for j in range(self.grid_size_height):

            for i in range(self.grid_size_width):

                rect = pygame.Rect(i*self.square_size, j*self.square_size, self.square_size, self.square_size)

                tile_val = self.grid[j][i]

                if type(tile_val) == list:

                    val1, val2 = tile_val

                    color1 = self.players[self.dic_id_index[-val1]].lighter_color

                    trig1 = [(i*self.square_size, j*self.square_size), (i*self.square_size+self.square_size, j*self.square_size), (i*self.square_size+self.square_size, j*self.square_size+self.square_size)]

                    color2 = self.players[self.dic_id_index[val2]].darker_color

                    trig2 = [(i*self.square_size, j*self.square_size), (i*self.square_size, j*self.square_size+self.square_size), (i*self.square_size+self.square_size, j*self.square_size+self.square_size)]

                    pygame.draw.polygon(screen, color1, trig1)

                    pygame.draw.polygon(screen, color2, trig2)

                elif tile_val > 0:

                    color = self.players[self.dic_id_index[tile_val]].darker_color

                    pygame.draw.rect(screen, color, rect)

                elif tile_val < 0:

                    color = self.players[self.dic_id_index[-tile_val]].lighter_color

                    pygame.draw.rect(screen, color, rect)

                pygame.draw.rect(screen, BLACK, rect, 3)

        for player in self.players:

            if player != None:

                player.draw()

        pygame.display.update()


class Player:

    def __init__(self, grid, id_):

        self.id = id_

        self.size = grid.square_size

        self.grid = grid

        if self.id == 1:

            self.pos = [100, 100]

        else:

            self.pos = [random.randint(300, 500), random.randint(300, 500)]

        ## initialises the player from the grid's perspective
        self.grid.initialise_player(self)

        self.pos_grid = Player.get_pos_grid(self)

        ##
        #self.pos = [100+100*index, 100+100*index]  # get_random_point_in_screen()

        self.updated_tile = 0

        self.invading = 0

        self.vecteur = [1, 0]

        self.speed = 5

        self.color = get_random_color()

        self.darker_color = [int(x*0.7) for x in self.color]

        self.lighter_color = [min(int(x*1.5), 255) for x in self.color]

    def get_center_pos(self):

        return [self.pos[0]+self.size//2, self.pos[1]+self.size//2]

    def get_pos_grid(self):

        real_pos = Player.get_center_pos(self)

        return self.grid.screen_pos_into_grid(real_pos)

    def out_of_bound(self):

        x, y = self.pos

        if x < 0 or y < 0 or (x >= screen_width - self.size*1.3) or (y >= screen_height - 1.3*self.size):

            return True

    def update(self):

        self.pos[0] += self.vecteur[0] * self.speed

        self.pos[1] += self.vecteur[1] * self.speed

        self.updated_tile = 0

        if Player.out_of_bound(self):

            return "dead"

        else:

            n_pos_grid = Player.get_pos_grid(self)

            if n_pos_grid != self.pos_grid:

                self.updated_tile = 1

                self.grid.update_tile(n_pos_grid, self.id)

                self.pos_grid = n_pos_grid

    def draw(self):

        x, y = self.pos

        rect = pygame.Rect(x, y, self.size, self.size)

        pygame.draw.rect(screen, self.color, rect)

    def turn_left(self):

        self.vecteur = tuple(self.vecteur)

        assoc = {(1, 0):(0, 1), (0, 1):(-1, 0), (-1, 0):(0, -1), (0, -1):(1, 0)}

        self.vecteur = assoc[self.vecteur]

    def turn_right(self):

        for _ in range(3):

            Player.turn_left(self)

        
class IA:

    def __init__(self, associated_player):

        self.compteur = 0

        self.associated_player = associated_player

        self.vecteur = self.associated_player.vecteur

    def decision(self):

        vecteurs = [[-1, 0], [0, 1], [1, 0], [0, -1]]

        self.compteur += 1

        if self.compteur % 7 == 0:

            idx = vecteurs.index(self.vecteur)

            self.vecteur = vecteurs[(idx+1)%4]

        self.associated_player.vecteur = self.vecteur


def main():

    play = True

    clicking = 0

    grid = Grid(30)

    player = grid.players[0]

    ia_s = []

    for i in range(1):

        ia_player = Player(grid, 2+i)

        ia_s.append(IA2(grid, ia_player))  # ia = IA(ia_player)

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

                    if not player.vecteur == [1, 0]:

                        player.vecteur = [-1, 0]

                elif event.key == pygame.K_RIGHT:

                    if not player.vecteur == [-1, 0]:

                        player.vecteur = [1, 0]

                elif event.key == pygame.K_UP:

                    if not player.vecteur == [0, 1]:

                        player.vecteur = [0, -1]

                elif event.key == pygame.K_DOWN:

                    if not player.vecteur == [0, -1]:

                        player.vecteur = [0, 1]

                elif event.key == pygame.K_q:

                    player = Player(grid, 1)

                    player.speed = 5

        grid.update()

        for ia in ia_s:

            ia.decision()

##        if ia_player.updated_tile == 1:
##
##            ia.decision()

        grid.draw()

        print(*grid.grid)

        pygame.display.update()

        clock.tick(60)


main()










