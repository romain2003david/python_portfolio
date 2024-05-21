from pig_tv import *


def get_screen_color_sum(x_max, y_max):

    color_sum = 0

    for y in range(y_max):

        for x in range(x_max):

            col = screen.get_at([x, y])[:3]

            for s in list(col):

                color_sum += s

    return color_sum


def set_fast_blur(x_max, y_max, blur_size):

    screen1Dfilter(x_max, y_max, blur_size)

    print("half job")

    screen1Dfilter(x_max, y_max, blur_size, 0)


def screen1Dfilter(x_max, y_max, blur_size, y_dimension=1):

    to_test = [x_max, y_max]

    for y in range(y_max):

        for x in range(x_max):

            color_sum = [0, 0, 0]

            divider = (2*blur_size+1)

            for b in range(-blur_size, blur_size+1):

                coors = [x, y]

                if (coors[y_dimension]+b >= 0) and (coors[y_dimension]+b < to_test[y_dimension]):

                    coors[y_dimension] += b

                    color_sum = sum_arrays(color_sum, list(screen.get_at(coors))[:3])

                else:

                    divider -= 1

            apply_function_to_array(color_sum, lambda x:x/divider)

            screen.set_at((x, y), color_sum)

##            if y == y_max-1:
##
##                print(get_screen_color_sum(x_max, y_max))

        pygame.display.update()


def set_screen_bw(x_max, y_max, progressive_update):

    for y in range(y_max):

        for x in range(x_max):

            cur_color = screen.get_at((x, y))

            col_sum = sum(cur_color[:3])

            screen.set_at((x, y), [col_sum/3 for x in range(3)])

        if progressive_update:

            pygame.display.update()



def invert_screen_colors(x_max, y_max, progressive_update):

    rand_int = 1  # random.randint(1, 3)

    ## changing screen
    for y in range(y_max):

        for x in range(x_max):

            cur_color = list(screen.get_at((x, y))[:3])

            for v in range(rand_int):

                cur_color[v] = (cur_color[v]-255)*-1

            screen.set_at((x, y), cur_color)

        if progressive_update:

            pygame.display.update()


def tweak_screen_colors(x_max, y_max, progressive_update):

    ch_index = 0

    ## changing screen
    for y in range(y_max):

        for x in range(x_max):

            cur_color = list(screen.get_at((x, y))[:3])

            first_col = cur_color[ch_index]

            del cur_color[ch_index]

            cur_color.append(first_col)

            screen.set_at((x, y), cur_color)

        if progressive_update:

            pygame.display.update()


def tweak_one_color(x_max, y_max, progressive_update):

    rand_int = 0  # random.randint(1, 3)

    chgmt = 40

    other_ones = [1, 2]

    ## changing screen
    for y in range(y_max):

        for x in range(x_max):

            cur_color = list(screen.get_at((x, y))[:3])

            cur_color[rand_int] += chgmt

            if cur_color[rand_int] > 255:

                cur_color[rand_int] = 255

            elif cur_color[rand_int] < 0:

                cur_color[rand_int] = 0

            for v in other_ones:

                cur_color[v] -= chgmt

                if cur_color[v] > 255:

                    cur_color[v] = 255

                elif cur_color[v] < 0:

                    cur_color[v] = 0

            screen.set_at((x, y), cur_color)

        if progressive_update:

            pygame.display.update()


def set_bw_screen_to_nearest_col(x_max, y_max, progressive_update):

    sum_colors = []

    for x in colors:

        sum_colors.append(sum(x))

    ## changing screen
    for y in range(y_max):

        for x in range(x_max):

            cur_color = screen.get_at((x, y))

            col_sum = sum(cur_color[:3])

            index = sum_colors.index(min(sum_colors, key=lambda x:abs(col_sum-x)))

            screen.set_at((x, y), colors[index])

        if progressive_update:

            pygame.display.update()


def set_screen_to_nearest_col(x_max, y_max, colors, progressive_update):

    ## changing screen
    for y in range(y_max):

        for x in range(x_max):

            cur_color = list(screen.get_at((x, y))[:3])

            all_diffs = []

            for col in colors:

                this_diff = 0

                diff = sum_arrays(cur_color, col, 1, -1)

                #print(diff)

                for v in range(3):

                    this_diff += abs(diff[v])

                all_diffs.append(this_diff)

            #print(all_diffs, cur_color)
                    
            index = all_diffs.index(min(all_diffs))

            #print(index, colors[index])

            screen.set_at((x, y), colors[index])

        if progressive_update:

            pygame.display.update()


def color_test():

    play = True

    while play:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                play = False

            elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):

                mouse_pos = pygame.mouse.get_pos()

                pygame.draw.circle(screen, screen.get_at(mouse_pos), [50, 50], 50)

                cur_color = list(screen.get_at(mouse_pos)[:3])

                all_diffs = []

                for col in colors:

                    this_diff = 0

                    diff = sum_arrays(cur_color, col, 1, -1)

                    #print(diff)

                    for v in range(3):

                        this_diff += abs(diff[v])

                    all_diffs.append(this_diff)

                #print(all_diffs, cur_color)
                        
                index = all_diffs.index(min(all_diffs))

                #print(index, colors[index])

                print(cur_color)

                print(colors[index])

                print(colors)

                pygame.draw.circle(screen, colors[index], [50, 150], 50)

            elif (event.type == pygame.MOUSEMOTION):

                translation = event.rel

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_LEFT:

                    pass

        pygame.display.update()

        clock.tick(60)


def set_random_tweak(x_max, y_max, progressive_update):

    chgmt = 60

    for y in range(y_max):

        for x in range(x_max):

            cur_color = list(screen.get_at((x, y))[:3])

            for v in range(3):

                cur_color[v] += random.randint(-chgmt, chgmt)

                if cur_color[v] > 255:

                    cur_color[v] = 255

                elif cur_color[v] < 0:

                    cur_color[v] = 0

            screen.set_at((x, y), cur_color)

        if progressive_update:

            pygame.display.update()

def main(inputs):

    color_size, blur_size, to_bw, progressive_update, filter_type = inputs

    simple_filters = [set_random_tweak, set_bw_screen_to_nearest_col, tweak_one_color, tweak_screen_colors, invert_screen_colors]

    # picture choice
    picture_path = select_picture()

    if not picture_path:

        return

    # loads the image

    try:

        img = pygame.image.load('pictures/'+picture_path+'.png')

    except:

        try:

            img = pygame.image.load('pictures/'+picture_path+'.jpg')

        except:

            img = pygame.image.load('pictures/'+picture_path+'jpeg')
    ##
    # setting picture to nice dimensions
    frame = img.get_rect()

    size_goal = 800

    facteur_multiplication = size_goal/(max(frame[2], frame[3]))

    n_screen_width, n_screen_height =  int(frame[2]*facteur_multiplication), int(frame[3]*facteur_multiplication)  # [900, 1100]# [[500, 350]  #[700, 500]  # [200, 150]  # 

    img = pygame.transform.scale(img, (n_screen_width, n_screen_height))

    screen = pygame.display.set_mode((n_screen_width, n_screen_height))

    screen.blit(img, (0, 0))

    pygame.display.update()
    ##
    #wait()

    a = time.time()

    # PROCESSING PICTURE

    if to_bw:

        set_screen_bw(n_screen_width, n_screen_height, progressive_update)

        pygame.display.update()

    # checks that filter isn't loosing color
    #print(get_screen_color_sum(n_screen_width, n_screen_height))

    if filter_type < 5:

        simple_filters[filter_type](n_screen_width, n_screen_height, progressive_update)

    elif filter_type == 5:

        colors = [get_random_color() for x in range(color_size)]

        set_screen_to_nearest_col(n_screen_width, n_screen_height, colors, progressive_update)

    elif filter_type == 6:

        set_fast_blur(n_screen_width, n_screen_height, blur_size)

    #set_screen_to_nearest_col(n_screen_width, n_screen_height, colors)  # color_test()# set_random_tweak(n_screen_width, n_screen_height)  # set_fast_blur(n_screen_width, n_screen_height, 10)  # invert_screen_colors(n_screen_width, n_screen_height)  # tweak_one_color(n_screen_width, n_screen_height)  # set_random_tweak(n_screen_width, n_screen_height)

    pygame.display.update()

    #print(get_screen_color_sum(n_screen_width, n_screen_height))

    ##

    print(time.time()-a)

    pygame.display.update()

    wait()



if __name__ == "__main__":

    filter_type = 0

    to_bw = 0

    progressive_update = 1

    color_size = 50

    blur_size = 3

    main([color_size, blur_size, to_bw, progressive_update, filter_type])

