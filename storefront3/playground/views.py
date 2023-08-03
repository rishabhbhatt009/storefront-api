from django.shortcuts import render
from django.core.cache import cache
from rest_framework.views import APIView
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.core.mail import send_mail, mail_admins, EmailMessage, BadHeaderError
from templated_mail.mail import BaseEmailMessage
from .tasks import notify_customers
import requests


#######################################################################################
# sending emails 
#######################################################################################

def send_email(request):
    try :    
        # ---------------------------------------------------------------------------------
        # sending email to normal person 
        # ---------------------------------------------------------------------------------
        # 
        # send_mail(subject='Testing', 
        #           message='This is a test email',
        #           from_email='admin@storefron.com',
        #           recipient_list=['user1@storefront.com']
        #           )
        
        
        # ---------------------------------------------------------------------------------
        # sending email to admin 
        # ---------------------------------------------------------------------------------
        # 
        # mail_admins(subject='subject', 
        #             message='message', 
        #             html_message='<h1>Hi, This is a test message</h1>')
        
        
        # ---------------------------------------------------------------------------------
        # sending email with attachment
        # - both send_mail and mail_admin use EmailMessage internally
        # - EmailMessage gives more control including cc, bcc 
        # ---------------------------------------------------------------------------------
        # 
        # message = EmailMessage(subject='Test with attachment',
        #                        body='This is a test message with attachment',
        #                        from_email='admin@storefront.com',
        #                        to=['user1@storefront.com'],
        #                        # attachments='playground\static\images\\nature.jpg',
        #                        )
        # message.attach_file('playground/static/images/nature.jpg')
        # message.send()
        
        
        # ---------------------------------------------------------------------------------
        # sending templated email 
        # - BaseEmailMessage extends EmailMessage and has all its functions 
        # ---------------------------------------------------------------------------------

        message = BaseEmailMessage(
            template_name='emails/hello.html',
            context={'name':'Admin Overlord'}
        )
        message.send(to=['user1@storefront.com'])
        
    except BadHeaderError:
        print('Bad Header detected')
    
    return render(request, 'hello.html', {'name': 'Rishabh'})

#######################################################################################
# sending messages / notification  
#######################################################################################

def message_broker(request):
    notify_customers.delay('Hello')
    return render(request, 'hello.html', {'name': 'Rishabh'})

#######################################################################################
# caching 
# - 1. Implementing cache on function base views
# - 2. Implementing cache on class base views
# - Note : changes wont be visible until the cache expires 
#######################################################################################

# -------------------------------------------------------------------------------------
# Implementing cache on function based views
# -------------------------------------------------------------------------------------
# # without decorator  
# def slow_api(request):
#     key = 'slow_api_result'
#     if cache.get('slow_api_result') is None : 
#         response = requests.get('https://httpbin.org/delay/2')
#         data = response.json()
#         cache.set(key=key,
#                   value=data,
#                   # timeout=10*60
#                   )
#     return render(request, 'hello.html', {'name': cache.get(key)})

# # with decorator 
# @cache_page(10*60)
# def slow_api(request):
#     response = requests.get('https://httpbin.org/delay/2')
#     data = response.json()
#     return render(request, 'hello.html', {'name': data})

# -------------------------------------------------------------------------------------
# Implementing cache on class based views
# -------------------------------------------------------------------------------------

# class based view 
class slow_api(APIView):
    @method_decorator(cache_page(5*60))
    def get(self, request):
        response = requests.get('https://httpbin.org/delay/2')
        data = response.json()
        return render(request, 'hello.html', {'name': data})

#######################################################################################