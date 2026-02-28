import numpy as np
import matplotlib.pyplot as plt

# =====================================================
#  MONTE CARLO & SNR GRID
# =====================================================
MC = int(2e5)                    # Monte Carlo samples
SNR_dB = np.arange(0, 31, 5)     # 0:5:30 dB      # 0:5:30 dB
SNR_lin = 10**(SNR_dB/10)        # Ps / sigma^2  (noise variance = 1)

# =====================================================
#  SYSTEM PARAMETERS
# =====================================================
K = 3            # <-- change to 2,3,4,...
beta  = 0.7
alpha = 0.01     # reduced to avoid trivial outage = 1

# Power allocation (must sum to 1)
a = np.array([0.3, 0.4, 0.3])    # example for K=3
# For K=2 you could use: a = np.array([0.3, 0.7])

# =====================================================
#  CHANNEL MEAN POWERS (Rayleigh fading)
# =====================================================
lambda_h = np.array([1.0, 0.5, 0.7])   # one per user
lambda_ht = 1.0
lambda_gk = 1.0

# =====================================================
#  TARGET RATES (DIFFERENT PER USER TO SEPARATE CURVES)
# =====================================================
R = np.array([0.2, 0.15, 0.1])         # bps/Hz

gamma_th = 2**R - 1                    # SINR thresholds

# =====================================================
#  STORAGE
# =====================================================
out_UE = np.zeros((K, len(SNR_dB)))

# =====================================================
#  MONTE CARLO LOOP
# =====================================================
for idx, Ps in enumerate(SNR_lin):

    # --- User channels |h_k|^2 ---
    h = np.zeros((K, MC))
    for k in range(K):
        h[k] = np.random.exponential(lambda_h[k], MC)

    # --- Backscatter channels ---
    ht = np.random.exponential(lambda_ht, MC)

    # --- PER-USER g_k channels (important fix) ---
    gk = np.zeros((K, MC))
    for k in range(K):
        gk[k] = np.random.exponential(lambda_gk, MC)

    # --- Compute commensal SINR for each user ---
    for k in range(K):

        # Z1 = (1-beta) + beta * sum_{i=1}^{k-1} a_i
        if k == 0:
            Z1 = (1 - beta)
        else:
            Z1 = (1 - beta) + beta * np.sum(a[:k])

        # Paper-matched commensal SINR
        sinr_k = (beta * Ps * a[k] * h[k]) / \
                 (Ps * h[k] * Z1 + alpha * Ps * ht * gk[k] + 1)

        # Monte-Carlo outage
        out_UE[k, idx] = np.mean(sinr_k < gamma_th[k])

# =====================================================
#  PLOTTING (USER OUTAGE ONLY)
# =====================================================
plt.figure(figsize=(7,5))
 
for k in range(K):
    plt.semilogy(SNR_dB, out_UE[k], marker='o',
                 label=f'UE{k+1} (commensal)')

plt.grid(True, which='both')
plt.xlabel('Average SNR = P_s/σ² (dB)')
plt.ylabel('Outage Probability')
plt.legend()
plt.tight_layout()
plt.show()
 