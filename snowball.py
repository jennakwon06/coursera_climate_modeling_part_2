import numpy
import matplotlib.pyplot

#### Define Constants ####
albedoM = -0.01
albedoB = 2.8
epsilon = 1
sigma = 5.67E-8
LRange = [1150, 1350]
nIters = 100
albedo = 0.15 # initial guess 

#### Initialize Data Lists ####
x_list = []              
y_list = []

#### Begin the cooling sweep from the highest L value
L = LRange[1]
while L > LRange[0] - 1:
    # Loop to find new values of T and albedo until they converge.
    for _ in range(nIters):
        T = (L * (1 - albedo) / (4 * sigma * epsilon))**(0.25)
        albedo = T * albedoM + albedoB
        albedo = max(min(albedo, 0.65), 0.15)
        x_list.append(_)
        y_list.append(T)
    matplotlib.pyplot.plot(x_list, y_list)
    L = L - 10
    
#### Show Plot

matplotlib.pyplot.show()
