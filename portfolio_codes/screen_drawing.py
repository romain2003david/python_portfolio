from pig_tv import *


def draw_circle(x, y):

    centre = [400, 300]

    radius = 100

    if (x-centre[0])**2 + (y-centre[1])**2 < radius**2:

        return 1


def draw_ellipse(x, y):

    foyer1 = [200, 200]

    foyer2 = [500, 500]

    ref_pt = [501, 501]

    ref_dist = get_distance(ref_pt, foyer1) + get_distance(ref_pt, foyer2)

    if sqrt((x-foyer1[0])**2 + (y-foyer1[1])**2)+sqrt((x-foyer2[0])**2 + (y-foyer2[1])**2) < ref_dist:

        return 1


def draw_s_ellipse(x, y):

    foyer1 = [200, 200]

    foyer2 = [500, 500]

    ref_pt = [550, 550]

    ref_dist = get_distance(ref_pt, foyer1) * get_distance(ref_pt, foyer2)

    if sqrt((x-foyer1[0])**2 + (y-foyer1[1])**2) * sqrt((x-foyer2[0])**2 + (y-foyer2[1])**2) < ref_dist:

        return 1


def draw_poly_centered_ellipse(x, y):

    quit_point_mapping = False

    foyers = []

    while not quit_point_mapping:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                play = False

            elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):

                foyers.append(pygame.mouse.get_pos())

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_Q:

                    quit_point_mapping = True

        for index in range(len(foyers)):

            pt = foyers[index]

            if index == len(foyers)-1:

                color = RED

            else:

                color = GREEN

            pygame.draw.circle(screen, color, pt, 10)

        pygame.display.update()

        clock.tick(60)

    ref_pt = foyers[-1]

    del foyers[-1]

    ref_dist = sum([get_distance(ref_pt, foyer) for x in foyers])

    if sum([get_distance((x, y), foyer) for x in foyers]) < ref_dist:

        return 1


def draw_three_centered_ellipse(x, y):

    foyer1 = [200, 200]

    foyer2 = [500, 200]

    foyer3 = [350, 400]

    ref_pt = [350, 410]

    ref_dist = get_distance(ref_pt, foyer1) + get_distance(ref_pt, foyer2) + get_distance(ref_pt, foyer3)

    if get_distance((x, y), foyer1) + get_distance((x, y), foyer2) + get_distance((x, y), foyer3)< ref_dist:

        return 1


def apply_function_to_screen(function):
    print("Loading screen")

    for y in range(screen_height):

        for x in range(screen_width):

            if function(x, y):

                col = WHITE

            else:

                col = BLACK

            screen.set_at((x, y), col)

    pygame.display.update()


def better_apply_function_to_screen(function):

    quit_point_mapping = False

    foyers = []

    while not quit_point_mapping:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                play = False

            elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):

                foyers.append(pygame.mouse.get_pos())

            elif event.type == pygame.KEYDOWN:

                if event.key == 13:

                    quit_point_mapping = True

        for index in range(len(foyers)):

            pt = foyers[index]

            if index == len(foyers)-1:

                color = RED

            else:

                color = GREEN

            pygame.draw.circle(screen, color, pt, 10)

        pygame.display.update()

        clock.tick(60)

    ref_pt = foyers[-1]

    del foyers[-1]

    ref_dist = product_sum([get_distance(ref_pt, foyer) for foyer in foyers])

    print("Loading screen")

    for y in range(screen_height):

        for x in range(screen_width):

            if product_sum([get_distance((x, y), foyer) for foyer in foyers]) < ref_dist:

                col = WHITE

            else:

                col = BLACK

            screen.set_at((x, y), col)

    pygame.display.update()


def main():

    play = True

    function = draw_poly_centered_ellipse

    clicking = 0

    print("Please click")

    while play:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                play = False

            elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):

                clicking = 1

                better_apply_function_to_screen(function)

                print("Please click")

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
