from collections import namedtuple

cube_coord = namedtuple('coord', ['x','y','z'])



class axial_coord():
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



#Base data structure for storage of any hex grid (grid with hexagonal points)
#stored in rhombus shapes (2-D list)
#wraps square of Nones around board that are only visible from this class, and hidden form getter and setters
class HexGridStorage():
    def __init__( self, size):
        self.size = size
        self._grid =   [[None for row in range(size + 2 )] for col in range(size + 2)]

    def __getitem__( self, coords  ):
        return self._grid[coords.y + 1 ][coords.x + 1 ]

    def __setitem__( self, coords , val ):
        self._grid[coords.y + 1 ][coords.x + 1 ] = val

    def __len__( self ):
        return self.size

    def __iter__( self ):
        return iter( self._grid )

    def __str__( self ):
        prt = ''
        row_count = 1

        for row in self:
            for val in row:
                prt += str( val ) + '     '
            prt += '\n'
            prt += '    ' * ( row_count)
            row_count +=1

        return prt

    def __repr__( self ):
        prt = ''
        for row in self:
            prt += repr(row) + '\n'

        return prt

        #Look up python getters and setters and add here


#hex to be placed on valid board squares, helps precompute values
class Hex():
    def __init__( self, x_pos, y_pos, val = 0 ):
        x_pos
        self.axial_coord = axial_coord( x_pos, y_pos )
        self.cube_coord = cube_coord( x_pos, y_pos, -x_pos - y_pos )
        self.possible_neighbors = self.get_neigh_coords( self.axial_coord )
        self.val = val


    @staticmethod
    def get_neigh_coords( axial_coords ):
        x,y  = axial_coords.x, axial_coords.y
        neighbors = []
        neighbors.append( axial_coord( x-1, y) )
        neighbors.append( axial_coord( x+1, y) )
        neighbors.append( axial_coord( x, y-1) )
        neighbors.append( axial_coord( x, y+1) )
        neighbors.append( axial_coord( x-1, y+1) )
        neighbors.append( axial_coord( x+1, y-1) )
        return neighbors

    def __str__( self ):
        return str( self.val )

    def __repr__( self ):
        return "Hex({},{},{})".format( self.axial_coord.x , self.axial_coord.y , self.val )


#Takes basic hexagonal data structure and builds a hexagon shaped grid out of it, lol lots of hexagons
class HexShapedBoard():
    def __init__( self, size ):
        self.size = size
        self.layout = self.make_layout()
        self.update_neighbors()  #this is weird but I'm not sure where else to put this


    #puts hexs in hexagonal pattern
    def make_layout( self ):
        empty_layout = HexGridStorage( self.size * 2 - 1 )
        center = axial_coord( self.size - 1 , self.size - 1  )

        for i in range( self.size * 2 - 1):
            for j in range( self.size * 2 - 1):
                coord = axial_coord( i , j )
                if( coord.distance( center ) < self.size):
                    empty_layout[ coord ] = Hex( i , j )



        return empty_layout

    def update_neighbors( self ):
        ind_neigh_to_remove = []
        for hex in self:
            for ind_neighbor in range( len( hex.possible_neighbors) ):
                if self[ hex.possible_neighbors[ind_neighbor] ] is None:
                    ind_neigh_to_remove.append( ind_neighbor )

            ind_neigh_to_remove.reverse()
            for i in ind_neigh_to_remove:
                del hex.possible_neighbors[i]

            ind_neigh_to_remove = []


    def __iter__( self ):
        return self.HexBoardIterator( self )

    def __len__( self ):
        return self.size


    def __getitem__( self, coords  ):
        return self.layout[ coords ]

    def __setitem__( self, coords, val ):
        self.layout[ coords ].val = val

    def __str__( self ):
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
        def __init__( self, HexGrid ):
            self.HexGrid = HexGrid
            self.cur_row = 0
            self.cur_col = 0

        def __iter__( self ):
            return self

        def __next__( self ):
            coord = axial_coord( self.cur_col , self.cur_row )
            hex = None

            while hex is None:
                coord = axial_coord( self.cur_col , self.cur_row )
                hex = self.HexGrid[ coord ]
                self.cur_col += 1

                if( self.cur_col == self.HexGrid.size * 2 - 1 ):
                    self.cur_col = 0
                    self.cur_row += 1

                if( self.cur_row == self.HexGrid.size * 2 - 1 ):
                    raise StopIteration


            return hex


#adds pieces and rules for abalone to hex board
class AbaloneBoard( HexShapedBoard ):
    WHITE = 2
    BLACK = 1
    EMPTY = 0


    #only setup for 2 right now
    def add_pieces( self ):
        for hex in self:
            if( hex.axial_coord.y == 0 ):
                hex.val = AbaloneBoard.WHITE

            if( hex.axial_coord.y == self.size * 2 - 1 - 1 ):
                hex.val = AbaloneBoard.BLACK

        if( self.size == 3 ):
            self[ axial_coord( 2, 1)] = AbaloneBoard.WHITE
            self[ axial_coord( 3, 1)] = AbaloneBoard.WHITE

            self[ axial_coord( 2, 3)] = AbaloneBoard.BLACK
            self[ axial_coord( 1, 3)] = AbaloneBoard.BLACK


    def is_valid_neighbor( self , coord_from , coord_to ):
        return (coord_to) in self[ coord_from ].possible_neighbors

    def is_empty_neighbor( self , coord_from , coord_to ):
        return ( (coord_to) in self[ coord_from ].possible_neighbors ) and ( self[ coord_to ].val == 0 )

    def direction_move( self, coords_from: list, direction: axial_coord ):
        def one_piece_move( coord_from , coord_to ):
            if( self.is_empty_neighbor( coord_from , coord_to ) ):
                temp_val = self[ coord_from ].val
                self[ coord_from ] = self[ coord_to ].val
                self[ coord_to ] = temp_val

        def push():
            coord_to = ( coords_from[0] + direction ) #had to do this to avoid UnBoundLocalError, which I understand but don't really know why it exists

            push_count = 1
            if( coord_to_val == AbaloneBoard.BLACK ):
                coord_from_val = AbaloneBoard.WHITE

            else:
                coord_from_val = AbaloneBoard.BLACK

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


                    self[ prev_coord ] = AbaloneBoard.EMPTY

                    break

                if( self[ coord_to ].val == coord_to_val ):
                    push_count += 1

                if( self[ coord_to ].val == AbaloneBoard.EMPTY ):
                    for i in range( push_count + 1 ):
                        self.direction_move( [ ( coord_to - direction ) ] , direction )
                        coord_to = ( coord_to - direction )

                    for coord in coords_from:
                        self.direction_move( [coord] , direction )

                    break


                if ( self[ coord_to ].val == coord_from_val ):
                    break



        def is_in_row( coords: list ):
            direction = coords[ 0 ] - coords[ 1 ]

            #if any of the conditions of false for any pair of neighboring points in the list then the points can't be in a row
            for i in range( len(coords) - 1 ):
                if( (coords[i] - coords[ i + 1 ] ) != direction ):
                    return False

                if(self[ coords[ i ] ].val != self[ coords[ i+1 ] ].val):
                    return False

                if( not self.is_valid_neighbor( coords[i] , coords[ i+1 ] ) ):
                    return False

            return True




        assert max( direction.x ,  direction.y ) <= 1
        assert min( direction.x , direction.y ) >= -1
        assert -2 < direction.x + direction.y < 2

        #one_piece_move
        if ( len( coords_from ) == 1 ):
            coord_from = coords_from[0]
            coord_to = coord_from + direction

            one_piece_move( coord_from, coord_to )


        if ( 2 <= len( coords_from ) <= 3  ):
            #they must be in a 'row' for any other movetype
            if is_in_row( coords_from ):

                #if the move direction and row direction are the same it must be an inline move (technically subset)
                if( direction == ( coords_from[0] - coords_from[1] ) ):
                    coord_to = ( coords_from[0] + direction )
                    coord_to_val = self[ coord_to ].val

                    if( coord_to_val == AbaloneBoard.EMPTY  ):
                        for coord in coords_from:
                            self.direction_move( [coord] , direction )

                    #defines a 'push' move
                    elif( coord_to_val != self[ coords_from[ 0 ] ].val ):
                            push()

                #broadside move
                else:
                    all_moves_valid = True
                    for coord in coords_from:
                        if( not ( self.is_empty_neighbor( coord, ( coord + direction ) ) ) ):
                            all_moves_valid = False
                            break


                        if( not (self[ coord ].val == AbaloneBoard.WHITE or self[ coord ].val == AbaloneBoard.BLACK) ):
                            all_moves_valid = False
                            break


                        if( not (self[ ( coord + direction ) ].val == AbaloneBoard.EMPTY) ):
                            all_moves_valid = False
                            break




                    if( all_moves_valid ):
                        for coord_from in coords_from:
                            coord_to = ( coord_from + direction )

                            temp_val = self[ coord_from ].val
                            self[ coord_from ] = self[ coord_to ].val
                            self[ coord_to ] = temp_val











if __name__ == '__main__':
    test = AbaloneBoard( 3 )
    test.add_pieces()
    #test.update_neighbors()

    # for hex in test:
    #     print( repr(hex) )
    print( repr( test[ axial_coord( 2, 1) ] ) )

    #print( test[ axial_coord( 1 , 0 ) ].possible_neighbors )
    #print( test.is_empty_neighbor( axial_coord( 1 , 0 ) , axial_coord( 1,1) ) )

    #print( axial_coord( 2,0 ) in [axial_coord( 1 , 0 ) , axial_coord( 2 , 0)])

    #print( test[ axial_coord( 2 , 2 )].possible_neighbors )

    # test = AbaloneBoard(3)
    # test.add_pieces()
    #
    # #print(repr( test[ axial_coord( 0 , 3 ) ]) )
    # test.direction_move( [ axial_coord( 0 , 2 ), axial_coord( 0 , 3 ), axial_coord( 0 , 4 ) ], axial_coord( 1, 0 ))
    # #test.direction_move( [ axial_coord( 1 , 2 ), axial_coord( 1 , 3 ), axial_coord( 1 , 4 ) ], axial_coord( 1, 0 ))

    # test.direction_move( [ axial_coord( 2 , 0 ), axial_coord( 3 , 0 ), axial_coord( 4 , 0 ) ], axial_coord( -1, 1 ))
    # test.direction_move( [ axial_coord( 3 , 1 ) ], axial_coord( -1, 1 ))
    #
    #
    # test.direction_move( [ axial_coord( 0 , 4 ), axial_coord( 1 , 4 ), axial_coord( 2 , 4 ) ], axial_coord( 1, -1 ))
    # test.direction_move( [ axial_coord( 2 , 3 ), axial_coord( 3 , 3 ) ], axial_coord( 1, -1 ))
    #
    # # test.direction_move( [ axial_coord( 3 , 2 ), axial_coord( 4 , 2 ) ], axial_coord( -1 , 0 ))
    # test.direction_move( [ axial_coord( 2 , 1 ) ], axial_coord( -1 , 1 ))
    #
    # test.direction_move( [ axial_coord( 3 , 2 ), axial_coord( 4 , 2 ) ], axial_coord( -1, 0 ))
    #
    # test.direction_move( [ axial_coord( 2 , 2 ), axial_coord( 3 , 2 ) ], axial_coord( -1 , 0 ))
    #
    # test.direction_move( [ axial_coord( 1 , 2 ), axial_coord( 2 , 2 ) ], axial_coord( -1 , 0 ))

    #test.direction_move( [ axial_coord( 2 , 2 ), axial_coord( 1 , 2  ), axial_coord( 0 , 2 ) ], axial_coord( 1, 0 ))

    #test.direction_move( [ axial_coord( 3 , 2 ), axial_coord( 2 , 2  ), axial_coord( 1 , 2 ) ], axial_coord( 1, 0 ))

    # test.direction_move( [ axial_coord( 1 , 0 ) ], axial_coord( -1, 1 ))
    # test.direction_move( [ axial_coord( 2 , 0 ) ], axial_coord( -1, 1 ))
    # #test.direction_move( [ axial_coord( 1 , 1 ) ], axial_coord( 1, 0 ))
    #
    # test.direction_move( [ axial_coord( 1 , 1 ) , axial_coord( 0 , 1 ) ], axial_coord( 1, 0 ))
    #
    # test.direction_move( [ axial_coord( 1 , 1 ) , axial_coord( 2 , 1 ) ], axial_coord( 0, -1 ))
    #
    # test.direction_move( [ axial_coord( 1 , 0 ) , axial_coord( 2 , 0 ) ], axial_coord( -1, 1 ))
    #
    # test.direction_move( [ axial_coord( 1 , 2 ) ], axial_coord( 1, -1 ))
    #
    #
    # test.direction_move( [ axial_coord( 1 , 1 ) , axial_coord( 0 , 1 ) ], axial_coord( 1, 0 ))

    print( test )
    # test.direction_move( [ axial_coord( 4 , 0 ) ], axial_coord( -1, 0 ))
    # # test.direction_move( [ axial_coord( 2 , 2 ), axial_coord( 2 , 3 ) ], axial_coord( 0, -1 ))


    #test.direction_move( [ axial_coord( 0 , 5 ), axial_coord( 0 , 6 ) ], axial_coord( 1, -1 ))
    #test.direction_move( [ axial_coord( 0 , 5 ), axial_coord( 0 , 6 ) ], axial_coord( 1, -1 ))

    #test.direction_move( [ axial_coord( 0 , 5 ), axial_coord( 0 , 6 ) ], axial_coord( 1, -1 ))
    #test.direction_move( [ axial_coord( 1 , 4 ), axial_coord( 0 , 4 ) ], axial_coord( 1, -1 ))

    # test.direction_move( [ axial_coord( 0 , 3 ) ], axial_coord( 1, -1 ))
    # test.direction_move( [ axial_coord( 1 , 2 ) ], axial_coord( 0, 1 ))


    # print( test.moveable( axial_coord( 0, 3 ), axial_coord( 1, 3 ) ) )
    #
    #
    # print( test[ axial_coord( 0, 3 ) ].possible_neighbors)
    #
    #
    #
    # neighs = []
    # for x in range(6):
    #     neighs.append( axial_coord( 0 , x) )
    #
    #
    # print( len(axial_coord(0,1))   )
    #
    # print('\n\n\n\n')
    # print(neighs[0] + neighs[1])

    # def direction_move( self, coords_from: list, direction: axial_coord ):
    #     def add_axial_coords( a , b ):
    #         return axial_coord( a.x + b.x , a.y + b.y)
    #
    #     def subtract_axial_coords( a , b ):
    #         return axial_coord(  (a.x - b.x) , (a.y - b.y) )
    #
    #     def one_piece_move( coord_from , coord_to ):
    #         if( self.is_empty_neighbor( coord_from , coord_to ) ):
    #             temp_val = self[ coord_from ].val
    #             self[ coord_from ] = self[ coord_to ].val
    #             self[ coord_to ] = temp_val
    #
    #
    #
    #     def is_in_row( coords ):
    #         direction = coords[ 0 ] - coords[ 1 ]
    #         for i in range( len(coords) - 1 ):
    #             if(  (coords[i] - coords[ i + 1 ] != direction) or (self[ coords[ i ] ].val != self[ coords[ i+1 ] ].val) or ( not self.is_valid_neighbor( coords[i] , coords[ i+1 ] ) ) ):
    #                 return False
    #
    #         return True
    #
    #
    #
    #
    #     assert max( direction.x ,  direction.y ) <= 1
    #     assert min( direction.x , direction.y ) >= -1
    #     assert -2 < direction.x + direction.y < 2
    #
    #     if ( len( coords_from ) == 1 ):
    #         coord_from = coords_from[0]
    #         coord_to = coord_from + direction
    #
    #         one_piece_move( coord_from, coord_to )
    #
    #     if ( 2 <= len( coords_from ) <= 3  ):
    #         #they must be in a 'row' for any movetype
    #         if is_in_row( coords_from ):
    #             #if the move direction and row direction are the same it must be an inline move
    #             if( direction == subtract_axial_coords( coords_from[0], coords_from[1] ) ):
    #                 print(' inline ')
    #                 move_val = self[add_axial_coords( coords_from[0] , direction )].val
    #
    #                 if( move_val == 0 ):
    #                     for coord in coords_from:
    #                         self.direction_move( [coord] , direction )
    #
    #                 elif( move_val == 1 and self[ coords_from[ 0 ] ].val == 2 ):
    #                     push_count = 1
    #
    #                     new_coord = add_axial_coords( coords_from[0] , direction )
    #
    #
    #                     while push_count < max(2, len( coords_from ) ):
    #                         new_coord = add_axial_coords( new_coord , direction )
    #
    #                         if( self[ new_coord ] is None ):
    #                             new_coord = new_coord - direction
    #                             for i in range( push_count + len(coords_from) - 1 ):
    #
    #                                 prev_coord = new_coord - direction
    #                                 temp_val = self[ prev_coord ].val
    #                                 self[ new_coord ] = temp_val
    #                                 new_coord = prev_coord
    #
    #
    #                             self[ prev_coord ] = 0
    #
    #                             break
    #
    #                         if( self[ new_coord ].val == 1 ):
    #                             push_count += 1
    #
    #                         if( self[ new_coord ].val == 0 ):
    #                             for i in range( push_count + 1 ):
    #                                 self.direction_move( [subtract_axial_coords( new_coord, direction )] , direction )
    #                                 new_coord = subtract_axial_coords( new_coord, direction )
    #
    #                             for coord in coords_from:
    #                                 self.direction_move( [coord] , direction )
    #
    #                             break
    #
    #
    #                         if ( self[ new_coord ].val == 2 ):
    #                             break
    #
    #
    #                             for coord in coords_from:
    #                                 self.direction_move( [coord] , direction )
    #
    #                             break
    #
    #                 elif( move_val == 2 and self[ coords_from[ 0 ] ].val == 1 ):
    #
    #                     push_count = 1
    #
    #                     new_coord = add_axial_coords( coords_from[0] , direction )
    #
    #
    #
    #                     while push_count < max(2, len( coords_from ) ):
    #                         new_coord = add_axial_coords( new_coord , direction )
    #
    #                         if( self[ new_coord ] is None ):
    #                             new_coord = new_coord - direction
    #                             for i in range( push_count + len(coords_from) - 1 ):
    #                                 prev_coord = new_coord - direction
    #                                 temp_val = self[ prev_coord ].val
    #                                 self[ new_coord ] = temp_val
    #                                 new_coord = prev_coord
    #
    #                             self[ prev_coord ] = 0
    #
    #                             break
    #
    #                         if( self[ new_coord ].val == 2 ):
    #                             push_count += 1
    #
    #                         if( self[ new_coord ].val == 0 ):
    #                             for i in range( push_count + 1 ):
    #                                 self.direction_move( [subtract_axial_coords( new_coord, direction )] , direction )
    #                                 new_coord = subtract_axial_coords( new_coord, direction )
    #
    #                             for coord in coords_from:
    #                                 self.direction_move( [coord] , direction )
    #
    #                             break
    #
    #
    #                         if ( self[ new_coord ].val == 1 ):
    #                             break
    #
    #
    #                             for coord in coords_from:
    #                                 self.direction_move( [coord] , direction )
    #
    #                             break
    #
    #
    #             #if not inline, then broadside
    #             else:
    #                 all_moves_valid = True
    #                 for coord in coords_from:
    #                     if( (self.is_empty_neighbor( coord, ( coord + direction ) ) ) and (self[ coord ].val == AbaloneBoard.WHITE or self[ coord ].val == AbaloneBoard.BLACK) and (self[  add_axial_coords( coord , direction ) ].val == 0) ):
    #                         pass
    #                     else:
    #                         all_moves_valid = False
    #                         break
    #
    #                 if( all_moves_valid ):
    #                     for coord_from in coords_from:
    #                         coord_to = add_axial_coords( coord_from , direction )
    #                         #
    #                         # print('move')
    #                         # print('from: ', coord_from )
    #                         # print('to: ', coord_to)
    #
    #                         temp_val = self[ coord_from ].val
    #                         self[ coord_from ] = self[ coord_to ].val
    #                         self[ coord_to ] = temp_val
