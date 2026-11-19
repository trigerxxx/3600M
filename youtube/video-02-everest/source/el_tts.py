"""Озвучка ElevenLabs: каждая часть сценария → build/<id>.wav (паузы между предложениями через <break>)."""
import json, os, re, subprocess, urllib.request
from script import SEGMENTS
B = "build"
VOICE = "nPczCjzI2devNBz1zQrb"   # Brian
SPECIAL = {"sp_radio": ("JBFqnCBsd6RMkjVDRZzb", "Ilyas, this is base camp. Do you copy? Ilyas, come in."),
           "sp_whisper": ("EXAVITQu4vr4xnSDxMaL", "Ilyas... Ilyas...")}

def tts(text, voice, out, prev="", nxt="", speed=0.94, stability=0.42):
    if os.path.exists(out): return
    body = dict(text=text, model_id="eleven_multilingual_v2", previous_text=prev, next_text=nxt,
                voice_settings=dict(stability=stability, similarity_boost=0.8, style=0.3, speed=speed))
    req = urllib.request.Request(f"https://api.elevenlabs.io/v1/text-to-speech/{voice}?output_format=mp3_44100_128",
                                 data=json.dumps(body).encode(), headers={"xi-api-key": "proxy-injected", "Content-Type": "application/json"})
    mp3 = out[:-4] + ".mp3"
    open(mp3, "wb").write(urllib.request.urlopen(req, timeout=120).read())
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", mp3, "-ac", "1", "-ar", "44100", out], check=True)

texts = [s for s in SEGMENTS if s["text"]]
for i, s in enumerate(texts):
    t = re.sub(r"(?<=[.!?])\s+", ' <break time="0.6s" /> ', s["text"])
    tts(t, VOICE, f"{B}/{s['id']}.wav", texts[i-1]["text"] if i else "", texts[i+1]["text"] if i + 1 < len(texts) else "")
    print(s["id"], flush=True)
for k, (v, t) in SPECIAL.items():
    tts(t, v, f"{B}/{k}.wav", speed=1.0, stability=0.5)
