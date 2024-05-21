def p_loop():

    play = True

    clicking = 0

    while play:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                play = False

            elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):

                clicking = 1

            elif (event.type == pygame.MOUSEBUTTONUP) and (event.button == 1):

                clicking = 0

            elif (event.type == pygame.MOUSEMOTION):

                translation = event.rel

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_LEFT:

                    pass

        pygame.display.update()

        clock.tick(60)


def affichage_while_condition(fct_affichage, condition_clicking=0, condition_pressing=0):
    """ the conditions that are equal to one are the stop conditions for the while loop ; fct_affichage prints what's necessary on the screen, given the "time" (nb of loops) """

    play = True

    clicking = 0

    pressing = 0

    c = -1

    while (not (condition_clicking and clicking)) and (not (condition_pressing and pressing)):

        c += 1

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                play = False

            elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):

                clicking = 1

            elif (event.type == pygame.MOUSEBUTTONUP) and (event.button == 1):

                clicking = 0

            elif (event.type == pygame.MOUSEMOTION):

                translation = event.rel

            elif event.type == pygame.KEYDOWN:

                pressing = 1

                if event.key == pygame.K_LEFT:

                    pass

        fct_affichage(c)

        pygame.display.update()

        clock.tick(60)


def end_game(points):

    screen.fill(RED)

    pygame.display.update()

    wait()

    screen.fill(BLACK)

    pygame.display.update()

    wait()

    aff_txt("Game Over", 100, 200, color=RED, taille=50)

    pygame.display.update()

    wait()

    aff_txt("Points : "+str(points), 100, 400, color=RED, taille=50)

    pygame.display.update()

    wait()


## Syntax functions

def invite(liste):
    """ takes a list with at each index a list of [str, str], which is expected output and string in input """

    choix = False

    string = ""

    for x in liste:

        string += "{} : {}\n".format(x[0], x[1])

    string += "\n"

    possible_inputs = [str(x[0]) for x in liste]

    while type(choix) != int:

        got = input(string)

        if got in possible_inputs:

            choix = possible_inputs.index(got)

    return choix


def get_time_from_sec(sec):

    secondes = str(sec%60)

    if int(secondes) < 10:

        secondes = "0"+secondes

    minutes = str(sec//60)

    if int(minutes) < 10:

        minutes = "0"+minutes

    return minutes+" : "+secondes


## Maths functions


def get_trigo_sole_angle(angle):
    """ returns the angle modulo[2pi], the only angle, so that two same angles are equal"""

    return angle % (2*pi)

    
def polar_to_cartesian_coors(angle, radius):

    return [radius*cos(angle), radius*sin(angle)]


def cartesian_to_polar_coors(x, y):

    dist = sqrt(x**2+y**2)

    if x == 0:

        if y > 0:

            angle = pi/2

        else:

            angle = -pi/2

    else:

        angle = atan(y/x)

    return [angle, dist]


def product_sum(liste):

    sum_ = liste[0]

    for x in range(1, len(liste)):

        sum_ *= liste[x]

    return sum_

    
def get_sign(nbr):

    if nbr < 0:

        return -1

    return 1


def get_sign_zero(nbr):

    if nbr < 0:

        return -1

    elif nbr == 0:

        return 0

    return 1


def factoriel(x):

    if x == 1:

        return 1

    return factoriel(x-1)*x


def get_sign_with_null(nbr):

    if nbr < 0:

        return -1

    elif nbr > 0:

        return 1

    return 0


# angles stuff

def get_pos_on_circle(pi_angle, radius=1, move_list=[0, 0]):
    """ returns the pos of a point on a circle according to some angle(0 to two pi) """

    return [cos(pi_angle)*radius+move_list[0], sin(pi_angle)*radius+move_list[1]]


def get_vect_from_angle(angle, pi_angle=1, rounding=5):

    if not pi_angle:

        angle = set_val_to_different_array([0, 360], [0, 2*pi], angle)

    if rounding:

        return get_vector_to_point([0, 0], [round(cos(angle), rounding), round(sin(angle), rounding)], 1)

    else:

        return get_vector_to_point([0, 0], [cos(angle), sin(angle)], 1)


##


def sym_to_point(pos, center):

    dist_x = center[0]-pos[0]

    n_x = center[0]+dist_x

    dist_y = center[1]-pos[1]

    n_y = center[1]+dist_y

    return [n_x, n_y]


def get_ratio(nbr1, nbr2):

    if nbr2:

        return nbr1/nbr2

    else:

        return nbr1


def get_contraire_in_array(val, array):

    ecart = array[1]-array[0]

    return array[0]+((val-array[0])-ecart)*-1


def test_get_contraire_in_array():

    print(  get_contraire_in_array(0.5, [0, 2]),
            get_contraire_in_array(1.5, [1, 2]),
            get_contraire_in_array(1.5, [0, 2]),
            get_contraire_in_array(0.5, [-1, 2]),
            get_contraire_in_array(-0.5, [-2, 0])
            )


# round


def round_between(nbr, bornes, to_go_bornes=[0, 1], round_to=2):

    return round(((to_go_bornes[1]-to_go_bornes[0])*(nbr-bornes[0]))/(bornes[1]-bornes[0]), round_to)


def round_list(to_round_list, round_to=0):

    for x in range(len(to_round_list)):

        to_round_list[x] = round(to_round_list[x], round_to)

        if round_to == 0:

            to_round_list[x] = int(to_round_list[x])

    return to_round_list


def out_screen(x, y, x_max, y_max, min_x=0, min_y=0):

    return (x<min_x) or (y<min_y) or (x>x_max) or (y>y_max)


# Array functions



def get_list_indexs(liste, element):

    indexs = []

    for x in rl(liste):

        item = liste[x]

        if item == element:

            indexs.append(x)

    return indexs


def get_list_indexs_deep(liste, element, max_depth=-1):

    indexs = []

    for x in rl(liste):

        item = liste[x]

        if item == element:

            indexs.append(x)

        elif type(item) == list and max_depth != 0:

            for res in get_list_indexs_deep(item, element, max_depth-1):

                if type(res) == int:

                   indexs.append([x, res])

                else:

                    indexs.append([x]+res)

    return indexs


def get_practical_format(frmt1, frmt2):

    if len(frmt1) > len(frmt2):

        return list(reversed(get_practical_format(frmt2, frmt1)))

    elif len(frmt1) < len(frmt2):  # array 2 might have a useless dimension

        one_indexs = get_list_indexs(frmt2, 1)

        for one_idx in one_indexs:  # trying all possibilities in exponential manner, but list sizes should be relatively small

            n_frmt2 = frmt2.copy()

            print(n_frmt2, one_idx)

            del n_frmt2[one_idx]

            n_frmts = get_practical_format(frmt1, n_frmt2)

            if n_frmts != None:

                return n_frmts

        return None

    else:

        if frmt1 == frmt2:

            return frmt1, frmt2

        else:  # can't be changed into the other format

            return None


def test_format_gestion():

    a1 = Arr([[1, 0]])

    print(a1.format)

    a2 = Arr([1, 0])

    print(a2.format)

    a3 = a1+a2

    print(a3, a3.format)




def get_flattened_list(liste, reduc_nb=-1):

    if reduc_nb != 0:

        if not (type(liste) == list or type(liste) == tuple):

            return liste

        n_liste = []

        for x in liste:

            if (type(x) == list or type(x) == tuple):

                n_liste.extend(get_flattened_list(x, reduc_nb-1))

            else:

                n_liste.append(x)

        return n_liste

    return liste


def get_reduced_dim_list(liste):

    n_liste = []

    for x in liste:

        if type(x) == list:

            n_liste.extend(x)

        else:

            n_liste.append(x)

    return n_liste


def replace_liste(liste, old_element, new_element):

    for idx in rl(liste):

        x = liste[idx]

        if type(x) == Arr:

            x.replace(old_element, new_element)

        elif type(x) == list:

            replace_liste(x, old_element, new_element)

        elif x == old_element:

            liste[idx] = new_element


def in_deep(liste, element):

    vrai = False

    for x in liste:

        if x == element:

            return True

        elif type(x) == list:

            if in_deep(x, element):

                vrai = True

        elif isinstance(x, Arr):

            if x.in_deep(element):

                vrai = True

    return vrai


def complete_copy_list(liste):

    copie = []

    for x in liste:

        if type(x) == list:

            copie.append(complete_copy_list(x))

        else:

            copie.append(x)

    return copie


class Arr:

    def __init__(self, liste):

        self.liste = liste

        self.len = len(liste)

        self.format = Arr.get_format(self)

    def __len__(self):

        return self.len

    def __eq__(self, arr):

        if isinstance(arr, Arr):

            return self.liste == arr.liste

        elif isinstance(arr, list):

            return self.liste == arr

        else:

            return False

    def __add__(self, arr2):

        if not isinstance(arr2, Arr):

            raise TypeError("Careful ! You're trying to add an Array and sth weird ({})".format(type(arr2)))

        #elif len(arr2) != self.len:

            #raise ValueError("The lists don't have same length")

        elif self.format != arr2.format:

            self.reduce_useless_dims()

            arr2.reduce_useless_dims()

            if arr1.format == arr2.format:

                return self+arr2

##            # on regarde si on peut interpreter les formats comme etant equivalent
##
##            n_frmts = get_practical_format(self.format, arr2.format)
##
##            print(n_frmts)
##
##            if n_frmts != None:
##
##                n_self_format, n_arr2_frmt = n_frmts
##
##                if self.format != n_self_format:
##
##                    array1 = self.adapted_to_n_format(n_self_format)
##
##                else:
##
##                    array1 = self
##
##                if arr2.format != n_arr2_frmt:
##
##                    array2 = arr2.adapted_to_n_format(n_arr2_frmt)
##
##                else:
##
##                    array2 = arr2
##
##                return array1 + array2  # returns the simplist format

            else:

                raise ValueError("Arrays that you're trying to add don't have same format : {} and {}".format(self.format, arr2.format))

        else:  # matching formats

            return Arr([self.liste[x]+arr2.liste[x] for x in range(self.len)])

    def __mul__(self, fact):

        # multiplication scalaire
        if type(fact) == float or type(fact) == int or (isinstance(fact, Arr) and (fact.format == [1, 1] or fact.format == [1])):  # produit par un scalaire

            if isinstance(fact, Arr) and (fact.format == [1, 1] or fact.format == [1]):

                fact.flatten()

                fact = fact.liste[0]

            if len(self.format) == 1 or (len(self.format) == 2 and self.format[1] ==1):

                return Arr([self.liste[x]*fact for x in range(self.len)])

            else:  # apllies the multiplication by fact recursively to sub arrays

                return Arr([(Arr(self.liste[x])*fact).liste for x in range(self.len)])

        # mutlipication par arr
        elif isinstance(fact, Arr):
            # multiplication scalaire masquee
            if (self.format == [1, 1] or self.format == [1]):

                arr = Arr.flattened(self)

                facteur = arr.liste[0]

                return facteur*fact

            # multiplication terme a terme (produit de Hadamard)
            if self.format == fact.format and (self.len == 1):

                if len(self.format) == 1:

                    return Arr([self.liste[x]*fact.liste[x] for x in range(self.format[0])])

                else:

                    return Arr([(Arr(self.liste[x])*Arr(fact.liste[x])).liste for x in range(self.format[0])])  # needs to transform the inner lists in arrays to treat recursively

            # dot product (produit de matrices)
            else:

                if len(self.format) == 2:  # matrice carree

                    other_format = fact.format

                    other_list = fact.liste

                    if len(other_format) == 1:  # format adaptation (and also list adaptation, accordingly)

                        other_format.append(1)

                        fact.liste = [[x] for x in other_list]

                        other_list = fact.liste

                    if other_format[0] != self.format[1]:

                        raise ValueError("Unvalid Array formats in Array multiplication (formats : {}, {})".format(self.format, fact.format))

                    res_liste = [[sum([self.liste[l][k]*other_list[k][c] for k in range(self.format[1])]) for c in range(other_format[1])] for l in range(self.format[0])]

                    return Arr(res_liste)

                elif len(fact.format) == 2:  # facteur : matrice carree

                    other_format = fact.format

                    if len(self.format) == 1:  # un vecteur ligne (x1, ..., xn) est aussi une matrice (n, 1)

                        self.liste = [self.liste]

                        self.format.insert(0, 1)

                    this_list = self.liste

                    #if self.format[0] == 1:

                     #   this_list = [this_list]

                    if other_format[0] != self.format[1]:

                        raise ValueError("Unvalid Array formats in Array multiplication (formats : {}, {})".format(self.format, fact.format))

                    res_liste = [[sum([this_list[l][k]*fact.liste[k][c] for k in range(self.format[1])]) for c in range(other_format[1])] for l in range(self.format[0])]

                    return Arr(res_liste)

                #elif self.format[

                else:

                    raise ValueError("Unvalid Array formats in Array multiplication (formats : {}, {})".format(self.format, fact.format))
        else:

            raise TypeError("Unexpected type in Array multiplication (type {})".format(type(fact)))

    def __rmul__(self, fact):

        return Arr.__mul__(self, fact)

##    def __divmod__(self, fact):
##
##        return Arr.__mul__(self, 1/fact)

    def __sub__(self, arr2):

        return Arr.__add__(self, (arr2*(-1)))

    def __neg__(self):

        return Arr([-x for x in self.liste])

    def __str__(self):

        return self.__repr__()

    def __repr__(self):

        if len(self.format) == 2:

            string = "\nArr ( \n"

            c = 0

            for x in self.liste:

                c += 1

                if c == 1:

                    string += "[ " + str(x) + " ]\n"

                else:

                    string += " [ " + str(x) + " ]\n"

            return string + " ) ; \nFormat: "+str(self.format)

        else:

            return "\nArr ( "+str(self.liste)+ " ) ; \nFormat: "+str(self.format)

    def is_nul(self):

        for x in self.liste:

            if x != 0:

                return False

        return True

    def __getitem__(self, key):

        return self.liste[key]

    def __setitem__(self, key, value):

        self.liste[key] = value

        self.format = Arr.get_format(self)

        self.len = len(self.liste)

    def produit_terme_a_terme(self):

        if len(self.liste) == 0:

            return 1
        else:

            return self.liste[0]*(Arr(self.liste[1:]).produit_terme_a_terme())

    def transposed(self):

        if len(self.format) == 2:

            n_liste = [[self.liste[i][j] for i in range(self.format[0])] for j in range(self.format[1])]

            return Arr(n_liste)

        elif len(self.format) == 1:

            n_liste = [[self.liste[i]] for i in range(len(self.liste))]

            return Arr(n_liste) 

        else:

            print("On transpose seulement des matrices")

    def transpose(self):

        transp_arr = Arr.transposed(self)

        self.liste = transp_arr.liste

        self.format = transp_arr.format

    def copy(self):

        return Arr(self.liste.copy())

    def append(self, item):

        self.reduce_useless_dims()

        self.format[0] += 1

        self.len += 1

        self.liste.append(item)

    def get_format(self):
        """ format is a list : it's len is the Array's depth, ie le nb de listes imbriquees, and each number of the list is the size of the dimension associated """

        def get_format_liste(liste):

            contains_list = 0

            contains_non_list = 0

            for x in liste:  # looking at item of this main list

                if type(x) == list:

                    contains_list = 1

                else:

                    contains_non_list = 1

            if contains_list == 0:

                return [len(liste)]

            elif contains_list == 1 and contains_non_list == 1:

                return [len(liste), "_"]  # invalid format

            else:  # list contains only sub lists

                liste_formats = []

                # computes format of each sublist
                for ss_liste in liste:

                    liste_formats.append(get_format_liste(ss_liste))

                for format_ in liste_formats[1:]:

                    if format_ != liste_formats[0]:

                        return [len(liste), "_"]  # invalid format

                return [len(liste)]+liste_formats[0]

        return get_format_liste(self.liste)

    def reduce_useless_dims(self):

        form = self.format

        for i in range(len(form)-1, -1, -1):

            if form[i] == 1:

                self.reduce_dim_rg(i)

    def reduce_dim_rg(self, i):

        def reduce_useless_dim_liste(liste, rg):

            if rg == 0:

                return liste[0]

            return [reduce_useless_dim_liste(ss_liste, rg-1) for ss_liste in liste]

        self.liste = reduce_useless_dim_liste(self.liste, i)

        del self.format[i]

        self.len = len(self.liste)

    def adapted_to_n_format(self, n_format):
        """ !!! not done yet """

        n_arr = self.copy()

        n_format

        return n_arr

    def get_nul(format_):

        def get_nul_liste(format_):

            if len(format_) == 1:

                return [0 for x in range(format_[0])]

            else:

                return [get_nul_liste(format_[1:]) for x in range(format_[0])]

        return Arr(get_nul_liste(format_))

    def get_mat_rot2D(angle):

        return Arr([[cos(angle), -sin(angle)], [sin(angle), cos(angle)]])

    def get_polar(self):
        """ for a 2D vector (x, y) returns radius and angle """

        if self.liste[0] == 0:

            if self.liste[1] >= 0:

                angle = pi/2

            else:

                angle = -pi/2

        else:

            ratio = self.liste[1] / self.liste[0]

            angle = arctan(ratio)

        return Arr.norme_eucli(self), angle

    def norme_eucli(self):

        #nbr_termes = Arr(self.format).produit_terme_a_terme()

        if len(self.format) == 1:

            return get_distance_eucli_rn(self.liste, [0 for x in range(self.format[0])])

        else:
            return (self.flattened()).norme_eucli()

    def get_distance(arr1, arr2):

        if len(arr1.format) == 1:

            return get_distance_eucli_rn(arr1.liste, arr2.liste)

        elif len(arr1.format) == 2:

            return sum([get_distance_eucli_rn(arr1.liste[x], arr2.liste[x]) for x in rl(arr1.liste)])
        else:

            print("bad format, not done yet")

    def normalize(self, norme=1, type_norme=2):

        if not Arr.is_nul(self):

            norme_actuelle = Arr.norme_eucli(self)

            facteur = norme/norme_actuelle

            self.liste = Arr.__mul__(self, facteur).liste

    def normalized(self, norme=1):

        arr = Arr.copy(self)

        arr.normalize(norme)

        return arr

    def get_random(norme=1, dim=2):

        liste = [random.random()-0.5 for x in range(dim)]

        arr = Arr(liste)

        arr.normalize(norme)

        return arr

    def get_angle(arr1, arr2):
        """ returns angle between two 2D vectors """

        #print(Arr.get_angle_with_x(arr2), arr2, arr1, Arr.get_angle_with_x(arr1))

        return Arr.get_angle_with_x(arr2)-Arr.get_angle_with_x(arr1)

    def get_angle_with_x(arr):

        if arr[1] >= 0:

            arr = arr.copy()

            arr.normalize()

            ps = Arr.p_s(Arr([1, 0]), arr)

            return acos(ps)

        else:

            return pi+Arr.get_angle_with_x(-arr)

    def spherical_coor(self):
        """ from euclidian to spherical coordinates """

        if self.format == [3]:

            r = self.norme_eucli()

            theta = acos(self.liste[2]/r)

            phi = Arr.get_angle_with_x(Arr([self.liste[0], self.liste[1]]))

            return r, theta, phi

        else:

            print("Pb, need an R3 vector")

    def normal_vects3D(self):

        r, theta, phi = self.spherical_coor()

        #print(r, theta, phi)

        u_theta = Arr([cos(theta)*cos(phi), cos(theta)*sin(phi), -sin(theta)])

        u_phi = Arr([-sin(phi), cos(phi), 0])

        round3 = lambda x:round(x, 3)

        return u_theta.with_fun_applied(round3), u_phi.with_fun_applied(round3)

    def apply_fun(self, function):

        self.liste = [function(x) for x in self.liste]

    def with_fun_applied(self, function):

        return Arr([function(x) for x in self.liste])

    def p_s(arr1, arr2):
        """ produit scalaire euclidien de deux vecteurs de R^n """

        if len(arr1) == len(arr2):

            return sum([arr1[x]*arr2[x] for x in range(len(arr1))])

        else:

            print("pb de format pour les vecteurs a scalariser")

            raise Exception

    def get_orth(self):
        """ retourne la droite orthogonale de norme 1 pour un vecteur 2D , (x' y') tq [(x y) scal (x' y') = 0]"""

        if self.format == [2]:

            x, y = self.liste

            if x == 0:

                return Arr([1, 0])

            else:

                y_prim = x**2/(x**2+y**2)

                x_prim = -y_prim*y/x

                return Arr([x_prim, y_prim])

        else:

            raise ValueError("Expected 2D vector, got format : {}".format(self.format))

    def draw(self):

        size = 100

        pygame.draw.line(screen, BLACK, [size, size], [size+self.liste[0]*10, size+self.liste[1]*10])

    def get_indexs(self, element):

        return get_list_indexs(self.liste, element)

    def get_indexs_deep(self, element, max_depth=-1):
        """ get all multidimensional indexes of an element in a multidimensional list ; if max_depth is not -1, the list elements that are more than max_depth dimensional are ignored """

        return get_list_indexs_deep(self.liste, element, max_depth)

    def in_deep(self, element):

        return in_deep(liste, element)

    def flatten(self):

        self.liste = get_flattened_list(self.liste)

        self.format = [len(self.liste)]

    def flattened(self):

        arr = Arr.copy(self)

        arr.flatten()

        return arr

    def replace(self, old_element, new_element):

        replace_liste(self.liste, old_element, new_element)

    def complete_copy(self):

        return Arr(complete_copy_list(self.liste))



def test_arr_class():

    ## tests format

    print("tests format")

    a = [1, 2, 3]

    b = [1, [], 3]

    c = [[1], [1], [1]]

    d = [[], [], []]

    e = [[1, 2], [3, 4], [5, 6]]

    f = [[1, 2], [3, 4], [5]]

    lis = [a, b, c, d, e, f]

    for x in lis:

        ar = Arr(x)

        print(ar.format)

    ## tests dot product

    print("tests dot product")

    X = [1, 2]

    Id = [[1, 0], [0, 1]]

    id_arr = Arr(Id)

    x_arr = Arr(X)

    homo2 = 2.5*id_arr

    print(id_arr*x_arr)

    print(homo2*x_arr)

    #print(x_arr*id_arr)

    print(homo2*homo2)

    A = [[0, 1], [0, 0]]

    a = Arr(A)

    print("a", a*a)

    M = [[0, 1, 0, 0],
         [0, 0, 1, 0],
         [0, 0, 0, 1],
         [0, 0, 0, 0]]

    m_arr = Arr(M)

    print(m_arr*m_arr)

    print(m_arr*m_arr*m_arr)

    print(m_arr*m_arr*m_arr*m_arr)

    ##

#test_arr_class()


def rl(liste):

    return range(len(liste))


#test_arr_class()


def get_average(array):

    return sum(array)/len(array)


def val_in_array(val, array, is_sorted=0):
    """ tests if a given value is "in" an array """

    if not is_sorted:

        array.sort()

    if array[0] <= val <= array[1]:

        return True


def sum_arrays(array1, array2, facteur1=1, facteur2=1, max_val=0):
    """ sums same size arrays """

    if len(array1) != len(array2):

        print("Arrays of different sizes !")

        return

    n_array = []

    for x in range(len(array1)):

        if type(array1[x]) == list:

            n_array.append(sum_arrays(array1[x], array2[x], facteur1, facteur2, max_val))

        else:

            n_array.append(array1[x]*facteur1 + array2[x]*facteur2)

            if max_val:

                if n_array[-1] > max_val:

                    n_array[-1] = max_val

    return n_array


def appartient(val, borne1, borne2):

    return (borne1 <= val <= borne2) or (borne2 <= val <= borne1)


def set_val_to_different_array(from_array_bornes, n_bornes, val, mustbe_inborne=False):

    ecart = from_array_bornes[1] - from_array_bornes[0]

    if not ecart:

        return n_bornes[0]  # switched from val to n_bornes[0] : might cause unexpected pbs?

    pos = val-from_array_bornes[0]

    pos_relative = pos/ecart

    if mustbe_inborne and (pos_relative < 0):

        return n_bornes[0]

    if mustbe_inborne and (pos_relative > 1):

        return n_bornes[1]

    n_ecart = n_bornes[1] - n_bornes[0]

    n_pos = pos_relative*n_ecart

    return n_bornes[0]+n_pos


def try_set_val_to_different_array():

    test_array = [[1, [-1, 1], [0, 1]], [-1, [-1, 1], [0, 1]], [0, [-1, 1], [0, 1]], [0.25, [-1, 1], [0, 1]], [0.5, [-1, 1], [0, 1]]]

    for x in test_array:

        print("{} from this array : {} to that one : {}\n-> {}".format(x[0], x[1], x[2], set_val_to_different_array(x[1], x[2], x[0])))


def set_array_to_different_array(last_bornes, n_bornes, array):

    for x in range(len(array)):

        array[x] = set_val_to_different_array(last_bornes, n_bornes, array[x])

    return array


def colliding_arrays(array1, array2, needa_sort=1):

    if needa_sort:

        array1.sort()

        array2.sort()

    return ((array1[0]<=array2[0]) and (array1[1]>=array2[0])) or ((array2[0]<=array1[0]) and (array2[1]>=array1[0]))


def index_2d_array(array, to_index):

    for y in array:

        for x in y:

            if x == to_index:

                return array.index(y)

    return False


def set_list_to(to_set_list, total=1):

    sum_list = sum(to_set_list)

    if sum_list == 0:

        return to_set_list

    for x in range(len(to_set_list)):

        to_set_list[x] /= sum_list * total

    return to_set_list


def get_random_vector(norme=1):

    return [(random.randint(-100, 100)/100)*norme, (random.randint(-100, 100)/100)*norme]


def get_normalized_vector(origin_vector, norme, approximation=0):
    """ scales a vector """

    dist = abs(origin_vector[0])+abs(origin_vector[1])

    if dist <= approximation:

        return [0, 0]

    else:

        facteur = norme / dist

        origin_vector[0] *= facteur

        origin_vector[1] *= facteur

        return origin_vector


def get_sign_of_array(liste):

    for x in range(len(liste)):

        if liste[x] > 0:

            liste[x] = 1

        elif liste[x] < 0:

            liste[x] = -1

        else:

            liste[x] = 0

    return liste


def graph_array(array, gets_into_it=1, graph_inversely=0):
    """ input : list of f(x) ; function that represents the values in a list as ordinates in the plan, their index being their x """

    ind_place = screen_width//len(array)

    radius = ind_place // 2

    screen.fill(WHITE)

    min_max = [min(array), max(array)]

    ly = 0

    for x in range(len(array)):

        y = array[x]

        if gets_into_it:

            y = set_val_to_different_array(min_max, [screen_height, 0], y)

        elif graph_inversely:

            y = (screen_height-y)

        pygame.draw.line(screen, BLACK, ((x-1)*(ind_place or 1), ly), (x*(ind_place or 1), y))

        if radius:

            pygame.draw.circle(screen, BLUE, (int(x*(ind_place or 1)), int(y)), radius)

        else:

            screen.set_at((int(x*(ind_place or 1)), int(y)), radius)



        ly = y

        pygame.display.update()

    wait()



def graph_arrays(array_of_arrays, min_val=None, max_val=None):

    screen.fill(WHITE)

    colors = [BLUE, RED, YELLOW, GREEN, BLACK, PURPLE]

    # defines max coors of grid

    if min_val == None:

        min_val = min(min(array_of_arrays, key=lambda x:min(x)))

        #min_val *= (9/10)

    if max_val == None:

        max_val = max(max(array_of_arrays, key=lambda x:max(x)))

        #min_val *= (11/10)

    point_nb = 0

    for arr in array_of_arrays:

        if len(arr) > point_nb:

            point_nb = len(arr)

    x_step = screen_width / point_nb

    # places the sequences on the grid
    for arr in array_of_arrays:

        last_pos = 0

        # initialisating each sequence's color
        index = array_of_arrays.index(arr)

        if index > len(colors)-1:

            color = get_random_color()

        else:

            color = colors[index]

        aff_txt(str(index), index*50, 0, color)

        # placing each point
        for indx in range(len(arr)):

            x_cor = indx * x_step

            y_cor = set_val_to_different_array([min_val, max_val], [screen_height-20, 20], arr[indx])

            cur_pos = [int(x_cor), int(y_cor)]

            pygame.draw.circle(screen, color, cur_pos, 10)

            if last_pos:

                pygame.draw.line(screen, color, last_pos, cur_pos)

            last_pos = cur_pos

    pygame.display.update()

    wait()


def get_vector_to_point(point1, point2, norme, approximation=0):
    """ Basically gets vector between 2 points, converts it to a given distance, returns """

    vector = []

    for x in range(2):

        vector.append(point2[x]-point1[x])

    dist = abs(vector[0])+abs(vector[1])

    if dist <= approximation:

        return [0, 0]

    else:

        facteur = norme / dist

        vector[0] *= facteur

        vector[1] *= facteur

        return vector


def add_arrays(add_to_array, array):
    """ Adds an array to an other one of same size """

    return [add_to_array[x]+array[x] for x in range(len(add_to_array))]


def random_weighted_choice(weight_list, must_set_to_one=0):
    """ takes the list from where to chose an element, and the list with each weight, sorted in the same order as the first list. if weights have to be set to_one, put to 0"""

    if must_set_to_one:

        set_list_to(weight_list, 1)

    if all(v == 0 for v in weight_list):

        return "Liste egale a 0"

    max_val = 1

    choix = random.randint(0, 1000)/1000

    index = 0

    while max_val > choix:

        try:

            max_val -= weight_list[index]

        except IndexError:  # probably because of bad approximation

            print("Error ?\n(random_weighted_choice function, as long as unfrequent errors, it's alright)")

            return len(weight_list)-1

        index += 1

    return index-1


def times_array_by_val(array, const):

    for x in range(len(array)):

        array[x] *= const

    return array


def add_val_to_array(array, const):

    for x in range(len(array)):

        if type(array[x]) == list:

            array[x] = add_val_to_array(array[x], const)

        else:

            array[x] += const

    return array


def apply_function_to_array(array, function):

    for x in range(len(array)):

        if type(array[x]) == list:

            array[x] = apply_function_to_array(array[x], function)

        else:

            array[x] = function(array[x])

    return array


def get_array_with_applied_function(array, function):

    return [function(x) for x in array]


# Geometrical functions


def add_vectors(vector1, vector2, scale_factor1=1, scale_factor2=1):

    return [vector1[i]*scale_factor1 + vector2[i]*scale_factor2 for i in range(len(vector1))]


def get_distance_eucli_rn(x, y):
    """ ok : get_distance_eucli_rn([0, 0, 0], [1, 1, 1]) = sqrt(3) """
##
##    print(x, y)
##
##    if type(x) == Arr:
##
##        return get_distance_eucli_rn(y, x.flattened)
##
##    elif type(y) == Arr:
##
##        return get_distance_eucli_rn(x, y.flattened)

    return sqrt(sum([(x[i]-y[i])**2 for i in range(len(x))]))


def get_normale_2D(vector):
    """ vecteur v tq <vector|v> = 0 et norme(v) = 1; dans R^2, produit scalair canonique = x*x' + y*y' """

    x, y = vector

    if x == 0:

        return [1, 0]

    else:

        y1 = sqrt(1/(1+(y**2/x**2)))

        x1 = -(y1*y)/x

        return [x1, y1]

    
def get_scaled_vecteur(vector, scale_factor):

    return [x*scale_factor for x in vector]


def vect_nul(vector):

    for x in vector:

        if x != 0:

            return False

    return True


def get_vect_unitaire(vector, norme):

    if not vect_nul(vector): 

        scale_factor = 1/norme(vector)

        return get_scaled_vecteur(vector, scale_factor)

    else:

        print("erreur vecteur nul -")
        a


def get_normalized_vector_eucli(vector, norme=1):

    if not vect_nul(vector): 

        scale_factor = norme/get_distance(vector, [0, 0])

        return get_scaled_vecteur(vector, scale_factor)

    else:

        print("erreur vecteur nul _")
        a

    
def get_vect_unitaire_dim2(vecteur):

    norme = lambda x:get_distance(x, [0, 0])

    return get_vect_unitaire(vecteur, norme)

class QuadTree:
    """ class creating quadtree instances, supposed to hold many entities, and keep track of which entity is close to which ones (divides the "universe" (often a grid) in smaller squares) """ 

    def __init__(self, x, y, width, height, max_subd_nb=4, ent_before_subd=4, cur_subd_nb=0):

        self.x = x

        self.width = width

        self.y = y

        self.height = height

        self.max_subd_nb = max_subd_nb

        self.cur_subd_nb = cur_subd_nb

        self.ent_before_subd = ent_before_subd

        self.content = []

        self.subdivided = 0

    def draw(self, color=(0, 0, 0), vector=[0, 0]):

        if self.subdivided:

            for baby_tree in self.content:

                baby_tree.draw(color, vector)

        else:

            rect = pygame.Rect(self.x+vector[0], self.y+vector[1], self.width, self.height)

            pygame.draw.rect(screen, color, rect, 3)

    def unite(self):

        if not self.subdivided:

            print("Uniting when already united !")

            a

        self.subdivided = 0

        n_content = []

        for child in self.content:

            n_content.append(child.content)

        self.content = n_content

    def subdivide(self):
        """ subdivides current tree (square) into an array of four new trees : [left top, right top, left bottom, right bottom] """

        # routine check
        if self.subdivided:

            print("Subdividing when already subdivided !")

            a

        self.subdivided = 1

        stored_entities = self.content.copy()

        self.content = []

        # creates the new children trees

        next_sub_nb = self.cur_subd_nb+1

        self.content.append(QuadTree(self.x, self.y, self.width/2, self.height/2, self.max_subd_nb, self.ent_before_subd, next_sub_nb))

        self.content.append(QuadTree(self.x+self.width/2, self.y, self.width/2, self.height/2, self.max_subd_nb, self.ent_before_subd, next_sub_nb))

        self.content.append(QuadTree(self.x, self.y+self.height/2, self.width/2, self.height/2, self.max_subd_nb, self.ent_before_subd, next_sub_nb))

        self.content.append(QuadTree(self.x+self.width/2, self.y+self.height/2, self.width/2, self.height/2, self.max_subd_nb, self.ent_before_subd, next_sub_nb))

        # fills the different trees
        for ent in stored_entities:

            QuadTree.add_in_children(self, ent)

    def add_entity(self, entity):

        if self.subdivided:  # adds entity in children trees

            QuadTree.add_in_children(self, entity)

        else:

            if (len(self.content) < self.ent_before_subd) or (self.cur_subd_nb == self.max_subd_nb):  # still has place in store, or the tree is already too subdivided

                self.content.append(entity)

            else:  # subdivides

                QuadTree.subdivide(self)

                QuadTree.add_in_children(self, entity)

    def add_in_children(self, ent):

        checking_with_radius = 1

        if checking_with_radius:  # putting circle in each square it's in

            if ent.x-ent.radius < self.x+self.width/2:  # a part of it is left of screen

                if ent.y-ent.radius < self.y+self.height/2:

                    self.content[0].add_entity(ent)

                if ent.y+ent.radius > self.y+self.height/2:

                    self.content[2].add_entity(ent)

            if ent.x+ent.radius > self.x+self.width/2:

                if ent.y-ent.radius < self.y+self.height/2:

                    self.content[1].add_entity(ent)

                if ent.y+ent.radius > self.y+self.height/2:

                    self.content[3].add_entity(ent)

        else:  # just putting in square where circle center is

            if ent.x < self.x+self.width/2:

                if ent.y < self.y+self.height/2:

                    self.content[0].add_entity(ent)

                else:

                    self.content[2].add_entity(ent)

            else:

                if ent.y < self.y+self.height/2:

                    self.content[1].add_entity(ent)

                else:

                    self.content[3].add_entity(ent)

    def get_colliding_entities(self, couple=0, colliding_func=0):

        if self.subdivided:

            to_return = []

            for baby_tree in self.content:

                to_return += baby_tree.get_colliding_entities(couple)

            return to_return

        else:

            # ABC : A-C, A-B, B-C

            colliding = []

            for x1 in range(len(self.content)-1):

                for x2 in range(len(self.content)-1, x1, -1):

                    pos1 = [self.content[x1].x, self.content[x1].y]

                    rad1 = self.content[x1].radius

                    pos2 = [self.content[x2].x, self.content[x2].y]

                    rad2 = self.content[x2].radius

                    if colliding_func:

                        collision_test = get_distance(pos1, pos2) < big_rad

                    else:

                        collision_test = collide_circle_to_circle(pos1, rad1, pos2, rad1)

                    if collision_test:

                        if couple:

                            colliding.append([self.content[x1], self.content[x2]])

                        else:

                            colliding.append(self.content[x1])

                            colliding.append(self.content[x2])

            return colliding

    def agario_collisions_and_closest(self, couple=0, colliding_func=0):

        if self.subdivided:

            to_return = []

            for baby_tree in self.content:

                to_return += baby_tree.agario_collisions_and_closest(couple=couple, colliding_func=colliding_func)

            return to_return

        else:

            # ABC : A-C, A-B, B-C

            colliding = []

            for x1 in range(len(self.content)):

                min_dist = 1000

                for x2 in range(len(self.content)-1, x1, -1):

                    pos1 = [self.content[x1].x, self.content[x1].y]

                    rad1 = self.content[x1].radius

                    pos2 = [self.content[x2].x, self.content[x2].y]

                    rad2 = self.content[x2].radius

                    this_dist = get_distance(pos1, pos2)

                    # sets future input for neural network to see closest entity to itself
                    if (self.content[x1].radius > 10) and (this_dist < min_dist):  # it's a moving entity, and needs to get it's closest dot updated

                        self.content[x1].neural_input = [pos1[0]-pos2[0], pos1[1]-pos2[1], get_sign_zero(rad2-rad1)]

                        min_dist = this_dist

                    if not x1 == len(self.content)-1:  # last one doesn't need to check collisions, just update closest

                        # checking collision
                        if colliding_func == 1:

                            collision_test = this_dist < max(self.content[x1].radius, self.content[x2].radius)

                        elif colliding_func == 2:

                            if ((self.content[x1].sick == 1) and not (self.content[x2].sick)):

                                collision_test = this_dist < self.content[x1].sick_radius+self.content[x2].radius

                            elif ((not(self.content[x1].sick)) and (self.content[x2].sick == 1)):

                                collision_test = this_dist < self.content[x2].sick_radius+self.content[x1].radius

                            else:

                                collision_test = 0

                        else:

                            collision_test = collide_circle_to_circle(pos1, rad1, pos2, rad1)

                        if collision_test:

                            if couple:

                                colliding.append([self.content[x1], self.content[x2]])

                            else:

                                colliding.append(self.content[x1])

                                colliding.append(self.content[x2])

            return colliding

    def get_branches_content(self):
        """ function that probably shouldn't exist anyway [yes it's useless], returns each group of entities (in most subdivided part of tree) contained in the tree """

        if self.subdivided:

            to_return = []

            for baby_tree in self.content:

                babe_content = baby_tree.get_branches_content()

                to_return.append()

            return to_return

        else:

            return self.content

def test_quad_tree():

    play = True

    clicking = 0

    rand_pop = [DotCenter(random.randint(0, screen_width), random.randint(0, screen_height), 5) for x in range(20)]

    while play:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                play = False

        tree = QuadTree(0, 0, screen_width, screen_height)

        screen.fill(WHITE)

        for dot in rand_pop:

            dot.update(get_normalized_vector(sum_arrays([dot.x, dot.y], pygame.mouse.get_pos(), -1, 1), 1))

            tree.add_entity(dot)

        tree.draw()

        colliding = tree.get_colliding_entities()

        for dot in rand_pop:

            if not dot in colliding:

                dot.draw()

            else:

                dot.draw(RED)

        pygame.display.update()

        clock.tick(60)

def get_random_edge_coor(max_x, max_y, min_x=0, min_y=0):

    if random.randint(0, 1):

        if random.randint(0, 1):

            x = random.randint(min_x, max_x)

            y = min_y

        else:

            x = random.randint(min_x, max_x)

            y = max_y
    else:

        if random.randint(0, 1):

            x = min_x

            y = random.randint(min_y, max_y)

        else:

            x = max_x

            y = random.randint(min_y, max_y)

    return [x, y]


def test_edge_repartition():

    for x in range(999):

        pygame.draw.circle(screen, RED, get_random_edge_coor(screen_width, screen_height), 20)

    pygame.display.update()


def get_rect_center(rect):

    return [rect[0]+rect[2]//2, rect[1]+rect[3]//2]


def format_rect(rect):

    if rect[2] < 0:  # width < 0; x coor is x-width

        rect[0] = rect[0]+rect[2]

        rect[2] = -rect[2]

    if rect[3] < 0:  # height < 0; y coor is y-height

        rect[1] = rect[1]+rect[3]

        rect[3] = -rect[3]

    return rect


def get_lines_of_rect(rect):

    A = [rect[0], rect[1]]

    B = [rect[0]+rect[2], rect[1]]

    C = [rect[0], rect[1]+rect[3]]

    D = [rect[0]+rect[2], rect[1]+rect[3]]

    return [A, B], [A, C], [B, D], [C, D]


def get_distance(p1, p2):

    return sqrt((p2[0]-p1[0])**2+(p2[1]-p1[1])**2)


def collide_circle_to_circle(pos1, rad1, pos2, rad2):

    dist = get_distance(pos1, pos2)

    max_dist_to_touch = (rad1 + rad2)

    if dist < max_dist_to_touch:  # distance between the two circles lesser than their combined radius

        return 1


def collide_line_to_circle(circle_pos, circ_rad, droite):
    """ checking if circle colliding line have solutions

    returns intersection pts or empty array

    circle_equation : (x-a)**2 + (y-b)**2 = r**2

    line_equation : ax + by + c = 0  """

    m, p = droite

    if m == []:  # ligne verticale

        if p == circle_pos[0]-circ_rad:

            return [p, circle_pos[1]]

        elif p == circle_pos[0]+circ_rad:

            return [p, circle_pos[1]]

        elif val_in_array(p, [circle_pos[0]-circ_rad, circle_pos[0]+circ_rad]):

            diff = (circ_rad)**2-((p-circle_pos[0])**2)

            return [[p, sqrt(diff)+circle_pos[0]], [p, -(sqrt(diff)+circle_pos[0])]]

        return []

    ca, cb = circle_pos

    a = 1+m**2

    b = -2*ca + 2*m*p - 2*cb*m

    c = -2*cb*p + cb**2 + ca**2 + p**2 - circ_rad**2

    delta = (b**2) - (4*a*c)

    if delta > 0:

        x1 = (-b-sqrt(delta))/(2*a)

        x2 = (-b+sqrt(delta))/(2*a)

        return [[x1, m*x1+p], [x2, m*x2+p]]

    elif delta == 0:

        x = -b/(2*a)

        return [[x, m*x+p]]

    return []


def collide_segment_to_circle(circ_pos, circ_rad, segment):
    """
    segment is two points

    first checking if circle colliding line have solutions, if yes, checks that point of line is on segment 

    circle_equation : (x-a)**2 + (y-b)**2 = r**2

    line_equation : ax + by + c = 0  """

    line = get_droite_from_pt(segment[0], segment[1])  # equation de droite du segment en question

    points = collide_line_to_circle(circ_pos, circ_rad, line)

    if points == []:

        return  # returns false

    for x in range(len(points)-1, -1, -1):

        point = points[x]

        if not collide_point_on_line_to_segment(point, segment):

            points.remove(point)

    return points

def collide_point_to_rect(point, rect):

    return val_in_array(point[0], [rect[0], rect[0]+rect[2]]) and val_in_array(point[1], [rect[1], rect[1]+rect[3]])


def collide_point_on_line_to_segment(point, segment):
    """ returns True if a given point (which is on the segment line) is on that segment """

    return val_in_array(point[0], [segment[0][0], segment[1][0]]) and val_in_array(point[1], [segment[0][1], segment[1][1]])


def segment_in_rect(segment, rect):

    if (collide_point_to_rect(segment[0], rect) and collide_point_to_rect(segment[1], rect)):

        return True

    for colliding_pt in collide_rect_to_line(segment[0], get_droite_from_pt(segment[0], segment[1]), rect):

        if collide_point_on_line_to_segment(colliding_pt, segment):

            return True


def collide_rect_to_demi_droite(rect, start_pos, line):

    inter_points = collide_rect_to_line(start_pos, line, rect)

    for pt in inter_points:

        if pt[0] >= start_pos[0]*line[0]:

            return pt

def collide_rect_to_line(start_pos, line, rect):
    """ returns if line[m, p] and rect[x, y, width, height] are colliding ; """

    A = [rect[0], rect[1]]

    B = [rect[0]+rect[2], rect[1]]

    C = [rect[0], rect[1]+rect[3]]

    D = [rect[0]+rect[2], rect[1]+rect[3]]

    line_1 = [A, B]

    line_2 = [B, D]

    line_3 = [A, C]

    line_4 = [C, D]

    rect_sides = [line_1, line_2, line_3, line_4]

    results = []

    for rect_side in rect_sides:

        inter_point = get_inter_from_droite(get_droite_from_pt(rect_side[0], rect_side[1]), line)

        if inter_point == True:

            #print("droite et cote du rectangle confondus...")

            results.append(rect_side[0])

            results.append(rect_side[1])

        elif inter_point:

            if line[0] == []:

                inter_point = [inter_point, rect_side[0][1]]  # is ordonne du rectangle si droite est une verticale

            else:

                inter_point = [inter_point, line[0]*inter_point+line[1]]

            if val_in_array(inter_point[0], [rect_side[0][0], rect_side[1][0]]) and val_in_array(inter_point[1], [rect_side[0][1], rect_side[1][1]]) :

                results.append(inter_point)

    return results  # .sort(key=lambda x:x*get_sign(liste[0]))[0]


def collide_segment_to_segment(seg1, seg2):

    line1 = get_droite_from_pt(seg1[0], seg1[1])

    line2 = get_droite_from_pt(seg2[0], seg2[1])

    inter_point = get_inter_from_droite(line1, line2)

    if inter_point == True:  # not the problem

        return seg1[0]

    elif inter_point:

        if line1[0] == []:

            if line2[0] == []:

                return seg1[0]

            else:

                inter_point = [inter_point, line2[0]*inter_point+line2[1]]  # is ordonne du rectangle si droite est une verticale

        else:

            inter_point = [round(inter_point, 5), round(line1[0]*inter_point+line1[1], 5)]

        if (collide_point_on_line_to_segment(inter_point, seg1)) and (collide_point_on_line_to_segment(inter_point, seg2)):

            return inter_point


def collide_segment_to_segments(segment, segments):

    line = get_droite_from_pt(segment[0], segment[1])

    results = []

    for seg in segments:

        inter_point = get_inter_from_droite(get_droite_from_pt(seg[0], seg[1]), line)

        if inter_point == True:

            #print("droite et cote du rectangle confondus...")

            results.append(min(seg[0], seg[1]))

            #results.append(seg[1])

        elif inter_point:

            inter_point = [inter_point, line[0]*inter_point+line[1]]

            if val_in_array(inter_point[0], [seg[0][0], seg[1][0]]) and val_in_array(inter_point[1], [seg[0][1], seg[1][1]]):

                if val_in_array(inter_point[0], [segment[0][0], segment[1][0]]) and val_in_array(inter_point[1], [segment[0][1], segment[1][1]]):

                    results.append(inter_point)

    return results


def collide_circle_to_rect(pos, rad, rect):  # pos[x, y]
    """ rect : [x, y, width, height] ; this function detects if a circle collides a rectangle; returns 1 if collides on xline, 2 if collides on yline, 3 if a mix of the txo (arriving in corner), None else """

    # puts rectangle to normal format

    print_help = 0

    rect = format_rect(rect)

    if pos[0] < rect[0]:  # The x coordinate of the circle is lesser than the left side of the rectangle -> closest x of rect from pos[0] (x centre of circle) is rect[0]
        # now searching closest y
        if pos[1] < rect[1]:  # rect[1] is closest in y to pos[1]

            dist = sqrt((rect[0]-pos[0])**2 + (rect[1]-pos[1])**2)

            if dist < rad:

                if print_help:

                    print(1, 3)

                return 2#3  # ball arriving in a corner (in that case left low corner) ; when used in some games often should not be interpreted as corner but horizontal part

        elif pos[1] > rect[1]+rect[3]:  # rect[1]+rect[3] (y coor of rect + its width) is closest in y

            dist = sqrt((rect[0]-pos[0])**2 + (rect[1]+rect[3]-pos[1])**2)

            if dist < rad:

                if print_help:

                    print(2, 3)

                return 3  # left up corner

        else:  # closest is pos[1] : don't have to substract in y

            dist = abs(rect[0]-pos[0])

            if dist < rad:

                if print_help:

                    print(3, 1)

                return 1  # ball ariving in the retangle from the left -> should switch (*-1) the x coor of the vector

    elif pos[0] > rect[0]+rect[2]:  # x coor of circle is bigger than x coor of rect + its width
        # now searching closest y
        if pos[1] < rect[1]:  # rect[1] is closest in y

            dist = sqrt((rect[0]+rect[2]-pos[0])**2 + (rect[1]-pos[1])**2)

            if dist < rad:

                if print_help:

                    print(4, 3)

                return 2#3  when used in some games often should not be interpreted as corner but horizontal part

        elif pos[1] > rect[1]+rect[3]:  # rect[1]+rect[3] (y coor of rect + its width) is closest in y

            dist = sqrt((rect[0]+rect[2]-pos[0])**2 + (rect[1]+rect[3]-pos[1])**2)

            if dist < rad:

                if print_help:

                    print(5, 3)

                return 3

        else:  # closest is pos[1] : don't have to substract in y

            dist = abs(rect[0]+rect[2]-pos[0])

            if dist < rad:

                if print_help:

                    print(6, 1)

                return 1

    else:  # pos x of circle is in rect

        if pos[1] < rect[1]:  # the ball in under the rect (same x coordinates, y coors of ball < rect's one) -> rect[1] (lowest point of rect (y without the height) is closest in y

            dist = abs(rect[1]-pos[1])

            if dist < rad:

                if print_help:

                    print(7, 2)

                return 2

        elif pos[1] > rect[1]+rect[3]:  # rect[1]+rect[3] (y coor of rect + its width) is closest in y

            dist = abs(rect[1]+rect[3]-pos[1])

            if dist < rad:

                if print_help:

                    print(8, 2)

                return 2

        else:  # the ball is in rect (left_rect<x_ball<right_rect, down_rect<y_ball<up_rect)

            if min((pos[0]-rect[0])/rect[2], 1-(pos[0]-rect[0])/rect[2]) < min((pos[1]-rect[1])/rect[3], 1-(pos[1]-rect[1])/rect[3]):

                if print_help:

                    print(9, 1)

                return 1

            else:

                if print_help:

                    print(10, 2)

                return 2


def collide_rect_to_rect(rect1, rect2):
    """ Functions that checks wheter to rectangles are colliding ; rect format is [left corner x, y, width, height] """

    rect1 = format_rect(rect1)

    rect2 = format_rect(rect2)

    if ((rect1[0]<=rect2[0]<=rect1[0]+rect1[2]) and (rect1[1]<=rect2[1]<=rect1[1]+rect1[3])) or ((rect1[0]<=rect2[0]+rect2[2]<=rect1[0]+rect1[2]) and (rect1[1]<=rect2[1]<=rect1[1]+rect1[3])) or ((rect1[0]<=rect2[0]<=rect1[0]+rect1[2]) and (rect1[1]<=rect2[1]+rect2[3]<=rect1[1]+rect1[3])) or ((rect1[0]<=rect2[0]+rect2[2]<=rect1[0]+rect1[2]) and (rect1[1]<=rect2[1]+rect2[3]<=rect1[1]+rect1[3])):

        return True


def collide_pt_on_line_to_half_line(pt, half_line):
    """ halfine is defined as half_line[seg_pt, line_pt) """

    x_diff = get_sign(half_line[0][0]-half_line[1][0])

    y_diff = get_sign(half_line[0][1]-half_line[1][1])

    pt_to_seg_end_x_diff = half_line[0][0]-pt[0]

    pt_to_seg_end_y_diff = half_line[0][1]-pt[1]

    condition_x = (not pt_to_seg_end_x_diff) or (get_sign(pt_to_seg_end_x_diff) == x_diff)  # point is on the segment end (so ok) or in the good direction (sens)

    condition_y = (not pt_to_seg_end_y_diff) or (get_sign(pt_to_seg_end_y_diff) == y_diff)

    return condition_x and condition_y


def collide_point_polygon(pt, polygon):
    """ Functions that returns wether a polygon (array of points) collides a pt """

    # defining polygon sides

    sides = []

    for x in range(len(polygon)):

        last_index = (x+2)%(len(polygon)+1)

        if not last_index:  # have to add last and first of the array

            sides.append([polygon[-1], polygon[0]])

        else:

            sides.append(polygon[x:last_index])

    # definig the polygon center (average of points)
    sum_x = 0

    sum_y = 0

    for x in polygon:

        sum_x += x[0]

        sum_y += x[1]

    # will first check if polygon center is in the polygon

    polygon_center = [sum_x//len(polygon), sum_y//len(polygon)]

    #pygame.draw.circle(screen, YELLOW, polygon_center, 25)

    # looks for the longest side

    side_lengths = [get_distance(x[0], x[1]) for x in sides]

    longest_side = sides[side_lengths.index(max(side_lengths))]

    testing_pt = get_milieu_droite(longest_side[0], longest_side[1])

    center_to_test_pt = get_droite_from_pt(polygon_center, testing_pt)  # line between polygon center and middle between two summits

    collisions = 0

    for index in range(len(sides)):

        cur_side = sides[index]

        #pygame.draw.line(screen, RED, cur_side[0], cur_side[1], 3)

        #pygame.draw.line(screen, RED, polygon_center, testing_pt, 3)

        side_line = get_droite_from_pt(cur_side[0], cur_side[1])

        collision_pt = get_inter_from_droite(side_line, center_to_test_pt, full_pt=1)

        collision_pt = [round(collision_pt[0], 2), round(collision_pt[1], 2)]

        if collision_pt and collide_point_on_line_to_segment(collision_pt, cur_side):  # side colliding

            #pygame.draw.circle(screen, YELLOW, (int(collision_pt[0]), int(collision_pt[1])), 20)

            if collide_pt_on_line_to_half_line(collision_pt, [polygon_center, testing_pt]):  # now checking if point collding with half line (sommet-center]

                collisions += 1

        #pygame.display.update()

    center_in = (collisions % 2==1)*1

    #print(collisions, center_in)

    # now checks how much collisions there are between the unknown point and center (that we now if it's in or out) segment and each side of the polygon, to count the number of times it goes in or out

    center_unknown_pt_seg = [polygon_center, pt]

    center_unknown_pt_line = get_droite_from_pt(center_unknown_pt_seg[0], center_unknown_pt_seg[1])

    in_out = 0

    for index in range(len(sides)):

        cur_side = sides[index]

        side_line = get_droite_from_pt(cur_side[0], cur_side[1])

        collision_pt = get_inter_from_droite(side_line, center_unknown_pt_line, full_pt=1)

        if collision_pt:

            collision_pt = [round(collision_pt[0], 2), round(collision_pt[1], 2)]

            if collide_point_on_line_to_segment(collision_pt, cur_side) and collide_point_on_line_to_segment(collision_pt, center_unknown_pt_seg):

                in_out += 1

    return (in_out%2 == 0)


def test_polygon_collision():

    test = 1

    if test == 1:

        screen.fill(BLACK)

        polygon_pt = []

        for x in range(random.randint(3, 4)):

            polygon_pt.append([random.randint(0, screen_width), random.randint(0, screen_height)])

        unknown_pt = DotCenter(random.randint(0, screen_width), random.randint(0, screen_height))

        play = True

        while play:

            for event in pygame.event.get():

                if event.type == pygame.QUIT:

                    play = False

            unknown_pt.update(get_vector_to_point([unknown_pt.x, unknown_pt.y], pygame.mouse.get_pos(), 1))

            if collide_point_polygon([unknown_pt.x, unknown_pt.y], polygon_pt):

                color = RED

            else:

                color = GREEN

            screen.fill(BLACK)

            pygame.draw.polygon(screen, GREY, polygon_pt)

            pygame.draw.circle(screen, color, [int(unknown_pt.x), int(unknown_pt.y)], 5)

            pygame.display.update()

    elif test == 2:

        polygon_pt = []

        for x in range(random.randint(30, 40)):

            polygon_pt.append([random.randint(0, screen_width//2), random.randint(0, screen_height)])

        # draws polygon on screen left
        screen.fill(BLACK)

        pygame.draw.polygon(screen, GREY, polygon_pt)

        pygame.display.update()

        # draws all pixel ,on right of screen, red if collidingg polyogn, green else

        a = time.time()

        for y in range(screen_height):

            for x in range(screen_width//2):

                for event in pygame.event.get():

                    if event.type == pygame.QUIT:

                        return

                if collide_point_polygon([x, y], polygon_pt):

                    color = RED

                else:

                    color = GREEN

                screen.set_at((x+screen_width//2, y), color)

            pygame.display.update()

        pygame.display.update()

        print(time.time()-a)

    wait()


def get_area_triangle(pt1, pt2=None, pt3=None):
    """ expects three Arr pts, returns area, with the technique area = base*hauteur """

    if pt2 == None:

        pt1, pt2, pt3 = pt1

    base = pt2-pt1

    base_normee = (base*(1/base.norme_eucli()))

    projete = pt1+base_normee*Arr.p_s(pt3, base_normee)

    hauteur = pt3-projete

    return (base.norme_eucli()*hauteur.norme_eucli())/2


def test_area_triangle():

    a, b, c = Arr([0, 0]), Arr([1, 0]), Arr([0, 1])

    print(get_area_triangle(a, b, c))

    print(get_area_triangle(Arr([0, 0]), Arr([1, 0]), Arr([0.5, 1])))

    for x in range(10):

        d = Arr([0.01*x, 0.1])

        s1, s2, s3 = get_area_triangle(a, b, d), get_area_triangle(a, d, c), get_area_triangle(d, b, c)

        print(s1+s2+s3)  # s1, (a, b, d), s2, (a, d, c), s3, (d, b, c), 


def collide_vect_to_line(vect, pos, line):
    """ returns the new vector when an entity with a vector has collided into a line (wall..) """

    #tail of the vect, pos is the intesection vector-line
    pos2 = sum_arrays(pos, vect, 1, -1)

    # creates a rectangle triangle
    first_perp = get_perpendiculaire_from_d(line, pos2)

    # is the intersection between the perpendicular to the line and the line, point that we need is symetric of this pt with pos
    inter_perp_droite = get_inter_from_droite(line, first_perp, full_pt=1)

    move_vect = sum_arrays(pos, inter_perp_droite, 1, -1)

    symetrical_pt = sum_arrays(pos, move_vect)

    # gets the line where the final point is lying
    n_inter_perp_droite = get_perpendiculaire_from_d(line, symetrical_pt)

    perp_to_tale_vect = sum_arrays(pos2, inter_perp_droite, 1, -1)

    final_point = sum_arrays(symetrical_pt, perp_to_tale_vect)

    final_vect = sum_arrays(final_point, pos, 1, -1)

    return final_vect


def collide_circle_to_triangle(pos_c, rad, pt1, pt2, pt3):
    """ Function that detects collisions between a circle and any triangle defined by three points. First computes in which zone the circle is : zone 1 or zone2 (hard to explain without a drawing) """
    pass


def deal_with_collisions(x, y, rad, rectangles=[], circles=[], triangles=[]):
    """ Deals with collisions for a ball(circle) ; returns 2 if collides some horizontal plain(floor, roof ..), or 1 if vertical (as a wall), None for nothing ofc """

    collisions = []

    for rect in rectangles:

        collision = collide_circle_to_rect((x, y), rad, rect)

        if collision:

            collisions.append(collision)

    return collisions


def circle_out_rect(dot, rect):
    """ checks if circle collides with line (therefore single value) ; returns 1 if colliding left, returns 2 if colliding right, returns 3 if colliding up, returns 4 if colliding down (line of the rect) """

    circle_y_array = [dot.y-dot.radius, dot.y+dot.radius]

    circle_x_array = [dot.x-dot.radius, dot.x+dot.radius]

    to_return = []

    if colliding_arrays(circle_x_array, [rect[0], rect[0]]):

        to_return.append(1)

    elif colliding_arrays(circle_x_array, [rect[0]+rect[2], rect[0]+rect[2]]):

        to_return.append(2)

    if colliding_arrays(circle_y_array, [rect[1], rect[1]]):

        to_return.append(3)

    elif colliding_arrays(circle_y_array, [rect[1]+rect[3], rect[1]+rect[3]]):

        to_return.append(4)

    return to_return



## Stuff about lines


def shrink_line(line, shrink_ratio=4):

    middle_x = (line[0][0]+line[1][0])//2

    middle_y = (line[0][1]+line[1][1])//2

    ecart_x = abs(line[0][0]-line[1][0])

    ecart_y = abs(line[0][1]-line[1][1])

    return [[middle_x-ecart_x/shrink_ratio, middle_y-ecart_y/shrink_ratio], [middle_x+ecart_x/shrink_ratio, middle_y+ecart_y/shrink_ratio]]


def shrink_rect(rect, shrink_ratio=4):

    pygame.draw.rect(screen, WHITE, pygame.Rect(rect[0], rect[1],rect[2], rect[3]))

    lines = get_lines_of_rect(rect)

    line1 = shrink_line(lines[0], shrink_ratio=4)

    line2 = shrink_line(lines[1], shrink_ratio=4)

    line3 = shrink_line([line1[1], [line1[1][0], line2[1][0]]], shrink_ratio=4)

    line4 = shrink_line([line2[1], [line1[1][0], line2[1][1]]], shrink_ratio=4)

    lines = [line1, line2, line3, line4]

    for x in range(4):

        pygame.draw.line(screen, RED, lines[x][0], lines[x][1])

    pygame.display.update()

    return lines


def get_random_line(m_borne=[-4, 4], p_borne=[-100, 600]):

    m = (random.randint(m_borne[0]*10, m_borne[1]*10)/10) or 0.01

    return [m, random.randint(p_borne[0], p_borne[1])]


def get_droite_from_pt(pt1, pt2):
    """ retourne le coefficient directeur et l'ordonnee a l'origine d'une fonction abscisse grace a deux de ses points """

    if not (pt1[0]-pt2[0]):  # droite verticale

        return [[], pt1[0]]

    m = (pt1[1]-pt2[1])/(pt1[0]-pt2[0])

    p = -(pt1[0]*m)+pt1[1]#1 - m

    return [m, p]


def get_line_steps(line, point, steps=1):

    if line[0] == 0:

        return [point[0]+steps, point[1]]

    elif line[0] == []:

        return [point[0], point[1]+steps]

    else:

        x_step = steps/(abs(line[0])+1)

        y_step = x_step*line[0]

        if line[0] < 0:

           x_step, y_step = x_step *-1, y_step *-1

        #print(x_step, y_step, steps)

        return [point[0]+x_step, point[1]+y_step]


def get_milieu_droite(pt1, pt2):

    return [(pt1[0]+pt2[0])/2, (pt1[1]+pt2[1])/2]


def get_inter_from_droite(d1, d2, full_pt=0):
    """
        renvoie point d'intersection de deux droites,
        d est une equation reduite de droite
        (sous la forme y=mx+p ; d=[m, p], donc d[0]:pente, d[1]:ordonnee a l'origine)
        full point est une option permet d'obtenir un point (x, y), par defaut renvoie seulement x """

    if d1[0] == d2[0]:

        if d1[1] == d2[1]:  # else no solution, returns None

            #print("droites confondues")
            return True  # ?? (shouldn't arise anyway)

    elif (d1[0] == []):  # droite verticale

        if full_pt == 1:

            return [d1[1], d2[0]*d1[1]+d2[1]]

        return d1[1]

    elif (d2[0] == []):  # droite verticale

        if full_pt == 1:

            return [d2[1], d1[0]*d2[1]+d1[1]]

        return d2[1]

    else:

        x = (-d1[1]+d2[1])/(d1[0]-d2[0])

        if full_pt == 1:

            return [x, d1[0]*x+d1[1]]

        return x


def get_perpendiculaire_from_d(droite, point):
    """ returns the perpendicular line going through a point given a line and the point (m, p, with y=mx+p) """

    m, p = droite

    if m == []:

        return [0, point[1]]

    if m == 0:

        m = 0.001

    nm = -1/m

    np = point[1]-(nm*point[0])

    return nm, np


def pt_between_lines(pt, line1, line2):
    """ returns 0 if under line 1, 1 if between line 1 and 2, 2 if higher than line2 (or equal) ; lines should be sorted, don't have much sense if not parallel """

    x, y = pt

    m1, p1 = line1

    m2, p2 = line2

    if p1 + m1*x > y:  # point under the line 1

        return 0

    if p2 + m2*x < y:  # point higher than line 2

        return 2

    return 1


def get_rects_colliding_line_with_direction(start_pos, line, rects_to_chk, vect_sign):
    """ returns a sorted array of all rects among (rects input) colliding a line going in a direction, sorted by order of collision """

    found_rects = []

    for rect in rects_to_chk:

        current_rect_colliding_points = collide_rect_to_line(start_pos, line, rect)

        found = 0

        for colliding_point in current_rect_colliding_points:

            if vect_sign==-1:

                print(get_sign(colliding_point[0]-start_pos[0]), )

            if (not found) and (get_sign(colliding_point[0]-start_pos[0])==vect_sign) and (get_sign(colliding_point[1]-start_pos[1])==vect_sign):

                found_rects.append(rect)

                found = 1

    return sorted(found_rects, key=lambda x:x*vect_sign)


## end geometrical functions

# string/letters function

def shift_string(string, shift):

    n_string = ""

    for car in string:

        n_string += abc[(abc.index(car)+shift)%26]

    return n_string


def try_all_combinations(string):

    for x in range(26):

        print(shift_string(string, x))



# genetic algorithms -> evolving randomly created population to fit a goal

class Population:

    def __init__(self, pop, parent_nb, mutation_rate, app_function_point):

        self.pop = pop.copy()

        self.parent_nb = parent_nb

        self.mutation_rate = mutation_rate  # round(1 / mutation_rate)  # to be able to chose with random.randint(0, mutation rate)

        self.app_function_point = app_function_point

    def evaluate(self):

        worst_entity = min(self.pop, key=lambda x:x.points)

        worst_points = worst_entity.points

        pop_points = [self.app_function_point(x.points-worst_points) for x in self.pop]

        total_points = sum(pop_points)

        if total_points == 0:

            return -1  # bad pop

        else:

            for entit in self.pop:

                entit.points = self.app_function_point(entit.points-worst_points) / total_points

    def get_randomly_selected_item_in_weighted_list(weight_list):

        rmoderateur = random.randint(0, 1000) / 1000

        compteur = -1

        choix = None

        while choix == None:

            compteur +=1

            try:

                rmoderateur -= weight_list[compteur]

                if rmoderateur <= 0:

                    choix = compteur

            except:  # shouldn't arise as long as sum of weight list bigger than one (in fact should precisely match one)

                choix = -1  # takes last one

        return choix

    def evolve(self):

        weight_list = [x.points for x in self.pop]

        to_add_entities = 0

        #print(sorted(weight_list)[-10:])

        for index in range(len(weight_list)-1, -1, -1):

            if weight_list[index] == 0:

                del weight_list[index]

                del self.pop[index]

                to_add_entities += 1

        # keeps the best bird from a generation to the next one

        best_index = weight_list.index(max(weight_list))

        n_pop = [self.pop[best_index].copy()]

        # loop generating new entities

        for index in range(len(self.pop)-1):

            if self.parent_nb > 1:  # select several parents and merge them into the new entity

                parents = []

                for x in range(self.parent_nb):

                    parent_index = Population.get_randomly_selected_item_in_weighted_list(weight_list)

                    parents.append(self.pop[parent_index])

                n_entit = merge(perents)

            else:  # 

                parent_index = Population.get_randomly_selected_item_in_weighted_list(weight_list)

                n_entit = self.pop[parent_index].copy()

            # big tweak in one parametr (small chances)

            if not random.randint(0, self.mutation_rate):

                n_entit.mutate(0.4)

            # small tweak in one parametr (high chances)

            elif random.randint(0, self.mutation_rate):

                n_entit.mutate(0.04)

            n_pop.append(n_entit)

        # replaces worst creatures of each generation by mutated best creature

        for index in range(to_add_entities):

            n_entity = self.pop[best_index].copy()

            for x in range(5):

                n_entity.mutate(0.1)

            n_pop.append(n_entity)

        self.pop = n_pop

##        for x in n_pop:
##
##            print(x, x.brain.weights, x.points)



# Pygame functions


def draw_test_circle(pos, color=(255, 0, 0)):

    x, y = pos

    pygame.draw.circle(screen, color, [int(x), int(y)], 10)


class Drawing:

    def __init__(self, screen, screen_width, screen_height):

        self.screen = screen

        self.screen_width = screen_width

        self.screen_height = screen_height

        self.list = []

    def get_coor(self, drawing_color):

        for y in range(self.screen_height):

            for x in range(self.screen_width):

                pix_color = self.screen.get_at((x, y))

                if pix_color == drawing_color:

                    self.list.append((x, y))


def load_picture(path, width=0, height=0):

    try:

        image = pygame.image.load("pictures/"+path)

    except pygame.error:

        return -1

    if width or height:

        image = pygame.transform.scale(image, (int(width), int(height)))

    return image


def get_random_point_in_screen():

    return [random.randint(0, screen_width), random.randint(0, screen_height)]


def get_pygame_rect(rect):

    return pygame.Rect(rect[0], rect[1], rect[2], rect[3])


def set_pause():

    panneau_play = Panneau("", screen_width//2-300, 300, 200, 200, color=GREY, image=draw_play, image_coors=[100, 100])

    panneau_quit = Panneau("", screen_width//2+100, 300, 200, 200, color=GREY, image=draw_quit, image_coors=[72, 70])

    choix = 0

    while choix == 0:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                choix = 1

                return 1

            elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):

                mouse_pos = pygame.mouse.get_pos()

                if panneau_play.clicked(mouse_pos):

                    choix = 1

                    return

                if panneau_quit.clicked(mouse_pos):

                    choix = 1

                    return 1

            screen.fill(BROWN)

            panneau_play.draw()

            panneau_quit.draw()

            pygame.display.update()

class DotCenter:
    """ A dot entity that moves quiet randomly but doesn't get too far of the center, and never leaves screen """

    def __init__(self, x, y, radius=1):

        self.x = x

        self.y = y

        self.radius = radius

        self.vector = [0, 0]

        self.color = BLUE

        self.compteur = 0

    def update(self, vector=0):

        self.compteur += 1

        self.color = BLUE

        if not vector:  # called with no special vector

            if not random.randint(0, 60):  # sometimes changes the vector to make the "random" walk

                if get_distance([self.x, self.y], [screen_width//2, screen_height//2]) > 400:  # if too far from center stears back

                    self.vector = get_vector_to_point([self.x, self.y], [screen_width//2, screen_height//2], 1)

                else:

                    self.vector = get_random_vector()

        else:  # applies the vector that has been ordered

            self.vector = vector

        self.x += self.vector[0]

        self.y += self.vector[1]

    def draw(self, color=(0, 0, 255)):

        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), self.radius)


class Menu:

    def __init__(self, x_pos, y_pos, width, height, box_nb, box_strings, box_margin=10, box_width=200, box_height=100, color=[255, 255, 255], vertical=0):
        """ grid entities (obstacles, player defenses..) """

        self.box_margin = box_margin

        self.box_width = box_width

        self.box_height = box_height

        self.box_strings = box_strings

        self.pyg_rect = pygame.Rect(x_pos, y_pos, width, height)

        self.menu_frame = Panneau("", self.pyg_rect[0], self.pyg_rect[1], self.pyg_rect[2], self.pyg_rect[3])

        self.vertical = vertical

        if vertical:

            self.available_box_nb = (self.pyg_rect[3]-2*self.box_margin)//(self.box_height+self.box_margin)

        else:

            self.available_box_nb = (self.pyg_rect[2]-2*self.box_margin)//(self.box_width+self.box_margin)

        self.arrow_size = 8

        self.page = 0  # current page (part of all options currently displayed on screen)

        self.page_nb = ceil(len(self.box_strings)/(self.available_box_nb-2))  # total page nb

        self.curr_boxes = []

        self.box_x = self.menu_frame.x+self.box_margin

        self.box_y = self.menu_frame.y+self.box_margin

        loop_nb = min(self.available_box_nb-2, len(self.box_strings)-1)  # if there is more available boxes than the number of boxes to display ; -2 for arrow buttons

        Menu.define_curr_boxes(self, 0)

        self.color = color

    def define_curr_boxes(self, first_index):
        """ defining current buttons of menu (all can't be displayed because of place available on screen)"""

        self.curr_boxes = []

        loop_nb = min(self.available_box_nb-2, len(self.box_strings[first_index:]))  # if there is more available boxes than the number of boxes to display (+2 arrow buttons)

        compteur = first_index

        for x in range(1, loop_nb+1):  # index is one further because of first arrow button

            # defining the button ; differences between arrow buttons and buying buttons

            if self.vertical:

                box_y = self.box_y + x*(self.box_margin+self.box_height)

                box = Panneau(self.box_strings[compteur], self.box_x, box_y, self.box_width, self.box_height, y_focus=-15)  # buy box, the string (self.options[x]) is the description of the article

            else:

                box_x = self.box_x + x*(self.box_margin+self.box_width)

                box = Panneau(self.box_strings[compteur], box_x, self.box_y, self.box_width, self.box_height, y_focus=-15)  # buy box, the string (self.options[x]) is the description of the article

            self.curr_boxes.append(box)

            compteur += 1

        first_box = Panneau("", self.menu_frame.x+self.box_margin, self.box_y, self.box_width, self.box_height, image=draw_fleche_formatted, image_coors=[70, 25], image_args=[self.arrow_size, GREY, 1])

        if self.vertical:

            last_box = Panneau("", self.box_x, self.box_y+(self.available_box_nb-1)*(self.box_margin+self.box_height), self.box_width, self.box_height, image=draw_fleche_formatted, image_coors=[25, 35], image_args=[self.arrow_size*-1, GREY, 1])

        else:

            last_box = Panneau("",self.box_x+(self.available_box_nb-1)*(self.box_margin+self.box_width), self.box_y, self.box_width, self.box_height, image=draw_fleche_formatted, image_coors=[25, 35], image_args=[self.arrow_size*-1, GREY, 1])

        self.curr_boxes.insert(0, first_box)

        self.curr_boxes.append(last_box)

    def change_page(self, change_val):

        self.page = (self.page+change_val) % self.page_nb

        first_index = self.page*(self.available_box_nb-2)

        Menu.define_curr_boxes(self, first_index)

    def draw(self):

        self.menu_frame.draw()

        for box in self.curr_boxes:

            box.draw()

    def clicked(self, mouse_pos):

        for x in range(len(self.curr_boxes)):

            panneau = self.curr_boxes[x]

            if panneau.clicked(mouse_pos):

                if x == len(self.curr_boxes)-1:

                    Menu.change_page(self, 1)

                    return  # breaks loop, for curr_boxes has changed, and anyway job done

                elif x == 0:

                    Menu.change_page(self, -1)

                    return

                else:

                    return panneau.contenu



class Panneau:

    def __init__(self, contenu, x, y, largeur=200, hauteur=50, color=(255, 255, 255), font_size=30, image=0, image_coors=[0, 0], index=0, background=(0, 0, 0), x_focus=0, y_focus=0, adjust_width_to_text=0, image_args=0):

        self.largeur = largeur

        if adjust_width_to_text:

            self.largeur = 19*(len(contenu)+2)*(font_size/30)

        self.index = index

        self.x = x

        self.hauteur = hauteur

        self.y = y

        self.pyg_rect = pygame.Rect(self.x, self.y, self.largeur, self.hauteur)

        bordure = 5

        self.pyg_cadre = pygame.Rect(self.x+bordure, self.y+bordure, self.largeur-2*bordure, self.hauteur-2*bordure)

        self.contenu = contenu

        self.color = color

        self.font_size = font_size

        self.small_font = pygame.font.SysFont("monospace", 20, True)

        self.image = image

        self.image_coors = image_coors

        self.background = background

        self.x_focus = x_focus

        self.y_focus = y_focus

        self.image_args = image_args

    def update_pos(self, pos):

        self.x += pos[0]

        self.y += pos[1]

        self.pyg_rect = pygame.Rect(self.x, self.y, self.largeur, self.hauteur)

        bordure = 5

        self.pyg_cadre = pygame.Rect(self.x+bordure, self.y+bordure, self.largeur-2*bordure, self.hauteur-2*bordure)

    def update_dimensions(self, n_width, n_height):

        self.largeur = n_width

        self.hauteur = n_height

        self.pyg_rect = pygame.Rect(self.x, self.y, self.largeur, self.hauteur)

        bordure = 5

        self.pyg_cadre = pygame.Rect(self.x+bordure, self.y+bordure, self.largeur-2*bordure, self.hauteur-2*bordure)

    def draw(self, contenu_special=None, several_lines=None, sev_line_col=None):

        pygame.draw.rect(screen, self.background, self.pyg_rect)

        pygame.draw.rect(screen, self.color, self.pyg_cadre, 3)

        if contenu_special != None:

            txt = self.contenu+str(contenu_special)

            aff_txt(txt, self.x+15+self.x_focus, self.y+10+self.y_focus, self.color, taille=20)

        elif several_lines != None:

            if sev_line_col == None:

                sev_line_col = YELLOW

            for line in range(len(self.contenu)):

                if line == several_lines-1:

                    aff_txt(self.contenu[line], self.x+15+self.x_focus, self.y+10+line*15+self.y_focus, sev_line_col, taille=20, font=self.small_font)

                else:

                    aff_txt(self.contenu[line], self.x+15+self.x_focus, self.y+10+line*15+self.y_focus, self.color, taille=20, font=self.small_font)

        else:

            txt = self.contenu

            if (self.font_size != 30) and (self.font_size != 20):

                aff_txt(txt, self.x+20+self.x_focus, self.y+30+self.y_focus, self.color, 1, font=self.font_size)

            else:

                aff_txt(txt, self.x+20+self.x_focus, self.y+30+self.y_focus, self.color, self.font_size)

        if self.image:

            if not self.image_args:

                self.image(self.x, self.y, self.image_coors)

            else:

                self.image(self.x, self.y, self.image_coors, self.image_args)  # , self.image_coors

    def clicked(self, pos):
        """ Si le bouton est appuye, active la fonction """

        return (self.pyg_rect.collidepoint(pos))

    def reset_size(self, size_x, size_y=None):

        self.x -= size_x

        self.y -= size_y or size_x

        self.largeur += 2*size_x

        self.hauteur += 2*size_y or 2*size_x

        self.pyg_rect = pygame.Rect(self.x, self.y, self.largeur, self.hauteur)

        bordure = 5

        self.pyg_cadre = pygame.Rect(self.x+bordure, self.y+bordure, self.largeur-2*bordure, self.hauteur-2*bordure)


class ColorFrame(Panneau):
    """ at first designed for chess, to help the lacks of the traditionnal Panneau class """

    def __init__(self, x, y, width, height, color, image):

        Panneau.__init__(self, "", x, y, width, height, color=color)

        self.image = image

        self.pyg_frame = pygame.Rect(x, y, width, height)

    def draw(self):

        pygame.draw.rect(screen, self.color, self.pyg_frame)

        if self.image:

            screen.blit(self.image, (self.x, self.y))

        
class BoolButton(Panneau):

    def __init__(self, x, y, content, bool_value=0, width=30, height=30):

        self.x = x

        self.y = y

        self.content = content

        self.bool_value = bool_value

        self.width = width

        self.height = height

        self.pyg_rect = pygame.Rect(self.x, self.y, self.width, self.height)

        if content:

            self.content_frame = Panneau(self.content, self.x+2*self.width, self.y-10, y_focus=-25, adjust_width_to_text=1)

        else:

            self.content_frame = None

    def update_pos(self, pos):

        self.x += pos[0]

        self.y += pos[1]

        self.pyg_rect = pygame.Rect(self.x, self.y, self.width, self.height)

        if self.content_frame:

            self.content_frame.update_pos(pos)

    def draw(self):

        pygame.draw.rect(screen, BLACK, self.pyg_rect)

        pygame.draw.rect(screen, WHITE, self.pyg_rect, 3)

        if self.bool_value:

            draw_cross(self.x, self.y, [15, 15], 10)

        if self.content_frame:

            self.content_frame.draw()


class RadioButtons:

    def __init__(self, x, y, contents, bool_value=0, width=30, height=30, color=(0, 0, 0)):

        self.color = color

        self.anti_color = [(x-255)*-1 for x in color]

        self.x = x

        self.y = y

        self.contents = contents

        self.bool_value = bool_value

        self.width = width

        self.height = height

        self.pyg_rects = []

        self.content_frames = []

        self.texts = []

        x_spread = 100

        text_height = 30

        last_x = self.x

        margin = 10

        self.police_height = 30

        self.biggest_text_frame = 0

        for x in range(len(self.contents)):

            if x == self.bool_value:

                bool_val = 1

            else:

                bool_val = 0

            self.pyg_rects.append(BoolButton(last_x, self.y, "", bool_val, self.width, self.height))

            last_x += margin

            self.texts.append(self.contents[x].split("\n"))

            x_width = 19*(len(max(self.texts[-1], key=lambda x:len(x)))+1)

            self.content_frames.append(pygame.Rect(last_x, self.y+self.height*(1.5), x_width, self.police_height*len(self.texts[-1])))  # Panneau(content, self.x+2*self.width, self.y-10, y_focus=-25, adjust_width_to_text=1))

            last_x += max(x_width, self.width) + margin

            if self.police_height*len(self.texts[-1]) > self.biggest_text_frame:

                self.biggest_text_frame = self.police_height*len(self.texts[-1])

        self.total_width = last_x

    def update_pos(self, pos):

        self.x += pos[0]

        self.y += pos[1]

        #print(self.pyg_rects[0], self.content_frames[0])

        for x in self.pyg_rects:

            x.update_pos(pos)

        for x in self.content_frames:

            x.x, x.y = x.x+pos[0], x.y+pos[1]

        #print(self.pyg_rects[0], self.content_frames[0])

    def draw(self):

        for x in range(len(self.pyg_rects)):

            self.pyg_rects[x].draw()

            pygame.draw.rect(screen, self.anti_color, self.content_frames[x])

            x_text_frame = self.content_frames[x][0]

            y_text_frame = self.content_frames[x][1]

            for index in range(len(self.texts[x])):

                aff_txt(self.texts[x][index], x_text_frame, y_text_frame+index*self.police_height, color=self.color)

    def update(self, mouse_pos, clicking):

        if clicking:

            for index in range(len(self.pyg_rects)):

                if self.pyg_rects[index].clicked(mouse_pos):

                    self.pyg_rects[self.bool_value].bool_value = 0

                    self.bool_value = index

                    self.pyg_rects[self.bool_value].bool_value = 1


class Lift:
    """ Le petit ascenseur avec lequel l'utilisateur choisit une valeur numerique """
    def __init__(self, x, y, width=200, height=10, square_size=16, min_borne=-1, max_borne=1, echelle=None, text=None, float_vals=1, afficher_echelle=1, vertical=0, color1=[50, 150, 50], color2=[215, 50, 50]):

        self.color1 = color1

        self.color2 = color2

        self.x = x

        self.y = y

        self.width = width

        self.height = height

        self.square_size = square_size

        self.pyg_rail = pygame.Rect(x, y, self.width, self.height)

        self.min_borne = min_borne

        self.max_borne = max_borne

        self.bornes = [min_borne, max_borne]

        if echelle == None:

            self.echelle = (min_borne+max_borne) / 2

        else:

            self.echelle = echelle

        if vertical:

            y_pyg_square = set_val_to_different_array(self.bornes, [self.pyg_rail[1], self.pyg_rail[1]+self.pyg_rail[3]], self.echelle)

            self.pyg_square = pygame.Rect(x-(self.square_size-self.width)/2, y_pyg_square, self.square_size, self.square_size)

        else:

            x_pyg_square = set_val_to_different_array(self.bornes, [self.pyg_rail[0], self.pyg_rail[0]+self.pyg_rail[2]], self.echelle)

            self.pyg_square = pygame.Rect(x_pyg_square, y-(self.square_size-self.height)/2, self.square_size, self.square_size)

        self.text = text

        if text:

            self.text_frame = Panneau(self.text, self.x-75, self.y-7*self.height, y_focus=-25, adjust_width_to_text=1)

        self.float_accuracy = float_vals  # vals of lift should be integers only

        if not self.float_accuracy:

            self.echelle = int(self.echelle)

        self.afficher_echelle = afficher_echelle

        self.forward_dimension_index = vertical

    def draw(self):

        pygame.draw.rect(screen, self.color1, self.pyg_rail)

        pygame.draw.rect(screen, self.color2, self.pyg_square)

        if self.afficher_echelle:

            decalage = 50

            pygame.draw.rect(screen, WHITE, pygame.Rect(self.pyg_rail[0]-decalage*(5/4), self.pyg_rail[1]-decalage/3, decalage, decalage))

            aff_txt(str(round(self.echelle, self.float_accuracy)), self.pyg_rail[0]-decalage*(5/4), self.pyg_square[1], taille=20)

        if self.text:

            self.text_frame.draw()

    def update_pos(self, pos):

        self.x += pos[0]

        self.y += pos[1]

        self.pyg_rail = pygame.Rect(self.x, self.y, self.width, self.height)

        if self.forward_dimension_index == 1:

            accurate_echelle = set_val_to_different_array([self.pyg_rail[1], self.pyg_rail[1]+self.pyg_rail[3]], self.bornes, self.pyg_square[1])

            y_pyg_square = set_val_to_different_array(self.bornes, [self.pyg_rail[1], self.pyg_rail[1]+self.pyg_rail[3]], accurate_echelle)

            self.pyg_square = pygame.Rect(self.x-(self.square_size-self.width)/2, y_pyg_square, self.square_size, self.square_size)

            self.pyg_square[0] += pos[0]

        else:

            accurate_echelle = set_val_to_different_array([self.pyg_rail[0], self.pyg_rail[0]+self.pyg_rail[2]], self.bornes, self.pyg_square[0])

            x_pyg_square = set_val_to_different_array(self.bornes, [self.pyg_rail[0], self.pyg_rail[0]+self.pyg_rail[2]], accurate_echelle)

            self.pyg_square = pygame.Rect(x_pyg_square, self.y-(self.square_size-self.height)/2, self.square_size, self.square_size)

            self.pyg_square[0] += pos[0]
            
##        self.pyg_square[0] += pos[0]
##
##        self.pyg_square[1] += pos[1]

        if self.text:

            self.text_frame = Panneau(self.text, self.x-75, self.y-7*self.height, y_focus=-25, adjust_width_to_text=1)

    def update_bornes(self, n_borne):

        self.bornes = n_borne

        self.min_borne = n_borne[0]

        self.max_borne = n_borne[1]

    def update_echelle(self, n_echelle):

        self.echelle = n_echelle

        if self.echelle > self.max_borne:

            self.echelle = self.max_borne

        elif self.echelle < self.min_borne:

            self.echelle = self.min_borne

        index = self.forward_dimension_index

        if index == 0:

            max_borne = self.x+self.width

            min_borne = self.x

        else:

            max_borne = self.y+self.height

            min_borne = self.y

        pos_pyg_square = set_val_to_different_array(self.bornes, [min_borne, max_borne], self.echelle)

        self.pyg_square[index] = pos_pyg_square

    def clicked(self, pos):

        return (self.pyg_square.collidepoint(pos))

    def go(self, dim_translation):

        index = self.forward_dimension_index

        if index == 0:

            max_borne = self.x+self.width

            min_borne = self.x

        else:

            max_borne = self.y+self.height

            min_borne = self.y

        self.pyg_square[index] += dim_translation

        if self.pyg_square[index] > max_borne:

            self.pyg_square[index] = max_borne

        elif self.pyg_square[index] < min_borne:

            self.pyg_square[index] = min_borne

        self.echelle = round(set_val_to_different_array([self.pyg_rail[index], self.pyg_rail[index]+self.pyg_rail[index+2]], self.bornes, self.pyg_square[index]), self.float_accuracy)

        if not self.float_accuracy:

            self.echelle = int(self.echelle)


class Tab:

    def __init__(self, rows, cols, pictures_paths):

        project_nb = len(pictures_paths)

        self.page_number = project_nb//(rows*cols) + 1

        self.page = 0

        self.rows = rows

        self.cols = cols

        self.x_margin = screen_width//8

        self.y_margin = screen_height//8

        self.pyg_rect = pygame.Rect(self.x_margin, self.y_margin, screen_width-2*self.x_margin, screen_height-2*self.y_margin)

        self.in_x_margin = screen_width//20

        self.in_y_margin = screen_height//20

        self.frame_width = (screen_width-2*self.x_margin-(self.cols+1)*self.in_x_margin)/self.cols

        self.frame_height = (screen_height-2*self.y_margin-(self.rows+1)*self.in_y_margin)/self.rows

        self.frames = [[[Panneau("", self.pyg_rect[0]+(x+1)*self.in_x_margin+x*self.frame_width,
                                    self.pyg_rect[1]+(y+1)*self.in_y_margin+y*self.frame_height,
                                    self.frame_width,
                                    self.frame_height)

                        for x in range(self.cols)] for y in range(self.rows)]

                       for p in range(self.page_number)]

        # takes off the useless frames

        to_del_nb = ((self.rows*self.cols)*self.page_number)-project_nb

        for x in range(to_del_nb//self.cols):

            self.frames[-1].pop()

        for x in range(to_del_nb%self.cols):

            self.frames[-1][-1].pop()

        # adds paths names to frames
        for p in range(len(self.frames)):

            for y in range(len(self.frames[p])):

                for x in range(len(self.frames[p][y])):

                    self.frames[p][y][x].contenu = pictures_paths[x+y*self.rows+p*(self.rows*self.cols)]

        ##
            
        self.color = WHITE

        self.frame_color = BLACK

        self.target_tile = 0

        taille = 60

        self.tile_page_number = Panneau("1", screen_width//2-taille/2, screen_height-taille, taille, taille, y_focus=-15)

        shrink = 10

        self.all_pictures = [[[load_picture(self.frames[p][y][x].contenu, self.frame_width, self.frame_height)

                        for x in range(len(self.frames[p][y]))] for y in range(len(self.frames[p]))]

                       for p in range(len(self.frames))]

        self.special_text = 0

    def move_page(self, value):

        if val_in_array(self.page+value, [0, self.page_number-1]):

            self.page += value

            self.tile_page_number.contenu = str(self.page+1)

    def update(self, clicking):

        actual_frames = self.frames[self.page]

        mouse = pygame.mouse.get_pos()

        if clicking:

            for y in range(len(actual_frames)):

                for x in range(len(actual_frames[y])):

                    if actual_frames[y][x].clicked(mouse):

                        return self.frames[self.page][y][x].contenu

        # checks if user's mouse is on a frame -> activates a demo

        for y in range(len(actual_frames)):

            for x in range(len(actual_frames[y])):

                if actual_frames[y][x].clicked(mouse):

                    self.special_text = [actual_frames[y][x].contenu[:-4], self.x_margin+10, self.y_margin+(y+1)*self.frame_height+(y+1)*self.in_y_margin]  # +x*self.frame_width+(x+1)*self.in_x_margin

        Tab.draw(self)

        # sets default for next frame, will be re-reset if needed

        if self.special_text:

            self.special_text = 0

    def draw(self):

        actual_frames = self.frames[self.page]

        screen.fill(BLACK)

        pygame.draw.rect(screen, self.color, self.pyg_rect)

        for y in range(len(actual_frames)):

            for x in range(len(actual_frames[y])):

                actual_frames[y][x].draw()  # pygame.draw.rect(screen, self.frame_color, self.frames[y][x])

                screen.blit(self.all_pictures[self.page][y][x], [actual_frames[y][x].x, actual_frames[y][x].y])

        self.tile_page_number.draw()

        if self.special_text:

            aff_txt(self.special_text[0], self.special_text[1], self.special_text[2])


def saisie():

    not_done = True

    clicking = 0

    string = ""

    while not_done:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                not_done = False

            elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):

                clicking = 1

            elif (event.type == pygame.MOUSEBUTTONUP) and (event.button == 1):

                clicking = 0

            elif (event.type == pygame.MOUSEMOTION):

                translation = event.rel

            elif event.type == pygame.KEYDOWN:

                print(event.key)

                if event.key == K_RETURN:

                    not_done = False

                elif event.key == 8:

                    print(string)

                    string = string[:-1]

                    print(string)

                else:

                    string += event.unicode

        screen.fill(WHITE)

        aff_txt(string, 0, 0, BLACK)

        pygame.display.update()

        clock.tick(60)


def select_picture():
    """ selects an image from "picture" file, with GUI """

    picture_list = [img for img in listdir("pictures") if not (img == "Thumbs.db")]  # if isfile(join("pictures", f))]

    tab = Tab(2, 2, picture_list)

    play = True

    clicking = 0

    # buttons

    play_button_height = 70

    quit_button = Panneau("Quitter", 0, screen_height-play_button_height, 200, play_button_height, y_focus=-15)

    # arrow buttons (to switch page)

    arrow_buttons = []

    arrow_button_width = 100

    arrow_button_height = 100

    arrow_buttons.append(Panneau("", 0, screen_height/2-arrow_button_height/2, arrow_button_width, arrow_button_height, image=draw_play, image_coors=[arrow_button_width/2, arrow_button_height/2], image_args=[WHITE, -1]))

    arrow_buttons.append(Panneau("", screen_width-arrow_button_width, screen_height/2-arrow_button_height/2, arrow_button_width, arrow_button_height, image=draw_play, image_coors=[arrow_button_width/2, arrow_button_height/2], image_args=[WHITE, 1]))

    # GUI Loop
    while play:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                play = False

            elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):

                mouse_pos = pygame.mouse.get_pos()

                clicking = 1

                if quit_button.clicked(mouse_pos):

                    play = False

                for button in arrow_buttons:

                    if button.clicked(mouse_pos):

                        direction = arrow_buttons.index(button) or -1

                        tab.move_page(direction)

            elif (event.type == pygame.MOUSEBUTTONUP) and (event.button == 1):

                clicking = 0

            elif (event.type == pygame.MOUSEMOTION):

                translation = event.rel

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_LEFT:

                    tab.move_page(-1)

                if event.key == pygame.K_RIGHT:

                    tab.move_page(1)

        path = tab.update(clicking)

        if path:

            play = False

            return path[:-4]

        quit_button.draw()

        for button in arrow_buttons:

            button.draw()

        pygame.display.update()

        clock.tick(60)


class Losange:

    def __init__(self, x_top, y_top, right_width, height, color=(255, 255, 255)):

        self.x_top = x_top

        self.right_width = right_width

        self.y_top = y_top

        self.height = height

        self.color = color

    def draw(self):

        pygame.draw.polygon(screen, self.color, ((self.x_top, self.y_top), (self.x_top-self.right_width, self.y_top+self.height/2), (self.x_top, self.y_top+self.height), (self.x_top+self.right_width, self.y_top+self.height/2), (self.x_top, self.y_top)))


class Rect:

    def __init__(self, x, y, width, height):

        self.x = x

        self.width = width

        self.y = y

        self.height = height


class Dot:

    def __init__(self, x, y, radius=1):

        self.x = x

        self.y = y

        self.radius = radius

        self.color = BLUE

    def draw(self):

        pygame.draw.circle(screen, self.color, [int(self.x), int(self.y)], self.radius)


class MovingDot(Dot):

    def __init__(self, x, y, radius=1, vector=[0, 0]):

        Dot.__init__(self, x, y, radius)

        self.vector = vector

    def update(self, vector=[0, 0]):

        #if random.randint(0, 100) == 0:

        if vector == [0, 0]:

            self.vector = get_random_vector()

        else:

            self.vector = vector

        self.x += self.vector[0]

        self.y += self.vector[1]


class GearWheel:

    """ not woring yet... """

    def __init__(self, x, y, wheel_radius, gear_width, gear_height, gear_number, color=(100, 100, 100), gear_color=(150, 150, 150)):

        self.x = x

        self.y = y

        self.wheel_radius = wheel_radius

        self.gear_width = gear_width

        self.gear_height = gear_height

        self.gear_number = gear_number

        self.color = color

        self.gear_color = gear_color

    def draw(self):

        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.wheel_radius)

        pi_var = (2*pi)/self.gear_number

        for delta_pi in range(self.gear_number):

            cos_val = cos(delta_pi*pi_var)

            sin_val = sin(delta_pi*pi_var)

            circle_point = (self.x+cos_val*(self.wheel_radius*(99/100)), self.y+sin_val*(self.wheel_radius*(99/100)))

            rayon = get_droite_from_pt((self.x, self.y), circle_point)

            total = self.gear_width+self.gear_height

            sin_diff = set_val_to_different_array([-1, 1], [0, 1], abs(cos_val)-abs(sin_val))

            cos_diff = set_val_to_different_array([-1, 1], [0, 1], abs(sin_val)-abs(cos_val))

            r_pt1, r_pt2 = get_segment_around_point(rayon, circle_point, 5, norme_len=10)

            tangente = get_perpendiculaire_from_d(rayon, circle_point)

            tan_pt1, tan_pt2 = get_segment_around_point(tangente, circle_point, 5, norme_len=10)

            print(cos_val, sin_val, cos_diff, sin_diff)

            pyg_gear = pygame.Rect(r_pt1[0], tan_pt1[1], cos_diff*100+20, sin_diff*100+20)#get_distance(r_pt1, r_pt2), get_distance(tan_pt1, tan_pt2))

            pygame.draw.rect(screen, self.gear_color, pyg_gear)

        pygame.display.update()


class RotatingObject:

    def __init__(self, circle_radius, circle_center, rotation_speed=200, points_avancements=[0, 10, 100, 110], visible_center=1, color=(255, 255, 255)):
        """ This object simulates a rotation for a polygon, every point must be on the circle defined by center and radius ; points of the polygon should be sorted the way you wish .. like be careful if you sort it the bad way your rectangle could end up in two weird tringles .. """

        self.point_deltas = points_avancements

        self.rotation_speed = (2*pi)/rotation_speed

        self.circle_radius = circle_radius

        self.circle_center = circle_center

        self.visible_center = visible_center

        self.color = color

        for x in range(len(self.point_deltas)):

            self.point_deltas[x] += 0.0001

    def update(self):

        for x in range(len(self.point_deltas)):

            self.point_deltas[x] += 1

    def draw(self):

        points = []

        for x in self.point_deltas:

            cos_pos, sin_pos = get_pos_on_circle(self.rotation_speed*x)

            points.append((int(self.circle_center[0]+cos_pos*self.circle_radius), int(self.circle_center[1]+sin_pos*self.circle_radius)))

        points.append(points[0])

        pygame.draw.polygon(screen, self.color, points)

        pygame.draw.circle(screen, RED, self.circle_center, 10)


class RotatingRectangle(RotatingObject):

    def __init__(self, circle_radius, circle_center, rotation_speed=200, points_avancements=[0, 10, 100, 110], visible_center=1, color=(255, 255, 255)):
        """ should just be four "points" (in fact just 0->2pi), sorted """

        RotatingObject.__init__(self, circle_radius, circle_center, rotation_speed, points_avancements, visible_center, color)

    def collide_with_circle(self, circle, circle_array_format=0):

        ## just formatting the arrays/objects

        if circle_array_format:

            circle_x = circle[0][0]

            circle_y = circle[0][1]

            circle_radius = circle[1]

        else:

            circle_x = circle.x

            circle_y = circle.y

            circle_radius = circle.radius

        # lines of the rectangle
        points = []

        for x in self.point_deltas:

            cos_pos, sin_pos = get_pos_on_circle(self.rotation_speed*x)

            points.append((int(self.circle_center[0]+cos_pos*self.circle_radius), int(self.circle_center[1]+sin_pos*self.circle_radius)))

        # getting segments

        seg1 = [points[0], points[3]]

        seg2 = [points[1], points[2]]

        colliding_segs = []

        if collide_segment_to_circle([circle_x, circle_y], circle_radius, seg1):

            colliding_segs.append(seg1)

        if collide_segment_to_circle([circle_x, circle_y], circle_radius, seg2):

            colliding_segs.append(seg2)

        if len(colliding_segs) == 2:

            return [min(colliding_segs, key=lambda x:get_distance(x[0], [circle_x, circle_y]))]

        return colliding_segs


def try_test_collision_rotating_rect_and_ball_visual():

    aff = True

    rect = RotatingRectangle(100, [300, 300], color=BLACK)

    radius = 30

    while aff:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                aff = False

            elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):

                aff = False

            elif (event.type == pygame.MOUSEMOTION):

                translation = event.rel

        rect.update()

        screen.fill(BLUE)

        rect.draw()

        if not rect.collide_with_circle([pygame.mouse.get_pos(), radius], 1):

            pygame.draw.circle(screen, WHITE, pygame.mouse.get_pos(), radius)

        else:

            pygame.draw.circle(screen, RED, pygame.mouse.get_pos(), radius)

        pygame.display.update()

        clock.tick(60)


def wait():

    click = 0

    while not click:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                click = 1

            elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):

                click = 1

            elif (event.type == KEYDOWN):

                click = 1


def get_click():

    click = 0

    while not click:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                click = 1

            elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):

                click = 1

                return pygame.mouse.get_pos()


class Particule:

    def __init__(self, x, y):

        self.x = x

        self.y = y

        self.vect = [0, 0]

    def apply_vect(self, facteur=1):

        self.x += self.vect[0] * facteur

        self.y += self.vect[1] * facteur

    def stear_off_screen(self):

        self.vect = [self.x-screen_center[0], self.y-screen_center[1]]

        vitesse = set_val_to_different_array([0, screen_width//2], [10, 5], get_distance((self.x, self.y), screen_center))

        get_normalized_vector(self.vect, vitesse)


def draw_barre_vie(ratio_plein, x, y, width, height=10):

    y -= height//2

    red_rect = pygame.Rect(x, y, width, height)

    green_rect = pygame.Rect(x, y, width*ratio_plein, height)

    pygame.draw.rect(screen, RED, red_rect)

    pygame.draw.rect(screen, GREEN, green_rect)


def draw_cible(x, y, xy_adjust, inputs):

    x, y = sum_arrays([x, y], xy_adjust)

    sizes, color = inputs

    pos = [x, y]

    pygame.draw.circle(screen, color, pos, sizes[0])

    pygame.draw.circle(screen, color, pos, sizes[1], 3)

    rect_thickness = 4

    hor_pyg_rect = pygame.Rect(x-sizes[1], y-rect_thickness/2, sizes[1]*2, rect_thickness)

    pygame.draw.rect(screen, color, hor_pyg_rect)

    vert_pyg_rect = pygame.Rect(x-rect_thickness/2, y-sizes[1], rect_thickness, sizes[1]*2)

    pygame.draw.rect(screen, color, vert_pyg_rect)


def draw_double_fire(x, y, xy_adjust, inputs):

    x, y = sum_arrays([x, y], xy_adjust)

    size, colors = inputs

    for idx in range(1, 3):

        draw_fire(x, y, [0, 0], [size/idx, colors[idx-1]])


def draw_fire(x, y, xy_adjust, inputs):

    x, y = sum_arrays([x, y], xy_adjust)

    size, color = inputs

    side_vects = [[-0.5, -1], [0.5, -1]]

    decals = [[-size/5, -size/8], [size/5, -size/8]]

    main_vect = [0, -1]

    draw_triangle_from_vect([x, y], main_vect, size, color)

    for ix in range(2):

        vect = side_vects[ix]

        nx = decals[ix][0]

        ny = decals[ix][1]

        draw_triangle_from_vect([x+nx, y+ny], vect, size, color)


def draw_coin(x, y, xy_adjust, inputs):

    x, y = sum_arrays([x, y], xy_adjust)

    rad = inputs[0]

    pygame.draw.circle(screen, YELLOW, [x, y], rad)


def draw_triangle_from_vect(pos, vect, size=None, color=(255, 255, 255)):

    if size != None:

        vect = get_normalized_vector(vect, size)

    else:

        size = get_distance(pos, sum_arrays(pos, vect))

    A = sum_arrays(pos, vect)

    milieuBC = pos

    d_milieuA = get_droite_from_pt(milieuBC, A)

    BC = get_perpendiculaire_from_d(d_milieuA, milieuBC)

    B, C = collide_line_to_circle(milieuBC, size/3, BC)

    pygame.draw.polygon(screen, color, [A, B, C])

    
def draw_heart(x, y, size):

    A = [x, y+size]

    B = [x-2*size, y-size]

    Z = [x+2*size, y-size]

    C = [x-size, y-2*size]

    Y = [x+size, y-2*size]

    O = [x, y-size]

    pygame.draw.polygon(screen, RED, [A, B, C, O, Y, Z, A])


def stear_of_screen(x, y, x_max, y_max):

    if x > (x_max // 2):

        nearest_x = x_max

        signe_x = -1

    else:

        nearest_x = 0

        signe_x = 1

    if y > (y_max // 2):

        nearest_y = y_max

        signe_y = -1

    else:

        nearest_y = 0

        signe_y = 1

    dist_x = abs(x-nearest_x)

    dist_y = abs(y-nearest_y)

    return [(dist_x-x_max//2)*-1*signe_x, (dist_y-y_max//2)*-1*signe_y]



def point_rotation(center, dist_to_center, speed, rotation_cycle_avancement=0):

    delta_pi = (2*pi)/speed

    aff = True

    x = rotation_cycle_avancement

    while aff:

        x += 1

        #print("\n\n", x)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                aff = False

            elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):

                aff = False

            elif (event.type == pygame.MOUSEMOTION):

                translation = event.rel

        screen.fill(WHITE)

        cos_pos, sin_pos = get_pos_on_circle(delta_pi*x)

        pygame.draw.circle(screen, RED, center, 20)

        current_pt = (int(center[0]+cos_pos*dist_to_center), int(center[1]+sin_pos*dist_to_center))

        pygame.draw.circle(screen, RED, current_pt, 20)

        pygame.display.update()

        clock.tick(60)


def rotate_rectangle(x, y, width, height, speed=200, center=0, dist_center=0):

    if not center:

        center = [x+width//2, y+height//2]

    if not dist_center:

        dist_center = width//2+height//2

    delta_pi = (2*pi)/speed

    aff = True

    x1 = 0

    x2 = speed//20

    x3 = speed//2

    x4 = speed//2+speed//20

    xs = [x1, x2, x3, x4]

    while aff:

        for y in range(len(xs)):

            xs[y] += 1

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                aff = False

            elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):

                aff = False

            elif (event.type == pygame.MOUSEMOTION):

                translation = event.rel

        screen.fill(WHITE)

        points = []

        for x in xs:

            cos_pos, sin_pos = get_pos_on_circle(delta_pi*x)

            points.append((int(center[0]+cos_pos*dist_center), int(center[1]+sin_pos*dist_center)))


        pygame.draw.polygon(screen, BLACK, (points[0], points[1], points[2], points[3], points[0]))

        pygame.draw.circle(screen, RED, center, 20)

        pygame.display.update()

        clock.tick(60)

    
def rotate_rect(line_rot_obj, rect_width, avancement, rotation_cycle=100):

    line = rotate_line(line_rot_obj, avancement, rotation_cycle=rotation_cycle)

    diff_x = abs(line[0][0]-line[1][0])

    diff_y = abs(line[0][1]-line[1][1])

    print(diff_x, diff_y)

    ratio_borne = [0, 1]

    ratio_x = set_val_to_different_array([-line_rot_obj[1]*2, line_rot_obj[1]*2], ratio_borne, diff_x-diff_y)

    width_y = rect_width*ratio_x*get_sign(line[0][0]-line[1][0])*-1

    width_x = rect_width*get_contraire_in_array(ratio_x, ratio_borne)*get_sign(line[0][1]-line[1][1])*-1

    print(width_x, width_y, ratio_x)

    line2 = [[line[1][0]+width_x, line[1][1]+width_y], [line[0][0]+width_x, line[0][1]+width_y]]

    return line, line2


def rotate_line(line_rot_obj, avancement, rotation_cycle=100):
    """ the line object is [[middle of line], len_line] """

    angular_speed = ((2*pi)/rotation_cycle)*avancement

    n_pos = get_pos_on_circle(angular_speed, line_rot_obj[1], line_rot_obj[0])

    return n_pos, sym_to_point(n_pos, line_rot_obj[0])


def test_rotation():

    line = [[300, 200], 100]

    line2 = [[300, 220], 100]

    line3 = [[290, 200], 100]

    lines = [line, line2]

    aff = True

    x = 0

    while aff:

        x += 1

        print("\n\n", x)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                aff = False

            elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):

                aff = False

            elif (event.type == pygame.MOUSEMOTION):

                translation = event.rel

        screen.fill(WHITE)

        pos_s = []

        rect = rotate_rect(line, 10, x, 10)

        pygame.draw.polygon(screen, BLACK, (rect[0][0], rect[0][1], rect[1][0], rect[1][1]))

        pygame.display.update()

        clock.tick(1)

    
# pygame draw functions


def draw_line(droite, color=(0, 0, 0), width=3):
    """ Draws a line given d[m, p] with y = mx+p """

    m, p = droite

    if m == []:

        p1 = [p, 0]

        p2 = [p, screen_height]

    else:

        p1 = [0, p]

        p2 = [screen_width, m*screen_width+p]

    pygame.draw.line(screen, color, p1, p2, width)

    pygame.display.update()


def draw_segment_around_point(line, point, x_gap, color=(255, 255, 255), width=3, norme_len=0):
    """ draw a segment from point-gap to point+gap """

    m, p = line

    p1 = [point[0]-x_gap, point[1]-x_gap*m]

    p2 = [point[0]+x_gap, point[1]+x_gap*m]

    if norme_len:

        facteur = get_distance(point, p1)/norme_len

        p1 = [point[0]-(x_gap/facteur), point[1]-(x_gap/facteur)*m]

        p2 = [point[0]+(x_gap/facteur), point[1]+(x_gap/facteur)*m]

    pygame.draw.line(screen, color, p1, p2, width)

    pygame.display.update()


def get_segment_around_point(line, point, x_gap, color=(255, 255, 255), width=3, norme_len=0):
    """ draw a segment from point-gap to point+gap """

    m, p = line

    p1 = [point[0]-x_gap, point[1]-x_gap*m]

    p2 = [point[0]+x_gap, point[1]+x_gap*m]

    if norme_len:

        facteur = get_distance(point, p1)/norme_len

        p1 = [point[0]-(x_gap/facteur), point[1]-(x_gap/facteur)*m]

        p2 = [point[0]+(x_gap/facteur), point[1]+(x_gap/facteur)*m]

    return p1, p2


def draw_segment_from_point(line, point, x_gap, color=(255, 255, 255), width=3, norme_len=0):
    """ draw a segment from point-gap to point+gap """

    m, p = line

    p1 = [point[0]+x_gap, point[1]+x_gap*m]

    if norme_len:

        facteur = get_distance(point, p1)/norme_len

        p1 = [point[0]+(x_gap/facteur), point[1]+(x_gap/facteur)*m]

    pygame.draw.line(screen, color, point, p1, width)

    pygame.display.update()


def draw_play(x, y, add, bonus_args=0):

    if bonus_args:

        col = bonus_args[0]

        sens = bonus_args[1]

    else:

        col = GREEN

        sens = 1

    thickness = 0

    x += add[0]

    y += add[1]

    size = 30

    pygame.draw.polygon(screen, col, ((x-(size*sens), y-size), (x+(size*sens), y), (x-(size*sens), y+size)), thickness)


def draw_pause(x, y, add):

    x += add[0]

    y += add[1]

    rect1 = pygame.Rect(x, y, 5, 20)

    rect2 = pygame.Rect(x+10, y, 5, 20)

    pygame.draw.rect(screen, WHITE, rect1)

    pygame.draw.rect(screen, WHITE, rect2)


def draw_quit(x, y, add):

    thickness = 0

    x += add[0]

    y += add[1]

    size = 66  # divisible par 3

    rect = pygame.Rect(x, y, size, size)

    pygame.draw.rect(screen, RED, rect)

    door = pygame.Rect(x+size//3, y+size, size//3, -size//3)

    pygame.draw.rect(screen, BLACK, door)

    pygame.draw.polygon(screen, RED, ((x, y), (x+size//2, y-size//2), (x+size, y), (x, y)), thickness)


def draw_cross(x, y, add, size=20, thickness=4):

    x += add[0]

    y += add[1]

    pygame.draw.line(screen, RED, (x-size, y-size), (x+size, y+size), thickness)

    pygame.draw.line(screen, RED, (x-size, y+size), (x+size, y-size), thickness)


def draw_fleche(x, y, size, color=[20, 255, 25]):
##
##    x += coor_add[0]
##
##    y += coor_add[0]

    A = [x, y]

    B = [x+size, y]

    C = [x+size, y-4*size]

    D = [x+2*size, y-4*size]

    E = [x+size//2, y-6*size]

    D2 = [x-size, y-4*size]

    C2 = [x, y-4*size]

    points = [A, B, C, D, E, D2, C2]

    pygame.draw.polygon(screen, color, points)


def draw_fleche_formatted(x, y, xy_tweak, inputs):

    size, color, xy_revert = inputs

    x, y = x+xy_tweak[0], y+xy_tweak[1]

    if xy_revert:

        first_index = 1

        second_index = 0

    else:

        first_index = 0

        second_index = 1

    points = [[x, y] for v in range(7)]

    addings = [[0, 0], [size, 0], [size, -4*size], [2*size, -4*size], [size//2, -6*size], [-size, -4*size], [0, -4*size]]

    for index in range(len(points)):

        points[index][first_index] += addings[index][0]

        points[index][second_index] += addings[index][1]

    pygame.draw.polygon(screen, color, points)


def draw_flower(x_pos, y_pos, size, color, colors, petal_nb, angle=0):

    pi_step = 2*pi / petal_nb

    for x in range(petal_nb):

        petal = [x_pos+(cos(angle+pi_step*x)*4*size), y_pos+(sin(angle+pi_step*x)*4*size)]

        pygame.draw.circle(screen, colors[x], [int(petal[0]), int(petal[1])], int(2*size))

    pygame.draw.circle(screen, color, [int(x_pos), int(y_pos)], size*4)


def aff_txt(contenu, x, y, color=(0, 0, 0), taille=30, centre=0, font=None):
    """ Permet d'afficher un texte """

    if centre == 1:

        # taille en fontsize=30 -> 18 px ; on ajuste pour que dans le cas majoritaire ca marche bien

        x -= (len(contenu)/2)*(18)*(taille/30)

    if taille == 30:

        font = font_30

    elif taille == 20:

        font = font_20

    elif (font == None):

        font = pygame.font.SysFont("monospace", taille, True)

    text = font.render(contenu, 1, color)

    screen.blit(text, (x, y))


def menu():

    shop_button = Panneau("Shop $", 200, 350, 150, 100, YELLOW)

    play_button = Panneau("Play !", 400, 350, 150, 100, BLUE)

    exit_button = Panneau("Exit..", 300, 475, 150, 100, RED)

    choix = 0

    while choix == 0:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                choix = 1

            elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):

                mouse_pos = pygame.mouse.get_pos()

                if shop_button.clicked(mouse_pos):

                    go_shop()

                elif play_button.clicked(mouse_pos):

                    game_loop()

                elif exit_button.clicked(mouse_pos):

                    choix = 1

        screen.fill(BROWN)

        shop_button.draw()

        play_button.draw()

        exit_button.draw()

        aff_txt("Fire & Fury Corp.", 250, 100)

        aff_txt("Game !", 300, 200, taille=50)

        pygame.display.update()

        clock.tick(10)

# Pygame color functions


class ColorManager:

    def __init__(self, color=0, selected_color=0):

        if not color:

            self.color =  get_random_color()


        else:

            self.color = color

        if not selected_color:

            self.selected_color =  [random.randint(0, 2), random.choice([-1, 1])]

        else:

            self.selected_color = selected_color

    def update_color(self):

        self.color, self.selected_color = update_colors(self.color, self.selected_color)

    def set_to_rand_color(self):

        self.color = get_random_color()

    def set_to_bw(self):

        average = get_average(self.color)

        self.color = [average, average, average]


def get_inv_color(color):

    return [(x-255)*-1 for x in color]


def set_color(col):

    rand = 0

    if rand:

        return get_random_color()

    return list(col)


def get_random_color():

    return [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]


def update_colors(color, selected_color, borne=[0, 255], inverse_growth=1):
    """ color is the actual color ; selected color [ index (0 to 2) , increment (-1 or 1)] """

    while (color[selected_color[0]]+selected_color[1] < borne[0]) or (color[selected_color[0]]+selected_color[1] > borne[1]):

        selected_color[0] = random.randint(0, 2)

        selected_color[1] = (1*random.randint(0, 1)) or -1  # 1 or -1

    color[selected_color[0]] = round(color[selected_color[0]]+selected_color[1]/inverse_growth, 2)

    return color, selected_color


## Tests

##def test_vitesse_2Darray():
##
##    while True:
##
##        a = time.time()
##
##        for y in range(screen_height):
##
##            for x in range(screen_width):
##
##                screen.set_at((x, y), get_random_color())
##
##        print(time.time()-a)
##
##        clock.tick(100)
##
##        print(clock.get_fps())


def test_vitesse_2Darray():

    while True:

        for y in range(screen_height):

            for x in range(screen_width):

                screen.set_at((x, y), get_random_color())

        clock.tick(60)

        print(clock.get_fps())


def random_pt_in_screen():

    return Arr([random.randint(0, screen_width), random.randint(0, screen_height)])


# to chose spawn location of window

x_screen = 0

y_screen = 30

import os

os.environ['SDL_VIDEO_WINDOW_POS'] = "{},{}".format(x_screen,y_screen)

## information you're able to import without a screen creation
from pigtv_constants import *

## pygame initialisation
import pygame

pygame.mixer.pre_init(buffer=256)

from pygame.locals import *

#from get_drawing_coors import Drawing

from math import *

import random

import time

from string import ascii_lowercase as abc

from os import listdir

from os.path import isfile, join

clock = pygame.time.Clock()

pygame.init()

MAX_SIZE = max([screen_width, screen_height])

screen_center = [screen_width//2, screen_height//2]

screen = pygame.display.set_mode((screen_width, screen_height))#  , FULLSCREEN)

font_30 = pygame.font.SysFont("monospace", 30, True)

font_20 = pygame.font.SysFont("monospace", 20, True)



## Color variables

WHITE = set_color((255, 255, 255))

BLACK = set_color((0, 0, 0))

RED = set_color((255, 0, 0))

LIGHT_RED = set_color((200, 0, 80))

DARK_RED = set_color((150, 0, 0))

YELLOW = set_color((255, 255, 0))

BEIGE = set_color((210, 210, 150))

GREEN = set_color((20, 255, 25))

DARK_GREEN = set_color((20, 60, 25))

BROWN = set_color((60, 30, 20))

BROWN2 = set_color([79, 51, 26])

DARK_BROWN = set_color((20, 0, 10))

GREY = set_color((150, 150, 150))

LIGHT_GREY = set_color((200, 200, 200))

DARK_GREY = set_color((60, 60, 60))

BLUE = set_color((0, 0, 150))

LIGHT_BLUE = set_color((0, 0, 255))

REAL_LIGHT_BLUE = set_color((200, 200, 255))

DARK_BLUE = set_color([0, 0, 60])

PURPLE = set_color([200, 10, 190])

ORANGE = set_color([255, 160, 0])

DARK_ORANGE = set_color([160, 40, 40])

PINK = set_color([255, 80, 80])

PINK2 = set_color([255, 20, 147])

##greys = []
##
##for x in range(25):
##
##    greys.append([x*10 for x in range(3)])


colors = [WHITE ,BLACK,RED ,LIGHT_RED ,DARK_RED ,YELLOW ,GREEN,DARK_GREEN,BROWN,BROWN2,DARK_BROWN,BLUE,LIGHT_BLUE ,REAL_LIGHT_BLUE ,DARK_BLUE ,PURPLE ,ORANGE, DARK_ORANGE, PINK, PINK2]


#colors += greys
#,GREY ,LIGHT_GREY,DARK_GREY, BEIGE

#test_area_triangle()


