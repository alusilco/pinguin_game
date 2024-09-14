import pgzrun

WIDTH = 1000
HEIGHT = 700

TITLE = "Pinguin Game"
FPS = 30

pinguin = Actor('pinguin', (100, 650))
background1 = Actor('background', (WIDTH // 2, HEIGHT // 2))
background2 = Actor('background', (WIDTH + WIDTH // 2, HEIGHT // 2))
ball = Actor('ball', (550, 710))
bee = Actor('bee', (850, 700))
go = Actor('go', (WIDTH // 2, HEIGHT // 2))
finish = Actor('finish', (970, HEIGHT - 50))
start = Actor('start', (50, HEIGHT - 50))
game_over = 0
new_image = 'pinguin'
show_go = False
game_started = False

background_speed = 2

jumping = False
jump_velocity = 0
gravity = 0.5
jump_height = 150
original_y = pinguin.y

animation_duration = 0.5
animation_timer = 0

def reset_game():
    global game_over, new_image, show_go, game_started, jumping, jump_velocity, animation_timer
    game_over = 0
    show_go = False
    game_started = False
    jumping = False
    jump_velocity = 0
    animation_timer = 0
    pinguin.y = original_y
    pinguin.image = 'pinguin'
    new_image = 'pinguin'
    ball.pos = (550, 600)
    bee.pos = (850, 665)

def show_go_cartel():
    global show_go
    show_go = True

def draw():
    background1.draw()
    background2.draw()
    pinguin.draw()
    ball.draw()
    bee.draw()
    if show_go:
        go.draw()
    if not show_go:
        start.draw()
        finish.draw()

def update(dt):
    global new_image, game_over, jumping, jump_velocity, animation_timer
    global background1, background2, game_started

    if game_over == 0:
        if game_started:
            background1.x -= background_speed
            background2.x -= background_speed
            
            if background1.x < -WIDTH // 2:
                background1.x = WIDTH + WIDTH // 2
            if background2.x < -WIDTH // 2:
                background2.x = WIDTH + WIDTH // 2

        if bee.x > -20:
            bee.x -= 5
        else:
            bee.x = WIDTH + 20

        if ball.x > -20:
            ball.x -= 5
            ball.angle += 5
        else:
            ball.x = WIDTH + 20

        if jumping:
            pinguin.y += jump_velocity
            jump_velocity += gravity

            if pinguin.y <= original_y - jump_height:
                pinguin.y = original_y - jump_height
                jump_velocity = 0
            elif pinguin.y >= original_y:
                pinguin.y = original_y
                jumping = False
                jump_velocity = 0

        if animation_timer > 0:
            animation_timer -= dt
            if animation_timer <= 0:
                pinguin.image = 'pinguin'
                new_image = 'pinguin'
                pinguin.y = original_y

        if (keyboard.left or keyboard.a) and pinguin.x > 20:
            pinguin.x -= 5
            if new_image != 'left':
                pinguin.image = 'left'
                new_image = 'left'
                animation_timer = animation_duration
            game_started = True
        elif (keyboard.right or keyboard.d) and pinguin.x < WIDTH - 50:
            pinguin.x += 5
            if new_image != 'right':
                pinguin.image = 'right'
                new_image = 'right'
                animation_timer = animation_duration
            game_started = True
        elif keyboard.down or keyboard.s:
            if new_image != 'sit':
                pinguin.image = 'sit'
                new_image = 'sit'
                pinguin.y = original_y - 0
                animation_timer = animation_duration
            game_started = True
        else:
            if new_image == 'hurt' and pinguin.y != original_y:
                pinguin.image = 'pinguin'
                new_image = 'pinguin'
                pinguin.y = original_y

        if pinguin.colliderect(ball) or pinguin.colliderect(bee):
            game_over = 1
            pinguin.image = 'hurt'
            new_image = 'hurt'
            clock.schedule(show_go_cartel, 0.5)
            clock.schedule(reset_game, 2.0)

    if game_over == 1 and keyboard.RETURN:
        reset_game()

def on_key_down(key):
    global game_started, jumping, jump_velocity

    if (key == keys.SPACE or key == keys.UP or key == keys.W) and game_over == 0 and not jumping:
        jumping = True
        jump_velocity = -10
        game_started = True

pgzrun.go()
