import numpy as np
import matplotlib.pyplot as plt

MC = int(2e5)
K = 3
SNR_dB = np.arange(0, 31, 5)
SNR_lin = 10**(SNR_dB/10)

a = np.array([0.3, 0.4, 0.3])
R = np.array([0.2, 0.15, 0.1])
gamma_th = 2**R - 1
beta, alpha = 0.7, 0.01

out_UE = np.zeros((K, len(SNR_lin)))
for idx, Ps in enumerate(SNR_lin):
    h = np.random.exponential(1.0, (K, MC))
    ht = np.random.exponential(1.0, MC)
    gk = np.random.exponential(1.0, (K, MC))

    for k in range(K):
        Z1 = (1 - beta) + beta * np.sum(a[:k]) if k else (1 - beta)
        sinr = (beta * Ps * a[k] * h[k] * ht * gk[k]) / (
            Ps * h[k] * Z1 + alpha * Ps * ht * gk[k] * Z1 + 1
        )
        out_UE[k, idx] = np.mean(sinr < gamma_th[k])
        
plt.figure(figsize=(7, 5))
for k in range(K):
    plt.semilogy(SNR_dB, out_UE[k], "o-", label=f"UE{k+1}")
plt.grid(True, which="both")
plt.xlabel("SNR (dB)")
plt.ylabel("Outage Probability")
plt.legend()
plt.tight_layout()
plt.show()