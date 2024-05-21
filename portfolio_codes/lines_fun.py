from pig_tv import *


def draw_lines(fps):

    play = True

    compteur = 0

    adding_rate = 1

    saved_line = get_random_line()

    draw_line(saved_line)

    screen.fill(WHITE)

    color = get_random_color()

    width = random.randint(1, 5)

    s_compteur = 0

    while play:

        compteur += 1

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                play = False

            elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):

                mouse_pos = pygame.mouse.get_pos()

            elif (event.type == pygame.MOUSEMOTION):

                translation = event.rel

        if compteur == adding_rate:

            s_compteur += 1

            if s_compteur == adding_rate*10:

                s_compteur = 0

                saved_line = get_random_line()

                color = get_random_color()

                width = random.randint(1, 5)

            compteur = 0

            n_point = [random.randint(0, screen_width), random.randint(0, screen_height)]

            n_droite = get_perpendiculaire_from_d(saved_line, n_point)#get_random_line()

            draw_line(n_droite, color, width*4)

            saved_line = n_droite

        pygame.display.update()

        clock.tick(fps)


def draw_circles(fps):

    radius = 1

    color = get_random_color()

    signe = 1

    keep_displaying = 1

    x = 0

    while keep_displaying:

        x += 1

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                keep_displaying = False

            elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):

                mouse_pos = pygame.mouse.get_pos()

                keep_displaying = 0

            elif (event.type == pygame.MOUSEMOTION):

                translation = event.rel

        if (x % 4 == 0):

            color = get_random_color()

        pygame.draw.circle(screen, color, (screen_width//2, screen_height//2), radius)

        radius += 1*signe

        if (radius > (screen_height//2)) or (radius < 2):

            signe *= -1

        clock.tick(fps)

        pygame.display.update()

def main(inputs):

    fps, anim_choice = inputs

    if anim_choice == 0:

        draw_lines(fps)

    elif anim_choice == 1:

        draw_circles(fps)

if __name__ == "__main__":

    main([60, 0])
