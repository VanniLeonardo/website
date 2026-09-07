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


def pyramid(base=1.0, height=None, courses=0):
    """A square pyramid in the proportions of the Great Pyramid: height is
    0.6366 of the base, which is what stops it reading as a tent.

    With `courses` > 0 it is built as a stack of stepped blocks, which reads
    unmistakably as masonry rather than as a triangle.
    """
    if height is None:
        height = base * 0.6366
    h = base / 2

    if courses:
        verts, faces = [], []
        for i in range(courses):
            t0, t1 = i / courses, (i + 1) / courses
            b0, b1 = h * (1 - t0), h * (1 - t1)
            z0, z1 = height * t0, height * t1
            base_i = len(verts)
            verts += [[-b0, -b0, z0], [b0, -b0, z0], [b0, b0, z0], [-b0, b0, z0],
                      [-b1, -b1, z1], [b1, -b1, z1], [b1, b1, z1], [-b1, b1, z1]]
            q = [(0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7),
                 (4, 5, 6, 7)]
            for a, b, c, d in q:
                faces += [[base_i + a, base_i + b, base_i + c],
                          [base_i + a, base_i + c, base_i + d]]
        return np.array(verts, float), np.array(faces)

    v = np.array([
        [-h, -h, 0.0], [h, -h, 0.0], [h, h, 0.0], [-h, h, 0.0],
        [0.0, 0.0, height],
    ])
    f = np.array([
        [0, 2, 1], [0, 3, 2],                      # base
        [0, 1, 4], [1, 2, 4], [2, 3, 4], [3, 0, 4],  # sides
    ])
    return v, f


def cake_sector(a0, a1, radius=1.0, height=0.42, seg=34):
    """A solid wedge of a round cake, from angle a0 to a1.

    Built rather than carved. A cake is a cylinder, so the exact geometry is
    two flat side faces, a curved wall, and a top and bottom: clean, closed,
    and with cut faces that are perfectly flat. Slicing a scanned model gives
    a ragged notch and a cap that spans the whole diameter.
    """
    n = max(2, int(seg * abs(a1 - a0) / (2 * np.pi)) + 2)
    ang = np.linspace(a0, a1, n)
    rim = np.c_[np.cos(ang), np.sin(ang)] * radius

    verts = [[0.0, 0.0, 0.0], [0.0, 0.0, height]]
    for x, y in rim:
        verts += [[x, y, 0.0], [x, y, height]]
    v = np.array(verts, float)

    faces = []
    for i in range(n - 1):
        b0, t0 = 2 + 2 * i, 3 + 2 * i
        b1, t1 = 2 + 2 * (i + 1), 3 + 2 * (i + 1)
        faces += [[b0, b1, t1], [b0, t1, t0]]     # outer wall
        faces += [[0, b1, b0]]                    # bottom fan
        faces += [[1, t0, t1]]                    # top fan
    # The two flat cut faces.
    faces += [[0, 2, 3], [0, 3, 1]]
    last_b, last_t = 2 + 2 * (n - 1), 3 + 2 * (n - 1)
    faces += [[0, last_t, last_b], [0, 1, last_t]]
    return v, np.array(faces)


def cut_face_quad(angle, radius=1.0, height=0.42):
    """The flat face one radial cut leaves: axis to rim, base to top."""
    d = np.array([np.cos(angle), np.sin(angle), 0.0])
    return np.array([[0, 0, 0], d * radius, d * radius + [0, 0, height],
                     [0, 0, height]])


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
