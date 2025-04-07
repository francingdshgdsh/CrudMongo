from pymongo import MongoClient
import certifi

MONGO_URI = 'mongodb+srv://2236001500:z7PEtFX4w2ytd5N0@cluster0.trppnmc.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'
ca = certifi.where()

def dbConnection():
    try:
        client = MongoClient(MONGO_URI, tlsCAFile=ca)
        db = client["dbb_products_app"]
        return db
    except ConnectionError:
        print("Error de conexión con la base de datos")
        return None