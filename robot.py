import pygame
import socket
import sys
import threading

PORT = 2024

# Inicializa o Pygame
pygame.init()

# Screen dimensions
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Colors
black = (0, 0, 0)

# Taxa de quadros por segundo
clock = pygame.time.Clock()
fps = 60

background_image = pygame.image.load("background2.jpeg")
background_image = pygame.transform.scale(
    background_image, (screen_width, screen_height)
)


# Robot class
class Robot(pygame.sprite.Sprite):
    def __init__(self):
        super(Robot, self).__init__()
        #Carrega a imagem e redimensiona
        original_image = pygame.image.load("manujogo.png")
        self.image = pygame.transform.scale_by(original_image, 0.45)
        self.rect = self.image.get_rect()
        self.rect.center = (screen_width // 2, screen_height // 1.5) 
        self.direction = "UP"

    def update(self, command):
        if command:
            if command == "up" and self.rect.top > 0:
                self.rect.y -= 10
            elif command == "down" and self.rect.bottom < screen_height:
                self.rect.y += 10
            elif command == "left" and self.rect.left > 0:
                self.rect.x -= 10
            elif command == "right" and self.rect.right < screen_width:
                self.rect.x += 10


# Inicializa o robô
robot = Robot()
all_sprites = pygame.sprite.Group() #Feito pra desenhar múltiplos elementos
all_sprites.add(robot)

# Configuração do Socket UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("", PORT)) #Associa à porta especificada
sock.setblocking(0)  # Configura o socket p/ não bloquear a execução ao esperar dados

# Thread para lidar com a comunicação via UDP
command_lock = threading.Lock()
current_command = None
running = True


def receive_commands():
    global current_command
    while running:
        try:
            data, _ = sock.recvfrom(4096)
            with command_lock:

                res = data.decode("utf-8").strip().lower().split(";")
                if res[0] == "controle":
                    current_command = res[1]
                else:
                    current_command = None
        except BlockingIOError:
            continue


# Inicia a thread para receber comandos
thread = threading.Thread(target=receive_commands)
thread.start()

# Loop principal do jogo
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Obtém o comando mais recente
    with command_lock:
        command_to_use = current_command
        current_command = None  # Reseta o comando após usá-lo

    # Atualiza c/ fundo preto
    screen.blit(background_image, (0, 0))

    # Retângulo vermelho no robô
    pygame.draw.rect(screen, (255,0,0), robot.rect, 2)

    # Atualiza e desenha todos os sprites
    if command_to_use:
        robot.update(command_to_use)
    all_sprites.draw(screen)

    # Atualiza o display
    pygame.display.flip()

    # Controla a taxa de quadros por segundo
    clock.tick(fps)

# Aguarda a finalização da thread
thread.join()

# Encerra
pygame.quit()
sys.exit()
