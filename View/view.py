import pygame
from math import sin,cos, sqrt, ceil,pi
import sys

sys.path.insert(1, "/home/picklesueat/Python_projects/Abalone/Model/")

from board import AbaloneBoard, Hex, axial_coord


BLACK = 0,0,0
WHITE = 200,200,200
SCREEN_SIZE = WIDTH, HEIGHT = 1800,1000
pygame.init()

screen = pygame.display.set_mode(SCREEN_SIZE)

screen.fill(WHITE)



class HexView():
    def __init__( self, rad, x , y , val = None ):
        self.radius = rad
        self.x = x
        self.y = y
        self.val = val





def draw_hexagon(Surface,  radius, position):
    pi2 = 2 * pi

    return pygame.draw.lines(Surface,
          BLACK,
          True,
          [(cos(i / 6 * pi2 + ( pi2 / 4)) * radius + position[0], sin(i / 6 * pi2 + ( pi2 / 4)) * radius + position[1]) for i in range(0, 6)])


#dependent on the data structure, but it doesn't have to be, all it needs is a Data type containing the cubic indices and values of the coordinates to map
def make_view( board_data ):
    hexs = []
    black_pieces = {}
    white_pieces = {}
    radius = min(SCREEN_SIZE)/ ((len( board_data ) * 3 ))

    screen_center = (SCREEN_SIZE[0]/2, SCREEN_SIZE[1]/2)
    board_offset = ( screen_center[0] - (radius * len(board_data)) , screen_center[1]- (radius * len(board_data) * 2/3 ) )   #offset of top left corner of board from (0,0)
    for hex in board_data:
        y = (hex.axial_coord.y * radius * 3 /2) #+ board_offset[1]
        x = (sqrt(3) * radius * ( hex.axial_coord.y/2 + hex.axial_coord.x)) #+ board_offset[0]
        hexs.append(HexView( radius , x , y, hex.val  ))


        if( hex.val == 1):
            black_pieces[( hex.axial_coord.x , hex.axial_coord.y )] = True


        if( hex.val == 2):
            white_pieces[( hex.axial_coord.x , hex.axial_coord.y )] = True

    return hexs, black_pieces, white_pieces


def load_pieces( radius ):

    radius = int(radius)
    white_ball = pygame.image.load("/home/picklesueat/Python_projects/Abalone/View/images/cody.jpg")
    black_ball = pygame.image.load("/home/picklesueat/Python_projects/Abalone/View/images/img.JPG")

    black_ball = pygame.transform.scale(black_ball, (radius, radius))
    white_ball = pygame.transform.scale(white_ball, (radius, radius))

    return white_ball, black_ball

def display_view( hex_lst ):
    white_ball, black_ball = load_pieces( hex_lst[0].radius )

    for hex_view in hex_lst:
        draw_hexagon( screen, hex_view.radius, ( hex_view.x , hex_view.y ) )
        if( hex_view.val == 1 ):
            screen.blit(white_ball, (hex_view.x - hex_view.radius / 2 , hex_view.y - hex_view.radius / 2 ))

        if( hex_view.val == 2 ):
            screen.blit( black_ball, (hex_view.x - hex_view.radius / 2 , hex_view.y - hex_view.radius / 2 ))

    pygame.display.flip()

    return hex_view.radius




# collections.NamedTuple
def hex_round( y , x ):
    z = -x - y
    rx = round(x)
    ry = round(y)
    rz = round(z)

    x_diff = abs(x - rx)
    y_diff = abs(y - ry)
    z_diff = abs(z - rz)


    if ((x_diff > y_diff) and (x_diff > z_diff)):
        rx = -ry-rz
    elif y_diff > z_diff:
        ry = -rx-rz
    else:
        rz = -rx-ry


    return rx, ry, rz


if __name__ == '__main__':
    board = AbaloneBoard( 3 )
    board.add_pieces()

    hexs, black_pieces, white_pieces = make_view( board )
    radius = display_view( hexs )
    prev_click = []

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                pos = hex_round(  ( ( sqrt(3)/3.0 * pos[0] )- 1.0/3 * pos[1] ) / radius ,  ( 2.0/3 * pos[1] )  / radius  )

                pos = axial_coord( pos[1]  , pos[0]   )
                # coords = pos
                # tile = board.get_tile(coords)
                # direction = get_direction(prev_coords, coords)
                # board.move(tile, direction)
                # and then this will call something

                if( board[ pos ] is not None ):
                    if prev_click :
                        if ( white_pieces.get( (pos.x, pos.y ), False ) and ( player_move == board[ pos ].val ) ):
                                prev_click.append(pos)




                        elif (  black_pieces.get( (pos.x, pos.y ), False ) and ( player_move == board[ pos ].val ) ):
                                prev_click.append(pos)



                        else:
                            def subtract_axial_coords( a , b ):
                                return axial_coord( -1 * (a.x - b.x) , -1 * (a.y - b.y) )

                            direction = subtract_axial_coords( prev_click[0], pos )




                            if( -1  <= direction.x <= 1 and -1 <= direction.y <= 1 and -1 <= direction.x + direction.y <= 1 ):
                                # Use NamedTuple
                                # prev_click.xm prev_click.y
                                #board.make_move( prev_click , pos )

                                # print( '\n\n\n')
                                # print('real direction')
                                # print( direction )

                                board.direction_move( prev_click , direction )
                                prev_click = []

                                screen.fill(WHITE)
                                hexs, white_pieces, black_pieces = make_view( board )
                                radius = display_view( hexs )




                    else:
                        pygame.draw.rect(screen ,(0,0,255),(100,100,100,50))
                        pygame.display.flip()

                        prev_click.append( pos )
                        if( board[ pos ].val != 0  ):
                            player_move = board[ pos ].val
