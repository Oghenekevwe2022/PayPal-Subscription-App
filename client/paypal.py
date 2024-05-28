# Make http request to an external/third party api(paypal API)

import requests
import json
from . models import Subscription
from django.conf import settings

# Getting an access token from a paypal api to enable a proper acess/interaction to paypal to perform some task

def get_access_token():
    
    data = {'grant_type': 'client_credentials'} 
    
    # Set https request headers to interact with paypal API
    
    headers = {'Accept': 'application/json', 'Accept-Language': 'en_US'} 
    
    client_Id = settings.SS_CLEINT_ID 
    
    secret_id = settings.SS_SECRET_ID
    
    # Define the url endpoint for making a post request to paypal API token endpoint in sandbox environment
    
    url = 'https://api.sandbox.paypal.com/v1/oauth2/token'
    
    r = requests.post(url, auth=(client_Id, secret_id), headers=headers, data=data).json()
    
    access_token = r['access_token'] #This extract the access token from the JSON response 'r' and stores it in a variable 'access_token'
    
    return access_token

# Creating a cancel function that directly interact with paypal

def cancel_subscription_paypal(access_token, subID):
    
    bearer_token = 'Bearer ' + access_token  #creating security to prove identity to access various services when accessing various paypal API
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': bearer_token,
    }
    
    # define the url endpoint to send request to the api environment
    
    url = 'https://api.sandbox.paypal.com/v1/billing/subscriptions/' + subID + '/cancel' # You can get/see this reference link in the cancel subscription under subscription management in developer paypal.com

    r = requests.post(url, headers=headers)
    
    print(r.status_code)
    

def update_subscription_paypal(access_token, subID):
    
    bearer_token = 'Bearer ' + access_token  #creating security to prove identity to access various services when accessing various paypal API
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': bearer_token,
    }
    
    subDetails = Subscription.objects.get(paypal_subscription_id = subID)
    
    # Obtain current subcription plan for user/client (Standard / Premium)
    
    current_sub_plan = subDetails.subscription_plan
    
    if current_sub_plan == "Standard":
        
        new_sub_plan_id = 'P-21520092JM963490FMZGTD3Y' # To Premium
    
    elif current_sub_plan == "Premium":
        
        new_sub_plan_id = 'P-58A65701M48606308MZGTDEY' # To Standard
        
    url = 'https://api.sandbox.paypal.com/v1/billing/subscriptions/' + subID + '/revise' 
    
    revision_data = {
        
        "plan_id": new_sub_plan_id
    }
    
    # Make a POST request to paypal's API for updating/revising a subscription
    
    r = requests.post(url, headers=headers, data=json.dumps(revision_data))
    
    # Output the response from paypal
    
    response_data = r.json()
    
    print(response_data)
    
    approve_link = None
    
    for link in response_data.get('links', []):
        
        if link.get('rel') == 'approve':
            
            approve_link = link['href']
            
    if r.status_code == 200:
        
        print("Request was a success")
        
        return approve_link
    
    else:
        
        print("Sorry, an error occur!")
    
    
def get_current_subscription(access_token, subID):
    
    bearer_token = 'Bearer ' + access_token  #creating security to prove identity to access various services when accessing various paypal API
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': bearer_token,
    }
    
    url = f'https://api.sandbox.paypal.com/v1/billing/subscriptions/{subID}'
    
    r = requests.get(url, headers = headers)
    
    if r.status_code ==200:
        
        subscription_data = r.json()

        current_plan_id = subscription_data.get('plan_id')
        
        return current_plan_id
    
    else:
        
        print('Failed to retrieve subscription details')
        
        return None
    
    
    