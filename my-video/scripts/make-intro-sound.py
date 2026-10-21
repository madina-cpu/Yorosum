"""Synthesises the original soundtrack for the Yorosum logo intro.

Run: python3 scripts/make-intro-sound.py  ->  public/audio/yorosum-intro.wav
Timings match src/LogoIntro.tsx (9 s at 30 fps).
"""
import os
import wave

import numpy as np

SR = 48000
DUR = 9.0
N = int(SR * DUR)
t = np.arange(N) / SR
rng = np.random.default_rng(7)


def env(start, attack, hold, release):
    """Smooth (raised-cosine) attack/hold/release envelope."""
    e = np.zeros(N)
    a0, a1 = start, start + attack
    h1 = a1 + hold
    r1 = h1 + release
    m = (t >= a0) & (t < a1)
    e[m] = 0.5 - 0.5 * np.cos(np.pi * (t[m] - a0) / attack)
    e[(t >= a1) & (t < h1)] = 1
    m = (t >= h1) & (t < r1)
    e[m] = 0.5 + 0.5 * np.cos(np.pi * (t[m] - h1) / release)
    return e


def bandpass(x, lo, hi):
    spec = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    shape = np.exp(-0.5 * ((np.log(f + 1) - np.log((lo * hi) ** 0.5)) / np.log(hi / lo) * 2.2) ** 2)
    return np.fft.irfft(spec * shape, len(x))


def bell(start, freq, amp, decay=2.4):
    out = np.zeros(N)
    m = t >= start
    tt = t[m] - start
    tone = (np.sin(2 * np.pi * freq * tt)
            + 0.35 * np.sin(2 * np.pi * freq * 2.0 * tt) * np.exp(-tt * 1.5)
            + 0.12 * np.sin(2 * np.pi * freq * 3.01 * tt) * np.exp(-tt * 3))
    out[m] = amp * tone * np.exp(-tt / decay) * np.minimum(tt / 0.008, 1)
    return out


left = np.zeros(N)
right = np.zeros(N)

# 1. Soft low tap as the centre dot appears.
tap = bell(0.05, 196.0, 0.22, decay=0.5)
left += tap
right += tap

# 2. The "breath": airy filtered noise swelling while the arcs draw outward.
breath_env = env(0.25, 0.9, 0.1, 0.9) ** 1.5
left += 0.55 * bandpass(rng.standard_normal(N), 350, 2600) / 4 * breath_env
right += 0.55 * bandpass(rng.standard_normal(N), 350, 2600) / 4 * breath_env

# 3. Warm pad (D add9) that rises with the wordmark and gently "breathes".
pad = np.zeros(N)
for f in (146.83, 220.0, 329.63, 369.99):
    for detune in (-0.6, 0.6):
        pad += np.sin(2 * np.pi * (f + detune) * t + rng.uniform(0, 6.28))
        pad += 0.25 * np.sin(2 * np.pi * 2 * (f + detune) * t)
pad /= 20
pad *= env(2.6, 1.8, 3.0, 1.6) * (0.85 + 0.15 * np.sin(2 * np.pi * 0.22 * t))
left += 0.9 * pad
right += 0.9 * np.roll(pad, int(0.012 * SR))

# 4. Chimes: one as YOROSUM rises, one for the tagline.
c1 = bell(3.0, 739.99, 0.16)
c2 = bell(5.6, 880.0, 0.11, decay=2.8)
left += c1 + 0.7 * c2
right += 0.7 * c1 + c2

mix = np.stack([left, right], axis=1)
mix *= env(0, 0.01, DUR - 0.31, 0.3)[:, None]
mix *= 0.7 / np.abs(mix).max()

out = os.path.join(os.path.dirname(__file__), "..", "public", "audio", "yorosum-intro.wav")
os.makedirs(os.path.dirname(out), exist_ok=True)
with wave.open(out, "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes((mix * 32767).astype("<i2").tobytes())
print("wrote", os.path.normpath(out))
