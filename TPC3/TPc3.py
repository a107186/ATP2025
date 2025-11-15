
import random

def menu():
    print("MENU:")
    print("(1) Criar Lista")
    print("(2) Ler Lista")
    print("(3) Soma")
    print("(4) Média")
    print("(5) Maior")
    print("(6) Menor")
    print("(7) Está ordenada por ordem crescente")
    print("(8) Está ordenada por ordem decrescente")
    print("(9) Procurar um elemento")
    print("(0) Sair")
    print("\nESCOLHA UMA OPÇÃO:")

def CRIAR_LISTA():
    tamanho = int(input("Qual é o tamanho da sua lista? "))
    lista = [random.randint(1, 100) for _ in range(tamanho)]
    print(f"Lista criada: {lista}")
    return lista

def ler_lista():
    lista = list(map(int, input("Digite os números separados por espaço: ").split()))
    print(f"Lista lida: {lista}")
    return lista

def soma(lista):
    if lista == []:
        print("É necessária a criação de uma lista. Por isso deve escolher a opção 1 ou 2.")
    else:
        print(lista)
        tamanho = len(lista)
        i = 0
        soma = 0
        while i < tamanho:
            num = lista[i]
            i += 1
            soma += num
        print(f"A soma é {soma}.")

def media_lista(lista):
    if lista == []:
        print("É necessária a criação de uma lista. Por isso deve escolher a opção 1 ou 2.")
    else:
        print(lista)
        tamanho = len(lista)
        i = 0
        soma = 0
        while i < tamanho:
            num = lista[i]
            i += 1
            soma += num
        media = soma / tamanho
        print(f"A média é {media}.")

def maior_lista(lista):
    if lista == []:
        print("É necessária a criação de uma lista. Por isso deve escolher a opção 1 ou 2.")
    else:
        print(lista)
        tamanho = len(lista)
        i = 1
        maior = lista[0]  
        while i < tamanho:
            num = lista[i]
            i += 1
            if num > maior:
                maior = num
        print(f"O maior número é {maior}.")

def menor_lista(lista):
    if lista == []:
        print("É necessária a criação de uma lista. Por isso deve escolher a opção 1 ou 2.")
    else:
        print(lista)
        tamanho = len(lista)
        i = 1
        menor = lista[0]  
        while i < tamanho:
            num = lista[i]
            i += 1
            if num < menor:
                menor = num
        print(f"O menor número é {menor}.")

def estaOrdenanda_por_ordem_crescente_lista(lista):
    if lista == []:
        print("É necessária a criação de uma lista. Por isso deve escolher a opção 1 ou 2.")
    else:
        print(lista)
        tamanho = len(lista) - 1
        i = 0
        while i < tamanho:
            if lista[i] > lista[i + 1]:
                print("NÃO!")
                return
            i += 1
        print("SIM!")

def estaOrdenanda_por_ordem_decrescente_lista(lista):
    if lista == []:
        print("É necessária a criação de uma lista. Por isso deve escolher a opção 1 ou 2.")
    else:
        print(lista)
        tamanho = len(lista) - 1
        i = 0
        while i < tamanho:
            if lista[i] < lista[i + 1]:
                print("NÃO!")
                return
            i += 1
        print("SIM!")

def procura_um_elemento_lista(lista):
    if lista == []:
        print("É necessária a criação de uma lista. Por isso deve escolher a opção 1 ou 2.")
    else:
        print(lista)
        tamanho = len(lista)
        i = 0
        elem = int(input("Introduza o elemento que pretende procurar: "))
        while i < tamanho:
            if lista[i] == elem:
                print(f"A posição do elemento {elem} é {i + 1}.")
                return
            i += 1
        print("A sua posição é -1.")

def main():
    lista = []
    continuar = True

    while continuar:
        menu()
        opcao = int(input("Opção: "))

        if opcao == 1:
            lista = CRIAR_LISTA()
        elif opcao == 2:
            lista = ler_lista()
        elif opcao == 3:
            soma(lista)
        elif opcao == 4:
            media_lista(lista)
        elif opcao == 5:
            maior_lista(lista)
        elif opcao == 6:
            menor_lista(lista)
        elif opcao == 7:
            estaOrdenanda_por_ordem_crescente_lista(lista)
        elif opcao == 8:
            estaOrdenanda_por_ordem_decrescente_lista(lista)
        elif opcao == 9:
            procura_um_elemento_lista(lista)
        elif opcao == 0:
            print(f"Lista final: {lista}")
            print("Aplicação terminada.")
            continuar = False
        else:
            print("Opção inválida! Tente novamente.")

if __name__ == "__main__":
    main()











       
    
    

    


    
