import os
from django.dispatch import receiver
from django_rest_passwordreset.signals import reset_password_token_created
import json
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from .utils.email_domain_verification import get_callback_url_domain

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    context = {
        'token' : reset_password_token.key,
        'url': get_callback_url_domain()  
    }

    email_message = render_to_string('password.html', context)
    subject, text_content, from_email, to = 'Recuperación de contraseña', email_message, 'yoseph12368@gmail.com', reset_password_token.user.email 
    header = {
                     "category": ["password"]
            }
    header = json.dumps(header)
    print(email_message)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(email_message, "text/html")
    msg.send()