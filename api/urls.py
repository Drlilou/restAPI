from django.urls import path,include
from . import views

from rest_framework.urlpatterns import format_suffix_patterns
urlpatterns = [
    
  
    path('accounts/signup/client/', views.ClientSignupView.as_view()),#post
    path('accounts/signup/driver/', views.DriverSignupView.as_view()),#post
    path('accounts/login/'        , views.CustomAuthToken.as_view()),#post
    path('accounts/logout/'       , views.LogoutView.as_view()),#post
    path('clients/'          ,views.getClient),
    path('clients/<pk>/'          ,views.getClient)
   
]


#urlpatterns = format_suffix_patterns(urlpatterns)