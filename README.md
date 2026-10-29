# Procedural Terrain generation tool inspired by Minecraft

## What is Procedural Terrain generation?
Procedural terrain generation is a method where algorithms create data algorithmically rather than manually.
Instead of a level designer hand crafting every hill, rock, and valley, a computer program uses mathematical formulas,
pseudo-random noise (such as Perlin noise or Simplex noise), and predefined rules to generate landscapes on the fly.

This approach allows developers to create massive, infinite, or uniquely varied worlds without needing hundreds of gigabytes of storage or years of manual sculpting.

## Where has it been used before?
Some notable examples may include:
| Minecraft | Terraria |
|:---:|:---:|
| <img src="https://github.com/user-attachments/assets/bb23970c-ab3c-4b7e-ab84-ba1a46b7e08a" width="300" alt="Minecraft terrain" /> | <img src="https://github.com/user-attachments/assets/da47fec9-297b-47f5-a679-d4ec9289cf32" width="300" alt="Terraria terrain" /> |
| **No Man's Sky** | **Valheim** |
| <img src="https://github.com/user-attachments/assets/d90e53b8-0b30-4663-bbe9-b4091b6e706a" width="300" alt="No Man's Sky landscape" /> | <img src="https://github.com/user-attachments/assets/2c554a72-626e-4376-97fc-2eaf6a28d2aa" width="300" alt="Valheim landscape" /> |


## The Idea behind Minecraft's Terrain Generation

The challenge is to generate terrain that is random enough to be varied, but structured enough to look natural.

One way to approach this is through noise functions. Unlike ordinary randomness, which produces unrelated values, noise functions generate values that vary smoothly across space.
This creates patterns that can form the basis of hills, plains, valleys, and mountain ranges

<img width="750" height="300" alt="image" src="https://github.com/user-attachments/assets/b66c1e49-57db-4a8c-b795-e84e8bb934ad" />

*(image taken from Henrik Kniberg's video) [1]*

A 2D noise function takes a position on a plane, represented by coordinates (x,z), and returns a value.
Because nearby positions tend to have similar values, the output forms a continuous-looking pattern rather than a collection of unrelated random numbers.
At each horizontal coordinate (x,z), the noise determines a height (y).
Applying this across the map produces a Heightmap.

## Terrain Shaping concept

Minecraft's terrain generation combines multiple noise-based signals to influence the landscape.
Three important Noise fields are Continentalness, Erosion, and Peaks & Valleys.

<img width="765" height="180" alt="image" src="https://github.com/user-attachments/assets/f06a719a-7b1a-4b45-af1a-fe2386ef7c61" />

*(image taken from Henrik Kniberg's video) [1]*

- **Continentalness** — helps shape the transition between oceans, coastlines, and inland terrain.
- **Erosion** — influences whether terrain tends toward flatter regions or more rugged landscapes.
- **Peaks & Valleys** — helps determine the character of the terrain, from valleys to prominent peaks.

These fields don't work as isolated terrain generators. Their interactions help determine what kind of landscape emerges at each location.

## Status
Work in progress.
The current output is an early version, not the final result.
Next steps: more noise layers (octaves) for finer detail, smoother coastlines, and more varied splines.

## My Approach
Rather than trying to recreate all of Minecraft's world-generation system at once, I'm starting with the underlying concepts:
generating smooth noise fields, studying their patterns, and combining them into a three-dimensional heightmap.

The current implementation uses smooth value noise, generated from randomized control grids and interpolation.
Separate fields represent continentalness, erosion, and peaks and valleys, each with its own scale and seed.

This is an experimental starting point, not a reproduction of Minecraft's actual terrain-generation algorithm.

### The Current Pipeline
1. Generate independent noise fields at different spatial scales.
2. Interpolate between control-grid values to create smooth variation.
3. Combine the fields into a terrain heightmap.
4. Visualize the resulting landscape in three dimensions.
5. Experiment with the parameters and relationships to produce more convincing landforms.

## Built With
- Python
- NumPy
- Matplotlib
- PyVista

## References
- [1] Henrik Kniberg — [How Minecraft Generates Terrain](https://youtu.be/CSa5O6knuwI)

