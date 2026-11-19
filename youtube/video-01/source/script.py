"""Сценарий ролика №1: каждая часть = текст озвучки + что показать на экране."""

TITLE = "How 3 Friends in a Shed Made $240 Million on Roblox"

SEGMENTS = [
    # --- крючок ---
    dict(id="hook1", text="Three friends. A tiny shed in New Zealand. Three months of work.",
         visual=dict(kind="lines", lines=["3 FRIENDS", "1 SHED", "3 MONTHS"])),
    dict(id="hook2", text="And then, fourteen million people playing their game at the same time.",
         visual=dict(kind="counter", value=14_000_000, label="players online at the same time", note="peak, per Roblox DevForum and games.gg")),
    dict(id="hook3", text="This is the story of 99 Nights in the Forest, one of the biggest games Roblox has ever seen. And the formula behind it, which you can actually learn from.",
         visual=dict(kind="title", big="99 NIGHTS", small="the formula behind a Roblox mega-hit")),

    # --- кто они ---
    dict(id="who1", text="The game was made by a studio called Grandma's Favourite Games. Three guys from Auckland. Two have been friends since school, and they met the third one on Roblox as teenagers.",
         visual=dict(kind="cards", items=[("Auckland", "New Zealand"), ("3 people", "the whole team"), ("met on Roblox", "as teenagers")])),
    dict(id="who2", text="In an interview with PC Games N, they said they started in a shed with just their desks in it. They started building in March twenty twenty-five, and released in June. Their earlier games took around six months. This time, speed was the goal.",
         visual=dict(kind="timeline", steps=[("MARCH 2025", "start building"), ("JUNE 2025", "release"), ("SUMMER", "explosion")])),

    # --- цифры ---
    dict(id="num1", text="Then things got crazy. In September twenty twenty-five, the game averaged about one hundred thirty-seven million visits per day, more than Grow a Garden, the previous summer hit.",
         visual=dict(kind="bars", title="Average daily visits, Sep 1 to 14, 2025", bars=[("99 Nights", 137), ("Grow a Garden", 108)], unit="M", note="Max Power Gaming, Rotrends data")),
    dict(id="num2", text="By late twenty twenty-six, it passed twenty-nine billion visits. It got added to Fortnite, and a movie is in the works.",
         visual=dict(kind="counter", value=29_500_000_000, label="total visits", note="PCGamesN, 2026")),
    dict(id="num3", text="How much money did it make? Roblox doesn't publish that. But revenue trackers estimate around two hundred forty million dollars over its lifetime. Treat that as a rough estimate, not a fact.",
         visual=dict(kind="money", value="~$240M", note="estimate by revenue trackers, not official")),

    # --- формула ---
    dict(id="f0", text="So why did it work? I studied the game, and I found a formula with six parts.",
         visual=dict(kind="title", big="THE FORMULA", small="6 parts")),
    dict(id="f1", text="One. The promise is in the name. Ninety nine nights, in the forest. A number, a place, a goal. You understand the whole game in one second.",
         visual=dict(kind="point", n=1, head="The promise is in the name", sub="a number + a place + a goal")),
    dict(id="f2", text="Two. A simple loop. During the day, you gather and build. At night, you defend. Anyone can learn it in a minute, even on a phone.",
         visual=dict(kind="point", n=2, head="Day: gather.  Night: defend.", sub="learn it in one minute")),
    dict(id="f3", text="Three. One object at the center of everything: the campfire. Upgrade the fire, and the map gets bigger. You literally see your progress.",
         visual=dict(kind="point", n=3, head="The campfire grows", sub="and the world grows with it")),
    dict(id="f4", text="Four. A monster you cannot kill. The Deer. You can only stun it with a flashlight. That makes it iconic. Memes, fan art, merch, even a movie.",
         visual=dict(kind="point", n=4, head="An unkillable icon", sub="you can only stun it")),
    dict(id="f5", text="Five. A reason to care. You are not just surviving. You are trying to rescue four missing kids.",
         visual=dict(kind="point", n=5, head="Someone to save", sub="not just survival")),
    dict(id="f6", text="And six. Friends, and timing. Up to five players together, which creates panic, screaming, and funny moments, perfect for TikTok and YouTube. Weekly updates while it was growing. And a release right at the start of summer, when Roblox is busiest.",
         visual=dict(kind="point", n=6, head="Friends + weekly updates + summer", sub="clips, comebacks, perfect timing")),

    # --- урок ---
    dict(id="l1", text="But here is the part people miss. You cannot copy their luck, and you cannot copy their years of experience. What you can copy is the formula.",
         visual=dict(kind="lines", lines=["DON'T COPY THE GAME", "COPY THE FORMULA"])),
    dict(id="l2", text="Their own advice was simple. Know your product better than anyone. Trust your instincts. And don't be afraid to fail. Try things, and move on if they don't work.",
         visual=dict(kind="quote", text="Don't be afraid to fail. Try things, and move on if they don't work.", who="paraphrased from the developers, PCGamesN")),

    # --- мой путь ---
    dict(id="me1", text="And that's exactly what I'm doing. I'm nineteen, from Kyrgyzstan, and I'm building Roblox games using this formula. My main game is called 33 Days. Your plane crashes in the Amazon, and search teams stop looking for you in thirty-three days.",
         visual=dict(kind="title", big="33 DAYS", small="my Roblox game, coming June 2027")),
    dict(id="me2", text="If you want to watch me build it, and see the real numbers when it launches, subscribe. See you in the next one.",
         visual=dict(kind="lines", lines=["FOLLOW THE JOURNEY", "SUBSCRIBE"])),
]
