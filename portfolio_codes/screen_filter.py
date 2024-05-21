"""
try xy border with wb and surexpo*5

filters that can blur images and detect walls

awfully slow (..)
"""

from pig_tv import *

import time

from os import listdir

from os.path import isfile, join


def get_col(blur_grid, zone_colors):

    somme = [0 for x in range(3)]

    for y in range(len(blur_grid)):

        for x in range(len(blur_grid[y])):

            for col in range(3):

                z = zone_colors[y][x][col]

                somme[col] += blur_grid[y][x] * z

    for x in range(len(somme)):

        if somme[x] < 0:

            somme[x] = 0

    return somme


def get_bw_col(blur_grid, zone_colors):

    somme = 0

    #print(zone_colors)

    for y in range(len(blur_grid)):

        for x in range(len(blur_grid[y])):

            z = (zone_colors[y][x][0]+zone_colors[y][x][1]+zone_colors[y][x][2])/3

            somme += blur_grid[y][x] * z

    if somme < 0:

        somme = 0

    return somme


def set_bw_blur(n_screen_width, n_screen_height, bw, dimension, blur_type, graphic=0):
    """ sets a black and white blur to the screen """

    no_blur = [[0, 0, 0], [0, 1, 0], [0, 0, 0]]

    norm_blur = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]

    doubleblur = [[2, 2, 2], [2, 1, 2], [2, 2, 2]]

    deca_blur = [[10, 10, 10], [10, 1, 10], [10, 10, 10]]

    scale5blur = [[1 for x in range(5)] for y in range(5)]

    scale7blur = [[1 for x in range(7)] for y in range(7)]

    scale13blur = [[1 for x in range(13)] for y in range(13)]

    inv_x_blur = [[1, 0, -1], [1, 0, -1], [1, 0, -1]]

    inv_y_blur = [[1, 1, 1], [0, 0, 0], [-1, -1, -1]]

    inv_y_blur_5 = [[2 for x in range(5)], [1 for x in range(5)], [0 for x in range(5)], [-1 for x in range(5)], [-2 for x in range(5)]]

    inv_x_blur_5 = [[2, 1, 0, -1, -2] for x in range(5)]

    inv_y_blur_9 = [[4 for x in range(9)], [3 for x in range(9)], [2 for x in range(9)], [1 for x in range(9)], [0 for x in range(9)], [-1 for x in range(9)], [-2 for x in range(9)], [-3 for x in range(9)], [-4 for x in range(9)]]

    inv_x_blur_9 = [[4, 3, 2, 1, 0, -1, -2, -3, -4] for x in range(9)]

    blur_types = [[norm_blur, doubleblur, deca_blur],
                  [scale5blur, scale7blur, scale13blur],
                  [inv_x_blur, inv_x_blur_5, inv_x_blur_9],
                  [inv_y_blur, inv_y_blur_5, inv_y_blur_9]]

    ## sets the blur
    blur_grid = blur_types[blur_type][dimension]

    blur_sum = 0

    for lis in blur_grid:

        for nbr in lis:

            blur_sum += abs(nbr)

    ecart = int(len(blur_grid[0]))

    new_grid = []

    for y in range(ecart, n_screen_height-ecart):

        new_grid.append([])

        for x in range(ecart, n_screen_width-ecart):

            zone_colors = []

            for y2 in range(-ecart, ecart):

                zone_colors.append([])

                for x2 in range(-ecart, ecart):

                    zone_colors[-1].append(screen.get_at((x+x2, y+y2)))

            if bw:

                col = int(get_bw_col(blur_grid, zone_colors) / blur_sum)

                full_col = [col for x in range(3)]

            else:

                col = get_col(blur_grid, zone_colors)

                full_col = [col[indx]/blur_sum for indx in range(3)]

            new_grid[-1].append(full_col)

    if graphic:

        set_n_screen(new_grid)

    else:

        return new_grid


def set_n_screen(grid):

    for y in range(len(grid)):

        for x in range(len(grid[y])):

            screen.set_at((x, y), grid[y][x])

    pygame.display.update()


def main(inputs):

    dimension, n_screen_width, n_screen_height, surexposition, black_white, blur_type = inputs

    picture_path = select_picture()

    # loads the image

    try:

        img = pygame.image.load('pictures/'+picture_path+'.png')

    except pygame.error:

        img = pygame.image.load('pictures/'+picture_path+'.jpg')

    img = pygame.transform.scale(img, (n_screen_width, n_screen_height))

    screen = pygame.display.set_mode((n_screen_width, n_screen_height))

    #screen = pygame.display.set_mode(img.get_rect().size,0,32)

    #screen_width, screen_height = img.get_rect()[2], img.get_rect()[3]

    screen.blit(img,(0,0))

    # blurs the image

    a = time.time()

    if blur_type == 4:

        n_liste1 = set_bw_blur(n_screen_width, n_screen_height, black_white, dimension, blur_type-1)

        n_liste2 = set_bw_blur(n_screen_width, n_screen_height, black_white, dimension, blur_type-2)

        final_list = sum_arrays(n_liste1, n_liste2, surexposition, surexposition, max_val=255)

    else:

        n_liste1 = set_bw_blur(n_screen_width, n_screen_height, black_white, dimension, blur_type)

        final_list = sum_arrays(n_liste1, n_liste1, surexposition/2, surexposition/2, max_val=255)

    set_n_screen(final_list)

    #print(time.time()-a)

    wait()

    screen = pygame.display.set_mode((screen_width, screen_height))


if __name__ == "__main__":

    dimension = 1

    blur_type = 4

    n_screen_width, n_screen_height = 200, 200

    black_white = 0

    surexposition = 3

    main([dimension, n_screen_width, n_screen_height, surexposition, black_white, blur_type])
