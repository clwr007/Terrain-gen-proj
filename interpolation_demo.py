import numpy as np 
width , depth  = 100, 100
scale = 25

gridWidth = width//scale +2
gridDepth = depth//scale +2

rng = np.random.default_rng(12345) #our seed can be 12345
controlGrid = rng.random((gridDepth,gridWidth))
# print(controlGrid)
# print(controlGrid.shape)

x,z = 30,40
cellX,cellZ = x//scale, z//scale
fracX,fracZ = x/scale - cellX , z/scale- cellZ
# print(cellX,cellZ)
# print(fracX,fracZ) 

# to find: 4 corners
topLeft = controlGrid[cellZ,cellX]
topRight = controlGrid[cellZ,cellX+1]
bottomLeft = controlGrid[cellZ+1,cellX]
bottomRight = controlGrid[cellZ+1,cellX+1]
# print(topLeft,topRight)
# print(bottomLeft,bottomRight)

"""
Suppose two neighboring control points have values a and b. If we're a fraction t of the way from a to b, linear interpolation gives:
    L(a,b,t)=a+(b-a)t
if a = 0.2, b = 0.8, and t = 0.25, then:
    L=0.2+(0.8-0.2)(0.25)=0.35
"""

top = topLeft + (topRight-topLeft)*fracX
bottom = bottomLeft + (bottomRight-bottomLeft)*fracX
# print(top,bottom)
# interpolating vertically:
noiseVal = top + (bottom-top)*fracZ
# print(noiseVal)

"""
problem: slope can change abruptly at the boundaries of cells
solution: 'SmoothStep'

The standard cubic smoothstep function that does this is: 
    s(t)=3t^2-2t^3
"""

smoothX = 3*(fracX**2) - 2*(fracX**3)
smoothZ = 3*(fracZ**2) - 2*(fracZ**3)

top = topLeft + (topRight-topLeft)*smoothX
bottom = bottomLeft + (bottomRight-bottomLeft)*smoothX
# print(top,bottom)
noiseVal = top + (bottom-top)*smoothZ
# print(noiseVal)
