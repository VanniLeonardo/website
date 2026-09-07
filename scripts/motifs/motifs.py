"""The three research motifs, built from real 3D geometry.

Run with:  npm run motifs
"""
import pathlib
import numpy as np
import motif3d as M
import geom as G
from render import Scene, cap_face_ids, autoscale, PAPER, INK, FAINT, ACCENT

EYE = (3.2, -3.6, 2.1)


# ------------------------------------------------------- 1. current research
def cut_over_time(path):
    """One object whose structure changes: whole with the blade entering, then
    the two halves apart with the fresh cut surfaces picked out."""
    v0, f0 = M.potato(subdiv=3)
    plane_n, plane_d = (1.0, 0.22, 0.0), 0.0
    n = np.asarray(plane_n, float)
    n /= np.linalg.norm(n)
    rot = G.rot_z(0.22)
    left, right = -2.15, 2.05

    whole = G.transform(v0, 0.92, rot, (left, 0, 0))
    pos, neg, ring = G.slice_mesh(v0, f0, plane_n, plane_d)
    # Only the body faces go to the silhouette pass; the cap is drawn from the
    # true intersection ring instead.
    halves = [(G.transform(vv + sgn * n * 0.55, 0.92, G.rot_z(0.22), (right, 0, 0)),
               ff[:body],
               G.transform(ring + sgn * n * 0.55, 0.92, G.rot_z(0.22), (right, 0, 0)))
              for (vv, ff, body), sgn in ((pos, +1), (neg, -1))]

    span = np.vstack([whole] + [h[0] for h in halves]
                     + [np.array([[left - 0.9, 0, -1.5], [right + 1.0, 0, -1.5]])])
    scale = autoscale(EYE, (0, 0, 0), span, margin=0.86)
    s = Scene(EYE, (0, 0, 0), scale=scale)

    s.add_mesh(whole, f0, stroke=INK, width=1.0)
    _blade(s, left, plane_n, scale)

    for vv, ff, rr in halves:
        s.add_mesh(vv, ff, stroke=INK, width=1.0, cap_ring=rr,
                   cap_stroke=ACCENT, include_boundary=False)

    _time_arrow(s, left, right)
    open(path, 'w').write(s.svg())
    return path


def _blade(s, x, plane_n, scale=1.0):
    """A thin knife lying in the cutting plane."""
    n = np.asarray(plane_n, float)
    n /= np.linalg.norm(n)
    e1 = np.cross(n, [0, 0, 1.0])
    e1 /= np.linalg.norm(e1)
    e2 = np.cross(n, e1)
    quad = np.array([
        -0.16 * e1 - 0.10 * e2,
        0.16 * e1 - 0.10 * e2,
        0.16 * e1 + 1.70 * e2,
        -0.16 * e1 + 1.70 * e2,
    ]) + np.array([x, 0, 0.30])
    v2, depth = s.project(quad)
    d = 'M' + 'L'.join(f'{a:.1f} {b:.1f}' for a, b in v2) + 'Z'
    s.add_raw(float(depth.mean()) - 1.2,
              f'<path d="{d}" fill="{PAPER}" stroke="{ACCENT}" '
              f'stroke-width="1" stroke-linejoin="round"/>')


def _time_arrow(s, left=-1.7, right=1.8):
    pts = np.array([[left - 0.7, 0, -1.45], [right + 0.8, 0, -1.45]])
    v2, _ = s.project(pts)
    (x0, y0), (x1, y1) = v2
    s.add_raw(-1e6,
              f'<path d="M{x0:.1f} {y0:.1f}L{x1:.1f} {y1:.1f}" stroke="{FAINT}" '
              f'stroke-width="1" stroke-dasharray="2 4"/>'
              f'<path d="M{x1-6:.1f} {y1-3:.1f}L{x1:.1f} {y1:.1f}'
              f'L{x1-6:.1f} {y1+3:.1f}" stroke="{FAINT}" stroke-width="1" '
              f'stroke-linecap="round" stroke-linejoin="round"/>')


# --------------------------------------------------------------- 2. thesis --
def views_and_uncertainty(path):
    """The same object seen from several cameras, with a real 3D uncertainty
    ellipsoid on the view that is least well constrained."""
    v0, f0 = M.potato(subdiv=3, seed=3)
    obj = G.transform(v0, 0.70, G.rot_z(-0.4))

    cams = [(-1.25, 1.85, 0.0), (-0.20, 1.90, 0.0), (1.10, 2.30, 0.17)]
    centres = [np.array([np.cos(a) * d, np.sin(a) * d, 0.35 + 0.18 * i])
               for i, (a, d, _) in enumerate(cams)]

    span = np.vstack([obj] + [c + np.array([0.55, 0.55, 0.55]) for c in centres]
                     + [c - np.array([0.55, 0.55, 0.55]) for c in centres])
    eye = (3.0, -3.4, 2.1)
    s = Scene(eye, (0, 0, 0), scale=autoscale(eye, (0, 0, 0), span, margin=0.88))

    s.add_mesh(obj, f0, stroke=INK, width=1.0)
    for c, (_, _, sigma) in zip(centres, cams):
        _frustum(s, c, np.zeros(3), accent=sigma > 0)
        if sigma:
            _ellipsoid(s, c, np.diag([sigma * 1.5, sigma, sigma * 0.7]))
    open(path, 'w').write(s.svg())
    return path


def _frustum(s, c, target, accent=False):
    f = np.asarray(target, float) - c
    f /= np.linalg.norm(f)
    up = np.array([0, 0, 1.0])
    r = np.cross(f, up); r /= np.linalg.norm(r)
    u = np.cross(r, f)
    k = 0.34
    tip = c
    quad = np.array([c + f * 0.60 + (a * r + b * u) * k
                     for a, b in ((-1, -0.75), (1, -0.75), (1, 0.75), (-1, 0.75))])
    v2, depth = s.project(np.vstack([[tip], quad]))
    col = ACCENT if accent else INK
    d = ('M' + 'L'.join(f'{x:.1f} {y:.1f}' for x, y in v2[1:]) + 'Z'
         + ''.join(f'M{v2[0,0]:.1f} {v2[0,1]:.1f}L{x:.1f} {y:.1f}'
                   for x, y in v2[1:]))
    s.add_raw(float(depth.mean()),
              f'<path d="{d}" fill="none" stroke="{col}" stroke-width="1" '
              f'stroke-linejoin="round"/>')


def _ellipsoid(s, centre, cov, rings=3):
    """Uncertainty drawn as it actually is: the covariance's iso-surface."""
    vals, vecs = np.linalg.eigh(cov)
    axes = vecs * np.sqrt(np.maximum(vals, 1e-9))
    out, depths = [], []
    for k in range(rings):
        t = np.linspace(0, 2 * np.pi, 40)
        circ = np.zeros((40, 3))
        i, j = [(0, 1), (1, 2), (0, 2)][k]
        circ[:, i], circ[:, j] = np.cos(t), np.sin(t)
        pts = centre + circ @ axes.T * 1.55
        v2, depth = s.project(pts)
        d = 'M' + 'L'.join(f'{x:.1f} {y:.1f}' for x, y in v2) + 'Z'
        out.append(f'<path d="{d}" fill="none" stroke="{ACCENT}" '
                   f'stroke-width="0.9" stroke-dasharray="3 3" opacity="0.85"/>')
        depths.append(depth.mean())
    s.add_raw(float(np.mean(depths)) - 0.4, '\n'.join(out))


# ------------------------------------------------------- 3. prosthetic arm --
def grasp_check(path):
    """A bottle, the detected 3D box around it, and a two-finger gripper."""
    v, f = _bottle()
    lo, hi = v.min(axis=0) - 0.02, v.max(axis=0) + 0.02
    span = np.vstack([v, [[0.4, 1.15, 0], [0.4, -1.15, 0]]])
    eye = (3.1, -3.5, 1.5)
    s = Scene(eye, (0, 0, 0.05),
              scale=autoscale(eye, (0, 0, 0.05), span, margin=0.88))
    s.add_mesh(v, f, stroke=INK, width=1.0)
    _box(s, lo, hi)
    _gripper(s)
    open(path, 'w').write(s.svg())
    return path


def _bottle(seg=20):
    """A lathe: bottle profile revolved about z. The two profile ends sit on
    the axis, so they are welded into single pole vertices; leaving one copy
    per segment makes the mesh non-manifold and the silhouette degenerate."""
    prof = [(0.00, -0.95), (0.40, -0.95), (0.42, -0.55), (0.42, 0.10),
            (0.34, 0.42), (0.17, 0.62), (0.15, 0.95), (0.17, 1.10),
            (0.00, 1.12)]
    ring = prof[1:-1]
    n = len(ring)
    verts = [[0.0, 0.0, prof[0][1]]]                 # bottom pole
    for a in np.linspace(0, 2 * np.pi, seg, endpoint=False):
        c, sn = np.cos(a), np.sin(a)
        for r, z in ring:
            verts.append([r * c, r * sn, z])
    verts.append([0.0, 0.0, prof[-1][1]])            # top pole
    bottom, top = 0, len(verts) - 1

    def vid(i, k):
        return 1 + (i % seg) * n + k

    faces = []
    for i in range(seg):
        j = i + 1
        faces.append([bottom, vid(j, 0), vid(i, 0)])
        faces.append([top, vid(i, n - 1), vid(j, n - 1)])
        for k in range(n - 1):
            a, b = vid(i, k), vid(i, k + 1)
            c, d = vid(j, k), vid(j, k + 1)
            faces += [[a, c, d], [a, d, b]]
    return np.array(verts, float), np.array(faces)


def _box(s, lo, hi):
    """Detected 3D bounding box. Corners in an explicit order so the twelve
    edges are unambiguous."""
    lo, hi = np.array(lo, float), np.array(hi, float)
    corners = np.array([
        [lo[0], lo[1], lo[2]], [hi[0], lo[1], lo[2]],
        [hi[0], hi[1], lo[2]], [lo[0], hi[1], lo[2]],
        [lo[0], lo[1], hi[2]], [hi[0], lo[1], hi[2]],
        [hi[0], hi[1], hi[2]], [lo[0], hi[1], hi[2]],
    ])
    edges = [(0, 1), (1, 2), (2, 3), (3, 0),
             (4, 5), (5, 6), (6, 7), (7, 4),
             (0, 4), (1, 5), (2, 6), (3, 7)]
    v2, depth = s.project(corners)
    d = ''.join(f'M{v2[a,0]:.1f} {v2[a,1]:.1f}L{v2[b,0]:.1f} {v2[b,1]:.1f}'
                for a, b in edges)
    s.add_raw(float(depth.mean()) - 0.5,
              f'<path d="{d}" fill="none" stroke="{ACCENT}" stroke-width="0.8" '
              f'stroke-dasharray="3 3" opacity="0.9"/>')


def _gripper(s):
    """Two opposing fingers, drawn as thin plates closing on the object."""
    out, depths = [], []
    for sgn in (+1, -1):
        y = sgn * 0.78
        plate = np.array([[-0.34, y, -0.34], [0.34, y, -0.34],
                          [0.34, y, 0.14], [-0.34, y, 0.14]])
        plate[:, 1] -= sgn * 0.06
        v2, depth = s.project(plate)
        d = 'M' + 'L'.join(f'{x:.1f} {y2:.1f}' for x, y2 in v2) + 'Z'
        out.append(f'<path d="{d}" fill="{PAPER}" stroke="{INK}" '
                   f'stroke-width="1" stroke-linejoin="round"/>')
        depths.append(depth.mean())
        arrow = np.array([[0.0, y - sgn * 0.14, -0.10], [0.0, y - sgn * 0.40, -0.10]])
        a2, _ = s.project(arrow)
        out.append(f'<path d="M{a2[0,0]:.1f} {a2[0,1]:.1f}'
                   f'L{a2[1,0]:.1f} {a2[1,1]:.1f}" stroke="{FAINT}" '
                   f'stroke-width="1" stroke-linecap="round"/>')
    s.add_raw(float(np.mean(depths)), '\n'.join(out))


OUT = pathlib.Path(__file__).resolve().parents[2] / 'src' / 'components' / 'motifs'

if __name__ == '__main__':
    OUT.mkdir(parents=True, exist_ok=True)
    for fn, name in ((cut_over_time, 'cut'),
                     (views_and_uncertainty, 'covariance'),
                     (grasp_check, 'grasp')):
        path = OUT / f'{name}.svg'
        fn(str(path))
        print(f'{path.relative_to(OUT.parents[2])}  {path.stat().st_size} bytes')
