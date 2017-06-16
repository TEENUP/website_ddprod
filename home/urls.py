from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home_list, name='home_list'),
    url(r'^contact_us', views.contact_us, name='contact_us'),
    url(r'^sign_up', views.sign_up, name='sign_up'),
    url(r'^about_us', views.about_us, name='about_us'),
    url(r'^dashboard', views.dashboard, name='dashboard'),
    url(r'^plans', views.plans, name='plans'),
    url(r'^user_profile',views.user_profile,name = 'user_profile'),
]