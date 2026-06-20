import pandas as pd
from scipy.stats import linregress
from scipy.stats import beta

import matplotlib.pyplot as plt
import numpy as np

def median_ranks(n, P=0.5):
    return np.array([beta.ppf(P, j, n - j + 1) for j in range(1, n + 1)])



data = [[5,6,11,13,13,16,20,22,22,26,32,35,36,37,37,40],
        [15,22,22,25,30,31,33,34,34,36,36,37,37,37,39,40],
        [34,34,34,34,35,35,35,35,37,37,38,38,38,39,40,40]]

n = len(data[0])

F = median_ranks(n, 0.5)
y = np.log(-np.log(1-F))

x1 = np.log(data[0])
x2 = np.log(data[1])
x3 = np.log(data[2])


fc1 = pd.DataFrame({
    "x": x1,
    "y": y
})

fc2 = pd.DataFrame({
    "x": x2,
    "y": y
})

fc3 = pd.DataFrame({
    "x": x3,
    "y": y
})

dfs = [fc1, fc2, fc3]

print("-"*50)
print("PART 1")
print("-"*50)
print('\n')

for df in dfs:
    plt.plot(df["x"], df["y"])
    
    result = linregress(df["x"], df["y"])
    print(f"Slope: {result.slope}")
    print(f"Intercept: {result.intercept}")
    print(f"R2: {result.rvalue**2:.3f}")

    plt.plot(df["x"], result.slope*df["x"]+result.intercept)

    beta_ = result.slope
    eta = np.exp(-result.intercept/beta_)
    print(f"Beta: {beta_}")
    print(f"Eta: {eta}")

    B1 = 0.99
    B10 = 0.9
    lifeB1 = eta*((-np.log(B1))**(1/beta_)) 
    lifeB10 = eta*((-np.log(B10))**(1/beta_)) 

    print(f"B1 lifetime: {lifeB1}")
    print(f"B10 lifetime: {lifeB10}")
    print("-"*50)
    print('\n')

plt.show()
plt.close()


print("-"*50)
print("PART 2")
print("-"*50)
print('\n')

data2 = {
    4: [1850.00, 1890.00, 1903.00, 1905.00, 1940.00, 2001.00, 2005.00, 2030.00, 2031.00, 2035.00, 2050.00, 2125.00, 2155.00, 2170.00, 2220.00],
    5: [31.00, 34.60, 35.00, 35.00, 35.00, 35.10, 36.00, 37.00, 37.00, 37.60, 38.10, 38.50, 38.70, 40.00, 41.00],
    5.5: [4.60, 4.70, 4.80, 4.80, 4.80, 5.00, 5.00, 5.00, 5.10, 5.10, 5.10, 5.30, 5.40, 5.40, 5.55],
    6: [0.30, 0.35, 0.38, 0.45, 0.52, 0.58, 0.60, 0.69, 0.69, 0.72, 0.75, 0.80, 0.90, 1.15, 1.20]
}

n = len(data2[4])
F90 = median_ranks(n, 0.9)
y90 = np.log(-np.log(1-F90))

F50 = median_ranks(n, 0.5)
y50 = np.log(-np.log(1-F50))

B001_90 = []
B1_50 = []


for v in data2:
    result90 = linregress(np.log(data2[v]), y90)
    plt.plot(np.log(data2[v]), y90)
    print(f"Slope 90: {result90.slope}")
    print(f"Intercept 90: {result90.intercept}")
    print(f"R2 90: {result90.rvalue**2:.3f}")
    plt.plot(np.log(data2[v]), np.log(data2[v])*result90.slope+result90.intercept)

    beta90 = result90.slope
    eta90 = np.exp(-result90.intercept/beta90)
    print(f"Beta 90: {beta90}")
    print(f"Eta 90: {eta90}")
    B001 = 0.9999
    lifeB001 = eta90*((-np.log(B001))**(1/beta90)) 
    B001_90.append(lifeB001)

    print(f"B0.01 lifetime: {lifeB001}")
    print("-"*50)
    print('\n')



    result50 = linregress(np.log(data2[v]), y50)
    plt.plot(np.log(data2[v]), y50)
    print(f"Slope 50: {result50.slope}")
    print(f"Intercept 50: {result50.intercept}")
    print(f"R2 50: {result50.rvalue**2:.3f}")
    plt.plot(np.log(data2[v]), np.log(data2[v])*result50.slope+result50.intercept)

    beta50 = result50.slope
    eta50 = np.exp(-result50.intercept/beta50)
    print(f"Beta 50: {beta50}")
    print(f"Eta 50: {eta50}")
    B1 = 0.99
    lifeB1 = eta50*((-np.log(B1))**(1/beta50)) 
    B1_50.append(lifeB1)

    print(f"B1 lifetime: {lifeB1}")
    print("-"*50)
    print('\n')


plt.show()
plt.close()

fit1 = linregress(np.log(list(data2.keys()))[:-1], np.log(B001_90)[:-1]) # 6V seems off, probably different failure mechanism
print("-"*50)
print('\n')
print(f"Slope B0.01 90%: {fit1.slope}")
print(f"Intercept B0.01 90%: {fit1.intercept}")
print(f"R2 B0.01 90%: {fit1.rvalue**2:.3f}")

plt.plot(np.log(list(data2.keys())), np.log(B001_90))
plt.plot(np.log(list(data2.keys())), np.log(list(data2.keys()))*fit1.slope+fit1.intercept)


fit2 = linregress(np.log(list(data2.keys()))[:-1], np.log(B1_50)[:-1])
print("-"*50)
print('\n')
print(f"Slope B1 50%: {fit2.slope}")
print(f"Intercept B1 50%: {fit2.intercept}")
print(f"R2 B1 50%: {fit2.rvalue**2:.3f}")

plt.plot(np.log(list(data2.keys())), np.log(B1_50))
plt.plot(np.log(list(data2.keys())), np.log(list(data2.keys()))*fit2.slope+fit2.intercept)

plt.show()
plt.close()

print("-"*50)
print('\n')
life_3V = np.exp(fit1.slope*np.log(3)+ fit1.intercept)
print(f"Estimated B0.01 lifetime with 90% confidence at 3V: {life_3V}")
