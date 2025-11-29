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
    
    def plot(bits, encoded_signal):
        """
        Plota codificação Manchester de forma super didática
        Mostra claramente as transições no meio de cada bit
        """
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 8))
        ax1.set_title("Bits Originais", fontsize=14, fontweight='bold')
        
        # Criar forma de onda quadrada para os bits
        time_bits = []
        signal_bits = []
        
        for i, bit in enumerate(bits):
            # Cada bit ocupa 2 unidades de tempo
            time_bits.extend([i*2, i*2+2])
            signal_bits.extend([bit, bit])
        
        ax1.plot(time_bits, signal_bits, 'b-', linewidth=2, drawstyle='steps-post')
        ax1.set_ylim(-0.5, 1.5)
        ax1.set_ylabel("Bit", fontsize=12)
        ax1.grid(True, alpha=0.3)
        ax1.set_yticks([0, 1])
        
        # Adiciona texto mostrando cada bit
        for i, bit in enumerate(bits):
            ax1.text(i*2 + 1, bit + 0.2, str(bit), 
                    ha='center', va='bottom', fontsize=12, fontweight='bold')
        
        # Marca as divisões de bits
        for i in range(len(bits) + 1):
            ax1.axvline(i*2, color='red', linestyle='--', alpha=0.3)
        
        ax1.set_xlim(0, len(bits)*2)
        ax2.set_title("Sinal Manchester Codificado", fontsize=14, fontweight='bold')
        
        # Criar forma de onda do sinal Manchester
        time_manchester = []
        signal_manchester = []
        
        for i in range(0, len(encoded_signal), 2):
            # Cada bit Manchester tem 2 símbolos
            # Primeiro símbolo (primeira metade do bit)
            time_manchester.extend([i, i+1])
            signal_manchester.extend([encoded_signal[i], encoded_signal[i]])
            
            # Segundo símbolo (segunda metade do bit)
            time_manchester.extend([i+1, i+2])
            signal_manchester.extend([encoded_signal[i+1], encoded_signal[i+1]])
        
        ax2.plot(time_manchester, signal_manchester, 'g-', linewidth=2.5, drawstyle='steps-post')
        ax2.set_ylim(-1.5, 1.5)
        ax2.set_ylabel("Nível de Sinal", fontsize=12)
        ax2.set_xlabel("Tempo", fontsize=12)
        ax2.grid(True, alpha=0.3)
        ax2.set_yticks([-1, 0, 1])
        ax2.axhline(0, color='black', linestyle='-', linewidth=0.5)
        
        # Marca as divisões de bits
        for i in range(len(bits) + 1):
            ax2.axvline(i*2, color='red', linestyle='--', alpha=0.3)
        
        # Adiciona anotações da transição
        for i in range(len(bits)):
            bit_value = bits[i]
            transition = "LOW→HIGH" if bit_value == 0 else "HIGH→LOW"
            ax2.text(i*2 + 1, 1.2, transition, 
                    ha='center', fontsize=9, 
                    bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7))
        
        # Adiciona anotações mostrando qual bit está sendo representado
        for i, bit in enumerate(bits):
            ax2.text(i*2 + 1, -1.3, f"Bit {bit}", 
                    ha='center', fontsize=11, fontweight='bold',
                    bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.7))
        
        ax2.set_xlim(0, len(bits)*2)
        
        plt.tight_layout()
        plt.show()


