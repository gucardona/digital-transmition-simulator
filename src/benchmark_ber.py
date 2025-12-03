import numpy as np
import matplotlib.pyplot as plt

import data as data
import encoder as encoder
import modulator as modulator
import utils as utils
import noise as noise

from utils import EncoderID, ModulatorID, NoiseID


def run_throughput_snr_benchmark(
    message: str = "A" * 10000,
    snr_list_db: list[float] | np.ndarray = None,
    combinations: list[tuple[EncoderID, ModulatorID]] | None = None,
    symbol_rate_hz: float = 1e6,  # Taxa de símbolos: 1 MHz (1 milhão de símbolos/segundo)
):
    """Executa benchmark de Throughput Efetivo vs SNR.

    O throughput efetivo considera apenas os bits transmitidos corretamente,
    simulando um sistema sem retransmissão (ou contando retransmissões como perda).

    Fórmula:
    Throughput = bits_por_símbolo × (1 - BER) × taxa_de_símbolos

    Parâmetros:
    - message: texto base para geração de bits.
    - snr_list_db: lista ou array de SNRs em dB.
    - combinations: lista de tuplas (EncoderID, ModulatorID).
    - symbol_rate_hz: taxa de símbolos em Hz (default: 1 MHz).

    Retorna: dict(label -> np.ndarray de throughputs) e plota o gráfico.
    """
    if snr_list_db is None:
        snr_list_db = np.arange(0.0, 30.0 + 1.0, 1.0)

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

    # Mapeamento de bits por símbolo
    bits_per_symbol = {
        'BPSK': 1,
        'QPSK': 2,
        'QAM16': 4,
        'QAM64': 6,
    }

    series = {}
    plt.figure(figsize=(14, 8))

    for enc_id, mod_id in combinations:
        enc = utils.select_encoder(enc_id)
        mod = utils.select_modulator(mod_id)
        encoder_name = enc.__class__.__name__.replace("Encoder", "")
        modulator_name = mod.__class__.__name__.replace("Modulator", "")
        label = f"{encoder_name} + {modulator_name}"

        # Codificar linha e preparar bits de referência
        encoded_signal = enc.encode(data_bits)
        tx_mod_bits = utils.bits_for_modulation(encoded_signal, modulator_name)

        # Obter bits por símbolo
        bps = bits_per_symbol.get(modulator_name, 1)

        throughput_list = []
        for snr_db in snr_list_db:
            tx_symbols = mod.modulate(encoded_signal)
            rx_symbols = awgn.aplicar(tx_symbols, snr_db)
            rx_bits = mod.demodulate(rx_symbols)
            ber, errors, compared = utils.compute_ber(tx_mod_bits, rx_bits)

            # Throughput efetivo = bits_por_símbolo × (1 - BER) × taxa_símbolos
            # Convertido para Mbps (megabits por segundo)
            throughput_bps = bps * (1 - ber) * symbol_rate_hz
            throughput_mbps = throughput_bps / 1e6  # Converter para Mbps

            throughput_list.append(throughput_mbps)

        throughput_arr = np.array(throughput_list)
        series[label] = throughput_arr
        plt.plot(snr_list_db, throughput_arr, label=label, linewidth=2)

    plt.grid(True, alpha=0.3)
    plt.xlabel('SNR (dB)', fontsize=13, fontweight='bold')
    plt.ylabel('Throughput Efetivo (Mbps)', fontsize=13, fontweight='bold')

    title = f'Throughput Efetivo vs SNR\n(Taxa de símbolos: {symbol_rate_hz/1e6:.1f} MHz, Mensagem: {len(message)} caracteres)'
    plt.title(title, fontsize=14, fontweight='bold')

    plt.legend(loc='best', fontsize=9, ncol=2, framealpha=0.9)
    plt.xlim(snr_list_db[0], snr_list_db[-1])
    plt.ylim(0, max([max(v) for v in series.values()]) * 1.1)  # 10% margem superior
    plt.tight_layout()
    plt.show()

    return series


if __name__ == "__main__":
    # Configuração da simulação
    message = "A" * 10000  # Mensagem de 10000 caracteres

    print("\n" + "="*70)
    print("BENCHMARK THROUGHPUT EFETIVO vs SNR")
    print("="*70)
    print(f"\nMensagem: {len(message)} caracteres = {len(data.text_to_bits(message))} bits")
    print(f"Taxa de símbolos: 1 MHz (1.000.000 símbolos/segundo)")
    print(f"{'─'*70}\n")

    # Executar benchmark
    results = run_throughput_snr_benchmark(
        message=message,
        symbol_rate_hz=1e6  # 1 MHz
    )

    print("\n" + "="*70)
    print("BENCHMARK CONCLUÍDO!")
    print("="*70)
    
    # Mostrar throughput máximo de cada configuração
    print("\nThroughput Máximo Atingido:")
    print("─"*70)
    for label, throughputs in results.items():
        max_throughput = np.max(throughputs)
        max_snr_idx = np.argmax(throughputs)
        max_snr = np.arange(0.0, 30.0 + 1.0, 1.0)[max_snr_idx]
        print(f"{label:30s}: {max_throughput:6.2f} Mbps @ SNR = {max_snr:.0f} dB")
    print("─"*70 + "\n")