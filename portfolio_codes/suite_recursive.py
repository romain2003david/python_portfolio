def suite(x, loop):

    resultat = 9 / (6-x)

    if loop == 0:

        return resultat

    return suite(resultat, loop-1)


for x in range(50):

    print(suite(1, x))
