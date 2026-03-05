import numpy as np
import matplotlib.pyplot as plt

MC = int(2e5)
SNR_dB = np.arange(0, 31, 5)
SNR_lin = 10**(SNR_dB/10)

K = 3
beta = 0.7
alpha = 0.01

a = np.array([0.3, 0.4, 0.3])

lambda_h = np.array([1.0, 0.5, 0.7])
lambda_ht = 1.0
lambda_gk = 1.0

R = np.array([0.2, 0.15, 0.1])
gamma_th = 2**R - 1

out_UE = np.zeros((K, len(SNR_dB)))

for idx, Ps in enumerate(SNR_lin):
    h = np.zeros((K, MC))
    for k in range(K):
        h[k] = np.random.exponential(lambda_h[k], MC)

    ht = np.random.exponential(lambda_ht, MC)

    gk = np.zeros((K, MC))
    for k in range(K):
        gk[k] = np.random.exponential(lambda_gk, MC)

    for k in range(K):
        if k == 0:
            Z1 = (1 - beta)
        else:
            Z1 = (1 - beta) + beta * np.sum(a[:k])

        sinr_k = (beta * Ps * a[k] * h[k]) / (
            Ps * h[k] * Z1 + alpha * Ps * ht * gk[k] + 1
        )
        out_UE[k, idx] = np.mean(sinr_k < gamma_th[k])

plt.figure(figsize=(7, 5))
for k in range(K):
    plt.semilogy(SNR_dB, out_UE[k], marker='o', label=f'UE{k+1} (commensal)')

plt.grid(True, which='both')
plt.xlabel('Average SNR = P_s/σ² (dB)')
plt.ylabel('Outage Probability')
plt.legend()
plt.tight_layout()
plt.show()
