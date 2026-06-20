import numpy as np

# ============================================================================
# Induction Motor Rated Rotor-Flux Current Calculation
# Rotor Flux Oriented Control (RFOC)
# ============================================================================

# -----------------------------
# Nameplate data
# -----------------------------
V_line = 400.0      # V (Y connection)
I_line = 1.1        # A (Y connection)
f = 50.0            # Hz
pf = 0.64

# -----------------------------
# Motor parameters
# -----------------------------
Rs = 26.5           # Ohm
Rr = 23.9           # Ohm

Ls = 0.79           # H
Lr = 0.79           # H
Lm = 0.71           # H

# -----------------------------
# Base quantities
# -----------------------------
omega_b = 2 * np.pi * f

# Leakage factor
K_sigma = 1.0 - (Lm**2) / (Ls * Lr)

# Power factor angle
phi = np.arccos(pf)

# -----------------------------
# Convert rated RMS values
# to peak values used in
# space-vector equations
# -----------------------------
V_phase_rms = V_line / np.sqrt(3)

V_dqs = np.sqrt(2) * V_phase_rms
I_dqs = np.sqrt(2) * I_line

# Complex stator current phasor
I_s = I_dqs * np.exp(-1j * phi)

# -----------------------------
# Stator flux linkage phasor
# λ_ds
# -----------------------------
lambda_s = (V_dqs - Rs * I_s) / (1j * omega_b)

# -----------------------------
# Rotor flux linkage phasor
# λ_dr
# -----------------------------
lambda_r = (Lr / Lm) * (lambda_s - K_sigma * Ls * I_s)

# -----------------------------
# Rotor-flux-oriented frame:
# i_dr = 0
#
# λ_dr = Lm * i_ds
#
# => i_ds = |λ_dr| / Lm
# -----------------------------
i_ds_peak = np.abs(lambda_r) / Lm
i_ds_rms = i_ds_peak / np.sqrt(2)

# -----------------------------
# Results
# -----------------------------
print("========== RESULTS ==========")
print(f"Base electrical speed ωb = {omega_b:.3f} rad/s")
print(f"Leakage factor Kσ        = {K_sigma:.6f}")
print()

print("Stator flux linkage:")
print(f"λs = {lambda_s.real:.6f} + j{lambda_s.imag:.6f} Wb")
print()

print("Rotor flux linkage:")
print(f"λr = {lambda_r.real:.6f} + j{lambda_r.imag:.6f} Wb")
print(f"|λr| = {np.abs(lambda_r):.6f} Wb")
print()

print("Rated d-axis current (Rotor Flux Oriented Control)")
print(f"i_ds_peak = {i_ds_peak:.6f} A")
print(f"i_ds_rms  = {i_ds_rms:.6f} A")
