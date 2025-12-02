import numpy as np
import matplotlib.pyplot as plt

class ManchesterEncoder:
    """
    Classe para codificação Manchester de dados binários.
    """

    def __init__(self):
        pass

    def encode(self, bits: np.ndarray) -> np.ndarray:
        """
        Codifica um array de bits usando codificação Manchester.
        Cada bit é representado por dois níveis: 0 -> [1, 0], 1 -> [0, 1].

        """

        # Cria array vazio com tamanho dobrado
        encoded = np.zeros(len(bits) * 2)

        # Processa cada bit
        for i, bit in enumerate(bits):
            # Posição onde vamos colocar os 2 símbolos
            pos = i * 2

            if bit == 0:
                # Bit 0: LOW-HIGH (sobe)
                encoded[pos] = -1      # primeiro símbolo
                encoded[pos + 1] = 1   # segundo símbolo
            else:
                # Bit 1: HIGH-LOW (desce)
                encoded[pos] = 1       # primeiro símbolo
                encoded[pos + 1] = -1  # segundo símbolo

        return encoded
    
    def decode(self, encoded_signal: np.ndarray) -> np.ndarray:
        """
        Decodifica um sinal Manchester em bits originais.
        Regra (com limiar 0):
        - Bit 0: primeira metade < segunda metade (LOW→HIGH)
        - Bit 1: primeira metade > segunda metade (HIGH→LOW)
        """
        # Garantir que o comprimento seja par (2 amostras por bit)
        n = len(encoded_signal) // 2
        bits = np.zeros(n, dtype=int)
        for i in range(n):
            a = encoded_signal[2*i]
            b = encoded_signal[2*i + 1]
            # Limiares simples em 0 para robustez
            # Decisão baseada na relação entre a e b
            bits[i] = 0 if a < b else 1
        return bits
    
class AMIBipolarEncoder:
    """Codificação AMI Bipolar"""
    
    def __init__(self):
        self.last_one_level = -1  # Começa em -1, primeiro será +1
    
    def encode(self, bits: np.ndarray) -> np.ndarray:
        """
        Codifica usando AMI Bipolar
        
        Bit 0 → 0
        Bit 1 → alterna entre +1 e -1
        """
        encoded = np.zeros(len(bits))
        self.last_one_level = -1  # Reset
        
        for i, bit in enumerate(bits):
            if bit == 0:
                # Bit 0: sempre zero
                encoded[i] = 0
            else:
                # Bit 1: alterna polaridade
                self.last_one_level *= -1  # -1 vira +1, +1 vira -1
                encoded[i] = self.last_one_level
        
        return encoded
    
    def decode(self, encoded_signal: np.ndarray) -> np.ndarray:
        """
        Decodifica AMI Bipolar:
        - Valores próximos de 0 → bit 0
        - Valores positivos/negativos → bit 1 (polaridade ignorada)
        """
        bits = np.zeros(len(encoded_signal), dtype=int)
        for i, v in enumerate(encoded_signal):
            bits[i] = 0 if abs(v) < 0.5 else 1
        return bits
    

def plot_encoding(bits, encoded_signal, encoder_name):
    """
    Plota codificação de qualquer encoder de forma didática
    Detecta automaticamente o tipo de encoder
    """
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 8))
    ax1.set_title("Bits Originais", fontsize=14, fontweight='bold')
    
    # Determina escala de tempo baseado no encoder
    if encoder_name == "Manchester":
        time_scale = 2  # Manchester: cada bit ocupa 2 unidades
    else:
        time_scale = 1  # NRZ/AMI: cada bit ocupa 1 unidade
    
    time_bits = []
    signal_bits = []
    
    for i, bit in enumerate(bits):
        time_bits.extend([i*time_scale, (i+1)*time_scale])
        signal_bits.extend([bit, bit])
    
    ax1.plot(time_bits, signal_bits, 'b-', linewidth=2, drawstyle='steps-post')
    ax1.set_ylim(-0.5, 1.5)
    ax1.set_ylabel("Bit", fontsize=12)
    ax1.grid(True, alpha=0.3)
    ax1.set_yticks([0, 1])
    
    # Adiciona texto mostrando cada bit
    for i, bit in enumerate(bits):
        ax1.text(i*time_scale + time_scale/2, bit + 0.2, str(bit), 
                ha='center', va='bottom', fontsize=12, fontweight='bold')
    
    # Marca as divisões de bits
    for i in range(len(bits) + 1):
        ax1.axvline(i*time_scale, color='red', linestyle='--', alpha=0.3)
    
    ax1.set_xlim(0, len(bits)*time_scale)
    ax2.set_title(f"Sinal {encoder_name} Codificado", fontsize=14, fontweight='bold')
    
    # Criar forma de onda baseado no tipo de encoder
    if encoder_name == "Manchester":
        # Manchester: 2 samples por bit
        time_encoded = []
        signal_encoded = []
        
        for i in range(0, len(encoded_signal), 2):
            # Primeiro símbolo (primeira metade do bit)
            time_encoded.extend([i, i+1])
            signal_encoded.extend([encoded_signal[i], encoded_signal[i]])
            
            # Segundo símbolo (segunda metade do bit)
            time_encoded.extend([i+1, i+2])
            signal_encoded.extend([encoded_signal[i+1], encoded_signal[i+1]])
    
    else:
        # NRZ/AMI: 1 sample por bit
        time_encoded = []
        signal_encoded = []
        
        for i, value in enumerate(encoded_signal):
            time_encoded.extend([i, i+1])
            signal_encoded.extend([value, value])
    
    ax2.plot(time_encoded, signal_encoded, 'g-', linewidth=2.5, drawstyle='steps-post')
    ax2.set_ylim(-1.5, 1.5)
    ax2.set_ylabel("Nível de Sinal", fontsize=12)
    ax2.set_xlabel("Tempo", fontsize=12)
    ax2.grid(True, alpha=0.3)
    ax2.set_yticks([-1, 0, 1])
    ax2.axhline(0, color='black', linestyle='-', linewidth=0.5)
    
    # Marca as divisões de bits
    for i in range(len(bits) + 1):
        ax2.axvline(i*time_scale, color='red', linestyle='--', alpha=0.3)
    
    # Adiciona anotações específicas por encoder
    if encoder_name == "Manchester":
        # Anotações de transição Manchester
        for i in range(len(bits)):
            bit_value = bits[i]
            transition = "LOW→HIGH" if bit_value == 0 else "HIGH→LOW"
            ax2.text(i*time_scale + time_scale/2, 1.2, transition, 
                    ha='center', fontsize=9, 
                    bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7))
            
            ax2.text(i*time_scale + time_scale/2, -1.3, f"Bit {bit_value}", 
                    ha='center', fontsize=11, fontweight='bold',
                    bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.7))
    
    elif encoder_name == "AMIBipolar":
        # Anotações AMI
        for i, (bit, value) in enumerate(zip(bits, encoded_signal)):
            if value == 0:
                label = "0 (zero)"
                color = 'gray'
            elif value > 0:
                label = "+1"
                color = 'lightgreen'
            else:
                label = "-1"
                color = 'lightcoral'
            
            ax2.text(i + 0.5, 1.2, f"Bit {bit}", 
                    ha='center', fontsize=9, fontweight='bold',
                    bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.7))
            
            ax2.text(i + 0.5, -1.3, label, 
                    ha='center', fontsize=9,
                    bbox=dict(boxstyle='round', facecolor=color, alpha=0.7))
    
    elif encoder_name == "NRZ":
        # Anotações NRZ
        for i, (bit, value) in enumerate(zip(bits, encoded_signal)):
            label = "+1" if value > 0 else "-1"
            color = 'lightgreen' if value > 0 else 'lightcoral'
            
            ax2.text(i + 0.5, 1.2, f"Bit {bit}", 
                    ha='center', fontsize=9, fontweight='bold',
                    bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.7))
            
            ax2.text(i + 0.5, -1.3, label, 
                    ha='center', fontsize=9,
                    bbox=dict(boxstyle='round', facecolor=color, alpha=0.7))
    
    ax2.set_xlim(0, len(bits)*time_scale)
    
    plt.tight_layout()
    plt.show()


def plot_decoded_bits(bits: np.ndarray, encoder_name: str):
    import matplotlib.pyplot as plt
    plt.figure(figsize=(12, 2.5))
    plt.step(range(len(bits)), bits, where='post', linewidth=2)
    plt.ylim(-0.2, 1.2)
    plt.title(f"Bits decodificados ({encoder_name})", fontsize=13, fontweight='bold')
    plt.xlabel("Índice")
    plt.ylabel("Bit")
    plt.grid(True, alpha=0.3)
    if len(bits) <= 64:
        for i, b in enumerate(bits):
            plt.text(i + 0.1, b + 0.15, str(b), fontsize=9, ha='center')
    plt.tight_layout()
    plt.show()
