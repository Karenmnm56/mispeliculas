from django.test import TestCase
from .models import User, Movie


class MovieModelTest(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username='admin',
            password='12345'
        )

        self.movie = Movie.objects.create(
            title='Batman',
            description='Película de acción',
            price=150,
            stock=5,
            owner=self.user
        )

    def test_movie_created(self):

        self.assertEqual(self.movie.title, 'Batman')

    def test_movie_stock(self):

        self.assertEqual(self.movie.stock, 5)

    def test_movie_price(self):

        self.assertEqual(self.movie.price, 150)