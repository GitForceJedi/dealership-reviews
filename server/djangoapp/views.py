from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from .restapis import get_request, get_dealers_from_cf, get_dealer_reviews_from_cf, get_dealer_by_id, get_dealers_by_state, analyze_review_sentiments
# from .restapis import related methods
from .models import CarMake, CarModel, CarDealer, CarReview, DealerReview
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.
# ./server/djangoapp/views.py
def static_template_view(request):
    return render(request, 'djangoapp/static_template.html')


# Create an `about` view to render a static about page
# def about(request):
# ...
def about(request):
    return render(request, 'djangoapp/about.html')


# Create a `contact` view to return a static contact page
#def contact(request):
def contact(request):
    return render(request, 'djangoapp/contact.html')

# Create a `login_request` view to handle sign in request
# def login_request(request):
# ...

#KenWillCode FOR COURSERA, LAB ENVIRONMENT WAS DOWN (Performed in VS Code)

def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/login.html', context)
    else:
            context['message'] = "Invalid username or password."

# Create a `logout_request` view to handle sign out request
# def logout_request(request):
# ...

#KenWillCode FOR COURSERA, LAB ENVIRONMENT WAS DOWN (Performed in VS Code)

def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')


# Create a `registration_request` view to handle sign up request
# def registration_request(request):
# ...
#KenWillCode FOR COURSERA, LAB ENVIRONMENT WAS DOWN (Performed in VS Code)
#THE DIRECTIONS FOR NAMING ARE CONFUSING, I HAVE ADDED BOTH REGISTRATION AND SIGNUP (AS THEY REFERRED TO IT BY DIFFERENT NAMES)
#BOTH WORK, BUT CURRENTLY registration_request is used 
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/registration.html', context)   

def signup(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/signup.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/signup.html', context)


# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        #Replace url with link to get-dealership on port 3000
        url = "http://localhost:3000/dealerships/get"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        return HttpResponse(dealer_names)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...
# views.py
# In views.py
from django.http import JsonResponse

# In views.py
from django.http import HttpResponse

def get_dealer_details(request, dealer_id):
    if request.method == "GET":
        # URL of your cloud function for reviews
        url = "http://localhost:5000/api/get_reviews"
        
        # Get dealer reviews from the URL using dealer_id
        dealer_reviews = get_dealer_reviews_from_cf(url, dealer_id)
        
        # Analyze sentiment for each review and append to reviews_data
        reviews_data = []
        for dealer_review in dealer_reviews:
            review_text = dealer_review.review  # Assuming 'review' is an attribute of the DealerReview model
            
            # Analyze sentiment for the review
            sentiment_result = analyze_review_sentiments(
                dealerreview=review_text,
                version="2021-08-01",
                features="sentiment",
                return_analyzed_text=True
            )
            
            if sentiment_result:
                sentiment_label, analyzed_text = sentiment_result
                reviews_data.append({
                    "review_text": review_text,
                    "sentiment_label": sentiment_label,
                    "analyzed_text": analyzed_text
                })
                dealer_review.sentiment = sentiment_label

        # Convert reviews_data to a string
        # Combine sentiment results with original dealer_reviews
        #combined_reviews_data = [f"{review['review_text']} - Sentiment: {review['sentiment_label']}\n" for review in reviews_data] + [str(review) for review in dealer_reviews]
        # Join the combined reviews data
        #reviews_data_str = ''.join(combined_reviews_data)

        # Return HttpResponse with the reviews_data_str
        #return HttpResponse(reviews_data_str)
        return HttpResponse(str(review) for review in dealer_reviews)

    
def dealer_by_id_view(request, dealer_id):
    # Replace 'your_cloud_function_url_here' with the actual URL of your cloud function
    url = 'your_cloud_function_url_here'
    
    dealer = get_dealer_by_id(url, dealer_id)
    
    return render(request, 'dealer_detail.html', {'dealer': dealer})

def dealers_by_state_view(request, state):
    # Replace 'your_cloud_function_url_here' with the actual URL of your cloud function
    url = 'your_cloud_function_url_here'
    
    dealers = get_dealers_by_state(url, state)
    
    return render(request, 'dealers_by_state.html', {'dealers': dealers})

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...

