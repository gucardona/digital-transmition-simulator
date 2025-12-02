# Simulador de Transmissão Digital - Redes de Computadores

**Universidade do Vale do Rio dos Sinos (UNISINOS)**

  * **Disciplina:** Redes de Computadores
  * **Professor:** Cristiano Bonato Both
  * **Semestre:** 2025/02
  * **Alunos:** Gustavo Parcianello Cardona, Murilo Schuck

-----

## Objetivo

Este projeto visa desenvolver um simulador completo de um sistema de transmissão digital, permitindo a análise prática dos conceitos de **codificação de canal** e **modulação digital**. O trabalho tem como meta analisar o impacto dessas técnicas na **Taxa de Erro de Bits (BER)** e na eficiência espectral de sistemas de comunicação.

O simulador cobre o fluxo de comunicação desde a geração da mensagem até a transmissão, permitindo visualizar como os dados são transformados em cada etapa.

-----

## Funcionalidades Implementadas

Atualmente, o simulador cobre as etapas de transmissão do sistema (Itens 1, 2 e 3 da avaliação descrita no PDF):

### 1\. Geração de Dados (`src/data.py`)

Responsável por converter a informação humana em dados brutos para transmissão.

  * **Conversão ASCII para Binário:** Transforma strings de texto em vetores de bits, onde cada caractere é representado por 8 bits.
  * **Conversão Binário para ASCII:** Reverte o processo para verificar a integridade da mensagem.
  * **Formatação:** Utilitários para visualização legível dos bytes gerados.

### 2\. Codificação de Canal (`src/encoder.py`)

Implementa técnicas de codificação de linha para adequar o sinal ao meio de transmissão.

  * **Manchester:** Divide cada bit em dois níveis de sinal (Low-High para '0', High-Low para '1').
  * **AMI Bipolar (Alternate Mark Inversion):** Utiliza três níveis de tensão (+1, 0, -1), alternando a polaridade nos bits '1' para evitar componente DC.

**Visualização:** O sistema gera gráficos temporais mostrando os bits originais comparados com o sinal codificado resultante.

### 3\. Modulação Digital + Demodulação (`src/modulator.py`)

Mapeia os bits (ou sinais codificados) em símbolos complexos para transmissão em banda passante.

  * **BPSK (Binary Phase Shift Keying):** 1 bit por símbolo.
  * **QPSK (Quadrature Phase Shift Keying):** 2 bits por símbolo.
  * **16-QAM:** 4 bits por símbolo.
  * **64-QAM:** 6 bits por símbolo.

**Visualização:** O sistema gera gráficos da Constelação (plano I/Q), permitindo visualizar a dispersão dos símbolos.

-----

## Estrutura do Projeto

```text
digital-transmission-simulator/
│
├── src/
│   ├── data.py       # Manipulação de texto e conversão binária
│   ├── encoder.py    # Algoritmos de codificação (Manchester, AMI) e plots
│   ├── modulator.py  # Modulação + demodulação (PSK, QAM) e plots
│   ├── noise.py      # Canal (AWGN)
│   ├── utils.py      # Seletores (Encoder/Modulator/Noise) e helpers
│   └── main.py       # Ponto de entrada e configuração da simulação
│
├── .gitignore        # Arquivos ignorados pelo git
└── README.md         # Documentação do projeto
```

-----

## Como Executar e Configurar

### Pré-requisitos

  * Python 3.8 ou superior
  * Bibliotecas: `numpy`, `matplotlib`

Instalação das dependências:

```bash
pip install numpy matplotlib
```

### Execução e Customização

Para rodar a simulação, execute o arquivo principal:

```bash
python src/main.py
```

### Alterando os Parâmetros da Simulação

Você pode alterar a mensagem enviada, o tipo de codificação e a modulação editando diretamente o arquivo `src/main.py`.

Abra o arquivo `src/main.py` e localize as seguintes linhas dentro da função `main()`:

**1. Alterar a mensagem de texto:**
Modifique a variável `message` para enviar qualquer string desejada.

```python
message = "Sua Mensagem Aqui"  # Digite o texto que deseja simular
```

**2. Alterar o Encoder (Codificação de Canal):**
Modifique o número passado para a função `utils.select_encoder(ID)`.

```python
# Opções disponíveis:
# 1: Manchester
# 2: AMI Bipolar

selected_encoder = utils.select_encoder(1) # Exemplo: Altere 1 para 2 para usar AMI
```

**3. Alterar o Modulador:**
Modifique o número passado para a função `utils.select_modulator(ID)`.

```python
# Opções disponíveis:
# 1: BPSK
# 2: QPSK
# 3: 16-QAM
# 4: 64-QAM

selected_modulator = utils.select_modulator(4) # Exemplo: Altere 4 para 2 para usar QPSK
```

Após salvar as alterações no arquivo, execute novamente o comando `python src/main.py` para visualizar os novos gráficos e logs gerados.

-----

## Próximas Implementações (Em Desenvolvimento)

As seguintes funcionalidades estão planejadas para completar os requisitos do trabalho:

### 4\. Demodulação (Integrada nas Classes de Modulação)

Cada classe em `modulator.py` possui método `demodulate(received)` que:
  * BPSK: decisão simples por sinal do eixo real.
  * QPSK / QAM: decisão por distância mínima (nearest neighbor) revertendo normalização.

Reconstituição dos níveis de linha para decodificação é feita por `utils.reconstruct_line_levels(...)` antes de chamar `encoder.decode`.

### 5\. Simulação de Canal Ruidoso (AWGN)

Implementado em `noise.py`:
  * Adição de ruído gaussiano branco aditivo conforme SNR.
  * Plot da constelação com símbolos ruidosos sobrepostos.

### 6\. Decodificação

`encoder.decode` reverte Manchester (pares) ou AMI (polos alternados) após reconstrução.

### 7\. Análise de Desempenho (BER) (Planejado)

  * Comparação bit a bit entre mensagem enviada e recebida.
  * Cálculo da Taxa de Erro de Bits (BER) e gráficos BER x SNR.

-----

## Exemplos de Saída (Logs)

Ao executar o código com a configuração padrão, você verá uma saída similar a esta no console:

```text
Mensagem ASCII: 'test message! longer than 8 bits'

Mensagem binária: 01110100 01100101 ... 01110011

Mensagem binária: 01101111

Mensagem ASCII recuperada: 'o'

Sinal Manchester codificado: [-1.  1.  1. -1.  1. -1. -1.  1.  1. -1.  1. -1.  1. -1.  1. -1.]

Sinal modulado QAM64: [(-0.1543+0.1543j) (-0.1543-0.1543j) ...]
```
