import glob
import os

import pymongo

dir_path = "C:/Users/Lasse/Programmieren/Risk/patterns/patterns"
extension = ".txt"
def get_files():
    os.chdir(dir_path)
    return [file for file in glob.glob(f"*{extension}")]

def mongo_insert(document, id):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    conn = pymongo.MongoClient('mongodb://python:a92Mqs9f!x@localhost:27017/')
    mydb = myclient["risk"]
    mycol = mydb["patterns"]

    mycol.delete_many({"_id": id})

    x = mycol.insert_one(document)
    print(x)
    myclient.close()

files = get_files()
for file_name in files:
    file = open(f"{dir_path}/{file_name}", "r")
    pattern = file.read().splitlines()[0]
    id = file_name[:-len(extension)]
    document = {"_id": id, "pattern": pattern}
    file.close()
    mongo_insert(document, id)