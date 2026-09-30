import os, sys, numpy as np
from multiprocessing import Pool
from crown import render

FPS = 30
OUT = "cache"
os.makedirs(OUT, exist_ok=True)

def yaw(f): return 0.35 + f/FPS*0.75

def ease(t):
    t = min(max(t, 0), 1)
    return t*t*(3-2*t)

def reveal(f):
    return ease((f-84)/96)

def job(f):
    p = f"{OUT}/c{f:04d}.png"
    if os.path.exists(p): return
    r = reveal(f)
    img = render(yaw(f), size=760, scale=200, reveal=r if r < 1 else 1.0)
    img.save(p)

if __name__ == "__main__":
    frames = list(range(78, 450))
    with Pool(2) as pool:
        for i, _ in enumerate(pool.imap_unordered(job, frames)):
            if i % 40 == 0: print(i, flush=True)
    print("done")
