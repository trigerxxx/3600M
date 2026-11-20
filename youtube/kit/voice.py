"""Озвучка ElevenLabs с временем каждого слова.
Ключ хранится в настройках окружения (Network secrets для api.elevenlabs.io) и подставляется прокси,
поэтому в коде вместо ключа стоит заглушка. Никогда не вписывать настоящий ключ в код и в чат."""
import base64
import json
import os
import subprocess
import urllib.request

VOICES = {
    "brian": "nPczCjzI2devNBz1zQrb",    # низкий американский, рассказчик (по умолчанию)
    "george": "JBFqnCBsd6RMkjVDRZzb",   # тёплый британский
    "bill": "pqHfZKP75CvOlQylNhV4",     # взрослый, документальный
    "sarah": "EXAVITQu4vr4xnSDxMaL",    # женский, мягкий
    "eric": "cjVigY5qzO86Huf0OWal",     # гладкий американский «продавец» — ГОЛОС ВОЛКА (выбор автора)
}


def say(text, out_wav, voice="brian", prev="", nxt="", speed=1.0, stability=0.4, style=0.35):
    """Озвучить text → out_wav (44.1 кГц, моно). Возвращает список слов [(start, end, word)] в секундах."""
    meta = out_wav[:-4] + ".json"
    if os.path.exists(out_wav) and os.path.exists(meta):
        return json.load(open(meta))
    body = dict(text=text, model_id="eleven_multilingual_v2", previous_text=prev, next_text=nxt,
                voice_settings=dict(stability=stability, similarity_boost=0.8, style=style, speed=speed))
    vid = VOICES.get(voice, voice)
    req = urllib.request.Request(
        f"https://api.elevenlabs.io/v1/text-to-speech/{vid}/with-timestamps?output_format=mp3_44100_128",
        data=json.dumps(body).encode(), headers={"xi-api-key": "proxy-injected", "Content-Type": "application/json"})
    d = json.loads(urllib.request.urlopen(req, timeout=180).read())
    mp3 = out_wav[:-4] + ".mp3"
    open(mp3, "wb").write(base64.b64decode(d["audio_base64"]))
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", mp3, "-ac", "1", "-ar", "44100", out_wav], check=True)
    a = d["alignment"]
    words, cur, t0, t1 = [], "", None, None
    for ch, s, e in zip(a["characters"], a["character_start_times_seconds"], a["character_end_times_seconds"]):
        if ch.isspace():
            if cur:
                words.append((t0, t1, cur))
            cur, t0 = "", None
            continue
        if t0 is None:
            t0 = s
        cur += ch
        t1 = e
    if cur:
        words.append((t0, t1, cur))
    json.dump(words, open(meta, "w"))
    return words
