import numpy as np

class AWGNNoise:
    """
    Classe de ruído AWGN (Gaussiano Branco Aditivo).
    Use o método `aplicar(signal, snr_db)` para adicionar ruído ao sinal.
    """

    def __init__(self, rng: np.random.Generator | None = None):
        self.rng = rng or np.random.default_rng()

    def aplicar(self, signal: np.ndarray, snr_db: float) -> np.ndarray:
        """
        Aplica AWGN ao `signal` com SNR em dB.

        Entradas:
        - signal: array NumPy de símbolos (real para BPSK, complexo para QPSK/QAM)
        - snr_db: relação sinal-ruído desejada em dB (referente à potência média do sinal)

        Saída:
    - Sinal com ruído adicionado (mesmo dtype/shape do original)

        Observações:
    - Constelações QAM já normalizadas continuam assim; não há renormalização pós-ruído.
        """
        # Potência média do sinal
        if np.iscomplexobj(signal):
            signal_power = np.mean(np.abs(signal) ** 2)
        else:
            signal_power = np.mean(signal ** 2)

        # Converte SNR de dB para linear e deriva a potência do ruído
        snr_linear = 10 ** (snr_db / 10.0)
        noise_power = signal_power / snr_linear

        # Gera ruído compatível com o tipo do sinal
        if np.iscomplexobj(signal):
            # Baseband complexo: ruído = n_I + j n_Q, cada um com variância = noise_power/2
            sigma = np.sqrt(noise_power / 2.0)
            noise = self.rng.normal(0.0, sigma, size=signal.shape) + 1j * self.rng.normal(0.0, sigma, size=signal.shape)
        else:
            sigma = np.sqrt(noise_power)
            noise = self.rng.normal(0.0, sigma, size=signal.shape)

        return signal + noise

    def plot_constelacao_ruido(self, modulador, sinal_ruidoso: np.ndarray, snr_db: float) -> None:
        """
        Plota a constelação ideal e sobrepõe os pontos ruidosos.

        - modulador: instância do modulador (deve possuir `constellation` mapeando bits->símbolo)
        - sinal_ruidoso: array de símbolos com ruído (real/complexo)
        - snr_db: SNR usado na geração do ruído (exibido no título)
        """
        import matplotlib.pyplot as plt
        import numpy as np

        plt.figure(figsize=(8, 8))
        # Pontos ideais
        for _, symbol in modulador.constellation.items():
            plt.plot(symbol.real, symbol.imag, 'ro', markersize=10, label='_nolegend_')

        # Pontos ruidosos
        plt.scatter(np.real(sinal_ruidoso), np.imag(sinal_ruidoso), s=20, c='blue', alpha=0.6, label='Ruidoso')

        plt.grid(True, alpha=0.3)
        plt.axhline(0, color='black', linewidth=0.5)
        plt.axvline(0, color='black', linewidth=0.5)
        plt.xlabel('In-Phase (I)', fontsize=12)
        plt.ylabel('Quadrature (Q)', fontsize=12)

        nome_modulador = modulador.__class__.__name__.replace('Modulator', '')
        plt.title(f'Constelação {nome_modulador} com AWGN (SNR={snr_db} dB)', fontsize=14, fontweight='bold')
        plt.legend()
        plt.axis('equal')
        plt.show()
