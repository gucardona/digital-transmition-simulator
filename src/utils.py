import encoder as encoder
import modulator as modulator

def select_encoder(encoder_num: int) -> encoder:
    """Seleciona o encoder baseado no número fornecido"""
    if encoder_num == 1:
        return encoder.ManchesterEncoder()
    elif encoder_num == 2:
        return encoder.AMIBipolarEncoder()
    else:
        raise ValueError("Número de encoder inválido. Use 1 para Manchester ou 2 para AMI Bipolar.")


def select_modulator(modulator_num: int) -> modulator:
    """Seleciona o modulador baseado no número fornecido"""
    if modulator_num == 1:
        return modulator.BPSKModulator()
    elif modulator_num == 2:
        return modulator.QPSKModulator()
    elif modulator_num == 3:
        return modulator.QAM16Modulator()
    elif modulator_num == 4:
        return modulator.QAM64Modulator()
    else:
        raise ValueError("Número de modulador inválido. Use 1 para BPSK, 2 para QPSK, 3 para 16-QAM ou 4 para 64-QAM.")