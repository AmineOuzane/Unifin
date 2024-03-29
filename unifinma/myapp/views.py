
from django.shortcuts import get_object_or_404, redirect, render
from django.core.mail import send_mail
from django.urls import reverse
from .forms import ContactForm
from django.core.mail import send_mail
from django.conf import settings
from .forms import CreateUserForm
from myapp.models import Produit,Category, Cart, Order
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserChangeForm
from decimal import ROUND_HALF_UP, Decimal



def index(request):
    return render (request, 'myapp/index.html')


from django.contrib.auth import login

def registerpage(request):
    if request.user.is_authenticated:
        return redirect('acceuil')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Votre compte a été créé avec succès' + user)
                return redirect('login')  # Redirect to the login page

        else:
            form = CreateUserForm()

        context = {'form': form}
        return render(request, 'myapp/register.html', context)



def loginpage(request):
    if request.user.is_authenticated:
        return redirect('acceuil')
    else:
        if request.method == 'POST':
            form = AuthenticationForm(request, data=request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('acceuil')  # Replace with the URL you want to redirect to after successful login
        else:
            form = AuthenticationForm()
            messages.info(request, 'Nom d\'utilisateur ou mot de passe incorrect')

    context = {'form': form}
    return render(request, 'myapp/login.html', context)

@login_required(login_url='login')
def logoutuser(request):
    logout(request)
    return redirect('login')

#def loginpage(request):
    if request.method == 'POST':
        request.POST.get('username')
        request.POST.get('password')
    context = {}
    return render(request, 'myapp/login.html', context)

@login_required(login_url='login')
def edit_profile(request):
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('acceuil')
    else:
        form = UserChangeForm(instance=request.user)

    context = {'form': form}
    return render(request, 'myapp/edit_profile.html', context)



def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        user_email = request.POST['user_email']
        contact_no = request.POST['contact_no']
        message = request.POST['message']

        # Vous pouvez ajouter ici la logique pour envoyer l'e-mail ou traiter les données
        send_mail(
            name,        # Sujet de l'e-mail
            message,     # Corps de l'e-mail
            user_email,  # Adresse e-mail de l'expéditeur
            ['amineouzane10@gmail.com'],  # Liste des destinataires
        )
        
        return render(request, 'myapp/contact.html')
    else:
        return render(request, 'myapp/contact.html')


def recette(request):
    return render (request, 'myapp/recette.html')


def about(request):
    return render (request, 'myapp/about.html')


def daawat(request):
    category = get_object_or_404(Category, name='Daawat')
    products = Produit.objects.filter(category=category)
    return render(request, 'myapp/daawat.html', {'products': products})


def catania(request):
    category = get_object_or_404(Category, name='Catania')
    products = Produit.objects.filter(category=category)
    return render(request, 'myapp/catania.html', {'products': products})


def magicclean(request):
    category = get_object_or_404(Category, name='Magicclean')
    products = Produit.objects.filter(category=category)
    return render(request, 'myapp/magicclean.html', {'products': products})



def product_list_general(request):
    products = Produit.objects.all()
    return render(request, 'myapp/produit.html', {'products': products})


def detail(request, produit_id):
    produit = get_object_or_404(Produit, pk=produit_id)
    return render(request, 'myapp/detail.html', {'produit': produit})


def blog(request):
    return render (request, 'myapp/blog.html')




@login_required(login_url='login')
def add_to_cart(request, produit_id):
    user = request.user
    produit = get_object_or_404(Produit, pk=produit_id)

    # Rechercher le panier de l'utilisateur
    cart, created = Cart.objects.get_or_create(user=user)

    # Vérifier si l'utilisateur a déjà ajouté ce produit au panier
    order, order_created = Order.objects.get_or_create(cart=cart, produit=produit, user=user, ordered=False)

    if not order_created:
        # Si la commande existe déjà, augmentez la quantité
        order.quantity += 1
        order.save()
    else:
        # Sinon, créez une nouvelle commande pour ce produit
        cart.orders.add(order)
        order.save()


    return redirect(reverse("cart"))


@login_required(login_url='login')
def cart(request):
    cart = get_object_or_404(Cart, user=request.user)
    
    # Calculate the total price 
    total_price = Decimal(0)
    for order in cart.orders.all():
        total_price += Decimal(order.produit.prix) * order.quantity
        
        # Round the total_price to 2 decimal places (adjust as needed)
    total_price = total_price.quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)

    
    # Update the cart's total_price field
    cart.total_price = total_price
    cart.save()

    
    
    return render(request, 'myapp/cart.html', context={"orders":cart.orders.all(), "total_price": cart.total_price})


@login_required(login_url='login')
def delete_cart(request):
    if cart := request.user.cart:
        cart.delete()
        
    return redirect ('acceuil')

@login_required(login_url='login')
def delete_order(request, order_id):
    # Assurez-vous que l'utilisateur est propriétaire de cet order
    order = get_object_or_404(Order, id=order_id, cart__user=request.user)
    
    # Supprimez l'order spécifié
    order.delete()
    
    return redirect('cart')


    
def checkout(request):
        context = {}
        return render (request, 'myapp/checkout.html', context)
    
 
def search_results(request):
    query = request.GET.get('text')
    results = []

    if query:
        results = Produit.objects.filter(nom__icontains=query)
        category = results.first().category if results else None

        if category == "Daawat":
            category_products = results.filter(category=category)
            return render(request, 'myapp/daawat.html', {'products': category_products})
        elif category == "Catania":
            category_products = results.filter(category=category)
            return render(request, 'myapp/catania.html', {'products': category_products})
        elif category == "Magicclean":
            category_products = results.filter(category=category)
            return render(request, 'myapp/magicclean.html', {'products': category_products})

    return render(request, 'myapp/search_results.html', {'results': results})

    