import numpy as np
import matplotlib.pyplot as plt

def _smart_signal_to_bits(signal: np.ndarray) -> np.ndarray:
    """
    Converte níveis de sinal para bits (0/1) inteligentemente.
    - Se houver zeros no sinal, assume codificação ternária (AMI):
      Níveis -1 e +1 viram bit 1. Nível 0 vira bit 0.
    - Se não houver zeros, assume codificação polar (NRZ/Manchester):
      Nível -1 vira bit 0. Nível +1 vira bit 1.
    """
    if np.any(signal == 0):
        # Lógica AMI: Magnitude indica bit 1
        return np.abs(signal).astype(int)
    else:
        # Lógica Manchester/BPSK: Nível positivo é 1, negativo é 0
        return ((signal + 1) / 2).astype(int)

class BPSKModulator:
    """BPSK: 1 bit por símbolo"""
    
    def __init__(self):
        self.constellation = {
            (0,): 1.0,   # Fase 0°
            (1,): -1.0   # Fase 180°
        }
    
    def modulate(self, signal: np.ndarray) -> np.ndarray:
        """Modula usando BPSK"""
        bits = _smart_signal_to_bits(signal)
        
        modulated = np.zeros(len(bits))
        for i, bit in enumerate(bits):
            modulated[i] = self.constellation[(bit,)]
        
        return modulated

    def demodulate(self, received: np.ndarray) -> np.ndarray:
        bits = (received < 0).astype(int)
        return bits

class QPSKModulator:
    """QPSK: 2 bits por símbolo"""
    
    def __init__(self):
        self.constellation = {
            (0, 0): complex(1, 1) / np.sqrt(2),
            (0, 1): complex(-1, 1) / np.sqrt(2),
            (1, 1): complex(-1, -1) / np.sqrt(2),
            (1, 0): complex(1, -1) / np.sqrt(2)
        }
        self.inverse_constellation = {v: k for k, v in self.constellation.items()}
    
    def modulate(self, signal: np.ndarray) -> np.ndarray:
        """Modula usando QPSK"""
        pad_length = len(signal) % 2
        if pad_length:
            signal = np.append(signal, [0]) # Padding com 0 mantém lógica do AMI se necessário
        
        bits = _smart_signal_to_bits(signal)
        
        num_symbols = len(bits) // 2
        modulated = np.zeros(num_symbols, dtype=complex)
        
        for i in range(num_symbols):
            bit_pair = tuple(bits[i*2:(i+1)*2])
            modulated[i] = self.constellation[bit_pair]
        
        return modulated

    def demodulate(self, received: np.ndarray) -> np.ndarray:
        points = np.array(list(self.constellation.values()))
        bit_pairs = list(self.constellation.keys())
        bits_out = []
        for r in received:
            d2 = np.abs(r - points) ** 2
            idx = np.argmin(d2)
            bits_out.extend(bit_pairs[idx])
        return np.array(bits_out, dtype=int)

class QAM16Modulator:
    """16-QAM: 4 bits por símbolo"""
    
    def __init__(self):
        self.constellation = {}
        positions = [-3, -1, 1, 3]
        index = 0
        for i in positions:
            for q in positions:
                bits = tuple([int(x) for x in format(index, '04b')])
                self.constellation[bits] = complex(i, q)
                index += 1
    
    def modulate(self, signal: np.ndarray) -> np.ndarray:
        """Modula usando 16-QAM"""
        pad_length = (4 - len(signal) % 4) % 4
        if pad_length > 0:
            signal = np.append(signal, np.zeros(pad_length))
        
        bits = _smart_signal_to_bits(signal)
        
        num_symbols = len(bits) // 4
        modulated = np.zeros(num_symbols, dtype=complex)
        
        for i in range(num_symbols):
            bit_group = tuple(bits[i*4:(i+1)*4])
            modulated[i] = self.constellation[bit_group]
        
        return modulated / np.sqrt(10)

    def demodulate(self, received: np.ndarray) -> np.ndarray:
        r = received * np.sqrt(10)
        points = np.array(list(self.constellation.values()))
        bit_quads = list(self.constellation.keys())
        bits_out = []
        for s in r:
            d2 = np.abs(s - points) ** 2
            idx = np.argmin(d2)
            bits_out.extend(bit_quads[idx])
        return np.array(bits_out, dtype=int)

class QAM64Modulator:
    """64-QAM: 6 bits por símbolo"""
    
    def __init__(self):
        self.constellation = {}
        positions = [-7, -5, -3, -1, 1, 3, 5, 7]
        index = 0
        for i in positions:
            for q in positions:
                bits = tuple([int(x) for x in format(index, '06b')])
                self.constellation[bits] = complex(i, q)
                index += 1
    
    def modulate(self, signal: np.ndarray) -> np.ndarray:
        """Modula usando 64-QAM"""
        pad_length = (6 - len(signal) % 6) % 6
        if pad_length > 0:
            signal = np.append(signal, np.zeros(pad_length))
        
        bits = _smart_signal_to_bits(signal)
        
        num_symbols = len(bits) // 6
        modulated = np.zeros(num_symbols, dtype=complex)
        
        for i in range(num_symbols):
            bit_group = tuple(bits[i*6:(i+1)*6])
            modulated[i] = self.constellation[bit_group]
        
        return modulated / np.sqrt(42)

    def demodulate(self, received: np.ndarray) -> np.ndarray:
        r = received * np.sqrt(42)
        points = np.array(list(self.constellation.values()))
        bit_groups = list(self.constellation.keys())
        bits_out = []
        for s in r:
            d2 = np.abs(s - points) ** 2
            idx = np.argmin(d2)
            bits_out.extend(bit_groups[idx])
        return np.array(bits_out, dtype=int)
    
def plot_constellation(modulator):
    plt.figure(figsize=(8, 8))
    for bits, symbol in modulator.constellation.items():
        plt.plot(symbol.real, symbol.imag, 'ro', markersize=15)
        bit_str = ''.join(map(str, bits))
        plt.text(symbol.real + 0.1, symbol.imag + 0.1, bit_str, fontsize=12, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.axhline(0, color='black', linewidth=0.5)
    plt.axvline(0, color='black', linewidth=0.5)
    plt.xlabel('In-Phase (I)', fontsize=12)
    plt.ylabel('Quadrature (Q)', fontsize=12)
    modulator_name = modulator.__class__.__name__.replace('Modulator', '')
    plt.title(f'Constelação {modulator_name}', fontsize=14, fontweight='bold')
    plt.axis('equal')
    plt.show()

def plot_demodulated_bits(demod_bits: np.ndarray, modulator_name: str):
    plt.figure(figsize=(12, 2.5))
    plt.step(range(len(demod_bits)), demod_bits, where='post', linewidth=2)
    plt.ylim(-0.2, 1.2)
    plt.title(f"Bits demodulados ({modulator_name})", fontsize=13, fontweight='bold')
    plt.xlabel("Índice")
    plt.ylabel("Bit")
    plt.grid(True, alpha=0.3)
    if len(demod_bits) <= 64:
        for i, b in enumerate(demod_bits):
            plt.text(i + 0.1, b + 0.15, str(b), fontsize=9, ha='center')
    plt.tight_layout()
    plt.show()