from pig_tv import *


import string


#  Instances


class Tile:
    """ brique de construction de base d'un user code """

    basic_height = 80

    indentation = 40

    letter_size = 18

    def __init__(self, x, y, content="_", color=[255 for _ in range(3)]):
        """ the code is made up of basic tiles """

        self.x = x

        self.y = y

        self.width = 100

        self.height = Tile.basic_height

        self.box = Panneau(content, self.x, self.y, self.width, self.height, color=color)

        self.content = ""

    def append(self):

        pass

    def draw(self):

        self.box.draw()

    def clicked(self, mouse_pos):

        return self.box.clicked(mouse_pos)

    def update_pos(self, x, y):

        self.box.update_pos([x, y])

    def modify_color(self, n_color):

        self.box.color = n_color



class BlankTile(Tile):
    """ A blank tile is placed between each tile and at the begining of each line, to allow user to add tiles (instead of blanks) """

    def __init__(self, x, y):

        Tile.__init__(self, x, y, "")

        self.width = 10


class UserInputBox(Tile):

    def __init__(self, x, y):

        Tile.__init__(self, x, y, "")


class StringVarUserInput(UserInputBox):

    def __init__(self, x, y):

        Tile.__init__(self, x, y, "")

        self.content = ""

    def add_string(self, string):

        self.box.contenu += string


class IntegerVarUserInput(UserInputBox):

    def __init__(self, x, y):

        Tile.__init__(self, x, y, "")

        self.content = ""

    def add_string(self, int_string):

        if int_string in string.printable[:10]:  # string's a number

            self.box.contenu += int(string)


class CodeBox:

    def __init__(self, rect):

        self.pyg_rect = rect

        self.tile_margin = 5

        self.user_code = [[BlankTile(rect[0]+self.tile_margin, rect[1]+self.tile_margin)]]

        self.cursor = [0, 0]  # coors of user cursor

    def draw(self):

        pygame.draw.rect(screen, WHITE, self.pyg_rect)

        pygame.draw.rect(screen, BLUE, self.pyg_rect, 3)

        for y in range(len(self.user_code)):

            for x in range(len(self.user_code[y])):

                self.user_code[y][x].draw()

    def run(self):

        print("Running user code")

    def add_line(self):

        self.user_code.append([])

        self.user_code[-1].append(BlankTile())

    def add_tile(self, coor, n_tile):

        self.user_code[coor[0]][coor[1]] = n_tile

        self.user_code[coor[0]].insert(BlankTile(), coor[1]+1)

    def delete_tile(self, coor):

        for x in range(2):  # deletes tile and blank tile

            del self.user_code[coor[0]][coor[1]]


class Menu:

    def __init__(self, menu_rect, options):
        """ Menu shop, that enables player to buy defenses """

        # graphic settings

        self.box_margin = 5  # 0

        self.pyg_rect = menu_rect

        self.menu_frame = Panneau("", self.pyg_rect[0], self.pyg_rect[1], self.pyg_rect[2], self.pyg_rect[3])

        self.box_width = self.pyg_rect[2]-2*self.box_margin

        self.box_height = 80  # self.menu_frame.hauteur - 2*self.box_margin

        self.y_up_margin = 50

        self.available_box_nb = (self.pyg_rect[3]-self.box_margin-self.y_up_margin)//(self.box_height+self.box_margin)

        self.arrow_size = 8

        self.box_x = self.menu_frame.x+self.box_margin

        # dealing with the organisation of which button/option is displayed
        self.page = 0  # current page (part of all options currently displayed on screen)

        self.dict_index = 0  # there are several dicts of options

        self.option_index = 0  # page in the chosen dict

        self.page_nb = ceil(len(self.options)/(self.available_box_nb-2))  # total page nb

        self.curr_boxes = []

        self.option_dicts = [x[0] for x in options]

        self.dicts_colors = [x[1] for x in options]

        self.color = self.dicts_colors[0]

        Menu.define_curr_boxes(self)

    def define_curr_boxes(self):
        """ defining current buttons of menu (all can't be displayed because of place available on screen)"""

        self.curr_boxes = []

        available_options = len(list(self.option_dicts[self.option_index].keys())[self.option_index:])

        loop_nb = min(self.available_box_nb-1, len(available_options))  # if there is more available boxes than the number of boxes to display (+2 arrow buttons)

        compteur = first_index

        # defining the button ; differences between arrow buttons and buying buttons

        for c in range(1, loop_nb+1):  # index is one further because of first arrow button

            box_y = self.menu_frame.y+self.box_margin+c*(self.box_margin+self.box_height)+self.y_up_margin

            image_coors = [25, 37]

            box = Panneau([self.options[compteur]], self.box_x, box_y, self.box_width, self.box_height, x_focus=0, y_focus=0)

            self.curr_boxes.append(box)

            compteur += 1

        first_box = Panneau("", self.menu_frame.x+self.box_margin, self.menu_frame.y+self.y_up_margin, self.box_width//2, self.box_height, image=draw_fleche_formatted, image_coors=[70, 25], image_args=[self.arrow_size, GREY, 1])

        last_box = Panneau("", self.menu_frame.x+self.box_margin+self.box_width//2, self.menu_frame.y+self.y_up_margin, self.box_width//2, self.box_height, image=draw_fleche_formatted, image_coors=[25, 35], image_args=[self.arrow_size*-1, GREY, 1])

        self.curr_boxes.insert(0, first_box)

        self.curr_boxes.insert(1, last_box)

    def change_page(self, change_val):

        self.page = (self.page+change_val) % self.page_nb

        self.first_index = self.page*(self.available_box_nb-1)  # one button place is taken by arrows

        if self.first_index > len(list(self.option_dicts[self.option_index].keys())):

            self.page = 0

            self.first_index = 0

            self.dict_index = (self.dict_index+1)%(len(self.option_dicts))

            self.color = self.dicts_colors[self.dict_index]

        Menu.define_curr_boxes(self, first_index)

    def draw(self):

        self.menu_frame.draw()

        for index in range(len(self.curr_boxes)):

            box = self.curr_boxes[index]

            if (index == 0):  #arrow buttons

                box.draw()

            else:

                box.draw(several_lines=2)

    def clicked(self, mouse_pos):

        for x in range(len(self.curr_boxes)):

            panneau = self.curr_boxes[x]

            if panneau.clicked(mouse_pos):

                if x == 1:

                    Menu.change_page(self, 1)

                    return  # breaks loop, for curr_boxes has changed, and anyway job done

                elif x == 0:

                    Menu.change_page(self, -1)

                    return

                else:

                    return panneau.contenu


class Window:

    def __init__(self):

        # defines the user options

        self.define_var_dict = {"variable":[StringTile],}


        self.test_dictionnary = {"si":        [[TestTile, "if"]],
                                 "sinon":      [[TestTile, "elif"]],
                                 "sinon si":   [[TestTile, "else"]],}

        self.affectation_dictionnary = {" = ":AffectTile,}

        self.object_related = {objet:EntityTile,}

        self.variable_val_dict = {"integer":    [IntegerTile],
                             "string":     [StringTile],}

        # options array stores all things that user can add to his code, and how they behave (else has no tile behind, whereas if has)
        self.options_dict = [[self.define_var_dict, BLUE],
                             [self.test_dictionnary, ORANGE],
                             [self.affectation_dictionnary, RED],
                             [self.object_related, GREEN],
                             [self.variable_val_dict, GREY],]

        ##

        # window organisation

        # left part will be a choice menu

        left_width = 200

        left_screen_rect = pygame.Rect(0, 0, left_width, screen_height)

        self.left_menu = Menu(left_screen_rect, self.options_dict)

        # upper part for some options (run, save..)

        up_height = 100

        self.upper_frame = pygame.Rect(left_width, 0, screen_width-left_width, up_height)

        self.run_button = Panneau("", left_width+10, 10, 100, 80, image=draw_play, image_coors=[45, 40])

        # right bottom rect is the biggest rect, that's where user writes (creates) his code

        box_rect = pygame.Rect(left_width, up_height, screen_width-left_width, screen_height-up_height)

        self.code_box = CodeBox(box_rect)

        ##

    def draw(self):

        # draws the global things of the screen
        self.left_menu.draw()

        pygame.draw.rect(screen, BLACK, self.upper_frame)

        self.run_button.draw()

        self.code_box.draw()

    def deal_with_click(self):

        mouse_pos = pygame.mouse.get_pos()

        # run button is clicked
        if self.run_button.clicked(mouse_pos):

            self.code_box.run()

        print(self.left_menu.clicked(mouse_pos))

##


def main():

    play = True

    window = Window()

    while play:

        # deals with user events
        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                play = False

            elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):

                mouse_pos = pygame.mouse.get_pos()

                window.deal_with_click()

            elif (event.type == pygame.MOUSEMOTION):

                translation = event.rel

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_LEFT:

                    pass

        window.draw()

        pygame.display.update()

        clock.tick(60)


if __name__ == "__main__":

    main()
