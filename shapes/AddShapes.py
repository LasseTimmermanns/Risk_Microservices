import glob
import os
import re

import pymongo

dir_path = "C:/Users/Lasse/Programmieren/Risk/shapes/shapes"
extension = ".svg"
def get_files():
    os.chdir(dir_path)
    return [file for file in glob.glob(f"*{extension}")]

def mongo_insert(document, id):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    conn = pymongo.MongoClient('mongodb://python:a92Mqs9f!x@localhost:27017/')
    mydb = myclient["risk"]
    mycol = mydb["shapes"]

    mycol.delete_many({"_id": id})

    x = mycol.insert_one(document)
    print(x)
    myclient.close()

def extract_path(string: str):
    general_regex = r"<path d=\"([^\"]*)\""
    matches = re.search(general_regex, string)

    if matches:    
        return matches.group(1)


files = get_files()
for i, file_name in enumerate(files):
    file = open(f"{dir_path}/{file_name}", "r")
    file_str = file.read()
    id = f"shape-{i}"
    document = {"_id": id, "path": extract_path(file_str), "pos": i}
    file.close()
    mongo_insert(document, id)