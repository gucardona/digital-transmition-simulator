import numpy as np

def generate_mock_signal(message: str = "Hi"):
    """
    MOCK - Simula o que voce vai entregar depois
    
    Sua dupla recebe:
    - signal_modulated: simbolos modulados
    - bits_original: bits originais (para calcular BER depois)
    """
    
    # Simula conversão ASCII -> bits
    bits_original = []
    for char in message:
        byte = format(ord(char), '08b')
        bits_original.extend([int(b) for b in byte])
    bits_original = np.array(bits_original)
    
    # Simula codificação Manchester (cada bit vira 2 símbolos)
    signal_encoded = []
    for bit in bits_original:
        if bit == 0:
            signal_encoded.extend([-1, 1])
        else:
            signal_encoded.extend([1, -1])
    signal_encoded = np.array(signal_encoded)
    
    # Simula modulação BPSK (inverte sinal)
    signal_modulated = -signal_encoded
    
    return signal_modulated, bits_original


def main():
    message = "Hi"
    snr_db = 10
    
    # MOCK - Simula saida das etapas 1-3
    signal_modulated, bits_original = generate_mock_signal(message)
    
    print(f"Mensagem: '{message}'")
    print(f"Bits originais: {bits_original}")
    print(f"Signal modulado: shape={signal_modulated.shape}, dtype={signal_modulated.dtype}")
    print(f"   Primeiros 10 valores: {signal_modulated[:10]}")
    print(f"SNR: {snr_db} dB")
    print()


if __name__ == "__main__":
    main()