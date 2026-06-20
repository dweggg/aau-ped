import numpy as np
import matplotlib.pyplot as plt

"""
Space Vector Modulation — the theory

Definition. 
A two-level three-phase voltage-source inverter has 8 possible switching states (2³), 
which correspond to 8 discrete voltage vectors in the stationary αβ plane: six non-zero "active" 
vectors V1…V6 of equal magnitude, 60° apart, forming a hexagon, and two zero vectors V0(000) and 
V7(111) at the origin. Space Vector Modulation synthesizes any desired reference voltage vector 
Vref (the output of the vector-control current/voltage loop) by applying, within every sampling 
period Ts, the two active vectors that bound the sector in which Vref currently lies, plus a zero 
vector, each for a calculated fraction of Ts. The time-averaged volt-second balance over Ts then 
reproduces Vref exactly (within the hexagon).

Why SVM is preferred over sinusoidal PWM in vector control. In field-oriented / vector control the 
controller already outputs Vref directly as a vector in the αβ (or dq, then rotated) frame — SVM 
consumes that vector natively, with no extra per-phase sine-wave reconstruction or carrier comparison 
needed, which is exactly the digital implementation a microcontroller/DSP wants. Beyond the 
architectural fit, SVM gives a higher DC-bus utilization: the maximum undistorted output voltage SVM 
can produce reaches the inscribed circle of the hexagon, radius Vdc/√3, whereas plain sinusoidal PWM 
is limited to Vdc/2 — about 15.5% more usable voltage from the same bus. For the same switching 
frequency, SVM also produces lower harmonic distortion/current ripple, and because the zero-vector 
time can be freely split between V0 and V7, it allows flexible loss-optimized patterns (continuous or 
discontinuous SVPWM) that plain SPWM doesn't offer.

Why the sequence is mirrored. 
The seven-segment sequence within one Ts is built so that (1) every transition between consecutive 
switching states changes only one inverter leg, minimizing switching losses and avoiding large 
simultaneous voltage steps, and (2) the pattern is symmetric (palindromic) about the centre of Ts, 
which centres every phase's pulse in the period. That symmetry gives the standard "centred" double-edge 
PWM, cancels even-order harmonics and minimizes THD for a given switching frequency compared with an 
edge-aligned (non-mirrored) sequence, and it also makes the end-state of one period match smoothly into 
the next.

Unified Formula (all sectors)

Let:

alpha = theta - (k - 1) * 60°

where:
k = sector number (1 to 6)
theta = reference vector angle
alpha = local angle inside the sector (0° to 60°)

Then for every sector:

T1 = Ts * (sqrt(3) * |Vref| / Vdc) * sin(60° - alpha)

T2 = Ts * (sqrt(3) * |Vref| / Vdc) * sin(alpha)

T0 = Ts - T1 - T2

"""

Vdc        = 400.0      # DC bus voltage [V]
Vref_mag   = 180.0       # magnitude of the reference voltage vector |Vref| [V]
theta_deg  = 12.0        # angle of Vref from the alpha-axis [deg], 0-360
Ts         = 100e-6      # switching / sampling period [s]

SECTOR_FOR_TABLE = 2     # which sector's switching table & gate signals to draw (1-6)
                          # (independent from theta_deg, so you can inspect
                          #  any sector's table even if Vref is elsewhere)

SHOW_HEXAGON       = True
SHOW_SEQUENCE_TABLE = True
SHOW_GATE_SIGNALS   = True
SHOW_VOLTAGE_LIMIT_CIRCLES = True   # SPWM vs SVM max-voltage circles on the hexagon plot
# ============================================================================

SQ3 = np.sqrt(3)

# Switching states (Sa, Sb, Sc) -- 1 = top switch of that leg ON
STATE = {0: (0, 0, 0), 1: (1, 0, 0), 2: (1, 1, 0), 3: (0, 1, 0),
         4: (0, 1, 1), 5: (0, 0, 1), 6: (1, 0, 1), 7: (1, 1, 1)}


# ----------------------------------------------------------------------------
# Core SVM math
# ----------------------------------------------------------------------------
def get_sector(angle_deg):
    """Sector number 1..6 for a given absolute angle."""
    angle_deg = angle_deg % 360
    return int(angle_deg // 60) + 1


def sector_vectors(k):
    """Lower / upper active-vector index that bound sector k (1..6)."""
    lower = k
    upper = k + 1 if k < 6 else 1
    return lower, upper


def sector_times(Vdc, Vref_mag, theta_deg, Ts):
    """
    Compute sector number and on-times T1 (lower vector Vk), T2 (upper
    vector Vk+1) and T0 (combined zero-vector time) for the given Vref.
    """
    angle = theta_deg % 360
    k = get_sector(angle)
    theta_local = angle - (k - 1) * 60.0          # 0-60 deg inside the sector

    a = SQ3 * Vref_mag / Vdc                      # modulation factor
    overmodulated = a > 1.0
    a = min(a, 1.0)                                # clip to linear region (hexagon boundary)

    T1 = Ts * a * np.sin(np.radians(60.0 - theta_local))   # on-time of lower vector Vk
    T2 = Ts * a * np.sin(np.radians(theta_local))           # on-time of upper vector Vk+1
    T0 = max(Ts - T1 - T2, 0.0)                              # combined zero-vector time

    return k, theta_local, T1, T2, T0, overmodulated


def seven_segment_sequence(k, T1, T2, T0):
    """
    Build the symmetric 7-segment switching sequence for sector k.
    T1 = on-time of the LOWER active vector Vk
    T2 = on-time of the UPPER active vector V(k+1)

    Odd sectors  (1,3,5): 0 -> lower -> upper -> 7 -> 7 -> upper -> lower -> 0
    Even sectors (2,4,6): 0 -> upper -> lower -> 7 -> 7 -> lower -> upper -> 0
    (this keeps every transition a single-bit / single-leg change)

    Returns a list of (state_index, duration) tuples spanning one full Ts.
    """
    lower, upper = sector_vectors(k)

    if k % 2 == 1:                      # odd sector
        first, second = lower, upper
        t_first, t_second = T1, T2
    else:                                # even sector
        first, second = upper, lower
        t_first, t_second = T2, T1

    first_half = [
        (0, T0 / 4.0),
        (first, t_first / 2.0),
        (second, t_second / 2.0),
        (7, T0 / 4.0),
    ]
    second_half = list(reversed(first_half))   # mirrored second half
    return first_half + second_half


# ----------------------------------------------------------------------------
# Plot 1: the space-vector hexagon with all 6 sectors / vectors
# ----------------------------------------------------------------------------
def plot_hexagon(Vdc, Vref_mag, theta_deg, Ts):
    k, theta_local, T1, T2, T0, overmod = sector_times(Vdc, Vref_mag, theta_deg, Ts)
    Vmag = (2.0 / 3.0) * Vdc            # magnitude of each active vector

    fig, ax = plt.subplots(figsize=(7.2, 7.2))

    # --- hexagon outline ---
    hex_angles = np.radians(np.arange(0, 360, 60))
    hx, hy = Vmag * np.cos(hex_angles), Vmag * np.sin(hex_angles)
    hx, hy = np.append(hx, hx[0]), np.append(hy, hy[0])
    ax.plot(hx, hy, 'k-', lw=1.5, zorder=1)

    # --- active vectors V1..V6 ---
    for i in range(6):
        ang = np.radians(i * 60)
        x, y = Vmag * np.cos(ang), Vmag * np.sin(ang)
        ax.annotate('', xy=(x, y), xytext=(0, 0),
                     arrowprops=dict(arrowstyle='->', color='dimgray', lw=1.2))
        ax.text(x * 1.14, y * 1.14, f"V{i+1}\n{STATE[i+1]}",
                 ha='center', va='center', fontsize=9)

    # --- sector labels ---
    for i in range(6):
        midang = np.radians(i * 60 + 30)
        rx, ry = 0.45 * Vmag * np.cos(midang), 0.45 * Vmag * np.sin(midang)
        ax.text(rx, ry, f"S{i+1}", fontsize=12, color='steelblue', fontweight='bold')

    # --- zero vectors ---
    ax.plot(0, 0, 'ko', ms=5, zorder=3)
    ax.text(0.04 * Vmag, -0.10 * Vmag, "V0 (000)\nV7 (111)", fontsize=8)

    # --- voltage-limit circles: SPWM (Vdc/2) vs SVM (Vdc/sqrt3) ---
    if SHOW_VOLTAGE_LIMIT_CIRCLES:
        th = np.linspace(0, 2 * np.pi, 200)
        r_spwm = Vdc / 2.0
        r_svm = Vdc / SQ3
        ax.plot(r_spwm * np.cos(th), r_spwm * np.sin(th), '--',
                 color='orange', lw=1.2, label=f"SPWM limit  Vdc/2 = {r_spwm:.0f} V")
        ax.plot(r_svm * np.cos(th), r_svm * np.sin(th), '--',
                 color='green', lw=1.2, label=f"SVM limit  Vdc/sqrt3 = {r_svm:.0f} V")

    # --- reference vector and its decomposition into T1, T2 components ---
    th = np.radians(theta_deg)
    vx, vy = Vref_mag * np.cos(th), Vref_mag * np.sin(th)
    ax.annotate('', xy=(vx, vy), xytext=(0, 0),
                 arrowprops=dict(arrowstyle='->', color='crimson', lw=2.6), zorder=4)
    ax.text(vx * 1.06, vy * 1.06, "Vref", color='crimson', fontsize=11, fontweight='bold')

    lower, upper = sector_vectors(k)
    angL, angU = np.radians((lower - 1) * 60), np.radians((upper - 1) * 60)
    compL = (T1 / Ts) * Vmag if Ts > 0 else 0
    compU = (T2 / Ts) * Vmag if Ts > 0 else 0
    Lx, Ly = compL * np.cos(angL), compL * np.sin(angL)
    Ux, Uy = compU * np.cos(angU), compU * np.sin(angU)
    ax.plot([0, Lx], [0, Ly], 'b--', lw=1.6, label=f"(T1/Ts)*V{lower}")
    ax.plot([Lx, Lx + Ux], [Ly, Ly + Uy], 'g--', lw=1.6, label=f"(T2/Ts)*V{upper}")

    lim = 1.45 * Vmag
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    ax.set_aspect('equal')
    ax.axhline(0, color='lightgray', lw=0.6)
    ax.axvline(0, color='lightgray', lw=0.6)

    om_note = "  (OVERMODULATED - clipped to hexagon boundary)" if overmod else ""
    ax.set_title(
        f"SVM space-vector hexagon   |Vref|={Vref_mag:.0f} V   theta={theta_deg:.1f} deg"
        f"   ->  Sector {k}{om_note}\n"
        f"T1={T1*1e6:.2f} us   T2={T2*1e6:.2f} us   T0={T0*1e6:.2f} us   "
        f"(Ts={Ts*1e6:.1f} us)"
    )
    ax.legend(loc='lower right', fontsize=8, framealpha=0.9)
    plt.tight_layout()
    plt.show()


# ----------------------------------------------------------------------------
# Plot 2: switching sequence table for a chosen sector
# ----------------------------------------------------------------------------
def plot_sequence_table(k, T1, T2, T0, Ts):
    seq = seven_segment_sequence(k, T1, T2, T0)
    col_labels = ["Segment", "Duration", "Sa", "Sb", "Sc", "Vector"]
    rows = []
    for i, (state, dur) in enumerate(seq):
        sa, sb, sc = STATE[state]
        vec_name = "V0" if state == 0 else ("V7" if state == 7 else f"V{state}")
        rows.append([str(i + 1), f"{dur*1e6:.2f} us", str(sa), str(sb), str(sc), vec_name])

    fig, ax = plt.subplots(figsize=(7.2, 3.4))
    ax.axis('off')
    tbl = ax.table(cellText=rows, colLabels=col_labels, loc='center', cellLoc='center')
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(10)
    tbl.scale(1, 1.5)
    ax.set_title(
        f"Symmetric 7-segment switching sequence - Sector {k}\n"
        f"T1={T1*1e6:.2f} us   T2={T2*1e6:.2f} us   T0={T0*1e6:.2f} us   Ts={Ts*1e6:.1f} us",
        fontsize=11
    )
    plt.tight_layout()
    plt.show()

    # also print it as plain text for quick console reading
    print(f"\nSwitching sequence - Sector {k}:")
    print("  Segment | Duration   | Sa Sb Sc | Vector")
    for r in rows:
        print(f"  {r[0]:>7} | {r[1]:>9} | {r[2]}  {r[3]}  {r[4]}  | {r[5]}")


# ----------------------------------------------------------------------------
# Plot 3: gate signals (Sa, Sb, Sc) over one switching period
# ----------------------------------------------------------------------------
def plot_gate_signals(k, T1, T2, T0, Ts):
    seq = seven_segment_sequence(k, T1, T2, T0)

    times = [0.0]
    sa, sb, sc = [], [], []
    cum = 0.0
    for state, dur in seq:
        s = STATE[state]
        sa.append(s[0]); sb.append(s[1]); sc.append(s[2])
        cum += dur
        times.append(cum)

    times = np.array(times)
    fig, axs = plt.subplots(3, 1, figsize=(8.5, 5.2), sharex=True)
    signals = [sa, sb, sc]
    labels = ['Phase A gate (Sa)', 'Phase B gate (Sb)', 'Phase C gate (Sc)']
    colors = ['tab:blue', 'tab:orange', 'tab:green']

    for ax, sig, lab, col in zip(axs, signals, labels, colors):
        y = np.array(sig + [sig[-1]])           # repeat last value for the closing edge
        ax.step(times * 1e6, y, where='post', lw=2.2, color=col)
        ax.set_ylim(-0.3, 1.3)
        ax.set_yticks([0, 1])
        ax.set_ylabel(lab, fontsize=9)
        ax.grid(alpha=0.3)
        for t in times:
            ax.axvline(t * 1e6, color='lightgray', lw=0.6, zorder=0)

    axs[-1].set_xlabel("time [us]")
    fig.suptitle(f"Generic gate signals - Sector {k}  (one switching period Ts={Ts*1e6:.1f} us)")
    plt.tight_layout()
    plt.show()


# ============================================================================
# RUN
# ============================================================================
if __name__ == "__main__":
    k_ref, theta_local, T1_ref, T2_ref, T0_ref, overmod = sector_times(
        Vdc, Vref_mag, theta_deg, Ts
    )
    print(f"Vref = {Vref_mag:.1f} V @ {theta_deg:.1f} deg  ->  Sector {k_ref}"
          f"  (local angle {theta_local:.1f} deg)")
    print(f"T1 = {T1_ref*1e6:.3f} us   T2 = {T2_ref*1e6:.3f} us   "
          f"T0 = {T0_ref*1e6:.3f} us   (Ts = {Ts*1e6:.1f} us)")
    if overmod:
        print("WARNING: |Vref| exceeds Vdc/sqrt(3) -> overmodulation, clipped to hexagon boundary.")

    if SHOW_HEXAGON:
        plot_hexagon(Vdc, Vref_mag, theta_deg, Ts)

    # the sequence table / gate signals use an independently chosen sector,
    # so you can inspect e.g. sector 2 even if Vref above sits in sector 1
    k_tab, _, T1_tab, T2_tab, T0_tab, _ = sector_times(
        Vdc, Vref_mag, (SECTOR_FOR_TABLE - 1) * 60.0 + 30.0, Ts
    )  # use the mid-angle of that sector so T1/T2 are representative

    if SHOW_SEQUENCE_TABLE:
        plot_sequence_table(k_tab, T1_tab, T2_tab, T0_tab, Ts)

    if SHOW_GATE_SIGNALS:
        plot_gate_signals(k_tab, T1_tab, T2_tab, T0_tab, Ts)
