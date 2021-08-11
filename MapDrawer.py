import sys
from argparse import ArgumentParser
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario
from AoE2ScenarioParser.datasets.terrains import TerrainId
from AoE2ScenarioParser.datasets.players import PlayerId
from PIL import Image, ImageDraw
from enum import Enum
import math
import random

TERRAIN_COLORS={
    0:  (152,184,82 ), # GRASS_1
    1:  (42, 125,171), # WATER_SHALLOW
    2:  (238,198,157), # BEACH
    3:  (186,170,115), # DIRT_3
    4:  (108,207,208), # SHALLOWS
    5:  (112,64,32  ), # UNDERBRUSH
    6:  (215,150,86 ), # DIRT_1
    7:  (103,112,7  ), # FARM
    8:  (215,195,151), # FARM_DEAD
    9:  (112,136,62 ), # GRASS_3
    10: (41, 51, 0  ), # FOREST_OAK
    11: (167,145,65 ), # DIRT_2
    12: (134,162,72 ), # GRASS_2
    13: (106,83,39  ), # FOREST_PALM_DESERT
    14: (255,210,153), # DESERT_SAND
    15: (66, 0,  255), # WATER_2D_SHORELESS
    16: (146,162,111), # GRASS_OTHER
    17: (2,  106,0  ), # FBOREST_JUNGLE
    18: (156,71,21  ), # FOREST_BAMBOO
    19: (0,  66, 28 ), # FOREST_PINE
    20: (17, 51, 0  ), # FOREST_OAK_BUSH
    21: (87, 128,105), # FOREST_PIN_SNOW
    22: (43, 88, 132), # WATER_DEEP
    23: (31, 90, 142), # WATER_MEDIUM
    24: (227,162,162), # ROAD
    25: (253,176,139), # ROAD_BROKEN
    26: (161,198,232), # ICE_NAVIGABLE
    27: (195,191,89 ), # GRASS_FOUNDATION
    28: (0,  0,  255), # WATER_2D_BRIDGE
    29: (139,141,117), # FARM_0
    30: (145,152,73 ), # FARM_33
    31: (133,142,37 ), # FARM_67
    32: (236,236,236), # SNOW
    35: (184,205,224), # ICE
    36: (200,200,200), # SNOW_FOUNDATION
    37: (132,176,212), # BEACH_ICE 
    40: (145,134,123), # ROCK_1
    41: (176,131,86 ), # DIRT_SAVANNAH
    42: (210,160,70 ), # DIRT_4
    45: (200,155,102), # DESERT_CRACKED
    46: (162,134,107), # DESERT_QUICKSAND
    47: (0,  0,  0  ), # BLACK
    48: (51, 77, 60 ), # FOREST_DRAGON_TREE
    49: (113,68,41  ), # FOREST_BAOBAB
    50: (65, 65, 0  ), # FOREST_ACACIA
    51: (187,201,163), # BEACH_WHITE_VEGETATION
    52: (155,146,94 ), # BEACH_VEGETATION 
    53: (239,223,210), # BEACH_WHITE
    54: (51, 163,164), # SHALLOWS_MANGROVE
    55: (1,  71, 62 ), # FOREST_MANGROVE
    56: (2,  40, 0  ), # FOREST_RAINFOREST
    57: (29, 61, 94 ), # WATER_DEEP_OCEAN
    58: (21, 169,195), # WATER_AZURE
    59: (19, 222,224), # SHALLOWS_AZURE
    60: (111,152,24 ), # GRASS_JUNGLE
    63: (69, 112,79 ), # RICE_FARM
    64: (143,168,174), # RICE_FARM_DEAD
    65: (92, 132,151), # RICE_FARM_0
    66: (96, 139,123), # RICE_FARM_33
    67: (87, 133,99 ), # RICE_FARM_67
    70: (205,187,177), # GRAVEL_DEFAULT
    71: (180,184,73 ), # UNDERBUSH_LEAVES 
    72: (244,218,189), # UNDERBUSH_SNOW 
    73: (255,255,255), # SNOW_LIGHT 
    74: (219,219,219), # SNOW_STRONG 
    75: (162,139,139), # ROAD_FUNGUS
    76: (239,119,47 ), # DIRT_MUD
    77: (83, 91, 39 ), # UNDERBUSH_JUNGLE 
    78: (234,139,139), # ROAD_GRAVEL
    79: (217,181,142), # BEACH_NON_NAVIGABLE 
    80: (178,143,114), # BEACH_NON_NAVIGABLE_WET_SAND 
    81: (144,129,113), # BEACH_NON_NAVIGABLE_WET_GRAVEL 
    82: (81, 74, 56 ), # BEACH_NON_NAVIGABLE_WET_ROCK 
    83: (98, 130,30 ), # GRASS_JUNGLE_RAINFOREST
    88: (53, 68, 0  ), # FOREST_MEDITERRANEAN
    89: (62, 102,51 ), # FOREST_BUSH
    90: (98, 98, 174), # FOREST_REEDS_SHALLOWS
    91: (114,114,136), # FOREST_REEDS_BEACH
    92: (71, 71, 96 ), # FOREST_REEDS
    95: (102,142,84 ), # WATER_GREEN 
    96: (147,121,75 ), # WATER_BROWN 
    100:(139,136,62 ), # GRASS_DRY
    101:(115,155,124), # SWAMP_BOGLAND 
    102:(215,165,138), # GRAVEL_DESERT
    104:(65, 32, 0  ), # FOREST_AUTUMN
    105:(142,124,107), # FOREST_AUTUMN_SNOW
    106:(69, 73,  68), # FOREST_DEAD
    107:(199,164,140), # BEACH_WET
    108:(168,147,135), # BEACH_WET_GRAVEL
    109:(90, 79,  65), # BEACH_WET_ROCK
}
GROUND_COVER_TYPES = {
    # ID   Tree(s)            Weights          # Terrain
    # TREES
    10:    ((411,           ),(1000,        )),# FOREST_OAK
    13:    ((351,           ),(1000,        )),# FOREST_PALM_DESERT
    17:    ((414,           ),(1000,        )),# FOREST_JUNGLE
    18:    ((348,           ),(1000,        )),# FOREST_BAMBOO
    19:    ((350,           ),(1000,        )),# FOREST_PINE
    20:    ((302,1053,349   ),(200,300,1000,)),# FOREST_OAK_BUSH
    21:    ((413,           ),(1000,        )),# FOREST_PINE_SNOW
    48:    ((1051,          ),(1000,        )),# FOREST_DRAGON_TREE
    49:    ((1052,          ),(250,         )),# FOREST_BAOBAB
    50:    ((1063,          ),(500,         )),# FOREST_ACACIA
    55:    ((1144,          ),(800,         )),# FOREST_MANGROVE
    56:    ((1146,          ),(1000,        )),# FOREST_RAINFOREST
    88:    ((1347,1349,1348 ),(100,500,1000,)),# FOREST_MEDITERRANEAN
    89:    ((302,1053,      ),(400,800,     )),# FOREST_BUSH
    90:    ((1350,          ),(1000,        )),# FOREST_REEDS_SHALLOWS
    91:    ((1350,          ),(1000,        )),# FOREST_REEDS_BEACH
    92:    ((1350,          ),(1000,        )),# FOREST_REEDS
    104:   ((1248,          ),(1000,        )),# FOREST_AUTUMN
    105:   ((1249,          ),(1000,        )),# FOREST_AUTUMN_SNOW
    106:   ((1054,1250      ),(300,1000     )),# FOREST_DEAD
    
    # OTHER GROUND COVER
    0:      ((1358,         ),(60,          )), # GRASS
    3:      ((1358,1359,    ),(10,10        )), # DIRT_3
    6:      ((1365,         ),(10,          )), # DIRT
    9:      ((1362,1359     ),(5,60,        )), # GRASS_3
    12:     ((1366,1364,1362,1360,1358),(4,4,4,4,80)), # GRASS_2
    41:     ((1359,         ),(80,          )), # SAVANNAH
    42:     ((1365,1359,    ),(10,10,       )), # DIRT_4
    60:     ((1351,1352,1358),(10,5,60      )), # JUNGLE_GRASS
    83:     ((1354,1355,1358),(10,5,60      )), # JUNGLE_GRASS_RAINFOREST
    100:    ((1359,         ),(80,          )), # DRY_GRASS
}
 
GROUND_COVER_VARIATIONS = {
    # ID:Rotations    Graphical ID
    # TREES
    411: 42,          # 2302
    351: 39,          # 2306
    414: 39,          # 5800
    348: 12,          # 2298
    350: 27,          # 2310
    302: 6,           # 8171
    1053:54,          # 8489
    349: 42,          # 2302
    413: 27,          # 5803
    1051:36,          # 8482
    1052:45,          # 8484
    1063:30,          # 8503
    1144:36,          # 10189
    1146:69,          # 10191
    1347:12,          # 10540
    1349:24,          # 10544
    1348:24,          # 10542
    1350:12,          # 2314
    1248:42,          # 10443
    1249:42,          # 10445
    1054:27,          # 8491
    1250:21,          # 10447
    
    # OTHER GROUND COVER
    1351:8,#11182
    1352:9,#11183
    1353:9,#11184
    1354:0,#11385
    1355:9,#11184
    1358:8,#11195
    1359:8,#11196
    1360:8,#11197
    1361:8,#11198
    1362:8,#11199
    1363:8,#11200
    1364:8,#11201
    1365:8,#11202
    1366:8,#11203
}

class Sizes(Enum):
    TINY = 120
    SMALL = 144
    MEDIUM = 168
    NORMAL = 200
    LARGE = 220
    GIANT = 240
    LUDICROUS = 480
    
class Modes(Enum):
    IMAGE = True
    SCENARIO = False
    
MAX_ELEVATION = 10

# return random choice of tree type using weights as percentage thresholds
# where 1000 = 100%. Some forest types, like baobab or bush, have empty
# space.
# 10 10 10 500
# 357
def wchoice(weights):
    c = random.randrange(0,1000)
    i = -1
    cumulative_weight = 0
    for weight in weights:
        cumulative_weight += weight
        if c < cumulative_weight:
            i = weights.index(weight)
            break
    return i

def get_ground_cover(terrain_id):
    gcs = GROUND_COVER_TYPES[terrain_id][0]
    gc = -1
    i = wchoice(GROUND_COVER_TYPES[terrain_id][1])
    if i != -1:
        gc = gcs[i]
    else:
        gc = -1
    return gc
    
def get_cover_rotation(gc_id):
    if gc_id != -1:
        return random.randrange(0,GROUND_COVER_VARIATIONS[gc_id])
    else:
        return gc_id
        
    
def get_terrain_id(color, terrain_data):
    for key in terrain_data:
        if terrain_data[key] == color:
            return key
        elif terrain_data[key][0] == color[0] and terrain_data[key][1] == color[1] and  terrain_data[key][2] == color[2]:
            return key
    print("Error: no terrain ID found matching "+str(color)+". Check source image for errors.")
    exit()
    
def get_elevation(height):
    height = math.floor(height/(255/MAX_ELEVATION))
    return height
    
def generate_map(infile, outfile, size, heightmap, layermap):
    input_image = Image.open(infile)
    width, height = input_image.size
    
    heightmap_image = None
    if heightmap != None:
        heightmap_image = Image.open(heightmap)
        hwidth, hheight = heightmap_image.size
        
    layermap_image = None
    if layermap != None:
        layermap_image = Image.open(layermap)
        lwidth, lheight = layermap_image.size
    
    # Resize source image to fit target size
    if size != None and (size != input_image.width or size != input_image.height):
        input_image = input_image.resize((size,size), resample=Image.NEAREST)
        width, height = input_image.size
    elif size == None and (width != height or width not in Sizes._value2member_map_):
        print("Please input a square image that matches a default map size, or specify a map size to use.")
        exit()
        
    if heightmap != None:
        if size != None and (size != heightmap_image.width or size != heightmap_image.height):
            heightmap_image = heightmap_image.resize((size,size), resample=Image.NEAREST)
            hwidth, hheight = heightmap_image.size
        elif size == None and (hwidth != height or hwidth not in Sizes._value2member_map_):
            print("Please input a square heightmap that matches a default map size, or specify a map size to use.")
            exit()
            
    if layermap != None:
        if size != None and (size != layermap_image.width or size != layermap_image.height):
            layermap_image = layermap_image.resize((size,size), resample=Image.NEAREST)
            hwidth, hheight = layermap_image.size
        elif size == None and (lwidth != height or lwidth not in Sizes._value2member_map_):
            print("Please input a square layermap that matches a default map size, or specify a map size to use.")
            exit()
        
    if width == Sizes.TINY.value:
        scenario = AoE2DEScenario().from_file('blank_maps\\TINY.aoe2scenario')
    if width == Sizes.SMALL.value:
        scenario = AoE2DEScenario().from_file('blank_maps\\SMALL.aoe2scenario')
    if width == Sizes.MEDIUM.value:
        scenario = AoE2DEScenario().from_file('blank_maps\\MEDIUM.aoe2scenario')
    if width == Sizes.NORMAL.value:
        scenario = AoE2DEScenario().from_file('blank_maps\\NORMAL.aoe2scenario')
    if width == Sizes.LARGE.value:
        scenario = AoE2DEScenario().from_file('blank_maps\\LARGE.aoe2scenario')
    if width == Sizes.GIANT.value:
        scenario = AoE2DEScenario().from_file('blank_maps\\GIANT.aoe2scenario')
    if width == Sizes.LUDICROUS.value:
        scenario = AoE2DEScenario().from_file('blank_maps\\LUDICROUS.aoe2scenario')
        
    map_manager = scenario.map_manager
    unit_manager = scenario.unit_manager
    
    x = 0
    while x < width:
        y = 0
        while y < width:
            color = input_image.getpixel((x,y))
            terrain_id = get_terrain_id(color, TERRAIN_COLORS)
            if heightmap != None:
                height = heightmap_image.getpixel((x,y))[0]
            map_manager.terrain[y*width+x].terrain_id = terrain_id
            if heightmap != None:
                map_manager.terrain[y*width+x].elevation = get_elevation(height)
            if layermap != None:
                lcolor = layermap_image.getpixel((x,y))
                if lcolor != (0,0,0,0):
                    lterrain_id = get_terrain_id(lcolor, TERRAIN_COLORS)
                    map_manager.terrain[y*width+x].layer = lterrain_id
            for key in GROUND_COVER_TYPES:
                if key == terrain_id:
                    gc_id = get_ground_cover(terrain_id)
                    gc_rot = get_cover_rotation(gc_id)
                    if gc_id != -1:
                        gc = unit_manager.add_unit(
                            player = PlayerId.GAIA,
                            unit_const = gc_id,
                            x=x+0.5,
                            y=y+0.5,
                            rotation=gc_rot
                        )
            y+=1
        x+=1
    
    scenario.write_to_file(outfile)
    
    
def generate_images(infile, outfile, heightmap):
    scenario = AoE2DEScenario().from_file(infile)
    map_manager = scenario.map_manager
    size = map_manager.map_size
    terrain = map_manager.terrain
    out_image = Image.new('RGB', (size,size))
    draw_out = ImageDraw.Draw(out_image)
    
    if heightmap != None:
        out_image_height = Image.new('RGB', (size,size))
        draw_out_height = ImageDraw.Draw(out_image_height)
        
    x = 0
    while x < size:
        y = 0
        while y < size:
            terrain_tile = terrain[x + y*size]
            terrain_type = terrain_tile.terrain_id
            draw_out.point((x,y), fill=TERRAIN_COLORS[terrain_type])
            if heightmap != None:
                terrain_height = int(terrain_tile.elevation/MAX_ELEVATION * 255)+1
                height_color = (terrain_height,terrain_height,terrain_height)
                draw_out_height.point((x,y), fill=height_color)
            y+=1
        x+=1
        
    out_image.save(outfile, "PNG")
    
    if heightmap != None:
        out_image_height.save(heightmap, "PNG")
        
    print("Images generated successfully.")
    exit()

def draw_map(infile, outfile, mode, size, heightmap, layermap):
    if (infile != None and outfile != None):
        pass
    else:
        print("Please specify both an input path and an output path.")
    if (mode != None):
        mode = getattr(Modes, mode)
    else:
        print("Please specify an output mode (IMAGE or SCENARIO)")
        exit()
    if (size != None):
        try:
            size = getattr(Sizes, size).value
        except AttributeError:
            print("Valid map size options are TINY, SMALL, MEDIUM, NORMAL, LARGE, GIANT, or LUDICROUS.")
            exit()
    
    
    if mode == Modes.IMAGE:
        generate_images(infile, outfile, heightmap)
    if mode == Modes.SCENARIO:
        generate_map(infile, outfile, size, heightmap, layermap)
    

if __name__ == "__main__":
    parser = ArgumentParser(
        prog="AoE2DEMapGenerator",
        description="Creates an AoE2DE map from a source image.")
    parser.add_argument("INFILE", help="Source file (*.aoe2scenario or image file)")
    parser.add_argument("OUTFILE", help="Output file (*.aoe2scenario or image file)")
    parser.add_argument('MODE', help='Which output mode to use: scenario to IMAGE, or image to SCENARIO')
    parser.add_argument('-s', '--size', help='Output file size for SCENARIO mode: TINY (120x120), SMALL (144x144), MEDIUM (168x168), NORMAL (200x200), LARGE (220x220), GIANT (240x240), or LUDICROUS (480x480)')
    parser.add_argument('-hm', '--heightmap', help='Specify a path for including height data in either the input or output')
    parser.add_argument('-lm','--layermap',help='Specify a path for including layered terrain decoration when building a scenario.')
    args = parser.parse_args()
    draw_map(args.INFILE, args.OUTFILE, args.MODE, args.size, args.heightmap, args.layermap)