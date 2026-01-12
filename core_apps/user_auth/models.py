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
    
    USERNAME_FIELD = "email"  ## This tells Django that email is the main identifier for login, instead of the default username. So whenever authentication happens (login, password reset, etc.), Django will treat the email
                               # field as the unique login field.
    
    REQUIRED_FIELDS = [
        "first_name",
        "last_name",
        "id_no",
        "security_question",
        "security_answer",
    ]                         ## REQUIRED_FIELDS applies only when creating a user via Django management commands, especially createsuperuser on the command line. When users are created through the frontend or APIs, Django
                               # does not enforce REQUIRED_FIELDS automatically. In those cases, validation is handled by your forms, serializers, or custom logic, not by REQUIRED_FIELDS. So for client-side user creation, 
                               # you must explicitly validate and require those fields.
                               # When you run python manage.py createsuperuser, Django first asks interactively only for the fields listed in REQUIRED_FIELDS (plus the USERNAME_FIELD). However, when the user is finally saved
                               # to the database, Django must still satisfy all model-level requirements. That means if a model field does not have blank=True, null=True, or a default value, then it must receive a value 
                               # somehow, otherwise saving the superuser will fail. Because the createsuperuser command only prompts for fields in REQUIRED_FIELDS, the practical and correct approach is to include all 
                               # mandatory (non-nullable, non-blank) fields in REQUIRED_FIELDS, so Django asks for them during the command. So yes — while REQUIRED_FIELDS controls what Django asks you for, model field 
                               # constraints control what must exist, and to avoid errors, they should align
    
    
    class SecurityQuestions(models.TextChoices):  ## Choice field classes options
        
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
        
        ## The crux of above is that we have these options(Maiden_name, Favorite_color, Birth_City) like drop down options for security_question field and user can choose from any of these only and once the user chooses that 
        # would be saved to DB for security_question field. For example user chooses MAIDEN_NAME, the user will get a question display as "What is your mother's maiden name?" and "maiden_name" would be saved to DB for the 
        # field value of security_question. Then in security_answer field we simple store the ans of the question. Now one might say we have CLASS_CHOICES field in Fitness-Studio-Booking-API Project, how this is different
        # from that. See first of all both are same in terms of logic, that is for a particular DB attribute we get to choose from the specified/fixed options. In the fitness model, we explicitly define a CLASS_CHOICES list
        # and attach it to a single field (like class_name), so that field can take one value from many options such as yoga, zumba, or hiit. In the security question case, we don’t have a separate CLASS_CHOICES variable for
        # one field; instead, we use models.TextChoices, where each option (like maiden_name, favourite_color, birth_city) represents a different predefined question. The user selects only one of these options, and that 
        # selected value (for example maiden_name) is stored in the database. Based on that value, the system knows which question text to show (like “What is your mother’s maiden name?”). The answer field then simply stores
        # the user’s answer to that chosen question.
        
    class AccountStatus(models.TextChoices): ## Choice field classes options
        
        ACTIVE = "active", gettext_lazy("Active")
        LOCKED = "locked", gettext_lazy("Locked")

    class RoleChoices(models.TextChoices):  ## Choice field classes options
        
        CUSTOMER = "customer", gettext_lazy("Customer")
        ACCOUNT_EXECUTIVE = "account_executive", gettext_lazy("Account Executive")
        TELLER = "teller", gettext_lazy("Teller")
        BRANCH_MANAGER = "branch_manager", gettext_lazy("Branch Manager") ## The first value i.e. "branch_manager" gets actually stored in DB and "Branch Manager" is what will appear to the User/Client
        
        
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) ## This creates a UUID-based primary key instead of an auto-incrementing integer. UUIDs are hard to guess, globally unique,
                                                                                 # and more secure, especially useful in APIs and distributed systems.
                                                                                 
    username = models.CharField(gettext_lazy("Username"), max_length=12, unique=True) ## This stores a system-generated username that uniquely identifies the user internally. Even though login uses email,
                                                                                       # usernames are still useful for internal references and display.
                                                                                       # The username field is not for the user to enter. It exists only so the system has a unique name to store in the database for each user.
                                                                                       # The user is not even required to enter value for this field and thus this field would not be visible to the user(in user form).
                                                                                       # Since your system uses email as the login field, the username is automatically generated inside the _create_user method(of UserManager) and then saved
                                                                                       # to the database. Its purpose is to give the system a stable, unique identifier that can be used internally (for references, logs, relationships,
                                                                                       # or display if needed) without depending on user input. Because it is generated by the backend, it makes perfect sense to hide this field from 
                                                                                       # user-facing forms, since the user never needs to know or edit it. So yes — the username field is there so the auto-generated username has a place
                                                                                       # to be stored, and keeping it hidden from the user is a clean and intentional design choice.
                                                                                       
    
    security_question = models.CharField(  ## This field stores a single value chosen from above security question field
        gettext_lazy("Security Question"),
        max_length=30,
        choices=SecurityQuestions.choices,
    )
    security_answer = models.CharField(gettext_lazy("Security Answer"), max_length=30)  ## Stores the answer of the security question
    
    email = models.EmailField(gettext_lazy("Email"), unique=True, db_index=True)  ## This stores the user’s email address and ensures it is unique, meaning no two users can share the same email. The database index makes email lookups faster during login
    
    first_name = models.CharField(gettext_lazy("First Name"), max_length=30)  ## This stores the user’s first name. It is required and commonly used for personalization and identification.
    
    middle_name = models.CharField(gettext_lazy("Middle Name"), max_length=30, blank=True, null=True) ## This stores the middle name, but it is optional. blank=True allows forms to accept it empty, and null=True allows the database to store it as empty.
    
    last_name = models.CharField(gettext_lazy("Last Name"), max_length=30) ## This stores the user’s last name and is required for proper identification and official records.
    
    id_no = models.PositiveIntegerField(gettext_lazy("ID Number"), unique=True) ## This stores a government or bank-issued ID number. It must be unique, ensuring that one real person cannot register multiple accounts.
    
    account_status = models.CharField(    ## value of this is chosen from above AccountStatus Enum class, default is Active(if no value is given)
        gettext_lazy("Account Status"),
        max_length=10,
        choices=AccountStatus.choices,
        default=AccountStatus.ACTIVE,
    )
    
    role = models.CharField(      ## ## value of this is chosen from above Role Enum class, default is Customer(if no value is given)
        gettext_lazy("Role"),
        max_length=20,
        choices=RoleChoices.choices,
        default=RoleChoices.CUSTOMER,
    )
    
    failed_login_attempts = models.PositiveSmallIntegerField(default=0)   ## This keeps count of how many times the user has entered a wrong password. It is used to decide when to lock the account.
    
    last_failed_login = models.DateTimeField(null=True, blank=True)  ## This stores the timestamp of the last failed login attempt. It helps in calculating lockout duration and resetting attempts after time passes.
    
    otp = models.CharField(gettext_lazy("OTP"), max_length=6, blank=True) ## See this field, one might think is for user to directly enter/store an OTP. But that is wrong, a user(in displayform) would not even see
                                                                           # this field. That is why its kept blank=True. So a value for this could be provided dynamically. If you remember with Mosaic Blueprint project,
                                                                           # we had the same concept. We had a OTP field and value for it was provided when e.g a user wanted to reset the password. And this field is 
                                                                           # particularly used for that. Its kept blank initially when the user registers. Then if he wants to login via OTP or wants to reset his password.
                                                                           # Same numeric code would be saved to this OTP field and the same code would be sent to email for the whole verification process
    
    otp_expiry_time = models.DateTimeField(gettext_lazy("OTP Expiry Time"), null=True, blank=True)  ## This field stores the exact date and time when the OTP becomes invalid. It is kept null=True and blank=True because initially,
                                                                                                     # when the user is created, no OTP exists, so there is no expiry time to store. When an OTP is generated, the backend sets this
                                                                                                     # field to a future time (for example, current time + 1 minute). During verification, the system checks this value to ensure the
                                                                                                     # OTP has not expired. This prevents old or reused OTPs from being accepted and is a crucial part of secure OTP-based authentication.

    objects = UserManager()     ## This connects your custom UserManager to the model. All user creation and database saving logic will go through this manager, which is required because you are using a custom user model.
    




    ## Now Below are some methods that we define within this User model. See these methods are invoked by the user instance/object that you have created and saved to DB. So we can initiate them user.set_otp(). 
    #  Just remember these methods can be accessed by user instance/object
    
    def set_otp(self, otp: str) -> None:      ## Now the above method is basically saving the OTP data for the OTP field. If you remember we had generate_OTP method in utils.py and by that we could generate OTP and share in
                                               # this method as parameter. The self.OTP is basically user.OTP i.e. the OTP field of current DB user. Here we are setting the user OTP field to generated OTP and also now setting 
                                               # up an expiry time. See this method would be most likely called when a user wants to login by OTP or wants to reset password. At that time he can use this set_otp() method
                                               # Here self refers to the current instance/object of the model
        
        self.otp = otp
        
        self.otp_expiry_time = timezone.now() + settings.OTP_EXPIRATION
        
        self.save()
        


    def verify_otp(self, otp: str) -> bool:     ## In this method we are going to check if the provided OTP is valid and within allowed time frame. In simple words, this method checks whether the OTP entered by the user matches
                                                 # the OTP stored in the database and whether it is still valid (not expired). Here, self.otp is the OTP saved in the user’s database record, and the otp parameter is the OTP that
                                                 # the user typed in (usually from the email they received). The OTP argument in parameter is not the one that is generated from generate_otp method. It is different from what we 
                                                 # did above method. In short, the otp parameter here is the OTP entered by the user, not the one generated by generate_otp. If both the OTP values match and the current time is 
                                                 # still before the expiry time, the OTP is considered valid. When the OTP is valid, the method clears the OTP and expiry time from the database and saves the user, so the same
                                                 # OTP cannot be reused again. Clearing out and resetting the OTP is needed, first to prevent reuse and also for further OTP verifications.
                                                 # The OTP is reset only when verification succeeds, not when it fails. If verification fails, the OTP remains unchanged so the user can try again (until it expires).
        
        if self.otp == otp and self.otp_expiry_time > timezone.now():     
            
            self.otp = ""
            
            self.otp_expiry_time = None
            
            self.save()
            
            return True
        
        return False

    def handle_failed_login_attempts(self) -> None:      ## This method is a model instance method, so it is always called on a specific user object (for example, user.handle_failed_login_attempts()). Django does not call it 
                                                          # automatically — it is usually called from your login or authentication logic when a login attempt fails (for example, when password verification fails or when verify_otp()
                                                          # returns False). Each time it is called, it increases the failed_login_attempts count and stores the current time as the last failed attempt. If the number of failed attempts
                                                          # reaches or exceeds settings.LOGIN_ATTEMPTS, the user’s account status is changed to LOCKED, the user record is saved, and an account-locked email is sent. If the limit has 
                                                          # not yet been reached, the method simply updates and saves the failed attempts count. This is exactly how account lockout logic is typically implemented.
        
        self.failed_login_attempts += 1
        
        self.last_failed_login = timezone.now()
        
        if self.failed_login_attempts >= settings.LOGIN_ATTEMPTS:
            
            self.account_status = self.AccountStatus.LOCKED
            
            self.save()
            
            send_account_locked_email(self)
            
        self.save()


    
    def reset_failed_login_attempts(self) -> None:          ## this method is used to clear all failure-related data once the user successfully verifies. When a user enters a wrong OTP, verify_otp() returns False, and your login logic
                                                             # can call handle_failed_login_attempts() to increase the failed_login_attempts count. When the user finally enters the correct OTP and verify_otp() returns True, this 
                                                             # reset_failed_login_attempts() method is called to reset the failed attempts back to zero, clear the last failed login time, and mark the account as ACTIVE again. This 
                                                             # ensures that past mistakes don’t keep affecting the user after a successful verification and keeps the account state clean and correct.
        
        self.failed_login_attempts = 0
        
        self.last_failed_login = None
        
        self.account_status = self.AccountStatus.ACTIVE
        
        self.save()