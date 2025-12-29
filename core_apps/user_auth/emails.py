## This file is going to hold the functions/methods that are going to be used to send our emails

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.translation import gettext_lazy 
from loguru import logger


## The below functions is going to be a function to send an email with OTP
def send_otp_email(email, otp):  ## This defines a function whose responsibility is to send an OTP email. It takes two inputs: the recipient’s email address and the OTP value that needs to be sent. Keeping this logic in one function
                                  # makes the authentication flow clean and reusable. For OTP generation, we have created a function called generate_otp in utils.py
    
    
    subject = gettext_lazy('Your OTP code for Login')   ## This sets the subject line of the email. gettext_lazy is used so the subject can be translated later if the application supports multiple languages. The translation is evaluated
                                                         # only when needed, not immediately.
    
    from_email = settings.DEFAULT_FROM_EMAIL   ## This fetches the sender’s email address from Django settings. 
    
    recipient_list = [email]    ## Django expects email recipients to be passed as a list because the email system is designed to be generic and flexible, not limited to single-user cases like OTPs. Emails are often sent to multiple
                                 # recipients at once (for example, notifications, alerts, or admin emails), and using a list provides a consistent interface for handling one or many recipients without changing the underlying logic.
                                 # Even when sending an OTP to a single user, Django still follows this unified design so the same email-sending code works everywhere, avoids special cases, and makes it easy to extend later if you
                                 # ever need to send the same email to multiple addresses. The email used in recipient_list = [email] is the same email address passed as an argument to the function. It represents the user’s email 
                                 # address to which the OTP should be sent.
     
    context = {            ## This dictionary holds the dynamic data that will be injected into the email template. The email template is otp_email.html and it has dynamic variables which need data from here and if you look at the
                            # html doc, its OTP, expire time and site name. The value for expiry and sitename are basically queried from the settings, as we have already defined the values for these there.
        
        "otp" : otp,
        
        "expiry_time" : settings.OTP_EXPIRATION,
        
        "site_name" : settings.SITE_NAME
    }
    
    html_email = render_to_string("emails/otp_email.html", context)  ## This renders an HTML email template using the provided context. It converts the template into a complete HTML string with the OTP and other details filled in.
                                                                      # render_to_string is useful when the HTML is needed for something other than a browser response, such as sending emails, generating PDFs, or storing HTML in the database.
                                                                      # Remember the “string” formatting here is just the transport format; once the email reaches the user, their email app renders that string back into a visually rich HTML
                                                                      # email, which improves user experience and reduces confusion. See we can say that render_to_string converts the HTML template into a string so it can be transported 
                                                                      # (sent over email systems), and when it reaches the user, the email client renders that string back into HTML, so the user sees the formatted email as intended.
                                                                      # __So here the html_email(variable) is a string basically which stores the otp_email(template) content as string__. When we use render_to_string, we provide the HTML
                                                                      # template (email template) that we want to convert into a string, and we also pass the context data (dynamic values like OTP, expiry time, site name).
    
    
    plain_email = strip_tags(html_email)  ## This creates a plain-text version of the email by removing all HTML tags. This ensures compatibility with email clients that do not support HTML. render_to_string() returns a string, and
                                           # strip_tags() simply removes HTML tags from that string and returns another string. So both html_email and plain_email are strings; the only difference is that one contains HTML markup
                                           # and the other is plain text.
    
    email = EmailMultiAlternatives(subject, plain_email, from_email, recipient_list)   ## this line creates an instance (an object) of an email, which represents one complete email message that is ready to be sent to the user. It
                                                                                        # holds all the details like subject, sender, receiver, plain text content, and later the HTML content. The email is not sent at this moment; 
                                                                                        # it is just prepared and stored in memory. When email.send() is called, this prepared email object is then actually delivered to the client/user.
                                                                                        # The plain text version is treated as the default and safest version, so even very old or restricted email clients can still show the message.
                                                                                        # Later, when you attach the HTML version, modern email clients will automatically choose the richer HTML email, while others fall back to the 
                                                                                        # plain text one. This ensures the email works correctly for all users and all email clients. So in short it basically creates an instance or a
                                                                                        # single record email that is about to be sent to the client/user
    
    email.attach_alternative(html_email, "text/html") ## This attaches the HTML version of the email so modern email clients can display a rich, formatted message while still keeping the plain text option.
    
    try:
        
        email.send()  ## This sends the email using Django’s configured email backend. If the email is sent successfully, execution continues without error.
        
        logger.info(f"OTP email sent successfully to {email}")
        
    except Exception as e:
            
            logger.error(f"Failed to send OTP email to {email}:  Error: {str(e)}")
            
    
## Another email sending function that is going to send an email to the user when their account has been locked due to too many failed login attempts 
def send_account_locked_email(request):
    
    current_user = request.user
    
    subject = gettext_lazy('Your account has been locked')
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [current_user.email]

    context = {
        "user": current_user,
        "lockout_duration": int(settings.LOCKOUT_DURATION.total_seconds() // 60),
        "site_name": settings.SITE_NAME
    }

    html_email = render_to_string("emails/account_locked.html", context)
    plain_email = strip_tags(html_email)

    email = EmailMultiAlternatives(subject, plain_email, from_email, recipient_list)
    email.attach_alternative(html_email, "text/html")

    try:
        email.send()
        logger.info(f"Account Locked, Email sent to : {email}")
    except Exception as e:
        logger.error(f"Failed to send acccount locked email to {email}:  Error: {str(e)}")
    

            
    
    
    
    
    
    
    
    
