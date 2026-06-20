import numpy as np

R = 0.18 # Ohm
L = 0.002 # H
lambda_pm = 0.123 # V*s/rad
J = 0.0146 # kg*m^2
pp = 4

# 2nd order tuning

Mp = 0.02 # p.u.
ts = 0.05 # s

xi = np.sqrt(np.log(Mp)**2/(np.pi**2+np.log(Mp)**2))
wn = 3/(xi * ts)

kp = 2*xi*wn*L-R
ki = wn**2 * L

print(f"Second order tuning with Mp = {Mp*100:.0f}%, ts = {ts:.1f} ms")
print(f"kp = {kp:.4f}\nki = {ki:.4f}")
print("-"*30)

# Bandwidth method
fb = 241 # Hz

kp = 2*np.pi*fb*L
ki = 2*np.pi*fb*R

print(f"First order tuning with bandwidth = {fb:.0f}Hz (w = {fb*2*np.pi:.0f} rad/s)")
print(f"kp = {kp:.4f}\nki = {ki:.4f}")
print("-"*30)


# Speed PI
fb_n = 30 # Hz


wb_n = fb_n*2*np.pi # rad/s
wb_i = 2*np.pi*fb

from scipy.optimize import fsolve
# Define the function f(delta) = 0
def func(delta):
    return delta + 2.16 * np.exp(delta/(-2.8)) - 1.86 - wb_i/wb_n

# Initial guess for delta
delta_0 = 10.0

# Solve
delta = fsolve(func, delta_0)[0]

K = 45*pp*lambda_pm/np.pi/J

kip_n = wb_i/(delta**2)
kp_n = kip_n * delta / K
ki_n = kip_n*kp_n

print(f"Speed loop tuning with delta = {delta:.3f} (wb_i/wb_n = {wb_i/wb_n:.1f})")
print(f"kp_n = {kp_n:.4f}\nki_n = {ki_n:.4f}")
print("-"*30)
