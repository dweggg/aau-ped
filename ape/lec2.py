"""
Exercise 1
"""

import matplotlib.pyplot as plt
import numpy as np

materials = [
			{"name":"Si", "Eg_eV": 1.124, "Nc_cm-3": 2.86e19, "Nv_cm-3": 3.10e19, "mu_n_cm2Vs": 1420, "epsilon": 11.9, "Ec_kV_cm": 300},
			{"name":"GaAs", "Eg_eV": 1.422, "Nc_cm-3": 4.7e17, "Nv_cm-3": 7.0e18, "mu_n_cm2Vs": 8000, "epsilon": 13.1, "Ec_kV_cm": 400},
			{"name":"4H-SiC", "Eg_eV": 3.23, "Nc_cm-3": 1.69e19, "Nv_cm-3": 2.49e19, "mu_n_cm2Vs": 1000, "epsilon": 10.1, "Ec_kV_cm": 2200},
			{"name":"GaN", "Eg_eV": 3.39, "Nc_cm-3": 2.2e18, "Nv_cm-3": 4.60e19, "mu_n_cm2Vs": 1000, "epsilon": 9, "Ec_kV_cm": 2000}
			]

temps = np.linspace(300,1800, num=600)

k_eVK = 8.617333262e-5

for material in materials:
	C = material["Nc_cm-3"]*material["Nv_cm-3"]*((np.exp(temps/300))**3.43)
	ni = np.sqrt(C*np.exp(-material["Eg_eV"]/(k_eVK*temps)))
	plt.plot(temps,ni, label=material["name"])
plt.yscale('log')
plt.legend()
#plt.show()

# ni = nd
# nd = 5e14
# ni^2 = (Nc*Nv*(exp(T/300))**3.43)*exp(-Eg/(k*T))
# Si

si_temp = 475.577
nd = np.sqrt(materials[0]["Nc_cm-3"]*materials[0]["Nv_cm-3"]*((np.exp(si_temp/300))**3.43)*np.exp(-materials[0]["Eg_eV"]/(k_eVK*si_temp)))
print("1. c) ",materials[0]["name"],": ","{:e}".format(nd))

sic_temp = 1106.023
nd = np.sqrt(materials[2]["Nc_cm-3"]*materials[2]["Nv_cm-3"]*((np.exp(sic_temp/300))**3.43)*np.exp(-materials[2]["Eg_eV"]/(k_eVK*sic_temp)))
print("1. c) ",materials[2]["name"],": ","{:e}".format(nd))

"""
Exercise 2

A piece of n-type Silicon doped at Nd=1 x 1015 cm-3 has a cross-sectional area of 0.5 cm2 and a thickness of
100 μm. Use necessary values from Table 2.2. You may assume that the donor electrons dominate the
carrier concentration completely which implies n≈Nd and p≈0.
a) Calculate the resistivity of the material
b) Calculate the vertical resistance of the Si piece.
c) In MOSFETS in the on-state the carriers typically have to cross a resistive layer of doped material like that
in a) and b) –this is called the drift layer or epilayer and adds to the on-state resistance. From table 2.2
argue why drift layers in MOSFETS often are n-type?

"""

nd_cm3 = 1e15
area_cm2 = 0.5
thickness_cm = 0.01
q = 1.602176634e-19

rho_ohm_cm = 1/(q*materials[0]["mu_n_cm2Vs"]*nd_cm3)

print("2. a) ",materials[0]["name"]," resistivity [ohm*cm]: ","{:e}".format(rho_ohm_cm))

R_vertical = rho_ohm_cm*thickness_cm/area_cm2

print("2. b) ",materials[0]["name"]," resistance [ohm]: ","{:e}".format(R_vertical))

print("2. c) Because the electron mobility is about three times larger than the hole mobility for Si, or nine times larger for SiC")

"""
Exercise 3

A silicon PN junction at room temperature (300K) has a doping concentration of 1 x 10^18 cm-3 on the P-
side and 1 x 10^15cm-3 on the N-side.

"""

Na_cm3 = 1e15
Nd_cm3 = 1e18
k_J = 1.380649e-23

ni_cm3_Si = 1.09e10
ni_cm3_SiC = 1.55e-8


phi_Si = (k_J*300/q)*np.log(Na_cm3*Nd_cm3/(ni_cm3_Si**2))
phi_SiC = (k_J*300/q)*np.log(Na_cm3*Nd_cm3/(ni_cm3_SiC**2))

print("3. a) Si: ", phi_Si)
print("3. a) SiC: ", phi_SiC)

"""
Exercise 4:
For the same doping structure used in exercise 3 calculate for T=300K and no applied bias the following:
a) The total thickness of the depletion layer (see eq. 19-17 on p517 in Mohan)
b) The maximum electric field given by the formula from the slides
c) How would the results be affected qualitatively by adding a large reverse bias?
"""
epsilon_0 = 8.85e-14

W0_Si = np.sqrt(2*epsilon_0*materials[0]["epsilon"]*phi_Si*(Na_cm3+Nd_cm3)/(q*Na_cm3*Nd_cm3))
W0_SiC = np.sqrt(2*epsilon_0*materials[1]["epsilon"]*phi_SiC*(Na_cm3+Nd_cm3)/(q*Na_cm3*Nd_cm3))

print("4. a) Si: ", W0_Si)
print("4. a) SiC: ", W0_SiC)

Emax_Si = np.sqrt(2*phi_Si*(q*Na_cm3*Nd_cm3)/((Na_cm3+Nd_cm3)*epsilon_0*materials[0]["epsilon"]))
Emax_SiC = np.sqrt(2*phi_SiC*(q*Na_cm3*Nd_cm3)/((Na_cm3+Nd_cm3)*epsilon_0*materials[1]["epsilon"]))

print("4. b) Si: ", Emax_Si)
print("4. b) SiC: ", Emax_SiC)

Vbias = 200
Emax_Si = np.sqrt(2*(Vbias+phi_Si)*(q*Na_cm3*Nd_cm3)/((Na_cm3+Nd_cm3)*epsilon_0*materials[0]["epsilon"]))
Emax_SiC = np.sqrt(2*(Vbias+phi_SiC)*(q*Na_cm3*Nd_cm3)/((Na_cm3+Nd_cm3)*epsilon_0*materials[1]["epsilon"]))

print("4. c) Si: ", Emax_Si)
print("4. c) SiC: ", Emax_SiC)
print("4. c) The electric fields would be similar.")

V_Si = 0.5*(materials[0]["Ec_kV_cm"]**2)*(epsilon_0*materials[0]["epsilon"])/(Nd_cm3*q)
V_SiC = 0.5*(materials[1]["Ec_kV_cm"]**2)*(epsilon_0*materials[1]["epsilon"])/(Nd_cm3*q)

print("5. a) Si: ", V_Si)
print("5. a) SiC: ", V_SiC)
