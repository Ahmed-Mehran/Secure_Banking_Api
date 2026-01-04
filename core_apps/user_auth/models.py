from django.db import models

## Now as we have created the User model manager, we can now define the Custom User Model
import uuid
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.utils.translation import gettext_lazy

from .emails import send_account_locked_email
from .Managers import UserManager


class User(AbstractUser):
    
    class SecurityQuestions(models.TextChoices):
        MAIDEN_NAME = (
            "maiden_name",
            gettext_lazy("What is your mother's maiden name?"),
        )
        FAVORITE_COLOR = (
            "favorite_color",
            gettext_lazy("What is your favorite color?"),
        )
        BIRTH_CITY = (
            "birth_city", 
            gettext_lazy("What is the city where you were born?")
        )
        CHILDHOOD_FRIEND = (
            "childhood_friend",
            gettext_lazy("What is the name of your childhood best friend?"),
        )
    
    
