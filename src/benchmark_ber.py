import numpy as np
import matplotlib.pyplot as plt

import data as data
import encoder as encoder
import modulator as modulator
import utils as utils
import noise as noise

from utils import EncoderID, ModulatorID, NoiseID


def run_ber_snr_benchmark(
    message: str = "benchmark message",
    snr_list_db: list[float] | np.ndarray = None,
    combinations: list[tuple[EncoderID, ModulatorID]] | None = None,
):
    """Executa benchmark BER vs SNR para múltiplas combinações Encoder+Modulador.

    Parâmetros:
    - message: texto base para geração de bits.
    - snr_list_db: lista ou array de SNRs em dB (default 0..20 em passos de 2).
    - combinations: lista de tuplas (EncoderID, ModulatorID). Se None, usa um conjunto padrão.

    Retorna: dict(label -> np.ndarray de BERs) e plota o gráfico.
    """
    if snr_list_db is None:
        # Mais pontos: 0 a 30 dB com passo de 0.5 dB
        snr_list_db = np.arange(0.0, 30.0 + 0.5, 0.5)

    if combinations is None:
        combinations = [
            (EncoderID.MANCHESTER, ModulatorID.BPSK),
            (EncoderID.MANCHESTER, ModulatorID.QPSK),
            (EncoderID.MANCHESTER, ModulatorID.QAM16),
            (EncoderID.MANCHESTER, ModulatorID.QAM64),
            (EncoderID.AMI_BIPOLAR, ModulatorID.BPSK),
            (EncoderID.AMI_BIPOLAR, ModulatorID.QPSK),
            (EncoderID.AMI_BIPOLAR, ModulatorID.QAM16),
            (EncoderID.AMI_BIPOLAR, ModulatorID.QAM64),
        ]

    # Preparar dados e ruído
    data_bits = data.text_to_bits(message)
    awgn = utils.select_noise(NoiseID.AWGN)

    series = {}
    plt.figure(figsize=(10, 6))

    for enc_id, mod_id in combinations:
        enc = utils.select_encoder(enc_id)
        mod = utils.select_modulator(mod_id)
        encoder_name = enc.__class__.__name__.replace("Encoder", "")
        modulator_name = mod.__class__.__name__.replace("Modulator", "")
        label = f"{encoder_name} + {modulator_name}"

        # Codificar linha e preparar bits de referência para BER pós-modulação
        encoded_signal = enc.encode(data_bits)
        tx_mod_bits = utils.bits_for_modulation(encoded_signal, modulator_name)

        ber_list = []
        for snr_db in snr_list_db:
            tx_symbols = mod.modulate(encoded_signal)
            rx_symbols = awgn.aplicar(tx_symbols, snr_db)
            rx_bits = mod.demodulate(rx_symbols)
            ber, errors, compared = utils.compute_ber(tx_mod_bits, rx_bits)
            ber_list.append(ber)

        ber_arr = np.array(ber_list)
        series[label] = ber_arr
        plt.plot(snr_list_db, ber_arr, marker='o', label=label)

    plt.grid(True, alpha=0.3)
    plt.xlabel('SNR (dB)')
    plt.ylabel('BER pós-modulação')
    plt.title('BER vs SNR (Múltiplas combinações Encoder + Modulador)')
    plt.legend()
    plt.tight_layout()
    plt.show()

    return series

if __name__ == "__main__":
    # Exemplo rápido com múltiplas combinações
    run_ber_snr_benchmark(message="Teste de BER em múltiplas combinações")