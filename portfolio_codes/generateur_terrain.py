import random
import numpy

from pig_tv import *


fact1 = 100
fact2 = 500

##def printalts(liste):
##
##  liste = [round(x) for x in liste]
##
##  maxalt, minalt = max(liste), min(liste)
##
##  tab = [['W' if (x+minalt <= liste[y]) else ' ' for x in range(maxalt-minalt) ] for y in range(len(liste))]
## 
##  ntab = numpy.array(tab)
##
##  ntab.transpose()
##
##  #print(ntab)
## 
##  for x in range(maxalt-minalt):
##    print()
##
##    for c in [tab[y][-x-1] for y in range(len(liste))]:
##      print(c, end='')


def draw(altitudes):

    c = 0

    width = screen_width/len(altitudes)

    height_unit = screen_height/(max(altitudes)-min(altitudes))

    screen.fill(LIGHT_BLUE)

    for tour in altitudes:

        height = (tour-min(altitudes))*height_unit

        rect = pygame.Rect(c*width, screen_height-height, width, height)

        pygame.draw.rect(screen, BROWN, rect)

        c += 1

    pygame.display.update()

def rand_centree():

  return random.random()-0.5



def terrain3D(terrain_square_nb_width=10, terrain_square_nb_height=10):

    altitudes = [[0 for j in range(terrain_square_nb_width)] for i in range(terrain_square_nb_height)]

    args =  [[[0, 1] for j in range(terrain_square_nb_width)] for i in range(terrain_square_nb_height)]

    distribution = [0.1, 0.2, 0.4, 0.2, 0.1]

    action_radius = 2

    for i in range(1, terrain_square_nb_height):

        for j in range(terrain_square_nb_width):

            e, s = args[i-1][j]

            randnb = numpy.random.normal(e, s)

            val = (altitudes[i-1][j]+randnb)

            altitudes[i][j] = val*distribution[action_radius]

            for k in range(1, 1+action_radius):

                for signe in [-1, 1]:

                    if (0 <= j+k*signe <= terrain_square_nb_width-1):

                        e, s = args[i-1][j+k*signe]

                        randnb = numpy.random.normal(e, s)

                        altitudes[i][j] = (altitudes[i-1][j+k*signe]+randnb)*distribution[action_radius+k*signe]

                    else:

                        altitudes[i][j] += val*distribution[action_radius+k*signe]

    return altitudes

            
def terrain2D():

    altitudes = [0]

    args =  [[0, 1]]  # stores local arguments of gaussian law that determines next jump
    for x in range(500):
      #print(altitudes, args)
      e, s = args[-1]
      randnb = numpy.random.normal(e, s)
      altitudes.append(altitudes[-1]+randnb)
      args.append([e+rand_centree()/fact1, abs(s+rand_centree()/fact2)])

    draw(altitudes)



terrain3D()
