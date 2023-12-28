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
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

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










def get_dealer_by_id(url, dealer_id):
    """
    Get a single dealer by dealer_id from a cloud function.

    Args:
    - url (str): The URL of the cloud function.
    - dealer_id (str): The ID of the dealer.

    Returns:
    - CarDealer: A CarDealer object representing the dealer.
    """
    params = {'dealerId': dealer_id}
    json_result = get_request(url, **params)

    if json_result:
        dealer_doc = json_result  # Assuming the response is a single dealer, modify if needed
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
        return dealer_obj
    else:
        return None


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
