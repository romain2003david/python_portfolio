from chess_babicka import *


class ScoreMoves:

    def __init__(self, delta_pawn, delta_rook, delta_bishop, delta_knight, delta_king, delta_queen, materiel_total):

        self.delta_pawn = delta_pawn

        self.delta_rook = delta_rook

        self.delta_bishop = delta_bishop

        self.delta_knight = delta_knight

        self.delta_king = delta_king

        self.delta_queen = delta_queen

        self.materiel_total = materiel_total

    def eval_position(self):

        score = 0

        facteur_div_bishop = 6

        score += self.delta_bishop/facteur_div_bishop

        facteur_div_rook = 6

        score += self.delta_rook/facteur_div_rook

        facteur_div_knight = 3

        score += self.delta_knight/facteur_div_knight

        facteur_div_pawn = 10

        score += self.delta_pawn/facteur_div_pawn

        if self.materiel_total > (2*(Grid.total_pieces_value-4)):

            facteur_div_queen = -10

        else:

            facteur_div_queen = 6

        score += self.delta_queen/facteur_div_queen

        if self.materiel_total > (0.7*(Grid.total_pieces_value)):

            facteur_div_queen = -10

        else:

            facteur_div_queen = 3

        score += self.delta_king/facteur_div_king

        return score


class AI:

    def __init__(self, grid, color):

        self.nb_moves_ahead = 2

        self.grid = grid

        self.color = color

    def eval(self):

        nb_pt = 0

        for piece in self.grid.get_pieces():

            if piece.color == self.color:

                nb_pt += piece.value

            else:

                nb_pt -= piece.value

        return nb_pt

    def move_eval(self, move):

        self.grid.move_m(move, graphical_change=False)

        res = AI.eval(self)

        self.grid.unmove(move)

        return res

    def eval_available_moves(self, move, col):

        move.start_piece

        start_t = move.start_tile

        end_t = move.end_tile

        self.grid.move_m(move, graphical_change=False)

        # remonter sur les coups

        bishop_move_gagné = Grid.remonter_sur_diagonales(start_t, end_t)

        ##

        self.grid.unmove(move)
##
##        liste = self.grid.all_moves(col, no_check=True).move_list
##
##        nb_move = len(liste)
##


        score_moves = ScoreMoves()

        return score_moves.eval_position()

    def eval_move_fast(self, move):

        taken_piece = move.end_pos_piece

        win_value = taken_piece.value

        return win_value

    def get_move(self):

        return AI.find_move_rec(self, self.nb_moves_ahead, self.color)[0]

    def find_move_rec(self, nb_moves_ahead, col):

        testing = 0

        testing2 = 0

        best_score = None

        oppo_color = Grid.get_other_col(col)

        possible_moves = self.grid.all_moves(col, no_check=True).move_list  # may contain some illegal moves, but that doesn't matter because they will have a bad rating at next depth

        nb_move = len(possible_moves)

        if nb_move == 0:

            res = AI.eval(self) # PAT ...

        #print(*possible_moves)

        if nb_moves_ahead == 1:

            for move in possible_moves:

                score = AI.eval_move_fast(self, move)

                nb_move2 = AI.eval_with_available_poss(self, move, col)

                score += (nb_move2-nb_move)/8

                if (best_score == None) or (score > best_score):

                    #print(move, score)

                    best_score = score

                    best_moves = [move]  # inits or reinits best_moves

                elif (score == best_score):

                    best_moves.append(move)

            if testing:

                print(best_score, *best_moves)

            return random.choice(best_moves), best_score

        else:

            self.grid.tour += 1  # simulates one move ahead

            for move in possible_moves:
                # evaluates direct benefit for player
                score = AI.eval_move_fast(self, move)  # what we get from the move

                nb_move2 = AI.eval_with_available_poss(self, move, col)

                score += (nb_move2-nb_move)/8
                # takes the king : immediate win
                if score > 50:  # took opponent's king, this move is definitely good, no matter what opponent plays

                    self.grid.tour -= 1

                    return move, score

                # else normally also looks at what the other player can reply
                self.grid.move_m(move, graphical_change=False)

                b_oppo_move, b_oppo_score = AI.find_move_rec(self, nb_moves_ahead-1, oppo_color)  # the best opponent counter move

                score -= b_oppo_score

                self.grid.unmove(move)

                # saves if worth it
                if (best_score == None) or (score > best_score):

                    best_score = score

                    best_moves = [move]  # inits or reinits best_moves

                elif (score == best_score):

                    best_moves.append(move)
                ##

            self.grid.tour -= 1

            if testing or (testing2 and nb_moves_ahead == self.nb_moves_ahead):

                print(best_score, *best_moves)

            return random.choice(best_moves), best_score

##    def play_with_ai(self):
##
##        while not self.grid.won:
##
##            self.grid.draw_gui()
##
##            self.grid.tour += 1
##
##            if self.grid.tour % 2 == self.color:  # player is black
##
##                move = self.grid.play_gui():  # quitting
##
##                if move == "quit":
##                    return True
##
##            else:
##
##                move = AI.get_move(self))
##            self.grid.move_m(self, move)
##            self.grid.draw_gui()



def main():

    game = Game(AI)

    game.play()


main()

















