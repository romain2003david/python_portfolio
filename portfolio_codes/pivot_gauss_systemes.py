import numpy as np

def switch_lines(matrix, i, j):

    if type(matrix[0]) != list:

        matrix[i], matrix[j] = matrix[j], matrix[i]

    else:

        for x in range(len(matrix[i])):

            matrix[i][x], matrix[j][x] = matrix[j][x], matrix[i][x]


def print_m(matrix):

    print()

    for r in matrix:

        for nb in r:

            if nb < 0:

                print(round(nb, 1), end=" ")

            else:

                print(round(nb, 1), end="  ")

        print()

    print()
    print()


def transvect(matrix, i, j, a):

    for x in range(len(matrix[i])):

        matrix[i][x] += a*matrix[j][x]


def biggest_nb_in_col(matrix, c, r_start=0):

    """ returns biggest number (abs) in the column of a matrix, starting from row r_start """

    return max(abs(matrix[r][c]) for r in range(r_start, len(matrix)))


def index_of_row_biggest_in_col(matrix, c, r_start=0):
    """ returns index of row of biggest nb in a col of a matrix """

    biggest_nb = biggest_nb_in_col(matrix, c, r_start)

    return [abs(matrix[r][c]) for r in range(r_start, len(matrix))].index(biggest_nb)+r_start


def pivot_gauss(square_matrix, sol_matrix):

    """ finds solution of n equations with n unknown values """

    # checks format

    n = len(square_matrix)

    if not(n == len(square_matrix[0]) == len(sol_matrix)):

        print("\nBad Format !")


    # descending part : applies the transvects

    for k in range(n-1):

        # remonte le plus grand pivot en valeur absolu

        new_k_line = index_of_row_biggest_in_col(square_matrix, k, k)

        if k != new_k_line:

            switch_lines(square_matrix, k, new_k_line)

            switch_lines(sol_matrix, k, new_k_line)

        # cancels out all lines under

        for l in range(k+1, n):

            coef = (-square_matrix[l][k]) / square_matrix[k][k]

            transvect(square_matrix, l, k, coef)

            sol_matrix[l] += sol_matrix[k] * coef

    # ascending part : finds unknown values

    # now that we have a diagonal matrix, we can find the unknowns one after the other

    sols = [0 for x in range(n)]

    for k in range(n):

        row = n-1-k

        sols[row] = sol_matrix[row]

        for r in range(row+1, n):

            sols[row] -= square_matrix[row][r]*sols[r]

        sols[row] /= square_matrix[row][row]

    ##

    return sols


# tests

#test 1
test_system = [[2, 2, -3], [-2, -1, -3], [6, 4, 4]]

second_membre = [2, -5, 16]

resultat_espere = [-14, 21, 4]

print(pivot_gauss(test_system, second_membre))

# test 2
test_system2 = [[0.003, 59.14], [5.291, -6.13]]

second_membre2 = [59.17, 46.78]

resultat_espere2 = [1, 10]

print(pivot_gauss(test_system2, second_membre2))

# test 3

test_system3 = [[1, 1, 1], [2, -1, 0], [3, 0, 2]]

second_membre3 = [2, 3, 4]

resultat_espere3 = [-2/3, -1/3, -1]

print(pivot_gauss(test_system3, second_membre3))

# test 4
test_system4 = [[4, 2], [1, -1]]

second_membre4 = [3, 2]

resultat_espere4 = [1.16, 0.83]

print(pivot_gauss(test_system4, second_membre4))

# exo I

elec_matrix = [[100, 220, 0, 0, 0], [0, -220, 220, 100, 0], [0, 0, 0, 100, -200], [1, -1, -1, 0, 0], [0, 0, 1, -1, -1]]

elec_tensions = [5, 0, 0, 0, 0]

print(pivot_gauss(elec_matrix, elec_tensions))

# exo II

systeme = [[0.005, -0.1, 0.1], [-0.1*0.1, -1, 0], [0.2*0.1, 0, -1]]

second_membre = [0, -0.1*9.18, -0.2*9.18]

print(pivot_gauss(systeme, second_membre))

num = 74653897
if num > 1:
    for i in range(2, num//2):
        if (num % i) == 0:
            print(num, "is not a prime number")
            break
        else:
            print(num, "is a prime number")
else:
    print(num, "is not a prime number")
