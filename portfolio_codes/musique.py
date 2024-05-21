"""
Code that should allow a user to mix his own music
by setting his beats, beats frequencies...
"""

from pig_tv import *

import pickle

import os


class Menu:

    def __init__(self):

        # frmae of menu

        self.width = 400

        self.x = 400

        self.y = 0

        self.height = 700

        self.frame = pygame.Rect(self.x, self.y, self.width, self.height)

        # lifts

        self.x_margin = 80

        self.y_margin = 80

        labels = ["BPM", "full time", "pattern time", "start time", "pattern size", "pattern unit 1", "pattern unit 2", "pattern unit 3"]

        self.constant_lifts_nb = labels.index("pattern unit 1")

        self.default_pattern_unit = [1, 9, 2]

        bornes = [[30, 300], [1, 5, 1], [1, 7, 1], [1, 200, 1], [1, 10, 3], [1, 9, 3], [1, 9, 3], [1, 9, 5]]

        self.y_lift_space = 100

        self.lifts = []

        for l in range(len(labels)):

            if len(bornes[l]) > 2:

                self.lifts.append(Lift(self.x_margin+self.x, self.y_margin+l*self.y_lift_space, text=labels[l], min_borne=bornes[l][0], max_borne=bornes[l][1], float_vals=0, echelle=bornes[l][2]))

            else:

                self.lifts.append(Lift(self.x_margin+self.x, self.y_margin+l*self.y_lift_space, text=labels[l], min_borne=bornes[l][0], max_borne=bornes[l][1], float_vals=0))

        self.clicked_lift = -1

        self.y_lift = Lift(750, 50, 10, 600, vertical=1, min_borne=0, echelle=0, max_borne=20, afficher_echelle=0, float_vals=0)

        self.y_lift_clicked = 0

    def set_menu(self, rythm):

        echelles = [rythm[1], rythm[2], rythm[3], rythm[0], len(rythm[5])]

        self.y_lift.echelle = 20

        for x in range(self.constant_lifts_nb):  # resets the vaues of the constant lifts (that are here for each rythm)

            self.lifts[x].update_echelle(echelles[x])

        del self.lifts[self.constant_lifts_nb:]

        for x in range(echelles[self.constant_lifts_nb-1]):

            Menu.add_unit_lift(self, rythm[5][x])

    def get_y_needed_space(self):

        return self.y_margin+len(self.lifts)*self.y_lift_space

    def add_unit_lift(self, echelle=None):

        if echelle == None:

            echelle = self.default_pattern_unit[2]

        n_lift = Lift(self.x_margin+self.x, self.y_margin+len(self.lifts)*self.y_lift_space, min_borne=self.default_pattern_unit[0], max_borne=self.default_pattern_unit[1], echelle=echelle, float_vals=0, text="pattern unit {}".format(len(self.lifts)-3))

        self.lifts.append(n_lift)

        needed_space = Menu.get_y_needed_space(self)

        if needed_space > self.height:

            self.y_lift.update_bornes([self.y_lift.min_borne, needed_space-self.height])

    def del_unit_lift(self):

        del self.lifts[-1]

        self.y_lift.update_bornes([self.y_lift.min_borne, self.y_lift.max_borne-self.y_lift_space])

    def update(self, clicking, clicked, translation):

        to_return = None

        y_trans = self.y_lift.echelle  # current value of y lift is stored for it might get modified in main loop and would have a different result at the end of the function (would move "back up" without having moved down)

        # moves every lift according to where user's "y lift" is
        for lift in self.lifts:

            lift.update_pos([0, -y_trans])

        Menu.draw(self)

        mouse_pos = pygame.mouse.get_pos()

        if clicked:

            for i in range(len(self.lifts)):

                lift = self.lifts[i]

                if lift.clicked(mouse_pos):

                    self.clicked_lift = i

            if self.y_lift.clicked(mouse_pos):

                self.y_lift_clicked = 1

        if clicking:

            if self.clicked_lift != -1:

                last_echelle = self.lifts[self.clicked_lift].echelle

                self.lifts[self.clicked_lift].go(translation[0])

                if self.clicked_lift == self.constant_lifts_nb-1:  # the size lift has been moved

                    delta_size = self.lifts[self.clicked_lift].echelle-last_echelle

                    # updates the vertical lift

                    if delta_size > 0:

                        for x in range(delta_size):

                            Menu.add_unit_lift(self)

                    elif delta_size < 0:

                        for x in range(-delta_size):

                            Menu.del_unit_lift(self)

                # returns button that has been clicked

                to_return = [self.clicked_lift, self.lifts[self.clicked_lift].echelle]

            if self.y_lift_clicked:

                self.y_lift.go(translation[1])

        if not clicking:

            self.clicked_lift = -1

            self.y_lift_clicked = 0

        # moves lifts back up again
        for lift in self.lifts:

            lift.update_pos([0, y_trans])

        return to_return

    def draw(self):
        """ draws the menu, the bg, it's lifts """

        pygame.draw.rect(screen, WHITE, self.frame)

        for lift in self.lifts:

            lift.draw()

        self.y_lift.draw()


class JukeBox:

    fps = 10

    def __init__(self, buttons):

        self.clock = 0

        self.beat_frequency = .5*JukeBox.fps

        rythms_paths = ["samples/bam.wav", "samples/caisse.wav", "samples/caisse2.wav", "samples/snap.wav"]# ["samples/tac.wav", "samples/bam.wav", "samples/panev.wav", "samples/tong.wav"]#, "samples/caisse2.wav", "samples/snap.wav"]

        self.rythm_sounds = [pygame.mixer.Sound(path) for path in rythms_paths]

        self.rythmes = [0 for x in range(len(rythms_paths))]  # all rythms are deactivated when init

        self.last_time = time.time()

        # some basic beat (basic unit of time) data
        self.half_time = self.beat_frequency*.5

        self.full_time = self.beat_frequency*2

        # general settings

        self.active_index = -1

        self.menu = Menu()

    def update_active_button(self, clicking, clicked, translation):

        if self.active_index != -1:

            change = self.menu.update(clicking, clicked, translation)

            if change:

                # change to beat waiting times
                if change[0] == 0:

                    self.rythmes[self.active_index][1] = change[1]  # changes bpm

                    bps = (self.rythmes[self.active_index][1]/60)

                    max_radius = self.rythmes[self.active_index][-1][-2]

                    self.rythmes[self.active_index][-1][-1] = (2*max_radius*bps) / JukeBox.fps  # changes growth vect of circle

                    self.rythmes[self.active_index][-1][2] = 0

                elif change[0] == 1:

                    self.rythmes[self.active_index][2] = change[1]

                elif change[0] == 2:

                    self.rythmes[self.active_index][3] = change[1]

                elif change[0] == 3:

                    self.rythmes[self.active_index][0] = change[1]

                # change to a unit pattern
                elif change[0] > 4:

                    pattern_index = change[0]-5

                    self.rythmes[self.active_index][5][pattern_index] = change[1]

                # change to size of pattern
                else:

                    while len(self.rythmes[self.active_index][5]) > change[1]:

                        del self.rythmes[self.active_index][5][-1]

                    while len(self.rythmes[self.active_index][5]) < change[1]:

                        self.rythmes[self.active_index][5].append(2)

                    # reinitiating beat data of current pattern

                    self.rythmes[self.active_index][4] = 0

                    self.rythmes[self.active_index][6] = 0

    def activate_rythm(self, index, default=True):
        """ An activated rythm contains data about it: it's index is where to locate in sound file, it's an array of [next_activation, bpm, full_time, pattern_time, beat_compteur, till_wait, till_wait_index, circle] """

        if default:

            next_activation = 1

            bpm = JukeBox.fps*5

            full_time = 1

            pattern_time = 1

            beat_compteur = 0

            till_wait = [3, 3, 5]

            till_wait_index = 0

            bps = bpm/60

            max_radius = random.randint(100, 200)

            growth_vect = (2*max_radius*bps) / JukeBox.fps

            circle = [get_random_color(), [random.randint(0, 200), random.randint(0, 200)], 0, max_radius, growth_vect]

            self.rythmes[index] = [next_activation, bpm, full_time, pattern_time, beat_compteur, till_wait, till_wait_index, circle]

    def update(self, clicking, clicked, translation):

        # will update the setting menu of a sound if needed
        JukeBox.update_active_button(self, clicking, clicked, translation)

        # updates internal time
        self.clock += 1

        # checks every available sounds
        for index in range(len(self.rythmes)):

            if self.rythmes[index]:  # sound has been activated by user

                next_activation, bpm, full_time, pattern_time, beat_compteur, till_wait, till_wait_index, circle = self.rythmes[index]

                next_activation -= 1

                bps = bpm/60  # 60 secs in a min

                to_wait_frames = JukeBox.fps/bps

                # graphic stuff
                pygame.draw.circle(screen, circle[0], circle[1], int(circle[2]))

                circle = update_circle(circle)

                # checks if time to play sound
                if next_activation <= 0:

                    next_activation = to_wait_frames

                    self.rythm_sounds[index].play()

                    beat_compteur += 1

                    if beat_compteur == till_wait[till_wait_index]:

                        till_wait_index = (till_wait_index+1)%len(till_wait)

                        beat_compteur = 0

                        if till_wait_index == 0:  # complete pattern's been finished

                            next_activation = max(pattern_time, full_time)*to_wait_frames

                        else:

                            next_activation = full_time*to_wait_frames  # already added some

                # stores new updated data
                self.rythmes[index] = [next_activation, bpm, full_time, pattern_time, beat_compteur, till_wait, till_wait_index, circle]


def update_circle(circle):
    # updates size of circle[color, pos, radius, max_radius, growth_vect]

    color, pos, radius, max_radius, growth_vect = circle

    if (radius+growth_vect > max_radius) or (radius+growth_vect < 0):

        growth_vect *= -1

    radius += growth_vect

    return [color, pos, radius, max_radius, growth_vect]


def main():

    play = True

    clicking = 0

    buttons = []

    size = 100

    y_pos = 300

    for y in range(3):

        for x in range(4):

            buttons.append(Panneau(str(x+4*y), x*size, y_pos+y*size, size, size))

    box = JukeBox(buttons)

    # setting buttons

    button_width = 120

    load_button = Panneau("load", 0, 600, largeur=button_width, hauteur=100, color=BLUE)

    save_button = Panneau("save", button_width, 600, largeur=button_width, hauteur=100, color=GREEN)

    quit_button = Panneau("quit", button_width*2, 600, largeur=button_width, hauteur=100, color=RED)

    setting_buttons = [load_button, save_button, quit_button]

    # main loop
    while play:

        clicked = 0

        translation = [0, 0]

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                play = False

            if event.type == pygame.KEYDOWN:

                if event.key == 97:

                    play = False

                elif event.key == pygame.K_SPACE:

                    pass

            elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):

                clicked = 1

                mouse_pos = pygame.mouse.get_pos()

                clicking = 1

                # dealing with the pad

                for i in range(len(buttons)):

                    b = buttons[i]

                    if b.clicked(mouse_pos):

                        # clicked button was previously selected (blue)
                        if (box.active_index == i):  # becomes white again

                            box.active_index = -1

                            b.color = WHITE

                            box.rythmes[i] = 0

                        else:  # the button was not selected before

                            if box.active_index != -1:  # if there was a previously selected button, it's unselected

                                buttons[box.active_index].color = RED

                            box.active_index = i

                            b.color = BLUE  # becomes blue (selected)

                            if box.rythmes[i] == 0:  # sounds get's activated if it wasn't before

                                box.activate_rythm(i)

                            box.menu.set_menu(box.rythmes[i])

                # checking the setting buttons

                for x in range(len(setting_buttons)):

                    button = setting_buttons[x]

                    if button.clicked(mouse_pos):

                        if button.contenu == "quit":

                            play = False

                        elif button.contenu == "load":

                            n_music = load_music()

                            if not n_music == -1:

                                blue_asssigned = False

                                box.rythmes = n_music

                                for i in range(len(box.rythmes)):

                                    rythm = box.rythmes[i]

                                    if type(rythm) == list:

                                        box.menu.set_menu(rythm)

                                        if not blue_asssigned:

                                            blue_asssigned = True

                                            buttons[i].color = BLUE

                                            box.active_index = i

                                        else:

                                            buttons[i].color = RED

                                    else:

                                        buttons[i].color = WHITE

                        elif button.contenu == "save":

                            save_music(box.rythmes)

            elif (event.type == pygame.MOUSEBUTTONUP) and (event.button == 1):

                clicking = 0

            elif (event.type == pygame.MOUSEMOTION):

                translation = event.rel

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_LEFT:

                    pass

        screen.fill(BLACK)

        for b in buttons:

            b.draw()

        for sb in setting_buttons:

            sb.draw()

        box.update(clicking, clicked, translation)

        pygame.display.update()

        test = 1
        
        if test and not random.randint(0, 50):

            print(clock.get_fps())

        clock.tick(10)

        #JukeBox.fps = clock.get_fps()


def load_music():
    """ loads music from folder musics """

    available_musics = []

    for x in os.listdir("musics"):

        available_musics.append(x)

    if available_musics == []:  # no saved music

        print("No saved music")

        return -1

    invite = "\nLoading saved music :\n"

    for x in range(len(available_musics)):

        invite += str(x+1)+" : "+available_musics[x]+"\n"

    invite += "q : quitter\n"

    choice = input(invite)

    if choice == "q":

        return -1

    try:

        choice = int(choice)

    except ValueError:

        return load_music()

    if 1 <= choice <= len(available_musics):

        return pickle.load(open("musics/"+available_musics[choice-1], "rb"))

    else:

        return load_music()


def save_music(rythmes):
    """ saves the current music into saved_music.txt """

    file_name = input("\nSaving music\nFile name : ")

    with open("musics/"+str(file_name)+".txt", "wb") as file:

        pickle.dump(rythmes, file)


def set_music_dir():

    path = "musics"

    if not os.path.exists('./'+path):

        os.mkdir(path)

    
if __name__ == "__main__":

    pygame.init()

    pygame.mixer.init()

    pygame.mixer.music.set_volume(1)

    set_music_dir()

    main()
