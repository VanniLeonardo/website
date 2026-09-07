"""
Build real 3D geometry, project it through a real camera, and emit hairline
SVG line art in the site's palette.

No runtime dependency: this runs at authoring time and the output is a static
SVG that inherits the page's CSS variables, so the motifs stay weightless and
theme-correct. numpy only.
"""
import numpy as np

PAPER = 'var(--bg)'
INK = 'var(--muted)'
FAINT = 'var(--rule)'
ACCENT = 'var(--accent)'


# ---------------------------------------------------------------- geometry --
def icosphere(subdiv=2):
    """Unit icosphere: vertices on the sphere, triangular faces."""
    t = (1 + 5 ** 0.5) / 2
    v = np.array([
        [-1, t, 0], [1, t, 0], [-1, -t, 0], [1, -t, 0],
        [0, -1, t], [0, 1, t], [0, -1, -t], [0, 1, -t],
        [t, 0, -1], [t, 0, 1], [-t, 0, -1], [-t, 0, 1],
    ], dtype=float)
    f = np.array([
        [0, 11, 5], [0, 5, 1], [0, 1, 7], [0, 7, 10], [0, 10, 11],
        [1, 5, 9], [5, 11, 4], [11, 10, 2], [10, 7, 6], [7, 1, 8],
        [3, 9, 4], [3, 4, 2], [3, 2, 6], [3, 6, 8], [3, 8, 9],
        [4, 9, 5], [2, 4, 11], [6, 2, 10], [8, 6, 7], [9, 8, 1],
    ])
    v /= np.linalg.norm(v, axis=1, keepdims=True)
    for _ in range(subdiv):
        mid, new_f = {}, []

        def midpoint(a, b):
            key = (min(a, b), max(a, b))
            if key not in mid:
                m = v[a] + v[b]
                mid[key] = len(v_list)
                v_list.append(m / np.linalg.norm(m))
            return mid[key]

        v_list = list(v)
        for a, b, c in f:
            ab, bc, ca = midpoint(a, b), midpoint(b, c), midpoint(c, a)
            new_f += [[a, ab, ca], [b, bc, ab], [c, ca, bc], [ab, bc, ca]]
        v = np.array(v_list)
        f = np.array(new_f)
    return v, f


def potato(subdiv=3, seed=7):
    """A lumpy tuber: an icosphere pushed around by a few low-frequency waves."""
    v, f = icosphere(subdiv)
    rng = np.random.default_rng(seed)
    r = np.ones(len(v))
    for _ in range(3):
        axis = rng.normal(size=3)
        axis /= np.linalg.norm(axis)
        freq = rng.uniform(0.8, 1.4)
        amp = rng.uniform(0.05, 0.09)
        r += amp * np.sin(freq * (v @ axis) * np.pi)
    v = v * r[:, None]
    v[:, 0] *= 1.45          # elongate
    v[:, 1] *= 0.92
    return v, f


def pyramid(base=1.0, height=1.35):
    """A square pyramid: a clean geometric solid whose pose is unambiguous,
    which is the point when the drawing is about pose uncertainty."""
    h = base / 2
    v = np.array([
        [-h, -h, 0.0], [h, -h, 0.0], [h, h, 0.0], [-h, h, 0.0],
        [0.0, 0.0, height],
    ])
    f = np.array([
        [0, 2, 1], [0, 3, 2],                      # base
        [0, 1, 4], [1, 2, 4], [2, 3, 4], [3, 0, 4],  # sides
    ])
    return v, f


# ------------------------------------------------------------------ camera --
def look_at(eye, target, up=(0, 0, 1)):
    eye, target, up = map(lambda a: np.asarray(a, float), (eye, target, up))
    f = target - eye
    f /= np.linalg.norm(f)
    s = np.cross(f, up)
    s /= np.linalg.norm(s)
    u = np.cross(s, f)
    m = np.eye(4)
    m[:3, :3] = np.stack([s, u, -f])
    m[:3, 3] = -m[:3, :3] @ eye
    return m


def project(pts, view, w, h, fov=32.0, scale=1.0):
    """World points to SVG pixel coordinates, plus camera-space depth."""
    p = np.c_[pts, np.ones(len(pts))] @ view.T
    depth = -p[:, 2]
    fl = (h / 2) / np.tan(np.radians(fov) / 2)
    x = w / 2 + fl * scale * p[:, 0] / np.maximum(depth, 1e-6)
    y = h / 2 - fl * scale * p[:, 1] / np.maximum(depth, 1e-6)
    return np.c_[x, y], depth


# ------------------------------------------------------------------- render --
def shade_faces(v2, depth, faces, normals, view_dir, fill=PAPER):
    """Painter's algorithm: far faces first, each filled with paper so the
    geometry occludes itself, then stroked so the form reads as line art."""
    facing = normals @ view_dir
    front = facing < 0
    order = np.argsort(-depth[faces].mean(axis=1))
    out = []
    for i in order:
        if not front[i]:
            continue
        pts = ' '.join(f'{v2[k, 0]:.1f},{v2[k, 1]:.1f}' for k in faces[i])
        # Faces angled away from the viewer get a fainter stroke, which reads
        # as curvature without any shading.
        w = 0.5 + 0.5 * float(min(1.0, abs(facing[i]) * 1.4))
        out.append(f'<polygon points="{pts}" fill="{fill}" stroke="{FAINT}" '
                   f'stroke-width="{w * 0.35:.2f}" stroke-linejoin="round"/>')
    return out


def silhouette(v2, faces, normals, view_dir):
    """Edges where a front face meets a back face: the object's outline."""
    facing = (normals @ view_dir) < 0
    edges = {}
    for i, (a, b, c) in enumerate(faces):
        for e in ((a, b), (b, c), (c, a)):
            key = (min(e), max(e))
            edges.setdefault(key, []).append(i)
    out = []
    for (a, b), fs in edges.items():
        if len(fs) == 2 and facing[fs[0]] != facing[fs[1]]:
            out.append(f'<path d="M{v2[a,0]:.1f} {v2[a,1]:.1f}L{v2[b,0]:.1f} '
                       f'{v2[b,1]:.1f}" stroke="{INK}" stroke-width="1.1" '
                       f'stroke-linecap="round"/>')
    return out


def face_normals(v, f):
    a, b, c = v[f[:, 0]], v[f[:, 1]], v[f[:, 2]]
    n = np.cross(b - a, c - a)
    return n / np.maximum(np.linalg.norm(n, axis=1, keepdims=True), 1e-9)


def svg(body, w=240, h=170):
    return (f'<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" '
            f'aria-hidden="true" fill="none" stroke-width="1">\n'
            + '\n'.join(body) + '\n</svg>\n')
