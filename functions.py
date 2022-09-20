import pymongo

def url_to_name(url:str, data:dict): # finding name of a document by url
    try: # to be able to get both pilot 'names' and films 'title' I used try except to overcome key error
        name = data[url]["name"] 
    except KeyError:
        name = data[url]["title"]
    return name


def referencing(collection, key:str, document_data:list,  url_data:dict): # establishing relations using referencing    
    for document in document_data:
        if document[key]:
            temp_list = []
            for url in document[key]:
                name = url_to_name(url, url_data)
                if key == 'pilots': # To be able to reference films key in starship documents I used an if statement
                    temp_list.append(collection.find_one({"name": name},{"_id":1})["_id"])
                else: # if key is other than pilots only the names of the references will be appended
                    temp_list.append(name)
            document[key] = temp_list
    return None