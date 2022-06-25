from django.urls import path,include
from . import views
from . import notification_sender


from rest_framework.urlpatterns import format_suffix_patterns
urlpatterns = [
    
    #login/signup
    path('accounts/signup/client/', views.ClientSignupView.as_view()),#post
    path('accounts/signup/driver/', views.DriverSignupView.as_view()),#post
    path('accounts/login/'        , views.CustomAuthToken.as_view()),#post
    path('accounts/logout/'       , views.LogoutView.as_view()),#post
    #clients
    path('clients/'               ,views.getClients),
    path('clients/<pk>/'          ,views.getClient),#
    path('clients/fav/<pk>/'      ,views.getClientFav),
    path('client/addClientFav/'   ,views.addandDeleteClientFav),
    path('clients/updatePlamcent' ,views.updatePlacemntClient),
    path('clients/nearest'        ,views.getNearsetDriver),
    path('clients/createCoursa'   ,views.createCoursa),
    path('clients/endCoursa'      ,views.endCoursa),
    
    #driver
    path('drivers/'               ,views.getDrivers),
    path('drivers/<pk>/'          ,views.getDriver),
    path('drivers/<pk>/activate'  ,views.activateDriver),
    path('drivers/updatePlamcent' ,views.updatePlacemntDriver),
    path('drivers/voitures/<driver>/'       ,views.getVoiture),
    path('drivers/addvoitures'    ,views.addVoiture),
    path('drivers/chooseVoiture'  ,views.chooseVoiture),

    #categories
    path('category/'                ,views.getCategory),
    #notifcations
    path('notification/',            notification_sender.notification),

]   

#real time notifcations 
#https://medium.com/geekculture/add-real-time-notifications-to-your-django-project-6ee2aed38597
