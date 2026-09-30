"""Procedural zirconia molar crown + fast point-splat renderer (numpy only).
Renders RGBA frames of a rotating crown, cached and reused for every lab video."""
import numpy as np
from PIL import Image

def crown_mesh(nt=1300, nf=900):
    th = np.linspace(0, 2*np.pi, nt, endpoint=False)
    ph = np.linspace(0.0, np.pi*0.98, nf)
    T, P = np.meshgrid(th, ph)              # rows = phi, cols = theta
    # superquadric-ish horizontal section (rounded square molar outline)
    c, s = np.cos(T), np.sin(T)
    n = 3.2
    rr = (np.abs(c)**n + np.abs(s)**n)**(-1/n)
    cx = rr*c
    sy = rr*s
    Rx, Ry = 1.0, 0.88
    sp = np.sin(P)
    # upper dome (phi<pi/2) squashed; lower part = tapered axial wall to margin
    upper = P <= np.pi/2
    zt = np.where(upper, 0.55*np.cos(P), -0.72*(P-np.pi/2)/(np.pi/2))
    rad = np.where(upper, sp, 1.0 - 0.13*np.clip((P-np.pi/2)/(np.pi/2),0,None)**1.3)
    # height of equator bulge (height of contour)
    rad = rad*(1 + 0.05*np.exp(-((P-np.pi*0.52)/0.18)**2))
    x = Rx*rad*cx
    y = Ry*rad*sy
    # occlusal anatomy: 4 cusps, central fossa, grooves (only on top)
    w = np.clip(np.cos(P), 0, 1)**1.2
    cusps = [(0.42, 0.36, 0.30), (-0.40, 0.36, 0.26), (0.44, -0.38, 0.28), (-0.38, -0.36, 0.24)]
    bump = np.zeros_like(x)
    for (ux, uy, a) in cusps:
        bump += a*np.exp(-(((x-ux)/0.33)**2 + ((y-uy)/0.30)**2))
    fossa = 0.22*np.exp(-((x/0.22)**2 + (y/0.20)**2))
    groove = 0.10*np.exp(-(y/0.05)**2)*np.exp(-(x/0.62)**2) + 0.08*np.exp(-(x/0.05)**2)*np.exp(-(y/0.55)**2)
    z = zt + w*(bump - fossa - groove) + 0.18*w
    # tiny surface texture for realism
    z += w*0.006*np.sin(23*x)*np.sin(19*y)
    V = np.stack([x, y, z], -1)
    # normals via finite differences
    dT = np.roll(V, -1, 1) - np.roll(V, 1, 1)
    dP = np.gradient(V, axis=0)
    N = np.cross(dT, dP)
    N /= np.linalg.norm(N, axis=-1, keepdims=True) + 1e-9
    # make normals point outward
    cen = V.reshape(-1,3).mean(0)
    if np.mean(np.sum(N*(V-cen), -1)) < 0:
        N = -N
    return V.reshape(-1, 3), N.reshape(-1, 3), P.reshape(-1)

_V, _N, _P = crown_mesh()
MARGIN_IDX = None

def rot(yaw, pitch):
    cy, sy = np.cos(yaw), np.sin(yaw)
    cp, sp = np.cos(pitch), np.sin(pitch)
    Rz = np.array([[cy, -sy, 0], [sy, cy, 0], [0, 0, 1]])
    Rx = np.array([[1, 0, 0], [0, cp, -sp], [0, sp, cp]])
    return Rx @ Rz

def render(yaw, pitch=0.62, size=900, scale=235, mode="solid", reveal=1.0, margin=0.0,
           teal=(32, 201, 187)):
    """mode solid; reveal 0..1 = fraction of points shown as solid (rest as teal scan dots);
    margin 0..1 = fraction of margin line traced."""
    S = size*2
    R = rot(yaw, pitch)
    V = _V @ R.T
    N = _N @ R.T
    px = (V[:, 0]*scale*2 + S/2).astype(np.int32)
    py = (-V[:, 2]*scale*2 + S/2 - 0.05*scale*2).astype(np.int32)  # z up on screen
    depth = V[:, 1]
    # lighting
    L = np.array([-0.45, -0.75, 0.5]); L /= np.linalg.norm(L)
    Vd = np.array([0, -1.0, 0])
    ndl = np.clip(N @ L, 0, 1)
    H = (L + Vd); H /= np.linalg.norm(H)
    spec = np.clip(N @ H, 0, 1)**48
    rim = np.clip(1 - np.abs(N @ Vd), 0, 1)**3
    base = np.array([238, 232, 220], float)  # ivory zirconia
    col = base*(0.42 + 0.66*ndl[:, None]) + 255*0.55*spec[:, None] + np.array(teal)*0.55*rim[:, None]
    # facing mask (backface) -> inner surface darker
    facing = (N @ Vd) > -0.05
    col[~facing] *= 0.35
    col = np.clip(col, 0, 255)
    alpha = np.full(len(px), 255.0)
    if reveal < 1.0:
        # dissolve: points above a moving threshold are shown as sparse teal scan dots
        rng = np.random.default_rng(7)
        key = (_V[:, 2] - _V[:, 2].min())/(np.ptp(_V[:, 2])) * 0.8 + rng.random(len(px))*0.2
        solid = key < reveal
        dot = (~solid) & (rng.random(len(px)) < 0.05)
        col[~solid] = np.array(teal)
        alpha[~solid] = 0
        alpha[dot] = 230
    ok = (px >= 2) & (px < S-3) & (py >= 2) & (py < S-3) & (alpha > 0) & ((N @ Vd) > -0.15)
    idx_l, d_l, c_l, a_l = [], [], [], []
    base_idx = py[ok]*S + px[ok]
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            idx_l.append(base_idx + dy*S + dx)
    idx = np.concatenate(idx_l)
    dd = np.tile(depth[ok], 9)
    cc = np.tile(col[ok], (9, 1))
    aa = np.tile(alpha[ok], 9)
    o = np.lexsort((dd, idx))
    idx, dd, cc, aa = idx[o], dd[o], cc[o], aa[o]
    u, first = np.unique(idx, return_index=True)
    img = np.zeros((S*S, 4), np.float32)
    img[u, :3] = cc[first]
    img[u, 3] = aa[first]
    img = img.reshape(S, S, 4)
    out = Image.fromarray(img.astype(np.uint8), "RGBA").resize((size, size), Image.LANCZOS)
    return out

if __name__ == "__main__":
    import time
    t = time.time()
    render(0.6).save("crown_test.png")
    render(0.6, reveal=0.5).save("crown_reveal.png")
    c=render(0.6); c.alpha_composite(margin_overlay(0.6,0.7)); c.save("crown_margin.png")
    print("s", time.time()-t)


def margin_overlay(yaw, frac, pitch=0.62, size=900, scale=235, teal=(32, 201, 187)):
    """Glowing margin line, only the visible (front) part, traced up to frac."""
    from PIL import ImageDraw, ImageFilter
    nt = 1300
    R = rot(yaw, pitch)
    ring = _V[-nt:] @ R.T
    nrm = _N[-nt:] @ R.T
    vis = (nrm @ np.array([0, -1.0, 0])) > 0.02
    k = max(2, int(nt*frac))
    xs = ring[:, 0]*scale + size/2
    ys = -ring[:, 2]*scale + size/2 - 0.05*scale
    segs, cur = [], []
    for i in range(k):
        if vis[i]:
            cur.append((float(xs[i]), float(ys[i])))
        elif cur:
            segs.append(cur); cur = []
    if cur: segs.append(cur)
    glow = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(glow)
    for sg in segs:
        if len(sg) > 1: d.line(sg, fill=teal+(255,), width=12)
    glow = glow.filter(ImageFilter.GaussianBlur(9))
    d = ImageDraw.Draw(glow)
    for sg in segs:
        if len(sg) > 1: d.line(sg, fill=(190, 255, 248, 255), width=4)
    # moving "pen" dot at the tracing head
    i = k-1
    if vis[i]:
        x, y = float(xs[i]), float(ys[i])
        d.ellipse([x-9, y-9, x+9, y+9], fill=(255, 255, 255, 255))
    return glow
