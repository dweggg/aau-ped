import numpy as np
import matplotlib.pyplot as plt

# Original data
apk = np.array([0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6])
vpk = np.array([3.4, 5.4, 6.7, 7.3, 7.8, 8.1, 8.4, 8.7, 8.9, 9.2, 9.4, 9.5])

# Linear fit parameters (from id >= 2.5 Apk)
slope = 0.5
intercept = 6.625

# Generate fitted line over full range for visualization
vpk_fit = slope * apk + intercept

# Plot
plt.figure()
plt.plot(apk, vpk)
plt.plot(apk, vpk_fit)
plt.xlabel("id [Apk]")
plt.ylabel("vd [Vpk]")
plt.title("Original Data and Linear Fit (id ≥ 2.5 Apk)")
plt.show()