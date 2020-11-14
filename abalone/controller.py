import sys
import time
import pygame

import random

import test
import abalone.model.board
from abalone.model.board import axial_coord
from abalone.model.game import TwoPlayerGame , PlayerVSAIGame
from math import sqrt
import copy


#I think the model is leaking
class Controller():
    def __init__( self , size, two_player = True, depth = 1 ):
        self.size = size
        if two_player:
            self.game = TwoPlayerGame( self.size )
        else:
            self.game = PlayerVSAIGame( self.size , depth )

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
        print( self.prev_click_coords )
        if( self.game[ coord ].val == self.game.turn and (len(self.prev_click_coords) + 1 < 4) ):
            self.prev_click_coords.append( coord )

        #direction to move
        else:
            direction =  (self.prev_click_coords[0] - coord).inverse()
            self.game.make_turn( self.prev_click_coords , direction )
            self.prev_click_coords = []
            self.updated = True

    # def update( self ):
    #     if( self.game.winner == 0 ):
    #         self.game.check_for_AI_move()
