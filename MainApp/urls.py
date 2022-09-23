from . import views
from django.urls import path

app_name = 'MainApp'

urlpatterns = [
    path('', views.index, name='index'),
    path('index/', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('forget/', views.forget, name='forget'),
    path('logout/', views.logout, name='logout'),
    path('unit/<int:id>', views.unit, name='unit'),
    path('comments/', views.comments, name='comments'),
    path('download/<int:file_id>', views.download, name='download'),
    path('setting/', views.setting, name='setting'),
    path('ln/', views.ln_index, name='ln_index'),
    path('ln/index', views.ln_index, name='ln_index'),
    path('ln/query', views.ln_query, name='ln_query'),
    path('ln/my', views.ln_my, name='ln_my'),
    path('ln/modify', views.ln_modify, name='ln_modify'),
]
