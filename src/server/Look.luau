--!nonstrict
-- «Сочная» картинка: свет, цвет и эффекты Roblox. Настройки описаны в docs/09-art-direction.md.
-- День и ночь различаются пресетами; Main вызывает Look.apply при смене фазы.

local Lighting = game:GetService("Lighting")

local Look = {}

local function get(className: string, name: string): Instance
	local inst = Lighting:FindFirstChild(name)
	if not inst then
		inst = Instance.new(className)
		inst.Name = name
		inst.Parent = Lighting
	end
	return inst
end

function Look.setup()
	-- Future даёт мягкие тени от каждой лампы и окна: главный источник «дорогого» вида
	pcall(function()
		Lighting.Technology = Enum.Technology.Future
	end)
	Lighting.GlobalShadows = true
	Lighting.EnvironmentDiffuseScale = 1
	Lighting.EnvironmentSpecularScale = 1
	get("Atmosphere", "Atmosphere")
	get("BloomEffect", "Bloom")
	get("ColorCorrectionEffect", "Grade")
	get("SunRaysEffect", "SunRays")
	get("DepthOfFieldEffect", "DOF")
	Look.apply("day")
end

local presets = {
	day = {
		clock = 14,
		brightness = 2.2,
		ambient = Color3.fromRGB(95, 110, 140),
		outdoor = Color3.fromRGB(150, 165, 200),
		exposure = 0.1,
		atmo = { density = 0.32, offset = 0.1, color = Color3.fromRGB(190, 210, 240), decay = Color3.fromRGB(120, 150, 200), glare = 0.4, haze = 1.6 },
		bloom = { intensity = 0.9, size = 28, threshold = 1.6 },
		grade = { brightness = 0.02, contrast = 0.18, saturation = 0.28, tint = Color3.fromRGB(255, 248, 240) },
		rays = 0.08,
	},
	night = {
		clock = 0.2,
		brightness = 0.6,
		ambient = Color3.fromRGB(28, 34, 60),
		outdoor = Color3.fromRGB(60, 80, 140),
		exposure = 0.25,
		atmo = { density = 0.42, offset = 0.2, color = Color3.fromRGB(70, 100, 170), decay = Color3.fromRGB(30, 45, 95), glare = 0.2, haze = 2.2 },
		bloom = { intensity = 1.4, size = 36, threshold = 1.2 },
		grade = { brightness = 0.0, contrast = 0.24, saturation = 0.35, tint = Color3.fromRGB(225, 235, 255) },
		rays = 0.0,
	},
	blizzard = {
		atmo = { density = 0.78, offset = 0.0, color = Color3.fromRGB(200, 215, 240), decay = Color3.fromRGB(150, 170, 210), glare = 0, haze = 3 },
	},
	breach = {
		grade = { brightness = -0.05, contrast = 0.35, saturation = -0.2, tint = Color3.fromRGB(170, 205, 255) },
	},
}

function Look.apply(name: string)
	local p = presets[name]
	if not p then
		return
	end
	if p.clock then
		Lighting.ClockTime = p.clock
		Lighting.Brightness = p.brightness
		Lighting.Ambient = p.ambient
		Lighting.OutdoorAmbient = p.outdoor
		Lighting.ExposureCompensation = p.exposure
	end
	if p.atmo then
		local a = Lighting.Atmosphere :: Atmosphere
		a.Density, a.Offset = p.atmo.density, p.atmo.offset
		a.Color, a.Decay = p.atmo.color, p.atmo.decay
		a.Glare, a.Haze = p.atmo.glare, p.atmo.haze
	end
	if p.bloom then
		local b = Lighting.Bloom :: BloomEffect
		b.Intensity, b.Size, b.Threshold = p.bloom.intensity, p.bloom.size, p.bloom.threshold
	end
	if p.grade then
		local g = Lighting.Grade :: ColorCorrectionEffect
		g.Brightness, g.Contrast, g.Saturation, g.TintColor = p.grade.brightness, p.grade.contrast, p.grade.saturation, p.grade.tint
	end
	if p.rays ~= nil then
		(Lighting.SunRays :: SunRaysEffect).Intensity = p.rays
	end
end

-- Снег, который всегда падает вокруг станции
function Look.snow(parent: Instance, center: Vector3)
	local emitterPart = Instance.new("Part")
	emitterPart.Name = "SnowEmitter"
	emitterPart.Anchored = true
	emitterPart.CanCollide = false
	emitterPart.CanQuery = false
	emitterPart.Transparency = 1
	emitterPart.Size = Vector3.new(160, 1, 160)
	emitterPart.Position = center + Vector3.new(0, 45, 0)
	emitterPart.Parent = parent
	local pe = Instance.new("ParticleEmitter")
	pe.Texture = "rbxasset://textures/particles/sparkles_main.dds"
	pe.Color = ColorSequence.new(Color3.fromRGB(235, 245, 255))
	pe.LightEmission = 0.6
	pe.Size = NumberSequence.new(0.25, 0.15)
	pe.Transparency = NumberSequence.new({ NumberSequenceKeypoint.new(0, 1), NumberSequenceKeypoint.new(0.1, 0.1), NumberSequenceKeypoint.new(1, 0.4) })
	pe.Lifetime = NumberRange.new(8, 12)
	pe.Rate = 220
	pe.Speed = NumberRange.new(4, 7)
	pe.SpreadAngle = Vector2.new(15, 15)
	pe.EmissionDirection = Enum.NormalId.Bottom
	pe.Acceleration = Vector3.new(1.5, 0, 0.5)
	pe.Parent = emitterPart
	return pe
end

return Look
