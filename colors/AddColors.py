
import json
import re

import pymongo

import ColorHelper


def mongo_delete_all():
  myclient = pymongo.MongoClient("mongodb://localhost:27017/")
  conn = pymongo.MongoClient('mongodb://python:a92Mqs9f!x@localhost:27017/')
  mydb = myclient["risk"]
  mycol = mydb["colors"]

  print(mycol.delete_many({}))
  myclient.close()

def mongo_insert(document, _id):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    conn = pymongo.MongoClient('mongodb://python:a92Mqs9f!x@localhost:27017/')
    mydb = myclient["risk"]
    mycol = mydb["colors"]

    mycol.delete_many({"_id": _id})

    x = mycol.insert_one(document)
    print(x)
    myclient.close()



# Created using bard.google.com
def get_text_color(background_color):
  """Returns the text color to use for a given background color."""
  background_rgb = tuple(int(background_color[i:i + 2], 16) for i in range(2, 6))
  brightness = 0.299 * background_rgb[0] + 0.587 * background_rgb[1] + 0.114 * background_rgb[2]
  if brightness > 128:
    return "000000"
  else:
    return "FFFFFF"

# Created using bard.google.com
def apply_svg_filter(hex_color):
  """Applies the SVG filter to a hex color and returns the output."""
  hex_color = re.sub("#", "", hex_color)
  rgb_values = [int(hex_color[i:i + 2], 16) for i in range(0, 6, 2)]
  filtered_rgb_values = [int(0.5 * value) for value in rgb_values]
  filtered_hex_color = "".join(["%02x" % value for value in filtered_rgb_values])
  return filtered_hex_color

class Color:
    def __init__(self, _id, hex):
        self._id = _id
        self.hex = hex

    def generate_text_color(self):
        self.text_color = "#"+get_text_color(self.hex)
    
    def generate_secondary_hex(self):
       self.secondary_hex = "#" + apply_svg_filter(self.hex)

    def generate_highlight_hex(self):
       self.highlight_hex = "#" + ColorHelper.change_hsv(self.hex[1:], 0, 1, 0)
    #    print(self.hex, "->", self.highlight_hex)

filename = "light_colors.json"
j = json.load(open(filename, "r"))

colors = []

mongo_delete_all()  
for x in j:
#    print(x)
   c = Color(x["_id"], x["hex"])
   c.generate_text_color()
   c.generate_secondary_hex()
   c.generate_highlight_hex()
   mongo_insert(c.__dict__, c._id)