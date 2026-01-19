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

class CustomUserCreationForm(UserCreationForm):
    
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
                                                   # SO THIS IS A FIELD LEVEL VALIDATION OF EMAIL OF USER MODEL
                                                   
        
        email = self.cleaned_data.get("email")
        
        if User.objects.filter(email=email).exists():
            raise ValidationError(gettext_lazy("A user with that email already exists."))
        
        return email
    
    
    def clean_id_no(self):                         ## Now this again is a field level validation of id_no field of User model. Here we are checking that user always enters a unique id_no for it while registering
        
        id_no = self.cleaned_data.get("id_no")
        
        if User.objects.filter(id_no=id_no).exists():
            raise ValidationError(gettext_lazy("A user with that ID number already exists."))
        
        return id_no
    
    
    
    #### -------   CONFUSION:  Tell in me very simple words, if unique =True for email field in User model(and for id_no field as well), why do we still need this validation
    #### -------   ANSWER:  In very simple words: unique=True protects the database, but clean_email protects the user experience. When you set unique=True on the email field, Django will stop duplicate
    #                       emails from being saved at the database level. But if a user enters an email that already exists, the error will only come after form submission, often as a generic database
    #                       error that is not very user-friendly. The clean_field validation checks this before saving, during form validation itself. This lets you show a clear, friendly message like
    #                       “A user with that email already exists” instead of a confusing database error. So, unique=True is the final safety lock, and clean_email is an early, clean check to give a better experience.
    
    
    
    def clean(self):                  ## In Django forms, clean() plays the same role as validate() in DRF serializers—it is used for object-level validation, meaning validation that depends on multiple fields together 
                                       # and runs after all field-level validations have already passed. At this stage, Django has not created or saved a User instance yet; it is only working with validated form data.
                                       # In serializers, you receive all validated values inside the attrs dictionary, so you can directly do attrs["email"], attrs["is_superuser"], etc. In Django forms, the equivalent 
                                       # container is cleaned_data. The only correct and supported way to access all validated field values inside clean() is by calling cleaned_data = super().clean(). This ensures that
                                       # Django’s built-in cleaning logic and all clean_<field>() methods have already run, and you are working with safe, validated values.
                                       # This super().clean() is direct and intended equivalent of attrs in serializer validate() methods.
                                       # This method checks that regular users (non-superusers) must provide a security question and security answer. If the user is a superuser, these fields are allowed to be empty, so 
                                       # the validation is skipped. This is why a separate object-level validation is needed here.
        
        cleaned_data = super().clean()
        
        is_superuser = cleaned_data.get("is_superuser")
        
        security_question = cleaned_data.get("security_question")
        
        security_answer = cleaned_data.get("security_answer")

        if not is_superuser:
            
            if not security_question:
                self.add_error(
                    "security_question",
                    gettext_lazy("Security question is required for regular users"),
                )
            if not security_answer:
                self.add_error(
                    "security_answer",
                    gettext_lazy("Security answer is required for regular users"),
                )
                
        return cleaned_data
    
    
    def save(self, commit=True):            ## In very simple words, this save() method is giving you control over when the user is actually saved to the database, instead of always saving it immediately. Normally, when you call
                                             # form.save(), Django creates the user object and directly saves it to the database. But sometimes you want to modify the user first (set extra fields, hash a password, send OTP, etc.) 
                                             # before saving. That’s why this method overrides the parent save().
                                             # commit=True, This is a flag which says by default commit parameter is True, so normal behavior is unchanged.
        
        user = super().save(commit=False)    ## This calls the parent form’s save() method but tells it, "Create the user object in memory, but DO NOT save it to the database yet". At this point, user exists as a Python object, but
                                              # there is no database row yet.
                                              
                                              
        
        if commit:    ## If commit=True, now the user is finally saved to the database.
            user.save()
            
        return user
    ## THIS ABOVE PATTERN OF SAVING USER IS USEFUL, as this pattern lets you do things like: user = form.save(commit=False), set extra fields on user, then user.save() when you’re ready. Without this, Django would save the user 
    # immediately and you’d lose control. In short commit=True/False gives you control over saving. commit=False creates the object without saving, and commit=True saves it to the database. This is why we override save() here.
    ## SEE WE CAN ALSO MIMIC THE ABOVE DIRECTLY IN THE USER VIEW FUNCTION i.e. we can also in view function do something like user = form.save(), then overwrite the fields and then save again as it rewrites that field. 
    #  Doing form.save() and then modifying the user and calling user.save() again means the database is written twice i.e it still affects the same record, does not create two records. From a correctness point of view, this is completely
    #  safe and Django does this kind of thing in many real projects. The main downside is performance: each save() call is a database hit, and database calls are expensive when your system scales (many users, high traffic).
    #  In small or medium applications, this extra write is usually not a big problem and is totally doable. However, best practice is to avoid unnecessary DB writes when possible. That’s why people often use commit=False inside
    #  the form’s save() method—so you can set all required fields first and then save once.
    
    

## Now we would create a form that is going to be used for updating existing users. See now we have this UserChangeForm which is used for updating existing users. In terms of serializers if we think, UserCreationForm is used when creating
# a new user, just like a UserCreateSerializer(Mosaic blueprint project) in DRF, and UserChangeForm is used when updating an existing user, similar to a UserEditSerializer. The purpose (use case) of both pairs is the same: one handles 
# creation and the other handles updates. The main difference is how they work internally—forms deal with HTML form input and Django views, while serializers deal with JSON data and APIs—but conceptually they serve the same roles in 
# their respective worlds.
class CustomUserChangeForm(UserChangeForm):
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
            "is_active",
            "is_staff",
            "is_superuser",
        ]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.exclude(pk=self.instance.pk).filter(email=email).exists():  ## This exclude logic here allows the user to keep their existing email while updating their profile(user might want to change any other stuff except the email),
                                                                                     # because their own record is ignored in the filter check using exclude(pk=self.instance.pk). But if the new email they enter matches the email of any other user
                                                                                     # in the database (any record with a different primary key), then the validation fails and an error is raised. This way, email uniqueness is maintained across 
                                                                                     # all users, while still allowing a user to update their own details safely.
            
            raise ValidationError(gettext_lazy("A user with that email already exists."))
        
        return email

    def clean_id_no(self):
        
        id_no = self.cleaned_data.get("id_no")
        
        if User.objects.exclude(pk=self.instance.pk).filter(id_no=id_no).exists():
            raise ValidationError(gettext_lazy("A user with that ID number already exists."))
        
        return id_no
    
    
    def clean(self):      ## This is again the object-level validation, reused from user creation logic above, to ensure security question and answer are required for non-superusers.
        
        cleaned_data = super().clean()
        
        is_superuser = cleaned_data.get("is_superuser")
        
        security_question = cleaned_data.get("security_question")
        
        security_answer = cleaned_data.get("security_answer")

        if not is_superuser:
            
            if not security_question:
                self.add_error(
                    "security_question",
                    gettext_lazy("Security question is required for regular users"),
                )
                
            if not security_answer:
                self.add_error(
                    "security_answer",
                    gettext_lazy("Security answer is required for regular users"),
                )
                
        return cleaned_data
    
    


#### ----- CONFUSION: In ecommerce project we have used ModelForm inheritance for updating a user and here we are using UserChangeForm, what is the difference??
#### ----- ANSWER: In simple words, both approaches are used to update users, but they are meant for different levels of responsibility. When you inherit from 
#                  ModelForm, you are taking full control of how the form works, which fields appear, and how validation and saving happen. This is fine for small or simple projects, but it also means you are responsible 
#                  for handling sensitive things like passwords and authentication correctly, which can be risky. On the other hand, UserChangeForm is specially built by Django for updating user objects safely and correctly.
#                  It already understands how Django users work, how passwords should be handled, and how updates should behave in admin and authentication flows. That is why in your current project, which is security-focused,
#                  using UserChangeForm is better and safer, while ModelForm was acceptable in your earlier, simpler projects. Also if we compare in terms of serializers. a ModelForm is like a basic serializers.Serializer 
#                  because you manually decide what fields to expose and how things should work, and Django doesn’t assume much special behavior. On the other hand, UserCreationForm and UserChangeForm are more like ModelSerializer
#                  because they are tightly coupled to the User model and come with a lot of built-in behavior, rules, and safety (especially around passwords and user updates).



