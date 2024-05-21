from pig_tv import *


def get_integrale_trapeze(fct, borne1, borne2, nbr_trap=100, rounded=1):

    step = (borne2-borne1)/nbr_trap

    points = [borne1+step*x for x in range(nbr_trap+1)]

    somme_trapezes = 0

    for x in range(nbr_trap):

        somme_trapezes += step * fct(points[x])  # rectangle de gauche

        somme_trapezes += (fct(points[x+1])-fct(points[x]))*step/2  # triangle

    if rounded:

        return round(somme_trapezes, 3)

    else:

        return somme_trapezes


def test_integrale_trapeze():

    def fct_test_cst(x):

        return 1

    borne1 = -5

    borne2 = 5

    #print("Integrale de fct cst egale a 1 entre {} et {} : expected 10, got {}".format(borne1, borne2, get_integrale_trapeze(fct_test_cst, borne1, borne2)))

    def fct_test_affin(x):

        return x

    borne1 = -5

    borne2 = 5

    print("Integrale de fct lineaire de pente 1 entre {} et {} : expected 0, got {}".format(borne1, borne2, get_integrale_trapeze(fct_test_affin, borne1, borne2)))

    def fct_test_quad(x):

        return x**2

    borne1 = 0

    borne2 = 1

    print("Integrale de fct lineaire de pente 1 entre {} et {} : expected 0.3333, got {}".format(borne1, borne2, get_integrale_trapeze(fct_test_quad, borne1, borne2, 1000, 0)))


#test_integrale_trapeze()


class ObjetPonctuel2D:

    def __init__(self, unite_temps, pos, vitesse, radius=10, masse=1):

        self.pos = pos

        self.vitesse = vitesse

        self.unite_temps = unite_temps

        self.temps = 0

        self.resultante = 0

        self.radius = radius

        self.masse = masse

        self.constante_grav_terre = 9.18

        self.binds = []

    def altitude(self):

        return self.pos[1]

    def get_poids_at_z(self):

        return Arr([0, self.masse * self.constante_grav_terre])

    def bind_to(self, fil):

        self.binds.append(fil)

    def get_resultante(self):

        resultante = Arr.get_nul([2])

        poids = ObjetPonctuel2D.get_poids_at_z(self)

        resultante += poids

        for fil in self.binds:

            if fil.is_tendu():

                tangente = fil.get_tangente(self)  # direction de tension : le fil tire

                #resultante.draw()

                resultante -= (Arr.p_s(resultante, tangente))*tangente  # annule le mouvement selon la direction du fil  # -fil.get_surtension()

                #resultante.draw()

        return resultante

    def time_forward(self, time_unit=None):

        if time_unit != None:

            time_unit = self.unite_temps

        ObjetPonctuel2D.pfd_instantane(self)  # computes new speed, depending on the forces applied on the system

        ObjetPonctuel2D.update_speed(self, time_unit)

        ObjetPonctuel2D.update_pos(self, time_unit)  # moves the system depending on its speed

    def update_pos(self, time_unit=None):

        if time_unit != None:

            time_unit = self.unite_temps

        print(self.pos, self.pos + self.unite_temps*self.vitesse)

        self.pos += self.unite_temps*self.vitesse

    def update_speed(self, time_unit=None):

        if time_unit != None:

            time_unit = self.unite_temps

        self.vitesse += self.unite_temps*self.acceleration

    def draw(self):

        pygame.draw.circle(screen, BLUE, self.pos.with_fun_applied(round), self.radius)

    def get_accel_instant(self):

        return ObjetPonctuel2D.get_resultante(self)*(1/self.masse)

    def pfd_instantane(self):
    # Prend le systeme ponctuel dans un etat à un moment donné (position, vitesse, acceleration) et les forces qui lui sont apliquees, met à jour sa vitesse par conséquent (par rapport a un moment de temps elementaire) en utilisant le principe fondamental de la dynamique 

        self.acceleration = ObjetPonctuel2D.get_accel_instant(self)

##        resultante_du_temps = lambda t:ObjetPonctuel.get_resultante(self, t)
##        integrale_resultante = get_integrale_trapeze(, self.temps, self.temps+self.unite_temps)
##
##        delta_v = integrale_resultante/self.masse
##
##        self.vitesse += delta_v

    def bind_pos(self):

        return self.pos

    def time_forward_corrige(self):

        test = 1

        origin_pos = self.pos.copy()

        print(1)

        if test:

            pygame.draw.circle(screen, BLUE, origin_pos.with_fun_applied(round), 15)

        ObjetPonctuel2D.time_forward(self, self.unite_temps/2)  # puts the object half the way where it was supposed to be in first approximation

        if test:

            pygame.draw.circle(screen, RED, self.pos.with_fun_applied(round), 15)

        print(self.pos)

        first_approximation_pos = self.pos + (self.unite_temps/2)*self.vitesse  # two times farther actually

        print(self.pos)

        vitesse_objet = self.vitesse.copy()

        if test:

            pygame.draw.circle(screen, GREEN, first_approximation_pos.with_fun_applied(round), 15)

        # gets pos better approximated

        ObjetPonctuel2D.pfd_instantane(self)  # computes new speed, depending on the forces applied on the system

        self.vitesse += self.acceleration  # gets normalized anyway

        self.vitesse.normalize(self.vitesse.norme_eucli())

        ObjetPonctuel2D.update_pos(self, self.unite_temps/2)

        if test:

            pygame.draw.circle(screen, YELLOW, self.pos.with_fun_applied(round), 15)

        correction_vect = self.pos-first_approximation_pos

        self.pos += correction_vect  # getting a better position

        if test:

            correction_vect.draw()

            pygame.draw.circle(screen, PURPLE, self.pos.with_fun_applied(round), 15)

        self.vitesse = (self.pos-origin_pos)*(1/self.unite_temps)  # recomputing real speed

        self.acceleration = ObjetPonctuel2D.get_accel_instant(self)

        pygame.display.update()

        wait()


class FilParfait:

    def __init__(self, bind1, bind2, length):

        self.bind1 = bind1

        self.bind2 = bind2

        self.length = length

        self.points_contact = []

    def get_surtension(self):

        if self.points_contact == []:

            length = get_distance(self.bind1.bind_pos(), self.bind2.bind_pos())

            if length > self.length:

                return length-self.length

            else:

                return 0

    def is_tendu(self):

        if self.points_contact == []:

            return FilParfait.get_surtension(self) > 0

        else:

            print("pas fait, devrait, tant qu'il y a pt de contact, gérer celui ci en divisant le fil en deux sous fils independants")

    def get_tangente(self, obj):
        """ returns which way the rope is pulling on object obj """

        if self.points_contact == []:

            if obj == self.bind1:

                antagoniste = self.bind2

            elif obj == self.bind2:

                antagoniste = self.bind1

            tangente = antagoniste.pos-obj.pos

            tangente.normalize()

            return tangente

    def draw(self):

        if self.points_contact == []:

            pygame.draw.line(screen, BLACK, self.bind1.bind_pos(), self.bind2.bind_pos())


class Bati(ObjetPonctuel2D):

    def __init__(self, pos, size=5):

        ObjetPonctuel2D.__init__(self, 0, pos, Arr.get_nul([2]))

        self.size = size

        self.rect = pygame.Rect(pos[0]-size/2, pos[1]-size/2, size, size)

    def draw(self):

        pygame.draw.rect(screen, BLACK, self.rect)


class Pendule:

    def __init__(self, time_unit):

        high_center = Arr([screen_width/2, screen_height/3])

        self.bati = Bati(high_center)

        self.fil_length = screen_height/3

        self.masse = ObjetPonctuel2D(time_unit, high_center+Arr([screen_height/3, 0]), Arr.get_nul([2]))

        self.fil = FilParfait(self.bati, self.masse, self.fil_length)

        self.masse.bind_to(self.fil)

    def time_forward(self):

        self.masse.time_forward_corrige()

        Pendule.draw(self)

    def draw(self):

        self.masse.draw()

        self.bati.draw()

        self.fil.draw()


class DoublePendule:

    def __init__(self, time_unit):

        high_center = Arr([screen_width/2, screen_height/3])

        self.bati = Bati(high_center)

        self.fil_length = screen_height/6

        self.masse1 = ObjetPonctuel2D(time_unit, high_center+Arr([screen_height/3, 0]), Arr.get_nul([2]))

        self.fil1 = FilParfait(self.bati, self.masse1, self.fil_length)

        self.masse1.bind_to(self.fil1)

        self.masse2 = ObjetPonctuel2D(time_unit, high_center+2*Arr([screen_height/3, 0]), Arr.get_nul([2]))

        self.fil2 = FilParfait(self.masse1, self.masse2, self.fil_length)

        self.masse1.bind_to(self.fil2)

        self.masse2.bind_to(self.fil2)

    def time_forward(self):

        self.masse1.time_forward()

        self.masse2.time_forward()

        DoublePendule.draw(self)

    def draw(self):

        self.masse1.draw()

        self.masse2.draw()

        self.bati.draw()

        self.fil1.draw()

        self.fil2.draw()


def main():

    play = True

    clicking = 0

    pend = Pendule(1)#, Arr([screen_width/2, 0]), Arr([0, 0]))

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

        pend.time_forward()

        pygame.display.update()

        clock.tick(60)


main()


class Pendule(ObjetPonctuel2D):

    def __init__(self, unite_temps, pos, vitesse):

        ObjetPonctuel2D.__init__(self, unite_temps, pos, vitesse)

        self.constante_grav_terre = 9.18

        self.radius = 20

    def altitude(self):

        return self.pos[1]

    def get_resultante_at_z(self, z):

        return self.masse * self.constante_grav_terre * z

    def set_resultante(self):

        z = Pendule.altitude(self)

        self.resultante = Pendule.get_resultante_at_z(self, z)

    def get_resultante(self, temps):

        if temps == self.temps:

            return self.resultante

        else:

            delta_t = temps-self.temps

            return Pendule.get_simul_force(self, delta_t)

    def get_simul_force(self, delta_t):

        simul_z = self.pos[1]+self.vitesse[1]*delta_t

        return get_resultante_at_z(self, simul_z)

    def draw(self):

        screen.fill(WHITE)

        origine = Arr([screen_width/2, screen_height/2])

        pygame.draw.circle(screen, BLUE, round(self.pos, 0), self.radius)

        pygame.display.update()

        






















