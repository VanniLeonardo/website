"""Scene assembly: project meshes, order them by depth, emit compact SVG."""
import numpy as np
import motif3d as M
import geom as G

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

    def add_mesh(self, v, f, stroke=INK, width=1.0, fill=PAPER,
                 cap_ring=None, cap_stroke=None, include_boundary=True):
        """Draw a solid: its outline as one filled path, so it occludes what
        lies behind it, plus optional highlighted cap faces (a cut surface)."""
        v2, depth = self.project(v)
        n = M.face_normals(v, f)
        nv = n @ self.view[:3, :3].T
        facing = nv[:, 2] < 0          # camera looks down -z in view space

        parts = []
        for loop in G.silhouette_loops(v2, f, facing, include_boundary):
            parts.append(f'<path d="{G.path_from_loop(v2, loop)}" fill="{fill}" '
                         f'stroke="{stroke}" stroke-width="{width}" '
                         f'stroke-linejoin="round"/>')

        if cap_ring is not None and len(cap_ring):
            # The cut surface, drawn from the true intersection ring.
            r2, rd = self.project(cap_ring)
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
