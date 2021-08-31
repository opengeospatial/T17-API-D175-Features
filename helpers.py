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