from django.urls import path,include
from . import views

from rest_framework.urlpatterns import format_suffix_patterns
urlpatterns = [
    
    #login/signup
    path('accounts/signup/client/', views.ClientSignupView.as_view()),#post
    path('accounts/signup/driver/', views.DriverSignupView.as_view()),#post
    path('accounts/login/'        , views.CustomAuthToken.as_view()),#post
    path('accounts/logout/'       , views.LogoutView.as_view()),#post
    #clients
    path('clients/'               ,views.getClients),
    path('clients/<pk>/'          ,views.getClient),
    #driver
    path('drivers/'               ,views.getDrivers),
    path('drivers/<pk>/'          ,views.getDrivers),
    path('drivers/<pk>/activate'  ,views.activateDriver)
]   


#urlpatterns = format_suffix_patterns(urlpatterns)