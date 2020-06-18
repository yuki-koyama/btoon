# BToon

Blender addon for toon rendering.

## Contour Rendering

### Approach 1: Mesh Displacement and Culling

![](./docs/contour-before.png)
![](./docs/contour-after.png)

#### Description

This is a mesh-based technique to rendering contours, where meshes are duplicated, flipped, and then displaced outside.

- Pros
  - Thickness can be controlled using textures
  - Contours can be displaced in the viewport
  - The result can be easily reproduced in other real-time rendering environment such as Unity.
  - ...
- Cons
  - This technique is not compatible with Cycles
  - Ridges, valleys, and suggestive contours are not supported.
  - ...

#### Usage

- Select target objects
- `3D Viewport` > `Object` > `BToon Utilities` > `Set Contours`

#### Implementation

- It applies `Solidify` and `Displace` modifiers to the selected objects.
- An emission-based material with backface culling enabled is created and set to contours.

### Future Work

- Utilities for composition-based contour rendering
- Utilities for FreeStyle-based contour rendering

## How to Install

(TODO)
