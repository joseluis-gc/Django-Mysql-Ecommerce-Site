from django.urls import path
from . import views

app_name = 'order_app'

urlpatterns = [
    path('thanks/<int:order_id>/', views.thanks, name='thanks'),
    path('history/', views.orderHistory, name='history'),
    path('<int:order_id>/', views.viewOrder, name='order_details'),

]

