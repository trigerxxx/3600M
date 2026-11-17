--!nonstrict
-- Станция из серых блоков для прототипа. Строится кодом при запуске сервера,
-- чтобы прототип работал без ручной постройки в Studio. Позже заменим на красивую карту,
-- сохранив имена точек и подсказок.

local Config = require(game:GetService("ReplicatedStorage").Shared.Config)

local Map = {}

local P = Config.Palette
local WALL_H = 12

export type Built = {
	model: Model,
	door: BasePart,
	prompts: { [string]: ProximityPrompt },
	spots: { [string]: Vector3 },
	lights: { Light },
	lamp: PointLight,
	eastLamp: BasePart,
}

local function part(parent: Instance, name: string, size: Vector3, pos: Vector3, color: Color3, props: { [string]: any }?): Part
	local p = Instance.new("Part")
	p.Name = name
	p.Anchored = true
	p.Size = size
	p.Position = pos
	p.Color = color
	p.Material = Enum.Material.SmoothPlastic
	p.TopSurface = Enum.SurfaceType.Smooth
	p.BottomSurface = Enum.SurfaceType.Smooth
	if props then
		for k, v in props do
			(p :: any)[k] = v
		end
	end
	p.Parent = parent
	return p
end

-- Стена по оси X (вдоль) или Z, с проёмом [gapFrom, gapTo] по длине
local function wall(parent: Instance, name: string, from: Vector3, to: Vector3, gap: { number }?)
	local color = Color3.fromRGB(80, 60, 45)
	local alongX = math.abs(to.X - from.X) > math.abs(to.Z - from.Z)
	local a = if alongX then math.min(from.X, to.X) else math.min(from.Z, to.Z)
	local b = if alongX then math.max(from.X, to.X) else math.max(from.Z, to.Z)
	local segments = { { a, b } }
	if gap then
		segments = { { a, gap[1] }, { gap[2], b } }
	end
	for i, seg in segments do
		local len = seg[2] - seg[1]
		if len > 0.05 then
			local mid = (seg[1] + seg[2]) / 2
			local size = if alongX then Vector3.new(len, WALL_H, 1) else Vector3.new(1, WALL_H, len)
			local pos = if alongX then Vector3.new(mid, WALL_H / 2, from.Z) else Vector3.new(from.X, WALL_H / 2, mid)
			part(parent, name .. i, size, pos, color)
		end
	end
end

local function prompt(parent: BasePart, key: string, text: string, hold: number?): ProximityPrompt
	local pp = Instance.new("ProximityPrompt")
	pp.Name = key
	pp.ActionText = text
	pp.ObjectText = ""
	pp.HoldDuration = hold or 0
	pp.MaxActivationDistance = 9
	pp.RequiresLineOfSight = false
	pp.Parent = parent
	return pp
end

function Map.build(): Built
	local old = workspace:FindFirstChild("Station")
	if old then
		old:Destroy()
	end
	local m = Instance.new("Model")
	m.Name = "Station"
	m.Parent = workspace

	local prompts: { [string]: ProximityPrompt } = {}
	local lights: { Light } = {}

	-- снег и площадка лобби
	part(m, "Snow", Vector3.new(500, 2, 500), Vector3.new(0, -1, 0), Color3.fromRGB(225, 233, 245), { Material = Enum.Material.Snow })
	part(m, "Lobby", Vector3.new(60, 2, 60), Vector3.new(0, 30, 200), P.blue)

	-- главная комната: x -20..20, z -15..15
	part(m, "FloorMain", Vector3.new(40, 1, 30), Vector3.new(0, 0.5, 0), P.wood)
	part(m, "Roof", Vector3.new(56, 1, 32), Vector3.new(7, WALL_H + 0.5, 0), Color3.fromRGB(60, 45, 35))
	wall(m, "WallSouth", Vector3.new(-20, 0, -15), Vector3.new(20, 0, -15), { -3, 3 })
	wall(m, "WallNorth", Vector3.new(-20, 0, 15), Vector3.new(20, 0, 15), { -8, -2 })
	wall(m, "WallWest", Vector3.new(-20, 0, -15), Vector3.new(-20, 0, 15))
	wall(m, "WallEast", Vector3.new(20, 0, -15), Vector3.new(20, 0, 15), { -10, -6 })

	-- северное окно
	part(m, "NorthWindow", Vector3.new(6, 6, 0.4), Vector3.new(-5, 6, 15), P.ice, { Transparency = 0.5, Material = Enum.Material.Glass })
	part(m, "NorthWindowLow", Vector3.new(6, 3, 1), Vector3.new(-5, 1.5, 15), Color3.fromRGB(80, 60, 45))
	part(m, "NorthWindowHigh", Vector3.new(6, 3, 1), Vector3.new(-5, 10.5, 15), Color3.fromRGB(80, 60, 45))

	-- дверь
	local door = part(m, "Door", Vector3.new(6, 9, 1), Vector3.new(0, 4.5, -15), P.blue, { Material = Enum.Material.Ice })
	part(m, "DoorTop", Vector3.new(6, 3, 1), Vector3.new(0, 10.5, -15), Color3.fromRGB(80, 60, 45))
	local doorLamp = Instance.new("PointLight")
	doorLamp.Color = P.warm
	doorLamp.Range = 12
	doorLamp.Brightness = 1.5
	local lampPart = part(m, "DoorLamp", Vector3.new(1, 1, 1), Vector3.new(0, 10, -14), P.warm, { Material = Enum.Material.Neon })
	doorLamp.Parent = lampPart
	table.insert(lights, doorLamp)
	-- снаружи у двери: постучать
	local knockPad = part(m, "KnockPad", Vector3.new(6, 1, 4), Vector3.new(0, 0.5, -18), Color3.fromRGB(200, 210, 225))
	prompts.knock = prompt(knockPad, "knock", "Постучать")

	-- печь
	local stove = part(m, "Stove", Vector3.new(5, 5, 5), Vector3.new(-15, 3, 9), Color3.fromRGB(25, 20, 18))
	local fire = Instance.new("PointLight")
	fire.Color = Color3.fromRGB(255, 150, 60)
	fire.Range = 30
	fire.Brightness = 2
	fire.Parent = stove
	table.insert(lights, fire)
	prompts.coal = prompt(stove, "coal", "Подкинуть уголь")

	-- стол с журналом
	local desk = part(m, "Desk", Vector3.new(10, 3, 5), Vector3.new(6, 2, 8), Color3.fromRGB(90, 67, 50))
	part(m, "JournalBook", Vector3.new(3, 0.3, 2), Vector3.new(6, 3.65, 8), P.paper)
	prompts.journal = prompt(desk, "journal", "Журнал")

	-- потолочный свет
	local ceiling = part(m, "CeilingLamp", Vector3.new(2, 0.5, 2), Vector3.new(0, WALL_H - 0.5, 0), P.warm, { Material = Enum.Material.Neon })
	local cl = Instance.new("PointLight")
	cl.Color = P.warm
	cl.Range = 35
	cl.Brightness = 1.2
	cl.Parent = ceiling
	table.insert(lights, cl)

	-- приборная (x 20..34, z -2..15) и генератор (x 20..34, z -15..-2)
	part(m, "FloorEast", Vector3.new(14, 1, 30), Vector3.new(27, 0.5, 0), Color3.fromRGB(70, 60, 55))
	wall(m, "WallEastOuter", Vector3.new(34, 0, -15), Vector3.new(34, 0, 15), { 6, 10 })
	wall(m, "WallEastSouth", Vector3.new(20, 0, -15), Vector3.new(34, 0, -15))
	wall(m, "WallEastNorth", Vector3.new(20, 0, 15), Vector3.new(34, 0, 15))
	wall(m, "WallInstrGen", Vector3.new(20, 0, -2), Vector3.new(34, 0, -2), { 24, 28 })

	local barometer = part(m, "Barometer", Vector3.new(2, 3, 1), Vector3.new(27, 5, 14), Color3.fromRGB(180, 160, 110))
	prompts.pressure = prompt(barometer, "pressure", "Барометр")

	local generator = part(m, "Generator", Vector3.new(5, 4, 4), Vector3.new(28, 2.5, -9), Color3.fromRGB(70, 75, 90))
	prompts.generator = prompt(generator, "generator", "Завести генератор", 1)

	-- лампа в восточном окне
	part(m, "EastWindow", Vector3.new(0.4, 4, 4), Vector3.new(34, 6, 8), P.ice, { Transparency = 0.5, Material = Enum.Material.Glass })
	part(m, "EastWindowLow", Vector3.new(1, 4, 4), Vector3.new(34, 2, 8), Color3.fromRGB(80, 60, 45))
	part(m, "EastWindowHigh", Vector3.new(1, 4, 4), Vector3.new(34, 10, 8), Color3.fromRGB(80, 60, 45))
	local eastLamp = part(m, "EastLamp", Vector3.new(1, 1.5, 1), Vector3.new(33, 4.75, 8), P.warm, { Material = Enum.Material.Neon })
	local lamp = Instance.new("PointLight")
	lamp.Color = P.warm
	lamp.Range = 14
	lamp.Brightness = 2
	lamp.Parent = eastLamp
	prompts.lamp = prompt(eastLamp, "lamp", "Зажечь лампу")

	-- холодная кладовка (закрытая коробка, сюда отправляют выбывших)
	part(m, "ColdFloor", Vector3.new(14, 1, 12), Vector3.new(-33, 0.5, -9), Color3.fromRGB(60, 70, 85))
	wall(m, "ColdS", Vector3.new(-40, 0, -15), Vector3.new(-26, 0, -15))
	wall(m, "ColdN", Vector3.new(-40, 0, -3), Vector3.new(-26, 0, -3))
	wall(m, "ColdW", Vector3.new(-40, 0, -15), Vector3.new(-40, 0, -3))
	part(m, "ColdE", Vector3.new(1, WALL_H, 12), Vector3.new(-26, WALL_H / 2, -9), P.ice, { Transparency = 0.6, Material = Enum.Material.Glass })
	part(m, "ColdRoof", Vector3.new(14, 1, 12), Vector3.new(-33, WALL_H + 0.5, -9), Color3.fromRGB(60, 45, 35))

	-- снаружи: метеомачта и снегомер
	local mast = part(m, "Mast", Vector3.new(1, 16, 1), Vector3.new(-28, 8, -32), Color3.fromRGB(200, 200, 210))
	part(m, "MastBox", Vector3.new(3, 3, 3), Vector3.new(-28, 3, -32), Color3.fromRGB(230, 230, 235))
	prompts.temp = prompt(mast, "temp", "Термометр")
	local vane = part(m, "Vane", Vector3.new(4, 0.5, 0.5), Vector3.new(-28, 16, -32), Color3.fromRGB(200, 60, 50))
	prompts.wind = prompt(vane, "wind", "Флюгер")
	prompts.wind.MaxActivationDistance = 20
	local mastFoot = part(m, "MastFoot", Vector3.new(4, 0.5, 4), Vector3.new(-28, 0.25, -36), Color3.fromRGB(200, 210, 225))
	prompts.nightMeasure = prompt(mastFoot, "nightMeasure", "Ночной замер", 1)
	local snowGauge = part(m, "SnowGauge", Vector3.new(0.6, 6, 0.6), Vector3.new(-14, 3, -20), Color3.fromRGB(30, 30, 35))
	prompts.snow = prompt(snowGauge, "snow", "Снегомер", 1)

	return {
		model = m,
		door = door,
		prompts = prompts,
		lights = lights,
		lamp = lamp,
		eastLamp = eastLamp,
		spots = {
			inside = Vector3.new(0, 3, 0),
			table = Vector3.new(6, 3, 3),
			mast = Vector3.new(-24, 3, -30),
			cold = Vector3.new(-33, 3, -9),
			lobby = Vector3.new(0, 34, 200),
			doorInside = Vector3.new(0, 3, -12),
		},
	}
end

function Map.setDoorClosed(built: Built, closed: boolean)
	built.door.CanCollide = closed
	built.door.Transparency = if closed then 0 else 0.7
end

return Map
