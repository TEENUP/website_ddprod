from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home_list, name='home_list'),
    url(r'^contact_us', views.contact_us, name='contact_us'),
    url(r'^sign_up', views.sign_up, name='sign_up'),
    url(r'^login', views.login, name='login'),
    url(r'^about_us', views.about_us, name='about_us'),
    url(r'^dashboard', views.dashboard, name='dashboard'),
    url(r'^products', views.products, name='plans'),
    url(r'^user_profile',views.user_profile,name = 'user_profile'),
    url(r'^contact', views.contact, name='contact'),
    url(r'^logout', views.logout, name='logout'),
    url(r'^thanks/', views.thanks, name='thanks'),
    url(r'^buyAnotherProduct/', views.buyAnotherProduct, name='buyAnotherProduct'),
    url(r'^slide/', views.slide, name='slide'),
]