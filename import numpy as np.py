import numpy as np
import matplotlib.pyplot as plt

# =====================================================
#  MONTE CARLO & SNR GRID
# =====================================================
MC = int(2e5)                    # Monte Carlo samples
SNR_dB = np.arange(0, 31, 5)     # 0:5:30 dB
SNR_dB = range(0, 31, 5)        # 0:5:30 dB