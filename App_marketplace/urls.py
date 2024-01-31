from django.urls import path
from . import views

# in cadrul acestui fisier vom defini lista de endpoint-urile aplicatiei

urlpatterns = [
    path('', views.home_view, name='home'),
    path('upload_product/', views.upload_product, name='upload_product'),
    path('products/', views.products_view, name='products'),
    path('product/<int:product_id>/', views.product_view, name='product_view'),
    path('contact/', views.contact_view, name='contact')
]
