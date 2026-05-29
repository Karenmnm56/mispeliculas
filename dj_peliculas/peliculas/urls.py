from django.urls import path
from . import views

urlpatterns = [
    # HOME
    path('', views.home, name='home'),

    # AUTH
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # DASHBOARD
    path('dashboard/', views.dashboard, name='dashboard'),

    # MOVIES
    path('movies/create/', views.movie_create, name='movie_create'),
    path('movies/<uuid:pk>/edit/', views.movie_update, name='movie_update'),
    path('movies/<uuid:pk>/delete/', views.movie_delete, name='movie_delete'),

    # CART
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<uuid:movie_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<uuid:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<uuid:item_id>/', views.update_cart_item, name='update_cart_item'),
]