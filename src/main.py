import data as data
import encoder as encoder
import modulator as modulator
import utils as utils

def main():
    message = "o"
    print(f"\nMensagem ASCII: '{message}'")
    
    data_bits = data.text_to_bits(message)
    print(f"\nMensagem binária: {data.format_bits(data_bits)}")
    
    recovered_message = data.bits_to_text(data_bits)
    print(f"\nMensagem ASCII recuperada: '{recovered_message}'")


    # Seleciona e aplica o encoder. 1: Manchester, 2: AMI Bipolar
    selected_encoder = utils.select_encoder(1)
    encoded_signal = selected_encoder.encode(data_bits)
    encoder_name = selected_encoder.__class__.__name__.replace('Encoder', '')
    print(f"\nSinal {encoder_name} codificado: {encoded_signal}")
    encoder.plot_encoding(data_bits, encoded_signal, encoder_name)

    # Seleciona e aplica o modulador. 1: BPSK, 2: QPSK, 3: 16-QAM, 4: 64-QAM
    selected_modulator = utils.select_modulator(4)
    modulated_signal = selected_modulator.modulate(encoded_signal)
    modulator_name = selected_modulator.__class__.__name__.replace('Modulator', '')
    print(f"\nSinal modulado {modulator_name}: {modulated_signal}")
    modulator.plot_constellation(selected_modulator)


if __name__ == "__main__":
    main()