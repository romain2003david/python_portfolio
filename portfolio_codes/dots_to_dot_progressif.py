from pig_tv import *


class Population:

    def __init__(self, pop_size, dna_size, max_dna_len, dna_add, largeur_barriere):

        self.largeur_barriere = largeur_barriere

        self.taille_population = pop_size

        self.pop = [Entitee(0, largeur_barriere, dna_size) for x in range(self.taille_population)]

        self.fitness = []

        self.max_dna_len = max_dna_len

        self.dna_add = dna_add

    def update(self, target, compteur, barrieres, obstacles):

        a = 0
        c = 0
        for dot in self.pop:
            b = dot.update(target, compteur, barrieres, obstacles)
            if b:
                if b == -1:
                    a = 1
                else:
                    c += b
        if c == len(self.pop):
            return -1
        return a

    def draw(self):

        for dot in self.pop:
            dot.draw()

    def evaluate(self, target):

        self.fitness = []

        for dot in self.pop:

            if dot.but != 0:
                fit = dot.but * 2

            elif not dot.hurt:
                fit = 1 / sqrt((target.x - dot.x)**2 + (target.y - dot.y)**2)

            else:
                if dot.hurt == 4:
                    fit = 1 / sqrt((target.x - dot.x)**2 + (target.y - dot.y)**2) / 4
                else:
                    fit = 1 / sqrt((target.x - dot.x)**2 + (target.y - dot.y)**2) / 20

            self.fitness.append([fit, dot.genes])

    def evoluer(self):

        total = 0
        npop = []

        for nbr in self.fitness:
            total += nbr[0]

        for nbr in self.fitness:
            nbr[0] = round(nbr[0]/total, 3)

        for entit in self.pop:

            rmoderateur = random.randint(0, 1000) / 1000
            compteur = -1
            if not self.pop.index(entit) == len(self.pop)-1:  # On garde la meilleure production de chaque generation pour la generation suivante
                choix = None
                while choix == None:
                    compteur +=1
                    try:
                        rmoderateur -= self.fitness[compteur][0]
                        if rmoderateur <= 0:
                            choix = compteur
                    except:
                        choix = -1

                parent = self.fitness[choix][1]

                n_entit = Entitee(parent.dna.copy(), self.largeur_barriere)
                for index in range(len(n_entit.genes.dna)):
                    if random.randint(0, 1000) == 0:
                        n_entit.genes.dna[index] = [random.randint((-self.largeur_barriere+1)/2, self.largeur_barriere-1), random.randint(-self.largeur_barriere+1, self.largeur_barriere-1)]
                npop.append(n_entit)

        npop.append(Entitee(self.fitness[self.fitness.index(max(self.fitness, key=lambda x: x[0]))][1].dna, (100, 100, 255), self.largeur_barriere))

        if len(npop[0].genes.dna) < self.max_dna_len:

            pop_add = self.dna_add

            for index in range(len(npop)):

                for compteur in range(pop_add):

                    npop[index].genes.dna.append([random.randint((-self.largeur_barriere+1)/2, self.largeur_barriere-1), random.randint(-self.largeur_barriere+1, self.largeur_barriere-1)])

        self.pop = npop            


class Barriere:

    def __init__(self, screen, x, y, largeur, hauteur):

        self.screen = screen

        self.x = x
        self.y = y
        self.largeur = largeur
        self.hauteur = hauteur

        self.rectangle = pygame.Rect(self.x, self.y, self.largeur, self.hauteur)

    def draw(self):

        pygame.draw.rect(self.screen, (0, 0, 0), self.rectangle)


class ObstacleMouvant:

        def __init__(self, screen, x, y, translation_x, translation_y, vitesse):

            self.screen = screen
            self.cote = 50

            self.vitesse = vitesse

            self.translation_x = translation_x
            self.translation_y = translation_y

            self.x_init = x*1
            self.y_init = y*1

            self.x = x
            self.y = y
            self.x2 = x+translation_x
            self.y2 = y+translation_y

            if translation_x == 0:
                self.add_x = 0
            else:
                self.add_x = vitesse

            if translation_y == 0:
                self.add_y = 0
            else:
                self.add_y = vitesse

        def update(self):

            self.x += self.add_x
            self.y += self.add_y

            if self.x2 > self.x_init:
                if not self.x in range(self.x_init+1, self.x2):

                    self.add_x *= -1
                    self.x += self.add_x
            elif not self.x in range(self.x2, self.x_init+1):
                self.add_x *= -1
                self.x += self.add_x

            if self.y2 > self.y_init:
                if not self.y in range(self.y_init+1, self.y2):
                    self.add_y *= -1
                    self.y += self.add_y
            elif not self.y in range(self.y2, self.y_init+1):
                self.add_y *= -1
                self.y += self.add_y

        def draw(self):

            rectangle = pygame.Rect(self.x, self.y, self.cote, self.cote)
            pygame.draw.rect(self.screen, (200, 0, 0), rectangle)


class Entitee:

    def __init__(self, genes, largeur_barriere, dna_size=0, color=(160, 160, 160)):

        self.x = int(screen_width / 2)

        self.y = int(screen_height)

        self.rayon = 10
        self.color = color

        self.but = 0

        self.injuries = [(255, 0, 0), (255, 230, 150), (90, 60, 40), (200, 200, 255)]
        self.hurt = 0

        taille_dna = dna_size

        if genes:  # sets the genes to those given in input

            self.genes = DNA(genes)

        else:  # if no input genes, defines random genes

            self.genes = DNA([[random.randint((-largeur_barriere+1)/2, largeur_barriere-1), random.randint(-largeur_barriere+1, largeur_barriere-1)] for x in range(taille_dna)])

    def update(self, target, compteur, barrieres, obstacles):

        if (self.but == 0) and (not(self.hurt)):
            self.x += self.genes.dna[compteur][1]
            self.y += self.genes.dna[compteur][0] * -1

            for bar in barrieres:
                if bar.rectangle.colliderect(pygame.Rect(self.x-self.rayon, self.y-self.rayon, 2*self.rayon, 2*self.rayon)):
                    self.hurt = 1

            for obs in obstacles:
                obs_rect = pygame.Rect(obs.x, obs.y, obs.cote, obs.cote)
                if obs_rect.colliderect(pygame.Rect(self.x-self.rayon, self.y-self.rayon, 2*self.rayon, 2*self.rayon)):
                    self.hurt = 2

            if (self.x-self.rayon < 0) or (self.x+self.rayon > screen_width) or (self.y+self.rayon > screen_height):
                self.hurt = 3

            elif (self.y-self.rayon < 0):
                self.hurt = 4

            distance_target = sqrt((target.x - self.x)**2 + (target.y - self.y)**2)
            if self.rayon + target.rayon > distance_target:  # Le dot touche l'objectif
                self.but = 1+(1/ compteur/400)
                return -1
        else:
            return 1

    def draw(self):

        if self.hurt:
            pygame.draw.circle(screen, self.injuries[self.hurt-1], (self.x, self.y), self.rayon)
        elif self.but:
            pygame.draw.circle(screen, (0, 0, 255), (self.x, self.y), self.rayon)
        else:
            pygame.draw.circle(screen, self.color, (self.x, self.y), self.rayon)


class Target:

    def __init__(self, screen):

        self.x = int(screen_width / 2)
        self. y = int(screen_height / 15)

        self.screen = screen
        self.rayon = 20

    def draw(self):

        pygame.draw.circle(self.screen, (0, 150, 0), (self.x, self.y), self.rayon)


class DNA:

    def __init__(self, genes):

        self.dna = genes

    def aff(self, fit, indx):

##        for liste in self.dna:
##            for item in liste:
##                if self.dna.index(liste) == 0:
##                    print("Barriere :")
##                    print("coor x : {}.\ncoor y : {}.\nlargeur : {}.\nlongueur : {}.\n".format(item.x, item.y, item.largeur, item.hauteur))
##                else:
##                    print("Obstacle mouvant :")
##                    print("coor x : {}.\ncoor y : {}.\ndeplacement x : {}.\ndeplacement y : {}.\nvitesse : {}.\n".format(item.x, item.y, item.translation_x, item.translation_y, item.vitesse))
        print("Fitness : {}\nIndex : {}".format(fit, indx))
        for liste in self.dna:
            for item in liste:
                if self.dna.index(liste) == 0:
                    print("Barriere(screen, {}, {}, {}, {})".format(item.x, item.y, item.largeur, item.hauteur))
                else:
                    print("ObstacleMouvant(screen, {}, {}, {}, {}, {})".format(item.x, item.y, item.translation_x, item.translation_y, item.vitesse))



def run_pop(population, barrieres, obstacles, show, generation, terrain_evolution):
    """ effectue une generation de dots """

    jeu = True

    target = Target(screen)

    for obs in obstacles:

        obs.x = obs.x_init

        obs.y = obs.y_init

    non_button = Button("Non", 0, (255, 0, 0), screen)
    oui_button = Button("Oui", 1, (0, 255, 0), screen)
    button1 = Button("1", 2, (255, 80, 0), screen, 15)
    button2 = Button("2", 3, (255, 155, 0), screen, 25)
    button3 = Button("3", 4, (255, 255, 0), screen, 42)

    buttons = [oui_button, non_button, button1, button2, button3]

    taille_dna = len(population.pop[0].genes.dna)
    print("taille de l'ADN", taille_dna, end=" ; ")
    for compteur in range(0, taille_dna):

        for event in pygame.event.get():
            if event.type == QUIT:
                print("stop")
                return 1

            elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):

                mouse_pos = pygame.mouse.get_pos()

                if terrain_evolution:  # when you evolve terrains only

                    for item in buttons:

                        if item.clicked(mouse_pos):

                            return item.value

        # calcul
        for obstacle in obstacles:
            obstacle.update()

        fin = population.update(target, compteur, barrieres, obstacles)
        #if fin == 1:
         #   return 1

        if fin == -1:

            population.evaluate(target)

            return 0

        # dessin
        if show:

            screen.fill((255, 255, 255))

            if terrain_evolution:

                for bout in buttons:
                    bout.draw()

            target.draw()

            for barriere in barrieres:

                barriere.draw()

            for obstacle in obstacles:

                obstacle.draw()

            population.draw()

            aff_txt("Generation : {}".format(generation), 0, 0, (0, 0, 0))

            aff_txt("Pop lenght : {}".format(population.taille_population), 0, 50, (0, 0, 0))

            aff_txt("DNA lenght : {}".format(taille_dna), 0, 100, (0, 0, 0))

            pygame.display.update()

            clock.tick(100)

    population.evaluate(target)


def terrain0(largeur_barriere):

    return [], []


def terrain1(largeur_barriere):

    barrieres = []

    barriere = Barriere(screen, int(screen_width/3), int(screen_height/2), int(screen_width/3)*2, largeur_barriere)
    barrieres.append(barriere)

    barriere = Barriere(screen, 0, int(screen_height/5), int(screen_width/2), largeur_barriere)
    barrieres.append(barriere)

    barriere = Barriere(screen, int(screen_width/2), int(screen_height/5)-10, largeur_barriere, 80)
    barrieres.append(barriere)

    obstacles = []

    obstacle = ObstacleMouvant(screen, int(screen_width/3), int(screen_height/3), 150, 0, 3)
    obstacles.append(obstacle)

    return barrieres, obstacles


def terrain2(largeur_barriere):

    barrieres = []

    barriere = Barriere(screen, int(screen_width/4), int(screen_height/2), int(screen_width/2), largeur_barriere)
    barrieres.append(barriere)

    obstacles = []

    obstacle = ObstacleMouvant(screen, 0, int(screen_height)-200, screen_width, 0, 10)
    obstacles.append(obstacle)

    obstacle = ObstacleMouvant(screen, screen_width-50, int(screen_height)-200, -screen_width+50, 0, 10)
    obstacles.append(obstacle)

    obstacle = ObstacleMouvant(screen, int(screen_width/2), int(screen_height/3)+30, int(screen_width/2)-50, 0, 5)
    obstacles.append(obstacle)

    obstacle = ObstacleMouvant(screen, int(screen_width/2), int(screen_height/3)+30, (int(screen_width/2)-50)*-1, 0, 5)
    obstacles.append(obstacle)

    obstacle = ObstacleMouvant(screen, int(screen_width/2)-100, 0, 0, int(screen_height/3), 5)
    obstacles.append(obstacle)

    obstacle = ObstacleMouvant(screen, int(screen_width/2)+100, 0, 0, int(screen_height/3), 5)
    obstacles.append(obstacle)

    obstacle = ObstacleMouvant(screen, int(screen_height/3)*2, 120, -(int(screen_height/3)), 0, 8)
    obstacles.append(obstacle)

    obstacle = ObstacleMouvant(screen, int(screen_height/3), 200, int(screen_height/3), 0, 8)
    obstacles.append(obstacle)
    

    return barrieres, obstacles


def terrain3(largeur_barriere):

    barrieres = []

    obstacles = []

    for y in range(6):

            if y%2 == 1:
                add = 50
            else:
                add = 0

            for x in range(3):

                obstacle = ObstacleMouvant(screen, int(add+x*(screen_width/3)), 50 +y*100, int(screen_width/4) + add, 100, 40)
                obstacles.append(obstacle)


    return barrieres, obstacles


def terrain4(largeur_barriere):

    barrieres = []

    obstacles = []

    for y in range(5):

            if y%2 == 1:
                add = 200
                add2 = 0
            else:
                add = 0
                add2 = -200

            barriere = Barriere(screen, add, 150 +y*100, screen_width + add2, largeur_barriere)
            barrieres.append(barriere)


    return barrieres, obstacles

def terrain5(largeur_barriere):

    barrieres = []

    obstacles = []

    for y in range(2):

        if y%2 == 1:
            add = -100
        else:
            add = 100

        barriere = Barriere(screen, int(screen_width/2+add), 0, largeur_barriere, screen_height)
        barrieres.append(barriere)

    for y in range(3):

        if y%2 == 1:
            add = -100
        else:
            add = 100

        obs = ObstacleMouvant(screen, int(screen_width/2-120), 80+y*200, 240, 0, y*-3+20)
        obstacles.append(obs)

    obs = ObstacleMouvant(screen, int(screen_width/2-120), 100, 240, screen_height-100, 30)
    obstacles.append(obs)    


    return barrieres, obstacles    


class Button:

    def __init__(self, name, index, color, screen, valeur=0):

        self.name = name
        self.index = index
        if valeur:
            self.value = valeur
        else:
            self.value = index*50 or 1

        self.screen = screen

        self.x = screen_width - 110
        self.y = index*110 + 10

        self.largeur = 100
        self.hauteur = 100

        self.bouton = pygame.Rect(self.x, self.y, self.largeur, self.hauteur)

        self.color = color
        self.color_bar = []
        for x in color:
            self.color_bar.append((x-255)*-1)

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.bouton)
        aff_txt(self.name, self.x+10, self.y+10, color=self.color_bar)
        

    def clicked(self, pos):
        """ Si le bouton est appuye, active la fonction """
        return (self.bouton.collidepoint(pos))



## terrain evolution



class PopTerrain:

    def __init__(self, screen, taille_population):

        self.taille_population = taille_population
        self.screen = screen
        self.pop = [Terrain(screen, 0) for x in range(self.taille_population)]
        self.fitness = []

    def evaluate(self):

        self.fitness = []
        max_frames = 50

        for ter in self.pop:
            if ter.fit > max_frames:
                ter.fit -= max_frames
            ter.fit /= max_frames
            ter.fit = round(ter.fit, 3)

            self.fitness.append([ter.fit, ter.genes])

        summ = 0
        for fit in self.fitness:
            summ += fit[0]

        if summ == 0:
            summ = 0.01

        for indx in range(len(self.fitness)):
            self.fitness[indx][0] /= summ
            self.pop[indx].fit = self.fitness[indx][0]

    def evoluer(self):

        npop = []

        for k in range(len(self.pop)):
            self.pop[k].genes.aff(self.pop[k].fit, k)

        for loop in range(len(self.pop)):

            rmoderateur = random.randint(0, 1000) / 1000
            parent = []

            for x in range(2):
                compteur = -1
                choix = None
                while choix == None:
                    compteur +=1
                    try:
                        rmoderateur -= self.fitness[compteur][0]
                        if rmoderateur <= 0:
                            choix = compteur
                    except:
                        choix = -1

                parent.append(self.fitness[choix][1])

            if parent[0] == parent[1]:
                parent[1] = self.fitness[random.randint(0, len(self.pop))][1]

            separation1 = int(len(parent[0].dna[0])/2)
            separation2 = int(len(parent[0].dna[1])/2)
            n_ter = Terrain(self.screen, [parent[0].dna[0][:separation1]+parent[1].dna[0][separation1:], parent[0].dna[1][:separation2]+parent[1].dna[1][separation2:]])

            for liste in range(len(n_ter.genes.dna)):
                for index in range(len(n_ter.genes.dna[liste])):
                    if random.randint(0, 10) == 0:
                        if liste == 0:
                            vh = random.randint(0, 1)
                            xpos = random.randint(0, screen_width)
                            ypos = random.randint(0, screen_height)

                            if vh:
                                n_ter.genes.dna[liste][index] = Barriere(screen, xpos, ypos, random.randint(0, screen_width-ypos), 10)
                            else:
                                n_ter.genes.dna[liste][index] = Barriere(screen, xpos, ypos, 10, random.randint(0, screen_height))

                        else:
                            xpos = random.randint(0, screen_width)
                            ypos = random.randint(0, screen_height)

                            n_ter.genes.dna[liste][index] = ObstacleMouvant(screen, xpos, ypos, random.randint(0, screen_width-ypos), random.randint(0, screen_height-ypos), random.randint(2, 20))

            npop.append(n_ter)

        self.pop = npop

    def aff_final(self):

        for ter in self.pop:
            ter.fit = self.fitness[self.pop.index(ter)][0]

        self.pop.sort(key=lambda x:x.fit)

        print("\n\nGenerations finales :\n\n")
        for ter in self.pop:
            ter.genes.aff(ter.fit, self.pop.index(ter))



class Terrain:

    def __init__(self, screen, genes):

        self.fit = None
        if genes:
            self.genes = DNA(genes)

        else:
            self.genes = [[], []]
            nbr_bar = random.randint(0, 6)

            for x in range(nbr_bar):
                vh = random.randint(0, 1)
                xpos = random.randint(0, screen_width)
                ypos = random.randint(0, screen_height)

                if vh:
                    self.genes[0].append(Barriere(screen, xpos, ypos, random.randint(0, screen_width-ypos), 10))
                else:
                    self.genes[0].append(Barriere(screen, xpos, ypos, 10, random.randint(0, screen_height)))

            nbr_obs = random.randint(0, 6)

            for obs in range(nbr_obs):
                xpos = random.randint(0, screen_width)
                ypos = random.randint(0, screen_height)
                self.genes[1].append(ObstacleMouvant(screen, xpos, ypos, random.randint(0, screen_width-ypos), random.randint(0, screen_height-ypos), random.randint(2, 20)))

            self.genes = DNA(self.genes)


def creer_ter():

    return [[
                Barriere(screen, 150, 191, 473, 10),\
                Barriere(screen, 346, 22, 155, 10)
             ],
            [
                ObstacleMouvant(screen, 114, 207, 85, 113, 2),\
                ObstacleMouvant(screen, 163, 567, 11, 207, 3),\
                ObstacleMouvant(screen, 246, 644, 12, 62, 12)
             ]]


## main (one terrain trial)


def main(inputs):

    pop_size, generation_cachees, dna_size, max_dna_len, dna_add, terrain_conteneur = inputs

    terrain_instance = 0

    largeur_barriere = 21

    population = Population(pop_size, dna_size, max_dna_len, dna_add, largeur_barriere)

##    if terrain_instance:  # when evolving terrains
##
##        barrieres, obstacles = terrain_conteneur.genes.dna[0], terrain_conteneur.genes.dna[1]#.terrain4()
##
##    else:

    terrains = [terrain0, terrain1, terrain2, terrain3, terrain4, terrain5]

    terrain = terrains[terrain_conteneur](largeur_barriere)

    barrieres, obstacles = terrain[0], terrain[1]

    generation = -1

    show = 0

    for x in range(100000):

        generation += 1

        if generation > generation_cachees:
            show = 1

        print("Génération : ", generation, end=" ; ")
        a = time.time()

        fin = run_pop(population, barrieres, obstacles, show, generation, terrain_instance)

        if fin:

            print("temps :", round(time.time()-a, 2))

            if fin != 1:

                return fin

            return generation

        population.evoluer()

        print("temps :", round(time.time()-a, 2))

    return 100


if __name__== "__main__":

    pygame.display.set_caption("Jeu")

    pop_size = 500

    generation_cachees = 0  # int(input("Combien de generations voulez vous sauter ?\n"))

    terrain_choice = 3

    dna_start_size = 80

    max_dna_len = 300

    dna_add = 4

    inputs = [pop_size, generation_cachees, dna_start_size, max_dna_len, dna_add, terrain_choice]

##    choix_gameplay = 1  # int(input("1) Version normale. 2) Mise en abime.\n"))
##
##    if choix_gameplay == 1:

    main(inputs)#main(terrain5(), 0)


##
##    else:
##
##        taille_pop_ter = int(input("Combien de terrains par generation?\n"))
##        nbr_generation = int(input("How many generation?\n"))
##
##        pop_ter = PopTerrain(screen, taille_pop_ter)
##
##        for loop in range(nbr_generation):
##
##            print("Generation de terrain : {}".format(loop))
##
##            for objet in pop_ter.pop:
##                print("Terrain numero : {}".format(pop_ter.pop.index(objet)))
##
##                objet.fit = main(objet, pop_size, generation_cachees)
##
##            pop_ter.evaluate()
##            if loop < nbr_generation-1:
##                pop_ter.evoluer()
##
##        pop_ter.aff_final()
