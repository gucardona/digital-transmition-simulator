import data as data
import encoder as encoder
import modulator as modulator

def main():
    message = "o"
    print(f"\nMensagem ASCII: '{message}'")
    
    data_bits = data.text_to_bits(message)
    print(f"\nMensagem binária: {data.format_bits(data_bits)}")
    
    recovered_message = data.bits_to_text(data_bits)
    print(f"\nMensagem ASCII recuperada: '{recovered_message}'")


    # Encoders
    ami_encoder = encoder.AMIBipolarEncoder()
    encoded_signal = ami_encoder.encode(data_bits)
    print(f"\nSinal AMI Bipolar codificado: {encoded_signal}")
    # encoder.plot_encoding(data_bits, encoded_signal, 'AMI Bipolar')

    manchester_encoder = encoder.ManchesterEncoder()
    encoded_signal = manchester_encoder.encode(data_bits)
    print(f"\nSinal Manchester codificado: {encoded_signal}")
    # encoder.plot_encoding(data_bits, manchester_encoder, 'Manchester')

    # Modulators
    bpsk_modulator = modulator.BPSKModulator()
    modulated_signal = bpsk_modulator.modulate(encoded_signal)
    print(f"\nSinal modulado BPSK: {modulated_signal}")
    # modulator.plot_constellation(bpsk_modulator)

    qpsk_modulator = modulator.QPSKModulator()
    modulated_signal = qpsk_modulator.modulate(encoded_signal)
    print(f"\nSinal modulado QPSK: {modulated_signal}")
    # modulator.plot_constellation(qpsk_modulator)

    qam16_modulator = modulator.QAM16Modulator()
    modulated_signal = qam16_modulator.modulate(encoded_signal)
    print(f"\nSinal modulado 16-QAM: {modulated_signal}")
    # modulator.plot_constellation(qam16_modulator)   

    qam64_modulator = modulator.QAM64Modulator()
    modulated_signal = qam64_modulator.modulate(encoded_signal)
    print(f"\nSinal modulado 64-QAM: {modulated_signal}")
    # modulator.plot_constellation(qam64_modulator)


if __name__ == "__main__":
    main()