import requests
import pymongo
from classes import *
from functions import *



print("Hello User! Commencing retrieval of data from SWAPI.")
swapi = Database()
people = Collections("people")
starships = Collections("starships")
films = Collections("films")
client = pymongo.MongoClient()
print("Existing Databases:", pymongo.MongoClient().list_database_names(), sep=' ')
database = input("Please select an existing database by typing or create a new one by typing a new name! : ").lower()
db = client[database]
print("Creating starships collection inside the database...")
if "starships" not in db.list_collection_names():   # checking if there is already a collection named starships inside the database
    collection = db["starships"]
elif input("It seems like you already have a collection named starships. Do you want me to drop the collection? (Y/N)").lower() == 'y': # giving option to be able to drop an existing collection named starships
    collection = db["starships"]
    collection.drop()
else:
    collection_name = input("Please type in what you want your new collection to be called.")
    collection = db[collection_name]
print("Collection created!")

print("To be able to start referencing You need to have an existing collection of characters.")
collection_name = None
while collection_name not in db.list_collection_names(): # to negate a typo I used a while loop
    print("Existing Collections: ",db.list_collection_names())
    collection_name = input("Please select an existing collection of characters by typing its name: ").lower()
character_collection = db[collection_name]
print("Starting Referencing...")
referencing(character_collection, 'pilots', starships.data, people.url_data) # using referencing
referencing(character_collection, 'films', starships.data,films.url_data) 
print("Referencing Completed")
print("Saving the starships collection")
collection.insert_many(starships.data) # saving to mongoDB 
print("Collection saved")
