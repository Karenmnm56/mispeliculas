from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import Movie, User, Cart, CartItem
from .forms import MovieForm, RegisterForm


# =========================
# 🏠 HOME
# =========================
def home(request):
    movies = Movie.objects.all()
    return render(request, 'peliculas/home.html', {'movies': movies})


# =========================
# 🔐 REGISTER (mejorado con form)
# =========================
def register(request):

    form = RegisterForm()

    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')

    return render(request, 'peliculas/register.html', {'form': form})


# =========================
# 🔐 LOGIN
# =========================
def login_view(request):

    if request.method == "POST":

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('home')

    return render(request, 'peliculas/login.html')


# =========================
# 🚪 LOGOUT
# =========================
def logout_view(request):
    logout(request)
    return redirect('home')


# =========================
# 📊 DASHBOARD
# =========================
@login_required
def dashboard(request):

    movies = Movie.objects.filter(owner=request.user)

    return render(request, 'peliculas/dashboard.html', {
        'movies': movies
    })


# =========================
# 🎬 CREATE MOVIE (CON FORM + CATEGORIES)
# =========================
@login_required
def movie_create(request):

    form = MovieForm()

    if request.method == "POST":

        form = MovieForm(request.POST, request.FILES)

        if form.is_valid():
            movie = form.save(commit=False)
            movie.owner = request.user
            movie.save()

            form.save_m2m()  # 🔥 IMPORTANTÍSIMO para categories

            return redirect('dashboard')

    return render(request, 'peliculas/movie_form.html', {
        'form': form
    })


# =========================
# ✏️ UPDATE MOVIE
# =========================
@login_required
def movie_update(request, pk):

    movie = get_object_or_404(Movie, id=pk)

    form = MovieForm(instance=movie)

    if request.method == "POST":

        form = MovieForm(request.POST, request.FILES, instance=movie)

        if form.is_valid():
            movie = form.save(commit=False)
            movie.owner = request.user
            movie.save()

            form.save_m2m()

            return redirect('dashboard')

    return render(request, 'peliculas/movie_form.html', {
        'form': form
    })


# =========================
# ❌ DELETE MOVIE
# =========================
@login_required
def movie_delete(request, pk):

    movie = get_object_or_404(Movie, id=pk)

    if request.method == "POST":
        movie.delete()
        return redirect('dashboard')

    return render(request, 'peliculas/movie_confirm_delete.html', {
        'movie': movie
    })


# =========================
# 🛒 CART
# =========================
@login_required
def cart_detail(request):

    cart, created = Cart.objects.get_or_create(user=request.user)

    return render(request, 'peliculas/cart_detail.html', {
        'cart': cart
    })


@login_required
def add_to_cart(request, movie_id):

    movie = get_object_or_404(Movie, id=movie_id)

    cart, created = Cart.objects.get_or_create(user=request.user)

    item, created = CartItem.objects.get_or_create(
        cart=cart,
        movie=movie,
        defaults={'quantity': 0}
    )

    item.quantity += 1
    item.save()

    return redirect('cart_detail')


@login_required
def remove_from_cart(request, item_id):

    item = get_object_or_404(CartItem, id=item_id)
    item.delete()

    return redirect('cart_detail')


@login_required
def update_cart_item(request, item_id):

    item = get_object_or_404(CartItem, id=item_id)

    if request.method == "POST":

        qty = int(request.POST['quantity'])

        if qty > 0:
            item.quantity = qty
            item.save()
        else:
            item.delete()

    return redirect('cart_detail')