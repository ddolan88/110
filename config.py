import pymongo
import certifi


con_str = "mongodb+srv://ddolan88:DDolan88!!@cluster0.4b2le.mongodb.net/?retryWrites=true&w=majority"


client = pymongo.MongoClient(con_str, tlsCAFile=certifi.where())

db = client.get_database("StoreDB")
