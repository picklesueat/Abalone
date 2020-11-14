import pygame
from math import sin,cos, sqrt, ceil,pi
import sys
import os

from abalone import BLACK, WHITE, EMPTY

from abalone.model.board import AbaloneBoard, Hex, axial_coord

from abalone.controller import Controller
import pygame_menu

from collections import namedtuple

pixel_coord = namedtuple('Pixel', ['x', 'y'] )


IMAGES_DIR = os.path.join(os.path.dirname(__file__), 'Images')
COLOR_BLACK = 0,0,0
COLOR_WHITE = 230, 230 , 230
SCREEN_SIZE = WIDTH, HEIGHT = 1800,1000
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)

def game( size , two_player = True , depth = 2 ):
    def load_pieces():
        white_ball = pygame.image.load(IMAGES_DIR + "/white_ball.jpg")
        black_ball = pygame.image.load(IMAGES_DIR + "/black_ball.jpg")

        black_ball = pygame.transform.scale(black_ball, (radius, radius))
        white_ball = pygame.transform.scale(white_ball, (radius, radius))

        return white_ball, black_ball

    def hex_to_pixel( coord  ):
        y = ( coord.y * radius * 3 /2)
        x = (sqrt(3) * radius * ( coord.y / 2 + coord.x))

        return pixel_coord(x,y)

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

    def draw_hex( pixel_coord , val ):
        draw_hexagon( screen, ( pixel_coord.x , pixel_coord.y ) )
        if( val == WHITE ):
            screen.blit( white_ball, (pixel_coord.x - radius / 2 , pixel_coord.y - radius / 2 ))

        if( val == BLACK ):
            screen.blit( black_ball, (pixel_coord.x - radius / 2 , pixel_coord.y - radius / 2 ))

        pygame.display.flip()

    def draw_hexagon(Surface, position):
        pi2 = 2 * pi

        return pygame.draw.lines(Surface,
              COLOR_BLACK,
              True,
              [(cos(i / 6 * pi2 + ( pi2 / 4)) * radius + position[0], sin(i / 6 * pi2 + ( pi2 / 4)) * radius + position[1]) for i in range(0, 6)])

    def update_view( game ):
        screen.fill(COLOR_WHITE)

        for hex in game:
            pixel_coord = hex_to_pixel( hex.axial_coord )

            draw_hex( pixel_coord , hex.val )

        cont.updated = False

    cont = Controller( size , two_player  , depth )
    radius = int( min(SCREEN_SIZE)/ ((cont.size * 3 )) )
    white_ball, black_ball = load_pieces()


    update_view( cont.game )
    while True:
        pygame.time.delay( 100 )

        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                pos = ( pos[0], pos[1])
                pos = axial_coord( *hex_round(  *pixel_to_hex( pos )  ) )

                cont.take_click( pos )

                if( cont.updated ):
                    update_view( cont.game )

                if( cont.prev_click_coords ):
                    pygame.draw.rect(screen ,(0,0,255),(100,100,100,50))
                    pygame.display.flip()


def main():
    menu = pygame_menu.Menu(HEIGHT/2, WIDTH/2 , 'Abalone',
                       theme=pygame_menu.themes.THEME_BLUE)

    menu.add_button('Two Player', game, 3 )
    menu.add_button('ArTiFicAil InTeLliGence', game, 3 , False , 2 )
    menu.add_button('Quit', pygame_menu.events.EXIT)

    menu.mainloop( screen )
