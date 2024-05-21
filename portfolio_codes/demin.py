from pig_tv import *

from random import *


class Bot:
  """ AI that should be able to play bomber fairly well """

  def __init__(self, grid):

    self.grid = grid

    self.proba_grid = [[0 for x in range(self.grid.cols)] for y in range(self.grid.rows)]  # not truly a prob, might be higher than one

    Bot.update_known_grid(self)

  def update_known_grid(self):

    self.useful_grid = [[-1 for x in range(self.grid.cols)] for y in range(self.grid.rows)]

    for y in range(self.grid.rows):

      for x in range(self.grid.cols):

        if not self.grid.game_grid[y][x].hidden:

          if (self.grid.game_grid[y][x].flag) or (self.grid.game_grid[y][x].type == -1):  # bomb

            self.useful_grid[y][x] = -2

          else:  # normal tile

            self.useful_grid[y][x] = self.grid.game_grid[y][x].type

  def get_neighbours(self, x, y, bomb_nb):

    possibles = []

    for delta_y in [-1, 0, 1]:

      for delta_x in [-1, 0, 1]:

        if (not ((delta_x == 0) and (delta_y == 0))) and Grid.in_grid(self.grid, x+delta_x, y+delta_y):

          if self.useful_grid[y+delta_y][x+delta_x] == -2:

            bomb_nb -= 1

          elif self.useful_grid[y+delta_y][x+delta_x] == -1:

            possibles.append([x+delta_x, y+delta_y])

    return [bomb_nb, possibles]

  def biggest_or_smallest(self):

    max_ = [-1, []]

    min_ = [1, []]

    for y in range(self.grid.rows):

      for x in range(self.grid.cols):

        if self.grid.game_grid[y][x].hidden == 1:

          proba = self.proba_grid[y][x]

          if proba > max_[0]:

            max_ = [proba, [x, y]]

          if proba < min_[0]:

            min_ = [proba, [x, y]]

    delta_max = 1-max_[0]

    if delta_max < min_[0]:  # we evaluate high enough the likeliness of finding a bomb

      return [max_[1], 1]

    else:

      return [min_[1], 0]

  def find_likeliest(self):

    for y in range(self.grid.rows):

      for x in range(self.grid.cols):

        if self.useful_grid[y][x] > 0:  # tiles that hold information

          bomb_nb, possibles = Bot.get_neighbours(self, x, y, self.useful_grid[y][x])

          if (bomb_nb == 0) and (len(possibles) > 0):  # this is not a bomb

            return [possibles[0], 0]

          elif (bomb_nb == len(possibles)) and (len(possibles) != 0):  # this is a bomb

            return [possibles[0], 1]

          else:

            for coor in possibles:

              t_x, t_y = coor

              self.proba_grid[t_y][t_x] += (bomb_nb/len(possibles))

    return Bot.biggest_or_smallest(self)

  def action(self):

    Bot.update_known_grid(self)

    chosen_tile_data = Bot.find_likeliest(self)

    if chosen_tile_data[0] == []:  # grid is full

      return -1

    else:

      Grid.activate_location(self.grid, chosen_tile_data[0], chosen_tile_data[1])


class Carre:

  def __init__(self, x, y, type_, size):
		
    self.x = x

    self.y = y

    self.size = size

    self.center = [int(self.x+self.size//2), int(self.y+self.size//2)]

    self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
    
    self.type = type_  # normal or bomb

    self.hidden = True

    self.flag = 0

    self.colors = [BLACK, BLUE, GREEN, RED, YELLOW, PURPLE, ORANGE, PINK]

  def draw_nbr(self):

    aff_txt(str(self.type), self.x, self.y, color=self.colors[self.type])

  def draw_bombe(self):

    pygame.draw.circle(screen, BLACK, self.center, int(self.size//2))

  def draw_flag(self):

    pygame.draw.circle(screen, RED, self.center, int(self.size//2))

  def draw(self):

    if not self.hidden:

      pygame.draw.rect(screen, GREY, self.rect)

      if self.flag == 1:

        Carre.draw_flag(self)

      else:

        if self.type == -1:

          Carre.draw_bombe(self)
        
        elif self.type != 0:

          Carre.draw_nbr(self)

    pygame.draw.rect(screen, BLACK, self.rect, 2)

    
class Grid:

  def __init__(self, cols, rows, fraction):

    self.cols = cols

    self.rows = rows

    self.square_size = min(screen_width//self.cols, screen_height/self.rows)

    print(self.square_size)

    self.facteur_frac = fraction

    self.coor_bombes = placement_bombes(rows-1, cols-1, (self.rows*self.cols)//self.facteur_frac)

    self.game_grid = [[0 for x in range(self.cols)] for y in range(self.rows)]

    for y in range(self.rows):

      for x in range(self.cols):

        if [x, y] in  self.coor_bombes:

          self.game_grid[y][x] = Carre(x*self.square_size, y*self.square_size, -1, self.square_size)   
        
        else:

          self.game_grid[y][x] = Carre(x*self.square_size, y*self.square_size, 0, self.square_size)
    
    Grid.init_bombes(self)

  def in_grid(self, x, y):
  
    return ((0 <= x < self.cols) and (0 <= y < self.rows))

  def init_bombes(self):

    for coor in self.coor_bombes:

      x_coor, y_coor = coor

      for y in range (-1,2):
        
        for x in range (-1,2):

          if Grid.in_grid(self, x+x_coor, y+y_coor):

            voisin = self.game_grid[y_coor+y][x_coor+x]

            if not voisin.type == -1:

              voisin.type += 1

  def draw(self):

    screen.fill(WHITE)

    for liste in self.game_grid:

      for carre in liste:

        carre.draw()
  
  def deal_with_click(self, flag=False):

    mouse_pos = pygame.mouse.get_pos()

    coors = [int(mouse_pos[0]/self.square_size), int(mouse_pos[1]/self.square_size)]

    if Grid.in_grid(self, coors[0], coors[1]):

      Grid.activate_location(self, coors, flag=flag)

  def activate_location(self, coor, flag=0):

      if flag:

        Grid.activate_flag(self, coor[0], coor[1])

      else:

        Grid.activate_case(self, coor[0], coor[1])

  def activate_flag(self, x, y):

    if self.game_grid[y][x].flag == 1:

      self.game_grid[y][x].hidden = 1

      self.game_grid[y][x].flag = 0

    else:

      self.game_grid[y][x].hidden = 0

      self.game_grid[y][x].flag = 1
  
  def activate_case(self, x, y):

    self.game_grid[y][x].hidden = 0

    if self.game_grid[y][x].type == 0:

      for delta_y in [-1, 0, 1]:

        for delta_x in [-1, 0, 1]:

          if (not ((delta_x == 0) and (delta_y == 0))) and Grid.in_grid(self, x+delta_x, y+delta_y):

            if self.game_grid[y+delta_y][x+delta_x].hidden:

              Grid.activate_case(self, x+delta_x, y+delta_y)


def placement_bombes (rows, cols, nb_bombe):
	
  liste = []

  bombe = 0
    
  while bombe  < nb_bombe:

    x = randint(0, rows) 

    y = randint(0, cols) 

    coor = [x, y]

    if not coor in liste:

      bombe += 1

      liste.append([x,y])

  return liste


def main():

  for x in range(9, 1, -1):

    rows_cols = 5

    grid = Grid(rows_cols, rows_cols, x)

    play = True

    clicking = 0

    bot = Bot(grid)

    while play:

      for event in pygame.event.get():

        if event.type == pygame.QUIT:

          play = False

        elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):

          grid.deal_with_click()

        elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 3):
        
          grid.deal_with_click(flag=True)

        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE:

              pass

      if bot.action():

        play = False

      grid.draw()

      pygame.display.update()

      #clock.tick(60)

    wait()


if __name__ == "__main__":

  main()




