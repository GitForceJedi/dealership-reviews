import requests
import json
# import related models here
from .models import CarMake, CarModel, CarDealer, CarReview, DealerReview
from requests.auth import HTTPBasicAuth


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))


# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload, **kwargs):
    response = requests.post(url, params=kwargs, json=json_payload)
    return response

# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative

def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    
    api_key = kwargs.get("api_key")
    
    try:
        # Check if api_key is provided
        if api_key:
            # Call get method of requests library with URL, parameters, and API key
            print('THIS IS API KEY:'+api_key)
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs, auth=HTTPBasicAuth('apikey', api_key))
            print('THIS IS RESPONSE:' +str(response))
            print('THIS IS URL: '+url)
        else:
            # Call get method of requests library with URL and parameters only
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
    except requests.exceptions.RequestException as e:
        # If any error occurs
        print("Network exception occurred: {}".format(e))
        return None

    status_code = response.status_code
    print("With status {} ".format(status_code))
    
    try:
        json_data = response.json()
        return json_data
    except json.JSONDecodeError as e:
        print("Error decoding JSON response: {}".format(e))
        return None

# https://api.us-east.natural-language-understanding.watson.cloud.ibm.com/instances/5a16e067-80db-4d73-bea5-7770ddfe6a3c
# https://api.us-east.natural-language-understanding.watson.cloud.ibm.com/instances/807751ef-aa26-49da-807d-c3a87eb7f717
# fKH5SZrRcNWHyfRw2AU7caiQJSqqr2XDKTZVL47V2QZw
# dC6K9B-AAWLw2nSdsc66_kCzYEeu7CWsp1AB0dtS-_tX
def analyze_review_sentiments(dealerreview, **kwargs):
    # Define the URL for IBM Watson NLU sentiment analysis
    url = "https://api.us-east.natural-language-understanding.watson.cloud.ibm.com/instances/807751ef-aa26-49da-807d-c3a87eb7f717/v1/analyze?version=2022-04-07"

    # Set the parameters for the sentiment analysis
    params = {
        "text": dealerreview,
        "version": kwargs.get("version", "2021-08-01"),
        "features": kwargs.get("features", "sentiment"),
        "return_analyzed_text": kwargs.get("return_analyzed_text", True),
        "language": 'en'
    }

    # Hardcode the API key
    api_key = "dC6K9B-AAWLw2nSdsc66_kCzYEeu7CWsp1AB0dtS-_tX"

    try:
        # Make a call to the updated get_request method
        response_data = get_request(url, api_key=api_key, **params)

        # Print the entire response
        print("API Response:", response_data)

        # Process the response_data and return sentiment result
        if response_data:
            # Extract sentiment information or perform further processing
            sentiment = response_data.get("sentiment", {}).get("document", {}).get("label")
            analyzed_text = response_data.get("analyzed_text")
            
            print("Sentiment: {}".format(sentiment))
            print("Analyzed Text: {}".format(analyzed_text))

            return sentiment, analyzed_text
        else:
            print("Failed to analyze sentiments. Response data is empty.")
            return None
    except requests.exceptions.HTTPError as errh:
        print("HTTP Error:", errh)
        print("Response Content:", errh.response.content)
    except requests.exceptions.RequestException as err:
        print("Error:", err)

    return None

def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result and isinstance(json_result, list):
        # Iterate over the list of dealers
        for dealer in json_result:
            # Assuming each dealer is a dictionary, modify accordingly if it's a different structure
            dealer_obj = CarDealer(
                address=dealer.get("address"),
                city=dealer.get("city"),
                full_name=dealer.get("full_name"),
                id=dealer.get("id"),
                lat=dealer.get("lat"),
                long=dealer.get("long"),
                short_name=dealer.get("short_name"),
                st=dealer.get("st"),
                zip=dealer.get("zip"),
                state=dealer.get("state"),
            )
            results.append(dealer_obj)

    return results


# In restapis.py
# In restapis.py
# In restapis.py
# In restapis.py
# In restapis.py
def get_dealer_reviews_from_cf(url, dealer_id, **kwargs):
    results = []
    # Ensure 'id' is included in kwargs
    kwargs['id'] = dealer_id
    
    # Call get_request with a URL parameter (dealerId)
    json_result = get_request(url, **kwargs)
    
    print("JSON Result:", json_result)  # Add this line for debugging
    
    if isinstance(json_result, list):
        # Ensure that the result is a list
        for review in json_result:
            if isinstance(review, dict):
                # Create a DealerReview object with values in the review dictionary
                review_obj = DealerReview(
                    dealership=review.get("dealership"),
                    name=review.get("name"),
                    purchase=review.get("purchase"),
                    review=review.get("review"),
                    purchase_date=review.get("purchase_date"),
                    car_make=review.get("car_make"),
                    car_model=review.get("car_model"),
                    car_year=review.get("car_year"),
                    sentiment=review.get("sentiment"),
                    id=review.get("_id")  # Use '_id' instead of 'id'
                )
                results.append(review_obj)
            else:
                print("Invalid review structure:", review)  # Add this line for debugging
    else:
        print("Invalid JSON result:", json_result)  # Add this line for debugging
    
    print("Results:", results)  # Add this line for debugging
    return results

def get_dealer_by_id_from_cf(url, id, **kwargs):
    result = {}
    # Call get_request with a URL parameter
    json_result = get_request(url, id=id)
    print("JSON RESULTSS"+str(json_result))
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result  
        # For each dealer object
        dealer = dealers[0]
        # Create a CarDealer object with values in `doc` object
        dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"],
                                id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
                                short_name=dealer["short_name"],
                                state=dealer["state"], st=dealer["st"], zip=dealer["zip"])
        result = dealer_obj
    return result

def get_dealer_by_state_from_cf(url, state, **kwargs):
    result = []
    # Call get_request with a URL parameter
    json_result = get_request(url, state=state)
    print("JSON RESULTSS"+str(json_result))
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result  
        # For each dealer object
        for dealer in dealers:        # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"],
                                    id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
                                    short_name=dealer["short_name"],
                                    state=dealer["state"], st=dealer["st"], zip=dealer["zip"])
            result.append(dealer_obj)
    return result


def get_dealers_by_state(url, state):
    """
    Get a list of dealers by state from a cloud function.

    Args:
    - url (str): The URL of the cloud function.
    - state (str): The state to filter dealers.

    Returns:
    - list: A list of CarDealer objects representing dealers in the specified state.
    """
    params = {'state': state}
    json_result = get_request(url, **params)

    results = []
    if json_result and isinstance(json_result, list):
        for dealer_doc in json_result:
            dealer_obj = CarDealer(
                id=dealer_doc["id"],
                city=dealer_doc["city"],
                state=dealer_doc["state"],
                st=dealer_doc["st"],
                address=dealer_doc["address"],
                zip_code=dealer_doc["zip"],
                lat=dealer_doc["lat"],
                long=dealer_doc["long"],
                short_name=dealer_doc["short_name"],
                full_name=dealer_doc["full_name"]
            )
            results.append(dealer_obj)

    return results
