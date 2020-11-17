
def
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
