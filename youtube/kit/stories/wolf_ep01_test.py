"""Тест канала Волка: первые ~40 секунд «How Inflation Fleeces You» (голос, анимация, удержание)."""
from cartoon import sheep_shot, title_shot, wolf_shot, word_shot
from kit import block

STORY = dict(name="wolf-ep01-test", accent=(214, 40, 40), voice="eric", speed=1.0, end_hold=1.0)

BLOCKS = [
    block("Hello, sheep.",
          shots=[(0, wolf_shot("stand", "bust", x=0.42))], mood="hope", amb="silence", pause=0.35),
    block("I'm a wolf. I work in *finance*.",
          shots=[(0, wolf_shot("stand", "full", x=0.35, text="FINANCE", text_at="finance"))], mood="hope", amb="silence", pause=0.3),
    block("Today I'm going to show you how you lose *wool* every single year, without anyone *touching* you.",
          shots=[(0, sheep_shot(1.0, 1.0, "calm", label="YOUR WOOL")),
                 ("without", sheep_shot(1.0, 0.45, "sad", label="NOBODY TOUCHED HER", label_color=(214, 40, 40)))],
          sfx=[("touching", "heart")], mood="tense", amb="silence", pause=0.3),
    block("It's called *inflation*.",
          shots=[(0, word_shot("INFLATION", "the haircut nobody sees"))], mood="tense", amb="silence", pause=0.4),
    block("And honestly? It's my favourite *haircut*.",
          shots=[(0, wolf_shot("shears", "bust", x=0.38))], sfx=[("haircut", "snip")], mood="hope", amb="silence", pause=0.3),
    block("And at the end, I'll show you exactly who is holding the *scissors*.",
          shots=[(0, wolf_shot("present", "full", x=0.3, prop="note")),
                 ("scissors", title_shot("HOW INFLATION\nFLEECES YOU", "explained by a wolf"))],
          mood="tense", amb="silence", pause=2.2),
    block("First, the rules. In this world, wool is *wealth*. A fluffy sheep is a *rich* sheep. A bald sheep… well. You'll see.",
          shots=[(0, sheep_shot(1.0, 1.0, "calm", label="WOOL = WEALTH", wolf=True)),
                 ("bald", sheep_shot(0.0, 0.0, "shock", label="…", gary=True)),
                 ("see", wolf_shot("stand", "bust", x=0.42))],
          sfx=[("bald", "hit")], mood="hope", amb="silence", pause=1.0),
]
