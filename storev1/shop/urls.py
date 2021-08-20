from django.urls import path
from shop import views

app_name = 'shop'

urlpatterns = [
    path('', views.allProductCat, name='allProductCat'),
    path('<slug:c_slug>/', views.allProductCat, name='products_by_category'),
]
