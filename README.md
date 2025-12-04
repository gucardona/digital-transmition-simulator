# Simulador de Transmissão Digital - Redes de Computadores

**Universidade do Vale do Rio dos Sinos (UNISINOS)**

* **Disciplina:** Redes de Computadores
* **Professor:** Cristiano Bonato Both
* **Semestre:** 2025/02
* **Alunos:** Gustavo Parcianello Cardona, Murilo Schuck

---

## Índice

1. [Objetivo](#objetivo)
2. [Contextualização](#contextualização)
3. [Arquitetura do Sistema](#arquitetura-do-sistema)
4. [Tecnologias Implementadas](#tecnologias-implementadas)
5. [Como Executar](#como-executar)
6. [Resultados e Análises](#resultados-e-análises)
7. [Conclusão](#conclusão)

---

## Objetivo

Desenvolver e aplicar os conceitos de **codificação de canal** e **modulação digital**, analisando seu impacto na **Taxa de Erro de Bits (BER)** e na eficiência espectral de sistemas de comunicação.

O simulador implementa um sistema completo de transmissão digital, desde a geração da mensagem até a recuperação da informação no receptor, em condições de ruído controlado.

### Objetivos específicos:
- Implementar codificação de canal (Manchester e AMI Bipolar)
- Implementar modulação digital (BPSK, QPSK, 16-QAM, 64-QAM)
- Simular canal ruidoso (AWGN) com SNR configurável
- Calcular e comparar BER entre diferentes esquemas

---

## Arquitetura do Sistema

O simulador implementa o fluxo completo de transmissão digital:

```
┌─────────────────────────────────────────────────────────────────┐
│                         TRANSMISSOR                             │
└─────────────────────────────────────────────────────────────────┘
       │
       ▼
   [ ASCII ]  ─────→  "Hello World"
       │
       ▼
   [ Bits ]   ─────→  01001000 01100101 01101100...
       │
       ▼
   [ Encoder ] ─────→  Manchester ou AMI Bipolar
       │
       ▼
   [ Modulator ] ───→  BPSK/QPSK/16-QAM/64-QAM
       │
       ▼
┌─────────────────────────────────────────────────────────────────┐
│                      CANAL COM RUÍDO (AWGN)                     │
│                        SNR configurável                         │
└─────────────────────────────────────────────────────────────────┘
       │
       ▼
   [ Símbolos + Ruído ]
       │
       ▼
┌─────────────────────────────────────────────────────────────────┐
│                           RECEPTOR                              │
└─────────────────────────────────────────────────────────────────┘
       │
       ▼
   [ Demodulator ] ──→  Decisão por distância mínima
       │
       ▼
   [ Decoder ] ───────→  Reconstrução dos níveis de linha
       │
       ▼
   [ Bits ] ──────────→  01001000 01100101 01101100...
       │
       ▼
   [ ASCII ] ─────────→  "Hello World"
       │
       ▼
   [ BER Calculation ] → Taxa de erro de bits
```

---

## Tecnologias Implementadas

### 1. Codificação de Canal

#### **Manchester Encoder**
- Cada bit é representado por uma transição
  - Bit 0: LOW → HIGH (transição ascendente)
  - Bit 1: HIGH → LOW (transição descendente)

#### **AMI Bipolar Encoder**
- Usa três níveis de tensão
  - Bit 0: Nível 0
  - Bit 1: Alterna entre +1 e -1

### 2. Modulação Digital

| Modulação | Bits/Símbolo | Pontos na Constelação |
|-----------|--------------|----------------------|
| **BPSK**  | 1            | 2                    |
| **QPSK**  | 2            | 4                    |
| **16-QAM**| 4            | 16                   |
| **64-QAM**| 6            | 64                   |


### 3. Canal Ruidoso (AWGN)

**AWGN** = Additive White Gaussian Noise (Ruído Gaussiano Branco Aditivo)

---

## Como Executar

### Pré-requisitos

- Python 3.8 ou superior
- Bibliotecas: `numpy`, `matplotlib`

### Instalação das Dependências

```bash
pip install numpy matplotlib
```

### Estrutura de Arquivos

```
digital-transmission-simulator/
│
├── src/
│   ├── data.py              # ASCII ↔ Bits
│   ├── encoder.py           # Manchester e AMI Bipolar
│   ├── modulator.py         # BPSK, QPSK, 16-QAM, 64-QAM
│   ├── noise.py             # Canal AWGN
│   ├── utils.py             # Funções auxiliares e BER
│   ├── main.py              # demo
│   └── benchmark_ber.py     # Benchmark BER vs SNR
│
├── README.md
└── .gitignore
```

### Execução

#### 1. Simulação Completa (Demo)

Executa o fluxo completo com visualizações:

```bash
python src/main.py
```

#### 2. Benchmark BER vs SNR

Gera o gráfico comparativo principal:

```bash
python src/benchmark_ber.py
```

---

## Resultados e Análises

### Gráfico Principal: BER vs SNR

![BER vs SNR](benchmark_result.png)

**Configuração do teste:**
- Mensagem: 10.000 caracteres (80.000 bits)
- SNR: 0 a 30 dB (passos de 1 dB)
- Total: 8 combinações testadas

### Observações do Gráfico

#### 1️⃣ **Desempenho em SNR Baixo (0-10 dB)**

**BPSK e QPSK dominam:**
- BPSK atinge BER < 10⁻³ com SNR ≈ 8 dB
- QPSK atinge BER < 10⁻³ com SNR ≈ 10 dB

**16-QAM e 64-QAM sofrem:**
- BER permanece alto (> 10⁻¹) até SNR ≈ 12-15 dB
- Símbolos muito próximos → facilmente confundidos com ruído

**Explicação:** Em ambientes ruidosos (SNR baixo), modulações simples com poucos símbolos bem separados são mais confiáveis.

#### 2️⃣ **Região de Transição (10-20 dB)**

Esta é a região onde ocorrem os **crossover points** - pontos onde vale a pena trocar de modulação:

- **SNR ≈ 10 dB:** QPSK começa a ter BER aceitável
- **SNR ≈ 14 dB:** 16-QAM torna-se viável
- **SNR ≈ 20 dB:** 64-QAM finalmente atinge BER < 10⁻³

**Aplicação prática:** Sistemas como WiFi e 4G usam **modulação adaptativa** nesta região, escolhendo a modulação ideal baseado no SNR medido em tempo real.

#### 3️⃣ **Desempenho em SNR Alto (>20 dB)**

Todas as modulações convergem para **BER muito baixo** (< 10⁻⁵):
- Ruído é insignificante comparado ao sinal
- Até 64-QAM consegue funcionar perfeitamente

**Mas qual é melhor?**
Embora todas tenham BER baixo, **64-QAM transmite 6× mais dados que BPSK** no mesmo tempo! Por isso é preferido quando o sinal é bom.

#### 4️⃣ **Comparação Manchester vs AMI Bipolar**

**Observação importante:** As curvas de Manchester e AMI para a mesma modulação são **praticamente idênticas**.

**Por quê?**
- O BER é medido **após a demodulação**, comparando bits de modulação
- Ambos encoders transformam bits em níveis de linha de forma determinística
- O ruído afeta os **símbolos modulados**, não diretamente os níveis de linha
- Portanto, para a mesma modulação, o BER é similar

**Diferença real:**
- **Eficiência espectral:** AMI é 2× mais eficiente (não duplica símbolos)
- **Sincronização:** Manchester garante transições (melhor clock recovery)
- **Detecção de erros:** AMI permite detectar violações de polaridade

### Tabela Comparativa

| Modulação | SNR para BER < 10⁻³ | Bits/Símbolo | Aplicação Real |
|-----------|---------------------|--------------|----------------|
| **BPSK** | ~8 dB | 1 | GPS, satélites distantes, controle espacial |
| **QPSK** | ~10 dB | 2 | DVB-S (TV satélite), links ponto-a-ponto |
| **16-QAM** | ~14 dB | 4 | 4G LTE, WiFi 4, TV digital terrestre |
| **64-QAM** | ~20 dB | 6 | WiFi 5/6, 5G (boa cobertura), cabo DOCSIS |

### Análise do Trade-off: Robustez vs Eficiência

**Robustez (SNR mínimo):**
```
BPSK (8 dB) > QPSK (10 dB) > 16-QAM (14 dB) > 64-QAM (20 dB)
```

**Eficiência (bits/símbolo):**
```
64-QAM (6 bits) > 16-QAM (4 bits) > QPSK (2 bits) > BPSK (1 bit)
```

**Conclusão:** Não existe modulação "melhor" - existe a modulação **adequada para cada cenário de SNR**.

### Impacto do BER na Comunicação

| BER | Qualidade | Impacto Prático |
|-----|-----------|-----------------|
| **> 10⁻¹** | Péssimo | Comunicação inviável (>10% de erros) |
| **10⁻³** | Aceitável | WiFi/4G operam nesta faixa (com FEC) |
| **10⁻⁶** | Bom | Comunicações confiáveis |
| **10⁻⁹** | Excelente | Padrão para Ethernet, fibra óptica |
| **< 10⁻¹²** | Praticamente perfeito | Enlaces de fibra de alta qualidade |

**Nota:** Sistemas reais usam **FEC** (Forward Error Correction) - códigos que adicionam redundância para corrigir erros. Isso permite operar com BER aparente de 10⁻³ mas entregar BER efetivo < 10⁻⁹ após correção.

---

## Conclusão

### Principais Aprendizados

1. **Trade-off Fundamental:**
   - Não existe modulação universalmente melhor
   - Escolha depende do SNR disponível e requisitos de throughput
   - Sistemas reais usam modulação adaptativa para otimizar

2. **Importância do SNR:**
   - SNR baixo (< 10 dB): Use BPSK/QPSK
   - SNR médio (10-20 dB): 16-QAM é ideal
   - SNR alto (> 20 dB): 64-QAM maximiza throughput

3. **Codificação de Canal:**
   - Manchester: Melhor sincronização, menor eficiência
   - AMI: Melhor eficiência, detecção de erros

4. **Aplicações Práticas:**
   - GPS usa BPSK porque precisa funcionar com sinal fraquíssimo
   - WiFi usa 64-QAM quando você está perto do roteador
   - 4G/5G ajustam modulação dinamicamente (CQI - Channel Quality Indicator)

### Limitações do Simulador

1. **Modelo de canal simplificado:**
   - Apenas AWGN (ruído branco gaussiano)
   - Não considera: fading, interferência, multi-percurso

2. **Sem códigos de correção de erro (FEC):**
   - Sistemas reais usam Turbo codes, LDPC, etc.
   - FEC melhora dramaticamente o BER efetivo

3. **Sem overhead de protocolo:**
   - Não considera headers, preâmbulos, checksums
   - Throughput real seria ~15-20% menor

4. **Modelo estático:**
   - Canal não varia no tempo
   - Sistemas reais têm SNR variável

### Trabalhos Futuros

- Implementar códigos de correção de erro (Hamming, Reed-Solomon)
- Adicionar modelo de canal com fading (Rayleigh, Rician)
- Simular modulação adaptativa automática (link adaptation)
- Implementar equalização de canal
- Adicionar métricas de throughput efetivo

---