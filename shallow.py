import numpy
import matplotlib.pyplot as plt
import matplotlib.ticker as tkr
import math

# Grid and Variable Initialization
NCOL = 5
NROW = NCOL
nSlices = 400
ntAnim = 1000
horizontalWrap = False
interpolateRotation = True
rotationScheme = "PlusMinus"
plotOutput = True
arrowScale = 30

dT = 600                                # seconds
G = 9.8e-4                              # m/s2, hacked (low-G) to make it run faster
HBackground = 4000                      # meters
dX = 10.E3                              # meters, small enough to respond quickly.  This is a very small ocean
                                        # on a very small, low-G planet.  
dxDegrees = dX / 110.e3
flowConst = G                           # 1/s2
dragConst = 1.E-6                       # about 10 days decay time
meanLatitude = 30                       # degrees

windScheme =  "Curled"                  # "Curled", "Uniform"
initialPerturbation = ""                # "Tower", "NSGradient", "EWGradient"
textOutput = False

# Set up latitute, rotational constant, and wind schemes. 
latitude = []
rotConst = []
windU = []
for irow in range(0,NROW):
    if rotationScheme is "WithLatitude":
        latitude.append( meanLatitude + (irow - NROW/2) * dxDegrees )
        rotConst.append( -7.e-5 * math.sin(math.radians(latitude[-1]))) # s-1
    elif rotationScheme is "PlusMinus":
        rotConst.append( -3.5e-5 * (1. - 0.8 * ( irow - (NROW-1)/2 ) / NROW )) # rot 50% +-
    elif rotationScheme is "Uniform":
        rotConst.append( -3.5e-5 ) 
    else:
        rotConst.append( 0 )

    if windScheme is "Curled":
        windU.append( 1e-8 * math.sin( (irow+0.5)/NROW * 2 * 3.14 ) ) 
    elif windScheme is "Uniform":
        windU.append( 1.e-8 )
    else:
        windU.append( 0 )


itGlobal = 0                        # Global iteration constant 

# Initialize the matrices
U = numpy.zeros((NROW, NCOL+1))     # Velocity
V = numpy.zeros((NROW+1, NCOL))     # Velocity
H = numpy.zeros((NROW, NCOL+1))     # Elevation
dUdT = numpy.zeros((NROW, NCOL))    # Time Derivative
dVdT = numpy.zeros((NROW, NCOL))    # Time Derivative
dHdT = numpy.zeros((NROW, NCOL))    # Time Derivative
dHdX = numpy.zeros((NROW, NCOL+1))  # Spatial Derivative
dHdY = numpy.zeros((NROW, NCOL))    # Spatial Derivative
dUdX = numpy.zeros((NROW, NCOL))    # Spatial Derivative
dVdY = numpy.zeros((NROW, NCOL))    # Spatial Derivative
rotV = numpy.zeros((NROW,NCOL))     # interpolated to u locations
rotU = numpy.zeros((NROW,NCOL))     #              to v
    
midCell = int(NCOL/2)
if initialPerturbation is "Tower":
    H[midCell,midCell] = 1
elif initialPerturbation is "NSGradient":
    H[0:midCell,:] = 0.1
elif initialPerturbation is "EWGradient":
    H[:,0:midCell] = 0.1

"""
This is the work-horse subroutine.  
It steps forward in time, taking ntAnim steps of duration dT.  
"""

dY = dX
def animStep():    

    global stepDump, itGlobal
    # Time Loop
    for it in range(0,ntAnim):

        #   ----V(00)-------V(01)--------V(02)----
        #   |           |            |           |
        # U(00) H(00) U(01) H(01)  U(02) H(02) [U(03)]
        #   |           |            |           |
        #   ----V(10)-------V(11)--------V(12)----
        #   |           |            |           |
        # U(10) H(10) U(11) H(11)  U(12) H(12) [U(13)]
        #   |           |            |           |  
        #   ----V(20)-------V(21)--------V(22)----
        #   |           |            |           |
        # U(20) H(20) U(21) H(21)  U(22) H(22) [U(23)]
        #   |           |            |           |  
        #   ---[V(30)]-----[V(31)]------[V(32)]---

 
        ############ 1. Longitudinal Derivatives ############
        # Calculate dH/dX (variable dHdX), making sure to put the value in each
        # index [irow, icol] so that it applies to the horizontal velocity at
        # that index location (U[irow, icol]).
        #####################################################

        for irow in range(NROW):
            for icol in range(NCOL + 1):
                dHdX[irow, icol] = (H[irow, icol] - H[irow, icol - 1]) / dX

        for irow in range(NROW):
            for icol in range(NCOL):
                dUdX[irow, icol] = (U[irow, icol + 1] - U[irow, icol]) / dX

        ############ 2. Latitudinal Derivatives #############
        # Northern and southern boundaries of the domains are always walls.
        #####################################################
        for irow in range(1, NROW):
            for icol in range(NCOL):
                dHdY[irow, icol] = (H[irow, icol] - H[irow - 1, icol]) / dY
                dVdY[irow, icol] = (V[irow + 1, icol] - V[irow, icol]) / dY

        ################ 3. Rotational Terms ################
        # Simpler way for now..
        # Problem with the simpler way; : U and V values are not at the same places in the grid.
        #####################################################
        for irow in range(NROW):
            for icol in range(NCOL):
                rotU[irow, icol] = rotConst[irow] * U[irow, icol]
                rotV[irow, icol] = rotConst[irow] * V[irow, icol]

        ################# 4. Time Directives ################
        # dU/dT = C_rotation * V - C_flow * dH/dX - C_drag * U + C_wind
        # dV/dT = - C_rotation * U - C_flow * dH/dY - C_drag * V
        # dH/dT = - ( dU/dX + dV/dY ) * Hbackground / dX
        #####################################################
        for irow in range(NROW):
            for icol in range(NCOL):
                dUdT[irow, icol] = rotV[irow, icol] - (flowConst * dHdX[irow, icol]) - (dragConst * U[irow, icol]) + windU[irow]
                dVdT[irow, icol] = - rotU[irow, icol] - (flowConst * dHdY[irow, icol]) - (dragConst * V[irow, icol])
                dHdT[irow, icol] = - (dUdX[irow, icol] + dVdY[irow, icol]) * (HBackground / dX)

        ############# 5. Stepping Forward In Time ###########
        # Update each variable U, V, and H by adding the time derivative multipled by the time step.
        # U(time+1) = U(time) + dU/dT * delta_t
        #####################################################
        U[:, 0:NCOL] = U[:, 0:NCOL] + dUdT[:, :] * dT
        V[0:NROW, :] = V[0:NROW, :] + dVdT[:, :] * dT
        H[:, 0:NCOL] = H[:, 0:NCOL] + dHdT[:, :] * dT

        ############### 6. Maintain Ghost Cells #############
        #####################################################
        # Velocity at the north wall should be zeroed
        V[0, :] = 0
        V[NROW, :] = 0

        if horizontalWrap:
            U[:, NCOL] = U[:, 0]
            H[:, NCOL] = H[:, 0]
        else:
            # U = zero at the eastern and western boundaries (indices [:,0] and [:,ncol]).
            U[:, 0] = 0
            U[:, NCOL] = 0

    itGlobal = itGlobal + ntAnim

def firstFrame():
    global fig, ax, hPlot
    fig, ax = plt.subplots()
    ax.set_title("H")   
    hh = H[:,0:NCOL]
    loc = tkr.IndexLocator(base=1, offset=1)
    ax.xaxis.set_major_locator(loc)
    ax.yaxis.set_major_locator(loc)
    grid = ax.grid(which='major', axis='both', linestyle='-')
    hPlot = ax.imshow(hh, interpolation='nearest', clim=(-0.5,0.5))   
    plotArrows()
    plt.show(block=False) 

def plotArrows():
    global quiv, quiv2
    xx = []
    yy = []
    uu = []
    vv = []
    for irow in range( 0, NROW ):
        for icol in range( 0, NCOL ):
            xx.append(icol - 0.5)
            yy.append(irow )
            uu.append( U[irow,icol] * arrowScale )
            vv.append( 0 )
    quiv = ax.quiver( xx, yy, uu, vv, color='white', scale=1)
    for irow in range( 0, NROW ):
        for icol in range( 0, NCOL ):
            xx.append(icol)
            yy.append(irow - 0.5)
            uu.append( 0 )
            vv.append( -V[irow,icol] * arrowScale )
    quiv2 = ax.quiver( xx, yy, uu, vv, color='white', scale=1)

def updateFrame():
    global fig, ax, hPlot, quiv, quiv2
    hh = H[:,0:NCOL]
    hPlot.set_array(hh)
    quiv.remove()    
    quiv2.remove()
    plotArrows()
    plt.pause(0.001)
    fig.canvas.draw()
    print("Time: ", math.floor( itGlobal * dT / 86400.*10)/10, "days")

def textDump():
    print("time step ", itGlobal)    
    print("H", H)
    print("dHdX" )
    print( dHdX)
    print("dHdY" )
    print( dHdY)
    print("U" )
    print( U)
    print("dUdX" )
    print( dUdX)
    print("rotV" )
    print( rotV)
    print("V" )
    print( V)
    print("dVdY" )
    print( dVdY)
    print("rotU" )
    print( rotU)
    print("dHdT" )
    print( dHdT)
    print("dUdT" )
    print( dUdT)
    print("dVdT" )
    print( dVdT)

if textOutput is True:
    textDump()
if plotOutput is True:
    firstFrame()
for i_anim_step in range(0,nSlices):
    animStep()
    if textOutput is True:
        textDump()
    if plotOutput is True:
        updateFrame()