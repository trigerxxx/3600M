# Генератор макетов интерфейса для Figma (SVG 1280x720, телефон горизонтально)
import os
OUT='/home/user/3600m/art/ui'
F='Inter, Arial, sans-serif'
H='Georgia, serif'
C=dict(night='#0b1220',blue='#22355c',ice='#9fc4ee',warm='#ffb866',wood='#8a5a3a',danger='#d92b20',paper='#efe6cf',ink='#2b3a5c')

def svg(name, body, w=1280, h=720):
    s=f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
<defs>
<radialGradient id="fire" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#ffb866" stop-opacity=".8"/><stop offset=".6" stop-color="#c8662a" stop-opacity=".22"/><stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient>
<radialGradient id="lamp" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#ffd27a" stop-opacity=".75"/><stop offset="1" stop-color="#ffd27a" stop-opacity="0"/></radialGradient>
<radialGradient id="vig" cx="50%" cy="50%" r="75%"><stop offset=".55" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".75"/></radialGradient>
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9fb8d6"/><stop offset="1" stop-color="#dfe8f3"/></linearGradient>
</defs>
{body}
</svg>'''
    open(os.path.join(OUT,name),'w').write(s)

def room(night=True):
    wall='#2a1f18' if night else '#5c4636'
    floor='#3a2a1e' if night else '#7a5c44'
    side='#1e1611' if night else '#4d3a2c'
    return f'''<g id="room">
<rect width="1280" height="720" fill="#0a0e18"/>
<polygon points="0,0 1280,0 1040,110 240,110" fill="{side}"/>
<polygon points="240,110 1040,110 1040,520 240,520" fill="{wall}"/>
<polygon points="0,0 240,110 240,520 0,720" fill="{side}"/>
<polygon points="1280,0 1040,110 1040,520 1280,720" fill="{side}"/>
<polygon points="0,720 240,520 1040,520 1280,720" fill="{floor}"/>
<g stroke="#00000033" stroke-width="3"><line x1="240" y1="220" x2="1040" y2="220"/><line x1="240" y1="320" x2="1040" y2="320"/><line x1="240" y1="420" x2="1040" y2="420"/></g>
<circle cx="330" cy="500" r="{340 if night else 260}" fill="url(#fire)"/>
<rect x="270" y="380" width="120" height="130" rx="10" fill="#15110f"/><rect x="296" y="425" width="68" height="50" rx="5" fill="#ff9a3a"/><rect x="318" y="110" width="26" height="270" fill="#15110f"/>
<rect x="225" y="180" width="90" height="120" fill="#7a2d22"/><path d="M238 240 q32 -38 64 0 q-32 38 -64 0" fill="none" stroke="#e9c37a" stroke-width="4"/>
<rect x="560" y="175" width="165" height="335" fill="#44536f" stroke="#9fc4ee" stroke-width="5"/>
<circle cx="642" cy="285" r="11" fill="#05080f" stroke="#c9d8ee" stroke-width="4"/><rect x="694" y="345" width="13" height="38" rx="5" fill="#c9d8ee"/>
<g fill="#eaf4ff" opacity=".85"><polygon points="560,175 592,175 572,206"/><polygon points="640,175 690,175 665,200"/><polygon points="560,510 600,510 572,482"/></g>
<rect x="560" y="506" width="165" height="7" fill="#d92b20" opacity=".8"/>
<circle cx="642" cy="150" r="90" fill="url(#lamp)"/><rect x="628" y="130" width="28" height="32" rx="5" fill="#ffd27a"/>
<rect x="830" y="200" width="150" height="125" fill="{'#1d3052' if night else '#a9c4e4'}" stroke="#6b5140" stroke-width="7"/><line x1="905" y1="200" x2="905" y2="325" stroke="#6b5140" stroke-width="6"/>
<rect x="780" y="420" width="220" height="18" fill="#5b4332"/><rect x="795" y="438" width="13" height="72" fill="#4a3628"/><rect x="972" y="438" width="13" height="72" fill="#4a3628"/><rect x="845" y="402" width="78" height="18" fill="#efe6cf" transform="rotate(-4 884 411)"/>
</g>'''

def people():
    return '''<g id="players">
<g><rect x="430" y="425" width="52" height="92" rx="10" fill="#2f6aa8"/><circle cx="456" cy="402" r="26" fill="#f1c9a0"/><rect x="430" y="374" width="52" height="18" rx="8" fill="#b83a2a"/></g>
<g><rect x="740" y="455" width="52" height="84" rx="10" fill="#3d8a5a"/><circle cx="766" cy="433" r="25" fill="#f1c9a0"/><rect x="741" y="408" width="50" height="17" rx="8" fill="#e9e2cf"/></g>
</g>'''

def topbar(phase='НОЧЬ 3/5 · 0:42', heat=0.55, coal=6, color=C['warm']):
    w=int(232*heat)
    return f'''<g id="topbar">
<rect x="24" y="22" width="300" height="56" rx="12" fill="#000" fill-opacity=".55"/>
<text x="44" y="59" font-family="{F}" font-size="24" font-weight="700" fill="{color}">{phase}</text>
<rect x="956" y="22" width="300" height="56" rx="12" fill="#000" fill-opacity=".55"/>
<text x="976" y="44" font-family="{F}" font-size="13" font-weight="600" fill="#9fc4ee">ТЕПЛО</text>
<text x="1236" y="44" text-anchor="end" font-family="{F}" font-size="13" font-weight="600" fill="#9fc4ee">уголь: {coal}</text>
<rect x="976" y="53" width="260" height="12" rx="6" fill="#26324b"/><rect x="976" y="53" width="{w}" height="12" rx="6" fill="#ff9a3a"/>
</g>'''

def journal_btn():
    return f'''<g id="btn-journal"><rect x="24" y="638" width="150" height="58" rx="14" fill="#b0641c"/><text x="99" y="674" text-anchor="middle" font-family="{F}" font-size="19" font-weight="700" fill="#fff">ЖУРНАЛ</text></g>'''

def joystick():
    return '''<g id="joystick" opacity=".9"><circle cx="150" cy="560" r="66" fill="#fff" fill-opacity=".12" stroke="#fff" stroke-opacity=".3" stroke-width="2"/><circle cx="165" cy="548" r="28" fill="#fff" fill-opacity=".3"/></g>'''

def banner(text, color='#fff', y=96):
    return f'''<g id="banner"><rect x="340" y="{y}" width="600" height="60" rx="14" fill="#000" fill-opacity=".6"/><text x="640" y="{y+38}" text-anchor="middle" font-family="{F}" font-size="20" font-weight="700" fill="{color}">{text}</text></g>'''

# 1. Роль в начале раунда
svg('01-role-reveal.svg', f'''<rect width="1280" height="720" fill="#070b14"/>
<circle cx="320" cy="360" r="330" fill="#22355c" opacity=".35"/><circle cx="960" cy="360" r="330" fill="#5a1410" opacity=".35"/>
<g id="card-meteorologist">
<rect x="120" y="110" width="400" height="500" rx="24" fill="#141c2e" stroke="#9fc4ee" stroke-width="3"/>
<text x="320" y="170" text-anchor="middle" font-family="{F}" font-size="18" font-weight="600" fill="#8fa0bd" letter-spacing="3">ТВОЯ РОЛЬ</text>
<circle cx="320" cy="300" r="78" fill="#22355c"/><rect x="292" y="300" width="56" height="70" rx="10" fill="#2f6aa8"/><circle cx="320" cy="275" r="30" fill="#f1c9a0"/><rect x="290" y="244" width="60" height="18" rx="8" fill="#b83a2a"/>
<text x="320" y="440" text-anchor="middle" font-family="{F}" font-size="38" font-weight="800" fill="#fff">МЕТЕОРОЛОГ</text>
<text x="320" y="485" text-anchor="middle" font-family="{F}" font-size="18" fill="#9fc4ee">Один из вас — не человек.</text>
<text x="320" y="512" text-anchor="middle" font-family="{F}" font-size="18" fill="#9fc4ee">Не открывай ему дверь.</text>
</g>
<g id="card-guest">
<rect x="760" y="110" width="400" height="500" rx="24" fill="#16090b" stroke="#d92b20" stroke-width="3"/>
<text x="960" y="170" text-anchor="middle" font-family="{F}" font-size="18" font-weight="600" fill="#c08080" letter-spacing="3">ТВОЯ РОЛЬ</text>
<circle cx="960" cy="300" r="78" fill="#2a0e0e"/><rect x="932" y="298" width="56" height="74" rx="10" fill="#05080f"/><circle cx="960" cy="272" r="30" fill="#05080f"/><circle cx="950" cy="270" r="4" fill="#bfe0ff"/><circle cx="970" cy="270" r="4" fill="#bfe0ff"/>
<text x="960" y="440" text-anchor="middle" font-family="{F}" font-size="38" font-weight="800" fill="#ff6a5a">ГОСТЬ</text>
<text x="960" y="485" text-anchor="middle" font-family="{F}" font-size="18" fill="#f0b8b0">Обмани их. Заставь открыть дверь.</text>
<text x="960" y="512" text-anchor="middle" font-family="{F}" font-size="18" fill="#f0b8b0">Браслет выдаёт тебя: будь осторожен.</text>
</g>
<text x="640" y="670" text-anchor="middle" font-family="{F}" font-size="16" fill="#5d6a82">Показывается 8 секунд в начале раунда. Игрок видит только свою карточку.</text>''')

# 2. День
svg('02-hud-day.svg', room(False)+people()+topbar('ДЕНЬ 2/5 · 1:04',0.72,9,C['warm'])+banner('ДЕНЬ 2. Сними показания и запиши в журнал.',C['warm'])+journal_btn()+joystick()+f'''
<g id="prompt"><rect x="860" y="250" width="200" height="64" rx="12" fill="#000" fill-opacity=".7"/><rect x="872" y="262" width="40" height="40" rx="8" fill="#fff"/><text x="892" y="290" text-anchor="middle" font-family="{F}" font-size="20" font-weight="700" fill="#000">E</text><text x="924" y="281" font-family="{F}" font-size="13" fill="#9fc4ee">Барометр</text><text x="924" y="301" font-family="{F}" font-size="16" font-weight="700" fill="#fff">Снять показания</text></g>
<g id="tasks"><rect x="1036" y="96" width="220" height="150" rx="12" fill="#000" fill-opacity=".5"/><text x="1052" y="124" font-family="{F}" font-size="14" font-weight="700" fill="#ffb866">ЗАДАНИЯ ДНЯ</text>
<text x="1052" y="152" font-family="{F}" font-size="15" fill="#dfe6f2">✓ Запись в журнал</text><text x="1052" y="180" font-family="{F}" font-size="15" fill="#dfe6f2">○ Уголь в печь</text><text x="1052" y="208" font-family="{F}" font-size="15" fill="#dfe6f2">○ Очистить мачту</text><text x="1052" y="234" font-family="{F}" font-size="12" fill="#8fa0bd">можно и не всё</text></g>''')

# 3. Ночь: стук и дверь
svg('03-hud-night-door.svg', room(True)+people()+'<rect width="1280" height="720" fill="url(#vig)"/>'+topbar('НОЧЬ 3/5 · 0:42',0.42,6)+journal_btn()+joystick()+f'''
<g id="window-guest"><g fill="#05080f" opacity=".8"><circle cx="945" cy="245" r="18"/><rect x="924" y="262" width="42" height="63"/></g></g>
<g id="knock"><rect x="420" y="560" width="440" height="78" rx="14" fill="#000" fill-opacity=".72" stroke="#d92b20" stroke-width="2"/>
<text x="640" y="592" text-anchor="middle" font-family="{F}" font-size="16" font-weight="700" fill="#ff8a7a" letter-spacing="2">ТУК · ТУК · ТУК · ТУК</text>
<text x="640" y="621" text-anchor="middle" font-family="{F}" font-size="19" fill="#fff">«Айбек»: это я, откройте, я замерзаю!</text></g>
<g id="door-buttons">
<circle cx="1176" cy="604" r="70" fill="#d92b20"/><text x="1176" y="598" text-anchor="middle" font-family="{F}" font-size="19" font-weight="800" fill="#fff">ОТКРЫТЬ</text><text x="1176" y="622" text-anchor="middle" font-family="{F}" font-size="13" fill="#ffd9d4">держать 3 с</text>
<circle cx="1176" cy="604" r="78" fill="none" stroke="#fff" stroke-width="5" stroke-dasharray="170 500" transform="rotate(-90 1176 604)"/>
<circle cx="1036" cy="636" r="46" fill="#3c465a"/><text x="1036" y="641" text-anchor="middle" font-family="{F}" font-size="14" font-weight="700" fill="#fff">ГЛАЗОК</text>
<circle cx="1036" cy="524" r="46" fill="#b0641c"/><text x="1036" y="529" text-anchor="middle" font-family="{F}" font-size="13" font-weight="700" fill="#fff">ОТТАЩИТЬ</text>
</g>
<text x="1176" y="500" text-anchor="middle" font-family="{F}" font-size="12" fill="#9fc4ee">кольцо = прогресс</text>''')

# 4. Журнал
rows=[('#1f4fa0','Д2  Температура: −18°',False),('#1c7a45','Д2  Ветер: С-З',False),('#1f4fa0','Д2  Давление: 642',True),('#b0641c','Д2  Снег: 60 см',False),('#7a2d8a','Д1  Температура: −12°',False)]
r=''
for i,(col,t,dark) in enumerate(rows):
    y=210+i*52
    c='#0f2550' if dark else col
    r+=f'<circle cx="252" cy="{y-6}" r="8" fill="{col}"/><text x="272" y="{y}" font-family="{H}" font-style="italic" font-size="21" fill="{c}">{t}</text>'
    if dark:
        r+=f'<ellipse cx="400" cy="{y-7}" rx="160" ry="22" fill="none" stroke="#d92b20" stroke-width="2.5"/><text x="272" y="{y+26}" font-family="{H}" font-style="italic" font-size="14" fill="#d92b20">чернила темнее — подделка?</text>'
svg('04-journal.svg', room(False)+'<rect width="1280" height="720" fill="#000" fill-opacity=".55"/>'+f'''
<g id="journal">
<rect x="200" y="80" width="880" height="560" rx="18" fill="#2a1f18"/>
<rect x="222" y="100" width="836" height="520" rx="8" fill="#efe6cf"/>
<g stroke="#c9d6e6" stroke-width="1">{''.join(f'<line x1="222" y1="{y}" x2="1058" y2="{y}"/>' for y in range(170,620,52))}</g>
<line x1="640" y1="100" x2="640" y2="620" stroke="#b9ad90" stroke-width="3"/><line x1="236" y1="100" x2="236" y2="620" stroke="#e0a09a" stroke-width="1.5"/>
<text x="252" y="148" font-family="{H}" font-style="italic" font-weight="700" font-size="28" fill="#2b3a5c">Журнал · День 2</text>
<circle cx="1036" cy="126" r="20" fill="#8c7a5a"/><text x="1036" y="133" text-anchor="middle" font-family="{F}" font-size="20" fill="#fff">✕</text>
{r}
<text x="664" y="148" font-family="{F}" font-size="22" font-weight="700" fill="#2b3a5c">Новая запись</text>
<g font-family="{F}" font-size="16" font-weight="600">
<rect x="664" y="172" width="180" height="48" rx="12" fill="#2b3a5c"/><text x="754" y="202" text-anchor="middle" fill="#fff">Температура</text>
<rect x="854" y="172" width="180" height="48" rx="12" fill="#d9ceb0"/><text x="944" y="202" text-anchor="middle" fill="#2b3a5c">Ветер</text>
<rect x="664" y="230" width="180" height="48" rx="12" fill="#d9ceb0"/><text x="754" y="260" text-anchor="middle" fill="#2b3a5c">Давление</text>
<rect x="854" y="230" width="180" height="48" rx="12" fill="#d9ceb0"/><text x="944" y="260" text-anchor="middle" fill="#2b3a5c">Снег</text></g>
<rect x="664" y="300" width="370" height="64" rx="12" fill="#d9ceb0"/>
<rect x="676" y="312" width="56" height="40" rx="10" fill="#c4b893"/><text x="704" y="340" text-anchor="middle" font-family="{F}" font-size="26" fill="#2b3a5c">−</text>
<text x="849" y="344" text-anchor="middle" font-family="{F}" font-size="30" font-weight="800" fill="#2b3a5c">−21°</text>
<rect x="966" y="312" width="56" height="40" rx="10" fill="#c4b893"/><text x="994" y="340" text-anchor="middle" font-family="{F}" font-size="26" fill="#2b3a5c">+</text>
<rect x="664" y="384" width="370" height="64" rx="14" fill="#b0641c"/><text x="849" y="424" text-anchor="middle" font-family="{F}" font-size="22" font-weight="800" fill="#fff">ЗАПИСАТЬ</text>
<g font-family="{F}" font-size="14" fill="#7a705a"><text x="664" y="486">Чернила:</text>
<circle cx="740" cy="481" r="6" fill="#1f4fa0"/><text x="752" y="486">Айбек</text><circle cx="812" cy="481" r="6" fill="#1c7a45"/><text x="824" y="486">Нурай</text><circle cx="884" cy="481" r="6" fill="#b0641c"/><text x="896" y="486">ты</text><circle cx="928" cy="481" r="6" fill="#7a2d8a"/><text x="940" y="486">Тимур</text></g>
<text x="664" y="580" font-family="{F}" font-style="italic" font-size="15" fill="#7a705a">Пиши то, что видишь. Даже если страшно.</text>
</g>''')

# 5. Совет и голосование
cards=''
names=[('Айбек','#1f4fa0','✓ писал'),('Нурай','#1c7a45','✓ писал'),('Тимур','#7a2d8a','✗ не писал'),('Бекзат','#a02832','✓ писал'),('ты','#b0641c','✓ писал')]
for i,(n,col,st) in enumerate(names):
    x=170+i*196
    sel = i==2
    cards+=f'''<g id="vote-{n}"><rect x="{x}" y="390" width="176" height="200" rx="18" fill="{'#3a1414' if sel else '#141c2e'}" stroke="{'#d92b20' if sel else '#26324b'}" stroke-width="{4 if sel else 2}"/>
<circle cx="{x+88}" cy="450" r="34" fill="#f1c9a0"/><rect x="{x+56}" y="412" width="64" height="18" rx="8" fill="{col}"/>
<text x="{x+88}" y="515" text-anchor="middle" font-family="{F}" font-size="21" font-weight="700" fill="#fff">{n}</text>
<circle cx="{x+30}" cy="545" r="7" fill="{col}"/><text x="{x+44}" y="550" font-family="{F}" font-size="14" fill="{'#ff8a7a' if '✗' in st else '#9fc4ee'}">{st}</text>
{'<text x="'+str(x+88)+'" y="578" text-anchor="middle" font-family="'+F+'" font-size="14" font-weight="700" fill="#ff8a7a">голосов: 3</text>' if sel else ''}</g>'''
svg('05-council-vote.svg', room(False)+'<rect width="1280" height="720" fill="#05080f" fill-opacity=".7"/>'+topbar('ГОЛОСОВАНИЕ · 0:11',0.6,5)+f'''
<text x="640" y="150" text-anchor="middle" font-family="{F}" font-size="34" font-weight="800" fill="#ffb866">Кого запереть в кладовке?</text>
<text x="640" y="190" text-anchor="middle" font-family="{F}" font-size="18" fill="#9fc4ee">Нужно больше половины голосов. Роль запертого увидят все.</text>
<g id="clues"><rect x="330" y="225" width="620" height="120" rx="14" fill="#000" fill-opacity=".45"/><text x="352" y="256" font-family="{F}" font-size="15" font-weight="700" fill="#ffb866">УЛИКИ ЭТОЙ НОЧИ</text>
<text x="352" y="284" font-family="{F}" font-size="16" fill="#dfe6f2">• запись «Давление: 642» — чернила темнее обычного</text>
<text x="352" y="310" font-family="{F}" font-size="16" fill="#dfe6f2">• утром следы на снегу ведут от сарая с генератором</text>
<text x="352" y="336" font-family="{F}" font-size="16" fill="#dfe6f2">• ложный стук был от имени Айбека, а Айбек стоял у печи</text></g>
{cards}
<g id="skip"><rect x="540" y="620" width="200" height="56" rx="14" fill="#3c465a"/><text x="640" y="655" text-anchor="middle" font-family="{F}" font-size="19" font-weight="700" fill="#fff">ПРОПУСТИТЬ</text></g>''')

# 6. Панель Гостя ночью
ab=[('Голос (стук)','2',True),('Подделать запись','1',True),('Тьма','1',True),('Чужие следы','1',True),('Украсть уголь','1',True),('Метель','3',False)]
a=''
for i,(n,c,ok) in enumerate(ab):
    y=170+i*62
    a+=f'<rect x="40" y="{y}" width="300" height="52" rx="12" fill="{"#22355c" if ok else "#262a33"}"/><text x="60" y="{y+33}" font-family="{F}" font-size="18" font-weight="700" fill="{"#fff" if ok else "#6b7385"}">{n}</text><circle cx="312" cy="{y+26}" r="16" fill="{"#9fc4ee" if ok else "#3c465a"}"/><text x="312" y="{y+32}" text-anchor="middle" font-family="{F}" font-size="16" font-weight="800" fill="#0b1220">{c}</text>'
svg('06-guest-panel.svg', room(True)+people()+'<rect width="1280" height="720" fill="url(#vig)"/>'+topbar('НОЧЬ 2/5 · 0:37',0.5,8)+journal_btn()+f'''
<g id="guest-panel"><rect x="24" y="100" width="332" height="520" rx="18" fill="#0a0e18" fill-opacity=".92" stroke="#9fc4ee" stroke-width="2"/>
<text x="44" y="138" font-family="{F}" font-size="20" font-weight="800" fill="#9fc4ee">ГОСТЬ</text>
<g id="cold-points"><circle cx="250" cy="131" r="11" fill="#9fc4ee"/><circle cx="278" cy="131" r="11" fill="#9fc4ee"/><circle cx="306" cy="131" r="11" fill="#3c465a"/><text x="232" y="160" font-family="{F}" font-size="12" fill="#8fa0bd">очки холода: 2</text></g>
{a}
<text x="44" y="565" font-family="{F}" font-size="14" fill="#9fc4ee">Каждое действие — браслет моргает</text><text x="44" y="585" font-family="{F}" font-size="14" fill="#9fc4ee">синим 3 секунды. Не попадайся на глаза.</text></g>
<g id="bracelet-example"><rect x="742" y="380" width="48" height="26" rx="6" fill="#50a0ff"/><text x="766" y="400" text-anchor="middle" font-family="{F}" font-size="18" fill="#fff">❄</text>
<text x="800" y="398" font-family="{F}" font-size="13" fill="#9fc4ee">так браслет видят игроки рядом</text></g>''')

# 7. Иконки
def icon(x, kind):
    base=f'<g transform="translate({x},60)"><rect width="512" height="512" rx="64" fill="#0b1220"/>'
    if kind=='A':
        b=f'''<ellipse cx="350" cy="290" rx="160" ry="260" fill="url(#lamp)"/>
<rect x="128" y="96" width="224" height="380" fill="#3b4a66" stroke="#9fc4ee" stroke-width="6"/>
<polygon points="352,96 376,110 376,476 352,476" fill="#ff9a3a"/>
<circle cx="240" cy="230" r="14" fill="#0a0f1a" stroke="#c9d8ee" stroke-width="4"/>
<g fill="#05080f" opacity=".85" transform="translate(170,260)"><rect x="0" y="36" width="66" height="64" rx="14"/><rect x="2" y="0" width="13" height="48" rx="6"/><rect x="18" y="-10" width="13" height="58" rx="6"/><rect x="34" y="-8" width="13" height="56" rx="6"/><rect x="50" y="4" width="13" height="46" rx="6"/></g>
<text x="256" y="72" text-anchor="middle" font-family="{F}" font-size="50" font-weight="900" fill="#fff">DON'T OPEN</text>
<rect x="372" y="420" width="116" height="50" rx="10" fill="#d92b20"/><text x="430" y="456" text-anchor="middle" font-family="{F}" font-size="30" font-weight="800" fill="#fff">04:40</text>'''
    elif kind=='B':
        b=f'''<circle cx="256" cy="380" r="230" fill="url(#fire)"/>
<rect x="210" y="300" width="92" height="90" rx="10" fill="#15110f"/><rect x="232" y="330" width="48" height="36" rx="5" fill="#ff9a3a"/>
<g><circle cx="110" cy="330" r="32" fill="#f1c9a0"/><rect x="80" y="362" width="60" height="90" rx="12" fill="#2f6aa8"/></g>
<g><circle cx="402" cy="330" r="32" fill="#f1c9a0"/><rect x="372" y="362" width="60" height="90" rx="12" fill="#3d8a5a"/></g>
<g><circle cx="176" cy="250" r="28" fill="#f1c9a0"/><rect x="150" y="278" width="52" height="70" rx="10" fill="#7a2d8a"/></g>
<g><circle cx="336" cy="250" r="28" fill="#1a1a22"/><circle cx="326" cy="248" r="5" fill="#bfe0ff"/><circle cx="346" cy="248" r="5" fill="#bfe0ff"/><rect x="310" y="278" width="52" height="70" rx="10" fill="#a02832"/></g>
<text x="256" y="90" text-anchor="middle" font-family="{F}" font-size="46" font-weight="900" fill="#fff">WHO'S</text><text x="256" y="146" text-anchor="middle" font-family="{F}" font-size="46" font-weight="900" fill="#ff6a5a">KNOCKING?</text>'''
    else:
        b=f'''<circle cx="256" cy="270" r="200" fill="#3b4a66"/><circle cx="256" cy="270" r="170" fill="#0e1728" stroke="#c9d8ee" stroke-width="14"/>
<circle cx="256" cy="270" r="150" fill="url(#sky)" opacity=".35"/>
<g fill="#05080f"><circle cx="256" cy="232" r="34"/><rect x="216" y="262" width="80" height="120" rx="18"/></g><circle cx="244" cy="230" r="5" fill="#bfe0ff"/><circle cx="268" cy="230" r="5" fill="#bfe0ff"/>
<g fill="#fff" opacity=".8"><circle cx="170" cy="200" r="4"/><circle cx="330" cy="300" r="5"/><circle cx="190" cy="330" r="3"/><circle cx="320" cy="180" r="3"/></g>
<rect x="156" y="440" width="200" height="50" rx="10" fill="#d92b20"/><text x="256" y="476" text-anchor="middle" font-family="{F}" font-size="30" font-weight="800" fill="#fff">04:40</text>'''
    return base+b+f'<text x="256" y="555" text-anchor="middle" font-family="{F}" font-size="22" font-weight="700" fill="#8fa0bd">Вариант {kind}</text></g>'
svg('07-icons.svg', '<rect width="1760" height="660" fill="#070b14"/>'+icon(48,'A')+icon(624,'B')+icon(1200,'C'), 1760, 660)
print('ok')
