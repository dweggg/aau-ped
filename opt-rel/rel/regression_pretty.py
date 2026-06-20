import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress, beta


# ─── Helpers ──────────────────────────────────────────────────────────────────

def median_ranks(n, P=0.5):
    """Exact median ranks via the beta distribution (Nelson 1982).
    P=0.5 → median ranks (point estimate fit)
    P=0.9 → 90th-percentile ranks (conservative / upper-bound fit)
    """
    return np.array([beta.ppf(P, j, n - j + 1) for j in range(1, n + 1)])


def weibull_transform(F):
    """Linearising transform for the Weibull CDF: y = ln(-ln(1-F))."""
    return np.log(-np.log(1 - F))


def fit_weibull(ln_t, y):
    """OLS fit on Weibull paper. Returns (beta, eta, R²).
    slope  = β  (shape)
    intercept → η = exp(-intercept / β)  (characteristic life)
    """
    res = linregress(ln_t, y)
    b   = res.slope
    eta = np.exp(-res.intercept / b)
    r2  = res.rvalue ** 2
    return b, eta, r2, res


def bx_lifetime(eta, beta_, reliability):
    """Time at which reliability == R, i.e. F = 1 - R.
    From R(t) = exp(-(t/η)^β)  →  t = η · (-ln R)^(1/β)
    """
    return eta * (-np.log(reliability)) ** (1 / beta_)


# ─── Part 1: Weibull fit for three failure criteria ───────────────────────────
#
# Three sets of time-to-failure data, each corresponding to a different
# leakage-current failure criterion: FC1=1µA, FC2=5µA, FC3=25µA.
# All 16 samples failed, so no censoring.

print("=" * 55)
print("PART 1: Weibull fit per failure criterion")
print("=" * 55)

ttf_data = {
    "FC1 (1 µA)":  [5,6,11,13,13,16,20,22,22,26,32,35,36,37,37,40],
    "FC2 (5 µA)":  [15,22,22,25,30,31,33,34,34,36,36,37,37,37,39,40],
    "FC3 (25 µA)": [34,34,34,34,35,35,35,35,37,37,38,38,38,39,40,40],
}

n   = len(next(iter(ttf_data.values())))
F   = median_ranks(n, P=0.5)
y   = weibull_transform(F)

fig, axes = plt.subplots(1, 3, figsize=(14, 5), sharey=True)
fig.suptitle("Part 1: Weibull probability plots (50% median ranks)")

for ax, (label, ttf) in zip(axes, ttf_data.items()):
    ln_t = np.log(ttf)
    b, eta, r2, res = fit_weibull(ln_t, y)

    # Bx lifetimes: B1 → F=0.01 (R=0.99), B10 → F=0.10 (R=0.90)
    t_B1  = bx_lifetime(eta, b, reliability=0.99)
    t_B10 = bx_lifetime(eta, b, reliability=0.90)

    print(f"\n{label}")
    print(f"  β   = {b:.3f}   η = {eta:.2f} h")
    print(f"  R²  = {r2:.3f}")
    print(f"  B1  lifetime : {t_B1:.2f} h")
    print(f"  B10 lifetime : {t_B10:.2f} h")

    # Plot data + fit line
    t_fit = np.linspace(ln_t[0], ln_t[-1], 100)
    ax.scatter(ln_t, y, zorder=3, label="Data")
    ax.plot(t_fit, res.slope * t_fit + res.intercept, "--", label=f"Fit (β={b:.2f})")
    ax.set_title(label)
    ax.set_xlabel("ln(TTF)")
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

axes[0].set_ylabel("ln(−ln(1−F))")
plt.tight_layout()
plt.show()
plt.close()


# ─── Part 2: Lifetime vs voltage (Inverse Power Law) ─────────────────────────
#
# Four voltage stress levels; 15 samples each (no censoring).
# B0.01 lifetime at 90% confidence: fit using 90th-percentile ranks.
# B1   lifetime at 50% confidence: fit using 50th-percentile (median) ranks.
#
# The Inverse Power Law gives:  ln(L) = -B·ln(V) + C
# so we regress  ln(Bx_lifetime)  vs  ln(V).
#
# NOTE: the 6V group is excluded from the regression: its β differs
# markedly from the lower-voltage groups, suggesting a different
# dominant failure mechanism kicks in at that stress level.

print("\n" + "=" * 55)
print("PART 2: Lifetime vs voltage (Inverse Power Law)")
print("=" * 55)

ttf_per_voltage = {
    4.0: [1850,1890,1903,1905,1940,2001,2005,2030,2031,2035,2050,2125,2155,2170,2220],
    5.0: [31,34.6,35,35,35,35.1,36,37,37,37.6,38.1,38.5,38.7,40,41],
    5.5: [4.6,4.7,4.8,4.8,4.8,5.0,5.0,5.0,5.1,5.1,5.1,5.3,5.4,5.4,5.55],
    6.0: [0.30,0.35,0.38,0.45,0.52,0.58,0.60,0.69,0.69,0.72,0.75,0.80,0.90,1.15,1.20],
}

n    = len(next(iter(ttf_per_voltage.values())))
y90  = weibull_transform(median_ranks(n, P=0.90))   # conservative upper-bound fit
y50  = weibull_transform(median_ranks(n, P=0.50))   # median / point-estimate fit

B001_90 = []   # B0.01 at 90% confidence, one value per voltage level
B1_50   = []   # B1   at 50% confidence, one value per voltage level

fig, axes = plt.subplots(1, 4, figsize=(16, 5), sharey=True)
fig.suptitle("Part 2: Weibull probability plots per voltage level")

for ax, (v, ttf) in zip(axes, ttf_per_voltage.items()):
    ln_t = np.log(ttf)

    # 90% rank fit → conservative B0.01
    b90, eta90, r2_90, res90 = fit_weibull(ln_t, y90)
    life_B001 = bx_lifetime(eta90, b90, reliability=0.9999)   # B0.01: F=0.0001
    B001_90.append(life_B001)

    # 50% rank fit → point-estimate B1
    b50, eta50, r2_50, res50 = fit_weibull(ln_t, y50)
    life_B1 = bx_lifetime(eta50, b50, reliability=0.99)       # B1:   F=0.01
    B1_50.append(life_B1)

    print(f"\nV = {v} V")
    print(f"  [90% ranks]  β={b90:.2f}  η={eta90:.3g}  R²={r2_90:.3f}  → B0.01={life_B001:.3g} h")
    print(f"  [50% ranks]  β={b50:.2f}  η={eta50:.3g}  R²={r2_50:.3f}  → B1  ={life_B1:.3g} h")

    t_fit = np.linspace(ln_t[0], ln_t[-1], 100)
    ax.scatter(ln_t, y90, s=20, label="Data (90%)", alpha=0.7)
    ax.scatter(ln_t, y50, s=20, label="Data (50%)", alpha=0.7)
    ax.plot(t_fit, res90.slope * t_fit + res90.intercept, "--", lw=1)
    ax.plot(t_fit, res50.slope * t_fit + res50.intercept, "--", lw=1)
    ax.set_title(f"V = {v} V")
    ax.set_xlabel("ln(TTF)")
    ax.grid(True, alpha=0.3)

axes[0].set_ylabel("ln(−ln(1−F))")
axes[0].legend(fontsize=7)
plt.tight_layout()
plt.show()
plt.close()


# ─── Part 2 (cont.): Inverse Power Law regression ────────────────────────────
#
# Regress  ln(Bx_lifetime)  vs  ln(V)  using the 4V–5.5V groups only.
# The fitted slope is -B (power law exponent) and exp(intercept) is the
# pre-factor.  Extrapolating to 3V uses the same log-log relationship.

voltages   = np.array(list(ttf_per_voltage.keys()))
ln_v_fit   = np.log(voltages[:-1])          # exclude 6V
ln_v_all   = np.log(voltages)

fit_B001 = linregress(ln_v_fit, np.log(B001_90)[:-1])
fit_B1   = linregress(ln_v_fit, np.log(B1_50)[:-1])

print("\n--- Inverse Power Law regression (4V – 5.5V) ---")
print(f"  B0.01/90%:  slope={fit_B001.slope:.3f}  intercept={fit_B001.intercept:.3f}  R²={fit_B001.rvalue**2:.3f}")
print(f"  B1/50%  :  slope={fit_B1.slope:.3f}  intercept={fit_B1.intercept:.3f}  R²={fit_B1.rvalue**2:.3f}")

# Plot ln(Bx) vs ln(V)
fig, ax = plt.subplots(figsize=(7, 5))
ln_v_range = np.linspace(np.log(3), np.log(7), 100)

ax.scatter(ln_v_all, np.log(B001_90), label="B0.01/90% data", zorder=3)
ax.scatter(ln_v_all, np.log(B1_50),   label="B1/50% data",    zorder=3)
ax.plot(ln_v_range, fit_B001.slope * ln_v_range + fit_B001.intercept, "--", label="B0.01/90% fit (4–5.5V)")
ax.plot(ln_v_range, fit_B1.slope   * ln_v_range + fit_B1.intercept,   "--", label="B1/50% fit (4–5.5V)")
ax.axvline(np.log(3), color="gray", lw=0.8, ls=":", label="3V (extrapolation)")
ax.set_xlabel("ln(V)")
ax.set_ylabel("ln(Bx lifetime)")
ax.set_title("Inverse Power Law: ln(lifetime) vs ln(V)")
ax.legend(fontsize=8)
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
plt.close()


# ─── Part 3: Extrapolate to 3V ───────────────────────────────────────────────
#
# Using the IPL model fitted in Part 2.
# NOTE: 3V is below the lowest tested stress (4V); extrapolation always
# carries uncertainty and assumes the same failure mechanism persists.

print("\n" + "=" * 55)
print("PART 3: Extrapolation to 3V")
print("=" * 55)

life_3V = np.exp(fit_B001.slope * np.log(3) + fit_B001.intercept)
print(f"\n  B0.01 lifetime at 90% confidence, V=3V: {life_3V:.0f} h")
print(f"  ({life_3V/8760:.1f} years)")
