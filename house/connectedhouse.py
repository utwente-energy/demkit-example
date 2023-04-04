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

# Now comes the house model
# This is defined as a function, such that multiple houses can be created easily
# Note that the following function is used in network models, so keeping it this way makes integration of networks convenient
def addHouse(node, coordx, coordy, phase, houseNum):
	# First add add a smart meter
	sm = MeterDev("SmartMeter-House-"+str(houseNum),  sim, list(commodities)) #params: name, simHost
	gm = MeterDev("SmartGasMeter-House-"+str(houseNum),  sim, commodities=['NATGAS'])

	if node is not None:
		node.addMeter(sm, phase)

# ADDING A HEMS
	#add a controller if necessary
	if useCongestionPoints:
		cph = CongestionPoint()
		if useMC:
			for c in commodities:
				cph.setUpperLimit(c, 15*230)
				cph.setLowerLimit(c, -15*230)
		else:
			cph.setUpperLimit('ELECTRICITY', 250) # 3 phase 25A connection power limits
			cph.setLowerLimit('ELECTRICITY', -250)


	if useCtrl:
		if useCongestionPoints:
			ctrl = GroupCtrl("HouseController-House-"+str(houseNum),  sim , rootctrl, cph)
		else:
			ctrl = GroupCtrl("HouseController-House-"+str(houseNum),  sim , rootctrl) #params: name, simHost
		ctrl.minImprovement = 0.001
		ctrl.timeBase = ctrlTimeBase	# 900 is advised hre, must be a multiple of the simulation timeBase
		ctrl.useEventControl = useEC	# Enable / disable event-based control
		ctrl.isFleetController = False 	# Very important to set this right in case of large structures. The root controller needs to be a fleetcontroller anyways. See 4.3 of Hoogsteen's thesis
		ctrl.initialPlan = True
		ctrl.simultaneousCommits = 1
		ctrl.strictComfort = not useIslanding

		ctrl.planHorizon = 2*int(24*3600/ctrlTimeBase)
		ctrl.planInterval = int(24*3600/ctrlTimeBase)
		ctrl.commodities = list(commodities)	# Overwrite the list of commodities
		ctrl.weights = dict(weights)			# Overwrite the weights


	# Or an auction (PowerMatcher) controller
	elif useAuction:
		# The real HEMS
		if useCongestionPoints:
			ctrl = AggregatorCtrl("HouseController-House-"+str(houseNum), rootctrl, sim, cph)
		else:
			ctrl = AggregatorCtrl("HouseController-House-"+str(houseNum), rootctrl, sim)

		ctrl.strictComfort = not useIslanding
		ctrl.islanding = useIslanding


	# Or a combination of the two
	elif usePlAuc:
		if useCongestionPoints:
			ctrl = PaGroupCtrl("HouseController-House-"+str(houseNum),  sim, rootctrl, cph)
		else:
			ctrl = PaGroupCtrl("HouseController-House-"+str(houseNum),  sim, rootctrl)
		ctrl.minImprovement = 0.0001
		ctrl.timeBase = ctrlTimeBase	# 900 is advised hre, must be a multiple of the simulation timeBase
		ctrl.useEventControl = useEC	# Enable / disable event-based control
		ctrl.isFleetController = False 	# Very important to set this right in case of large structures. The root controller needs to be a fleetcontroller anyways. See 4.3 of Hoogsteen's thesis
		ctrl.initialPlan = True 		# Recommended to speed up the process
		ctrl.commodities = list(commodities)	# Overwrite the list of commodities
		ctrl.weights = dict(weights)			# Overwrite the weights
		ctrl.strictComfort = not useIslanding
		ctrl.islanding = useIslanding
		ctrl.planHorizon = 2*int(24*3600/ctrlTimeBase)
		ctrl.planInterval = int(24*3600/ctrlTimeBase)

	elif useAdmm:
		# For now we only support one higher level controller, hence we use a simple object reference:
		ctrl = rootctrl
		# if useCongestionPoints:
		# 	ctrl = AdmmGroupCtrl("HouseController-House-"+str(houseNum),  sim , rootctrl, cp)
		# else:
		# 	ctrl = AdmmGroupCtrl("HouseController-House-"+str(houseNum),  sim , rootctrl) #params: name, simHost
		# ctrl.multipleCommits = False	# Allow multiple commits to speedup the optimization
		# ctrl.maxIters = 20
		# ctrl.timeBase = ctrlTimeBase	# 900 is advised hre, must be a multiple of the simulation timeBase
		# ctrl.useEventControl = useEC	# Enable / disable event-based control
		# ctrl.isFleetController = True 	# Very important to set this right in case of large structures. The root controller needs to be a fleetcontroller anyways. See 4.3 of Hoogsteen's thesis
		# ctrl.initialPlan = False 		# Recommended to speed up the process
		# ctrl.strictComfort = True
		# ctrl.islanding = False
		# ctrl.planHorizon = 2*int(24*3600/ctrlTimeBase)
		# ctrl.planInterval = int(24*3600/ctrlTimeBase)
		#
		# ctrl.commodities = list(commodities)	# Overwrite the list of commodities
		# ctrl.weights = dict(weights)			# Overwrite the weights
