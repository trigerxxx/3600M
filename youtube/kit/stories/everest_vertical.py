"""Everest: 44 Days — вертикальная версия в формате «слово за словом» (~75 с)."""
from kit import block, counter, device, news, scene, stamp, tally, title

STORY = dict(name="everest-vertical", accent=(255, 122, 26), voice="brian", speed=1.04)

BLOCKS = [
    block("He counted *forty-four* days alone on *Everest*. Then he checked the date.",
          hud=("DAY 44 · DEATH ZONE · 8,400 M", "05:58:12"),
          shots=[(0, scene("tent_ledge", mode="full", night=True, cx=0.47)),
                 ("forty-four", tally(38, 44)),
                 ("checked", device("tracker", "SAT TRACKER", "NO SIGNAL", msgs=[("date", "DAY ??", "sys")]))],
          sfx=[("date", "riser")], mood="tense", amb="wind"),

    block("The storm hit the summit in *minutes*. Two weeks later, the search was called off. For the world, Ilyas was *dead*.",
          hud=("DAY 1 · SUMMIT RIDGE", "16:20:05"),
          shots=[(0, scene("storm", mode="full", climber=True, cx=0.55)),
                 ("search", news("CLIMBER MISSING", "Search called off after 14 days · No survivors expected above 8,000 m", bg="basecamp")),
                 ("world", scene("tent_ledge", mode="circle", night=True, cx=0.46))],
          sfx=[(0, "gust"), ("dead", "boom")], mood="dark", amb="storm"),

    block("But he was *alive*. In a torn tent, at minus forty. With one rule above all.",
          hud=("DAY 2 · TENT · 8,400 M", "09:14:40"),
          shots=[(0, scene("tent_int", mode="card", cx=0.6)),
                 ("minus", counter(-40, 0, label="TEMPERATURE", suffix="°C", color=(120, 180, 255))),
                 ("rule", stamp("RULE #1", "never go outside after dark", bg="night_ext"))],
          sfx=[("alive", "heart")], mood="tense", amb="tent"),

    block("Every night, he scratched one line on his flask. *One*. *Two*. *Twelve*. *Thirty*.",
          hud=("DAY 12 · TENT", "21:03:09"),
          shots=[(0, scene("night_ext", mode="card", cx=0.4)),
                 ("one", tally(1, 1)), ("two", tally(2, 2)), ("twelve", tally(12, 12)), ("thirty", tally(30, 30))],
          sfx=[("one", "scratch"), ("two", "scratch"), ("twelve", "scratch"), ("thirty", "scratch")], mood="dark", amb="tent"),

    block("On day *forty-one*, the wall ripped open. He sewed it shut in the dark, with fingers he couldn't *feel*.",
          hud=("DAY 41 · TENT", "00:12:51"),
          shots=[(0, scene("tent_int", mode="card", dim=True, cx=0.6)),
                 ("ripped", scene("tear", mode="full", cx=0.35)),
                 ("sewed", scene("hands", mode="circle", cx=0.6))],
          sfx=[("ripped", "rip"), ("sewed", "stitch"), ("feel", "heart")], mood="tense", amb="storm"),

    block("Day *forty-four*. The wind stopped. He opened the tent, and the sun painted the peaks *red*. He made it.",
          hud=("DAY 44 · DEATH ZONE", "05:58:12"),
          shots=[(0, tally(44, 44)),
                 ("wind", scene("tent_door", mode="card")),
                 ("sun", scene("dawn", mode="full", cx=0.72))],
          sfx=[("opened", "zip"), ("made", "swell")], mood="hope", amb="silence"),

    block("Then the tracker woke up. Day *fifty-two*.",
          hud=("DAY ?? · DEATH ZONE", "06:01:30"),
          shots=[(0, device("tracker", "SAT TRACKER", "SIGNAL FOUND", msgs=[("woke", "Signal found", "sys"), ("fifty-two", "DAY 52", "in", "alert")])),
                 ("fifty-two", scene("tracker", mode="card", day="52", label="DAY", alarm_on=True))],
          sfx=[("fifty-two", "boom")], mood="tense", amb="silence"),

    block("He had been passing out for *days*. Nobody counted those.",
          hud=("DAY 52 · DEATH ZONE", "06:02:10"),
          shots=[(0, scene("tent_int", mode="circle", dim=True, cx=0.6)), ("nobody", tally(44, 44, dark=True))],
          sfx=[("days", "heart")], mood="tense", amb="wind_soft"),

    block("The weather window wasn't opening. It was *closing*.",
          hud=("DAY 52 · DEATH ZONE", "06:02:31"),
          shots=[(0, scene("storm_coming", mode="full", wall=1.0, cx=0.3)),
                 ("closing", stamp("MISTAKE #1", "he stopped counting right", bg="storm_coming", wall=1.0))],
          sfx=[(0, "rumble")], mood="tense", amb="wind"),

    block("Three thousand meters down. One day of strength. Could *you* get down alive?",
          hud=("DAY 52 · 8,400 M", "06:03:00"),
          shots=[(0, scene("descent", mode="card")),
                 ("could", title("GET DOWN\nALIVE?", "EVEREST · PART 2 SOON"))],
          sfx=[], mood="tense", amb="wind", pause=0.8),
]
