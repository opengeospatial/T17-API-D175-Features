import requests
from pprint import pprint

'''
    HELPERS
'''

def get_useful_links(landing_page):
    links = []

    try:
        api_response = requests.get(url = landing_page, params = {'f':'json'})
        json_api_response = api_response.json()
    except requests.ConnectionError as exception:
        return False
        
    for link in json_api_response["links"]:
        if (link["rel"] == "self"):
            links.append((link["href"], "Landing"))
        
        if (link["rel"] == "service-desc"):
            links.append((link["href"], "Definition"))
        
        if (link["rel"] == "http://www.opengis.net/def/rel/ogc/1.0/conformance"):
            links.append((link["href"], "Conformance"))
        
        if (link["rel"] == "data"):
            links.append((link["href"], "Collections"))

    return links


def get_api_name(landing_page):
    try:
        api_response = requests.get(url = landing_page, params = {'f':'json'})
        json_api_response = api_response.json()
    except requests.ConnectionError as exception:
        return False

    return json_api_response["title"]


def get_collections(landing_page):
    collections = []
    url = landing_page+'/collections'

    try:
        api_response = requests.get(url = url, params = {'f':'json'})
        json_api_response = api_response.json()
    except requests.ConnectionError as exception:
        return False
        
    for collection in json_api_response["collections"]:
        element = dict(id=collection["id"], name=collection["title"])
        collections.append(element)
        

    return collections


def get_queriables(landing_page):
    queriables_selector = []
    collections = []
    url = landing_page+'/collections'

    # Get collections id
    try:
        api_response = requests.get(url = url, params = {'f':'json'})
        json_api_response = api_response.json()
    except requests.ConnectionError as exception:
        return False
        
    for collection in json_api_response["collections"]:
        collections.append(collection["id"])

    # Get queriables for each collection
    for collection in collections:
        try:
            url = landing_page+'/collections/'+collection+'/queryables'
            api_response = requests.get(url = url, params = {'f':'json'})
            json_api_response = api_response.json()
        except requests.ConnectionError as exception:
            return False
            
        group = []
        aux = []

        for queriable in json_api_response["properties"]:
            aux.append(queriable)

        group.append(aux)
        queriables_selector.append(
            dict(
                collection_id = collection, 
                queriables = group
            )
        )
        
    return queriables_selector