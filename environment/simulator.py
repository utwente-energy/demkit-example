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

##### HERE STARTS THE REAL MODEL DEFINITION OF THE HOUSE TO BE SIMULATED #####
# First we need to instantiate the Host environment:
sim = SimHost()

#Some simulation settings
sim.timeBase = timeBase
sim.timeOffset = timeOffset
sim.timezone = timeZone
sim.intervals = intervals
sim.startTime = startTime
sim.db.database = database
sim.db.prefix = dataPrefix
# Use the following flags to log more/less details (significantly influences simulation speed)
sim.extendedLogging = extendedLogging
sim.logDevices = logDevices
sim.logControllers = True 	# NOTE: Controllers do not log so much, keep this on True (default)!
sim.logFlow = False
sim.enablePersistence = enablePersistence
if clearDB:
	sim.clearDatabase() 	# Removes and creates a database
