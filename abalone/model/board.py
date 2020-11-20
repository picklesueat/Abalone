from collections import namedtuple
from typing import List
from abalone import BLACK, WHITE, EMPTY

cube_coord = namedtuple('coord', ['x','y','z'])

class axial_coord():
    ''' Represents an Axial Coordinate, a way of describing a Hexagonal Coordinate System

        Notes:
        Although x is similar to the rectangular coordinate system we all know and love
        y is at a 45 degree angle to x.
        Axial Coordinates work well for easily thinking about positions on a hexagonal grid, but Cube coordinates make
        calculating algorithms easier

        Attributes
        ----------
        x -- the x value of the coordinate
        y -- the y value of the coordinate
        '''
    def __init__( self, x , y ):
        self.x = x
        self.y = y

    def axial_to_cube( self ):
        return cube_coord( self.x , self.y , -self.x - self.y )

    def distance( self, other ):
        cube_coords_from = self.axial_to_cube()
        cube_coords_to = other.axial_to_cube()

        return max( abs( cube_coords_from.x - cube_coords_to.x ), abs( cube_coords_from.y - cube_coords_to.y ) , abs( cube_coords_from.z - cube_coords_to.z) )

    def __str__( self ):
        return 'axial: ' + '({} , {})'.format( self.x, self.y )

    def __repr__( self ):
        return 'axial: ' + '({} , {})'.format( self.x, self.y )

    def __eq__( self , other ):
        return ( self.x , self.y ) == ( other.x , other.y )

    def __add__( self , other ):
        return axial_coord( self.x + other.x , self.y + other.y)

    def __sub__( self , other ):
        return axial_coord( self.x - other.x , self.y - other.y)

    def inverse( self ):
        return axial_coord( self.x * -1 , self.y * -1 )



class Hex():
    ''' Hex placed on Grid spots, controls movements across Hexagonal Grid by pre-computing neighbors
    '''
    def __init__( self, x_pos, y_pos, val = EMPTY ):
        self.axial_coord = axial_coord( x_pos, y_pos )
        self.cube_coord = cube_coord( x_pos, y_pos, -x_pos - y_pos )
        self.possible_neighbors = self.get_neigh_coords( self.axial_coord )
        self.half_neighbors = self.get_half_neigh_coords( self.axial_coord )
        self.val = val


    @staticmethod
    def get_neigh_coords( axial_coords ) -> List[axial_coord]:
        x,y  = axial_coords.x, axial_coords.y
        neighbors = []
        neighbors.append( axial_coord( x+1, y) )
        neighbors.append( axial_coord( x, y+1) )
        neighbors.append( axial_coord( x-1, y+1) )
        neighbors.append( axial_coord( x-1, y) )
        neighbors.append( axial_coord( x, y-1) )
        neighbors.append( axial_coord( x+1, y-1) )
        return neighbors

    @staticmethod
    def get_half_neigh_coords( axial_coords ):
        x,y  = axial_coords.x, axial_coords.y
        neighbors = []
        neighbors.append( axial_coord( x+1, y) )
        neighbors.append( axial_coord( x, y+1) )
        neighbors.append( axial_coord( x-1, y+1) )

        return neighbors

    def __str__( self ):
        return str( self.val )

    def __repr__( self ):
        return "Hex({},{},{})".format( self.axial_coord.x , self.axial_coord.y , self.val )


class Grid():
    '''Forms a grid (2-d list) to store data, with a border of None's that is not directly accesible

        None None None None None
        None  0    0     0  None
        None  1    2     3  None
        None  4    5     6  None
        None None None None None

        >>> grid[axial_coords(2,1)]
        3
    '''

    def __init__( self, size):
        self.size = size
        self._grid =   [[None for row in range(size + 2 )] for col in range(size + 2)]

    def __getitem__( self, coords: axial_coord ):
        return self._grid[coords.y + 1 ][coords.x + 1 ]

    def __setitem__( self, coords : axial_coord , val : int ) -> None:
        self._grid[coords.y + 1 ][coords.x + 1 ] = val

    def __len__( self ):
        return self.size

    def __iter__( self ):
        return Grid.GridIterator( self )

    class GridIterator():
        def __init__( self , grid ):
            self.grid = grid
            self.size = grid.size
            self.cur_row = 0
            self.cur_col = 0

        def __iter__( self ):
            return self

        def __next__( self ):
            if( self.cur_col  == self.size ):
                self.cur_row += 1
                self.cur_col = 0

            if( self.cur_row == self.size ):
                raise StopIteration


            coord = axial_coord( self.cur_col , self.cur_row )

            self.cur_col += 1
            return self.grid[ coord ]

class HexShapedBoard():
    ''' Hexagonal shaped group of Hexagons

        None None None None None
        None None  0     0  None
        None  1    2     3  None
        None  4    5   None None
        None None None None None


    '''
    def __init__( self, size ):
        self.size = size  #distance from center to outermost hexs of regular hexagon
        self.center = axial_coord( self.size - 1 , self.size - 1  )
        self.layout = self.make_layout()
        self.initialize_neighbors()


    def make_layout( self ) -> Grid:
        ''' Returns a Grid objects with Hexs objects forming a Hexagonal Shape.'''

        grid_dist = self.size * 2 - 1
        empty_layout = Grid( grid_dist )

        for i in range( grid_dist ):
            for j in range( grid_dist ):
                coord = axial_coord( i , j )
                if( coord.distance( self.center ) < self.size):
                    empty_layout[ coord ] = Hex( i , j )

        return empty_layout

    def initialize_neighbors( self ):
        ''' Removes all None neighbors for each Hex in the board '''
        ind_neigh_to_remove = []
        for hex in self:
            for ind_neighbor in range( len( hex.possible_neighbors) ):
                if self[ hex.possible_neighbors[ind_neighbor] ] is None:
                    ind_neigh_to_remove.append( ind_neighbor )

            ind_neigh_to_remove.reverse()
            for i in ind_neigh_to_remove:
                del hex.possible_neighbors[i]

            ind_neigh_to_remove = []

        ind_neigh_to_remove = []
        for hex in self:
            for ind_neighbor in range ( len( hex.half_neighbors)):
                if( hex.half_neighbors[ ind_neighbor ] not in hex.possible_neighbors ):
                    ind_neigh_to_remove.append( ind_neighbor )

            ind_neigh_to_remove.reverse()
            for i in ind_neigh_to_remove:
                del hex.half_neighbors[i]

            ind_neigh_to_remove = []

    def __iter__( self ):
        return HexShapedBoard.HexBoardIterator( self.layout )

        # DOESNT WORK, I must be misunderstanding generators
        # board = iter( self.layout )
        #
        # def piece_generator():
        #     next_piece = next( board )
        #     while next_piece is None:
        #         next_piece = next( board )
        #         print('yee')
        #     yield next_piece
        #
        # return piece_generator()

    def __len__( self ):
        return self.size

    def __getitem__( self, coords  ):
        return self.layout[ coords ]

    def __setitem__( self, coords, val ):
        self.layout[ coords ].val = val

    def __str__( self ):
        '''
                      0  0
                    1  2  3
                     4  5
        '''
        prt = ''
        row_count = 1

        for i in range( self.size * 2 - 1):
            for j in range( self.size * 2 - 1):
                prt += str( self[ axial_coord( j , i ) ] ) + '     '
            prt += '\n'
            prt += '    ' * ( row_count)
            row_count +=1

        return prt


    class HexBoardIterator():
        ''' Only iterates over non-None values in the Grid
        '''
        def __init__( self, Grid ):
            self.Grid_iter = iter( Grid )
            self.cur_row = 0
            self.cur_col = 0

        def __iter__( self ):
            return self

        def __next__( self ):
            next_hex = next( self.Grid_iter )

            while ( next_hex is None ):
                next_hex = next( self.Grid_iter )

            return next_hex

class AbaloneBoard( HexShapedBoard ):
    '''Adds Abalone Rules to the HexShapedBoard

        Methods
        --------
              Broadside move --

                    0 0
                   1 1 0
                    0 0

                    to

                    1 1
                   0 0 0
                    0 0


             Inline move --

                    0 0
                   1 1 2
                    0 0

                    to

                    0 0
                   0 1 1
                    0 0

            Attributes
            ----------
            INVALID - unable to make move under any of Abalone Rules
            VALID - move made, only effects pieces in moved and has no side effects
            PUSH - move made, also pushes pieces according to Abalone Rules, doesn't change the number of pieces on the board
            POINT -move made, also pushes pieces according to Abalone Rules, changes number of pieces on the board

    '''

    #Move Types
    INVALID = 0
    VALID = 1
    PUSH  = 2
    POINT = 3

    @staticmethod
    def is_valid_direction( direction : axial_coord ):
        ''' Returns validity of direction
        '''
        if not max( direction.x ,  direction.y ) <= 1:
            return False
        if not min( direction.x , direction.y ) >= -1:
            return False
        if not -2 < direction.x + direction.y < 2:
            return False

        return True

    def is_valid_neighbor( self , coord_from , coord_to ) -> bool:
        return (coord_to) in self[ coord_from ].possible_neighbors

    def is_empty_neighbor( self , coord_from , coord_to ):
        return ( (coord_to) in self[ coord_from ].possible_neighbors ) and ( self[ coord_to ].val == EMPTY )

    def is_valid_one_piece_move( self , coord_from , coord_to ):
        if( self.is_empty_neighbor( coord_from , coord_to ) ):
            return AbaloneBoard.VALID
        return AbaloneBoard.INVALID

    def make_one_piece_move( self , coord_from , coord_to ):
        temp_val = self[ coord_from ].val
        self[ coord_from ] = self[ coord_to ].val
        self[ coord_to ] = temp_val


    def is_in_row( self , coords: list ):
        '''Returns True if the list of coords is in a row, and of the same type
        '''
        direction = coords[ 0 ] - coords[ 1 ]

        for i in range( len(coords) - 1 ):
            if( (coords[i] - coords[ i + 1 ] ) != direction ):  #same direction
                return False

            if(self[ coords[ i ] ].val != self[ coords[ i+1 ] ].val): #same color
                return False

            if( not self.is_valid_neighbor( coords[i] , coords[ i+1 ] ) ): #neighbors
                return False

        return True

    def is_valid_broadside_move( self , coords_from: list , direction: axial_coord ):
        all_moves_valid = True
        for coord in coords_from:
            if( not ( self.is_empty_neighbor( coord, ( coord + direction ) ) ) ):
                all_moves_valid = False
                break


            if( not (self[ coord ].val == WHITE or self[ coord ].val == BLACK) ):
                all_moves_valid = False
                break


            if( not (self[ ( coord + direction ) ].val == EMPTY) ):
                all_moves_valid = False
                break

        if all_moves_valid :
            return AbaloneBoard.VALID
        return AbaloneBoard.INVALID


    def make_broadside_move( self , coords_from: list , direction: axial_coord ):
        for coord_from in coords_from:
            coord_to = ( coord_from + direction )

            temp_val = self[ coord_from ].val
            self[ coord_from ] = self[ coord_to ].val
            self[ coord_to ] = temp_val

    def is_valid_push_move( self , coords_from , direction ):
        coord_to = ( coords_from[0] + direction ) #had to do this to avoid UnBoundLocalError, which I understand but don't really know why it exists
        coord_to_val = self[ coord_to ].val

        push_count = 1
        if( coord_to_val == BLACK ):
            coord_from_val = WHITE

        else:
            coord_from_val = BLACK

        while push_count < max(2, len( coords_from ) ):
            coord_to = ( coord_to + direction )  #referencing variable in one frame up, is this good practice?

            if( self[ coord_to ] is None ):
                return AbaloneBoard.POINT


            if( self[ coord_to ].val == coord_to_val ):
                push_count += 1

            if( self[ coord_to ].val == EMPTY ):
                return AbaloneBoard.PUSH * push_count

            if ( self[ coord_to ].val == coord_from_val ):
                return AbaloneBoard.INVALID

        return AbaloneBoard.INVALID

    def make_push_move( self , coords_from , direction ):
        coord_to = ( coords_from[0] + direction ) #had to do this to avoid UnBoundLocalError, which I understand but don't really know why it exists
        coord_to_val = self[ coord_to ].val

        push_count = 1
        if( coord_to_val == BLACK ):
            coord_from_val = WHITE
        else:
            coord_from_val = BLACK
        while push_count < max(2, len( coords_from ) ):
            coord_to = ( coord_to + direction )  #referencing variable in one frame up, is this good practice?
            if( self[ coord_to ] is None ):
                #we need to get back on the board
                coord_to = coord_to - direction
                for i in range( push_count + len(coords_from) - 1 ):
                    prev_coord = coord_to - direction
                    temp_val = self[ prev_coord ].val
                    self[ coord_to ] = temp_val
                    coord_to = prev_coord
                self[ prev_coord ] = EMPTY
                break
            if( self[ coord_to ].val == coord_to_val ):
                push_count += 1
            if( self[ coord_to ].val == EMPTY ):
                for i in range( push_count + 1 ):
                    self.direction_move( [ ( coord_to - direction ) ] , direction )
                    coord_to = ( coord_to - direction )
                for coord in coords_from:
                    self.direction_move( [coord] , direction )
                break
            if ( self[ coord_to ].val == coord_from_val ):
                break

    def is_valid_move( self , coords_from: list, direction: axial_coord ):
        if not self.is_valid_direction( direction ):
            return AbaloneBoard.INVALID

        num_pieces_to_move = len( coords_from )

        if num_pieces_to_move == 1 :
            coord_from = coords_from[0]
            coord_to = coord_from + direction
            return self.is_valid_one_piece_move( coord_from , coord_to )

        if 2 <= num_pieces_to_move <= 3:
            if self.is_in_row( coords_from ):
                if( direction.inverse() == ( coords_from[0] - coords_from[1] ) ):
                    coords_from.reverse()

                if( direction == ( coords_from[0] - coords_from[1] ) ):
                    coord_to = ( coords_from[0] + direction )
                    if( self[ coord_to ] is None ):
                        return AbaloneBoard.INVALID

                    if( self[ coord_to ].val == EMPTY  ):
                        return AbaloneBoard.VALID

                    #defines a 'push' move
                    elif( self[ coord_to ].val != self[ coords_from[ 0 ] ].val ):

                        return self.is_valid_push_move( coords_from , direction )

                #broadside move
                else:
                    return self.is_valid_broadside_move( coords_from , direction )

    def make_move( self, coords_from: list, direction: axial_coord  ): #assumes the move has already been validated
        num_pieces_to_move = len( coords_from )
        if ( num_pieces_to_move == 1 ):
            coord_from = coords_from[0]
            coord_to = coord_from + direction
            self.make_one_piece_move( coord_from , coord_to )

        elif ( 2 <= num_pieces_to_move <= 3  ):
            if( direction.inverse() == ( coords_from[0] - coords_from[1] ) ):
                coords_from.reverse()

            if( direction == ( coords_from[0] - coords_from[1] ) ):
                coord_to = ( coords_from[0] + direction )
                if( self[ coord_to ].val == EMPTY  ):
                    for coord in coords_from:
                        self.make_move( [coord] , direction )

                else:
                    self.make_push_move( coords_from , direction )

            else:
                self.make_broadside_move( coords_from , direction )


    def direction_move( self, coords_from: List[axial_coord], direction: axial_coord ):
        ''' Moves pieces in specified direction according to the Abalone Rules.

            Notes:
            Uses all previous methods in this class.
        '''
        move_type = self.is_valid_move( coords_from , direction )
        if( move_type ):
            self.make_move( coords_from , direction )

        return move_type

    def get_piece_formations( self , player ):
        ''' Gets all different combinations of pieces that could be moved

            Notes:
            Uses 'half-neighbors' so as not to double count, moves from top left to bottom right.
        '''
        piece_formations = []

        for hex in self:
            if ( hex.val == player ):
                piece_formations.append( [hex.axial_coord] )
                for neigh in hex.half_neighbors:
                    if ( self[ neigh ].val == player):
                        piece_formations.append( [hex.axial_coord , neigh ] )
                        neigh_2 = (neigh - hex.axial_coord) + neigh
                        if( self[ neigh_2 ] is not None ):
                            if ( self[ neigh_2 ].val == player):
                                piece_formations.append( [hex.axial_coord , neigh , neigh_2 ] )
        return piece_formations

    def all_moves( self , coords_from: list ):
        all_direction_moves = []
        directions = [ axial_coord( 1 , 0 ) , axial_coord( -1 , 0 ) , axial_coord( 0 , 1 ) , axial_coord( 0 , -1 ) , axial_coord( 1 , -1 ) , axial_coord( -1 , 1 ) ]
        for direction in directions:
            move_type = self.is_valid_move( coords_from , direction)
            if( move_type ):
                    all_direction_moves.append( [ coords_from , direction , move_type ]  )
        return all_direction_moves

    def move_generation( self , player ):
        piece_formations = self.get_piece_formations( player )
        move_list = []
        for group in piece_formations:
            move_list.extend( self.all_moves( group ) )
        return move_list

    def undo_move( self , coords_from , direction , move_type ):
        def simple_move_undo():
            new_coords_from = []
            for i in range( len(coords_from )):
                new_coords_from.append(coords_from[i] + direction)

            new_direction = direction.inverse()
            self.make_move( new_coords_from , new_direction)

        simple_move_undo()

        new_direction = direction.inverse()



        if move_type == self.POINT:
            if( self[ coords_from[0] ].val == WHITE ):
                push_val = BLACK
            else:
                push_val = WHITE

            if( coords_from[0] + direction != coords_from[1] ):
                next_hex_inline = coords_from[0] + direction
            else:
                next_hex_inline = coords_from[-1] + direction

            for _ in range( len( coords_from ) - 1 ):
                next_hex_inline = next_hex_inline + direction

                if( self[ next_hex_inline ] is None ):
                    self[ next_hex_inline + new_direction ] = push_val
                    break
                elif( self[ next_hex_inline ].val == push_val ):
                    self.make_move( [next_hex_inline] , new_direction )

                else:
                    break

        # need an identifier of how many pieces were pushed
        elif move_type % 2 == 0:
            if( self[ coords_from[0] ].val == WHITE ):
                push_val = BLACK
            else:
                push_val = WHITE

            if( coords_from[0] + direction != coords_from[1] ):
                next_hex_inline = coords_from[0] + direction
            else:
                next_hex_inline = coords_from[-1] + direction


            for _ in range( move_type // 2 ):
                next_hex_inline = next_hex_inline + direction
                if( self[ next_hex_inline ] is None ):
                    break

                elif( self[ next_hex_inline ].val == push_val ):
                    self.make_move( [next_hex_inline] , new_direction )

                else:
                    break


        #
        # if not self.is_valid_direction( direction ):
        #     return AbaloneBoard.INVALID
        #
        # num_pieces_to_move = len( coords_from )
        #
        # #one_piece_move
        # if ( num_pieces_to_move == 1 ):
        #     coord_from = coords_from[0]
        #     coord_to = coord_from + direction
        #
        #     outcome = self.is_valid_one_piece_move( coord_from , coord_to )
        #
        #     if( outcome ):
        #         self.make_one_piece_move( coord_from , coord_to )
        #
        #     return outcome
        #
        #
        # elif ( 2 <= num_pieces_to_move <= 3  ):
        #     #they must be in a 'row' for any other movetype
        #     if self.is_in_row( coords_from ):
        #         if( direction.inverse() == ( coords_from[0] - coords_from[1] ) ):
        #             coords_from.reverse()
        #
        #
        #         #if the move direction and row direction are the same it must be an inline move (technically subset)
        #         if( direction == ( coords_from[0] - coords_from[1] ) ):
        #             coord_to = ( coords_from[0] + direction )
        #             if( self[ coord_to ] is None ):
        #                 return AbaloneBoard.INVALID
        #
        #             coord_to_val = self[ coord_to ].val
        #
        #             if( coord_to_val == EMPTY  ):
        #                 for coord in coords_from:
        #                     self.make_move( [coord] , direction )
        #                 return AbaloneBoard.VALID
        #
        #             #defines a 'push' move
        #             elif( coord_to_val != self[ coords_from[ 0 ] ].val ):
        #
        #                 push_outcome = self.is_valid_push_move( coords_from , direction )
        #
        #                 if( push_outcome ):
        #                     self.make_push_move( coords_from , direction )
        #                 return push_outcome
        #
        #
        #         #broadside move
        #         else:
        #             outcome = self.is_valid_broadside_move( coords_from , direction )
        #             if outcome:
        #                 self.make_broadside_move( coords_from , direction )
        #             return outcome
