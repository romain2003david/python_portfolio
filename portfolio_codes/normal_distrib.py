from pig_tv import *


def normal_repartition(x, mean, standard_deviation):

    return 1/(standard_deviation*sqrt(2*pi))*e**((-1/2)*((x-mean)/standard_deviation)**2)


def main():

    mean, stand_dev = 0, 1

    print(normal_repartition(0.12, mean, stand_dev))

##    range_ = 100
##
##    for x in range(10):
##
##        stand_dev += 4
##
##        array = []
##
##        for x in range(-range_, range_):
##
##            fx = normal_repartition(x, mean, stand_dev)
##
##            array.append(fx)
##
##        graph_array(array, 1)
##
##        wait()


if __name__ == "__main__":

    main()
