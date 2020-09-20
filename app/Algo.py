import copy
import random, string, math

example_input = {
    "sublet": {
    "name": 'joe',
    "sqft": 1000,
    "lowPrice": 600,
    "highPrice": 1000,
    "bedroom": 3.0,
    "lat": 75,
    "lon": 30,
    "range": 20
    },
    "subleasers": [
        {
            "name": 'jim',
            "sqft": 1000,
            "price": 900,
            "bedroom": 3.0,
            "address": '2918 Ravensport Dr',
            "lat": 75,
            "lon": 30,

        },
        {
            "name": 'karen',
            "sqft": 975,
            "price": 1100,
            "bedroom": 4.0,
            "address": '2626 Salado Dr',
            "lat": 75,
            "lon": 30,
        },
        {
        "name": 'pam',
        "sqft" : 650,
        "price" : 625,
        "bedroom" : 2.0,
        "address": '4734 Burclare Ct',
        "lat": 75,
        "lon": 30,
        }
    ],
    "scoring_weights": {
        "sqft": 1.0,
        "price range": 1.0,
        "bedroom": 1.0,
        "coordinates": 1.0,
        "amenities": 0.3,
        "hospital": 1,
    }
}

class AlgorithmError(Exception):
     def __init__(self, value):
         self.value = value
     def __str__(self):
         return repr(self.value)

def apply(input):
    # default weights for the scoring function
    default_weights = {
        "sqft": 1.0,
        "price": 1.0,
        "bedroom": 1.0,
        "coordinates": 1.0,
         "amenities": 0.3,
         "hospital" : 1,
         "range" : 20,
    }
    # overwrite the weights if given by user
    if "scoring_weights" in input:
        weights = overwriteWeights(default_weights, input["scoring_weights"])
    else:
        weights = default_weights


    scoring_list = {}
    for sublease in input["subleasers"]:
            score = scoring_function(weights, input["sublet"], sublease)
            if score:
                scoring_list[sublease["address"]] = score

    sorted_list = sorted(scoring_list.items(), key=lambda x: x[1], reverse=True)
    print(sorted_list)



def overwriteWeights(default, new):
    rVal = default

    if "sqft" in new:
        rVal["sqft"] = float(new["sqft"])
    if "price" in new:
        rVal["price"] = float(new["price"])
    if "bedroom" in new:
        rVal["bedroom"] = float(new["bedroom"])
    if "coordinates" in new:
        rVal["coordinates"] = float(new["coordinates"])

    return rVal

def coords_distance(lat1, lon1, lat2, lon2):
    R = 3958.8 # miles

    dlon = lon2 - lon1

    dlat = lat2 - lat1

    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def scoring_function(weights, sublet, sublease):
    score = 10.0

    call = sublease["sqft"] / sublet["sqft"]
    w1 = min(call, 1 / call)
    score = score * w1 * ((1 - 0.37 * weights["sqft"])**.5)

    l = sublet["lowPrice"]
    h = sublet["highPrice"]
    if sublease["price"] > h:
        w2 = 2 * (sublease["price"] - h) / (l + h)
        score = score - w2 * ((1 - 0.37 * weights["price"])**.5)

    if sublease["price"] < l:
        w2 = (l - sublease["price"]) / (l + h)
        score = score - w2 * ((1 - 0.37 * weights["price"])**.5)

    if sublet["bedroom"] > sublease["bedroom"]:
        score = score - 2 * (sublet["bedroom"] - sublease["bedroom"]) * weights["bedroom"]

    if sublet["bedroom"] < sublease["bedroom"]:
        score = score - (sublease["bedroom"] - sublet["bedroom"]) * weights["bedroom"]

    # old coordinates
    if "lat" in sublet and "lon" in sublease:
        coord_inputs = (sublet["lat"], sublet["lon"], sublease["lat"], sublease["lon"])
        distance = coords_distance(*coord_inputs)
        if distance > sublet["range"]:
            score -= 5
        if sublet["range"]  == 0:
            score += 5
        #score -= distance * weights["coordinates"]

        # res = api_additions(weights, sublet, sublease, score)
        #
        # return res
    return score

# TODO
def api_additions(weights, sublet, sublease, score):

        lat = sublet["lat"]
        lon = sublease["lon"]
        restaurants = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={0},{1}&radius=2000&type=restaurant&keyword=chinese&key=AIzaSyBJsPR0hLvmnSgGu4u9KThHP0M7acYkFM0'.format(lat, lon)

        count = len[restaurants]
        score = score - 2 * weights["amenities"] / count^1.5

        hos = max(weight["hospital"], 0.25)

        hospitals = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={0},{1}&radius=(12000/hos)&type=restaurant&keyword=chinese&key=AIzaSyBJsPR0hLvmnSgGu4u9KThHP0M7acYkFM0'.format(lat, lon)
        if len[hospitals] == 0:
            score -= 1.2 * weight["hospital"]

        address = sublease["address"]
        loc = 'https://maps.googleapis.com/maps/api/geocode/json?address={0}&key=IzaSyBJsPR0hLvmnSgGu4u9KThHP0M7acYkFM0'.format(address)
        ID = loc["place_id"]
        result = 'https://maps.googleapis.com/maps/api/place/details/json?placeid={0}&key=AIzaSyBJsPR0hLvmnSgGu4u9KThHP0M7acYkFM0'.format(ID)

        if result["rating"] != 'ZERO_RESULTS':
            score = score * result["rating"] / 5

        return score

apply(example_input)
