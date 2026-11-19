import os, subprocess, wave, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from script import SEGMENTS
SC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
tot = 0
for s in SEGMENTS:
    if not s["text"]: tot += s["dur"]; continue
    wav = f"build/{s['id']}.wav"
    if not os.path.exists(wav):
        subprocess.run([f"{SC}/tts/bin/piper", "-m", f"{SC}/voices/en_US-ryan-high.onnx", "--length-scale", "1.3",
                        "--sentence-silence", "0.75", "-f", wav], input=s["text"].encode(), check=True, stderr=subprocess.DEVNULL)
    with wave.open(wav) as w: d = w.getnframes() / w.getframerate()
    tot += d + 1.8
    print(s["id"], round(d, 1))
print("TOTAL", round(tot / 60, 2), "min")
