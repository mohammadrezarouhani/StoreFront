from django.core.mail import EmailMessage
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.shortcuts import render
from templated_mail.mail import BaseEmailMessage
from .tasks import notify_customer
from rest_framework.views import APIView
from rest_framework.response import Response
import requests


class SayHelloView(APIView):
    @method_decorator(cache_page(10*60))
    def get(self, request):
        try:
            response = requests.get('https://httpbin.org/delay/1')
            response.raise_for_status()  
            data = response.json()
            return render(request, 'hello.html', {'data': data})
        except requests.exceptions.RequestException as e:
            return render(request, 'error.html', {'error_message': 'Failed to fetch data'})
        except ValueError as e:
            return render(request, 'error.html', {'error_message': 'Invalid JSON response'})


def say_hello(request):
        
    ### low level cashe api
        key="httpbin"
        if cache.get(key) is None:
            response=requests.get('https://httpbin.org/delay/2')
            data=response.json()
            cache.set(key,data)

        return render(request,'hello.html',{'data':cache.get(key)})

    ### Sending EMail with django 
    # message = EmailMessage(
    #     'subject',
    #     'message',
    #     'from@example.com',
    #     ['to@examples.com']
    # )
    # message.attach_file('playground/..')

    # message = BaseEmailMessage(
    #     template_name='email.html',
    #     context={
    #         'name': 'mohammadreza'
    #     })
    # message.send(['to@example.com'])


    ### call resdis task
    # notify_customer.delay('hello')

    # return render(request, 'hello.html', {'name': 'Mosh'})
