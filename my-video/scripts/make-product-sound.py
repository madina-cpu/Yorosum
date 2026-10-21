"""Synthesises the original soundtrack for the Glow Peptide intro.

Run: python3 scripts/make-product-sound.py  ->  public/audio/glow-peptide-intro.wav
Scene starts match src/ProductIntro.tsx (663 frames at 30 fps, 0.4 s fades).
"""
import os
import wave

import numpy as np

SR = 48000
DUR = 663 / 30
N = int(SR * DUR)
t = np.arange(N) / SR
rng = np.random.default_rng(11)

# Opening, Hero, Per stick, In the box, Flavour, How to enjoy, End card.
SCENES = [0.0, 2.6, 5.7, 9.8, 12.4, 15.0, 18.1]


def env(start, attack, hold, release):
    """Smooth (raised-cosine) attack/hold/release envelope."""
    e = np.zeros(N)
    a1 = start + attack
    h1 = a1 + hold
    r1 = h1 + release
    m = (t >= start) & (t < a1)
    e[m] = 0.5 - 0.5 * np.cos(np.pi * (t[m] - start) / attack)
    e[(t >= a1) & (t < h1)] = 1
    m = (t >= h1) & (t < r1)
    e[m] = 0.5 + 0.5 * np.cos(np.pi * (t[m] - h1) / release)
    return e


def bandpass(x, lo, hi):
    spec = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    centre = np.log((lo * hi) ** 0.5)
    shape = np.exp(-0.5 * ((np.log(f + 1) - centre) / np.log(hi / lo) * 2.2) ** 2)
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


def pad_chord(freqs, start, length):
    p = np.zeros(N)
    for f in freqs:
        for detune in (-0.6, 0.6):
            p += np.sin(2 * np.pi * (f + detune) * t + rng.uniform(0, 6.28))
            p += 0.25 * np.sin(2 * np.pi * 2 * (f + detune) * t)
    return p / 20 * env(start, 0.9, max(length - 1.8, 0.1), 0.9)


left = np.zeros(N)
right = np.zeros(N)

# Breath as the mark draws.
breath = env(0.25, 0.9, 0.1, 0.9) ** 1.5
left += 0.14 * bandpass(rng.standard_normal(N), 350, 2600) * breath
right += 0.14 * bandpass(rng.standard_normal(N), 350, 2600) * breath

# Calm pad moving D -> Bm -> G -> A -> D, overlapping across scene changes.
D3, E3, Fs3, G3, A3, B3 = 146.83, 164.81, 185.0, 196.0, 220.0, 246.94
chords = [
    ((D3, A3, 329.63, 369.99), 0.0, 6.2),
    ((B3 / 2, Fs3, D3 * 2, A3 * 2), 5.3, 4.9),
    ((G3 / 2 * 2, B3, D3 * 2, Fs3 * 2), 9.4, 5.9),
    ((A3 / 2 * 2, E3 * 2, A3 * 2, 2 * 246.94), 14.6, 3.9),
    ((D3, A3, 329.63, 369.99), 17.7, DUR - 17.7),
]
pad = sum(pad_chord(*c) for c in chords)
pad *= 0.85 + 0.15 * np.sin(2 * np.pi * 0.22 * t)
left += 0.9 * pad
right += 0.9 * np.roll(pad, int(0.012 * SR))

# Soft chimes on each new scene, three ticks for the per-stick figures.
notes = [None, 739.99, 880.0, 659.25, 739.99, 880.0, 1174.66]
for start, freq in zip(SCENES, notes):
    if freq:
        c = bell(start + 0.15, freq, 0.12)
        left += c
        right += 0.75 * c
for i, freq in enumerate((587.33, 739.99, 880.0)):
    c = bell(SCENES[2] + 0.3 + 0.6 * i, freq, 0.07, decay=0.9)
    left += 0.75 * c
    right += c

mix = np.stack([left, right], axis=1)
mix *= env(0, 0.01, DUR - 0.81, 0.8)[:, None]
mix *= 0.7 / np.abs(mix).max()

out = os.path.join(os.path.dirname(__file__), "..", "public", "audio", "glow-peptide-intro.wav")
os.makedirs(os.path.dirname(out), exist_ok=True)
with wave.open(out, "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes((mix * 32767).astype("<i2").tobytes())
print("wrote", os.path.normpath(out))
