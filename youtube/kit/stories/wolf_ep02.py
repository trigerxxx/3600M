"""The Sheep Standard — EP02: Pump and Dump: How Penny Stocks Fleece Sheep. Монтаж по плагину doodle-explainer-edit.
Факты (в описание, проверить перед выпуском):
- Stratton Oakmont — брокерская фирма на Лонг-Айленде, основана в 1989 г. (Jordan Belfort, Danny Porush), продавала penny stocks через «boiler room».
- 1996: NASD исключила фирму, она закрылась.
- 1999: Белфорт признал вину в мошенничестве с ценными бумагами и отмывании денег; приговор (2003) — 4 года, отбыл ~22 мес.; суд обязал выплатить ~$110 млн пострадавшим.
- 2013: фильм «The Wolf of Wall Street» (Scorsese).
- Дек. 2022: SEC обвинила 8 инфлюенсеров соцсетей в схеме pump-and-dump на ~$100 млн (sec.gov, пресс-релиз 2022-221).
"""
from doodle import seq, shot

STORY = dict(name="wolf-ep02", accent=(214, 40, 40), voice="eric", speed=1.03, end_hold=1.5)


def wolf(x=960, pose="stand", s=1.4, **k):
    return dict(kind="wolf", x=x, pose=pose, s=s, **k)


def sheep(x=860, f=1.0, mood="calm", c=None, s=1.8, **k):
    return dict(kind="sheep", x=x, f=f, mood=mood, c=c, s=s, **k)


def gary(x=860, s=1.8, **k):
    return dict(kind="gary", x=x, s=s, **k)


def herd(f=1.0, mood="calm", s=1.0):
    return [sheep(260, f, mood, s=s), sheep(760, f, mood, s=s), sheep(1260, f, mood, s=s)]


def stall(x=1350, price=None, sign="GRASS"):
    return dict(kind="stall", x=x, price=price, sign=sign)


def chart(stage):
    return dict(kind="chart", stage=stage)


def chat(*msgs, title="Moon Club", x=780):
    return dict(kind="phone", x=x, y=200, s=1.0, title=title, msgs=list(msgs))


MEME = lambda: shot(kind="gary")
FACE = lambda cap=None: shot(kind="wolfface", caption=cap, cap=(1150, 120))
T = lambda t: shot(kind="title", title=t)
TXT = lambda t, size=200, color=(17, 17, 17), cap=None: shot(dict(kind="text", text=t, size=size, y=400, color=color), caption=cap)
SHARE = lambda s=2.6, text="1 SHARE": dict(kind="note", x=960 - 115 * s, y=540 - 58 * s, s=s, text=text)
MIRACLE = "MIRACLE GRASS"

BLOCKS = [
    seq([
        ("Sheep.", shot(wolf(960, "phone"))),
        ("Come closer.", FACE()),
        ("I've got a deal for you.", shot(wolf(820, "phone"), caption="psst", cap=(1200, 160))),
        ("A tiny company.", shot(stall(960, sign=MIRACLE))),
        ("Nobody's heard of it.", shot(stall(960, sign=MIRACLE), caption="exclusive")),
        ("The stock costs one receipt.", shot(SHARE(), caption="1 receipt")),
        ("Next month? Ten.", TXT("10", 360, (40, 160, 70))),
        ("Maybe fifty.", TXT("50", 360, (40, 160, 70))),
        ("I'm really not supposed to tell you this.", shot(wolf(820, "phone"), caption="(he is)", cap=(1200, 160))),
        ("But I like you.", FACE("aww")),
        ("I don't like you.", FACE()),
        ("That was a pump and dump.", T("PUMP\nAND DUMP")),
        ("And in the next few minutes, I'll show you exactly how it shears you.", shot(wolf(820, "shears")), ("shears", shot(gary(), caption="like this"))),
        ("Bald.", MEME()),
        ("And at the end, I'll give you a three-second test that would have saved every single sheep in this video.", shot(wolf(960)),
         ("three-second", TXT("3 SECONDS", 220, cap="the test"))),
    ], mood="tense"),
    seq([
        ("First, what is a stock?", T("WHAT IS\nA STOCK?")),
        ("Imagine a grass shop.", shot(stall(960))),
        ("The owner wants to grow, so she sells tiny pieces of her shop.", shot(sheep(480, c="hat", s=1.4), stall(1450)), ("tiny", shot(SHARE(), caption="a tiny piece"))),
        ("Each piece is a share.", shot(SHARE(), caption="(share = stock)")),
        ("If the shop does well, your piece is worth more wool.", shot(sheep(c="shades"), caption="nice")),
        ("If it does badly, your piece is worth less.", shot(sheep(f=0.5, mood="sad"))),
        ("Simple.", FACE()),
        ("Now, big famous companies have millions of owners.", shot(dict(kind="notes", x=320, y=880, n0=30, cols=6, s=1.3), caption="millions of owners")),
        ("Millions of buyers, millions of sellers, and a lot of very boring people watching every move.", shot(*herd(s=0.9), caption="boring people"),
         ("watching", FACE("watching"))),
        ("Pushing their price around is hard.", shot(chart("start"), caption="hard to move")),
    ]),
    seq([
        ("But some companies are tiny.", shot(stall(960, sign=MIRACLE))),
        ("A shop with three bundles of grass and a dream.", shot(dict(kind="grass", x=760, y=880, n=3, s=1.8), caption="and a dream")),
        ("Their shares cost pennies.", shot(SHARE(text="1 CENT"), caption="pennies")),
        ("We call them penny stocks.", T("PENNY\nSTOCKS")),
        ("Barely anyone buys them.", shot(stall(960, sign=MIRACLE), caption="*crickets*")),
        ("Barely anyone watches them.", shot(gary(), caption="not even gary")),
        ("And with a stock that small, a few big buyers can push the price almost anywhere they want.", shot(chart("start")), ("push", shot(chart("up"), caption="anywhere"))),
        ("So, can you guess who has the big buyers?", FACE()),
        ("Hi.", FACE("hi")),
    ]),
    seq([
        ("Step one.", T("STEP 1:\nBUY QUIETLY")),
        ("I buy a mountain of Miracle Grass.", shot(dict(kind="notes", x=320, y=880, n0=4, step=4, at=["buy", "mountain", "miracle", "grass"], cols=6, s=1.3))),
        ("Quietly.", shot(wolf(960), caption="shhh")),
        ("One receipt per share.", shot(SHARE(), caption="cheap")),
        ("Nobody notices.", shot(*herd(s=0.9))),
        ("Nobody cares.", MEME()),
        ("Yet.", FACE("yet")),
    ], mood="tense"),
    seq([
        ("Step two.", T("STEP 2:\nTHE PUMP")),
        ("I hire a room full of very charming wolves with very loud telephones.", shot(dict(kind="boiler"))),
        ("They call it a boiler room.", T("BOILER\nROOM")),
        ("And they call sheep.", shot(sheep(c=None), caption="ring ring")),
        ("Thousands of sheep.", shot(*herd(s=0.9))),
        ("All day long.", shot(dict(kind="boiler"), caption="all day")),
        ("They have a script.", shot(wolf(820, "phone"), caption="the script", cap=(1200, 160))),
        ("Once in a lifetime.", TXT("ONCE IN A LIFETIME", 140, (214, 40, 40))),
        ("Only today.", TXT("ONLY TODAY", 170, (214, 40, 40))),
        ("Everyone's already buying.", TXT("EVERYONE'S BUYING", 140, (214, 40, 40))),
        ("They never say: this might be a terrible idea.", FACE("never")),
        ("They say: you'll miss out.", T("YOU'LL\nMISS OUT")),
        ("But that's not the worst part.", shot(wolf(960))),
        ("Some sheep say no.", shot(sheep(f=1.0), caption="no thanks")),
        ("So we send them news.", shot(chat("BREAKING NEWS", "Miracle Grass", "signs huge deal!", title="Grass News"))),
        ("Amazing news.", TXT("AMAZING NEWS", 160)),
        ("That we wrote ourselves.", FACE("oops")),
        ("And sheep do what sheep do best.", shot(*herd(s=0.9))),
        ("They follow the other sheep.", T("HERD\nMENTALITY")),
        ("Everybody buys.", shot(*herd(mood="shock", s=0.9), caption="buy buy buy")),
        ("The price goes up.", shot(chart("up"))),
        ("Which makes more sheep buy.", shot(*herd(s=0.9), caption="more sheep")),
        ("Which makes the price go up even more.", shot(chart("peak"))),
        ("It's beautiful.", FACE("beautiful")),
        ("It's like watching wool grow in fast forward.", shot(sheep(c="shades"), caption="fast forward")),
    ], mood="tense"),
    seq([
        ("And then, step three.", T("STEP 3:\nTHE DUMP")),
        ("At the very top, I sell everything I bought at one receipt.", shot(chart("peak")), ("sell", shot(wolf(960), caption="sell"))),
        ("For fifteen.", TXT("15", 360, (40, 160, 70), cap="per share")),
        ("Now there's nobody left to buy.", shot(stall(960, sign=MIRACLE), caption="empty")),
        ("Because I was the buyer.", FACE("it was me")),
        ("The price falls off a cliff.", shot(chart("crash"))),
        ("And the sheep are holding a very expensive piece of nothing.", shot(SHARE(text="0.01"), caption="a piece of nothing")),
        ("Wolves walk away fluffy.", shot(wolf(960), caption="fluffy")),
        ("Sheep walk away bald.", shot(sheep(260, 0.0, "shock", s=1.0), sheep(760, 0.0, "shock", s=1.0), gary(1260, s=1.0))),
        ("Every single time.", MEME()),
    ], mood="tense"),
    seq([
        ("Now you're thinking, that's just a cartoon about sheep.", FACE("just a cartoon")),
        ("It's not.", T("THIS ACTUALLY\nHAPPENED")),
        ("In nineteen eighty-nine, on Long Island, New York, a brokerage firm opened called Stratton Oakmont.", TXT("1989", 300), ("brokerage", TXT("NEW YORK", 200))),
        ("It was run by a young broker named Jordan Belfort.", shot(wolf(960), caption="a real person")),
        ("Rooms full of young brokers, phones glued to their ears, pushing tiny stocks to ordinary people.", shot(dict(kind="boiler")), ("pushing", shot(*herd(s=0.9), caption="ordinary people"))),
        ("Pump the price.", shot(chart("up"))),
        ("Dump the shares.", shot(chart("crash"))),
        ("Repeat.", FACE("repeat")),
        ("Regulators shut the firm down in nineteen ninety-six.", TXT("1996", 300, cap="shut down")),
        ("Belfort later pleaded guilty to securities fraud and money laundering.", shot(dict(kind="gavel", x=900, y=640))),
        ("He spent about twenty-two months in prison.", TXT("22 MONTHS", 200)),
        ("And a court ordered him to pay back about one hundred and ten million dollars to his victims.", TXT("$110,000,000", 190, (214, 40, 40), cap="to his victims")),
        ("His story later became a famous Hollywood movie.", FACE("you've seen it")),
        ("Great movie.", FACE()),
        ("Terrible retirement plan for the investors.", MEME()),
    ], mood="tense"),
    seq([
        ("But here's the thing.", shot(wolf(960))),
        ("Pump and dumps didn't disappear.", T("THEY NEVER\nLEFT")),
        ("They just changed phones.", shot(chat("TO THE MOON", "BUY NOW!!!", "trust me bro"))),
        ("Today, it's not a loud broker calling your house.", shot(wolf(820, "phone"), caption="old school", cap=(1200, 160))),
        ("It's a group chat.", shot(chat("100x soon", "dont miss it", "last chance"))),
        ("An influencer with expensive sunglasses.", shot(sheep(c="shades"), caption="influencer")),
        ("A random account full of rocket emojis.", shot(chat("TO THE MOON", "TO THE MOON", "TO THE MOON"))),
        ("A brand new coin with a funny name.", shot(dict(kind="coin", x=960, y=520, r=230))),
        ("Same trick.", FACE()),
        ("In twenty twenty-two, the U.S. Securities and Exchange Commission charged eight social media influencers in a pump and dump scheme worth about one hundred million dollars.", TXT("2022", 300),
         ("charged", TXT("8 INFLUENCERS", 170)), ("worth", TXT("$100,000,000", 190, (214, 40, 40)))),
        ("Different costume.", shot(sheep(c="shades"))),
        ("Same wolf.", FACE("same wolf")),
        ("And here's the worst part.", shot(wolf(960))),
        ("The loudest voice in the chat is usually the one who bought first.", T("WHO BOUGHT\nFIRST?")),
        ("They don't need you to get rich.", FACE()),
        ("They need you to be the exit.", T("YOU ARE\nTHE EXIT")),
    ], mood="tense"),
    seq([
        ("Alright. I promised you a test.", shot(wolf(960))),
        ("Here it is.", T("THE 3-SECOND\nTEST")),
        ("If someone you don't know is in a hurry to make you rich, ask one question.", shot(wolf(820, "phone")), ("ask", FACE("one question"))),
        ("Why are they telling me?", T("WHY ARE THEY\nTELLING ME?")),
        ("If it's so good, why aren't they buying quietly, like I did?", FACE("like i did")),
        ("That's it. Three seconds.", TXT("3 SECONDS", 220)),
        ("And three red flags.", shot(wolf(960))),
        ("One. A tiny company nobody has heard of.", shot(stall(960, sign=MIRACLE), caption="1. tiny + unknown")),
        ("Two. Huge promises.", TXT("100x !!!", 260, (214, 40, 40), cap="2. huge promises")),
        ("Three. Buy right now.", TXT("ONLY TODAY", 170, (214, 40, 40), cap="3. buy right now")),
        ("All three together?", FACE()),
        ("That's a wolf.", shot(wolf(960), caption="hello")),
        ("Every time.", MEME()),
        ("Not financial advice.", FACE("not financial advice")),
        ("I'm a wolf.", shot(wolf(960))),
    ], mood="hope"),
    seq([
        ("So, that's a pump and dump.", shot(wolf(960, "phone"))),
        ("Excuse me.", shot(wolf(960, "phone"), caption="ring ring")),
        ("It's a sheep.", shot(sheep())),
        ("Wants to know about a hot new stock.", shot(stall(960, sign=MIRACLE))),
        ("Hello, sheep.", FACE()),
        ("If you don't want to end up bald like Gary… subscribe.", shot(kind="outro")),
        ("Gary bought Miracle Grass.", shot(kind="outro", caption="gary bought miracle grass.", cap=(900, 200))),
    ], mood="hope", pause=1.6),
]
