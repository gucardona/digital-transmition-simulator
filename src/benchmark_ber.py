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
    title_suffix: str = "",
):
    """Executa benchmark BER vs SNR para múltiplas combinações Encoder+Modulador.

    Parâmetros:
    - message: texto base para geração de bits.
    - snr_list_db: lista ou array de SNRs em dB (default 0..30 em passos de 1).
    - combinations: lista de tuplas (EncoderID, ModulatorID). Se None, usa um conjunto padrão.
    - title_suffix: sufixo adicional para o título do gráfico.

    Retorna: dict(label -> np.ndarray de BERs) e plota o gráfico.
    """
    if snr_list_db is None:
        # Pontos espaçados: 0 a 30 dB com passo de 1 dB (para gráficos mais limpos)
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

    series = {}
    plt.figure(figsize=(14, 8))

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
        # Linha contínua sem marcadores para leitura mais limpa
        plt.plot(snr_list_db, ber_arr, label=label, linewidth=2)

    plt.grid(True, alpha=0.3)
    plt.xlabel('SNR (dB)', fontsize=13, fontweight='bold')
    plt.ylabel('BER (Taxa de Erro de Bit)', fontsize=13, fontweight='bold')
    
    # Título com informações adicionais
    title = f'BER vs SNR - {title_suffix}\n({len(message)} caracteres = {len(data_bits)} bits)'
    plt.title(title, fontsize=14, fontweight='bold')
    
    plt.legend(loc='best', fontsize=9, ncol=2, framealpha=0.9)
    plt.yscale('log')  # Escala logarítmica para melhor visualização do BER
    plt.ylim(1e-5, 1)  # Limita o eixo Y entre 10⁻⁵ e 1
    plt.xlim(snr_list_db[0], snr_list_db[-1])
    plt.tight_layout()
    plt.show()

    return series


if __name__ == "__main__":
    # Configuração da simulação
    message = "A" * 10000  # Mensagem de 10000 caracteres
    
    print("\n" + "="*70)
    print("BENCHMARK BER vs SNR")
    print("="*70)
    print(f"\nMensagem: {len(message)} caracteres = {len(data.text_to_bits(message))} bits")
    print(f"{'─'*70}\n")
    
    # Configuração opcional de SNR e combinações
    # Você pode descomentar e modificar estas linhas para personalizar
    
    # SNR personalizado (exemplo: menos pontos para execução mais rápida)
    # custom_snr = np.arange(0.0, 25.0, 1.0)
    
    # Combinações personalizadas (exemplo: apenas algumas combinações)
    # custom_combinations = [
    #     (EncoderID.MANCHESTER, ModulatorID.BPSK),
    #     (EncoderID.MANCHESTER, ModulatorID.QPSK),
    #     (EncoderID.AMI_BIPOLAR, ModulatorID.BPSK),
    #     (EncoderID.AMI_BIPOLAR, ModulatorID.QPSK),
    # ]
    
    # Executar benchmark com configuração padrão
    results = run_ber_snr_benchmark(
        message=message,
        title_suffix="Análise de Desempenho"
    )
    
    # Ou com configuração personalizada:
    # results = run_ber_snr_benchmark(
    #     message=message,
    #     snr_list_db=custom_snr,
    #     combinations=custom_combinations,
    #     title_suffix="Análise de Desempenho"
    # )
    
    print("\n" + "="*70)
    print("BENCHMARK CONCLUÍDO!")
    print("="*70 + "\n")