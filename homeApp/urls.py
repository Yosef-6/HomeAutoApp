from django.urls import path
from .import views
urlpatterns = [
    path('index/', views.home, name = 'index'),
    path("login/",views.login_view,name="login"),
    path("logout/",views.logout_view,name="logout"),

    #API ROUTES
    path("create/<str:ID>",views.create_device,name="create"),
    path("deviceList/<str:ID>",views.device_list,name="deviceList"),
    path("delete/<str:ID>",views.delete_device,name="delete"),
    path("hardwareQuery/<str:ID>",views.hardware_query,name="Query"),
    path("deviceListUpdated/<str:ID>",views.device_list_updated,name="deviceListUpdated"),
    
]
