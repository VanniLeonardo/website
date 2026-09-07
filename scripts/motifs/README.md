# Research motifs

The motifs on `/research/` are drawn from real 3D models rather than sketched
by hand. A mesh is loaded, decimated, and projected through a real camera;
hidden surfaces are removed by depth sorting and the silhouette is emitted as
hairline SVG in the site's palette.

The output is static SVG using the site's CSS variables, so the motifs cost
nothing at runtime: no WebGL, no client JavaScript, and no runtime dependency.

## Sources

Meshes come from [Poly Haven](https://polyhaven.com), which publishes
everything as **CC0**: no attribution is required and there are no licence
conditions on the derived artwork.

| Motif | Model | Slug |
| --- | --- | --- |
| Current research | Avocado | `food_avocado_01` |
| Thesis | Lemon | `lemon` |
| Prosthetic arm | Wine bottle | `wine_bottles_01` |

Only the `.gltf` and its `.bin` are downloaded; textures are skipped, since
only the geometry is used. Models are cached in `cache/` and not committed.

## Regenerating

Needs a Python environment; it is not part of the Node build.

```bash
python3 -m venv .venv && .venv/bin/pip install -r scripts/motifs/requirements.txt
.venv/bin/python scripts/motifs/motifs.py
```

`npm run motifs` runs the same script with the system `python3`, which works
if the dependencies are installed there.

## Files

- `fetch.py` downloads and caches models
- `models.py` isolates, decimates and slices meshes, and simplifies polylines
- `motif3d.py` mesh primitives, camera, projection
- `geom.py` silhouette extraction and transforms
- `render.py` scene assembly, depth ordering, SVG output
- `motifs.py` the three scenes
