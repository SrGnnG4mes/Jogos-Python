import socket
import threading
import pickle
from jogador import Jogador

HOST = '127.0.0.1'
PORT = 12345

jogadores = {}

def lidar_com_cliente(conn, addr):
    nome = conn.recv(1024).decode()
    jogador = Jogador(nome)
    jogadores[nome] = jogador

    while True:
        try:
            dados = conn.recv(4096)
            acao = pickle.loads(dados)

            if acao == "comer":
                jogador.comer()
            elif acao == "dormir":
                jogador.dormir()
            elif acao == "trabalhar":
                jogador.trabalhar()

            estado = pickle.dumps(jogadores)
            conn.sendall(estado)
        except:
            break

    print(f"{nome} saiu.")
    del jogadores[nome]
    conn.close()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print("Servidor rodando...")

    while True:
        conn, addr = s.accept()
        thread = threading.Thread(target=lidar_com_cliente, args=(conn, addr))
        thread.start()
