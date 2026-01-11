
import json
import os
import random
import heapq

ARQUIVO_HISTORICO = "historico_simulacoes.json"

PARAMETROS_DEFAULTS = {
    "Taxa de Chegada (doentes/hora)": "20",
    "Número de Médicos": "8",
    "Distribuição de Serviço": "exponencial",
    "Tempo Médio de Consulta (min)": "15",
    "Duração da Simulação (min)": "480",
}



def carregar_historico_json():
    """Carrega as simulações salvas do disco."""
    try:
        diretorio_atual = os.path.dirname(os.path.abspath(__file__))
        caminho = os.path.join(diretorio_atual, ARQUIVO_HISTORICO)
        if not os.path.exists(caminho):
            return {}
        with open(caminho, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Erro ao carregar histórico: {e}")
        return {}

def salvar_simulacao_no_historico(nome, dados_simulacao):
    """Guarda uma nova simulação no JSON."""
    historico = carregar_historico_json()
    historico[nome] = dados_simulacao
    
    try:
        diretorio_atual = os.path.dirname(os.path.abspath(__file__))
        caminho = os.path.join(diretorio_atual, ARQUIVO_HISTORICO)
        with open(caminho, 'w', encoding='utf-8') as f:
            json.dump(historico, f, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Erro ao salvar: {e}")
        return False

def limpar_historico_json():
    """Apaga todo o conteúdo do JSON."""
    try:
        diretorio_atual = os.path.dirname(os.path.abspath(__file__))
        caminho = os.path.join(diretorio_atual, ARQUIVO_HISTORICO)
        with open(caminho, 'w', encoding='utf-8') as f:
            json.dump({}, f)
        return True
    except Exception as e:
        return False



def normalizar_especialidade(texto):
    """
    Converte nomes de profissionais (ex: Pediatra) 
    para a área médica (ex: Pediatria) e padroniza a escrita.
    """
    if not texto: return "Geral"
    
    
    texto_limpo = str(texto).strip().title()
    
    
    mapa = {
        "Pediatra": "Pediatria",
        "Cardiologista": "Cardiologia",
        "Ortopedista": "Ortopedia",
        "Dermatologista": "Dermatologia",
        "Oftalmologista": "Oftalmologia",
        "Ginecologista": "Ginecologia",
        "Urologista": "Urologia",
        "Psiquiatra": "Psiquiatria",
        "Neurologista": "Neurologia",
        "Gastroenterologista": "Gastroenterologia",
        "Cirurgião": "Cirurgia",
        "Cirurgiao": "Cirurgia",
        "Medico Geral": "Geral",
        "Médico Geral": "Geral",
        "Clinico Geral": "Geral"
    }
    
    
    return mapa.get(texto_limpo, texto_limpo)

def carregar_medicos():
    try:
        diretorio_atual = os.path.dirname(os.path.abspath(__file__))
        caminho_medicos = os.path.join(diretorio_atual, "médicos.json")
        with open(caminho_medicos, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

def carregar_registos():
    try:
        diretorio_atual = os.path.dirname(os.path.abspath(__file__))
        caminho_registos = os.path.join(diretorio_atual, "registos_5000.json")
        with open(caminho_registos, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

def analisar_registos_para_simulacao():
    registos = carregar_registos()
    if not registos: return None
    return {"registos": registos}

def carregar_ficheiro_configuracao(caminho_arquivo):
    """Lê um ficheiro JSON externo com parâmetros de configuração."""
    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        raise ValueError(f"Erro ao ler ficheiro: {str(e)}")



CHEGADA = 1
SAIDA = 2

def criar_paciente(id_p, tempo_chegada, dados_reais=None):
    paciente = {
        "id": id_p,
        "tempo_chegada": tempo_chegada,
        "dados_reais": dados_reais
    }
    
    if dados_reais:
        
        raw_esp = dados_reais.get('especialidade_requerida', 'Geral')
        paciente["especialidade"] = normalizar_especialidade(raw_esp)
        
        paciente["prioridade"] = dados_reais.get('prioridade', 'Normal')
        nome_real = dados_reais.get('nome', 'Paciente')
        id_real = dados_reais.get('id', id_p)
        paciente["nome_display"] = f"{nome_real} (ID-{id_real})"
    else:
        paciente["especialidade"] = random.choice(['Geral', 'Cardiologia', 'Ortopedia', 'Pediatria'])
        paciente["prioridade"] = random.choice(['Normal', 'Urgente'])
        paciente["nome_display"] = f"Paciente {id_p}"
        
    return paciente

def criar_medico(id_m, nome, especialidade):
    return {
        "id": id_m,
        "nome": nome,
        "especialidade": especialidade,
        "livre": True,         
        "tempo_ocupado": 0.0,  
        "num_consultas": 0     
    }

def gerar_tempo_servico(tempo_medio, distribuicao):
    if distribuicao == "exponencial" or distribuicao == "exponential":
        return random.expovariate(1.0 / tempo_medio)
    elif distribuicao == "normal":
        return max(1, random.gauss(tempo_medio, tempo_medio * 0.2))
    elif distribuicao == "uniforme" or distribuicao == "uniform":
        return random.uniform(tempo_medio * 0.5, tempo_medio * 1.5)
    else:
        return tempo_medio

def verifica_compatibilidade(medico, paciente):
    if medico['especialidade'] == paciente['especialidade']: return True
    if medico['especialidade'] == 'Geral': return True
    if paciente['especialidade'] == 'Geral': return True
    return False

def simular_clinica_real(taxa_chegada, num_medicos_input, tempo_medio, duracao_sim, distribuicao, dados_dataset=None):
    
    if tempo_medio > duracao_sim:
        raise ValueError(f"Erro: O tempo médio de consulta ({tempo_medio}min) não pode ultrapassar a duração da simulação ({duracao_sim}min)")
    
    
    
    random.seed() 
    
    tempo_atual = 0.0
    queue_eventos = [] 
    fila_espera = []   
    
    db_medicos = carregar_medicos()
    medicos = [] 
    
    
    for i in range(num_medicos_input):
        if i < len(db_medicos):
            nome = f"Dr. {db_medicos[i]['nome']}"
            
            raw_esp = db_medicos[i].get('especialidade', 'Geral')
            esp = normalizar_especialidade(raw_esp)
        else:
            nome = f"Médico {i+1}"
            esp = 'Geral'
        medicos.append(criar_medico(i, nome, esp))

    
    todas_especialidades = set(m['especialidade'] for m in medicos)
    todas_especialidades.update(['Geral', 'Cardiologia', 'Ortopedia', 'Pediatria'])

    lista_pacientes_reais = []
    if dados_dataset and 'registos' in dados_dataset:
        lista_pacientes_reais = dados_dataset['registos']
    idx_paciente_real = 0
    cont_pacientes = 0
    
    taxa_por_min = taxa_chegada / 60.0
    primeira_chegada = random.expovariate(taxa_por_min)
    heapq.heappush(queue_eventos, (primeira_chegada, CHEGADA, None))
    
    log_atendimentos = [] 
    stats_tempos_espera = []
    stats_tempos_clinica = []
    stats_fila_tamanhos = []
    
    series_tempo = [0.0]
    series_fila = [0]
    series_ocupacao = [0]
    series_fila_esp = {esp: [0] for esp in todas_especialidades}
    
    while queue_eventos:
        tempo_evento, tipo_evento, dados = heapq.heappop(queue_eventos)
        
        
        if tempo_evento > duracao_sim:
            series_tempo.append(duracao_sim)
            series_fila.append(len(fila_espera))
            medicos_ocupados = sum(1 for m in medicos if not m['livre'])
            series_ocupacao.append(medicos_ocupados)
            
            for esp in series_fila_esp:
                ultimo = series_fila_esp[esp][-1] if series_fila_esp[esp] else 0
                series_fila_esp[esp].append(ultimo)
            break 
            
        tempo_atual = tempo_evento
        
        
        medicos_ocupados = sum(1 for m in medicos if not m['livre'])
        series_tempo.append(tempo_atual)
        series_fila.append(len(fila_espera))
        series_ocupacao.append(medicos_ocupados)
        stats_fila_tamanhos.append(len(fila_espera))
        
        
        contagem_temp = {}
        for p in fila_espera:
            e = p['especialidade']
            contagem_temp[e] = contagem_temp.get(e, 0) + 1
            
        todas_keys = set(series_fila_esp.keys()).union(todas_especialidades).union(contagem_temp.keys())
        
        for esp in todas_keys:
            qtd = contagem_temp.get(esp, 0)
            if esp not in series_fila_esp:
                series_fila_esp[esp] = [0] * (len(series_tempo) - 1)
            series_fila_esp[esp].append(qtd)
        
        if tipo_evento == CHEGADA:
            cont_pacientes += 1
            dados_p = None
            if idx_paciente_real < len(lista_pacientes_reais):
                dados_p = lista_pacientes_reais[idx_paciente_real]
                idx_paciente_real += 1
            
            novo_paciente = criar_paciente(cont_pacientes, tempo_atual, dados_p)
            
            medico_escolhido = None
            candidatos = [m for m in medicos if m['livre'] and verifica_compatibilidade(m, novo_paciente)]
            if candidatos:
                medico_escolhido = candidatos[0]
            
            if medico_escolhido:
                medico_escolhido['livre'] = False
                duracao_consulta = gerar_tempo_servico(tempo_medio, distribuicao)
                medico_escolhido['tempo_ocupado'] += duracao_consulta
                medico_escolhido['num_consultas'] += 1
                
                heapq.heappush(queue_eventos, (tempo_atual + duracao_consulta, SAIDA, (medico_escolhido, novo_paciente)))
                
                stats_tempos_espera.append(0)
                stats_tempos_clinica.append(duracao_consulta)
                
                log_atendimentos.append({
                    "medico": medico_escolhido['nome'],
                    "esp_med": medico_escolhido['especialidade'],
                    "paciente": novo_paciente['nome_display'],
                    "esp_req": novo_paciente['especialidade'],
                    "prioridade": novo_paciente['prioridade'],
                    "espera": 0.0,
                    "duracao": duracao_consulta
                })
            else:
                fila_espera.append(novo_paciente)
            
            prox_chegada = tempo_atual + random.expovariate(taxa_por_min)
            if prox_chegada <= duracao_sim:
                heapq.heappush(queue_eventos, (prox_chegada, CHEGADA, None))
                
        elif tipo_evento == SAIDA:
            medico_que_acabou, paciente_que_saiu = dados
            medico_que_acabou['livre'] = True
            
            paciente_da_fila = None
            idx_na_fila = -1
            
            if fila_espera:
                fila_espera.sort(key=lambda p: (0 if p['prioridade']=='Urgente' else 1, p['tempo_chegada']))
                
                for i, p in enumerate(fila_espera):
                    if verifica_compatibilidade(medico_que_acabou, p):
                        paciente_da_fila = p
                        idx_na_fila = i
                        break
            
            if paciente_da_fila:
                fila_espera.pop(idx_na_fila)
                
                medico_que_acabou['livre'] = False
                duracao_consulta = gerar_tempo_servico(tempo_medio, distribuicao)
                medico_que_acabou['tempo_ocupado'] += duracao_consulta
                medico_que_acabou['num_consultas'] += 1
                
                heapq.heappush(queue_eventos, (tempo_atual + duracao_consulta, SAIDA, (medico_que_acabou, paciente_da_fila)))
                
                tempo_espera = tempo_atual - paciente_da_fila['tempo_chegada']
                stats_tempos_espera.append(tempo_espera)
                stats_tempos_clinica.append(tempo_espera + duracao_consulta)
                
                log_atendimentos.append({
                    "medico": medico_que_acabou['nome'],
                    "esp_med": medico_que_acabou['especialidade'],
                    "paciente": paciente_da_fila['nome_display'],
                    "esp_req": paciente_da_fila['especialidade'],
                    "prioridade": paciente_da_fila['prioridade'],
                    "espera": tempo_espera,
                    "duracao": duracao_consulta
                })

    total_atendidos = len(stats_tempos_espera)
    media_espera = sum(stats_tempos_espera) / total_atendidos if total_atendidos > 0 else 0
    media_clinica = sum(stats_tempos_clinica) / total_atendidos if total_atendidos > 0 else 0
    media_fila = sum(stats_fila_tamanhos) / len(stats_fila_tamanhos) if stats_fila_tamanhos else 0
    max_fila = max(stats_fila_tamanhos) if stats_fila_tamanhos else 0
    
    metricas_medicos = []
    for m in medicos:
        perc_ocupacao = (m['tempo_ocupado'] / duracao_sim) * 100
        metricas_medicos.append({
            "nome": m['nome'],
            "especialidade": m['especialidade'],
            "ocupacao": min(100, perc_ocupacao),
            "consultas": m['num_consultas'],
            "tempo_medio_consulta": (m['tempo_ocupado'] / m['num_consultas']) if m['num_consultas'] > 0 else 0
        })
        
    
    media_ocupacao_equipa = 0
    if metricas_medicos:
        media_ocupacao_equipa = sum(m['ocupacao'] for m in metricas_medicos) / len(metricas_medicos)
        
    metricas_globais = {
        "pacientes_atendidos": total_atendidos,
        "tempo_espera": media_espera,
        "tempo_consulta": tempo_medio,
        "tempo_clinica": media_clinica,
        "tamanho_medio_fila": media_fila,
        "tamanho_max_fila": max_fila,
        "ocupacao_media_medicos": media_ocupacao_equipa 
    }
    
    return {
        "globais": metricas_globais,
        "medicos": metricas_medicos,
        "log": log_atendimentos,
        "series": {
            "tempo": series_tempo,
            "fila": series_fila,
            "ocupacao": series_ocupacao,
            "fila_por_especialidade": series_fila_esp
        }
    }