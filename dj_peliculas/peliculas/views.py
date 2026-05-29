from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import Movie, User, Cart, CartItem


# =========================
# 🏠 HOME
# =========================
def home(request):
    movies = Movie.objects.all()
    return render(request, 'peliculas/home.html', {'movies': movies})


# =========================
# 🔐 REGISTER
# =========================
def register(request):

    if request.method == "POST":

        username = request.POST['username']
        password = request.POST['password']

        user = User.objects.create_user(
            username=username,
            password=password
        )

        login(request, user)
        return redirect('home')

    return render(request, 'peliculas/register.html')


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
# 🎬 CREATE MOVIE
# =========================
@login_required
def movie_create(request):

    if request.method == "POST":

        Movie.objects.create(
            title=request.POST['title'],
            description=request.POST['description'],
            price=request.POST['price'],
            stock=request.POST['stock'],
            image=request.FILES.get('image'),
            owner=request.user
        )

        return redirect('dashboard')

    return render(request, 'peliculas/movie_form.html')


# =========================
# ✏️ UPDATE MOVIE
# =========================
@login_required
def movie_update(request, pk):

    movie = get_object_or_404(Movie, id=pk)

    if request.method == "POST":

        movie.title = request.POST['title']
        movie.description = request.POST['description']
        movie.price = request.POST['price']
        movie.stock = request.POST['stock']

        # si suben nueva imagen
        if request.FILES.get('image'):
            movie.image = request.FILES.get('image')

        movie.save()

        return redirect('dashboard')

    return render(request, 'peliculas/movie_form.html', {'movie': movie})


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