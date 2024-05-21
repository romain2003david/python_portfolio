from pig_tv import *


class Brique:

    def __init__(self, pt1, pt2=None, pt3=None, pt4=None, width=None, height=None, angle=None):
        """ rectangles can be created either by giving 3 (or even 4 points) or 1 point and a width, a height and an angle """

        self.pt1 = Arr(pt1)

        if self.pt2 != None:  # on definit par la methode des points

            self.pt2 = Arr(pt2)

            self.pt3 = Arr(pt3)

            if pt4 == None:

                pt4 = pt1 + (pt2-pt1) + (pt3-pt1)

            else:

                self.pt4 = Arr(pt4)

            width = abs(Arr.get_distance(self.pt1, self.pt2))

            height = abs(Arr.get_distance(self.pt1, self.pt3))

        else:  # on definit avec longueur largeur angle
                # l'angle 
            self.pt2 = self.pt1 + width*(Arr.get_mat_rot2D(angle)*[1, 0])

            angle2 = angle+pi/2

            self.pt3 = self.pt1 + height*(Arr.get_mat_rot2D(angle)*[1, 0])

            self.pt4 = Arr(pt4)

        self.width = width

        self.height = height

        self.pts = [self.pt1, self.pt2, self.pt3, self.pt4]

        self.rect = [self.pt1[0], self.pt1[1], self.width, self.height]

        Brique.set_gravity_center(self)

    def set_gravity_center(self):

        self.gravity_center = self.pt1 + (self.pt4-self.pt1)/2

    def get_extremite_basse(self):

        return max(pt[1] for pt in self.pts)

    def get_extremite_haute(self):

        return min(pt[1] for pt in self.pts)

    def get_extremite_gauche(self):

        return min(pt[0] for pt in self.pts)

    def get_extremite_droite(self):

        return max(pt[0] for pt in self.pts)

    def update(self, force):

        pass


def inter_objet(brik1, brik2):

    limite_angle = 10**(-3)

    # collision quelconque
    if collide_rect_to_rect(brik1.rect, brik2.rect):

        # mtn regarde si deux faces des objets sont paralelles donc collees, ou bien si cest un coin qui vient taper

        if abs(brik1.angle-brik2.angle) < limite_angle:  # faces collees

            # trouve la face commune

            vecteur_barycentre = brik2.gravity_center - brik1.gravity_center

            vecteurs_diag = [brik1.gravity_center-brik1.pt1, brik1.gravity_center-brik1.pt2, brik1.gravity_center-brik1.pt3, brik1.gravity_center-brik1.pt4]

            angles = [vecteur.get_polar()[1] for vecteur in vecteurs_diag]

            angle_bary = vecteur_barycentre.get_polar()[1]

            if appartient(angle_bary, angles[0], angles[1]):  # face basse

                normale = []

            elif appartient(angle_bary, angles[0], angles[2]):  # face gauche

                pass

            elif appartient(angle_bary, angles[1], angles[3]):  # face droite

                pass

            elif appartient(angle_bary, angles[2], angles[3]):  # face haute

                pass

            # now find which block actually collided : the one whose speed is close to normal to the collision surface

            if Arr.get_distance(brik1.speed, normale) <= Arr.get_distance(brik2.speed, normale):

                brik1.recule()

            else:

                brik2.recule()

        else:

            pass


class Univers:

    def __init__(self):

        self.objets = []

        self.floor = screen_height

        self.gravite = Arr([0, 1])

    def update(self):

        for idx in rl(self.objets):

            obj = self.objets[idx]

            # poids

            force = self.gravite

            # autres objets

            for idx2 in rl(self.objets):

                obj2 = self.objets[idx2]

            # gere le floor

            if obj.get_extremite_basse() <= self.floor:

                obj.rectifie_pos(1, 1, self.floor)

                force = Arr.get_nul([2])

def main():

    




















