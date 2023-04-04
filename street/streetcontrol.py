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

if useCongestionPoints:
	cpstreet = CongestionPoint()
	if useMC:
		for c in commodities:
			cpstreet.setUpperLimit(c,  numOfHouses*500)
			cpstreet.setLowerLimit(c,  -1*numOfHouses*500)
	else:
		cpstreet.setUpperLimit('ELECTRICITY',  numOfHouses*500)
		cpstreet.setLowerLimit('ELECTRICITY',  -1*numOfHouses*500)




# ADD A FLEETCONTROLLER FOR THIS STREET
if useCtrl:
	if useCongestionPoints:
		rootctrl = GroupCtrl("GroupController",  sim, None, cpstreet)
	else:
		rootctrl = GroupCtrl("GroupController",  sim)
	rootctrl.useEventControl = useEC
	rootctrl.minImprovement = 0.001
	rootctrl.planHorizon = 2*int(24*3600/ctrlTimeBase)
	rootctrl.planInterval = int(24*3600/ctrlTimeBase)
	rootctrl.isFleetController = True
	rootctrl.timeBase = ctrlTimeBase
	rootctrl.commodities = list(commodities)
	rootctrl.weights = dict(weights)
	rootctrl.strictComfort = not useIslanding

	if pricesElectricity is not None:
		for c in commodities:
			rootctrl.prices = {}
			rootctrl.prices[c] = pricesElectricity
		rootctrl.profileWeight = profileWeight


elif useAuction:
	# Auctioneer, usually not in the house
	if useCongestionPoints:
		rootctrl = AuctioneerCtrl("Auctioneer",  sim, cpstreet)
	else:
		rootctrl = AuctioneerCtrl("Auctioneer",  sim, None)
	rootctrl.maxGeneration = 0.0    # We try to island here
	rootctrl.minGeneration = 0.0	# Set these two differently, based on an estimated power usage for example
	rootctrl.timeBase = ctrlTimeBase

	rootctrl.strictComfort = not useIslanding
	rootctrl.islanding = useIslanding

elif usePlAuc:
	if useCongestionPoints:
		rootctrl = PaGroupCtrl("GroupController",  sim, None, cpstreet)
	else:
		rootctrl = PaGroupCtrl("GroupController",  sim)
	rootctrl.useEventControl = useEC
	rootctrl.minImprovement = 0.001
	rootctrl.timeBase = ctrlTimeBase
	rootctrl.planHorizon = 2*int(24*3600/ctrlTimeBase)
	rootctrl.planInterval = int(24*3600/ctrlTimeBase)
	rootctrl.isFleetController = True
	rootctrl.timeBase = ctrlTimeBase

	rootctrl.strictComfort = not useIslanding
	rootctrl.islanding = useIslanding

	if pricesElectricity is not None:
		for c in commodities:
			rootctrl.prices = {}
			rootctrl.prices[c] = pricesElectricity
		rootctrl.profileWeight = profileWeight

elif useAdmm:
	if useCongestionPoints:
		rootctrl = AdmmGroupCtrl("GroupController",  sim, None, cpstreet)
	else:
		rootctrl = AdmmGroupCtrl("GroupController",  sim)
	rootctrl.multipleCommits = False	# Allow multiple commits to speedup the optimization
	rootctrl.maxIters = 200 #2.5*numOfHouses
	rootctrl.timeBase = ctrlTimeBase	# 900 is advised hre, must be a multiple of the simulation timeBase
	rootctrl.useEventControl = useEC	# Enable / disable event-based control
	rootctrl.isFleetController = True 	# Very important to set this right in case of large structures. The root controller needs to be a fleetcontroller anyways. See 4.3 of Hoogsteen's thesis
	rootctrl.initialPlan = False 		# Recommended to speed up the process
	rootctrl.strictComfort = True
	rootctrl.planHorizon = 2*int(24*3600/ctrlTimeBase)
	rootctrl.planInterval = int(24*3600/ctrlTimeBase)

	rootctrl.commodities = list(commodities)	# Overwrite the list of commodities
	rootctrl.weights = dict(weights)			# Overwrite the weights