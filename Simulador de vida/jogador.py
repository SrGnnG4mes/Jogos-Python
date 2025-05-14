class Jogador:
    def __init__(self, nome):
        self.nome = nome
        self.fome = 100
        self.energia = 100
        self.dinheiro = 0

    def comer(self):
        if self.dinheiro >= 10:
            self.fome += 30
            self.dinheiro -= 10
            self.fome = min(100, self.fome)
        else:
            return "Sem dinheiro!"

    def dormir(self):
        self.energia += 40
        self.energia = min(100, self.energia)

    def trabalhar(self):
        self.energia -= 20
        self.fome -= 10
        self.dinheiro += 30
