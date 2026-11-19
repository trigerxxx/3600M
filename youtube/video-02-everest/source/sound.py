"""Звуковой дизайн: всё синтезируется кодом (без чужих записей → без проблем с правами)."""
import numpy as np
from scipy.signal import butter, fftconvolve, sosfilt

SR = 44100
R = np.random.default_rng(11)


def t_(d):
    return np.arange(int(d * SR)) / SR


def noise(d, rng=R):
    return rng.standard_normal(int(d * SR))


def brown(d, rng=R):
    x = np.cumsum(rng.standard_normal(int(d * SR)))
    x = x - sosfilt(butter(1, 5, "hp", fs=SR, output="sos"), x) * 0 - np.convolve(x, np.ones(4410) / 4410, "same")
    return x / (np.abs(x).max() + 1e-9)


def bp(x, lo, hi, order=2):
    return sosfilt(butter(order, [lo, hi], "bp", fs=SR, output="sos"), x)


def lp(x, f, order=2):
    return sosfilt(butter(order, f, "lp", fs=SR, output="sos"), x)


def hp(x, f, order=2):
    return sosfilt(butter(order, f, "hp", fs=SR, output="sos"), x)


def env(n, a, r, shape=2.0):
    """атака a сек, затухание r сек (экспонента)."""
    t = np.arange(n) / SR
    e = np.where(t < a, (t / max(a, 1e-4)), np.exp(-(t - a) / max(r, 1e-4) * shape))
    return e


def norm(x, peak=1.0):
    m = np.abs(x).max()
    return x / m * peak if m > 0 else x


def lfo_noise(d, rate, rng=R):
    """медленная случайная огибающая 0..1"""
    n = int(d * SR)
    k = max(2, int(d * rate) + 2)
    pts = rng.uniform(0, 1, k)
    return np.interp(np.linspace(0, k - 1, n), np.arange(k), pts)


def st(x, pan=0.0):
    l, r = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
    return np.stack([x * l * 1.414, x * r * 1.414], 1)


def reverb(x, d=2.2, wet=0.3, rng=np.random.default_rng(5)):
    n = int(d * SR)
    ir = rng.standard_normal((n, 2)) * np.exp(-np.arange(n) / SR * 6.9 / d)[:, None]
    ir = np.stack([lp(ir[:, 0], 6000), lp(ir[:, 1], 6000)], 1)
    ir /= np.sqrt((ir ** 2).sum(0))
    if x.ndim == 1:
        x = st(x)
    y = np.stack([fftconvolve(x[:, c], ir[:, c])[: len(x)] for c in range(2)], 1)
    return x * (1 - wet) + y * wet


# ---------------- фоны ----------------
def amb(kind, d, seed):
    rng = np.random.default_rng(seed)
    n = int(d * SR)
    if kind == "silence":
        x = hp(rng.standard_normal(n), 2000) * 0.004
        return st(x)
    base = {"storm": (900, 1.0, 0.7), "wind": (600, 0.55, 0.45), "wind_soft": (400, 0.3, 0.25),
            "tent": (260, 0.32, 0.12), "camp": (450, 0.25, 0.2)}[kind]
    out = np.zeros((n, 2))
    for ch in range(2):
        g = 0.4 + 0.6 * lfo_noise(d, 0.35, rng) ** 1.5
        rumble = lp(rng.standard_normal(n), base[0], 2) * g
        whistle = bp(rng.standard_normal(n), 700 + 500 * ch, 1100 + 600 * ch, 4) * (lfo_noise(d, 0.25, rng) ** 3) * base[2]
        out[:, ch] = norm(rumble) * base[1] + norm(whistle) * base[2] * 0.6
    if kind in ("tent", "storm"):
        # дрожь ткани
        fl = bp(rng.standard_normal(n), 120, 900) * (lfo_noise(d, 3.0, rng) ** 4)
        out += st(norm(fl) * (0.25 if kind == "tent" else 0.35))
    return out * 0.32


# ---------------- музыка ----------------
NOTES = {"dark": [38, 45, 50, 53], "tense": [38, 44, 50, 51], "hope": [41, 48, 53, 57, 60]}


def mtof(m):
    return 440 * 2 ** ((m - 69) / 12)


def pad(mood, d, seed):
    rng = np.random.default_rng(seed)
    t = t_(d)
    x = np.zeros((len(t), 2))
    for i, m in enumerate(NOTES[mood]):
        for ch, det in enumerate((-0.12, 0.12)):
            f = mtof(m) * 2 ** (det / 12)
            ph = rng.uniform(0, 6.28)
            w = sum(np.sin(2 * np.pi * f * k * t + ph * k) / k ** 1.6 for k in range(1, 6))
            x[:, ch] += w * (0.9 if i == 0 else 0.5) * (0.6 + 0.4 * np.sin(2 * np.pi * (0.05 + 0.03 * i) * t + ph))
    x = np.stack([lp(x[:, c], 1400 if mood == "hope" else 800) for c in range(2)], 1)
    if mood == "tense":
        pulse = (np.sin(2 * np.pi * 0.9 * t) > 0.96).astype(float)
        sub = lp(pulse, 60) * np.sin(2 * np.pi * 45 * t)
        x += st(norm(sub) * 0.5)
    return norm(x) * 0.22


# ---------------- эффекты ----------------
def fx(name, seed=0, voice_fn=None):
    rng = np.random.default_rng(seed + hash(name) % 1000)
    if name == "boom":
        t = t_(3.0)
        f = 70 * np.exp(-t * 1.2) + 28
        x = np.sin(2 * np.pi * np.cumsum(f) / SR) * env(len(t), 0.005, 0.9)
        x += lp(rng.standard_normal(len(t)), 900) * env(len(t), 0.002, 0.08) * 0.8
        return reverb(st(norm(x)), 3.0, 0.35) * 0.95
    if name == "hit":
        t = t_(1.2)
        x = np.sin(2 * np.pi * 110 * t * np.exp(-t * 2)) * env(len(t), 0.003, 0.25)
        x += bp(rng.standard_normal(len(t)), 300, 3000) * env(len(t), 0.001, 0.04)
        return reverb(st(norm(x)), 2.0, 0.3) * 0.6
    if name == "whoosh":
        d = 1.0
        n = int(d * SR)
        x = rng.standard_normal(n)
        e = np.sin(np.linspace(0, np.pi, n)) ** 2
        segs = [bp(x[i:i + 2205], 300 + 3000 * e[i], 600 + 5000 * e[i]) for i in range(0, n, 2205)]
        y = np.concatenate(segs)[:n] * e
        pan = np.linspace(-0.8, 0.8, n)
        return np.stack([y * np.cos((pan + 1) * np.pi / 4), y * np.sin((pan + 1) * np.pi / 4)], 1) / (np.abs(y).max() + 1e-9) * 0.5
    if name == "riser":
        t = t_(3.0)
        e = (t / 3.0) ** 2.5
        x = np.sin(2 * np.pi * np.cumsum(200 + 900 * e) / SR) * 0.4 + hp(rng.standard_normal(len(t)), 2000) * 0.6
        return reverb(st(x * e), 1.5, 0.3) * 0.45
    if name == "rumble":
        x = lp(rng.standard_normal(int(4 * SR)), 120, 4)
        return st(norm(x) * np.sin(np.linspace(0, np.pi, len(x)))) * 0.8
    if name == "gust":
        n = int(2.8 * SR)
        e = np.sin(np.linspace(0, np.pi, n)) ** 1.5
        x = bp(rng.standard_normal(n), 300, 2500) * e + bp(rng.standard_normal(n), 900, 1300, 4) * e ** 3 * 3
        return st(norm(x), rng.uniform(-0.6, 0.6)) * 0.45
    if name in ("breath", "exhale"):
        parts = []
        if name == "breath":
            n = int(0.8 * SR)
            parts.append(bp(rng.standard_normal(n), 700, 2600) * np.sin(np.linspace(0, np.pi, n)) ** 2 * 0.7)
            parts.append(np.zeros(int(0.15 * SR)))
        n = int(1.3 * SR)
        parts.append(bp(rng.standard_normal(n), 300, 1500) * np.sin(np.linspace(0, np.pi, n)) ** 1.5)
        return reverb(st(norm(np.concatenate(parts))), 0.6, 0.15) * 0.32
    if name == "heart":
        t = t_(0.7)
        def thump(a):
            return np.sin(2 * np.pi * 52 * t) * env(len(t), 0.01, 0.09) * a
        x = thump(1.0) + np.roll(thump(0.7), int(0.22 * SR))
        return st(lp(x, 160)) * 0.9
    if name == "crunch":
        n = int(0.3 * SR)
        clicks = (rng.random(n) < 0.05) * rng.standard_normal(n)
        x = bp(clicks + rng.standard_normal(n) * 0.2, 900, 6000) * env(n, 0.03, 0.12)
        return st(norm(x), rng.uniform(-0.3, 0.3)) * 0.4
    if name == "flap":
        out = np.zeros(int(0.9 * SR))
        for k in range(rng.integers(3, 6)):
            s = int(rng.uniform(0, 0.6) * SR)
            n = int(0.12 * SR)
            out[s:s + n] += lp(rng.standard_normal(n), 1800) * env(n, 0.002, 0.03)
        return st(norm(out), rng.uniform(-0.5, 0.5)) * 0.55
    if name == "zip":
        out = np.zeros(int(1.2 * SR))
        times = np.cumsum(np.linspace(0.04, 0.012, 50))
        for tt in times:
            s = int(tt * SR)
            if s + 200 < len(out):
                out[s:s + 200] += hp(rng.standard_normal(200), 2500) * np.exp(-np.arange(200) / 40)
        return st(norm(out)) * 0.35
    if name == "paper":
        n = int(0.6 * SR)
        x = bp(rng.standard_normal(n), 2000, 7000) * (lfo_noise(0.6, 40, rng) ** 3) * env(n, 0.05, 0.3)
        return st(norm(x)) * 0.3
    if name == "beep":
        t = t_(0.18)
        x = np.sin(2 * np.pi * 1950 * t) * (t < 0.12) * env(len(t), 0.003, 0.2)
        return reverb(st(x), 0.5, 0.15) * 0.22
    if name == "click":
        x = hp(rng.standard_normal(int(0.02 * SR)), 1500) * env(int(0.02 * SR), 0.0005, 0.004)
        return st(norm(x)) * 0.35
    if name == "static":
        n = int(2.0 * SR)
        x = bp(rng.standard_normal(n), 400, 3500) * (0.5 + 0.5 * lfo_noise(2.0, 20, rng)) * env(n, 0.01, 1.0, 1.0)
        return st(norm(x)) * 0.25
    if name in ("radio", "whisper") and voice_fn is not None:
        return voice_fn(name, rng)
    if name == "scratch":
        n = int(0.45 * SR)
        x = bp(rng.standard_normal(n), 2500, 8000) * (lfo_noise(0.45, 90, rng) ** 2) * env(n, 0.02, 0.25)
        return st(norm(x)) * 0.35
    if name == "rustle":
        n = int(1.3 * SR)
        x = bp(rng.standard_normal(n), 800, 5000) * (lfo_noise(1.3, 25, rng) ** 3)
        return st(norm(x), rng.uniform(-0.4, 0.4)) * 0.25
    if name == "clink":
        t = t_(0.9)
        x = sum(np.sin(2 * np.pi * f * t) * np.exp(-t * k) for f, k in ((1250, 5), (2830, 8), (4170, 12)))
        return reverb(st(norm(x)), 0.6, 0.2) * 0.22
    if name == "stove":
        n = int(3.5 * SR)
        x = hp(rng.standard_normal(n), 1500) * np.minimum(1, np.arange(n) / (0.3 * SR)) * np.minimum(1, (n - np.arange(n)) / (0.8 * SR))
        x[:400] += rng.standard_normal(400) * np.exp(-np.arange(400) / 60) * 4
        return st(norm(x)) * 0.16
    if name == "drip":
        t = t_(0.15)
        x = np.sin(2 * np.pi * np.cumsum(900 + 2500 * t / 0.15) / SR) * env(len(t), 0.002, 0.05)
        return reverb(st(x), 0.6, 0.25) * 0.3
    if name == "rip":
        n = int(1.4 * SR)
        dens = np.linspace(0.02, 0.4, n)
        cr = (rng.random(n) < dens) * rng.standard_normal(n)
        x = bp(cr + rng.standard_normal(n) * 0.3, 400, 5000) * np.minimum(1, np.arange(n) / (0.1 * SR))
        x[-int(0.15 * SR):] *= np.linspace(1, 0, int(0.15 * SR))
        return reverb(st(norm(x)), 1.0, 0.2) * 0.75
    if name == "stitch":
        n = int(0.5 * SR)
        x = bp(rng.standard_normal(n), 500, 3000) * env(n, 0.01, 0.15)
        x[:300] += rng.standard_normal(300) * np.exp(-np.arange(300) / 50) * 3
        return st(norm(x)) * 0.3
    if name == "ring":
        t = t_(6.0)
        x = np.sin(2 * np.pi * 5800 * t) * np.sin(np.linspace(0, np.pi, len(t))) ** 2
        return st(x) * 0.03
    if name == "swell":
        t = t_(7.0)
        x = np.zeros((len(t), 2))
        for m in (53, 60, 64, 67, 72):
            for ch, det in enumerate((-0.08, 0.08)):
                x[:, ch] += np.sin(2 * np.pi * mtof(m) * 2 ** (det / 12) * t)
        e = np.sin(np.linspace(0, np.pi, len(t))) ** 1.5
        return reverb(x * e[:, None] / 6, 2.5, 0.4) * 0.35
    raise KeyError(name)
