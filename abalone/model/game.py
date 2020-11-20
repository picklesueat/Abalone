from abalone import BLACK, WHITE, EMPTY
from . import board
from .board import axial_coord
from copy import deepcopy


class Move():
    def __init__( self , coords_from , direction , move_type = board.AbaloneBoard.VALID ):
        self.coords_from = coords_from
        self.direction = direction
        self.move_type = move_type

    def __str__(self):
        return "Pieces moved: {}, Direction: {}, Move Type {}".format( self.coords_from, self.direction, self.move_type )

class Game():
    ''' Represents a game of Abalone

        Methods
        -------
        make_turn -- Takes a move and makes a turn

        Attributes
        ----------
        size -- max distance from a hex to the center
        lives -- lives for each player at start, function of size
        board -- a board with a state
        turn -- current players turn
    '''
    lives = {2: 1,
            3:2,
            4:4,
            5:6}

    class Player():
        def __init__( self , color , lives ):
            self.color = color
            self.lives = lives


    class AI( Player ):
        def __init__( self , color , lives,  depth ):
            super().__init__( color , lives)
            self.depth = depth


    def __init__( self , size ):
        self.size = size

        self.board = board.AbaloneBoard( self.size )
        self.add_pieces()

        self.lives = self.lives[ self.size ]
        self.winner = EMPTY

        self.turn = BLACK
        self.history = []


    def add_pieces( self ):
        # #regular setup
        if( self.size == 2 ):
            for hex in self.board:
                if( hex.axial_coord.y == 0 ):
                    hex.val = WHITE

                if( hex.axial_coord.y == self.size * 2 - 1 - 1 ):
                    hex.val = BLACK
        #
        # if( self.size == 3 ):
        #     self.board[ axial_coord( 2, 1)] = WHITE
        #     self.board[ axial_coord( 3, 1)] = WHITE
        #
        #     self.board[ axial_coord( 2, 3)] = BLACK
        #     self.board[ axial_coord( 1, 3)] = BLACK

        #Belgian Daisy
        if( self.size == 3 ):
            self.board[ axial_coord( 2, 0)] = WHITE
            self.board[ axial_coord( 1, 1)] = WHITE
            self.board[ axial_coord( 2, 1)] = WHITE

            self.board[ axial_coord( 2, 4)] = WHITE
            self.board[ axial_coord( 3, 3)] = WHITE
            self.board[ axial_coord( 2, 3)] = WHITE


            self.board[ axial_coord( 4, 0)] = BLACK
            self.board[ axial_coord( 4, 1)] = BLACK
            self.board[ axial_coord( 3, 1)] = BLACK

            self.board[ axial_coord( 0, 4)] = BLACK
            self.board[ axial_coord( 1, 3)] = BLACK
            self.board[ axial_coord( 0, 3)] = BLACK

        if( self.size == 4 ):
            self.board[ axial_coord( 3, 0)] = WHITE
            self.board[ axial_coord( 4, 0)] = WHITE
            self.board[ axial_coord( 5, 0)] = WHITE
            self.board[ axial_coord( 6, 0)] = WHITE

            self.board[ axial_coord( 3, 1)] = WHITE
            self.board[ axial_coord( 4, 1)] = WHITE
            self.board[ axial_coord( 5, 1)] = WHITE
            self.board[ axial_coord( 2, 1)] = WHITE
            self.board[ axial_coord( 6, 1)] = WHITE


            self.board[ axial_coord( 0, 6)] = BLACK
            self.board[ axial_coord( 1, 6)] = BLACK
            self.board[ axial_coord( 2, 6)] = BLACK
            self.board[ axial_coord( 3, 6)] = BLACK

            self.board[ axial_coord( 1, 5)] = BLACK
            self.board[ axial_coord( 2, 5)] = BLACK
            self.board[ axial_coord( 3, 5)] = BLACK
            self.board[ axial_coord( 0, 5)] = BLACK
            self.board[ axial_coord( 4, 5)] = BLACK

        if( self.size == 5 ):
            for hex in self.board:
                if( hex.axial_coord.y == 0 or hex.axial_coord.y == 1 ):
                    hex.val = WHITE

                if( hex.axial_coord.y == self.size * 2 - 1 - 1 or  hex.axial_coord.y == self.size * 2 - 1 - 2 ):
                    hex.val = BLACK

            self.board[ axial_coord( 2, 6)] = BLACK
            self.board[ axial_coord( 3, 6)] = BLACK
            self.board[ axial_coord( 4, 6)] = BLACK

            self.board[ axial_coord( 4, 2)] = WHITE
            self.board[ axial_coord( 5, 2)] = WHITE
            self.board[ axial_coord( 6, 2)] = WHITE


    def change_player( self ):
        ''' Changes the player to the opposite of the current one
        '''
        if( self.turn == BLACK ):
            self.turn = WHITE
        else:
            self.turn = BLACK

    def lose_piece( self ):
        ''' Takes away one life, from whichever players turn it is NOT
        '''
        if( self.turn == BLACK ):
            self.black_player.lives = self.black_player.lives - 1
        else:
            self.white_player.lives = self.white_player.lives - 1

    def undo_lose_piece( self ):
        ''' Takes away one life, from whichever players turn it is NOT
        '''
        if( self.turn == BLACK ):
            self.black_player.lives = self.black_player.lives + 1
        else:
            self.white_player.lives = self.white_player.lives + 1

    def check_winner( self ):
        ''' Checks if either player has lost
        '''
        if( self.white_player.lives == 0 ):
            self.winner = BLACK
        if( self.black_player.lives == 0 ):
            self.winner = WHITE

    def make_turn( self , coords_from: list , direction: axial_coord ):
        '''  Takes coordinates, makes move, and updates game state based on the move_type that is returned.

            Arguments:
            coords_from -- list of coords, known to be on the board, and not None
        '''

        move_type = self.board.direction_move( coords_from, direction )

        if( move_type == self.board.POINT ):
            self.change_player()
            self.lose_piece()
            self.history.append(Move( coords_from , direction , move_type ))

        elif( move_type % 2 == 0 and move_type != 0  ):
            self.change_player()
            self.history.append(Move( coords_from , direction , move_type ))

        elif( move_type ):
            self.change_player()
            self.history.append(Move( coords_from , direction ))

        else:
            print( 'oh no')
            print( self.board )
            for move in self.history:
                print( move )
            print( 'Trying to make: ' ,coords_from , direction )
            print('\n')
            #shitty error handling
            return 'bleh'

        self.check_winner()

    def undo_last_turn( self ):
        last_move = self.history.pop(-1)
        self.board.undo_move( last_move.coords_from , last_move.direction , last_move.move_type )
        if( last_move.move_type == board.AbaloneBoard.POINT ):
            self.undo_lose_piece()
        self.change_player()
        self.winner = EMPTY



    def __str__( self ):
        return str( self.board )

    def __len__( self ):
        return self.size

    def __iter__( self ):
        return iter( self.board )

    def __getitem__( self, coords ):
        return self.board[ coords ]

    def __setitem__( self, coords, val ):
        self.board[ coords ] = val

class TwoPlayerGame( Game ):
    ''' Game class where both players are human
    '''
    def __init__( self , size ):
        super().__init__( size )

        self.white_player = self.Player( WHITE , self.lives)
        self.black_player = self.Player( BLACK , self.lives)

        self.turn = BLACK

class PlayerVSAIGame( Game ):
    ''' Game class with one human, and on AI

        Methods
        -------
        make_AI_turn -- gets AI move, and makes it
        children_generator

        Attributes
        ----------
        depth -- depth of AI search
    '''
    def __init__( self , size , depth = 1):
        super().__init__( size )

        self.white_player = self.Player( WHITE , self.lives)
        self.black_player = super().AI( BLACK , self.lives , depth )

        self.turn = BLACK

        self.make_AI_turn()


    def make_AI_turn( self ):
        if( self.turn != BLACK or self.winner != EMPTY ):
            return None

        move = self.minimax( self.black_player.depth , float('-inf') , float('inf') )
        move = move[1]

        self.make_turn( move.coords_from , move.direction )

        return True

    def children_generator( self ):
        ''' Returns a list of every possible move as their own games

            Notes:
            For each move in the possible moves of a given game state,
            create a copy of the current game and make the move on that copy
        '''
        children = []
        for move in self.board.move_generation( self.turn ):
            temp = deepcopy( self )
            temp.make_turn( move[0] , move[1] )
            children.append( temp )

        return children


    def eval_func( self ):
        ''' Returns a numerical value of the 'goodness' of a given game state

            Notes:
            Only setup for Black, as in Black win is the highest number
        '''
        if ( self.winner == WHITE ):
            return float('-1000')
        elif ( self.winner == BLACK ):
            return float('1000')

        else:
            eval = self.black_player.lives - self.white_player.lives
            eval += self.centerness_eval() / 10
            return eval

    def centerness_eval( self ):
        black_dist = 0
        white_dist = 0
        center = self.board.center

        for hex in self:
            if( hex.val == BLACK ):
                black_dist += hex.axial_coord.distance( center )

            if( hex.val == WHITE ):
                white_dist += hex.axial_coord.distance( center )

        return 1 / black_dist - white_dist / 100

    def minimax( self , depth , alpha , beta , maximizing_player = True ): #AI AI AI
        if( depth == 0 or self.winner == WHITE or self.winner == BLACK ):
            return self.eval_func() , self.history[-1]

        if maximizing_player:
            maxEval = float('-inf')
            best_move = []
            for move in self.board.move_generation( self.turn ):
                #handle something that is going wrong in move generation/making/undoing lol
                outcome = self.make_turn( move[0] , move[1] )
                if( outcome == 'bleh' ):
                    continue
                eval, _ = self.minimax( depth - 1 , alpha , beta , False )
                if( eval > maxEval ):
                    maxEval = eval
                    best_move = self.history[-1]
                    alpha = max( alpha, maxEval)
                    if beta <= alpha:
                        self.undo_last_turn()
                        break
                self.undo_last_turn()

            return maxEval, best_move

        else:
            minEval = float('inf')
            worst_move = []
            for move in self.board.move_generation( self.turn ):
                #handle something that is going wrong in move generation/making/undoing lol
                outcome = self.make_turn( move[0] , move[1] )
                if( outcome == 'bleh'):
                    continue
                eval, _ = self.minimax( depth - 1 , alpha , beta , True )
                if( eval < minEval ):
                    minEval = eval
                    worst_move = self.history[-1]
                    beta = min( beta, minEval)
                    if beta <= alpha:
                        self.undo_last_turn()
                        break
                self.undo_last_turn()
            return minEval, worst_move


    # def minimax( self , depth , alpha , beta , maximizing_player = True ): #AI AI AI
    #
    #     if( depth == 0 or self.winner == WHITE or self.winner == BLACK ):
    #         return self.eval_func() , self
    #     if( depth == 3):
    #         for move in self.history:
    #             print( move )
    #
    #         print('\n')
    #     if maximizing_player:
    #         maxEval = float('-inf')
    #         best_move = []
    #         for move in self.board.move_generation( self.turn ):
    #             self.make_turn( move[0] , move[1] )
    #             eval , _ = self.minimax( depth - 1 , alpha , beta , False )
    #             if( eval > maxEval ):
    #                 maxEval = eval
    #                 best_move = self.history[-1]
    #                 alpha = max( alpha, maxEval)
    #                 if beta <= alpha:
    #                     self.undo_last_turn()
    #                     break
    #             self.undo_last_turn()
    #         return maxEval, best_move
    #
    #
    #         # for child in self.children_generator():
    #         #     eval , _ = child.minimax( depth - 1 , alpha , beta , False )
    #         #     if( eval > maxEval ):
    #         #         maxEval = eval
    #         #         best_move = child.history[-1]
    #         #         alpha = max( alpha, maxEval)
    #         #         if beta <= alpha:
    #         #             break
    #         # return maxEval, best_move
    #
    #     else:
    #         minEval = float('inf')
    #         worst_move = []
    #
    #         # for child in self.children_generator():
    #         #     eval, _ = child.minimax( depth - 1 , alpha , beta , True )
    #         #     if( eval < minEval ):
    #         #         minEval = eval
    #         #         worst_move = child.history[-1]
    #         #         beta = min( beta, minEval)
    #         #         if beta <= alpha:
    #         #             break
    #         # return minEval, worst_move
    #
    #         #pseudo-code for alternative, when using undo move
    #         for move in self.board.move_generation( self.turn ):
    #             self.make_turn( move[0] , move[1] )
    #             eval, _ = self.minimax( depth - 1 , alpha , beta , True )
    #             if( eval < minEval ):
    #                 minEval = eval
    #                 worst_move = self.history[-1]
    #                 beta = min( beta, minEval)
    #                 if beta <= alpha:
    #                     self.undo_last_turn()
    #                     break
    #             self.undo_last_turn()
    #         return minEval, worst_move
