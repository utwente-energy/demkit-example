# Copyright 2023 University of Twente

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

# http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Heating system
	# NOTE: Islanding is not implemented
	# NOTE: No support for threephase connected heatsources
	# NOTE: Only supported with ALPG data at the moment
	idx = alpg.indexFromFile(alpgFolder+"HeatingSettings.txt", houseNum)

	if not useMC:
		elPhase = 'ELECTRICITY'
	else:
		elPhase = commodities[phase - 1]

	zone = ZoneDev2R2C("Zone-House-"+str(houseNum), weather, sun, sim)
	# Zone parameters by R.P. van Leeuwen for heavy semi-detached
	zone.perfectPredictions = usePP
	zone.rFloor = 0.001		# K/W
	zone.rEnvelope = 0.0064	# K/W
	zone.cFloor = 5100 * 3600	# J/K
	zone.cZone = 21100 * 3600	# J/K
	zone.initialTemperature = 18.5

	zone.gainFile = alpgFolder+"Heatgain_Profile.csv"
	zone.ventilationFile = alpgFolder+"Airflow_Profile_Ventilation.csv" # Provides the airflow in M3/h!
	zone.gainColumn =  houseNum
	zone.ventilationColumn = houseNum
	# Add windows to the zone
	zone.addWindow(10, 180)

	# Add a thermostat
	thermostat = Thermostat("Thermostat-House-"+str(houseNum), zone, None, sim)
	thermostat.temperatureSetpointHeating = 18.5 			# setpoint temperature for the zone
	thermostat.temperatureSetpointCooling = 23.0
	thermostat.temperatureMin = 18.5 	# min setpoint temperature for the zone (turn on heating overnight on cold days)
	thermostat.temperatureMax = 23.0 	# max setpoint temperature for the zone (turn on cooling when above)
	thermostat.temperatureDeadband = [-0.1, 0.0, 0.5, 0.6]	# deadband control: [Below heating setpoint (HEAT), Above Heating setpoint (OFF), Below Cooling setpoint (OFF), Above Cooling setpoint (COOL)]
	thermostat.preheatingTime = 3600 			# Preaheating time in seconds before the actual starttime
	thermostat.perfectPredictions = usePP
	thermostat.timeBase = ctrlTimeBase
	# Add the heating schedule
	idx = alpg.indexFromFile(alpgFolder+"Thermostat_Starttimes.txt", houseNum)
	for j in range(0,  len(therm_setpoints[idx])):
		thermostat.addJob(therm_starttimes[idx][j],  therm_setpoints[idx][j])

	# Add a DHW tap
	dhw = DhwDev("DomesticHotWater-House-"+str(houseNum), sim)
	dhw.dhwFile = alpgFolder+"Heatdemand_Profile.csv" # using the weather profile as a quick and dirty test
	dhw.dhwColumn = houseNum
	dhw.perfectPredictions = usePP

	# # add a heat source
	if heat_specs[idx][0] == "CONVENTIONAL": # Gas boiler
		heatsource = GasBoilerDev("GasBoiler-House-"+str(houseNum), sim)
		heatsource.producingTemperatures = [0, 60.0]


	elif heat_specs[idx][0] == "HP":
		heatsource = HeatPumpDev("HeatPump-House-"+str(houseNum), sim)
		heatsource.producingTemperatures = [0, 35.0]
		heatsource.producingPowers = [0, 4500] # use [-4500, 4500] for cooling, but this is unsported yet
		heatsource.commodities = [elPhase, 'HEAT']
		heatsource.cop = {elPhase: 4.0} # Pretty common CoP, each unit of electricity consumed produces 4 units of heat
	else:
		heatsource = CombinedHeatPowerDev("Heatsource-House-"+str(houseNum), sim)
		heatsource.commodities = [elPhase, 'NATGAS', 'HEAT'] # INPUT, OUTPUT
		heatsource.cop = {elPhase: (-13.5/6.0), 'NATGAS': (13.5/21.0)}
	# Look in the sourcecodes of these heating devices to find out about CoP and conversionfactors

	# Define buffer capacity
	heatsource.capacity = 	50000.0
	heatsource.soc = 		25000.0
	heatsource.initialSoC = 25000.0
	heatsource.strictComfort = not useIslanding
	heatsource.islanding = useIslanding

	# Now link the source to the zone, thermostat and dhw
	heatsource.addZone(zone)
	heatsource.addThermostat(thermostat)

	sm.addDevice(heatsource)
	gm.addDevice(heatsource)

	if heat_specs[idx][0] == "CHP" or heat_specs[idx][0] == "HP":
		if useCtrl or useAdmm:
			heatctrl = ThermalBufConvCtrl("HeatController-House-"+str(houseNum),  heatsource,  ctrl,  sim)
			heatctrl.commodities = list(heatsource.commodities)
			if heat_specs[idx][0] == "CHP":
				heatctrl.weights = {elPhase: 1.0, 'NATGAS': 0.0, 'HEAT': 0.0}
			elif heat_specs[idx][0] == "HP":
				heatctrl.weights = {elPhase: 1.0, 'HEAT': 0.0}

			heatctrl.perfectPredictions = usePP
			heatctrl.useEventControl = useEC
			heatctrl.timeBase = ctrlTimeBase
		elif useAuction:
			# Control enabled:
			heatctrl = ThermalBufConvAuctionCtrl("HeatController-House-"+str(houseNum),  heatsource, ctrl,  sim)
			heatctrl.commodities = list(heatsource.commodities)
			if heat_specs[idx][0] == "CHP":
				heatctrl.weights = {elPhase: 1.0, 'NATGAS': 0.0, 'HEAT': 0.0}
			elif heat_specs[idx][0] == "HP":
				heatctrl.weights = {elPhase: 1.0, 'HEAT': 0.0}
			heatctrl.timeBase = ctrlTimeBase
			heatctrl.strictComfort = not useIslanding
			heatctrl.islanding = useIslanding
		elif usePlAuc:
			# Control enabled:
			heatctrl = ThermalPaBufConvCtrl("HeatController-House-"+str(houseNum),  heatsource, ctrl,  sim)
			heatctrl.commodities = list(heatsource.commodities)
			if heat_specs[idx][0] == "CHP":
				heatctrl.weights = {elPhase: 1.0, 'NATGAS': 0.0, 'HEAT': 0.0}
			elif heat_specs[idx][0] == "HP":
				heatctrl.weights = {elPhase: 1.0, 'HEAT': 0.0}
			heatctrl.perfectPredictions = usePP
			heatctrl.useEventControl = useEC
			heatctrl.timeBase = ctrlTimeBase
			heatctrl.strictComfort = not useIslanding
			heatctrl.islanding = useIslanding

	if not heat_specs[idx][0] == "HP":
		heatsource.addDhwTap(dhw)
	else:
		# Heatpump has not enough power to provide tapwater, so we need another to heat water. Note that the generic heatsource is not applicable to planning
		dhwsrc = HeatPumpDev("DomesticHotWaterControllerBoiler-House-"+str(houseNum), sim)
		dhwsrc.producingTemperatures = [0, 60.0]
		dhwsrc.producingPowers = [0, 25000]
		dhwsrc.perfectPredictions = usePP
		dhwsrc.strictComfort = not useIslanding
		dhwsrc.islanding = useIslanding
		dhwsrc.commodities = [elPhase, 'HEAT']
		dhwsrc.cop = {elPhase: 4.0} # Pretty common CoP, each unit of electricity consumed produces 4 units of heat
		dhwsrc.addDhwTap(dhw)

		sm.addDevice(dhwsrc)
		gm.addDevice(dhwsrc)

		if useCtrl or useAdmm:
			dhwctrl = ThermalBufConvCtrl("DomesticHotWaterController-House-"+str(houseNum),  dhwsrc,  ctrl,  sim)
			dhwctrl.commodities = list(dhwsrc.commodities)
			dhwctrl.weights = {elPhase: 1.0, 'HEAT': 0.0}
			dhwctrl.perfectPredictions = usePP
			dhwctrl.useEventControl = useEC
			dhwctrl.timeBase = ctrlTimeBase

		elif useAuction:
			dhwctrl = ThermalBufConvAuctionCtrl("DomesticHotWaterController-House-"+str(houseNum),  dhwsrc,  ctrl,  sim)
			dhwctrl.commodities = list(dhwsrc.commodities)
			dhwctrl.weights = {elPhase: 1.0, 'HEAT': 0.0}
			dhwctrl.timeBase = ctrlTimeBase
			dhwctrl.strictComfort = not useIslanding
			dhwctrl.islanding = useIslanding

		elif usePlAuc:
			dhwctrl = ThermalPaBufConvCtrl("DomesticHotWaterController-House-"+str(houseNum),  dhwsrc,  ctrl,  sim)
			dhwctrl.commodities = list(dhwsrc.commodities)
			dhwctrl.weights = {elPhase: 1.0, 'HEAT': 0.0}
			dhwctrl.perfectPredictions = usePP
			dhwctrl.useEventControl = useEC
			dhwctrl.timeBase = ctrlTimeBase
			dhwctrl.strictComfort = not useIslanding
			dhwctrl.islanding = useIslanding
