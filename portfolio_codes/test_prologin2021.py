##input()
##code = list(map(int, input().split()))
##
##
##if 65 <= code[0] <= 90:
##
##    inde = sum(code[1:])%26
##
##    inde_f = inde+code[0]
##
##    if inde_f > 90:
##
##        inde_f -= 26
##
##    print(chr(inde_f))
##
##else:
##
##    print(" ")


##nbr_famille = int(input())
##
##membre_par_famille = int(input())
##
##familles = []
##
##for x in range(nbr_famille):
##
##    familles.append(input())
##
##nbr_carte = int(input())
##
##main = input()
##
##scores = []
##
##for fam in familles:
##
##    cur_score = membre_par_famille
##
##    for car in fam:
##
##        if car in main:
##
##            cur_score -= 1
##
##    scores.append(cur_score)
##
##print(min(scores))



##class PathDown:
##
##    def __init__(self):
##
##        self.paths = [[[] for x in range(cols)] for y in range(2)]
##
##        PathDown.init_path(self)
##
##    def init_path(self):
##
##        for x in range(cols):
##
##            lifes = vies-grid[0][x]
##
##            if lifes:
##
##                self.paths[0][x] = [[x], lifes]
##
##    def down(self, y_cur_coor):
##
##        last_paths = self.paths[0]
##
##        for x_cor in range(len(last_paths)):
##
##            path_data = last_paths[x_cor]
##
##            if path_data != []:
##
##                path, path_life = path_data
##
##                if (x_cor > 0):
##
##                    lifes_would_be = path_life-grid[y_cur_coor+1][x_cor-1]
##
##                    if (lifes_would_be >= 0) and (self.paths[1][x_cor-1] == [] or self.paths[1][x_cor-1][1] < lifes_would_be):
##
##                        self.paths[1][x_cor-1] = [path+[x_cor-1], lifes_would_be]
##
##                if (x_cor < cols-1):
##
##                    lifes_would_be = path_life-grid[y_cur_coor+1][x_cor+1]
##
##                    if (lifes_would_be >= 0) and (self.paths[1][x_cor+1] == [] or self.paths[1][x_cor+1][1] < lifes_would_be):
##
##                        self.paths[1][x_cor+1] = [path+[x_cor+1], lifes_would_be]
##
##                lifes_would_be = path_life-grid[y_cur_coor+1][x_cor]
##
##
##                if (lifes_would_be >= 0) and (self.paths[1][x_cor] == [] or self.paths[1][x_cor][1] < lifes_would_be):
##
##                    self.paths[1][x_cor] = [path+[x_cor], lifes_would_be]
##
##        self.paths = self.paths[1:]
##
##        self.paths.append([[] for x in range(cols)])
##
##
##vies = int(input())
##
##lines = int(input())
##
##cols = int(input())
##
##grid = []
##
##for x in range(lines):
##
##    grid.append(list(map(int, input().split())))
##
##clas = PathDown()
##
##for x in range(lines-1):
##
##    clas.down(x)
##
##
##saved_path = "IMPOSSIBLE"
##
##min_ = -1
##
##for x in clas.paths[-2]:
##
##    if (x != []) and (x[1] > min_):
##
##        saved_path = x[0]
##
##        min_ = x[1]
##
##if saved_path == "IMPOSSIBLE":
##
##    print("IMPOSSIBLE")
##
##else:
##
##    print(*saved_path)
        
##best_score = -1
##
##best_path = "IMPOSSIBLE"
##
##cur_path = [0 for x in range(cols)]
##
##while (cur_path != [lines-1 for x in range(cols)]) and (best_score < vies):
##
##    cur_score = calc_score(cur_path)
##
##    print(cur_score)
##
##    if cur_score > best_score:
##
##        best_path = cur_path
##
##    cur_path = update_path(cur_path)
##
##print(best_path)



                    
##def calc_score(path):
##
##    score = 0
##
##    for y in path:
##
##        x = path[y]
##
##        score += grid[y][x]
##
##    return score
##
##
##def update_path(path):
##
##    changed = False
##
##    indx = -1
##
##    while not changed:
##
##        if path[indx] < lines-1:
##
##            changed = True
##
##            path[indx] += 1
##
##        else:
##
##            path[indx] = 0
##
##        indx -= 1
##
##        return path





"""
8
11
0 1
0 2
0 3
0 4
1 6
2 5
3 5
4 5
5 6
6 7
5 7
0
7

->
2
5 7
6 7


5
5
0 1
1 2
1 3
2 3
3 4
0
4

->
1
0 1 / 3 4


8
9
0 1
0 2
1 3
2 3
3 4
4 5
4 6
5 7
6 7
0
7

->
1
3 4

#
3
1
1 2
0
2

->
0
"""


def get_all_paths(grid, rome_index, other_index):
   
    snake_heads = [[rome_index]]
   
    paths = []
   
    while snake_heads != []:
       
        for indx in range(len(snake_heads)-1, -1, -1):

            path = snake_heads[indx]

            for x in grid[path[-1]]:
               
                if (x != rome_index) and (x not in path):
                   
                    if x == other_index:
                       
                        paths.append(path+[x])
                   
                    else:
                   
                        snake_heads.append(path+[x])
               
            del snake_heads[indx]
   
    return paths


def sub_list_in_list(sub, liste):

    if sub[0] in liste:

        rang = liste.index(sub[0])

        if rang == 0:

            if liste[1] == sub[1]:

                return True

        if rang == len(liste)-1:

            if liste[-2] == sub[1]:

                return True

        else:

            if (liste[rang-1] == sub[1]) or (liste[rang+1] == sub[1]):

                return True


def all_sub_paths(paths):

    sub_paths = []

    for path in paths:

        for indx in range(len(path)-1):

            n_sub = [path[indx], path[indx+1]]

            if (not n_sub in sub_paths) and (not n_sub[::-1] in sub_paths):

                sub_paths.append(n_sub)

    return sub_paths


town_nb = int(input())

path_nb = int(input())

path_grid = [[] for x in range(town_nb)]

for x in range(path_nb):

    t1, t2 = list(map(int, input().split()))

    path_grid[t1].append(t2)

    path_grid[t2].append(t1)

rome_index = int(input())

other_index = int(input())

paths = get_all_paths(path_grid, rome_index, other_index)

sub_paths = all_sub_paths(paths)

sub_pts = [0 for x in range(len(sub_paths))]

deleted_paths = []

while paths != []:

    to_del_subs = []

    for indx in range(len(sub_paths)):

        to_del_subs.append([])

        sub = sub_paths[indx]

        pts = 0

        for indx2 in range(len(paths)):

            liste = paths[indx2]

            if sub_list_in_list(sub, liste):

                pts += 1

                to_del_subs[-1].append(indx2)

        sub_pts[indx] += pts

    win_indx = sub_pts.index(max(sub_pts))

    to_del_subs[win_indx].sort(reverse=True)

    for to_del_indx in to_del_subs[win_indx]:

        del paths[to_del_indx]

    deleted_paths.append(sub_paths[win_indx])

    del sub_paths[win_indx]

    del sub_pts[win_indx]


print(len(deleted_paths))

for x in deleted_paths:

    print(*x)
