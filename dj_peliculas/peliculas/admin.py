from django.contrib import admin
from .models import User, Category, Movie, Cart, CartItem

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Movie)
admin.site.register(Cart)
admin.site.register(CartItem)