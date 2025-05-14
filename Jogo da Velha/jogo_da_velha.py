import tkinter as tk
from tkinter import messagebox
import random

class JogoDaVelha:
    def __init__(self, root):
        self.root = root
        self.root.title("Jogo da Velha 🤖🧠")
        self.jogador = "X"
        self.vs_ia = False
        self.dificuldade = "dificil"
        self.botoes = [[None for _ in range(3)] for _ in range(3)]
        self.placar = {"X": 0, "O": 0, "Empates": 0}
        self.menu_inicial()

    def menu_inicial(self):
        self.frame_menu = tk.Frame(self.root, bg="#222")
        self.frame_menu.pack(padx=20, pady=20)

        tk.Label(self.frame_menu, text="Escolha o modo de jogo:", font=("Arial", 16), fg="white", bg="#222").pack(pady=10)
        tk.Button(self.frame_menu, text="Jogador vs Jogador", font=("Arial", 14),
                  command=self.iniciar_pvp, bg="#4CAF50", fg="white", width=25).pack(pady=5)

        tk.Label(self.frame_menu, text="Jogador vs IA", font=("Arial", 14), fg="white", bg="#222").pack(pady=(15, 5))
        tk.Button(self.frame_menu, text="Fácil", font=("Arial", 12),
                  command=lambda: self.iniciar_vs_ia("facil"), bg="#9E9E9E", fg="white", width=20).pack(pady=2)
        tk.Button(self.frame_menu, text="Médio", font=("Arial", 12),
                  command=lambda: self.iniciar_vs_ia("medio"), bg="#FFC107", fg="black", width=20).pack(pady=2)
        tk.Button(self.frame_menu, text="Difícil", font=("Arial", 12),
                  command=lambda: self.iniciar_vs_ia("dificil"), bg="#F44336", fg="white", width=20).pack(pady=2)

    def iniciar_pvp(self):
        self.vs_ia = False
        self.frame_menu.destroy()
        self.criar_interface()

    def iniciar_vs_ia(self, nivel):
        self.vs_ia = True
        self.dificuldade = nivel
        self.frame_menu.destroy()
        self.criar_interface()

    def criar_interface(self):
        self.frame_jogo = tk.Frame(self.root, bg="#111")
        self.frame_jogo.pack()

        self.label_placar = tk.Label(self.root, text="", font=("Arial", 14), bg="#111", fg="white")
        self.label_placar.pack(pady=10)
        self.atualizar_placar()

        for linha in range(3):
            for coluna in range(3):
                btn = tk.Button(self.frame_jogo, text="", font=("Arial", 36), width=5, height=2,
                                command=lambda l=linha, c=coluna: self.clique(l, c),
                                bg="#333", fg="white", activebackground="#555")
                btn.grid(row=linha, column=coluna, padx=2, pady=2)
                self.botoes[linha][coluna] = btn

    def clique(self, linha, coluna):
        btn = self.botoes[linha][coluna]
        if btn["text"] == "":
            btn["text"] = self.jogador
            if self.verificar_vitoria():
                self.placar[self.jogador] += 1
                messagebox.showinfo("Fim de Jogo", f"Jogador {self.jogador} venceu!")
                self.reiniciar()
                return
            elif self.verificar_empate():
                self.placar["Empates"] += 1
                messagebox.showinfo("Fim de Jogo", "Empate!")
                self.reiniciar()
                return
            self.jogador = "O" if self.jogador == "X" else "X"
            if self.vs_ia and self.jogador == "O":
                self.root.after(300, self.jogada_ia)

    def jogada_ia(self):
        if self.dificuldade == "facil":
            self.jogada_aleatoria()
        elif self.dificuldade == "medio":
            if random.random() < 0.5:
                self.jogada_aleatoria()
            else:
                self.jogada_minimax()
        else:
            self.jogada_minimax()

    def jogada_aleatoria(self):
        opcoes = [(i, j) for i in range(3) for j in range(3) if self.botoes[i][j]["text"] == ""]
        if opcoes:
            i, j = random.choice(opcoes)
            self.botoes[i][j]["text"] = "O"
            if self.verificar_vitoria():
                self.placar["O"] += 1
                messagebox.showinfo("Fim de Jogo", "IA venceu!")
                self.reiniciar()
            elif self.verificar_empate():
                self.placar["Empates"] += 1
                messagebox.showinfo("Fim de Jogo", "Empate!")
                self.reiniciar()
            else:
                self.jogador = "X"

    def jogada_minimax(self):
        melhor_pontuacao = -float("inf")
        melhor_jogada = None

        for i in range(3):
            for j in range(3):
                if self.botoes[i][j]["text"] == "":
                    self.botoes[i][j]["text"] = "O"
                    pontuacao = self.minimax(0, False)
                    self.botoes[i][j]["text"] = ""
                    if pontuacao > melhor_pontuacao:
                        melhor_pontuacao = pontuacao
                        melhor_jogada = (i, j)

        if melhor_jogada:
            i, j = melhor_jogada
            self.botoes[i][j]["text"] = "O"
            if self.verificar_vitoria():
                self.placar["O"] += 1
                messagebox.showinfo("Fim de Jogo", "IA venceu!")
                self.reiniciar()
            elif self.verificar_empate():
                self.placar["Empates"] += 1
                messagebox.showinfo("Fim de Jogo", "Empate!")
                self.reiniciar()
            else:
                self.jogador = "X"

    def minimax(self, profundidade, is_maximizando):
        vencedor = self.checar_vencedor()
        if vencedor == "O":
            return 1
        elif vencedor == "X":
            return -1
        elif self.verificar_empate():
            return 0

        if is_maximizando:
            melhor = -float("inf")
            for i in range(3):
                for j in range(3):
                    if self.botoes[i][j]["text"] == "":
                        self.botoes[i][j]["text"] = "O"
                        pontuacao = self.minimax(profundidade + 1, False)
                        self.botoes[i][j]["text"] = ""
                        melhor = max(melhor, pontuacao)
            return melhor
        else:
            melhor = float("inf")
            for i in range(3):
                for j in range(3):
                    if self.botoes[i][j]["text"] == "":
                        self.botoes[i][j]["text"] = "X"
                        pontuacao = self.minimax(profundidade + 1, True)
                        self.botoes[i][j]["text"] = ""
                        melhor = min(melhor, pontuacao)
            return melhor

    def checar_vencedor(self):
        b = self.botoes
        for i in range(3):
            if b[i][0]["text"] == b[i][1]["text"] == b[i][2]["text"] != "":
                return b[i][0]["text"]
            if b[0][i]["text"] == b[1][i]["text"] == b[2][i]["text"] != "":
                return b[0][i]["text"]
        if b[0][0]["text"] == b[1][1]["text"] == b[2][2]["text"] != "":
            return b[0][0]["text"]
        if b[0][2]["text"] == b[1][1]["text"] == b[2][0]["text"] != "":
            return b[0][2]["text"]
        return None

    def verificar_vitoria(self):
        return self.checar_vencedor() is not None

    def verificar_empate(self):
        for linha in self.botoes:
            for btn in linha:
                if btn["text"] == "":
                    return False
        return self.checar_vencedor() is None

    def reiniciar(self):
        for linha in self.botoes:
            for btn in linha:
                btn["text"] = ""
        self.jogador = "X"
        self.atualizar_placar()
        if self.vs_ia and self.jogador == "O":
            self.root.after(300, self.jogada_ia)

    def atualizar_placar(self):
        self.label_placar.config(
            text=f"Placar – X: {self.placar['X']} | O: {self.placar['O']} | Empates: {self.placar['Empates']}"
        )

# Início
if __name__ == "__main__":
    root = tk.Tk()
    root.configure(bg="#111")
    jogo = JogoDaVelha(root)
    root.mainloop()
