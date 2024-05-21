from typing import List


def situation_finale(n: int, m: int, villes: List[str], actions: List[str]) -> None:
    """
    :param n: le nombre de villes autour de Midgard
    :param m: le nombre d'années avant le Ragnarök
    :param villes: le nom des villes autour de Midgard, en partant de la queue de Jörmungandr

    :param actions: la liste des actions prochaines de Jörmungandr
    
    """

    def get_encoutered_villes(indice_start, deletes, followers):

        vs = []

        last_element = villes[indice_start]
        last_index = indice_start
        if not last_element in deletes:
                vs.append(last_element)

        for x in range(len(villes)):
            last_index = followers[last_index]
            last_element = villes[last_index]
            if not last_element in deletes:
                vs.append(last_element)
        return vs

    def print_ville(indice_start, deletes, reverse, followers):
        vs = get_encoutered_villes(indice_start, deletes, followers)
        if reverse == -1:
            vs.reverse()
        
        for v in vs:
            print(v)

    indice_start, followers, reverse = 0, [i+1 for i in range(len(villes))], 1
    pile_mangees = []

    for a in actions:
        if a == "A":
            indice_start += 1
            if indice_start >= len(villes):
                indice_start -= len(villes)
        elif a=="M":
            pile_mangees.append(villes[indice_start])
            indice_start += 1
            if indice_start >= len(villes):
                indice_start -= len(villes)
        elif a == "R":
            reverse *= -1
        elif a == "C":
            element = pile_mangees.pop()
            followers[element] = indice_start
            indice_start = element
            
    print_ville(indice_start, pile_mangees, reverse, followers)
        


if __name__ == "__main__":
    n = int(input())
    m = int(input())
    villes = [input() for _ in range(n)]
    actions = list(input())
    situation_finale(n, m, villes, actions)
