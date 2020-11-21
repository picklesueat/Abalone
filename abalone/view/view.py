import pygame
from math import sin,cos, sqrt, ceil,pi
import sys
import os
import time

from abalone import BLACK, WHITE, EMPTY

from abalone.model.board import AbaloneBoard, Hex, axial_coord

from abalone.controller import Controller
import pygame_menu

from collections import namedtuple

pixel_coord = namedtuple('Pixel', ['x', 'y'] )


IMAGES_DIR = os.path.join(os.path.dirname(__file__), 'Images')
COLOR_BLACK = 0,0,0
COLOR_WHITE = 250, 250 , 250
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
        y = ( coord.y * radius * 3 /2) + 1/size * 400
        x = (sqrt(3) * radius * ( coord.y / 2 + coord.x)) + 1/size * 400

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

        pix_x , pix_y = pos.x - 1/size * 400 ,  pos.y - 1/size * 400
        x = ( ( sqrt(3)/3.0 * pix_x )- 1.0/3 * pix_y ) / radius
        y = ( 2.0/3 * pix_y )  / radius

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
              COLOR_WHITE,
              True,
              [(cos(i / 6 * pi2 + ( pi2 / 4)) * radius + position[0], sin(i / 6 * pi2 + ( pi2 / 4)) * radius + position[1]) for i in range(0, 6)] , width = 5)

    def draw_depth_button():
        if cont.two_player :
            return None

        button_width = 300
        button_height = 100
        pygame.draw.rect(screen, ( 255 , 255 , 255 ),(WIDTH - button_width , 0 , button_width ,button_height))

        pygame.font.init()
        text = pygame.font.SysFont('Comic Sans MS', 50)
        text_surf = text.render('AI Strength', False , COLOR_BLACK )
        screen.blit( text_surf , ( WIDTH - button_width/ 1.25 , button_height /4 ))

        pygame.font.init()
        text = pygame.font.SysFont('Comic Sans MS', 30)
        text_surf = text.render( '('+str(cont.game.black_player.depth)+')' , False , COLOR_BLACK )
        screen.blit( text_surf , ( WIDTH - button_width/ 2 , button_height /1.5 ))

        #plus button
        plus_button_height = 75
        plus_rect = pygame.draw.rect(screen, ( 200 , 200 , 200 ),(WIDTH - button_width , button_height , button_width /2 , plus_button_height ))

        pygame.font.init()
        text = pygame.font.SysFont('Comic Sans MS', 50)
        text_surf = text.render('+', False , COLOR_BLACK )
        screen.blit( text_surf , ( WIDTH - 3*button_width/4 , button_height + plus_button_height / 4 ))

        #minue button
        minus_rect = pygame.draw.rect(screen, ( 220 , 220 , 220 ),(WIDTH - button_width / 2 , button_height , button_width /2 , plus_button_height ))


        pygame.font.init()
        text = pygame.font.SysFont('Comic Sans MS', 50)
        text_surf = text.render('-', False , COLOR_BLACK )
        screen.blit( text_surf , ( WIDTH - button_width/4 , button_height + plus_button_height / 4 ))

        return plus_rect , minus_rect

    def update_view( game ):
        screen.fill(COLOR_BLACK)

        draw_depth_button()
        draw_lives( game )

        for hex in game:
            pixel_coord = hex_to_pixel( hex.axial_coord )

            draw_hex( pixel_coord , hex.val )

        cont.updated = False
        pygame.display.flip()



    def draw_lives( game ):
        for i in range( game.black_player.lives ):
            screen.blit( black_ball, ( i * radius + 20 , HEIGHT - radius ))


        for j in range( game.white_player.lives ):
            screen.blit( white_ball, (WIDTH - j * radius - 130 ,  HEIGHT - radius))

    def display_winner_text( winner: int ):
        pygame.font.init()
        text = pygame.font.SysFont('Comic Sans MS', 100)
        if( winner == 1 ):
            text_surf = text.render('Black Wins', False , COLOR_WHITE )
        else:
            text_surf = text.render('White Wins', False , COLOR_WHITE )
        screen.blit( text_surf , ( 0 , 0 ))
        pygame.display.flip()

    def change_losers_piece( winner: int ):
        nonlocal white_ball , black_ball
        if(winner == 1):
            white_ball = pygame.image.load(IMAGES_DIR + "/sponge.jpg")
            white_ball = pygame.transform.scale(white_ball, (radius, radius))
        else:
            black_ball = pygame.image.load(IMAGES_DIR + "/sponge.jpg")
            black_ball = pygame.transform.scale(black_ball, (radius, radius))


    cont = Controller( size , two_player  , depth )
    radius = int( min(SCREEN_SIZE)/ ((cont.size * 3 )) )
    white_ball, black_ball = load_pieces()

    update_view( cont.game )
    if not two_player:
        plus_rect , minus_rect = draw_depth_button()

    running = True
    while running:
        pygame.time.delay( 100 )

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_u:
                    cont.undo_move()
                    update_view( cont.game )


            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                if not two_player:
                    if( plus_rect.collidepoint( pos )):
                        cont.adjust_AI_depth( 1 )
                        update_view( cont.game )
                    elif( minus_rect.collidepoint( pos ) ):
                        cont.adjust_AI_depth( -1 )
                        update_view( cont.game )

                pos = pixel_coord( pos[0] , pos[1] )

                pos = axial_coord( *hex_round(  *pixel_to_hex( pos )  ) )

                cont.take_click( pos )

                if( cont.updated ):
                    update_view( cont.game )

                cont.check_for_AI_move()


                if( cont.updated ):
                    update_view( cont.game )

                if( cont.prev_click_coords ):
                    pygame.draw.rect(screen ,(0,200,75),(25,100,200,75))
                    pygame.font.init()
                    text = pygame.font.SysFont('Comic Sans MS', 30)
                    text_surf = text.render('Piece(s) in hand', False , COLOR_BLACK )
                    screen.blit( text_surf , ( 50 , 125 ))
                    pygame.display.flip()

            if( cont.check_winner() ):
                change_losers_piece(cont.check_winner())
                update_view(cont.game)
                display_winner_text(cont.check_winner())
                pygame.time.delay( 4000 )
                running = False




def game_type_menu(  ):
    menu = pygame_menu.Menu(HEIGHT/2, WIDTH/2 , 'Game',
                       theme=pygame_menu.themes.THEME_BLUE)

    size = 2
    two_player = True


    def set_size( val , siz ):
        nonlocal size
        size = siz

    def set_game_type( val , two_playe):
        nonlocal two_player
        two_player = two_playe


    menu.add_selector('Size :', [('2', 2), ('3', 3), ('4', 4), ('5', 5)], onchange=set_size)
    menu.add_selector('Game Type :', [('Two Player', True), ('ArTiFicAil InTeLliGence', False)], onchange=set_game_type)



    def start():
        game( size , two_player)

    menu.add_button('Start', start )





    menu.mainloop( screen )

def main():
    menu = pygame_menu.Menu(HEIGHT/2, WIDTH/2 , 'Abalone',
                       theme=pygame_menu.themes.THEME_BLUE)

    menu.add_button('Play', game_type_menu )
    menu.add_button('Quit', pygame_menu.events.EXIT )

    menu.mainloop( screen )
