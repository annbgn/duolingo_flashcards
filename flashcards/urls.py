from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('practice', views.practice, name='practice'),
    path('get_login_data', views.get_login_data_view, name='get_login_data'),
]