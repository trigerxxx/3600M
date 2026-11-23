"""The Sheep Standard — горячий Shorts: NVIDIA, уход и возвращение CEO (ноябрь 2026). По NEWS-PLAYBOOK: только факты, без политики и личных подробностей.
Факты (проверено 24.11.2026):
- 12 ноября 2026 Дженсен Хуанг ушёл с поста CEO NVIDIA; за неделю компания потеряла почти $500 млрд стоимости (CBS News), капитализация впервые с 2025 г. ниже $4 трлн (Bloomberg, CNBC).
- 23 ноября совет директоров единогласно вернул его (пресс-релиз NVIDIA); акции выросли более чем на 30% за день (Yahoo Finance, NBC News).
Рендер 16:9, всё важное в центре 1440 px (обрезка в 4:3 для Shorts через shorts.py).
"""
from doodle import seq, shot

STORY = dict(name="wolf-news-nvidia", accent=(214, 40, 40), voice="eric", speed=1.05, tempo=0.95, end_hold=1.0)
GREEN, RED = (40, 160, 70), (214, 40, 40)


def wolf(x=960, pose="stand", s=1.4, **k):
    return dict(kind="wolf", x=x, pose=pose, s=s, **k)


def gary(x=960, s=1.8, **k):
    return dict(kind="gary", x=x, s=s, **k)


def herd(mood="calm"):
    return [dict(kind="sheep", x=x, f=1.0, mood=mood, s=0.8) for x in (500, 860, 1220)]


MEME = lambda: shot(kind="gary")
FACE = lambda cap=None: shot(kind="wolfface", caption=cap, cap=(1150, 120))
T = lambda t: shot(kind="title", title=t)
TXT = lambda t, size=200, color=(17, 17, 17), cap=None: shot(dict(kind="text", text=t, size=size, y=400, color=color), caption=cap)

BLOCKS = [
    seq([
        ("One man quit his job.", shot(wolf(960))),
        ("And his company lost almost five hundred billion dollars.", TXT("-$500,000,000,000", 120, RED)),
        ("In about a week.", TXT("1 WEEK", 260, RED)),
        ("November twelfth. The boss of Nvidia steps down.", TXT("NVIDIA", 280), ("steps", TXT("CEO OUT", 260, RED))),
        ("The stock falls.", shot(dict(kind="chart", stage="crash"))),
        ("Sheep panic.", shot(*herd("shock"), caption="panic")),
        ("Sheep sell.", TXT("SELL!", 320, RED)),
        ("Eleven days later?", TXT("11 DAYS LATER", 190)),
        ("The board brings him back.", T("HE'S\nBACK")),
        ("The stock jumps over thirty percent. In one day.", TXT("+30%", 360, GREEN), ("day", TXT("1 DAY", 300, GREEN))),
        ("So who lost the most wool?", FACE()),
        ("The sheep who sold at the bottom.", shot(gary(), caption="sold at the bottom")),
        ("Lesson one. Never put all your wool in one company.", TXT("1 COMPANY = RISK", 140, RED)),
        ("Lesson two. Panic is the most expensive feeling in finance.", T("PANIC\nCOSTS WOOL")),
        ("Gary sold.", MEME()),
        ("Of course he did.", FACE("of course")),
        ("Not financial advice. Full story on my channel.", FACE("full story on the channel")),
    ], mood="tense", pause=0.3),
]
