import numpy as np
import matplotlib.pyplot as plt
import pyvista as pv
from getNoiseVal import getNoiseVal, generateControlgrid


width, depth = 500,500
cCell, eCell, pvCell = 150, 120, 40

seed = 69420

# Cg => continental control grid
# Eg => erosion control grid
# PVg => Peaks and Valleys control grid

Cg1 = generateControlgrid(width, depth, cCell, seed)
Cg2 = generateControlgrid(width, depth, cCell//2, seed+2)
Cg3 = generateControlgrid(width, depth, cCell//4, seed+3)

Eg1 = generateControlgrid(width, depth, eCell, seed+10)
Eg2 = generateControlgrid(width, depth, eCell//2, seed+11)
Eg3 = generateControlgrid(width, depth, eCell//4, seed+12)

PVg1 = generateControlgrid(width, depth, pvCell, seed+20)
PVg2 = generateControlgrid(width, depth, pvCell//2, seed+21)
PVg3 = generateControlgrid(width, depth, pvCell//4, seed+22)

Cnf1 = np.zeros((depth, width))
Cnf2 = np.zeros((depth, width))
Cnf3 = np.zeros((depth, width))

Enf1 = np.zeros((depth, width))
Enf2 = np.zeros((depth, width))
Enf3 = np.zeros((depth, width))

PVnf1 = np.zeros((depth, width))
PVnf2 = np.zeros((depth, width))
PVnf3 = np.zeros((depth, width))

for z in range(depth):
    for x in range(width):
        Cnf1[z, x] = getNoiseVal(x, z, Cg1, cCell)
        Cnf2[z, x] = getNoiseVal(x, z, Cg2, cCell//2)
        Cnf3[z, x] = getNoiseVal(x, z, Cg3, cCell//4)

        Enf1[z, x] = getNoiseVal(x, z, Eg1, eCell)
        Enf2[z, x] = getNoiseVal(x, z, Eg2, eCell//2)
        Enf3[z, x] = getNoiseVal(x, z, Eg3, eCell//4)

        PVnf1[z, x] = getNoiseVal(x, z, PVg1, pvCell)
        PVnf2[z, x] = getNoiseVal(x, z, PVg2, pvCell//2)
        PVnf3[z, x] = getNoiseVal(x, z, PVg3, pvCell//4)


Cfinal = (1.0*(Cnf1)+ 0.5*(Cnf2) + 0.25*(Cnf3))/1.75
Efinal = (1.0*(Enf1)+ 0.5*(Enf2) + 0.25*(Enf3))/1.75
PVfinal = (1.0*(PVnf1)+ 0.5*(PVnf2) + 0.25*(PVnf3))/1.75

fig, axes = plt.subplots(1, 3, figsize=(15, 5))

axes[0].imshow(Cfinal, cmap="gray", origin="lower")
axes[0].set_title("Continentalness")

axes[1].imshow(Efinal, cmap="gray", origin="lower")
axes[1].set_title("Erosion")

axes[2].imshow(PVfinal, cmap="gray", origin="lower")
axes[2].set_title("Peaks & Valleys")

plt.tight_layout()
plt.show()

seaLevel = 0
pvStrength = 10

cHeight = np.interp(Cfinal, [0.0, 0.35, 0.45, 0.55, 0.8, 1.0], [-40, -30, -2, 8, 12, 40]) + seaLevel
ruggedness = np.interp(Efinal, [0, 0.4, 0.6, 1], [1.0, 0.7, 0.05, 0.0])
pvShape = 1 - np.abs(2*PVfinal - 1)

heightField = (
    cHeight+ (pvShape*pvStrength*ruggedness)
)

dx = np.abs(np.diff(heightField, axis=1))
dy = np.abs(np.diff(heightField, axis=0))

X, Z = np.meshgrid(np.arange(width), np.arange(depth))

grid = pv.StructuredGrid(X, Z, heightField)
grid["height"] = heightField.ravel(order="F")

plotter = pv.Plotter()
plotter.add_mesh(grid, scalars="height", cmap="terrain", smooth_shading=True)

water = pv.Plane(center=(width / 2, depth / 2, seaLevel),direction=(0, 0, 1),i_size=width, j_size=depth)
plotter.add_mesh(water, color="royalblue", opacity=0.6)

# vertical exaggeration, tweak to taste
plotter.set_scale(zscale=2)  
plotter.show(screenshot=f"terrain_seed_{seed}.png")

print("seed:", seed, "| C grid first values:", Cnf1[0, :3])
print(Cfinal.min(), Cfinal.max())