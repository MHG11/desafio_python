from abc import ABC, abstractproperty, abstractclassmethod
import datetime
import textwrap

class ContasIterador:
    def __init__(self, contas):
        self.contas = contas
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        try:
            conta = self.contas[self._index]
            return f"""\
            Agência:\t{conta}
            Número:\t\t{conta.numero}
            Titular:\t{conta.cliente.nome}
            Saldo:\t\tR$ {conta.saldo:.2f}
        """
        except IndexError:
            raise StopIteration
        finally:
            self._index += 1


class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []
        self.indice_conta = 0

    def realizar_transacao(self, conta, transacao):
        if len(conta.historico.transacoes_do_dia()) >= 10:
            print('Você excedeu o número de transações diarias.')
            return
        
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)
        
class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf
        
        
class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        if valor > self._saldo:
            print("Saque não realizado, saldo insuficiente.")

        elif valor > 0:
            self._saldo -= valor
            return True
        else:
            print("Operação falhou, valor inválido.")
            return False
        
        return True

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("Deposito realizado com sucesso.")
        else:
            print("Operação falhou, valor inválido.")
            return False
        
        return True



class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len([transacao for transacao in self.historico.transacoes if transacao["tipo"] == "Saque"])

        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques >= self.limite_saques

        if excedeu_limite:
            print("Operação falhou, o valor do saque excede o limite.")
        elif excedeu_saques:
            print("Operação falhou, número máximo de saques excedido.")
        else:
            return super().sacar(valor)

        return False

    def __str__(self):
        return f"Agência: {self.agencia} C/c: {self.numero} Titular: {self.cliente.nome}"

class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self, conta):
        pass

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.datetime.now().strftime("%d-%m-%Y"),
            }
        )
    
    def gerar_relatorio(self, tipo_transacao=None):
        for transacao in self._transacoes:
            if tipo_transacao is None or transacao["tipo"].lower() == tipo_transacao.lower():
                yield transacao
    
    def transacoes_do_dia(self):
        data_atual = datetime.date()
        transacoes = []
        for transacao in self._transacoes:
            data_transacao = datetime.strptime(transacao["data"], "%d-%m-%Y %H:%M").date()
            if data_atual == data_transacao:
                transacoes.append(transacao)
        
        return transacoes
                    




class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

def log_sla(func):
    def log():
        func()
        agora = datetime.datetime.now()
        data_format = agora.strftime("%d/%m/%Y  %H:%M")
        print(f"Momento da expedição: {data_format}")
    
    return log 
    

def filtrar_clientes(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("Cliente não possui uma conta.")
        return None
    return cliente.contas[0]

 
def sacar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_clientes(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado.")
        return

    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)

 
def depositar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_clientes(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado.")
        return

    valor = float(input("Informe o valor do depósito: "))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)

def menu():
    menu = """
    ---------MENU---------
    [D]epositar
    [S]acar
    [E]xtrato
    [Q]sair
    [C]adastrar cliente
    [L]istar contas
    [N]ova conta 
    ----------------------
    = """
    return input(textwrap.dedent(menu))

 
def cadastros(clientes):
    cpf = input("Digite o CPF: ")
    usuario = filtrar_clientes(cpf, clientes)

    if usuario:
        print("Já existe um usuário com esse CPF.")
        return

    nome = input("Digite o nome: ")
    dataNascimento = input("Digite sua data de nascimento: ")
    endereco = input("Digite o endereço: ")

    cliente = PessoaFisica(nome, dataNascimento, cpf, endereco)
    clientes.append(cliente)
    print("Cliente criado com sucesso.")

def criar_conta(contas, numero_conta, clientes):
    cpf = input("Informe o CPF do usuário: ")
    cliente = filtrar_clientes(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado.")
        return None

    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    cliente.adicionar_conta(conta)
    return conta

def listar_contas(contas):
    for conta in ContasIterador(contas):
        print("=" * 100)
        print(textwrap.dedent(str(conta)))

 
def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_clientes(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado.")
        return

    conta = recuperar_conta_cliente(cliente)

    if not conta:
        return

    print('--------------------EXTRATO--------------------')
    transacoes = conta.historico.transacoes

    extrato = ""

    if not transacoes:
        extrato = "Não foram realizadas movimentações."
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['data']}\n{transacao['tipo']}: R${transacao['valor']:.2f}"

    print(extrato)
    print(f"Saldo: R$ {conta.saldo:.2f}")
    print('-----------------------------------------------')

def main():
    clientes = []
    contas = []

    while True:
        opcao = menu().lower()

        if opcao == 'd':
            depositar(clientes)
        elif opcao == 's':
            sacar(clientes)
        elif opcao == 'e':
            exibir_extrato(clientes)
        elif opcao == 'q':
            break
        elif opcao == 'c':
            cadastros(clientes)
        elif opcao == 'l':
            listar_contas(contas)
        elif opcao == 'n':
            numero_conta = len(contas) + 1
            criar_conta(contas, numero_conta, clientes)
        else:
            print("Digite uma opção válida.")

main()
