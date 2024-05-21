from pig_tv import *


class Player:

    def __init__(self, indice, player2, earth):

        self.indice = indice

        self.lr = self.indice*-1 or 1  # left or right : du bon cote

        self.hauteur = 100

        self.largeur = 40

        self.side = (indice*(screen_width//2+50) or 10)

        self.x = ((indice*(screen_width-100)) or 70)

        self.color = [random.randint(50, 250) for x in range(3)]

        self.color_tete = [255, 0, 0]

        self.color_pied = (50, 20, 30)

        self.y = earth - self.hauteur

        self.jump = 0

        self.active_jump = 0

        self.direction = 0

        self.speed = 0

        self.max_vie = 100

        self.vie = self.max_vie

        self.active_shield = 0

        self.active_kick = 0

        self.active_low_kick = 0

        self.active_punch = 0

        self.active_empoignade = 0

        self.action = 0

        self.hurt = 0

        self.player2 = player2

        self.explosion = 0

        self.kick_time = 25

        self.punch_time = 25

        self.low_kick_time = 25

        self.empoignade_time = 45

        self.earth = earth

    def set_jump(self):

        if self.y == self.earth - self.hauteur:

            self.jump = 15

            self.active_jump = 1

    def draw(self):

        moitie_x = self.x + self.largeur//2  # Pour la symetrie

        couleur_oeil = (0, 0, 0)
        couleur_body = self.color
        couleur_jambe = self.color_pied
        couleur_tete = self.color_tete

        if self.hurt:

            self.hurt -= 1

            if not self.hurt:  # hurt vient d'etre decrementer a 0

                self.action = 0  # Donc on release

            couleur_oeil = (255, 0, 0)
            couleur_body = (255, 255, 255)
            couleur_jambe = (255, 255, 255)
            couleur_tete = (255, 255, 255)

        #corps
        rectangle = pygame.Rect(self.x, self.y, self.largeur, self.hauteur//2)

        pygame.draw.rect(screen, couleur_body, rectangle)

        #pieds

        largeur_pied = 0.5

        for x in [-1, 1]:

            if (not self.lr == x) or ((not self.active_kick) and (not self.active_low_kick)):

                vect = x

                pied = ((moitie_x, self.y+self.hauteur//2), (moitie_x+(self.largeur*largeur_pied)*vect, self.y+self.hauteur//2), (moitie_x+(self.largeur)*vect, self.y+self.hauteur//1.5), (moitie_x+int(self.largeur*1.3)*vect, self.y+self.hauteur), (moitie_x+self.largeur*(1.3-largeur_pied)*vect, self.y+self.hauteur), (moitie_x+(self.largeur*largeur_pied)*vect, self.y+self.hauteur//1.5), (moitie_x, self.y+self.hauteur//2))

                pygame.draw.polygon(screen, couleur_jambe, pied)

        #bras

        if not self.active_empoignade:

            for x in [-1, 1]:

                if (not self.lr == x) or ((not self.active_punch) and (not self.active_shield)):

                    vect = x

                    remise_a_niveau = -10

                    bras = ((moitie_x+(self.largeur*largeur_pied)*vect, self.y+self.hauteur//3+remise_a_niveau), (moitie_x+(self.largeur)*vect, self.y+self.hauteur//2.5+remise_a_niveau), (moitie_x+int(self.largeur*1.3)*vect, self.y+self.hauteur//1.5+remise_a_niveau), (moitie_x+(self.largeur*(1.3-largeur_pied)+10)*vect, self.y+self.hauteur//1.5+remise_a_niveau), (moitie_x+(self.largeur*largeur_pied)*vect, self.y+self.hauteur//2.5+remise_a_niveau), (moitie_x+(self.largeur*largeur_pied)*vect, self.y+self.hauteur//3+remise_a_niveau))

                    pygame.draw.polygon(screen, couleur_body, bras)

        #barre de vie
        len_barre = screen_width//2.6

        vert = self.vie / self.max_vie

        rouge = (vert-1) * -1

        barre = pygame.Rect(self.side-5, 5, len_barre+10, 30)

        pygame.draw.rect(screen, (0, 0, 0), barre)

        rect_vert = pygame.Rect(self.indice*(int(self.side+len_barre*(rouge))) or self.side, 10, int(len_barre*vert), 20)

        pygame.draw.rect(screen, (0, 255, 0), rect_vert)

        rect_rouge = pygame.Rect(self.indice*(self.side) or int(self.side+len_barre*(vert)), 10, int(len_barre*rouge), 20)

        pygame.draw.rect(screen, (255, 0, 0), rect_rouge)

        # Partie reservee aux graphismes speciaux (dus aux attaques..)
        # S'occupe aussi des release programmes avec un temps (attaques)

        if self.active_shield:

            arm = pygame.Rect(moitie_x+(self.largeur//2)*self.lr, self.y+25, 40*self.lr, 15)

            pygame.draw.rect(screen, self.color, arm)

            shiel = pygame.Rect(moitie_x+(self.largeur//2+40)*self.lr, self.y-10, 5*self.lr, self.hauteur-10)

            pygame.draw.rect(screen, (70, 70, 70), shiel)


        elif self.active_punch:

            self.active_punch -= 1

            if not self.active_punch:  # active_punch vient d'etre decrementer a 0

                self.action = 0  # Donc on release

            arm = pygame.Rect(moitie_x+(self.largeur//2)*self.lr, self.y+22, 30*self.lr, 14)

            pygame.draw.rect(screen, self.color, arm)

            fist = pygame.Rect(moitie_x+(self.largeur//2+30)*self.lr, self.y+18, 10*self.lr, 20)

            pygame.draw.rect(screen, (220, 100, 80), fist)

            if self.active_punch == self.punch_time-1:

                hitbox = pygame.Rect(moitie_x+(self.largeur//2)*self.lr, self.y+18, 40*self.lr, 20)

                attack_type = 1

                strenght = 13

                Player.attaque(self, attack_type, hitbox, strenght)

        elif self.active_kick:

            self.active_kick -= 1

            if not self.active_kick:

                self.action = 0  # release

            feet = pygame.Rect(moitie_x+(self.largeur//2)*self.lr, self.y+self.hauteur//2, 50*self.lr, 20)

            pygame.draw.rect(screen, self.color_pied, feet)

            feet_end = pygame.Rect(moitie_x+(self.largeur//2+50)*self.lr, self.y+self.hauteur//2-7, 6*self.lr, 24)

            pygame.draw.rect(screen, (0, 0, 0), feet_end)

            pygame.draw.polygon(screen, self.color_pied, ((moitie_x, self.y+self.hauteur//2), (moitie_x+(self.largeur//2)*self.lr, self.y+self.hauteur//2), (moitie_x+(self.largeur//2)*self.lr, self.y+self.hauteur//2+18), (moitie_x, self.y+self.hauteur//2)))

            if self.active_kick == self.kick_time-1:

                hitbox = pygame.Rect(moitie_x+(self.largeur//2)*self.lr, self.y+self.hauteur//2, 50*self.lr, 20)

                attack_type = 1

                strenght = 7

                Player.attaque(self, attack_type, hitbox, strenght)

        elif self.active_low_kick:

            self.active_low_kick -= 1

            if not self.active_low_kick:

                self.action = 0  # release 

            pygame.draw.polygon(screen, self.color_pied, ((moitie_x, self.y+self.hauteur//2), (moitie_x+(self.largeur//2)*self.lr, self.y+self.hauteur//2), (moitie_x+(self.largeur//2)*self.lr, self.y+self.hauteur//2+18), (moitie_x, self.y+self.hauteur//2)))

            pygame.draw.polygon(screen, self.color_pied, ((moitie_x+(self.largeur//2)*self.lr, self.y+self.hauteur//2), (moitie_x+(self.largeur)*self.lr, self.y+self.hauteur//1.3), (moitie_x+(self.largeur+30)*self.lr, self.y+self.hauteur-5), (moitie_x+(self.largeur+10)*self.lr, self.y+self.hauteur-5), (moitie_x+(self.largeur//1.5)*self.lr, self.y+self.hauteur//1.35), (moitie_x+(self.largeur//2)*self.lr, self.y+self.hauteur//2+18), (moitie_x+(self.largeur//2)*self.lr, self.y+self.hauteur//2)))

##            feet_end = pygame.Rect(moitie_x+(self.largeur+25)*self.lr, self.y+self.hauteur//2+25, 5, 20)
##
##            pygame.draw.rect(screen, (0, 0, 0), feet_end)

            if self.active_low_kick == self.low_kick_time-1:

                hitbox = pygame.Rect((moitie_x+(self.largeur))*self.lr, self.y+self.hauteur-20, 30*self.lr, 15)

                attack_type = 1

                strenght = 10

                Player.attaque(self, attack_type, hitbox, strenght)

        elif self.active_empoignade:

            self.active_empoignade -= 1

            if not self.active_empoignade:

                self.action = 0  # release

                # Attaque
                hitbox = pygame.Rect(moitie_x+(self.largeur//2)*self.lr, self.y+18, 30*self.lr, 22)

                attack_range = 30

                attack_type = 2

                strenght = 25

                if Player.attaque(self, attack_type, hitbox, strenght):

                    self.explosion = 5

            arm = pygame.Rect(moitie_x+(self.largeur//2)*self.lr, self.y+18, 30*self.lr, 14)

            pygame.draw.rect(screen, (120, 120, 120), arm)

            arm = pygame.Rect(moitie_x+(self.largeur//2)*self.lr, self.y+26, 30*self.lr, 14)

            pygame.draw.rect(screen, self.color, arm)

        #tete
        tete = pygame.Rect(self.x-5, self.y-5, self.largeur+10, self.hauteur//4)

        pygame.draw.rect(screen, couleur_tete, tete)

        oeil = pygame.Rect(moitie_x+(self.largeur//2-5)*self.lr, self.y+10, 5*self.lr, 5)

        pygame.draw.rect(screen, couleur_oeil, oeil)

        if self.explosion:

            pygame.draw.circle(screen, (255, 0, 0), (moitie_x+(self.largeur)*self.lr, self.y+self.largeur//2), 60)

            self.explosion -= 1


    def forward(self):

        if self.speed:

            self.x += self.direction * 3

        else:

            self.x += self.direction

        if self.active_jump:

            if self.jump + self.earth - self.hauteur < self.y:

                self.y = self.earth - self.hauteur
                self.active_jump = 0

            else:

                self.y -= self.jump

                self.jump -= 1

    def move(self, direction):

        if direction > 0:

            self.lr = 1

        else:

            self.lr = -1

        self.direction = direction

    def stop(self):

        self.direction = 0

    def speed_up(self):

        self.speed = 1

    def slow_down(self):

        self.speed = 0

    def got_hurt(self, vie):

        self.hurt = 25

        self.action = 1

        self.vie -= vie

        self.empoignade = 0  # L'empoignade est annule si on se fait attaquer avant 45 frame (ou le temps imparti)

    def attaque(self, attack_type, hitbox, strenght):

        hurt = 0

        if not ((self.player2.shield) and (attack_type == 1) and (hitbox.colliderect(self.player2.get_rect_shield()))):  # L'adversaire a un bouclier et l'attaque est une attaque simple et la hitbox de l'attaque touche le bouclier

                for part in self.player2.get_hitbox():

                    if (not hurt) and (hitbox.colliderect(part)):  # la hitbox de l'attaque touche l'ennemi

                        hurt = 1  #  Permet a l'adversaire de ne pas perdre plusieurs fois des vies si la hitbox de l'attaque touche plusieurs parties de son corps

                        self.player2.got_hurt(strenght)

    def kick(self):

        self.active_kick = self.kick_time  # Pour le graphique

        attack_range = 50

        attack_type = 1

        self.action = 1  # Le player ne peut pas faire plusieurs attaques en meme temps, tant que son personnage attaque, il ne peut faire d'autre action

    def low_kick(self):

        self.active_low_kick = self.low_kick_time  # Pour le graphique

        attack_range = 45

        attack_type = 3    

        self.action = 1

    def punch(self):

        self.active_punch = self.punch_time  # Pour le graphique

        attack_range = 30

        attack_type = 1

        self.action = 1

    def empoignade(self):

        self.active_empoignade =  self.empoignade_time  # Pour le graphique

        self.action = 1

    def set_player(self, player2):

        self.player2 = player2

    def shield(self):

        self.active_shield = 1

        self.action = 1

    def un_shield(self):

        self.active_shield = 0

        self.action = 0  # Release le personnage (lui permet de faire autre chose)

    def get_rect_shield(self):

        moitie_x = self.x + self.largeur//2

        return pygame.Rect(moitie_x+(self.largeur//2+40)*self.lr, self.y-10, 5*self.lr, self.hauteur-10)

    def get_hitbox(self):

        tete = pygame.Rect(self.x-5, self.y-5, self.largeur+10, self.hauteur//4)

        rectangle = pygame.Rect(self.x-20, self.y, self.largeur+20, self.hauteur)

        return tete, rectangle


def aff_txt(contenu, x, y, color=(0, 0, 0), taille=30):
    """ Permet d'afficher un texte """
    myfont = pygame.font.SysFont("monospace", taille, True)
    label = myfont.render(contenu, 1, color)
    screen.blit(label, (x, y))


class Earth:

    def __init__(self, earth):

        self.earth = earth

        #terre
        self.rect = pygame.Rect(0, self.earth, screen_width, screen_height-self.earth)

        self.color = (30, 180, 30)

        #ciel
        self.rect_bar = pygame.Rect(0, 0, screen_width, self.earth)

        self.color_bar = (30, 30, 220)

    def draw(self):

        pygame.draw.rect(screen, self.color_bar, self.rect_bar)

        pygame.draw.rect(screen, self.color, self.rect)


def main(speed_rate):

    earth = 500

    play = True

    player1 = Player(0, 0, earth)

    player2 = Player(1, 0, earth)

    players = [player1, player2]

    player1.set_player(player2)

    player2.set_player(player1)    

    bg = Earth(earth)  # Background

    while play:

        bg.draw()

        player2.draw()

        player1.draw()

        player1.forward()

        player2.forward()

        for event in pygame.event.get():

            if event.type == QUIT:

                play = False

            if (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):

                mouse_pos = pygame.mouse.get_pos()

            if event.type == pygame.KEYDOWN:

##                caractere = event.dict['unicode']
##
##                print(caractere)

                if (event.key == K_SPACE):

                    player1.set_jump()

                elif (event.key == K_LEFT):

                    player1.move(-speed_rate)

                elif (event.key == K_RIGHT):

                    player1.move(speed_rate)

                elif (event.key == K_s):

                    player1.speed_up()

                if not player1.action:
                    #print(event.key)

                    if (event.key == K_d):

                        player1.punch()

                    elif (event.key == K_q):

                        player1.kick()

                    elif (event.key == K_f):

                        player1.shield()

                    elif (event.key == K_e):

                        player1.low_kick()

                    elif (event.key == K_z):

                        player1.empoignade()

            elif event.type == pygame.KEYUP:

                if (event.key == K_LEFT):

                    player1.stop()

                elif (event.key == K_RIGHT):

                    player1.stop()

                elif (event.key == K_s):

                    player1.slow_down()

                elif (event.key == K_f):

                    player1.un_shield()

        for player in players:

            if player.vie <= 0:

                play = False

                player.vie = 0

                bg.draw()

                for player in players:

                    player.draw()

                aff_txt("Game over!", 200, 300, color=(255, 0, 0), taille=30)
                aff_txt("Player {} won".format(players.index(player) or 2), 190, 350, color=(255, 0, 0), taille=30)

        pygame.display.update()

        clock.tick(60)



## Constantes

if __name__ == "__main__":

    speed_rate = 3

    main(speed_rate)
