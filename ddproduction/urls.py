"""ddproduction URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
# from django.conf.urls import include,url
# from django.contrib import admin
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

admin.autodiscover()


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'', include('home.urls')),
    url(r'^contact_us/', include('home.urls')),
    url(r'^sign_up/', include('home.urls')),
    url(r'^login/', include('home.urls')),
    url(r'^about_us/', include('home.urls')),
    url(r'^dashboard/', include('home.urls')),
    url(r'^plans/', include('home.urls')),
    url(r'^user_profile/', include('home.urls')),
    url(r'^contact/' , include('home.urls')),
    url(r'^logout/' , include('home.urls')),
    url(r'^thanks/' , include('home.urls')),
    url(r'^buy/', include('home.urls')),
    url(r'^slide/', include('home.urls')),
    url(r'^all/', include('home.urls')),
    url(r'^single/', include('home.urls')),
    url(r'^singles/', include('home.urls')),
    url(r'^TermsAndConditions/', include('home.urls')),
    url(r'^buyProducts/', include('home.urls')),
    url(r'^paymentGateway/', include('home.urls')),
    url(r'^popup/', include('home.urls')),
    url(r'^myHome/', include('home.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
