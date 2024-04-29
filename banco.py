menu = '[D]epositar [S]acar [E]xtrato [Q]sair: '

saldo = 0 
limite = 500
extrato = ''
numero_saques = 0
LIMITE_SAQUES = 3

while True:
    opcao = input(menu).lower()

    if opcao == 'd':
        valor = input('Valor a ser depositado: ')
        valor_float = float(valor)
        if valor_float > 0:
            saldo +=valor_float
        else:
            print('Digite um valor positivo.')
        extrato_msg = 'Deposito feito no valor de:R${:.2f}'.format(valor_float)
        extrato += extrato_msg
        continue
    elif opcao == 's':
        valor = input('Qual valor deseja sacar: ')
        valor_float = float(valor)
        if valor_float <= saldo:  
            if numero_saques < LIMITE_SAQUES:
                saldo -= valor_float
                numero_saques += 1
            else:
                print('Você nao contem mais saques diarios.')
                continue
        else:
            print('Você não contém saldo.')  
            continue  
        extrato_msg = '\nSaque feito no valor de:R${:.2f}'.format(valor_float)
        extrato += extrato_msg
        continue
    elif opcao == 'e':
        print(f'Saldo atual é de R${saldo:.2f}')
        print(extrato)
    elif opcao == 'q':
        break
    else:
        print("Digite uma opção valida")
    