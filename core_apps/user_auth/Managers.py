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
    

## Now we will define our custom manager class which is going to extend django's built in user manager(UserManager)
class UserManager(UserManager):  ## The code for is totally same the User manager in the Mosaic Blueprint
    
    def _create_user(self, email, password, **extra_fields):   ## This is our private helper method that is going to be used to handle the user creation(private because it has _create, i.e dash before create and we dont call these methods directly)

        if not email:
            
            raise ValueError(gettext_lazy("An email address must be provided"))
        
        if not password:
            
            raise ValueError(gettext_lazy("A Password must be provided"))
        
        username = generate_username()
        
        email = self.normalize_email()
        
        validate_email_address(email)
        
        user = self.model(
            
            username = username,
            email = email,
            **extra_fields
        )
        
        user.password = make_password(password)
        user.save(using=self._db)
        
        return user
    
    def create_user(self, email, password, **extra_fields):
        
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_staff', False)
        
        return self._create_user(email, password, **extra_fields)
    
    def create_superuser(self, email, password, **extra_fields): 
        
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(gettext_lazy('Superuser must have is_staff=True.'))

        if extra_fields.get('is_superuser') is not True:
            raise ValueError(gettext_lazy('Superuser must have is_superuser=True.'))

        return self._create_user(email, password, **extra_fields)
    
## Qs.  See above we are defining a custom way to create and store user objects in the model. We are doing this because we are not working with the Default User model, we are working with a Custom user model and
# for that we have to define a custom way to create and store users. That is what UserManagers() are for Now one confusion is that generally we directly define the UserManager() class and make it inherit from
# Baseusermanager so we could easily get methods like normalize email and other, but why the tutor hasnt done that here and can we do that like class UserManager(BaseUserManager):
        
## Sol.  Your understanding of why UserManagers exist is correct, and the confusion you have is very valid. Normally, when we create a fully custom user model, we define our own manager by inheriting from BaseUserManager
#  so we get helper methods like normalize_email() and full control over user creation. In your case, the tutor has chosen to inherit from Django’s built-in UserManager instead, which already extends BaseUserManager 
#  internally and already provides useful methods like normalize_email() and the standard user-creation behavior. By inheriting from UserManager, the tutor is essentially reusing Django’s default user manager logic 
#  while slightly customizing it to fit the project’s needs, instead of rebuilding everything from scratch. Yes, you absolutely can write class UserManager(BaseUserManager), and many projects do exactly that, but 
#  inheriting from UserManager is also valid and sometimes preferred when you want Django’s default behavior plus small custom changes.
        
            
            
    
    
    
    