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

from datetime import datetime
from pytz import timezone

timeZone = timezone('Europe/Amsterdam')
startTime = int(timeZone.localize(datetime(2023, 1, 29)).timestamp())
timeOffset = -1 * int(timeZone.localize(datetime(2023, 1, 1)).timestamp())

timeBase = 60 # Default timebase
intervals = 7*24*int(3600/timeBase)	# Simulating 7 days of data (calculations based on the timeBase)

# Number of houses, not used in the demohouse:
numOfHouses = 10

# Data storage settings
database = 'dem'					# Database to store results
dataPrefix = ''						# A prefix (optional) can be used to put multiple simulations in one database conveniently. NOTE: Disable the cleardatabase!
clearDB = True						# Clear the database or not. !


# ALPG input
alpgFolder = 'alpg/output/demo/'
useALPG = True	# Use ALPG data

# Logging:
logDevices = True				# When disabled, only overall stats will be logged which saves simulation time to quickly estimate the effects of settings
extendedLogging = False			# Extended logging adds more information (such as reactive power) but slows down the simulation

# Restore data on restart (for demo purposes)
enablePersistence = False

# Enable control:
# NOTE: AT MOST ONE OF THESE MAY BE TRUE! They can all be False, however
useCtrl = True		# Use smart control, defaults to Profile steering
useAuction = False	# Use an auction instead, NOTE useMC must be False!
usePlAuc = False	# Use a planned auction instead (Profile steering planning, auction realization), NOTE useMC must be False!
useAdmm = False		# USe ADMM optimization (under development), only limited options available (usePP, useEC)

# Specific options for control
useCongestionPoints = False	# Use congestionpoints
useIslanding = False		# Use islanding mode

# Specific for device control:
useFillMethod = True		# Use a sort of valley filling approach with only the battery

ctrlTimeBase = 900		# Timebase for controllers
useEC = True			# Use Event-based control
usePP = False			# Use perfect predictions (a.k.a no predictions)
useQ = False			# Perform reactive power optimization
useMC = False			# Use three phases and multicommodity control
# Note either EC or PP should be enabled

pricesElectricity = None #Insert a file, e.g. 'data/prices/apx.csv'
# pricesElectricity = CsvReader(dataSource='data/prices/apx.csv', timeBase=timeBase, column=0, timeOffset=timeOffset)
profileWeight = 1 # For only steering on prices, set to 0. Floats allowed as weight between prices / profile steering

# Example with putting a sine as a price signal instead:
# pricesElectricity = FuncReader(timeOffset = timeOffset)
# pricesElectricity.functionType = "sin"
# pricesElectricity.period = 12*3600
# pricesElectricity.amplitude = -5000
# pricesElectricity.dutyCycle = 0.5
# pricesElectricity.powerOffset = 2500
# profileWeight = 0



# NOTE: No need to modify lines below
if useMC:
	assert(useAuction == False)
	assert(usePlAuc == False)
	assert(useAdmm == False)

### MODEL CREATION ####

# Now it is time to create the complete model using the loaded modules
if useMC:
	commodities = ['EL1', 'EL2', 'EL3']
	weights = {'EL1': (1/3), 'EL2': (1/3), 'EL3': (1/3)}
else:
	commodities = ['ELECTRICITY']
	weights = {'ELECTRICITY': 1}

# Initialize the random seed. Not required, but definitely preferred
random.seed(1337)