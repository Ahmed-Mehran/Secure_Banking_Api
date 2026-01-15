## This file would include two custom forms for user management. The first is going to be user creation form and next one is user updation form. Both of these will extend Django's built in forms and add
## custom fields and validation logic. 

##### ---- diff between django serializers and django forms
# Django forms and DRF serializers serve different purposes but share similar ideas. Django forms are mainly used to create HTML form fields so that users can enter data through a web page, and they also handle cleaning and
# validating that input before saving it to the database. Django REST Framework serializers, on the other hand, are used to convert data to and from JSON (or other formats) so it can be sent and received through APIs. Even
# though their outputs are different (HTML vs JSON), both are responsible for validating data.
# In both forms and serializers, field-level validation mostly happens automatically. For example, if a field is required, has a max length, or must be an email, Django checks all of that for you. If the data is invalid, 
# errors are raised automatically. Object-level validation is where you add your own rules that depend on multiple fields together, such as checking if two passwords match or if a date range is valid. This type of validation
# is custom and must be written manually in both forms (clean() method) and serializers (validate() method).
# So in simple words: forms are for user input through web pages, serializers are for data exchange through APIs, but both validate data in almost the same way, using automatic field checks and custom object-level rules when needed.


### --- What is UserCreationForm
# When you use UserCreationForm, Django automatically converts important User model fields into form fields, shows them as input boxes, and handles basic validation for you. Most importantly, it already includes password1 and
# password2 fields and checks that both passwords match and follow Django’s password rules (like minimum length, common password checks, etc.).
# This form also takes care of securely hashing the password before saving the user to the database, which is very important for security. You can still customize it by extending the form to add extra fields (like email or full name)
# or add your own validations. In simple words, UserCreationForm makes user signup easy by giving you a ready-made, secure, and validated form that turns user input into a properly saved User object.

from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy

from .models import User

class DjangoUserCreationForm(UserCreationForm):
    
    class Meta:
        
        model = User
        
        fields = [
            "email",
            "id_no",
            "first_name",
            "middle_name",
            "last_name",
            "security_question",
            "security_answer",
            "is_staff",
            "is_superuser",
        ]                             ####### ------   Confusion: why isnt password included in the fields option. I clearly know that the field names that are included in the fields option, those would only appear to the User while 
                                      #                registering or filling the form?? why isnt that here
                                      ####### ------   Answer: The reason password is not listed in fields is because UserCreationForm already adds password fields by itself. Internally, UserCreationForm defines password1 and password2
                                      #                        (password and confirm password) as form fields, even though they are not model fields. Since they are not part of your User model directly, you should not include them in
                                      #                        Meta.fields. Django automatically shows these password inputs on the form, validates them (match check, strength rules), hashes the password, and stores it in the hidden 
                                      #                        password field inherited from AbstractUser(user model is inheriting from this AbstractUser)
                                      #                        In short: We don’t mention password1 and password2 in Meta.fields because they are not model fields of our custom User model. They are form-only fields provided by 
                                      #                        UserCreationForm. Since we inherit from UserCreationForm, these two password fields automatically appear in the registration form, get validated, and Django then saves 
                                      #                        the hashed password into the model’s single password field.
                             
                                      
                                      
         
    def clean_email(self):                        ## See this clean_email() in a Django form plays the same role as validate_email() in a Django REST Framework serializer. Both are field-level validation methods. Django automatically 
                                                   # calls clean_email() when the form is validated, just like DRF automatically calls validate_email() when a serializer is validated. The purpose of both is to add extra validation logic
                                                   # on top of Django’s built-in checks. Here, the built-in validation already ensures that the email has a valid format, and this method adds an additional rule: checking whether the email 
                                                   # already exists in the database. If it does, a validation error is raised; otherwise, the cleaned (valid) email is returned. So yes, you can safely say that clean_<field>() in forms and
                                                   # validate_<field>() in serializers are conceptually the same—they are both used for custom field-level validation.
                                                   # These validations are automatically called when a user is trying to register e.g if a user registers with email, first of all the in built validations, provided by UserCreationForm
                                                   # here and model.serializers for serializers, these built in validations check if the email is in right format and then this field level validations check for addition validations.
                                                   # In short: Built-in validations run first (like checking email format), and then custom field-level validations (clean_email in forms or validate_email in serializers) run automatically
                                                   # to check additional rules.
                                                   
        
        email = self.cleaned_data.get("email")
        
        if User.objects.filter(email=email).exists():
            raise ValidationError(gettext_lazy("A user with that email already exists."))
        
        return email
    
    
    


