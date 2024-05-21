"""
Romain DAVID
26/05/2019
The purpose of this project
is to gather all the codes that
I've done to this day.
"""

import os

from pig_tv import *

from portfolio_codes.calculette import main as calculette_demo  # portfolio_codes/

from portfolio_codes.horloge_gui import main as horloge_demo

from portfolio_codes.anim_noel5 import main as anim_noel_demo

from portfolio_codes.mums_day import main as mum_day_demo

from portfolio_codes.dads_day import main as dads_day_demo

from portfolio_codes.electrons import main as electrons_demo

from portfolio_codes.cardioid import main as cardioid_demo

from portfolio_codes.sand_piles import main as sand_piles_demo

from portfolio_codes.casse_brique import  main as casse_brique_demo

from portfolio_codes.chaos_or_random import  main as chaos_or_random_demo

from portfolio_codes.black_hole import main as black_hole_demo

from portfolio_codes.relief import main as relief_demo

from portfolio_codes.bille_dash_2 import main as bille_dash_2_demo

from portfolio_codes.paint import main as paint_demo

from portfolio_codes.dictionnary_pasting import main as dictionnary_pasting_demo

from portfolio_codes.geometry_animations import main as geometry_animations_demo

from portfolio_codes.snake_rebuild import main as snake_rebuild_demo

from portfolio_codes.geometrie_en_dimension import main as geometrie_en_dimension_demo

from portfolio_codes.rosace import main as rosace_demo

from portfolio_codes.capture_the_ball import main as capture_the_ball_demo

from portfolio_codes.balles_rebondissantes import main as balles_rebondissantes_demo

from portfolio_codes.collisions import main as collisions_demo

from portfolio_codes.fight import main as fight_demo

from portfolio_codes.screen_filter import main as screen_filter_demo

from portfolio_codes.image_dithering import main as image_dithering_demo

from portfolio_codes.flappy_bird2 import main as flappy_bird2_demo

from portfolio_codes.maze import main as maze_demo

from portfolio_codes.maze3 import main as maze2_demo

from portfolio_codes.rays import main as rays_demo

from portfolio_codes.four_in_a_row import main as four_in_a_row_demo

from portfolio_codes.dots_to_dot_progressif import main as dots_to_dot_progressif_demo

from portfolio_codes.meteo import main as meteo_demo

from portfolio_codes.mandelbrot_set import main as mandelbrot_set_demo

from portfolio_codes.bird_training import main as bird_training_demo

from portfolio_codes.turret_game import main as turret_game_demo

from portfolio_codes.paint2 import main as paint2_demo

from portfolio_codes.screen_filters2 import main as screen_filters2_demo

from portfolio_codes.function_graphing import main as function_graphing_demo

from portfolio_codes.create_puzzle import main2 as create_puzzle_demo



def get_pictures(path):

    pass


def run_demo(nb):

    demo = Demo(code_args[nb])

    wants_to_run = demo.user_chose()

    if wants_to_run == -1:

        return

    if wants_to_run:

        demo.run()


class Demo:

    def __init__(self, code_info):  # int_vals, bool_buttons):

        self.int_vals = code_info[0]  # made up of all tweakable interger value, presented as an array[default_val, min_val, max_val]

        self.bool_buttons = code_info[1]

        self.radio_buttons = code_info[2]

        self.code_input = []

        self.to_exec = code_info[-1]

        self.user_input = []

    def user_chose(self):

        if (self.int_vals != []) or (self.int_vals != []) or (self.int_vals != []):

            # commandes

            play = True

            clicking = 0

            start_move = 0

            # buttons

            width = 150

            height = 100

            play_button = Panneau("Play !", screen_width-width, screen_height-height, width, height)

            # tweakable values

            # Lifts

            margin = 100

            between_lift_y_space = margin*1.5

            if len(self.int_vals) > 2:

                between_lift_y_space = margin

            lifts = []

            y_add_right_lift = 0

            farthest_x = margin

            for index in range(len(self.int_vals)):

                if (index % 2) == 0:

                    x_pos = farthest_x

                y_index = index%2

                width = 200

                lifts.append(Lift(x_pos, margin+y_index*between_lift_y_space, width=width, min_borne=self.int_vals[index][1], max_borne=self.int_vals[index][2], echelle=self.int_vals[index][0], text=self.int_vals[index][-1], float_vals=self.int_vals[index][3]))

                this_far_x = x_pos + max(width, len(self.int_vals[index][-1])*18) + 100

                if this_far_x > farthest_x:

                    farthest_x = this_far_x
                
            if len(self.int_vals) == 0:

                lifts_space = 0

            elif len(self.int_vals) == 1:

                lifts_space = between_lift_y_space

            else:

                lifts_space = 2*between_lift_y_space

            # Bool buttons (checked or not)

            x_margin = 100

            y_bool_margin = margin + lifts_space

            between_button_y_space = margin

            bool_buttons = []

            width = 30

            letter_width = 19

            for index in range(len(self.bool_buttons)):

                bool_buttons.append(BoolButton(x_margin, y_bool_margin, self.bool_buttons[index][1], self.bool_buttons[index][0], width=width))

                x_margin += width*2 + letter_width*(len(self.bool_buttons[index][1])+5)

            # Radio buttons (one True, all other False)

##            if (lifts != []) and (bool_buttons != []):
##
##                if len(lifts) > 2:
##
##                    if len(lifts) > 4:
##
##                        lowest_index = -1
##
##                    else:
##
##                        lowest_index = 1
##                else:
##
##                    lowest_index = -1
##
##                lowest_y_object = max(lifts[lowest_index].y+lifts[-1].height, bool_buttons[-1].y+bool_buttons[-1].height) + 40
##
##            elif (lifts == []) and (bool_buttons == []):
##
##                lowest_y_object = 10
##
##            elif (lifts == []):
##
##                lowest_y_object =  bool_buttons[-1].y+bool_buttons[-1].height + 40
##
##            elif (bool_buttons == []):
##
##                if len(lifts) > 2:
##
##                    if len(lifts) > 4:
##
##                        lowest_index = -1
##
##                    else:
##
##                        lowest_index = 1
##                else:
##
##                    lowest_index = -1
##
##                lowest_y_object =  lifts[lowest_index].y+lifts[-1].height + 40

            radio_buttons_y = y_bool_margin + 30*2

            radio_buttons = []

            for index in range(len(self.radio_buttons)):

                radio_buttons_x = 40

                radio_buttons.append(RadioButtons(radio_buttons_x, radio_buttons_y, self.radio_buttons[index][0], self.radio_buttons[index][1]))

                radio_buttons_y += (radio_buttons[-1].biggest_text_frame)*2 + 30

                farthest_x = max(farthest_x, radio_buttons[-1].total_width+radio_buttons_x)

                radio_buttons_x += radio_buttons[-1].total_width

            more_than_screen_width = farthest_x-screen_width

            if more_than_screen_width > 0:

                max_derouleur_borne = more_than_screen_width

            else:

                max_derouleur_borne = 1

            derouleur = Lift(margin, screen_height-margin, width=screen_height-2*margin, min_borne=0, max_borne=max_derouleur_borne, echelle=0, float_vals=0, afficher_echelle=0)

            derouleur_clicked = 1

            # GUI loop
            while play:

                mouse_pos = list(pygame.mouse.get_pos())

                mouse_pos[0] += derouleur.echelle  # to fit with the derouleur

                #print(derouleur.echelle)

                for event in pygame.event.get():

                    if event.type == pygame.QUIT:

                        play = False

                        return -1 # goes back to main menu

                    elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):

                        clicking = 1

                        if play_button.clicked([mouse_pos[0]-derouleur.echelle, mouse_pos[1]]):

                            play = False

                        for bool_button in bool_buttons:

                            if bool_button.clicked(mouse_pos):

                                bool_button.bool_value = (bool_button.bool_value+1)%2

                        for lift in lifts:

                            if lift.clicked(mouse_pos):

                                start_move = lifts.index(lift)+1

                        if derouleur.clicked([mouse_pos[0]-derouleur.echelle, mouse_pos[1]]):

                            derouleur_clicked = 1

                    elif (event.type == pygame.MOUSEBUTTONUP) and (event.button == 1):

                        clicking = 0

                        start_move = 0

                        derouleur_clicked = 0

                    elif (event.type == pygame.MOUSEMOTION):

                        translation = event.rel

                        # move the setting lifts around (if need be)
                        if start_move:

                            lifts[start_move-1].go(translation[0])

                        # move the page x location around (if need be)
                        elif derouleur_clicked:

                            derouleur.go(translation[0])

                screen.fill(BLACK)

                # allows to display a bigger surface than the screen, in which the user can move around
                entities = [lifts, bool_buttons, radio_buttons]

                for z in entities:

                    for ent in z:

                        ent.update_pos([-derouleur.echelle, 0])

                mouse_pos[0] -= derouleur.echelle

                # draws all the buttons
                for lift in lifts:

                    lift.draw()

                for bool_button in bool_buttons:

                    bool_button.draw()

                for radio_button in radio_buttons:

                    radio_button.update(mouse_pos, clicking)

                    radio_button.draw()

                play_button.draw()

                derouleur.draw()

                #pygame.draw.rect(screen, RED, pygame.Rect(play_button.x, play_button.y, play_button.largeur, play_button.hauteur))

                pygame.display.update()

                # puts the entities to their original place again

                for z in entities:

                    for ent in z:

                        ent.update_pos([derouleur.echelle, 0])

                clock.tick(60)

##                if not random.randint(0, 60):
##
##                    print(clock.get_fps())

            self.user_input = []

            self.user_input += [x.echelle for x in lifts]
            self.user_input += [x.bool_value for x in bool_buttons]
            self.user_input += [x.bool_value for x in radio_buttons]

            for x in range(len(self.user_input)):

                if self.user_input[x] == []:

                    del self.user_input[x]

            return 1


        else:

            screen.fill(BLACK)

            self.to_exec()

    def run(self):
        """ runs demo program with user chosen inputs """

        print(self.user_input)

        screen.fill(BLACK)

        self.to_exec(self.user_input)


class Tab:

    def __init__(self, rows, cols, total_pages, project_nb):

        self.page_number = total_pages

        self.project_nb = project_nb

        self.page = 0

        self.rows = rows

        self.cols = cols

        self.x_margin = screen_width//8

        self.y_margin = screen_height//8

        self.pyg_rect = pygame.Rect(self.x_margin, self.y_margin, screen_width-2*self.x_margin, screen_height-2*self.y_margin)

        self.in_x_margin = screen_width//20

        self.in_y_margin = screen_height//20

        self.frame_width = (screen_width-2*self.x_margin-(self.cols+1)*self.in_x_margin)/self.cols

        self.frame_height = (screen_height-2*self.y_margin-(self.rows+1)*self.in_y_margin)/self.rows

        self.frames = [[[Panneau("", self.pyg_rect[0]+(x+1)*self.in_x_margin+x*self.frame_width,
                                    self.pyg_rect[1]+(y+1)*self.in_y_margin+y*self.frame_height,
                                    self.frame_width,
                                    self.frame_height)

                        for x in range(self.cols)] for y in range(self.rows)]

                       for p in range(self.page_number)]

        # takes off the useless frames

        to_del_nb = ((self.rows*self.cols)*total_pages)-project_nb

        for x in range(to_del_nb//self.cols):

            self.frames[-1].pop()

        for x in range(to_del_nb%self.cols):

            self.frames[-1][-1].pop()

        ##
            
        self.color = WHITE

        self.frame_color = BLACK

        self.target_tile = 0

        taille = 60

        self.tile_page_number = Panneau("1", screen_width//2-taille/2, screen_height-taille, taille, taille, y_focus=-15)

        shrink = 10

        # loads all pictures (or string name of file) in an array

        self.small_pictures = []

        self.big_pictures = []

        for p in range(len(self.frames)):

            self.small_pictures.append([])

            self.big_pictures.append([])

            for y in range(len(self.frames[p])):

                self.small_pictures[-1].append([])

                self.big_pictures[-1].append([])

                for x in range(len(self.frames[p][y])):

                    picture = load_picture(picture_paths[x+self.cols*y+p*(self.rows*self.cols)], self.frame_width-shrink, self.frame_height-shrink)

                    if picture != -1:

                        self.small_pictures[-1][-1].append(load_picture(picture_paths[x+self.cols*y+p*(self.rows*self.cols)], self.frame_width-shrink, self.frame_height-shrink))

                        self.big_pictures[-1][-1].append(load_picture(picture_paths[x+self.cols*y+p*(self.rows*self.cols)], self.frame_width+shrink*2, self.frame_height+shrink))

                    else:

                        self.small_pictures[-1][-1].append(picture_paths[x+self.cols*y+p*(self.rows*self.cols)])

                        self.big_pictures[-1][-1].append(picture_paths[x+self.cols*y+p*(self.rows*self.cols)])

    def move_page(self, value):

        if val_in_array(self.page+value, [0, self.page_number-1]):

            self.page += value

            self.tile_page_number.contenu = str(self.page+1)

    def update(self, clicking):

        did_demo = 0

        actual_frames = self.frames[self.page]

        mouse = pygame.mouse.get_pos()

        if clicking:

            for y in range(len(actual_frames)):

                for x in range(len(actual_frames[y])):

                    if actual_frames[y][x].clicked(mouse):

                        run_demo(self.page*(self.rows*self.cols)+y*self.rows+x)

                        did_demo = 1

        self.target_tile = 0

        # checks if user's mouse is on a frame -> activates a demo

        for y in range(len(actual_frames)):

            for x in range(len(actual_frames[y])):

                if actual_frames[y][x].clicked(mouse):

                    self.target_tile = [y, x]

        # makes the selected frame bigger

        if self.target_tile:

            actual_frames[self.target_tile[0]][self.target_tile[1]].reset_size(self.in_x_margin/2, self.in_y_margin/2)

        Tab.draw(self)

        # sets default for next frame, will be re-reset if needed

        if self.target_tile:

            actual_frames[self.target_tile[0]][self.target_tile[1]].reset_size(-self.in_x_margin/2, -self.in_y_margin/2)

        # if did a demo, need to reset the mouse

        return did_demo

    def draw(self):

        actual_frames = self.frames[self.page]

        screen.fill(BLACK)

        pygame.draw.rect(screen, self.color, self.pyg_rect)

        for y in range(len(actual_frames)):

            for x in range(len(actual_frames[y])):

                actual_frames[y][x].draw()  # pygame.draw.rect(screen, self.frame_color, self.frames[y][x])

                if actual_frames[y][x].largeur == self.frame_width:

                    if type(self.small_pictures[self.page][y][x]) == str:  # picture not found while loading pictures

                        aff_txt(self.small_pictures[self.page][y][x], actual_frames[y][x].x+5, actual_frames[y][x].y+5)

                    else:

                        screen.blit(self.small_pictures[self.page][y][x], [actual_frames[y][x].x+5, actual_frames[y][x].y+5])

                else:

                    if type(self.big_pictures[self.page][y][x]) == str:  # picture not found while loading pictures

                        aff_txt(self.big_pictures[self.page][y][x], actual_frames[y][x].x+10, actual_frames[y][x].y+10)

                    else:

                        screen.blit(self.big_pictures[self.page][y][x], [actual_frames[y][x].x+10, actual_frames[y][x].y+10])

        self.tile_page_number.draw()


def main():

    # vars

    play = True

    clicking = 0

    page_nb = ceil((project_nb)/(rows*cols))

    # Instances

    tab = Tab(rows, cols, page_nb, project_nb)

    # buttons

    play_button_height = 70

    quit_button = Panneau("Quitter", 0, screen_height-play_button_height, 200, play_button_height, y_focus=-15)

    # arrow buttons (to switch page)

    arrow_buttons = []

    arrow_button_width = 100

    arrow_button_height = 100

    arrow_buttons.append(Panneau("", 0, screen_height/2-arrow_button_height/2, arrow_button_width, arrow_button_height, image=draw_play, image_coors=[arrow_button_width/2, arrow_button_height/2], image_args=[WHITE, -1]))

    arrow_buttons.append(Panneau("", screen_width-arrow_button_width, screen_height/2-arrow_button_height/2, arrow_button_width, arrow_button_height, image=draw_play, image_coors=[arrow_button_width/2, arrow_button_height/2], image_args=[WHITE, 1]))

    # GUI Loop
    while play:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                play = False

            elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):

                mouse_pos = pygame.mouse.get_pos()

                clicking = 1

                if quit_button.clicked(mouse_pos):

                    play = False

                for button in arrow_buttons:

                    if button.clicked(mouse_pos):

                        direction = arrow_buttons.index(button) or -1

                        tab.move_page(direction)

            elif (event.type == pygame.MOUSEBUTTONUP) and (event.button == 1):

                clicking = 0

            elif (event.type == pygame.MOUSEMOTION):

                translation = event.rel

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_LEFT:

                    tab.move_page(-1)

                if event.key == pygame.K_RIGHT:

                    tab.move_page(1)

        if tab.update(clicking):

            clicking = 0

        quit_button.draw()

        for button in arrow_buttons:

            button.draw()

        pygame.display.update()

        clock.tick(60)


def test(user_input):

    print("test", user_input)

if __name__ == "__main__":

    cols = 3
    rows = 3
    
    os.chdir("C:/Users/Romai/Downloads/python_portfolio")

    pygame.display.set_caption("Port Folio")

    # code argument is an array of all required information to run the codes : each code has an array composed of [lifts, radio_buttons, .., code_to_execute_name]
    # lifts, radio_buttons, ..., are arrays composed each of information to create GUI objects
    # lift[default number, min number, max number, int(=0) or float accepted, and name of item

    code_args = [
                #[[[3, 0, 10, "Speed"], [0, 0, 100, "Power"], [15, 14, 15, "Health Points"]], [[0, "Jump"], [1, "Hard Mode"], [0, "Hapiness"]], [], test],
                #[[[3, 3, 10, 1, "thickness"], [60, 1, 1000, 0, "fps"]], [[0, "effect"]], [[["test1", "test2"], 0]], test_demo],
                [[], [], [], calculette_demo],
                [[], [], [], horloge_demo],
                [[], [], [], anim_noel_demo],
                [[], [], [], mum_day_demo],
                [[], [], [], dads_day_demo],
                [[[40, 1, 150, 0, "Entity number"]], [[0, "see cloud"]], [], electrons_demo],
                [[[500, 1, 1000, 0, "Nombre de rais"], [325, 1, 1000, 0, "Table de multiplication"], [1, 0, 5, 0, "Nombre de rais : incrementation"], [1, 0, 5, 1, "Tables : incrementation"], [4, 1, 100, 0, "FPS"]], [], [], cardioid_demo],
                [[[2, 0, 6, 0, "all sand piles"], [100, 0, 1000, 0, "center sand pile"], [20, 0, 1000, 0, "Other main SP"], [0, 0, 4, 0, "Formation"]], [], [], sand_piles_demo],
                [[], [], [], casse_brique_demo],
                [[[3, 3, 10, 0, "Vertices nb"], [1000, 1, 100000, 0, "steps per frame"]], [[0, "glass effect"]], [[["No\nres-\ntric-\ntions", "no\nsame", "not\nleft", "no\nneighbor", "no\n+2", "no\nneighbor\nif prev=2prev"], 0]], chaos_or_random_demo],
                [[[1000, 1, 10000, 0, "steps per frame"], [0.1, 0, 10, 1, "black hole speed"]], [], [], black_hole_demo],
                [[[100, 1, screen_height, 0, "rows"], [100, 1, screen_width, 0, "columns"], [127, 0, 255, 0, "basic fill"], [10, 1, 200, 0, "growing rate"]], [[0, "draw lines"]], [], relief_demo],
                [[[.7, .1, 3, 2, "gravity"], [12, 8, 20, 1, "jump"]], [], [], bille_dash_2_demo],
                [[[3, 1, 20, 0, "thickness"], [4, 1, 15, 0, "color variation speed"]], [], [[["symetrie 2", "symetrie 4"], 0]], paint_demo],
                [[[3, 1, 40, 0, "size"]], [[0, "bounce on edges"], [0, "rgb colors"]], [[["1", "2", "3", "4", "5", "6", "7", "8"], 0]], dictionnary_pasting_demo],
                [[[60, 1, 1000, 0, "fps"]], [], [[["ortho lines", "circles", "squares", "stars", "black hole"], 1], [["random color", "degrade", "bw"], 0]], geometry_animations_demo],
                [[[80, 10, 800, 0, "rows"], [60, 1, 300, 0, "fps"], [10, 1, 100, 0, "food size"]], [], [], snake_rebuild_demo],
                [[[10, 1, 20, 0, "line thickness"]], [], [[["ligne", "triangle", "etoile"], 0]], geometrie_en_dimension_demo],
                [[[30, 5, 100, 0, "radius"], [6, 1, 20, 0, "number of created circles"], [1, 0, 20, 0, "thickness"]], [], [[["one circle", "five circles", "user choice"], 0]], rosace_demo],
                [[[60, 1, 150, 0, "FPS"], [10, 1, 50, 0, "speed"]], [], [], capture_the_ball_demo],
                [[[10, 1, 100, 0, "mouse radius"], [0.3, 0, 1, 2, "gravity constant"]], [], [], balles_rebondissantes_demo],
                [[], [], [], collisions_demo],
                [[], [], [], fight_demo],
                [[[0, 0, 10, 0, "filter size"], [200, 5, 1000, 0, "image width"], [200, 5, 1000, 0, "image height"], [1, 0.1, 5, 1, "surexposition"]], [[0, "black and white"]], [[["normal\nblur", "strong\nblur", "x lines\nsharp", "y lines\nsharp", "xy lines\nsharp"], 0]], screen_filter_demo],
                [[], [], [], image_dithering_demo],
                [[[20, 5, 50, 0, "radius"], [10, 5, 25, 0, "jump_height"], [180, 100, 300, 0, "pillar space"], [5, 1, 20, 0, "pillar speed"], [80, 40, 160, 0, "pillar spawn (frames)"]], [], [[["random\ncolor", "rouge", "jaune", "vert", "bleu"], 0]], flappy_bird2_demo],
                [[[40, 3, 700, 0, "rows"]], [[1, "show building steps"]], [], maze_demo],
                [[[8, 3, 80, 0, "rows"], [8, 3, 80, 0, "cols"]], [[1, "traditional style"]], [], maze2_demo],
                [[[50, 5, 1000, 0, "ray number"], [1, 1, 4, 0, "size of 3D (2 -> half ..)"], [1, 0.5, 2*pi, 2, "view angle"], [4, 3, 10, 0, "maze size"]], [], [], rays_demo],
                [[], [], [], four_in_a_row_demo],
                [[[300, 1, 10000, 0, "pop_size"], [0, 0, 100, 0, "generation_cachees"], [80, 1, 400, 0, "dna_start_size"], [300, 50, 2000, 0, "max_dna_len"], [4, 0, 50, 0, "dna_add"]], [], [[["terrain 0", "terrain 1", "terrain 2", "terrain 3", "terrain 4", "terrain 5"], 0]], dots_to_dot_progressif_demo],
                [[[1, 0.1, 4, 1, "sun speed"]], [], [], meteo_demo],
                [[], [], [], mandelbrot_set_demo],
                [[[100, 1, 10000, 0, "population length"], [8, 3, 20, 0, "mutation rate"], [2, 0, 8, 0, "layer number"], [4, 1, 10, 0, "layer size"]], [], [], bird_training_demo],
                [[[13, 1, 30, 0, "columns"]], [], [], turret_game_demo],
                [[], [], [], paint2_demo],
                [[[50, 3, 500, 0, "color aray size (for \"set screen colors to nearest color constant\" only"], [3, 1, 100, 0, "blur size (for blurs only)"]], [[0, "set to black and white"], [1, "show progressive update"]], [[["random add filter", "black and white screen to nearest color", "one color tweaking", "screen colors tweaking", "invert screen colors", "set screen colors to nearest color constant", "set fast blur"], 1]], screen_filters2_demo],
                [[], [], [], function_graphing_demo],
                [[[50, 5, 200, 0, "tile width"]], [], [], create_puzzle_demo]
                ]

    project_nb = len(code_args)

    picture_paths = ["calculette.png", "horloge.png", "anim_noel.png", "mum_s_day.png", "dads_day.png", "electrons.png", "cardioid.png", "sand_piles.png", "casse_brique.png", "chaos_or_random.png", "black_hole.png", "relief.png", "bille_dash.png", "paint.png", "dictionnary_pasting.png", "geometry_animations.png", "snake_rebuild.png", "geometrie_en_dimension.png", "rosace.png", "capture_the_ball.png", "balles_rebondissantes.png", "collisions.png", "fight.png", "screen_filter.png", "image_dithering.png", "flappy_bird2.png", "maze.png", "maze2.png", "rays.png", "four_in_a_row.png", "dots_to_dot_progressif.png", "meteo.png", "mandelbrot_set.png", "bird_training.png", "turret_game.png", "paint2.png", "screen_filters2.png", "function_graphing.png", "puzzle.png"]

    main()
