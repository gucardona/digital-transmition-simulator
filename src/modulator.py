import numpy as np
import matplotlib.pyplot as plt

class BPSKModulator:
    """BPSK: 1 bit por símbolo"""
    
    def __init__(self):
        self.constellation = {
            (0,): 1.0,   # Fase 0°
            (1,): -1.0   # Fase 180°
        }
    
    def modulate(self, signal: np.ndarray) -> np.ndarray:
        """Modula usando BPSK"""
        # Converte -1,+1 para 0,1
        bits = ((signal + 1) / 2).astype(int)
        
        modulated = np.zeros(len(bits))
        for i, bit in enumerate(bits):
            modulated[i] = self.constellation[(bit,)]
        
        return modulated

    def demodulate(self, received: np.ndarray) -> np.ndarray:
        """
        Demodula BPSK por decisão no eixo real.
        Símbolo >= 0 → bit 0; símbolo < 0 → bit 1.
        """
        bits = (received < 0).astype(int)
        return bits

class QPSKModulator:
    """
    QPSK: 2 bits por símbolo
    Usado em GPS, satélites, WiFi básico
    """
    
    def __init__(self):
        # Mapeamento Gray coding (minimiza erros)
        # Símbolos nas diagonais (45°, 135°, 225°, 315°)
        self.constellation = {
            (0, 0): complex(1, 1) / np.sqrt(2),    # 45°
            (0, 1): complex(-1, 1) / np.sqrt(2),   # 135°
            (1, 1): complex(-1, -1) / np.sqrt(2),  # 225°
            (1, 0): complex(1, -1) / np.sqrt(2)    # 315°
        }
        
        # Inverso para demodulação
        self.inverse_constellation = {v: k for k, v in self.constellation.items()}
    
    def modulate(self, signal: np.ndarray) -> np.ndarray:
        """
        Modula usando QPSK
        
        Passo 1: Agrupar de 2 em 2 símbolos
        Passo 2: Mapear cada par para fase QPSK
        """
        # Padding para múltiplo de 2
        pad_length = len(signal) % 2
        if pad_length:
            signal = np.append(signal, [0])
        
        # Converte -1,+1 para 0,1
        bits = ((signal + 1) / 2).astype(int)
        
        # Agrupa de 2 em 2
        num_symbols = len(bits) // 2
        modulated = np.zeros(num_symbols, dtype=complex)
        
        for i in range(num_symbols):
            bit_pair = tuple(bits[i*2:(i+1)*2])
            modulated[i] = self.constellation[bit_pair]
        
        return modulated

    def demodulate(self, received: np.ndarray) -> np.ndarray:
        """
        Demodula QPSK por distância mínima aos pontos da constelação.
        Retorna bits agrupados sequencialmente.
        """
        # Decisão por nearest-neighbor
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
        # Constelação 16-QAM (4x4 = 16 pontos)
        self.constellation = {}
        
        # Amplitudes: -3, -1, +1, +3
        positions = [-3, -1, 1, 3]
        
        index = 0
        for i in positions:
            for q in positions:
                # Converte índice (0-15) para 4 bits
                bits = tuple([int(x) for x in format(index, '04b')])
                self.constellation[bits] = complex(i, q)
                index += 1
    
    def modulate(self, signal: np.ndarray) -> np.ndarray:
        """Modula usando 16-QAM"""
        # Padding para múltiplo de 4
        pad_length = (4 - len(signal) % 4) % 4
        if pad_length > 0:
            signal = np.append(signal, np.zeros(pad_length))
        
        # Converte -1,+1 para 0,1
        bits = ((signal + 1) / 2).astype(int)
        
        # Agrupa de 4 em 4
        num_symbols = len(bits) // 4
        modulated = np.zeros(num_symbols, dtype=complex)
        
        for i in range(num_symbols):
            bit_group = tuple(bits[i*4:(i+1)*4])
            modulated[i] = self.constellation[bit_group]
        
        # Normalização
        return modulated / np.sqrt(10)

    def demodulate(self, received: np.ndarray) -> np.ndarray:
        """
        Demodula 16-QAM por distância mínima (com normalização correspondente).
        """
        # Reverte normalização
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
    """
    64-QAM: 6 bits por símbolo
    Usado em LTE, WiFi 5/6
    """
    
    def __init__(self):
        # Constelação 64-QAM (8x8)
        self.constellation = {}
        positions = [-7, -5, -3, -1, 1, 3, 5, 7]
        
        index = 0
        for i in positions:
            for q in positions:
                bits = tuple([int(x) for x in format(index, '06b')])
                self.constellation[bits] = complex(i, q)
                index += 1
    
    def modulate(self, signal: np.ndarray) -> np.ndarray:
        """Similar ao 16-QAM, mas agrupa de 6 em 6 bits"""
        pad_length = (6 - len(signal) % 6) % 6
        if pad_length > 0:
            signal = np.append(signal, np.zeros(pad_length))
        
        bits = ((signal + 1) / 2).astype(int)
        num_symbols = len(bits) // 6
        modulated = np.zeros(num_symbols, dtype=complex)
        
        for i in range(num_symbols):
            bit_group = tuple(bits[i*6:(i+1)*6])
            modulated[i] = self.constellation[bit_group]
        
        return modulated / np.sqrt(42)  # Normalização

    def demodulate(self, received: np.ndarray) -> np.ndarray:
        """
        Demodula 64-QAM por distância mínima (com normalização correspondente).
        """
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
    """Plota constelação de qualquer modulador"""
    plt.figure(figsize=(8, 8))
    
    for bits, symbol in modulator.constellation.items():
        plt.plot(symbol.real, symbol.imag, 'ro', markersize=15)
        bit_str = ''.join(map(str, bits))
        plt.text(symbol.real + 0.1, symbol.imag + 0.1, bit_str, 
                fontsize=12, fontweight='bold')
    
    plt.grid(True, alpha=0.3)
    plt.axhline(0, color='black', linewidth=0.5)
    plt.axvline(0, color='black', linewidth=0.5)
    plt.xlabel('In-Phase (I)', fontsize=12)
    plt.ylabel('Quadrature (Q)', fontsize=12)
    
    # Título dinâmico baseado no nome da classe
    modulator_name = modulator.__class__.__name__.replace('Modulator', '')
    plt.title(f'Constelação {modulator_name}', fontsize=14, fontweight='bold')
    
    plt.axis('equal')
    plt.show()

def plot_demodulated_bits(demod_bits: np.ndarray, modulator_name: str):
    """Plota sequência de bits demodulados (0/1).
    Usa gráfico em degraus para visualizar decisões de bit após a demodulação.
    """
    plt.figure(figsize=(12, 2.5))
    plt.step(range(len(demod_bits)), demod_bits, where='post', linewidth=2)
    plt.ylim(-0.2, 1.2)
    plt.title(f"Bits demodulados ({modulator_name})", fontsize=13, fontweight='bold')
    plt.xlabel("Índice")
    plt.ylabel("Bit")
    plt.grid(True, alpha=0.3)
    # Anotação leve por bit (opcional se curto)
    if len(demod_bits) <= 64:  # evita poluição visual para sequências grandes
        for i, b in enumerate(demod_bits):
            plt.text(i + 0.1, b + 0.15, str(b), fontsize=9, ha='center')
    plt.tight_layout()
    plt.show()