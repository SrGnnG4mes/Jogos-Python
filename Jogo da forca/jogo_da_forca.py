import tkinter as tk
import random

def carregar_palavras_organizadas():
    temas = {}
    tema_atual = "Geral"
    try:
        with open("palavras.txt", "r", encoding="utf-8") as f:
            for linha in f:
                linha = linha.strip()
                if not linha:
                    continue
                if linha.lower().startswith("# tema:"):
                    tema_atual = linha[7:].strip().capitalize()
                    temas[tema_atual] = []
                else:
                    temas.setdefault(tema_atual, []).append(linha.lower())
    except FileNotFoundError:
        temas = {
            "Padrão": ["python", "computador", "teclado", "internet"]
        }
    return temas

class JogoForca:
    def __init__(self, root):
        self.root = root
        self.root.title("Jogo da Forca")
        self.root.configure(bg="#1e1e1e")

        self.temas = carregar_palavras_organizadas()
        self.tema_escolhido = None
        self.palavras_usadas = {}
        self.dificuldade = 1

        self.root.bind("<Key>", self.tecla_pressionada)
        self.menu_temas()

    def menu_temas(self):
        self.limpar_tela()
        tk.Label(self.root, text="Escolha um Tema", font=("Arial", 20), fg="white", bg="#1e1e1e").pack(pady=10)
        for tema in self.temas.keys():
            tk.Button(self.root, text=tema, font=("Arial", 14), width=20,
                      command=lambda t=tema: self.salvar_tema_e_abrir_dificuldade(t),
                      bg="#00AAFF", fg="white").pack(pady=5)

    def salvar_tema_e_abrir_dificuldade(self, tema):
        self.tema_escolhido = tema
        if tema not in self.palavras_usadas:
            self.palavras_usadas[tema] = []
        self.menu_dificuldade()

    def menu_dificuldade(self):
        self.limpar_tela()
        tk.Label(self.root, text=f"Tema escolhido: {self.tema_escolhido}", font=("Arial", 18), fg="white", bg="#1e1e1e").pack(pady=5)
        tk.Label(self.root, text="Escolha a Dificuldade", font=("Arial", 20), fg="white", bg="#1e1e1e").pack(pady=10)

        dificuldades = [("Fácil", 1), ("Médio", 2), ("Difícil", 3)]
        for nome, nivel in dificuldades:
            tk.Button(self.root, text=nome, font=("Arial", 14), width=20,
                      command=lambda n=nivel: self.iniciar_com_dificuldade(n),
                      bg="#00CC88", fg="white").pack(pady=5)

    def iniciar_com_dificuldade(self, nivel):
        self.dificuldade = nivel
        self.novo_jogo()

    def escolher_palavra(self):
        todas = self.temas[self.tema_escolhido]
        usadas = self.palavras_usadas[self.tema_escolhido]

        if self.dificuldade == 1:
            filtradas = [p for p in todas if len(p) <= 5]
        elif self.dificuldade == 2:
            filtradas = [p for p in todas if 6 <= len(p) <= 8]
        else:
            filtradas = [p for p in todas if len(p) > 8]

        opcoes = [p for p in filtradas if p not in usadas]
        if not opcoes:
            usadas.clear()
            opcoes = filtradas or todas

        palavra = random.choice(opcoes) if opcoes else random.choice(todas)
        usadas.append(palavra)
        return palavra

    def novo_jogo(self):
        self.palavra = self.escolher_palavra()
        self.letras_certas = []
        self.letras_erradas = []
        self.tentativas = 6

        self.limpar_tela()

        titulo = f"Tema: {self.tema_escolhido} | Dificuldade: {['Fácil', 'Médio', 'Difícil'][self.dificuldade - 1]}"
        self.label_titulo = tk.Label(self.root, text=titulo, font=("Arial", 20), fg="white", bg="#1e1e1e")
        self.label_titulo.pack(pady=10)

        self.label_palavra = tk.Label(self.root, text=self.formatar_palavra(), font=("Courier", 32), fg="#00FFAA", bg="#1e1e1e")
        self.label_palavra.pack(pady=10)

        self.label_tentativas = tk.Label(self.root, text=f"Tentativas restantes: {self.tentativas}", font=("Arial", 14), fg="white", bg="#1e1e1e")
        self.label_tentativas.pack(pady=5)

        self.label_erros = tk.Label(self.root, text="", font=("Arial", 14), fg="#FF6666", bg="#1e1e1e")
        self.label_erros.pack(pady=5)

        self.frame_teclado = tk.Frame(self.root, bg="#1e1e1e")
        self.frame_teclado.pack(pady=10)

        self.letras_botoes = {}
        for i, letra in enumerate("abcdefghijklmnopqrstuvwxyz"):
            btn = tk.Button(self.frame_teclado, text=letra.upper(), width=4, height=2,
                            font=("Arial", 12), command=lambda l=letra: self.tentar_letra(l),
                            bg="#333", fg="white", activebackground="#555")
            btn.grid(row=i // 9, column=i % 9, padx=2, pady=2)
            self.letras_botoes[letra] = btn

    def formatar_palavra(self):
        return " ".join([letra if letra in self.letras_certas else "_" for letra in self.palavra])

    def tentar_letra(self, letra):
        if letra in self.letras_certas or letra in self.letras_erradas:
            return

        self.letras_botoes[letra]["state"] = "disabled"

        if letra in self.palavra:
            self.letras_certas.append(letra)
        else:
            self.letras_erradas.append(letra)
            self.tentativas -= 1

        self.atualizar_interface()
        self.verificar_fim()

    def tecla_pressionada(self, event):
        letra = event.char.lower()
        if letra in "abcdefghijklmnopqrstuvwxyz":
            self.tentar_letra(letra)

    def atualizar_interface(self):
        self.label_palavra.config(text=self.formatar_palavra())
        self.label_tentativas.config(text=f"Tentativas restantes: {self.tentativas}")
        self.label_erros.config(text="Letras erradas: " + ", ".join(self.letras_erradas))

    def verificar_fim(self):
        if all(letra in self.letras_certas for letra in self.palavra):
            self.fim_jogo(vitoria=True)
        elif self.tentativas <= 0:
            self.fim_jogo(vitoria=False)

    def fim_jogo(self, vitoria):
        for btn in self.letras_botoes.values():
            btn["state"] = "disabled"

        msg = "🎉 Parabéns! Você venceu!" if vitoria else f"💀 Fim de jogo! A palavra era: {self.palavra}"
        cor = "#00FF00" if vitoria else "#FF3333"
        self.label_resultado = tk.Label(self.root, text=msg, font=("Arial", 18), fg=cor, bg="#1e1e1e")
        self.label_resultado.pack(pady=10)

        btn_novo = tk.Button(self.root, text="🔄 Jogar Novamente", font=("Arial", 14),
                             command=self.novo_jogo, bg="#00AAFF", fg="white")
        btn_novo.pack(pady=5)

        btn_tema = tk.Button(self.root, text="📚 Mudar Tema", font=("Arial", 12),
                             command=self.menu_temas, bg="#444", fg="white")
        btn_tema.pack(pady=2)

    def limpar_tela(self):
        for widget in self.root.winfo_children():
            widget.destroy()

# Execução
if __name__ == "__main__":
    root = tk.Tk()
    jogo = JogoForca(root)
    root.mainloop()
