from pig_tv import *

import pygame.surfarray as surfarray

import numpy as N

#allblack = N.zeros((128, 128))

def main2():

    print("chosing images")

    images = []

    for x in range(2):

        # picture choice
        picture_path = select_picture()

        if not picture_path:

            return

        # loads the image

        try:

            images.append(pygame.image.load('pictures/'+picture_path+'.png'))

        except:

            images.append(pygame.image.load('pictures/'+picture_path+'.jpg'))

    rgb_array1 = surfarray.array3d(images[0])

    rgb_array1 = rgb_array1[:min(len(rgb_array1), screen_height), :min(len(rgb_array1[0]), screen_width)]

    rgb_array2 = surfarray.array3d(images[1])

    rgb_array2 = rgb_array2[:min(len(rgb_array2), screen_height), :min(len(rgb_array2[0]), screen_width)]

    screen_image1 = N.zeros((screen_width, screen_height, 3))

    screen_image2 = N.zeros((screen_width, screen_height, 3))

    screen_image1[:len(rgb_array1), :len(rgb_array1[0]), :] = rgb_array1

    screen_image2[:len(rgb_array1), :len(rgb_array1[0]), :] = rgb_array2

    #new_image = allblack = N.zeros((dimensions[0], dimensions[1], 3))  # creates a 2D plane, with each coordinate being an array of 3 int (color), of dimensions defined earlier

    facteur = 100

    print("processing")

    vectors = N.array([[apply_function_to_array(sum_arrays(screen_image1[y][x], screen_image2[y][x], -1), lambda x:x/facteur) for x in range(screen_width)] for y in range(screen_height)])

    print("ready to show")

    #wait()

    print("displaying")

    for x in range(facteur+1):

        pygame.surfarray.blit_array(screen, screen_image1)

        pygame.display.update()

        #print(N.shape(screen_image1), N.shape(vectors))

        screen_image1 += vectors


def main():

    main()
