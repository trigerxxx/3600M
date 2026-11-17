--!nonstrict
-- Прогресс игрока между раундами: уровни, задания дня, дни экспедиции, страницы досье.
-- Всё, что заставляет вернуться завтра. Описание: docs/13-retention.md

local DataStoreService = game:GetService("DataStoreService")

local Progress = {}

local store = nil
pcall(function()
	store = DataStoreService:GetDataStore("Progress_v1")
end)

-- ---------- уровни ----------
-- Первые уровни очень быстрые: первый уровень берётся за первый же раунд
function Progress.xpForLevel(level: number): number
	return math.floor(50 + 30 * (level - 1) ^ 1.35)
end

Progress.Titles = {
	{ level = 1, name = "Стажёр" },
	{ level = 5, name = "Наблюдатель" },
	{ level = 10, name = "Метеоролог" },
	{ level = 20, name = "Смотритель" },
	{ level = 35, name = "Старший станции" },
	{ level = 50, name = "Легенда 3600" },
}

-- Награды за уровни (пока названия; модели и скины появятся позже)
Progress.LevelRewards = {
	[2] = "Шарф: синий",
	[3] = "Чернила: бирюзовые",
	[5] = "Звание «Наблюдатель»",
	[7] = "Кружка с оленем",
	[10] = "Звание «Метеоролог» и шапка-ушанка",
	[15] = "Фонарь: тёплый янтарь",
	[20] = "Звание «Смотритель»",
	[25] = "Силуэт Гостя: «Иней»",
	[35] = "Звание «Старший станции»",
	[50] = "Звание «Легенда 3600»",
}

-- Награды за дни экспедиции: считаем дни, в которые игрок играл, а не дни подряд.
-- Пропуск ничего не обнуляет. Это совпадает с метрикой «игровые дни», которую ценит Roblox.
Progress.DayRewards = {
	[2] = { xp = 60, name = "Тёплые варежки" },
	[3] = { xp = 80, name = "Значок «3 дня на станции»" },
	[5] = { xp = 100, name = "Свитер с узором" },
	[7] = { xp = 150, name = "Значок «Неделя на станции»" },
	[14] = { xp = 250, name = "Тулуп смотрителя" },
	[28] = { xp = 400, name = "Значок «Месяц на станции»" },
}

-- Страницы досье станции: первая после первого раунда, дальше каждые 5 раундов
Progress.DossierEvery = 5
Progress.Dossier = {
	"1987. Станцию открыли осенью. Первый смотритель жаловался, что ночью кто-то стучит, но снег у двери всегда был нетронутым.",
	"Из журнала: «Записал −18. Утром в журнале стояло −81. Почерк мой».",
	"Правило, которое никто не помнит, кто придумал: три удара — ветер, четыре — нет.",
	"Смена из пяти человек. Утром их было шесть. Никто не смог сказать, кто лишний.",
	"Лампа в восточном окне горела всю зиму 1994 года. Говорят, иначе оно подходит ближе.",
	"Записка на обороте карты: «Оно знает наши голоса. Оно не знает наших записей».",
	"Последняя смена 2003 года ушла вниз пешком. В журнале остался ещё один день, которого никто не записывал.",
	"Чабан внизу говорит: «На 3600 всегда на одного больше, чем приехало».",
}

-- ---------- задания дня ----------
local TaskPool = {
	{ id = "journal3", text = "Сделай 3 записи в журнале", kind = "journal", target = 3, xp = 40 },
	{ id = "correct2", text = "Запиши 2 верных показания", kind = "correct", target = 2, xp = 40 },
	{ id = "coal5", text = "Подкинь уголь 5 раз", kind = "coal", target = 5, xp = 35 },
	{ id = "letin1", text = "Впусти товарища с мороза", kind = "letIn", target = 1, xp = 45 },
	{ id = "drag1", text = "Оттащи кого-нибудь от двери", kind = "drag", target = 1, xp = 45 },
	{ id = "catch1", text = "Проголосуй против Гостя", kind = "catch", target = 1, xp = 60 },
	{ id = "rounds3", text = "Сыграй 3 раунда", kind = "round", target = 3, xp = 60 },
	{ id = "win2", text = "Победи 2 раза", kind = "win", target = 2, xp = 70 },
	{ id = "friend1", text = "Сыграй раунд с другом", kind = "friend", target = 1, xp = 50 },
}

local function today(): number
	return math.floor(os.time() / 86400)
end

-- Три задания дня одинаковые для всех игроков мира: есть о чём поговорить
function Progress.tasksFor(day: number)
	local rng = Random.new(day * 7919)
	local pool = table.clone(TaskPool)
	local out = {}
	for _ = 1, 3 do
		local i = rng:NextInteger(1, #pool)
		table.insert(out, pool[i])
		table.remove(pool, i)
	end
	return out
end

-- ---------- данные ----------
local cache: { [number]: any } = {}

local function blank()
	return {
		xp = 0,
		level = 1,
		rounds = 0,
		wins = 0,
		guestWins = 0,
		playDays = 0,
		lastDay = 0,
		taskDay = 0,
		taskProgress = {},
		taskDone = {},
		dossier = 0,
		rewards = {},
	}
end

function Progress.load(player: Player)
	local data = nil
	if store then
		local ok, result = pcall(function()
			return store:GetAsync("p_" .. player.UserId)
		end)
		if ok then
			data = result
		end
	end
	local d = blank()
	if typeof(data) == "table" then
		for k, v in data do
			d[k] = v
		end
	end
	cache[player.UserId] = d
	return d
end

function Progress.get(player: Player)
	return cache[player.UserId]
end

function Progress.save(player: Player)
	local d = cache[player.UserId]
	if not d or not store then
		return
	end
	pcall(function()
		store:UpdateAsync("p_" .. player.UserId, function()
			return d
		end)
	end)
end

function Progress.release(player: Player)
	Progress.save(player)
	cache[player.UserId] = nil
end

-- ---------- начисления ----------
local function titleFor(level: number): string
	local name = Progress.Titles[1].name
	for _, t in Progress.Titles do
		if level >= t.level then
			name = t.name
		end
	end
	return name
end

-- Возвращает список новых наград уровня
local function addXp(d, amount: number): { string }
	local unlocked = {}
	d.xp += amount
	while d.xp >= Progress.xpForLevel(d.level) do
		d.xp -= Progress.xpForLevel(d.level)
		d.level += 1
		local reward = Progress.LevelRewards[d.level]
		table.insert(unlocked, string.format("Уровень %d%s", d.level, if reward then ": " .. reward else ""))
		if reward then
			table.insert(d.rewards, reward)
		end
	end
	return unlocked
end

local function refreshDay(d)
	local t = today()
	if d.taskDay ~= t then
		d.taskDay = t
		d.taskProgress = {}
		d.taskDone = {}
	end
end

-- Событие для заданий дня: kind из TaskPool, amount обычно 1
function Progress.event(player: Player, kind: string, amount: number?)
	local d = cache[player.UserId]
	if not d then
		return
	end
	refreshDay(d)
	for _, task in Progress.tasksFor(d.taskDay) do
		if task.kind == kind and not d.taskDone[task.id] then
			d.taskProgress[task.id] = (d.taskProgress[task.id] or 0) + (amount or 1)
		end
	end
end

-- Итог раунда для игрока. result = { won, wasGuest, survived, correctEntries, withFriend }
function Progress.finishRound(player: Player, result)
	local d = cache[player.UserId]
	if not d then
		return nil
	end
	refreshDay(d)
	local lines = {}
	local gained = 0
	local unlocked = {}

	local function give(amount: number, why: string)
		gained += amount
		table.insert(lines, string.format("+%d  %s", amount, why))
		for _, u in addXp(d, amount) do
			table.insert(unlocked, u)
		end
	end

	give(40, "Смена отработана")
	if result.won then
		give(if result.wasGuest then 60 else 40, if result.wasGuest then "Победа за Гостя" else "Победа")
		d.wins += 1
		if result.wasGuest then
			d.guestWins += 1
		end
	end
	if result.survived and not result.wasGuest then
		give(10, "Дожил до конца")
	end
	if (result.correctEntries or 0) > 0 then
		give(5 * math.min(result.correctEntries, 6), "Верные записи в журнале")
	end
	if result.withFriend then
		give(20, "Смена с другом")
	end

	d.rounds += 1
	Progress.event(player, "round", 1)
	if result.won then
		Progress.event(player, "win", 1)
	end
	if result.withFriend then
		Progress.event(player, "friend", 1)
	end

	-- задания дня
	local tasks = {}
	for _, task in Progress.tasksFor(d.taskDay) do
		local prog = d.taskProgress[task.id] or 0
		if prog >= task.target and not d.taskDone[task.id] then
			d.taskDone[task.id] = true
			give(task.xp, "Задание: " .. task.text)
		end
		table.insert(tasks, {
			text = task.text,
			progress = math.min(prog, task.target),
			target = task.target,
			done = d.taskDone[task.id] == true,
		})
	end

	-- дни экспедиции
	local t = today()
	local newDay = false
	if d.lastDay ~= t then
		d.lastDay = t
		d.playDays += 1
		newDay = true
		local reward = Progress.DayRewards[d.playDays]
		if reward then
			table.insert(d.rewards, reward.name)
			table.insert(unlocked, string.format("День экспедиции %d: %s", d.playDays, reward.name))
			give(reward.xp, "День экспедиции " .. d.playDays)
		end
	end

	-- досье
	local page = nil
	-- первая страница открывается сразу после первого раунда, дальше каждые DossierEvery раундов
	local wantPages = math.min(#Progress.Dossier, math.floor((d.rounds + Progress.DossierEvery - 1) / Progress.DossierEvery))
	if wantPages > d.dossier then
		d.dossier = wantPages
		page = { index = wantPages, total = #Progress.Dossier, text = Progress.Dossier[wantPages] }
	end

	Progress.save(player)
	return {
		gained = gained,
		lines = lines,
		unlocked = unlocked,
		level = d.level,
		xp = d.xp,
		xpNext = Progress.xpForLevel(d.level),
		title = titleFor(d.level),
		tasks = tasks,
		playDays = d.playDays,
		newDay = newDay,
		nextDayReward = (function()
			for day = d.playDays + 1, d.playDays + 30 do
				if Progress.DayRewards[day] then
					return { day = day, name = Progress.DayRewards[day].name }
				end
			end
			return nil
		end)(),
		roundsToPage = if d.dossier < #Progress.Dossier
			then (d.dossier * Progress.DossierEvery + 1) - d.rounds
			else nil,
		page = page,
	}
end

-- Короткая сводка для лобби
function Progress.summary(player: Player)
	local d = cache[player.UserId]
	if not d then
		return nil
	end
	refreshDay(d)
	local tasks = {}
	for _, task in Progress.tasksFor(d.taskDay) do
		table.insert(tasks, {
			text = task.text,
			progress = math.min(d.taskProgress[task.id] or 0, task.target),
			target = task.target,
			done = d.taskDone[task.id] == true,
		})
	end
	return {
		level = d.level,
		xp = d.xp,
		xpNext = Progress.xpForLevel(d.level),
		title = titleFor(d.level),
		rounds = d.rounds,
		playDays = d.playDays,
		tasks = tasks,
		dossier = d.dossier,
		newbie = d.rounds < 2,
	}
end

return Progress
