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
	idx = alpg.indexFromFile(alpgFolder + "HeatingSettings.txt", houseNum)

	# An overall setting to disable/enable discrete heating:
	discrete = True

	# Creating a controller for the heating system

	# Check if we need to have a controller
	hCtrl = not useAuction and not usePlAuc and not useAdmm

	# Add a congestion point to limit the overall power of the combined thermal asset (heatpump or CHP)
	cpheat = None
	if True:
		cpheat = CongestionPoint()
		if useMC:
			for c in commodities:
				cpheat.setUpperLimit(c, 667)  # 2kW limit in total over three phases
				cpheat.setLowerLimit(c, -667)
		else:
			cpheat.setUpperLimit('ELECTRICITY', 2001)  # 2kW limit, 1W margin for rounding errors
			cpheat.setLowerLimit('ELECTRICITY', -2001)

	# Check if there is a higher level house controller
	heatsysctrl = None
	if useAdmm:
		heatsysctrl = ctrl

	# if hCtrl, then we need a heat contoller
	if hCtrl:
		if not useCtrl:
			heatsysctrl = GroupCtrl("HeatController-House-" + str(houseNum), sim, None, cpheat)
		else:
			heatsysctrl = GroupCtrl("HeatController-House-" + str(houseNum), sim, ctrl, cpheat)
		heatsysctrl.minImprovement = 0.001
		heatsysctrl.timeBase = ctrlTimeBase  # 900 is advised hre, must be a multiple of the simulation timeBase
		heatsysctrl.useEventControl = useEC  # Enable / disable event-based control
		heatsysctrl.isFleetController = False  # Very important to set this right in case of large structures. The root controller needs to be a fleetcontroller anyways. See 4.3 of Hoogsteen's thesis
		if ctrl is None:
			heatsysctrl.isFleetController = True  # Very important to set this right in case of large structures. The root controller needs to be a fleetcontroller anyways. See 4.3 of Hoogsteen's thesis
		heatsysctrl.initialPlan = False
		heatsysctrl.simultaneousCommits = 1
		heatsysctrl.strictComfort = not useIslanding

		heatsysctrl.planHorizon = 2 * int(24 * 3600 / ctrlTimeBase)
		heatsysctrl.planInterval = int(24 * 3600 / ctrlTimeBase)
		heatsysctrl.commodities = list(commodities)  # Overwrite the list of commodities
		heatsysctrl.weights = dict(weights)  # Overwrite the weights

		if pricesElectricity is not None:
			for c in commodities:
				heatsysctrl.prices = {}
				heatsysctrl.prices[c] = pricesElectricity
			heatsysctrl.profileWeight = profileWeight

	if not useMC:
		elPhase = 'ELECTRICITY'
	else:
		elPhase = commodities[phase - 1]

	zone = ZoneDev2R2C("Zone-House-" + str(houseNum), weather, sun, sim)
	# Zone parameters by R.P. van Leeuwen for heavy semi-detached
	zone.perfectPredictions = usePP
	zone.rFloor = 0.001  # K/W
	zone.rEnvelope = 0.0064  # K/W
	zone.cFloor = 5100 * 3600  # J/K
	zone.cZone = 21100 * 3600  # J/K
	zone.initialTemperature = 20.0

	zone.gainFile = alpgFolder + "Heatgain_Profile.csv"
	zone.ventilationFile = alpgFolder + "Airflow_Profile_Ventilation.csv"  # Provides the airflow in M3/h!
	zone.gainColumn = houseNum
	zone.ventilationColumn = houseNum
	# Add windows to the zone
	zone.addWindow(10, 180)

	# Add a thermostat
	thermostat = Thermostat("Thermostat-House-" + str(houseNum), zone, None, sim)
	thermostat.temperatureSetpointHeating = 18.5  # setpoint temperature for the zone
	thermostat.temperatureSetpointCooling = 23.0
	thermostat.temperatureMin = 18.5  # min setpoint temperature for the zone (turn on heating overnight on cold days)
	thermostat.temperatureMax = 23.0  # max setpoint temperature for the zone (turn on cooling when above)
	thermostat.temperatureDeadband = [-0.5, 0.0, 5.0,
	                                  5.5]  # deadband control: [Below heating setpoint (HEAT), Above Heating setpoint (OFF), Below Cooling setpoint (OFF), Above Cooling setpoint (COOL)]
	thermostat.preheatingTime = 3600  # Preaheating time in seconds before the actual starttime
	thermostat.perfectPredictions = usePP
	thermostat.timeBase = ctrlTimeBase
	# Add the heating schedule
	idx = alpg.indexFromFile(alpgFolder + "Thermostat_Starttimes.txt", houseNum)
	for j in range(0, len(therm_setpoints[idx])):
		thermostat.addJob(therm_starttimes[idx][j], therm_setpoints[idx][j])

	# Initialize the room temperature at the max of the first two thermostat setpoints
	zone.initialTemperature = max(therm_setpoints[idx][0], therm_setpoints[idx][1])

	# Add a DHW tap
	dhw = DhwDev("DomesticHotWater-House-" + str(houseNum), sim)
	dhw.dhwFile = alpgFolder + "Heatdemand_Profile.csv"  # using the weather profile as a quick and dirty test
	dhw.dhwColumn = houseNum
	dhw.perfectPredictions = usePP


	# # add a heat source
	if heat_specs[idx][0] == "CONVENTIONAL":  # Gas boiler
		heatsource = GasBoilerDev("GasBoiler-House-" + str(houseNum), sim)
		heatsource.producingTemperatures = [0, 60.0]
	elif heat_specs[idx][0] == "HP":
		heatsource = HeatPumpDev("HeatPump-House-" + str(houseNum), sim)
		heatsource.producingTemperatures = [0, 35.0]
		heatsource.producingPowers = [0, 5500]  # use [-4500, 4500] for cooling, but this is unsported yet
		heatsource.commodities = [elPhase, 'HEAT']
		heatsource.cop = {elPhase: 5.0}  # Pretty common CoP, each unit of electricity consumed produces 4 units of heat
	else:
		heatsource = CombinedHeatPowerDev("Heatsource-House-" + str(houseNum), sim)
		heatsource.commodities = [elPhase, 'NATGAS', 'HEAT']  # INPUT, OUTPUT
		heatsource.cop = {elPhase: (-13.5 / 6.0), 'NATGAS': (13.5 / 21.0)}
	# Look in the sourcecodes of these heating devices to find out about CoP and conversionfactors

	# Define buffer capacity
	heatsource.capacity = 35000.0
	heatsource.soc = 17000.0
	heatsource.initialSoC = 17000.0
	heatsource.strictComfort = not useIslanding
	heatsource.islanding = useIslanding

	heatsource.discrete = discrete

	# Now link the source to the zone, thermostat and dhw
	heatsource.addZone(zone)
	heatsource.addThermostat(thermostat)

	sm.addDevice(heatsource)
	gm.addDevice(heatsource)


	if heat_specs[idx][0] == "CHP" or heat_specs[idx][0] == "HP":
		if hCtrl or useAdmm:
			heatctrl = ThermalBufConvCtrl("HeatPumpController-House-" + str(houseNum), heatsource, heatsysctrl, sim)
			heatctrl.commodities = list(heatsource.commodities)
			if heat_specs[idx][0] == "CHP":
				heatctrl.weights = {elPhase: 1.0, 'NATGAS': 0.0, 'HEAT': 0.0}
			elif heat_specs[idx][0] == "HP":
				heatctrl.weights = {elPhase: 1.0, 'HEAT': 0.0}

			heatctrl.perfectPredictions = usePP
			heatctrl.useEventControl = useEC
			heatctrl.timeBase = ctrlTimeBase

			heatctrl.discrete = discrete
		elif useAuction:
			# Control enabled:
			heatctrl = ThermalBufConvAuctionCtrl("HeatPumpController-House-" + str(houseNum), heatsource, ctrl, sim)
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
			heatctrl = ThermalPaBufConvCtrl("HeatPumpController-House-" + str(houseNum), heatsource, ctrl, sim)
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



	# Add cooling capabilities in case of HP, only supported for Profile Steering
	if hCtrl:
		# # add a heat source
		if heat_specs[idx][0] == "HP":
			coolsource = HeatPumpDev("HeatPump-Cooler-House-" + str(houseNum), sim)
			coolsource.producingTemperatures = [0, 35.0]
			coolsource.producingPowers = [-5500, 0]  # use [-4500, 4500] for cooling, but this is unsported yet
			coolsource.commodities = [elPhase, 'HEAT']
			coolsource.cop = {
				elPhase: 27.0}  # Pretty common CoP, each unit of electricity consumed produces 4 units of heat

			# Define buffer capacity
			coolsource.capacity = 10000.0
			coolsource.soc = 5000.0
			coolsource.initialSoC = 5000.0
			coolsource.strictComfort = not useIslanding
			coolsource.islanding = useIslanding

			coolsource.discrete = discrete

			# Now link the source to the zone, thermostat and dhw
			coolsource.addZone(zone)
			coolsource.addThermostat(thermostat)

			sm.addDevice(coolsource)
			gm.addDevice(coolsource)


			# FIXME: For now we only support profile steering with thermal
			if hCtrl:
				coolctrl = ThermalBufConvCtrl("CoolerController-House-" + str(houseNum), coolsource, heatsysctrl, sim)
				coolctrl.commodities = list(coolsource.commodities)
				if heat_specs[idx][0] == "CHP":
					coolctrl.weights = {elPhase: 1.0, 'NATGAS': 0.0, 'HEAT': 0.0}
				elif heat_specs[idx][0] == "HP":
					coolctrl.weights = {elPhase: 1.0, 'HEAT': 0.0}

				coolctrl.perfectPredictions = usePP
				coolctrl.useEventControl = useEC
				coolctrl.timeBase = ctrlTimeBase
				coolctrl.discrete = discrete






	if not heat_specs[idx][0] == "HP":
		heatsource.addDhwTap(dhw)
	else:
		# Heatpump has not enough power to provide tapwater, so we need another to heat water. Note that the generic heatsource is not applicable to planning
		dhwsrc = HeatPumpDev("HeatPump-DHW-House-" + str(houseNum), sim)
		dhwsrc.producingTemperatures = [0, 60.0]
		dhwsrc.producingPowers = [0, 4000]
		dhwsrc.capacity = 14000
		dhwsrc.perfectPredictions = usePP
		dhwsrc.strictComfort = not useIslanding
		dhwsrc.islanding = useIslanding
		dhwsrc.commodities = [elPhase, 'HEAT']
		dhwsrc.cop = {elPhase: 2.0}  # Pretty common CoP, each unit of electricity consumed produces 4 units of heat

		dhwsrc.discrete = discrete

		dhwsrc.addDhwTap(dhw)

		sm.addDevice(dhwsrc)
		gm.addDevice(dhwsrc)

		if True:
			dhwctrl = ThermalBufConvCtrl("DomesticHotWaterController-House-" + str(houseNum), dhwsrc, heatsysctrl, sim)
			dhwctrl.commodities = list(dhwsrc.commodities)
			dhwctrl.weights = {elPhase: 1.0, 'HEAT': 0.0}
			dhwctrl.perfectPredictions = usePP
			dhwctrl.useEventControl = useEC
			dhwctrl.timeBase = ctrlTimeBase

			dhwctrl.discrete = discrete

		elif useAuction:
			dhwctrl = ThermalBufConvAuctionCtrl("DomesticHotWaterController-House-" + str(houseNum), dhwsrc, ctrl, sim)
			dhwctrl.commodities = list(dhwsrc.commodities)
			dhwctrl.weights = {elPhase: 1.0, 'HEAT': 0.0}
			dhwctrl.timeBase = ctrlTimeBase
			dhwctrl.strictComfort = not useIslanding
			dhwctrl.islanding = useIslanding

		elif usePlAuc:
			dhwctrl = ThermalPaBufConvCtrl("DomesticHotWaterController-House-" + str(houseNum), dhwsrc, ctrl, sim)
			dhwctrl.commodities = list(dhwsrc.commodities)
			dhwctrl.weights = {elPhase: 1.0, 'HEAT': 0.0}
			dhwctrl.perfectPredictions = usePP
			dhwctrl.useEventControl = useEC
			dhwctrl.timeBase = ctrlTimeBase
			dhwctrl.strictComfort = not useIslanding
			dhwctrl.islanding = useIslanding
