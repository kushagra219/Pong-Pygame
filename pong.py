# PONG GAME
import sys
import os

def resource_path(relative_path):
    try: 
        base_path = sys._MEIPASS
        base_path = base_path.replace("\\", "/")
    except:
        base_path = os.path.abspath('.')
    
    return base_path + '/' + relative_path

import pygame
pygame.init()

screen_width = 720
screen_height = 406

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (239, 245, 66)
GRAY_DARK = (104, 107, 106)
GRAY_LIGHT = (161, 166, 165)

screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
pygame.display.set_caption("PONG")

icon = pygame.image.load(resource_path('assets/pong_icon.png'))
pygame.display.set_icon(icon)

clock = pygame.time.Clock()

font_small = pygame.font.SysFont('Comic Sans MS', 20)
font_medium = pygame.font.SysFont('Comic Sans MS', 30)
font_large = pygame.font.SysFont('Comic Sans MS', 50)

background_img = pygame.image.load(resource_path('assets/pong-bg.png'))
ball_img = pygame.image.load(resource_path('assets/ball.png'))
paddle_img = pygame.image.load(resource_path('assets/paddle.png'))
speaker_on_img = pygame.image.load(resource_path('assets/sound-on-img.png'))
speaker_off_img = pygame.image.load(resource_path('assets/sound-off-img.png'))

music = pygame.mixer.music.load(resource_path('assets/Monkeys-Spinning-Monkeys.mp3'))
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.5)

paddle1_hit_ball = pygame.mixer.Sound(resource_path("assets/paddle1-hit-ball.mp3"))
paddle2_hit_ball = pygame.mixer.Sound(resource_path("assets/paddle2-hit-ball.mp3"))
lost_point = pygame.mixer.Sound(resource_path("assets/hit.mp3"))
bounce_sound = pygame.mixer.Sound(resource_path("assets/ball-bounce.mp3"))


class Paddle(pygame.sprite.Sprite):
    
    def __init__(self, up_key, down_key):
        pygame.sprite.Sprite.__init__(self)
        self.image = paddle_img
        self.rect = self.image.get_rect()
        self.rect.height = 100
        self.rect.width = 21
        self.up_key = up_key
        self.down_key = down_key
        self.points = 0
        self.vel = 10
        self.won = False
    
    def set_player_name(self, player_name):
        self.player_name = player_name
        
        
class Ball(pygame.sprite.Sprite):
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = ball_img
        self.rect = self.image.get_rect()
        self.rect.height = 25
        self.rect.width = 25
        # x direction of of ball (1 = right, -1 = left)
        self.dx = 1
        # y direction of ball (1 = down, -1 = up) 
        self.dy = 1
        self.vel = 12
        

class Button(pygame.sprite.Sprite):
    
    def __init__(self, text):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([200, 50])
        self.image.fill(GRAY_DARK)
        self.rect = self.image.get_rect()
        self.text = text
        

class InputBox(pygame.sprite.Sprite):
    
    def __init__(self, text, color, text_color):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([200, 40])
        self.rect = self.image.get_rect()
        self.color = color
        self.text_color = text_color
        self.text = text
        self.active = False
        
player1_box = InputBox("Player 1", RED, RED)
player1_box.rect.x = 2 * screen_width // 3 - player1_box.rect.width // 2
player1_box.rect.y = 125

player2_box = InputBox("Player 2", BLUE, BLUE)
player2_box.rect.x = 2 * screen_width // 3 - player2_box.rect.width // 2
player2_box.rect.y = 200

letsgo_btn = Button("Let's Go")
letsgo_btn.rect.x = screen_width // 2 - letsgo_btn.rect.width // 2
letsgo_btn.rect.y = 300

input_boxes = [player1_box, player2_box]
        
def input_player_names():
    global run, play_started
    
    screen.fill(BLACK)
    text = font_large.render('PONG', False, WHITE)
    screen.blit(text, (screen_width // 2 - text.get_rect().width // 2, 20))
    
    text = font_medium.render('Player 1 Name: ', False, WHITE)
    screen.blit(text, (screen_width // 3 - text.get_rect().width // 2, 125))
    
    text = font_medium.render('Player 2 Name: ', False, WHITE)
    screen.blit(text, (screen_width // 3 - text.get_rect().width // 2, 200))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            return
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if player1_box.rect.collidepoint(event.pos):
                # Toggle the active variable.
                player1_box.active = not player1_box.active
            else:
                player1_box.active = False
                
            if player2_box.rect.collidepoint(event.pos):
                # Toggle the active variable.
                player2_box.active = not player1_box.active
            else:
                player2_box.active = False
                
                
        player1_box.color = RED if player1_box.active else WHITE
        player2_box.color = BLUE if player2_box.active else WHITE
        
        if event.type == pygame.KEYDOWN:
            if player1_box.active:
                if event.key == pygame.K_BACKSPACE:
                    player1_box.text = player1_box.text[:-1]
                else:
                    player1_box.text += event.unicode
                    
            if player2_box.active:
                if event.key == pygame.K_BACKSPACE:
                    player2_box.text = player2_box.text[:-1]
                else:
                    player2_box.text += event.unicode
               
        if event.type == pygame.MOUSEBUTTONDOWN:
            if letsgo_btn.rect.collidepoint(event.pos) == True: 
                pygame.time.delay(100)
                player1_name = player1_box.text if player1_box.text != "" else "Player 1"
                player2_name = player2_box.text if player2_box.text != "" else "Player 2"
                paddle1.set_player_name(player1_name)
                paddle2.set_player_name(player2_name)
                play_started = True 
                return
                    
    for box in input_boxes:
        box.image.fill(box.color)
        box.image.fill(WHITE, box.image.get_rect().inflate(-3, -3))
        screen.blit(box.image, (box.rect.x, box.rect.y))
        text = font_medium.render(box.text, False, box.text_color)
        screen.blit(text, (box.rect.x + box.rect.width // 2 - text.get_rect().width // 2, box.rect.y))
        
    mouse_pos = pygame.mouse.get_pos()
    
    if letsgo_btn.rect.collidepoint(mouse_pos) == True:
        letsgo_btn.image.fill(GRAY_LIGHT)
    else:
        letsgo_btn.image.fill(GRAY_DARK)
        
    screen.blit(letsgo_btn.image, (letsgo_btn.rect.x, letsgo_btn.rect.y))
    text = font_medium.render(letsgo_btn.text, False, WHITE)
    screen.blit(text, (letsgo_btn.rect.x + letsgo_btn.rect.width // 2 - text.get_rect().width // 2, letsgo_btn.rect.y))
    
    pygame.display.update()
        
        
start_btn = Button("Start")
start_btn.rect.x = screen_width // 2 - start_btn.rect.width // 2
start_btn.rect.y = 150

quit_btn = Button("Quit")
quit_btn.rect.x = screen_width // 2 - quit_btn.rect.width // 2
quit_btn.rect.y = 250

btn_sprites = pygame.sprite.Group()
btn_sprites.add(start_btn, quit_btn)
buttons = [start_btn, quit_btn]

def start():
    global run, input_players

    screen.fill(BLACK)
    
    text = font_large.render('PONG', False, WHITE)
    screen.blit(text, (screen_width // 2 - text.get_rect().width // 2, 20))
    
    mouse_pos = pygame.mouse.get_pos()
    
    if start_btn.rect.collidepoint(mouse_pos) == True:
        start_btn.image.fill(GRAY_LIGHT)
    else:
        start_btn.image.fill(GRAY_DARK)
        
    
    if quit_btn.rect.collidepoint(mouse_pos) == True:
        quit_btn.image.fill(GRAY_LIGHT)
    else:
        quit_btn.image.fill(GRAY_DARK)
        
    
    btn_sprites.draw(screen)
    
    for btn in buttons:
        text = font_medium.render(btn.text, False, WHITE)
        screen.blit(text, (btn.rect.x + btn.rect.width // 2 - text.get_rect().width // 2, btn.rect.y))
        
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            run = False
            return
        
        # checks if a mouse is clicked 
        if event.type == pygame.MOUSEBUTTONDOWN:
            if start_btn.rect.collidepoint(event.pos) == True: 
                pygame.time.delay(100)
                input_players = True 
                return
            
            if quit_btn.rect.collidepoint(event.pos) == True:
                run = False
                return
                
    pygame.display.update()
    
    
replay_btn = Button("Replay")
replay_btn.rect.x = screen_width // 3 - replay_btn.rect.width // 2
replay_btn.rect.y = 225

exit_btn = Button("Exit")
exit_btn.rect.x = 2 * screen_width // 3 - exit_btn.rect.width // 2
exit_btn.rect.y = 225

game_over_btns = [replay_btn, exit_btn]
    
def game_over():
    global run, is_game_over
    
    screen.fill(BLACK)
    
    mouse_pos = pygame.mouse.get_pos()
    
    if replay_btn.rect.collidepoint(mouse_pos) == True:
        replay_btn.image.fill(GRAY_LIGHT)
    else:
        replay_btn.image.fill(GRAY_DARK)
        
    
    if exit_btn.rect.collidepoint(mouse_pos) == True:
        exit_btn.image.fill(GRAY_LIGHT)
    else:
        exit_btn.image.fill(GRAY_DARK)
    
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            run = False
            return
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if replay_btn.rect.collidepoint(event.pos) == True: 
                pygame.time.delay(100)
                paddle1.points = 0
                paddle2.points = 0
                paddle1.won = False
                paddle2.won = False
                is_game_over = False
                return
            
            if exit_btn.rect.collidepoint(event.pos) == True:
                run = False
                return
        
    if paddle1.won == True:
        text = font_large.render(paddle1.player_name + ' WON !', False, WHITE)
        screen.blit(text, (screen_width // 2 - text.get_rect().width // 2, 100))
        
    if paddle2.won == True:
        text = font_large.render(paddle2.player_name + ' WON !', False, WHITE)
        screen.blit(text, (screen_width // 2 - text.get_rect().width // 2, 100))
        
    for btn in game_over_btns:
        screen.blit(btn.image, (btn.rect.x, btn.rect.y))
        text = font_medium.render(btn.text, False, WHITE)
        screen.blit(text, (btn.rect.x + btn.rect.width // 2 - text.get_rect().width // 2, btn.rect.y))
        
        
    pygame.display.update()

p1_up_box = InputBox("W", GREEN, RED)
p1_up_box.rect.x = 125
p1_up_box.rect.y = 175

p1_down_box = InputBox("S", GREEN, RED)
p1_down_box.rect.x = 125
p1_down_box.rect.y = 250

p2_up_box = InputBox("UP", GREEN, BLUE)
p2_up_box.rect.x = 4 * screen_width // 5 - p2_up_box.rect.width // 2
p2_up_box.rect.y = 175

p2_down_box = InputBox("DOWN", GREEN, BLUE)
p2_down_box.rect.x = 4 * screen_width // 5 - p2_down_box.rect.width // 2
p2_down_box.rect.y = 250

control_boxes = [p1_up_box, p1_down_box, p2_up_box, p2_down_box]
speaker_img = speaker_on_img
    
def controls():
    global run, play_paused, music_paused, speaker_img
    screen.fill(BLACK)
    
    text = font_large.render('Controls', False, WHITE)
    screen.blit(text, (screen_width // 2 - text.get_rect().width // 2, 20))
    
    text = font_medium.render('Player 1', False, WHITE)
    screen.blit(text, (150, 110))
    
    text = font_medium.render('Player 2', False, WHITE)
    screen.blit(text, (485, 110))
    
    text = font_small.render('UP', False, WHITE)
    screen.blit(text, (50, 175))
    
    text = font_small.render('DOWN', False, WHITE)
    screen.blit(text, (40, 250))
    
    text = font_small.render('UP', False, WHITE)
    screen.blit(text, (3 * screen_width // 5 - text.get_rect().width // 2, 175))
    
    text = font_small.render('DOWN', False, WHITE)
    screen.blit(text, (3 * screen_width // 5 - text.get_rect().width // 2, 250))
    
    text = font_medium.render('Audio (ON/OFF)', False, WHITE)
    screen.blit(text, (screen_width // 3 - text.get_rect().width // 2 + 50, 330))
    
    for box in control_boxes:
        box.color = GREEN if box.active else WHITE
    
    screen.blit(speaker_img, (2 * screen_width // 3 - speaker_off_img.get_rect().width // 2, 325))
    
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            run = False
            return
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            for box in control_boxes:
                if box.rect.collidepoint(event.pos):
                    box.active = not player1_box.active
                else:
                    box.active = False
                box.color = GREEN if box.active else WHITE
                
            if event.pos[0] >= (2 * screen_width // 3 - speaker_off_img.get_rect().width // 2) and \
            event.pos[0] <= (2 * screen_width // 3 - speaker_off_img.get_rect().width // 2 + 50):
                if event.pos[1] >= 325 and event.pos[1] <= 375:
                    if music_paused:
                        speaker_img = speaker_on_img
                        pygame.mixer.music.unpause()
                        music_paused = False
                    else:
                        speaker_img = speaker_off_img
                        pygame.mixer.music.pause()
                        music_paused = True
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE: 
                try:
                    paddle1.up_key = pygame.key.key_code(p1_up_box.text.strip())
                except:
                    paddle1.up_key = pygame.K_w
                try:
                    paddle1.down_key = pygame.key.key_code(p1_down_box.text.strip())
                except:
                    paddle1.down_key = pygame.K_s
                try:
                    paddle2.up_key = pygame.key.key_code(p2_up_box.text.strip())
                except:
                    paddle2.up_key = pygame.K_UP
                try:
                    paddle2.down_key = pygame.key.key_code(p2_down_box.text.strip())
                except:
                    paddle1.down_key = pygame.K_DOWN
                play_paused = False
                return

            for box in control_boxes:
                if box.active:
                    if event.key == pygame.K_BACKSPACE:
                        box.text = box.text[:-1]
                    else:
                        box.text += event.unicode
            
            
    for box in control_boxes:
        box.image.fill(box.color)
        box.image.fill(WHITE, box.image.get_rect().inflate(-3, -3))
        screen.blit(box.image, (box.rect.x, box.rect.y))
        text = font_medium.render(box.text, False, box.text_color)
        screen.blit(text, (box.rect.x + box.rect.width // 2 - text.get_rect().width // 2, box.rect.y))
    
    pygame.display.update()


def redraw():
    screen.blit(background_img, (0, 0))
    
    for i in range(19):
        pygame.draw.rect(screen, WHITE, (360, 20 + 20 * i, 8, 10))
    
#     text = font_medium.render('PONG', True, WHITE)
#     screen.blit(text, (screen_width // 2 - text.get_rect().width // 2, 10))
    
    player1_text = font_medium.render(paddle1.player_name, False, RED)
    screen.blit(player1_text, (screen_width // 4 - player1_text.get_rect().width // 2, 10))
    
    player2_text = font_medium.render(paddle2.player_name, False, BLUE)
    screen.blit(player2_text, (3 * screen_width // 4 - player2_text.get_rect().width // 2, 10))
    
    player1_score = font_medium.render(str(paddle1.points), False, RED)
    screen.blit(player1_score, (screen_width // 4 - player1_score.get_rect().width // 2, 50))
    
    player2_score = font_medium.render(str(paddle2.points), False, BLUE)
    screen.blit(player2_score, (3 * screen_width // 4 - player2_score.get_rect().width // 2, 50))
    
    obj_sprites.draw(screen)
    pygame.display.update()
    

def play():
    global run, is_game_over, play_paused
    
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            run = False
            return
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE: 
                play_paused = True
                return
            
    
    keys_pressed = pygame.key.get_pressed()

    if keys_pressed[paddle2.up_key] == True and paddle2.rect.y - paddle2.vel > 0:
        paddle2.rect.y -= paddle2.vel  

    if keys_pressed[paddle2.down_key] == True and paddle2.rect.y + paddle2.rect.height + paddle2.vel < screen_height:
        paddle2.rect.y += paddle2.vel

    if keys_pressed[paddle1.up_key] == True and paddle1.rect.y - paddle1.vel > 0:
        paddle1.rect.y -= paddle1.vel  

    if keys_pressed[paddle1.down_key] == True and paddle1.rect.y + paddle1.rect.height + paddle1.vel < screen_height:
        paddle1.rect.y += paddle1.vel

    if ball.dx == -1:
        ball.rect.x -= ball.vel
    else:
        ball.rect.x += ball.vel

    if ball.dy == -1:
        ball.rect.y -= ball.vel
    else:
        ball.rect.y += ball.vel

    # y-axis boundary conditions for the ball 
    if ball.rect.y <= 0 or ball.rect.y + ball.rect.height >= screen_height:
        ball.dy = (-1) * ball.dy
        bounce_sound.play()

    # if any player loses a point
    if ball.rect.x <= 0:
        ball.rect.x = screen_width // 2 - ball.rect.width // 2
        ball.rect.y = screen_height // 2 - ball.rect.height // 2
        ball.dx = -1
        ball.dy = 1
        paddle2.points += 1
        lost_point.play()

    elif ball.rect.x + ball.rect.width >= screen_width:
        ball.rect.x = screen_width // 2 - ball.rect.width // 2
        ball.rect.y = screen_height // 2 - ball.rect.height // 2
        ball.dx = 1
        ball.dy = 1
        paddle1.points += 1
        lost_point.play()
        
    if paddle1.points >= 10:
        is_game_over = True
        paddle1.won = True
        game_over()
    
    if paddle2.points >= 10:
        is_game_over = True
        paddle2.won = True
        game_over()

    if paddle1.rect.colliderect(ball) == True:
        ball.dx = (-1) * ball.dx
        paddle1_hit_ball.play()

    if paddle2.rect.colliderect(ball) == True:
        ball.dx = (-1) * ball.dx
        paddle2_hit_ball.play()

    redraw()


paddle1 = Paddle(pygame.K_w, pygame.K_s)
paddle1.rect.x = paddle1.rect.width + 5
paddle1.rect.y = screen_height // 2 - paddle1.rect.height // 2

paddle2 = Paddle(pygame.K_UP, pygame.K_DOWN)
paddle2.rect.x = screen_width - 2 * paddle2.rect.width - 5
paddle2.rect.y = screen_height // 2 - paddle2.rect.height // 2

ball = Ball()
ball.rect.x = screen_width // 2 - ball.rect.width // 2 
ball.rect.y = screen_height // 2 - ball.rect.height // 2

obj_sprites = pygame.sprite.Group()
obj_sprites.add(paddle1, paddle2, ball)


run = True
play_started = False
is_game_over = False
input_players = False
play_paused = False
music_paused = False

if __name__.endswith('__main__'):
    while run == True:
        clock.tick(20)
            
        if play_started == True:
            if is_game_over == True:
                game_over()
            elif play_paused == True:
                controls()
            else:
                play()
        elif input_players == True:
            input_player_names()
        else:
            start()
        

pygame.quit()