from . import views
from django.urls import path

app_name = 'MainApp'

urlpatterns = [
    path('', views.index, name='index'),
    path('index/', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('forget/', views.forget, name='forget'),
    path('logout/', views.logout, name='logout'),
    path('cycle_protocol/', views.cycle_protocol, name='cycle_protocol'),
    path('centrifuge/', views.centrifuge, name='centrifuge'),
    path('comments/', views.comments, name='comments'),
    path('commitment/', views.commitment, name='commitment'),
    path('cultured_basic/', views.cultured_basic, name='cultured_basic'),
    path('cylinder/', views.cylinder, name='cylinder'),
    path('incubator/', views.incubator, name='incubator'),
    path('manage_rule/', views.manage_rule, name='manage_rule'),
    path('note/', views.note, name='note'),
    path('safe/', views.safe, name='safe'),
    path('star_cell_cultured/', views.star_cell_cultured, name='star_cell_cultured'),
    path('sterilizer/', views.sterilizer, name='sterilizer'),
    path('tank/', views.tank, name='tank'),
    path('download/<int:file_id>', views.download, name='download'),
    path('setting/', views.setting, name='setting')

]
