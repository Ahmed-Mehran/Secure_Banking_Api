## This file is going to hold the functions/methods that are going to be used to send our emails

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.translation import gettext_lazy 
from loguru import logger


## The below functions is going to be a function to send an email with OTP
def send_otp_email(email, otp):
    
    subject = gettext_lazy('Your OTP code for Login')
    
    from_email = settings.DEFAULT_FROM_EMAIL
    
    recipient_list = [email]
    
    context = {
        
        "otp" : otp,
        
        "expiry_time" : settings.OTP_EXPIRATION,
        
        "site_name" : settings.SITE_NAME
    }
    
    html_email = render_to_string("emails/otp_email.html", context)
    plain_email = strip_tags(html_email)
    email = EmailMultiAlternatives(subject, plain_email, from_email, recipient_list)
    email.attach_alternative(html_email, "text/html")
    
    try:
        
        email.send()
        logger.info(f"OTP email sent successfully to {email}")
        
    except Exception as e:
            
            logger.error(f"Failed to send OTP email to {email}:  Error: {str(e)}")
    
    
    
    
    
    
    
