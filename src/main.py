import os
from typing import Tuple
import amulet
import cv2
from cv2 import Mat
import numpy as np
import time
# from PIL import Image, ImageOps
from amulet.api.errors import ChunkLoadError, ChunkDoesNotExist
from amulet.api.block import Block
from logging import getLogger, StreamHandler, DEBUG
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False

assets_dir = "assets"

if not os.path.isdir(assets_dir):
    raise ValueError("assets are not found.") 


level = amulet.load_level("debug_world")

exclude_blocks = [
    Block("universal_minecraft", "air"),
    Block("universal_minecraft", "barrier"),
    Block("universal_minecraft", "sapling"),
    Block("universal_minecraft", "moving_block"),
    Block("universal_minecraft", "fire"),
    Block("universal_minecraft", "bed"),  # omit
    Block("universal_minecraft", "plant"),
    Block("universal_minecraft", "tall_seagrass"),
    Block("universal_minecraft", "soul_fire"),
    Block("universal_minecraft", "chest"), # omit
    Block("universal_minecraft", "sign"), 
    Block("universal_minecraft", "hanging_sign"), 
    Block("universal_minecraft", "wheat"), 
    Block("universal_minecraft", "door"), 
    Block("universal_minecraft", "wall_sign"), 
    Block("universal_minecraft", "wall_hanging_sign"), 
    Block("universal_minecraft", "trapdoor"), 
    Block("universal_minecraft", "glass_pane"), # omit 
    Block("universal_minecraft", "stained_glass"), # omit 
    Block("universal_minecraft", "pressure_plate"), # omit 
    Block("universal_minecraft", "fence"), # omit 
    Block("universal_minecraft", "button"), # omit 
    Block("universal_minecraft", "fence_gate"), # omit 
    Block("universal_minecraft", "nether_wart"), # omit 
    Block("universal_minecraft", "end_portal"), # omit 
    Block("universal_minecraft", "cocoa"), 
    # ... so on
    ]

def get_top_block(x: int, z: int): 
    for y in reversed(range(-64, 320+1)):
        block = level.get_block(
            x, y, z,
            "minecraft:overworld",
        )
        if isinstance(block, Block):
            valid = True
            for exclude_block in exclude_blocks:
                if (block.namespace == exclude_block.namespace) and (block.base_name == exclude_block.base_name):
                    valid = False
            if valid:
                return block, y
    return Block("universal_minecraft", "air"), -64

hoge = 2

def get_block_minecraft_texture(block: Block) -> np.ndarray:
    block_dir = f"{assets_dir}/minecraft/textures/block"
    if not os.path.isdir(block_dir):
        raise ValueError(f"assets are not found: {block_dir}") 
    
    def get_tex(name: str, enable_color: bool = False, rgb: Tuple[int, int, str] = (0, 0, 0)):
        texture_path = f"{block_dir}/{name}.png"
        if not os.path.isfile(texture_path):
            raise ValueError(f"assets are not found: {texture_path}") 
        texture = cv2.imread(texture_path, cv2.IMREAD_COLOR)
        if texture.shape[0] != texture.shape[1]:
            texture = texture[0 : texture.shape[1], 0: texture.shape[1]]
        texture = cv2.resize(texture, (texture.shape[1] // hoge, texture.shape[1] // hoge))
        if enable_color:
            texture = np.round(texture * np.array([rgb[2] / 255, rgb[1] / 255, rgb[0] / 255])).astype(np.uint8)
        return texture



    if block.base_name == "air":
        return np.zeros((16 // hoge, 16 // hoge, 3), dtype=np.uint8)  
    if (block.base_name == "log") or (block.base_name == "wood"):
        material = block.properties["material"].py_str
        if material == "bamboo": # easy
            return get_tex("bamboo_block")
        return get_tex(f"{material}_log_top")
    if block.base_name == "planks":
        material = block.properties["material"].py_str
        return get_tex(f"{material}_planks")
    if block.base_name == "stairs":
        material = block.properties["material"].py_str
        return get_tex(f"{material}_planks")
    
    if block.base_name == "lava":
        raw_tex = get_tex("lava_still")
        return raw_tex[0 : raw_tex.shape[1], 0: raw_tex.shape[1]]
    
    if block.base_name == "water":
        raw_tex = get_tex("water_still", True, (14, 78, 207)) # meadow
        return raw_tex[0 : raw_tex.shape[1], 0: raw_tex.shape[1]]
    if block.base_name == "leaves":
        return get_tex("oak_leaves", True, (89, 174, 48)) # forest
    if block.base_name == "grass_block":
        return get_tex("grass_block_top", True, (145, 189, 89)) # plains
    
    if block.base_name == "mangrove_roots":
        return get_tex("mangrove_roots_top")
    if block.base_name == "muddy_mangrove_roots":
        return get_tex("muddy_mangrove_roots_top")
    if block.base_name == "podzol":
        return get_tex("podzol_top")
    if block.base_name == "mycelium":
        return get_tex("mycelium_top")
    if block.base_name == "cactus":
        return get_tex("cactus_top")
    if block.base_name == "pumpkin":
        return get_tex("pumpkin_top")
    if (block.base_name == "melon"): # easy
        return get_tex("melon_top") 
    
    
    if block.base_name == "crafting_table":
        return get_tex("crafting_table_top")
    if block.base_name == "jukebox":
        return get_tex("jukebox_top")
    if (block.base_name == "furnace") or (block.base_name == "dispenser"):
        return get_tex("furnace_top") # plains
    
    if block.base_name == "basalt":
        return get_tex("basalt_top")
    if block.base_name == "polished_basalt":
        return get_tex("polished_basalt_top")
    if block.base_name == "cake": # easy
        return get_tex("cake_top")
    
    if (block.base_name == "piston_head") or (block.base_name == "piston"): # easy
        return get_tex("piston_top") 
    if (block.base_name == "sticky_piston_head") or (block.base_name == "sticky_piston"): # easy
        return get_tex("piston_top_sticky") 
    if (block.base_name == "chiseled_bookshelf"):
        return get_tex("chiseled_bookshelf_top") 
    if (block.base_name == "cauldron"):
        return get_tex("cauldron_top") 
    if (block.base_name == "redstone_wire"): # easy
        return get_tex("redstone_dust_dot") 
    
    if (block.base_name == "wool"): # easy, 全て白にする
        return get_tex("white_wool") 
    if (block.base_name == "tnt"):
        return get_tex("tnt_top") 
    if (block.base_name == "enchanting_table"):
        return get_tex("enchanting_table_top") 
    if (block.base_name == "snow_block"):
        return get_tex("snow") 
    
    if (block.base_name == "end_portal_frame"):
        return get_tex("end_portal_frame_top") 
    
    if (block.base_name == "brick_block") or (block.base_name == "brick_planks"):
        return get_tex("bricks") 
    if (block.base_name == "cobblestone_planks"): # easy
        return get_tex("cobblestone") 
    if (block.base_name == "stone_brick_planks"): # easy
        return get_tex("stone_bricks") 
    if (block.base_name == "sandstone_planks"): # easy
        return get_tex("sandstone_top") 
    if (block.base_name == "nether_brick_planks"): # easy
        return get_tex("nether_bricks") 
    if (block.base_name == "mud_brick_planks"): # easy
        return get_tex("mud_bricks") 
    
    if block.base_name == "suspicious_sand":
        return get_tex("suspicious_sand_3")
    if block.base_name == "suspicious_gravel":
        return get_tex("suspicious_gravel_3")
    if (block.base_name == "infested_block"): # easy
        return get_tex("stone_bricks") 
    
    return get_tex(block.base_name)        

def get_pixel_image(x: int, z: int): 
    top_block, y = get_top_block(x, z) 
    try:
        if top_block.namespace == "universal_minecraft":
            tex = get_block_minecraft_texture(top_block)    
        return tex
    except ValueError as e:
        logger.debug(f"({x},{y},{z}): {e}")
        ata = np.zeros((16 // hoge, 16 // hoge, 3), dtype=np.uint8)
        return ata

def get_chunk_image(chunk_x, chunk_z) -> np.ndarray:  
    ong = [ 0.]
    chunk_image = cv2.hconcat(
        [
            cv2.vconcat(
                [ 
                    get_pixel_image(chunk_x * 16 + offset_x, chunk_z * 16 + offset_z)
                    for offset_z in range(16)
                ]
            ) 
            for offset_x in range(16)
        ]
    )
    logger.debug(f"chunk rendered: ({chunk_x}, {chunk_z})")
    return chunk_image

def get_chunks_image(min_chunk_x, max_chunk_x, min_chunk_z, max_chunk_z) -> np.ndarray:
    if (min_chunk_x > max_chunk_x) or (min_chunk_z > max_chunk_z):
        raise ValueError(f"invalid chunk size.") 
        
    chunks_image = cv2.hconcat(
        [
            cv2.vconcat(
                [ 
                    get_chunk_image(chunk_x, chunk_z)
                    for chunk_z in range(min_chunk_z, max_chunk_z + 1)
                ]
            ) 
            for chunk_x in range(min_chunk_x, max_chunk_x + 1)
        ]
    )

    return chunks_image

# cv2.imwrite("test5.png", get_chunks_image(16, 17, 100, 101))

cv2.imwrite("test6.png", get_chunks_image(0, 0, 0, 0))

# level.save()
level.close()