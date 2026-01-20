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

### After configuring the settings of DRF spectacular in base.py, we can now add drf spectacular URLS to this main URLS.py file.
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from django.conf import settings
urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    
    ## These url for DRF spectactular are by default provided
    path("api/v1/schema/", SpectacularAPIView.as_view(), name="schema"), 
    
    path("api/v1/schema/swagger-ui/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    
    path("api/v1/schema/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc")
]




## The lines below are purely Django Admin customization, not relared to DRF spectacular:
## site_header → The big title at the top of the admin panel
## site_title → The browser tab title
## index_title → The heading on the admin dashboard home page
admin.site.site_header = "NextGen Bank Admin"
admin.site.site_title = "NextGen Bank Admin Portal"
admin.site.index_title = "Welcome to NextGen Bank Admin Portal"
#### -- CONFUSION: But why the above in the urls.py and not admin.py if they are admin related
#### -- ANSWER: Those lines are often placed near urls.py (or project setup code) simply because the admin site is initialized and loaded when URLs are configured. At that point, admin.site is guaranteed to
#               exist, so setting site_header, site_title, and index_title works safely. Conceptually, they belong to the admin, not to URLs — and yes, putting them in admin.py is also perfectly correct. Many
#               developers prefer urls.py or a central config file just to keep all global project-level customizations in one place, especially things that affect how the admin site looks when accessed via its URL.
#               In short: They’re in urls.py for convenience and visibility during project setup, not because they are URL-related.

