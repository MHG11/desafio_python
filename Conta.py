import textwrap
from Cliente import Cliente
from Historico import Historico
class Conta:
   
    def __init__(self, saldo, numero, agencia, cliente, historico):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()
        
    @classmethod    
    def nova_conta(cls, cliente, numero):
        return cls(cliente, numero)
    
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
        saldo = self.saldo
        excedeu_saldo = valor  > saldo
        
        if excedeu_saldo:
            print("Saldo excedido, saque não realizado.")
        
        elif valor > 0:
            self._saldo -= valor
            print("\nSaque realizado com sucesso!!")
            return True
        
        else:
            print("\nOperação falhou.")
        
        return False
    
    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("Deposito realizado com sucesso!")
        else:
            print("Operação falhou, valor informado invalido.")
    
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
        usuario = filtrar_clientes(cpf,clientes)
        
        if usuario:
            print("Já existe usuários com esse cpf")
            return
        
        nome = input("Digite o nome: ")
        dataNascimento = input('Digite sua data de nascimento: ')
        end = input("Digite o endereço: ")
        
        clientes.append({"nome":nome, "Data Nascimento":dataNascimento, "cpf":cpf, "endereço":end})
        print('clientes criado com sucesso')

    def filtrar_clientes(cpf, clientes):
        clientes_filtrados = [clientes for clientes in clientes if clientes["cpf"] == cpf]
        return clientes_filtrados[0] if clientes_filtrados else None

    def deposito(self, valor):
        if valor > 0:
            saldo +=valor
        else:
            return'Digite um valor positivo.'
        extrato_msg = 'Deposito feito no valor de:R${:.2f}'.format(valor)
        extrato += extrato_msg
        return saldo, extrato
    
    def saque(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo
        
        
        if excedeu_saldo:  
            print("Saque nao realizado, saldo excedido")
        
        elif valor > 0:
            self._saldo -= valor
            print("Saque feito com sucesso!!")
            return True
        
        else:
            print("Operação falhou.")
            
        return False

    def criar_conta(agencia, numero_conta, clientes):
        cpf = input("Informe o CPF do usuário: ")
        clientes = filtrar_clientes(cpf, clientes)

        if clientes:
            print("\n=== Conta criada com sucesso! ===")
            return {"agencia": agencia, "numero_conta": numero_conta, "clientes": clientes}

    

    

    

    def listar_contas(contas):
        for conta in contas:
            linha = f"""\
                Agência:\t{conta['agencia']}
                C/C:\t\t{conta['numero_conta']}
                Titular:\t{conta['clientes']['nome']}
            """
            print("=" * 100)
            print(textwrap.dedent(linha))

    def main():
        
        while True:
        
            opcao = menu()

            if opcao == 'd':
                valor = float(input('Valor a ser depositado: '))
                
                saldo, extrato = deposito(saldo, valor, extrato)
                
                continue
            elif opcao == 's':
                valor = float(input('Qual valor deseja sacar: '))

                saldo, extrato = saque(saldo=saldo,
                                    valor=valor,
                                    limite=limite,
                                    numero_saques=numero_saques,
                                    LIMITE_SAQUES=LIMITE_SAQUES,
                                    extrato=extrato)
                continue
            elif opcao == 'e':
                extrato_imprimir(saldo,extrato=extrato)
            elif opcao == 'q':
                break
            elif opcao == 'c':
                cadastros(clientes)
            elif opcao == 'l':
                listar_contas(contas)
                
            elif opcao == 'n':
                numero_conta = len(contas)+1
                conta = criar_conta(AGENCIA,numero_conta,clientes)
                if conta:
                    contas.append(conta)
            else:
                print("Digite uma opção valida")

    main()
    