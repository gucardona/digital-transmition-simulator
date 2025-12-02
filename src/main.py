import data as data
import encoder as encoder
import modulator as modulator
import utils as utils
import noise as noise
import matplotlib.pyplot as plt
import numpy as np
from utils import EncoderID, ModulatorID, NoiseID

def main():
    message = "test message! long message!"
    print(f"\nMensagem ASCII: '{message}'")
    
    data_bits = data.text_to_bits(message)
    print(f"\nMensagem binária: {data.format_bits(data_bits)}")
    
    recovered_message = data.bits_to_text(data_bits)
    print(f"\nMensagem ASCII recuperada: '{recovered_message}'")

    encoder_id = EncoderID.MANCHESTER
    selected_encoder = utils.select_encoder(encoder_id)
    encoded_signal = selected_encoder.encode(data_bits)
    encoder_name = selected_encoder.__class__.__name__.replace('Encoder', '')
    print(f"\nSinal {encoder_name} codificado: {encoded_signal}")
    encoder.plot_encoding(data_bits, encoded_signal, encoder_name)

    modulator_id = ModulatorID.QPSK
    selected_modulator = utils.select_modulator(modulator_id)
    modulated_signal = selected_modulator.modulate(encoded_signal)
    modulator_name = selected_modulator.__class__.__name__.replace('Modulator', '')
    print(f"\nSinal modulado {modulator_name}: {modulated_signal}")
    modulator.plot_constellation(selected_modulator)

    noise_id = NoiseID.AWGN
    selected_noise = utils.select_noise(noise_id)
    snr_db = 20  # Ajuste do SNR em dB conforme desejado
    noisy_signal = selected_noise.aplicar(modulated_signal, snr_db)
    print(f"\nSinal modulado {modulator_name} com AWGN (SNR={snr_db} dB): {noisy_signal}")
    selected_noise.plot_constelacao_ruido(selected_modulator, noisy_signal, snr_db)

    demod_bits = selected_modulator.demodulate(noisy_signal)
    print(f"\nBits demodulados: {demod_bits}")
    modulator.plot_demodulated_bits(demod_bits, modulator_name)

    tx_mod_bits = utils.bits_for_modulation(encoded_signal, modulator_name)
    ber, errors, compared = utils.compute_ber(tx_mod_bits, demod_bits)
    print(f"\nBER pós-modulação: {ber:.6f} (erros={errors} em {compared} bits)")

    line_levels = utils.reconstruct_line_levels(demod_bits, encoder_name, original_length=len(data_bits))
    rx_bits = selected_encoder.decode(line_levels)
    print(f"\nBits decodificados: {rx_bits}")
    encoder.plot_decoded_bits(rx_bits, encoder_name)

    final_len = (len(rx_bits) // 8) * 8
    recovered_text = data.bits_to_text(rx_bits[:final_len])
    print(f"\nMensagem final recuperada: '{recovered_text}'")


if __name__ == "__main__":
    main()