from abalone.model.board import axial_coord
from abalone.model.game import TwoPlayerGame , PlayerVSAIGame
from math import sqrt


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
        '''Ensures the coord is on the board '''
        x_valid = coord.x >= 0 and coord.x < self.size * 2 - 1
        y_valid = coord.y >= 0 and coord.y < self.size * 2 - 1
        if( x_valid and y_valid ):
            return self.game[ coord ] is not None

    def take_click( self , coord: axial_coord ):
        ''' Adds the piece to the pieces 'in hand'
        '''
        if( not self.is_valid_click( coord ) ):
            return None

        if( self.game[ coord ].val == self.game.turn and (len(self.prev_click_coords) + 1 < 4) ):
            self.prev_click_coords.append( coord )

        else:
            if( self.prev_click_coords ):
                direction =  (self.prev_click_coords[0] - coord).inverse()
                self.game.make_turn( self.prev_click_coords , direction )
                self.prev_click_coords = []
                self.updated = True

    def check_winner( self ):
        return self.game.winner

    def check_for_AI_move( self ):
        ''' Checks if AI move can be made and makes it
        '''
        if( self.two_player == False ):
            if self.game.make_AI_turn():
                self.updated = True

    def undo_move( self ):
        if self.two_player:
            self.game.undo_last_turn()
        else:
            self.game.undo_last_turn()
            self.game.undo_last_turn()
