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
                   
ADMIN_URL = getenv("ADMIN_URL")
                   
EMAIL_BACKEND = "djcelery_email.backends.CeleryEmailBackend"

EMAIL_HOST = getenv("EMAIL_HOST")
EMAIL_PORT = getenv("EMAIL_PORT")
DEFAULT_FROM_EMAIL = getenv("DEFAULT_FROM_EMAIL")
DOMAIN = getenv("DOMAIN")

MAX_UPLOAD_SIZE = 1 * 1024 * 1024




                   

