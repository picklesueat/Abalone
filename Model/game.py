import board
from board import axial_coord


class Game():
    WHITE = 2
    BLACK = 1
    lives = {2: 1,
            3:2,
            4:4,
            5:6
    }

    class Player():
        def __init__( self , color , lives , pieces ):
            self.color = color
            self.lives = lives
            self.pieces = pieces


    def __init__( self , size , two_player = True ):
        self.size = size

        self.board = board.AbaloneBoard( self.size )
        self.add_pieces()

        self.lives = self.lives[ self.size ]
        pieces = 0
        self.white_player = self.Player( Game.WHITE , self.lives , pieces )
        self.black_player = self.Player( Game.BLACK , self.lives , pieces )

        self.status = 1

        self.turn = Game.BLACK
        self.two_player = two_player




    def add_pieces( self ):
        for hex in self.board:
            if( hex.axial_coord.y == 0 ):
                hex.val = Game.WHITE

            if( hex.axial_coord.y == self.size * 2 - 1 - 1 ):
                hex.val = Game.BLACK

        if( self.size == 3 ):
            self.board[ axial_coord( 2, 1)] = Game.WHITE
            self.board[ axial_coord( 3, 1)] = Game.WHITE

            self.board[ axial_coord( 2, 3)] = Game.BLACK
            self.board[ axial_coord( 1, 3)] = Game.BLACK


    def change_player( self ):
        if( self.turn == Game.BLACK ):
            self.turn = Game.WHITE

        else:
            self.turn = Game.BLACK

    def lose_piece( self ):
        if( self.turn == Game.BLACK ):
            self.black_player.pieces = self.black_player.pieces - 1
            self.black_player.lives = self.black_player.lives - 1

        else:
            self.white_player.pieces = self.white_player.pieces - 1
            self.white_player.lives = self.white_player.lives - 1

    def check_winner( self ):
        if( self.white_player.lives == 0 ):
            print(' Black Wins ')
            self.status = 0
            return True

        if( self.black_player.lives == 0 ):
            print(' White Wins ')
            self.status = 0
            return True


    def make_turn( self , coords_from: list , direction: axial_coord ):  #doing this weird shit with return functions
        if( self.status == 1 ):
            for coord in coords_from:
                if( self.board[ coord ] is None or self.board[ coord ].val != self.turn ):
                    return 'Error wrong player'


            move = self.board.direction_move( coords_from, direction )
            if( move == 'point' ):
                self.change_player()
                self.lose_piece()

            elif( move ):
                self.change_player()

            else:
                return 'Illegal Move try again'

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
