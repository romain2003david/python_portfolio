from sklearn.datasets import load_digits

from pig_tv import *

digits = load_digits()

X, strings = digits.data, digits.target

strings = [str(x) for x in strings]

nbrs = []

for k in rl(X):

    tab = X[k]

    s = 8

    liste = [[0 for x in range(s)] for y in range(s)]

    for y in range(s):

        for x in range(s):

            liste[y][x] = tab[y*s+x]

    nbrs.append(liste)


class Img:

    def __init__(self, array):

        self.array = Arr(array)

        self.formated_array = Img.get_formated_array(self)

    def get_formated_array(self):

        return self.array

    def draw(self):

        for y in rl(self.formated_array):

            for x in rl(self.formated_array[y]):

                color = [self.formated_array[y][x]*(255/16) for t in range(3)]

                rect = pygame.Rect(x*20, y*20, 20, 20)

                pygame.draw.rect(screen, color, rect)

                #screen.set_at((x, y), )

        pygame.display.update()


def set_pixel(array, set_fct):
    """ enables to access each pixel of a picture (=2D array) and apply function of x and y without double looping """

    for y in rl(array):

        for x in rl(array[y]):

            array[y][x] = set_fct(x, y)


def create_avg_digits():

    """ from the set of digit examples, that have a specific format (ex: centred image(poids = black color) with a width and height, deduces an average digit for each digit """

    labeled_imgs = [(nbrs[x], strings[x]) for x in rl(nbrs[:1000])]

    dict_image = {}  # dictionnary contains for each digit number of examples and the summed example images

    for x in range(10):

        dict_image[str(x)] = [0, Arr([[0 for x in rl(labeled_imgs[0][0][y])] for y in rl(labeled_imgs[0][0]) ])]

    for (img, label) in labeled_imgs:

        dict_image[label][0] += 1

        tab = dict_image[label][1]

        set_pixel(tab, lambda x, y : tab[y][x]+img[y][x])

    modeles = []

    for x in range(10):

        compteur, image = dict_image[str(x)]

        set_pixel(image, lambda x, y : image[y][x]/compteur)

        dict_image[str(x)] = image

    return dict_image


def format_img(img):

    return img


def recognise_digit(img, dico_model):

    best_index = 0

    best_distance = Arr.get_distance(img, dico_model["0"])

    for x in range(1, 10):

        model_img = dico_model[str(x)]

        distance = Arr.get_distance(img, model_img)  # black and white images : int-2D array ; takes matrix norm

        #print(img, model_img)

        if distance < best_distance:

            best_distance = distance

            best_index = x

    return best_index


def main():

    tests = nbrs[1000:]

    model_dict = create_avg_digits()  # creates the dictionnary containing each digit model

    liste_modeles = [Img(model_dict[str(x)]) for x in range(10)]
    erreur = 0
    for nbr in liste_modeles:

        pass#nbr.draw()  #

        #wait()

    c = 0
    for test in tests:

        test = Img(Arr(test))
        if (recognise_digit(test.array, model_dict)!= digits.target[1000+c]):

            erreur += 1

        #test.draw()

        #wait()

        c += 1
    print(erreur/c)


main()
