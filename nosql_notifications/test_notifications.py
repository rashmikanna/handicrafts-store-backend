from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models_nosql import UserNotification, AdminLog, ErrorLog


class UserNotificationTests(APITestCase):
    def setUp(self):
        UserNotification.objects.delete()  
        self.notification_data = {
            'user_id': 'test_user_1',
            'title': 'Welcome',
            'message': 'Thank you for joining us!'
        }
        UserNotification.objects.create(**self.notification_data)

    def test_create_notification(self):
        url = reverse('user-notification-list')
        data = {
            'user_id': 'test_user_2',
            'title': 'New Message',
            'message': 'You have a new message in your inbox.'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_notifications(self):
        url = reverse('user-notification-list')
        response = self.client.get(url, {'user_id': 'test_user_1'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Welcome')


class AdminLogTests(APITestCase):
    def setUp(self):
        AdminLog.objects.delete()  
        self.log_data = {
            'admin_id': 'admin_1',
            'action': 'Add Product',
            'details': 'Added a new product to the inventory'
        }
        AdminLog.objects.create(**self.log_data)

    def test_create_admin_log(self):
        url = reverse('admin-log-list')
        data = {
            'admin_id': 'admin_2',
            'action': 'Delete Product',
            'details': 'Deleted a product from the inventory'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_admin_logs(self):
        url = reverse('admin-log-list')
        response = self.client.get(url, {'admin_id': 'admin_1'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['action'], 'Add Product')


class ErrorLogTests(APITestCase):
    def setUp(self):
        ErrorLog.objects.delete() 
        self.error_log_data = {
            'error_type': 'Database Error',
            'message': 'Unable to connect to the database'
        }
        ErrorLog.objects.create(**self.error_log_data)

    def test_create_error_log(self):
        url = reverse('error-log-list')
        data = {
            'error_type': 'Network Error',
            'message': 'Unable to reach external server'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_error_logs(self):
        url = reverse('error-log-list')
        response = self.client.get(url, {'error_type': 'Database Error'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['message'], 'Unable to connect to the database')
