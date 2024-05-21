from pig_tv import *


class Ball:

    def __init__(self, width):

        self.vect = [0, 0]

        self.x, self.y = screen_center

        self.radius = 30

        self.normal_speed = width-1

        self.speed = int(self.normal_speed/2)

        self.got_normal_speed = 0

        Ball.init_vect(self)

        self.points = [0, 0]

    def init_ball(self):

        self.got_normal_speed = 0

        self.speed = int(self.normal_speed/3)

        Ball.init_vect(self)

        self.x, self.y = screen_center

    def init_vect(self):

        self.vect[0] = -1

        self.vect[1] = random.randint(-100, 100)/100

        apply_function_to_array(self.vect, lambda x:x*self.speed)

    def update_pos(self):

        self.x += self.vect[0]

        self.y += self.vect[1]

    def tweak_vect(self):

        self.vect[1] += random.randint(-100, 100)/500

    def update(self, rect1, rect2):

        if collide_circle_to_rect([self.x, self.y], self.radius, rect1):

            self.vect[0] *= -1

            Ball.tweak_vect(self)

            self.speed = self.normal_speed

            if not self.got_normal_speed:

                self.got_normal_speed = 1

                apply_function_to_array(self.vect, lambda x:x*3)

        if collide_circle_to_rect([self.x, self.y], self.radius, rect2):

            self.vect[0] *= -1

            Ball.tweak_vect(self)

        if (self.x) < 0:

            Ball.init_ball(self)

            self.points[1] += 1

            return 1

        elif (self.x+self.radius) > screen_width:

            Ball.init_ball(self)

            self.points[0] += 1

            return 1

        elif ((self.y-self.radius) < 0) or ((self.y+self.radius) > screen_height):

            self.vect[1] *= -1

        Ball.update_pos(self)

        Ball.draw(self)

    def draw(self):

        pygame.draw.circle(screen, WHITE, [int(self.x), int(self.y)], self.radius)

        aff_txt("{} : {}".format(self.points[0], self.points[1]), screen_width//2-50, 300, YELLOW)


class Player:

    def __init__(self, numero, width):

        self.numero = numero

        if numero == 0:

            self.color = GREEN

        else:

            self.color = RED

        #self.color = get_random_color()

        self.height = 100

        self.width = width

        self.y = screen_height//2-self.height//2

        self.x = numero*(screen_width-self.width)

        self.y_vect = [0]

        self.speed = 8

    def reinit(self):

        self.y = screen_height//2-self.height//2

    def update(self):

        self.y += self.y_vect[-1]*self.speed  # last clicked button is what players wants

        return Player.draw(self)

    def draw(self):

        rect = pygame.Rect(self.x, self.y, self.width, self.height)

        pygame.draw.rect(screen, self.color, rect)

        return rect

    def go_to(self, y_target):

        if self.y > y_target:

            self.y_vect = [-1]

        else:

            self.y_vect = [1]


def main():

    play = True

    clicking = 0

    width = 10

    ball = Ball(width)

    player1 = Player(0, width)

    player2 = Player(1, width)

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

            elif event.type == pygame.KEYUP:

                if event.key == pygame.K_UP:

                    player1.y_vect.remove(-1)

                    if player1.y_vect == []:

                        player1.y_vect = [0]

                if event.key == pygame.K_DOWN:

                    player1.y_vect.remove(1)

                    if player1.y_vect == []:

                        player1.y_vect = [0]

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_UP:

                    if player1.y_vect == [0]:

                        player1.y_vect = [-1]

                    else:

                        player1.y_vect.append(-1)

                if event.key == pygame.K_DOWN:

                    if player1.y_vect == [0]:

                        player1.y_vect = [1]

                    else:

                        player1.y_vect.append(1)

                if event.key == pygame.K_m:

                    pass

                if event.key == pygame.K_p:

                    pass

        screen.fill(BLACK)

        rect1 = player1.update()

        rect2 = player2.update()

        player2.go_to(ball.y)

        point = ball.update(rect1, rect2)

        if point:

            player1.reinit()

            player2.reinit()

        pygame.display.update()

        clock.tick(100)


if __name__ == "__main__":

    main()
