# -*- coding: utf-8 -*-
import io
from pymongo import MongoClient
from datetime import datetime
import gridfs
from PIL import Image

def MongoGetImage():
    #Connecting server
    client = MongoClient("mongodb+srv://brian02oriel:UTP-cat5@birdieproject.xctgi.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    db = client.get_database('BirdieProject')
    collection_names = db.list_collection_names()
    print(collection_names)

    #Initialize gridfs
    fs = gridfs.GridFSBucket(db)

    #Setting my db column
    col = db.BirdInfo

    #Getting columns
    getfiles = col.find({})

    

    #Getting file_IDs
    file_id_columns = [ getfileID for getfileID in getfiles]
    file_ids = list()

    for i in range(len(file_id_columns)):
        file_ids.append(file_id_columns[i]['fileID'])

    #Getting image files
    for j in range(len(file_ids)):
        grid_out = fs.open_download_stream(file_ids[j])
        contents = grid_out.read()
        SaveFile(contents, j)

#Saving image into dataset folder
def SaveFile(data, j):
    img = Image.open(io.BytesIO(data))
    img.save("downloads/" + str(j) +".jpg", "JPEG")

MongoGetImage()