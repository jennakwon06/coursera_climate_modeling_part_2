## Shallow Water Equations
- Doesnt' mean the water is shallow!
- There's water flow in the model, driven by differences in the elevation of the water surface, which arise from the flow itself. 
- The flow is also altered by rotation (as on a rotating planet), potentially by wind, and by friction. 
- The water is assumed to be homogeneous in the vertical, no differences in temperature, density, or velocity are tracked.
- Because of the vertical homogeneity, these are called the "shallow water equations".
- A similar formulation can be used to model flows in the atmosphere, with the same assumption that the fluid "piles up" in some places, generating differences in pressure at the base of the fluid which drive fluid flow.

## Initial Condition
- In its simplest configuration, this model can start with an initial "hill" of high water level in the center of the computational grid. Water starts to flow outward from the hill, but it rotates to the side, and so tends to find a pattern where the flow is going around and around the hill, rather than simply flowing straight down as it would if there were no rotation.

## Problem Simplification
- low gravity, which slows down the waves and allows a longer time step
- a small ocean with grid cells that are not too large, so that the amount of water in them can change quickly
- a much steeper change in rotation rate with latitude, as if the ocean was on a very small planet.

## Grid
- Latitute
- Longitude

## Variables
- Cell center: Elevation of water level height which is defined in the cell center
- Between cells: Flows between the cells

## Boundaries
- North and south boundaries: Let's say there are walls (val = 0)
- Horizontal: You can either put the walls (val = 0), or wrap around

## Calculating the evolution of the elevation
- Track the flows coming in and going out of the boundaries
- dh/dt = (du/dx + dv/dy) * (dh/dx)
    - du/dx : velocity
    - dh/dx = aspect ratio


# Initialize the matrices
U = numpy.zeros((NROW, NCOL+1))    # Velocity
V = numpy.zeros((NROW+1, NCOL))    # Velocity
H = numpy.zeros((NROW, NCOL+1))    # Elevation
dUdT = numpy.zeros((NROW, NCOL))   # Time Derivative
dVdT = numpy.zeros((NROW, NCOL))   # Time Derivative
dHdT = numpy.zeros((NROW, NCOL))   # Time Derivative
dHdX = numpy.zeros((NROW, NCOL+1)) # Spatial Derivative
dHdY = numpy.zeros((NROW, NCOL))   # Spatial Derivative
dUdX = numpy.zeros((NROW, NCOL))   # Spatial Derivative
dVdY = numpy.zeros((NROW, NCOL))   # Spatial Derivative
rotV = numpy.zeros((NROW,NCOL))    # interpolated to u locations
rotU = numpy.zeros((NROW,NCOL))    #              to v

## Python vs. Fortran
- Fortran code would be capable of much higher resolution (more grid points) than the Python version could handle in a reasonable amount of computer time. 
- Plotting an animation in Fortran is not built-in or convenient in a code that might take a long time to run (like a climate model), so the usual strategy would be to save data files periodically from the running Fortran, then use some other software to read those data files and make a plot or movie (this is called "post processing").


## The Grid

Variables that are enclosed with square brackets in this diagram are "ghost" variables. They aren't computed as part of the real grid, but are used to make it simpler to calculate differences, say between the North/South velocities (V) at the top and the bottom of each cell.

V: longitudinal
U: latitudinal

```

  ----V(00)-------V(01)--------V(02)----
  |           |            |           |
U(00) H(00) U(01) H(01)  U(02) H(02) [U(03)]
  |           |            |           |
  ----V(10)-------V(11)--------V(12)----
  |           |            |           |
U(10) H(10) U(11) H(11)  U(12) H(12) [U(13)]
  |           |            |           |  
  ----V(20)-------V(21)--------V(22)----
  |           |            |           |
U(20) H(20) U(21) H(21)  U(22) H(22) [U(23)]
  |           |            |           |  
  ---[V(30)]-----[V(31)]------[V(32)]---
```

## The Differential Equation

```
dU/dT = C_rotation * V - C_flow * dH/dX - C_drag * U + C_wind

dV/dT = - C_rotation * U - C_flow * dH/dY - C_drag * V

dH/dT = - ( dU/dX + dV/dY ) * Hbackground / dX

```

- C_ terms : Constants
	- Note: C_rotation term transfers energy between the U and V velocities. 
	- C_rotation; higher # means faster, and sign determines the direction of rotation. 
- dV/dY, dH/dX : Spatial derivatives;  how much the velocity (V) changes with latitude (y), for example. 
- dU/dT, dV/dT, dH/dT:  Used to update the values according to;
	- U(time+1) = U(time) + dU/dT * delta_t
	- where delta_t is a time step.

- dU/dT equation
	- list of things that change longitudinal velocity with time
	- Rotation changes the flow direction, moving the velocity between the U and V directions according to the rotational constant, C_rotation
	- dH/dX tells whether the surface is sloping. If it is, then it drives the flow to accelerate according to a flow constant C_Flow. 
	- Drag slows the flow down; the larger the flow (U), the faster the slowdown (dU/dT). 
	- Allow the wind to blow in an East/West direction, driving circulation.

## Mapping the Equations Numerically onto the Grid
- Differential equations apply to a continuous fluid
- Numerically - we cast equations to a coarser systems of boxes
- We derive pressure driver from differences of heights between adjacent boxes
- H (slope in the sea surface), appropriate to U(01), would span H(01) - H(00), divided by the grid spacing delta_x.