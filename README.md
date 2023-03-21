# DEMKit Example Simulation Scenario

This is an example scenario model for simulations with DEMKit. See https://github.com/utwente-energy/demkit for more information on usage of this code. This example can service as a template for the creation of new DEMKit simulation scenarios.

## Generation of input data
Before using the demostreet model, you will need to obtain input data using the Artificial Load Profile Generator (ALPG): https://github.com/utwente-energy/alpg

### Docker based setup
For a Docker based DEMKit installation, it suffices to run the "setup_alpg" script provided (*.bat for Windows, *.sh for UNIX based operating systems) once. Upon starting DEMKit, it will then first generate the data.

### Stand-alone setup
The data can be generated using the command line with the following commands from the main folder (python may need to be replaced by python3 depending on your system):
    
    git clone https://github.com/GENETX/alpg.git
    cd alpg
    python profilegenerator.py -c example -o demo --force

Now you are done. This example contains the right relative paths to include the ALPG output into the model.

## License
This software is made available under the Apache version 2.0 license: https://www.apache.org/licenses/LICENSE-2.0

Note that the ALPG software, that can be used in conjunction, is licensed using GPL version 3.0.

## Contact
In case you need assistance, please contact:

Gerwin Hoogsteen:
- https://people.utwente.nl/g.hoogsteen
- g.hoogsteen [at] utwente [dot] nl
- demgroup-eemcs [at] utwente [dot] nl

