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

# AND ADD THE HOUSES BASED ON A STREET MODEL
# Add a load-flow simulator
import math

lfSim = ElLoadFlow("LoadflowSim", sim)

# Legacy lists
networknodes = []
cables = []



#functions to create nodes and edges for the new simulator
def newNode(name):
	node = LvNode(name, lfSim, sim)
	networknodes.append(node) #GERWIN: Yes I know that this is redundant... but this is a dirty way to hack the old models into the python environment
	return node

def newConnection(nodeFrom, nodeTo):
	cable = LvCable("LVCable-"+str(len(cables)), lfSim, nodeFrom, nodeTo, sim)
	cables.append(cable)
	print(nodeFrom.name+" -> "+nodeTo.name)
	return cable

#Functions to set cable properties
def setCableParams0(cable):
	cable.ampacity = 225
	cable.impedance = [complex(0.26, 0.8), complex(0.05, 0.73), complex(0.05, 0.71), complex(0.05, 0.73)]

def setCableParams1(cable):
	cable.ampacity = 170
	cable.impedance = [complex(0.37, 0.81), complex(0.05, 0.74), complex(0.05, 0.72), complex(0.05, 0.74)]

def setCableParams2(cable):
	cable.ampacity = 110
	cable.impedance = [complex(0.69, 0.83), complex(0.05, 0.76), complex(0.051, 0.74), complex(0.05, 0.76)]

def setCableParams3(cable):
	cable.ampacity = 60 #60, house cables not interesting
	cable.impedance = [complex(1.99, 0.83), complex(0.09, 0.74), complex(0.09, 0.72), complex(0.09, 0.74)]


# Creating a network using a generic style that is soemwhat resembling typical dutch grids
# For a more improved version, we might want to add the work by Dickert et al.
# J. Dickert, M. Domagk and P. Schegner. “Benchmark low voltage distribution networks based on cluster analysis of actual grid properties”. PowerTech, 2013 IEEE Grenoble

# Structure:
# Transformator (multiple feeders) -> 150AL (50m) -> 20 houses (150AL, spaced ~6m) -> 150AL (10m) -> Y-fork, within both directions: 10M AL95 -> up to 15 houses spaced ~6m

# First determine the number of houses per feeder
numOfFeeders = math.ceil(numOfHouses/50)
housesPerFeeder = math.ceil(numOfHouses / numOfFeeders)

connectedHouses = 0

networknodes.append(newNode("transformer"))

for f in range(0, int(numOfFeeders)):
	# Keeps the number of houses we need to lay down on this feeder!
	housesLeft = min(housesPerFeeder, (numOfHouses-connectedHouses))

	# Connect the first section:
	networknodes.append(newNode("feeder-"+str(f)))
	lvCable = newConnection(networknodes[0], networknodes[len(networknodes)-1])
	setCableParams0(lvCable)
	lvCable.length = 100.0
	c = len(networknodes)-1

	# Add the first 10 houses
	for h in range(0, int(min(housesLeft, 20))):
		networknodes.append(newNode("feeder-"+str(f)+"-house-"+str(connectedHouses)))
		lvCable = newConnection(networknodes[c], networknodes[len(networknodes)-1])
		setCableParams0(lvCable)
		lvCable.length = 10.0
		c = len(networknodes)-1

		networknodes.append(newNode("houseconnection-"+str(connectedHouses)))

		# Add a house at this point in the network. Params:
		# Node, coordx, coordy, phase (1-3), housenumber
		addHouse(networknodes[len(networknodes)-1], 0, 0, None, connectedHouses)

		connectedHouses += 1
		housesLeft -= 1

		lvCable = newConnection(networknodes[c], networknodes[len(networknodes)-1])
		setCableParams3(lvCable)
		lvCable.length = 6.0

	if housesLeft > 0:
		# Now branch
		networknodes.append(newNode("feeder-"+str(f)+"-tobranch"))
		lvCable = newConnection(networknodes[c], networknodes[len(networknodes)-1])
		setCableParams0(lvCable)
		lvCable.length = 25.0
		j = len(networknodes)-1 # junction point

		# Determine the number of houses por branch:
		housesPerBranch = math.ceil(housesLeft / 2)

		for b in range(0, min(2, housesPerBranch)):
			networknodes.append(newNode("feeder-"+str(f)+"-branch-"+str(b)))
			lvCable = newConnection(networknodes[j], networknodes[len(networknodes)-1])
			setCableParams1(lvCable)
			lvCable.length = 25.0
			c = len(networknodes)-1

			for h in range(0, int(min(housesLeft, 15))):
				networknodes.append(newNode("feeder-"+str(f)+"-branch-"+str(b)+"-house-"+str(connectedHouses)))
				lvCable = newConnection(networknodes[c], networknodes[len(networknodes)-1])
				setCableParams1(lvCable)
				lvCable.length = 10.0
				c = len(networknodes)-1

				networknodes.append(newNode("houseconnection-"+str(connectedHouses)))

				# Add a house at this point in the network. Params:
				# Node, coordx, coordy, phase (1-3), housenumber
				addHouse(networknodes[len(networknodes)-1], 0, 0, None, connectedHouses)

				connectedHouses += 1
				housesLeft -= 1

				lvCable = newConnection(networknodes[c], networknodes[len(networknodes)-1])
				setCableParams3(lvCable)
				lvCable.length = 6.0


#and select the rootNode (slack bus)
lfSim.rootNode = networknodes[0]

# START THE SIMULATION!
# The last thing to do is starting the simulation!
sim.startSimulation()

