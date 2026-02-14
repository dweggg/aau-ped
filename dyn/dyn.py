import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# --- Styling to get serif/LaTeX-like look (without external LaTeX) ---
plt.rcParams.update({
    "font.family": "serif",
    "mathtext.fontset": "cm",   # Computer Modern
    "axes.unicode_minus": False
})

# Constants
lambda_pm = 1.0
I_m = 1.0

# One full rotation of ωt
omega_t = np.linspace(0, 2*np.pi, 500)

# Torque equation
T = -lambda_pm * I_m * 0.5 - lambda_pm * I_m * np.cos(-4*omega_t - np.pi/3)

# Reference level
T_avg = -lambda_pm * I_m * 0.5

# Formatter for ticks in multiples of pi
def pi_formatter(x, pos):
    if np.isclose(x, 0):
        return r"$0$"
    elif np.isclose(x, np.pi):
        return r"$\pi$"
    elif np.isclose(x, 2*np.pi):
        return r"$2\pi$"
    else:
        return r"$%.2f$" % x

# Plot
plt.figure()
plt.plot(omega_t, T, label=r"$T_{m,\mathrm{total}}$", color="#3AB795")

# Dashed horizontal line at -λ_pm I_m 1/2
plt.axhline(T_avg, linestyle="--", linewidth=1.5,
            label=r"$-\lambda_{pm} I_m \frac{1}{2}$", color="#AB74CF")

# Dashed horizontal line at -λ_pm I_m 1/2
plt.axhline(0, linestyle="-", linewidth=0.5, color="#000000")

# Labels and title (LaTeX-style)
plt.xlabel(r"$\omega t$")
plt.ylabel(r"$T_{m,\mathrm{total}}$")
plt.title(r"$T_{m,\mathrm{total}}=-\lambda_{pm}I_m\frac{1}{2}-\lambda_{pm}I_m\cos(-4\omega t-\pi/3)$")

# Ticks
ax = plt.gca()
ax.xaxis.set_major_formatter(FuncFormatter(pi_formatter))

plt.legend()

# Save as PDF
output_path = "torque_plot.svg"
plt.savefig(output_path, format="svg", bbox_inches="tight")
plt.close()