"""Mesh operations: plane slicing with caps, and silhouette extraction."""
import numpy as np


def slice_mesh(v, f, n, d):
    """Split a mesh by the plane n·x = d. Returns (pos, neg) meshes, each
    capped with the real cross-section polygon so the cut face is solid."""
    n = np.asarray(n, float)
    n = n / np.linalg.norm(n)
    dist = v @ n - d

    out = {1: {'v': [], 'f': []}, -1: {'v': [], 'f': []}}
    index = {1: {}, -1: {}}
    cut_pts = []

    def push(side, p):
        key = tuple(np.round(p, 6))
        m = index[side]
        if key not in m:
            m[key] = len(out[side]['v'])
            out[side]['v'].append(p)
        return m[key]

    def interp(a, b):
        da, db = dist[a], dist[b]
        t = da / (da - db)
        return v[a] + t * (v[b] - v[a])

    for tri in f:
        ds = dist[tri]
        pos = [i for i, x in zip(tri, ds) if x >= 0]
        neg = [i for i, x in zip(tri, ds) if x < 0]

        if not neg:
            idx = [push(1, v[i]) for i in tri]
            out[1]['f'].append(idx)
            continue
        if not pos:
            idx = [push(-1, v[i]) for i in tri]
            out[-1]['f'].append(idx)
            continue

        # One vertex alone on its side; two on the other.
        if len(pos) == 1:
            lone, side, pair = pos[0], 1, neg
        else:
            lone, side, pair = neg[0], -1, pos
        p0, p1 = interp(lone, pair[0]), interp(lone, pair[1])
        cut_pts += [p0, p1]

        a = push(side, v[lone]); b = push(side, p0); c = push(side, p1)
        out[side]['f'].append([a, b, c])

        o = -side
        q0 = push(o, v[pair[0]]); q1 = push(o, v[pair[1]])
        r0 = push(o, p0); r1 = push(o, p1)
        out[o]['f'] += [[q0, q1, r1], [q0, r1, r0]]

    body_count = {side: len(out[side]['f']) for side in (1, -1)}

    # Cap both sides with the cross-section, fan-triangulated about its centre.
    if cut_pts:
        # Every crossed triangle contributes both of its intersection points,
        # so the ring arrives with each point duplicated. Weld them first:
        # sorting near-duplicates by angle interleaves them and the cut face
        # comes out as a sawtooth.
        pts = np.unique(np.round(np.array(cut_pts), 5), axis=0)
        centre = pts.mean(axis=0)
        e1 = pts[0] - centre
        e1 /= np.linalg.norm(e1)
        e2 = np.cross(n, e1)
        ang = np.arctan2((pts - centre) @ e2, (pts - centre) @ e1)
        ring = pts[np.argsort(ang)]
        for side in (1, -1):
            ci = push(side, centre)
            ids = [push(side, p) for p in ring]
            for i in range(len(ids)):
                tri = [ci, ids[i], ids[(i + 1) % len(ids)]]
                out[side]['f'].append(tri if side == 1 else tri[::-1])

    ring_out = ring if cut_pts else np.zeros((0, 3))
    res = []
    for side in (1, -1):
        res.append((np.array(out[side]['v']), np.array(out[side]['f']),
                    body_count[side]))
    return res[0], res[1], ring_out


def silhouette_loops(v2, faces, facing, include_boundary=True):
    """Chain silhouette edges (front face meets back face) into closed loops,
    so an object ships as one path instead of hundreds of segments."""
    edges = {}
    for i, tri in enumerate(faces):
        for a, b in ((tri[0], tri[1]), (tri[1], tri[2]), (tri[2], tri[0])):
            edges.setdefault((min(a, b), max(a, b)), []).append(i)

    # An open mesh's boundary edges are silhouette-like, but on a sliced half
    # they trace the cut, which is drawn separately from the true intersection
    # ring. Chaining both together makes the outline zigzag between them.
    sil = [e for e, fs in edges.items()
           if (len(fs) == 1 and include_boundary)
           or (len(fs) > 1 and facing[fs[0]] != facing[fs[-1]])]
    if not sil:
        return []

    adj = {}
    for a, b in sil:
        adj.setdefault(a, []).append(b)
        adj.setdefault(b, []).append(a)

    seen, loops = set(), []
    for start in adj:
        if start in seen:
            continue
        loop, cur, prev = [start], start, None
        seen.add(start)
        while True:
            nxt = next((x for x in adj[cur] if x != prev and x not in seen), None)
            if nxt is None:
                if start in adj[cur] and len(loop) > 2:
                    pass
                break
            loop.append(nxt)
            seen.add(nxt)
            prev, cur = cur, nxt
        if len(loop) > 2:
            loops.append(loop)
    return loops


def path_from_loop(v2, loop, close=True):
    pts = v2[loop]
    d = f'M{pts[0,0]:.1f} {pts[0,1]:.1f}'
    d += ''.join(f'L{x:.1f} {y:.1f}' for x, y in pts[1:])
    return d + ('Z' if close else '')


def transform(v, scale=1.0, rot=None, shift=(0, 0, 0)):
    out = v * scale
    if rot is not None:
        out = out @ np.asarray(rot).T
    return out + np.asarray(shift, float)


def rot_z(a):
    c, s = np.cos(a), np.sin(a)
    return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])


def y_up_to_z_up(v):
    """Poly Haven models stand on the y axis; the scene is z-up."""
    return np.c_[v[:, 0], -v[:, 2], v[:, 1]]


def rot_y(a):
    c, s = np.cos(a), np.sin(a)
    return np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])
