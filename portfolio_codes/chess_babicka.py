from pig_tv import *

def add_arr(arr1, arr2):

    return [arr1[0]+arr2[0], arr1[1]+arr2[1]]


def copy(tupple):

    return tuple(list(tupple).copy())


class Piece:

    string_color = ['White', 'Black']

    rgb_color = [YELLOW, BROWN]

    margin = 110

    board_size = screen_height-margin

    tile_size = (screen_height-margin)//8

    def __init__(self, pos, color):

        self.pos = pos

        self.i = pos[0]

        self.j = pos[1]

        self.color = color

        Piece.update_visual(self)

    def move(self, i, j, graphical_change=True):

        self.i = i

        self.j = j

        self.pos = (i, j)

        if graphical_change:

            Piece.update_visual(self)

    def update_visual(self):

        self.x = self.j*Piece.tile_size

        self.y = (7-self.i)*Piece.tile_size

        self.gui_color = Piece.rgb_color[(self.i+self.j)%2]

        self.square = pygame.Rect(self.x, self.y, Piece.tile_size, Piece.tile_size)

    def move_arr(self, pos, graphical_change=True):

        i, j = pos

        Piece.move(self, i, j, graphical_change)

    def is_empty(self):

        return self.color == -1

    def draw(self):

        pygame.draw.rect(screen, self.gui_color, self.square)

        pygame.draw.rect(screen, BLACK, self.square, 2)

    def unhighlight(self):

        self.gui_color = Piece.rgb_color[(self.i+self.j)%2]

    def highlight(self):

        self.gui_color = GREEN

    def unhighlight_target(self):

        self.gui_color = Piece.rgb_color[(self.i+self.j)%2]

    def highlight_target(self):

        self.gui_color = RED

    def __str__(self):

        return "{} : {}".format(self.name, self.pos)


class EmptyTile(Piece):

    def __init__(self, pos):

        Piece.__init__(self, pos, -1)

        self.name = 'Empty tile'

        self.value = 0

        self.code_name = '.'

    def update_visual(self):

        self.gui_color = Piece.rgb_color[(self.i+self.j)%2]

        self.square = pygame.Rect(self.x, self.y, Piece.tile_size, Piece.tile_size)


class Rook(Piece):

    value = 5

    def __init__(self, pos, color, grid):

        Piece.__init__(self, pos, color)

        self.name = Piece.string_color[color] + ' rook'

        self.grid = grid

        if self.color == 0:

            self.code_name = 'r'

        else:

            self.code_name = 'R'

        img = pygame.image.load('chess_pictures/rook{}.png'.format(self.color))

        self.image = pygame.transform.scale(img, (Piece.tile_size, Piece.tile_size))

        self.value = Rook.value

    def get_moves(self, no_check=0, only_attacks=False):

        moves = []

        for dirxion in [[-1, 0], [1, 0], [0, -1], [0, 1]]:

            cur_coor = copy(self.pos)

            keep_forward = True

            while keep_forward:

                cur_coor = add_arr(cur_coor, dirxion)

                if self.grid.in_borne(cur_coor):

                    piece = self.grid.get_at_arr(cur_coor)

                    move = Move(self.grid, self.pos, cur_coor)

                    if piece.color != self.color:  # cannot move on piece of same color

                        if no_check or self.grid.try_move_m(move):  # makes sure that the piece's king won't get in trouble, except if this is already a safety check

                            moves.append(move)

                    if not piece.is_empty():  # can't go further after piece encounter

                        keep_forward = False

                else:  # out of grid

                    keep_forward = False

        return Moves(moves)

    def draw(self):

        Piece.draw(self)

        screen.blit(self.image, (self.x, self.y))


class Knight(Piece):

    value = 3

    def __init__(self, pos, color, grid):

        Piece.__init__(self, pos, color)

        self.name = Piece.string_color[color] + ' knight'

        self.grid = grid

        if self.color == 0:

            self.code_name = 'c'

        else:

            self.code_name = 'C'

        img = pygame.image.load('chess_pictures/knight{}.png'.format(self.color))

        self.image = pygame.transform.scale(img, (Piece.tile_size, Piece.tile_size))

        self.value = Knight.value

    def draw(self):

        Piece.draw(self)

        screen.blit(self.image, (self.x, self.y))

    def get_moves(self, no_check=0, only_attacks=False):

        moves = []

        for sgn1 in [-1, 1]:

            for sgn2 in [-1, 1]:

                for delta_x in [1, 2]:

                    if delta_x == 2:

                        delta_y = 1

                    else:

                        delta_y = 2

                    vector = [sgn1*delta_y, sgn2*delta_x]

                    n_pos = add_arr(self.pos, vector)

                    if self.grid.in_borne(n_pos):

                        n_move = Move(self.grid, self.pos, n_pos)

                        piece = self.grid.get_at_arr(n_pos)

                        if piece.color != self.color:

                            if no_check or Grid.try_move_m(self.grid, n_move):

                                moves.append(n_move)

        return Moves(moves)


class Queen(Piece):

    value = 9

    def __init__(self, pos, color, grid):

        Piece.__init__(self, pos, color)

        self.name = Piece.string_color[color] + ' queen'

        self.grid = grid

        if self.color == 0:

            self.code_name = 'q'

        else:

            self.code_name = 'Q'

        img = pygame.image.load('chess_pictures/queen{}.png'.format(self.color))

        self.image = pygame.transform.scale(img, (Piece.tile_size, Piece.tile_size))

        self.value = Queen.value

    def draw(self):

        Piece.draw(self)

        screen.blit(self.image, (self.x, self.y))

    def get_moves(self, no_check=0, only_attacks=False):

        moves = []

        # bishop moves
        for dir_y in [-1, 1]:

            for dir_x in [-1, 1]:

                dir_vect = [dir_y, dir_x]

                cur_coor = copy(self.pos)

                keep_forward = True

                while keep_forward:

                    cur_coor = add_arr(cur_coor, dir_vect)

                    if self.grid.in_borne(cur_coor):

                        piece = self.grid.get_at_arr(cur_coor)

                        move = Move(self.grid, self.pos, cur_coor)

                        if piece.color != self.color:

                            if no_check or Grid.try_move_m(self.grid, move):

                                moves.append(move)

                        if not piece.is_empty():

                            keep_forward = False

                    else:

                        keep_forward = False

        # rook moves
        for dirxion in [[-1, 0], [1, 0], [0, -1], [0, 1]]:

            cur_coor = copy(self.pos)

            keep_forward = True

            while keep_forward:

                cur_coor = add_arr(cur_coor, dirxion)

                if self.grid.in_borne(cur_coor):

                    piece = self.grid.get_at_arr(cur_coor)

                    move = Move(self.grid, self.pos, cur_coor)

                    if piece.color != self.color:  # cannot move on piece of same color

                        if no_check or self.grid.try_move_m(move):  # makes sure that the piece's king won't get in trouble, except if this is already a safety check

                            moves.append(move)

                    if not piece.is_empty():  # can't go further after piece encounter

                        keep_forward = False

                else:  # out of grid

                    keep_forward = False

        return Moves(moves)


class King(Piece):

    value = 100

    def __init__(self, pos, color, grid):

        Piece.__init__(self, pos, color)

        self.name = Piece.string_color[color] + ' king'

        self.grid = grid

        if self.color == 0:

            self.code_name = 'k'

        else:

            self.code_name = 'K'

        img = pygame.image.load('chess_pictures/king{}.png'.format(self.color))

        self.image = pygame.transform.scale(img, (Piece.tile_size, Piece.tile_size))

        self.value = King.value

        self.has_moved = False

    def draw(self):

        Piece.draw(self)

        screen.blit(self.image, (self.x, self.y))

    def get_moves(self, no_check=0, only_attacks=False):

        moves = []

        for i in range(-1, 2):

            for j in range(-1, 2):

                n_pos = add_arr(self.pos, [i, j])

                if self.grid.in_borne(n_pos):

                    n_move = Move(self.grid, self.pos, n_pos)

                    piece = self.grid.get_at_arr(n_pos)

                    if piece.color != self.color:

                        if no_check or self.grid.try_move_m(n_move):

                            moves.append(n_move)

        # castling
        if not (only_attacks or self.has_moved):

            if not self.grid.in_check_cur:  # king can't be in check when castling

                # petit rokk /grand rokk

                pos1, pos2, pos3 = [self.pos[0], self.pos[1]+1], [self.pos[0], self.pos[1]+2], [self.pos[0], self.pos[1]+3]

                move1, move2, move3 = Move(self.grid, self.pos, pos1), Move(self.grid, self.pos, pos2), Move(self.grid, self.pos, pos3)  # both have to be safe places (king needs to cross safely)

                if (self.grid.try_move_m(move1) and self.grid.try_move_m(move2)):#((move1.end_pos_piece == -1) and (move2.end_pos_piece == -1)) and (self.grid.try_move_m(move1) and self.grid.try_move_m(move2)) and (self.color == 0 or move3.end_pos_piece == -1):  # empty tiles and not in check

                    moves.append(move2)

                pos4, pos5, pos6 = [self.pos[0], self.pos[1]-1], [self.pos[0], self.pos[1]-2], [self.pos[0], self.pos[1]-3]  # both have to be safe places (king needs to cross safely)

                move4, move5, move6 = Move(self.grid, self.pos, pos4), Move(self.grid, self.pos, pos5), Move(self.grid, self.pos, pos6)

                if ((move4.end_pos_piece == -1) and (move5.end_pos_piece == -1)) and (self.grid.try_move_m(move4) and self.grid.try_move_m(move5)) and (self.color == 1 or move6.end_pos_piece == -1):  # empty tiles and not in check

                    moves.append(move5)

        return Moves(moves)


class Pawn(Piece):

    value = 1

    def __init__(self, pos, color, grid):

        Piece.__init__(self, pos, color)

        self.name = Piece.string_color[color] + ' pawn'

        self.grid = grid

        if self.color == 0:

            self.code_name = 'p'

            self.vect = 1

        else:

            self.code_name = 'P'

            self.vect = -1

        self.start_ordonnee = pos[0]

        img = pygame.image.load('chess_pictures/pawn{}.png'.format(self.color))

        self.image = pygame.transform.scale(img, (Piece.tile_size, Piece.tile_size))

        self.value = Pawn.value

    def draw(self):

        Piece.draw(self)

        screen.blit(self.image, (self.x, self.y))

    def get_moves(self, no_check=False, only_attacks=False):

        moves = []

        pos = self.pos

        piece_devant = self.grid.get_at(pos[0]+self.vect, pos[1])

        if not only_attacks:

            if piece_devant.color == -1:

                possible_move = Move(self.grid, self.pos, (pos[0]+self.vect, pos[1]))

                if no_check or self.grid.try_move_m(possible_move):

                    moves.append(possible_move)

                if pos[0] == self.start_ordonnee:  # even if moving pawn forward of one might not avoid check, moving forward two could

                    pos2forward = (pos[0]+self.vect*2, pos[1])

                    if self.grid.in_borne(pos2forward):

                        piece_devant2 = self.grid.get_at_arr(pos2forward)

                        if piece_devant2.color == -1:

                            possible_move2 = Move(self.grid, self.pos, pos2forward)

                            if no_check or self.grid.try_move_m(possible_move2):

                                moves.append(possible_move2)

        other_pos_s = [(pos[0]+self.vect, pos[1]-1), (pos[0]+self.vect, pos[1]+1)]

        for oth_pos in other_pos_s:

            if self.grid.in_borne(oth_pos):

                piece = self.grid.get_at_arr(oth_pos)

                if ((piece.color != -1) and (piece.color != self.color)) or (oth_pos[1] in self.grid.available_passant and ((self.color == 0 and pos[0] == 4) or (self.color == 1 and pos[0] == 3))):  # opponent piece or coup en passant

                    #if (oth_pos[1] in self.grid.available_passant and ((self.color == 0 and pos[0] == 4) or (self.color == 1 and pos[0] == 3))):

                    n_move = Move(self.grid, self.pos, oth_pos)

                    if no_check or self.grid.try_move_m(n_move):

                        moves.append(n_move)

        return Moves(moves)


class Bishop(Piece):

    value = 3

    def __init__(self, pos, color, grid):

        Piece.__init__(self, pos, color)

        self.name = Piece.string_color[color] + ' bishop'

        self.grid = grid

        if self.color == 0:

            self.code_name = 'b'

        else:

            self.code_name = 'B'

        img = pygame.image.load('chess_pictures/bishop{}.png'.format(self.color))

        self.image = pygame.transform.scale(img, (Piece.tile_size, Piece.tile_size))

        self.value = Bishop.value

    def draw(self):

        Piece.draw(self)

        screen.blit(self.image, (self.x, self.y))

    def get_moves(self, no_check=0, only_attacks=False):

        moves = []

        for dir_y in [-1, 1]:

            for dir_x in [-1, 1]:

                dir_vect = [dir_y, dir_x]

                cur_coor = copy(self.pos)

                keep_forward = True

                while keep_forward:

                    cur_coor = add_arr(cur_coor, dir_vect)

                    if self.grid.in_borne(cur_coor):

                        piece = self.grid.get_at_arr(cur_coor)

                        move = Move(self.grid, self.pos, cur_coor)

                        #print(move, piece.name)

                        if piece.color != self.color:

                            if no_check or Grid.try_move_m(self.grid, move):

                                moves.append(move)

                        if piece.color != -1:

                            keep_forward = False

                    else:

                        keep_forward = False

        return Moves(moves)


class Move:

    def __init__(self, grid, start_pos, end_pos):

        #self.grid = grid

        self.start_pos = list(start_pos)

        self.end_pos = list(end_pos)

        self.start_pos_piece = grid.get_at_arr(start_pos)

        self.end_pos_piece = grid.get_at_arr(end_pos)

    def __eq__(self, move):

        if not isinstance(move, Move):

            return False

        return (self.start_pos == move.start_pos and self.end_pos == move.end_pos)

    def __str__(self):

        return "{} : {} -> {}".format(self.start_pos_piece, str(self.start_pos), str(self.end_pos))

##    def __repr__(self):
##
##        return 

    def end_pos_is(self, pos):

        return list(pos) == self.end_pos


class Moves:

    def __init__(self, move_list):

        self.move_list = move_list

    def contains(self, test_move):

        for move in self.move_list:

            if move == test_move:

                return True

    def contains_end_pos(self, pos):

        for move in self.move_list:

            if move.end_pos_is(pos):

                return True

    def __str__(self):

        return str([str(move) for move in self.move_list])

    def get_pieces(self):

        pieces = []

        for move in self.move_list:

            pieces.append(move.end_pos_piece)

        return pieces

    def add_moves(self, moves_inst):

        self.move_list.extend(moves_inst.move_list)

    def is_nul(self):

        return self.move_list == []


class Grid:
    """ all_moves """

    total_pieces_value = Queen.value + 2*(Bishop.value+Knight.value+Rook.value) + 8*Pawn.value

    def __init__(self):

        # grid content, pieces and positions
        self.won = False

        self.grid = [[EmptyTile((i, j)) for j in range(8)] for i in range(8)]

        pieces = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]

        self.available_passant = []

        self.kings_moved = [False, False]

        self.in_check_cur = False

        # test
        test_grid = 0

        # normal chessboard
        if test_grid == 0:

            for j in range(8):

                self.grid[1][j] = Pawn((1, j), 0, self)  # black pawns

                self.grid[6][j] = Pawn((6, j), 1, self)  # white pawns

                self.grid[0][j] = pieces[j]((0, j), 0, self)  # black pieces

                self.grid[7][j] = pieces[j]((7, j), 1, self)

            self.kings = [Grid.get_at(self, 0, 4), Grid.get_at(self, 7, 4)]

        # only for testing purpose : begins at custom chessboard
        elif test_grid == 1:

            Grid.create_piece_at(self, Pawn, (7, 4), 1)

            Grid.create_piece_at(self, Pawn, (6, 4), 1)

            Grid.create_piece_at(self, Knight, (3, 3), 1)

            Grid.create_piece_at(self, Rook, (0, 7), 0)

            Grid.create_piece_at(self, King, (0, 0), 0)

            Grid.create_piece_at(self, King, (7, 0), 1)

            self.kings = [Grid.get_at(self, 0, 0), Grid.get_at(self, 7, 0)]

            print(*self.kings)

        elif test_grid == 2:

            Grid.create_piece_at(self, Pawn, (6, 4), 0)

            Grid.create_piece_at(self, King, (6, 2), 0)

            Grid.create_piece_at(self, King, (7, 0), 1)

            self.kings = [Grid.get_at(self, 6, 2), Grid.get_at(self, 7, 0)]
    ##

        self.tour = -1

        # gui interface

        self.selected_piece = None

        self.target_piece = None

        self.possible_targets = []

    def create_piece_at(self, piece, pos, col):

        i, j = pos

        self.grid[i][j] = piece((i, j), col, self)

    def get_at(self, i, j):

        return self.grid[i][j]

    def get_at_arr(self, pos):

        return Grid.get_at(self, pos[0], pos[1])

    def coor_conversion(string_coor):

        abcs = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

        j = abcs.index(string_coor[0])

        i = int(string_coor[1])-1

        return (i, j)

    def in_borne(self, coor):

        x, y = coor

        return 0<=x<=7 and 0<=y<=7

    def play(self):

        testing = True

        test_sequence = [["e2", "e4"], ["e7", "e5"], ["f1", "c4"], ["d7", "d6"], ["c4", "f7"], ["e8", "f7"], ["d1", "e2"], ["g8", "f6"]]

        finished = False

        print('\nTour {}\n{} to play\n'.format(str(self.tour-1), Piece.string_color[Grid.get_color_cur(self)]))

        if Grid.in_check_cur:

            print('Le {} est en échec !\n'.format(self.kings[Grid.get_color_cur(self)].name))

        while not finished:

            Grid.draw(self)

            #Grid.draw_pieces(self)

            if testing:

                start_coor = test_sequence[self.tour-1][0]

                end_coor = test_sequence[self.tour-1][1]

            else:

                start_coor = input("\nStart coor : ")

                end_coor = input("\nEnd coor : ")


            exception = False

            try:

                i1, j1 = Grid.coor_conversion(start_coor)

                i2, j2 = Grid.coor_conversion(end_coor)

            except ValueError:

                print('\nBad coordinate format.\n')

                exception = True

            if not exception:

                move = Move(self, (i1, j1), (i2, j2))

                s_piece = Grid.get_at(self, i1, j1)

                if s_piece.color == Grid.get_color_cur(self):  # chose tile where there is their piece

                    possible_moves = s_piece.get_moves()  # all possible moves of a piece

                    #print(possible_moves, move)

                    if possible_moves.contains(move):  # the destination tile is one of the possible moves

                        Grid.move_m(self, move)

                        finished = True  # player played

                    else:

                        print('\nBad move for '+s_piece.name+'.\n')

                else:

                    print('\n'+s_piece.name+' is not one of your pieces.\n')

    def draw(self):

        print()

        for i in range(8):

            print(str(8-i), end='  ')

            for j in range(8):

                print(self.grid[8-i-1][j].code_name, end=' ')

            print()

        print()
        print('   A B C D E F G H')

    def draw_pieces(self):

        print()
        print(Grid.get_at(self, 0, 0).name, end=' ')
        for i in range(8):

            print(str(8-i), end='  ')

            for j in range(8):

                print(Grid.get_at(self, 8-i-1, j).name, end=' ')

            print()

        print()
        print('   A B C D E F G H')

    def draw_gui(self):

        check = self.in_check_cur
        
        for piece in get_flattened_list(self.grid):

            piece.draw()

        aff_txt("Tour de jeu {}, au {} de jouer".format(self.tour, Grid.get_str_color_cur(self)), 10, Piece.board_size+20)

        if check:

            aff_txt("Check !", screen_width-200, 50)

        pygame.display.update()

    def unmove(self, move, graphical_change=False):
        """ cancels a move that we've tried out, after a safety "no checks" check for instance """
        pos1 = move.start_pos

        pos2 = move.end_pos

        piece1 = move.start_pos_piece

        piece2 = move.end_pos_piece

        piece1.move_arr(pos1, graphical_change=graphical_change)

        if graphical_change:

            piece2.update_visual()

        Grid.set_at_arr(self, pos1, piece1)

        Grid.set_at_arr(self, pos2, piece2)

        # coup en passant
        if isinstance(piece1, Pawn) and (pos1[1] != pos2[1]) and (piece2.color == -1):

            if piece1.color == 0:

                pos_cree = [pos2[0]-1, pos2[1]]

            else:

                pos_cree = [pos2[0]+1, pos2[1]]

            Grid.create_piece_at(self, Pawn, pos_cree, Grid.oppo_col(piece1.color))

    def move_m(self, move, graphical_change=True, gui_mode=True, try_mode=False):

        Grid.move(self, move.start_pos, move.end_pos, graphical_change, gui_mode, try_mode)

    def move(self, pos1, pos2, graphical_change=True, gui_mode=True, try_mode=False):

        piece1 = Grid.get_at_arr(self, pos1)

        piece2 = Grid.get_at_arr(self, pos2)

        piece1.move_arr(pos2, graphical_change)

        if not try_mode:  # only if real move, to know if next player can "coup en passant"

            self.available_passant = []  # a priori, no passant available

            # disabling castling
            if isinstance(piece1, King):

                piece1.has_moved = True

        # checking for promotion

        if isinstance(piece1, Pawn):

            # promotion

            if pos2[0] in [0, 7]:  # end of line for black or white

                if gui_mode:

                    n_piece = Grid.choose_promotion(self, piece1.color)

                else:

                    n_piece = Queen  # I hope AI's like queens ; to my mind they should

                piece1 = n_piece(piece1.pos, piece1.color, self)

            # coup en passant updating

            if not try_mode:  # only if real move, to know if next player can "coup en passant"

                if (abs(pos2[0]-pos1[0]) == 2):  # difference en ligne (le pion a avance de deux cases)

                    self.available_passant = [pos1[1]]

            # coup en passant eating

            if (pos2[1] != pos1[1]) and piece2.color == -1:  # chgmt de colonne (pion mange) mais case d'arrivee vide

                if piece1.color == 0:

                    pos_supprimee = [pos2[0]-1, pos2[1]]

                else:

                    pos_supprimee = [pos2[0]+1, pos2[1]]

                Grid.set_at_arr(self, pos_supprimee, EmptyTile(pos_supprimee))

        if isinstance(piece1, King):

            if :

                

        Grid.set_at_arr(self, pos2, piece1)

        Grid.set_at_arr(self, pos1, EmptyTile(pos1))

    def set_at_arr(self, arr_pos, piece):
        """ sets a position arr_pos of the grid to a new piece """
        a, b = arr_pos

        self.grid[a][b] = piece

    def oppo_col(col):

        return -(col%2-1)

    def get_color_opp(self):

        return Grid.oppo_col(Grid.get_color_cur(self))

    def get_color_cur(self):

        return self.tour%2

    def get_other_col(col):

        return -(col-1)

    def get_str_color_cur(self):

        return Piece.string_color[Grid.get_color_cur(self)]

    def get_pieces(self):

        return get_flattened_list(self.grid)

    def get_all_pieces_except_king(self, color):

        pieces = []

        for i in range(8):

            for j in range(8):

                piece = Grid.get_at(self, i, j)

                if piece.color == color:

                    if not isinstance(piece, King):

                        pieces.append(piece)

        return pieces

    def try_move(self, pos1, pos2):

        move = Move(self, pos1, pos2)

        return Grid.try_move_m(self, Move(self, pos1, pos2))

    def try_move_m(self, move):

        test = False  # True

        Grid.move_m(self, move, graphical_change=test, gui_mode=False, try_mode=True)  # gui mode lets the player chose his piece when he promotes a pawn

        if test:

            Grid.draw_gui(self)

            time.sleep(.02)  # wait()
        
        result = Grid.in_check(self)

        Grid.unmove(self, move, graphical_change=test)

        if test:

            Grid.draw_gui(self)

            time.sleep(.02)  # wait()

        return not result

    def in_check(self):

        king_pos = self.kings[Grid.get_color_cur(self)].pos

        #print(king_pos)

        oppo_pieces = Grid.all_pieces(self, Grid.get_color_opp(self))

        for piece in oppo_pieces:

            if piece.get_moves(no_check=1, only_attacks=True).contains_end_pos(king_pos):  # only attacks because moves that don't attack (such as castling) can't threaten the king

                return True

        return False

    def get_clicked_piece(self, mouse_pos):

        x, y = mouse_pos

        i, j = y//Piece.tile_size, x//Piece.tile_size

        if Grid.in_borne(self, (i, j)):

            return Grid.get_at(self, (7-i), j)

        return None

    def player_move_gui(self):
        """ lets a player chose the piece he wants to move and the destination tile """

        Grid.cancel_selected_piece(self)

        choose = True

        clicking = 0

        quite = False

        while choose:

            for event in pygame.event.get():

                if event.type == pygame.QUIT:

                    choose = False

                    quite = True

                elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):

                    clicking = 1

                    piece = Grid.get_clicked_piece(self, pygame.mouse.get_pos())

                    if piece != None:

                        #player has no selected piece nor has he clicked on one of his pieces 
                        if (piece.color != Grid.get_color_cur(self)) and (self.selected_piece == None):

                            Grid.cancel_selected_piece(self)

                        # player has selected one of his pieces
                        elif (self.selected_piece == None) or (piece.color == Grid.get_color_cur(self)):

                            Grid.update_selected_piece(self, piece)

                        else:

                            if Grid.valid_target_piece(self, piece):

                                choose = False

                            else:

                                Grid.cancel_selected_piece(self)

                elif (event.type == pygame.MOUSEBUTTONUP) and (event.button == 1):

                    clicking = 0

                elif (event.type == pygame.MOUSEMOTION):

                    translation = event.rel

                elif event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_LEFT:

                        pass

            screen.fill(WHITE)

            Grid.draw_gui(self)

            clock.tick(60)

        return quite

    def cancel_selected_piece(self):

        Grid.cancel_targets(self)

        if not self.selected_piece == None:

            self.selected_piece.unhighlight()

            self.selected_piece = None

    def cancel_targets(self):

        for piece in self.possible_targets:

            piece.unhighlight_target()

        self.possible_targets = []

    def update_selected_piece(self, piece):

        # cancels last selected piece
        Grid.cancel_selected_piece(self)

        # sets new selected piece
        self.selected_piece = piece

        if (piece != None) and (piece.color == Grid.get_color_cur(self)):

            # computation
            possible_moves = self.selected_piece.get_moves(no_check=False)  # only legal moves

            self.possible_targets = possible_moves.get_pieces()

            # graphical update
            piece.highlight()

            for piece in self.possible_targets:

                piece.highlight_target()

    def valid_target_piece(self, target_piece):

        if (self.possible_targets != []) and (target_piece in self.possible_targets):  # .contains(move):

            self.target_piece = target_piece

            return True

    def choose_promotion(self, color):
        """ during the special move when a pawn promotes """

        chosing = True

        x_rect, y_rect = 100, 100

        margin = 10

        size = Piece.tile_size + margin

        possible_pieces = [Knight, Bishop, Rook, Queen]

        false_grid = Grid()

        possible_pieces_inst = [piece([0, 0], color, false_grid)for piece in possible_pieces]

        gui_rects = [Panneau("", 2*margin+x_rect+i*size, y_rect, Piece.tile_size, Piece.tile_size) for i in range(4)]

        rect_menu = pygame.Rect(x_rect, y_rect, int(size*(len(gui_rects)+1)), 200)

        while chosing:

            for event in pygame.event.get():

                if event.type == pygame.QUIT:

                    chosing = False

                    quite = True

                elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):

                    clicking = 1

                    for rect in gui_rects:

                        if rect.clicked(pygame.mouse.get_pos()):

                            return possible_pieces[gui_rects.index(rect)]


            pygame.draw.rect(screen, BLUE, rect_menu)

            aff_txt("Choose your new piece ", 2*margin+x_rect, y_rect+100)

            for i in range(len(gui_rects)):

                rect = gui_rects[i]

                rect.draw()

                screen.blit(possible_pieces_inst[i].image, (int(2*margin+x_rect+i*size), int(y_rect)))

            pygame.display.update()

            clock.tick(60)


    def get_move_gui(self):

        # let's player select their move
        quite = Grid.player_move_gui(self)

        if quite:

            return "quit"

        # updates move
        i1, j1 = self.selected_piece.pos

        i2, j2 = self.target_piece.pos

        # graphical purposes only

        Grid.cancel_selected_piece(self)

        return Move(self, (i1, j1), (i2, j2))

    def all_pieces(self, col):

        return [piece for piece in Grid.get_pieces(self) if piece.color == col]

    def is_legal(self, move):

        return Grid.all_moves(self, Grid.get_color_cur(self)).contains(move)

    def all_moves(self, col, no_check=False):
        """ get all moves of a piece's color, set no_check= false if you want all seemingly legal moves but without making sure the king isn't in check """
        rs = Moves([])

        #print(AI.all_pieces(self, col)[0])

        for piece in Grid.all_pieces(self, col):

            rs.add_moves(piece.get_moves(no_check))

        return rs

    def before_each_move(self):

        self.tour += 1

        self.in_check_cur = Grid.in_check(self)

        if self.in_check_cur:

            print("check")

        all_moves = Grid.all_moves(self, Grid.get_color_cur(self))

        if all_moves.is_nul():

            if self.in_check_cur:

                if self.tour % 2 == 1:

                    self.won = "white won"

                else:

                    self.won = "black won"

            else:

                self.won = "pat"

    def play_game(self):

        gui = True

        Grid.before_each_move(self)

        while not self.won:

            if gui:

                move = Grid.get_move_gui(self)

                if move == "quit":  # quitting

                    return True

                Grid.move_m(self, move)

            else:

                grid.play()

            Grid.before_each_move(self)

        print(self.won)


class Game:

    def __init__(self, player1=None, player2=None):
        """
        simulates a game with two players, potentially AIs
        an AI player has :
        - a function get_move() which returns a Move instance, or "quit" if a problem occurs
        - is initialised with the grid instance and a color (0 for white, 1 for black)
        
        the grid class contains the 2D array grid.grid of Piece instances, and interesting functions:
        - all_move, return a moves instance, do moves.move_list to get Move array
        - 
        """

        self.grid = Grid()

        self.player1 = player1

        self.player2 = player2

        # player 1
        # human player
        if self.player1 == None:

            self.move_function1 = self.grid.get_move_gui

        else:  # bot player

            self.player1 = player1(self.grid, 0)

            self.move_function1 = self.player1.get_move

        # player 2
        if self.player2 == None:

            self.move_function2 = self.grid.get_move_gui

        else:

            self.player2 = player1(self.grid, 1)

            self.move_function2 = self.player2.get_move

    def play(self):

        self.grid.tour += 1

        while not self.grid.won:

            self.grid.draw_gui()

            # black (second player) about to move
            if self.grid.tour % 2 == 0:

                time_before = time.time()

                move = self.move_function2()

                print("response time : {} s".format(round(time.time()-time_before, 1)))

                if move == "quit":

                        return

            # white (first player) about to move
            else:

                time_before = time.time()

                move = self.move_function1()

                print("response time : {} s".format(round(time.time()-time_before, 1)))

                if move == "quit":

                        return

            if self.grid.is_legal(move):

                self.grid.move_m(move)

            else:

                print("coup illégal : {}".format(move))

                break

            self.grid.draw_gui()

            # next tour
            self.grid.tour += 1

            self.grid.before_each_move()


        print(self.grid.won)

    # simulations de coups inverse (pour compter move nb)

    def remonter_sur_diagonales(self):

        pass


def main():

    grid = Grid()

    grid.play_game()


if __name__ == "__main__":

    main()




