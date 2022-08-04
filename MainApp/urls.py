from . import views
from django.urls import path

app_name = 'MainApp'

urlpatterns = [
    path('', views.index, name='index'),
    path('index/', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('forget/', views.forget, name='forget'),
    path('logout/', views.logout, name='logout')
]