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

# ELECTRIC VEHICLE
	# Add an electric vehicle, for which a buffer-timeshiftable is required
	idx = alpg.indexFromFile(alpgFolder+"ElectricVehicle_Specs.txt", houseNum)
	if not useALPG:
		print("[MODEL] Cannot add an EV without proper data! Enable ALPG input")

	if idx != -1:
		ev = BtsDev("ElectricVehicle-House-"+str(houseNum),  sim)	# params: name, simHost
		#Set the parameters:
		if not useALPG:
			ev.capacity = 100000 			# Tesla Model X maxed out
			ev.chargingPowers = [0, 7400] 	# Up to 32A home charging
		else:
			ev.capacity = ev_specs[idx][0]				# Capacity in Wh
			ev.chargingPowers = [0, ev_specs[idx][1]]	# Charging powers, NOTE: PER PHASE IN N PHASE CHARGING
														# NOTE! For the case where only charging 0 or charging between a min and max bound is allowed, "ev.chargingPowers" must have the form "[0, min, max]". bts.ctr. will automatically use the correct EV algorithm for such inputs
			# ChargingPowers is either:
			# 		- a list of possible states (including 0), if discrete is True
			# 		- or a minimum and maximum (thus 2 values) if discrete is False

		if useMC:
			# Now we use default 3 phase charging
			ev.chargingPowers = [0, 22000/3] # Charging power is given per phase!
			ev.commodities = list(commodities)

		ev.soc = ev.capacity 			# recommended to sync (initial)soc and capacity
		ev.discrete = False				# Use discrete chargingsteps instead?
		ev.strictComfort = not useIslanding


		#  System to add charging jobs
		for j in range(0,  len(ev_energy[idx])):
			if min(ev_energy[idx][j], ev.capacity) > 0:
				ev.addJob(ev_starttimes[idx][j],  ev_endtimes[idx][j],  min(ev_energy[idx][j], ev.capacity))
				# Optionally, another parameter can be provided that specifies the EV type, i.e., ev.addJob(ev_starttimes[idx][j],  ev_endtimes[idx][j],  min(ev_energy[idx][j], ev.capacity), ev_type)

		# Decide between Hybrid PHEV or FEV:
		if ev.capacity < 15000:
			ev.hybrid = True
		else:
			ev.hybrid = False

		sm.addDevice(ev)

		if useCtrl or useAdmm:
			#add a controller for the EV.
			#Note, we need to give it a name, connect it to the EV, connect it to the group controller and finally connect it to the host:
			evc = BtsCtrl("ElectricVehicleController-House-"+str(houseNum),  ev,  ctrl,  sim) 	# params: name, device, higher-level controller, simHost
			#Controller params
			evc.perfectPredictions = usePP
			evc.useEventControl = useEC
			evc.timeBase = ctrlTimeBase
			evc.weights = dict(weights)
			evc.commodities = list(ev.commodities)

		elif useAuction:
			evc = BtsAuctionCtrl("ElectricVehicleController-House-"+str(houseNum),  ev,  ctrl,  sim)
			evc.strictComfort = not useIslanding
			evc.islanding = useIslanding

		elif usePlAuc:
			evc = PaBtsCtrl("ElectricVehicleController-House-"+str(houseNum),  ev,  ctrl,  sim)
			evc.perfectPredictions = usePP
			evc.useEventControl = useEC
			evc.timeBase = ctrlTimeBase
			evc.strictComfort = not useIslanding
			evc.islanding = useIslanding