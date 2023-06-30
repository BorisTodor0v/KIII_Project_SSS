import os

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth import *
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login
from .models import *
from .forms import *


# Create your views here.
def home_page(request):
    random_products = list(Product.objects.all().order_by('?')[:5])
    context = {
        'random_products': random_products,
    }
    return render(request, 'home.html', context)


def product_page(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    images = ProductImage.objects.filter(product=product)
    random_products = list(Product.objects.all().order_by('?')[:5])
    in_cart = False
    enable_add_to_cart = False
    if request.user.is_authenticated:
        cart_item = CartItem.objects.filter(cart__user=request.user, product=product).first()
        if cart_item:
            in_cart = True
            if cart_item.quantity == product.stock:
                enable_add_to_cart = False
            else:
                enable_add_to_cart = True
        else:
            enable_add_to_cart = True
    is_owner = (request.user.id == product.seller.user.id)
    context = {
        'product': product,
        'images': images,
        'in_cart': in_cart,
        'enable_add_to_cart': enable_add_to_cart,
        'random_products': random_products,
        'is_owner': is_owner
    }
    return render(request, 'product.html', context)


@login_required
def add_product_page(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        description = request.POST.get('description')
        category_id = request.POST.get('category')
        category = Category.objects.get(id=category_id)
        racing_series_id = request.POST.get('racing_series')
        racing_series = RacingSeries.objects.get(id=racing_series_id)
        team_id = request.POST.get('team')
        team = Team.objects.get(id=team_id)
        seller = request.user
        user_seller = UserInfo.objects.get(user=seller)

        product = Product(name=name, price=price, description=description, seller=user_seller, team=team, category=category,
                          racing_series=racing_series, stock=stock)
        product.save()

        images = request.FILES.getlist('images')
        for image in images:
            ProductImage.objects.create(product=product, image=image)

        return redirect('Product', product_id=product.id)
    else:
        racing_series = sorted(RacingSeries.objects.all(), key=lambda x: x.name.lower())
        teams = sorted(Team.objects.all(), key=lambda x: x.name.lower())
        categories = sorted(Category.objects.all(), key=lambda x: x.name.lower())

    context = {
        'teams': teams,
        'racing_series': racing_series,
        'categories': categories
    }
    return render(request, 'add_product.html', context)


@login_required
def edit_product_page(request, product_id):
    user = request.user
    user_info = UserInfo.objects.get(user=user)
    product = get_object_or_404(Product, id=product_id)
    if user_info == product.seller or user.is_superuser:
        teams = sorted(Team.objects.all(), key=lambda x: x.name.lower())
        racing_series = sorted(RacingSeries.objects.all(), key=lambda x: x.name.lower())
        categories = sorted(Category.objects.all(), key=lambda x: x.name.lower())

        if request.method == 'POST':
            product.name = request.POST.get('name')
            product.price = request.POST.get('price')
            product.description = request.POST.get('description')
            product.team_id = request.POST.get('team')
            product.racing_series_id = request.POST.get('racing_series')
            product.category_id = request.POST.get('category')
            product.stock = request.POST.get('stock')

            images = request.FILES.getlist('images')
            product_image_objects = []
            for image in images:
                product_image = ProductImage(product=product, image=image)
                product_image.save()
                product_image_objects.append(product_image)

            product.save()

            delete_image_ids = request.POST.getlist('delete_images')
            ProductImage.objects.filter(id__in=delete_image_ids).delete()

            return redirect('Product', product_id=product.id)
    else:
        return redirect('Home')

    context = {
        'product': product,
        'teams': teams,
        'racing_series': racing_series,
        'categories': categories
    }
    return render(request, 'edit_product.html', context)


@login_required
def confirm_delete_page(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    images = ProductImage.objects.filter(product=product)
    user = request.user
    user_info = UserInfo.objects.get(user=user)
    if user_info == product.seller or request.user.is_superuser:
        return render(request, 'confirm_delete.html', {'product': product, 'images': images})
    else:
        return redirect('Home')


@login_required
def delete_product_page(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    user = request.user
    user_info = UserInfo.objects.get(user=user)
    if user_info == product.seller or request.user.is_superuser:
        for product_image in product.productimage_set.all():
            image_path = product_image.image.path
            os.remove(image_path)
        product.delete()
        return redirect('Products')
    else:
        return redirect('Home')


def search_products(request):
    query = request.GET.get('query')
    page_number = request.GET.get('page')
    team_id = request.GET.get('team')
    category_id = request.GET.get('category')
    racing_series_id = request.GET.get('racing_series')

    products = Product.objects.all()

    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query) | Q(team__name__icontains=query) | Q(racing_series__name__icontains=query))

    if team_id:
        products = products.filter(team__id=team_id)

    if category_id:
        products = products.filter(category__id=category_id)

    if racing_series_id:
        products = products.filter(racing_series__id=racing_series_id)

    teams = sorted(Team.objects.all(), key=lambda x: x.name.lower())
    racing_series = sorted(RacingSeries.objects.all(), key=lambda x: x.name.lower())
    categories = sorted(Category.objects.all(), key=lambda x: x.name.lower())

    products = products.order_by('-id')

    products_per_page = request.GET.get('per_page', 10)
    paginator = Paginator(products, products_per_page)
    page_obj = paginator.get_page(page_number)
    random_products = list(Product.objects.all().order_by('?')[:5])

    context = {
        'query': query,
        'products': page_obj,
        'products_per_page': products_per_page,
        'teams': teams,
        'racing_series': racing_series,
        'categories': categories,
        'random_products': random_products,
    }

    return render(request, 'products.html', context)


def login_page(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            username = request.POST['usernameInput']
            password = request.POST['passwordInput']
            remember_me = request.POST.get('remember_me') == 'on'
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                if remember_me:
                    request.session.set_expiry(settings.SESSION_COOKIE_AGE)
                next_url = request.POST.get('next', 'Home')
                return redirect(next_url)
            else:
                error_message = 'Invalid username or password'
                return render(request, 'login.html', {'error_message': error_message})

        return render(request, 'login.html')
    return redirect('Home')


def logout_method(request):
    logout(request)
    next_url = request.POST.get('next', 'Home')
    return redirect(next_url)


def register_page(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = UserRegisterForm(request.POST)
            if form.is_valid():
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']
                username = form.cleaned_data['username']
                user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email,
                                                password=password)
                user_info = UserInfo.objects.create(user=user)
                return redirect('/')
        else:
            form = UserRegisterForm()
        return render(request, 'register.html', {'form': form})
    return redirect('Home')


def profile_page(request, user_id):
    user = User.objects.get(id=user_id)
    user_info = UserInfo.objects.get(user=user)
    products = Product.objects.filter(seller=user_info)
    products = products.order_by('-id')
    page_number = request.GET.get('page')
    products_per_page = request.GET.get('per_page', 10)
    paginator = Paginator(products, products_per_page)
    page_obj = paginator.get_page(page_number)

    is_owner = (request.user.id == user.id)

    context = {
        'user_info': user_info,
        'is_owner': is_owner,
        'products': page_obj,
        'products_per_page': products_per_page,
    }
    return render(request, 'profile.html', context)


@login_required
def edit_profile_page(request):
    if request.method == 'POST':
        user = request.user
        user_info = UserInfo.objects.get(user=user)
        user.username = request.POST['username']
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.email = request.POST['email']
        user_info.bio = request.POST['bio']

        profile_image = request.FILES.get('profile_image')
        if profile_image:
            user_info.profile_image = profile_image

        user.save()
        user_info.save()

        return redirect('Profile', user_id=user.id)
    else:
        user = request.user
        user_info = UserInfo.objects.get(user=user)
        context = {
            'user': user,
            'user_info': user_info,
        }
        return render(request, 'edit_profile.html', context)


def legal_info_page(request):
    return render(request, 'legal.html')


@login_required
def add_to_cart(request, product_id):
    if request.method == 'POST':
        product = Product.objects.get(id=product_id)

        cart, created = Cart.objects.get_or_create(user=request.user)

        cart_item = cart.items.filter(product=product).first()

        if cart_item:
            cart_item.quantity += 1
            cart_item.save()
        else:
            cart_item = CartItem(product=product, quantity=1)
            cart_item.save()

            cart.items.add(cart_item)

        return redirect('Cart')
    return render(request, 'cart.html')


@login_required
def cart_page(request):
    cart = Cart.objects.get(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    context = {
        'cart': cart,
        'cart_items': cart_items
    }
    return render(request, 'cart.html', context)


@login_required
def remove_from_cart(request, item_id):
    cart = Cart.objects.get(user=request.user)
    try:
        cart_item = CartItem.objects.get(id=item_id)
    except CartItem.DoesNotExist:
        # Handle the case when the CartItem does not exist
        return redirect('Cart')

    # Check if the CartItem belongs to the user's cart
    if cart.user == request.user:
        cart_item.delete()

    return redirect('Cart')


@login_required
def increment_quantity(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)

    if cart_item.quantity < cart_item.product.stock:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('Cart')


@login_required
def decrement_quantity(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)

    # If the quantity is 1, remove the item from the cart
    if cart_item.quantity == 1:
        cart_item.delete()
    else: # Just remove 1
        cart_item.quantity -= 1
        cart_item.save()

    return redirect('Cart')


@login_required
def payment(request):
    cart = Cart.objects.get(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    payment_failed = False

    if request.method == 'POST':
        cc_number = request.POST.get('cc_number')
        expiration_date = request.POST.get('expiration_date')
        cvv = request.POST.get('cvv')

        if len(cc_number) != 16 or len(cvv) != 3:
            payment_failed = True
        else:
            for cart_item in cart_items:
                product = cart_item.product
                product.stock -= cart_item.quantity
                product.save()

            cart_items.delete()

            return redirect('Payment_Success')

    context = {
        'payment_failed': payment_failed,
        'cart': cart,
        'cart_items': cart_items
    }
    return render(request, 'cart.html', context)


@login_required
def payment_success_page(request):
    return render(request, 'payment_success.html')


def about_page(request):
    return render(request, 'about.html')


def tmp(request):
    return render(request, 'tmp.html')
