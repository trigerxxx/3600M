# Исходники графики

- `keyart.py` — сцена ключевого арта для Blender (строится кодом).
  `blender -b --factory-startup -P keyart.py -- out.png 1080 1920 48`
- `post.py` — свечение, цвет, виньетка, заголовок: `python3 post.py out.png keyart.png`
- `ui_mockups.py` — генератор SVG-макетов экранов в `art/ui/` (пути внутри файла).
