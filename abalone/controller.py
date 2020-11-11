import sys
import time
import pygame

import random

import test
import abalone.model.board
from abalone.model.board import axial_coord
from abalone.model.game import Game
from math import sqrt
import copy


#I think the model is leaking
class Controller():
    def __init__( self , size, two_player = True, depth = 1 ):
        self.size = size
        self.game = Game( self.size, two_player, depth )
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

    def update( self ):
        self.game.check_for_AI_move()
