from main.views import MainView
from django.urls import path


app_name = 'main'


urlpatterns = [
    path('', MainView.as_view(), name='index'),
]