"""
Real source meshes, prepared for line art.

Poly Haven models arrive far denser than a 176 px drawing can use, and some
files hold several objects. This module loads, isolates, decimates and
normalises them, and slices them with trimesh's capped plane cut.
"""
import numpy as np
import trimesh

import fetch


def _mesh(slug, res='2k'):
    v, f = fetch.load(slug, res)
    return trimesh.Trimesh(v, f, process=True)


def biggest_part(mesh, cluster=True):
    """Isolate one object from a file that holds several.

    Parts are grouped by position first, because a single bottle is itself
    several components (glass, label, cork) that belong together.
    """
    parts = mesh.split(only_watertight=False)
    if len(parts) <= 1:
        return mesh
    if not cluster:
        return max(parts, key=lambda p: len(p.faces))

    centres = np.array([p.bounds.mean(axis=0) for p in parts])
    groups, used = [], set()
    for i in range(len(parts)):
        if i in used:
            continue
        near = [j for j in range(len(parts))
                if j not in used
                and np.linalg.norm(centres[j][:2] - centres[i][:2]) < 0.22]
        used.update(near)
        groups.append(near)

    best = max(groups, key=lambda g: sum(len(parts[j].faces) for j in g))
    return trimesh.util.concatenate([parts[j] for j in best])


def prepare(slug, faces=900, part=False, res='2k'):
    """Load, optionally isolate one object, decimate, and normalise to a unit
    box centred on the origin."""
    m = _mesh(slug, res)
    if part:
        m = biggest_part(m)
    if len(m.faces) > faces:
        m = m.simplify_quadric_decimation(face_count=faces)
    v = np.asarray(m.vertices, float)
    v -= (v.min(axis=0) + v.max(axis=0)) / 2
    v /= np.abs(v).max()
    return v, np.asarray(m.faces, int)


def slice_capped(v, f, normal, origin=(0, 0, 0)):
    """Cut a mesh with a plane, keeping both capped halves and the ring of the
    cut. trimesh's cap is robust on meshes that are not perfectly watertight,
    which hand-rolled slicing is not."""
    m = trimesh.Trimesh(v, f, process=True)
    out = []
    for sign in (1, -1):
        half = trimesh.intersections.slice_mesh_plane(
            m, plane_normal=np.array(normal) * sign,
            plane_origin=np.asarray(origin, float), cap=True)
        out.append((np.asarray(half.vertices, float),
                    np.asarray(half.faces, int)))

    section = m.section(plane_normal=np.asarray(normal, float),
                        plane_origin=np.asarray(origin, float))
    ring = np.zeros((0, 3))
    if section is not None:
        loops = section.discrete
        if len(loops):
            ring = np.asarray(max(loops, key=len), float)
    return out[0], out[1], ring


def simplify(points, eps=0.7, closed=True):
    """Douglas-Peucker. A silhouette traced over a few thousand faces carries
    far more points than the drawing needs; this keeps the shape and drops the
    weight."""
    pts = np.asarray(points, float)
    if len(pts) < 3:
        return pts

    keep = np.zeros(len(pts), bool)
    keep[0] = keep[-1] = True
    stack = [(0, len(pts) - 1)]
    while stack:
        a, b = stack.pop()
        if b <= a + 1:
            continue
        seg = pts[b] - pts[a]
        n = np.linalg.norm(seg)
        chunk = pts[a + 1:b]
        if n < 1e-9:
            d = np.linalg.norm(chunk - pts[a], axis=1)
        else:
            rel = chunk - pts[a]
            d = np.abs(seg[0] * rel[:, 1] - seg[1] * rel[:, 0]) / n
        i = int(np.argmax(d))
        if d[i] > eps:
            keep[a + 1 + i] = True
            stack += [(a, a + 1 + i), (a + 1 + i, b)]
    out = pts[keep]
    return out
