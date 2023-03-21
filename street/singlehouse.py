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

# add a household using the previously defined function
addHouse(None, 0, 0, 1, 0) # Phase must be: 0 < phase < 4
# For a larger group of houses, use a for loop and change the housenumber (and if applicable the phase).
# Usually it is useful to use the dynamic idx-code as well, and multiple input files.

# The last thing to do is starting the simulation!
sim.startSimulation()