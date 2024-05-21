
def other_color(color):
    if color == 1:
        return 2
    return 1

def chemin_valide(n: int, dieux):
    arretes = [[0 for i in range(n)] for j in range(n)]

    sommets = [i for i in range(n)]
    c = 0

    for dieu in dieux:
        prenom, nom = dieu.split()
        v = 0
        for dieu2 in dieux:
            if dieu2 != dieu:
                prenom2, nom2 = dieu2.split()
                if prenom == prenom2:
                    arretes[c][v] = 1
                elif nom == nom2:
                    arretes[v][c] = 2
            v += 1
        c += 1

##    # colors of vertices
##    vertices_color = [0 for x in range(n)]
##    red_indices = []
##    blue_indices = []
##    start = None
##
##    for i in range(n):
##        red_nei = 1 in arretes[i]
##        blue_nei = 2 in arretes[i]
##        if red_nei:
##            if blue_nei:
##                vertices_color[i] = 3
##            else:
##                vertices_color[i] = 1
##                red_indices.append(i)
##        elif blue_nei:
##            vertices_color[i] = 2
##            blue_indices.append(i)
##        else:
##            return False  # pas connexe

##    # colors force special parcours
##    if len(blue_indices) + len(red_indices) > 2:
##        return False
##
##    if (len(blue_indices) == 2 or len(red_indices) == 2):
##        if n%2==1:
##            return False
##        else:
##            
##            if len(blue_indices) == 2:
##                start = blue_indices[0]
##                end = blue_indices[1]
##            else:
##                start = red_indices[0]
##                end = red_indices[1]
##    if (len(blue_indices) == 1 and len(red_indices) == 1):
##        if (n%2==0):
##            return False
##        else:
##            start = blue_indices[0]
##            end = red_indices[0]

    def get_neis_except(vertex, link_color, except_vertices):
        neis = []
        for j in range(n):
            if not j in except_vertices:
                if arretes[vertex][j] == link_color:
                    neis.append(j)
        return neis

    def try_parcours(current_vertex, visited_vertices, next_color):
        #print(current_vertex, visited_vertices, next_color)
        visited_vertices.append(current_vertex)
        if len(visited_vertices) == n:
            return visited_vertices  # ordonne

        possible_neighbors = get_neis_except(current_vertex, next_color, visited_vertices)
        #print(possible_neighbors)
        if possible_neighbors == []:
            del visited_vertices[-1]
            return False
        else:
            for nei in possible_neighbors:
                return_val = try_parcours(nei, visited_vertices, other_color(next_color))
                if return_val:
                    return return_val

    for vertex in sommets:
        for color in [1, 2]:
            liste = try_parcours(vertex, [], color)
            if liste:
                for dieu in [dieux[i] for i in liste]:
                    print(dieu)
                return True



if __name__ == "__main__":
    n = int(input())
    dieux = [input() for _ in range(n)]  # sommets du grph  # arretes

    if not chemin_valide(n, dieux):
        print("IMPOSSIBLE")




