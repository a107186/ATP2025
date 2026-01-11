# Relatório Técnico: Simulador de Clínica 

## Algoritmos e Técnicas de Programação
## Licenciatura em Engenharia Biomédica
### Universidade do Minho
### Docentes: José Carlos Ramalho, Luís Filipe Cunha
### Alunos: A107272 Beatriz Ribeiro, A107186 Pedro Gomes
---

## Índice

1. [Introdução](#introdução)
2. [Análise e Requisitos](#análise-e-requisitos)
   - 2.1 [Requisitos Funcionais](#requisitos-funcionais)
   - 2.2 [Requisitos Técnicos](#requisitos-técnicos)
3. [Conceção do Algoritmo](#conceção-do-algoritmo)
   - 3.1 [Estrutura de Dados](#estrutura-de-dados)
   - 3.2 [Motor de Simulação](#motor-de-simulação)
   - 3.3 [Algoritmos Principais](#algoritmos-principais)
   - 3.4 [Interface Gráfica (GUI)](#interface-gráfica-gui)
4. [Problemas de Concretização](#problemas-de-concretização)
   - 4.1 [Sincronização de Tempos no Evento SAIDA](#1-sincronização-de-tempos-no-evento-saida)
   - 4.2 [Inicialização da Fila de Eventos](#inicialização-da-fila-de-eventos)
   - 4.3 [Validação de Parâmetros no Frontend](#validação-de-parâmetros-no-frontend)
5. [Conclusão](#conclusão)
   - 5.1 [Síntese do Trabalho Realizado](#síntese-do-trabalho-realizado)
   - 5.2 [Pontos Fortes](#pontos-fortes)
   - 5.3 [Aprendizagens Obtidas](#aprendizagens-obtidas)
   - 5.4 [Possíveis Extensões Futuras](#possíveis-extensões-futuras)
   - 5.5 [Avaliação Final](#avaliação-final)

---

## Introdução

O presente projeto consiste no desenvolvimento de um sistema computacional robusto, concebido em linguagem Python, dedicado à simulação de clínicas. O principal objetivo deste sistema é proporcionar aos utilizadores uma ferramenta eficiente e intuitiva para a análise e otimização do funcionamento de unidades clínicas, permitindo a avaliação de diferentes cenários de atendimento, a gestão de filas de espera e o cálculo de métricas críticas de desempenho.

O sistema implementa um motor de simulação avançado que processa eventos de chegada e saída de pacientes de forma cronológica, permitindo estudar o comportamento das filas em diferentes contextos operacionais. A interface gráfica intuitiva facilita a configuração de parâmetros de simulação, enquanto a persistência de dados em JSON permite o armazenamento e análise histórica de simulações anteriores.

Este relatório integra o trabalho desenvolvido no âmbito da Unidade Curricular de Algoritmos e Técnicas de Programação e encontra-se organizado da seguinte forma:

- Apresentação detalhada dos requisitos funcionais e técnicos do sistema, seguida de uma análise minuciosa dos mesmos;
- Descrição pormenorizada da conceção do algoritmo de simulação, estrutura de dados e fluxo de processamento;
- Análise dos problemas enfrentados durante a concretização e respectivas soluções implementadas;
- Reflexão conclusiva sobre o trabalho realizado, destacando os pontos fortes e as aprendizagens obtidas ao longo do processo.

---

## Análise e Requisitos

O sistema foi concebido para atender aos seguintes requisitos principais:

### Requisitos Funcionais

1. **Simulação de Chegada de Pacientes:** O sistema deve simular a chegada de pacientes seguindo uma distribuição de Poisson, permitindo configurar a taxa de chegada em doentes/hora. Esta funcionalidade é essencial para criar cenários realistas de carga de trabalho na clínica.

2. **Gestão de Filas de Espera:** O sistema deve manter e processar filas de espera de pacientes, aplicando critérios de priorização (Normal vs. Urgente) e compatibilidade de especialidades médicas. As filas devem ser atualizadas dinamicamente ao longo da simulação.

3. **Atribuição de Médicos:** O sistema deve permitir configurar o número de médicos e suas especialidades, aplicando algoritmos de alocação que garantem a compatibilidade entre especialidade do paciente e disponibilidade do médico.

4. **Distribuições de Tempo de Serviço:** O sistema deve suportar múltiplas distribuições para modelar tempos de consulta: exponencial (realista para atendimentos clínicos), normal e uniforme.

5. **Cálculo de Métricas:** O sistema deve calcular e disponibilizar métricas estatísticas detalhadas, incluindo:
   - Tempo médio de espera em fila
   - Tempo total em clínica (espera + consulta)
   - Tamanho médio e máximo da fila
   - Ocupação percentual de cada médico
   - Número de pacientes atendidos

6. **Persistência de Simulações:** O sistema deve armazenar histórico de simulações em formato JSON, permitindo recuperar e analisar simulações anteriores.

7. **Visualização de Resultados:** O sistema deve gerar gráficos interativos mostrando a evolução das filas, ocupação de médicos e distribuição de pacientes por especialidade ao longo do tempo.

8. **Utilização de Dataset Realista:** O sistema deve permitir a utilização de dados reais de pacientes (5000 registos com especialidades requeridas) para simulações mais precisas.

### Requisitos Técnicos

- **Linguagem de Programação:** Python 3.8
- **Biblioteca Gráfica:** FreeSimpleGUI para interface desktop intuitiva
- **Visualização de Dados:** Matplotlib para geração de gráficos estatísticos
- **Persistência de Dados:** JSON para armazenamento de configurações e resultados
- **Performance:** Capacidade de simular até 5000 pacientes em tempo razoável

---

## Conceção do Algoritmo

### Estrutura de Dados

#### 1. Representação de Pacientes

Cada paciente é representado como um dicionário Python com os seguintes campos:

```python
paciente = {
    "id": int,                     
    "tempo_chegada": float,         
    "especialidade": str,           
    "prioridade": str,              
    "nome_display": str,            
    "dados_reais": dict ou None     
}
```

**Especialidades:**
- Geral
- Cardiologia
- Ortopedia
- Pediatria
- Dermatologia
- Neurologia
- Psiquiatria
- Gastroenterologia
- Oftalmologia
- Ginecologia
- Urologia

#### 2. Representação de Médicos

Cada médico é representado como um dicionário com estado em tempo real:

```python
medico = {
    "id": int,                      
    "nome": str,                    
    "especialidade": str,           
    "livre": bool,                  
    "tempo_ocupado": float,        
    "num_consultas": int            
}
```

#### 3. Estrutura de Fila de Eventos

O sistema utiliza uma **priority queue (heap)** para armazenar e processar eventos de forma eficiente:

```python
queue_eventos = [
    (tempo_evento, tipo_evento, dados_evento),
    ...
]
```

Onde:
- `tempo_evento`: Momento em que o evento ocorre (float, em minutos)
- `tipo_evento`: CHEGADA (1) ou SAIDA (2)
- `dados_evento`: Informações específicas do evento (paciente, médico, etc)

#### 4. Estrutura de Resultados

Os resultados da simulação são organizados hierarquicamente:

```python
resultados = {
    "globais": {
        "pacientes_atendidos": int,
        "tempo_espera": float,             
        "tempo_consulta": float,
        "tempo_clinica": float,             
        "tamanho_medio_fila": float,
        "tamanho_max_fila": int,
        "ocupacao_media_medicos": float     
    },
    "medicos": [
        {
            "nome": str,
            "especialidade": str,
            "ocupacao": float,              
            "consultas": int,
            "tempo_medio_consulta": float
        },
        ...
    ],
    "log": [
        {
            "medico": str,
            "paciente": str,
            "espera": float,
            "duracao": float,
            "prioridade": str
        },
        ...
    ],
    "series": {
        "tempo": [float],                  
        "fila": [int],                     
        "ocupacao": [int],                  
        "fila_por_especialidade": {         
            "especialidade": [int]
        }
    }
}
```

---


#### Fluxo Principal da Simulação

```
INICIALIZAÇÃO
    ├─ Carregar médicos da base de dados
    ├─ Inicializar fila de eventos com primeiro evento de CHEGADA
    └─ Preparar estruturas de dados estatísticas

LOOP PRINCIPAL (enquanto houver eventos)
    ├─ Extrair próximo evento do heap
    ├─ SE tempo_evento > duracao_simulação
    │  └─ TERMINAR SIMULAÇÃO
    ├─ SE tipo = CHEGADA
    │  ├─ Criar novo paciente
    │  ├─ Procurar médico compatível e disponível
    │  ├─ SE médico encontrado
    │  │  ├─ Agendar SAIDA (fim de consulta)
    │  │  └─ Adicionar à estatística
    │  └─ SENÃO
    │     └─ Adicionar à fila de espera
    │     └─ Agendar próxima CHEGADA
    └─ SE tipo = SAIDA
       ├─ Marcar médico como livre
       ├─ Procurar paciente prioritário na fila
       ├─ SE paciente encontrado
       │  ├─ Remover da fila
       │  ├─ Agendar SAIDA para este paciente
       │  └─ Registar tempo de espera
       └─ Atualizar métricas

CÁLCULO DE MÉTRICAS
    ├─ Computar estatísticas globais
    ├─ Agregar dados por médico
    └─ Preparar series temporais para visualização

RETORNO DE RESULTADOS
```

---

### Algoritmos Principais

#### 1. Algoritmo de Geração de Tempos de Serviço

```python
def gerar_tempo_servico(tempo_medio, distribuicao):
    if distribuicao == "exponencial":
        return random.expovariate(1.0 / tempo_medio)
    elif distribuicao == "normal":
        return max(1, random.gauss(tempo_medio, tempo_medio * 0.2))
    elif distribuicao == "uniforme":
        return random.uniform(tempo_medio * 0.5, tempo_medio * 1.5)
    else:
        return tempo_medio
```

**Justificação:**
- **Exponencial:** Modela realistically o tempo de serviço em clínicas (sem memória, apropriado para processos sem padrão)
- **Normal:** Quando há tempos médios consistentes com pequna variação
- **Uniforme:** Para cenários com limites mínimos e máximos bem definidos

**Validação:** Tempo de serviço nunca inferior a 1 minuto na distribuição normal.

#### 2. Algoritmo de Compatibilidade Médico-Paciente

```python
def verifica_compatibilidade(medico, paciente):
    if medico['especialidade'] == paciente['especialidade']:
        return True
    if medico['especialidade'] == 'Geral':
        return True
    if paciente['especialidade'] == 'Geral':
        return True
    return False
```

**Lógica:**
- Match exato de especialidade: compatível ✓
- Médico generalista: atende qualquer especialidade ✓
- Paciente de especialidade geral: qualquer médico pode atender ✓
- Caso contrário: incompatível ✗

#### 3. Algoritmo de Priorização de Fila

```python
fila_espera.sort(key=lambda p: (
    0 if p['prioridade'] == 'Urgente' else 1,  
    p['tempo_chegada']                          
))
```

**Estratégia:** Two-level priority
- **Nível 1:** Pacientes urgentes têm precedência absoluta
- **Nível 2:** Dentro da mesma prioridade, ordem de chegada (FIFO)

#### 4. Algoritmo de Extração de Paciente da Fila

```python
paciente_da_fila = None
idx_na_fila = -1

for i, p in enumerate(fila_espera):
    if verifica_compatibilidade(medico_disponivel, p):
        paciente_da_fila = p
        idx_na_fila = i
        break  
```

**Comportamento:** Greedy approach - seleciona o primeiro paciente compatível encontrado (já está ordenado por prioridade).

#### 5. Algoritmo de Cálculo de Ocupação

```python
perc_ocupacao = (tempo_ocupado / duracao_simulacao) * 100
ocupacao = min(100, perc_ocupacao) 
```

**Justificação:** 
- Proporção de tempo que o médico efectivamente realizou consultas
- Capped em 100% para evitar anomalias computacionais

#### 6. Algoritmo de Contabilização de Fila por Especialidade

```python
contagem_temp = {}
for paciente in fila_espera:
    esp = paciente['especialidade']
    contagem_temp[esp] = contagem_temp.get(esp, 0) + 1

for especialidade in todas_especialidades:
    qty = contagem_temp.get(especialidade, 0)
    series_fila_esp[especialidade].append(qty)
```

**Propósito:** Gerar data para visualização da distribuição de filas por especialidade.

---

### Interface Gráfica (GUI)

#### Tecnologia

- **Framework:** FreeSimpleGUI (PySimpleGUI)
- **Estilo:** Clean/White palette com acentos azuis
- **Responsividade:** Layout adaptativo para diferentes resoluções

#### Paleta de Cores

```python
HEADER_BG = "#FFFFFF"           
MAIN_BG = "#FFFFFF"             
ACCENT_PRIMARY = "#1E3A8A"      
TEXT_PRIMARY = "#0F172A"       
TEXT_SECONDARY = "#475569"      
METRIC_ACCENT = "#2563EB"       
DIVIDER_COLOR = "#E2E8F0"      
```

#### Estrutura de Janelas

##### 1. Janela Principal de Configuração

**Elementos:**
- Campo de entrada: Taxa de chegada (doentes/hora)
- Campo de entrada: Número de médicos
- Dropdown: Distribuição de serviço (exponencial/normal/uniforme)
- Campo de entrada: Tempo médio de consulta (minutos)
- Campo de entrada: Duração da simulação (minutos)
- Checkbox: Usar dataset realista (5000 pacientes)
- Botão: Executar Simulação
- Botão: Carregar Simulação Histórica
- Botão: Limpar Histórico

**Validações Implementadas:**
- Taxa de chegada: Valor positivo
- Número de médicos: Inteiro positivo (1-100)
- Tempo médio: Não pode ser superior à duração total
- Duração: Valor positivo (mínimo 10 minutos)

##### 2. Janela de Resultados

**Separadores (Tabs):**

**2.1. Métricas Globais**
- Pacientes Atendidos
- Tempo Médio de Espera
- Tempo Médio em Clínica
- Tamanho Médio da Fila
- Tamanho Máximo da Fila
- Ocupação Média da Equipa

**2.2. Gráficos**
- Gráfico 1: Evolução da fila ao longo do tempo
- Gráfico 2: Ocupação de médicos (série temporal)
- Gráfico 3: Distribuição de fila por especialidade
- Gráfico 4: Comparativo de carga por médico

**2.3. Tabela de Médicos**
- Nome
- Especialidade
- % de Ocupação (barra visual)
- Número de Consultas
- Tempo Médio por Consulta

**2.4. Log Detalhado**
- Lista scrollable de todos os atendimentos
- Colunas: Médico, Paciente, Especialidade, Tempo Espera, Duração

**2.5. Ficha de Paciente (Popup)**
- Informações de paciente selecionado
- Médico atendedor
- Tempos de espera e consulta
- Prioridade

##### 3. Popups Especializados

**Popup de Erro Visual:**
```
⛔ TÍTULO_ERRO
_______________________
Mensagem Principal (negrito)
Detalhes adicionais
```

**Popup de Confirmação:**
```
Pergunta ao utilizador
[Sim] [Não]
```

**Popup de Ficha de Atendimento:**
```
Ficha de Atendimento
👤 Paciente: Nome (ID)
🏥 Especialidade: Especialidade
⏳ Tempo Espera: X.XX min
⏱️ Duração: Y.YY min
```

#### Fluxo de Interação

```
UTILIZADOR INICIA APLICAÇÃO
    ↓
CARREGA HISTÓRICO SIMULAÇÕES (JSON)
    ↓
APRESENTA INTERFACE PRINCIPAL
    ↓
UTILIZADOR INSERE PARÂMETROS
    ↓
VALIDA INPUTS
    ├─ SE INVÁLIDO → MOSTRA ERRO E AGUARDA CORREÇÃO
    └─ SE VÁLIDO → PROSSEGUE
    ↓
EXECUTA SIMULAÇÃO (backend.simular_clinica_real)
    ↓
RECEBE RESULTADOS
    ↓
APRESENTA GRÁFICOS E MÉTRICAS
    ↓
PERMITE SALVAR SIMULAÇÃO
    ↓
AGUARDA PRÓXIMA AÇÃO
```

#### Gestão de Gráficos

**Integração Matplotlib:**
```python
import matplotlib.pyplot as plt


fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)


ax1.plot(series_tempo, series_fila, 'b-', linewidth=2)
ax1.set_xlabel('Tempo (minutos)')
ax1.set_ylabel('Tamanho da Fila')
ax1.grid(True, alpha=0.3)


ax2.plot(series_tempo, series_ocupacao, 'g-', linewidth=2)
ax2.set_ylabel('Médicos Ocupados')


for esp, valores in series_fila_esp.items():
    ax3.plot(series_tempo, valores, label=esp, linewidth=1.5)
ax3.legend()


ocupacoes = [m['ocupacao'] for m in medicos]
ax4.boxplot(ocupacoes)

plt.tight_layout()
plt.show()
```

---

## Problemas de Concretização

### 1. **Sincronização de Tempos no Evento SAIDA**

**Problema:** 
Inicialmente, ao processar o evento SAIDA, havia casos onde o paciente era removido da fila mas não era realizado o cálculo correto do tempo de espera, causando inconsistências nas estatísticas.

**Solução Implementada:**
```python
elif tipo_evento == SAIDA:
    medico_que_acabou, paciente_que_saiu = dados
    medico_que_acabou['livre'] = True
    
    
    tempo_espera = tempo_atual - paciente_que_saiu['tempo_chegada']
    stats_tempos_espera.append(tempo_espera)
    stats_tempos_clinica.append(tempo_espera + duracao_consulta)
```

**Justificação:** O tempo de espera é calculado ANTES da remoção da fila, garantindo precisão.

---

### 2. **Inicialização da Fila de Eventos**

**Problema:** 
Se a primeira chegada fosse agendada muito perto de tempo=0 ou exatamente em 0, alguns pacientes poderiam ser ignorados.

**Solução:**
```python
taxa_por_min = taxa_chegada / 60.0  
primeira_chegada = random.expovariate(taxa_por_min)
heapq.heappush(queue_eventos, (primeira_chegada, CHEGADA, None))


prox_chegada = tempo_atual + random.expovariate(taxa_por_min)
if prox_chegada <= duracao_sim:
    heapq.heappush(queue_eventos, (prox_chegada, CHEGADA, None))
```

**Justificação:** Garante que eventos sempre estão agendados dentro do intervalo de simulação.


### 3. **Validação de Parâmetros no Frontend**

**Problema:** 
Parâmetros inválidos (negativos, zero, etc) causavam exceções não tratadas no backend.

**Solução no tb.py:**
```python
try:
    taxa_chegada = float(values['taxa_chegada_input'])
    if taxa_chegada <= 0:
        raise ValueError("Taxa de chegada deve ser positiva")
    
    num_medicos = int(values['num_medicos_input'])
    if num_medicos < 1 or num_medicos > 100:
        raise ValueError("Número de médicos deve estar entre 1 e 100")
    
    tempo_medio = float(values['tempo_medio_input'])
    duracao_sim = float(values['duracao_input'])
    
    if tempo_medio > duracao_sim:
        raise ValueError(f"Tempo médio ({tempo_medio}) não pode ser superior à duração ({duracao_sim})")
    
    
except ValueError as e:
    popup_erro_visual("Validação de Parâmetros", str(e), "Verifique os valores introduzidos")
```

**Justificação:** Validação em camada de apresentação previne erros no motor.

---

## Conclusão

### Síntese do Trabalho Realizado

O projeto de Simulador de Clínica representa uma implementação bem-sucedida de um motor de **Discrete Event Simulation** com interface gráfica profissional. O sistema atinge todos os objetivos propostos:

✅ **Motor de Simulação Robusto:** Implementação eficiente usando heap para gestão de eventos  
✅ **Interface Intuitiva:** Frontend em FreeSimpleGUI com design clean e responsivo  
✅ **Análise Detalhada:** Geração de métricas abrangentes e visualizações gráficas  
✅ **Persistência de Dados:** Histórico de simulações em JSON com compatibilidade UTF-8  
✅ **Dataset Realista:** Suporte para 5000 pacientes com especialidades variadas  
✅ **Algoritmos Sofisticados:** Priorização, compatibilidade, múltiplas distribuições  

### Pontos Fortes

1. **Eficiência Computacional:** O uso de heap garante que o motor processa apenas eventos relevantes, permitindo simular cenários com milhares de pacientes

2. **Flexibilidade de Configuração:** Suporte para diferentes distribuições de tempo de serviço (exponencial, normal, uniforme) permite modelar diversos cenários reais

3. **Priorização Inteligente:** Sistema de duas camadas (urgência + FIFO) reflete práticas clínicas reais

4. **Compatibilidade de Especialidades:** Lógica de matching entre médicos e pacientes garante realismo

5. **Visualizações Ricas:** Gráficos multi-eixo fornecem insights sobre dinâmica da clínica

6. **Tratamento de Erros:** Validações em múltiplas camadas e fallbacks graciosos

### Aprendizagens Obtidas

- **Estruturas de Dados:** Aplicação prática de heaps e sua importância em algoritmos eficientes
- **Interfacing:** Integração de múltiplas bibliotecas (FreeSimpleGUI, Matplotlib, JSON) de forma coesa
- **Tratamento de Erros:** Importância de validação em camadas múltiplas
- **Persistência:** Handling de dados estruturados e UTF-8 para suporte a português



### Avaliação Final

O sistema demonstra uma implementação coerente e profissional de conceitos avançados de programação e simulação. A combinação de um motor de simulação robusto com uma interface gráfica intuitiva resulta numa ferramenta prática e educativa, potencialmente útil para análise e otimização de unidades clínicas reais.

---


