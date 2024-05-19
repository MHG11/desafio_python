import textwrap

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

def deposito(saldo,valor, extrato,/):
    if valor > 0:
         saldo +=valor
    else:
        return'Digite um valor positivo.'
    extrato_msg = 'Deposito feito no valor de:R${:.2f}'.format(valor)
    extrato += extrato_msg
    return saldo, extrato

def criar_conta(agencia, numero_conta, clientes):
    cpf = input("Informe o CPF do usuário: ")
    clientes = filtrar_clientes(cpf, clientes)

    if clientes:
        print("\n=== Conta criada com sucesso! ===")
        return {"agencia": agencia, "numero_conta": numero_conta, "clientes": clientes}

   

def saque(*,saldo,valor,numero_saques,LIMITE_SAQUES, extrato):
    
    if valor <= saldo:  
        if numero_saques < LIMITE_SAQUES:
            saldo -= valor
            numero_saques += 1
        else:
            return'Você nao contem mais saques diarios.'
    else:
        return'Você não contém saldo.'
    
    extrato_msg = '\nSaque feito no valor de:R${:.2f}'.format(valor)
    extrato+= extrato_msg
    return saldo, extrato

def extrato_imprimir(saldo,/,*, extrato):
    print(f'Saldo atual é de R${saldo:.2f}')

    return saldo, extrato

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
    LIMITE_SAQUES=3
    AGENCIA="0001"
    contas = []
    clientes = []
    saldo = 0.0
    limite = 500
    extrato = ''
    numero_saques = 0
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
    