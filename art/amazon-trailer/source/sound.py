"""Звук черновика: гул двигателей и сирена → удар → тишина → птицы и треск рации → гул титра."""
import wave
import numpy as np

SR = 48000
DUR = 13.0
n = int(SR * DUR)
t = np.arange(n) / SR
rng = np.random.default_rng(3)
IMPACT = 92 / 24  # 3.83 с
mix = np.zeros(n)

def env(a, b, fa=0.2, fb=0.2):
    return np.clip((t - a) / fa, 0, 1) * np.clip((b - t) / fb, 0, 1)

def lowpass(x, cut):
    a = np.exp(-2 * np.pi * cut / SR)
    y = np.empty_like(x); acc = 0.0
    for i in range(len(x)):
        acc = (1 - a) * x[i] + a * acc; y[i] = acc
    return y

# гул реактивного двигателя, нарастает и «срывается» вниз
pitch = 90 + 60 * np.clip(t / IMPACT, 0, 1)
engine = np.sin(2 * np.pi * np.cumsum(pitch) / SR) * 0.25
roar = lowpass(rng.standard_normal(n), 900) * 0.9
mix += (engine + roar) * env(0, IMPACT, 0.3, 0.02) * (0.4 + 0.6 * np.clip(t / IMPACT, 0, 1))
# сирена в кабине
siren = np.sign(np.sin(2 * np.pi * 2.0 * t)) * 0.5 + 0.5
mix += np.sin(2 * np.pi * (700 + 300 * siren) * t) * 0.07 * env(1.0, IMPACT, 0.1, 0.02)
# удар: низкий бум + треск
k = t >= IMPACT
boom = np.sin(2 * np.pi * (55 - 20 * np.clip(t - IMPACT, 0, 1)) * t) * np.exp(-np.clip(t - IMPACT, 0, None) * 2.0) * k
crack = rng.standard_normal(n) * np.exp(-np.clip(t - IMPACT, 0, None) * 5) * k
mix += boom * 1.0 + crack * 0.5
# птицы после тишины (с 6 с)
for i in range(14):
    st = 6.2 + rng.uniform(0, 3.5)
    f0 = rng.uniform(2500, 4200)
    d = 0.12
    m = (t >= st) & (t < st + d)
    tt = t[m] - st
    mix[m] += np.sin(2 * np.pi * (f0 + 1500 * np.sin(2 * np.pi * 12 * tt)) * tt) * np.sin(np.pi * tt / d) * 0.12
# треск рации под субтитр (5.5–8.5 с)
mix += rng.standard_normal(n) * 0.05 * env(5.5, 8.5, 0.05, 0.3) * (0.6 + 0.4 * np.sin(2 * np.pi * 7 * t))
# гул под титр
mix += (np.sin(2 * np.pi * 55 * t) + np.sin(2 * np.pi * 82.5 * t)) * 0.12 * env(9.0, DUR, 0.8, 1.0)

mix = mix / np.abs(mix).max() * 0.85
st = np.stack([mix, np.roll(mix, 200)], 1)
with wave.open("sound.wav", "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((st * 32767).astype(np.int16).tobytes())
print("ok")
