from pig_tv import *

import matplotlib.pyplot as plt


liste = [0.01, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.9, 0.99]

#liste = [0.52+0.05*i for i in range(10)]

figure, axis = plt.subplots(2, 5)

for proba_mut in liste:

    compt = liste.index(proba_mut)


    mat_passage = Arr([[(1-proba_mut)**2, proba_mut*(1-proba_mut)/2, 0],
                   [proba_mut*(1-proba_mut)*2, 1/2*(proba_mut**2+(1-proba_mut)**2), 0],
                   [(proba_mut)**2, proba_mut*(1-proba_mut)/2, 0]])

    deux_mut = (1-proba_mut)*proba_mut**2

    une_mut = (1-proba_mut)**2*proba_mut

    zero_mut = (1-proba_mut)**3

##    mat_passage = Arr([[(1-proba_mut)**3, 2/3*une_mut, 1/3*deux_mut, 0],
##                       [(1-proba_mut)**3, 2/3*(zero_mut+2*deux_mut), 1/3*(proba_mut**3+2*une_mut), 0],
##                       [3*deux_mut, 2/3*(proba_mut**3+2*une_mut), 1/3*(zero_mut+2*deux_mut), 0],
##                       [proba_mut**3, 2/3*deux_mut, 1/3*une_mut, 0]])

    mat_init = Arr([1, 0, 0])#, 0])

    def reproduce(mat):

        mat = mat_passage*mat

        return mat

    for i in range(5001):

        mat_init = reproduce(mat_init)

        mat_init.normalize()

    mat_init.flatten()

    mat_init.normalize(100)

    mat_init.apply_fun(int)

    a, b, c = mat_init

    #print(a, b, c)
    
##
##    fig, ax = plt.subplots()
##    ax.pie([a, b, c], ["full normal", "semi", "full handicap"], startangle=90)
##    ax.axis('equal')
##    plt.show()

    #print(c//5, c%5, c)
##        

    axis[compt//5, compt%5].pie([a, b, c], labels=["11", "10", "00"])#labels=["111", "110", "100", "000"])#, normalize=True)
    axis[compt//5, compt%5].set_title("muta:"+str(round(proba_mut, 2)))

plt.show()
