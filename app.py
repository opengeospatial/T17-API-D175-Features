import json
import requests
from pprint import pprint

from flask import Flask, jsonify, render_template, request, url_for
app = Flask(__name__)

API_BASE_URL = 'https://test.cubewerx.com/cubewerx/cubeserv/demo/ogcapi/Foundation/'
API_NAME = "Foundation"

# OGC API useful links
useful_links = [
    (API_BASE_URL+'?f=json','Landing page'),
    (API_BASE_URL+'api?f=json','Api definition'),
    (API_BASE_URL+'conformance?f=json','Conformance classes'),
    (API_BASE_URL+'collections?f=json','Collections'),
]

@app.route('/')
def index():
    if not request.root_url:
        # this assumes that the 'index' view function handles the path '/'
        request.root_url = url_for('index', _external=True)
    return render_template('index.html', links=useful_links, name=API_NAME)


@app.route('/collections/<collectionId>/items/', defaults={
    'bbox': '-0.489,51.28,0.236,51.686', # London  bbox by default
    'collectionId': 'aerofacp_1m',
    'l': 10
})
def foundation_get_features(collectionId, l, bbox):
    if (request.args.get('bbox') == '' or request.args.get('bbox') == None):
        bboxArg = bbox
    else:
        bboxArg = request.args.get('bbox')

    if (request.args.get('l') == '' or request.args.get('l') == None):
        limitArg = l
    else:
        limitArg = request.args.get('l')

    # Get the collection ID
    collection_id = collectionId
    # Set the API resource url
    URL = API_BASE_URL+"/collections/"+collection_id+"/items"
    f = "json" # str | A MIME type indicating the representation of the resources to be presented (e.g. application/gml+xml; version=3.2 for GML 3.2). (optional)
    limitParam = limitArg # int | The optional limit parameter limits the number of items that are presented in the response document.  Only items are counted that are on the first level of the collection in the response document. Nested objects contained within the explicitly requested items shall not be counted. (optional) (default to 10)
    bboxParam = bboxArg # list[float] | Only features that have a geometry that intersects the bounding box are selected. The bounding box is provided as four or six numbers, depending on whether the coordinate reference system includes a vertical axis (elevation or depth): * Lower left corner, coordinate axis 1 * Lower left corner, coordinate axis 2 * Lower left corner, coordinate axis 3 (optional) * Upper right corner, coordinate axis 1 * Upper right corner, coordinate axis 2 * Upper right corner, coordinate axis 3 (optional) The coordinate reference system of the values is WGS84 longitude/latitude (http://www.opengis.net/def/crs/OGC/1.3/CRS84) unless a different coordinate reference system is specified in the parameter `bbox-crs`. For WGS84 longitude/latitude the values are in most cases the sequence of minimum longitude, minimum latitude, maximum longitude and maximum latitude. However, in cases where the box spans the antimeridian the first value (west-most box edge) is larger than the third value (east-most box edge). If a feature has multiple spatial geometry properties, it is the decision of the server whether only a single spatial geometry property is used to determine the extent or all relevant geometries. (optional)
    # defining a params dict for the parameters to be sent to the API
    PARAMS = {
        'f':f,
        'limit':limitParam,
        'bbox': bboxParam
    }
    # sending get request and saving the response as response object
    api_response = requests.get(url = URL, params = PARAMS)
    # extracting data in json format
    json_api_response = api_response.json()
    json_fearures_list = json_api_response["features"]
    # Parsing to string
    features_list = json.dumps(json_fearures_list)
    # Returning string
    return features_list

@app.route('/collections/<collectionId>/items/<itemId>/', defaults={
    'bbox': '-0.489,51.28,0.236,51.686', # London  bbox by default
    'collectionId': 'aerofacp_1m',
    'itemId': 'CWFID.AEROFACP_1M.0.0.1009C50A276905DE1F20020000',
    'l': 10
})
def foundation_get_feature(collectionId, itemId, l, bbox):
    if (request.args.get('bbox') == '' or request.args.get('bbox') == None):
        bboxArg = bbox
    else:
        bboxArg = request.args.get('bbox')

    if (request.args.get('l') == '' or request.args.get('l') == None):
        limitArg = l
    else:
        limitArg = request.args.get('l')

    # Get the collection ID
    collection_id = collectionId
    # get the item ID
    item_id = itemId
    # bbox = [3.4] # list[float] | Only features that have a geometry that intersects the bounding box are selected. The bounding box is provided as four or six numbers, depending on whether the coordinate reference system includes a vertical axis (elevation or depth): * Lower left corner, coordinate axis 1 * Lower left corner, coordinate axis 2 * Lower left corner, coordinate axis 3 (optional) * Upper right corner, coordinate axis 1 * Upper right corner, coordinate axis 2 * Upper right corner, coordinate axis 3 (optional) The coordinate reference system of the values is WGS84 longitude/latitude (http://www.opengis.net/def/crs/OGC/1.3/CRS84) unless a different coordinate reference system is specified in the parameter `bbox-crs`. For WGS84 longitude/latitude the values are in most cases the sequence of minimum longitude, minimum latitude, maximum longitude and maximum latitude. However, in cases where the box spans the antimeridian the first value (west-most box edge) is larger than the third value (east-most box edge). If a feature has multiple spatial geometry properties, it is the decision of the server whether only a single spatial geometry property is used to determine the extent or all relevant geometries. (optional)
    # Set the API resource url
    URL = API_BASE_URL+"/collections/"+collection_id+"/items/"+item_id
    f = "json" # str | A MIME type indicating the representation of the resources to be presented (e.g. application/gml+xml; version=3.2 for GML 3.2). (optional)
    limitParam = limitArg # int | The optional limit parameter limits the number of items that are presented in the response document.  Only items are counted that are on the first level of the collection in the response document. Nested objects contained within the explicitly requested items shall not be counted. (optional) (default to 10)
    bboxParam = bboxArg # list[float] | Only features that have a geometry that intersects the bounding box are selected. The bounding box is provided as four or six numbers, depending on whether the coordinate reference system includes a vertical axis (elevation or depth): * Lower left corner, coordinate axis 1 * Lower left corner, coordinate axis 2 * Lower left corner, coordinate axis 3 (optional) * Upper right corner, coordinate axis 1 * Upper right corner, coordinate axis 2 * Upper right corner, coordinate axis 3 (optional) The coordinate reference system of the values is WGS84 longitude/latitude (http://www.opengis.net/def/crs/OGC/1.3/CRS84) unless a different coordinate reference system is specified in the parameter `bbox-crs`. For WGS84 longitude/latitude the values are in most cases the sequence of minimum longitude, minimum latitude, maximum longitude and maximum latitude. However, in cases where the box spans the antimeridian the first value (west-most box edge) is larger than the third value (east-most box edge). If a feature has multiple spatial geometry properties, it is the decision of the server whether only a single spatial geometry property is used to determine the extent or all relevant geometries. (optional)
    # defining a params dict for the parameters to be sent to the API
    PARAMS = {
        'f':f,
        'limit':limitParam,
        'bbox': bboxParam
    }
    # sending get request and saving the response as response object
    api_response = requests.get(url = URL, params = PARAMS)
    # extracting data in json format
    json_api_response = api_response.json()
    # Parsing to string
    features_item = json.dumps(json_api_response)
    # Returning string
    return features_item
