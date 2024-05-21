def get_prim(polynom=[], exp=0, parenthese_exp=[]):

    reponse = ""

    reponse += get_prim_polynom(polynom)

    if exp != 0:

        reponse += "+({}/({}))*exp({})".format(exp, get_deriv_polynom(parenthese_exp), get_str_polynom(parenthese_exp))

    return reponse


def get_prim_polynom(polynom):

    reponse = ""

    for x in range(len(polynom[:])):

        degre = x+1

        const = polynom[x]

        reponse += "+({}*(1/{})*x^{})".format(const, degre, degre)

    return reponse


def get_deriv_polynom(polynom=[]):

    reponse = ""

    for x in range(len(polynom[1:])):

        degre = x+1

        const = polynom[degre]

        reponse += "+({}*x^{})".format(const*degre, degre-1)

    if reponse == "":

        return "0"

    else:

        return reponse


def get_str_polynom(polynom=[]):

    reponse = ""

    for x in range(len(polynom)):

        degre = x

        const = polynom[degre]

        reponse += "+({}*x^{})".format(const, degre)

    return reponse


def get_deriv_poly_exp(polynom=[], exp=0, parenthese_exp=[]):

    reponse = ""

    reponse += get_deriv_polynom(polynom)

    if exp != 0:

        reponse += "+{}*({})*exp({})".format(exp, get_deriv_polynom(parenthese_exp), get_str_polynom(parenthese_exp))

    return reponse


def get_deriv_sin(const=1, polynom=[]):

    reponse = ""

    reponse += get_deriv_polynom(polynom)

    reponse += "*({})".format(const)

    reponse += "*cos({})".format(get_str_polynom(polynom))

    return reponse

        
def get_deriv_cos(const=1, polynom=[]):

    reponse = ""

    reponse += get_deriv_polynom(polynom)

    reponse += "*({})".format(-const)

    reponse += "*sin({})".format(get_str_polynom(polynom))

    return reponse


def get_str_sin(const=1, polynom=[]):

    reponse = ""

    reponse += "({}*sin({}))".format(const, get_str_polynom(polynom))

    return reponse


def get_str_cos(const=1, polynom=[]):

    reponse = ""

    reponse += "({}*cos({}))".format(const, get_str_polynom(polynom))

    return reponse


def get_deriv_quotient(const, fct1, poly1, fct2, poly2):

    reponse = ""

    reponse += "({}*({}*{}-({})*{}))".format(const, deriv_dico[fct1](polynom=poly1), str_dico[fct2](polynom=poly2), deriv_dico[fct2](polynom=poly2), str_dico[fct1](polynom=poly1))

    reponse += "/({}^2)".format(str_dico[fct2](polynom=poly2))

    return reponse


def get_prim_sin(const=1, polynom=[]):

    reponse = ""

    reponse += "({}/{}*sin({}))".format(-const, get_deriv_polynom(polynom), get_str_polynom(polynom))

    return reponse


def get_prim_cos(const=1, polynom=[]):

    reponse = ""

    reponse += "({}/{}*sin({}))".format(const, get_deriv_polynom(polynom), get_str_polynom(polynom))

    return reponse


def get_deriv_cos(const=1, polynom=[]):

    reponse = ""

    reponse += get_deriv_polynom(polynom)

    reponse += "*({})".format(-const)

    reponse += "*sin({})".format(get_str_polynom(polynom))

    return reponse



deriv_dico = {"poly":get_deriv_polynom,
              "sin":get_deriv_sin,
              "cos":get_deriv_cos
              }

primi_dico = {"poly":get_prim_polynom,
              "sin":get_prim_sin,
              "cos":get_prim_cos}

str_dico = {"poly":get_str_polynom,
            "sin":get_str_sin,
            "cos":get_str_cos}

