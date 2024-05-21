from pig_tv import *


def get_bool_statement(statement_index, rand, last_rand, last2rand, len_points):

    if statement_index == 0:

        return False

    elif statement_index == 1:

        return (last2rand == last_rand)

    elif statement_index == 2:

        return (rand == (last_rand+1)%len_points)

    elif statement_index == 3:

        return ((rand == (last_rand+1)%len_points) or (rand == (last_rand-1)%len_points) or (last_rand == (rand-1)%len_points) or (last_rand == (rand+1)%len_points))

    elif statement_index == 4:

        return (rand == (last_rand+2)%len_points)

    elif statement_index == 5:

        return ((last2rand == last_rand) and ((rand == (last_rand+1)%len_points) or (rand == (last_rand-1)%len_points) or (last_rand == (rand-1)%len_points) or (last_rand == (rand+1)%len_points)))


def init_sommet(nbr_sommet):

    screen.fill(BLACK)

    pygame.display.update()

    print("select the points on the black screen")

    points = []

    for x in range(nbr_sommet):

        wait()

        points.append(pygame.mouse.get_pos())

    screen.fill(WHITE)

    for x in points:

        screen.set_at((x[0], x[1]), BLACK)#pygame.draw.circle(screen, BLACK, (x[0], x[1]), 5)#

    colors = [get_random_color() for x in range(nbr_sommet)]

    return points, colors

def main(inputs):

    nbr_sommet, pt_par_loop, effet_miroir, statement_index = inputs

    points, colors = init_sommet(nbr_sommet)

    play = True

    curseur = screen_center  # [random.randint(0, screen_width), random.randint(0, screen_height)]

    ratio = 2

    rand = 0

    two_in_a_row = 0

    last_rand = 0

    second_last_rand = 1

    while play:

        if effet_miroir:

            ratio = random.randint(120, 290)/100

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                play = False

        #for f in range(9999):

##            if random.randint(0, 10) != 0:
##
##                rand = 0
##
##            elif random.randint(0, 5) == 0:
##
##                rand = 1
##
##            else:

                #rand = 2
            elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):

                mouse_pos = pygame.mouse.get_pos()


        for x in range(pt_par_loop):

            second_last_rand = last_rand

            last_rand = rand

            rand = random.randint(0, len(points)-1)

            # useful for some kind of patterns (see wikipedia page "chaos game")
            while get_bool_statement(statement_index, rand, last_rand, second_last_rand, len(points)):

                rand = random.randint(0, len(points)-1)

            curseur = [(curseur[0]+points[rand][0])//ratio, (curseur[1]+points[rand][1])//ratio]

            screen.set_at((int(curseur[0]), int(curseur[1])), colors[rand])#BLACK)#)pygame.draw.circle(screen, BLACK, (int(curseur[0]), int(curseur[1])), 5)#

        pygame.display.update()

        #clock.tick(10)



if __name__ == "__main__":

    nbr_sommet = 4

    statement = 5

    effet_miroir = 1

    main([nbr_sommet, 10000, effet_miroir, statement])
