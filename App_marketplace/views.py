from django.shortcuts import render, redirect
from django.contrib.auth import login
from App_marketplace.forms import ProductForm
from App_marketplace.models.product import Product
from os.path import splitext


def home_view(request):
    return render(request, 'App_marketplace/home.html')


def upload_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            return redirect('home')
    else:
        form = ProductForm()

    return render(request, 'App_marketplace/upload_product.html', {'form': form})


def products_view(request):
    products = Product.objects.all()
    image_names = {}
    for product in products:
        if '/' in product.image.name:
            image_name_parts = product.image.name.split('/')
            info = splitext(image_name_parts[1])[0]
            image_names[product.id] = info
        else:
            image_names[product.id] = splitext(product.image.name)[0]
    context = {'products': products, 'image_names': image_names}
    return render(request, 'App_marketplace/products.html', context)


def product_view(request, product_id):
    product = Product.objects.get(id=product_id)
    return render(request, 'App_marketplace/product.html', {'product':product})


def contact_view(request):
    return render(request, 'App_marketplace/contact.html')


