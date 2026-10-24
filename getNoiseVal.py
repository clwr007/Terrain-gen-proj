import numpy as np

width , depth  = 100, 100
scale = 16

gridWidth = width//scale +2
gridDepth = depth//scale +2

def generateControlgrid(w,d,scale,seed):
    gridWidth = w//scale +2
    gridDepth = d//scale +2
    
    rng = np.random.default_rng(seed) 
    cg = rng.random((gridDepth,gridWidth))

    return cg

def getNoiseVal(x, z, controlGrid, scale):
    cellX,cellZ = x//scale, z//scale
    fracX,fracZ = x/scale - cellX , z/scale- cellZ
    # Apply smoothstep
    smoothX = 3*(fracX**2) - 2*(fracX**3)
    smoothZ = 3*(fracZ**2) - 2*(fracZ**3)

    topLeft = controlGrid[cellZ,cellX]
    topRight = controlGrid[cellZ,cellX+1]
    bottomLeft = controlGrid[cellZ+1,cellX]
    bottomRight = controlGrid[cellZ+1,cellX+1]

    # interpolating horizontally and vertically
    top = topLeft + (topRight-topLeft)*smoothX
    bottom = bottomLeft + (bottomRight-bottomLeft)*smoothX
    noiseVal = top + (bottom-top)*smoothZ
    return noiseVal

