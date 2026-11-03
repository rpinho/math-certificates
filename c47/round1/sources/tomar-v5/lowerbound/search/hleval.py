"""Python wrapper of eval.c: weak-type ratio of periodic point-mass configurations (rectangular period cell)."""
import ctypes, math, os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
_lib = ctypes.CDLL(os.path.join(HERE, 'libeval.so'))
_lib.superlevel_area.restype = ctypes.c_double
_lib.superlevel_area.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double),
                                 ctypes.POINTER(ctypes.c_double), ctypes.c_double, ctypes.c_double, ctypes.c_double,
                                 ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.POINTER(ctypes.c_int)]


def area_in_cell(px, py, pm, lam, cell, reach):
    px = np.ascontiguousarray(px, float); py = np.ascontiguousarray(py, float); pm = np.ascontiguousarray(pm, float)
    nr = ctypes.c_int(0)
    a = _lib.superlevel_area(len(px), px.ctypes.data_as(ctypes.POINTER(ctypes.c_double)),
                             py.ctypes.data_as(ctypes.POINTER(ctypes.c_double)),
                             pm.ctypes.data_as(ctypes.POINTER(ctypes.c_double)), lam, cell[0], cell[1], cell[2], cell[3],
                             reach, ctypes.byref(nr))
    return a, nr.value


_lib.superlevel_area2.restype = ctypes.c_double
_lib.superlevel_area2.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double),
                                  ctypes.POINTER(ctypes.c_double), ctypes.c_double, ctypes.c_double, ctypes.c_double,
                                  ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double,
                                  ctypes.POINTER(ctypes.c_int)]


def area_in_cell2(px, py, pm, lam, cell, reach, rho_max):
    px = np.ascontiguousarray(px, float); py = np.ascontiguousarray(py, float); pm = np.ascontiguousarray(pm, float)
    nr = ctypes.c_int(0)
    dp = ctypes.POINTER(ctypes.c_double)
    a = _lib.superlevel_area2(len(px), px.ctypes.data_as(dp), py.ctypes.data_as(dp), pm.ctypes.data_as(dp), lam,
                              cell[0], cell[1], cell[2], cell[3], reach, rho_max, ctypes.byref(nr))
    return a, nr.value


def periodic_ratio(Px, Py, pts, lam=0.25, reach_factor=1.0, margin_cells=None, reach_abs=None):
    """pts: list of (x, y, m) in the cell [0, Px) x [0, Py). Returns (ratio, area, nrect).
    Window: enough periods around the cell to contain every box whose rectangle can meet the cell."""
    m_cell = sum(p[2] for p in pts)
    dens = m_cell / (Px * Py)
    # a box of side <= reach: its mass is at most about (reach/P + 1)^2 m_cell; rho = sqrt(mass/(4 lam))
    reach = reach_factor * 4.0 * math.sqrt(m_cell / (4 * lam)) + 2 * max(Px, Py)
    if reach_abs is None and os.environ.get('HL_REACH'):
        reach_abs = float(os.environ['HL_REACH'])
    if reach_abs is not None:
        reach = reach_abs
    nx = margin_cells or int(math.ceil((reach + 2 * math.sqrt(max(1.0, (reach / Px + 1) * (reach / Py + 1)) * m_cell / (4 * lam))) / Px)) + 1
    ny = margin_cells or int(math.ceil((reach + 2 * math.sqrt(max(1.0, (reach / Px + 1) * (reach / Py + 1)) * m_cell / (4 * lam))) / Py)) + 1
    I, J = np.meshgrid(np.arange(-nx, nx + 1), np.arange(-ny, ny + 1), indexing='ij')
    I = I.ravel(); J = J.ravel()
    P = np.array(pts, float)
    px = (P[None, :, 0] + I[:, None] * Px).ravel()
    py = (P[None, :, 1] + J[:, None] * Py).ravel()
    pm = np.broadcast_to(P[None, :, 2], (len(I), len(P))).ravel()
    rho_max = math.sqrt(max(1.0, (reach / Px + 2) * (reach / Py + 2)) * m_cell / (4 * lam))
    a, nr = area_in_cell2(px, py, pm, lam, (0.0, Px, 0.0, Py), reach, rho_max)
    return lam * a / m_cell, a, nr


def lin_config():
    s22 = math.sqrt(22.0)
    h = (5 + s22) / 6; V = h + 1; w = (17 + 4 * s22) / 9
    return 2 * h, V, [(0.0, 0.0, 1.0), (h, 0.0, w)]


if __name__ == '__main__':
    Px, Py, pts = lin_config()
    for lam in (1.0, 0.25):
        print('lam', lam, periodic_ratio(Px, Py, pts, lam=lam))


_lib.coverage_grid.restype = None
_lib.coverage_grid.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double),
                               ctypes.POINTER(ctypes.c_double), ctypes.c_double, ctypes.c_double, ctypes.c_double,
                               ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_int,
                               ctypes.POINTER(ctypes.c_double), ctypes.c_int, ctypes.POINTER(ctypes.c_double),
                               ctypes.POINTER(ctypes.c_ubyte)]


def periodic_uncovered(Px, Py, pts, lam=1.0, n=600):
    """grid of size n x n (cell centres) with True where {M mu >= lam} does not cover; same window as periodic_ratio."""
    m_cell = sum(p[2] for p in pts)
    reach = 4.0 * math.sqrt(m_cell / (4 * lam)) + 2 * max(Px, Py)
    ext = reach + 2 * math.sqrt(max(1.0, (reach / Px + 1) * (reach / Py + 1)) * m_cell / (4 * lam))
    nx = int(math.ceil(ext / Px)) + 1; ny = int(math.ceil(ext / Py)) + 1
    I, J = np.meshgrid(np.arange(-nx, nx + 1), np.arange(-ny, ny + 1), indexing='ij')
    I = I.ravel(); J = J.ravel()
    P = np.array(pts, float)
    px = np.ascontiguousarray((P[None, :, 0] + I[:, None] * Px).ravel())
    py = np.ascontiguousarray((P[None, :, 1] + J[:, None] * Py).ravel())
    pm = np.ascontiguousarray(np.broadcast_to(P[None, :, 2], (len(I), len(P))).ravel())
    gx = np.ascontiguousarray((np.arange(n) + 0.5) / n * Px); gy = np.ascontiguousarray((np.arange(n) + 0.5) / n * Py)
    out = np.zeros(n * n, np.uint8)
    dp = ctypes.POINTER(ctypes.c_double)
    _lib.coverage_grid(len(px), px.ctypes.data_as(dp), py.ctypes.data_as(dp), pm.ctypes.data_as(dp), lam, 0.0, Px, 0.0,
                       Py, reach, n, gx.ctypes.data_as(dp), n, gy.ctypes.data_as(dp),
                       out.ctypes.data_as(ctypes.POINTER(ctypes.c_ubyte)))
    return gx, gy, out.reshape(n, n) == 0
