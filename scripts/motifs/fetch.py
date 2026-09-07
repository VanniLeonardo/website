"""
Fetch source meshes from Poly Haven, which publishes everything as CC0.

Only the .gltf and its .bin are downloaded; the textures are skipped, since
the motifs use geometry alone. Models are cached outside the repository build
output and are not committed: the committed artefact is the generated SVG.
"""
import json
import pathlib
import urllib.request

API = 'https://api.polyhaven.com/files/{slug}'
CACHE = pathlib.Path(__file__).resolve().parent / 'cache'


# The asset CDN rejects requests without a User-Agent.
UA = {'User-Agent': 'leonardovanni.com motif generator (static site build)'}


def _open(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60)


def _get(url, dest):
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        return dest
    with _open(url) as r:
        dest.write_bytes(r.read())
    return dest


def fetch(slug, res='2k'):
    """Download one Poly Haven model and return the path to its .gltf."""
    out = CACHE / slug
    gltf_path = out / f'{slug}_{res}.gltf'
    if gltf_path.exists():
        return gltf_path

    with _open(API.format(slug=slug)) as r:
        files = json.load(r)
    entry = files['gltf'][res]['gltf']
    _get(entry['url'], gltf_path)

    # The .bin holds the geometry; textures are not needed for line art.
    for name, meta in entry.get('include', {}).items():
        if name.endswith('.bin'):
            _get(meta['url'], out / name)
    return gltf_path


KHRONOS = ('https://raw.githubusercontent.com/KhronosGroup/glTF-Sample-Assets/'
           'main/Models/{name}/glTF-Binary/{name}.glb')


def fetch_khronos(name):
    """Fetch one model from the Khronos glTF sample assets. Check the model's
    README for its licence before using it: the collection mixes CC0 and CC-BY,
    and only CC0 keeps this site free of attribution obligations."""
    dest = CACHE / 'khronos' / f'{name}.glb'
    return _get(KHRONOS.format(name=name), dest)


def load(slug, res='2k'):
    """Return (vertices, faces) for a Poly Haven model, centred and unit-sized."""
    import numpy as np
    import trimesh

    scene = trimesh.load(str(fetch(slug, res)), force='mesh', process=True)
    v = np.asarray(scene.vertices, float)
    f = np.asarray(scene.faces, int)
    v -= (v.min(axis=0) + v.max(axis=0)) / 2
    v /= np.abs(v).max()
    return v, f


if __name__ == '__main__':
    import sys
    for slug in sys.argv[1:]:
        v, f = load(slug)
        print(f'{slug}: {len(v)} verts, {len(f)} faces')
