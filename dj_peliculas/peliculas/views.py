from django.shortcuts import render
from .models import Movie


# Página principal
def home(request):

    movies = Movie.objects.all()

    context = {
        'movies': movies
    }

    return render(request, 'home.html', context)