import pygame
from math import sin,cos, sqrt, ceil,pi
import sys



sys.path.insert(1, "/home/picklesueat/Python_projects/Abalone/Model/")
sys.path.insert(1, "/home/picklesueat/Python_projects/Abalone/")

from board import AbaloneBoard, Hex, axial_coord
from controller import Game, Controller


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

    radius = min(SCREEN_SIZE)/ ((len( board_data ) * 3 ))

    x_offset = 200
    y_offset = 50* (7 - board_data.size)

    for hex in board_data:
        y = (hex.axial_coord.y * radius * 3 /2) + y_offset
        x = (sqrt(3) * radius * ( hex.axial_coord.y/2 + hex.axial_coord.x))  + x_offset
        hexs.append(HexView( radius , x , y, hex.val  ))



    return hexs


def load_pieces( radius ):

    radius = int(radius)
    white_ball = pygame.image.load("/home/picklesueat/Python_projects/Abalone/View/images/white_ball.jpg")
    black_ball = pygame.image.load("/home/picklesueat/Python_projects/Abalone/View/images/black_ball.jpg")

    black_ball = pygame.transform.scale(black_ball, (radius, radius))
    white_ball = pygame.transform.scale(white_ball, (radius, radius))

    return white_ball, black_ball

def display_view( hex_lst ):
    white_ball, black_ball = load_pieces( hex_lst[0].radius )


    for hex_view in hex_lst:
        draw_hexagon( screen, hex_view.radius, ( hex_view.x , hex_view.y ) )
        if( hex_view.val == 2 ):
            screen.blit(white_ball, (hex_view.x - hex_view.radius / 2 , hex_view.y - hex_view.radius / 2 ))

        if( hex_view.val == 1 ):
            screen.blit( black_ball, (hex_view.x - hex_view.radius / 2 , hex_view.y - hex_view.radius / 2 ))

    pygame.display.flip()

    return hex_view.radius




# collections.NamedTuple
def hex_round( x , y ):
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


    return rx, ry

def pixel_to_hex( pos ):
    x = ( ( sqrt(3)/3.0 * pos[0] )- 1.0/3 * pos[1] ) / radius
    y = ( 2.0/3 * pos[1] )  / radius

    return ( x , y )


def update_board( ):
    screen.fill(WHITE)
    hexs = make_view( cont.game )


    radius = display_view( hexs )
    cont.updated = False

    return radius


if __name__ == '__main__':
    BLACK = 0,0,0
    WHITE = 200,200,200
    SCREEN_SIZE = WIDTH, HEIGHT = 1800,1000

    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)


    cont = Controller( 3 , two_player = False )

    radius = update_board()


    prev_click = []

    while True:
        pygame.time.delay( 100 )

        if( cont.game.two_player == False ):
            if( cont.game.turn == 1 ):
                cont.get_best_move( 3 )
                update_board()


        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                pos = ( pos[0] - 200, pos[1] - 50* (7 - cont.size ))

                pos = axial_coord( *hex_round(  *pixel_to_hex( pos )  ) )

                if( cont.is_valid_click( pos ) ):
                    if cont.prev_click_coords :
                        cont.take_click( pos )

                        if( cont.updated ):
                            update_board()




                    else:
                        if cont.take_first_click( pos ):
                            pygame.draw.rect(screen ,(0,0,255),(100,100,100,50))
                            pygame.display.flip()
