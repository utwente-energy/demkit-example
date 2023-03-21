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

	if not useALPG:
		print("[MODEL] Cannot add an Whitegoods without proper data! Enable ALPG input")

# WASHING MACHINE
	idx = alpg.indexFromFile(alpgFolder+"WashingMachine_Starttimes.txt", houseNum)
	if idx != -1:
		wm = TsDev("WashingMachine-House-"+str(houseNum),  sim) # same name, host
		# Static profile, complex numbers ot reflect reactive power
		wm.profile = [complex(66.229735, 77.4311402954),complex(119.35574, 409.21968),complex(162.44595, 516.545199388),complex(154.744551, 510.671236335),complex(177.089979, 584.413201848),complex(150.90621, 479.851164854),complex(170.08704, 540.84231703),complex(134.23536, 460.23552),complex(331.837935, 783.490514121),complex(2013.922272, 587.393996),complex(2032.267584, 592.744712),complex(2004.263808, 584.576944),complex(2023.32672, 590.13696),complex(2041.49376, 595.43568),complex(2012.8128, 587.0704),complex(2040.140352, 595.040936),complex(1998.124032, 582.786176),complex(2023.459776, 590.175768),complex(1995.309312, 581.965216),complex(2028.096576, 591.528168),complex(1996.161024, 582.213632),complex(552.525687, 931.898925115),complex(147.718924, 487.486021715),complex(137.541888, 490.4949133),complex(155.996288, 534.844416),complex(130.246299, 464.477753392),complex(168.173568, 497.908089133),complex(106.77933, 380.79103735),complex(94.445568, 323.813376),complex(130.56572, 317.819806804),complex(121.9515, 211.226194059),complex(161.905679, 360.175184866),complex(176.990625, 584.085324519),complex(146.33332, 501.71424),complex(173.06086, 593.35152),complex(145.07046, 517.342925379),complex(188.764668, 522.114985698),complex(88.4058, 342.394191108),complex(117.010432, 346.43042482),complex(173.787341, 326.374998375),complex(135.315969, 185.177207573),complex(164.55528, 413.181298415),complex(150.382568, 515.597376),complex(151.517898, 540.335452156),complex(154.275128, 509.122097304),complex(142.072704, 506.652479794),complex(171.58086, 490.815333752),complex(99.13293, 368.167736052),complex(94.5507, 366.193286472),complex(106.020684, 378.085592416),complex(194.79336, 356.012659157),complex(239.327564, 302.865870739),complex(152.75808, 209.046388964),complex(218.58576, 486.26562702),complex(207.109793, 683.481346289),complex(169.5456, 581.2992),complex(215.87571, 712.409677807),complex(186.858018, 573.073382584),complex(199.81808, 534.79864699),complex(108.676568, 403.611655607),complex(99.930348, 356.366544701),complex(151.759998, 358.315027653),complex(286.652289, 300.697988258),complex(292.921008, 266.244164873),complex(300.5829, 265.089200586),complex(296.20425, 261.22759426),complex(195.74251, 216.883021899),complex(100.34136, 260.038063655),complex(312.36975, 275.4842252),complex(287.90921, 261.688800332),complex(85.442292, 140.349851956),complex(44.8647, 109.208529515)]
		wm.timeBase = 60		# NOTE: TimeBase of the dataset
		wm.strictComfort = not useIslanding

		# Add all jobs
		for j in range(0,  len(wm_starttimes[idx])):
			wm.addJob(wm_starttimes[idx][j],  wm_endtimes[idx][j])

		if useMC:
			wm.commodities = [commodities[phase%3]]

		sm.addDevice(wm)

		if useCtrl or useAdmm:
			#add a controller for the Timeshitable
			wmc = TsCtrl("WashingMachineController-House-"+str(houseNum),  wm,  ctrl,  sim) 	# params: name, device, higher-level controller, simHost
			wmc.perfectPredictions = usePP						# Same tricks
			wmc.useEventControl = useEC
			wmc.timeBase = ctrlTimeBase

			wmc.commodities = list(wm.commodities)
			wmc.weights = dict(weights)
		elif useAuction:
			wmc = TsAuctionCtrl("WashingMachineController-House-"+str(houseNum),  wm,  ctrl,  sim) 	# This time: (<name>, <device to be controlled>, <parent controller>, <host>)
			wmc.strictComfort = not useIslanding
			wmc.islanding = useIslanding

		elif usePlAuc:
			wmc = PaTsCtrl("WashingMachineController-House-"+str(houseNum),  wm,  ctrl,  sim)
			wmc.perfectPredictions = usePP						# Same tricks
			wmc.useEventControl = useEC
			wmc.timeBase = ctrlTimeBase
			wmc.strictComfort = not useIslanding
			wmc.islanding = useIslanding

# DISHWASHER
	# Follows the exact same reasoning as the Washing Machine above
	idx = alpg.indexFromFile(alpgFolder+"Dishwasher_Starttimes.txt", houseNum)
	if idx != -1:
		dw = TsDev("DishWasher-House-"+str(houseNum), sim)
		dw.profile =[complex(2.343792, 9.91720178381),complex(0.705584, 8.79153133754),complex(0.078676, 7.86720661017),complex(0.078744, 7.87400627016),complex(0.078948, 7.89440525013),complex(0.079152, 7.91480423011),complex(0.079016, 7.90120491012),complex(0.078812, 7.88080593015),complex(0.941108, 3.10574286964),complex(10.449, 18.0981988883),complex(4.523148, 1.78766247656),complex(34.157214, 15.5624864632),complex(155.116416, 70.6731270362),complex(158.38641, 72.1629803176),complex(158.790988, 67.6446776265),complex(158.318433, 72.1320090814),complex(158.654276, 67.5864385584),complex(131.583375, 109.033724507),complex(13.91745, 13.0299198193),complex(4.489968, 1.91271835851),complex(1693.082112, 669.148867416),complex(3137.819256, 447.115028245),complex(3107.713851, 442.825240368),complex(3120.197256, 444.604029241),complex(3123.464652, 445.069607955),complex(3114.653256, 443.814052026),complex(3121.27497, 444.757595169),complex(3116.305863, 444.04953577),complex(3106.801566, 442.695246796),complex(3117.703743, 444.248722882),complex(3118.851648, 444.412290486),complex(3110.016195, 443.15330662),complex(3104.806122, 442.410911425),complex(1148.154728, 416.724520071),complex(166.342624, 70.8616610914),complex(161.205252, 68.6731497838),complex(160.049824, 68.1809395169),complex(158.772588, 67.6368392593),complex(158.208076, 67.3963581543),complex(157.926096, 67.2762351774),complex(157.01364, 66.8875305491),complex(112.30272, 108.243298437),complex(11.65632, 9.35164905552),complex(17.569056, 18.4299236306),complex(4.947208, 2.10750178285),complex(4.724016, 2.012422389),complex(143.12025, 65.2075123351),complex(161.129536, 68.6408949029),complex(160.671915, 63.501604078),complex(23.764224, 12.8265693277),complex(136.853808, 62.352437012),complex(159.11184, 62.8850229849),complex(159.464682, 63.0244750664),complex(159.04302, 62.8578235805),complex(36.68544, 55.7061505818),complex(9.767628, 7.07164059421),complex(4.902772, 2.08857212612),complex(2239.315008, 885.033921728),complex(3116.846106, 444.126516228),complex(3111.034014, 443.298337972),complex(3118.112712, 444.306997808),complex(3111.809778, 443.408878355),complex(3113.442189, 443.641484325),complex(3110.529708, 443.226478259),complex(3104.676432, 442.392431601),complex(3101.093424, 441.881880613),complex(3121.076178, 444.729268843),complex(1221.232208, 443.248103556),complex(159.964185, 63.2218912841),complex(2663.07828, 966.568347525),complex(272.524675, 436.038267268),complex(7.76832, 5.82624),complex(3.258112, 1.75854256572),complex(3.299408, 1.69033685682),complex(3.295136, 1.68814824631),complex(3.256704, 1.75778260783),complex(3.258112, 1.75854256572),complex(3.262336, 1.7608224394),complex(2224.648744, 807.439674778),complex(367.142872, 587.426961418),complex(4.711025, 11.8288968082)]
		dw.timeBase = 60
		dw.strictComfort = not useIslanding

		for j in range(0,  len(dw_starttimes[idx])):
			dw.addJob(dw_starttimes[idx][j],  dw_endtimes[idx][j])

		if useMC:
			dw.commodities = [commodities[phase%3]]

		sm.addDevice(dw)

		if useCtrl or useAdmm:
			dwc = TsCtrl("DishWasherController-House-"+str(houseNum), dw, ctrl, sim)
			dwc.perfectPredictions = usePP
			dwc.useEventControl = useEC
			dwc.timeBase = ctrlTimeBase
			dwc.weights = dict(weights)
			dwc.commodities = list(dw.commodities)

		elif useAuction:
			dwc = TsAuctionCtrl("DishWasherController-House-"+str(houseNum),  dw,  ctrl,  sim) 	# This time: (<name>, <device to be controlled>, <parent controller>, <host>)
			dwc.strictComfort = not useIslanding
			dwc.islanding = useIslanding

		elif usePlAuc:
			dwc = PaTsCtrl("DishWasherController-House-"+str(houseNum), dw, ctrl, sim)
			dwc.perfectPredictions = usePP						# Same tricks
			dwc.useEventControl = useEC
			dwc.timeBase = ctrlTimeBase
			dwc.strictComfort = not useIslanding
			dwc.islanding = useIslanding
