AoE2 Map Drawer

A small script for turning images into AoE2 DE scenario files, or for making a map out of an already-existing scenario file. Syntax is:

C:\>python MapDrawer.py INFILE OUTFILE MODE [-s SIZE] [-hm HEIGHTMAP]

where INFILE is the path to the source scenario or image, OUTFILE is the path to write the output to, MODE is whether you want to go scenario -> IMAGE or image -> SCENARIO, -s is an option size parameter for specifying the size of the resulting map in SCENARIO mode, and -hm is an optional parameter for outputting a heightmap also (in IMAGE mode), or for including elevation data in the scenario file (in SCENARIO mode).

This script uses Pillow (https://pillow.readthedocs.io/en/stable/) and the AoE2ScenarioParser module by KSneijders, which can be installed using pip ('pip install AoE2ScenarioParser') or found on GitHub at https://github.com/KSneijders/AoE2ScenarioParser.

To convert an image to a scenario file, the image should use pixels of one color for each terrain type. The color to terrain ID mapping is found in the TERRAIN_COLORS dict in MapDrawer.py. Forest terrains should now correctly generate the associated tree types at about the frequency found in the Scenario Editor, but note that other terrain types do *not* generate normal eyecandy. You can change what units (Gaia or otherwise) are generated with what terrain by messing around with the TREE_TYPES and TREE_VARIATIONS dicts.