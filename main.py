import numpy as np
import matplotlib.pyplot as plt
import pyvista as pv
from getNoiseVal import getNoiseVal, generateControlgrid


width, depth = 500,500
cCell, eCell, pvCell = 150, 120, 40

seed = 676767
continentalGrid = generateControlgrid(width, depth, cCell, seed)
erosionGrid = generateControlgrid(width, depth, eCell, seed+1)
pvGrid = generateControlgrid(width, depth, pvCell, seed+2)

CnoiseField = np.zeros((depth, width))
EnoiseField = np.zeros((depth, width))
PVnoiseField = np.zeros((depth, width))

for z in range(depth):
    for x in range(width):
        CnoiseField[z, x] = getNoiseVal(x, z, continentalGrid, cCell)
        EnoiseField[z, x] = getNoiseVal(x, z, erosionGrid, eCell)
        PVnoiseField[z, x] = getNoiseVal(x, z, pvGrid, pvCell)


fig, axes = plt.subplots(1, 3, figsize=(15, 5))

axes[0].imshow(CnoiseField, cmap="gray", origin="lower")
axes[0].set_title("Continentalness")

axes[1].imshow(EnoiseField, cmap="gray", origin="lower")
axes[1].set_title("Erosion")

axes[2].imshow(PVnoiseField, cmap="gray", origin="lower")
axes[2].set_title("Peaks & Valleys")

plt.tight_layout()
plt.show()


seaLevel = 0
pvStrength = 10

cHeight = np.interp(CnoiseField, [0.0, 0.35, 0.45, 0.55, 0.8, 1.0], [-40, -30, -2, 8, 12, 40]) + seaLevel
ruggedness = np.interp(EnoiseField, [0, 0.4, 0.6, 1], [1.0, 0.7, 0.05, 0.0])
pvShape = 1 - np.abs(2*PVnoiseField - 1)

heightField = (
    cHeight+ (pvShape*pvStrength*ruggedness)
)

dx = np.abs(np.diff(heightField, axis=1))
dy = np.abs(np.diff(heightField, axis=0))
# print("mean |slope| x:", dx.mean(), " z:", dy.mean())
# print("% x-steps > 3:", (dx > 3).mean() * 100)
Ecrop = EnoiseField[:, :-1]
# print("slope where E>0.65:", dx[Ecrop > 0.65].mean())
# print("slope where E<0.35:", dx[Ecrop < 0.35].mean())
# print("count E>0.65:", (Ecrop > 0.65).sum(), " count E<0.35:", (Ecrop < 0.35).sum())

# fig = plt.figure(figsize=(10, 7))
# ax = fig.add_subplot(111, projection="3d")

# x = np.arange(width)
# z = np.arange(depth)
# X, Z = np.meshgrid(x, z)

# ax.plot_surface(X, Z, heightField, cmap="terrain", rstride=4, cstride=4)

# ax.set_title("Procedural Terrain - C, E and PV")
# ax.set_xlabel("X")
# ax.set_ylabel("Z")
# ax.set_zlabel("Height")
# ax.set_box_aspect((1, 1, 0.25))

# fig.savefig("terrain.png", dpi=150)
# plt.show()
X, Z = np.meshgrid(np.arange(width), np.arange(depth))

grid = pv.StructuredGrid(X, Z, heightField)
grid["height"] = heightField.ravel(order="F")

plotter = pv.Plotter()
plotter.add_mesh(grid, scalars="height", cmap="terrain", smooth_shading=True)

water = pv.Plane(center=(width / 2, depth / 2, seaLevel),direction=(0, 0, 1),i_size=width, j_size=depth)
plotter.add_mesh(water, color="royalblue", opacity=0.6)

plotter.set_scale(zscale=2)   # vertical exaggeration, tweak to taste
plotter.show(screenshot=f"terrain_seed_{seed}.png")

# print("Minimum height:", np.min(heightField))
# print("Maximum height:", np.max(heightField))

# print("C range:", CnoiseField.min(), CnoiseField.max())
# print("E range:", EnoiseField.min(), EnoiseField.max())
# print("PV range:", PVnoiseField.min(), PVnoiseField.max())


print("seed:", seed, "| C grid first values:", continentalGrid[0, :3])