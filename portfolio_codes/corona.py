from pig_tv import *


class Ent:

    def __init__(self, index):

        self.x = random.randint(0, screen_width)

        self.y = random.randint(0, screen_height)

        self.size = 30

        self.color = GREEN

        self.sick = 0

        self.vect = get_random_vector()

        if index == 0:

            self.sick = 1

            self.color = RED

    def update(self):

        Ent.move(self)

        Ent.draw(self)

    def move(self):

        if not random.randint(0, 300):

            self.vect = get_random_vector()

        self.x += self.vect[0]

        self.y += self.vect[1]

        if self.x < 0:

            self.x = screen_width

        elif self.x > screen_width:

            self.x = 0

        if self.y < 0:

            self.y = screen_height

        elif self.y > screen_height:

            self.y = 0

    def draw(self):

        pos = [self.x*self.size+self.size//2, self.size*self.y+self.size//2]

        pygame.draw.circle(screen, self.color, pos, self.size//2)


class Pop:

    def __init__(self, pop_size):

        self.pop_size = pop_size

        self.pop = [Ent(x) for x in range(self.pop_size)]

    def update(self):

        Pop.make_sick(self)

        Pop.draw(self)

    def make_sick(self):

        for y in range(self.row_nb):

            for x in range(self.col_nb):

                index = x+y*self.col_nb

                if not index > self.pop_size-1:

                    pass

    def draw(self):

        for liste in self.pop:

            for ent in liste:

                ent.draw()



def main():

    play = True

    clicking = 0

    pop = Pop(50)

    while play:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                play = False

            elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):

                clicking = 1
                
                screen.fill(BLACK)

                pop.update()

                pygame.display.update()

            elif (event.type == pygame.MOUSEBUTTONUP) and (event.button == 1):

                clicking = 0

            elif (event.type == pygame.MOUSEMOTION):

                translation = event.rel

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_LEFT:

                    pass

        clock.tick(60)


if __name__ == "__main__":

    main()
