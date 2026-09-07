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
    """An avocado, the blade coming down, then the two halves turned to show
    their cut faces. Turning the far half through 180 degrees is what makes
    the cut read: seen edge-on, a cut face is only a sliver."""
    v, f = MD.prepare('food_avocado_01', faces=1100)
    v = G.y_up_to_z_up(v) * 0.95

    # Cut on a vertical plane, so the blade reads as a knife coming down. Each
    # half is then turned a quarter turn to present its cut face to the camera.
    normal = (1.0, 0.0, 0.0)
    (va, fa), (vb, fb), ring = MD.slice_capped(v, f, normal)

    left, right = -1.75, 1.05
    gap = 0.80
    whole = v + np.array([left, 0, 0])

    # A quarter turn each, in opposite directions, brings both cut faces round
    # to the camera; without it a cut face is only a sliver.
    halves = []
    for (vv, ff), turn, dx in (((va, fa), np.pi / 2 - 0.30, -gap),
                               ((vb, fb), -np.pi / 2 + 0.30, gap)):
        rot = G.rot_z(turn)
        shift = np.array([right + dx, 0, 0])
        halves.append((G.transform(vv, 1.0, rot, shift), ff,
                       G.transform(ring, 1.0, rot, shift)))

    span = np.vstack([whole] + [h[0] for h in halves]
                     + [[[left - 0.8, 0, -1.25], [right + gap + 0.8, 0, -1.25],
                         [left, 0.0, 2.05]]])
    eye = (0.55, -4.9, 1.35)
    s = Scene(eye, (0, 0, 0), scale=autoscale(eye, (0, 0, 0), span, margin=0.9))

    s.add_mesh(whole, f, stroke=INK, width=1.0)
    _blade(s, left)
    for vv, ff, rr in halves:
        s.add_mesh(vv, ff, stroke=INK, width=1.0, cap_ring=rr,
                   cap_stroke=ACCENT, include_boundary=False)
    _time_arrow(s, left, right + gap)

    _write(path, s)
    return path


def _blade(s, x):
    """A knife coming down through the object, in the cutting plane."""
    blade = np.array([
        [x, -0.07, 0.10], [x, 0.07, 0.10],
        [x, 0.07, 1.45], [x, -0.07, 1.45],
    ])
    handle = np.array([
        [x, -0.10, 1.45], [x, 0.10, 1.45],
        [x, 0.10, 2.05], [x, -0.10, 2.05],
    ])
    for quad, w in ((blade, 1.0), (handle, 1.0)):
        v2, depth = s.project(quad)
        d = 'M' + 'L'.join(f'{a:.1f} {b:.1f}' for a, b in v2) + 'Z'
        s.add_raw(float(depth.mean()) - 1.5,
                  f'<path d="{d}" fill="{PAPER}" stroke="{ACCENT}" '
                  f'stroke-width="{w}" stroke-linejoin="round"/>')


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
    """One object seen from several cameras, drawn as the pyramid frusta the
    3D reconstruction literature uses, with a covariance ellipsoid on the view
    that is least well constrained."""
    v, f = MD.prepare('lemon', faces=800)
    obj = G.transform(G.y_up_to_z_up(v), 0.62, G.rot_z(0.4))

    cams = [(-1.30, 1.75, 0.0), (-0.30, 1.80, 0.0), (0.95, 2.15, 0.20)]
    centres = [np.array([np.cos(a) * d, np.sin(a) * d, 0.30 + 0.16 * i])
               for i, (a, d, _) in enumerate(cams)]

    span = np.vstack([obj]
                     + [c + np.array([0.5, 0.5, 0.5]) for c in centres]
                     + [c - np.array([0.5, 0.5, 0.5]) for c in centres])
    eye = (3.0, -3.4, 2.1)
    s = Scene(eye, (0, 0, 0), scale=autoscale(eye, (0, 0, 0), span, margin=0.9))

    s.add_mesh(obj, f, stroke=INK, width=1.0)
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
    k, depth_k = 0.30, 0.52
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
