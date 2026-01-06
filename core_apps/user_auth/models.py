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
        
    class AccountStatus(models.TextChoices):
        ACTIVE = "active", gettext_lazy("Active")
        LOCKED = "locked", gettext_lazy("Locked")

    class RoleChoices(models.TextChoices):
        CUSTOMER = "customer", gettext_lazy("Customer")
        ACCOUNT_EXECUTIVE = "account_executive", gettext_lazy("Account Executive")
        TELLER = "teller", gettext_lazy("Teller")
        BRANCH_MANAGER = "branch_manager", gettext_lazy("Branch Manager") ## The first value i.e. "branch_manager" gets actually stored in DB and "Branch Manager" is what will appear to the User/Client
        
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(gettext_lazy("Username"), max_length=12, unique=True)
    security_question = models.CharField(
        gettext_lazy("Security Question"),
        max_length=30,
        choices=SecurityQuestions.choices,
    )
    security_answer = models.CharField(gettext_lazy("Security Answer"), max_length=30)
    email = models.EmailField(gettext_lazy("Email"), unique=True, db_index=True)
    first_name = models.CharField(gettext_lazy("First Name"), max_length=30)
    middle_name = models.CharField(
        gettext_lazy("Middle Name"), max_length=30, blank=True, null=True
    )
    last_name = models.CharField(gettext_lazy("Last Name"), max_length=30)
    id_no = models.PositiveIntegerField(gettext_lazy("ID Number"), unique=True)
    account_status = models.CharField(
        gettext_lazy("Account Status"),
        max_length=10,
        choices=AccountStatus.choices,
        default=AccountStatus.ACTIVE,
    )
    role = models.CharField(
        gettext_lazy("Role"),
        max_length=20,
        choices=RoleChoices.choices,
        default=RoleChoices.CUSTOMER,
    )
    failed_login_attempts = models.PositiveSmallIntegerField(default=0)
    last_failed_login = models.DateTimeField(null=True, blank=True)
    otp = models.CharField(gettext_lazy("OTP"), max_length=6, blank=True)
    otp_expiry_time = models.DateTimeField(gettext_lazy("OTP Expiry Time"), null=True, blank=True)

    objects = UserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "first_name",
        "last_name",
        "id_no",
        "security_question",
        "security_answer",
    ]
    
    

        
    
    
    
