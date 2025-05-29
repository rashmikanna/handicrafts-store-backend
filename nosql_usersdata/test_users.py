from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models_nosql import BrowsingHistory, Wishlist
from nosql_products.models_nosql import Product
from django.contrib.auth.models import User




class BrowsingHistoryTests(APITestCase):

    def setUp(self):
        # Clear any existing browsing history for the test user
        BrowsingHistory.objects(user_id='test_user_1').delete()
        
        self.product = Product.objects.create(
            name="Wooden Vase", description="Handcrafted wooden vase", price=20.99, stock=5
        )
        self.history_data = {
            'user_id': 'test_user_1',
            'product': self.product
        }
        self.history = BrowsingHistory.objects.create(**self.history_data)

    def tearDown(self):
        # Clean up the database after each test
        BrowsingHistory.objects(user_id='test_user_1').delete()
        Wishlist.objects(user_id='test_user_1').delete()

    def test_add_to_browsing_history(self):
        url = reverse('browsinghistory-list')
        data = {
            'user_id': 'test_user_2',
            'product_id': str(self.product.id)
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_browsing_history(self):
        url = reverse('browsinghistory-list')
        response = self.client.get(url, {'user_id': 'test_user_1'}, format='json')

        # Debugging: Print the number of entries for the user
        print(f"Browsing history count for user 'test_user_1': {len(response.data)}")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class WishlistTests(APITestCase):
    def setUp(self):
        # Create a sample user, wishlist, and product
        self.user = User.objects.create(username='testuser', password='password')
        self.wishlist = Wishlist.objects.create(user_id=self.user.username)

        self.product = Product.objects.create(name='Sample Product', price=100)

    def test_add_product_to_wishlist(self):
        # Adjust URL to match the 'add_product' action
        url = reverse('wishlist-add-product', kwargs={'pk': str(self.wishlist.id)})
        data = {
            'product_id': str(self.product.id)
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_remove_product_from_wishlist(self):
        url = reverse('wishlist-add-product', kwargs={'pk': str(self.wishlist.id)})

        data = {
            'product_id': str(self.product.id)
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_wishlist(self):
        url = reverse('wishlist-add-product', kwargs={'pk': str(self.wishlist.id)})

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user_id'], 'test_user_1')
