# from django.urls import path
# from . import views

from django.urls import path
from App_marketplace.views import home_view, contact, ProductListView, product_detail, upload_product, add_to_cart
from App_marketplace.views import delete_product, shopping_cart, finalizeaza_comanda
from .views import LoginView, register

# in acest fisier definim rutele specifice aplicatiei
app_name = 'App_marketplace'

urlpatterns = [
    path('', home_view, name='home'),
    path('upload_product/', upload_product, name='upload-product'),
    path('products/', ProductListView.as_view(), name='products'),
    path('product/<int:product_id>/', product_detail, name='product'),
    path('cart/', shopping_cart, name='cart'),
    path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('delete_product/<int:product_id>/', delete_product, name='delete_product'),
    path('finalizeaza_comanda/', finalizeaza_comanda, name='finalizeaza_comanda'),
    path('contact/', contact, name='contact'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', register, name='register'),

    ]