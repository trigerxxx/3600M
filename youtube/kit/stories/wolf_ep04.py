"""The Sheep Standard — EP04: Why the Rich Sheep Get Richer. Монтаж по плагину doodle-explainer-edit. Голос Eric.
Факты (в описание, источники в ../sheep-standard/ep04/PACKAGE.md):
- Наш расчёт (7% в год в среднем, ежемесячно, не гарантия): $500/мес с 25 до 65 → ~$1,31 млн; с 35 → ~$610 тыс.
- Две овцы: A — $300/мес с 25 до 35 (всего $36 тыс.), дальше не вносит → ~$395 тыс. к 65; B — $300/мес с 35 до 65 ($108 тыс.) → ~$366 тыс.
- Комиссия 1% в год: $500/мес 40 лет при 7% → ~$1,31 млн, при 6% → ~$996 тыс. (~$317 тыс. разницы).
- Самые богатые 10% американцев владеют примерно 90% акций (Federal Reserve, Distributional Financial Accounts).
- Фондовый рынок США в среднем ~10% в год за последние ~100 лет до инфляции (S&P 500 и предшественники), с годами больших падений.
- Уоррен Баффетт купил первую акцию в 11 лет; подавляющая часть его состояния появилась после 65 лет (Morgan Housel, The Psychology of Money).
- В США налог на долгосрочный прирост капитала 0/15/20%, на зарплату — до 37% (IRS).
- Шанс сорвать джекпот Powerball — 1 из 292,2 млн (powerball.com).
- «70% победителей лотереи разоряются» — популярная цифра без надёжного источника (её опровергали NEFE и исследователи).
- Рональд Рид (Вермонт), заправщик и уборщик, умер в 2014 г. в 92 года, оставил ~$8 млн, в основном в акциях, которые держал десятилетиями; ~$4,8 млн завещал библиотеке Брэттлборо и ~$1,2 млн больнице (Brattleboro Reformer, WSJ).
"""
from doodle import seq, shot

STORY = dict(name="wolf-ep04", accent=(214, 40, 40), voice="eric", speed=1.03, tempo=0.93, end_hold=1.5)
GREEN, RED = (40, 160, 70), (214, 40, 40)


def wolf(x=960, pose="stand", s=1.4, **k):
    return dict(kind="wolf", x=x, pose=pose, s=s, **k)


def sheep(x=860, f=1.0, mood="calm", c=None, s=1.8, **k):
    return dict(kind="sheep", x=x, f=f, mood=mood, c=c, s=s, **k)


def gary(x=860, s=1.8, **k):
    return dict(kind="gary", x=x, s=s, **k)


def herd(f=1.0, mood="calm", s=0.9):
    return [sheep(260, f, mood, s=s), sheep(760, f, mood, s=s), sheep(1260, f, mood, s=s)]


def tree(x=960, n=6, s=1.0, **k):
    return dict(kind="tree", x=x, n=n, s=s, **k)


def grow(x=960, at=(), n0=2, s=1.0):
    return dict(kind="tree", x=x, n0=n0, step=2, at=list(at), s=s)


def house(x=960, s=1.0, sign=None):
    return dict(kind="house", x=x, s=s, sign=sign)


def car(x=960, s=1.0, rust=False):
    return dict(kind="car", x=x, s=s, rust=rust)


def notes(n0=6, at=(), step=1, x=320, y=880, cols=6, s=1.3):
    return dict(kind="notes", x=x, y=y, n0=n0, step=step, at=list(at), cols=cols, s=s)


MEME = lambda: shot(kind="gary")
FACE = lambda cap=None: shot(kind="wolfface", caption=cap, cap=(1150, 120))
T = lambda t: shot(kind="title", title=t)
TXT = lambda t, size=200, color=(17, 17, 17), cap=None: shot(dict(kind="text", text=t, size=size, y=400, color=color), caption=cap)
TWO = lambda cap=None, fa=1.0, fb=1.0, ca=None, cb=None: shot(sheep(500, fa, c=ca, s=1.4), sheep(1350, fb, c=cb, s=1.4), caption=cap)
RICH = lambda cap=None: shot(sheep(c="shades"), caption=cap)

HOOK = seq([
    ("Sheep.", shot(wolf(960))),
    ("Meet two sheep.", TWO()),
    ("Same meadow. Same job. Same wool.", TWO("same everything")),
    ("Thirty years later, one of them is rich.", TXT("30 YEARS LATER", 170), ("rich", RICH("rich"))),
    ("The other one is Gary.", MEME()),
    ("Gary didn't work less.", shot(gary(), caption="worked hard")),
    ("Gary actually worked more.", shot(gary(), caption="worked harder")),
    ("So what happened?", FACE()),
    ("The rich sheep knew one thing that I know.", FACE("one thing")),
    ("Today, I'm going to tell you.", T("WHY THE RICH\nGET RICHER")),
    ("And at the end, I'll tell you the true story of a janitor who beat Wall Street.", shot(wolf(960)), ("janitor", shot(sheep(c="helmet"), caption="a janitor")), ("wall", TXT("WALL STREET", 200))),
    ("With a broom.", FACE("with a broom")),
], mood="tense")

TWO_WAYS = seq([
    ("There are only two ways to get wool.", T("TWO WAYS\nTO GET WOOL")),
    ("Way one. You grow it yourself.", TXT("1. WORK", 240), ("grow", shot(sheep(c="helmet"), caption="you grow it"))),
    ("Every day. With your own body.", shot(sheep(c="helmet"), caption="every day")),
    ("Stop working, the wool stops.", shot(sheep(f=0.3, mood="sad"), caption="stops")),
    ("Way two. You own something that grows wool for you.", TXT("2. OWN", 240), ("own", shot(tree(n=8), caption="grows by itself"))),
    ("A shop.", shot(dict(kind="stall", x=960, sign="GRASS SHOP"))),
    ("A house you rent out.", shot(house(sign="RENT"))),
    ("A piece of a big company.", shot(dict(kind="note", x=670, y=420, s=2.5, text="1 SHARE"))),
    ("These things grow wool while you sleep.", shot(tree(n=10), caption="while you sleep")),
    ("Gary has way one.", shot(gary(), caption="way one")),
    ("Rich sheep have way two.", RICH("way two")),
    ("That's it. That's the whole secret.", FACE("that's it")),
    ("But let me show you why it's so powerful.", shot(wolf(960))),
], mood="calm")

EATERS = seq([
    ("First, some things eat wool.", T("WOOL\nEATERS")),
    ("Gary gets a raise.", shot(gary(), caption="a raise!")),
    ("And Gary buys a brand new car.", shot(gary(500, s=1.3), car(1300, 0.9)), ("car", TXT("NEW CAR", 220))),
    ("The moment he drives it home, it's worth less.", shot(car(960, 1.1)), ("less", TXT("WORTH LESS", 200, RED))),
    ("Every year, a little less.", shot(car(960, 1.1, rust=True), caption="every year")),
    ("Plus insurance. Plus gas. Plus repairs.", TXT("INSURANCE", 200, RED), ("gas", TXT("GAS", 260, RED)), ("repairs", TXT("REPAIRS", 220, RED))),
    ("The car doesn't grow wool.", shot(car(960, 1.1, rust=True), caption="no wool")),
    ("It eats wool.", FACE("it eats wool")),
    ("New phone. Eats wool.", TXT("NEW PHONE", 200), ("eats", MEME())),
    ("Bigger apartment. Eats wool.", shot(house(sign="$$$")), ("eats", MEME())),
    ("Every raise Gary ever got, he fed to something that eats wool.", shot(gary(), caption="every raise")),
    ("It's called lifestyle creep.", T("LIFESTYLE\nCREEP")),
    ("More wool in. More wool out.", TXT("+ IN  - OUT", 220)),
    ("Gary stays exactly where he was.", shot(gary(), caption="still here")),
    ("Just with a nicer car.", shot(gary(500, s=1.3), car(1300, 0.9), caption="nice car though")),
], mood="calm")

GROWERS = seq([
    ("Now look at the rich sheep.", RICH()),
    ("She gets the same raise.", RICH("same raise")),
    ("And she plants it.", shot(sheep(500, c="shades", s=1.4), tree(1350, n=2, s=0.9), caption="she plants it")),
    ("In things that grow wool.", shot(grow(at=["grow", "wool"], n0=2))),
    ("That wool grows more wool.", shot(grow(at=["grows", "more"], n0=4))),
    ("And that wool grows even more wool.", shot(grow(at=["grows", "even", "more"], n0=6))),
    ("Wool on wool on wool.", shot(tree(n=12), caption="wool on wool")),
    ("It's called compounding.", T("COMPOUNDING")),
    ("Remember the debt snowball from the credit card video?", shot(dict(kind="snowball", x=960, y=560, r=220, text="DEBT"))),
    ("This is the same snowball.", FACE("same snowball")),
    ("Rolling the other way.", shot(dict(kind="snowball", x=960, y=560, r=260, text="YOUR WOOL"), caption="your way")),
], mood="hope")

NUMBERS = seq([
    ("Let's do the math.", T("THE MATH")),
    ("Say a sheep puts five hundred dollars a month into things that grow.", TXT("$500 / MONTH", 200)),
    ("And they grow about seven percent a year on average.", TXT("7% A YEAR", 220, GREEN, cap="on average, not guaranteed")),
    ("Start at twenty-five, stop at sixty-five.", TXT("25 TO 65", 260)),
    ("About one point three million dollars.", TXT("$1,300,000", 210, GREEN)),
    ("But the sheep only put in two hundred and forty thousand.", TXT("$240,000", 230, cap="put in")),
    ("The other million?", FACE()),
    ("Grew by itself.", shot(tree(n=12), caption="by itself")),
    ("Now start at thirty-five instead.", TXT("35 TO 65", 260)),
    ("About six hundred and ten thousand.", TXT("$610,000", 240)),
    ("Ten years late. Less than half the wool.", TXT("LESS THAN HALF", 180, RED)),
    ("The money didn't change.", FACE()),
    ("Time did.", T("TIME")),
], mood="hope")

EARLY = seq([
    ("And here's the craziest part.", shot(wolf(960))),
    ("Two sheep. Molly and Gary.", shot(sheep(500, c="scarf", s=1.4), gary(1350, s=1.4), caption="molly & gary")),
    ("Molly invests three hundred a month from twenty-five to thirty-five.", shot(sheep(c="scarf"), caption="molly"), ("three", TXT("$300 x 10 YEARS", 170))),
    ("Then she stops. Never adds another cent.", TXT("STOP", 300, RED)),
    ("Gary starts at thirty-five.", shot(gary(), caption="gary starts")),
    ("Three hundred a month, for thirty whole years.", TXT("$300 x 30 YEARS", 170)),
    ("Gary puts in three times more wool.", TXT("3x MORE", 260, cap="gary put in")),
    ("Who has more at sixty-five?", FACE("guess")),
    ("Molly.", shot(sheep(c="scarf"), caption="molly")),
    ("About three hundred and ninety-five thousand, against Gary's three hundred and sixty-five.", TXT("$395K", 280, GREEN, cap="molly"), ("gary's", TXT("$365K", 280, cap="gary"))),
    ("Ten years of planting beat thirty years of catching up.", T("EARLY\nBEATS MORE")),
    ("Because Molly's wool had more time to grow wool.", shot(tree(n=12), caption="time")),
    ("Gary's still confused.", MEME()),
], mood="hope")

BUFFETT = seq([
    ("Want proof from the real world?", FACE()),
    ("Warren Buffett.", TXT("WARREN BUFFETT", 190)),
    ("One of the richest investors in history.", RICH("one of the richest ever")),
    ("He bought his first stock at eleven years old.", TXT("AGE 11", 280)),
    ("He's a brilliant investor, sure.", FACE("brilliant")),
    ("But here's what people miss.", shot(wolf(960))),
    ("The vast majority of his fortune came after his sixty-fifth birthday.", TXT("AFTER 65", 260, GREEN, cap="most of his fortune")),
    ("His real secret isn't genius.", FACE("not genius")),
    ("It's time.", T("TIME")),
    ("He started early and never stopped.", shot(tree(n=12), caption="never stopped")),
], mood="hope")

WHO_OWNS = seq([
    ("So who owns the things that grow wool?", T("WHO OWNS\nTHE TREES?")),
    ("In America, the richest ten percent own about ninety percent of all stocks.", TXT("TOP 10%", 240), ("ninety", TXT("~90% OF STOCKS", 180, cap="usa"))),
    ("So when companies grow, guess whose wool grows?", shot(dict(kind="chart", stage="up"))),
    ("Theirs.", RICH("theirs")),
    ("And when prices go up, guess who feels it?", TXT("PRICES UP", 240, RED)),
    ("Gary.", MEME()),
    ("Remember my first video?", FACE()),
    ("Inflation melts wool sitting in a drawer.", shot(dict(kind="ice", x=960, y=560), caption="melting")),
    ("But things that grow wool usually grow faster than inflation over time.", shot(tree(n=10), caption="faster")),
    ("So the sheep with savings in a drawer gets poorer.", shot(sheep(f=0.4, mood="sad"), caption="poorer")),
    ("And the sheep with trees gets richer.", RICH("richer")),
    ("Without either of them doing anything.", FACE("nothing")),
], mood="tense")

INTEREST_FLOW = seq([
    ("But that's not the worst part.", shot(wolf(960))),
    ("Where do you think the interest on Gary's credit card goes?", shot(gary(500, s=1.3), dict(kind="card", x=1350, y=520, s=1.0))),
    ("To whoever owns the bank.", shot(dict(kind="stall", x=960, sign="WOLF BANK"))),
    ("Gary pays twenty-two percent.", TXT("22%", 360, RED, cap="gary pays")),
    ("Someone else collects it.", RICH("collects")),
    ("Debt is a pipe.", T("DEBT IS\nA PIPE")),
    ("It carries wool from the sheep who owe to the sheep who own.", shot(gary(400, s=1.2), notes(3, x=780, y=640, cols=3, s=1.0), sheep(1500, c="shades", s=1.2)),
     ("own", TXT("OWE  >  OWN", 220))),
    ("Every month.", TXT("EVERY MONTH", 200)),
    ("Automatically.", FACE("automatically")),
], mood="tense")

RULES_RICH = seq([
    ("And the rules?", FACE()),
    ("Written by people who read the rules.", T("THE RULES")),
    ("In the U.S., wool from a job can be taxed up to thirty-seven percent.", TXT("JOB: UP TO 37%", 170, RED)),
    ("Wool from investments held over a year?", shot(tree(n=10))),
    ("Usually zero, fifteen, or twenty percent.", TXT("0 / 15 / 20%", 220, GREEN)),
    ("Same wool. Different tax.", T("SAME WOOL\nDIFFERENT TAX")),
    ("And when rich sheep need cash, they often don't sell their trees.", RICH("need cash?")),
    ("They borrow against them.", shot(dict(kind="stall", x=960, sign="WOLF BANK"), caption="borrow")),
    ("The trees keep growing. No sale. No tax on a sale.", shot(tree(n=12), caption="keeps growing")),
    ("It's legal.", FACE("legal")),
    ("It's just in the part of the rulebook nobody reads.", FACE("nobody reads it")),
    ("I read it.", FACE("i read it")),
], mood="tense")

LOTTERY = seq([
    ("So what's Gary's plan to get rich?", shot(gary())),
    ("The lottery.", shot(dict(kind="note", x=670, y=420, s=2.5, text="LOTTO"), caption="the plan")),
    ("The odds of winning the Powerball jackpot are one in two hundred and ninety-two million.", TXT("1 IN 292,000,000", 150, RED)),
    ("You're far more likely to be struck by lightning.", FACE("lightning")),
    ("And you've probably heard that most lottery winners go broke.", TXT("70% GO BROKE?", 190)),
    ("That famous number?", FACE()),
    ("Nobody can find where it came from.", T("NO SOURCE")),
    ("But the lesson behind it is real.", shot(wolf(960))),
    ("A pile of wool is not the same as a tree.", shot(notes(12, x=300, y=880, cols=4, s=1.2), tree(1450, n=10, s=0.9))),
    ("A pile gets eaten.", MEME()),
    ("A tree feeds you forever.", shot(tree(n=12), caption="forever")),
], mood="calm")

JANITOR = seq([
    ("Now, I promised you a story.", shot(wolf(960))),
    ("Brattleboro, Vermont.", TXT("VERMONT", 240)),
    ("A man named Ronald Read.", shot(sheep(c="helmet"), caption="ronald read")),
    ("He pumped gas for about twenty-five years.", shot(car(960, 1.0), caption="pumped gas")),
    ("Later, he worked as a janitor.", shot(sheep(c="helmet"), caption="janitor")),
    ("He drove an old used car.", shot(car(960, 1.0, rust=True), caption="old car")),
    ("He cut his own firewood.", shot(sheep(c="helmet"), caption="firewood")),
    ("Nobody thought he had money.", shot(*herd(), caption="nobody knew")),
    ("He died in twenty fourteen, at ninety-two.", TXT("2014", 300)),
    ("And his town found out he was worth about eight million dollars.", TXT("$8,000,000", 230, GREEN)),
    ("Eight million.", T("EIGHT\nMILLION")),
    ("How?", FACE()),
    ("He bought shares in big, boring companies.", shot(notes(4, at=["bought", "shares", "boring", "companies"], step=2))),
    ("And then he held them. For decades.", shot(tree(n=12), caption="for decades")),
    ("No genius. No lottery. Just time.", TXT("NO GENIUS", 200), ("lottery", TXT("NO LOTTERY", 200)), ("time", T("JUST TIME"))),
    ("He left millions to his local library and his hospital.", shot(house(sign="LIBRARY"))),
    ("A janitor beat Wall Street.", T("JANITOR\nBEATS WALL ST")),
    ("And around the same time, plenty of Wall Street executives with huge salaries borrowed big, spent big, and lost almost everything.", RICH("huge salaries"),
     ("borrowed", shot(dict(kind="chart", stage="crash"))), ("lost", shot(sheep(f=0.0, mood="shock", c="shades"), caption="everything"))),
    ("High income doesn't make you rich.", TXT("INCOME IS NOT RICH", 200)),
    ("Owning does.", T("OWNING\nDOES")),
], mood="hope")

HOW = seq([
    ("So how does a sheep start growing trees?", T("HOW TO\nGROW TREES")),
    ("Rule one. Pay yourself first.", TXT("RULE 1", 220), ("first", TXT("PAY YOU FIRST", 180, GREEN))),
    ("The day your wool arrives, move a piece of it somewhere you can't easily spend it.", shot(notes(6, x=420, y=820, cols=3), tree(1450, n=2, s=0.8), caption="move it first")),
    ("Automatically. Before Gary-brain wakes up.", MEME()),
    ("Rule two. Own things that grow.", TXT("RULE 2", 220), ("own", shot(tree(n=10)))),
    ("For most sheep, the boring answer is a low-cost index fund.", T("INDEX\nFUND")),
    ("A tiny piece of hundreds of companies at once.", shot(notes(30, x=320, y=880, cols=6, s=1.3), caption="hundreds of companies")),
    ("Boring. Cheap. Works.", FACE("boring works")),
    ("Rule three. Watch the fees.", TXT("RULE 3", 220), ("fees", TXT("FEES", 280, RED))),
    ("A one percent yearly fee sounds tiny.", TXT("1%", 360)),
    ("Over forty years, it can eat about a quarter of your wool.", TXT("-$317,000", 230, RED, cap="40 years, our example")),
    ("Rule four. Don't feed your raises to wool eaters.", TXT("RULE 4", 220), ("eaters", shot(car(960, 1.0), caption="wool eater"))),
    ("Rule five. Start now. Even small.", TXT("RULE 5", 220), ("now", T("START\nNOW"))),
    ("Twenty dollars planted today beats a thousand planted never.", TXT("$20 > $0", 260, GREEN)),
    ("And when the market falls, and it will, don't pull your trees out of the ground.", shot(dict(kind="chart", stage="crash")), ("pull", shot(tree(n=6), caption="don't pull it"))),
    ("Not financial advice. I'm a wolf.", FACE("not financial advice")),
], mood="hope")

WHY_TELL = seq([
    ("And you're wondering, why would a wolf tell you this?", FACE("why?")),
    ("Simple.", FACE()),
    ("A sheep with trees doesn't need my credit card.", shot(dict(kind="card", x=960, y=540, s=1.6), caption="no thanks")),
    ("Doesn't need my loans.", shot(dict(kind="stall", x=960, sign="WOLF BANK"), caption="no thanks")),
    ("That's bad for business.", FACE("bad for business")),
    ("But you watched this far.", shot(wolf(960))),
    ("So I guess you earned it.", FACE("earned it")),
], mood="hope")

RECAP = seq([
    ("Cheat sheet.", T("CHEAT\nSHEET")),
    ("Working grows wool. Owning grows wool while you sleep.", TXT("WORK < OWN", 220)),
    ("Don't feed your raises to wool eaters.", shot(car(960, 1.0, rust=True), caption="wool eater")),
    ("Wool grows on wool.", shot(tree(n=12))),
    ("Time beats amount.", TXT("TIME > AMOUNT", 200, GREEN)),
    ("Watch the fees.", TXT("FEES", 280, RED)),
    ("Plant your first tree this week.", shot(tree(n=2), caption="this week")),
    ("Send this to the Gary in your life.", shot(gary(), caption="send to your gary")),
], mood="hope")

GARY_END = seq([
    ("And Gary?", shot(gary())),
    ("Gary finally planted a tree.", shot(gary(500, s=1.4), tree(1350, n=0, s=0.9), caption="a tree!")),
    ("He's very proud.", MEME()),
    ("He planted his last piece of wool.", shot(gary(500, s=1.4), tree(1350, n=1, s=0.9), caption="his last piece")),
    ("Hello, sheep.", FACE()),
    ("If you don't want to end up bald like Gary… subscribe.", shot(kind="outro")),
    ("Gary's retirement plan is a lottery ticket.", shot(dict(kind="note", x=1420, y=700, s=0.9, text="LOTTO"), kind="outro", caption="gary's retirement plan: a lottery ticket.", cap=(560, 200))),
], mood="hope", pause=1.6)

LOOKS = seq([
    ("Here's something sheep get wrong all the time.", FACE()),
    ("Who looks rich?", T("WHO LOOKS\nRICH?")),
    ("The sheep with the shiny car and the giant phone.", shot(sheep(500, c="shades", s=1.3), car(1350, 0.8)), ("phone", TXT("SHINY", 240))),
    ("But a lot of that shine is borrowed.", shot(dict(kind="card", x=960, y=540, s=1.6), caption="borrowed")),
    ("In the nineties, two researchers studied thousands of American millionaires.", TXT("THE STUDY", 220), ("thousands", shot(*herd(), caption="thousands of millionaires"))),
    ("They wrote a famous book called The Millionaire Next Door.", T("THE MILLIONAIRE\nNEXT DOOR")),
    ("What did they find?", FACE()),
    ("Many millionaires lived in ordinary houses.", shot(house(), caption="ordinary house")),
    ("Drove ordinary cars.", shot(car(960, 1.0), caption="ordinary car")),
    ("And spent much less than they earned.", TXT("SPEND < EARN", 220, GREEN)),
    ("Rich sheep often look like Gary.", shot(sheep(500, s=1.4), gary(1350, s=1.4), caption="spot the rich one")),
    ("Gary looks like a rich sheep. On credit.", MEME()),
], mood="calm")

RENT = seq([
    ("And debt isn't the only pipe.", shot(wolf(960))),
    ("Every month, Gary pays rent.", shot(gary(500, s=1.3), house(1350, 0.8, sign="RENT"), caption="rent")),
    ("Where does it go?", FACE()),
    ("To the sheep who owns the house.", RICH("owns the house")),
    ("Gary's wool pays off her house.", shot(house(sign="PAID")), ("pays", shot(gary(), caption="paying it off"))),
    ("And in thirty years, she owns a house, and Gary owns thirty years of receipts.", TXT("30 YEARS", 240), ("receipts", shot(notes(30, x=320, y=880, cols=6, s=1.3), caption="receipts"))),
    ("Renting isn't always bad. Sometimes it's the smart move.", FACE("not always bad")),
    ("But only if the money you save goes into trees.", shot(tree(n=10), caption="into trees")),
    ("Not into a bigger car.", shot(car(960, 1.1), caption="not this")),
], mood="tense")

BROKE = seq([
    ("But wolf, I don't have any wool left over to plant.", shot(gary(), caption="i have nothing")),
    ("Fair.", FACE("fair")),
    ("Then start in this order.", T("THE ORDER")),
    ("One. A small cushion. A few hundred, then one month of bills, in a separate account.", TXT("1. CUSHION", 220), ("separate", shot(notes(4, x=600, y=760, cols=4, s=1.3), caption="for emergencies"))),
    ("So one broken tooth doesn't go on a credit card.", shot(dict(kind="card", x=960, y=540, s=1.6), caption="not here")),
    ("Two. Kill the high-interest debt.", TXT("2. KILL DEBT", 210, RED)),
    ("Paying off a card at twenty-two percent is like a guaranteed twenty-two percent return.", TXT("22% GUARANTEED", 180, GREEN)),
    ("No investment I know promises you that.", FACE("not even me")),
    ("Three. Then plant trees. Every month.", TXT("3. PLANT", 230, GREEN), ("trees", shot(tree(n=6)))),
    ("Small is fine.", shot(tree(n=1), caption="small is fine")),
    ("Every rich tree was a tiny seed once.", FACE("tiny seed")),
], mood="hope")

BLOCKS = [HOOK, TWO_WAYS, EATERS, LOOKS, GROWERS, NUMBERS, EARLY, BUFFETT, WHO_OWNS, INTEREST_FLOW, RENT, RULES_RICH, LOTTERY, JANITOR, BROKE, HOW, WHY_TELL, RECAP, GARY_END]
