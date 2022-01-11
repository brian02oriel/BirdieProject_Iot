from pymongo import MongoClient
from datetime import datetime
import gridfs

def MongoConnection(url):
    # Connecting server
    client = MongoClient("mongodb+srv://brian02oriel:UTP-cat5@birdieproject.xctgi.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    db = client.get_database('BirdieProject')
    #collection_names = db.list_collection_names()
    
    MongoWrite(db, url)

def MongoWrite(db, url):
    #Setting gridfs for mongo file save
    fs = gridfs.GridFS(db)
    fileID = fs.put(open(url, 'rb'))
    #out = fs.get(fileID)

    #Insert images
    col = db.BirdInfo
    col.insert_one({
        "fileID": fileID,
        "datetime":  datetime.now()
    })

    print(url + ' insertada correctamente ' + str(datetime.now()))

