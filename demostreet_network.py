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

from util.modelComposer import ModelComposer

composer = ModelComposer("demostreet_network")

# Generic components
composer.add("misc/components.py")
composer.add("settings/settings_demostreet.py")
composer.add("misc/alpgdata.py")

# Add the simulation environment
composer.add("environment/simulator.py")

# Add global environment like the sun and weather
composer.add("environment/global.py")

# Start of the household composition
composer.add("house/connectedhouse.py")
composer.add("house/baseload.py")
composer.add("house/pv.py")
composer.add("house/timeshifters.py")
composer.add("house/electricvehicle.py")
composer.add("house/battery.py")
composer.add("house/thermal.py")
# End of a household definition

# Add a neighbourhood controller
composer.add("street/streetcontrol.py")

# Now instantiate one house and add the startsimulation command
composer.add("networks/network_generator.py")

# make a composition of all these files and load it
composer.compose()
composer.load()
