""" inspired from L system """

from pig_tv import *


def get_dictionnary(dictionnary_index):

    if dictionnary_index == 0:

        return {"f": "f+R++R-f--ff-R+", "R" : "-f+RR++R+f--f-R"}, [-pi/3, pi/3], [screen_width, screen_height], 0, "f"

    elif dictionnary_index == 1:

        return {"f":"f+f--f+f", "R" : "-f+RR++R+f--f-R"}, [-pi/3, pi/3], [100, 500], 0, "f"

    elif dictionnary_index == 2:

        return {"f":"ff+[+f-f-f]-[-f+f+f]", "F":"FFFFFF"}, [-pi/4, pi/4], [screen_width//2, screen_height-100], pi/2, "f"

    elif dictionnary_index == 3:

        return {"f":"f+R-f-R+f", "R":"RR"}, [-2*pi/3, 5*pi/3], [0, 0], 0, "f"

    elif dictionnary_index == 4:

        angle = set_val_to_different_array([0, 360], [0, 2*pi], 120)

        return {"f":"f-R+f+R-f", "R":"RR"}, [-angle, angle], screen_center, 0, "f-R-R"#[0, screen_height], 0

    elif dictionnary_index == 5:

        angle = set_val_to_different_array([0, 360], [0, 2*pi], 60)

        return {"f":"R-f-R", "R":"f+R+f"}, [-angle, angle], [0, screen_height], 0, "f"

    elif dictionnary_index == 6:

        angle = set_val_to_different_array([0, 360], [0, 2*pi], 25)

        return {"X":"f+[[X]-X-f[-fX]+X", "f":"ff"}, [-angle, angle], [100, screen_height], pi/2, "X"

    elif dictionnary_index == 7:

        angle = set_val_to_different_array([0, 360], [0, 2*pi], 90)

        return {"X":"X+Yf+", "Y":"-fX-Y"}, [-angle, angle], screen_center, pi/2, "fX"

    elif dictionnary_index == 8:

        angle = set_val_to_different_array([0, 360], [0, 2*pi], 90)

        return {"f":"+G++f++G-f+G++f++G-", "X":"f[-f]"}, [-angle, angle], screen_center, pi/2, "f"

    elif dictionnary_index == 9:

        angle = set_val_to_different_array([0, 360], [0, 2*pi], 90)

        return {"f":"f+f+f", "X":"f[-f]"}, [-angle, angle], screen_center, pi/2, "f+f+f"

    elif dictionnary_index == 10:

        angle = set_val_to_different_array([0, 360], [0, 2*pi], 60)

        return {"f":"f+f+X", "X":"f-X-"}, [-angle, angle], screen_center, pi/2, "f"

    elif dictionnary_index == 11:

        angle = set_val_to_different_array([0, 360], [0, 2*pi], 1)  # 11

        return {"f":"f[--f]+f", "X":"f-X-"}, [-angle, angle], screen_center, pi/2, "f"

    elif dictionnary_index == 12:

        angle = set_val_to_different_array([0, 360], [0, 2*pi], 45)  # 60

        return {"f":"f[-f]+f", "X":"f-X-"}, [-angle, angle], screen_center, pi/2, "f"

    elif dictionnary_index == 13:

        angle = set_val_to_different_array([0, 360], [0, 2*pi], 1)

        return {"f":"f[[---ff]+f-f]+f", "X":"f-X-"}, [-angle, angle], screen_center, pi/2, "f"

    elif dictionnary_index == 14:

        angle = set_val_to_different_array([0, 360], [0, 2*pi], 15)  # 45, 46, 190

        return {"f":"f-f[-f]+f", "X":"f-X-"}, [-angle, angle], screen_center, pi/2, "f"


def set_dictionnary(sentence, dictionnary):

    n_sentence = ""

    for x in range(len(sentence)):

        try:

            n_sentence += dictionnary[sentence[x]]

        except KeyError:

            n_sentence += sentence[x]

    return n_sentence


def draw_sentence(sentence, dictionnary_index, angles, norme, pos, start_angle, reverse, active_color):

    def update_orientation(orientation, angle):

        orientation[1] += angle

        orientation[1] %= 2*pi

        orientation[0] = get_vect_from_angle(orientation[1])

        return orientation

    screen.fill(WHITE)

    pos_s = []

    color = [0, 0, 0]

    selected_color = [0, 1]

    orientation = [get_vect_from_angle(start_angle), start_angle]

    for index in range(len(sentence)):

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                play = False

        x = sentence[index]

        # draw forward

        if (x == "f") or (x == "R"):

            line_width = 1#set_val_to_different_array([0, len(sentence)], [4, 1], index)

            n_pos = [pos[0]+norme*orientation[0][0], pos[1]-norme*orientation[0][1]]

            pygame.draw.line(screen, color, pos, n_pos, int(line_width))

            if active_color:

                color, selected_color = update_colors(color, selected_color)

            pos = n_pos

            if reverse and out_screen(pos[0], pos[1], screen_width, screen_height):

                orientation = update_orientation(orientation, pi/2)

        # go forward without drawing

        elif (x == "F"):

            pos = [pos[0]+norme*orientation[0][0], pos[1]-norme*orientation[0][1]]

        elif (x == "G"):

            pos = [pos[0]+.5*norme*orientation[0][0], pos[1]-(0.5)*norme*orientation[0][1]]

        elif (x == "2"):

            circle_radius = set_val_to_different_array([0, len(sentence)], [norme//2, norme//4], sentence.index(x))

            pygame.draw.circle(screen, color, (int(pos[0]), int(pos[1])), int(circle_radius))

        elif (x == "["):

            pos_s.append(pos)

        elif (x == "]"):

            pos = pos_s[-1]

            pos_s.pop()

            pygame.display.update()

        elif (x == "-"):

            orientation = update_orientation(orientation, angles[0])

        elif (x == "+"):

            orientation = update_orientation(orientation, angles[1])

    pygame.display.update()


def main(inputs):

    size, reverse, active_color, dictionnary_index = inputs

    dictionnary, angle, pos, start_angle, sentence = get_dictionnary(dictionnary_index)

    draw_sentence(sentence, dictionnary, angle, size, pos, start_angle, reverse, active_color)

    play = True

    while play:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                play = False

            elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):

                sentence = set_dictionnary(sentence, dictionnary)

                draw_sentence(sentence, dictionnary, angle, size, pos, start_angle, reverse, active_color)

                print(len(sentence))

        clock.tick(60)


#alphabet = "f+-[]F"  # f is forward, F is forward without drawing, [ is remember actual pos, ] is go to last remembered pos, + is rotate right, - is rotate left



if __name__ == "__main__":

    size = 10

    reverse, active_color = 1, 1

    dictionnary_index = 14

    main([size, reverse, active_color, dictionnary_index])
