from django.shortcuts import render
from django.core.mail import EmailMessage
from templated_mail.mail import BaseEmailMessage


def say_hello(request):
    # message = EmailMessage(
    #     'subject',
    #     'message',
    #     'from@example.com',
    #     ['to@examples.com']
    # )
    # message.attach_file('playground/..')

    message = BaseEmailMessage(
        template_name='email.html',
        context={
            'name': 'mohammadreza'
        })
    message.send(['to@example.com'])
    return render(request, 'hello.html', {'name': 'Mosh'})
