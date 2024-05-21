from pig_tv import *

import pickle

import os

"""

lorsque la souris passe sur une branche, afficher l'exercice ...
"""


class Fiche:

    def __init__(self, name, scores={}):

        self.name = name

        ## espace pour les differentes combinaisons, configurations d'exercices

        self.pull = ["normal_pull_ups", "biceps_pull_ups", "clapping_pull_ups", "archer_pull_ups", "tuck_front_pull_ups", "pull_over", "toes_to_bar", "dragon_flag", "dead_lift", "wind_mill", "bar_jumps", "muscle_ups_(kipping)", "muscle_ups_(full_force)", "skin_the_cat", "L-sit_pull_ups"]

        self.push = ["normal_push_ups", "diamond_push_ups", "clapping_push_ups", "balance_push_ups", "pseudo_planche_push_ups", "triceps_push_ups", "dips", "straight_dips", "squats", "pistol_squats"]

        self.hold = ["front_lever_hold", "front_lever_tuck_hold", "back_lever_hold", "plank", "side_plank", "hanging", "bar_L-sit", "dips_bars_L-sit", "floor_L-sit", "handstand", "elbow_lever", "full_planche", "semi_planche", "drapeau"]

        self.exercises = self.pull + self.push + self.hold

        self.exercises_config1 = [self.pull, self.push, self.hold]

        # Dans la configuration groupes musculaires, chaque exercice est reparti parmi les differents groupes musculaires qu'il mobilise, avec un total de 1 (pompes [0.5 bras, 0.35 pecs, 0.15 bas du dos])

        self.pecs = [["normal_push_ups", 0.3], ["diamond_push_ups", 0.4], ["clapping_push_ups", 0.3],
                     ["dips", 0.5], ["straight_dips", 0.5], ["back_lever_hold", 0.2], ["normal_pull_ups", 0.1],
                     ["biceps_pull_ups", 0.1], ["clapping_pull_ups", 0.1], ["archer_pull_ups", 0.1],
                     ["tuck_front_pull_ups", 0.05], ["pull_over", 0.15], ["dead_lift", 0.05], ["bar_jumps", 0.1],
                     ["muscle_ups_(kipping)", 0.1], ["muscle_ups_(full_force)", 0.15], ["skin_the_cat", 0.1],
                     ["L-sit_pull_ups", 0.05], ["balance_push_ups", 0.15], ["pseudo_planche_push_ups", 0.1],
                     ["front_lever_hold", 0.15], ["front_lever_tuck_hold", 0.2], ["dips_bars_L-sit", 0.1], ["floor_L-sit", 0.1], ]

        self.obliques = [["wind_mill", 0.3], ["side_plank", 0.4], ["drapeau", 0.2], ]

        self.abs = [["normal_push_ups", 0.1], ["diamond_push_ups", 0.1], ["normal_pull_ups", 0.05],
                    ["biceps_pull_ups", 0.05], ["clapping_pull_ups", 0.05], ["archer_pull_ups", 0.05], ["tuck_front_pull_ups", 0.15],
                    ["pull_over", 0.05], ["toes_to_bar", 0.15], ["dragon_flag", 0.15], ["dead_lift", 0.1], ["wind_mill", 0.1],
                    ["muscle_ups_(kipping)", 0.1], ["muscle_ups_(full_force)", 0.05], ["skin_the_cat", 0.1],
                    ["L-sit_pull_ups", 0.2], ["hanging", 0.1], ["balance_push_ups", 0.1], ["pseudo_planche_push_ups", 0.1],
                    ["triceps_push_ups", 0.1], ["squats", 0.1], ["pistol_squats", 0.05], ["front_lever_hold", 0.15],
                    ["front_lever_tuck_hold", 0.2], ["plank", 0.3], ["side_plank", 0.1], ["bar_L-sit", 0.25], ["dips_bars_L-sit", 0.25],
                    ["floor_L-sit", 0.35], ["handstand", 0.1], ["elbow_lever", 0.25], ["drapeau", 0.05], ]

        self.biceps = [["normal_push_ups", 0.15], ["diamond_push_ups", 0.25], ["clapping_push_ups", 0.3],
                       ["dips", 0.2], ["straight_dips", 0.2], ["back_lever_hold", 0.2], ["normal_pull_ups", 0.15],
                       ["biceps_pull_ups", 0.2], ["clapping_pull_ups", 0.15], ["archer_pull_ups", 0.25], ["tuck_front_pull_ups", 0.1],
                       ["pull_over", 0.2], ["toes_to_bar", 0.15], ["dragon_flag", 0.15], ["dead_lift", 0.1],
                       ["wind_mill", 0.1], ["bar_jumps", 0.3], ["muscle_ups_(kipping)", 0.2], ["muscle_ups_(full_force)", 0.2],
                       ["skin_the_cat", 0.2], ["L-sit_pull_ups", 0.15], ["hanging", 0.15], ["balance_push_ups", 0.25],
                       ["pseudo_planche_push_ups", 0.1], ["front_lever_hold", 0.1], ["front_lever_tuck_hold", 0.1], ["plank", 0.2],
                       ["side_plank", 0.1], ["bar_L-sit", 0.15], ["elbow_lever", 0.1], ]

        self.triceps = [["normal_push_ups", 0.05], ["diamond_push_ups", 0.1], ["clapping_push_ups", 0.3],
                        ["dips", 0.2], ["straight_dips", 0.2], ["normal_pull_ups", 0.1], ["biceps_pull_ups", 0.15],
                        ["clapping_pull_ups", 0.1], ["archer_pull_ups", 0.1], ["tuck_front_pull_ups", 0.1],
                        ["pull_over", 0.05], ["toes_to_bar", 0.1], ["bar_jumps", 0.1], ["muscle_ups_(kipping)", 0.2],
                        ["muscle_ups_(full_force)", 0.1], ["L-sit_pull_ups", 0.05], ["balance_push_ups", 0.1], ["triceps_push_ups", 0.4],
                        ["squats", 0.1], ["dips_bars_L-sit", 0.15], ["floor_L-sit", 0.2], ["drapeau", 0.1], ]

        self.fore_arms = [["normal_push_ups", 0.1], ["normal_pull_ups", 0.2], ["biceps_pull_ups", 0.2],
                          ["clapping_pull_ups", 0.2], ["archer_pull_ups", 0.25], ["tuck_front_pull_ups", 0.05],
                          ["pull_over", 0.1], ["dead_lift", 0.05], ["wind_mill", 0.1], ["bar_jumps", 0.2],
                          ["muscle_ups_(kipping)", 0.1], ["muscle_ups_(full_force)", 0.2], ["skin_the_cat", 0.3],
                          ["L-sit_pull_ups", 0.1], ["hanging", 0.45], ["balance_push_ups", 0.2], ["pseudo_planche_push_ups", 0.4],
                          ["triceps_push_ups", 0.2], ["front_lever_hold", 0.1], ["front_lever_tuck_hold", 0.1],
                          ["bar_L-sit", 0.15], ["dips_bars_L-sit", 0.15], ["handstand", 0.4], ["elbow_lever", 0.4], ["drapeau", 0.15], ]

        self.shoulders = [["normal_push_ups", 0.1], ["diamond_push_ups", 0.05], ["clapping_push_ups", 0.1], ["dips", 0.1],
                          ["straight_dips", 0.1], ["back_lever_hold", 0.2], ["normal_pull_ups", 0.2], ["biceps_pull_ups", 0.15],
                          ["clapping_pull_ups", 0.2], ["archer_pull_ups", 0.1], ["tuck_front_pull_ups", 0.2],
                          ["pull_over", 0.2], ["toes_to_bar", 0.35], ["dragon_flag", 0.1], ["dead_lift", 0.2],
                          ["wind_mill", 0.2], ["bar_jumps", 0.3], ["muscle_ups_(kipping)", 0.2],
                          ["muscle_ups_(full_force)", 0.2], ["skin_the_cat", 0.3], ["L-sit_pull_ups", 0.1], ["hanging", 0.3],
                          ["balance_push_ups", 0.2], ["pseudo_planche_push_ups", 0.2], ["triceps_push_ups", 0.2],
                          ["front_lever_hold", 0.1], ["front_lever_tuck_hold", 0.1], ["plank", 0.05],
                          ["side_plank", 0.1], ["bar_L-sit", 0.2], ["dips_bars_L-sit", 0.1],
                          ["handstand", 0.4], ["elbow_lever", 0.15], ["drapeau", 0.2], ]

        self.lower_back = [["normal_push_ups", 0.15], ["diamond_push_ups", 0.1], ["back_lever_hold", 0.2],
                           ["tuck_front_pull_ups", 0.1],
                           ["pull_over", 0.1], ["dragon_flag", 0.4], ["dead_lift", 0.15], ["wind_mill", 0.1],
                           ["L-sit_pull_ups", 0.1], ["pseudo_planche_push_ups", 0.1], ["triceps_push_ups", 0.1],
                           ["plank", 0.2], ["side_plank", 0.1], ]

        self.upper_back = [["back_lever_hold", 0.2], ["normal_pull_ups", 0.2], ["biceps_pull_ups", 0.15],
                           ["clapping_pull_ups", 0.2], ["archer_pull_ups", 0.15], ["tuck_front_pull_ups", 0.2],
                           ["pull_over", 0.1], ["dead_lift", 0.25], ["front_lever_hold", 0.25],
                           ["front_lever_tuck_hold", 0.25], ["handstand", 0.05], ["drapeau", 0.1], ]

        self.glutes = [["normal_push_ups", 0.05], ["tuck_front_pull_ups", 0.05], ["dragon_flag", 0.1],
                       ["dead_lift", 0.1], ["squats", 0.3], ["pistol_squats", 0.15], ["front_lever_hold", 0.05],
                       ["front_lever_tuck_hold", 0.05], ["plank", 0.2], ["side_plank", 0.1], ["handstand", 0.05],
                       ["elbow_lever", 0.1], ["drapeau", 0.1], ]

        self.legs = [["pull_over", 0.05], ["toes_to_bar", 0.25], ["dragon_flag", 0.1], ["wind_mill", 0.1],
                     ["muscle_ups_(kipping)", 0.1], ["muscle_ups_(full_force)", 0.1], ["L-sit_pull_ups", 0.25],
                     ["squats", 0.5], ["pistol_squats", 0.8], ["front_lever_hold", 0.1], ["plank", 0.05],
                     ["side_plank", 0.1], ["bar_L-sit", 0.25], ["dips_bars_L-sit", 0.25], ["floor_L-sit", 0.35], ["drapeau", 0.1], ]

        self.front_core = [self.pecs, self.abs, self.obliques]

        self.arms = [self.biceps, self.triceps, self.fore_arms, self.shoulders]

        self.back = [self.lower_back, self.upper_back]

        self.lower_body = [self.glutes, self.legs]

        self.exercises_config2 = [self.front_core, self.arms, self.back, self.lower_body]

        test = 0

        if test:

            for exo in self.exercises:

                used = 0

                for liste in self.exercises_config2:

                   for sous_liste in liste:

                       for item in sous_liste:

                           if item[0] == exo:

                               used += item[1]

                print(exo, used)

        ##
        # initialisation des records de la fiche joueur

        if scores == {}:

            self.scores = scores

            print("Veuillez entrer vos performance pour chacun des exercices suivants:\n[En nombre de répétitions pour les dynamiques, en secondes pour les statiques]\n")

            for x in range(len(self.exercises)):

                print(self.exercises[x], " :\n")

                self.scores[self.exercises[x]] = float(input())

            print("User initialised\n")

            Fiche.save_stats(self)

            print("User saved\n")


        else:

            self.scores = scores

            modified = 0

            keys = list(self.scores.keys())

            for key in keys:  # checks if an exercise has not been deleted

                if not key in self.exercises:

                    del self.scores[key]

                    modified = 1

            for exercise in self.exercises:

                if not exercise in self.scores.keys():  # a new exercise has been added

                    print("\nA new exercise stat is needed for {}.\nPlease enter your record for the {}.\n".format(self.name, exercise))

                    self.scores[exercise] = float(input())

                    modified = 1

            if modified:

                Fiche.save_stats(self)

    def save_stats(self):

        file = open("workout_ids/"+str(self.name)+".txt", "wb")

        pickle.dump(self.scores, file)

    def print_stats(self):

        c = 0

        for x in self.exercises:

            c += 1

            print("Exercice {} ({}) : record personnel : {}".format(c, x, self.scores[x]))

    def modify(self):

        play = True

        while play:

            choix = invite([["1", "Change name"], ["2", "Change exercise record"], ["3", "Save modifications and go back to menu"], ["4", "Fast multiple record changes"]])

            if choix == 0:

                to_remove_name = self.name

                self.name = input("New name:\n")

                Fiche.save_stats(self)

                os.remove("workout_ids/"+to_remove_name+".txt")

                print("New name saved")

            elif choix == 1:

                choix1 = invite([["1", "Change pull exercise record"], ["2", "Change push exercise record"], ["3", "Change hold exercise record"]])

                liste = self.exercises_config1[choix1]

                choix2 = invite([[x, "{} [{}]".format(liste[x], self.scores[liste[x]])] for x in range(len(liste))])

                to_change_exo = self.exercises_config1[choix1][choix2]

    ##            index_ = choix2
    ##
    ##            for x in range(choix1-1):
    ##
    ##                index_ += len(self.exercises_config1[x])

                new_record = float(input("Your last record was {}.\nNew record:\n".format(self.scores[to_change_exo])))

                self.scores[to_change_exo] = new_record

                os.remove("workout_ids/"+self.name+".txt")

                Fiche.save_stats(self)

                print("New record saved")

            elif choix == 2:

                play = False

            elif choix == 3:

                Fiche.change_records(self)

    def change_records(self):

        play = True

        while play:

            print("\nPut part of exercise name, or \"!\" to exit\n")

            inpt = input()

            if inpt == "!":

                return

            else:

                c = 1

                liste = []

                dico_corres = {}

                for x in range(len(self.exercises)):

                    if inpt in self.exercises[x]:

                        liste.append([c, "{} [{}]".format(self.exercises[x], self.scores[self.exercises[x]])])

                        dico_corres[c] = x

                        c += 1

                if liste != []:

                    liste.append([len(liste)+1, "Choisir un nouvel exercice"])

                    choix = invite(liste)+1

                    if not (choix == len(liste)):

                        to_change_exo = self.exercises[dico_corres[choix]]

                        new_record = float(input("Your last record was {}.\nNew record:\n".format(self.scores[to_change_exo])))

                        self.scores[to_change_exo] = new_record

                        os.remove("workout_ids/"+self.name+".txt")

                        Fiche.save_stats(self)

                        print("New record saved")

                else:

                    print("No exercise found")


class Star:

    def __init__(self, fiche, record):

        # data part

        self.fiche = fiche  # array containing relative stregth in each exercise of an id

        self.record = record  # records between all users

        self.force = [1 for x in range(len(self.fiche.exercises))]

        self.explosivite = []

        self.endurance = []

        self.equilibre = []

        self.coefs = [self.force, self.explosivite, self.endurance, self.equilibre]  # goes from zero to one

        # star settings

        self.mode = 0

        # drawing part

        self.circle_radius = int(min(screen_width, screen_height)*(9/19))  # a bit smaller than half of screen

        self.colors = [RED, ORANGE, BLUE, GREEN]

        self.star_start_const = .15

    def draw_branche(self, angle, width_angle, lenght, color=None):

        if color == None:

            color = self.colors[self.mode]

        branch_extrema = sum_arrays(screen_center, [cos(angle)*self.circle_radius*lenght, sin(angle)*self.circle_radius*lenght])

        branch_sides = []

        branch_sides.append(sum_arrays(screen_center, [cos(angle+width_angle)*self.circle_radius*self.star_start_const, sin(angle+width_angle)*self.circle_radius*self.star_start_const]))

        branch_sides.append(sum_arrays(screen_center, [cos(angle-width_angle)*self.circle_radius*self.star_start_const, sin(angle-width_angle)*self.circle_radius*self.star_start_const]))

        pygame.draw.polygon(screen, color, [screen_center, branch_sides[0], branch_extrema, branch_sides[1]])

    def draw(self):

        pygame.draw.circle(screen, self.colors[self.mode], screen_center, self.circle_radius//8)

        mode = 2

        if mode == 1:  # met en valeur une capacité (force, explosivite...) en creant une branche par exercice

            branch_nb = 0

            coefs = self.coefs[self.mode]

            for x in coefs:

                branch_nb += ceil(x)  # not 0

            exercise_intervalle = (2*pi)/branch_nb

            angle = 0

            c = 0

            for exo in self.fiche.exercises:

                branch_width = coefs[c]

                c += 1

                if branch_width and self.record.scores[exo]:

                    branch_lenght = self.fiche.scores[exo]/self.record.scores[exo]  # between 0 and 1

                    branch_width_angle = (exercise_intervalle/2)*branch_width

                    Star.draw_branche(self, angle, branch_width_angle, 1, LIGHT_GREY)

                    Star.draw_branche(self, angle, branch_width_angle, branch_lenght)

                    angle += exercise_intervalle

        elif mode == 2:  # cree une etoile a 3 branches, regroupe les exercices selon s'ils sont pull, push ou hold

            branch_nb = len(self.fiche.exercises_config1)

            angle = 0

            exercise_intervalle = (2*pi)/branch_nb

            for liste in self.fiche.exercises_config1:

                total_liste = 0

                for exo in liste:

                    if self.record.scores[exo] > 0:  # check for division

                        total_liste += (self.fiche.scores[exo]/self.record.scores[exo])

                total_liste /= len(liste)

                branch_width_angle = (exercise_intervalle/2)

                Star.draw_branche(self, angle, branch_width_angle, 1, LIGHT_GREY)

                Star.draw_branche(self, angle, branch_width_angle, total_liste)

                angle += exercise_intervalle


def aff_star(fiche, record):

    play = True

    star = Star(fiche, record)

    screen.fill(BLACK)

    star.draw()

    pygame.display.update()

    wait()

##    while play:
##
##        for event in pygame.event.get():
##
##            if event.type == pygame.QUIT:
##
##                play = False
##
##            elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):
##
##                clicking = 1
##
##            elif (event.type == pygame.MOUSEBUTTONUP) and (event.button == 1):
##
##                clicking = 0
##
##            elif (event.type == pygame.MOUSEMOTION):
##
##                translation = event.rel
##
##            elif event.type == pygame.KEYDOWN:
##
##                if event.key == pygame.K_LEFT:
##
##                    pass
##
##        pygame.display.update()
##
##        clock.tick(60)


def load_users():

    users = []

    for x in os.listdir("workout_ids"):

        if not x == "record.txt":

            scores = pickle.load(open("workout_ids/"+x, "rb"))

            users.append(Fiche(x[:-4], scores))

    if users != []: # creation de la fiche Record (records parmi tout les utilisateurs)

        dico_records = {}

        for exo in users[0].exercises:

            record = max([users[u].scores[exo] for u in range(len(users))])

            dico_records[exo] = record

        users.append(Fiche("record", dico_records))

    return users


def main():

    play = True

    users = load_users()

    while play:

        print("\n\nMenu\n\n")

        choix = invite([["1", "Load saved users"], ["2", "save new user"], ["3", "draw user star"], ["4", "Display loaded users"], ["5", "Modify loaded user"], [6, "Display loaded user records"]])

        if choix == 0:

            users = load_users()

            print("Saved users were succesfully loaded\n")

        elif choix == 1:

            users.append(Fiche(input("Enter your name:\n"), {}))

            print("New user loaded")

            users = load_users()

        elif choix == 2:

            if users == []:

                print("No users loaded")

            else:

                choix = invite([[str(x), users[x].name] for x in range(len(users))])

                aff_star(users[choix], users[-1])

        elif choix == 3:

            if users == []:

                print("No users loaded")

            else:

                print("Displaying loaded users:\n")

                for x in range(len(users)):

                    user = users[x]

                    print(str(x+1)+" : "+user.name)

        elif choix == 4:

            if users == []:

                print("No users loaded")

            else:

                choix = invite([[str(x), users[x].name] for x in range(len(users))])

                users[choix].modify()

                users = load_users()

        elif choix == 5:

            if users == []:

                print("No users loaded")

            else:

                choix = invite([[str(x), users[x].name] for x in range(len(users))])

                users[choix].print_stats()


if __name__ == "__main__":

    main()
