"""The Sheep Standard — EP05: How Christmas Fleeces You. Монтаж по плагину doodle-explainer-edit. Голос Eric. Выход 1–5 декабря.
Факты (источники в ../sheep-standard/ep05/PACKAGE.md):
- NRF: праздничные продажи ноябрь–декабрь 2025 впервые > $1 трлн (прогноз $1,01–1,02 трлн).
- NRF/Prosper 2025: в среднем ~$890 на человека (подарки, еда, украшения), из них подарки ~$628.
- LendingTree (опрос 10–15 дек. 2025): 37% взяли праздничный долг, в среднем $1 223; 41% из них ещё платили за прошлый год; 48% родителей детей до 18 занимали.
- Наш расчёт: $1 223 под 22%, минимум = 1% + проценты (не меньше $25) → ~90 мес. (7,5 лет), ~$1 175 процентов.
- Joel Waldfogel, «The Deadweight Loss of Christmas», American Economic Review, 1993: получатели ценят подарки меньше их цены (оценки ~10–33%).
- Flynn & Adams, «Money can't buy love», Journal of Experimental Social Psychology, 2009: дарители думают, что дорогой подарок ценят больше; получатели — нет.
"""
from doodle import seq, shot

STORY = dict(name="wolf-ep05", accent=(214, 40, 40), voice="eric", speed=1.03, tempo=0.93, end_hold=1.5)
GREEN, RED, BLUE = (40, 160, 70), (214, 40, 40), (40, 120, 210)


def wolf(x=960, pose="stand", s=1.4, **k):
    return dict(kind="wolf", x=x, pose=pose, s=s, **k)


def sheep(x=860, f=1.0, mood="calm", c=None, s=1.8, **k):
    return dict(kind="sheep", x=x, f=f, mood=mood, c=c, s=s, **k)


def gary(x=860, s=1.8, **k):
    return dict(kind="gary", x=x, s=s, **k)


def herd(f=1.0, mood="calm", s=0.9):
    return [sheep(260, f, mood, s=s), sheep(760, f, mood, s=s), sheep(1260, f, mood, s=s)]


def gift(x=960, y=600, s=1.3, col=RED, label=None):
    return dict(kind="gift", x=x, y=y, s=s, col=col, label=label)


def gifts(n=3, s=0.9):
    xs = [360, 960, 1560, 660, 1260][:n]
    cols = [RED, BLUE, GREEN, RED, BLUE]
    return [gift(x, 640, s, cols[i]) for i, x in enumerate(xs)]


def card(x=960, y=540, s=1.6, text="WOLF CARD"):
    return dict(kind="card", x=x, y=y, s=s, text=text)


def bill(*lines, x=650, y=160, s=1.0):
    return dict(kind="bill", x=x, y=y, s=s, lines=[(t[1:], True) if t.startswith("!") else (t, False) for t in lines])


def chat(*msgs, title="Wolf Store", x=780):
    return dict(kind="phone", x=x, y=200, s=1.0, title=title, msgs=list(msgs))


def store(sign="WOLF STORE", price=None):
    return dict(kind="stall", x=960, sign=sign, price=price)


MEME = lambda: shot(kind="gary")
FACE = lambda cap=None: shot(kind="wolfface", caption=cap, cap=(1150, 120))
T = lambda t: shot(kind="title", title=t)
TXT = lambda t, size=200, color=(17, 17, 17), cap=None: shot(dict(kind="text", text=t, size=size, y=400, color=color), caption=cap)
GIFT = lambda cap=None, **k: shot(gift(**k), caption=cap)

HOOK = seq([
    ("Sheep.", shot(wolf(960))),
    ("The most expensive day of your year isn't Black Friday.", T("NOT BLACK\nFRIDAY")),
    ("It's a quiet morning in January.", TXT("JANUARY", 240)),
    ("When this arrives.", shot(bill("Balance: $1,223", "!Minimum: $35", "Rate: 22%"))),
    ("Every year, I get the best present of all.", FACE("best present")),
    ("Your wool.", shot(sheep(f=0.3, mood="sad"), caption="your wool")),
    ("Today, I'll show you exactly how Christmas fleeces you.", T("HOW CHRISTMAS\nFLEECES YOU")),
    ("And at the end, one simple rule that turns a holiday loan back into a gift.", shot(wolf(960)), ("rule", TXT("ONE RULE", 240, GREEN))),
    ("Gary never heard it.", MEME()),
], mood="tense")

NUMBERS = seq([
    ("Let's start with the numbers.", T("THE NUMBERS")),
    ("In twenty twenty-five, Americans were expected to spend over one trillion dollars on the holidays.", TXT("$1 TRILLION", 220, RED), ("holidays", shot(*gifts(3)))),
    ("For the first time ever.", TXT("FIRST TIME EVER", 170)),
    ("That's about nine hundred dollars per sheep.", TXT("~$890", 300, cap="per person")),
    ("Gifts. Food. Decorations.", GIFT(), ("food", TXT("FOOD", 260)), ("decorations", TXT("DECORATIONS", 200))),
    ("And here's the part I love.", FACE("i love this")),
    ("More than one in three people took on debt to pay for it.", TXT("37%", 360, RED, cap="took on debt")),
    ("On average, about twelve hundred dollars.", TXT("$1,223", 300, RED, cap="average holiday debt")),
    ("And four in ten of them were still paying off the year before.", TXT("41%", 360, RED, cap="still paying last year")),
    ("Last year's presents.", GIFT("last year's", col=BLUE)),
    ("Still unwrapping the bill.", MEME()),
], mood="tense")

GARY_XMAS = seq([
    ("Let's watch Gary's Christmas.", T("GARY'S\nCHRISTMAS")),
    ("Presents for Mom. For Dad. For the cousins.", shot(gift(500, 640, 0.9)), ("dad", shot(gift(500, 640, 0.9), gift(960, 640, 0.9, BLUE))), ("cousins", shot(*gifts(5, 0.7)))),
    ("For the coworker he barely knows.", shot(gift(960, 640, 0.9, GREEN), caption="who is this?")),
    ("A bigger tree than last year.", shot(dict(kind="tree", x=960, n=0, s=1.1), caption="bigger than last year")),
    ("A flight home.", TXT("FLIGHT HOME", 220)),
    ("A dinner for twelve.", TXT("DINNER FOR 12", 200)),
    ("All on the card.", shot(card(), caption="all of it")),
    ("Gary feels amazing.", shot(gary(), caption="amazing")),
    ("For about three weeks.", TXT("3 WEEKS", 260)),
    ("Then January arrives.", TXT("JANUARY", 260, RED)),
    ("One thousand, two hundred dollars.", shot(bill("Balance: $1,223", "!Minimum: $35", "Rate: 22%")), ("hundred", TXT("$1,223", 300, RED))),
    ("Minimum payment: about thirty-five dollars.", TXT("$35", 340, GREEN, cap="so friendly")),
    ("You know where this goes.", FACE("you know")),
    ("If Gary pays only the minimum, that Christmas takes about seven and a half years to pay off.", TXT("7.5 YEARS", 280, RED)),
    ("And costs him almost twelve hundred dollars more in interest.", TXT("+$1,175", 300, RED, cap="interest")),
    ("One Christmas. Paid for twice.", T("PAID FOR\nTWICE")),
    ("By the time it's paid off, the cousins will be in college.", shot(*herd(s=0.9), caption="the cousins, all grown up")),
], mood="tense")

CREEP = seq([
    ("Now, let me show you how I set the trap.", shot(wolf(960, "present"))),
    ("Trick one. Christmas creep.", TXT("1. CHRISTMAS CREEP", 150)),
    ("Ever notice the decorations show up in September?", TXT("SEPTEMBER?!", 230, RED)),
    ("That's not an accident.", FACE("not an accident")),
    ("A longer season means more weeks of shopping.", shot(store(), caption="open since september")),
    ("More weeks of shopping means more wool.", shot(dict(kind="notes", x=320, y=880, n0=4, step=4, at=["weeks", "shopping", "more", "wool"], cols=6, s=1.3))),
    ("If I could start Christmas in July, I would.", FACE("i would")),
], mood="calm")

FAKE_SALE = seq([
    ("Trick two. The fake discount.", TXT("2. FAKE DISCOUNT", 160)),
    ("Was one ninety-nine. Now ninety-nine.", shot(store(price="$199")), ("now", TXT("$99", 340, GREEN))),
    ("Half off!", T("HALF OFF!")),
    ("Except it almost never really sold for one ninety-nine.", TXT("$199?", 300, RED, cap="never real")),
    ("That first number isn't a price.", FACE()),
    ("It's an anchor.", T("AN ANCHOR")),
    ("It's there so ninety-nine feels like a gift.", TXT("$99 = GIFT?", 220)),
    ("You didn't save one hundred dollars.", TXT("SAVED $100?", 220, RED)),
    ("You spent ninety-nine.", TXT("SPENT $99", 240)),
], mood="calm")

SHIPPING = seq([
    ("Trick three. Free shipping.", TXT("3. FREE SHIPPING", 160)),
    ("Free shipping on orders over fifty dollars.", shot(chat("FREE SHIPPING", "on orders $50+", "you're at $41!"))),
    ("Gary's cart is at forty-one.", TXT("$41", 300)),
    ("Shipping costs six.", TXT("$6", 300, RED, cap="shipping")),
    ("So Gary adds a fifteen dollar candle he doesn't need, to save six.", shot(gift(960, 640, 0.9, GREEN), caption="a candle"), ("save", TXT("+$15 TO SAVE $6", 160, RED))),
    ("Free shipping is never free.", T("NEVER\nFREE")),
    ("It's a minimum order in a costume.", FACE("a costume")),
], mood="calm")

TIMER = seq([
    ("Trick four. The countdown.", TXT("4. THE COUNTDOWN", 160)),
    ("Deal ends in two hours.", TXT("ENDS IN 02:00:00", 160, RED)),
    ("Only three left.", TXT("ONLY 3 LEFT", 220, RED)),
    ("Remember from my pump and dump video?", FACE()),
    ("A deadline means no time to think.", T("NO TIME\nTO THINK")),
    ("And a sheep who doesn't think buys more.", shot(*herd(mood="shock"), caption="buy buy buy")),
    ("Funny thing. Next week, the same deal comes back.", TXT("NEXT WEEK: SAME DEAL", 130)),
    ("With a brand new timer.", FACE("new timer")),
], mood="tense")

GIFT_CARDS = seq([
    ("Trick five. My favourite. Gift cards.", TXT("5. GIFT CARDS", 180)),
    ("You give the store your wool today.", shot(card(text="GIFT CARD"), caption="wool in")),
    ("Your cousin forgets the card in a drawer.", shot(sheep(f=0.8), caption="forgot it")),
    ("Some gift cards are never used.", TXT("NEVER USED", 230, RED)),
    ("The store got the wool. And never had to give anything back.", shot(store(), caption="kept the wool")),
    ("That's not a present for your cousin.", FACE()),
    ("That's a present for me.", FACE("thank you")),
], mood="calm")

BNPL = seq([
    ("And at checkout, one more little friend.", shot(store())),
    ("Buy now, pay later.", TXT("BUY NOW, PAY LATER", 130, RED)),
    ("Four easy payments.", shot(dict(kind="notes", x=520, y=760, n0=1, step=1, at=["four", "easy", "payments"], cols=4, s=1.3))),
    ("For a toy that will be broken by February.", shot(gift(960, 640, 0.9, BLUE), caption="broken by february")),
    ("Payment three is due in March.", TXT("MARCH", 260, RED, cap="payment 3 of 4")),
    ("Christmas lasts a day. The payments last a season.", T("1 DAY\nVS 4 MONTHS")),
], mood="tense")

WHY = seq([
    ("But why do sheep do this to themselves?", FACE()),
    ("Because a price tag feels like love.", T("PRICE = LOVE?")),
    ("A bigger gift feels like a bigger hug.", shot(gift(960, 600, 1.5), caption="a bigger hug?")),
    ("But scientists actually tested this.", TXT("THE STUDY", 230)),
    ("People giving gifts thought expensive gifts would be appreciated more.", shot(gift(960, 600, 1.5), caption="the giver thinks")),
    ("People receiving them? Didn't feel more grateful.", shot(sheep(f=1.0), caption="the receiver: same")),
    ("The extra wool bought nothing.", MEME()),
    ("And an economist named Joel Waldfogel found something even funnier.", TXT("ECONOMIST", 230)),
    ("People usually value the gifts they get at less than what they cost.", TXT("$100 GIFT", 230), ("less", TXT("FEELS LIKE $80", 200, RED))),
    ("He called it the deadweight loss of Christmas.", T("DEADWEIGHT\nLOSS")),
    ("Wool that just disappears.", shot(sheep(f=0.4, mood="sad"), caption="poof")),
    ("Somewhere between your wallet and their face.", FACE("poof")),
], mood="calm")

PRESSURE = seq([
    ("And then there's the gift war.", T("THE GIFT\nWAR")),
    ("Your aunt gave you a fifty dollar gift last year.", shot(sheep(c="scarf"), caption="$50 last year")),
    ("So this year, you feel you have to spend fifty.", TXT("$50", 300)),
    ("So she spends seventy.", TXT("$70", 300, RED)),
    ("Nobody wants it. Nobody can stop.", shot(sheep(500, c="scarf", s=1.4), gary(1350, s=1.4), caption="nobody can stop")),
    ("It's an arms race. With socks.", FACE("with socks")),
], mood="calm")

RULE = seq([
    ("So, I promised you a rule.", shot(wolf(960))),
    ("Here it is.", T("THE RULE")),
    ("If it isn't paid off by January first, it isn't a gift.", TXT("JANUARY 1ST", 220), ("gift", TXT("NOT A GIFT", 240, RED))),
    ("It's a loan.", T("IT'S A LOAN")),
    ("With your name on it.", shot(card(text="YOUR NAME"), caption="your name")),
    ("Wrapped in pretty paper.", GIFT("pretty paper")),
], mood="hope")

HOW = seq([
    ("Here's how to keep your wool this Christmas.", T("KEEP YOUR\nWOOL")),
    ("One. Pick one number before December starts.", TXT("1. ONE NUMBER", 180), ("number", TXT("$300", 300, GREEN, cap="your budget"))),
    ("Not per person. The total.", TXT("THE TOTAL", 230)),
    ("Two. Pay with money you already have.", TXT("2. YOUR WOOL ONLY", 160)),
    ("Debit or cash. Not the card.", shot(card(), caption="not this")),
    ("Three. Big family? Do a Secret Santa.", TXT("3. SECRET SANTA", 170)),
    ("One good gift each instead of twelve bad ones.", shot(gift(960, 600, 1.5, GREEN), caption="one good gift")),
    ("Four. Wait one day before you buy.", TXT("4. WAIT 24H", 200)),
    ("If the deal is gone tomorrow, it was a timer, not a deal.", FACE("just a timer")),
    ("Five. Give time, not stuff.", TXT("5. TIME > STUFF", 180, GREEN)),
    ("A dinner you cooked. A trip together. A letter.", shot(sheep(500, c="scarf", s=1.3), sheep(1300, s=1.3), caption="together")),
    ("Nobody remembers a gift card in ten years.", TXT("10 YEARS LATER", 190)),
    ("Everybody remembers the day you showed up.", shot(*herd(), caption="showed up")),
    ("Not financial advice. I'm a wolf.", FACE("not financial advice")),
], mood="hope")

RECAP = seq([
    ("Cheat sheet.", T("CHEAT\nSHEET")),
    ("The season starts early so you spend longer.", TXT("EARLY = LONGER", 190)),
    ("The first price is an anchor.", TXT("FIRST PRICE = ANCHOR", 130)),
    ("Free shipping isn't free.", TXT("NOT FREE", 240, RED)),
    ("Timers are fake.", TXT("FAKE TIMERS", 220)),
    ("One budget. Your own wool.", TXT("ONE BUDGET", 230, GREEN)),
    ("Paid by January first, or it's a loan.", T("JAN 1 RULE")),
    ("Send this to the Gary in your family before he starts shopping.", shot(gary(), caption="send to your gary")),
], mood="hope")

GARY_END = seq([
    ("And Gary?", shot(gary())),
    ("Gary followed the rule this year.", shot(gary(), caption="the rule!")),
    ("No card. No debt.", shot(card(), caption="no card")),
    ("He made every gift himself.", shot(*gifts(3), caption="handmade")),
    ("Warm, cozy sweaters.", GIFT("sweaters")),
    ("Hello, sheep.", FACE()),
    ("If you don't want to end up bald like Gary… subscribe.", shot(kind="outro")),
    ("Gary knitted the sweaters from his own wool.", shot(gift(1500, 820, 0.45), kind="outro", caption="from his own wool.", cap=(820, 200))),
], mood="hope", pause=1.6)

BLOCKS = [HOOK, NUMBERS, GARY_XMAS, CREEP, FAKE_SALE, SHIPPING, TIMER, GIFT_CARDS, BNPL, WHY, PRESSURE, RULE, HOW, RECAP, GARY_END]
