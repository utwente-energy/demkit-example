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

# Utils
import util.alpg as alpg
# This example shows how to configure a simple model of one household.
# It can be used to test if everything is working correctly
# but also as a template for new models

# Usually we create a couple of global variables which we use for some general settings
# The idea is that we can easily change these parameters for different cases
# Think of using/not using control, or the amount of data to be logged
# Some general, and often useful, variables are:

# Read in raw ALPG output data to configure devices
try:
	ev_starttimes = alpg.listFromFile(alpgFolder+'ElectricVehicle_Starttimes.txt')
	ev_endtimes = alpg.listFromFile(alpgFolder+'ElectricVehicle_Endtimes.txt')
	ev_energy = alpg.listFromFile(alpgFolder+'ElectricVehicle_RequiredCharge.txt')
	ev_specs = alpg.listFromFile(alpgFolder+'ElectricVehicle_Specs.txt')

	wm_starttimes = alpg.listFromFile(alpgFolder+'WashingMachine_Starttimes.txt')
	wm_endtimes = alpg.listFromFile(alpgFolder+'WashingMachine_Endtimes.txt')

	dw_starttimes = alpg.listFromFile(alpgFolder+'Dishwasher_Starttimes.txt')
	dw_endtimes = alpg.listFromFile(alpgFolder+'Dishwasher_Endtimes.txt')

	pv_specs = alpg.listFromFile(alpgFolder+'PhotovoltaicSettings.txt')
	bat_specs = alpg.listFromFile(alpgFolder+'BatterySettings.txt')

	therm_starttimes = alpg.listFromFile(alpgFolder+'Thermostat_Starttimes.txt')
	therm_setpoints = alpg.listFromFile(alpgFolder+'Thermostat_Setpoints.txt')

	heat_specs = alpg.listFromFileStr(alpgFolder+'HeatingSettings.txt')
except:
	print("[ERROR] An error occurred when reading ALPG input data. \n\tPossible causes: \n\t  -Have you generated the data (refer to the README)? \n\t  -Is the variable alpgFolder configured correctly?")
	exit()