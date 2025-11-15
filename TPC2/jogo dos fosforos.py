import random

def jogador_primeiro():
    fosforos = 21
    while fosforos > 1:
        jogador = int(input(f"Há {fosforos} fósforos. Quantos deseja retirar (1-4)? "))
        while (jogador < 1 or jogador > 4) or jogador > fosforos:
            jogador = int(input("Entrada inválida. Escolha um valor entre 1 e 4 que não exceda o número de fósforos restantes: "))
            
        fosforos -= jogador

        computador = 5 - jogador
        fosforos -= computador
        print(f"O computador retirou {computador} fósforos.")
    print('Perdeste!')



def computador_primeiro():
    fosforos = 21

    while fosforos > 0:
        # Turno do computador
        computador = (fosforos - 1) % 5
        if computador == 0 or computador > fosforos:
            computador = random.randint(1, min(4, fosforos))

        fosforos -= computador
        print(f"O computador retirou {computador} fósforos.")

      
        if fosforos == 1:
            print("Sobrou apenas 1 fósforo. O computador ganhou!")
            return  # Encerra a função se o computador perder

        # Turno do jogador
        jogador = int(input(f"Há {fosforos} fósforos. Quantos deseja retirar (1-4)? "))
        while jogador < 1 or jogador > 4 or jogador > fosforos:
            jogador = int(input("Entrada inválida. Escolha um valor entre 1 e 4 que não exceda o número de fósforos restantes: "))
  
        fosforos -= jogador
        if fosforos == 1:
            print("Sobrou 1 fósforo. Ganhaste!")
            return        

def main():
    print("Bem-vindo ao jogo dos 21 fósforos!")
    modo = ''
    while modo != '3':
        modo = input("Escolha o modo de jogo:\n1 - Jogador começa\n2 - Computador começa\n3 - Sair do jogo\nEscolha: ")
        if modo == '1':
            jogador_primeiro()
            modo = input("Escolha o modo de jogo:\n1 - Jogador começa\n2 - Computador começa\n3 - Sair do jogo\nEscolha: ")
        elif modo == '2':
            computador_primeiro()
            modo = input("Escolha o modo de jogo:\n1 - Jogador começa\n2 - Computador começa\n3 - Sair do jogo\nEscolha: ")
        elif modo == '3':
            print("Saindo do jogo. Até a próxima!")
        else:
            print("Modo inválido. Por favor, escolha 1, 2 ou 3.")
    


main()
