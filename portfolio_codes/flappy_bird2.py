"""

19/06/2019

flappy bird refait de maniere propre XD

"""

from pig_tv import *


class Bird:

    def __init__(self, radius, jump_height, color):

        self.x = screen_width//6

        self.y = screen_height//2

        self.radius = radius

        self.y_movement = 0

##        color_dict = {0:get_random_color(),
##                      1:RED,
##                      2:YELLOW,
##                      3:GREEN,
##                      4:BLUE}
##
##        self.color = color_dict[color]

        self.color = ColorManager()

        self.jump_height = jump_height

    def update(self, graphic):

        self.y_movement += .4

        self.y += self.y_movement

        if graphic:

            Bird.draw(self)

        if not Bird.in_borne(self):

            Bird.die(self)

            return 1

    def die(self):

        self.color.color = RED

        Bird.draw(self)

    def in_borne(self):

        return ((self.y > 0) and (self.y < screen_height))

    def jump(self):

        self.y_movement = -self.jump_height

    def draw(self):

        pygame.draw.circle(screen, self.color.color, (int(self.x), int(self.y)), self.radius)

        for x in range(2):

            self.color.update_color()


class Pilier:

    def __init__(self, inter_ecart, pillar_speed):

        self.x = screen_width

        self.width = 50

        self.y1 = 0

        self.height1 = random.randint(screen_height//2-inter_ecart, screen_height//2+inter_ecart)

        self.inter_ecart = inter_ecart

        self.y2 = self.height1 + inter_ecart

        self.height2 = screen_height - self.y1

        self.color = ColorManager()

        self.pillar_speed = pillar_speed

    def update(self, graphic):

        self.x -= self.pillar_speed

        if (self.x+self.width) < 0:

            return 1

        if graphic:

            Pilier.draw(self)

    def draw(self):

        up_rect = pygame.Rect(self.x, self.y1, self.width, self.height1)

        low_rect = pygame.Rect(self.x, self.y2, self.width, self.height2)

        pygame.draw.rect(screen, self.color.color, up_rect)

        pygame.draw.rect(screen, self.color.color, low_rect)

        for x in range(3):

            self.color.update_color()


def main(inputs):

    # variables

    radius, jump_height, inter_ecart, pillar_speed, pillar_spawn_time, color = inputs

    graphic = 1

    new_pillar_time = 1

    points = 0

    piliers = []

    # Instances

    bird = Bird(radius, jump_height, color)

    # game loop

    play = True

    aff_txt("click to play", screen_width//3, screen_height//3, color=RED)

    pygame.display.update()

    wait()

    while play:

        new_pillar_time -= 1

        if not new_pillar_time:

            piliers.append(Pilier(inter_ecart, pillar_speed))

            new_pillar_time = random.randint(pillar_spawn_time-pillar_spawn_time//8, pillar_spawn_time+pillar_spawn_time//8)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                play = False

            elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):

                mouse_pos = pygame.mouse.get_pos()

            elif (event.type == pygame.MOUSEMOTION):

                translation = event.rel

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_SPACE:

                    bird.jump()

        screen.fill(BLUE)

        aff_txt("points : "+str(points), 0, 0, color=YELLOW)

        for x in range(len(piliers)-1, -1, -1):

            pilier_out = piliers[x].update(graphic)

            if pilier_out:

                del piliers[x]

                points += 1

            if collide_circle_to_rect([bird.x, bird.y], bird.radius, [piliers[x].x, piliers[x].y1, piliers[x].width, piliers[x].height1]) or \
               collide_circle_to_rect([bird.x, bird.y], bird.radius, [piliers[x].x, piliers[x].y2, piliers[x].width, piliers[x].height2]):

                   play = False

                   bird.die()

        if play:

            play = not(bird.update(graphic))

        pygame.display.update()

        clock.tick(60)

    wait()

    end_game(points)


if __name__ == "__main__":

    radius = 20

    jump_height = 10

    inter_ecart = 180

    pillar_speed = 5

    pillar_spawn_time = 80

    main([radius, jump_height, inter_ecart, pillar_speed, pillar_spawn_time, 0])
