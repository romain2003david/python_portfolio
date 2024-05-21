"""
turret game
10/07/2019

"""


from pig_tv import *



# classes

# graphic menus for user

class Menu:

    def __init__(self, terrain, coor, options, menu_type, prices, fire_menu=0):
        """ Menu shop, that enables player to buy defenses """

        self.type = menu_type  # 0 for buying, 1 for (sell/upgrade), 2 for special power menu

        self.prices = prices

        self.options = options

        self.fire_menu = fire_menu

        self.box_margin = 0

        self.frame_height = terrain.up_margin-2*self.box_margin

        x_pos = terrain.panneau_pause.x + terrain.panneau_pause.largeur

        self.pyg_rect = pygame.Rect(x_pos+self.box_margin, self.box_margin, screen_width-x_pos-2*self.box_margin, self.frame_height)

        self.menu_frame = Panneau("", self.pyg_rect[0], self.pyg_rect[1], self.pyg_rect[2], self.pyg_rect[3])

        self.box_width = 140

        self.box_height = self.frame_height - 2*self.box_margin

        self.available_box_nb = (self.pyg_rect[2]-2*self.box_margin)//(self.box_width+self.box_margin)

        self.arrow_size = 8

        self.grid_coors = coor  # locates the coor of a menu, which is outside the grid

        self.page = 0  # current page (part of all options currently displayed on screen)

        self.page_nb = ceil(len(self.options)/(self.available_box_nb-2))  # total page nb

        self.curr_boxes = []

        self.box_y = self.menu_frame.y+self.box_margin

        loop_nb = min(self.available_box_nb-2, len(self.options)-1)  # if there is more available boxes than the number of boxes to display ; -2 for arrow buttons

        Menu.define_curr_boxes(self, 0)

    def define_curr_boxes(self, first_index):
        """ defining current buttons of menu (all can't be displayed because of place available on screen)"""

        self.curr_boxes = []

        loop_nb = min(self.available_box_nb-2, len(self.options[first_index:]))  # if there is more available boxes than the number of boxes to display (+2 arrow buttons)

        compteur = first_index

        # defining the button ; differences between arrow buttons and buying buttons

        for x in range(1, loop_nb+1):  # index is one further because of first arrow button

            box_x = self.menu_frame.x+self.box_margin+x*(self.box_margin+self.box_width)

            image_coors = [25, 37]

            if self.prices[compteur]:

                image_coors[0] += 13*(int(log(self.prices[compteur], 10))+2)  # width of digit in pixels * numbre of digits

                if self.fire_menu:

                    box = Panneau([self.options[compteur], str(self.prices[compteur])], box_x, self.box_y, self.box_width, self.box_height, x_focus=0, y_focus=0, image=draw_double_fire, image_args=[16, [RED, YELLOW]], image_coors=sum_arrays(image_coors, [5, 5]))

                else:

                        box = Panneau([self.options[compteur], str(self.prices[compteur])], box_x, self.box_y, self.box_width, self.box_height, x_focus=0, y_focus=0, image=draw_coin, image_args=[8], image_coors=image_coors)  # buy box, the string (self.options[x]) is the description of the article

            else:

                box = Panneau([self.options[compteur]], box_x, self.box_y, self.box_width, self.box_height, x_focus=0, y_focus=0)

            self.curr_boxes.append(box)

            compteur += 1

        first_box = Panneau("", self.menu_frame.x+self.box_margin, self.box_y, self.box_width, self.box_height, image=draw_fleche_formatted, image_coors=[70, 25], image_args=[self.arrow_size, GREY, 1])

        last_box = Panneau("", self.menu_frame.x+self.box_margin+(self.available_box_nb-1)*(self.box_margin+self.box_width), self.box_y, self.box_width, self.box_height, image=draw_fleche_formatted, image_coors=[25, 35], image_args=[self.arrow_size*-1, GREY, 1])

        self.curr_boxes.insert(0, first_box)

        self.curr_boxes.append(last_box)

    def change_page(self, change_val):

        self.page = (self.page+change_val) % self.page_nb

        first_index = self.page*(self.available_box_nb-2)

        Menu.define_curr_boxes(self, first_index)

    def draw(self):

        self.menu_frame.draw()

        for index in range(len(self.curr_boxes)):

            box = self.curr_boxes[index]

            if (index == 0) or (index+1 == len(self.curr_boxes)):  #arrow buttons

                box.draw()

            else:

                if self.fire_menu:

                    box.draw(several_lines=2, sev_line_col=RED)

                else:

                    box.draw(several_lines=2)

    def clicked(self, mouse_pos):

        for x in range(len(self.curr_boxes)):

            panneau = self.curr_boxes[x]

            if panneau.clicked(mouse_pos):

                if x == len(self.curr_boxes)-1:

                    Menu.change_page(self, 1)

                    return  # breaks loop, for curr_boxes has changed, and anyway job done

                elif x == 0:

                    Menu.change_page(self, -1)

                    return

                else:

                    return panneau.contenu


# logic useless entity, olly graphic info for player

class Spectre:
    """ limited in time info for player """

    def __init__(self, pos, val, fire=0):

        self.life_time = 60

        self.txt = str(val)

        self.x = int(pos[0])

        self.y = int(pos[1])

        self.fire = fire

    def update(self):

        self.life_time -= 1

        self.y -= 1

        aff_txt(self.txt, self.x, self.y, color=YELLOW, taille=20)

        if self.fire:

            draw_fire(self.x, self.y, [-15, 10], [8, RED])

            draw_fire(self.x, self.y, [-15, 10], [4, YELLOW])

        else:

            draw_coin(self.x, self.y, [-15, 10], [8])

        if not self.life_time:

            return -1


class WaveSign(Spectre):

    def __init__(self, pos):

        self.life_time = 150

        decalage = 170

        self.x = pos[0] + set_val_to_different_array([0, screen_width], [decalage, -decalage], pos[0])

        self.y = pos[1] + set_val_to_different_array([0, screen_height], [decalage, -decalage], pos[1])

        self.size = 30

    def update(self):

        self.life_time -= 1

        pygame.draw.polygon(screen, WHITE, ((self.x-self.size, self.y), (self.x+self.size, self.y), (self.x, self.y-(2*self.size))))

        pygame.draw.polygon(screen, RED, ((self.x-self.size, self.y), (self.x+self.size, self.y), (self.x, self.y-(2*self.size))), 3)

        aff_txt("!", self.x-10, self.y-40)

        if not self.life_time:

            return -1


# Special Powers


class SpecialPower:

    def __init__(self):

        pass


class GuidedMissile(SpecialPower):

    need_target = 1

    def __init__(self, terrain):

        self.start_pt = [screen_width, 0]

        self.terrain = terrain

        self.name = "Guided Missile"

        self.atk_val = 250

    def activate(self, pos, facteur):

        return [BombBullet(self.terrain, self.start_pt, pos, self.atk_val*(facteur+1))]


class BombShell(SpecialPower):

    need_target = 1

    def __init__(self, terrain):

        self.start_pt = [screen_width, 0]

        self.far_vector = [1, -1]

        self.distance = 70

        self.terrain = terrain

        self.name = "Bomb Shell"

        self.atk_val = 150

    def activate(self, target_pos, facteur):

        to_return = []

        for x in range(5):

            random_tweak = [random.randint(-self.distance, self.distance) for k in range(2)]

            n_pos = sum_arrays(target_pos, random_tweak)

            start_pt = sum_arrays(self.start_pt, self.far_vector)

            to_return.append(BombBullet(self.terrain, start_pt, n_pos, self.atk_val*(facteur+1)))

            apply_function_to_array(self.far_vector, lambda x:x+get_sign(x)*self.distance)

        return to_return


class FreezeSpell(SpecialPower):

    need_target = 1

    def __init__(self, terrain):

        self.start_pt = [screen_width, 0]

        self.terrain = terrain

        self.name = "Freeze Spell"

        self.atk_val = 30

    def activate(self, target_pos, facteur):

        return [BombBullet(self.terrain, self.start_pt, target_pos, self.atk_val*(facteur+1), REAL_LIGHT_BLUE)]


class EarthQuake(SpecialPower):

    need_target = 0

    def __init__(self, terrain):

        self.terrain = terrain

        self.name = "Earth Quake"

        self.atk_val = 5

    def activate(self, facteur):

        to_return = []

        for ent in self.terrain.entities:

            to_return.append(MovingBullet(self.terrain, ent.center, ent, self.atk_val))

        return to_return


class Volcano:

    need_target = 0

    def __init__(self, terrain):

        self.start_pt = terrain.get_tile(terrain.base_coor).center.copy()

        self.start_pt[1] += terrain.tile_size//3

        self.vect = [0, -1]

        self.terrain = terrain

        self.name = "Volcano"

        self.atk_val = 250

        self.ready_to_shoot = 0

        self.to_spawn_nb = 12

        self.spawn_time = 25

        self.spawn_compteur = self.spawn_time

        self.facteur = 0

        self.color = DARK_GREY

    def activate(self, facteur):

        self.facteur = facteur

        self.terrain.spectres.append(self)

        return []

    def update(self, graphic):

        if not self.ready_to_shoot:  # drawing graphic animation

            self.vect[1] -= 1

            if abs(self.vect[1]) > self.terrain.tile_size:  # time to shoot

                self.ready_to_shoot = 1

        else:

            self.spawn_compteur -= 1

            if not self.spawn_compteur:

                self.spawn_compteur = self.spawn_time

                rand_pos = [random.randint(0, screen_width), random.randint(0, screen_height)]

                self.terrain.bullets.append(BombBullet(self.terrain, self.start_pt, rand_pos, self.atk_val*(self.facteur+1)))

                self.to_spawn_nb -= 1

                if not self.to_spawn_nb:

                    for x in range(6):

                        rand_pos = [random.randint(0, screen_width), random.randint(0, screen_height)]

                        self.terrain.bullets.append(BombBullet(self.terrain, self.start_pt, rand_pos, self.atk_val*(self.facteur+1)))

                    self.terrain.bullets.append(BombBullet(self.terrain, self.start_pt, self.start_pt, self.atk_val*(self.facteur+1)))

                    return -1  # end of volcano


        if graphic:

            Volcano.draw(self)

    def draw(self):

        draw_triangle_from_vect(self.start_pt, self.vect, color=self.color)


# entities on the grid, with grid coordinates (don't move)
class StaticEntity:

    def __init__(self, coor, terrain, lifes):
        """ grid entities (obstacles, player defenses..) """

        self.total_lifes = lifes

        self.coor_x = coor[0]  # coordinates in the board (tile index)

        self.coor_y = coor[1]

        self.x, self.y = terrain.get_pos_of_coor(coor)  # position in the screen

        self.center = [self.x+terrain.tile_size//2, self.y+terrain.tile_size//2]

        self.terrain = terrain

    def out_terrain(self):

        return out_screen(self.x, self.y, self.cols, self.rows)

    def draw(self):

        if self.lifes != self.total_lifes:

            draw_barre_vie(self.lifes/self.total_lifes, self.center[0]-self.radius//2, self.center[1], self.radius)


class Tree(StaticEntity):

    def __init__(self, coor, terrain):

       life_borne = [300, 500]

       self.lifes = random.randint(life_borne[0], life_borne[1])

       self.radius = int(set_val_to_different_array(life_borne, [terrain.tile_size//5, terrain.tile_size//3], self.lifes))

       StaticEntity.__init__(self, coor, terrain, self.lifes)
       
    def draw(self):

        pygame.draw.circle(screen, ORANGE, self.center, self.radius)

        StaticEntity.draw(self)


class Rock(StaticEntity):

    def __init__(self, coor, terrain):

       life_borne = [700, 1000]

       self.lifes = random.randint(life_borne[0], life_borne[1])

       self.radius = int(set_val_to_different_array(life_borne, [terrain.tile_size//5, terrain.tile_size//3], self.lifes))

       StaticEntity.__init__(self, coor, terrain, self.lifes)

    def draw(self):

        pygame.draw.circle(screen, GREY, self.center, self.radius)

        StaticEntity.draw(self)


class Bush(StaticEntity):

    def __init__(self, coor, terrain):

       life_borne = [100, 250]

       self.lifes = random.randint(life_borne[0], life_borne[1])

       self.radius = int(set_val_to_different_array(life_borne, [terrain.tile_size//5, terrain.tile_size//3], self.lifes))

       StaticEntity.__init__(self, coor, terrain, self.lifes)

    def draw(self):

        pygame.draw.circle(screen, GREEN, self.center, self.radius)

        StaticEntity.draw(self)


class Defense(StaticEntity):

    circle_width = 3

    def __init__(self, coor, terrain, cost, lifes):

        self.cost = cost

        StaticEntity.__init__(self, coor, terrain, lifes)

        self.active = False

        self.niveau = 1

    def level_up(self):

        self.niveau += 1

        self.lifes += self.total_lifes

        self.total_lifes *= 2

    def draw(self):

        pos = [self.center[0]+20, self.center[1]+20]

        pygame.draw.circle(screen, WHITE, pos, 9)

        aff_txt(str(self.niveau), pos[0]-5, pos[1]-10, taille=20)

        StaticEntity.draw(self)

    def die(self):

        self.terrain.set_tile([self.coor_x, self.coor_y], 0)


class Base(Defense):

    def __init__(self, coor, terrain):

       self.lifes = 10**5

       Defense.__init__(self, coor, terrain, 0, self.lifes)

       self.total_lifes = self.lifes

       self.radius = floor(self.terrain.tile_size/2.5)

    def draw(self):

        pygame.draw.circle(screen, PURPLE, self.center, self.radius)

        StaticEntity.draw(self)


class Wall(Defense):

    def __init__(self, coor, terrain, cost):

        self.name = "wall"

        self.lifes = 10**4*4

        Defense.__init__(self, coor, terrain, cost, self.lifes)

        self.radius = self.terrain.tile_size/4

        self.pyg_rect = pygame.Rect(self.center[0]-self.radius, self.center[1]-self.radius, self.radius*2, self.radius*2)

    def draw(self):

        pygame.draw.rect(screen, BLACK, self.pyg_rect)

        pygame.draw.rect(screen, GREY, self.pyg_rect, 5)

        Defense.draw(self)


class Mine(Defense):

    def __init__(self, coor, terrain, cost, lifes):

        Defense.__init__(self, coor, terrain, cost, lifes)

        self.radius = self.terrain.tile_size/4

        self.pyg_rect = pygame.Rect(self.center[0]-self.radius, self.center[1]-self.radius, self.radius*2, self.radius*2)

        self.compteur = 0

        self.wait_time = 600  # ten secs

    def update(self):

        self.compteur += 1

        if self.compteur == self.wait_time:

            self.compteur = 0

            return self.earn

    def draw(self):

        pygame.draw.rect(screen, DARK_BROWN, self.pyg_rect)

        pygame.draw.rect(screen, BLACK, self.pyg_rect, 3)


class GoldMine(Mine):

    def __init__(self, coor, terrain, cost):

        self.name = "gold mine"

        self.lifes = 10**4 / 4

        self.earn = 150

        Mine.__init__(self, coor, terrain, cost, self.lifes)

    def level_up(self):

        Defense.level_up(self)

        if self.wait_time < 1800:  # 30 secs

            self.wait_time += 120

        self.earn *= 2.2

        self.earn = int(self.earn)

    def draw(self):

        Mine.draw(self)

        draw_coin(self.x, self.y, [30, 30], [12])

        Defense.draw(self)


class PowerMine(Mine):

    def __init__(self, coor, terrain, cost):

        self.name = "power mine"

        self.lifes = 10**4

        self.earn = 1

        Mine.__init__(self, coor, terrain, cost, self.lifes)

    def level_up(self):

        Defense.level_up(self)

        self.earn += 1

    def draw(self):

        Mine.draw(self)

        draw_fire(self.x, self.y, [30, 30], [12, RED])

        draw_fire(self.x, self.y, [30, 30], [6, YELLOW])

        Defense.draw(self)


class ShootingDefense(Defense):

    def __init__(self, coor, terrain, cost, lifes):

        self.intern_clock = 0

        Defense.__init__(self, coor, terrain, cost, self.lifes)

    def update(self):

        if self.intern_clock == self.shooting_time:

            return 1

        else:

            self.intern_clock += 1

    def shoot(self):

        self.intern_clock = 0

    def level_up(self):

        Defense.level_up(self)

        self.atk_val *= 2

    def draw(self):

        if self.active:

            pygame.draw.circle(screen, RED, self.center, self.action_radius, Defense.circle_width)

        Defense.draw(self)


class Mortar(ShootingDefense):

    def __init__(self, coor, terrain, cost):

       self.name = "mortar"

       self.lifes = 10**4*2

       ShootingDefense.__init__(self, coor, terrain, cost, self.lifes)

       self.radius = floor(self.terrain.tile_size/2.5)

       self.action_radius = 200

       self.shooting_time = 180

       self.atk_val = 80

    def draw(self):

        pygame.draw.circle(screen, GREY, self.center, self.radius)

        pygame.draw.circle(screen, RED, self.center, self.radius//2)

        ShootingDefense.draw(self)

    def shoot(self, entity):

        ShootingDefense.shoot(self)

        return MortarBullet(self.terrain, self.center, entity, self.atk_val)


class Gun(ShootingDefense):

    def __init__(self, coor, terrain, cost):

        self.name = "gun"

        self.lifes = 10**4*(1/2)

        ShootingDefense.__init__(self, coor, terrain, cost, self.lifes)

        self.radius = floor(self.terrain.tile_size/2.3)

        self.action_radius = 175

        self.shooting_time = 20

        self.atk_val = 45

    def draw(self):

        pygame.draw.circle(screen, BLACK, self.center, self.radius)

        pygame.draw.circle(screen, GREEN, self.center, self.radius//2)

        ShootingDefense.draw(self)

    def shoot(self, entity):

        ShootingDefense.shoot(self)

        return GunBullet(self.terrain, self.center, entity, self.atk_val)


class Laser(ShootingDefense):

    def __init__(self, coor, terrain, cost):

        self.name = "laser"

        self.lifes = 10**4*(1/2)

        ShootingDefense.__init__(self, coor, terrain, cost, self.lifes)

        self.radius = floor(self.terrain.tile_size/3)

        self.action_radius = 145

        self.shooting_time = 80

        self.atk_val = 120

    def draw(self):

        pygame.draw.circle(screen, BLUE, self.center, self.radius)

        pygame.draw.circle(screen, YELLOW, self.center, self.radius//2)

        ShootingDefense.draw(self)

    def shoot(self, entity):

        ShootingDefense.shoot(self)

        return LaserBullet(self.terrain, self.center, entity, self.atk_val)


class SniperTower(ShootingDefense):

    def __init__(self, coor, terrain, cost):

        self.name = "sniper tower"

        self.lifes = 10**4*(1/8)

        ShootingDefense.__init__(self, coor, terrain, cost, self.lifes)

        self.radius = floor(self.terrain.tile_size/2.3)

        self.action_radius = 280

        self.shooting_time = 120

        self.atk_val = 200

        x, y = self.center

        self.losange_points = [[x, y-self.radius],
                               [x+self.radius, y],
                               [x, y+self.radius],
                               [x-self.radius, y]]

    def draw(self):

        pygame.draw.circle(screen, BLACK, self.center, self.radius)

        pygame.draw.polygon(screen, PURPLE, self.losange_points)

        ShootingDefense.draw(self)

    def shoot(self, entity):

        ShootingDefense.shoot(self)

        return SniperBullet(self.terrain, self.center, entity, self.atk_val)


class InfernoTower(ShootingDefense):

    def __init__(self, coor, terrain, cost):

        self.name = "inferno tower"

        self.lifes = 10**4

        ShootingDefense.__init__(self, coor, terrain, cost, self.lifes)

        self.radius = floor(self.terrain.tile_size/2.3)

        self.action_radius = 175

        self.shooting_time = 180

        self.atk_val = 1

        x, y = self.center

        self.losange_points = [[x, y-self.radius],
                               [x+self.radius, y],
                               [x, y+self.radius],
                               [x-self.radius, y]]

        self.pyg_rect = pygame.Rect(self.center[0]-self.radius, self.center[1]-self.radius, self.radius*2, self.radius*2)

        self.last_target = 0

        self.cumule = 0

    def update(self):

        return 1

    def shoot(self, target):

        if target == self.last_target:

            self.cumule += 1

        else:

            self.last_target = target

            self.cumule = 0

        atk_val = self.atk_val * self.niveau * self.cumule

        return LineBullet(self.terrain, self.center, target, atk_val)

    def draw(self):

        pygame.draw.rect(screen, RED, self.pyg_rect)

        pygame.draw.circle(screen, YELLOW, self.center, self.radius)

        pygame.draw.polygon(screen, RED, self.losange_points)

        ShootingDefense.draw(self)


class FreezeTower(ShootingDefense):

    def __init__(self, coor, terrain, cost):

        self.name = "freeze tower"

        self.lifes = 10**4*(1/2)

        ShootingDefense.__init__(self, coor, terrain, cost, self.lifes)

        self.radius = floor(self.terrain.tile_size/2.3)

        self.action_radius = 300

        self.shooting_time = 20

        self.atk_val = 10

        x, y, = self.center

        self.losange_points = [[x, y-self.radius],
                               [x+self.radius, y],
                               [x, y+self.radius],
                               [x-self.radius, y]]

    def draw(self):

        pygame.draw.circle(screen, DARK_BLUE, self.center, self.radius)

        pygame.draw.polygon(screen, LIGHT_BLUE, self.losange_points)

        ShootingDefense.draw(self)

    def shoot(self, entity):

        ShootingDefense.shoot(self)

        if random.randint(0, 10):

            return GunBullet(self.terrain, self.center, entity, self.atk_val, LIGHT_BLUE)

        else:

            return GunBullet(self.terrain, self.center, entity, self.atk_val, REAL_LIGHT_BLUE)


# Ennemy classes (soldiers..), theses classes keep track of moving entities


class MovingEntity:

    def __init__(self, terrain, pos):

        self.terrain = terrain

        self.x, self.y = pos

        self.center = [self.x, self.y]

    def apply_vect(self):

        self.x += self.vect[0]

        self.y += self.vect[1]

        self.center = [self.x, self.y]

    def move(self, x, y):

        self.x += x

        self.y += y

        self.center = [self.x, self.y]

    def set_vector(self):

        self.vect = sum_arrays(self.next_target, [self.x, self.y], 1, -1)

        self.vect = get_normalized_vector(self.vect, self.speed)


class Bullet:

    def __init__(self, terrain, pos, target, atk_val):

        MovingEntity.__init__(self, terrain, pos)

        self.target = target

        self.next_target = target.center

        self.atk_val = atk_val

##        if isinstance(self.target, MovingEntity):
##
##            self.speed = self.target.speed * self.rel_speed
##
##        else:
##
##            self.speed = self.rel_speed

        MovingEntity.set_vector(self)

    def update(self, check_target=1):

        # moves

        MovingEntity.apply_vect(self)

        if check_target:  # not needed for laserbullet

            # checks if hit target

            if collide_circle_to_circle(self.center, self.radius, self.target.center, self.target.radius/2):  # target's radius divided by two for mortar bullet to explode only when really within ennemies

                return 1


class GunBullet(MovingEntity):

    def __init__(self, terrain, pos, target, atk_val, color=(0, 0, 0)):

        self.color = color

        self.radius = 4

        self.speed = 3

        self.froz_val = 60

        Bullet.__init__(self, terrain, pos, target, atk_val)

    def update(self, graphic):

        if isinstance(self.target, MovingEntity):
            # updates info that might have changed since last update

            #self.speed = self.target.speed * self.rel_speed

            self.next_target = self.target.center

            MovingEntity.set_vector(self)

        # draws if needed
        if graphic:

            GunBullet.draw(self)

        if Bullet.update(self):

            return [[self.target, self.atk_val, 1]]  # 1 : bullet will get destroyed

    def draw(self):

        pygame.draw.circle(screen, self.color, [int(self.x), int(self.y)], self.radius)


class SniperBullet(MovingEntity):

    def __init__(self, terrain, pos, target, atk_val):

        self.color = RED

        self.radius = 4

        self.speed = 8

        Bullet.__init__(self, terrain, pos, target, atk_val)

    def update(self, graphic):

        if isinstance(self.target, MovingEntity):
            # updates info that might have changed since last update

            #self.speed = self.target.speed * self.rel_speed

            self.next_target = self.target.center

            MovingEntity.set_vector(self)

        # draws if needed
        if graphic:

            GunBullet.draw(self)

        if Bullet.update(self):

            return [[self.target, self.atk_val, 1]]  # 1 : bullet will get destroyed

    def draw(self):

        draw_triangle_from_vect(self.center, self.vect, 10)


class LaserBullet(MovingEntity):

    def __init__(self, terrain, pos, target, atk_val):

        self.color = BLUE

        self.radius = 4

        self.speed = 5

        Bullet.__init__(self, terrain, pos, target, atk_val)

        self.hit_entities = []  # stores entities it has hit, cause it can only hit once

    def update(self, graphic):

        to_return = []

        if graphic:

            LaserBullet.draw(self)

        Bullet.update(self, 0)

        for index in range(len(self.terrain.entities)-1,-1, -1):

            entity = self.terrain.entities[index]

            if (not entity in self.hit_entities) and collide_circle_to_circle(self.center, self.radius, entity.center, entity.radius):

                self.hit_entities.append(entity)

                to_return.append([entity, self.atk_val, 0])

        if out_screen(self.x, self.y, screen_width, screen_height, 0, 0):

            return [[0, 0, 1]]

        return to_return

    def draw(self):

        pygame.draw.circle(screen, self.color, [int(self.x), int(self.y)], self.radius)


class MortarBullet(MovingEntity):

    def __init__(self, terrain, pos, target, atk_val):

        self.color = BLACK

        self.color2 = RED

        self.radius = 8

        self.speed = 2

        Bullet.__init__(self, terrain, pos, target, atk_val)

        self.explosion_radius = 50

    def update(self, graphic):

        if isinstance(self.target, MovingEntity):

            # updates info that might have changed since last update

            #self.speed = self.target.speed * self.rel_speed

            self.next_target = self.target.center

            MovingEntity.set_vector(self)

        # draws bullet
        if graphic:

            MortarBullet.draw(self)

        # checks if reached target, if yes, will explode
        hit = Bullet.update(self)

        if hit:

            to_return = [[0, 0, 1]]

            for index in range(len(self.terrain.entities)-1, -1, -1):

                entity = self.terrain.entities[index]

                if collide_circle_to_circle(self.center, self.explosion_radius, entity.center, entity.radius):

                    to_return.append([entity, self.atk_val, 1])

            return to_return

    def draw(self):

        pygame.draw.circle(screen, self.color, [int(self.x), int(self.y)], self.radius)

        pygame.draw.circle(screen, self.color2, [int(self.x), int(self.y)], self.radius//2)


class LineBullet:

    def __init__(self, terrain, pos, target, atk_val):

        self.terrain = terrain

        self.pos = pos

        self.target = target

        self.atk_val = atk_val

        self.color = RED

    def update(self, graphic):

        # draws bullet
        if graphic:

            LineBullet.draw(self)

        return [[self.target, self.atk_val, 1]]

    def draw(self):

        tx, ty = self.target.center

        pygame.draw.line(screen, self.color, self.pos, [int(tx), int(ty)], 5)


class BombBullet(MovingEntity):

    def __init__(self, terrain, pos, pos_target, atk_val, color=None):

        if color == None:

            self.color = RED

        else:

            self.color = color

        if self.color == REAL_LIGHT_BLUE:

            self.froz_val = 300  # 5 secs

        self.radius = 16

        self.speed = 6

        self.terrain = terrain

        self.center = pos

        self.x, self.y = pos

        self.next_target = pos_target

        self.atk_val = atk_val

        self.explosion_radius = 75

        MovingEntity.set_vector(self)

        self.already_hit = 0

    def update(self, graphic):

        # draws bullet
        if graphic:

            BombBullet.draw(self)

        if self.already_hit:  # when exploded, bullet doesn't move anymore

            self.radius += 1

            if self.radius > self.explosion_radius:  # after the explosion, bullet's destroyed

                return [[0, 0, 1]]

        else:

            MovingEntity.apply_vect(self)

        # checks if reached target, if yes, will explode

        hit = collide_circle_to_circle(self.center, self.radius, self.next_target, 1)

        if hit and (not self.already_hit):

            self.already_hit = 1

            to_return = [[0, 0, 0]]

            for index in range(len(self.terrain.entities)-1, -1, -1):

                entity = self.terrain.entities[index]

                if collide_circle_to_circle(self.center, self.explosion_radius, entity.center, entity.radius):

                    to_return.append([entity, self.atk_val, 0])

            return to_return

    def draw(self):

        pygame.draw.circle(screen, self.color, [int(self.x), int(self.y)], self.radius)


class MovingBullet(MovingEntity):

    def __init__(self, terrain, pos, target, atk_val):

        self.color = BLACK

        self.radius = 1

        self.rel_speed = 1.5

        self.x, self.y = pos

        self.explosion_radius = 75

        Bullet.__init__(self, terrain, pos, target, atk_val)

        self.lifes = 15        

    def update(self, graphic):

        # updates infos

        self.next_target = self.target.center

        MovingEntity.set_vector(self)

        MovingEntity.apply_vect(self)

        # checks if reached target, if yes, will explode

        hit = collide_circle_to_circle(self.center, self.radius, self.next_target, 1)

        if hit:

            dist = int(5*self.speed)

            self.target.move(random.randint(-dist, dist), random.randint(-dist, dist))

            self.lifes -= 1

            return [[self.target, self.atk_val, self.lifes==0]]

    def draw(self):

        pygame.draw.circle(screen, self.color, [int(self.x), int(self.y)], self.radius)


# ennemies (opponent entities)

class EnnemyEntity(MovingEntity):

    def __init__(self, terrain, lifes, pos=0):

        self.lifes += self.lifes * (terrain.dead_ops/50)  # new ennemy's health increases with each ennemy's death

        self.total_lifes = self.lifes

        self.atk_val += self.atk_val * (terrain.dead_ops/50)

        self.reward += int(self.reward * (terrain.dead_ops/500))  # needa stay integer for we're talking of coins ; coins growing slower

        self.frozen = 0

        self.real_frozen = 0

        self.normal_speed = self.speed

        self.small_speed = self.speed / 2.5

        self.powered = 0

        # sometimes ennemies are supercharged : they're stronger, and release a special power when they die
        if not random.randint(0, 20):

            self.powered = 1  # power reward

            self.small_speed = self.speed  # can't be slowed down

            self.total_lifes *= 3

            self.lifes *= 3

            self.atk_val *= 2
        ##

        if pos:

            self.x, self.y = pos

        else:

            self.x, self.y = get_random_edge_coor(screen_width, screen_height)

        MovingEntity.__init__(self, terrain, [self.x, self.y])  # [0, 0])  # 

        self.attacking = 0

        base = self.terrain.get_tile(self.terrain.base_coor)

        # checks base coordinates
        test = 0

        if test:

            pygame.draw.circle(screen, RED, base.center, 15)

            pygame.display.update()

            wait()
        ###

        self.side_segs = []

        self.next_target = base.center  # position of the target this moving entity will attack next, which means it's vector points to it

        MovingEntity.set_vector(self)  # initializes the vector

        self.targets = [base]  # first target of each ennemy is player's base

        EnnemyEntity.init_path(self)

    def init_path(self):
        # collision detection is made between circles that are making up the terrain and the segments on each side of the entity's vect

        pos = [self.x, self.y]

        check_distance = self.radius * 3  # radius of the check circle, that defines how far the parallel segments are

        width_interval = 30

        side_line_nb = check_distance // width_interval

        self.main_line = get_droite_from_pt(pos, self.next_target)  # [self.x+self.vect[0], self.y+self.vect[1]])

        self.main_seg = [pos, self.next_target]

        # getting the lines on each side of the main line

        perpendiculaire = get_perpendiculaire_from_d(self.main_line, pos)

        diffs = sum_arrays(self.next_target, pos, 1, -1)

        for x in range(1, side_line_nb+1):

            side_pt1, side_pt2 = collide_line_to_circle(pos, width_interval*x, perpendiculaire)  # points on each side of the line, on the perpendiculaire

            side_line1 = get_droite_from_pt(side_pt1, sum_arrays(side_pt1, self.vect))

            side_line2 = get_droite_from_pt(side_pt2, sum_arrays(side_pt2, self.vect))

            side_seg1 = [side_pt1, sum_arrays(side_pt1, diffs)]

            side_seg2 = [side_pt2, sum_arrays(side_pt2, diffs)]

            self.side_segs.append(side_seg1)

            self.side_segs.append(side_seg2)

        EnnemyEntity.init_targets(self)

        test = 0

        if test:

            for seg in self.side_segs:

                pygame.draw.line(screen, RED, seg[0], seg[1], 3)

            pygame.draw.line(screen, RED, self.main_seg[0], self.main_seg[1], 3)

            pygame.display.update()

            wait()

    def circle_on_path(self, circle):

        collision_pts = []

        for seg in self.side_segs:

            collision_pts.append(collide_segment_to_circle(circle.center, circle.radius, seg))

        collision_pts.append(collide_segment_to_circle(circle.center, circle.radius, self.main_seg))

        return any(collision_pts)  # colliding with the path, or path sides

    def init_targets(self):
        """ function designed to look for nearest obstacle (defenses, walls, eventually base)
            this entity will encounter to update faster while none is reached ;
            nearest goal of each creature should be updated when a new defense is built """

        pos = [self.x, self.y]

        # checking which tiles collide with path
        for line in self.terrain.tiles:

            for circle in line:

                if circle and (isinstance(circle, Defense)) and (not isinstance(circle, Base)): # tile's a defense

                    if EnnemyEntity.circle_on_path(self, circle):

                        self.targets.append(circle)

        # entity directly goes to nearest defense

        EnnemyEntity.set_next_target(self)

    def set_next_target(self):
        """ finds the next entity's target amongst self.target (all the defenses that come into account) """

        pos = [self.x, self.y]

        nearest_defense = min(self.targets, key=lambda x:get_distance(pos, x.center))

        self.next_target = nearest_defense.center

        MovingEntity.set_vector(self)
                               
    def update_targets(self, n_circle, new=1):
        """ will change the entity's vector and next target because of some event, if new==1 then a new entity (defense) has appeared, else a defense has been destroyed"""

        if new == 1:  # a defense has been added

            if not n_circle in self.targets:

                if EnnemyEntity.circle_on_path(self, n_circle):

                    pos = [self.x, self.y]

                    self.targets.append(n_circle)

                    # checks if this target is closer than current one
                    last_min_dist = get_distance(pos, self.next_target)

                    n_dist = get_distance(pos, n_circle.center)

                    if n_dist < last_min_dist:

                        self.next_target = n_circle.center

                        MovingEntity.set_vector(self)

        elif new == -1:  # a defense has been destroyed

            if n_circle in self.targets:  # this defense's not an option to chose anymore

                self.targets.remove(n_circle)

                n_circle_coor = n_circle.center

                if n_circle_coor == self.next_target:  # if it was entity's target, needa find a new one

                    self.attacking = 0  # entity doesn't attack anymore, for it's target has been destroyed

                    EnnemyEntity.set_next_target(self)

    def update(self):

        if self.real_frozen:

            self.real_frozen -= 1

        else:

            last_speed = self.speed

            if self.frozen > 0:

                self.frozen -= 1

                self.speed = self.small_speed

            else:

                self.speed = self.normal_speed

            if self.speed != last_speed:

                MovingEntity.set_vector(self)  # sets new speed to vector

            if not self.attacking:

                MovingEntity.apply_vect(self)

                diffs = sum_arrays([self.x, self.y], self.next_target, -1, 1)

                if self.shooting_radius > (abs(diffs[0]) + abs(diffs[1])):
                    
                    self.attacking = 1

            if self.attacking:

                return self.atk_val

    def hurt(self, atk_val):

        self.lifes -= atk_val

        if self.lifes <= 0:

            return -1

    def draw(self):

        if self.powered:

            pygame.draw.circle(screen, RED, [int(self.x), int(self.y)], self.radius, 5)

            pygame.draw.circle(screen, YELLOW, [int(self.x), int(self.y)], self.radius, 3)

        if self.lifes != self.total_lifes:

            draw_barre_vie(self.lifes/self.total_lifes, self.center[0]-self.radius//2, self.center[1], self.radius)

    def die(self):

        self.terrain.entities.remove(self)


class Soldier(EnnemyEntity):

    def __init__(self, terrain, inputs, pos=0):

        lifes, atk_val, reward = inputs

        self.lifes = lifes

        self.atk_val = atk_val

        self.reward = reward

        ##
        self.speed = 1

        self.radius = 15

        self.color = ORANGE

        EnnemyEntity.__init__(self, terrain, self.lifes, pos)  # calls parent function  (MovingEntity)

        self.shooting_radius = self.radius * 5

    def update(self, graphic):

        if graphic:

            Soldier.draw(self)

        return EnnemyEntity.update(self)

    def draw(self):

        if self.real_frozen:

            col = REAL_LIGHT_BLUE

        elif self.frozen:

            col = LIGHT_BLUE

        else:

            col = self.color

        pygame.draw.circle(screen, col, [int(self.x), int(self.y)], self.radius)

        EnnemyEntity.draw(self)


class SlimeSoldier(EnnemyEntity):

    def __init__(self, terrain, pos=0):

        self.speed = 0.7

        self.color = GREEN

        EnnemyEntity.__init__(self, terrain, self.lifes, pos)  # calls parent function  (MovingEntity)

        self.shooting_radius = self.radius * 5

        decal_size = 15

        self.decalage = [[-decal_size, -decal_size],
                         [-decal_size, decal_size],
                         [decal_size, -decal_size],
                         [decal_size, decal_size]]

    def update(self, graphic):

        if graphic:

            Soldier.draw(self)

        return EnnemyEntity.update(self)


class BigSlime(SlimeSoldier):

    def __init__(self, terrain, inputs, pos=0):

        lifes, atk_val, reward = inputs

        self.lifes = lifes

        self.atk_val = atk_val

        self.reward = reward

        ##
        self.radius = 30

        SlimeSoldier.__init__(self, terrain, pos)

    def die(self):

        EnnemyEntity.die(self)

        for x in range(4):

            self.terrain.entities.append(MediumSlime(self.terrain, self.terrain.entity_arg_dict[MediumSlime], sum_arrays(self.center, self.decalage[x])))


class MediumSlime(SlimeSoldier):

    def __init__(self, terrain, inputs, pos=0):

        lifes, atk_val, reward = inputs

        self.lifes = lifes

        self.atk_val = atk_val

        self.reward = reward

        ##
        self.radius = 20

        SlimeSoldier.__init__(self, terrain, pos)

    def die(self):

        EnnemyEntity.die(self)

        for x in range(4):

            self.terrain.entities.append(Soldier(self.terrain, self.terrain.entity_arg_dict[Soldier], sum_arrays(self.center, self.decalage[x])))


class Troll(EnnemyEntity):

    def __init__(self, terrain, inputs, pos=0):

        lifes, atk_val, reward = inputs

        self.lifes = lifes

        self.atk_val = atk_val

        self.reward = reward

        ##

        self.speed = 1

        self.radius = 45

        EnnemyEntity.__init__(self, terrain, self.lifes, pos)  # calls parent function  (MovingEntity)

        self.color = PURPLE

        self.shooting_radius = self.radius * 2

    def update(self, graphic):

        if graphic:

            Troll.draw(self)

        return EnnemyEntity.update(self)

    def draw(self):

        if self.real_frozen:

            col = REAL_LIGHT_BLUE

        elif self.frozen:

            col = LIGHT_BLUE

        else:

            col = self.color

        pygame.draw.circle(screen, col, [int(self.x), int(self.y)], self.radius)

        EnnemyEntity.draw(self)


class Sniper(EnnemyEntity):

    def __init__(self, terrain, inputs, pos=0):

        lifes, atk_val, reward = inputs

        self.lifes = lifes

        self.atk_val = atk_val

        self.reward = reward

        ##

        self.speed = .5

        self.radius = 20

        EnnemyEntity.__init__(self, terrain, self.lifes, pos)  # calls parent function  (MovingEntity)

        self.color = RED

        self.shooting_radius = self.radius * 7

    def update(self, graphic):

        if graphic:

            Sniper.draw(self)

        return EnnemyEntity.update(self)

    def draw(self):

        if self.real_frozen:

            col = REAL_LIGHT_BLUE

        elif self.frozen:

            col = LIGHT_BLUE

        else:

            col = self.color

        pygame.draw.circle(screen, col, [int(self.x), int(self.y)], self.radius)

        EnnemyEntity.draw(self)


class FastSoldier(EnnemyEntity):

    def __init__(self, terrain, inputs, pos=0):

        lifes, atk_val, reward = inputs

        self.lifes = lifes

        self.atk_val = atk_val

        self.reward = reward

        ##
        self.speed = 3

        self.radius = 15

        self.have_bomb = 1

        self.bomb_damage = 3000

        EnnemyEntity.__init__(self, terrain, self.lifes, pos)  # calls parent function  (MovingEntity)

        self.color1 = YELLOW

        self.color2 = RED

        self.shooting_radius = self.radius * 5

    def update(self, graphic):

        if graphic:

            FastSoldier.draw(self)

        damage = EnnemyEntity.update(self)

        if damage and self.have_bomb:

            self.have_bomb = 0

            return self.bomb_damage

        else:  # damage can be None too

            return damage

    def draw(self):

        if self.real_frozen:

            col1 = REAL_LIGHT_BLUE

            col2 = BLACK

        elif self.frozen:

            col1 = LIGHT_BLUE

            col2 = BLACK

        else:

            col1 = self.color1

            col2 = self.color2

        pygame.draw.circle(screen, col1, [int(self.x), int(self.y)], self.radius)

        if self.have_bomb:

            pygame.draw.circle(screen, col2, [int(self.x), int(self.y)], self.radius//2)

        EnnemyEntity.draw(self)


# other classes

class Terrain:

    def __init__(self, cols, panneau_pause, defense_dict, defense_cost_dict):

        self.panneau_pause = panneau_pause

        self.defense_dict = defense_dict  # to create the shop menus

        self.defense_cost_dict = defense_cost_dict

        self.sell_menu = ["upgrade", "sell"]  # to create (sell / upgrade) menu

        self.cols = cols

        self.x_margin = 10

        self.tile_size = (screen_width-2*self.x_margin)//cols

        self.up_margin = 100

        self.rows = floor((screen_height-self.up_margin)/self.tile_size)

        # defining the board, made out of tiles

        self.gui_board = []

        self.entities = []  # entities

        self.bullets = []  # entities shouted by the defenses

        self.spectres = []  # infos that will last for a little while (gold earn..)

        self.dead_ops = 0  #compteur d'ennemis tues

        self.active_defense = 0  # player can see it's (upgrade/sell) menu, action radius visible

        self.active_obstacle = 0  # obstacle that's attacked by defenses nearby

        self.obstacle_attacking_defenses = []  # defenses nearby active_obstacle

        for y in range(self.rows):

            self.gui_board.append([])

            for x in range(self.cols):

                if not ((y%2 == 1) and (x == self.cols-1)):  # last col of one row every two is deleted

                    x_pos = x*self.tile_size + (self.tile_size//2)*(1+(y%2==1)) + self.x_margin

                    y_pos = y*self.tile_size + self.tile_size//2 + self.up_margin

                    tile = [[x_pos, y_pos], self.tile_size//2]  # [x_pos, y*self.tile_size, self.tile_size, self.tile_size]

                    self.gui_board[-1].append(tile)

        self.tiles = [[0 for x in y] for y in self.gui_board]  # will contain "entities"

##        # graphic format of tiles
##        self.tile_centers = [[[int(t[0]+t[2]/2)+self.x_margin, int(t[1]+t[3]/2)+self.up_margin], int(t[3]/2)] for t in self.tiles]  # [pygame.Rect(t[0], t[1], t[2], t[3]) for t in tiles]

        # player's base, he must protect it
        self.base_coor = [self.rows//2, self.cols//2]

        home_base = Base(self.base_coor, self)

        Terrain.append_entity(self, self.base_coor, home_base)

        # placing random stuff (decoration, obstacles)

        entities = [Rock, Bush, Tree]

        for x in range(random.randint(10, 20)):

            rand_coor = [random.randint(0, self.rows-1), random.randint(0, self.cols-2)]  # cols-2 : cause one row out of two is smaller

            if not Terrain.get_tile(self, rand_coor):  # empty tile

                n_entity = random.choice(entities)(rand_coor, self)

                Terrain.append_entity(self, rand_coor, n_entity)

        self.entity_type = [Soldier, Troll, FastSoldier, BigSlime, MediumSlime, Sniper]

        self.weight_list = [0.6, 0.05, 0.1, 0.1, 0.05, 0.1]  # [0, 0, 0, 0.5, 0.5]  # [0.85, 0.02, 0.13]  # [0, 1, 0]  # [0, 0, 1]  #

        self.entity_arg_dict = {Soldier    :[40 , 1 , 20],
                                Troll      :[500, 15, 200],
                                BigSlime   :[250 , 5 , 100],
                                MediumSlime:[125 , 2 , 60],
                                Sniper     :[50 , 10, 75],
                                FastSoldier:[100 , 1 , 75],}

        self.spawn_time = 110

        self.next_wave = 35  # 0

        self.active_wave = 0

        self.wave_interval = 30

        self.interval_count = 0

        self.wave_nb = 15

        self.wave_count = 0

        self.wave_spot = [0, 0]

        self.last_mouse_coor = [0, 0]

        self.level_spawning = 0  # only when player's playing levels, will get filled in game loop if necessary

        self.time_compteur = -1

        #print(Terrain.get_coor_of_pos(self, Terrain.get_pos_of_coor(self, [4, 4])))  # check

    def print_terrain(self):

        for x in range(len(self.tiles)):

            print(x, *self.tiles[x])

    def get_stearing_path_to_center(self, coor):
        """

        returns a path (for ennemies) from a coor(screen edge) to the center,
        uses a path finding algorithm that should try to find a way
        without walls, so tries to avoid them, but not to much
        (a wall in a path "adds" weight to this choice,
         so it's less likely to get chosen, but can be chosen
         if the wall is long enough)

         -> in fact not, the entities don't care about the grid, which is for defenses, and they attack a wall or anything else when they spot it

        """

        return sum_arrays(self.base_coor, coor, -1, 1)  # vect from coor to base  #  wow, what an algorithm

    def update(self, graphic, player_preparing):

        if player_preparing != 1:

            self.time_compteur += 1

            # checks if player has won
            if (self.entities == []) and (self.level_spawning == []):  # no more entities on terrain and to spawn

                return "level_win"

        test = 0
        
        if test and (not random.randint(0, 180)):

            print(len(self.bullets))

        # rewards won by player
        coins = 0

        power_coins = 0

        # ennemy spawning

        if player_preparing == 0:

            if self.active_wave:

                self.interval_count += 1

                if self.interval_count == self.wave_interval:

                    self.interval_count = 0

                    self.wave_count += 1

                    this_spot = sum_arrays(self.wave_spot, get_random_vector(150))

                    rand_ent = self.entity_type[random_weighted_choice(self.weight_list, 1)]

                    args = self.entity_arg_dict[rand_ent]

                    entity = rand_ent(self, args, this_spot)

                    self.entities.append(entity)

                    if self.wave_count == self.wave_nb:

                        self.active_wave = 0

                        self.wave_count = 0

            else:

                # deals with ennemy spawning
                self.spawn_time -= 1

                if self.spawn_time == 0:

                    self.spawn_time = 60

                    self.next_wave -= 1

                    rand_ent = self.entity_type[random_weighted_choice(self.weight_list, 1)]

                    args = self.entity_arg_dict[rand_ent]

                    entity = rand_ent(self, args)

                    self.entities.append(entity)

                if self.next_wave == 0:

                    self.next_wave = random.randint(25, 35)

                    self.active_wave = 1

                    self.wave_spot = get_random_edge_coor(screen_width+150, screen_height+150, -150, -150)

                    self.spectres.append(WaveSign(self.wave_spot))

        elif player_preparing == -1:

            if self.level_spawning != []:

                # for levels
                needed_time = self.level_spawning[0][0]

                if self.time_compteur == needed_time:

                    chosen_entity = self.entity_type[self.level_spawning[0][1]]

                    args = self.entity_arg_dict[chosen_entity]

                    pos = [self.level_spawning[0][2], self.level_spawning[0][3]]

                    entity = chosen_entity(self, args, pos)

                    self.entities.append(entity)

                    del self.level_spawning[0]

                    if (self.level_spawning != []) and (self.level_spawning[0][0] == self.time_compteur):

                        self.time_compteur -= 1  # if next should have been spawned at the same time, will be spawned next frame


        # terrain's drawn first
        if graphic:

            Terrain.draw(self)

        # updates the entities (player's ennemies) ; they attack ..

        should_update_vects = []

        for entity in self.entities:

            atk = entity.update(graphic)

            if atk:

                coor = Terrain.get_coor_of_pos(self, entity.next_target)  # get coor of attacked defense

                attacked_entity = Terrain.get_tile(self, coor)

                if attacked_entity:

                    attacked_entity.lifes -= atk  # ennemy's attacking a defense

                    if attacked_entity.lifes < 0:  #defense is dead

                        if isinstance(attacked_entity, Base):

                            return "gameover"

                        attacked_entity.die()

                        if not coor in should_update_vects:

                            should_update_vects.append(attacked_entity)

        # updates the vectors of all entities when some defense's been destroyed

        if should_update_vects != []:

            for destroyed_entity in should_update_vects:

                for entity in self.entities:

                    entity.update_targets(destroyed_entity, -1)

        # updates the player's defenses (throw bullets..)

        if player_preparing != 1:  # should not update defenses (gold mine, destroying obstacles..)

            for defense in Terrain.get_defenses(self):

                if isinstance(defense, ShootingDefense):

                    shoot = defense.update()

                    if shoot:

                        if defense in self.obstacle_attacking_defenses:

                            obst = Terrain.get_tile(self, Terrain.get_coor_of_pos(self, self.active_obstacle[0]))

                            self.bullets.append(defense.shoot(obst))

                        elif (self.entities != []):

                            if isinstance(defense, FreezeTower):  # FreezeTower is targetting ennemies at random, to slow them all down

                                targets = [ent for ent in self.entities if ((get_distance(ent.center, defense.center)-ent.radius) < defense.action_radius)]

                                if targets:

                                    self.bullets.append(defense.shoot(random.choice(targets)))

                            else:

                                nearest_target = min(self.entities, key=lambda x:get_distance(x.center, defense.center))

                                if defense.action_radius > (get_distance(nearest_target.center, defense.center)-nearest_target.radius):

                                    self.bullets.append(defense.shoot(nearest_target))

                elif isinstance(defense, Mine):

                    earn = defense.update()

                    if earn:

                        if isinstance(defense, GoldMine):

                            if graphic:

                                self.spectres.append(Spectre(defense.center, earn))

                            coins += earn

                        elif isinstance(defense, PowerMine):

                            if graphic:

                                self.spectres.append(Spectre(defense.center, earn, 1))

                            power_coins += earn

        # updates the bullets thrown by player's defenses
        for index in range(len(self.bullets)-1, -1, -1):

            bullet = self.bullets[index]

            hit_ennemies = bullet.update(graphic)

            if hit_ennemies:  # hit is an array of all [hit entities, damages, kill_bullet]

                if bullet.color == LIGHT_BLUE:  # freezing bullet

                    frozen = 100

                elif bullet.color == REAL_LIGHT_BLUE:

                    real_frozen = bullet.froz_val

                    frozen = 0

                else:  # normalbullet

                    frozen = 0

                    real_frozen = 0

                for hit_info in hit_ennemies:

                    hit_entity, damage_val, del_bullet = hit_info

                    if del_bullet:

                        if bullet in self.bullets:  # for mortar for ex bullet might return several hit message (in one update), with several destroy orders

                            del self.bullets[index]

                    if hit_entity:

                        hit_entity.lifes -= damage_val

                        if frozen:

                            hit_entity.frozen = frozen

                        elif real_frozen:

                            hit_entity.real_frozen = real_frozen

                        # Attcked entity is an ENNEMY
                        if (hit_entity in self.entities) and (hit_entity.lifes <= 0):  # cause bullet might have been sent just before entitie's death

                            self.dead_ops += 1

                            if hit_entity.powered:  # power reward

                                power_coins += 1

                                if graphic:

                                    self.spectres.append(Spectre(sum_arrays(hit_entity.center, [0, 30]), 1, 1))

                            # coin reward
                            coins += hit_entity.reward

                            if graphic:

                                self.spectres.append(Spectre(hit_entity.center, hit_entity.reward))

                            hit_entity.die()

                        # obstacle destroyed
                        elif isinstance(hit_entity, StaticEntity) and (hit_entity.lifes <= 0):

                            obst_pos = hit_entity.center

                            obst_coor = Terrain.get_coor_of_pos(self, obst_pos)

                            if self.active_obstacle == [obst_pos, hit_entity.radius]:

                                self.active_obstacle = 0

                            if Terrain.get_tile(self, obst_coor) != 0:

                                Terrain.set_tile(self, obst_coor, 0)

                            self.obstacle_attacking_defenses = []

        for index in range(len(self.spectres)-1, -1, -1):

            spec = self.spectres[index]

            if isinstance(spec, Spectre) and graphic:  # there are some other instances, as the volcano, stored in spectres

                if spec.update():  # draws spectre and counts if not dead already (lives for 60 frames)

                    del self.spectres[index]

            elif not isinstance(spec, Spectre):  # non spectral entities

                if spec.update(graphic):

                    del self.spectres[index]

        return [coins, power_coins]

    def get_defenses(self):

        defs = []

        for line in self.tiles:

            for tile in line:

                if isinstance(tile, Defense):

                    defs.append(tile)

        return defs

    def set_new_active_obstacle(self, obst):
        """ player has chosed to destroy an obstacle, all defenses that can reach obstacle make it their target """

        for defense in Terrain.get_defenses(self):

            if isinstance(defense, ShootingDefense):

                if (get_distance(obst.center, defense.center)-obst.radius) < defense.action_radius:   # defense can reach obstacle

                    self.obstacle_attacking_defenses.append(defense)

        self.active_obstacle = [obst.center, obst.radius]

    def draw(self):
        """ draws background then entities of terrain (tiles, trees, ..) """

        # draws bg

        screen.fill(BROWN)

        self.panneau_pause.draw()

        # draws tiles

        for y in range(len(self.gui_board)):

            for x in range(len(self.gui_board[y])):

                center = self.gui_board[y][x]

                if self.tiles[y][x]:

                    pygame.draw.circle(screen, WHITE, center[0], center[1], 3)

                    self.tiles[y][x].draw()

        if self.active_obstacle:

            x, y = self.active_obstacle[0]

            draw_fleche(x+3, y-25, -5, RED)

    def get_coor_of_pos(self, pos):
        """ returns the coors on the grid of a pos on the screen """

        pos = [pos[0]-self.x_margin, pos[1]-self.up_margin]  # rectified pos without margins

        row = pos[1]//self.tile_size

        if row%2 == 1:

            pos[0] -= self.tile_size//2

        return [row, pos[0]//self.tile_size]

    def get_pos_of_coor(self, coor):
        """ returns the coors on the grid of a pos on the screen ; coor[row, col]"""

        y = coor[0]*self.tile_size

        x = coor[1]*self.tile_size

        if coor[0]%2 == 1:

            x += self.tile_size//2

        x += self.x_margin

        y += self.up_margin

        return [x, y]

    def get_tile(self, tile_coor):
        """ returns tile of tiles; tile_coor[row][col] """

        return self.tiles[tile_coor[0]][tile_coor[1]]

    def set_tile(self, tile_coor, stuff):
        """ sets a tile in the terrain (tiles) ; tile_coor[row][col] """

        if isinstance(Terrain.get_tile(self, tile_coor), Defense):

            defense = Terrain.get_tile(self, tile_coor)

            for entity in self.entities:

                entity.update_targets(defense, -1)

        self.tiles[tile_coor[0]][tile_coor[1]] = stuff

    def append_entity(self, coor, to_append_entity):

        self.tiles[coor[0]][coor[1]] = to_append_entity

        if isinstance(to_append_entity, Defense):

            if not isinstance(to_append_entity, Base):  # all the entities (moving ennemies) on the board are updated, cause new defense might be on their way

                for entity in self.entities:

                    entity.update_targets(to_append_entity, 1)

            if isinstance(to_append_entity, ShootingDefense):

                if self.active_obstacle and ((get_distance(self.active_obstacle[0], to_append_entity.center)-self.active_obstacle[1]) < to_append_entity.action_radius):   # defense can reach obstacle

                     self.obstacle_attacking_defenses.append(to_append_entity)

    def deal_with_click(self, mouse_pos):

        mouse_coor_on_grid = Terrain.get_coor_of_pos(self, mouse_pos)

        if (mouse_coor_on_grid[1] < 0) or ((mouse_coor_on_grid[0]%2 == 1) and (mouse_coor_on_grid[1] == 12)) or (mouse_coor_on_grid[1] > 12):

            return

        tile = Terrain.get_tile(self, mouse_coor_on_grid)

        if tile:

            if not isinstance(tile, Base):

                if isinstance(tile, Defense):  # Player has clicked on a defense

                    if self.active_defense:

                        self.active_defense.active = False

                    self.active_defense = tile

                    self.active_defense.active = True

                    if tile.niveau < 9:

                        upgrade_price = self.defense_cost_dict[tile.name]*2**tile.niveau

                        sell_price = (self.defense_cost_dict[tile.name]*2**(tile.niveau-1))//2

                        sell_menu = self.sell_menu

                        prices = [upgrade_price, sell_price]

                        return Menu(self, Terrain.get_coor_of_pos(self, tile.center), sell_menu, 1, prices)  # returns a menu (evolution or sell options)  # self input is in fact this terrain instance

                    else:

                        sell_price = (self.defense_cost_dict[tile.name]*2**(tile.niveau-1))//2

                        sell_menu = [self.sell_menu[1]]

                        prices = [sell_price]

                        return Menu(self, Terrain.get_coor_of_pos(self, tile.center), sell_menu, 1, prices)

                else:  # Player has clicked on an obstacle

                    n_obst = [tile.center, tile.radius]

                    if self.active_obstacle == n_obst:

                        self.active_obstacle = 0

                        self.obstacle_attacking_defenses = []                   

                    else:

                        # defenses in range of the obstacle target it
                        Terrain.set_new_active_obstacle(self, tile)

        else:  # player has clicked on an empty tile

            # returns a menu (buying options)

            prices = [self.defense_cost_dict[x] for x in list(self.defense_dict.keys())]

            return Menu(self, mouse_coor_on_grid, list(self.defense_dict.keys()), 0, prices)  # returns a defense buying menu for player ; self input is in fact this terrain instance


class Player:

    def __init__(self, width):

        self.gold = 500

        self.piece_x = 20

        self.piece_y = 20

        self.coin_margin = 20

        self.coin_rad = 12

        self.special_power = 0

        tile_height = 50

        self.coin_tile = Panneau(str(self.gold), 0, 0, largeur=width, hauteur=tile_height, color=YELLOW, image=draw_coin, image_args=[self.coin_rad], image_coors=[25, 25], x_focus=self.coin_margin, y_focus=-20)

        self.special_power_tile = Panneau(str(self.special_power), 0, tile_height, largeur=width, hauteur=tile_height, color=RED, image=draw_double_fire, image_args=[self.coin_rad*2, [RED, YELLOW]], image_coors=[25, 35], x_focus=self.coin_margin, y_focus=-20)

        self.active_cible = 0

        self.cible_pos = None

        self.power = 0

        Player.update(self, [0, 0])

    def update(self, add):

        # coins
        self.gold += add[0]

        if self.gold:  # != 0

            len_digits = int(log(self.gold, 10))

            # formatting the graphic number
            if len_digits > 4:  # milions

                self.coin_tile.contenu = str(round((self.gold/100000), 1)) + "M"

            elif len_digits > 2:  # thousands

                self.coin_tile.contenu = str(round((self.gold/1000), 1)) + "k"

            else:

                self.coin_tile.contenu = str(self.gold)

        else:

            self.coin_tile.contenu = str(self.gold)

        # spe power
        self.special_power += add[1]

        if self.special_power:  # != 0

            len_digits = int(log(self.special_power, 10))

            # formatting the graphic number
            if len_digits > 4:  # milions

                self.special_power_tile.contenu = str(round((self.special_power/100000), 1)) + "M"

            elif len_digits > 2:  # thousands

                self.special_power_tile.contenu = str(round((self.special_power/1000), 1)) + "k"

            else:

                self.special_power_tile.contenu = str(self.special_power)

        else:

            self.special_power_tile.contenu = str(self.special_power)

    def draw(self):

        y_fire_decal = 40

        #coin tile
        self.coin_tile.draw()

        # special power tile

        self.special_power_tile.draw()

        if self.active_cible:

            if self.cible_pos == None:

                pos = pygame.mouse.get_pos()

                if pos[1] < 100:

                    return

            else:

                pos = self.cible_pos

            draw_cible(pos[0], pos[1], [0, 0], [[10, 30], RED])


def game_loop(inputs, level=[0]):

    # variables

    cols = inputs[0]

    points = 0

    graphic = 1

    # dicts

    defense_dict = {"gun":Gun,
                    "laser":Laser,
                    "mortar":Mortar,
                    "wall":Wall,
                    "gold mine":GoldMine,
                    "power mine":PowerMine,
                    "sniper tower":SniperTower,
                    "inferno tower":InfernoTower,
                    "freeze tower":FreezeTower,
                    }

    defense_cost_dict = {"mortar":300,
                         "wall":50,
                         "gun":150,
                         "laser":200,
                         "sniper tower":450,
                         "freeze tower":300,
                         "inferno tower":2000,
                         "gold mine":300,
                         "power mine":500,
                         }

    special_powers = {"Guided Missile":GuidedMissile,
                      "Freeze Spell":FreezeSpell,
                      "Bomb Shell":BombShell,
                      "Earth Quake":EarthQuake,
                      "Volcano":Volcano,}

    special_powers_prices = {"Guided Missile":1,
                             "Freeze Spell":1,
                             "Bomb Shell":3,
                             "Earth Quake":4,
                             "Volcano":10}

    # Instances

    pause_x_pos = 140  # screen_width//2-50

    panneau_pause = Panneau("", pause_x_pos, 0, 100, 100, color=GREY, image=draw_pause, image_coors=[43, 40])

    terrain = Terrain(cols, panneau_pause, defense_dict, defense_cost_dict)

    menu = 0  # when defined, contains the buying options of the player

    player = Player(pause_x_pos)  # mainly to store some game info, as cash..

    player_preparing = 0

    level_win = 0

    if level[0] == 1:

        go_button = Panneau("", pause_x_pos, 0, 100, 100, color=GREEN, image=draw_play, image_coors=[43, 40])

        # player will have time to prepare to fight against ennemy waves

        player_preparing = 1

        # gives bonus money

        player.update([-500, 0])

        player.update([level[1], 0])

        player.draw()

        # sends terrain (which deals with ennemy spawning) the entities to spawn and their coordinates)

        terrain.level_spawning = sorted(level[2], key=lambda x:x[0])

    # game loop

    play = True

    while play:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                play = False

            elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):

                if terrain.active_defense:

                    terrain.active_defense.active = False

                terrain.active_defense = 0

                mouse_pos = pygame.mouse.get_pos()

                if mouse_pos[1] >= terrain.up_margin:  # user click is in lower part of screen, user has clicked on a tile

                    if player.active_cible:

                        player.cible_pos = mouse_pos

                    else:  # will show some menu, given the tile clicked (defense in it or not)

                        if menu:  # if user clicked on board (not in menu buttons) when a menu is activated, the menu is taken out

                            menu = 0

                        else:  # might create a menu if user clicked on a tile

                            menu = terrain.deal_with_click(mouse_pos)

                if (player_preparing == 1) and go_button.clicked(pygame.mouse.get_pos()):

                    player_preparing = -1

                elif panneau_pause.clicked(mouse_pos):  # check if user has clicked on sth of importance in the upper part (pause button, menu..)

                    leave = set_pause()

                    if leave:

                        play = False

                elif menu:  # a menu is currently activated, which means that the player might have clicked on it

                    # click might activate a change in the function (change the page of menu) or return a user choice (of bought object..)
                    choice = menu.clicked(mouse_pos)

                    if choice:

                        # buy menu
                        if menu.type == 0:

                            defense_cost = defense_cost_dict[choice[0]]

                            n_defense = defense_dict[choice[0]](menu.grid_coors, terrain, defense_cost)

                            if defense_cost <= player.gold:  # has enough gold to buy

                                player.update([-defense_cost, 0])  # cost in gold and special power

                                terrain.append_entity(menu.grid_coors, n_defense)  # creates the new chosen defense

                                menu = 0  # menu has served it's purpose, now it's destroyed

                        # (sell/upgrade menu)
                        elif menu.type == 1:

                            tile = terrain.get_tile(menu.grid_coors)

                            if choice[0] == "sell":  # player wants to sell defense

                                gold = defense_cost_dict[tile.name]*2**(tile.niveau-1)//2

                                player.update([gold, 0])

                                terrain.set_tile(menu.grid_coors, 0)  #deletes defense from the board

                                menu = 0  # menu has served it's purpose, now it's destroyed

                            elif choice[0] == "upgrade":  # player wants to upgrade defense

                                upgrade_price = defense_cost_dict[tile.name]*2**tile.niveau

                                if upgrade_price <= player.gold:  # has enough gold to buy

                                    player.update([-upgrade_price, 0])

                                    tile.level_up()

                                    if tile.niveau < 9:

                                        upgrade_price = terrain.defense_cost_dict[tile.name]*2**tile.niveau

                                        sell_price = (terrain.defense_cost_dict[tile.name]*2**(tile.niveau-1))//2

                                        sell_menu = terrain.sell_menu

                                        prices = [upgrade_price, sell_price]

                                        menu = Menu(terrain, terrain.get_coor_of_pos(tile.center), sell_menu, 1, prices) 

                                    else:

                                        menu = 0  # menu has served it's purpose, now it's destroyed

                        # special powers menu
                        elif menu.type == 2:

                            power_cost = special_powers_prices[choice[0]]

                            if power_cost <= player.special_power:  # has enough gold to buy

                                if special_powers[choice[0]].need_target:  # players needs to specify a target before launching the bombs

                                    player.active_cible = 1

                                    player.power = special_powers[choice[0]](terrain)

                                    menu = Menu(terrain, None, ["activate", "cancel"], 3, [0, 0])  # menu has served it's purpose, now it's destroyed

                                else:

                                    power_cost = special_powers_prices[choice[0]]

                                    player.update([0, -power_cost])  # cost in (gold and) special power

                                    n_bullets = special_powers[choice[0]](terrain).activate((terrain.dead_ops/60))  # powers add new (often bombs) bullets to terrain ; (terrain.dead_ops/60) is somefactor by which damages are multiplied to be on similar levels as ennemy entities

                                    for bull in n_bullets:

                                        terrain.bullets.append(bull)

                                    menu = 0

                        # (Valider / Annuler) menu

                        elif menu.type == 3:

                            if choice[0][0] == "a":  # "a"ctivate power

                                if player.cible_pos != None:

                                    power_cost = special_powers_prices[player.power.name]

                                    player.update([0, -power_cost])  # cost in (gold and) special power

                                    n_bullets = player.power.activate(player.cible_pos, (terrain.dead_ops/60))  # powers add new (often bombs) bullets to terrain ; (terrain.dead_ops/60) is somefactor by which damages are multiplied to be on similar levels as ennemy entities

                                    for bull in n_bullets:

                                        terrain.bullets.append(bull)

                                    player.active_cible = 0

                                    player.cible_pos = None

                                    menu = 0

                                    player.power = 0

                                else:

                                    print("No target chosen yet")

                            elif choice[0][0] == "c":  # cancel

                                player.active_cible = 0

                                player.cible_pos = None

                                menu = Menu(terrain, None, list(special_powers.keys()), 2, [special_powers_prices[x] for x in list(special_powers.keys())], fire_menu=1)

                                player.power = 0

                if player.special_power_tile.clicked(mouse_pos):  # not elif, cause player that has a menu might wanna replace it, so prog checks upper block, then this one

                    menu = Menu(terrain, None, list(special_powers.keys()), 2, [special_powers_prices[x] for x in list(special_powers.keys())], fire_menu=1)

            elif (event.type == pygame.MOUSEMOTION):

                translation = event.rel

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_LEFT:

                    pass

        terrain_update = terrain.update(graphic, player_preparing)  # draws bg, terrain, buttons (pause button..), also updates entities, checks attacks..

        if terrain_update == "gameover":

            play = False

        elif terrain_update == "level_win":

            play = False

            level_win = 1

        elif terrain_update != [0, 0]:

            player.update(terrain_update)

        # checks that menu isn't one of a just destroyed entity
        if menu and (menu.type == 1) and (0 == terrain.get_tile(menu.grid_coors)):

            menu = 0

        # draws menu
        if menu:

            menu.draw()

            cur_circle_coor = terrain.last_mouse_coor

        else:

            cur_circle_coor = terrain.get_coor_of_pos(pygame.mouse.get_pos())

            terrain.last_mouse_coor = cur_circle_coor

        # draws the circle of grid where user mouse currently is

        try:

            center = terrain.gui_board[cur_circle_coor[0]][cur_circle_coor[1]]

            pygame.draw.circle(screen, WHITE, center[0], center[1], 3)

        except IndexError:

            pass
        ##

        player.draw()

        if player_preparing == 1:

            go_button.draw()

        pygame.display.update()

        clock.tick(60)

    if level_win == 1:

        print("gg")

        return "win"

    end_game(terrain.dead_ops)


def go_shop():

    print("No shop available yet")


def save_points(points):

    with open("turret_game_file.txt", "a") as file:

        file.write(">"+str(points)+"<\n")


def change_file(to_change_line, change=1):

    copie = []

    with open("turret_game_file.txt", "r") as file:

        for line in file:

            copie.append(line)

    with open("turret_game_file.txt", "w") as file:

        for x in range(len(copie)):

            if x == to_change_line:

                file.write((">{};{}<\n".format(x, change)))

            else:

                file.write(copie[x])


def chose_levels(inputs):

    open_level = -1

    with open("turret_game_file.txt", "r") as file:

        for line in file:

            if line[0] == ">":

                if line[-3] == "1":  # available level

                    open_level += 1

    levels = []

    with open("turret_level_data.txt", "r") as file:  # contains for each level the [times, types and positions] of to be spawned ennemies

        for line in file:

            if line[0] == "{":

                levels.append([1, int(line[1:-1]), []])

            elif (not(line[0] == "}")) and (not(line[0] == "\n")):

                levels[-1][2].append(list(map(int, line.split())))

    buttons = []

    button_width = 160

    button_height = 120

    x_places = screen_width//button_width

    c = 0

    for y in range(len(levels)//x_places):

        for x in range(x_places):

            if c <= open_level:

                buttons.append(Panneau("Lv {}".format(x+y*x_places+1), x*button_width, y*button_height, button_width-20, button_height-20, get_random_color()))

                c += 1

            else:

                buttons.append(Panneau("Locked", x*button_width, y*button_height, button_width-20, button_height-20, RED))

    choix = 0

    while choix == 0:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                choix = 1

                return

            elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):

                mouse_pos = pygame.mouse.get_pos()

                for x in range(len(buttons)):

                    if buttons[x].clicked(mouse_pos) and (not buttons[x].contenu == "Locked"):

                        win = game_loop(inputs, levels[x])

                        if win == "win":

                            change_file(x+1)

                        return

        screen.fill(BROWN)

        for button in buttons:

            button.draw()

        pygame.display.update()

        clock.tick(10)


def main(inputs):

    shop_button = Panneau("Shop $", 50, 350, 150, 100, YELLOW)

    play_button = Panneau("Infinite Mode !", 220, 350, 300, 100, BLUE)

    levels_button = Panneau("Levels !", 550, 350, 180, 100, GREEN)

    exit_button = Panneau("Exit.. ", 300, 475, 150, 100, RED)

    choix = 0

    while choix == 0:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                choix = 1

                return

            elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):

                mouse_pos = pygame.mouse.get_pos()

                if shop_button.clicked(mouse_pos):

                    go_shop()

                elif play_button.clicked(mouse_pos):

                    game_loop(inputs)

                elif exit_button.clicked(mouse_pos):

                    choix = 1

                    return  # goes back to main, then (should) save file then quits

                elif levels_button.clicked(mouse_pos):

                    chose_levels(inputs)

        screen.fill(BROWN)

        shop_button.draw()

        play_button.draw()

        exit_button.draw()

        levels_button.draw()

        aff_txt("Fire & Fury Corp.", 250, 100)

        aff_txt("Turret Game !", 225, 200, taille=50)

        pygame.display.update()

        clock.tick(10)


def check_file_stuff(level_nb):

    file = open("turret_game_file.txt", "a")

    file.close()

    with open("turret_game_file.txt", "r+") as file:

        if (file.readline() == ""):

            for x in range(level_nb):

                file.write(">{};{}<\n".format(x, int(x==0)))


if __name__ == "__main__":

    level_nb = 30

    check_file_stuff(level_nb)

    cols = 13

    inputs = [cols]

    main(inputs)
