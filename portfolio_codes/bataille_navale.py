from pig_tv import *


class Bot:

    def __init__(self, sea):

        self.sea = sea

        self.grid = [[0 for x in range(self.sea.cols)] for y in range(self.sea.rows)]

        Bot.init_terrain(self)

    def print_grid(self):

        for arr in self.grid:

            print(*arr)

    def init_terrain(self):

        for c in range(len(self.sea.boat_sizes)):  # each boat's placed on terrain

            orientation = random.randint(0, 1)

            size = self.sea.boat_sizes[c]

            boat_empty_place = 0

            while not boat_empty_place:  # while new boat spawns on already occupied space, it has to respawn somewhere else

                random_spot = Bot.get_random_spot(self, orientation, size)

                n_boat = Boat(random_spot, orientation, size)

                boat_empty_place = 1

                boat_coors = n_boat.get_boat_tiles()

                for coor in boat_coors:

                    if self.grid[coor[0]][coor[1]]:

                        boat_empty_place = 0

            for coor in boat_coors:

                self.grid[coor[0]][coor[1]] = n_boat

    def get_random_spot(self, orientation, size):

        if orientation == 0:  # 0 -> rows -> ys

            return [random.randint(0, self.sea.rows-1-size), random.randint(0, self.sea.cols-1)]

        else:  # 0 -> cols -> xs

            return [random.randint(0, self.sea.rows-1), random.randint(0, self.sea.cols-1-size)]


class Sea:

    def __init__(self):

        self.margin = 10

        self.rows = 10

        self.cols = 10

        self.tile_size = 50

        self.grid = [[0 for x in range(self.cols)] for y in range(self.rows)]

##        self.secret_grid = [[0 for x in range(self.cols)] for y in range(self.rows)]
##
##        self.secret_grid[1] = [1 for x in range(self.cols)]

        self.boat_sizes = [5, 4, 3, 3, 2]

        self.opponent = Bot(self)

        self.secret_grid = self.opponent.grid

    def get_coor_of_pos(self, mouse_pos):
        """ returns coor in grid [x, y] """

        mouse_pos = sum_arrays(mouse_pos, [self.margin, self.margin], 1, -1)

        apply_function_to_array(mouse_pos, lambda x:x//self.tile_size)

        return mouse_pos

    def get_secret_neigbors(self, coors):
        """ return an array of orthogonal neighbors and of diagonal neighbors, of secret grid """

        diag = []

        ortho = []

        for x in range(-1, 2):

            for y in range(-1, 2):

                if (x or y) and not(out_screen(coors[0]+x, coors[1]+y, self.cols-1, self.rows-1)):

                    if not(x and y):  # left, right, up, down

                        ortho.append(self.secret_grid[coors[1]+y][coors[0]+x])

                    else:

                        diag.append(self.secret_grid[coors[1]+y][coors[0]+x])

        return [ortho, diag]

    def attack(self, mouse_pos):

        coor = Sea.get_coor_of_pos(self, mouse_pos)

        if isinstance(self.secret_grid[coor[1]][coor[0]], Boat):  # a boat's been touched

            boat = self.secret_grid[coor[1]][coor[0]]

            boat.attack(coor)

            if boat.dead:

                for tile in boat.get_boat_tiles():

                    self.grid[tile[0]][tile[1]] = 4

            else:

                self.grid[coor[1]][coor[0]] = 2

        elif any(Sea.get_secret_neigbors(self, coor)[0]):  # a boat's near ; if checking get_secret_neigbors(self, coor)[0], it means only left right up down, else, also diagonals

            self.grid[coor[1]][coor[0]] = 3

        else:  # nothing

            self.grid[coor[1]][coor[0]] = 1

    def in_grid(self, mouse_pos):

        return (self.margin < mouse_pos[0] < self.margin + (self.cols*self.tile_size)) and (self.margin < mouse_pos[1] < self.margin + (self.rows*self.tile_size))

    def check_click(self, mouse_pos):

        if Sea.in_grid(self, mouse_pos):

            Sea.attack(self, mouse_pos)

            return 1

    def update(self, graphic):

        if graphic:

            Sea.draw()

    def draw(self):

        for y in range(self.rows):

            for x in range(self.cols):

                if self.grid[y][x] == 0:

                    col = BLUE

                elif self.grid[y][x] == 1:

                    col = GREY

                elif self.grid[y][x] == 2:

                    col = RED

                elif self.grid[y][x] == 3:

                    col = GREEN

                elif self.grid[y][x] == 4:

                    col = ORANGE

                pygame.draw.rect(screen, col, pygame.Rect(self.margin+self.tile_size*x, self.margin+self.tile_size*y, self.tile_size, self.tile_size))

                pygame.draw.rect(screen, WHITE, pygame.Rect(self.margin+self.tile_size*x, self.margin+self.tile_size*y, self.tile_size, self.tile_size), 2)


class Boat:

    def __init__(self, coor, orientation, size):

        self.coor = coor

        self.orientation = orientation

        self.size = size

        self.crashing = 0

        self.active = 0

        self.crashing_col = sum_arrays(RED, GREEN)

        self.crashing_col = sum_arrays(RED, self.crashing_col)

        self.crashing_col = sum_arrays(get_random_color(), self.crashing_col)

        self.dead = 0

        apply_function_to_array(self.crashing_col, lambda x:x/4)

        self.col = [random.randint(0, 50) for x in range(3)]

        self.attacked_coors = []

    def get_boat_tiles(self):

        add = [0, 0]

        boat = []

        for c in range(self.size):

            boat.append(sum_arrays(self.coor, add))

            add[self.orientation] += 1

        return boat

    def move(self, vect):

        self.coor = sum_arrays(self.coor, vect)

    def attack(self, coor):

        if not coor in self.attacked_coors:

            self.attacked_coors.append(coor)

        if len(self.attacked_coors) == self.size:

            self.dead = 1


class Player:

    def __init__(self, sea):

        self.sea = sea

        self.margin = self.sea.margin  # when using Sea functions

        self.tile_size = self.sea.tile_size

        self.cols = self.sea.cols

        self.rows = self.sea.rows

        self.playing = 1

        font = pygame.font.SysFont("monospace", 40, True)

        self.shoot_panneau = Panneau("SHOOT !", 0, screen_height-50, color=RED, font_size=font, y_focus=-25)

        self.boat_select_panneau = Panneau("Select your boats !", 0, screen_height-50, largeur=380, color=RED, y_focus=-25)

        self.done_panneau = Panneau("Done", 400, screen_height-50, color=GREEN, y_focus=-25)

        self.rotate_panneau = Panneau("", 0, screen_height-150, 100, 100, BLUE, image=draw_coin, image_coors=[48, 48], image_args=[35])

        self.grid = [[0 for x in range(self.sea.cols)] for y in range(self.sea.rows)]

        Bot.init_terrain(self)

        self.boats = []

        for arr in self.grid:

            for ent in arr:

                if isinstance(ent, Boat) and (not ent in self.boats):

                    self.boats.append(ent)

        Player.update_sea(self)

        Player.chose_boats(self)

    def chose_boats(self):
        """ allows user to select the position of his boats """

        play = True

        clicking = 0

        while play:

            for event in pygame.event.get():

                if event.type == pygame.QUIT:

                    play = False

                elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):

                    clicking = 1

                    mouse_pos = pygame.mouse.get_pos()

                    if self.done_panneau.clicked(mouse_pos):

                        play = False

                    elif self.rotate_panneau.clicked(mouse_pos):

                        active_boat = 0

                        for boat in self.boats:

                            if boat.active:

                                active_boat = boat

                        if active_boat:

                            active_boat.orientation = (boat.orientation-1) * -1

                            Player.update_sea(self)

                    elif Sea.in_grid(self, mouse_pos):

                        coor = Sea.get_coor_of_pos(self, mouse_pos)

                        tile_val = self.grid[coor[1]][coor[0]]

                        Player.activate_boat(self, tile_val)

                elif (event.type == pygame.MOUSEBUTTONUP) and (event.button == 1):

                    clicking = 0

                elif (event.type == pygame.MOUSEMOTION):

                    translation = event.rel

                elif event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_LEFT:

                        Player.move_active_boat(self, [-1, 0])

                    if event.key == pygame.K_RIGHT:

                        Player.move_active_boat(self, [1, 0])

                    if event.key == pygame.K_UP:

                        Player.move_active_boat(self, [0, -1])

                    if event.key == pygame.K_DOWN:

                        Player.move_active_boat(self, [0, 1])

            self.boat_select_panneau.draw()

            self.done_panneau.draw()

            self.rotate_panneau.draw()

            Player.draw(self)

            pygame.display.update()

            clock.tick(60)

    def activate_boat(self, n_active):
        """ when user choses boats configuration, deals with which boat's selected """

        row, col = self.sea.rows, self.sea.cols

        for boat in self.boats:

            if boat.active:

                boat.active = 0

        if n_active != 0:

            n_active.active = 1

    def move_active_boat(self, vect):
        """ moves active boat of vect[x, y] """

        row, col = self.sea.rows, self.sea.cols

        active_boat = 0

        for boat in self.boats:

            if boat.active:

                active_boat = boat

        if active_boat:

            active_boat.move(vect)

            Player.update_sea(self)

    def update_sea(self):

        occupied_coors = []

        self.grid = [[0 for x in range(self.sea.cols)] for y in range(self.sea.rows)]

        for boat in self.boats:

            this_boat_crashing = 0

            coors = boat.get_boat_tiles()

            for coor in coors:

                if not coor in occupied_coors:

                    occupied_coors.append(coor)

                else:

                    this_boat_crashing = 1

                    boat.crashing = 1

                    other_coor = occupied_coors[occupied_coors.index(coor)]

                    self.grid[other_coor[1]][other_coor[0]].crashing = 1

                if not out_screen(coor[1], coor[0], self.rows-1, self.cols-1):

                    self.grid[coor[1]][coor[0]] = boat

                else:

                    this_boat_crashing = 1

                    boat.crashing = 1

                if not this_boat_crashing:

                    boat.crashing = 0

    def draw(self):

        margin = self.sea.margin

        tile_size = self.sea.tile_size

        for y in range(self.sea.rows):

            for x in range(self.sea.cols):

                if isinstance(self.grid[y][x], Boat):  # selected boat

                    boat = self.grid[y][x]

                    if boat.active:  # active boat

                        if boat.crashing:  # boat that can't be in this position

                            col = boat.crashing_col

                        else:

                            col = sum_arrays(DARK_GREEN, GREEN)

                            apply_function_to_array(col, lambda x:x/2)

                    else:  # normal boat

                        if boat.crashing:  # boat that can't be in this position

                            col = boat.crashing_col

                        else:

                            col = boat.col

                else:  # sea tile

                    col = BLUE

                pygame.draw.rect(screen, col, pygame.Rect(margin+tile_size*x, margin+tile_size*y, tile_size, tile_size))

                pygame.draw.rect(screen, WHITE, pygame.Rect(margin+tile_size*x, margin+tile_size*y, tile_size, tile_size), 2)


    def draw_play(self):

        self.shoot_panneau.draw()

    def update(self):

        mouse_pos = pygame.mouse.get_pos()

        if self.playing:

            Player.draw_play(self)


class PlayerGrid:

    def __init__(self, grid):

        self.grid = grid

        self.margin = 10

        self.rows = 10

        self.cols = 10

        self.tile_size = 50

        for y in range(len(self.grid)):

            for x in range(len(self.grid[y])):

                if self.grid[y][x]:

                   self.grid[y][x] = 2

        self.color_dict = {0 : 1,
                           2 : 3}

    def get_rand_free_coor(self):

        free_places = 0

        for y in range(len(self.grid)):

            for x in range(len(self.grid[y])):

                if (self.grid[y][x] == 0) or (self.grid[y][x] == 2):

                    free_places += 1

        index = random.randint(0, free_places-1)

        for y in range(len(self.grid)):

            for x in range(len(self.grid[y])):

                if (self.grid[y][x] == 0) or (self.grid[y][x] == 2):

                    index -= 1

                    if index == 0:

                        return [y, x]

    def rand_attack(self):

        coor = PlayerGrid.get_rand_free_coor(self)

        self.grid[coor[0]][coor[1]] = self.color_dict[self.grid[coor[0]][coor[1]]]

    def draw(self):

        for y in range(len(self.grid)):

            for x in range(len(self.grid[y])):

                if self.grid[y][x] == 0:

                    col = LIGHT_BLUE

                elif self.grid[y][x] == 1:

                    col = PURPLE

                elif self.grid[y][x] == 2:

                    col = BLACK

                elif self.grid[y][x] == 3:

                    col = RED

                pygame.draw.rect(screen, col, pygame.Rect(self.margin+self.tile_size*x, self.margin+self.tile_size*y, self.tile_size, self.tile_size))

                pygame.draw.rect(screen, WHITE, pygame.Rect(self.margin+self.tile_size*x, self.margin+self.tile_size*y, self.tile_size, self.tile_size), 2)

        pygame.display.update()


def main(inputs):

    play = True

    clicking = 0

    sea = Sea()

    player = Player(sea)

    player_grid = PlayerGrid(player.grid)

    panneau_pause = Panneau("", screen_width-100, 0, 100, 100, color=GREY, image=draw_pause, image_coors=[43, 40])

    while play:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                play = False

            elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):

                clicking = 1

                mouse_pos = pygame.mouse.get_pos()

                if player.playing:

                    has_attacked = sea.check_click(mouse_pos)

                    if has_attacked:

                        screen.fill(BLACK)

                        sea.draw()

                        pygame.display.update()

                        wait()

                        player_grid.draw()

                        wait()

                        player_grid.rand_attack()

                        player_grid.draw()

                        wait()

                if panneau_pause.clicked(mouse_pos):

                    if set_pause():

                        play = False

            elif (event.type == pygame.MOUSEBUTTONUP) and (event.button == 1):

                clicking = 0

            elif (event.type == pygame.MOUSEMOTION):

                translation = event.rel

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_LEFT:

                    pass

        screen.fill(BLACK)

        sea.draw()

        panneau_pause.draw()

        player.update()

        pygame.display.update()

        clock.tick(60)

    end_game(0)


if __name__ == "__main__":

    main([])
