from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User
from .forms import CustomUserChangeForm, CustomUserCreationForm


###### ---- Confusion: When we use admin.site.register() and the below method for registering models on admin panel
###### ---- ANSWER: See when registering models on admin panel(in admin.py) we can do it in two ways. The simplest way is writing admin.site.register(model_name). In this we just directly register the model on admin panel
#                   and actually we dont customize it at all. But if we want to customize our model so that it may appear a specific way on admin panel we use a decorator with class i.e. @admin.register(model_name) and a class().
#                   In simple terms, admin.site.register(ModelName) is the quickest way to make a model appear in the Django admin, but it uses default behavior with no customization. If you want to control how the model looks or
#                   behaves in the admin—such as which fields are shown, how they’re ordered, adding search, filters, or custom forms—you use @admin.register(ModelName) with a class. This second approach gives you full control
#                   over the admin interface for that model while still registering it at the same time.
#                   Now when we mostly work with customizing the model for admin, we mostly work with admin.ModelAdmin i.e make our class inherit from this model(e.g class CategoryAdmin(admin.ModelAdmin), like we have used in ecommerce project)
#                   This admin.ModelAdmin can be used for customizing when working non User models but UserAdmin is different. UserAdmin is a special admin class provided by Django specifically for the User model. It already knows how to handle
#                   user-specific things like passwords, permissions, groups, staff status, superuser flags, and the special “add user” vs “change user” forms in the admin panel. So below when we write CustomUserAdmin(UserAdmin):, we are
#                   extending Django’s built-in User admin behavior, not starting from scratch. This is why you can plug in form (for editing users) and add_form (for creating users) safely, and Django will still handle password hashing, permission
#                   logic, and admin UI correctly. So in very simple words: ModelAdmin → use for normal models where you just want to customize how fields look or behave, UserAdmin → use only for User models, because users are special and need 
#                   extra built-in logic. 

@admin.register(User)    ## This decorator tells Django: “I want to register the User model in the admin panel, and I want to control how it looks using the class written below.” 
class CustomUserAdmin(UserAdmin):     ## Here we are creating a custom admin configuration for the User model. We inherit from UserAdmin (not ModelAdmin) because users are special in Django. UserAdmin already knows how to handle passwords, 
                                       # permissions, groups, superusers, and separate add/change forms. By inheriting it, we keep all that logic and just customize what we need.
                                       
                                       
    
    ### --- CONFUSION: why do we have form and add_form here in this UserAdmin logic and not when we customize with admin.ModelAdmin(for store app in ecommerce proj)
    ### --- SOLUTION : When you register a model with admin.ModelAdmin (like CategoryAdmin(admin.ModelAdmin)), Django automatically generates a default ModelForm behind the scenes for both add and change operations. This auto-generated
    #                  form is based directly on the model fields and basic model-level validation. Because Category-like models are usually simple (name, slug, description, etc.), the default behavior is sufficient, so you don’t need 
    #                  to explicitly define or attach a form. Django handles everything for you without you even noticing the form layer. BUT THE MAIN FACT THAT WE DONT DEFINE A FORM FIELD FOR CategoryAdmin(admin.ModelAdmin) is, see for
    #                  the CategoryAdmin(admin.ModelAdmin) i.e using the admin.ModelAdmin we could also define a form field i.e not use the default auto-generated ModelForm, if we had a form.py for category model. In our e-commerce proj, 
    #                  we dont have a custom forms.py for category model and thus we use the default one. If we had a custom form we could simple define it by form = CategoryForm under class CategoryAdmin(admin.ModelAdmin):. So main
    #                  difference is that if we have a custom form for a model, we could define it even if using admin.ModelAdmin for customizing. But if you have form and dont define it explicity, the admin.py would use a default one.
    #                  See for User model, using a default one is not possible because User model is not just data, it is security-critical. Creating a user and editing a user are two very different operations. On creation, we need things like:
    #                  password + confirm password, password hashing, initial permissions and flags and On update, we usually don’t re-enter passwords, must avoid showing raw password fields, may restrict which fields are editable. Because of
    #                  this, Django cannot safely rely on a single default ModelForm for users. And also this is the reason why we explicitly define form and add_form in UserAdmin, add_form → used when creating a user and form → used when
    #                  updating an existing user. 
    #                  Also form and add_form are not random variables. They are predefined hooks provided by Django’s UserAdmin class. In simple words: UserAdmin already knows when it is editing a user and when it is creating a user. The
    #                  form attribute tells Django which form to use while updating an existing user, and add_form tells Django which form to use while creating a new user from the admin panel. By setting these, you are plugging your custom
    #                  svalidation and fields into Django’s admin workflow instead of using the default forms.
    
    form = CustomUserChangeForm         ## This tells Django which form to use when editing an existing user in the admin panel. When an admin clicks “Change” on a user, Django will use CustomUserChangeForm instead of the default one. 
                                         # This allows you to control validations, visible fields, and behavior during user updates.
    
    add_form = CustomUserCreationForm    ## This tells Django which form to use when creating a new user from the admin panel. When an admin clicks “Add User”, Django uses this form. This is important because user creation needs password
                                          # confirmation, extra validations, and custom fields.
                                          
    
    model = User        ## This explicitly tells Django that this admin class is managing the User model. It makes the intent clear and avoids confusion, especially when working with custom user models.
    
    
    list_display = [               ## This controls which columns are shown in the user list page in the admin panel. Instead of just showing a username, Django will now show email, username, first name, last name, staff status, active status,
                                    # and role. This makes it easy for admins to quickly understand who the user is without opening each record. Basically whatever field we want to appear on admin panel for this User model, we can have that in
                                    # this list_display field and it will be visible on admin panel. This list_display is also provided by UserAdmin class. In short Any field you include here will be visible as a column in the admin panel’s user list.
        "email",
        "username",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
        "role",
    ]
    list_filter = ["email", "is_staff", "is_active", "role"]        ## list_filter is used to add filter options in the right sidebar of the Django admin list page, so an admin can quickly narrow down records without writing queries.
                                                                     # In your example, list_filter = ["email", "is_staff", "is_active", "role"] means Django will generate clickable filters for these fields. For boolean fields like 
                                                                     # is_staff and is_active, Django shows simple Yes / No filters, making it very easy to see only active users or only staff users. For role (usually a choice or FK field),
                                                                     # Django shows each role as a selectable option (e.g., Admin, Manager, User). While email is less commonly used as a filter (because it may have many unique values), Django
                                                                     # will still allow filtering by distinct email values if supported. If you have 1,000 users, an admin can click: is_active → Yes to see only active users, is_staff → Yes to
                                                                     # see staff members, role → Manager to see only managers. So its basically used when we want to view/filter results by a specific parameter like we can filter by is_active 
                                                                     # and we will get all the user with account status = is_active
    
    
    fieldsets = (                               ## So basically fieldsets are used to group fields of a common section. See if we have fields like first_name, last_name, email. We can have them as individual fields on admin panel or we can
                                                 # neatly organize them under one common section like Personal_information will contain these fields. So now instead of these three fields appearing individually, there would be a common section
                                                 # for them which would be Personal_information and as you would click on it, you would get the three fields(first_name,last_name,email). This is basically used when you have lot of DB fields and
                                                 # all of them appearing individually would be messy. Suppose you would want to change the last_name, then you would have to go through each field to look for this particular field. But with 
                                                 # sections you would know that this last_name field would be most probably under personal_information section. Just one small correction to make it perfectly accurate: Fields do not open on click 
                                                 # by default as the section is always visible, just grouped under a clear heading.
        (
            _("Login Credentials"),
            {
                "fields": (
                    "username",
                    "email",
                    "password",
                )
            },
        ),
        
        (
            _("Personal Information"),
            {"fields": ("first_name", "middle_name", "last_name", "id_no", "role")},
        ),
        
        (
            _("Account Status"),
            {
                "fields": (
                    "account_status",
                    "failed_login_attempts",
                    "last_failed_login",
                )
            },
        ),
        
        (
            _("Security"),
            {"fields": ("security_question", "security_answer")},
        ),
        
        (
            _("Permissions and Groups"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        
        (
            _("Important dates"),
            {
                "fields": (
                    "last_login",
                    "date_joined",
                )
            },
        ),
    )
    
    search_fields = ["email", "username", "first_name", "last_name"]       ## This enables the search box in the admin panel. Admins can type a name or email and instantly find matching users. Without this, searching users would be painful.
    
    ordering = ["email"]        ## This defines the default ordering of users in the admin list page. Users will be sorted by email automatically, which is often more meaningful than sorting by ID.