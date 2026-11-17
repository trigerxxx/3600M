"""Файл монтажа для DaVinci Resolve (File → Import → Timeline → FCPXML).
Кладите рядом: crash.mp4, radio.png, title.png, sound.wav."""
from xml.sax.saxutils import escape

FPS = 24
def tc(sec):  # время в формате FCPXML
    return f"{round(sec * FPS)}/{FPS}s"

clips = [  # (имя, файл, начало, длительность)
    ("Крушение", "crash.mp4", 0.0, 106 / 24),
    ("Рация", "radio.png", 106 / 24 + 0.4, 3.2),
    ("Титул 33 DAYS", "title.png", 106 / 24 + 0.4 + 3.2, 4.2),
]
total = 106 / 24 + 0.4 + 3.2 + 4.2

assets = []
for i, (name, f, _, dur) in enumerate(clips, start=1):
    vid = 'hasVideo="1"'
    dur_attr = tc(dur) if f.endswith(".mp4") else "0s"
    assets.append(f'<asset id="r{i+1}" name="{escape(name)}" src="file:./{f}" start="0s" duration="{dur_attr}" {vid} format="r1"/>')
assets.append(f'<asset id="r9" name="Звук" src="file:./sound.wav" start="0s" duration="{tc(total)}" hasAudio="1" audioSources="1" audioChannels="2" audioRate="48000"/>')

spine = []
cursor = 0.0
for i, (name, f, start, dur) in enumerate(clips, start=1):
    if start > cursor:
        spine.append(f'<gap name="Пауза" offset="{tc(cursor)}" duration="{tc(start - cursor)}" start="0s"/>')
    tag = "asset-clip" if f.endswith(".mp4") else "video"
    inner = ""
    if i == 1:
        inner = f'<asset-clip ref="r9" lane="-1" name="Звук" offset="0s" duration="{tc(total)}" start="0s"/>'
    spine.append(f'<{tag} ref="r{i+1}" name="{escape(name)}" offset="{tc(start)}" duration="{tc(dur)}" start="0s">{inner}</{tag}>')
    cursor = start + dur

xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE fcpxml>
<fcpxml version="1.9">
  <resources>
    <format id="r1" name="FFVideoFormat720p24" frameDuration="1/24s" width="1280" height="720"/>
    {chr(10).join("    " + a for a in assets)}
  </resources>
  <library>
    <event name="33 Days трейлер">
      <project name="Тизер крушения">
        <sequence format="r1" duration="{tc(total)}" tcStart="0s" tcFormat="NDF">
          <spine>
            {chr(10).join("            " + s for s in spine)}
          </spine>
        </sequence>
      </project>
    </event>
  </library>
</fcpxml>
'''
open("teaser.fcpxml", "w").write(xml)
print("ok")
