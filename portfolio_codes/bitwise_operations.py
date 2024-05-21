def dec_to_bin(dec, return_liste=0):

    liste = []

    while dec > 0:

        liste.insert(0, dec%2)

        dec //= 2

    if return_liste:

        return liste

    return list_nb_to_int_nb(liste)


def list_nb_to_int_nb(liste):

    result = 0

    for x in range(len(liste)):

        power = len(liste)-x-1

        result += 10**(power)*liste[x]

    return result


def int_nb_to_liste_nb(nb):

    liste = []

    while nb > 0:

        liste.insert(0, dec%10)

        nb //= 10

    return liste[::-1]


def bin_to_dec(binr, return_liste=0):

    liste = []

    while binr > 0:

        liste.append(binr%10)

        binr //= 10

    if return_liste:

        return liste

    result = 0

    for x in range(len(liste)):

        boo = liste[::-1][x]

        result += 2**(x)*boo

    return result
        

def equalize_bit_lists(bit_list1, bit_list2):

    if len(bit_list1) > len(bit_list2):

        for x in range(len(bit_list1)-len(bit_list2)):

            bit_list2.insert(0, 0)

    elif len(bit_list2) > len(bit_list1):

        for x in range(len(bit_list2)-len(bit_list1)):

            bit_list1.insert(0, 0)

    return bit_list1, bit_list2


def and_bitwise(bit_list1, bit_list2):

    bit_list1, bit_list2 = equalize_bit_lists(bit_list1, bit_list2)

    result = []

    for x in range(len(bit_list1)):

        if bit_list1[x] and bit_list2[x]:

            result.append(1)

        else:

            result.append(0)

    return result


def or_bitwise(bit_list1, bit_list2):

    bit_list1, bit_list2 = equalize_bit_lists(bit_list1, bit_list2)

    result = []

    for x in range(len(bit_list1)):

        if bit_list1[x] or bit_list2[x]:

            result.append(1)

        else:

            result.append(0)

    return result


def xor_bitwise(bit_list1, bit_list2):

    bit_list1, bit_list2 = equalize_bit_lists(bit_list1, bit_list2)

    result = []

    for x in range(len(bit_list1)):

        if (bit_list1[x] or bit_list2[x]) and not (bit_list1[x] and bit_list2[x]):

            result.append(1)

        else:

            result.append(0)

    return result


def right_shift(bit_list, nb):

    for x in range(nb):

        bit_list.insert(0, 0)

    return bit_list[:-nb]


def left_shift(bit_list, nb):

    for x in range(nb):

        bit_list.append(0)

    return bit_list[nb:]


def test():
    """
    ((1 << (1 << 3 | (i >> 3) | 7)) ^ i) >> 15
    """

    i = 0

    still = True

    while still:

        i += 1

        bit_list4 = right_shift(dec_to_bin(i, return_liste=1), 3)

        bit_list3 = or_bitwise(bit_list4, dec_to_bin(7, return_liste=1))

        bit_list2 = left_shift([1], 3)  # dec_to_bin(3, return_liste=1))

        nblis = or_bitwise(bit_list2, bit_list3)

        bit_list1 = left_shift([1], list_nb_to_int_nb(nblis))

        bitlist_0 = xor_bitwise(bit_list1, dec_to_bin(i, return_liste=1))

        val = right_shift(bitlist_0, 15)

        if (1 in val) or (i % 100 == 0):

            print(i, val)
