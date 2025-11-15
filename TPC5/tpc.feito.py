

#   Funções auxiliares
def criar_turma():
    print("Turma criada com sucesso.")
    return []

def inserir_aluno(turma):
    nome = input("Nome do aluno: ")
    id_aluno = int(input("ID do aluno: "))
    
    # Verificação para IDs únicos
    while any(id_aluno == aluno[1] for aluno in turma):
        print("Já existe um aluno com esse ID.")
        id_aluno = int(input("Introduza o ID do aluno: "))

    # Validação das notas
    notaTPC = float(input("Nota do TPC: "))
    while notaTPC < 0 or notaTPC > 20:
        print("Nota inválida. (Nota deve estar entre 0 e 20 valores)")
        notaTPC = float(input("Nota do TPC: "))
    
    notaProj = float(input("Nota do Projeto: "))
    while notaProj < 0 or notaProj > 20:
        print("Nota inválida. (Nota deve estar entre 0 e 20 valores)")
        notaProj = float(input("Nota do Projeto: "))

    notaTeste = float(input("Nota do Teste: "))
    while notaTeste < 0 or notaTeste > 20:
        print("Nota inválida. (Nota deve estar entre 0 e 20 valores)")
        notaTeste = float(input("Nota do Teste: "))

    aluno = (nome, id_aluno, [notaTPC, notaProj, notaTeste])
    turma.append(aluno)
    print(f"Aluno {nome} inserido com sucesso!")

def listar_turma(turma):
    if not turma:
        print("A turma está vazia.")
    else:
        print("Listagem dos alunos da turma:")
        for aluno in turma:
            nome, id_aluno, notas = aluno
            print(f"Nome: {nome}, ID: {id_aluno}, Notas: {notas}")

def consultar_aluno(turma):
    id_aluno = int(input("ID do aluno a consultar: "))
    for aluno in turma:
        if aluno[1] == id_aluno:
            print(f"Aluno encontrado: Nome: {aluno[0]}, Notas: {aluno[2]}")
            return
    print(f"O aluno com o ID {id_aluno} não se encontra na turma.")

# Converte o aluno (tuplo) para uma linha de texto
def linha(aluno):
    nome, id_aluno, notas = aluno
    return f"{nome},{id_aluno},{notas[0]},{notas[1]},{notas[2]}\n"

def guardar_turma(turma, nome_ficheiro="turma.txt"):
    with open(nome_ficheiro, "w") as file:
        for aluno in turma:
            file.write(linha(aluno))
    print(f"Turma guardada no ficheiro '{nome_ficheiro}'.")

def carregar_turma(nome_ficheiro="turma.txt"):
    try:
        turma = []
        with open(nome_ficheiro, 'r') as file:
            for linha in file:
                dados = linha.strip().split(',')
                if len(dados) == 5:
                    nome, id_aluno, notaTPC, notaProj, notaTeste = dados
                    aluno = (nome, int(id_aluno), [float(notaTPC), float(notaProj), float(notaTeste)])
                    turma.append(aluno)
        print(f"Turma carregada do ficheiro '{nome_ficheiro}'.")
        return turma
    except FileNotFoundError:
        print(f"Ficheiro '{nome_ficheiro}' não encontrado.")
        return criar_turma()
    except ValueError:
        print("Erro ao processar o ficheiro. Verifique o formato dos dados.")
        return criar_turma()

def menu():
    print("""
    1. Criar Turma
    2. Inserir aluno
    3. Listar turma
    4. Consultar aluno por ID
    5. Guardar turma em ficheiro
    6. Carregar turma dum ficheiro
    0. Sair da aplicação
    """)
    opcao = input("Escolha uma opção: ")
    return opcao

# Função principal
def main():
    turma = criar_turma()
    while True:
        opcao = menu()

        if opcao == "1":
            turma = criar_turma()
        elif opcao == "2":
            inserir_aluno(turma)
        elif opcao == "3":
            listar_turma(turma)
        elif opcao == "4":
            consultar_aluno(turma)
        elif opcao == "5":
            guardar_turma(turma)
        elif opcao == "6":
            turma = carregar_turma()
        elif opcao == "0":
            print("Saindo da aplicação.")
            break
        else:
            print("Opção inválida! Tente novamente.")

# Executar a aplicação
if __name__ == "__main__":
    main()
