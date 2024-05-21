import matplotlib.pyplot as plt

from matplotlib.pyplot import imread

import pickle


def encode_message_into_image(message, image, start_index=0, encryption_method=0, commencer_a_la_fin=-1, encryption_arg=0):

    image_width = len(image[0])

    image_height = len(image)

    ## test on image

    test = 1

    if test:

        print(len(image), len(image[0]), len(image[0][0]))

        #print(image[0][0:21])

    ##

    if commencer_a_la_fin > 0:

        x = (image_width-1)-(commencer_a_la_fin%image_width)

        y = (image_height-1)-(commencer_a_la_fin//image_width)

    else:

        x = start_index%image_width

        y = start_index//image_width

    for string in message:

        # native function ord can return a number up to 1114111, which is a 21 digits long binary number

        if encryption_method == 0:

            value = bin(ord(string))

        elif encryption_method == "cesar":

            value = bin(ord(string)+encryption_arg)

        to_fill = value[2:]

        liste = []

        for str_ in to_fill:

            liste.append(int(str_))

        for v in range(21-len(liste)):

            liste.insert(0, 0)

        for k in range(7):  # a string is encoded into 7 pixels of 3 colors each (7*3=21)

            color = image[y, x]

            for l in range(3):

                n_color_list = []

                temp_color = bin(color[l])  # converts color integer into binary

                n_color = temp_color[:-1]+str(liste[k*3+l])  # changes last digit of binary, it can't be seen

                n_color_list.append(n_color)

                n_color_list = "0b".join(n_color_list)

##                if (y == 0) and (x < 7):
##
##                    print(k, l, n_color_list, temp_color, liste[k*3+l], int(n_color_list, 2))

                n_color_list = int(n_color_list, 2)  # converts back to decimal

                color[l] = n_color_list

            x += 1

            if x == image_width:

                x = 0

                y += 1

                if y == image_height:

                    print("Image trop petite !! while encoding")

                    return

    #print(image[0][0:21])

    return image


def decode_image(image, car_len=20, start_index=0, converting_method="ord", encryption_method=0, reverse=0, commencer_a_la_fin=-1, encryption_arg=5):

    ##

    test = 0

    if test:

        print(image[0][0:21])

    ##

    image_width = len(image[0])

    image_height = len(image)

    if commencer_a_la_fin > 0:

        x = (image_width-1)-(commencer_a_la_fin%image_width)

        y = (image_height-1)-(commencer_a_la_fin//image_width)

    else:

        x = start_index%image_width

        y = start_index//image_width

    print(x, y)

    secret_string = ""

    if converting_method == "ord":

        for car in range(car_len):

            secret_str_nb = "0b"

            for p in range(7):  # a caracter is stored in 7 pixels with ord method

                pixel = image[y, x]

                for k in range(3):

                    bin_digit = bin(pixel[k])

                    secret_str_nb += str(bin_digit[-1])

                x += 1

                if x == image_width:

                    x = 0

                    y += 1

                    if y == image_height:

                        print("Image trop petite !! while decoding")

                        return

            secret_str_nb = int(secret_str_nb, 2)

            if secret_str_nb < 10000:

                if encryption_method == 0:

                    car = chr(secret_str_nb)

                elif encryption_method == "cesar":

                    car = chr(secret_str_nb-encryption_arg)

                secret_string += car
##
##            else:  # a non coded series of pixels has been detected, end of message reached
##
##                return secret_string

    return secret_string


if __name__ == "__main__":

    picture = imread("pictures/stega2.jpg")

    picture = picture.copy()

    message = "13600CESAR+5"

    n_image = encode_message_into_image(message, picture)

    message = "Il me vient à l'esprit ce qui plus que tout me manque :"

    n_image = encode_message_into_image(message, picture, start_index=13600, encryption_method="cesar", encryption_arg=5)

    with open("n_image.txt", "wb") as file:

        pickle.dump(n_image, file)

    plt.imshow(n_image)

    print(decode_image(n_image, car_len=48))

    #for x in range(7):

    print(decode_image(n_image, car_len=75, start_index=13600, encryption_method="cesar", encryption_arg=5))#, commencer_a_la_fin=245))#

    plt.show()
