"""GHOST — Part 1. История автора (вымысел), формат «слово за словом», рассказ от «you»."""
import scenes_ghost  # noqa: F401  регистрирует сцены сериала
from kit import block, counter, device, scene, stamp, title

STORY = dict(name="ghost-part1", accent=(80, 220, 255), voice="brian", speed=1.04)

BLOCKS = [
    block("The FBI made you hunt the most dangerous hacker in the world. The *problem*? It's *you*.",
          hud=("FBI FIELD OFFICE", "09:00:00"),
          shots=[(0, scene("wall", mode="full", cx=0.5)), ("problem", scene("mask", mode="circle", title=False)),
                 ("you#2", stamp("IT'S YOU", bg="mask", title=False))],
          sfx=[(0, "riser")], mood="tense", amb="silence"),

    block("They call you *Ghost*. You've hacked a bank, a ministry, and three stock exchanges. Nobody has ever seen your face.",
          hud=("WANTED · WORLDWIDE", "--:--:--"),
          shots=[(0, scene("mask", mode="card")), ("hacked", counter(5, 0, label="SYSTEMS BROKEN", suffix="", dur=1.6)),
                 ("nobody", scene("wall", mode="circle", cx=0.5))],
          sfx=[("ghost", "boom")], mood="dark", amb="silence"),

    block("In real life, you rent a tiny apartment. You have a cat, and the résumé of a boring programmer.",
          hud=("HOME · 3RD FLOOR", "23:41:08"),
          shots=[(0, scene("apartment", mode="full", cx=0.45)), ("cat", scene("apartment", mode="circle", cx=0.62, cy=0.62))],
          sfx=[], mood="dark", amb="wind_soft"),

    block("Then you slip up on something *stupid*. You hack a pizza place. For *free pizza*.",
          hud=("HOME · 3RD FLOOR", "01:12:44"),
          shots=[(0, scene("pizza", mode="card")), ("free", stamp("MISTAKE #1", "free pizza", bg="pizza"))],
          sfx=[("hack", "type")], mood="dark", amb="silence"),

    block("Six a.m. The FBI kicks your door in.",
          hud=("HOME · 3RD FLOOR", "06:00:00"),
          shots=[(0, scene("door", mode="full")), ("kicks", stamp("FBI", "open the door", bg="door"))],
          sfx=[("kicks", "boom")], mood="tense", amb="silence"),

    block("But they don't know who you are. They think they caught some kid with a *pizza problem*.",
          hud=("INTERROGATION ROOM", "08:15:30"),
          shots=[(0, scene("liz", mode="card", cx=0.45)), ("pizza", scene("pizza", mode="circle", cx=0.3))],
          sfx=[], mood="dark", amb="silence"),

    block("So they offer you a deal. *Ten years* in prison. Or work for them, and help catch *Ghost*.",
          hud=("INTERROGATION ROOM", "08:21:02"),
          shots=[(0, scene("choice", mode="card")), ("ghost", scene("mask", mode="circle"))],
          sfx=[("ghost", "hit")], mood="tense", amb="silence"),

    block("Day one. A badge. Free coffee. And a whole wall covered in *your* hacks. Photos. Arrows. And in the middle, a silhouette with a question mark.",
          hud=("DAY 1 · FBI CYBER UNIT", "09:02:17"),
          shots=[(0, scene("office", mode="full", cx=0.55)), ("wall", scene("wall", mode="full")),
                 ("silhouette", scene("wall", mode="circle", z=(1.6, 1.9)))],
          sfx=[("silhouette", "heart")], mood="tense", amb="camp"),

    block("Your new partner is Agent Liz. She has been hunting Ghost for *eight years*. He's a genius, she says. But geniuses make mistakes. I only need *one*.",
          hud=("DAY 1 · FBI CYBER UNIT", "09:30:40"),
          shots=[(0, scene("liz", mode="full", cx=0.5)), ("eight", counter(8, 0, label="YEARS HUNTING GHOST", dur=0.8)),
                 ("geniuses", scene("liz", mode="circle", cx=0.5))],
          sfx=[("one", "hit")], mood="tense", amb="camp"),

    block("A week later, she drops a printout on your desk. Every message Ghost ever sent. Look. He never uses emojis. Just *one* bracket.",
          hud=("DAY 8 · FBI CYBER UNIT", "17:48:05"),
          shots=[(0, device("phone", "GHOST", "last seen: never", msgs=[
                     ("printout", "Bank done )", "in"), ("message", "See you in two months )", "in"),
                     ("emojis", "You'll never find me )", "in"), ("bracket", ")", "in", "alert")]))],
          sfx=[("bracket", "boom")], mood="tense", amb="silence"),

    block("Only Russians type like that. There are forty people in this office, she says. And only *one* Russian.",
          hud=("DAY 8 · FBI CYBER UNIT", "17:48:31"),
          shots=[(0, counter(40, 0, label="PEOPLE IN THIS OFFICE", dur=0.9)), ("only#2", counter(1, 40, label="RUSSIANS", color=(232, 48, 42), dur=0.5))],
          sfx=[("one", "boom")], mood="tense", amb="silence"),

    block("She slowly looks at your phone. It lights up. A text from Mom. And it ends with a *bracket*.",
          hud=("DAY 8 · FBI CYBER UNIT", "17:48:44"),
          shots=[(0, scene("liz", mode="circle", cx=0.5)),
                 ("lights", device("phone", "Mom", "online", msgs=[("text", "Call me when you're free )", "in", "alert")])),
                 ("bracket", title(")", "PART 2 SOON", color=(232, 48, 42)))],
          sfx=[("lights", "msg"), ("bracket", "boom")], mood="tense", amb="silence", pause=1.4),
]
