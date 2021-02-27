from django.urls import path
from .views import IndexView


app_name = 'myapp'

urlpatterns = [
    path('', IndexView.as_view(), name='index')
]
