"""Everest: 44 Days in the Dark — сценарий длинного ролика.
Каждая часть: текст рассказчика, сцена, движение камеры, фон звука, звуковые эффекты.
Звуковые эффекты: (имя, секунда от начала части; отрицательное число = от конца).
"""

TITLE = "He Survived 44 Days on Everest. Then He Checked the Date."

S = []


def seg(id, text, scene, amb="wind", sfx=(), mood="dark", cam="push", **p):
    S.append(dict(id=id, text=text, scene=scene, amb=amb, sfx=list(sfx), mood=mood, cam=cam, p=p))


def card(id, big, small, amb="wind", mood="dark", dur=3.6):
    S.append(dict(id=id, text=None, scene="card", amb=amb, sfx=[("whoosh", 0.0), ("boom", 0.35)], mood=mood,
                  cam="still", p=dict(big=big, small=small), dur=dur))


# ---------- холодное начало ----------
seg("c1", "On the night of the storm, nobody could see the summit. Only white. Only wind.",
    "storm", amb="storm", sfx=[("boom", 0.2)], cam="push_slow")
seg("c2", "Two weeks later, the search was called off. Helicopters can't fly that high. And in that weather, people don't survive.",
    "news", amb="wind_soft", sfx=[("paper", 0.1), ("hit", 0.4)])
seg("c3", "For the whole world, a climber named Ilyas was missing, presumed dead. But Ilyas was alive.",
    "tent_ledge", amb="wind", sfx=[("heart", -2.2), ("heart", -1.3)], night=True)
seg("c4", "And he had a number. Forty-four. Forty-four days until the weather window, when the winds would drop enough to try to get down alone.",
    "tracker", amb="tent", sfx=[("beep", 0.9), ("beep", 1.6)], cam="push", day="44", label="DAYS TO WINDOW")
seg("c5", "This is the story of those forty-four days. And of the one thing Ilyas got wrong.",
    "flask", amb="tent", sfx=[("scratch", 0.6), ("riser", -3.0)], count=44, dark=True, mood="tense")
card("title", "EVEREST", "44 DAYS IN THE DARK AND COLD", amb="storm", dur=4.8)

# ---------- глава 1 ----------
card("ch1", "CHAPTER 1", "THE STORM")
seg("s1", "It came out of nowhere. One moment, the sky above the summit was clear and deep blue. The next, a wall of cloud swallowed the ridge.",
    "summit_clear", amb="wind_soft", sfx=[("rumble", -4.0)], cam="pan_right")
seg("s2", "The wind hit at over a hundred kilometers an hour. Ice needles in the face. The rope ahead of him vanished into white.",
    "storm", amb="storm", sfx=[("gust", 0.3), ("gust", 3.5), ("breath", 1.5), ("breath", 4.2)], cam="shake", climber=True)
seg("s3", "Ilyas did the only thing he could. He found a ledge below the ridge, dug in, and pitched a small tent. It was half torn before he even crawled inside.",
    "tent_ledge", amb="storm", sfx=[("crunch", 1.0), ("crunch", 1.6), ("crunch", 2.2), ("flap", 4.0), ("zip", -2.0)], night=True)
seg("s4", "The ledge sat above eight thousand meters. Climbers call it the death zone. The air holds only a third of the oxygen you breathe at sea level. Every breath burns. At night, it's minus forty.",
    "deathzone", amb="wind", sfx=[("hit", 2.6), ("breath", 6.0), ("breath", 9.0)], cam="tilt_up")
seg("s5", "Far below, at base camp, his team waited. They called his name on the radio for days. Nobody answered.",
    "basecamp", amb="camp", sfx=[("radio", 2.5), ("radio", 6.0)], cam="pan_left")
seg("s6", "His radio had died on the first night. The cold had killed the battery. All he had left was a satellite tracker. And it could only do one thing. Count.",
    "radio", amb="tent", sfx=[("static", 0.3), ("click", 3.2), ("beep", -1.2)])

# ---------- глава 2 ----------
card("ch2", "CHAPTER 2", "THE RULES", amb="tent")
seg("r1", "Inside the tent, Ilyas took stock. A bag of freeze-dried food. One small gas canister for the stove. A knife. A plastic flask. And a sleeping bag, stiff with frost.",
    "tent_int", amb="tent", sfx=[("rustle", 1.8), ("clink", 4.0), ("clink", 6.2), ("rustle", 8.5)], mood="tense")
seg("r2", "He made two rules. Rule one: strict rationing. A handful of food and a few sips of warm water a day. Every minute the stove burned was fuel he would never get back.",
    "rule", amb="tent", sfx=[("hit", 0.9), ("stove", 5.0)], n="1", head="STRICT RATIONING", sub="a handful of food, a few sips of water", icon="flame")
seg("r3", "Rule two: never go outside after sunset. When the sun dropped behind the peaks, the temperature fell like a stone. Outside, at night, frostbite comes in minutes.",
    "rule", amb="wind", sfx=[("hit", 0.6), ("gust", 4.0)], n="2", head="NEVER GO OUT AFTER DARK", sub="minus forty, frostbite in minutes", icon="moon")
seg("r4", "To keep track of time, he scratched a line on the flask with his knife. One line for every day.",
    "flask", amb="tent", sfx=[("scratch", 2.4), ("scratch", 3.6)], count=1)
seg("r5", "One. Two. Seven. Twelve.",
    "flask", amb="tent", sfx=[("scratch", 0.2), ("scratch", 0.8), ("scratch", 1.4), ("scratch", 2.0)], count=12, grow=True, cam="push_fast")

# ---------- глава 3 ----------
card("ch3", "CHAPTER 3", "THE LONG DARK")
seg("d1", "The days became the same day. Melt snow. Eat a little. Sleep. Listen to the wind.",
    "night_ext", amb="wind_soft", sfx=[("stove", 1.5)], cam="pan_right", mood="dark")
seg("d1b", "Melting snow was the hardest part. A whole pot of snow gives you only a cup of water. And every cup costs gas.",
    "tent_int", amb="tent", sfx=[("stove", 0.5), ("drip", 4.0), ("drip", 5.2)], warm=True)
seg("d2", "And the wind never stopped. It slammed the tent so hard, it felt like something outside was trying to tear it off the mountain.",
    "tent_ledge", amb="storm", sfx=[("flap", 1.0), ("flap", 2.4), ("gust", 3.0), ("flap", 4.6), ("flap", 5.5)], night=True, cam="shake")
seg("d3", "Sometimes he heard voices in it. His mother. His friends at base camp, calling his name. He knew they weren't real. That's what the death zone does to your mind.",
    "tent_int", amb="wind", sfx=[("whisper", 1.8), ("whisper", 4.5), ("heart", -3.0), ("heart", -2.2)], dim=True, mood="tense")
seg("d3b", "One night, he was certain someone was standing outside the tent. He could see a shadow on the fabric. He held his breath until sunrise. In the morning, there were no footprints in the snow. Only his own.",
    "tent_int", amb="wind_soft", sfx=[("crunch", 3.0), ("crunch", 3.8), ("heart", 6.0), ("heart", 6.7), ("heart", 7.4), ("hit", -4.5)], dim=True, shadow=True, mood="tense")
seg("d4", "By day thirty, his body was running on nothing. He was as thin as a skeleton. Every breath came with a rattle. He couldn't feel his fingers anymore.",
    "flask", amb="tent", sfx=[("breath", 2.0), ("breath", 5.0), ("breath", 8.0)], count=30)
seg("d5", "But his mind stayed sharp. He kept counting. He kept the rules.",
    "tent_int", amb="tent", sfx=[("scratch", 2.0)], mood="hope")

# ---------- глава 4 ----------
card("ch4", "CHAPTER 4", "DAY 41", mood="tense")
seg("t1", "Then came day forty-one. The worst storm since the first night.",
    "storm", amb="storm", sfx=[("rumble", 0.3), ("gust", 2.0)], cam="shake", mood="tense")
seg("t2", "Around midnight, he heard the sound he had been dreading for weeks. A long, ripping tear. The windward wall split open.",
    "tent_int", amb="storm", sfx=[("rip", -3.4), ("boom", -3.2)], mood="tense", dim=True)
seg("t3", "The blizzard poured in. Snow filled the sleeping bag. The temperature inside dropped to the temperature outside.",
    "tear", amb="storm", sfx=[("gust", 0.2), ("flap", 1.2), ("flap", 2.2), ("gust", 4.0)], cam="shake", mood="tense")
seg("t4", "He had to fix it. Right now. In total darkness, by touch, with fingers he couldn't feel, he pushed a needle through the frozen fabric. Again. And again.",
    "hands", amb="storm", sfx=[("breath", 3.0), ("stitch", 7.0), ("stitch", 8.4), ("breath", 9.2), ("stitch", 9.8)], mood="tense")
seg("t5", "Every stitch could cost him a finger. He knew that. He kept sewing.",
    "hands", amb="storm", sfx=[("stitch", 1.0), ("heart", 2.4), ("heart", 3.1), ("stitch", 3.8)], mood="tense", cam="push_fast")
seg("t6", "By dawn, the hole was closed. The tent held. He had survived the night that should have killed him.",
    "tent_int", amb="wind_soft", sfx=[("exhale", 1.0)], mood="hope", warm=True)
seg("t7", "His hands were burning with pain. And that was good news. Pain meant they were still alive.",
    "hands", amb="wind_soft", sfx=[("exhale", 1.5)], mood="hope", warm=True)

# ---------- глава 5 ----------
card("ch5", "CHAPTER 5", "DAY 44", amb="wind_soft", mood="hope")
seg("f1", "Three days later, he scratched the last line. Forty-four.",
    "flask", amb="tent", sfx=[("scratch", 2.4), ("hit", 3.3)], count=44, mood="hope")
seg("f2", "The storm had stopped. For the first time in six weeks, there was no wind. Only a ringing, total silence.",
    "tent_int", amb="silence", sfx=[("ring", 1.0)], mood="hope", warm=True)
seg("f2b", "He counted the lines on the flask one more time. Forty-four. For the first time in six weeks, he let himself smile.",
    "flask", amb="silence", sfx=[("swell", 3.0)], count=44, mood="hope")
seg("f3", "Ilyas cut the frozen zipper with his knife, and looked outside.",
    "tent_door", amb="silence", sfx=[("zip", 1.6), ("whoosh", -1.0)], mood="hope", cam="push_fast")
seg("f4", "The first rays of sun were painting the Himalayas blood red. An endless ocean of white peaks below him. He had made it. Forty-four days in the death zone. Alive.",
    "dawn", amb="wind_soft", sfx=[("swell", 0.0)], mood="hope", cam="pan_right")

# ---------- глава 6 ----------
card("ch6", "CHAPTER 6", "THE MISTAKE", mood="tense")
seg("m1", "Then he looked at the tracker. He had stopped checking it weeks ago. He trusted his flask.",
    "tracker", amb="silence", sfx=[("click", 2.0), ("beep", 2.6)], day="44?", label="DAY", mood="tense")
seg("m2", "The screen said: day fifty-two.",
    "tracker", amb="silence", sfx=[("beep", 0.3), ("boom", 1.0)], day="52", label="DAY", alarm=True, mood="tense", cam="push_fast")
seg("m3", "Fifty-two. Not forty-four.",
    "flask", amb="silence", sfx=[("heart", 0.5), ("heart", 1.2), ("heart", 1.9)], count=44, dark=True, mood="tense")
seg("m4", "In the thin air, he had been passing out. For hours. Sometimes for whole days. And on those days, nobody scratched a line on the flask.",
    "tent_int", amb="wind_soft", sfx=[("breath", 2.0), ("heart", 6.0), ("heart", 6.7)], dim=True, mood="tense")
seg("m5", "Which meant the weather window wasn't about to open. It had already been open. For eight days. And it was closing.",
    "storm_coming", amb="wind_soft", sfx=[("riser", 2.0), ("boom", 7.0)], mood="tense", cam="pan_left")
seg("m6", "On the horizon, a grey wall of cloud was already rising. The next storm. Maybe a bigger one.",
    "storm_coming", amb="wind", sfx=[("rumble", 1.5)], mood="tense", cam="push", wall=1.0)
seg("m7", "Below him lay three thousand meters of ice, cliffs and crevasses. And he could barely stand.",
    "descent", amb="wind", sfx=[("gust", 1.0), ("breath", 4.0)], mood="tense", cam="tilt_down")
seg("m8", "The food. The gas. His strength. Almost everything was gone. He had maybe one day left in him. Maybe less.",
    "tent_int", amb="wind", sfx=[("heart", 1.0), ("heart", 1.7), ("riser", -3.0)], dim=True, mood="tense")

# ---------- финал ----------
seg("e1", "Ilyas survived forty-four days at the top of the world. Or fifty-two. But the hardest part was still ahead.",
    "dawn", amb="wind_soft", sfx=[("swell", 0.0)], mood="hope", cam="pull")
seg("e2", "Getting down. Alive.",
    "end", amb="wind", sfx=[("boom", 0.4)], mood="tense", cam="still")
seg("e3", "Could you have survived? Tell me in the comments how many days you would last. And if you want to see what happened on the way down, subscribe. The descent is coming.",
    "end", amb="wind_soft", sfx=[], mood="hope", cam="push_slow", cta=True)

SEGMENTS = S
