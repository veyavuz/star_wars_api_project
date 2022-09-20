import requests
from pprint import pprint

# making a class in case the swapi.dev gets closed and we might have to use another starwars rest api
class Database:
    def __init__(self):
        self.data = self.retrieve_data() #attributing the retrieved data
    
    def retrieve_data(self,url:str = "https://swapi.dev/api/"): # retrieving data from a url
        return requests.get(url).json()


class Collections(Database):
    def __init__(self, collection = "starships"):
        super().__init__() #inheriting to use parent method     
        self.url = self.data[collection] # getting the passed in collection's url
        self.results = self.get_results(self.url)       
        self.url_data = self.url_to_data(self.results)
        self.data = self.cleaned_data(self.results) # using polymorphism
    
    def get_results(self,url:str):
        print("Downloading data from " + url)
        response = self.retrieve_data(url) # initial data retrieving 
        results = response["results"]
        while response["next"] is not None: # looping through pages of response
            print("Next page found, retrieving data from", response["next"])
            response = self.retrieve_data(response["next"])
            results = results + response["results"]
        return results
    
    def cleaned_data(self, data:list): # cleaning unuseful information
        copy_data = data
        for document in copy_data:
            del document["created"]
            del document["edited"]
            del document["url"]
        return copy_data
    
    def url_to_data(self, data: list): # getting a dictionary based on url to make less http request and save time
        url_dict = {}
        for document in data:
            url_dict[document["url"]] = document
        return url_dict

if __name__ == "__main__":
    x = Database()
    pprint(x.data, sort_dicts=False)

