import socket
import pickle
import pygame
from pygame.locals import *

pygame.init()

WIDTH, HEIGHT = 500, 300
tela = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulador de Vida Online")

font = pygame.font.SysFont(None, 24)
clock = pygame.time.Clock()

nome = input("Digite seu nome: ")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 12345))
s.sendall(nome.encode())

def desenhar(jogadores):
    tela.fill((255, 255, 255))
    y = 20
    for j in jogadores.values():
        texto = f"{j.nome} | Fome: {j.fome} | Energia: {j.energia} | Dinheiro: ${j.dinheiro}"
        img = font.render(texto, True, (0, 0, 0))
        tela.blit(img, (20, y))
        y += 30
    pygame.display.flip()

rodando = True
while rodando:
    for event in pygame.event.get():
        if event.type == QUIT:
            rodando = False
        elif event.type == KEYDOWN:
            if event.key == K_c:
                s.sendall(pickle.dumps("comer"))
            elif event.key == K_t:
                s.sendall(pickle.dumps("trabalhar"))
            elif event.key == K_d:
                s.sendall(pickle.dumps("dormir"))

    dados = s.recv(4096)
    jogadores = pickle.loads(dados)
    desenhar(jogadores)
    clock.tick(30)

pygame.quit()
s.close()
