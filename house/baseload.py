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

# STATIC LOAD
	#add a lumped uncontrollable load
	unc = CurtDev("Load-House-"+str(houseNum),  sim) #params: name, simHost
	unc.filename = alpgFolder+'Electricity_Profile.csv' 						# Specify the file for active power
	unc.filenameReactive = alpgFolder+'Reactive_Electricity_Profile.csv'		# Optional, specify the file for reactive power
	unc.column = houseNum
	unc.timeBase = 60		# Timebase, NOTE this is the timebase of the dataset and not the simulation!
	unc.strictComfort = not useIslanding

	if useMC:
		# Typically, one has to do the following with multiple commodities:
		unc.commodities = [(commodities[phase-1])]			# Add applicable commoditie(s)

	sm.addDevice(unc)

	# Optionally, add a controller to the device:
	if useCtrl or useAdmm:
		uncc = CurtCtrl("LoadController-House-"+str(houseNum), unc, ctrl, sim) 	# params: name, device, higher-level controller, simHost
		uncc.perfectPredictions = usePP							# Use perfect predictions or not
		uncc.useEventControl = useEC							# Use event-based control
		uncc.timeBase = ctrlTimeBase							# TimeBase for controllers

		uncc.commodities = list(unc.commodities)    		# Add applicable commodity
		uncc.weights = dict(weights)						# Overwrite the weights

	elif useAuction:
		uncc = CurtAuctionCtrl("LoadController-House-"+str(houseNum), unc, ctrl, sim)
		uncc.strictComfort = not useIslanding
		uncc.islanding = useIslanding

	elif usePlAuc:
		uncc = PaCurtCtrl("LoadController-House-"+str(houseNum), unc, ctrl, sim)
		uncc.perfectPredictions = usePP							# Use perfect predictions or not
		uncc.useEventControl = useEC							# Use event-based control
		uncc.timeBase = ctrlTimeBase							# TimeBase for controllers
		uncc.strictComfort = not useIslanding
		uncc.islanding = useIslanding
	#From here on, same reasoning applies, so comments become sparse