import random
import string
from os import getenv
from typing import Any, Optional

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import UserManager 
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy

## The first thing we are going to do is to define a function that is going to help us to generate usernames automatically(this is to follow standardize username for banks. See banks usually have a unique(random) username for bank users so as to
#  to distuingish uniquely and easily between customers.
def generate_username():
    
    bank_name = getenv('BANK_NAME')
    
    words = bank_name.split()   ## Splits the name into a list first, so we can iterate
    
    prefix = "".join([word[0] for word in words]).upper()  ## we iterate here because we want the intitals of every part of name e.g Jammu Kashmir Bank would be JKB and in our case it woulb be NB for Nextgen Bank
    
    remaining_length = 12 - len(prefix) -1 # Username length should ideally be a fixed number (for example, 8 or 10 characters)
    
    random_chars = "".join(random.choices(string.ascii_uppercase + string.digits, k= remaining_length)) # Here we are using the random to generate a unique username for the bank user(by which he would be identified)
                                                                                                        # and below we are attaching the prefix to this username. The prefix part specifies the Bank Name and the other
                                                                                                        # part the unique username
    
    username = f"{prefix}--{random_chars}" ## appending the prefix and random username generated
    
    return username ## the username might look like NB--M1H8O9AEOP


## Now we are going to create a custom function to validate email addresses using Django's validate email method
def validate_email_address(email):   ## This function validates whether the given email address follows the correct email format (for example, having @ and a valid domain structure). It uses Django’s built-in validate_email,
                                     ## which checks only the syntax and structure of the email, not whether the email actually exists or can receive messages. This is field-level validation because it validates only one field \
                                     ## (the email address) and checks its format independently, without needing any other fields or context.
    
    try:
        validate_email(email)
        
    except ValidationError:
        raise ValidationError (gettext_lazy("Enter a valid Email Address"))
    
    
    
    
    