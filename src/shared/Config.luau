--!strict
-- Все числа баланса в одном месте. Описание: docs/07-tasks-balance.md

local Config = {}

Config.MinPlayers = 4
Config.MaxPlayers = 8
Config.LobbyCountdown = 10

-- Гостей и ночей по числу игроков
function Config.GuestsFor(n: number): number
	if n >= 7 then
		return 2
	end
	return 1
end

function Config.NightsFor(n: number): number
	if n <= 4 then
		return 4
	end
	return 5
end

function Config.ColdPointsFor(n: number): number
	if n >= 7 then
		return 2
	end
	return 3
end

-- Длительность фаз, секунды
Config.Phase = {
	intro = 15,
	day = 75,
	night = 60,
	discuss = 25,
	vote = 15,
	ended = 10,
}

-- Тепло
Config.HeatStart = 70
Config.HeatMax = 100
Config.HeatDrainDay = 0.4
Config.HeatDrainNight = 0.8
Config.CoalStart = 14
Config.CoalPerLoad = 25
Config.HeatSlowBelow = 20
Config.FreezeSeconds = 20

-- Дверь
Config.DoorHold = 3
Config.OutsideFreezeSeconds = 30
Config.FakeKnockHeatLoss = 40
Config.FakeKnockDarkSeconds = 10
Config.EmptyDoorHeatLoss = 10
Config.PeepholeTruth = 0.7

-- Гость
Config.Ability = {
	voice = { cost = 2 },
	forge = { cost = 1 },
	dark = { cost = 1, seconds = 10 },
	prints = { cost = 1 },
	steal = { cost = 1, coal = 2 },
	blizzard = { cost = 3, seconds = 15, oncePerRound = true },
}
Config.BraceletSeconds = 3
Config.BraceletRadius = 25 -- в стадах (около 8 шагов)

-- Задание лампы ночью
Config.LampRelightSeconds = 15
Config.LampHeatLoss = 15

-- Журнал
Config.Instruments = { "temp", "wind", "pressure", "snow" }
Config.InstrumentNames = {
	temp = "Температура",
	wind = "Ветер",
	pressure = "Давление",
	snow = "Снег",
}
Config.WindDirs = { "С", "С-В", "В", "Ю-В", "Ю", "Ю-З", "З", "С-З" }
Config.InkColors = {
	Color3.fromRGB(31, 79, 160),
	Color3.fromRGB(28, 122, 69),
	Color3.fromRGB(176, 100, 28),
	Color3.fromRGB(122, 45, 138),
	Color3.fromRGB(160, 40, 50),
	Color3.fromRGB(20, 120, 130),
	Color3.fromRGB(110, 90, 30),
	Color3.fromRGB(60, 60, 60),
}

-- Цвета стиля
Config.Palette = {
	night = Color3.fromRGB(11, 18, 32),
	blue = Color3.fromRGB(34, 53, 92),
	ice = Color3.fromRGB(159, 196, 238),
	warm = Color3.fromRGB(255, 184, 102),
	wood = Color3.fromRGB(138, 90, 58),
	danger = Color3.fromRGB(217, 43, 32),
	paper = Color3.fromRGB(239, 230, 207),
}

return Config
