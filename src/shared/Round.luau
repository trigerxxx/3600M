--!nonstrict
-- Логика одного раунда режима «Один из нас стучит».
-- Здесь нет ничего от Roblox, кроме Config: только правила. Сервер вызывает эти функции
-- и рассылает игрокам результат. Так правила можно переиспользовать в следующих играх
-- и проверять отдельно от карты и интерфейса.

local Config = require(script.Parent.Config)

export type PlayerState = {
	id: number,
	name: string,
	role: "met" | "guest",
	status: "inside" | "outside" | "locked" | "frozen",
	ink: number,
	wroteToday: boolean,
	nightTask: boolean,
	outsideSince: number?,
}

export type Entry = {
	author: number,
	day: number,
	instrument: string,
	value: string,
	forged: boolean,
	correct: boolean,
}

export type Knock = {
	real: boolean,
	name: number, -- от чьего имени стучат
	at: number,
}

export type Event = { [string]: any }

local Round = {}

-- ---------- создание ----------

local function shuffle<T>(list: { T }, rng: Random): { T }
	for i = #list, 2, -1 do
		local j = rng:NextInteger(1, i)
		list[i], list[j] = list[j], list[i]
	end
	return list
end

function Round.new(players: { { id: number, name: string } }, seed: number?)
	local rng = Random.new(seed or os.clock() * 1000)
	local n = #players
	local order = {}
	for i = 1, n do
		order[i] = i
	end
	shuffle(order, rng)

	local guests = Config.GuestsFor(n)
	local state = {
		rng = rng,
		clock = 0,
		phase = "intro",
		phaseLeft = Config.Phase.intro,
		night = 0,
		nights = Config.NightsFor(n),
		players = {} :: { [number]: PlayerState },
		order = {} :: { number },
		heat = Config.HeatStart,
		coal = Config.CoalStart,
		frozenFor = 0,
		lampOutSince = nil :: number?,
		lightsOffUntil = 0,
		blizzardUntil = 0,
		blizzardUsed = false,
		truth = {} :: { [string]: string },
		journal = {} :: { Entry },
		knock = nil :: Knock?,
		opening = nil :: { by: number, held: number }?,
		points = {} :: { [number]: number },
		bracelet = {} :: { [number]: number },
		votes = {} :: { [number]: number },
		prints = {} :: { { from: string } },
		events = {} :: { Event },
		winner = nil :: string?,
		reason = nil :: string?,
	}

	for rank, idx in order do
		local p = players[idx]
		state.players[p.id] = {
			id = p.id,
			name = p.name,
			role = if rank <= guests then "guest" else "met",
			status = "inside",
			ink = rank,
			wroteToday = false,
			nightTask = false,
			outsideSince = nil,
		}
		table.insert(state.order, p.id)
	end
	table.sort(state.order)
	return state
end

export type State = typeof(Round.new({}))

-- ---------- помощники ----------

local function emit(s: State, e: Event)
	table.insert(s.events, e)
end

local function alive(p: PlayerState): boolean
	return p.status == "inside" or p.status == "outside"
end

function Round.alivePlayers(s: State, role: string?): { PlayerState }
	local out = {}
	for _, id in s.order do
		local p = s.players[id]
		if alive(p) and (role == nil or p.role == role) then
			table.insert(out, p)
		end
	end
	return out
end

local function addHeat(s: State, delta: number)
	s.heat = math.clamp(s.heat + delta, 0, Config.HeatMax)
end

local function rollTruth(s: State)
	local rng = s.rng
	s.truth = {
		temp = tostring(-rng:NextInteger(5, 30)) .. "°",
		wind = Config.WindDirs[rng:NextInteger(1, #Config.WindDirs)],
		pressure = tostring(rng:NextInteger(600, 660)),
		snow = tostring(rng:NextInteger(2, 12) * 10) .. " см",
	}
end

-- Неправильное значение того же прибора (для подделки)
local function wrongValue(s: State, instrument: string, current: string): string
	for _ = 1, 10 do
		local saved = s.truth
		rollTruth(s)
		local v = s.truth[instrument]
		s.truth = saved
		if v ~= current then
			return v
		end
	end
	return current
end

local function checkWin(s: State)
	if s.winner then
		return
	end
	local mets = #Round.alivePlayers(s, "met")
	local guests = #Round.alivePlayers(s, "guest")
	if guests == 0 then
		s.winner, s.reason = "met", "Все Гости заперты"
	elseif mets <= guests then
		s.winner, s.reason = "guest", "Метеорологов не осталось"
	elseif s.frozenFor >= Config.FreezeSeconds then
		s.winner, s.reason = "guest", "Станция замёрзла"
	end
	if s.winner then
		s.phase, s.phaseLeft = "ended", Config.Phase.ended
		emit(s, { type = "ended", winner = s.winner, reason = s.reason })
	end
end

local function freeze(s: State, p: PlayerState, why: string)
	p.status = "frozen"
	p.outsideSince = nil
	emit(s, { type = "frozen", id = p.id, why = why })
	checkWin(s)
end

-- ---------- фазы ----------

local function startDay(s: State)
	s.phase, s.phaseLeft = "day", Config.Phase.day
	s.night += 1
	rollTruth(s)
	for _, p in s.players do
		p.wroteToday = false
		p.nightTask = false
	end
	s.prints = {}
	emit(s, { type = "phase", phase = "day", night = s.night })
end

local function startNight(s: State)
	s.phase, s.phaseLeft = "night", Config.Phase.night
	s.votes = {}
	for _, g in Round.alivePlayers(s, "guest") do
		s.points[g.id] = Config.ColdPointsFor(#s.order)
	end
	-- один случайный метеоролог идёт на ночной замер
	local mets = Round.alivePlayers(s, "met")
	if #mets > 0 then
		local chosen = mets[s.rng:NextInteger(1, #mets)]
		chosen.nightTask = true
		emit(s, { type = "nightTask", id = chosen.id })
	end
	emit(s, { type = "phase", phase = "night", night = s.night })
end

local function startDiscuss(s: State)
	s.phase, s.phaseLeft = "discuss", Config.Phase.discuss
	s.knock, s.opening = nil, nil
	s.points = {}
	-- кто остался снаружи на рассвете, замерзает
	for _, p in s.players do
		if p.status == "outside" then
			freeze(s, p, "Остался снаружи до рассвета")
		end
	end
	emit(s, { type = "phase", phase = "discuss", night = s.night })
end

local function startVote(s: State)
	s.phase, s.phaseLeft = "vote", Config.Phase.vote
	s.votes = {}
	emit(s, { type = "phase", phase = "vote", night = s.night })
end

local function finishVote(s: State)
	local alivePlayers = Round.alivePlayers(s)
	local counts: { [number]: number } = {}
	for voter, target in s.votes do
		local v = s.players[voter]
		if v and alive(v) and target ~= 0 then
			counts[target] = (counts[target] or 0) + 1
		end
	end
	local need = math.floor(#alivePlayers / 2) + 1
	local lockedId = nil
	for target, c in counts do
		if c >= need then
			lockedId = target
		end
	end
	if lockedId then
		local p = s.players[lockedId]
		p.status = "locked"
		emit(s, { type = "locked", id = p.id, role = p.role })
	else
		emit(s, { type = "locked", id = 0 })
	end
	checkWin(s)
	if s.winner then
		return
	end
	if s.night >= s.nights then
		s.winner, s.reason = "met", "Станция дожила до последнего рассвета"
		s.phase, s.phaseLeft = "ended", Config.Phase.ended
		emit(s, { type = "ended", winner = s.winner, reason = s.reason })
	else
		startDay(s)
	end
end

local function nextPhase(s: State)
	if s.phase == "intro" then
		startDay(s)
	elseif s.phase == "day" then
		startNight(s)
	elseif s.phase == "night" then
		startDiscuss(s)
	elseif s.phase == "discuss" then
		startVote(s)
	elseif s.phase == "vote" then
		finishVote(s)
	end
end

-- Вызывать каждый кадр сервера
function Round.step(s: State, dt: number)
	if s.phase == "ended" then
		s.phaseLeft -= dt
		return
	end
	s.clock += dt

	-- тепло
	if s.phase == "day" or s.phase == "night" then
		addHeat(s, -(if s.phase == "night" then Config.HeatDrainNight else Config.HeatDrainDay) * dt)
	end
	if s.heat <= 0 then
		s.frozenFor += dt
	else
		s.frozenFor = 0
	end

	-- погасшая лампа в восточном окне
	if s.lampOutSince and s.clock - s.lampOutSince >= Config.LampRelightSeconds then
		s.lampOutSince = nil
		addHeat(s, -Config.LampHeatLoss)
		emit(s, { type = "lampPenalty" })
	end

	-- кто ждёт снаружи слишком долго
	for _, p in s.players do
		if p.status == "outside" and p.outsideSince and s.clock - p.outsideSince >= Config.OutsideFreezeSeconds then
			freeze(s, p, "Не впустили")
		end
	end

	-- открытие двери
	if s.opening then
		s.opening.held += dt
		if s.opening.held >= Config.DoorHold then
			Round.resolveDoor(s, s.opening.by)
		end
	end

	checkWin(s)
	if s.winner then
		return
	end

	s.phaseLeft -= dt
	if s.phaseLeft <= 0 then
		nextPhase(s)
	end
end

-- ---------- задания ----------

-- Снять показание прибора. Возвращает значение, которое видит игрок.
function Round.readInstrument(s: State, id: number, instrument: string): string?
	local p = s.players[id]
	if not p or not alive(p) or s.phase ~= "day" then
		return nil
	end
	return s.truth[instrument]
end

function Round.writeJournal(s: State, id: number, instrument: string, value: string): boolean
	local p = s.players[id]
	if not p or not alive(p) or s.phase ~= "day" or s.truth[instrument] == nil then
		return false
	end
	value = string.sub(value, 1, 16)
	table.insert(s.journal, {
		author = id,
		day = s.night,
		instrument = instrument,
		value = value,
		forged = false,
		correct = value == s.truth[instrument],
	})
	p.wroteToday = true
	emit(s, { type = "journal" })
	return true
end

function Round.loadCoal(s: State, id: number): boolean
	local p = s.players[id]
	if not p or not alive(p) or s.coal <= 0 then
		return false
	end
	s.coal -= 1
	addHeat(s, Config.CoalPerLoad)
	return true
end

function Round.relightLamp(s: State, id: number): boolean
	local p = s.players[id]
	if not p or not alive(p) or not s.lampOutSince then
		return false
	end
	s.lampOutSince = nil
	emit(s, { type = "lamp", lit = true })
	return true
end

-- Генератор возвращает свет, погашенный Гостем или метелью у двери
function Round.fixGenerator(s: State, id: number): boolean
	local p = s.players[id]
	if not p or not alive(p) or s.lightsOffUntil <= s.clock then
		return false
	end
	s.lightsOffUntil = s.clock
	emit(s, { type = "lights" })
	return true
end

-- Ночной замер на мачте: игрок оказывается снаружи и должен постучать
function Round.nightMeasure(s: State, id: number): boolean
	local p = s.players[id]
	if not p or p.status ~= "inside" or not p.nightTask or s.phase ~= "night" then
		return false
	end
	p.nightTask = false
	p.status = "outside"
	p.outsideSince = s.clock
	emit(s, { type = "outside", id = id })
	return true
end

-- ---------- дверь ----------

function Round.knockReal(s: State, id: number): boolean
	local p = s.players[id]
	if not p or p.status ~= "outside" then
		return false
	end
	s.knock = { real = true, name = id, at = s.clock }
	emit(s, { type = "knock", name = id })
	return true
end

function Round.beginOpen(s: State, id: number): boolean
	local p = s.players[id]
	if not p or p.status ~= "inside" or s.opening then
		return false
	end
	s.opening = { by = id, held = 0 }
	emit(s, { type = "opening", by = id })
	return true
end

function Round.cancelOpen(s: State, id: number)
	if s.opening and s.opening.by == id then
		s.opening = nil
		emit(s, { type = "openingStopped" })
	end
end

function Round.drag(s: State, id: number): boolean
	local p = s.players[id]
	if not p or p.status ~= "inside" or not s.opening or s.opening.by == id then
		return false
	end
	emit(s, { type = "dragged", by = id, who = s.opening.by })
	s.opening = nil
	return true
end

function Round.resolveDoor(s: State, openerId: number)
	s.opening = nil
	local opener = s.players[openerId]
	local knock = s.knock
	s.knock = nil
	if knock and knock.real then
		local outside = s.players[knock.name]
		if outside and outside.status == "outside" then
			outside.status = "inside"
			outside.outsideSince = nil
			emit(s, { type = "letIn", id = outside.id, by = openerId })
		end
	elseif knock and not knock.real then
		addHeat(s, -Config.FakeKnockHeatLoss)
		s.lightsOffUntil = s.clock + Config.FakeKnockDarkSeconds
		emit(s, { type = "breach", by = openerId })
		if opener and alive(opener) then
			freeze(s, opener, "Открыл не тому")
		end
	else
		addHeat(s, -Config.EmptyDoorHeatLoss)
		emit(s, { type = "emptyDoor", by = openerId })
	end
	-- если снаружи кто-то ещё, он заходит, раз дверь всё равно открыли
	for _, p in s.players do
		if p.status == "outside" then
			p.status = "inside"
			p.outsideSince = nil
			emit(s, { type = "letIn", id = p.id, by = openerId })
		end
	end
	checkWin(s)
end

-- Глазок: true, если за дверью человек. С вероятностью PeepholeTruth ответ верный.
function Round.peephole(s: State, id: number): boolean?
	local p = s.players[id]
	if not p or p.status ~= "inside" or not s.knock then
		return nil
	end
	local truth = s.knock.real
	if s.rng:NextNumber() < Config.PeepholeTruth then
		return truth
	end
	return not truth
end

-- ---------- Гость ----------

local function spend(s: State, id: number, ability: string): boolean
	local p = s.players[id]
	local def = Config.Ability[ability]
	if not p or p.role ~= "guest" or not alive(p) or s.phase ~= "night" or not def then
		return false
	end
	if (s.points[id] or 0) < def.cost then
		return false
	end
	if ability == "blizzard" and s.blizzardUsed then
		return false
	end
	s.points[id] -= def.cost
	s.bracelet[id] = s.clock + Config.BraceletSeconds
	emit(s, { type = "bracelet", id = id })
	return true
end

function Round.useAbility(s: State, id: number, ability: string, arg: any): boolean
	-- проверяем цель до списания очков
	if ability == "voice" then
		local target = s.players[arg]
		if not target or s.knock then
			return false
		end
	elseif ability == "forge" then
		local entry = s.journal[arg]
		if not entry or entry.author == id then
			return false
		end
	end
	if not spend(s, id, ability) then
		return false
	end

	if ability == "voice" then
		s.knock = { real = false, name = arg, at = s.clock }
		emit(s, { type = "knock", name = arg })
	elseif ability == "forge" then
		local entry = s.journal[arg]
		entry.value = wrongValue(s, entry.instrument, entry.value)
		entry.forged = true
		entry.correct = false
		emit(s, { type = "journal" })
	elseif ability == "dark" then
		s.lightsOffUntil = s.clock + Config.Ability.dark.seconds
		s.lampOutSince = s.clock
		emit(s, { type = "dark" })
	elseif ability == "prints" then
		local posts = { "метеомачты", "сарая с генератором", "северного окна", "кладовки" }
		table.insert(s.prints, { from = posts[s.rng:NextInteger(1, #posts)] })
	elseif ability == "steal" then
		s.coal = math.max(0, s.coal - Config.Ability.steal.coal)
	elseif ability == "blizzard" then
		s.blizzardUsed = true
		s.blizzardUntil = s.clock + Config.Ability.blizzard.seconds
		emit(s, { type = "blizzard" })
	end
	return true
end

-- ---------- голосование ----------

-- target = 0 означает «пропустить»
function Round.vote(s: State, id: number, target: number): boolean
	local p = s.players[id]
	if not p or not alive(p) or s.phase ~= "vote" then
		return false
	end
	if target ~= 0 then
		local t = s.players[target]
		if not t or not alive(t) then
			return false
		end
	end
	s.votes[id] = target
	return true
end

-- ---------- выход игрока ----------

function Round.removePlayer(s: State, id: number)
	local p = s.players[id]
	if not p then
		return
	end
	p.status = "frozen"
	if s.opening and s.opening.by == id then
		s.opening = nil
	end
	emit(s, { type = "left", id = id })
	if #Round.alivePlayers(s) < 3 and not s.winner then
		s.winner, s.reason = "draw", "Слишком мало игроков"
		s.phase, s.phaseLeft = "ended", Config.Phase.ended
		emit(s, { type = "ended", winner = s.winner, reason = s.reason })
		return
	end
	checkWin(s)
end

-- ---------- итоги ----------

function Round.journalAccuracy(s: State): number
	-- верность записи проверяется в момент записи: правда меняется каждый день
	local total, good = 0, 0
	for _, e in s.journal do
		total += 1
		if e.correct then
			good += 1
		end
	end
	if total == 0 then
		return 0
	end
	return good / total
end

-- То, что можно показать конкретному игроку (без чужих ролей)
function Round.snapshotFor(s: State, viewer: number)
	local me = s.players[viewer]
	local players = {}
	for _, id in s.order do
		local p = s.players[id]
		local showRole = s.phase == "ended"
			or p.status == "locked"
			or (me ~= nil and me.role == "guest" and p.role == "guest")
			or id == viewer
		table.insert(players, {
			id = id,
			name = p.name,
			status = p.status,
			ink = p.ink,
			wroteToday = p.wroteToday,
			role = if showRole then p.role else nil,
			bracelet = (s.bracelet[id] or 0) > s.clock,
		})
	end
	local journal = {}
	for i, e in s.journal do
		journal[i] = {
			author = e.author,
			day = e.day,
			instrument = e.instrument,
			value = e.value,
			-- подделка видна всем как «чуть темнее чернила», но не подписана
			darker = e.forged,
		}
	end
	return {
		phase = s.phase,
		phaseLeft = math.max(0, math.ceil(s.phaseLeft)),
		night = s.night,
		nights = s.nights,
		heat = math.floor(s.heat),
		coal = s.coal,
		lampOut = s.lampOutSince ~= nil,
		dark = s.lightsOffUntil > s.clock,
		blizzard = s.blizzardUntil > s.clock,
		knock = if s.knock then { name = s.knock.name } else nil,
		opening = if s.opening then { by = s.opening.by, held = s.opening.held } else nil,
		players = players,
		journal = journal,
		points = if me and me.role == "guest" then (s.points[viewer] or 0) else nil,
		blizzardUsed = s.blizzardUsed,
		myVote = s.votes[viewer],
		nightTask = me ~= nil and me.nightTask,
		prints = if s.phase == "discuss" or s.phase == "vote" then s.prints else {},
		winner = s.winner,
		reason = s.reason,
	}
end

return Round
