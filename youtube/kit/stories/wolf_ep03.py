"""The Sheep Standard — EP03: Credit Cards: Selling Wool You Don't Have Yet. Монтаж по плагину doodle-explainer-edit.
Выход к Black Friday (27.11.2026). Голос Eric. Факты (в описание, источники в ../sheep-standard/ep03/PACKAGE.md):
- Средняя ставка по картам в США ~21–23% годовых (Federal Reserve G.19, счета с начисленными процентами, 2025).
- Долг по кредиткам в США > $1.2 трлн (New York Fed, Household Debt and Credit Report, 2025).
- Пример минимального платежа (наш расчёт): $3 000 под 22%, минимум = 1% долга + проценты (не меньше $25) → 15 лет, ~$4 400 процентов.
- $1 000 под 22% с ежедневной капитализацией без платежей: ~$1 250 через год, ~$3 000 через 5 лет (расчёт, без штрафов).
- Сентябрь 1958: Bank of America разослала ~60 000 карт BankAmericard жителям Фресно (Калифорния) без запроса.
- 1970: в США запрещено рассылать кредитные карты без запроса (Unsolicited Credit Card Act of 1970).
- Prelec & Simester (2001), MIT, «Always Leave Home Without It»: с картой люди предлагали за билеты заметно больше, в одном тесте примерно вдвое.
- Комиссия магазина за оплату картой (interchange) в США обычно ~2–3%.
- Льготный период: если платить весь баланс выписки до срока, проценты на покупки не начисляются.
- «Deadbeats» — жаргон индустрии для клиентов, которые платят полностью и не платят процентов.
"""
from doodle import seq, shot

STORY = dict(name="wolf-ep03", accent=(214, 40, 40), voice="eric", speed=1.03, tempo=0.93, end_hold=1.5)
GREEN, RED = (40, 160, 70), (214, 40, 40)


def wolf(x=960, pose="stand", s=1.4, **k):
    return dict(kind="wolf", x=x, pose=pose, s=s, **k)


def sheep(x=860, f=1.0, mood="calm", c=None, s=1.8, **k):
    return dict(kind="sheep", x=x, f=f, mood=mood, c=c, s=s, **k)


def gary(x=860, s=1.8, **k):
    return dict(kind="gary", x=x, s=s, **k)


def herd(f=1.0, mood="calm", s=0.9):
    return [sheep(260, f, mood, s=s), sheep(760, f, mood, s=s), sheep(1260, f, mood, s=s)]


def card(x=960, y=540, s=1.6, text="WOLF CARD", **k):
    return dict(kind="card", x=x, y=y, s=s, text=text, **k)


def bill(*lines, x=650, y=160, s=1.0):
    return dict(kind="bill", x=x, y=y, s=s, lines=[(t[1:], True) if t.startswith("!") else (t, False) for t in lines])


def ball(r=200, text="DEBT", x=960, y=560):
    return dict(kind="snowball", x=x, y=y, r=r, text=text)


def bag(x=960, text="SALE", s=1.4):
    return dict(kind="bag", x=x, y=620, s=s, text=text)


def chat(*msgs, title="Wolf Bank", x=780):
    return dict(kind="phone", x=x, y=200, s=1.0, title=title, msgs=list(msgs))


MEME = lambda: shot(kind="gary")
FACE = lambda cap=None: shot(kind="wolfface", caption=cap, cap=(1150, 120))
T = lambda t: shot(kind="title", title=t)
TXT = lambda t, size=200, color=(17, 17, 17), cap=None: shot(dict(kind="text", text=t, size=size, y=400, color=color), caption=cap)
CARD = lambda cap=None, **k: shot(card(**k), caption=cap)
GARY_CARD = lambda cap=None: shot(gary(600, s=1.6), card(1350, 520, 1.1), caption=cap)
STMT = ("Balance: $3,000", "!Minimum: $85", "Rate: 22%")

HOOK = seq([
    ("Sheep.", shot(wolf(960, "present"))),
    ("I have a gift for you.", shot(wolf(720, "present"), card(1400, 480, 1.0), caption="a gift")),
    ("A little plastic card.", CARD()),
    ("Gold color.", CARD("gold. fancy.")),
    ("Your name on it.", CARD(text="YOUR NAME")),
    ("Buy anything you want. Today.", shot(bag(700), bag(1250, "NEW TV")), ("today", TXT("TODAY", 260, RED))),
    ("Pay later.", TXT("PAY LATER", 220, GREEN)),
    ("Doesn't that feel nice?", FACE("nice, right?")),
    ("Here's what I'm not telling you.", FACE()),
    ("Every time you swipe this card, you're selling me wool that hasn't even grown yet.", CARD(), ("selling", shot(sheep(f=0.5, mood="sad"), caption="wool that hasn't grown yet"))),
    ("And I buy it very, very cheap.", FACE("very cheap")),
    ("Today, I'll show you exactly how a credit card shears you.", T("CREDIT\nCARDS")),
    ("Gary already knows.", MEME()),
    ("And at the end, I'll show you one simple habit that makes my card completely free for you.", shot(wolf(960)), ("free", TXT("FREE", 300, GREEN, cap="for you"))),
    ("Wolves hate this habit.", FACE("we hate it")),
], mood="tense")

WHAT = seq([
    ("First, what is a credit card?", T("WHAT IS A\nCREDIT CARD?")),
    ("A normal card spends wool you already have.", shot(sheep(c="shades"), caption="your wool")),
    ("A credit card spends wool you don't have.", shot(sheep(f=0.3, mood="sad"), caption="not your wool")),
    ("Whose wool is it?", FACE()),
    ("Mine.", FACE("mine")),
    ("I lend it to you.", shot(wolf(720, "present"), dict(kind="notes", x=1200, y=780, n0=6, cols=3, s=1.0), caption="a loan")),
    ("Every swipe is a tiny loan.", CARD("every swipe = a loan")),
    ("And every loan has a price.", TXT("THE PRICE?", 220, RED)),
    ("Interest.", T("INTEREST")),
], mood="calm")

GARY_TV = seq([
    ("Let me show you on my favourite customer.", shot(wolf(960, "present"))),
    ("Gary.", MEME()),
    ("It's Black Friday.", T("BLACK\nFRIDAY")),
    ("Gary sees a giant TV.", shot(gary(500, s=1.4), bag(1350, "NEW TV")), ("giant", TXT("BIG TV", 260))),
    ("Three thousand dollars.", TXT("$3,000", 300)),
    ("Gary doesn't have three thousand dollars.", shot(gary(), caption="has $0")),
    ("But Gary has my card.", GARY_CARD("but...")),
    ("Swipe.", CARD("swipe")),
    ("The TV is his.", shot(gary(500, s=1.4), bag(1350, "NEW TV"), caption="happy gary")),
    ("Gary is happy.", MEME()),
    ("I'm happier.", FACE("happier")),
], mood="calm")

STATEMENT = seq([
    ("A month later, Gary gets a letter.", shot(gary(), caption="a letter")),
    ("The statement.", shot(bill(*STMT))),
    ("Balance: three thousand dollars.", shot(bill(STMT[0])), ("dollars", TXT("$3,000", 260))),
    ("And then, in a friendly little box, a much nicer number.", shot(bill(*STMT[:2])), ("nicer", FACE("so friendly"))),
    ("Minimum payment: about eighty-five dollars.", TXT("$85", 340, GREEN, cap="minimum payment")),
    ("Gary thinks: eighty-five? I can do that!", shot(gary(), caption="i can do that!")),
    ("And this is the number I really hope you never read.", FACE("don't read it")),
    ("Rate: twenty-two percent a year.", shot(bill(*STMT)), ("twenty-two", TXT("22%", 360, RED, cap="per year"))),
    ("That's about the average in the U.S. right now.", TXT("AVERAGE", 220, cap="usa, ~21-23%")),
], mood="tense")

MINIMUM = seq([
    ("So Gary pays the minimum.", shot(gary(), caption="pays the minimum")),
    ("Every month.", TXT("EVERY MONTH", 200)),
    ("Like a responsible sheep.", MEME()),
    ("Do you know how long it takes to pay off that TV?", FACE()),
    ("Guess.", FACE("guess")),
    ("One year?", TXT("1 YEAR?", 240)),
    ("Three?", TXT("3 YEARS?", 240)),
    ("Fifteen years.", TXT("15 YEARS", 300, RED)),
    ("Fifteen.", T("FIFTEEN\nYEARS")),
    ("And Gary pays about four thousand four hundred dollars just in interest.", TXT("$4,400", 300, RED, cap="just interest")),
    ("A three thousand dollar TV costs him over seven thousand.", TXT("$3,000", 260), ("seven", TXT("$7,400", 300, RED, cap="real price"))),
    ("The TV will be dead in eight years.", shot(bag(960, "OLD TV"), caption="rip tv")),
    ("Gary will still be paying for it.", shot(gary(), caption="still paying")),
    ("For a dead TV.", MEME()),
], mood="tense")

WHY_MIN = seq([
    ("Why is the minimum so small?", T("WHY SO\nSMALL?")),
    ("Is it because I'm kind?", FACE("kind?")),
    ("No.", FACE("no")),
    ("The minimum is designed so you pay mostly interest.", shot(bill(*STMT[:2])), ("interest", TXT("INTEREST", 220, RED))),
    ("Most of Gary's eighty-five dollars doesn't touch the TV.", TXT("$85", 300), ("touch", shot(bag(960, "NEW TV"), caption="barely touched"))),
    ("It goes straight to me.", shot(wolf(960), dict(kind="notes", x=1200, y=780, n0=2, step=2, at=["straight", "me"], cols=3, s=1.0))),
    ("The debt shrinks like a glacier.", shot(ball(220), caption="slowly...")),
    ("Very slowly.", FACE("very slowly")),
    ("In fact, it's printed on the statement.", shot(bill(*STMT))),
    ("By law, U.S. statements must show how long it takes if you only pay the minimum.", T("IT'S ON THE\nSTATEMENT"), ("only", TXT("15 YEARS", 260, RED, cap="it's right there"))),
    ("Nobody reads it.", shot(*herd(), caption="nobody")),
    ("Wolves love that.", FACE("love it")),
], mood="tense")

SNOWBALL = seq([
    ("But that's not the worst part.", shot(wolf(960))),
    ("Interest on a card grows on itself.", T("INTEREST ON\nINTEREST")),
    ("Most cards calculate it every single day.", TXT("EVERY DAY", 220, RED)),
    ("Today you owe interest.", shot(ball(120))),
    ("Tomorrow, you owe interest on that interest.", shot(ball(170))),
    ("It's a snowball.", shot(ball(230))),
    ("Made of your wool.", shot(ball(260, "YOUR WOOL"))),
    ("Leave one thousand dollars on a card at twenty-two percent and don't pay.", TXT("$1,000", 280), ("twenty-two", TXT("22%", 300, RED))),
    ("After one year: about twelve hundred and fifty.", TXT("$1,250", 260, cap="1 year")),
    ("After five years: about three thousand.", TXT("$3,000", 300, RED, cap="5 years")),
    ("Before late fees.", FACE("before fees")),
    ("You didn't buy anything new.", shot(gary(), caption="bought nothing")),
    ("The snowball just kept rolling.", shot(ball(300))),
    ("Downhill.", MEME()),
    ("On Gary.", shot(gary(500, s=1.3), ball(180, x=1350), caption="on gary")),
], mood="tense")

BOTH_SIDES = seq([
    ("Now here's my favourite part.", FACE("favourite")),
    ("I make money even when you don't pay me a single cent of interest.", T("I WIN\nANYWAY")),
    ("How?", FACE()),
    ("Every time you swipe, the shop pays me too.", shot(dict(kind="stall", x=960, sign="GRASS SHOP"))),
    ("Usually two or three percent.", TXT("2-3%", 320, RED, cap="from the shop")),
    ("So the shop raises its prices a little.", shot(dict(kind="stall", x=960, sign="GRASS SHOP", price="+3%"))),
    ("For everyone.", shot(*herd(), caption="everyone pays")),
    ("Even the sheep paying with cash.", shot(sheep(c="scarf"), caption="even grandma")),
    ("And those cashback rewards I give you?", TXT("CASHBACK!", 220, GREEN)),
    ("That's your own wool.", shot(sheep(f=0.6), caption="your own wool")),
    ("Returned with a little bow on it.", FACE("you're welcome")),
], mood="calm")

BRAIN = seq([
    ("And cards have one more trick. They change your brain.", T("YOUR BRAIN\nON CARDS")),
    ("Paying cash hurts.", TXT("CASH = OUCH", 200)),
    ("You see the wool leave your paws.", shot(sheep(f=0.7, mood="sad"), dict(kind="notes", x=1250, y=780, n0=3, cols=3, s=1.0), caption="ouch")),
    ("A card doesn't hurt.", TXT("CARD = NOTHING", 180)),
    ("Tap. Beep. Done.", CARD("beep")),
    ("Researchers at MIT tested this.", TXT("MIT", 320, cap="real study")),
    ("They auctioned sports tickets.", shot(*herd(), caption="an auction")),
    ("Some people could only pay cash, others could pay by card.", shot(sheep(500, c="scarf", s=1.3), sheep(1300, c="shades", s=1.3)), ("others", CARD("card"))),
    ("The card group offered far more money.", TXT("MORE $$$", 240, RED)),
    ("In one test, roughly double.", TXT("2x", 380, RED, cap="roughly double")),
    ("Same tickets.", FACE()),
    ("Same sheep.", shot(*herd())),
    ("Just plastic.", CARD("just plastic")),
], mood="calm")

FRESNO = seq([
    ("And you didn't even ask for this card.", FACE()),
    ("I sent it to you.", shot(wolf(960, "present"))),
    ("That idea has a history.", T("TRUE\nSTORY")),
    ("Fresno, California, nineteen fifty-eight.", TXT("FRESNO, 1958", 200)),
    ("Bank of America mails about sixty thousand credit cards to people who never asked for one.", TXT("60,000", 300), ("never", shot(*herd(mood="shock"), caption="never asked"))),
    ("Just shows up in the mailbox.", CARD("surprise!")),
    ("People start spending.", shot(bag(600), bag(1300, "STUFF"))),
    ("Lots of people don't pay it back.", shot(sheep(f=0.3, mood="sad"), caption="oops")),
    ("Fraud everywhere.", TXT("FRAUD", 300, RED)),
    ("The bank loses millions on the experiment.", TXT("-$$$", 300, RED, cap="millions lost")),
    ("And then?", FACE()),
    ("They did it in more cities.", shot(*herd(), caption="more cities")),
    ("Because the plan worked.", FACE("it worked")),
    ("Millions of sheep got used to spending wool they didn't have.", shot(sheep(260, 0.4, "sad", s=0.9), sheep(760, 0.4, "sad", s=0.9), gary(1260, s=0.9))),
    ("By nineteen seventy, America banned mailing out cards nobody asked for.", TXT("1970", 300), ("banned", T("BANNED"))),
    ("Too late.", FACE("too late")),
    ("The habit stayed.", MEME()),
], mood="tense")

TODAY = seq([
    ("And today?", shot(wolf(960))),
    ("Americans owe more than one point two trillion dollars on credit cards.", TXT("$1.2 TRILLION", 190, RED), ("cards", CARD("in plastic"))),
    ("Trillion. With a T.", T("TRILLION\nWITH A T")),
    ("That's a lot of TVs.", shot(bag(500, "TV"), bag(960, "TV"), bag(1420, "TV"))),
    ("And a lot of Garys.", shot(gary(260, s=0.9), gary(760, s=0.9), gary(1260, s=0.9))),
    ("This Black Friday, you'll see a new costume, too.", T("NEW\nCOSTUME")),
    ("Buy now, pay later.", TXT("BUY NOW, PAY LATER", 130, RED)),
    ("Four small easy payments.", shot(dict(kind="notes", x=520, y=760, n0=1, step=1, at=["small", "easy", "payments"], cols=4, s=1.3))),
    ("Small bites feel safe.", FACE("small bites")),
    ("But miss one, and the fees show up.", TXT("LATE FEE", 220, RED)),
    ("And five little loans in five different apps are very easy to forget.", shot(chat("payment 2 of 4", "payment 1 of 4", "payment 3 of 4", "LATE", title="Pay Later"))),
    ("Same wolf.", FACE()),
    ("Smaller bites.", MEME()),
], mood="tense")

STORE = seq([
    ("Oh, and one more Black Friday classic.", shot(dict(kind="stall", x=960, sign="MEGA STORE"))),
    ("At the checkout, the cashier smiles.", shot(sheep(c="hat"), caption="hi!")),
    ("Want ten percent off today? Just open our store card.", TXT("10% OFF", 280, GREEN), ("store", CARD("store card", text="MEGA CARD"))),
    ("Ten percent off a TV.", TXT("-10%", 300, GREEN)),
    ("Then twenty-five percent interest or more, on a card you'll forget you have.", TXT("25%+", 320, RED, cap="interest")),
    ("Store cards often have some of the highest rates out there.", FACE("highest")),
    ("Ten percent off, to start paying twenty-five percent a year.", T("-10%\n+25%")),
    ("Great deal.", FACE("great deal")),
    ("For me.", FACE("for me")),
], mood="calm")

CONFESS = seq([
    ("Now, you're probably thinking, so credit cards are evil.", FACE("evil?")),
    ("No.", FACE("no")),
    ("A credit card is a tool.", CARD("a tool")),
    ("Like my shears.", shot(wolf(960, "shears"))),
    ("Shears are great for cutting paper.", shot(wolf(960, "shears"), caption="paper")),
    ("Or for cutting sheep.", MEME()),
    ("It depends who's holding them.", FACE("who holds them?")),
    ("So let me give you the habit I promised.", shot(wolf(960))),
    ("The one wolves hate.", FACE("we hate it")),
], mood="hope")

HABIT = seq([
    ("Here it is.", T("THE HABIT")),
    ("Pay the full statement balance. Every month. Before the due date.", shot(bill(*STMT)), ("every", TXT("FULL. EVERY MONTH.", 150, GREEN))),
    ("Not the minimum.", TXT("NOT $85", 240, RED)),
    ("The whole thing.", TXT("$3,000", 300, GREEN, cap="the whole thing")),
    ("If you do that, most cards charge you zero interest on your purchases.", TXT("0%", 400, GREEN, cap="zero interest")),
    ("It's called the grace period.", T("GRACE\nPERIOD")),
    ("You borrow my wool for a month, for free.", shot(sheep(c="shades"), caption="free wool")),
    ("You get the points.", CARD("points")),
    ("You build your credit score.", TXT("CREDIT SCORE", 170, GREEN)),
    ("And I get nothing.", FACE("nothing")),
    ("You know what bankers call people like that?", FACE()),
    ("Deadbeats.", T("DEADBEATS")),
    ("That's real industry slang.", TXT("REAL SLANG", 200, cap="look it up")),
    ("For people who pay on time.", FACE("rude, right?")),
    ("Be a deadbeat, sheep.", shot(sheep(c="shades"), caption="be a deadbeat")),
], mood="hope")

RULES = seq([
    ("Three more rules, and you're safe.", T("3 RULES")),
    ("Rule one. If you can't pay cash for it today, you can't afford it on a card.", TXT("RULE 1", 220), ("afford", TXT("NO CASH = NO BUY", 150, RED))),
    ("Use your card like a debit card.", CARD("like debit")),
    ("Rule two. Turn on autopay for the full balance.", TXT("RULE 2", 220), ("autopay", TXT("AUTOPAY: FULL", 170, GREEN))),
    ("Your memory is not a financial plan.", MEME()),
    ("Rule three. If you're already in debt, pay more than the minimum.", TXT("RULE 3", 220), ("more", TXT("MORE THAN $85", 170, GREEN))),
    ("Every extra dollar goes straight at the snowball.", shot(ball(220), caption="extra dollars")),
    ("Attack the card with the highest rate first.", TXT("HIGHEST % FIRST", 160, RED)),
    ("And call the bank. Ask for a lower rate.", shot(sheep(c="shades"), caption="ring ring")),
    ("Sometimes they say yes.", FACE("sometimes")),
    ("Because a sheep who pays slowly is better than a sheep who leaves.", shot(sheep(f=0.5), caption="better than leaving")),
    ("And if you can't stop swiping?", FACE()),
    ("Cut it.", CARD("snip", cut=True)),
    ("Dramatic. Works.", FACE("works")),
    ("Not financial advice. I'm a wolf.", FACE("not financial advice")),
], mood="hope")

RECAP = seq([
    ("Okay. Cheat sheet.", T("CHEAT\nSHEET")),
    ("A card is a loan.", CARD("a loan")),
    ("The minimum is a trap.", TXT("$85 = TRAP", 220, RED)),
    ("Interest grows on interest.", shot(ball(220))),
    ("Free gifts are paid with your wool.", TXT("CASHBACK = YOUR WOOL", 120)),
    ("Pay in full, every month.", TXT("PAY IN FULL", 220, GREEN)),
    ("Be a deadbeat.", T("DEADBEAT")),
    ("Screenshot this, and send it to the Gary in your life before Friday.", shot(gary(), caption="send to your gary")),
], mood="hope")

GARY_END = seq([
    ("And Gary?", shot(gary())),
    ("Gary's still paying for the TV.", shot(gary(500, s=1.4), bag(1350, "OLD TV"), caption="year 3 of 15")),
    ("But this Black Friday, he finally did something about it.", T("BLACK\nFRIDAY")),
    ("He bought scissors.", GARY_CARD("scissors?")),
    ("On the card.", CARD("on the card")),
    ("Hello, sheep.", FACE()),
    ("If you don't want to end up bald like Gary… subscribe.", shot(kind="outro")),
    ("Gary paid the minimum.", shot(card(1500, 760, 0.6), kind="outro", caption="gary paid the minimum.", cap=(820, 200))),
], mood="hope", pause=1.6)

GARY_YEAR = seq([
    ("And it never stops at one TV.", shot(gary(500, s=1.4), bag(1350, "NEW TV"))),
    ("Let's watch Gary's year.", T("GARY'S\nYEAR")),
    ("December. Presents for the whole herd.", TXT("DECEMBER", 220), ("presents", shot(bag(500, "GIFTS"), bag(1000, "GIFTS"), bag(1500, "GIFTS")))),
    ("On the card.", CARD("on the card")),
    ("March. The car needs new tires.", TXT("MARCH", 240), ("tires", TXT("TIRES $600", 200))),
    ("On the card.", CARD("on the card")),
    ("July. A little vacation. Gary deserves it.", TXT("JULY", 240), ("vacation", shot(gary(), caption="he deserves it"))),
    ("On the card.", CARD("on the card")),
    ("Now the minimum isn't eighty-five anymore.", TXT("$85", 260), ("anymore", TXT("$310", 300, RED, cap="new minimum"))),
    ("So Gary gets a second card.", shot(gary(600, s=1.6), card(1250, 420, 0.9), card(1450, 640, 0.9, text="CARD #2"))),
    ("To pay the first card.", FACE("smart, gary")),
    ("Now Gary has two wolves.", shot(wolf(500, s=1.1), wolf(1420, s=1.1), caption="two wolves")),
    ("Neither of them is me. Just kidding. Both of them are me.", FACE("both me")),
], mood="tense")

PENALTY = seq([
    ("And if Gary is late, even once?", FACE()),
    ("A late fee.", TXT("LATE FEE", 240, RED)),
    ("And on many cards, a penalty rate.", T("PENALTY\nRATE")),
    ("The rate can jump to around thirty percent.", TXT("22%", 280), ("jump", TXT("~30%", 340, RED, cap="penalty rate"))),
    ("And it can stay there for a long time.", FACE("a long time")),
    ("One forgotten payment.", shot(chat("PAYMENT DUE", "PAYMENT LATE", "NEW RATE: 29.99%", title="Wolf Bank"))),
    ("Months of extra interest.", MEME()),
], mood="tense")

ZERO = seq([
    ("Now, maybe you've seen this one.", shot(wolf(960, "present"))),
    ("Zero percent for twelve months!", TXT("0% FOR 12 MONTHS", 140, GREEN)),
    ("Sounds amazing. And it can be useful.", FACE("can be useful")),
    ("If you pay everything off before the year ends.", TXT("PAY IT ALL", 200, GREEN, cap="before the year ends")),
    ("But some store deals have a trap called deferred interest.", T("DEFERRED\nINTEREST")),
    ("Miss the deadline by one dollar, and they can charge you interest for the whole year.", TXT("$1 LEFT", 240), ("whole", TXT("ALL 12 MONTHS", 170, RED, cap="of interest"))),
    ("Backwards.", FACE("backwards")),
    ("From day one.", TXT("DAY 1", 300, RED)),
    ("Read the small print, sheep.", shot(bill("0% for 12 months*", "!*if paid in full", y=260), caption="small print")),
    ("That's where I live.", FACE("i live here")),
], mood="tense")

SCORE = seq([
    ("Wait, what's a credit score?", T("CREDIT\nSCORE")),
    ("It's a number that tells banks how much they can trust you.", TXT("750", 340, GREEN, cap="your score")),
    ("High score: cheaper loans for a car or a house.", TXT("HIGH = CHEAP", 200, GREEN), ("house", shot(sheep(c="shades"), caption="cheap loans"))),
    ("Low score: everything costs more wool.", TXT("LOW = EXPENSIVE", 170, RED)),
    ("And the best way to build it is boring.", FACE("boring")),
    ("Pay on time. Don't use most of your limit.", TXT("ON TIME", 220, GREEN), ("limit", TXT("USE LESS THAN 30%", 140, cap="a common rule"))),
    ("Boring sheep have the cheapest loans.", shot(sheep(c="scarf"), caption="boring = rich")),
], mood="hope")

DINERS = seq([
    ("And where did all this start?", FACE()),
    ("With dinner.", T("IT STARTED\nWITH DINNER")),
    ("New York, nineteen fifty.", TXT("NEW YORK, 1950", 190)),
    ("The story goes, a businessman finishes a fancy dinner and realizes he forgot his wallet.", shot(sheep(c="shades"), caption="fancy dinner"), ("forgot", shot(sheep(f=0.8, mood="shock", c="shades"), caption="no wallet"))),
    ("So he invents a card for paying at restaurants.", CARD("for dinners", text="DINER CARD")),
    ("That became Diners Club, one of the first modern charge cards.", TXT("DINERS CLUB", 200, cap="1950")),
    ("Back then, you had to pay the whole bill every month.", TXT("PAY IT ALL", 200, GREEN)),
    ("No minimum. No snowball.", FACE("no snowball")),
    ("Then banks noticed something.", shot(wolf(960))),
    ("Sheep who don't pay it all are worth much more.", shot(sheep(f=0.4, mood="sad"), caption="worth more")),
    ("And the minimum payment was born.", T("THE MINIMUM\nIS BORN")),
], mood="calm")

TARGETS = seq([
    ("So who do I send my cards to first?", FACE()),
    ("Young sheep.", shot(sheep(s=1.4), caption="young")),
    ("First job. First apartment. First paycheck.", TXT("FIRST JOB", 220), ("apartment", TXT("FIRST HOME", 220)), ("paycheck", TXT("FIRST PAY", 220, GREEN))),
    ("No history with money, and big dreams.", shot(sheep(c="shades"), caption="big dreams")),
    ("A sheep who learns to swipe at twenty can pay me interest for forty years.", TXT("40 YEARS", 280, RED, cap="of interest")),
    ("That's not a customer.", FACE()),
    ("That's a pension.", T("MY\nPENSION")),
    ("Mine.", FACE("mine")),
], mood="tense")

BLOCKS = [HOOK, WHAT, GARY_TV, STATEMENT, MINIMUM, WHY_MIN, SNOWBALL, GARY_YEAR, PENALTY, BOTH_SIDES, BRAIN, DINERS, FRESNO, TARGETS, TODAY, ZERO, STORE, CONFESS, HABIT, SCORE, RULES, RECAP, GARY_END]
