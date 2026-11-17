--!nonstrict
-- Сервер прототипа: лобби, запуск раунда, связь правил (Round) с картой и игроками.

local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local RunService = game:GetService("RunService")
local Lighting = game:GetService("Lighting")

local Shared = ReplicatedStorage:WaitForChild("Shared")
local Config = require(Shared.Config)
local Round = require(Shared.Round)
local Map = require(script.Parent.Map)

-- ---------- сеть ----------
local net = Instance.new("Folder")
net.Name = "Net"
local actionRemote = Instance.new("RemoteEvent")
actionRemote.Name = "Action" -- клиент → сервер
actionRemote.Parent = net
local stateRemote = Instance.new("RemoteEvent")
stateRemote.Name = "State" -- сервер → клиент: снимок раунда
stateRemote.Parent = net
local eventRemote = Instance.new("RemoteEvent")
eventRemote.Name = "Event" -- сервер → клиент: разовые события
eventRemote.Parent = net
net.Parent = ReplicatedStorage

local built = Map.build()
local atmosphere = Instance.new("Atmosphere")
atmosphere.Parent = Lighting

-- ---------- состояние сервера ----------
local mode: "lobby" | "round" = "lobby"
local countdown = Config.LobbyCountdown
local round: Round.State? = nil
local lastPhase = ""

local function lobbyPlayers(): { Player }
	local list = {}
	for _, plr in Players:GetPlayers() do
		table.insert(list, plr)
	end
	return list
end

local function teleport(plr: Player, pos: Vector3)
	local char = plr.Character
	local root = char and char:FindFirstChild("HumanoidRootPart") :: BasePart?
	if root then
		local offset = Vector3.new(math.random(-3, 3), 0, math.random(-3, 3))
		root.CFrame = CFrame.new(pos + offset)
	end
end

local function playerById(id: number): Player?
	return Players:GetPlayerByUserId(id)
end

local function sendLobby()
	for _, plr in Players:GetPlayers() do
		stateRemote:FireClient(plr, {
			phase = "lobby",
			players = #Players:GetPlayers(),
			need = Config.MinPlayers,
			countdown = if #Players:GetPlayers() >= Config.MinPlayers then math.ceil(countdown) else nil,
		})
	end
end

-- Где должен стоять игрок после смены фазы
local function placeAll(s: Round.State)
	for id, p in s.players do
		local plr = playerById(id)
		if plr then
			if p.status == "locked" or p.status == "frozen" then
				teleport(plr, built.spots.cold)
			elseif s.phase == "discuss" or s.phase == "vote" then
				teleport(plr, built.spots.table)
			elseif s.phase == "night" then
				if p.nightTask then
					teleport(plr, built.spots.mast)
				else
					teleport(plr, built.spots.inside)
				end
			elseif s.phase == "intro" then
				teleport(plr, built.spots.inside)
			end
		end
	end
end

local function applyWorld(s: Round.State)
	local isNight = s.phase == "night"
	Lighting.ClockTime = if isNight or s.phase == "discuss" or s.phase == "vote" then 0.5 else 13
	Lighting.Brightness = if isNight then 0.5 else 2
	Lighting.Ambient = if isNight then Color3.fromRGB(20, 25, 40) else Color3.fromRGB(110, 115, 130)
	local dark = s.lightsOffUntil > s.clock
	for _, light in built.lights do
		light.Enabled = not dark
	end
	built.lamp.Enabled = s.lampOutSince == nil and not dark
	built.eastLamp.Material = if built.lamp.Enabled then Enum.Material.Neon else Enum.Material.SmoothPlastic
	atmosphere.Density = if s.blizzardUntil > s.clock then 0.75 else (if isNight then 0.4 else 0.25)
	Map.setDoorClosed(built, isNight)
	built.prompts.nightMeasure.Enabled = isNight
	built.prompts.knock.Enabled = isNight

	-- холод замедляет
	local speed = if s.heat < Config.HeatSlowBelow then 10 else 16
	for id, p in s.players do
		local plr = playerById(id)
		local hum = plr and plr.Character and plr.Character:FindFirstChildOfClass("Humanoid")
		if hum then
			hum.WalkSpeed = if p.status == "locked" or p.status == "frozen" then 8 else speed
		end
	end
end

local function sendEvents(s: Round.State)
	for _, e in s.events do
		if e.type == "nightTask" then
			local plr = playerById(e.id)
			if plr then
				eventRemote:FireClient(plr, e)
			end
		else
			eventRemote:FireAllClients(e)
		end
		if e.type == "letIn" then
			local plr = playerById(e.id)
			if plr then
				teleport(plr, built.spots.doorInside)
			end
		elseif e.type == "frozen" or e.type == "locked" then
			local plr = playerById(e.id)
			if plr then
				teleport(plr, built.spots.cold)
			end
		end
	end
	table.clear(s.events)
end

local function startRound()
	local list = {}
	for i, plr in lobbyPlayers() do
		if i > Config.MaxPlayers then
			break
		end
		table.insert(list, { id = plr.UserId, name = plr.DisplayName })
	end
	round = Round.new(list)
	mode = "round"
	lastPhase = ""
end

local function endRound()
	round = nil
	mode = "lobby"
	countdown = Config.LobbyCountdown
	Lighting.ClockTime = 13
	Map.setDoorClosed(built, false)
	for _, plr in Players:GetPlayers() do
		teleport(plr, built.spots.lobby)
		local hum = plr.Character and plr.Character:FindFirstChildOfClass("Humanoid")
		if hum then
			hum.WalkSpeed = 16
		end
	end
end

-- ---------- подсказки на карте ----------
local function onPrompt(key: string, plr: Player)
	local s = round
	if not s then
		return
	end
	local id = plr.UserId
	if key == "coal" then
		Round.loadCoal(s, id)
	elseif key == "lamp" then
		Round.relightLamp(s, id)
	elseif key == "generator" then
		Round.fixGenerator(s, id)
	elseif key == "nightMeasure" then
		Round.nightMeasure(s, id)
	elseif key == "knock" then
		Round.knockReal(s, id)
	elseif key == "journal" then
		eventRemote:FireClient(plr, { type = "openJournal" })
	elseif key == "temp" or key == "wind" or key == "pressure" or key == "snow" then
		local value = Round.readInstrument(s, id, key)
		if value then
			eventRemote:FireClient(plr, { type = "reading", instrument = key, value = value })
		end
	end
end

for key, pp in built.prompts do
	pp.Triggered:Connect(function(plr)
		onPrompt(key, plr)
	end)
end

-- ---------- действия из интерфейса ----------
local lastAction: { [number]: number } = {}

actionRemote.OnServerEvent:Connect(function(plr: Player, action: any, arg: any)
	local s = round
	if not s or typeof(action) ~= "string" then
		return
	end
	-- простая защита от спама
	local now = os.clock()
	if lastAction[plr.UserId] and now - lastAction[plr.UserId] < 0.1 then
		return
	end
	lastAction[plr.UserId] = now
	local id = plr.UserId

	if action == "write" and typeof(arg) == "table" then
		if typeof(arg.instrument) == "string" and typeof(arg.value) == "string" then
			Round.writeJournal(s, id, arg.instrument, arg.value)
		end
	elseif action == "beginOpen" then
		Round.beginOpen(s, id)
	elseif action == "cancelOpen" then
		Round.cancelOpen(s, id)
	elseif action == "drag" then
		Round.drag(s, id)
	elseif action == "peep" then
		local human = Round.peephole(s, id)
		if human ~= nil then
			eventRemote:FireClient(plr, { type = "peep", human = human })
		end
	elseif action == "ability" and typeof(arg) == "table" and typeof(arg.name) == "string" then
		Round.useAbility(s, id, arg.name, arg.arg)
	elseif action == "vote" and typeof(arg) == "number" then
		Round.vote(s, id, arg)
	end
end)

-- ---------- игроки ----------
Players.PlayerAdded:Connect(function(plr)
	plr.CharacterAdded:Connect(function()
		task.wait(0.2)
		local s = round
		if s and s.players[plr.UserId] then
			placeAll(s)
		else
			teleport(plr, built.spots.lobby)
		end
	end)
end)

Players.PlayerRemoving:Connect(function(plr)
	lastAction[plr.UserId] = nil
	local s = round
	if s then
		Round.removePlayer(s, plr.UserId)
	end
end)

-- ---------- главный цикл ----------
local sendTimer = 0

RunService.Heartbeat:Connect(function(dt)
	sendTimer += dt
	local shouldSend = sendTimer >= 0.25
	if shouldSend then
		sendTimer = 0
	end

	if mode == "lobby" then
		if #Players:GetPlayers() >= Config.MinPlayers then
			countdown -= dt
			if countdown <= 0 then
				startRound()
			end
		else
			countdown = Config.LobbyCountdown
		end
		if shouldSend then
			sendLobby()
		end
		return
	end

	local s = round
	if not s then
		return
	end
	Round.step(s, dt)

	if s.phase ~= lastPhase then
		lastPhase = s.phase
		placeAll(s)
	end
	applyWorld(s)
	sendEvents(s)

	if s.phase == "ended" and s.phaseLeft <= 0 then
		endRound()
		return
	end

	if shouldSend then
		for _, plr in Players:GetPlayers() do
			stateRemote:FireClient(plr, Round.snapshotFor(s, plr.UserId))
		end
	end
end)
