--!nonstrict
-- Замеры, где уходят игроки. Работает только в опубликованной игре (в Studio вызовы игнорируются).
-- Смотреть: Creator Hub → Analytics → Funnels. Описание шагов: docs/13-retention.md

local AnalyticsService = game:GetService("AnalyticsService")
local HttpService = game:GetService("HttpService")

local Analytics = {}

-- Воронка первого знакомства с игрой. Шаги идут строго по порядку.
Analytics.Onboarding = {
	"Зашёл в игру",
	"Увидел лобби",
	"Начался первый раунд",
	"Увидел свою роль",
	"Первая запись в журнале",
	"Первая ночь",
	"Первое голосование",
	"Закончил первый раунд",
	"Начал второй раунд",
	"Закончил третий раунд",
}

local stepByName = {}
for i, name in Analytics.Onboarding do
	stepByName[name] = i
end

local reached: { [number]: number } = {}

function Analytics.onboarding(player: Player, name: string)
	local step = stepByName[name]
	if not step then
		return
	end
	local last = reached[player.UserId] or 0
	if step <= last then
		return
	end
	reached[player.UserId] = step
	pcall(function()
		AnalyticsService:LogOnboardingFunnelStepEvent(player, step, name)
	end)
end

-- Повторяющаяся воронка: как далеко доходят игроки в каждом раунде
local roundSession: { [number]: string } = {}
local RoundSteps = { "Старт раунда", "День 1", "Ночь 1", "Голосование 1", "Ночь 3", "Конец раунда" }
local roundStepIndex = {}
for i, name in RoundSteps do
	roundStepIndex[name] = i
end

function Analytics.roundStart(player: Player)
	roundSession[player.UserId] = HttpService:GenerateGUID(false)
	Analytics.roundStep(player, "Старт раунда")
end

function Analytics.roundStep(player: Player, name: string)
	local sid = roundSession[player.UserId]
	local step = roundStepIndex[name]
	if not sid or not step then
		return
	end
	pcall(function()
		AnalyticsService:LogFunnelStepEvent(player, "Раунд", sid, step, name)
	end)
end

-- В какой фазе игрок вышел из игры
function Analytics.left(player: Player, phase: string)
	pcall(function()
		AnalyticsService:LogCustomEvent(player, "Вышел: " .. phase, 1)
	end)
	reached[player.UserId] = nil
	roundSession[player.UserId] = nil
end

function Analytics.forget(player: Player)
	reached[player.UserId] = nil
	roundSession[player.UserId] = nil
end

return Analytics
