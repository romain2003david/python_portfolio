from pig_tv import *


class Tile:
    """ brique de construction de base d'un code """

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



class UserInputTile(Tile):

    width = 100

    height = 80


class StringTile(Tile):

    def __init__(self, x, y, content):

        color = YELLOW

        Tile.__init__(self, x, y, content, color)

        self.box.update_dimensions((len(content)+2)*Tile.letter_size, self.box.hauteur)

        if content == "_":

            self.next_curs_pos = [self.box.x, self.box.y]

            self.next_obj_pos = [self.box.x+self.box.largeur, self.box.y]

        else:

            self.next_curs_pos = [self.box.x+self.box.largeur, self.box.y]

            self.next_obj_pos = self.next_curs_pos


class IntegerTile(Tile):

    def __init__(self, x, y, int_content):

        Tile.__init__(self, x, y, int_content)


class TestTile(Tile):

    def __init__(self, x, y, test_type):

        Tile.__init__(self, x, y, test_type)

        self.box.color = GREEN

        self.box.hauteur += Tile.basic_height

        state_ti = StatementTile(x+Tile.indentation, y+Tile.basic_height)

        self.children_tiles = [state_ti]

        if test_type != "else":

            condition_tile = ConditionTile(x+Tile.letter_size*len(test_type), y)

            self.children_tiles.append(condition_tile)

            self.next_cursor_coor = [x+Tile.letter_size*len(test_type), y]

        else:

            self.next_cursor_coor = [x+Tile.indentation, y+Tile.basic_height]

        self.next_obj_pos = [x, y+2*Tile.basic_height]

    def draw(self):

        self.box.draw()

        aff_txt("alors", x+indentation, y+Tile.basic_height)

        for tile in self.children_tiles:

            tile.draw()


class StatementTile(Tile):

    def __init__(self, x, y):

        Tile.__init__(self, x, y)

        self.color = BLUE

        self.box.color = self.color

    def draw(self):

        self.box.draw()


class CodeBox:

    def __init__(self, left_menu_width):

        # defines the user options

        self.define_var_dict = {"variable":[StringTile],}


        self.test_dictionnary = {"si":        [[TestTile, "if"]],
                                 "sinon":      [[TestTile, "elif"]],
                                 "sinon si":   [[TestTile, "else"]],}

        self.affectation_dictionnary = {" = ":AffectTile,}

        self.object_related = {objet:EntityTile,}

        self.variable val = {"integer":    [IntegerTile],
                             "string":     [StringTile],}

        # options array stores all things that user can add to his code, and how they behave (else has no tile behind, whereas if has)
        options = [self.define_var_dict, self.test_dictionnary, self.affectation_dictionnary, self.objetc_related, self.variable val]

        ##
  
        self.code_list = []

        self.margin = 10

        self.y = 100

        self.x = left_menu_width

        self.width = screen_width-left_menu_width

        self.height = screen_height-self.y

        self.gui = Panneau("", self.x, self.y, self.width, self.height)

        self.x_lift = Lift(left_menu_width+10, self.height+80, self.width-40, 10, 16, -1000, 1000, afficher_echelle=0)

        self.x_lift_clicked = 0

        self.y_lift = Lift(left_menu_width+self.width-30, 120, 10, self.height-70, 16, -1000, 1000, afficher_echelle=0, vertical=1)

        self.y_lift_clicked = 0

        self.active_tile = 0

        self.cursor = [self.x+self.margin, self.y+self.margin]

        self.saved_color = 0

    def define_active_tile(self, index):

        if self.active_tile:

            self.active_tile.modify_color(self.saved_color)

        if index != None:

            self.active_tile = self.code_list[index]

            self.saved_color = self.active_tile.box.color

            self.active_tile.modify_color(RED)

        else:

            self.active_tile = 0

    def draw(self):

        x_trans, y_trans = self.x_lift.echelle, self.y_lift.echelle

        self.gui.draw()

        self.x_lift.draw()

        self.y_lift.draw()

        for box in self.code_list:

            last_x = box.x

            box.draw()

            box.update_pos(x_trans, y_trans)

    def append(self, element):

        to_append = self.option_dictionnary[element]

        if self.active_tile:

            for x in to_append:

                self.active_tile.append(x)

        else:

            for x in to_append:

                if type(x) == list:

                    self.code_list.append(x[0](self.cursor[0], self.cursor[1], x[1]))

                elif type(x) == str:

                    self.code_list.append(StringTile(self.cursor[0], self.cursor[1], x))

                elif x == StringTile:

                    self.code_list.append(StringTile(self.cursor[0], self.cursor[1], "_"))

                self.cursor = self.code_list[-1].next_obj_pos

            self.cursor = self.code_list[-1].next_curs_pos

    def run(self):

        print("Running user code")

    def check_click(self, mouse_pos, translation, mouse_got_clicked):
        """ when users clicks, check if a tile has been clicked, or some other part of the code """

        x_trans, y_trans = self.x_lift.echelle, self.y_lift.echelle

        for box in self.code_list:

            box.update_pos(-x_trans, -y_trans)

        if self.x_lift_clicked:

            self.x_lift.go(translation[0])

        if self.y_lift_clicked:

            self.y_lift.go(translation[1])

        if mouse_got_clicked:

            found_active = 0

            for index in range(len(self.code_list)):

                box = self.code_list[index]

                if box.clicked(mouse_pos):

                    CodeBox.define_active_tile(self, index)

                    found_active = 1

            if (not found_active) and mouse_pos:

                CodeBox.define_active_tile(self, None)


def main():

    # instances

    options = ["variable = ", "string", "integer", "skin",  "egal a", "different de", "superieur a", "inferieur a", "si", "sinon", "sinon si", "fonction", "et", "ou", "xor"]

    left_menu_width = screen_width//3

    left_menu = Menu(0, 0, left_menu_width, screen_height, 4, options, vertical=1, box_width=250)

    code_box = CodeBox(left_menu_width)

    run_box = Panneau("", left_menu_width+10, 10, 100, 80, image=draw_play, image_coors=[45, 40])

    upper_part = pygame.Rect(left_menu_width, 0, screen_width-left_menu_width, 100)

    # variables

    play = True

    #clicking = 0

    # main loop

    while play:

        mouse_got_clicked = 0

        mouse_pos = pygame.mouse.get_pos()

        translation = [0, 0]

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                play = False

            elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):

                mouse_got_clicked = 1

                #if not clicking:

                    #clicking = 1

                # checking user actions

                if code_box.x_lift.clicked(mouse_pos):

                    code_box.x_lift_clicked = 1

                if code_box.y_lift.clicked(mouse_pos):

                    code_box.y_lift_clicked = 1

                user_choice = left_menu.clicked(mouse_pos)

                if user_choice:

                    code_box.append(user_choice)

                if run_box.clicked(mouse_pos):

                    code_box.run()

            elif (event.type == pygame.MOUSEBUTTONUP) and (event.button == 1):

                #clicking = 0

                if code_box.x_lift_clicked:

                    code_box.x_lift_clicked = 0

                if code_box.y_lift_clicked:

                    code_box.y_lift_clicked = 0

            elif (event.type == pygame.MOUSEMOTION):

                translation = event.rel

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_LEFT:

                    pass

        # dealing with user events

        code_box.check_click(mouse_pos, translation, mouse_got_clicked)

        # drawing GUI

        code_box.draw()

        pygame.draw.rect(screen, BLACK, upper_part)

        run_box.draw()

        left_menu.draw()

        pygame.display.update()

        clock.tick(60)


if __name__ == "__main__":

    main()
