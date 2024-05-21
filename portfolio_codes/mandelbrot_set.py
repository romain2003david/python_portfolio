from pig_tv import *


def get_nplus1(cur_u, c):

    return cur_u**2+c


def get_cartographie(bornex1, bornex2, borney1, borney2):

    pass


def steady_pixel(u, c):

    for x in range(50):

        #print(u.real, c)

        if abs(u.real) > 20:

            return 0

        u = get_nplus1(u, c)

    return 1


def main():

    u = 0+0j  # int(input("u0 : "))

    #c = int(input("c : "))

    xborne1 = -2  # float(input("x borne 1 : "))

    xborne2 = 2  # float(input("x borne 2 : "))#-xborne1  # 

    x_step = (xborne2-xborne1)/screen_width

##    yborne1 = -2  # float(input("y borne 1 : "))# xborne1  # 
##
##    yborne2 = 2  # float(input("y borne 2 : "))# xborne2  # 
##
##    y_step = (yborne2-yborne1)/screen_height

    yborne1 = -2*(screen_height/screen_width)  # float(input("y borne 1 : "))# xborne1  # 

    yborne2 = 2*(screen_height/screen_width)  # float(input("y borne 2 : "))# xborne2  #

    y_step = x_step

    while True:

        for y in range(screen_height):

            for event in pygame.event.get():

                if event.type == pygame.QUIT:

                    play = False

                    return

            for x in range(screen_width):

                #math_coors = [xborne1 + x*x_step, (yborne1 + y*y_step)]

                pixel_value = xborne1 + x*x_step + (yborne1 + y*y_step)*1j# c

                if steady_pixel(u, pixel_value):

                    screen.set_at((x, y), BLACK)

                else:

                    screen.set_at((x, y), WHITE)

            pygame.display.update()

        pygame.display.update()

        # drawing finished

        click1, click2 = 0, 0

        while (not(click1)) or (not(click2)):

            for event in pygame.event.get():

                if event.type == pygame.QUIT:

                    play = False

                elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):

                    if click1:

                        click2 = pygame.mouse.get_pos()

                    else:

                        click1 = pygame.mouse.get_pos()

                elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 3):

                    mouse_pos = pygame.mouse.get_pos()

                    pixel_value = xborne1 + mouse_pos[0]*x_step + (yborne1 + mouse_pos[1]*y_step)*1j

                    for x in range(50):

                        pos_x = (pixel_value.real-xborne1)/x_step  # set_val_to_different_array([xborne1, xborne2], [0, screen_width], xborne1 + pixel_value.real*x_step)

                        pos_y = (pixel_value.imag-yborne1)/y_step  # set_val_to_different_array([yborne1, yborne2], [0, screen_height], yborne1 + pixel_value.imag*y_step)

                        pygame.draw.circle(screen, RED, [int(pos_x), int(pos_y)], 15)

                        if abs(pixel_value.real) > 20:

                            break

                        pixel_value = get_nplus1(pixel_value, 0+0j)

                    pygame.display.update()

##        click1 = get_click()
##
##        click2 = get_click()

        old_x_borne = [xborne1, xborne2]

        xborne1 = set_val_to_different_array([0, screen_width], old_x_borne, click1[0])

        xborne2 = set_val_to_different_array([0, screen_width], old_x_borne, click2[0])

        x_step = (xborne2-xborne1)/screen_width

        x_ecart = xborne2-xborne1

        old_y_borne = [yborne1, yborne2]

        yborne1 = set_val_to_different_array([0, screen_height], old_y_borne, click1[1])

        yborne2 = yborne1 + x_ecart*(screen_height/screen_width)  # yborne2 = set_val_to_different_array([0, screen_height], old_y_borne, click2[1])

        y_step = (yborne2-yborne1)/screen_height


if __name__ == "__main__":

    main()
