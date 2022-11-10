from django.urls import path
from . import views

urlpatterns = [
    path('', views.loginPage ,name='login'),
    path('register/', views.registerPage ,name='register'),
    path('search/', views.searchPage ,name='search'),
    path('logout/', views.logoutPage ,name='logout'),
    path('client-detail/<str:pk>/',views.clientDetail,name='client-detail'),
    path('client-detail-list/',views.clientDetailList,name='client-detail-list'),
    path('client-Delete/',views.clientDelete,name='client-Delete'),
]
