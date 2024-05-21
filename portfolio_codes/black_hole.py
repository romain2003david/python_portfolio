from pig_tv import *


class Terrain:

    def __init__(self, steps_per_frame, move_speed):

        self.rows = 100

        self.cols = 100

        self.cote = screen_height//self.rows

        self.grid = [[0 for x in range(self.cols)] for y in range(self.rows)]

        self.montagne_x = self.rows//2

        self.montagne_y = self.cols//2

        self.grid[self.montagne_x][self.montagne_y] = 255

        self.last_vector = get_random_vector(move_speed)

        self.steps_per_frame = steps_per_frame

    def update(self, graphic):

        if random.randint(0, 3):

            self.montagne_x, self.montagne_y = self.montagne_x+self.last_vector[0], self.montagne_y+self.last_vector[1]

        else:

            self.last_vector = get_random_vector(0.1)

            self.montagne_x, self.montagne_y = self.montagne_x+self.last_vector[0], self.montagne_y+self.last_vector[1]

        for x in range(self.steps_per_frame):

            Terrain.add_near_spot(self, round(self.montagne_x), round(self.montagne_y))

        if graphic:

            Terrain.draw(self)

    def add_near_spot(self, x, y, back=0):

        if back > 5:

            return

        x_add = random.randint(random.randint(-5, 0), random.randint(1, 5))

        y_add = random.randint(random.randint(-5, 0), random.randint(1, 5))

        if not out_screen(y+y_add, x+x_add, self.cols-1, self.rows-1):

            if (self.grid[y+y_add][x+x_add] >= random.randint(230, 254)) or (random.randint(0, 4) == 0):

                Terrain.add_near_spot(self, x+x_add, y+y_add, back+1)

            else:

                self.grid[y+y_add][x+x_add] += 2

    def draw(self):

        for y in range(self.rows):

            for x in range(self.cols):

                val = (self.grid[y][x]-255)*-1

                if not val == 0:

                    pygame.draw.rect(screen, (val, val, val), pygame.Rect(x*self.cote, y*self.cote, self.cote, self.cote))#screen.set_at((x, y), (val, val, val))


def main(inputs):

    steps_per_frame, move_speed = inputs

    terr = Terrain(steps_per_frame, move_speed)

    aff = True

    graphic = 1

    while aff:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                aff = False

        terr.update(graphic)

        pygame.display.update()

        #clock.tick(60)

if __name__ == "__main__":

    main([1000, 0.1])
