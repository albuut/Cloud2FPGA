"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf import settings #library for storing images
from django.conf.urls.static import static #library for storing images
from django.urls import include, path
from django.conf.urls import url
from account.api.views import ChildCreateView

urlpatterns = [
    path('api/', include('api.urls')),
    path('admin/', admin.site.urls),
    path('account/',include('account.api.urls', 'accounts')), #This was in the api folder I and it didnt work
    #when i put it in the backend it worked. made it unique kept getting error
    path('parent/<int:id>/child/create/', ChildCreateView.as_view(), name='create_child'),
    #REST
    path('api/account/', include('account.api.urls', 'account_api')),
    #url(r'^', include('account.api.urls'))

    
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
