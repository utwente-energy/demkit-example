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

# BATTERY
	#add a battery
	idx = alpg.indexFromFile(alpgFolder+"BatterySettings.txt", houseNum)
	if not useALPG or idx != -1:
		# Follows very much the same reasoning as with the EV above, so the documentation is sparse here
		buf = BufDev("Battery-House-"+str(houseNum), sim, sm)		# params: name, simHost

		#Set the parameter
		if useALPG:
			buf.chargingPowers = [-1*bat_specs[idx][0], bat_specs[idx][0]]
			buf.capacity = bat_specs[idx][1]
			buf.initialSoC = bat_specs[idx][2]
		else:
			# Not using ALPG data
			buf.chargingPowers = [-3700, 3700]
			buf.capacity = 13500
			buf.initialSoC = buf.capacity * 0.5

		buf.soc = buf.initialSoC
		buf.commodities = commodities
		buf.discrete = False

		# Marks to spawn events
		buf.highMark = buf.capacity * 0.8
		buf.lowMark = buf.capacity * 0.2

		buf.strictComfort = not useIslanding

		if useMC:
			if buf.capacity <= 7500:
				buf.commodities = []
				buf.commodities = [(commodities[phase-1])]
			else:
				buf.commodities = ['EL1', 'EL2', 'EL3']

		# add the battery to the smart meter
		sm.addDevice(buf)

		if useFillMethod:
			buf.meter = sm


		# Add a controller
		if useCtrl or useAdmm:
			bufc = BufCtrl("Battery-Controller-House-"+str(houseNum),  buf,  ctrl,  sim) 	# params: name, device, higher-level controller, simHost
			bufc.useEventControl = useEC
			bufc.timeBase = ctrlTimeBase
			bufc.commodities = list(buf.commodities)
			if useMC:
				bufc.weights = dict(weights)
			# Battery reservation options
			bufc.planningCapacity = 1.0 #0.8			# Fraction to use for planning, symmetric (i.e. it uses a Soc ranging from 0+x/2 - 1-x/2, where x is the variable
			bufc.planningPower = 1.0 #0.6			# Fraction of the power to use, as above.
			bufc.eventPlanningCapacity = 1.0	# Fraction to use for planning, symmetric (i.e. it uses a Soc ranging from 0+x/2 - 1-x/2, where x is the variable
			bufc.eventPlanningPower = 1.0		# Fraction of the power to use, as above.

			# Balancing battery
			if useFillMethod:
				buf.parent = ctrl
				buf.balancing = True
			#
			# if useCongestionPoints:
			# 	bufc.congestionPoint = cp

		elif useAuction:
			bufc = BufAuctionCtrl("Battery-Controller-House-"+str(houseNum),  buf,  ctrl,  sim)
			bufc.strictComfort = not useIslanding
			bufc.islanding = useIslanding

		elif usePlAuc:
			bufc = PaBufCtrl("Battery-Controller-House-"+str(houseNum),  buf,  ctrl,  sim)
			bufc.useEventControl = useEC
			bufc.timeBase = ctrlTimeBase
			bufc.strictComfort = not useIslanding
			bufc.islanding = useIslanding

