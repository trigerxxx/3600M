"""The Sheep Standard — EP02: Pump and Dump: How Penny Stocks Fleece Sheep. Монтаж по плагину doodle-explainer-edit.
Факты (в описание, проверить перед выпуском):
- Stratton Oakmont — брокерская фирма на Лонг-Айленде, основана в 1989 г. (Jordan Belfort, Danny Porush), продавала penny stocks через «boiler room».
- 1996: NASD исключила фирму, она закрылась.
- 1999: Белфорт признал вину в мошенничестве с ценными бумагами и отмывании денег; приговор (2003) — 4 года, отбыл ~22 мес.; суд обязал выплатить ~$110 млн пострадавшим.
- 2013: фильм «The Wolf of Wall Street» (Scorsese).
- Дек. 2022: SEC обвинила 8 инфлюенсеров соцсетей в схеме pump-and-dump на ~$100 млн (sec.gov, пресс-релиз 2022-221).
"""
from doodle import seq, shot

STORY = dict(name="wolf-ep02", accent=(214, 40, 40), voice="eric", speed=1.03, tempo=0.93, end_hold=1.5)


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
         ("three-second", TXT("3 SECONDS", 220, cap="the test")), ("saved", shot(*herd(s=0.9), caption="every sheep"))),
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
        ("I hire a room full of very charming wolves with very loud telephones.", shot(dict(kind="boiler")), ("loud", shot(wolf(820, "phone"), caption="very loud", cap=(1200, 160)))),
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
        ("Belfort later pleaded guilty to securities fraud and money laundering.", shot(dict(kind="gavel", x=900, y=640)), ("money", TXT("FRAUD", 280, (214, 40, 40), cap="+ money laundering"))),
        ("He spent about twenty-two months in prison.", TXT("22 MONTHS", 200)),
        ("And a court ordered him to pay back about one hundred and ten million dollars to his victims.", shot(dict(kind="gavel", x=900, y=640), caption="the court"), ("pay", TXT("$110,000,000", 190, (214, 40, 40), cap="to his victims"))),
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
         ("charged", TXT("8 INFLUENCERS", 170)), ("pump", shot(sheep(c="shades"), caption="pump and dump")), ("worth", TXT("$100,000,000", 190, (214, 40, 40)))),
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

# ================= расширение до 10–12 минут =================
GARY_CALL = seq([
    ("Let me show you how it really works.", shot(wolf(960, "phone"))),
    ("Meet my favourite customer.", shot(gary(), caption="gary")),
    ("Gary.", MEME()),
    ("Ring ring.", shot(wolf(500, "phone", s=1.2), gary(1350, s=1.3), caption="ring ring")),
    ("Gary, my friend.", shot(wolf(820, "phone"), caption="friend", cap=(1200, 160))),
    ("You seem like a smart sheep.", shot(gary(), caption="(he is not)")),
    ("I don't call just anyone.", FACE("he calls everyone")),
    ("I've got something special. But it's only for today.", shot(stall(960, sign=MIRACLE)), ("only", TXT("ONLY TODAY", 170, (214, 40, 40)))),
    ("Half the meadow is already in.", shot(*herd(s=0.9), caption="(they aren't)")),
    ("Start small. Just ten receipts.", shot(dict(kind="notes", x=520, y=760, n0=2, step=2, at=["small", "just", "ten", "receipts"], cols=4, s=1.3))),
    ("And Gary says yes.", shot(gary(), caption="yes")),
    ("Of course he does.", FACE("of course")),
], mood="tense")

BREAKDOWN = seq([
    ("Let's break down exactly what I did to Gary.", T("THE SALES\nSCRIPT")),
    ("Trick number one. Flattery.", TXT("1. FLATTERY", 160, cap="you seem smart")),
    ("A sheep who feels smart stops asking questions.", shot(gary(), caption="no questions")),
    ("Trick number two. A deadline.", TXT("2. DEADLINE", 160, (214, 40, 40), cap="only today")),
    ("No time to think means no time to say no.", FACE("tick tock")),
    ("Trick number three. Everyone else is doing it.", TXT("3. THE HERD", 160, cap="half the meadow")),
    ("Sheep trust sheep more than they trust facts.", shot(*herd(s=0.9))),
    ("Trick number four. Start small.", TXT("4. START SMALL", 160, cap="just ten receipts")),
    ("Ten receipts feels safe.", shot(dict(kind="notes", x=520, y=760, n0=10, cols=5, s=1.3))),
    ("Next week, I'll call again, and ask for a hundred.", shot(wolf(820, "phone")), ("hundred", shot(dict(kind="notes", x=320, y=880, n0=30, cols=6, s=1.3), caption="a hundred"))),
    ("Four tricks. One phone call.", shot(wolf(960, "phone"))),
    ("Gary never had a chance.", MEME()),
], mood="tense")

FOMO = seq([
    ("But why do sheep fall for it, again and again?", FACE()),
    ("It has a name.", T("F.O.M.O.")),
    ("Fear of missing out.", TXT("FEAR OF MISSING OUT", 120)),
    ("When the sheep next to you gets rich, your brain doesn't see a graph.", shot(sheep(400, c="shades", s=1.3), sheep(1250, f=0.8, mood="sad", s=1.3)), ("brain", shot(chart("up"), caption="not this"))),
    ("It sees a sheep with more wool than you.", shot(sheep(c="shades"), caption="this")),
    ("And that hurts more than losing.", shot(sheep(f=0.7, mood="sad"), caption="ouch")),
    ("So you buy at the top.", shot(chart("peak"), caption="the top")),
    ("Right when the wolves are selling.", FACE("hi")),
    ("Greed brings you in.", TXT("GREED", 260, (40, 160, 70))),
    ("Fear makes you sell at the bottom.", shot(chart("crash")), ("fear", TXT("FEAR", 260, (214, 40, 40)))),
    ("Buy high, sell low.", T("BUY HIGH,\nSELL LOW")),
    ("The sheep's favourite strategy.", MEME()),
], mood="tense")

SOUTH_SEA = seq([
    ("And this is not new.", shot(wolf(960))),
    ("Not even close.", FACE()),
    ("London, seventeen twenty.", TXT("LONDON, 1720", 200)),
    ("The South Sea Company promised huge profits from trade with South America.", shot(stall(960, sign="SOUTH SEA CO.")), ("huge", TXT("HUGE PROFITS", 170, (40, 160, 70)))),
    ("Everyone wanted in.", shot(*herd(mood="shock", s=0.9), caption="everyone")),
    ("Shares that cost around one hundred pounds at the start of the year went to around one thousand by the summer.", shot(chart("start"), caption="£100"),
     ("year", shot(chart("up"), caption="up")), ("thousand", TXT("£1,000", 260, (40, 160, 70), cap="by summer"))),
    ("Then the bubble popped.", shot(chart("crash"))),
    ("By the end of the year, most of that was gone.", TXT("GONE", 300, (214, 40, 40))),
    ("Even Isaac Newton reportedly lost a fortune.", shot(sheep(f=0.3, mood="sad", c="scarf"), caption="isaac newton (probably)")),
    ("The smartest man in England.", FACE("smartest")),
    ("Fleeced.", MEME()),
    ("Three hundred years later, the costumes changed.", TXT("300 YEARS", 220)),
    ("The trick didn't.", T("SAME\nTRICK")),
], mood="tense")

MEMECOIN = seq([
    ("Here's how a modern pump looks, step by step.", T("THE MODERN\nPUMP")),
    ("Someone creates a coin in five minutes.", shot(dict(kind="coin", x=960, y=520, r=230), caption="5 minutes")),
    ("They keep a big pile for themselves.", shot(dict(kind="notes", x=320, y=880, n0=24, cols=6, s=1.3), caption="for themselves")),
    ("They pay accounts to shout about it.", shot(chat("NEXT 100x", "dont fade this", "LFG"))),
    ("Sheep rush in.", shot(*herd(mood="shock", s=0.9), caption="rush")),
    ("The price goes vertical.", shot(chart("peak"))),
    ("The creators sell.", FACE("sold")),
    ("Sometimes, the whole thing takes a few hours.", TXT("A FEW HOURS", 180, (214, 40, 40))),
    ("By the time Gary hears about it, it's already over.", shot(gary(), caption="too late")),
], mood="tense")

IF_BOUGHT = seq([
    ("And if you already bought something like this?", FACE()),
    ("Don't let the same chat talk you into buying more to win it back.", shot(chat("buy the dip!!", "hold!!", "trust me bro")), ("win", shot(gary(), caption="don't"))),
    ("That's how one haircut becomes two.", shot(sheep(f=0.4, mood="sad")), ("two", MEME())),
], mood="hope")

CONFESSION = seq([
    ("You know what's funny?", FACE()),
    ("I didn't even need to lie about the company.", shot(stall(960, sign=MIRACLE), caption="no lies needed")),
    ("I just needed you to stop thinking.", T("STOP\nTHINKING")),
    ("Every pump in history works the same way.", shot(wolf(960))),
    ("Excitement goes up.", shot(chart("up"), caption="excitement")),
    ("Thinking goes down.", shot(gary(), caption="thinking")),
    ("And somewhere in the middle, a wolf gets very fluffy.", shot(wolf(960), caption="fluffy")),
], mood="tense")

LEGAL = seq([
    ("So, is this legal?", T("IS THIS\nLEGAL?")),
    ("No.", FACE("no")),
    ("Hyping a stock with lies so you can dump it on other people is market manipulation and fraud.", shot(chart("crash"), caption="lies"), ("market", TXT("MARKET MANIPULATION", 120)), ("fraud", TXT("FRAUD", 300, (214, 40, 40)))),
    ("Regulators like the SEC chase it.", shot(dict(kind="gavel", x=900, y=640), caption="the SEC")),
    ("But they usually arrive after the sheep are already bald.", shot(sheep(260, 0.0, "shock", s=1.0), sheep(760, 0.0, "shock", s=1.0), gary(1260, s=1.0))),
    ("Justice is slow.", FACE("slow")),
    ("Wool grows back even slower.", shot(sheep(f=0.2, mood="sad"), caption="slower")),
], mood="tense")

REAL_VS = seq([
    ("So how do you tell a real company from a pump?", T("REAL OR\nPUMP?")),
    ("A real company grows wool slowly.", shot(stall(960), caption="slow")),
    ("It sells more grass every year.", shot(dict(kind="grass", x=500, y=900, n=8, s=1.6), caption="more grass")),
    ("Its price goes up because the business grows, not because someone shouts.", shot(chart("up")), ("not", shot(chat("TO THE MOON", "TO THE MOON", "TO THE MOON")))),
    ("A pump has a story. No business.", shot(stall(960, sign=MIRACLE), caption="just a story")),
    ("So ask two boring questions.", shot(wolf(960))),
    ("What does this company actually sell?", TXT("WHAT DO THEY SELL?", 130)),
    ("And does it make any money?", TXT("DO THEY MAKE MONEY?", 130)),
    ("If the answer is vibes, you know what to do.", FACE("vibes")),
], mood="hope")

LEGEND = seq([
    ("There's an old Wall Street legend.", T("A WALL STREET\nLEGEND")),
    ("New York, nineteen twenty-nine.", TXT("NEW YORK, 1929", 190)),
    ("A rich investor stops to get his shoes shined.", shot(sheep(c="shades"), caption="rich")),
    ("And the shoeshine boy gives him a stock tip.", shot(sheep(480, s=1.3), sheep(1250, c="shades", s=1.3), caption="a stock tip")),
    ("The investor thinks: if even the shoeshine boy is buying, who's left to buy?", FACE("who's left?")),
    ("So he sells everything.", shot(chart("peak"), caption="sell")),
    ("Weeks later, the market crashes.", shot(chart("crash"))),
    ("Nobody knows if the story is true.", FACE("legend")),
    ("But the lesson is.", shot(wolf(960))),
    ("When everyone is shouting buy, the wolves are already selling.", T("EVERYONE BUYING?\nWOLVES SELLING")),
], mood="tense")

RECAP = seq([
    ("Okay. Let's put it all in one place.", T("CHEAT\nSHEET")),
    ("Four tricks.", shot(wolf(960))),
    ("Flattery.", TXT("FLATTERY", 220)),
    ("A deadline.", TXT("DEADLINE", 220, (214, 40, 40))),
    ("The herd.", TXT("THE HERD", 220)),
    ("Start small.", TXT("START SMALL", 200)),
    ("One test.", shot(wolf(960))),
    ("Why are they telling me?", T("WHY ARE THEY\nTELLING ME?")),
    ("Screenshot this. Send it to the Gary in your life.", shot(gary(), caption="send to your gary")),
], mood="hope")

GARY_END = seq([
    ("And Gary?", shot(gary())),
    ("Gary's fine.", shot(gary(), caption="fine")),
    ("Bald. But fine.", MEME()),
    ("And this morning, his phone rang again.", shot(wolf(500, "phone", s=1.2), gary(1350, s=1.3), caption="ring ring")),
], mood="hope")

_b = BLOCKS
BLOCKS = [_b[0], GARY_CALL, _b[1], _b[2], _b[3], _b[4], BREAKDOWN, _b[5], FOMO, CONFESSION, SOUTH_SEA, _b[6], LEGAL, _b[7], LEGEND, MEMECOIN, IF_BOUGHT, REAL_VS, _b[8], RECAP, GARY_END, _b[9]]
