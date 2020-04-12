import numpy
import matplotlib.pyplot

### Define constants 
nX = 10                             # number of grid points
domainWidth = 1e6                   # meters
dX = domainWidth / nX               # meters
timeStep = 160                      # years
nYears = 25000                      # years
flowParam = 1e4                     # m horizontal / yr
snowFall = 1                        # m / y
plotLimit = 10000                   # meters

### Initialize the elevations and flows
elevations = numpy.zeros(nX+2)
flows = numpy.zeros(nX+1)

### Set up plotting
fig, ax = matplotlib.pyplot.subplots()
ax.plot(elevations)
ax.set_ylim([0,plotLimit])
matplotlib.pyplot.show(block=False)


### Create a time loop which first calculates flows 
# (by looping over the horizontal grid points, using the current values of the elevations), 
# then takes a time step for the elevations (looping over the horizontal grid again).
currentYear = 0
while currentYear <= nYears:
    for ix in range(0, nX + 1):
        flows[ix] = ( elevations[ix] - elevations[ix+1] ) / dX * flowParam  * \
            ( elevations[ix] + elevations[ix+1] ) / 2 / dX

    for ix in range(1, nX + 1):
        elevations[ix] += ( snowFall + flows[ix-1] - flows[ix] ) * timeStep

    print("{} {}".format(currentYear, elevations[5]))
    currentYear += timeStep 
    ax.clear()
    ax.plot( elevations )
    ax.set_ylim([0,plotLimit])
    matplotlib.pyplot.show( block=False )
    matplotlib.pyplot.pause(0.001)
    fig.canvas.draw()
