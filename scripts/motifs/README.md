# Research motifs

The motifs on `/research/` are drawn from real 3D models rather than sketched
by hand. A mesh is loaded, decimated, and projected through a real camera;
hidden surfaces are removed by depth sorting and the silhouette is emitted as
hairline SVG in the site's palette.

The output is static SVG using the site's CSS variables, so the motifs cost
nothing at runtime: no WebGL, no client JavaScript, and no runtime dependency.

## Sources

Meshes come from [Poly Haven](https://polyhaven.com), which publishes
everything as **CC0**, and from the
[Khronos glTF sample assets](https://github.com/KhronosGroup/glTF-Sample-Assets).
Everything used here is CC0: no attribution is required and there are no
licence conditions on the derived artwork.

| Motif | Subject | Source |
| --- | --- | --- |
| Current research | Round cake with a slice cut | built in `motif3d.cake_sector` |
| Thesis | Car | Khronos `ToyCar`, **CC0** |
| Prosthetic arm | Wine bottle | Poly Haven `wine_bottles_01`, **CC0** |

The cake is built rather than downloaded. A cake is a cylinder, so the exact
geometry gives perfectly flat cut faces; slicing a scanned model left a ragged
notch and a cap spanning the whole diameter.

The Khronos glTF sample assets mix CC0 and CC-BY. `ToyCar` is CC0; check any
other model's README before using it, since CC-BY would put an attribution
obligation on the site.

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
