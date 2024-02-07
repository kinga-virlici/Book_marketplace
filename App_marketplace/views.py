from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views import View

from .models.product import Product
from .models.order import Order
from .models.order import OrderItem
from .models.mesage import Mesaj
from .forms import OrderItemForm, ProductForm, MesajForm
from django.http import JsonResponse
from django.urls import reverse
from django.db.models import F
from django.views.generic import ListView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView as AuthLoginView, LogoutView as AuthLogoutView
from django.contrib.auth import authenticate, login
from account.forms import RegisterForm
from django.http import HttpResponse
import sys


def home_view(request):
    return render(request, 'App_marketplace/home.html')


class ProductListView(ListView): # clasa cu ajutorul caruia afisam o lista de obiecte
    model = Product
    template_name = 'App_marketplace/products.html'

    def get_context_data(self, **kwargs): # metoda cu ajutorul careia furnizam date suplimentare  catre sablon, pagina products.html
        context = super().get_context_data(**kwargs)
        context['products'] = context['object_list']
        return context


def product_detail(request, product_id): # functia care ne afiseaza informatii despre produs tinand cond de un id
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'App_marketplace/product.html', {'product': product})


def upload_product(request): # functie cu ajutorul careia putem incarca produse in aplicatia noastra folosind un sablon, pagina upload_product.html
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            return redirect('/')
    else:
        form = ProductForm()

    return render(request, 'App_marketplace/upload_product.html', {'form': form})

@login_required
def add_to_cart(request, product_id): # functie cu ajutorul cauia putem adauga produse in cosul de cumparaturi
    try:
        # Obtine produsul pe baza id-ului
        product = get_object_or_404(Product, id=product_id)

        # Verificam daca exista deja un OrderItem pentru acest produs și utilizator
        order_item, created = OrderItem.objects.get_or_create(
            user=request.user,
            ordered=False,
            product=product
        )

        if created:
            messages.success(request, f"{product.name} a fost adăugat în coș.")
        else:
            # Daca OrderItem exista deja, vom actualiza cantitatea
            order_item.quantity = F('quantity') + 1
            order_item.save()
            messages.info(request, f"Cantitatea pentru {product.name} a fost actualizată în coș.")

        # Redirectionam catre pagina de shopping cart
        return redirect(reverse('App_marketplace:cart'))
    except Exception as e:
        # Putem gestiona eroarea si returnam un mesaj
        messages.error(request, f"Eroare la adăugarea produsului în coș: {str(e)}")
        return redirect('/')


@login_required
def create_order(request): # functie cu ajutorul cauia putem crea o comanda
    form = OrderItemForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            product_id = form.cleaned_data['product'].id
            quantity = form.cleaned_data['quantity']

            order_item, created = OrderItem.objects.get_or_create(
                user=request.user,
                ordered=False,
                product_id=product_id,
            )
            order_item.quantity += quantity
            order_item.save()

            return JsonResponse({'status': 'success'})

    order_items = OrderItem.objects.filter(user=request.user, ordered=False)
    order_total = sum(item.get_final_price() for item in order_items)

    context = {
        'form': form,
        'order_items': order_items,
        'order_total': order_total,
    }
    return render(request, 'App_marketplace/cart.html', context)


def finalizeaza_comanda(request):
    if request.method == 'POST':

        order_items = OrderItem.objects.filter(user=request.user, ordered=False)

        new_order = Order.objects.create(user=request.user, ordered=True)
        new_order.items.set(order_items)

        order_items.update(ordered=True)

        messages.success(request, 'Comanda a fost plasată cu succes!')
        return redirect(reverse('App_marketplace:home'))

    return redirect(reverse('App_marketplace:home'))


def shopping_cart(request):
    order_items = OrderItem.objects.filter(user=request.user, ordered=False)

    order_total = sum(item.get_final_price() for item in order_items)

    context = {
        'order_items': order_items,
        'total_cumparaturi': order_total,
    }

    return render(request, 'App_marketplace/cart.html', context)


@login_required
def delete_product(request, product_id):
    if request.method == 'DELETE':
        try:
            order_item = OrderItem.objects.get(user=request.user, product_id=product_id, ordered=False)
            order_item.delete()
            return JsonResponse({'status': 'success'})
        except OrderItem.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Produsul nu a fost găsit în coș'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Metoda solicitată nu este permisă'})

#Varianta1


class MessageView(View):
    def get(self, request):
        form = MesajForm()

        return render(request, 'App_marketplace/contact.html', {'form': form})


    def post(self, request):
        form = MesajForm(request.POST)
        if form.is_valid():
            mesaj_nou = form.save(commit=False)
            mesaj_nou.status = 'necitit'
            mesaj_nou.save()
            return redirect('/')  # Redirectionam la pagina de home
        else:
            return render(request, 'App_marketplace/contact.html', {'form': form})
# Varianta 2.1
# class MessageView(View):
#     def get(self, request):
#         form = MesajForm()
#         return render(request, 'App_marketplace/contact.html', {'form': form})
#
#     def post(self,request):
#         if request.method == 'POST':
#             form = MesajForm(request.POST)
#             if form.is_valid():
#                 mesaj_nou = form.save(commit=False)
#                 mesaj_nou.status = 'necitit'
#                 mesaj_nou.save()
#                 return redirect('/')  # Redirectionam la pagina de home
#         else:
#             form = MesajForm()
#
#         return render(request, 'App_marketplace/contact.html', {'form': form})

# Varianta 2.2
# class MessageView(View):
#     def get(self, request):
#         # Handle GET requests (display the contact form)
#         return render(request, 'App_marketplace/contact.html')
#
#     def post(self, request):
#         # Handle POST requests (process form submission)
#         # Example logic to process form data and save it to the database
#         fullname = request.POST.get('fullname')
#         email = request.POST.get('email')
#         phone = request.POST.get('phone')
#         message = request.POST.get('message')
#         # Perform any additional processing, such as saving to the database
#         return HttpResponse('Form submitted successfully')


#in acest fisier vom crea clase, metode sau functii cu ajutorul carora putem gestiona cererile HTTP primite de la utilizator

class LoginView(AuthLoginView):          #aceasta clasa moesteneste clasa AuthLoginView() si ne ofera functionalitatea de login,
    template_name = 'account/login.html' #aceasta clasa ne ofera sablonul personalizat pt pagina de login a aplicatiei


class LogoutView(AuthLogoutView):         #aceasta clasa moesteneste clasa AuthLogoutView() si ne ofera functionalitatea de logout
    template_name = 'account/logout.html' #aceasta clasa ne ofera sablonul personalizat pt pagina de logout a aplicatiei


def register(request):
    # functia gestioneaza cererile GET - ne afiseaza formularul si POST - ne salveaza noul utilizator in baza de date

    if request.method == "GET":
        form = RegisterForm
        context = {
            "form": form
        }
        return render(request, 'account/register.html', context=context)
    elif request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")

            user = authenticate(username=username, password=password)

            if user:
                login(request, user)

            return redirect('/')

    return render(request, "registration/login.html", {})