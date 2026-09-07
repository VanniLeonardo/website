"""Scene assembly: project meshes, order them by depth, emit compact SVG."""
import numpy as np
import motif3d as M
import geom as G
import models as MD

PAPER, INK, FAINT, ACCENT = M.PAPER, M.INK, M.FAINT, M.ACCENT


class Scene:
    def __init__(self, eye, target=(0, 0, 0), w=240, h=170, fov=32, scale=1.0):
        self.view = M.look_at(eye, target)
        self.w, self.h, self.fov, self.scale = w, h, fov, scale
        self.items = []          # (depth, svg string)

    def project(self, v):
        return M.project(v, self.view, self.w, self.h, self.fov, self.scale)

    def add_raw(self, depth, svg):
        self.items.append((depth, svg))

    def add_faceted(self, v, f, stroke=INK, width=1.0, fill=PAPER):
        """Draw a simple solid face by face, far to near.

        Silhouette chaining assumes a dense mesh: on a solid with a handful of
        vertices the chain runs through shared corners and the outline comes
        out broken. For a pyramid or a box, painter's algorithm is both exact
        and cheap.
        """
        v2, depth = self.project(v)
        nv = M.face_normals(v, f) @ self.view[:3, :3].T
        order = np.argsort(-depth[f].mean(axis=1))
        parts = []
        for i in order:
            if nv[i, 2] >= 0:            # back-facing
                continue
            pts = ' '.join(f'{v2[k,0]:.1f},{v2[k,1]:.1f}' for k in f[i])
            parts.append(f'<polygon points="{pts}" fill="{fill}" '
                         f'stroke="{stroke}" stroke-width="{width}" '
                         f'stroke-linejoin="round"/>')
        self.add_raw(float(depth.mean()), '\n'.join(parts))

    def add_mesh(self, v, f, stroke=INK, width=1.0, fill=PAPER,
                 cap_ring=None, cap_stroke=None, include_boundary=True,
                 eps=0.8, min_size=0.0, creases=False):
        """Draw a solid: its outline as one filled path, so it occludes what
        lies behind it, plus optional highlighted cap faces (a cut surface)."""
        v2, depth = self.project(v)
        n = M.face_normals(v, f)
        nv = n @ self.view[:3, :3].T
        facing = nv[:, 2] < 0          # camera looks down -z in view space

        parts = []
        for loop in G.silhouette_loops(v2, f, facing, include_boundary):
            pts = MD.simplify(v2[loop], eps=eps)
            if len(pts) < 3:
                continue
            # Surface detail on a scanned model throws off dozens of tiny
            # silhouette loops that read as speckle and dominate the file size.
            extent = pts.max(axis=0) - pts.min(axis=0)
            if max(extent) < min_size:
                continue
            closed = np.linalg.norm(pts[0] - pts[-1]) < 6.0
            d = 'M' + 'L'.join(f'{x:.1f} {y:.1f}' for x, y in pts)
            parts.append(
                f'<path d="{d}Z" fill="{fill}" stroke="{stroke}" '
                f'stroke-width="{width}" stroke-linejoin="round"/>' if closed else
                f'<path d="{d}" fill="none" stroke="{stroke}" '
                f'stroke-width="{width}" stroke-linejoin="round" '
                f'stroke-linecap="round"/>')

        if creases:
            fe = G.feature_edges(v, f, nv, facing)
            if fe:
                d = ''.join(f'M{v2[a,0]:.1f} {v2[a,1]:.1f}'
                            f'L{v2[b,0]:.1f} {v2[b,1]:.1f}' for a, b in fe)
                parts.append(f'<path d="{d}" fill="none" stroke="{stroke}" '
                             f'stroke-width="{width * 0.85}" '
                             f'stroke-linecap="round"/>')

        if cap_ring is not None and len(cap_ring):
            # The cut surface, drawn from the true intersection ring.
            r2, rd = self.project(cap_ring)
            r2 = MD.simplify(r2, eps=eps * 0.6)
            d = 'M' + 'L'.join(f'{x:.1f} {y:.1f}' for x, y in r2) + 'Z'
            parts.append(f'<path d="{d}" fill="{PAPER}" '
                         f'stroke="{cap_stroke or ACCENT}" '
                         f'stroke-width="{width}" stroke-linejoin="round"/>')

        self.add_raw(float(depth.mean()), '\n'.join(parts))

    def svg(self):
        body = [s for _, s in sorted(self.items, key=lambda t: -t[0])]
        return M.svg(body, self.w, self.h)


def autoscale(eye, target, pts, w=240, h=170, fov=32, margin=0.90):
    """Scale that makes `pts` fill the frame with a margin."""
    view = M.look_at(eye, target)
    v2, _ = M.project(np.asarray(pts, float), view, w, h, fov, 1.0)
    ex = max(v2[:, 0].max() - w / 2, w / 2 - v2[:, 0].min())
    ey = max(v2[:, 1].max() - h / 2, h / 2 - v2[:, 1].min())
    return margin * min((w / 2) / max(ex, 1e-6), (h / 2) / max(ey, 1e-6))


def _order_ring(pts):
    c = pts.mean(axis=0)
    a = np.arctan2(pts[:, 1] - c[1], pts[:, 0] - c[0])
    return pts[np.argsort(a)]


def cap_face_ids(v, f, n, d, tol=1e-4):
    """Faces lying in the cutting plane: the fresh cut surface."""
    n = np.asarray(n, float) / np.linalg.norm(n)
    centroids = v[f].mean(axis=1)
    return np.where(np.abs(centroids @ n - d) < tol)[0]
