from django.shortcuts import render
from .forms import SubscriberForm, PostsForm, EmailSentForm
from .models import Subscribers, Posts, EmailSent
from datetime import datetime
from pytz import timezone
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import time
import json
from django.conf import settings

from decouple import config



def subscriber(request):

    if request.method == 'POST':
        form = SubscriberForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'subscribers/completed.html')
    else:
        form = SubscriberForm()
    
    import facebook
    graph = facebook.GraphAPI(config('FACEBOOK_USER_TOKEN'))
    # Extend the expiration time of a valid OAuth access token.
    #extended_token = graph.extend_access_token(app_id, app_secret)
    #print(extended_token) 
    #id is the facebook page_id & feed is the news feed  
    post = graph.get_object(id=
        config('GNDEC_PAGE_ID'), fields='feed')
    post_id = post['feed']['data'][0]['id']
    post_date_time = post['feed']['data'][0]['created_time'][:-5]
    #facebook provie post time in UTC so we have to convert it into IST
    date_str = post_date_time
    datetime_obj_naive = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S")
    datetime_obj_pacific = timezone('UTC').localize(datetime_obj_naive)
    datetime_obj_pacific = datetime_obj_pacific.astimezone(timezone('Asia/Kolkata'))
    #date of post
    post_date = datetime_obj_pacific.strftime("%Y-%m-%d")
    #time of post
    post_time = datetime_obj_pacific.strftime("%H:%M:%S(%Z)")
    #facebook post data
    message = post['feed']['data'][0]['message']
    print(post_time)
    #last post id to whom email was sent
    last_email_post = EmailSent.objects.last()
    last_email_post = last_email_post.post_id 
   # print(last_email_post)
    #subscriber



     
    

    last_entry = Posts.objects.last()

    if not last_entry.post_id == post_id:
        Posts.objects.create(created_time = post_time, created_date = post_date, post_id = post_id, message = message)
        last_message = message
        last_post_date = post_date
        last_post_time = post_time
    #    for email 
    else:
        last_message = last_entry.message
        last_post_date = last_entry.created_date
        last_post_time = last_entry.created_time        
    return render(request, 'subscribers/contact.html', {
    	'form': form,
        'last_message':last_message,
        'last_post_date':last_post_date,
        'last_post_time':last_post_time,
    	})

@csrf_exempt
def subscribed(request):
    if request.method == 'POST':
        email = request.POST
        print(email)
        email = email['email']
        try:
            subscribers = Subscribers.objects.get(email=email)
            email = subscribers.email
            print(email)
            time.sleep(1);
            return HttpResponse(json.dumps({'email': email,}), content_type='application/json')
        except:
            Subscribers.objects.create(email=email)
            print("no user")

            time.sleep(1);
            return HttpResponse(json.dumps({'user': "Alert enabled for"+email,}), content_type='application/json')
