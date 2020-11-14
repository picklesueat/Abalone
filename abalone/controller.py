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
        self.two_player = two_player

    def is_valid_click( self, coord ):
        return self.game[ coord ] is not None

    def take_click( self , coord: axial_coord ):
        #'grab' another piece
        if( not self.is_valid_click( coord ) ):
            return None



        if( self.game[ coord ].val == self.game.turn and (len(self.prev_click_coords) + 1 < 4) ):
            self.prev_click_coords.append( coord )

        #direction to move
        else:
            if( self.prev_click_coords ):
                direction =  (self.prev_click_coords[0] - coord).inverse()
                self.game.make_turn( self.prev_click_coords , direction )
                self.prev_click_coords = []

                if( self.two_player == False):
                    self.game.make_AI_turn()
