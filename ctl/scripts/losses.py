"""
Power Electronics Loss Calculator
==================================
Solves MOSFET and IGBT switching/conduction loss problems
based on Lecture 8: Hardware Design of Inverters (Aalborg University)

Problems solved:
  Problem 1 – MOSFET turn-off switching loss + conduction loss + thermal resistance
  Problem 2 – IGBT switching loss + conduction loss + thermal resistance
"""

# ─────────────────────────────────────────────────────────────────────────────
# Utility helpers
# ─────────────────────────────────────────────────────────────────────────────

def section(title: str) -> None:
    width = 70
    print("\n" + "=" * width)
    print(f"  {title}")
    print("=" * width)

def subsection(title: str) -> None:
    print(f"\n  {'─'*60}")
    print(f"  {title}")
    print(f"  {'─'*60}")

def result(label: str, value: float, unit: str, indent: int = 4) -> None:
    pad = " " * indent
    print(f"{pad}► {label:<45} {value:>10.4f}  {unit}")

def step(text: str, indent: int = 6) -> None:
    print((" " * indent) + text)


# ─────────────────────────────────────────────────────────────────────────────
# Problem 1 – MOSFET
# ─────────────────────────────────────────────────────────────────────────────

def solve_problem1() -> None:
    section("PROBLEM 1 – MOSFET Switching Loss, Conduction Loss & Thermal Resistance")

    # ── Given parameters ──────────────────────────────────────────────────────
    V_plateau   = 8        # V   – gate plateau voltage
    V_th        = 4        # V   – gate threshold voltage
    R_G         = 5        # Ω   – gate resistance
    V_DS_block  = 70       # V   – blocking voltage
    I_D         = 25       # A   – drain current
    C_ISS       = 6e-9     # F   – input capacitance  (6 nF)
    C_RSS       = 350e-12  # F   – reverse-transfer capacitance (350 pF)
    f_sw        = 10e3     # Hz  – switching frequency (10 kHz)
    I_RMS       = 7        # A   – RMS current for conduction loss
    r_dson      = 5e-3     # Ω   – on-state resistance (5 mΩ)
    delta_T_max = 50       # °C  – allowable junction temperature rise

    print("\n  Given parameters:")
    print(f"    V_plateau  = {V_plateau} V")
    print(f"    V_th       = {V_th} V")
    print(f"    R_G        = {R_G} Ω")
    print(f"    V_DS_block = {V_DS_block} V")
    print(f"    I_D        = {I_D} A")
    print(f"    C_ISS      = {C_ISS*1e9:.1f} nF")
    print(f"    C_RSS      = {C_RSS*1e12:.0f} pF")
    print(f"    f_sw       = {f_sw/1e3:.0f} kHz")
    print(f"    I_RMS      = {I_RMS} A")
    print(f"    r_ds(on)   = {r_dson*1e3:.0f} mΩ")
    print(f"    ΔT_max     = {delta_T_max} °C")

    # ── Part (a): Turn-off switching loss ─────────────────────────────────────
    subsection("Part (a) – Turn-off Switching Loss")

    # Zone 1: V_DG rises (voltage transition), capacitance is C_RSS
    # Gate current during Zone 1 (constant at plateau level):
    I_G2 = V_plateau / R_G
    step(f"Gate current during voltage rise (Zone 1):  I_G2 = V_plateau / R_G"
         f" = {V_plateau}/{R_G} = {I_G2:.4f} A")

    # Transition time t2: charge C_RSS through ΔV_DG ≈ V_DS_blocking
    delta_V_DG = V_DS_block          # ≈ V_DS,blocking
    t2 = (C_RSS * delta_V_DG) / I_G2
    step(f"Voltage-rise time:  t2 = C_RSS · ΔV_DG / I_G2"
         f" = ({C_RSS*1e12:.0f}p × {delta_V_DG}) / {I_G2:.4f}"
         f" = {t2*1e9:.4f} ns")

    # Zone 2: V_GS falls from plateau to V_th, capacitance is C_ISS
    # Average gate current during Zone 2:
    I_G3 = 0.5 * (V_plateau + V_th) / R_G
    step(f"Average gate current during current fall (Zone 2):  I_G3 = 0.5(V_plateau + V_th) / R_G"
         f" = 0.5×({V_plateau}+{V_th})/{R_G} = {I_G3:.4f} A")

    delta_V_GS = V_plateau - V_th   # gate voltage swing in Zone 2
    t3 = (C_ISS * delta_V_GS) / I_G3
    step(f"Current-fall time:  t3 = C_ISS · ΔV_GS / I_G3"
         f" = ({C_ISS*1e9:.1f}n × {delta_V_GS}) / {I_G3:.4f}"
         f" = {t3*1e9:.4f} ns")

    t_turnoff = t2 + t3
    step(f"Total turn-off time:  t_turnoff = t2 + t3 = {t_turnoff*1e9:.4f} ns")

    E_off = 0.5 * V_DS_block * I_D * t_turnoff
    step(f"Turn-off energy:  E_off = 0.5 × V_DS_block × I_D × t_turnoff"
         f" = 0.5 × {V_DS_block} × {I_D} × {t_turnoff*1e6:.6f}µs"
         f" = {E_off*1e6:.4f} µJ")

    P_off = E_off * f_sw
    step(f"Turn-off power loss:  P_off = E_off × f_sw"
         f" = {E_off*1e6:.4f}µJ × {f_sw/1e3:.0f}kHz = {P_off:.4f} W")

    # Assumption: turn-on loss ≈ turn-off loss
    P_on  = P_off
    P_sw  = P_on + P_off
    step(f"Assumption: P_on ≈ P_off  →  P_on = {P_on:.4f} W")
    step(f"Total switching loss:  P_sw = P_on + P_off = {P_sw:.4f} W")

    result("Turn-off power loss  P_off",  P_off,  "W")
    result("Total switching loss P_sw",   P_sw,   "W")

    # ── Part (b): Conduction loss + total loss + thermal resistance ────────────
    subsection("Part (b) – Conduction Loss, Total Loss & Thermal Resistance")

    P_cond = (I_RMS ** 2) * r_dson
    step(f"Conduction loss:  P_cond = I_RMS² × r_ds(on)"
         f" = {I_RMS}² × {r_dson*1e3:.0f}m = {P_cond:.4f} W")

    P_total = P_cond + P_sw
    step(f"Total loss:  P_total = P_cond + P_sw = {P_cond:.4f} + {P_sw:.4f} = {P_total:.4f} W")

    # Thermal resistance: R_theta = ΔT / P_total
    R_theta = delta_T_max / P_total
    step(f"Required thermal resistance (junction-to-ambient):")
    step(f"  R_θ_ja = ΔT_max / P_total = {delta_T_max} / {P_total:.4f} = {R_theta:.4f} °C/W")

    result("Conduction loss    P_cond",     P_cond,   "W")
    result("Total loss         P_total",    P_total,  "W")
    result("Thermal resistance R_θ(j-a)",   R_theta,  "°C/W")


# ─────────────────────────────────────────────────────────────────────────────
# Problem 2 – IGBT
# ─────────────────────────────────────────────────────────────────────────────

def solve_problem2() -> None:
    section("PROBLEM 2 – IGBT Switching Loss, Conduction Loss & Thermal Resistance")

    # ── Given parameters ──────────────────────────────────────────────────────
    E_on        = 0.9e-3   # J   – turn-on energy at test conditions  (4 mJ)
    E_off       = 0.6e-3   # J   – turn-off energy at test conditions (2 mJ)
    V_t         = 600    # V   – test voltage
    I_t         = 15     # A   – test current
    V_dc        = 650    # V   – actual blocking voltage
    I_avg       = 8     # A   – actual average current
    f_sw        = 10e3    # Hz  – switching frequency (3 kHz)
    P_cond      = 12.5      # W   – conduction loss (given)
    delta_T_max = 125-45     # °C  – maximum allowable temperature rise

    print("\n  Given parameters:")
    print(f"    E_on        = {E_on*1e3:.0f} mJ  (at V_t={V_t} V, I_t={I_t} A)")
    print(f"    E_off       = {E_off*1e3:.0f} mJ  (at V_t={V_t} V, I_t={I_t} A)")
    print(f"    V_dc        = {V_dc} V  (actual)")
    print(f"    I_avg       = {I_avg} A  (actual)")
    print(f"    f_sw        = {f_sw/1e3:.0f} kHz")
    print(f"    P_cond      = {P_cond} W  (given)")
    print(f"    ΔT_max      = {delta_T_max} °C")

    # ── Part (a): IGBT switching loss ─────────────────────────────────────────
    subsection("Part (a) – IGBT Total Switching Loss")

    # Scale formula from lecture slides:
    #   P_sw = (E_on + E_off) × (V_dc / V_t) × (I_avg / I_t) × f_sw
    voltage_scale  = V_dc / V_t
    current_scale  = I_avg / I_t

    step(f"Voltage scaling factor:  V_dc / V_t = {V_dc} / {V_t} = {voltage_scale:.4f}")
    step(f"Current scaling factor:  I_avg / I_t = {I_avg} / {I_t} = {current_scale:.4f}")

    E_total = E_on + E_off
    step(f"Total switching energy per cycle (at test conditions):")
    step(f"  E_on + E_off = {E_on*1e3:.2f} mJ + {E_off*1e3:.2f} mJ = {E_total*1e3:.2f} mJ")

    P_sw = E_total * voltage_scale * current_scale * f_sw
    step(f"Switching power loss:")
    step(f"  P_sw = (E_on + E_off) × (V_dc/V_t) × (I_avg/I_t) × f_sw")
    step(f"       = {E_total*1e3:.0f}mJ × {voltage_scale:.4f} × {current_scale:.4f} × {f_sw/1e3:.0f}kHz")
    step(f"       = {P_sw:.4f} W")

    result("Total switching loss P_sw", P_sw, "W")

    # ── Part (b): Total loss + thermal resistance ──────────────────────────────
    subsection("Part (b) – Total Loss & Thermal Resistance")

    P_total = P_cond + P_sw
    step(f"Total losses:  P_total = P_cond + P_sw = {P_cond} + {P_sw:.4f} = {P_total:.4f} W")

    R_theta = delta_T_max / P_total
    step(f"Required thermal resistance (junction-to-ambient):")
    step(f"  R_θ_ja = ΔT_max / P_total = {delta_T_max} / {P_total:.4f} = {R_theta:.4f} °C/W")

    result("Conduction loss    P_cond",    P_cond,   "W")
    result("Total loss         P_total",   P_total,  "W")
    result("Thermal resistance R_θ(j-a)",  R_theta,  "°C/W")


# ─────────────────────────────────────────────────────────────────────────────
# Summary
# ─────────────────────────────────────────────────────────────────────────────

def print_summary() -> None:
    section("SUMMARY")
    print("""
  Key formulas used
  ─────────────────
  MOSFET conduction loss:
      P_cond = I_rms² × r_ds(on)

  MOSFET turn-off transition times:
      I_G2       = V_plateau / R_G
      I_G3       = 0.5 × (V_plateau + V_th) / R_G
      t2         = C_RSS × ΔV_DG / I_G2          (voltage-rise zone)
      t3         = C_ISS × ΔV_GS / I_G3          (current-fall zone)
      t_turnoff  = t2 + t3

  MOSFET turn-off energy & power:
      E_off = 0.5 × V_DS,off × I_D × t_turnoff
      P_off = E_off × f_sw
      (P_on ≈ P_off assumed)

  IGBT switching loss (scaled from datasheet):
      P_sw = (E_on + E_off) × (V_dc / V_t) × (I_avg / I_t) × f_sw

  IGBT conduction loss:
      P_cond = V_F × i_avg + i_rms² × r_on

  Thermal resistance (junction-to-ambient):
      R_θ_ja = ΔT_allowable / P_total
    """)


# ─────────────────────────────────────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    solve_problem1()
    solve_problem2()
    print_summary()
    print("=" * 70)
    print("  Done.")
    print("=" * 70 + "\n")
