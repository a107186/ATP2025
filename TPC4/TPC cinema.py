cinema = []


def inserirSala(cinema):
    filme = input("Introduza o nome do filme: ")
    existe = False
    for n in cinema:
        nlugares, vendidos, nome = n
        if nome == filme:
            existe = True
    if existe:
        print("O filme já existe")
    else:
        nlugares = int(input("Introduza o número de lugares na sala: "))
        vendidos = []
        cinema.append((nlugares, vendidos, filme))
        print("Sala criada")
    print("Salas:", cinema)
    menu()

def removerSala(cinema):
    index = int(input("Introduza o índice da sala: "))
    if 0 <= index < len(cinema):
        cinema.pop(index)
        print("Sala removida")
    else:
        print("Índice inválido")
    print("Salas:", cinema)
    menu()

def listarSalas(cinema):
    print("Sala           Filme")
    print("--------------------------")
    for p in cinema:
        nlugares, vendidos, filme = p
        print("Sala{}".format(cinema.index(p)), "   ", filme)
    menu()

def lugarDisponivel(cinema, filme, lugar):
    disponivel = False
    for p in cinema:
        nlugares, vendidos, nome = p
        if nome == filme and lugar not in vendidos:
            disponivel = True
    return disponivel

def vendebilhete(cinema, filme, lugar):
    for p in cinema:
        nlugares, vendidos, nome = p 
        if nome == filme:
            if lugarDisponivel(cinema, filme, lugar):
                vendidos.append(lugar)
                print("O lugar foi vendido")
            else:
                print("Lugar indisponível")
    print("Salas:", cinema)
    menu()

def listardisponibilidadesala(cinema):
    print("Sala  Filme  Lugares disponíveis")
    print("----------------------------------")
    for p in cinema:
        nlugares, vendidos, filme = p
        print("Sala{}".format(cinema.index(p)), " ", filme, " ", nlugares - len(vendidos))
    menu()

def menu():
    print("""
    -------------------
    1- Criar sala
    2- Remover sala
    3- Listar salas
    4- Lugar disponível
    5- Vender bilhete
    6- Consultar salas
    0- Sair
    ------------------- 
    """)

    opc = int(input("Escolha a opção de 0 a 6 do menu: "))
    if opc == 1:
        inserirSala(cinema)
    elif opc == 2:
        removerSala(cinema)
    elif opc == 3:
        listarSalas(cinema)
    elif opc == 4:
        filme = input("Introduza o nome do filme: ")
        lugar = int(input("Introduza o lugar: "))
        if lugarDisponivel(cinema, filme, lugar):
            print("Lugar disponível")
        else:
            print("Lugar indisponível")
    elif opc == 5:
        filme = input("Introduza o nome do filme: ")
        lugar = int(input("Introduza o lugar: "))
        vendebilhete(cinema, filme, lugar)
    elif opc == 6:
        listardisponibilidadesala(cinema)
    elif opc == 0:
        print("Reset efetuado com sucesso")
        print("Salas:", cinema)

menu()
