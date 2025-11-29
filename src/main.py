import data as data
import encoder as encoder
import modulator as modulator

import matplotlib.pyplot as plt

def main():
    message = "o"
    print(f"\nMensagem ASCII: '{message}'")
    
    data_bits = data.text_to_bits(message)
    print(f"\nMensagem binária: {data.format_bits(data_bits)}")
    
    recovered_message = data.bits_to_text(data_bits)
    print(f"\nMensagem ASCII recuperada: '{recovered_message}'")

    manchester_encoder = encoder.ManchesterEncoder()
    encoded_signal = manchester_encoder.encode(data_bits)
    print(f"\nSinal Manchester codificado: {encoded_signal}")
    # plot_manchester_detailed(data_bits, encoded_signal)

    qpsk_modulator = modulator.QPSKModulator()
    modulated_signal = qpsk_modulator.modulate(encoded_signal)
    print(f"\nSinal modulado QPSK: {modulated_signal}")
    # modulator.plot_constellation(qpsk_modulator)

    qam64_modulator = modulator.QAM64Modulator()
    modulated_signal = qam64_modulator.modulate(encoded_signal)
    print(f"\nSinal modulado 64-QAM: {modulated_signal}")
    # modulator.plot_constellation(qam64_modulator)


if __name__ == "__main__":
    main()