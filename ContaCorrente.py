from Conta import Conta
from Cliente import Cliente
from Historico import Historico
class ContaCorrente(Conta):
    def __init__(self, numero, cliente , limite=500, 
                 limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques
        
        def sacar(self, valor):
            numero_saques = len([transacao for transacao in self.historico.tansacoes if transacao["tipo"] == "Saque"])
            
            excedeu_limite = valor > self.limite
            excedeu_saques = numero_saques >= self.limite_saques
            
            if excedeu_limite:
                print("Operação falhou, o valor do saque excede o limite.")
            elif excedeu_saques:
                print("Operação falhou Número maximo de saques excedido.")
                
            else:
                return super().sacar(valor)
            
            return False
        
    def __str__(self):
        return f"Agência: {self.agencia} C/c: {self.numero}Titular: {self.cliente.nome} "