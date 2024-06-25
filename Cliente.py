from Conta import Conta
from Transacao import Transacao

class Cliente:
    
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacoes(self, conta):
        Transacao.registrar(conta)
        
    def adicionar_conta(self, conta):
        self.contas.append(conta)