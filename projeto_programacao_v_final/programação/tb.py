import FreeSimpleGUI as sg
import matplotlib.pyplot as plt

# --- CORREÇÃO DO BUG DA ESCALA (DPI) NO WINDOWS ---
import ctypes
import platform

if platform.system() == "Windows":
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        try:
            ctypes.windll.user32.SetProcessDPIAware()
        except Exception:
            pass
# --------------------------------------------------

from backend import (
    PARAMETROS_DEFAULTS, 
    simular_clinica_real, 
    analisar_registos_para_simulacao,
    carregar_historico_json,
    salvar_simulacao_no_historico,
    limpar_historico_json,
    carregar_medicos,
    carregar_ficheiro_configuracao
)




simulacoes_guardadas = carregar_historico_json()


HEADER_BG = "#FFFFFF"       
MAIN_BG = "#FFFFFF"         
CARD_BG = "#FFFFFF"         
PARAM_PANEL_BG = "#FFFFFF"  
INPUT_BG = "#F8FAFC"        

ACCENT_PRIMARY = "#1E3A8A"  
TEXT_PRIMARY = "#0F172A"    
TEXT_SECONDARY = "#475569"  
TEXT_MUTED = "#94A3B8"      
METRIC_BG = "#F8FAFC"       
METRIC_ACCENT = "#2563EB"   
DIVIDER_COLOR = "#E2E8F0"   


sg.theme_background_color(MAIN_BG)
sg.theme_text_color(TEXT_PRIMARY)
sg.theme_element_background_color(MAIN_BG)
sg.theme_input_background_color(INPUT_BG)
sg.theme_input_text_color(TEXT_PRIMARY)
sg.theme_button_color((TEXT_PRIMARY, HEADER_BG))



def popup_pt(texto, titulo="Confirmação"):
    layout = [
        [sg.Text(texto, font=("Segoe UI", 11), pad=(20, 20), background_color=HEADER_BG, text_color=TEXT_PRIMARY)],
        [sg.Button("Sim", size=(10, 1), button_color=("white", "#059669"), font=("Segoe UI", 10, "bold")), 
         sg.Button("Não", size=(10, 1), button_color=("white", "#DC2626"), font=("Segoe UI", 10, "bold"))]
    ]
    win = sg.Window(titulo, layout, modal=True, element_justification='center', keep_on_top=True, background_color=HEADER_BG)
    evento, _ = win.read(close=True)
    return evento == "Sim"

def popup_erro_visual(titulo, msg_principal, msg_detalhe):
    """Novo Popup de Erro com design consistente"""
    layout = [
        [sg.Text("⛔ " + titulo, font=("Segoe UI", 14, "bold"), text_color="#DC2626", background_color=HEADER_BG, pad=(0, 10))],
        [sg.Text("_"*40, text_color="#E2E8F0", background_color=HEADER_BG)],
        
        [sg.Text(msg_principal, font=("Segoe UI", 11, "bold"), text_color=TEXT_PRIMARY, background_color=HEADER_BG, size=(45, 2), justification='center')],
        [sg.Text(msg_detalhe, font=("Segoe UI", 10), text_color=TEXT_SECONDARY, background_color=HEADER_BG, size=(45, 3), justification='center')],
        
        [sg.Text(" ", background_color=HEADER_BG)],
        [sg.Button("Entendido", size=(15, 1), button_color=("white", "#DC2626"), font=("Segoe UI", 10, "bold"))]
    ]
    win = sg.Window("Erro", layout, modal=True, element_justification='center', keep_on_top=True, background_color=HEADER_BG, finalize=True)
    win.read(close=True)

def popup_paciente_visual(dados):
    layout = [
        [sg.Text("Ficha de Atendimento", font=("Segoe UI", 16, "bold"), text_color=ACCENT_PRIMARY, background_color=HEADER_BG, pad=(0, 10))],
        [sg.Text("_"*35, text_color="#E2E8F0", background_color=HEADER_BG)],
        [sg.Text("👤 Paciente:", font=("Segoe UI", 10, "bold"), text_color=TEXT_SECONDARY, background_color=HEADER_BG, size=(13, 1)),
         sg.Text(dados['paciente'], font=("Segoe UI", 11), text_color=TEXT_PRIMARY, background_color=HEADER_BG)],
        [sg.Text("🏥 Especialidade:", font=("Segoe UI", 10, "bold"), text_color=TEXT_SECONDARY, background_color=HEADER_BG, size=(13, 1)),
         sg.Text(dados['esp_req'], font=("Segoe UI", 11), text_color=TEXT_PRIMARY, background_color=HEADER_BG)],
        [sg.Text(" ", background_color=HEADER_BG)],
        [sg.Column([
            [sg.Text("⏳ Tempo Espera:", font=("Segoe UI", 10), text_color=TEXT_SECONDARY, background_color=METRIC_BG, size=(15, 1)),
             sg.Text(f"{dados['espera']:.2f} min", font=("Segoe UI", 11, "bold"), text_color=TEXT_PRIMARY, background_color=METRIC_BG)],
            [sg.Text("⏱️ Duração Cons.:", font=("Segoe UI", 10), text_color=TEXT_SECONDARY, background_color=METRIC_BG, size=(15, 1)),
             sg.Text(f"{dados['duracao']:.2f} min", font=("Segoe UI", 11, "bold"), text_color=TEXT_PRIMARY, background_color=METRIC_BG)]
        ], background_color=METRIC_BG, pad=(10, 10), expand_x=True)],
        [sg.Text(" ", background_color=HEADER_BG)],
        [sg.Button("Fechar", size=(12, 1), button_color=("white", ACCENT_PRIMARY), font=("Segoe UI", 10))]
    ]
    win = sg.Window("Detalhes do Paciente", layout, modal=True, element_justification='center', keep_on_top=True, background_color=HEADER_BG, finalize=True)
    win.read(close=True)



def criar_titulo_principal(texto): return sg.Text(texto, font=("Segoe UI", 32, "bold"), text_color=ACCENT_PRIMARY, background_color=HEADER_BG)
def criar_subtitulo(texto): return sg.Text(texto, font=("Segoe UI", 11), text_color=TEXT_SECONDARY, background_color=HEADER_BG)
def criar_titulo_secao(texto): return sg.Text(texto, font=("Segoe UI", 18, "bold"), text_color=ACCENT_PRIMARY, background_color=CARD_BG)
def criar_linha_separadora(): return sg.Text("-" * 300, text_color=DIVIDER_COLOR, background_color=HEADER_BG, pad=(0, 0), expand_x=True)
def criar_divisoria_card(): return sg.Text("-" * 300, text_color=DIVIDER_COLOR, background_color=CARD_BG, pad=(0, 8), expand_x=True)
def criar_espacador(altura=1): return sg.Text("", background_color=CARD_BG, size=(1, int(altura)))

def criar_campo_parametro(label, valor_padrao=""):
    return sg.Column([[
        sg.Text(label, font=("Segoe UI", 12), text_color=TEXT_SECONDARY, background_color=PARAM_PANEL_BG, size=(35, 1)),
        sg.InputText(valor_padrao, font=("Segoe UI", 12), size=(20, 1), key=f"INPUT_{label}", background_color=INPUT_BG, text_color=TEXT_PRIMARY)
    ]], background_color=PARAM_PANEL_BG, pad=(0, 10))

def criar_metrica_lista(titulo, valor, unidade, key=None):
    return sg.Column([
        [sg.Text(f"{titulo}:", font=("Segoe UI", 9), text_color=TEXT_SECONDARY, background_color=METRIC_BG, size=(30, 1)),
         sg.Text(f"{valor}", font=("Segoe UI", 13, "bold"), text_color=METRIC_ACCENT, background_color=METRIC_BG, key=key)]
    ], background_color=METRIC_BG, pad=(0, 0), expand_x=True)

def criar_caixa_metricas(titulo, metricas_lista):
    linhas = [[sg.Text(titulo, font=("Segoe UI", 12, "bold"), text_color=METRIC_ACCENT, background_color=METRIC_BG)]]
    for m in metricas_lista: linhas.append([m])
    return sg.Column(linhas, background_color=METRIC_BG, pad=(16, 8), expand_x=True, vertical_alignment='top')

def criar_area_detalhe_medico():
    layout = [
        [criar_metrica_lista("Taxa Ocupação Média", "0%", "%", key="METRIC_ocupacao_media_equipa")],
        [criar_espacador(1)],
        [sg.Text("Pesquise ou selecione o Médico:", font=("Segoe UI", 10, "bold"), text_color=TEXT_SECONDARY, background_color=METRIC_BG)],
        [sg.Combo(values=[], default_value="Simule primeiro...", size=(40, 1), key="COMBO_MEDICOS", enable_events=True, readonly=False, font=("Segoe UI", 11), background_color=INPUT_BG)],
        [criar_espacador(1)],
        [criar_metrica_lista("Nome", "---", "", key="METRIC_single_nome")],
        [criar_metrica_lista("Especialidade", "---", "", key="METRIC_single_especialidade")],
        [criar_metrica_lista("Ocupação", "---", "", key="METRIC_single_ocupacao")],
        [criar_metrica_lista("Consultas Realizadas", "---", "", key="METRIC_single_consultas")],
        [criar_metrica_lista("Tempo Médio/Consulta", "---", "", key="METRIC_single_tempo")],
        [criar_espacador(1)],
        [sg.Text("Pacientes Atendidos:", font=("Segoe UI", 9, "bold"), text_color=TEXT_SECONDARY, background_color=METRIC_BG)],
        [sg.Listbox(values=[], size=(45, 10), key="LISTBOX_PACIENTES", enable_events=True, font=("Segoe UI", 9), background_color=INPUT_BG, no_scrollbar=False)]
    ]
    return [sg.Column(layout, background_color=METRIC_BG, pad=(0,0), expand_x=True)]


def gerar_texto_parametros_comparacao(lista_simulacoes_dados):
    if not lista_simulacoes_dados: return "", ""
    primeira_sim = lista_simulacoes_dados[0]
    keys_params = primeira_sim["parametros"].keys()
    fixos = {}
    variaveis = []
    for k in keys_params:
        valor_base = primeira_sim["parametros"][k]
        eh_fixo = True
        for item in lista_simulacoes_dados[1:]:
            if item["parametros"].get(k) != valor_base:
                eh_fixo = False; break
        if eh_fixo: fixos[k] = valor_base
        else: variaveis.append(k)
    txt_fixos = ""
    if fixos:
        itens = []
        for k, v in fixos.items():
            k_clean = k.split("(")[0].strip().replace("Tempo Médio de ", "T. Médio ").replace("Duração da ", "Duração ")
            itens.append(f"{k_clean}: {v}")
        txt_fixos = "  |  ".join(itens)
    txt_vars = ""
    if not variaveis: txt_vars = "Nenhuma diferença nos parâmetros de entrada."
    else:
        for item in lista_simulacoes_dados:
            vals = []
            for var in variaveis:
                var_clean = var.split("(")[0].strip().replace("Taxa de Chegada", "Taxa").replace("Número de ", "Nº ")
                val = item['parametros'].get(var, "?")
                vals.append(f"{var_clean}: {val}")
            txt_vars += f"• {item['nome']}:  " + ", ".join(vals) + "\n"
    return txt_fixos, txt_vars

def plot_grafico_simples(titulo, tempo, dados, label_y, cor, params_dict=None):
    plt.figure(figsize=(10, 7))
    plt.plot(tempo, dados, label=titulo, color=cor, linewidth=2)
    plt.xlabel("Tempo (min)", color="#475569"); plt.ylabel(label_y, color="#475569")
    plt.title(titulo, fontsize=14, fontweight='bold', color="#1E3A8A")
    plt.grid(True, linestyle='--', alpha=0.6); plt.legend()
    if params_dict:
        txt = " | ".join([f"{k.split('(')[0]}: {v}" for k,v in params_dict.items()])
        plt.figtext(0.5, 0.02, txt, wrap=True, horizontalalignment='center', fontsize=8, color="#555555", bbox=dict(boxstyle='round,pad=0.5', facecolor='#F8FAFC', edgecolor='#cbd5e1', alpha=1.0))
        plt.subplots_adjust(bottom=0.15)
    plt.show()

def plot_grafico_multilinhas(titulo, tempo, dados_dict, label_y, params_dict=None):
    plt.figure(figsize=(10, 7))
    for nome_linha, dados in dados_dict.items():
        if len(dados) == len(tempo): plt.plot(tempo, dados, label=nome_linha, linewidth=2)
    plt.xlabel("Tempo (min)", color="#475569"); plt.ylabel(label_y, color="#475569")
    plt.title(titulo, fontsize=14, fontweight='bold', color="#1E3A8A")
    plt.grid(True, linestyle='--', alpha=0.6); plt.legend()
    if params_dict:
        txt = " | ".join([f"{k.split('(')[0]}: {v}" for k,v in params_dict.items()])
        plt.figtext(0.5, 0.02, txt, wrap=True, horizontalalignment='center', fontsize=8, color="#555555", bbox=dict(boxstyle='round,pad=0.5', facecolor='#F8FAFC', edgecolor='#cbd5e1', alpha=1.0))
        plt.subplots_adjust(bottom=0.15)
    plt.show()

def plot_grafico_comparativo(titulo, dados_simulacoes, label_y):
    cores = ['#1E3A8A', '#DC2626', '#059669', '#EA580C', '#7C3AED', '#0891B2']
    estilos = ['-', '--', '-.', ':', '-', '--']
    fig = plt.figure(figsize=(12, 8)); ax = plt.subplot(111)
    for idx, item in enumerate(dados_simulacoes):
        cor = cores[idx % len(cores)]; estilo = estilos[idx % len(estilos)]
        ax.plot(item['tempo'], item['dados'], label=item['nome'], color=cor, linewidth=2, linestyle=estilo)
    ax.set_xlabel("Tempo de Simulação (min)", fontsize=10, color="#475569")
    ax.set_ylabel(label_y, fontsize=10, color="#475569")
    ax.set_title(titulo, fontsize=16, fontweight='bold', color="#1E3A8A", pad=20)
    ax.grid(True, linestyle=':', alpha=0.6)
    ax.legend(loc='best', frameon=True, framealpha=0.9, edgecolor="#cbd5e1")
    txt_fixos, txt_vars = gerar_texto_parametros_comparacao(dados_simulacoes)
    plt.figtext(0.05, 0.26, "DADOS DA COMPARAÇÃO", fontsize=10, fontweight='bold', color="#1E3A8A")
    texto_final = f"CONSTANTES:\n{txt_fixos}\n\nCENÁRIOS:\n{txt_vars}"
    props_caixa = dict(boxstyle='round,pad=1', facecolor='#F8FAFC', edgecolor='#cbd5e1', alpha=1.0)
    plt.figtext(0.05, 0.02, texto_final, fontsize=9, fontfamily="sans-serif", bbox=props_caixa, verticalalignment="bottom", horizontalalignment="left", color="#334155", linespacing=1.6)
    plt.subplots_adjust(bottom=0.32); plt.show()

def plot_histograma_espera(dados_logs, params_dict=None):
    esperas = [float(l['espera']) for l in dados_logs]
    if not esperas:
        popup_erro_visual("Sem dados", "Não há dados para gerar histograma.", "")
        return
    plt.figure(figsize=(10, 7))
    plt.hist(esperas, bins=15, color='#2563EB', edgecolor='white', alpha=0.7)
    plt.xlabel("Tempo de Espera (min)", color="#475569")
    plt.ylabel("Número de Pacientes", color="#475569")
    plt.title("Distribuição dos Tempos de Espera", fontsize=14, fontweight='bold', color="#1E3A8A")
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    media = sum(esperas) / len(esperas)
    plt.axvline(media, color='#DC2626', linestyle='dashed', linewidth=1.5, label=f'Média: {media:.2f} min')
    plt.legend()
    if params_dict:
        txt = " | ".join([f"{k.split('(')[0]}: {v}" for k,v in params_dict.items()])
        plt.figtext(0.5, 0.02, txt, wrap=True, horizontalalignment='center', fontsize=8, color="#555555", bbox=dict(boxstyle='round,pad=0.5', facecolor='#F8FAFC', edgecolor='#cbd5e1', alpha=1.0))
        plt.subplots_adjust(bottom=0.15)
    plt.show()

def plot_pizza_especialidades(dados_logs, params_dict=None):
    if not dados_logs: return
    contagem = {}
    for l in dados_logs:
        esp = l['esp_req']
        contagem[esp] = contagem.get(esp, 0) + 1
    labels = list(contagem.keys())
    sizes = list(contagem.values())
    cores = ['#2563EB', '#059669', '#EA580C', '#7C3AED', '#0891B2', '#DB2777']
    plt.figure(figsize=(10, 7))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=cores[:len(labels)], textprops={'color':"#334155", 'weight':'bold'})
    plt.title("Procura por Especialidade", fontsize=14, fontweight='bold', color="#1E3A8A")
    if params_dict:
        txt = " | ".join([f"{k.split('(')[0]}: {v}" for k,v in params_dict.items()])
        plt.figtext(0.5, 0.05, txt, wrap=True, horizontalalignment='center', fontsize=8, color="#555555", bbox=dict(boxstyle='round,pad=0.5', facecolor='#F8FAFC', edgecolor='#cbd5e1', alpha=1.0))
    plt.show()


coluna_parametros_input = [
    [sg.Button("CARREGAR CONFIGURAÇÃO", key="BUTTON_LOAD_CONFIG", font=("Segoe UI", 10, "bold"), button_color=("white", "#475569"), size=(25, 1), pad=((0, 0), (0, 15)))],
    [sg.Text("Parâmetros de Entrada", font=("Segoe UI", 12, "bold"), background_color=PARAM_PANEL_BG, text_color=ACCENT_PRIMARY, pad=(0, 10))],
    [criar_campo_parametro("Taxa de Chegada (doentes/hora)", PARAMETROS_DEFAULTS["Taxa de Chegada (doentes/hora)"])],
    [criar_campo_parametro("Número de Médicos", PARAMETROS_DEFAULTS["Número de Médicos"])],
    [sg.Column([[sg.Text("Distribuição de Serviço", font=("Segoe UI", 12), text_color=TEXT_SECONDARY, background_color=PARAM_PANEL_BG, size=(35, 1)),
                 sg.Combo(['exponencial', 'normal', 'uniforme'], default_value=PARAMETROS_DEFAULTS["Distribuição de Serviço"], font=("Segoe UI", 12), size=(18, 1), key="INPUT_Distribuição de Serviço", background_color=INPUT_BG, readonly=True)]], background_color=PARAM_PANEL_BG, pad=(0, 10))],
    [criar_campo_parametro("Tempo Médio de Consulta (min)", PARAMETROS_DEFAULTS["Tempo Médio de Consulta (min)"])],
    [criar_campo_parametro("Duração da Simulação (min)", PARAMETROS_DEFAULTS["Duração da Simulação (min)"])],
    
    [sg.Text("Estado do Dataset:", font=("Segoe UI", 11, "bold"), text_color=TEXT_SECONDARY, background_color=PARAM_PANEL_BG, pad=(0,5))],
    [sg.Text("A verificar...", key="TEXT_STATUS_DATASET", font=("Segoe UI", 11), text_color=METRIC_ACCENT, background_color=PARAM_PANEL_BG)],
    [criar_espacador(2)],
    [sg.Button("EXECUTAR SIMULAÇÃO", key="BUTTON_RUN_SIM", font=("Segoe UI", 14, "bold"), button_color=("white", ACCENT_PRIMARY), size=(30, 1), pad=((0, 0), (20, 0)))]
]

tab_parametros = [
    [criar_titulo_secao("Configuração da Simulação")], 
    [criar_linha_separadora()],                         
    [sg.VPush(background_color=CARD_BG)],
    [
        sg.Push(background_color=CARD_BG), 
        sg.Column(coluna_parametros_input, background_color=PARAM_PANEL_BG, element_justification='center', pad=(0, 0), expand_x=False, sbar_background_color=PARAM_PANEL_BG), 
        sg.Push(background_color=CARD_BG)
    ],
    [sg.VPush(background_color=CARD_BG)],
    [sg.Text("", background_color=CARD_BG, expand_y=True)]
]


coluna_esquerda_dashboard = [
    [criar_caixa_metricas("Métricas de Pacientes", [
        criar_metrica_lista("Pacientes Atendidos", "0", "", key="METRIC_pacientes_atendidos"),
        criar_metrica_lista("Tempo Médio de Espera", "0 min", "min", key="METRIC_tempo_espera"),
        criar_metrica_lista("Tempo Médio de Consulta", "0 min", "min", key="METRIC_tempo_consulta"),
        criar_metrica_lista("Tempo Médio na Clínica", "0 min", "min", key="METRIC_tempo_clinica")
    ])],
    [criar_espacador(1)],
    [criar_caixa_metricas("Métrica de Fila:", [
        criar_metrica_lista("Tamanho Médio da Fila", "0", "", key="METRIC_tamanho_medio_fila"),
        criar_metrica_lista("Tamanho Máximo da Fila", "0", "", key="METRIC_tamanho_max_fila")
    ])]
]
coluna_direita_dashboard = [[criar_caixa_metricas("Detalhes dos Médicos", criar_area_detalhe_medico())]]
tab_dashboard = [
    [sg.Column([
        [criar_titulo_secao("Dashboard Operacional")], [criar_divisoria_card()],
        [sg.Column(coluna_esquerda_dashboard, background_color=CARD_BG, expand_x=True, vertical_alignment='top'),
         sg.Column(coluna_direita_dashboard, background_color=CARD_BG, expand_x=True, vertical_alignment='top')],
        [criar_espacador(10)]
    ], background_color=CARD_BG, expand_x=True, expand_y=True, scrollable=True, vertical_scroll_only=True)]
]


cabecalho_tabela = ["Médico", "Especialidade Méd.", "Paciente", "Especialidade Req.", "Tempo Espera (min)", "Duração (min)"]
tab_registos = [
    [criar_titulo_secao("Log Real da Simulação")], [criar_divisoria_card()],
    [sg.Table(values=[], headings=cabecalho_tabela, auto_size_columns=False, col_widths=[20, 15, 25, 15, 15, 15], 
              num_rows=25, key='TABLE_REGISTOS', row_height=30, font=("Segoe UI", 10), 
              header_font=("Segoe UI", 10, "bold"), header_background_color=ACCENT_PRIMARY, header_text_color='white',
              background_color='white', alternating_row_color=METRIC_BG,
              text_color=TEXT_PRIMARY, selected_row_colors=('white', ACCENT_PRIMARY),
              expand_x=True, expand_y=True)]
]


coluna_graficos_atual = [
    [sg.Text("Gráficos Desta Simulação", font=("Segoe UI", 12, "bold"), text_color=ACCENT_PRIMARY, background_color=CARD_BG)],
    [sg.Text("Selecione para abrir:", font=("Segoe UI", 9), text_color=TEXT_SECONDARY, background_color=CARD_BG)],
    [sg.Listbox(values=["Evolução da Fila de Espera", "Evolução da Ocupação dos Médicos", "Fila por Especialidade", "Distribuição Tempo Espera (Histograma)", "Procura por Especialidade (Pie)"], size=(40, 6), key="LISTBOX_GRAFICOS_ATUAL", enable_events=True, font=("Segoe UI", 11), background_color=METRIC_BG)]
]

coluna_graficos_comparacao = [
    [sg.Text("Histórico e Comparação", font=("Segoe UI", 12, "bold"), text_color=ACCENT_PRIMARY, background_color=CARD_BG)],
    [sg.Text("1. Selecione simulação(ões):", font=("Segoe UI", 9, "bold"), text_color=TEXT_SECONDARY, background_color=CARD_BG)],
    [sg.Listbox(values=list(simulacoes_guardadas.keys()), size=(40, 8), key="LISTBOX_SIMULACOES_GUARDADAS", font=("Segoe UI", 10), background_color=METRIC_BG, select_mode='multiple')],
    [sg.Button("LIMPAR HISTÓRICO", key="BUTTON_CLEAR_JSON", size=(20, 1), font=("Segoe UI", 8, "bold"), button_color=("white", "#DC2626"), pad=(0, 5))],
    [criar_espacador(1)],
    [sg.Text("2. Ver Gráfico Individual (Selecione 1 acima):", font=("Segoe UI", 9, "bold"), text_color=TEXT_SECONDARY, background_color=CARD_BG)],
    [sg.Listbox(values=["Evolução da Fila de Espera", "Evolução da Ocupação dos Médicos", "Fila por Especialidade", "Distribuição Tempo Espera (Histograma)", "Procura por Especialidade (Pie)"], size=(40, 4), key="LISTBOX_GRAFICOS_HISTORICO_INDIVIDUAL", enable_events=True, font=("Segoe UI", 10), background_color=METRIC_BG)],
    [criar_espacador(1)],
    [sg.Text("3. Comparar Várias (Selecione 2+ acima):", font=("Segoe UI", 9, "bold"), text_color=TEXT_SECONDARY, background_color=CARD_BG)],
    [sg.Listbox(values=["Comparar Evolução da Fila", "Comparar Ocupação dos Médicos"], size=(40, 3), key="LISTBOX_GRAFICOS_COMPARACAO", enable_events=True, font=("Segoe UI", 10), background_color=METRIC_BG)]
]

tab_graficos = [
    [sg.Column([
        [criar_titulo_secao("Gráficos e Análise")], [criar_divisoria_card()], [criar_espacador(1)],
        [sg.Column(coluna_graficos_atual, background_color=CARD_BG, expand_x=True, vertical_alignment='top'),
         sg.VerticalSeparator(color=DIVIDER_COLOR),
         sg.Column(coluna_graficos_comparacao, background_color=CARD_BG, expand_x=True, vertical_alignment='top')],
        [criar_espacador(10)]
    ], background_color=CARD_BG, expand_x=True, expand_y=True, scrollable=True, vertical_scroll_only=True)]
]


header = [[sg.Column([[criar_titulo_principal("SIMULAÇÃO DA CLÍNICA")], [criar_subtitulo("Sistema de Simulação de Eventos de uma Clínica Médica")]], background_color=HEADER_BG, pad=(20, 20), expand_x=True)], [criar_linha_separadora()]]

abas = [[sg.TabGroup([[
            sg.Tab("Parâmetros", tab_parametros, background_color=CARD_BG, title_color=TEXT_PRIMARY),
            sg.Tab("Dashboard", tab_dashboard, background_color=CARD_BG, title_color=TEXT_PRIMARY),
            sg.Tab("Registos", tab_registos, background_color=CARD_BG, title_color=TEXT_PRIMARY),
            sg.Tab("Gráficos", tab_graficos, background_color=CARD_BG, title_color=TEXT_PRIMARY)
        ]], 
        tab_location='top', 
        title_color=TEXT_SECONDARY, 
        selected_title_color=ACCENT_PRIMARY,
        tab_background_color=MAIN_BG, 
        selected_background_color=CARD_BG, 
        background_color=MAIN_BG, 
        border_width=0, 
        expand_x=True, expand_y=True
)]]

layout = header + abas + [[sg.Text("Engenharia Biomédica - UMinho", font=("Segoe UI", 9), text_color=TEXT_MUTED, background_color=MAIN_BG, pad=(20, 12))]]

janela = sg.Window("Simulador Clínica", layout, size=(1600, 950), resizable=True, finalize=True, background_color=MAIN_BG)
try: janela.maximize() 
except: pass


dados_simulacao_carregados = analisar_registos_para_simulacao()
if dados_simulacao_carregados: janela["TEXT_STATUS_DATASET"].update("Dataset Carregado (registos_5000.json)")
else: janela["TEXT_STATUS_DATASET"].update("Nenhum dataset encontrado (Simulação Aleatória)")

cache_resultados_medicos = []
cache_logs_simulacao = []
cache_series_atual = None
cache_params_atuais = None

while True:
    evento, valores = janela.read(timeout=100)
    if evento == sg.WINDOW_CLOSED: break
    
    
    if evento == "BUTTON_LOAD_CONFIG":
        filename = sg.popup_get_file("Selecione o ficheiro JSON de configuração:", file_types=(("JSON Files", "*.json"),))
        if filename:
            try:
                config = carregar_ficheiro_configuracao(filename)
                
                
                if "taxa_chegada" in config: janela["INPUT_Taxa de Chegada (doentes/hora)"].update(config["taxa_chegada"])
                if "num_medicos" in config: janela["INPUT_Número de Médicos"].update(config["num_medicos"])
                if "distribuicao" in config: janela["INPUT_Distribuição de Serviço"].update(config["distribuicao"])
                if "tempo_medio" in config: janela["INPUT_Tempo Médio de Consulta (min)"].update(config["tempo_medio"])
                if "duracao" in config: janela["INPUT_Duração da Simulação (min)"].update(config["duracao"])
                
                sg.popup("Configuração carregada com sucesso!", title="Sucesso")
            except Exception as e:
                popup_erro_visual("Erro de Configuração", "Falha ao ler ficheiro", str(e))

    
    if evento == "BUTTON_RUN_SIM":
        try:
            taxa = float(valores["INPUT_Taxa de Chegada (doentes/hora)"])
            n_med = int(valores["INPUT_Número de Médicos"])
            t_med = float(valores["INPUT_Tempo Médio de Consulta (min)"])
            duracao = float(valores["INPUT_Duração da Simulação (min)"])
            dist = valores["INPUT_Distribuição de Serviço"]
            
            if taxa<=0 or n_med<=0 or t_med<=0 or duracao<=0: raise ValueError("Valores devem ser positivos")
            if t_med > duracao: raise ValueError("Tempo de consulta maior que duração")
            
            
            db_medicos = carregar_medicos()
            if db_medicos:
                total_db = len(db_medicos)
                if n_med > total_db:
                    popup_erro_visual("Impossível Executar", 
                                      f"Pediu {n_med} médicos, mas só existem {total_db} registados.", 
                                      f"Por favor, reduza o número de médicos para no máximo {total_db}.")
                    continue 
            
            if dados_simulacao_carregados and 'registos' in dados_simulacao_carregados:
                total_pacientes = len(dados_simulacao_carregados['registos'])
                total_esperado = taxa * (duracao / 60.0)
                if total_esperado > total_pacientes:
                    popup_erro_visual("Dataset Insuficiente", 
                                      f"Simulação requer ~{int(total_esperado)} pacientes.", 
                                      f"O ficheiro 'registos_5000.json' só tem {total_pacientes} pacientes.\nReduza a Taxa de Chegada ou a Duração.")
                    continue
            
            janela['BUTTON_RUN_SIM'].update(disabled=True)
            resultados = simular_clinica_real(taxa, n_med, t_med, duracao, dist, dados_simulacao_carregados)
            janela['BUTTON_RUN_SIM'].update(disabled=False)
            
            globais = resultados["globais"]
            cache_resultados_medicos = resultados["medicos"]
            cache_logs_simulacao = resultados["log"]
            cache_series_atual = resultados["series"]
            cache_params_atuais = {
                "Taxa de Chegada (doentes/hora)": str(taxa), "Número de Médicos": str(n_med),
                "Distribuição de Serviço": dist, "Tempo Médio de Consulta (min)": str(t_med),
                "Duração da Simulação (min)": str(duracao)
            }
            
            janela["METRIC_pacientes_atendidos"].update(f"{globais['pacientes_atendidos']}")
            janela["METRIC_tempo_espera"].update(f"{globais['tempo_espera']:.2f} min")
            janela["METRIC_tempo_consulta"].update(f"{globais['tempo_consulta']:.2f} min")
            janela["METRIC_tempo_clinica"].update(f"{globais['tempo_clinica']:.2f} min")
            janela["METRIC_tamanho_medio_fila"].update(f"{globais['tamanho_medio_fila']:.2f}")
            janela["METRIC_tamanho_max_fila"].update(f"{globais['tamanho_max_fila']}")
            janela["METRIC_ocupacao_media_equipa"].update(f"{globais.get('ocupacao_media_medicos', 0):.1f}%")
            
            
            tabela_dados = []
            cores_linhas = []
            for idx, item in enumerate(cache_logs_simulacao):
                tabela_dados.append([item['medico'], item['esp_med'], item['paciente'], item['esp_req'], f"{item['espera']:.2f}", f"{item['duracao']:.2f}"])
                try:
                    val_espera = float(item['espera'])
                    if val_espera > 30.0:
                        cores_linhas.append((idx, "#991B1B", "#FEF2F2")) # Vermelho
                    elif val_espera < 10.0:
                        cores_linhas.append((idx, "#166534", "#F0FDF4")) # Verde
                except: pass

            janela['TABLE_REGISTOS'].update(values=tabela_dados, row_colors=cores_linhas)
            
            nomes_medicos = [m['nome'] for m in cache_resultados_medicos]
            if nomes_medicos:
                janela["COMBO_MEDICOS"].update(values=nomes_medicos, value=nomes_medicos[0])
                janela.write_event_value("COMBO_MEDICOS", "")

            if popup_pt("Simulação concluída com sucesso!\n\nDeseja guardar esta simulação no histórico?", "Guardar?"):
                nome_sim = sg.popup_get_text("Dê um nome a esta simulação:", title="Guardar Simulação")
                if nome_sim:
                    if nome_sim in simulacoes_guardadas:
                        if not popup_pt(f"O nome '{nome_sim}' já existe. Sobrescrever?", "Sobrescrever?"):
                            nome_sim = None
                    if nome_sim:
                        nova_sim = {
                            "parametros": cache_params_atuais,
                            "cache_series": cache_series_atual,
                            "cache_resultados_medicos": cache_resultados_medicos,
                            "cache_logs_simulacao": cache_logs_simulacao
                        }
                        if salvar_simulacao_no_historico(nome_sim, nova_sim):
                            simulacoes_guardadas[nome_sim] = nova_sim
                            janela["LISTBOX_SIMULACOES_GUARDADAS"].update(values=list(simulacoes_guardadas.keys()))
                            sg.popup("Simulação guardada!", title="Sucesso")
        except ValueError as e:
            janela['BUTTON_RUN_SIM'].update(disabled=False)
            popup_erro_visual("Erro de Execução", "Parâmetros Inválidos", str(e))

    
    if evento == "BUTTON_CLEAR_JSON":
        if popup_pt("Tem a certeza? Isto apagará todo o histórico.", "Apagar Tudo"):
            if limpar_historico_json():
                simulacoes_guardadas = {}
                janela["LISTBOX_SIMULACOES_GUARDADAS"].update(values=[])
                sg.popup("Histórico limpo.", title="Sucesso")

    
    if evento == "LISTBOX_GRAFICOS_HISTORICO_INDIVIDUAL" and valores["LISTBOX_GRAFICOS_HISTORICO_INDIVIDUAL"]:
        escolha = valores["LISTBOX_GRAFICOS_HISTORICO_INDIVIDUAL"][0]
        selecao = valores["LISTBOX_SIMULACOES_GUARDADAS"]
        
        if not selecao:
            popup_erro_visual("Seleção Inválida", "Nenhuma simulação selecionada.", "Selecione uma simulação na lista 'Histórico e Comparação'.")
        elif len(selecao) > 1:
            popup_erro_visual("Seleção Múltipla", "Selecione apenas UMA simulação.", "Para ver gráficos individuais, escolha apenas uma.\nPara comparar várias, use o menu de baixo.")
        else:
            nome_sim = selecao[0]
            dados = simulacoes_guardadas[nome_sim]
            series = dados["cache_series"]
            params = dados["parametros"]
            logs = dados.get("cache_logs_simulacao", [])
            
            if escolha == "Evolução da Fila de Espera":
                plot_grafico_simples(f"Fila: {nome_sim}", series['tempo'], series['fila'], "Pessoas", "#2563EB", params)
            elif escolha == "Evolução da Ocupação dos Médicos":
                n_med_hist = int(params.get("Número de Médicos", 1))
                dados_perc = [(x / n_med_hist * 100) for x in series['ocupacao']]
                plot_grafico_simples(f"Ocupação: {nome_sim}", series['tempo'], dados_perc, "Ocupação (%)", "#EA580C", params)
            elif escolha == "Fila por Especialidade":
                dados_esp = series.get('fila_por_especialidade', {})
                if not dados_esp:
                    sg.popup_error("Esta simulação guardada é antiga e não tem dados de especialidade.")
                else:
                    plot_grafico_multilinhas(f"Especialidades: {nome_sim}", series['tempo'], dados_esp, "Pessoas na Fila", params)
            elif escolha == "Distribuição Tempo Espera (Histograma)":
                if logs: plot_histograma_espera(logs, params)
                else: popup_erro_visual("Sem Dados", "Simulação antiga sem logs detalhados.", "")
            elif escolha == "Procura por Especialidade (Pie)":
                if logs: plot_pizza_especialidades(logs, params)
                else: popup_erro_visual("Sem Dados", "Simulação antiga sem logs detalhados.", "")
        
        janela["LISTBOX_GRAFICOS_HISTORICO_INDIVIDUAL"].update(set_to_index=[])

   
    if evento == "LISTBOX_GRAFICOS_COMPARACAO" and valores["LISTBOX_GRAFICOS_COMPARACAO"]:
        tipo_grafico = valores["LISTBOX_GRAFICOS_COMPARACAO"][0]
        nomes_selecionados = valores["LISTBOX_SIMULACOES_GUARDADAS"]
        
        if not nomes_selecionados or len(nomes_selecionados) < 2:
            popup_erro_visual("Dados Insuficientes", "Selecione pelo menos 2 simulações.", "Para comparar, precisa de selecionar 2 ou mais itens na lista de histórico acima.")
            janela["LISTBOX_GRAFICOS_COMPARACAO"].update(set_to_index=[])
            continue
            
        dados_para_plot = []
        chave_dados = 'fila' if tipo_grafico == "Comparar Evolução da Fila" else 'ocupacao'
        label_y = "Pessoas na Fila" if chave_dados == 'fila' else "Ocupação (%)"
        
        duracoes = set()
        for nome in nomes_selecionados:
            sim_obj = simulacoes_guardadas[nome]
            duracoes.add(sim_obj["parametros"]["Duração da Simulação (min)"])
            
            dados_raw = sim_obj["cache_series"][chave_dados]
            
            if chave_dados == 'ocupacao':
                n_med_comp = int(sim_obj["parametros"].get("Número de Médicos", 1))
                dados_final = [(x / n_med_comp * 100) for x in dados_raw]
            else:
                dados_final = dados_raw

            dados_para_plot.append({
                "nome": nome, "tempo": sim_obj["cache_series"]["tempo"],
                "dados": dados_final, "parametros": sim_obj["parametros"] 
            })
            
        if len(duracoes) > 1:
            if not popup_pt("Durações diferentes detetadas no gráfico. Continuar?", "Aviso"):
                janela["LISTBOX_GRAFICOS_COMPARACAO"].update(set_to_index=[])
                continue

        plot_grafico_comparativo(f"{tipo_grafico}", dados_para_plot, label_y)
        janela["LISTBOX_GRAFICOS_COMPARACAO"].update(set_to_index=[])

    
    if evento == "LISTBOX_GRAFICOS_ATUAL" and valores["LISTBOX_GRAFICOS_ATUAL"]:
        escolha = valores["LISTBOX_GRAFICOS_ATUAL"][0]
        if not cache_series_atual: 
            popup_erro_visual("Sem Dados", "Execute a simulação primeiro!", "Não há dados para mostrar. Configure os parâmetros e clique em 'EXECUTAR'.")
        elif escolha == "Evolução da Fila de Espera":
            plot_grafico_simples("Fila de Espera", cache_series_atual['tempo'], cache_series_atual['fila'], "Pessoas", "#2563EB", cache_params_atuais)
        elif escolha == "Evolução da Ocupação dos Médicos":
            n_med = int(cache_params_atuais["Número de Médicos"])
            dados_perc = [(x / n_med * 100) for x in cache_series_atual['ocupacao']]
            plot_grafico_simples("Ocupação Médica (%)", cache_series_atual['tempo'], dados_perc, "Ocupação (%)", "#EA580C", cache_params_atuais)
        elif escolha == "Fila por Especialidade":
            dados_esp = cache_series_atual.get('fila_por_especialidade', {})
            plot_grafico_multilinhas("Fila por Especialidade", cache_series_atual['tempo'], dados_esp, "Pessoas na Fila", cache_params_atuais)
        elif escolha == "Distribuição Tempo Espera (Histograma)":
            plot_histograma_espera(cache_logs_simulacao, cache_params_atuais)
        elif escolha == "Procura por Especialidade (Pie)":
            plot_pizza_especialidades(cache_logs_simulacao, cache_params_atuais)

    
    if evento == "COMBO_MEDICOS":
        nome_sel = valores["COMBO_MEDICOS"]
        m_enc = next((m for m in cache_resultados_medicos if m['nome'] == nome_sel), None)
        if m_enc:
            janela["METRIC_single_nome"].update(m_enc["nome"])
            janela["METRIC_single_especialidade"].update(m_enc["especialidade"])
            janela["METRIC_single_ocupacao"].update(f"{m_enc['ocupacao']:.1f}%")
            janela["METRIC_single_consultas"].update(f"{m_enc['consultas']}")
            janela["METRIC_single_tempo"].update(f"{m_enc['tempo_medio_consulta']:.2f} min")
            
            pacs = []
            for l in cache_logs_simulacao:
                if l['medico'] == m_enc['nome']:
                    lbl = f"{l['paciente']}"
                    pacs.append(lbl)
            janela["LISTBOX_PACIENTES"].update(values=pacs)

    
    if evento == "LISTBOX_PACIENTES" and valores["LISTBOX_PACIENTES"]:
        nome = valores["LISTBOX_PACIENTES"][0].split(" | ")[0]
        reg = next((l for l in cache_logs_simulacao if l['paciente'] == nome), None)
        if reg: popup_paciente_visual(reg)

janela.close()