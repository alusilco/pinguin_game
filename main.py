import pgzrun

WIDTH = 1000  # Ancho de la ventana
HEIGHT = 700  # Altura de la ventana

TITLE = "Pinguin Game"  # Título para la ventana de juego
FPS = 30  # Número de fotogramas por segundo

pinguin = Actor('pinguin', (100, 650))
background = Actor('background', (WIDTH // 2, HEIGHT // 2))
ball = Actor('ball', (550, 590))
bee = Actor('bee', (850, 675))
go = Actor('go', (WIDTH // 2, HEIGHT // 2))
finish = Actor('finish', (970, HEIGHT - 50))
start = Actor('start', (50, HEIGHT - 50))
game_over = 0
new_image = 'pinguin'
show_go = False  # Variable para controlar la aparición del cartel "go"
start = Actor('start', (50, HEIGHT - 50))

# Función para reiniciar el juego
def reset_game():
    global game_over, new_image, show_go
    game_over = 0
    show_go = False  # Ocultar el cartel "go" al reiniciar
    pinguin.pos = (100, 650)  # Restablecer a su posición original
    ball.pos = (550, 590)
    bee.pos = (850, 675)
    pinguin.image = 'pinguin'
    new_image = 'pinguin'

# Función para mostrar el cartel "go" con retraso
def show_go_cartel():
    global show_go
    show_go = True  # Mostrar el cartel "go"

def draw():
    background.draw()
    pinguin.draw()
    ball.draw()
    bee.draw()
    if show_go:  # Mostrar el cartel "go" cuando show_go es True
        go.draw()
    finish.draw()
    start.draw()

def update(dt):
    global new_image, game_over
    
    if game_over == 0:  # Solo actualizamos cuando no hay game over
        # Movimiento de la abeja
        if bee.x > -20:
            bee.x = bee.x - 5
        else:
            bee.x = WIDTH + 20

        # Movimiento de la pelota
        if ball.x > -20:
            ball.x = ball.x - 5
            ball.angle = ball.angle + 5
        else:
            ball.x = WIDTH + 20

        # Controles
        if (keyboard.left or keyboard.a) and pinguin.x > 20:
            pinguin.x = pinguin.x - 5
            if new_image != 'left':
                pinguin.image = 'left'
                new_image = 'left'
        elif (keyboard.right or keyboard.d) and pinguin.x < 580:
            pinguin.x = pinguin.x + 5
            if new_image != 'right':
                pinguin.image = 'right'
                new_image = 'right'
        elif keyboard.down or keyboard.s:
            if new_image != 'sit':
                pinguin.image = 'sit'
                new_image = 'sit'
                pinguin.y = 250
        else:
            if new_image == 'hurt' and pinguin.y != 240:
                pinguin.image = 'pinguin'
                new_image = 'pinguin'
                pinguin.y = 240

        # Colisión
        if pinguin.colliderect(ball) or pinguin.colliderect(bee):
            game_over = 1
            pinguin.image = 'hurt'  # Cambiar a la imagen 'hurt' tras la colisión
            new_image = 'hurt'
            clock.schedule(show_go_cartel, 0.5)  # Mostrar el cartel "go" después de 2 segundos
            clock.schedule(reset_game, 2.0)  # Reiniciar el juego después de 4 segundos

    if game_over == 1 and keyboard.RETURN:
        reset_game()

def on_key_down(key):
    # Salto
    if (key == keys.SPACE or key == keys.UP or key == keys.W) and game_over == 0:
        pinguin.y = 100
        animate(pinguin, tween='bounce_end', duration=2, y=240)

pgzrun.go()


