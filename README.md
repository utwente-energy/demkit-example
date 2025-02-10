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

## Acknowledgements

The development and maintenance of this software is made possible through the funding from several research projects:

- This work is part of the research programme Energy Autonomous Smart Micro-grids (EASI) with project number 12700 which is financed by the Netherlands Organisation for Scientific Research (NWO).
- This research has been conducted within the SIMPS project (project number 647.002.003). This research is supported by the Dutch Research Council (NWO).
- This research is supported by Rijksdienst voor Ondernemend Nederland (RVO) through project TKI Switch2Smargrids "Smart Grid Evolution" (project number TESG113013). This research is supported by Dr Ten B.V.
- This research is conducted within the Grid Flex Heeten project (project number TEUE116230) supported by the Dutch organisation Rijksdienst voor Ondernemend Nederland (RVO).
- This research is supported by the RVO TKI iDeego ORTEP project.
- This research is funded by the Topsector Energy, part of the Netherlands Enterprise Agency (RVO) and funded by the Dutch Ministry of Economic Affairs as part of the TKI program Switch2Smartgrids, Smart Grid Meppelenergie (project number 01005).
- This research is funded by NWO in the iCARE project (STW project number 11854).
- This work was supported by the Dutch National Program TKI FAIRPLAY Project funded by the Dutch Enterprise Agency (RVO) under Grant TEUE419004.
- This research is conducted within the SmoothEMS met GridShield project subsidized by the Dutch ministries of EZK and BZK (MOOI32005).
- This research is conducted within the Dutch national research programs TKI Urban Energy PPS (project SLIMPARK).
- This project has received funding from the European Union’s Horizon 2020 research and innovation programme under grant agreement No 101022587 (SUSTENANCE).
- This project has received funding from the European Union’s Horizon 2020 research and innovation programme under grant agreement No 957682 (SERENE).
- This research is conducted within the EIGEN (Energy Hubs voor Inpassing van Grootschalige Hemieuwbare Energie) project subsidised by the Dutch ministries EZK. 
-  This research is part of the research program ‘MegaMind- Measuring, Gathering, Mining and Integrating Data for Self-management in the Edge of the Electricity System’, (partly) financed by the Dutch Research Council  (NWO) through the Perspectief program under number P19-25.
