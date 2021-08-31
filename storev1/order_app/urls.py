from django.urls import path
from . import views

app_name = 'order_app'

urlpatterns = [
    path('thanks/<int:order_id>/', views.thanks, name='thanks'),
]

