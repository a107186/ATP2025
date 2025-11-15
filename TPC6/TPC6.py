import matplotlib.pyplot as plt

# Código original fornecido
def medias(tabMeteo):
    res = []
    for data, tmin, tmax, precip in tabMeteo:
        res.append((data, (tmin + tmax) / 2))
    return res

def guardaTabMeteo(t, fnome):
    f = open(fnome, "w")
    for data, tmin, tmax, precip in t:
        linha = f"{data[0]}::{data[1]}::{data[2]}::{tmin}::{tmax}::{precip}\n"
        f.write(linha)
    f.close()
    return len(t)

def carregaTabMeteo(fnome):
    res = []
    f = open(fnome)
    for linha in f:
        campos = linha.split('::')
        data = (int(campos[0]), int(campos[1]), int(campos[2]))
        res.append((data, float(campos[3]), float(campos[4]), float(campos[5])))
    f.close()
    return res

def minMin(tabMeteo):
    minima = tabMeteo[0][1]
    for data, tmin, tmax, precip in tabMeteo[1:]:
        if tmin < minima:
            minima = tmin
    return minima

def amplTerm(tabMeteo):
    res = []
    for data, tmin, tmax, _ in tabMeteo:
        res.append((data, tmax - tmin))
    return res

def maxChuva(tabMeteo):
    max_prec = tabMeteo[0][3]
    max_data = tabMeteo[0][0]
    for dia in tabMeteo:
        if dia[3] > max_prec and dia[0] != max_data:
            max_prec = dia[3]
            max_data = dia[0]
    return (max_data, max_prec)

def diasChuva(tabMeteo, p):
    dias_chuvosos = []
    for data, tmin, tmax, precip in tabMeteo:
        if precip > p:
            dias_chuvosos.append((data, precip))
    return dias_chuvosos

def maxPeriodoCalor(tabMeteo, p):
    consecutivos = 0
    consecutivos_global = 0
    for dias in tabMeteo:
        if dias[3] < p:
            consecutivos += 1
        else:
            if consecutivos_global < consecutivos:
                consecutivos_global = consecutivos
            consecutivos = 0

    if consecutivos_global < consecutivos:
        consecutivos_global = consecutivos

    return consecutivos_global

def graficosMeteo(tabMeteo):
    datas = [f"{data[2]}/{data[1]}/{data[0]}" for data, _, _, _ in tabMeteo]
    temperaturas_minimas = [tmin for _, tmin, _, _ in tabMeteo]
    temperaturas_maximas = [tmax for _, _, tmax, _ in tabMeteo]
    precipitacao = [precip for _, _, _, precip in tabMeteo]

    fig, ax1 = plt.subplots()

    ax1.set_xlabel('Data')
    ax1.set_ylabel('Temperatura (ºC)')
    ax1.plot(datas, temperaturas_minimas, color='blue', label='Temp. Mínima')
    ax1.plot(datas, temperaturas_maximas, color='red', label='Temp. Máxima')
    ax1.tick_params(axis='y')
    ax1.legend(loc='upper left')

    ax2 = ax1.twinx()
    ax2.set_ylabel('Precipitação (mm)')
    ax2.bar(datas, precipitacao, color='green', alpha=0.3, label='Precipitação')
    ax2.tick_params(axis='y')
    ax2.legend(loc='upper right')

    fig.tight_layout()
    plt.xticks(rotation=45)
    plt.show()

# Menu interativo
def menu():
    print("""
    --- Menu Meteorologia ---
    1. Calcular médias das temperaturas (mínima e máxima)
    2. Guardar dados meteorológicos em ficheiro
    3. Carregar dados meteorológicos de ficheiro
    4. Calcular temperatura mínima global
    5. Calcular amplitude térmica diária
    6. Determinar o dia com maior precipitação
    7. Listar dias com precipitação superior a um valor
    8. Calcular maior período de calor (precipitação < limite)
    9. Gerar gráficos meteorológicos
    0. Sair
    """)

# Programa principal
def main():
    tabMeteo = []  # Inicializar a tabela de dados meteorológicos

    while True:
        menu()
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            if tabMeteo:
                print("Médias das temperaturas:", medias(tabMeteo))
            else:
                print("Sem dados meteorológicos carregados.")

        elif opcao == "2":
            if tabMeteo:
                nome_ficheiro = input("Nome do ficheiro para guardar (ex: meteorologia.txt): ")
                n = guardaTabMeteo(tabMeteo, nome_ficheiro)
                print(f"{n} registos guardados no ficheiro '{nome_ficheiro}'.")
            else:
                print("Sem dados meteorológicos carregados.")

        elif opcao == "3":
            nome_ficheiro = input("Nome do ficheiro para carregar (ex: meteorologia.txt): ")
            tabMeteo = carregaTabMeteo(nome_ficheiro)
            print("Dados meteorológicos carregados com sucesso.")

        elif opcao == "4":
            if tabMeteo:
                print(f"A temperatura mínima registrada foi: {minMin(tabMeteo)} ºC")
            else:
                print("Sem dados meteorológicos carregados.")

        elif opcao == "5":
            if tabMeteo:
                print("Amplitudes térmicas diárias:", amplTerm(tabMeteo))
            else:
                print("Sem dados meteorológicos carregados.")

        elif opcao == "6":
            if tabMeteo:
                data_prec, max_prec = maxChuva(tabMeteo)
                print(f"O dia com maior precipitação foi {data_prec} com {max_prec} mm.")
            else:
                print("Sem dados meteorológicos carregados.")

        elif opcao == "7":
            if tabMeteo:
                p = float(input("Insira o limite de precipitação: "))
                print("Dias com precipitação superior ao limite:", diasChuva(tabMeteo, p))
            else:
                print("Sem dados meteorológicos carregados.")

        elif opcao == "8":
            if tabMeteo:
                p = float(input("Insira o limite de precipitação para considerar período seco: "))
                print(f"O maior período seco foi de {maxPeriodoCalor(tabMeteo, p)} dias consecutivos.")
            else:
                print("Sem dados meteorológicos carregados.")

        elif opcao == "9":
            if tabMeteo:
                graficosMeteo(tabMeteo)
            else:
                print("Sem dados meteorológicos carregados.")

        elif opcao == "0":
            print("Saindo da aplicação. Até breve!")
            break

        else:
            print("Opção inválida. Tente novamente.")

# Executar aplicação
if __name__ == "__main__":
    main()
