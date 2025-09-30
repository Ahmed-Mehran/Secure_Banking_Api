"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path


#from .settings.local import ADMIN_URL
# urlpatterns = [
#     path(ADMIN_URL, admin.site.urls),
    
# ]
## Can do the above as well but the above is not flexible as settings could be from production as well, so we do the below

from django.conf import settings
urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
]

