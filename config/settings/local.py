from os import getenv, path
from dotenv import load_dotenv
from .base import *
from .base import BASE_DIR


local_env_file = BASE_DIR / ".env" / ".env.local"

if path.isfile(local_env_file):  
    load_dotenv(local_env_file)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = getenv("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = getenv("DEBUG")

SITE_NAME = getenv("SITE_NAME")

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "0.0.0.0"] ## the domain names that would be in allowed_hosts would only be able to access the server of this application, but here we keep it empty because we are running it locally
                   ## Basically when someone makes a request to your server, Django looks at the Host header in the HTTP request (basically, the domain name used to reach your app).
                   #  If that domain name is not listed in ALLOWED_HOSTS, Django immediately rejects the request with a 400 Bad Request error. 
                   
ADMIN_URL = getenv("ADMIN_URL") ## This setting defines the URL path where your Django admin panel will be accessible. By default, Django uses /admin/, but here it’s being taken from an environment variable 
                                # (ADMIN_URL). This is a security best practice — instead of leaving it as /admin/ (which is predictable for attackers), you can set something like /secure-admin-123/.
                                # We can in main urls.py do something like, urlpatterns = [path(settings.ADMIN_URL, admin.site.urls),], we could technically do path("super-secret-admin/", admin.site.urls), if we
                                # want to change the admin url but It hardcodes the URL, which is not flexible and If you need a different admin URL for staging vs production, you’d have to edit urls.py every time.
                   
EMAIL_BACKEND = "djcelery_email.backends.CeleryEmailBackend" ## By default, Django uses the synchronous email backend (django.core.mail.backends.smtp.EmailBackend). That means When a user does something that triggers 
                                                            # an email (like registering or resetting a password), Django will connect to the mail server immediately and send the email. This takes time
                                                            # (sometimes a few seconds), and the user has to wait before the page loads or the response is sent back.
                                                            # With djcelery_email.backends.CeleryEmailBackend, Django doesn’t directly send emails; instead, it places the "send email" task into a Celery task 
                                                            # queue, where a separate worker process running in the background picks it up and sends the email, allowing the user to get an immediate response
                                                            # without waiting, which makes the application faster, more scalable, and more user-friendly, especially when handling many emails like confirmations,
                                                            # notifications, or password resets.

EMAIL_HOST = getenv("EMAIL_HOST") ## This defines the mail server address that Django will connect to for sending emails. For example, if you’re using Gmail, your host would be smtp.gmail.com. If you’re 
                                  # using something like AWS SES, Mailgun, or SendGrid, they give you their own SMTP host. Storing this in an environment variable allows you to switch email providers without changing your code.

EMAIL_PORT = getenv("EMAIL_PORT") # This specifies the port number used to connect to the email server.

DEFAULT_FROM_EMAIL = getenv("DEFAULT_FROM_EMAIL") ## This is the default email address that will appear in the "From" field when your Django app sends an email. For example, you might want all your emails to 
                                                  ## come from mehran@gmail.com. Instead of hardcoding it, you take it from an environment variable so you can set a different "from" email in production,
                                                  # staging, or local testing. THIS IS THE EMAIL ADDRESS THAT DJANGO USES TO SEND THE EMAIL

DOMAIN = getenv("DOMAIN") ## This represents your project’s domain name (e.g., mywebsite.com).

MAX_UPLOAD_SIZE = 1 * 1024 * 1024 ## This sets the maximum allowed file size for uploads in your project. Here, it’s set to 1 MB (because 1 * 1024 * 1024 = 1,048,576 bytes = 1 MB). This is used to prevent users
                                  # from uploading excessively large files (like videos or huge images) that could slow down or crash your server. You can enforce this limit in file fields or forms.




                   

