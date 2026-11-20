"""The Sheep Standard — EP01: How Inflation Fleeces You. Монтаж по плагину doodle-explainer-edit.
Факты (в описание): Германия ноябрь 1923 — буханка ~200 млрд марок; Зимбабве 2008 — цены удваивались ~каждые 24 ч
(Hanke & Kwok, Cato Journal 2009), купюра 100 трлн Z$; США июнь 2022 — инфляция 9,1% г/г (BLS), максимум ~40 лет;
ориентир многих центробанков ~2%/год."""
from doodle import seq, shot

STORY = dict(name="wolf-ep01", accent=(214, 40, 40), voice="eric", speed=1.03, end_hold=1.5)


def wolf(x=960, pose="stand", s=1.4, **k):
    return dict(kind="wolf", x=x, pose=pose, s=s, **k)


def sheep(x=860, f=1.0, mood="calm", c=None, s=1.8, **k):
    return dict(kind="sheep", x=x, f=f, mood=mood, c=c, s=s, **k)


def gary(x=860, s=1.8, **k):
    return dict(kind="gary", x=x, s=s, **k)


def notes(x, y, n0, at=(), step=1, cols=4, s=1.1):
    return dict(kind="notes", x=x, y=y, n0=n0, at=list(at), step=step, cols=cols, s=s)


def grassn(x=700, y=880, n=8, s=1.6):
    return dict(kind="grass", x=x, y=y, n=n, s=s)


def stall(x=1350, price=None):
    return dict(kind="stall", x=x, price=price)


MEME = lambda: shot(kind="gary")          # повторяющийся мем-панч: Гэри крупно
FACE = lambda cap=None: shot(kind="wolfface", caption=cap, cap=(1150, 120))
T = lambda t: shot(kind="title", title=t)
TXT = lambda t, size=200, color=(17, 17, 17), cap=None: shot(dict(kind="text", text=t, size=size, y=400, color=color), caption=cap)

BLOCKS = [
    seq([
        ("Hello, sheep.", shot(wolf(960))),
        ("I'm a wolf.", FACE()),
        ("I work in finance.", shot(wolf(820), caption="(trust me)", cap=(1150, 160))),
        ("And today, I'm going to show you how you lose wool every single year.", shot(wolf(820)), ("lose", shot(sheep(), caption="your wool"))),
        ("Without anyone touching you.", shot(sheep(f=0.45, mood="sad"), caption="nobody touched her")),
        ("It's called inflation.", T("INFLATION")),
        ("And honestly?", FACE()),
        ("It's my favourite haircut.", shot(wolf(820, "shears"), caption="*snip*", cap=(1250, 160))),
        ("Stick around, because at the end, I'll tell you exactly who's holding the scissors.", shot(wolf(960)),
         ("tell", shot(wolf(820, "shears"), caption="(spoiler: not you)", cap=(1150, 160)))),
    ], mood="hope"),
    seq([
        ("First, the rules.", T("WOOL\n= WEALTH")),
        ("In this world, wool is wealth.", shot(sheep(330, 1.0, s=1.2), sheep(880, 0.5, "sad", s=1.2), gary(1430, s=1.2))),
        ("A fluffy sheep is a rich sheep.", shot(sheep(c="shades"), caption="rich")),
        ("A bald sheep…", shot(gary())),
        ("well.", MEME()),
        ("That's Gary.", shot(wolf(520), gary(1250, s=1.4), caption="say hi to gary", cap=(1000, 140))),
        ("You'll be seeing a lot of Gary.", FACE()),
    ]),
    seq([
        ("Now, paying with wool is a nightmare.", shot(sheep(480, 0.8, "sad", s=1.4), stall(), caption="ouch")),
        ("You walk into a shop, and you pay with a chunk of your own back.", shot(sheep(480, 1.0, s=1.4), stall()),
         ("pay", shot(sheep(f=0.55, mood="sad"), caption="itchy"))),
        ("So the King of the sheep had an idea.", shot(sheep(c="crown"))),
        ("Give him your wool, and he gives you a receipt.", shot(sheep(420, c="crown", s=1.5), dict(kind="note", x=1150, y=420, s=1.7, **{"in": "receipt"}))),
        ("One receipt. One bag of wool.", shot(dict(kind="note", x=600, y=330, s=3.0), caption="(receipt = money)")),
        ("Light. Clean. Doesn't itch.", shot(notes(520, 620, 1, at=["clean", "itch"], cols=3, s=1.4))),
        ("Congratulations, sheep.", FACE("clap clap")),
        ("You just invented money.", T("MONEY")),
    ]),
    seq([
        ("Now, here's the only formula in this whole video.", shot(wolf(960), caption="i promise")),
        ("Price equals money, divided by stuff.", T("PRICE = MONEY\n÷ STUFF")),
        ("In the whole meadow, there are one hundred receipts.", shot(notes(380, 780, 2, step=2, at=["whole", "meadow", "hundred", "receipts"], cols=4, s=1.3), caption="100 receipts")),
        ("And one hundred bundles of grass.", shot(grassn(560, 900, 8, 1.9), caption="100 grass")),
        ("So one bundle of grass costs one receipt.", shot(sheep(420, s=1.4), stall(1350, 1))),
        ("Simple. Fair. Boring.", shot(kind="sheepface", c="hat", caption="boring", cap=(1400, 120))),
        ("Until the King gets an idea.", shot(sheep(c="crown"), caption="uh oh")),
    ]),
    seq([
        ("This is called monetary inflation.", T("MONETARY\nINFLATION")),
        ("The King wants a statue.", shot(sheep(c="crown"))),
        ("A giant, golden statue.", shot(dict(kind="statue", x=960))),
        ("Of himself.", shot(dict(kind="statue", x=960), caption="of course")),
        ("But statues are expensive, and he doesn't have enough receipts.", shot(dict(kind="statue", x=1350), sheep(380, c="crown", s=1.3)),
         ("doesn't", shot(sheep(f=1.0, mood="sad", c="crown")))),
        ("He could raise taxes.", shot(sheep(c="crown"))),
        ("But sheep hate taxes.", shot(sheep(330, 1.0, "shock", s=1.2), sheep(880, 1.0, "sad", s=1.2), sheep(1430, 1.0, "shock", s=1.2), caption="boooo")),
        ("He could borrow.", shot(sheep(c="crown"))),
        ("But that's embarrassing.", FACE("cringe")),
        ("Then he looks at his stamp.", shot(sheep(480, c="crown", s=1.5), dict(kind="stamp", x=1350, y=520))),
        ("And he realizes something beautiful.", FACE("here we go")),
        ("Sheep take a whole spring to grow.", shot(sheep(f=0.4), caption="slow")),
        ("Receipts take one stamp.", shot(dict(kind="stamp", x=420, y=520), notes(760, 760, 1, at=["take", "one", "stamp"], cols=4, s=1.3))),
        ("So he stamps one hundred brand new receipts.", shot(notes(380, 880, 4, step=3, at=["stamps", "hundred", "brand", "new", "receipts"], cols=6, s=1.3))),
        ("No new wool behind them.", shot(gary(), caption="no wool")),
        ("Just ink, and optimism.", shot(notes(380, 880, 19, cols=6, s=1.3), caption="just vibes")),
    ], mood="tense"),
    seq([
        ("Now here's the question that really matters.", shot(wolf(960))),
        ("Who gets the new receipts first?", T("WHO GETS IT\nFIRST?")),
        ("The builders.", shot(sheep(c="helmet"))),
        ("The King's friends.", shot(sheep(500, c="crown", s=1.4), sheep(1250, c="shades", s=1.4))),
        ("And the bank.", shot(wolf(960))),
        ("I am the bank.", FACE("hi")),
        ("I take the new receipts, walk into the shop, and buy grass at the old price.", shot(wolf(820, "present")),
         ("walk", shot(wolf(500, "present"), stall(1450, 1)))),
        ("One receipt.", shot(stall(960, 1))),
        ("Lovely.", FACE("lovely")),
    ], mood="tense"),
    seq([
        ("But now, look at the meadow.", shot(notes(260, 820, 24, cols=6), grassn(1150, 900, 8, 1.4))),
        ("Two hundred receipts.", shot(notes(300, 900, 30, cols=6, s=1.3), caption="200 receipts")),
        ("Still one hundred bundles of grass.", shot(grassn(560, 900, 8, 1.9), caption="same grass")),
        ("The shopkeeper sees a long line of sheep, all waving receipts.", shot(sheep(220, s=1.0), sheep(560, s=1.0), stall(1400, 1)),
         ("waving", shot(kind="sheepface", c="hat"))),
        ("So she does what any shopkeeper would do.", shot(stall(960, 1))),
        ("Two receipts.", shot(stall(960, 2))),
        ("Same grass.", shot(grassn(560, 900, 8, 1.9))),
        ("Prices double.", MEME()),
        ("That, sheep, is inflation.", shot(wolf(960))),
    ], mood="tense"),
    seq([
        ("And here's the trick.", FACE()),
        ("Watch this sheep.", shot(sheep())),
        ("She earns ten receipts a week.", shot(sheep(480, s=1.4), notes(1050, 760, 2, step=2, at=["earns", "ten", "receipts", "week"], cols=4, s=1.2))),
        ("Nobody cut her pay.", shot(sheep(), caption="untouched")),
        ("Nobody touched her.", shot(sheep(f=0.9))),
        ("But grass costs twice as much now.", shot(stall(960, 2))),
        ("So every week, she can buy less.", shot(sheep(f=0.5, mood="sad"))),
        ("Inflation doesn't take your wool.", FACE()),
        ("It makes your wool worth less.", T("WORTH LESS")),
        ("But that's not the worst part.", shot(wolf(960))),
        ("Grandma saved receipts her whole life.", shot(sheep(480, c="scarf", s=1.4), dict(kind="chest", x=1350, n=5))),
        ("Overnight, her savings buy half as much grass.", shot(sheep(f=0.4, mood="sad", c="scarf"))),
        ("Nobody stole from Grandma.", shot(wolf(960))),
        ("Technically.", MEME()),
    ], mood="tense"),
    seq([
        ("So who wins?", FACE()),
        ("Whoever gets the new money first.", T("FIRST SPENDER\nWINS")),
        ("They spend it before prices go up.", shot(wolf(330, s=1.1), stall(1250, 1))),
        ("Everyone after them pays.", shot(sheep(400, 1.0, s=1.1), sheep(900, 0.6, "sad", s=1.1), gary(1400, s=1.1))),
        ("But the statue still isn't finished.", shot(dict(kind="statue", x=960, headless=True))),
        ("And now the builders want more receipts, because everything costs more.", shot(sheep(c="helmet"), caption="pay up"),
         ("because", shot(stall(960, 2)))),
        ("So the King prints more.", shot(notes(380, 880, 12, step=6, at=["prints", "more"], cols=6, s=1.3))),
        ("Prices go up.", shot(stall(960, 4))),
        ("He prints more.", shot(notes(380, 880, 30, cols=6, s=1.3))),
        ("Prices go up again.", shot(stall(960, 100))),
        ("When this spins out of control, it's called hyperinflation.", FACE(), ("it's", T("HYPER-\nINFLATION"))),
        ("And that's how a sheep ends up pushing a wheelbarrow of receipts to buy one salad.", shot(sheep(380, 0.6, "sad", s=1.3), dict(kind="barrow", x=1200, n=6)),
         ("buy", shot(grassn(860, 880, 1, 2.6), caption="one salad"))),
    ], mood="tense"),
    seq([
        ("But printing isn't the only way to get fleeced.", shot(wolf(960))),
        ("Sometimes, nobody prints anything.", shot(notes(380, 780, 8, cols=4, s=1.3), caption="same receipts")),
        ("A storm hits the meadow, and half the grass is gone.", shot(grassn(560, 900, 8, 1.9), caption="storm"), ("half", shot(grassn(700, 900, 4, 1.9)))),
        ("Same receipts.", shot(notes(380, 780, 8, cols=4, s=1.3))),
        ("Half the grass.", shot(grassn(700, 900, 4, 1.9))),
        ("Prices double, again.", shot(stall(960, 2))),
        ("Economists call this cost-push inflation.", FACE(), ("cost-push", T("COST - PUSH\nINFLATION"))),
        ("Less stuff.", shot(grassn(700, 900, 4, 1.9))),
        ("Same money.", shot(notes(380, 780, 8, cols=4, s=1.3))),
        ("Higher prices.", shot(stall(960, 2))),
    ], mood="tense"),
    seq([
        ("Meanwhile, in the real world.", T("MEANWHILE,\nIN THE REAL WORLD")),
        ("You think this is a cartoon?", FACE()),
        ("It's not.", FACE("it's not")),
        ("Germany, nineteen twenty-three.", TXT("GERMANY, 1923", 170)),
        ("The government printed money to pay its bills.", shot(dict(kind="barrow", x=960, n=6))),
        ("By November, a single loaf of bread cost around two hundred billion marks.", shot(grassn(860, 880, 1, 2.6), caption="one loaf of bread"),
         ("two", TXT("200,000,000,000", 170, (214, 40, 40)))),
        ("People were paid twice a day, and ran to the shops before prices changed again.", shot(sheep(400, 1.0, "shock", s=1.1), sheep(1300, 1.0, "shock", s=1.1), caption="paid twice a day"),
         ("ran", shot(sheep(f=1.0, mood="shock"), caption="run"))),
        ("Zimbabwe, two thousand eight.", TXT("ZIMBABWE, 2008", 170)),
        ("Prices were doubling roughly every day.", TXT("x2   x2   x2   x2", 170)),
        ("The country printed a one hundred trillion dollar note.", shot(dict(kind="note", x=440, y=320, s=4.4, text="100,000,000,000,000"))),
        ("And in the United States, in June twenty twenty-two, prices were rising at nine point one percent a year.", TXT("USA, 2022", 170),
         ("prices", TXT("9.1%", 340, (214, 40, 40), cap="per year"))),
        ("The highest in about forty years.", FACE("40 years")),
        ("Same story every time.", shot(wolf(960))),
        ("More money, or less stuff.", T("MORE MONEY\nOR LESS STUFF")),
        ("Higher prices.", MEME()),
    ], mood="tense"),
    seq([
        ("So, is all inflation bad?", FACE()),
        ("Not really.", shot(wolf(960))),
        ("A little is normal.", shot(sheep(f=0.95))),
        ("Many central banks aim for about two percent a year.", TXT("2%", 360, cap="per year")),
        ("Slow, and predictable.", FACE()),
        ("The problem is fast inflation.", shot(stall(960, 100))),
        ("Because fast inflation shears the sheep who can least afford it.", shot(sheep(500, 0.4, "sad", c="scarf", s=1.4), gary(1250, s=1.4))),
        ("So, since I'm in a generous mood.", T("HOW TO KEEP\nYOUR WOOL")),
        ("One. Cash sitting still slowly loses value.", shot(notes(620, 700, 6, cols=3, s=1.4), caption="1. cash shrinks")),
        ("It's a melting ice cube.", shot(dict(kind="ice", x=960, y=560), caption="melting")),
        ("Two. If your pay doesn't grow with prices, you're getting a haircut.", shot(sheep(f=0.6, mood="sad"), caption="2. pay must grow")),
        ("Ask for a raise.", FACE("ask")),
        ("Three. Learn how saving and investing work, so your wool grows faster than prices.", shot(sheep(f=0.6), caption="3. learn to invest"),
         ("so", shot(sheep(c="shades"), caption="grow it"))),
        ("Not financial advice.", FACE("not financial advice")),
        ("I'm a wolf.", shot(wolf(960))),
    ], mood="hope"),
    seq([
        ("Oh, and the scissors.", shot(wolf(820, "shears"))),
        ("I promised.", FACE()),
        ("Who's holding them?", T("WHO HOLDS\nTHE SCISSORS?")),
        ("Whoever gets the new money first.", T("FIRST SPENDER\nWINS")),
        ("This time?", FACE()),
        ("That was me.", FACE("hi again")),
        ("If you don't want to end up bald like Gary… subscribe.", shot(kind="outro")),
        ("Gary didn't.", shot(kind="outro", caption="gary didn't.", cap=(1100, 200))),
    ], mood="hope", pause=1.6),
]
