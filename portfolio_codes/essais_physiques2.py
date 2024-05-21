from pig_tv import *


class ObjetPonctuel2D:

    constante_grav_terre = 9.18

    def __init__(self, pos, vitesse, unite_temps, masse=1):

        self.pos = pos

        self.vitesse = vitesse

        self.acceleration = Arr.get_nul([2])

        self.unite_temps = unite_temps

        self.resultante = Arr.get_nul([2])

        self.masse = masse

        self.binds = []

    def get_poids(self):

        return Arr([0, self.masse*ObjetPonctuel2D.constante_grav_terre])

    def time_forward(self):

        n_accel = self.resultante

        n_pos = self.pos + self.unite_temps*self.vitesse + ((self.unite_temps**2)/2)*self.acceleration

        n_speed = self.vitesse + (self.unite_temps/2)*(n_accel+self.acceleration)

        self.acceleration = n_accel

        self.vitesse = n_speed

        self.pos = n_pos


class Pendule(ObjetPonctuel2D):

    def __init__(self, unite_temps):

        self.len = 100

        ObjetPonctuel2D.__init__(self, Arr(screen_center)+Arr([100, 0]), Arr.get_nul([2]), unite_temps)

        self.direction_fil = Arr.get_nul([2])

        Pendule.update_direction_fil(self)

    def update_direction_fil(self):

        self.direction_fil = self.pos-Arr(screen_center)

    def get_len(self):

        return (Arr(screen_center)-self.pos).norme_eucli()
    
    def update_resultante(self):

        self.resultante = ObjetPonctuel2D.get_poids(self)

        Pendule.update_direction_fil(self)

        vecteur_support_force = self.direction_fil.get_orth()

        norme_scalaire = self.resultante*(vecteur_support_force.transposed())

        self.resultante = norme_scalaire*vecteur_support_force

        # elasticité

        allongement = Pendule.get_len(self)-self.len

        self.resultante -= allongement*self.direction_fil.normalized(1)

    def update(self):

        Pendule.time_forward(self)

        Pendule.draw(self)

    def time_forward(self):

        Pendule.update_resultante(self)

        ObjetPonctuel2D.time_forward(self)

    def draw(self):

        approx_pos = self.pos.copy()

        approx_pos.apply_fun(round)

        pygame.draw.circle(screen, BLUE, screen_center, 10)

        pygame.draw.line(screen, BLACK, screen_center, approx_pos.liste)

        pygame.draw.circle(screen, GREEN, approx_pos.liste, 10)

        

def p_loop():

    unite_temps = 0.1

    play = True

    clicking = 0

    pendule = Pendule(unite_temps)

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

        screen.fill(WHITE)

        pendule.update()

        pygame.display.update()

        clock.tick(60)


p_loop()
