AoE2 Map Drawer 

A small script for turning images into AoE2 DE scenario files, or for making a map out of an already-existing scenario file. Syntax is: 

C:\>python MapDrawer.py INFILE OUTFILE MODE [-s SIZE] [-hm HEIGHTMAP] [-lm LAYERMAP] 

where INFILE is the path to the source scenario or image, OUTFILE is the path to write the output to, MODE is whether you want to go scenario -> IMAGE or image -> SCENARIO. -s is an optional size parameter for specifying the size of the resulting map in SCENARIO mode. Additionally, -hm is an optional parameter for outputting a heightmap also (in IMAGE mode), or for including elevation data in the scenario file (in SCENARIO mode); and -lm is an optional parameter for inputting a separate layer map that will add layer terrains as specified (by color, as in the terrain map), with transparent areas being ignored. 

This script uses Pillow (https://pillow.readthedocs.io/en/stable/) and the AoE2ScenarioParser module by KSneijders, which can be installed using pip ('pip install AoE2ScenarioParser') or found on GitHub at https://github.com/KSneijders/AoE2ScenarioParser. 

To convert an image to a scenario file, the image should use pixels of one color for each terrain type. The color to terrain ID mapping is found in the TERRAIN_COLORS dict in MapDrawer.py. 

Terrains should now correctly generate the associated tree types and ground scatter at about the frequency found in the Scenario Editor. You can change what objects (Gaia or otherwise) are generated with what terrain by messing around with the GROUND_COVER_TYPES and GROUND_COVER_VARIATIONS dicts.