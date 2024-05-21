from pig_tv import *


class Tile:

    def __init__(self):

        self.hidden = 1


def get_random_tile():

    return random.randint(2, 9)


class Grid:

    def __init__(self, player_nb):

        self.rows = 8

        self.cols = 10

        self.tile_size = min(screen_width//self.cols, screen_height//self.rows)

        self.tiles = [[get_random_tile() for x in range(self.cols)] for y in range(self.rows)]

        self.tiles_coor = [[pygame.Rect(x*self.tile_size, y*self.tile_size, self.tile_size, self.tile_size) for x in range(self.cols)] for y in range(self.rows)]

        self.player_nb = player_nb

        self.players = []

        for x in range(player_nb):

            self.players.append(Player(x, self.tile_size))

        self.active_player = 0

    def draw(self):

        for y in range(self.rows):

            for x in range(self.cols):

                pygame.draw.rect(screen, BLACK, self.tiles_coor[y][x], 3)

        for player in self.players:

            player.draw()

    def play(self, move):

        self.players[self.active_player].move(move)

        x, y = self.players[self.active_player].coors

        if self.tiles[y][x].hidden:

            self.tiles[y][x].show()

            Grid.activate_tile(self, self.players[self.active_player], self.tiles[y][x])

        self.active_player = (self.active_player+1)%self.player_nb

    def activate_tile(self, player, tile, move):

        if tile.code == "wall":

            ap(move, lambda x:x*-1)

            self.players[self.active_player].move(move)


class Player:

    def __init__(self, index, tile_size):

        self.index = index

        colors = [RED, BLUE, GREEN, YELLOW, PURPLE]

        self.color = colors[index]

        self.coor = [0, 0]

        self.tile_size = tile_size

        self.radius = 20

        self.special_coors = [random.randint(self.radius, self.tile_size-self.radius), random.randint(self.radius, self.tile_size-self.radius)]

    def draw(self):

        pygame.draw.circle(screen, self.color, [self.coor[0]*self.tile_size+self.special_coors[0], self.coor[1]*self.tile_size+self.special_coors[1]], self.radius)


def main():

    play = True

    clicking = 0

    grid = Grid(5)

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

        grid.draw()

        pygame.display.update()

        clock.tick(60)


if __name__ == "__main__":

    main()
