import sys
from argparse import ArgumentParser
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario
from AoE2ScenarioParser.datasets.terrains import TerrainId
from PIL import Image, ImageDraw
from enum import Enum
import math

TERRAIN_COLORS={
    0:(152,184,82),
    1:(42,125,171),
    2:(238,198,157),
    3:(186,170,115),
    4:(108,207,208),
    5:(112,64,32),
    6:(215,150,86),
    7:(103,112,7),
    8:(215,195,151),
    9:(112,136,62),
    10:(41,51,0),
    11:(167,145,65),
    12:(134,162,72),
    13:(106,83,39),
    14:(255,210,153),
    15:(66,0,255),
    16:(146,162,111),
    17:(2,106,0),
    18:(156,71,21),
    19:(0,66,28),
    20:(17,51,0),
    21:(87,128,105),
    22:(43,88,132),
    23:(31,90,142),
    24:(227,162,162),
    25:(253,176,139),
    26:(161,198,232),
    27:(195,191,89),
    28:(0,0,255),
    29:(139,141,117),
    30:(145,152,73),
    31:(133,142,37),
    32:(236,236,236),
    35:(184,205,224),
    36:(200,200,200),
    37:(132,176,212),
    40:(145,134,123),
    41:(176,131,86),
    42:(210,160,70),
    45:(200,155,102),
    46:(162,134,107),
    47:(0,0,0),
    48:(51,77,60),
    49:(113,68,41),
    50:(65,65,0),
    51:(187,201,163),
    52:(155,146,94),
    53:(239,223,210),
    54:(51,163,164),
    55:(1,71,62),
    56:(2,40,0),
    57:(29,61,94),
    58:(21,169,195),
    59:(19,222,224),
    60:(111,152,24),
    63:(69,112,79),
    64:(143,168,174),
    65:(92,132,151),
    66:(96,139,123),
    67:(87,133,99),
    70:(205,187,177),
    71:(180,184,73),
    72:(244,218,189),
    73:(255,255,255),
    74:(219,219,219),
    75:(162,139,139),
    76:(239,119,47),
    77:(83,91,39),
    78:(234,139,139),
    79:(217,181,142),
    80:(178,143,114),
    81:(144,129,113),
    82:(81,74,56),
    83:(98,130,30),
    88:(53,68,0),
    89:(62,102,51),
    90:(98,98,174),
    91:(114,114,136),
    92:(71,71,96),
    95:(102,142,84),
    96:(147,121,75),
    100:(139,136,62),
    101:(115,155,124),
    102:(215,165,138),
    104:(65,32,0),
    105:(142,124,107),
    106:(69,73,68),
    107:(199,164,140),
    108:(168,147,135),
    109:(90,79,65)
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
    
MAX_ELEVATION = 7
    
def get_terrain_id(color, terrain_data):
    for key in terrain_data:
        if terrain_data[key] == color:
            return key
    print("Error: no terrain ID found matching "+str(color)+". Check source image for errors.")
    exit()
    
def get_elevation(height):
    height = math.floor(height/(255/MAX_ELEVATION))
    return height
    
def generate_map(infile, outfile, size, heightmap):
    input_image = Image.open(infile)
    width, height = input_image.size
    
    heightmap_image = None
    if heightmap != None:
        heightmap_image = Image.open(heightmap)
        hwidth, hheight = heightmap_image.size
    
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
    
    x = 0
    while x < width:
        y = 0
        while y < width:
            color = input_image.getpixel((x,y))
            height = heightmap_image.getpixel((x,y))[0]
            map_manager.terrain[y*width+x].terrain_id = get_terrain_id(color, TERRAIN_COLORS)
            map_manager.terrain[y*width+x].elevation = get_elevation(height)
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
                terrain_height = int(terrain_tile.elevation/12 * 255)
                height_color = (terrain_height,terrain_height,terrain_height)
                draw_out_height.point((x,y), fill=height_color)
            y+=1
        x+=1
        
    out_image = out_image.rotate(90)
    out_image.save(outfile, "PNG")
    
    if heightmap != None:
        out_image_height = out_image_height.rotate(90)
        out_image_height.save(heightmap, "PNG")
        
    print("Images generated successfully.")
    exit()

# If a preexisting map file is provided, and a size is also, the output should resize the input (convert it to
# an image then resize using PIL). If the image output flag is chosen, output an image only.
def draw_map(infile, outfile, mode, size, heightmap):
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
    
    if size != None and mode != Modes.SCENARIO:
        print("'size' parameter is only valid in SCENARIO mode.")
        exit()
    
    
    if mode == Modes.IMAGE:
        generate_images(infile, outfile, heightmap)
    if mode == Modes.SCENARIO:
        generate_map(infile, outfile, size, heightmap)
    

if __name__ == "__main__":
    parser = ArgumentParser(
        prog="AoE2DEMapGenerator",
        description="Creates an AoE2DE map from a source image.")
    parser.add_argument("INFILE", help="Source file (*.aoe2scenario or image file)")
    parser.add_argument("OUTFILE", help="Output file (*.aoe2scenario or image file)")
    parser.add_argument('MODE', help='Which output mode to use: scenario to IMAGE, or image to SCENARIO')
    parser.add_argument('-s', '--size', help='Output file size for SCENARIO mode: TINY (120x120), SMALL (144x144), MEDIUM (168x168), NORMAL (200x200), LARGE (220x220), GIANT (240x240), or LUDICROUS (480x480)')
    parser.add_argument('-hm', '--heightmap', help='Specify a path for including height data in either the input or output')
    args = parser.parse_args()
    draw_map(args.INFILE, args.OUTFILE, args.MODE, args.size, args.heightmap)