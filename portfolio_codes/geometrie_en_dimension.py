from pig_tv import *

import random

import time


def add_dimension(vect_dir, points, lines):

    n_points = []

    n_lines = []

    for point in points:

        n_point = (point[0]+vect_dir[0], point[1]+vect_dir[1])

        n_points.append(n_point)

        n_lines.append(["p", points.index(point), points.index(point)+len(points)])  # p means it's a points

    for line in lines:

        if not line == "c":

            index1 = line[1]+len(points)

            index2 = line[2]+len(points)

            n_lines.append(["m", index1, index2])  # m means it's a mirror

    n_lines.insert(0, "c")

    return points+n_points, lines+n_lines



def draw(lines, points, colors, line_thickness):

    test = 0

    if test:

        lines.reverse()

    for point in points:

        cote = 5

        rect = pygame.Rect(point[0], point[1], cote, cote)

        pygame.draw.rect(screen, RED, rect)    # circle(screen, RED, point, 4)

    color_avancement = 0

    for line in lines:

        if line == "c":

            color_avancement += 1

            if test:

                screen.fill(BLACK)

        else:

            #if line[0] == "p":

                #pygame.draw.line(screen, GREY, points[line[1]], points[line[2]], line_thickness)

            #else:

            pygame.draw.line(screen, colors[color_avancement], points[line[1]], points[line[2]], line_thickness)

            pygame.display.update()

def def_start(a):

    #line

    if a == 0:

        point1 = (50, screen_height-20)#screen_width//2-50, screen_height//2-50)

        point2 = (150, screen_height-120)#screen_width//2+50, screen_height//2+50)

        points = [point1, point2]

        lines = [["n", 0, 1]]  # n means it's a normal line

    # triangle

    elif a == 1:

        point1 = (50, screen_height-20)#screen_width//2-50, screen_height//2-50)

        point2 = (150, screen_height-120)#screen_width//2+50, screen_height//2+50)

        point3 = (60, screen_height-80)

        points = [point1, point2, point3]

        lines = [["n", 0, 1], ["n", 0, 2], ["n", 2, 1]]  # n means it's a normal line

    # star

    elif a == 2:

        point1 = (100, screen_height-20)#screen_width//2-50, screen_height//2-50)

        point2 = (50, screen_height-120)#screen_width//2+50, screen_height//2+50)

        point3 = (150, screen_height-20)

        point4 = (200, screen_height-120)

        point5 = (125, screen_height-200)

        points = [point1, point2, point3, point4, point5]

        lines = [["n", 0, 1], ["n", 0, 2], ["n", 2, 1], ["n", 0, 3], ["n", 0, 4], ["n", 3, 1], ["n", 4, 1], ["n", 2, 3], ["n", 2, 4], ["n", 3, 4]]  # n means it's a normal line

    return points, lines


def main(inputs):

    colors = [WHITE, GREEN, BLUE, RED, YELLOW, ORANGE, PINK, PURPLE]*10

    vects = [[200, 0], [0, -150], [230, -50], [100, -300]]  # les directions disponibles pour faire des figures droites, "comprehensibles"

    thickness, start_form = inputs

    points, lines = def_start(start_form)

    draw(lines, points, colors, thickness)

    play = True

    avancement = 0

    while play:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                play = False

            elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):

                try:

                    n_vect = vects[avancement]  # [int(input("x\n")), int(input("y\n"))]   #(random.randint(-10, 10)*10, random.randint(-10, 10)*10)

                except IndexError:

                    n_vect = (random.randint(-10, 10)*10, random.randint(-10, 10)*10)

                points, lines = add_dimension(n_vect, points, lines)

                avancement += 1

                #print(len(lines)-avancement)

                draw(list(reversed(lines)), points, colors, thickness)

        clock.tick(60)


if __name__ == "__main__":

    line_thickness = 10

    inputs = [line_thickness, 0]

    main(inputs)
