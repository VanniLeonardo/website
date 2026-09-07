"""The three research motifs, drawn from real 3D models.

Source meshes come from Poly Haven (CC0). They are loaded, decimated, and
projected through a real camera; hidden surfaces are removed by depth sorting
and the silhouette is emitted as hairline SVG in the site's palette.

Run with:  npm run motifs
"""
import pathlib

import numpy as np

import geom as G
import models as MD
import motif3d as M
from render import Scene, autoscale, PAPER, INK, FAINT, ACCENT


# --------------------------------------------------- 1. current research ----
def cut_over_time(path):
    """A round cake with one slice cut and drawn pulled clear, the knife still
    in the cut. A wedge missing from a circle reads as 'this was cut' at a
    glance."""
    a0, a1 = 0.35, 1.30
    R, H = 1.0, 0.44

    rest_v, rest_f = M.cake_sector(a1, a0 + 2 * np.pi, R, H)
    wedge_v, wedge_f = M.cake_sector(a0, a1, R, H)

    mid = (a0 + a1) / 2
    pull = np.array([np.cos(mid), np.sin(mid), 0]) * 0.62

    eye = (1.15, -3.6, 2.5)
    span = np.vstack([rest_v, wedge_v + pull, [[0, 0, 1.15]]])
    s = Scene(eye, (0, 0, 0), scale=autoscale(eye, (0, 0, 0), span, margin=0.92))

    s.add_faceted(rest_v, rest_f, stroke=INK, width=0.9)
    for ang in (a0, a1):
        _cut_face(s, M.cut_face_quad(ang, R, H))

    s.add_faceted(wedge_v + pull, wedge_f, stroke=INK, width=0.9)
    for ang in (a0, a1):
        _cut_face(s, M.cut_face_quad(ang, R, H) + pull)

    _knife(s, a0, lift=H + 0.16)
    _write(path, s)
    return path


def _cut_face(s, ring):
    """A fresh cut surface: outlined and lightly tinted, so the eye lands on
    what changed rather than on the object's outline."""
    r2, depth = s.project(ring)
    r2 = MD.simplify(r2, eps=0.5)
    if len(r2) < 3:
        return
    d = 'M' + 'L'.join(f'{x:.1f} {y:.1f}' for x, y in r2) + 'Z'
    s.add_raw(float(depth.mean()) - 0.05,
              f'<path d="{d}" fill="{ACCENT}" fill-opacity="0.16" '
              f'stroke="{ACCENT}" stroke-width="1" stroke-linejoin="round"/>')


def _knife_profile(n=26):
    """A chef's knife in profile: a curved belly rising to a pointed tip, a
    straight spine, a bolster, and a handle. Returned as one closed polygon in
    blade coordinates, x from heel to tip and z up."""
    t = np.linspace(0.0, 1.0, n)

    # Spine: nearly straight, dropping into the tip at the very end.
    spine_x = -0.30 + 1.42 * t
    spine_z = 0.150 - 0.01 * t - 0.150 * t ** 4

    # Edge: the belly curve, rising to meet the spine at the tip.
    edge_x = spine_x
    edge_z = -0.165 + 0.165 * t ** 1.9

    blade = np.r_[np.c_[spine_x, spine_z], np.c_[edge_x, edge_z][::-1]]

    # Handle, with a bolster step where it meets the blade.
    handle = np.array([
        [-0.30, -0.075], [-0.40, -0.105], [-1.16, -0.115],
        [-1.24, -0.055], [-1.24, 0.075], [-1.16, 0.135],
        [-0.40, 0.125], [-0.30, 0.155],
    ])
    return np.vstack([blade, handle])


def _knife(s, angle, lift=0.60, tilt=0.26, scale=0.72):
    """The knife laid along the cut it made, edge down into the cake."""
    prof = _knife_profile()
    d = np.array([np.cos(angle), np.sin(angle), 0.0])
    up = np.array([0.0, 0.0, 1.0])
    # Tilt the blade so the tip dips towards the cut.
    d_t = d * np.cos(tilt) - up * np.sin(tilt)
    up_t = d * np.sin(tilt) + up * np.cos(tilt)

    prof = prof * scale
    pts3 = np.array([d_t * x + up_t * z + up * lift for x, z in prof])
    v2, depth = s.project(pts3)
    path = 'M' + 'L'.join(f'{a:.1f} {b:.1f}' for a, b in v2) + 'Z'
    s.add_raw(float(depth.mean()) - 2.0,
              f'<path d="{path}" fill="{PAPER}" stroke="{INK}" '
              f'stroke-width="1" stroke-linejoin="round"/>')

    # Bolster: the short line where handle meets blade.
    b = np.array([d_t * -0.30 * scale + up_t * -0.075 * scale + up * lift,
                  d_t * -0.30 * scale + up_t * 0.150 * scale + up * lift])
    b2, bd = s.project(b)
    s.add_raw(float(bd.mean()) - 2.1,
              f'<path d="M{b2[0,0]:.1f} {b2[0,1]:.1f}L{b2[1,0]:.1f} '
              f'{b2[1,1]:.1f}" stroke="{INK}" stroke-width="0.8" '
              f'stroke-linecap="round"/>')


def _time_arrow(s, left, right):
    pts = np.array([[left - 0.55, 0, -1.30], [right + 0.75, 0, -1.30]])
    v2, _ = s.project(pts)
    (x0, y0), (x1, y1) = v2
    s.add_raw(-1e6,
              f'<path d="M{x0:.1f} {y0:.1f}L{x1:.1f} {y1:.1f}" stroke="{FAINT}" '
              f'stroke-width="1" stroke-dasharray="2 4"/>'
              f'<path d="M{x1-5:.1f} {y1-3:.1f}L{x1:.1f} {y1:.1f}'
              f'L{x1-5:.1f} {y1+3:.1f}" stroke="{FAINT}" stroke-width="1" '
              f'stroke-linecap="round" stroke-linejoin="round"/>')


# ------------------------------------------------------------- 2. thesis ----
def views_and_uncertainty(path):
    """A car seen from several cameras, drawn as the pyramid frusta the 3D
    reconstruction literature uses, with a covariance ellipsoid on the view
    that is least well constrained."""
    v, f = MD.prepare('khronos:ToyCar', faces=2600, drop_flat=True)
    obj = G.transform(G.y_up_to_z_up(v), 1.18, G.rot_z(-0.86), (0, 0, -0.16))

    cams = [(-1.50, 2.30, 0.0), (-0.32, 2.40, 0.0), (1.00, 2.70, 0.20)]
    centres = [np.array([np.cos(a) * d, np.sin(a) * d, 0.30 + 0.16 * i])
               for i, (a, d, _) in enumerate(cams)]

    span = np.vstack([obj]
                     + [c + np.array([0.5, 0.5, 0.5]) for c in centres]
                     + [c - np.array([0.5, 0.5, 0.5]) for c in centres])
    eye = (3.0, -3.4, 2.1)
    s = Scene(eye, (0, 0, 0), scale=autoscale(eye, (0, 0, 0), span, margin=0.9))

    s.add_mesh(obj, f, stroke=INK, width=1.0, eps=1.3, min_size=8.0,
               creases=True, crease_angle=38.0, crease_min_px=4.5)
    for c, (_, _, sigma) in zip(centres, cams):
        _frustum(s, c, np.zeros(3), accent=sigma > 0)
        if sigma:
            _ellipsoid(s, c, np.diag([sigma * 1.5, sigma, sigma * 0.7]))

    _write(path, s)
    return path


def _frustum(s, c, target, accent=False):
    """A camera drawn as a pyramid: apex at the centre of projection, base at
    the image plane, with the up direction marked."""
    fwd = np.asarray(target, float) - c
    fwd /= np.linalg.norm(fwd)
    r = np.cross(fwd, [0, 0, 1.0])
    r /= np.linalg.norm(r)
    u = np.cross(r, fwd)
    k, depth_k = 0.24, 0.42
    base = np.array([c + fwd * depth_k + (a * r + b * u) * k
                     for a, b in ((-1, -0.72), (1, -0.72), (1, 0.72), (-1, 0.72))])
    v2, depth = s.project(np.vstack([[c], base]))
    col = ACCENT if accent else INK
    d = ('M' + 'L'.join(f'{x:.1f} {y:.1f}' for x, y in v2[1:]) + 'Z'
         + ''.join(f'M{v2[0,0]:.1f} {v2[0,1]:.1f}L{x:.1f} {y:.1f}'
                   for x, y in v2[1:]))
    s.add_raw(float(depth.mean()),
              f'<path d="{d}" fill="none" stroke="{col}" stroke-width="1" '
              f'stroke-linejoin="round"/>')


def _ellipsoid(s, centre, cov, rings=3):
    """Uncertainty drawn as it actually is: the iso-surface of the covariance,
    from its eigendecomposition."""
    vals, vecs = np.linalg.eigh(cov)
    axes = vecs * np.sqrt(np.maximum(vals, 1e-9))
    out, depths = [], []
    for k in range(rings):
        t = np.linspace(0, 2 * np.pi, 48)
        circ = np.zeros((48, 3))
        i, j = [(0, 1), (1, 2), (0, 2)][k]
        circ[:, i], circ[:, j] = np.cos(t), np.sin(t)
        v2, depth = s.project(centre + circ @ axes.T * 1.55)
        d = 'M' + 'L'.join(f'{x:.1f} {y:.1f}' for x, y in v2) + 'Z'
        out.append(f'<path d="{d}" fill="none" stroke="{ACCENT}" '
                   f'stroke-width="0.9" stroke-dasharray="3 3" opacity="0.85"/>')
        depths.append(depth.mean())
    s.add_raw(float(np.mean(depths)) - 0.4, '\n'.join(out))


# ----------------------------------------------------- 3. prosthetic arm ----
def grasp_check(path):
    """A real bottle, the detected 3D box around it, and a two-finger gripper
    closing in. The demo footage used a bottle, so the motif matches it."""
    v, f = MD.prepare('wine_bottles_01', faces=1300, part=True)
    v = G.transform(G.y_up_to_z_up(v), 1.0, G.rot_z(0.3))

    lo, hi = v.min(axis=0) - 0.03, v.max(axis=0) + 0.03
    span = np.vstack([v, [[0.0, 0.62, 0], [0.0, -0.62, 0]]])
    eye = (3.1, -3.5, 1.4)
    s = Scene(eye, (0, 0, 0),
              scale=autoscale(eye, (0, 0, 0), span, margin=0.92))

    s.add_mesh(v, f, stroke=INK, width=1.0)
    _box(s, lo, hi)
    _gripper(s, reach=max(abs(lo[1]), abs(hi[1])) + 0.20)

    _write(path, s)
    return path


def _box(s, lo, hi):
    """Detected 3D bounding box, corners in an explicit order so the twelve
    edges are unambiguous."""
    corners = np.array([
        [lo[0], lo[1], lo[2]], [hi[0], lo[1], lo[2]],
        [hi[0], hi[1], lo[2]], [lo[0], hi[1], lo[2]],
        [lo[0], lo[1], hi[2]], [hi[0], lo[1], hi[2]],
        [hi[0], hi[1], hi[2]], [lo[0], hi[1], hi[2]],
    ])
    edges = [(0, 1), (1, 2), (2, 3), (3, 0), (4, 5), (5, 6), (6, 7), (7, 4),
             (0, 4), (1, 5), (2, 6), (3, 7)]
    v2, depth = s.project(corners)
    d = ''.join(f'M{v2[a,0]:.1f} {v2[a,1]:.1f}L{v2[b,0]:.1f} {v2[b,1]:.1f}'
                for a, b in edges)
    s.add_raw(float(depth.mean()) - 0.6,
              f'<path d="{d}" fill="none" stroke="{ACCENT}" stroke-width="0.8" '
              f'stroke-dasharray="3 3" opacity="0.9"/>')


def _gripper(s, reach=0.62):
    """Two opposing fingers closing on the object."""
    out, depths = [], []
    for sgn in (+1, -1):
        y = sgn * reach
        plate = np.array([[-0.30, y, -0.30], [0.30, y, -0.30],
                          [0.30, y, 0.16], [-0.30, y, 0.16]])
        v2, depth = s.project(plate)
        d = 'M' + 'L'.join(f'{a:.1f} {b:.1f}' for a, b in v2) + 'Z'
        out.append(f'<path d="{d}" fill="{PAPER}" stroke="{INK}" '
                   f'stroke-width="1" stroke-linejoin="round"/>')
        depths.append(depth.mean())
        arrow = np.array([[0.0, y - sgn * 0.10, -0.07],
                          [0.0, y - sgn * 0.32, -0.07]])
        a2, _ = s.project(arrow)
        out.append(f'<path d="M{a2[0,0]:.1f} {a2[0,1]:.1f}'
                   f'L{a2[1,0]:.1f} {a2[1,1]:.1f}" stroke="{FAINT}" '
                   f'stroke-width="1" stroke-linecap="round"/>')
    s.add_raw(float(np.mean(depths)), '\n'.join(out))


# ------------------------------------------------------------------ output --
OUT = pathlib.Path(__file__).resolve().parents[2] / 'src' / 'components' / 'motifs'


def _write(path, scene):
    pathlib.Path(path).write_text(scene.svg())


if __name__ == '__main__':
    OUT.mkdir(parents=True, exist_ok=True)
    for fn, name in ((cut_over_time, 'cut'),
                     (views_and_uncertainty, 'covariance'),
                     (grasp_check, 'grasp')):
        p = OUT / f'{name}.svg'
        fn(str(p))
        print(f'{name:12} {p.stat().st_size:6d} bytes')
