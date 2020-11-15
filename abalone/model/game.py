from abalone import BLACK, WHITE, EMPTY
from . import board
from .board import axial_coord
from copy import deepcopy
import random
import time



class Game():
    WHITE = WHITE
    BLACK = BLACK
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
        self.winner = 0

        self.turn = BLACK
        self.last_move = None


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

            self.board[ axial_coord( 0, 6)] = BLACK
            self.board[ axial_coord( 1, 6)] = BLACK
            self.board[ axial_coord( 2, 6)] = BLACK
            self.board[ axial_coord( 3, 6)] = BLACK

            self.board[ axial_coord( 1, 5)] = BLACK
            self.board[ axial_coord( 2, 5)] = BLACK
            self.board[ axial_coord( 3, 5)] = BLACK

    def change_player( self ):
        if( self.turn == BLACK ):
            self.turn = WHITE

        else:
            self.turn = BLACK

    def lose_piece( self ):
        if( self.turn == BLACK ):
            self.black_player.lives = self.black_player.lives - 1

        else:
            self.white_player.lives = self.white_player.lives - 1

    def check_winner( self ):
        if( self.white_player.lives == 0 ):
            self.winner = BLACK

        if( self.black_player.lives == 0 ):
            self.winner = WHITE

    def make_turn( self , coords_from: list , direction: axial_coord ):
        if( self.winner == EMPTY  ):
            for coord in coords_from:
                if( self.board[ coord ] is None or self.board[ coord ].val != self.turn ):
                    return None

            move_type = self.board.direction_move( coords_from, direction )
            if( move_type == self.board.POINT ):
                self.change_player()
                self.lose_piece()
                self.last_move = [ coords_from , direction , move_type ]

            elif( move_type ):
                self.change_player()
                self.last_move = [ coords_from , direction , move_type ]

            else:
                return None


            self.check_winner()



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
    def __init__( self , size ):
        super().__init__( size )

        self.white_player = self.Player( WHITE , self.lives)
        self.black_player = self.Player( BLACK , self.lives)

        self.turn = BLACK



class PlayerVSAIGame( Game ):
    def __init__( self , size , depth = 1):
        super().__init__( size )

        self.white_player = self.Player( WHITE , self.lives)
        self.black_player = super().AI( BLACK , self.lives , depth )

        self.turn = BLACK

        self.make_AI_turn()


    def make_AI_turn( self ):
        if( self.turn != BLACK ):
            return None

        move = self.minimax( self.black_player.depth , float('-inf') , float('inf') )

        move = move[1]
        self.make_turn( move[0] , move[1] )

        return True

    def children_generator( self ):
        children = []
        for move in self.board.move_generation( self.turn ):
            temp = deepcopy( self )
            temp.make_turn( move[0] , move[1] )
            children.append( temp )

        return children

    def eval_func( self ):
        if ( self.winner == WHITE ):
            return float('-1000')
        elif ( self.winner == BLACK ):
            return float('1000')

        else:
            eval = self.black_player.lives - self.white_player.lives
            eval += self.centerness_eval() / 10
            return eval

    #sooo slow
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
            return self.eval_func() , self

        if maximizing_player:
            maxEval = float('-inf')
            best_move = []

            for child in self.children_generator():
                eval , _ = child.minimax( depth - 1 , alpha , beta , False )
                if( eval > maxEval ):
                    maxEval = eval
                    best_move = child.last_move
                    alpha = max( alpha, maxEval)
                    if beta <= alpha:
                        break
            return maxEval, best_move

        else:
            minEval = float('inf')
            worst_move = []

            for child in self.children_generator():
                eval, _ = child.minimax( depth - 1 , alpha , beta , True )
                if( eval < minEval ):
                    minEval = eval
                    worst_move = child.last_move
                    beta = min( beta, minEval)
                    if beta <= alpha:
                        break
            return minEval, worst_move
