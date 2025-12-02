import encoder as encoder
import modulator as modulator
import noise as noise
import numpy as np
from enum import IntEnum


# Enums para seleção de esquemas (compatíveis com inteiros)
class EncoderID(IntEnum):
    MANCHESTER = 1
    AMI_BIPOLAR = 2

class ModulatorID(IntEnum):
    BPSK = 1
    QPSK = 2
    QAM16 = 3
    QAM64 = 4

class NoiseID(IntEnum):
    AWGN = 1


def select_encoder(encoder_num: int | EncoderID) -> encoder:
    """Seleciona o encoder baseado no número fornecido"""
    if int(encoder_num) == EncoderID.MANCHESTER:
        return encoder.ManchesterEncoder()
    elif int(encoder_num) == EncoderID.AMI_BIPOLAR:
        return encoder.AMIBipolarEncoder()
    else:
        raise ValueError("Número de encoder inválido. Use 1 para Manchester ou 2 para AMI Bipolar.")


def select_modulator(modulator_num: int | ModulatorID) -> modulator:
    """Seleciona o modulador baseado no número fornecido"""
    if int(modulator_num) == ModulatorID.BPSK:
        return modulator.BPSKModulator()
    elif int(modulator_num) == ModulatorID.QPSK:
        return modulator.QPSKModulator()
    elif int(modulator_num) == ModulatorID.QAM16:
        return modulator.QAM16Modulator()
    elif int(modulator_num) == ModulatorID.QAM64:
        return modulator.QAM64Modulator()
    else:
        raise ValueError("Número de modulador inválido. Use 1 para BPSK, 2 para QPSK, 3 para 16-QAM ou 4 para 64-QAM.")


def select_noise(noise_num: int | NoiseID) -> noise:
    """Seleciona o modelo de ruído baseado no número fornecido"""
    if int(noise_num) == NoiseID.AWGN:
        return noise.AWGNNoise()
    else:
        raise ValueError("Número de ruído inválido. Use 1 para AWGN.")


def reconstruct_line_levels(bits_demod: np.ndarray, encoder_name: str, original_length: int | None = None) -> np.ndarray:
    """Reconstrói níveis de linha a partir de bits demodulados conforme o encoder.

    Parâmetros:
    - bits_demod: sequência de bits (0/1) saída da demodulação.
    - encoder_name: nome da classe de encoder (ex: 'Manchester').
    - original_length: número de bits antes da codificação de linha. Necessário
      para distinguir se 'bits_demod' já representam sub-bits Manchester.

    Regras:
    - Manchester:
        * Se len(bits_demod) == 2 * original_length (sub-bits já em pares),
          agrupa pares e reconstrói níveis (-1,+1) ou (+1,-1) sem duplicar.
        * Caso contrário (não sabemos tamanho original), assume cada bit lógico
          e expande (comportamento anterior).
    - AMI Bipolar: 1 alterna polaridade (+1/-1), 0 -> 0 (sem expansão).
    - Fallback NRZ: 0 -> -1, 1 -> +1.
    """
    name = encoder_name.lower()
    if name == "manchester":
        if original_length is not None and len(bits_demod) == 2 * original_length:
            # bits_demod contém sub-bits: cada par forma um bit Manchester
            levels = []
            for i in range(original_length):
                a = bits_demod[2*i]
                b = bits_demod[2*i + 1]
                # Mapear (0,1) -> [-1,+1]; (1,0) -> [+1,-1]
                if a == 0 and b == 1:
                    levels.extend([-1, +1])
                elif a == 1 and b == 0:
                    levels.extend([+1, -1])
                else:
                    # Par inválido (erro de demodulação); estratégia simples: marcar como transição de erro
                    levels.extend([0, 0])
            return np.array(levels)
        else:
            # Comportamento legado: tratar cada bit como lógico e expandir
            levels = []
            for b in bits_demod:
                if b == 0:
                    levels.extend([-1, +1])
                else:
                    levels.extend([+1, -1])
            return np.array(levels)
    elif name in ("amibipolar", "ami_bipolar", "ami"):
        levels = []
        last_one = -1
        for b in bits_demod:
            if b == 1:
                last_one = -last_one
                levels.append(last_one)
            else:
                levels.append(0)
        return np.array(levels)
    else:
        return np.where(bits_demod == 1, 1, -1).astype(int)


## Demodulação agora é responsabilidade de cada classe em `modulator.py`.
## Use: selected_modulator.demodulate(received_signal)


def bits_for_modulation(signal: np.ndarray, modulator_name: str) -> np.ndarray:
    """Converte níveis de linha (-1,+1 ou -1,0,+1) em bits (0/1) e aplica
    o mesmo padding esperado pelo modulador, para alinhar comprimento com os
    bits demodulados.

    Regras:
    - BPSK: 1 bit por símbolo (sem padding além do original)
    - QPSK: padding para múltiplos de 2
    - 16-QAM: padding para múltiplos de 4
    - 64-QAM: padding para múltiplos de 6
    """
    name = modulator_name.lower()
    # Mapear níveis para bits lógicos
    bits = ((signal + 1) / 2).astype(int)
    # Determinar tamanho do grupo
    if name == "bpsk":
        group = 1
    elif name == "qpsk":
        group = 2
    elif name in ("qam16", "16qam", "16-qam"):
        group = 4
    elif name in ("qam64", "64qam", "64-qam"):
        group = 6
    else:
        group = 1  # Fallback conservador
    pad_len = (group - (len(bits) % group)) % group
    if pad_len:
        bits = np.append(bits, np.zeros(pad_len, dtype=int))
    return bits.astype(int)


def compute_ber(tx_bits: np.ndarray, rx_bits: np.ndarray, original_length: int | None = None) -> tuple[float, int, int]:
    """Calcula Bit Error Rate (BER).

    Parâmetros:
    - tx_bits: bits transmitidos na etapa comparada (após mapeamento para bits de modulação).
    - rx_bits: bits recebidos demodulados na mesma etapa.
    - original_length: opcional, para truncar comparação caso exista conhecimento do tamanho original (por exemplo, para ignorar bits extras em pipelines).

    Retorna:
    - (ber, errors, compared): taxa de erro, contagem de erros, número de bits comparados.
    """
    # Garantir arrays 1D de ints
    tx_bits = np.asarray(tx_bits, dtype=int).flatten()
    rx_bits = np.asarray(rx_bits, dtype=int).flatten()

    # Determinar comprimento de comparação
    n = min(len(tx_bits), len(rx_bits))
    if original_length is not None:
        n = min(n, int(original_length))
    if n == 0:
        return (0.0, 0, 0)

    tx_c = tx_bits[:n]
    rx_c = rx_bits[:n]
    errors = int(np.sum(tx_c != rx_c))
    ber = errors / n
    return (ber, errors, n)