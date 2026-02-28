import numpy as np
import matplotlib.pyplot as plt

# ===============================
# Monte Carlo parameters
# ===============================
MC = int(1e6)
SNR_dB = np.arange(0, 31, 5)

# Convert SNR from dB to linear (average SNR)
SNR_lin = 10 ** (SNR_dB / 10)

# ===============================
# System constants
# ===============================
a1 = 0.3
a2 = 1 - a1
beta = 0.7
alpha = 0.1

# ===============================
# Channel mean powers (Rayleigh)
# ===============================
lambda_h1 = 1
lambda_h2 = 0.5
lambda_f  = 1     # h_t
lambda_gb = 1     # g_k

# ===============================
# Target rates
# ===============================
R1 = 1
R2 = 1
Ri = 0.05

gamma_th_1 = 2**R1 - 1
gamma_th_2 = 2**R2 - 1
gamma_th_i = 2**Ri - 1

# ===============================
# Storage
# ===============================
out_UE1_sim = []
out_UE2_sim = []
out_BD_sim  = []

# ===============================
# Monte Carlo simulation
# ===============================
for gamma_bar in SNR_lin:

    # Instantaneous channel power gains
    h1 = np.random.exponential(lambda_h1, MC)
    h2 = np.random.exponential(lambda_h2, MC)
    ht = np.random.exponential(lambda_f,  MC)
    gk = np.random.exponential(lambda_gb, MC)

    # ===============================
    # Instantaneous SINRs (parasitic, noise-normalized)
    # ===============================

    # UE1 (k = 1, sum_{i=1}^{k-1} a_i = 0)
    sinr_UE1 = (gamma_bar * beta * a1 * h1) / (
                   gamma_bar * beta * a2 * h1 + 1
               )

    # UE2 (after SIC, noise-limited assumption)
    sinr_UE2 = gamma_bar * beta * a2 * h2

    # Backscatter device
    sinr_BD = gamma_bar * (1 - beta) * alpha * ht * gk

    # ===============================
    # Outage probabilities
    # ===============================
    out_UE1_sim.append(np.mean(sinr_UE1 < gamma_th_1))
    out_UE2_sim.append(np.mean(sinr_UE2 < gamma_th_2))
    out_BD_sim.append(np.mean(sinr_BD  < gamma_th_i))

# ===============================
# Plot
# ===============================
plt.figure(figsize=(7, 5))

plt.semilogy(SNR_dB, out_UE2_sim, 'rx', markersize=7, label=r'UE$_2$ (parasitic)')
plt.semilogy(SNR_dB, out_UE1_sim, 'b*', markersize=7, label=r'UE$_1$ (parasitic)')
plt.semilogy(SNR_dB, out_BD_sim,  'r+', markersize=7, label=r'BD$_T$ (parasitic)')

plt.grid(True, which='both')
plt.xlabel('SNR (dB)')
plt.ylabel('Outage Probability')
plt.legend()
plt.tight_layout()
plt.show()
