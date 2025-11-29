import numpy as np

def text_to_bits(message: str) -> np.ndarray:
    """
    Converte uma string de texto em um array de bits.
    Cada caractere é representado por 8 bits (ASCII).
    """
    bits = []
    for char in message:
        byte = format(ord(char), '08b')
        bits.extend([int(b) for b in byte])
    return np.array(bits)


def bits_to_text(bits: np.ndarray) -> str:
    """
    Converte um array de bits de volta para uma string de texto.
    Assume que o número de bits é múltiplo de 8.
    """
    chars = []
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        char = chr(int(''.join(str(b) for b in byte), 2))
        chars.append(char)
    return ''.join(chars)


def format_bits(bits: np.ndarray) -> str:
    """
    Formata um array de bits em uma string para exibição.
    Agrupa de 8 em 8 bits (1 byte por caractere).
    """
    formatted = []
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        byte_str = ''.join(str(b) for b in byte)
        formatted.append(byte_str)
    return ' '.join(formatted)