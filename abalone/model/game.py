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


    def __init__( self , size , two_player = True , depth = 1 ):
        self.size = size

        self.board = board.AbaloneBoard( self.size )
        self.add_pieces()

        self.lives = self.lives[ self.size ]
        if two_player:
            self.white_player = self.Player( WHITE , self.lives)
            self.black_player = self.Player( BLACK , self.lives)

        else:
            self.white_player = self.Player( WHITE , self.lives)
            self.black_player = self.AI( BLACK , self.lives , depth )

        self.winner = 0

        self.turn = BLACK
        self.two_player = two_player
        self.check_for_AI_move()
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
        if( self.winner == 0  ):
            for coord in coords_from:
                if( self.board[ coord ] is None or self.board[ coord ].val != self.turn ):
                    return 'Error wrong player'

            move_type = self.board.direction_move( coords_from, direction )
            if( move_type == self.board.POINT ):
                self.change_player()
                self.lose_piece()
                self.last_move = [ coords_from , direction , move_type ]

            elif( move_type ):
                self.change_player()
                self.last_move = [ coords_from , direction , move_type ]

            else:
                return 'Illegal Move try again'

            self.check_winner()


    def check_for_AI_move( self ):
        if( self.turn == BLACK and self.two_player == False ):
            time.sleep( .5 )
            self.AI_move()


    def AI_move( self ):
        # moves = self.board.move_generation( self.turn )
        #
        # rand_move = random.randint( 0 , len( moves ) - 1 )
        # move = moves[ rand_move ]
        #
        # self.make_turn( move[0] , move[1] )

        move = self.minimax( self.black_player.depth )


        move = move[1]
        self.make_turn( move.last_move[0] , move.last_move[1] )

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


    def centerness_eval( self ):
        #change is distance to center
        center = self.board.center
        pre_distance_to_center = 0
        post_distance_to_center = 0
        move = self.last_move

        for piece in move[0]:
            pre_distance_to_center += piece.distance( center )

        for piece in move[0]:
            piece_post = piece + move[1]
            post_distance_to_center += piece_post.distance( center )

        change_in_dist = pre_distance_to_center - post_distance_to_center

        if( self.board[ move[0][0] + self.last_move[1] ].val == BLACK ):
            return change_in_dist
        else:
            return -change_in_dist


    def minimax( self , depth , maximizing_player = True ): #AI AI AI
        if( depth == 0 or self.winner == WHITE or self.winner == BLACK ):
            return self.eval_func() , None

        if maximizing_player:
            maxEval = float('-inf')
            best_board = 0

            for child in self.children_generator():
                eval , _ = child.minimax( depth - 1 , False )
                if( eval > maxEval ):
                    maxEval = eval
                    best_board = child
            return maxEval, best_board

        else:
            minEval = float('inf')
            worst_board = 0

            for child in self.children_generator():
                eval, _ = child.minimax( depth - 1 , True )
                if( eval < minEval ):
                    minEval = eval
                    worst_board = child
            return minEval, worst_board


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






if __name__ == '__main__':
    test = Game( 3 )

    for child in test.children_generator():
        print( child )
