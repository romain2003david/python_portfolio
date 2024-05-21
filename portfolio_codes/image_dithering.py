from pig_tv import *


def set_filter_to_array(array, filter_function, coors=False):

    for y in range(len(array)):

        for x in range(len(array[y])):

            if coors:

                array[y][x] = filter_function(array[y][x], x, y)

            else:

                array[y][x] = filter_function(array[y][x])

    return array


def gray_average(x):

    if len(x) == 1:

        return x

    return [int((x[0]+x[1]+x[2])/3)]


def black_and_white(x):

    if (x[0]+x[1]+x[2])/3 > 127:

        return [255]

    else:

        return [0]


def b_w_dithering1(val, x, y):

    weights = [64, 128, 192, 0]

    if (y % 2) == 0:

        weight = weights[:2][x%2]

    else:

        weight = weights[2:][x%2]

    return [((weight < val[0])*256 or 1)-1]


def b_w_dithering2(val, x, y):

    weights = [(x/9)*255 for x in range(9)]

    index = (y%3)*3+x%3

    return [((weights[index] < val[0])*256 or 1)-1]


def get_gray(col):

    return col*3


def get_rgb(col):

    return col


def dithering(array):

    array = set_filter_to_array(array, gray_average)

    #set_screen_array(array, len(array[0]), len(array))

    #pygame.display.update()

    array = set_filter_to_array(array, b_w_dithering2, 1)

    set_screen_array(array, len(array[0]), len(array))

    pygame.display.update()


def get_screen_array(x_len, y_len):

    array = []

    for y in range(y_len):

        array.append([])

        for x in range(x_len):

            array[-1].append(screen.get_at((x, y)))

    return array


def set_screen_array(array, x_len, y_len):

    if len(array[0][0]) == 1:

        col_function = get_gray

    else:

        col_function = get_rgb_col

    for y in range(y_len):

        for x in range(x_len):

            screen.set_at((x, y), col_function(array[y][x]))


def main():

    image_path = select_picture()

    try:
        image = pygame.image.load('pictures/'+image_path+'.png')
    except FileNotFoundError:
        image = pygame.image.load('pictures/'+image_path+'.jpg')

    image = pygame.transform.scale(image, (screen_width, screen_height))

    x_screen, y_screen = screen_width, screen_height

##    x_screen, y_screen = image.get_height(), image.get_width()
##
##    screen = pygame.display.set_mode((x_screen, y_screen))

    screen.blit(image, [0, 0])

    pygame.display.update()

    last_time = time.time()

    array = get_screen_array(x_screen, y_screen)

    dithering(array)

    #print(time.time()-last_time)

    wait()


if __name__ == "__main__":

    main()
