from pig_tv import *


def triangle_interpol():

    points = [Arr([10, 10]), Arr([screen_width-10, 10]), Arr([10, screen_height-10])]  # [Arr(get_random_point_in_screen()), Arr(get_random_point_in_screen()), Arr(get_random_point_in_screen())]

    colors = [Arr(x) for x in [RED, GREEN, BLUE]]

    nb = 10

    rad = 10

##    for a in range(nb):
##
##        for b in range(nb):
##
##            c = nb-a
##
##            a, c, b = (a-b/2)/nb, (c-b/2)/nb, b/nb

    screen.fill(WHITE)

    pygame.draw.polygon(screen, BLACK, points)

    for i in range(3):

       pygame.draw.circle(screen, colors[i], points[i], rad)

    while True:

##        pt = Arr(get_random_point_in_screen())
##
##        pygame.draw.circle(screen, colors[i], points[i], rad)
##
##        if collide_point_polygon(pt, points):
##
##            area_tot = get_area_triangle(points)  # dist_tot = sum([(pt-points[i]).norme_eucli() for i in range(3)])
##
##            a, b, c = [get_area_triangle(pt, points[(i+1)%3], points[(i+2)%3])/area_tot for i in range(3)]

            a, b = random.random(), random.random()

            mi, ma = min(a, b), max(a, b)

            a, b, c = mi, ma-mi, 1-ma

            #print(a+b+c)#, a+b+c, area_tot, [get_area_triangle(pt, points[(i+1)%3], points[(i+2)%3]) for i in range(3)])

            pos = a*points[0]+b*points[1]+c*points[2]

            pos.apply_fun(int)

            color = a*colors[0]+b*colors[1]+c*colors[2]

            color.apply_fun(int)

            pygame.draw.circle(screen, color, pos, rad)


            pygame.display.update()


triangle_interpol()
