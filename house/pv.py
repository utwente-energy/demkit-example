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

# SOLAR PANEL SETUP
	# Add a solar pane
	idx = alpg.indexFromFile(alpgFolder+"PhotovoltaicSettings.txt", houseNum)

	if not useALPG or idx != -1:
		pv = SolarPanelDev("PV-House-" + str(houseNum), sim, sun) # <- see, here the sun object has to be provided ;)

		#Set the parameters
		if not useALPG:
			pv.size = 10*1.6		# in m2, (12 panels of 1.6 m2)
			pv.efficiency = 20		# efficiency in percent
			pv.azimuth = 180		# in degrees, 0=north, 90 is east, 180 is south
			pv.inclination = 35		# angle
		else:
			# Not using ALPG data
			pv.size = pv_specs[idx][3]			# in m2, (12 panels of 1.6 m2)
			pv.efficiency = pv_specs[idx][2]	# efficiency in percent
			pv.azimuth = pv_specs[idx][1]		# in degrees, 0=north, 90 is east
			pv.inclination = pv_specs[idx][0]	# angle

		pv.strictComfort = not useIslanding

		pv.commodities = commodities
		if useMC:
			pv.commodities = [commodities[phase - 1]]
			# Note, for a three phase inverter one needs to instantiate three separate PV instances!

		sm.addDevice(pv)

		# Add controllers
		if useCtrl or useAdmm:
			pvpc = CurtCtrl("PVController-House-" + str(houseNum), pv, ctrl, sim)
			pvpc.useEventControl = useEC
			pvpc.perfectPredictions = usePP
			pvpc.perfectPredictions = True # Historic data is not correct for the current implementation

			pvpc.commodities = list(pv.commodities)
			pvpc.weights = dict(weights)

		elif useAuction:
			pvpc = CurtAuctionCtrl("PVController-House-" + str(houseNum), pv, ctrl, sim)
			pvpc.strictComfort = not useIslanding
			pvpc.islanding = useIslanding

		elif usePlAuc:
			pvpc = PaCurtCtrl("PVController-House-" + str(houseNum), pv, ctrl, sim)
			pvpc.useEventControl = useEC
			pvpc.perfectPredictions = usePP
			pvpc.perfectPredictions = True # Historic data is not correct for the current implementation
			pvpc.strictComfort = not useIslanding
			pvpc.islanding = useIslanding

		# NOTE: Solar panels connected using a three phase inverter can be modelled as three separate PV panels
		# Use a for loop to instantiate these three panels
		# This "workaround" is required as uncontrollables, of which the PV is inherited, do not support multiple commodities
