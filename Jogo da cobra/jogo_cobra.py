import pygame
import random
import time

# Inicializa o pygame
pygame.init()

# Dimensões
largura, altura = 600, 400
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Snake Evoluída")

# Cores
BRANCO = (255, 255, 255)
VERDE = (0, 255, 0)
VERMELHO = (255, 0, 0)
AZUL = (0, 0, 255)
DOURADO = (255, 215, 0)
CINZA = (100, 100, 100)

# Relógio
clock = pygame.time.Clock()

# Fonte
fonte = pygame.font.SysFont("arial", 20)

# Tamanho do bloco
bloco = 20

# Cobra
cobra = [(100, 50)]
direcao = "DIREITA"
velocidade_base = 10
velocidade = velocidade_base
boost_duracao = 0

# Comida
def nova_comida():
    return (random.randrange(0, largura, bloco), random.randrange(0, altura, bloco))

comida = nova_comida()
comida_dourada = None
tempo_ultima_comida = time.time()
combo = 0
pontos = 0

# Obstáculos
obstaculos = []

# Funções auxiliares
def desenhar_texto(texto, x, y, cor=BRANCO):
    img = fonte.render(texto, True, cor)
    tela.blit(img, (x, y))

def desenhar_cobra():
    for segmento in cobra:
        pygame.draw.rect(tela, VERDE, (*segmento, bloco, bloco))

def desenhar_obstaculos():
    for obs in obstaculos:
        pygame.draw.rect(tela, CINZA, (*obs, bloco, bloco))

# Loop principal
rodando = True
while rodando:
    tela.fill((0, 0, 0))

    # Eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_UP and direcao != "BAIXO":
                direcao = "CIMA"
            elif evento.key == pygame.K_DOWN and direcao != "CIMA":
                direcao = "BAIXO"
            elif evento.key == pygame.K_LEFT and direcao != "DIREITA":
                direcao = "ESQUERDA"
            elif evento.key == pygame.K_RIGHT and direcao != "ESQUERDA":
                direcao = "DIREITA"
            elif evento.key == pygame.K_LSHIFT and boost_duracao <= 0:
                boost_duracao = 30

    # Movimento
    x, y = cobra[0]
    if direcao == "CIMA":
        y -= bloco
    elif direcao == "BAIXO":
        y += bloco
    elif direcao == "ESQUERDA":
        x -= bloco
    elif direcao == "DIREITA":
        x += bloco
    nova_cabeca = (x, y)

    # Verifica colisões
    if nova_cabeca in cobra or x < 0 or x >= largura or y < 0 or y >= altura or nova_cabeca in obstaculos:
        rodando = False

    cobra.insert(0, nova_cabeca)

    # Comeu comida
    if cobra[0] == comida:
        comida = nova_comida()
        tempo_entre = time.time() - tempo_ultima_comida
        tempo_ultima_comida = time.time()
        if tempo_entre < 5:
            combo += 1
        else:
            combo = 0
        pontos += 10 + (combo * 2)

        # 20% de chance de aparecer comida dourada
        if random.random() < 0.2 and not comida_dourada:
            comida_dourada = nova_comida()
        
        # 10% de chance de criar obstáculo
        if random.random() < 0.1:
            obstaculos.append(nova_comida())
    elif comida_dourada and cobra[0] == comida_dourada:
        comida_dourada = None
        pontos += 50
    else:
        cobra.pop()

    # Desenhar
    desenhar_cobra()
    pygame.draw.rect(tela, VERMELHO, (*comida, bloco, bloco))
    if comida_dourada:
        pygame.draw.rect(tela, DOURADO, (*comida_dourada, bloco, bloco))
    desenhar_obstaculos()

    desenhar_texto(f"Pontos: {pontos}  Combo: x{combo}", 10, 10)
    if boost_duracao > 0:
        desenhar_texto("BOOST!", 10, 30, AZUL)
        boost_duracao -= 1
        velocidade = 20
    else:
        velocidade = velocidade_base

    pygame.display.update()
    clock.tick(velocidade)

pygame.quit()
