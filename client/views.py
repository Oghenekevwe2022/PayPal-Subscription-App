from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from writer.models import Article
from .models import Subscription
from account.models import CustomUser
from . paypal import *
from django.http import HttpResponse
from . forms import UpdateUserForm


# This function/code is to output the plan of a subscriber when they log in
@login_required(login_url= 'my-login')

def client_dashboard(request):
    
    try:
        
        subDetails = Subscription.objects.get(user=request.user)
        
        subscription_plan = subDetails.subscription_plan
        
        context = {'Subplan': subscription_plan}
        
        return render(request, 'client/client-dashboard.html', context)
    
    except:
        
        subscription_plan = "None"
        
        context = {'Subplan': subscription_plan}
    
        return render (request, 'client/client-dashboard.html', context)


@login_required(login_url= 'my-login')

def browse_article(request):
    
    try:
        
        subDetails = Subscription.objects.get(user=request.user, is_active = True) # Checking if a. the user trying to access the subscription has been registered and b. if the subscription is still active
    
    except:
        
        return redirect('subscription-locked')
    
    current_subscription_plan = subDetails.subscription_plan
    
    if current_subscription_plan == 'Standard':
        
        articles = Article.objects.all().filter(is_premium = False)
    
    elif current_subscription_plan == 'Premium':
        
        articles = Article.objects.all()
        
    context = {'AllClientArticles': articles}
    
    return render(request, 'client/browse-article.html', context)

@login_required(login_url= 'my-login')

def subscription_locked(request):
    
    return render(request, 'client/subscription-locked.html')

@login_required(login_url= 'my-login')

def subscription_plans(request):
    
    if not Subscription.objects.filter(user=request.user).exists():
        
        return render(request, 'client/subscription-plan.html')
    
    else:
        
        return redirect('client-dashboard')


# @login_required(login_url= 'my-login')

# def account_management(request):
    
#     return render(request, 'client/account-management-client.html')


@login_required(login_url= 'my-login')

def create_subscription(request, subID, plan):
    
    custom_user = CustomUser.objects.get(email=request.user)
    
    if not Subscription.objects.filter(user=request.user).exists():
        
        firstName = custom_user.first_name
        
        lastName = custom_user.last_name
        
        fullName = firstName + " " + lastName
        
        selected_sub_plan = plan
        
        if selected_sub_plan == "Standard":
            
            sub_cost = "4.99"
        
        elif selected_sub_plan == "Premium":
            
            sub_cost = "9.99"
            
        subscription = Subscription.objects.create(
            subscriber_name = fullName, 
            subscription_plan = selected_sub_plan,
            subscription_cost = sub_cost,
            paypal_subscription_id = subID,
            is_active = True,
            user = request.user
        )
        
        context = {'SubscriptionPlan': selected_sub_plan}
        
        return render(request, 'client/create-subscription.html', context)

    else:
        
        return redirect('client-dashboard')

@login_required(login_url= 'my-login')

def delete_subscription(request, subID):
    
    # Delete subscription from paypal
    
    access_token = get_access_token()
    
    try:
        cancel_subscription_paypal(access_token, subID)
        
        # Delete a subscription from Django(application side)
        
        subscription = Subscription.objects.get(user=request.user, paypal_subscription_id = subID)
        
        subscription.delete()
        
        return render(request, 'client/delete-subscription.html')
    
    except:
        
        return redirect('client-dashboard')
    
    
@login_required(login_url= 'my-login')

def account_management(request):
    
    try:
        
    # update account details of a log in user
    
        form = UpdateUserForm(instance= request.user)  # Note that the instance is to populate the information of a signed in user
        
        if request.method == "POST":
            
            form = UpdateUserForm(request.POST, instance = request.user)
            
            if form.is_valid():
                
                form.save()
                
                return redirect('client-dashboard')
        
    
    # Check if user has a subscription
    
        subDetails = Subscription.objects.get(user=request.user)
            
        subscription_id = subDetails.paypal_subscription_id
        
        context = {'SubscriptionID': subscription_id, 'UpdateUserForm': form}

        return render(request, 'client/account-management.html', context)
    
    except:
        
        form = UpdateUserForm(instance= request.user)  # Note that the instance is to populate the information of a signed in user
    
        if request.method == "POST":
        
            form = UpdateUserForm(request.POST, instance = request.user)
            
            if form.is_valid():
                
                form.save()
                
                return redirect('client-dashboard')
        
        context = {"UpdateUserForm": form}
        
        return render(request, 'client/account-management.html', context)
    
    
@login_required(login_url= 'my-login')
def delete_account_2(request):
    
    if request.method == "POST":
        
        deleteUser = CustomUser.objects.get(email=request.user)
        
        deleteUser.delete()
        
        return redirect("")
    
    return render(request, 'client/delete-account.html')
    
    
    

@login_required(login_url= 'my-login')
def update_subscription(request, subID):
    
    access_token  = get_access_token()
    
    # approval_link = Hateoas link from paypal
    
    approval_link = update_subscription_paypal(access_token, subID)
    
    if approval_link:
        
        return redirect(approval_link)
    
    else:
        
        return HttpResponse("Unable to obtain the approval link")
    
    
@login_required(login_url= 'my-login')
def paypal_update_sub_confirmed(request):
    
    try:
        subDetails = Subscription.objects.get(user=request.user)
        
        subscriptionID = subDetails.paypal_subscription_id
        
        context = {'SubscriptionID': subscriptionID}
        
        return render(request, 'client/paypal-update-sub-confirmed.html', context)
    
    except:
        
        return render(request, 'client/paypal-update-sub-confirmed.html')
    

@login_required(login_url= 'my-login')
def django_update_sub_confirmed(request, subID):
    
    access_token = get_access_token()
    
    current_plan_id = get_current_subscription(access_token, subID)
    
    if current_plan_id == 'P-58A65701M48606308MZGTDEY': #Standard
        new_plan_name = 'Standard'
        new_cost = '4.99'
        
        Subscription.objects.filter(paypal_subscription_id=subID).update(subscription_plan=new_plan_name, subscription_cost=new_cost)
        
    elif current_plan_id == 'P-21520092JM963490FMZGTD3Y':  #Premium
        new_plan_name = 'Premium'
        new_cost = '9.99'
        
        Subscription.objects.filter(paypal_subscription_id=subID).update(subscription_plan=new_plan_name, subscription_cost=new_cost)
        
        return render(request, 'client/django-update-sub-confirmed.html')   