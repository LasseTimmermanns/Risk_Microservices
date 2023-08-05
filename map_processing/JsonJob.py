import json
import pathlib
import re
from random import random
from typing import Dict, List, Tuple

import numpy as np
import PIL.Image
import pymongo
from svgpathtools import parse_path

import PathContains

name_id_dict : Dict[str, int] = {}
parent_dir = pathlib.Path(__file__).parent.resolve()

def get_file_as_string(filepath: str):
    with open(filepath, "r") as file:
        return file.read()

class Territory:
    territories = []

    def __init__(self, name, path, id):
        self.name = name
        self.path = path
        self.id = id
        name_id_dict[name] = id
        Territory.territories.append(self)
        print("Added Territory", name)

    def set_center_x(self, center_x):
        self.center_x = center_x

    def set_center_y(self, center_y):
        self.center_y = center_y

    def set_target_x(self, target_x):
        self.target_x = target_x

    def set_target_y(self, target_y):
        self.target_y = target_y

    def set_borders(self, borders):
        self.borders = borders

    def get_path(self):
        return self.path
    
    def get_name(self):
        return self.name
    
    def get_id(self):
        return self.id
    
    def get_by_id(id):
        return Territory.territories[id]
    
    def __str__(self):
        return self.name + " " + str(self.id)
    
    def to_dict(self):
        # print(json.dumps(self.__dict__))
        return self.__dict__

def generate_territories(full_str: str) -> List[Territory]:
    territories = []    

    territory_str = get_section("territories", full_str)
    general_regex = r"<path id=\"([^\"]*)\".+?(?=d=\")d=\"([^\"]*)\""
    matches = re.finditer(general_regex, territory_str, re.MULTILINE)
    for matchNum, match in enumerate(matches, start=1):    
        name = match.group(1)
        path_str = match.group(2)
        territories.append(Territory(name, path_str, matchNum - 1))

    return territories

def get_section(section_name: str, test_string: str):
    regex = fr'<g id="{section_name}">(.*?)</g>'
    match = re.search(regex, test_string, re.DOTALL)

    if match:
        captured_content = match.group(1)
        return captured_content.strip()
    else:
        raise Exception("No Section found with " + section_name)

def get_dimensions(json: str) -> Tuple[int, int]:
    # dimensions
    border_regex = r"width=\"([^\"]*)\" height=\"([^\"]*)\""
    matches = re.search(border_regex, json)

    if matches:    
        return (matches.group(1), matches.group(2))
    
    raise Exception("No Dimensions found")

def get_borders(json_str : str):
    json_array = json.loads(json_str)

    for entry in json_array:
        territory_name = next(iter(entry))
        border_names = entry[territory_name]

        id = name_id_dict[territory_name]
        borders = []
        for border_name in border_names:
            borders.append(name_id_dict[border_name])
        Territory.get_by_id(id).set_borders(borders)

def generate_display_path(territories: List[Territory]):
    output = ""
    for t in territories:
        output += t.get_path()
    return output

def generate_display_access_matrix(path: str):
    image = PIL.Image.open(path)

    image = image.convert('RGBA')
    pixels = np.array(image.split()[-1])
    pixels_bools = pixels.astype(bool)

    # pixels_lumina = np.array(pixels_bools, dtype=np.uint8) * 255
    # maskImg =  PIL.Image.fromarray(pixels_lumina, mode='L')
    # maskImg.save("./maskImg.jpg")

    list_bools = [layer.tolist() for layer in pixels_bools]
    return list_bools

def generate_cards(territory_count: int):
    cards: List[int] = [-1 for _ in range(territory_count)]

    def append_number(number, times):
        slots_left = cards.count(-1)
        if slots_left < times: 
            raise Exception(f"Can't put {times} {number}s in the list, there are {slots_left} slots left.")
        
        for _ in range(times):
            rand = int(random() * len(cards))
            while(cards[rand] != -1):
                rand += 1
                rand %= len(cards)
            cards[rand] = {"territory_id": rand, "race": number}

    general_amount = int(territory_count / 3)
    
    append_number(0, general_amount)        
    append_number(1, general_amount + 1 if territory_count % 3 >= 2 else general_amount)        
    append_number(2, general_amount + 1 if territory_count % 3 >= 1 else general_amount)        

    #Jokers
    cards += [{"territory": -1, "race": 3}, {"territory": -1, "race": 3}]
    return cards

def get_map_dict(id: str):
    dir = f"{parent_dir}/maps/{id}"
    svg_input = get_file_as_string(f"{dir}/{id}_map.svg")
    territories : List[Territory] = generate_territories(svg_input)

    continents = get_continents(svg_input, territories)

    generate_centers(svg_input, territories)
    generate_targets(svg_input, territories)
    cards = generate_cards(len(territories))

    width, height = get_dimensions(svg_input)

    border_json = get_file_as_string(f"{parent_dir}/maps/{id}/{id}_borders.json")
    get_borders(border_json)

    territory_jsons : List[str] = [t.to_dict() for t in territories]

    display_path = generate_display_path(territories)

    display_access_matrix = generate_display_access_matrix(f"{dir}/{id}_display.png")
    display_height, display_width = np.shape(display_access_matrix)
    risk_map = {'continents': continents, 'territories': territory_jsons, 'cards': cards, 'display_matrix': display_access_matrix, 'display_path': display_path, 'display_width': display_width, 'display_height': display_height, 'svg_width': int(width), 'svg_height': int(height), '_id': id}
    # print(risk_map)
    return risk_map
  
def mongo_insert(document, id):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    conn = pymongo.MongoClient('mongodb://python:a92Mqs9f!x@localhost:27017/')
    mydb = myclient["risk"]
    mycol = mydb["maps"]

    mycol.delete_many({"_id": id})

    x = mycol.insert_one(document)
    print(x)
    myclient.close()

def generate_centers(full_str: str, territories: List[Territory]):
    regex = r"<circle[^>]+cx=\"(\d+)\"\s+cy=\"(\d+)\""  
    centers_str = get_section("centers", full_str)
    matches = re.finditer(regex, centers_str, re.MULTILINE)

    for _, match in enumerate(matches, start=1):    
        center_x = int(match.group(1))
        center_y = int(match.group(2))
        append_center_to_territory(center_x, center_y, territories)

def append_center_to_territory(cx, cy, territories: List[Territory]):
    c = complex(cx, cy)
    for t in territories:
        path = parse_path(t.path)
        if PathContains.path_contains(path, c):
            t.set_center_x(cx)
            t.set_center_y(cy)
            return


def generate_targets(full_str: str, territories: List[Territory]):
    regex = r"<circle[^>]+cx=\"(\d+)\"\s+cy=\"(\d+)\""  
    targets_str = get_section("targets", full_str)
    matches = re.finditer(regex, targets_str, re.MULTILINE)

    for _, match in enumerate(matches, start=1):    
        center_x = int(match.group(1))
        center_y = int(match.group(2))
        append_target_to_territory(center_x, center_y, territories)

def append_target_to_territory(cx, cy, territories: List[Territory]):
    c = complex(cx, cy)
    for t in territories:
        path = parse_path(t.path)
        if PathContains.path_contains(path, c):
            t.set_target_x(cx)
            t.set_target_y(cy)
            return


def get_continents(full_str: str, territories: List[Territory]):
    continents_str = get_section("continents", full_str)

    colors = ["#FF8585", "#C8EEFD", "#FFF0A8", "#75F086", "#ABC4F2", "#FFD257", "#FDD9DF", "#3E00E0"]

    general_regex = r"<path id=\"([^\"]*)\".+?(?=d=\")d=\"([^\"]*)\""
    matches = re.finditer(general_regex, continents_str, re.MULTILINE)
    continents = []
    continents_with_territories = []
    for i, match in enumerate(matches, start=1):    
        name, bonus_troops = match.group(1).split("+")
        continent_path = match.group(2)

        path = parse_path(continent_path)
        current_territories = []
        
        for t in territories:
            if PathContains.path_intersects(path, parse_path(t.get_path())):
                current_territories.append(t)
                print(t.get_name(), "lies in", name)


        continent = {
            "name": name,
            "bonus": int(bonus_troops),
            "hex": colors[i],
            "territories": [t.get_id() for t in current_territories]
        }

        continents.append(continent)
        continents_with_territories.append((name, current_territories))

    regex = r"<circle[^>]+cx=\"(\d+)\"\s+cy=\"(\d+)\""  
    matches = re.finditer(regex, continents_str, re.MULTILINE)

    continents_left = continents.copy()

    for _, match in enumerate(matches, start=1):    
        cx = int(match.group(1))
        cy = int(match.group(2))
        center = complex(cx, cy)

        found = False
        for name, territories in continents_with_territories:
            if found: break
            for t in territories:
                if PathContains.path_contains(parse_path(t.get_path()), center):
                    c = next((item for item in continents if item.get("name") == name), None)
                    print("found center of", name)
                    c["center_x"] = cx
                    c["center_y"] = cy
                    found = True
                    break;                

    return continents


if __name__ == "__main__":
    maps = ["classic", "germany"]

    # maps = ["classic"]
    for map_name in maps:
        name_id_dict : Dict[str, int] = {}
        parent_dir = pathlib.Path(__file__).parent.resolve()
        
        map_dict = get_map_dict(map_name)
        mongo_insert(map_dict, map_name)
        