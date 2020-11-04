import sys
import time
import pygame

import random

sys.path.insert(1, "/home/picklesueat/Python_projects/Abalone/Model/")
sys.path.insert(1, "/home/picklesueat/Python_projects/Abalone/View/")

import test
#import view
import board
from board import axial_coord
from game import Game
from math import sqrt
import copy
import settings

#I think the model is leaking
class Controller():
    def __init__( self , size, two_player = True ):
        self.size = size
        self.game = Game( self.size, two_player )
        self.prev_click_coords = []
        self.updated = False

    def is_valid_click( self, coord ):
        return self.game[ coord ] is not None

    def is_first_click( self ):
        return not self.prev_click_coords

    def take_first_click( self, coord: axial_coord ):  #too many return values
        if( self.game[ coord ].val == self.game.turn ):
            self.prev_click_coords.append( coord )
            return True

    def take_click( self , coord: axial_coord ):
        #'grab' another piece
        if( self.game[ coord ].val == self.game.turn and (len(self.prev_click_coords) + 1 < 4) ):
            self.prev_click_coords.append( coord )

        #direction to move
        else:
            direction =  (self.prev_click_coords[0] - coord).inverse()
            self.game.make_turn( self.prev_click_coords , direction )
            self.prev_click_coords = []
            self.updated = True


    def get_best_move( self , depth ):
        self.game =  self.game.minimax( depth )[1]






        # for move in moves:
        #     if( move[2] == board.AbaloneBoard.POINT ):
        #         self.game.make_turn( move[ 0 ] , move[ 1 ] )
        #         return None
        #
        #     pre_distance_to_center = 0
        #     post_distance_to_center = 0
        #
        #     for piece in move[0]:
        #         pre_distance_to_center += piece.distance( center )
        #
        #     pre_distance_to_center = pre_distance_to_center  / len( move[ 0 ] )
        #
        #     for piece in move[0]:
        #         piece_post = piece + move[1]
        #         post_distance_to_center += piece_post.distance( center )
        #
        #     post_distance_to_center = post_distance_to_center  / len( move[ 0 ] )
        #
        #
        #     move_vals.append( (pre_distance_to_center - post_distance_to_center, len( move[ 0 ] ) ) )
        #
        #
        # best_move_index = move_vals.index( max( move_vals ) )
        #
        # best_move = moves[ best_move_index ]
        #
        # self.game.make_turn( best_move[ 0 ] , best_move[ 1 ] )
