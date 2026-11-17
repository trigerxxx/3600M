--!nonstrict
-- Интерфейс прототипа. Весь интерфейс строится кодом; финальный вид делаем по макетам из art/ui.

local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local RunService = game:GetService("RunService")

local Shared = ReplicatedStorage:WaitForChild("Shared")
local Config = require(Shared.Config)
local Net = ReplicatedStorage:WaitForChild("Net")
local Action = Net:WaitForChild("Action") :: RemoteEvent
local StateRemote = Net:WaitForChild("State") :: RemoteEvent
local EventRemote = Net:WaitForChild("Event") :: RemoteEvent

local me = Players.LocalPlayer
local P = Config.Palette

-- ---------- конструктор интерфейса ----------
local gui = Instance.new("ScreenGui")
gui.Name = "HUD"
gui.ResetOnSpawn = false
gui.IgnoreGuiInset = true
gui.Parent = me:WaitForChild("PlayerGui")

local function frame(parent: Instance, size: UDim2, pos: UDim2, color: Color3?, alpha: number?): Frame
	local f = Instance.new("Frame")
	f.Size = size
	f.Position = pos
	f.BackgroundColor3 = color or Color3.new(0, 0, 0)
	f.BackgroundTransparency = alpha or 0.35
	f.BorderSizePixel = 0
	local c = Instance.new("UICorner")
	c.CornerRadius = UDim.new(0, 10)
	c.Parent = f
	f.Parent = parent
	return f
end

local function label(parent: Instance, text: string, size: UDim2, pos: UDim2, color: Color3?, textSize: number?): TextLabel
	local l = Instance.new("TextLabel")
	l.BackgroundTransparency = 1
	l.Size = size
	l.Position = pos
	l.Text = text
	l.TextColor3 = color or Color3.new(1, 1, 1)
	l.TextSize = textSize or 18
	l.Font = Enum.Font.GothamBold
	l.TextWrapped = true
	l.Parent = parent
	return l
end

local function button(parent: Instance, text: string, size: UDim2, pos: UDim2, color: Color3): TextButton
	local b = Instance.new("TextButton")
	b.Size = size
	b.Position = pos
	b.BackgroundColor3 = color
	b.TextColor3 = Color3.new(1, 1, 1)
	b.Text = text
	b.TextSize = 18
	b.Font = Enum.Font.GothamBold
	b.AutoButtonColor = true
	b.BorderSizePixel = 0
	local c = Instance.new("UICorner")
	c.CornerRadius = UDim.new(0, 12)
	c.Parent = b
	b.Parent = parent
	return b
end

local function clear(parent: Instance)
	for _, ch in parent:GetChildren() do
		if not ch:IsA("UIListLayout") and not ch:IsA("UICorner") and not ch:IsA("UIPadding") then
			ch:Destroy()
		end
	end
end

local function list(parent: Instance, padding: number)
	local l = Instance.new("UIListLayout")
	l.Padding = UDim.new(0, padding)
	l.SortOrder = Enum.SortOrder.LayoutOrder
	l.Parent = parent
end

-- верхняя панель
local top = frame(gui, UDim2.fromOffset(260, 46), UDim2.new(0, 16, 0, 16))
local phaseLabel = label(top, "", UDim2.fromScale(1, 1), UDim2.fromScale(0, 0), P.warm, 20)

local heatBox = frame(gui, UDim2.fromOffset(240, 46), UDim2.new(1, -256, 0, 16))
label(heatBox, "ТЕПЛО", UDim2.fromOffset(80, 18), UDim2.fromOffset(10, 2), P.ice, 12)
local coalLabel = label(heatBox, "", UDim2.fromOffset(100, 18), UDim2.new(1, -110, 0, 2), P.ice, 12)
local heatBack = frame(heatBox, UDim2.new(1, -20, 0, 10), UDim2.fromOffset(10, 26), Color3.fromRGB(38, 50, 75), 0)
local heatFill = frame(heatBack, UDim2.fromScale(0.5, 1), UDim2.fromScale(0, 0), Color3.fromRGB(255, 154, 58), 0)

-- баннер по центру
local banner = frame(gui, UDim2.fromOffset(520, 70), UDim2.new(0.5, -260, 0, 80))
local bannerText = label(banner, "", UDim2.new(1, -20, 1, 0), UDim2.fromOffset(10, 0), Color3.new(1, 1, 1), 20)
banner.Visible = false
local bannerUntil = 0

local function showBanner(text: string, color: Color3?, seconds: number?)
	bannerText.Text = text
	bannerText.TextColor3 = color or Color3.new(1, 1, 1)
	banner.Visible = true
	bannerUntil = os.clock() + (seconds or 4)
end

-- стук
local knockBox = frame(gui, UDim2.fromOffset(420, 60), UDim2.new(0.5, -210, 1, -170), Color3.new(0, 0, 0), 0.25)
local knockStroke = Instance.new("UIStroke")
knockStroke.Color = P.danger
knockStroke.Thickness = 2
knockStroke.Parent = knockBox
local knockText = label(knockBox, "", UDim2.new(1, -20, 1, 0), UDim2.fromOffset(10, 0), Color3.new(1, 1, 1), 18)
knockBox.Visible = false

-- кнопки двери
local doorPanel = Instance.new("Frame")
doorPanel.BackgroundTransparency = 1
doorPanel.Size = UDim2.fromOffset(240, 120)
doorPanel.Position = UDim2.new(1, -256, 1, -140)
doorPanel.Parent = gui
local openBtn = button(doorPanel, "ОТКРЫТЬ\n(держать)", UDim2.fromOffset(120, 110), UDim2.fromOffset(120, 0), P.danger)
local peepBtn = button(doorPanel, "ГЛАЗОК", UDim2.fromOffset(105, 50), UDim2.fromOffset(0, 0), Color3.fromRGB(60, 70, 90))
local dragBtn = button(doorPanel, "ОТТАЩИТЬ", UDim2.fromOffset(105, 50), UDim2.fromOffset(0, 60), Color3.fromRGB(176, 100, 28))
doorPanel.Visible = false

openBtn.MouseButton1Down:Connect(function()
	Action:FireServer("beginOpen")
end)
openBtn.MouseButton1Up:Connect(function()
	Action:FireServer("cancelOpen")
end)
openBtn.MouseLeave:Connect(function()
	Action:FireServer("cancelOpen")
end)
peepBtn.Activated:Connect(function()
	Action:FireServer("peep")
end)
dragBtn.Activated:Connect(function()
	Action:FireServer("drag")
end)

-- кнопка журнала
local journalBtn = button(gui, "ЖУРНАЛ", UDim2.fromOffset(120, 46), UDim2.new(0, 16, 1, -62), Color3.fromRGB(176, 100, 28))

-- журнал
local journal = frame(gui, UDim2.fromOffset(640, 380), UDim2.new(0.5, -320, 0.5, -190), P.paper, 0)
journal.Visible = false
label(journal, "Журнал наблюдений", UDim2.fromOffset(300, 30), UDim2.fromOffset(16, 8), Color3.fromRGB(43, 58, 92), 20)
local closeJ = button(journal, "✕", UDim2.fromOffset(36, 36), UDim2.new(1, -46, 0, 8), Color3.fromRGB(140, 120, 90))
local entries = Instance.new("ScrollingFrame")
entries.Size = UDim2.new(0, 330, 1, -56)
entries.Position = UDim2.fromOffset(16, 46)
entries.BackgroundTransparency = 1
entries.ScrollBarThickness = 6
entries.AutomaticCanvasSize = Enum.AutomaticSize.Y
entries.CanvasSize = UDim2.new()
entries.Parent = journal
list(entries, 4)

local form = Instance.new("Frame")
form.BackgroundTransparency = 1
form.Size = UDim2.new(0, 270, 1, -56)
form.Position = UDim2.new(0, 356, 0, 46)
form.Parent = journal
label(form, "Новая запись", UDim2.fromOffset(270, 24), UDim2.fromOffset(0, 0), Color3.fromRGB(43, 58, 92), 16)
local instrumentRow = Instance.new("Frame")
instrumentRow.BackgroundTransparency = 1
instrumentRow.Size = UDim2.fromOffset(270, 84)
instrumentRow.Position = UDim2.fromOffset(0, 30)
instrumentRow.Parent = form
local valueBox = Instance.new("TextBox")
valueBox.Size = UDim2.fromOffset(270, 44)
valueBox.Position = UDim2.fromOffset(0, 124)
valueBox.PlaceholderText = "значение с прибора"
valueBox.Text = ""
valueBox.TextSize = 20
valueBox.Font = Enum.Font.Gotham
valueBox.BackgroundColor3 = Color3.fromRGB(217, 206, 176)
valueBox.TextColor3 = Color3.fromRGB(43, 58, 92)
valueBox.ClearTextOnFocus = false
valueBox.Parent = form
local writeBtn = button(form, "ЗАПИСАТЬ", UDim2.fromOffset(270, 50), UDim2.fromOffset(0, 180), Color3.fromRGB(176, 100, 28))
local formHint = label(form, "Пиши то, что видишь. Даже если страшно.", UDim2.fromOffset(270, 40), UDim2.fromOffset(0, 240), Color3.fromRGB(122, 112, 90), 13)

local chosenInstrument = "temp"
local instrumentButtons: { [string]: TextButton } = {}
for i, key in Config.Instruments do
	local x = ((i - 1) % 2) * 137
	local y = math.floor((i - 1) / 2) * 42
	local b = button(instrumentRow, Config.InstrumentNames[key], UDim2.fromOffset(133, 38), UDim2.fromOffset(x, y), Color3.fromRGB(217, 206, 176))
	b.TextColor3 = Color3.fromRGB(43, 58, 92)
	b.TextSize = 15
	instrumentButtons[key] = b
	b.Activated:Connect(function()
		chosenInstrument = key
		for k, other in instrumentButtons do
			other.BackgroundColor3 = if k == key then Color3.fromRGB(43, 58, 92) else Color3.fromRGB(217, 206, 176)
			other.TextColor3 = if k == key then Color3.new(1, 1, 1) else Color3.fromRGB(43, 58, 92)
		end
	end)
end

writeBtn.Activated:Connect(function()
	if valueBox.Text ~= "" then
		Action:FireServer("write", { instrument = chosenInstrument, value = valueBox.Text })
		valueBox.Text = ""
	end
end)
journalBtn.Activated:Connect(function()
	journal.Visible = not journal.Visible
end)
closeJ.Activated:Connect(function()
	journal.Visible = false
end)

-- панель Гостя
local guestPanel = frame(gui, UDim2.fromOffset(250, 270), UDim2.new(0, 16, 0.5, -135), Color3.fromRGB(10, 14, 24), 0.2)
local guestStroke = Instance.new("UIStroke")
guestStroke.Color = P.ice
guestStroke.Parent = guestPanel
local guestTitle = label(guestPanel, "", UDim2.new(1, -20, 0, 30), UDim2.fromOffset(10, 6), P.ice, 16)
local guestList = Instance.new("Frame")
guestList.BackgroundTransparency = 1
guestList.Size = UDim2.new(1, -20, 1, -44)
guestList.Position = UDim2.fromOffset(10, 40)
guestList.Parent = guestPanel
list(guestList, 6)
guestPanel.Visible = false

-- выбор игрока (для «Голоса» и голосования)
local picker = frame(gui, UDim2.fromOffset(320, 360), UDim2.new(0.5, -160, 0.5, -180), Color3.fromRGB(16, 22, 38), 0.05)
local pickerTitle = label(picker, "", UDim2.new(1, -20, 0, 36), UDim2.fromOffset(10, 6), P.warm, 18)
local pickerList = Instance.new("Frame")
pickerList.BackgroundTransparency = 1
pickerList.Size = UDim2.new(1, -20, 1, -52)
pickerList.Position = UDim2.fromOffset(10, 46)
pickerList.Parent = picker
list(pickerList, 6)
picker.Visible = false

-- ---------- состояние ----------
local snap: any = nil
local lastReading: { instrument: string, value: string }? = nil
local pickerMode = ""
local lastKey = ""

local function nameOf(id: number): string
	if snap then
		for _, p in snap.players do
			if p.id == id then
				return p.name
			end
		end
	end
	return "?"
end

local function myState(): any
	if not snap or not snap.players then
		return nil
	end
	for _, p in snap.players do
		if p.id == me.UserId then
			return p
		end
	end
	return nil
end

local function openPicker(mode: string, title: string)
	pickerMode = mode
	pickerTitle.Text = title
	clear(pickerList)
	if not snap then
		return
	end
	for _, p in snap.players do
		if (p.status == "inside" or p.status == "outside") and (mode ~= "voice" or p.id ~= me.UserId) then
			local b = button(pickerList, p.name, UDim2.new(1, 0, 0, 40), UDim2.new(), Color3.fromRGB(34, 53, 92))
			b.Activated:Connect(function()
				if pickerMode == "voice" then
					Action:FireServer("ability", { name = "voice", arg = p.id })
				elseif pickerMode == "vote" then
					Action:FireServer("vote", p.id)
				end
				picker.Visible = false
			end)
		end
	end
	if mode == "vote" then
		local skip = button(pickerList, "Пропустить", UDim2.new(1, 0, 0, 40), UDim2.new(), Color3.fromRGB(80, 80, 90))
		skip.Activated:Connect(function()
			Action:FireServer("vote", 0)
			picker.Visible = false
		end)
	end
	local cancel = button(pickerList, "Закрыть", UDim2.new(1, 0, 0, 36), UDim2.new(), Color3.fromRGB(60, 60, 70))
	cancel.Activated:Connect(function()
		picker.Visible = false
	end)
	picker.Visible = true
end

local function renderJournal()
	clear(entries)
	if not snap or not snap.journal then
		return
	end
	local mine = myState()
	local isGuest = mine and mine.role == "guest"
	local inks: { [number]: number } = {}
	for _, p in snap.players do
		inks[p.id] = p.ink
	end
	for i, e in snap.journal do
		local row = Instance.new("Frame")
		row.BackgroundTransparency = 1
		row.Size = UDim2.new(1, -8, 0, 28)
		row.LayoutOrder = -i
		row.Parent = entries
		local color = Config.InkColors[inks[e.author] or 8] or Color3.new(0, 0, 0)
		if e.darker then
			color = color:Lerp(Color3.new(0, 0, 0), 0.35)
		end
		local text = string.format("Д%d  %s: %s", e.day, Config.InstrumentNames[e.instrument] or e.instrument, e.value)
		local l = label(row, text, UDim2.new(1, -90, 1, 0), UDim2.new(), color, 16)
		l.TextXAlignment = Enum.TextXAlignment.Left
		l.Font = Enum.Font.Gotham
		if isGuest and snap.phase == "night" and (snap.points or 0) >= Config.Ability.forge.cost and e.author ~= me.UserId then
			local f = button(row, "подделать", UDim2.fromOffset(84, 24), UDim2.new(1, -84, 0, 2), Color3.fromRGB(34, 53, 92))
			f.TextSize = 12
			f.Activated:Connect(function()
				Action:FireServer("ability", { name = "forge", arg = i })
			end)
		end
	end
end

local abilityNames = {
	voice = "Голос (стук)",
	dark = "Тьма",
	prints = "Чужие следы",
	steal = "Украсть уголь",
	blizzard = "Метель",
}
local abilityOrder = { "voice", "dark", "prints", "steal", "blizzard" }

local function renderGuest()
	local mine = myState()
	local show = snap and snap.phase == "night" and mine and mine.role == "guest"
		and (mine.status == "inside" or mine.status == "outside")
	guestPanel.Visible = show and true or false
	if not show then
		return
	end
	guestTitle.Text = string.format("ГОСТЬ · очки холода: %d", snap.points or 0)
	clear(guestList)
	for _, key in abilityOrder do
		local def = Config.Ability[key]
		local usable = (snap.points or 0) >= def.cost and not (key == "blizzard" and snap.blizzardUsed)
		local b = button(guestList, string.format("%s · %d", abilityNames[key], def.cost), UDim2.new(1, 0, 0, 36), UDim2.new(),
			if usable then Color3.fromRGB(34, 53, 92) else Color3.fromRGB(40, 40, 48))
		b.TextSize = 15
		b.Activated:Connect(function()
			if key == "voice" then
				openPicker("voice", "От чьего имени постучать?")
			else
				Action:FireServer("ability", { name = key })
			end
		end)
	end
	local hint = label(guestList, "Подделка — кнопки в журнале. Браслет моргает синим 3 с: не попадайся на глаза.", UDim2.new(1, 0, 0, 44), UDim2.new(), P.ice, 12)
	hint.Font = Enum.Font.Gotham
end

-- синий браслет «холодные руки» у тех, кто рядом
local braceletTags: { [number]: BillboardGui } = {}

local function renderBracelets()
	if not snap or not snap.players then
		return
	end
	local myRoot = me.Character and me.Character:FindFirstChild("HumanoidRootPart") :: BasePart?
	for _, p in snap.players do
		local plr = Players:GetPlayerByUserId(p.id)
		local root = plr and plr.Character and plr.Character:FindFirstChild("HumanoidRootPart") :: BasePart?
		local near = myRoot and root and (myRoot.Position - root.Position).Magnitude <= Config.BraceletRadius
		local on = p.bracelet and near and p.id ~= me.UserId
		local tag = braceletTags[p.id]
		if on and root and not tag then
			tag = Instance.new("BillboardGui")
			tag.Size = UDim2.fromOffset(60, 24)
			tag.StudsOffset = Vector3.new(0, 3.5, 0)
			tag.AlwaysOnTop = true
			local t = Instance.new("TextLabel")
			t.Size = UDim2.fromScale(1, 1)
			t.BackgroundColor3 = Color3.fromRGB(80, 160, 255)
			t.Text = "❄"
			t.TextColor3 = Color3.new(1, 1, 1)
			t.TextScaled = true
			t.Parent = tag
			tag.Adornee = root
			tag.Parent = gui
			braceletTags[p.id] = tag
		elseif not on and tag then
			tag:Destroy()
			braceletTags[p.id] = nil
		end
	end
end

-- ---------- удержание: прогресс в лобби, итоги раунда, подсказки новичкам ----------
local GOLD = Color3.fromRGB(255, 205, 90)

local function bar(parent: Instance, pos: UDim2, width: number, fill: number): Frame
	local back = frame(parent, UDim2.fromOffset(width, 12), pos, Color3.fromRGB(38, 50, 75), 0)
	frame(back, UDim2.fromScale(math.clamp(fill, 0, 1), 1), UDim2.fromScale(0, 0), Color3.fromRGB(255, 154, 58), 0)
	return back
end

local function taskRows(parent: Instance, tasks: { any }, y: number, width: number): number
	for _, t in tasks do
		local mark = if t.done then "✓" else string.format("%d/%d", t.progress, t.target)
		local l = label(parent, string.format("%s  %s", mark, t.text), UDim2.fromOffset(width, 22), UDim2.fromOffset(16, y),
			if t.done then Color3.fromRGB(140, 220, 150) else Color3.fromRGB(223, 230, 242), 14)
		l.TextXAlignment = Enum.TextXAlignment.Left
		l.Font = Enum.Font.Gotham
		y += 24
	end
	return y
end

-- панель прогресса в лобби
local lobbyCard = frame(gui, UDim2.fromOffset(340, 230), UDim2.new(0, 16, 0.5, -115), Color3.fromRGB(14, 20, 34), 0.15)
lobbyCard.Visible = false

local function renderLobbyCard(p)
	clear(lobbyCard)
	if not p then
		lobbyCard.Visible = false
		return
	end
	lobbyCard.Visible = true
	local title = label(lobbyCard, string.format("%s · уровень %d", p.title, p.level), UDim2.fromOffset(310, 26), UDim2.fromOffset(16, 10), P.warm, 18)
	title.TextXAlignment = Enum.TextXAlignment.Left
	bar(lobbyCard, UDim2.fromOffset(16, 42), 308, p.xp / math.max(1, p.xpNext))
	local info = label(lobbyCard, string.format("Опыт %d/%d · дней экспедиции: %d · досье: %d", p.xp, p.xpNext, p.playDays, p.dossier),
		UDim2.fromOffset(310, 20), UDim2.fromOffset(16, 58), P.ice, 12)
	info.TextXAlignment = Enum.TextXAlignment.Left
	info.Font = Enum.Font.Gotham
	local head = label(lobbyCard, "ЗАДАНИЯ ДНЯ", UDim2.fromOffset(200, 20), UDim2.fromOffset(16, 88), P.warm, 13)
	head.TextXAlignment = Enum.TextXAlignment.Left
	taskRows(lobbyCard, p.tasks, 112, 310)
end

-- итоги раунда
local summaryCard = frame(gui, UDim2.fromOffset(460, 440), UDim2.new(0.5, -230, 0.5, -220), Color3.fromRGB(14, 20, 34), 0.05)
local summaryStroke = Instance.new("UIStroke")
summaryStroke.Color = P.warm
summaryStroke.Thickness = 2
summaryStroke.Parent = summaryCard
summaryCard.Visible = false
local summaryUntil = 0

local function showSummary(sm)
	clear(summaryCard)
	summaryCard.Visible = true
	summaryUntil = os.clock() + (sm.nextRoundIn or 15)
	local y = 12
	label(summaryCard, string.format("+%d ОПЫТА", sm.gained), UDim2.fromOffset(430, 40), UDim2.fromOffset(15, y), GOLD, 30)
	y += 44
	for _, line in sm.lines do
		local l = label(summaryCard, line, UDim2.fromOffset(420, 20), UDim2.fromOffset(20, y), Color3.fromRGB(223, 230, 242), 14)
		l.TextXAlignment = Enum.TextXAlignment.Left
		l.Font = Enum.Font.Gotham
		y += 20
	end
	y += 6
	local lv = label(summaryCard, string.format("%s · уровень %d", sm.title, sm.level), UDim2.fromOffset(420, 22), UDim2.fromOffset(20, y), P.warm, 16)
	lv.TextXAlignment = Enum.TextXAlignment.Left
	y += 26
	bar(summaryCard, UDim2.fromOffset(20, y), 420, sm.xp / math.max(1, sm.xpNext))
	y += 20
	for _, u in sm.unlocked do
		local l = label(summaryCard, "★ " .. u, UDim2.fromOffset(420, 22), UDim2.fromOffset(20, y), GOLD, 15)
		l.TextXAlignment = Enum.TextXAlignment.Left
		y += 22
	end
	if sm.page then
		local paper = frame(summaryCard, UDim2.fromOffset(420, 70), UDim2.fromOffset(20, y + 4), P.paper, 0)
		local t = label(paper, string.format("Досье %d/%d: %s", sm.page.index, sm.page.total, sm.page.text), UDim2.new(1, -16, 1, -8), UDim2.fromOffset(8, 4), Color3.fromRGB(43, 58, 92), 13)
		t.Font = Enum.Font.Gotham
		t.TextXAlignment = Enum.TextXAlignment.Left
		y += 80
	end
	y = taskRows(summaryCard, sm.tasks, y + 4, 420)
	-- что ждёт дальше: причина сыграть ещё и вернуться завтра
	local nextBits = {}
	if sm.roundsToPage then
		table.insert(nextBits, string.format("Новая страница досье через %d раунд(а)", sm.roundsToPage))
	end
	if sm.nextDayReward then
		table.insert(nextBits, string.format("День экспедиции %d: %s", sm.nextDayReward.day, sm.nextDayReward.name))
	end
	local nx = label(summaryCard, table.concat(nextBits, "\n"), UDim2.fromOffset(420, 40), UDim2.fromOffset(20, y + 4), P.ice, 13)
	nx.TextXAlignment = Enum.TextXAlignment.Left
	nx.Font = Enum.Font.Gotham
end

-- подсказки новичкам: одна короткая строка, без стены текста
local hint = frame(gui, UDim2.fromOffset(560, 40), UDim2.new(0.5, -280, 0, 156), Color3.fromRGB(10, 14, 24), 0.25)
local hintText = label(hint, "", UDim2.new(1, -16, 1, 0), UDim2.fromOffset(8, 0), Color3.fromRGB(255, 230, 170), 15)
hint.Visible = false

local function renderHint()
	if not snap or not snap.newbie or snap.phase == "lobby" or snap.phase == "ended" then
		hint.Visible = false
		return
	end
	local mine = myState()
	local text = ""
	if snap.phase == "day" then
		text = "Подойди к прибору (у мачты или в приборной) и запиши показание в журнал"
	elseif snap.phase == "night" then
		if mine and mine.role == "guest" then
			text = "Ты Гость: способности слева. Действуй, когда рядом никого"
		elseif snap.knock then
			text = "Стучат! Проверь глазок. Открыть = держать кнопку 3 секунды"
		else
			text = "Держи печь и лампу. Дверь без проверки не открывай"
		end
	elseif snap.phase == "discuss" then
		text = "Сравните журнал: чьи записи не сходятся?"
	elseif snap.phase == "vote" then
		text = "Выбери, кого запереть. Не уверен — пропусти"
	end
	hintText.Text = text
	hint.Visible = text ~= ""
end


local phaseNames = {
	intro = "НАЧАЛО",
	day = "ДЕНЬ",
	night = "НОЧЬ",
	discuss = "СОВЕТ",
	vote = "ГОЛОСОВАНИЕ",
	ended = "КОНЕЦ",
}

local function render()
	if not snap then
		return
	end
	if snap.phase == "lobby" then
		phaseLabel.Text = if snap.countdown
			then string.format("Старт через %d", snap.countdown)
			else string.format("Ждём игроков: %d/%d", snap.players, snap.need)
		heatBox.Visible, doorPanel.Visible, knockBox.Visible = false, false, false
		guestPanel.Visible, journalBtn.Visible = false, false
		journal.Visible = false
		renderLobbyCard(snap.progress)
		renderHint()
		return
	end
	lobbyCard.Visible = false
	if summaryCard.Visible and snap.phase == "intro" then
		summaryCard.Visible = false
	end
	renderHint()
	heatBox.Visible, journalBtn.Visible = true, true
	phaseLabel.Text = string.format("%s %d/%d · %d", phaseNames[snap.phase] or snap.phase, snap.night, snap.nights, snap.phaseLeft)
	heatFill.Size = UDim2.fromScale(math.clamp(snap.heat / 100, 0, 1), 1)
	heatFill.BackgroundColor3 = if snap.heat < Config.HeatSlowBelow then P.danger else Color3.fromRGB(255, 154, 58)
	coalLabel.Text = string.format("уголь: %d", snap.coal)

	-- стук
	if snap.knock then
		knockBox.Visible = true
		knockText.Text = string.format("ТУК · ТУК · ТУК · ТУК\n«%s»: это я, откройте!", nameOf(snap.knock.name))
	else
		knockBox.Visible = false
	end

	-- кнопки двери: ночью, если ты внутри и рядом с дверью
	local mine = myState()
	local station = workspace:FindFirstChild("Station")
	local door = station and station:FindFirstChild("Door") :: BasePart?
	local root = me.Character and me.Character:FindFirstChild("HumanoidRootPart") :: BasePart?
	local nearDoor = door and root and (door.Position - root.Position).Magnitude < 14
	doorPanel.Visible = snap.phase == "night" and mine ~= nil and mine.status == "inside" and nearDoor and true or false
	local someoneOpening = snap.opening and snap.opening.by ~= me.UserId
	dragBtn.Visible = someoneOpening and true or false
	peepBtn.Visible = snap.knock ~= nil

	-- журнал и панель Гостя перестраиваем, только когда в них что-то изменилось
	local key = string.format("%s|%d|%s|%s", snap.phase, #snap.journal, tostring(snap.points), tostring(snap.blizzardUsed))
	for _, e in snap.journal do
		key ..= e.value
	end
	if key ~= lastKey then
		lastKey = key
		renderJournal()
		renderGuest()
	end
	formHint.Text = if snap.phase == "day"
		then "Пиши то, что видишь. Даже если страшно."
		else "Записывать можно только днём."
end


-- ---------- сеть ----------
StateRemote.OnClientEvent:Connect(function(s)
	snap = s
	render()
end)

EventRemote.OnClientEvent:Connect(function(e)
	local t = e.type
	if t == "phase" then
		if e.phase == "day" then
			showBanner(string.format("ДЕНЬ %d. Сними показания приборов и запиши в журнал.", e.night), P.warm)
		elseif e.phase == "night" then
			showBanner("НОЧЬ. Дверь не открывать.", P.ice)
		elseif e.phase == "discuss" then
			showBanner("УТРО. Совет станции: кто врёт в журнале?", P.warm)
			journal.Visible = true
		elseif e.phase == "vote" then
			journal.Visible = false
			openPicker("vote", "Кого запереть в кладовке?")
		end
	elseif t == "nightTask" then
		showBanner("Ты на ночном замере. Сделай замер у мачты и постучи в дверь.", P.ice, 6)
	elseif t == "reading" then
		lastReading = { instrument = e.instrument, value = e.value }
		chosenInstrument = e.instrument
		valueBox.Text = e.value
		journal.Visible = true
		showBanner(string.format("%s: %s", Config.InstrumentNames[e.instrument], e.value), P.warm, 3)
	elseif t == "openJournal" then
		journal.Visible = true
	elseif t == "peep" then
		showBanner(if e.human then "В глазке силуэт. Похоже на человека." else "В глазке метель… что-то не так.", P.ice, 4)
	elseif t == "breach" then
		showBanner(string.format("%s открыл дверь. Это был не человек.", nameOf(e.by)), P.danger, 5)
	elseif t == "letIn" then
		showBanner(string.format("%s впустил %s.", nameOf(e.by), nameOf(e.id)), P.warm, 3)
	elseif t == "frozen" then
		showBanner(string.format("%s замёрз: %s", nameOf(e.id), e.why), P.ice, 4)
	elseif t == "locked" then
		if e.id == 0 then
			showBanner("Никого не заперли.", P.warm)
		else
			showBanner(string.format("%s заперт. Это был %s.", nameOf(e.id), if e.role == "guest" then "ГОСТЬ" else "метеоролог"),
				if e.role == "guest" then P.danger else P.ice, 5)
		end
	elseif t == "dragged" then
		showBanner(string.format("%s оттащил %s от двери!", nameOf(e.by), nameOf(e.who)), P.warm, 3)
	elseif t == "ended" then
		local text = if e.winner == "met" then "ПОБЕДА МЕТЕОРОЛОГОВ" elseif e.winner == "guest" then "ПОБЕДА ГОСТЯ" else "НИЧЬЯ"
		showBanner(text .. "\n" .. (e.reason or ""), if e.winner == "guest" then P.danger else P.warm, 9)
		picker.Visible = false
	elseif t == "summary" then
		showSummary(e.summary)
	elseif t == "blizzard" then
		showBanner("Метель!", P.ice, 3)
	elseif t == "lampPenalty" then
		showBanner("Лампа в восточном окне погасла. Холодает.", P.ice, 3)
	end
end)

-- роль в начале раунда
local announcedRole = false
RunService.Heartbeat:Connect(function()
	if banner.Visible and os.clock() > bannerUntil then
		banner.Visible = false
	end
	if summaryCard.Visible and os.clock() > summaryUntil then
		summaryCard.Visible = false
	end
	renderBracelets()
	if snap and snap.phase == "intro" and not announcedRole then
		local mine = myState()
		if mine and mine.role then
			announcedRole = true
			if mine.role == "guest" then
				showBanner("Ты — ГОСТЬ. Обмани их и заставь открыть дверь.", P.danger, 8)
			else
				showBanner("Ты — метеоролог. Один из вас — не человек.", P.ice, 8)
			end
		end
	elseif snap and snap.phase ~= "intro" then
		announcedRole = false
	end
end)

local _ = lastReading
