from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.test import TestCase
from .models import Auction
from django.contrib.auth.models import User
from .models import Token  # Assuming you have a Token model
from .serializers import UserSerializer, TokenSerializer  # Import your serializers
from django.utils import timezone
from .models import Token, Auction, Bid  # Import your Token, Auction, and Bid models
from django.db.models import Max
from .models import Auction, Bid, User  # Import your Auction, Bid, and User models

# Create your tests here.

class CreateUserTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword",
            "role": "user",
        }
        response = self.client.post('/create_user/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_user_missing_fields(self):
        data = {
            "username": "testuser",
            "email": "test@example.com",
        }
        response = self.client.post('/create_user/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("username, email, password, and role are required", str(response.content))

    def test_create_user_invalid_role(self):
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword",
            "role": "invalid_role",
        }
        response = self.client.post('/create_user/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("role must be either admin or user", str(response.content))

    def test_create_user_existing_email(self):
        User.objects.create(username="existinguser", email="test@example.com", password="testpassword", role="user")
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword",
            "role": "user",
        }
        response = self.client.post('/create_user/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email already exists", str(response.content))

class UpdateUserTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Create a user for testing
        self.user = User.objects.create(username="testuser", email="test@example.com", password="testpassword", role="user")

    def test_update_user_success(self):
        data = {
            "email": "test@example.com",
            "password": "testpassword",
            "new_password": "newpassword",
            "username": "newusername",
        }
        self.client.force_authenticate(user=self.user)  # Authenticate the user
        response = self.client.put('/update_user/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the user's data has been updated
        updated_user = User.objects.get(pk=self.user.pk)
        self.assertEqual(updated_user.username, "newusername")
        self.assertTrue(updated_user.check_password("newpassword"))

    def test_update_user_missing_email(self):
        data = {
            "password": "testpassword",
            "new_password": "newpassword",
            "username": "newusername",
        }
        self.client.force_authenticate(user=self.user)  # Authenticate the user
        response = self.client.put('/update_user/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email is required", str(response.content))

    def test_update_user_missing_password(self):
        data = {
            "email": "test@example.com",
            "new_password": "newpassword",
            "username": "newusername",
        }
        self.client.force_authenticate(user=self.user)  # Authenticate the user
        response = self.client.put('/update_user/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password is required", str(response.content))

    def test_update_user_invalid_credentials(self):
        data = {
            "email": "test@example.com",
            "password": "wrongpassword",
            "new_password": "newpassword",
            "username": "newusername",
        }
        self.client.force_authenticate(user=self.user)  # Authenticate the user
        response = self.client.put('/update_user/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email or password id wrong", str(response.content))

    def test_update_user_change_password(self):
        data = {
            "email": "test@example.com",
            "password": "testpassword",
            "new_password": "newpassword",
        }
        self.client.force_authenticate(user=self.user)  # Authenticate the user
        response = self.client.put('/update_user/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the user's password has been updated
        updated_user = User.objects.get(pk=self.user.pk)
        self.assertTrue(updated_user.check_password("newpassword"))

    def test_update_user_change_username(self):
        data = {
            "email": "test@example.com",
            "password": "testpassword",
            "username": "newusername",
        }
        self.client.force_authenticate(user=self.user)  # Authenticate the user
        response = self.client.put('/update_user/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the user's username has been updated
        updated_user = User.objects.get(pk=self.user.pk)
        self.assertEqual(updated_user.username, "newusername")

class DeleteUserTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Create a user for testing
        self.user = User.objects.create(username="testuser", email="test@example.com", password="testpassword", role="user")

    def test_delete_user_success(self):
        data = {
            "email": "test@example.com",
            "password": "testpassword",
        }
        self.client.force_authenticate(user=self.user)  # Authenticate the user
        response = self.client.delete('/delete_user/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the user has been deleted
        self.assertFalse(User.objects.filter(email="test@example.com").exists())

    def test_delete_user_missing_email(self):
        data = {
            "password": "testpassword",
        }
        self.client.force_authenticate(user=self.user)  # Authenticate the user
        response = self.client.delete('/delete_user/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email is required", str(response.content))

    def test_delete_user_missing_password(self):
        data = {
            "email": "test@example.com",
        }
        self.client.force_authenticate(user=self.user)  # Authenticate the user
        response = self.client.delete('/delete_user/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password is required", str(response.content))

    def test_delete_user_invalid_credentials(self):
        data = {
            "email": "test@example.com",
            "password": "wrongpassword",
        }
        self.client.force_authenticate(user=self.user)  # Authenticate the user
        response = self.client.delete('/delete_user/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("profile does not exist", str(response.content))

class UserLoginTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Create a user for testing
        self.user = User.objects.create(username="testuser", email="test@example.com", password="testpassword", role="user")

    def test_user_login_with_existing_user(self):
        data = {
            "email": "test@example.com",
            "password": "testpassword",
        }
        response = self.client.post('/api/user_login/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the response contains user and token data
        self.assertIn("user", response.data)
        self.assertIn("token", response.data)

    def test_user_login_with_existing_token(self):
        # Create a token for testing
        token = Token.objects.create(user_id=self.user, token_value="testtoken")
        token.save()

        data = {
            "token_value": "testtoken",
        }
        response = self.client.post('/api/user_login/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the response contains user and token data
        self.assertIn("user", response.data)
        self.assertIn("token", response.data)

    def test_user_login_missing_email(self):
        data = {
            "password": "testpassword",
        }
        response = self.client.post('/api/user_login/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email is required", str(response.content))

    def test_user_login_missing_password(self):
        data = {
            "email": "test@example.com",
        }
        response = self.client.post('/api/user_login/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password is required", str(response.content))

    def test_user_login_invalid_credentials(self):
        data = {
            "email": "test@example.com",
            "password": "wrongpassword",
        }
        response = self.client.post('/api/user_login/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email or password id wrong", str(response.content))

    def test_user_login_invalid_token(self):
        data = {
            "token_value": "invalidtoken",
        }
        response = self.client.post('/api/user_login/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("token does not exist", str(response.content))

class CreateAuctionTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_auction_success(self):
        data = {
            "start_time": "2023-10-10T12:00:00Z",  # Replace with a valid date and time
            "end_time": "2023-10-11T12:00:00Z",    # Replace with a valid date and time
            "start_price": 100.0,                  # Replace with a valid start price
            "item_name": "Test Item",
        }
        response = self.client.post('/api/create_auction/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check if the auction has been created
        self.assertTrue(Auction.objects.filter(item_name="Test Item").exists())

    def test_create_auction_missing_fields(self):
        data = {
            "start_time": "2023-10-10T12:00:00Z",  # Replace with a valid date and time
            "end_time": "2023-10-11T12:00:00Z",    # Replace with a valid date and time
            "start_price": 100.0,                  # Replace with a valid start price
        }
        response = self.client.post('/api/create_auction/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("start_time, end_time, start_price, and item_name are required", str(response.content))

    def test_create_auction_invalid_date_format(self):
        data = {
            "start_time": "2023-10-10",            # Invalid date format
            "end_time": "2023-10-11T12:00:00Z",    # Replace with a valid date and time
            "start_price": 100.0,                  # Replace with a valid start price
            "item_name": "Test Item",
        }
        response = self.client.post('/api/create_auction/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Enter a valid date/time.", str(response.content))

class UpdateAuctionTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Create an auction for testing
        self.auction = Auction.objects.create(
            start_time="2023-10-10T12:00:00Z",
            end_time="2023-10-11T12:00:00Z",
            start_price=100.0,
            item_name="Test Item"
        )

    def test_update_auction_success(self):
        data = {
            "auction_id": self.auction.id,
            "start_time": "2023-10-12T12:00:00Z",  # Replace with a valid date and time
            "end_time": "2023-10-13T12:00:00Z",    # Replace with a valid date and time
            "start_price": 200.0,                  # Replace with a valid start price
            "item_name": "Updated Test Item",
        }
        response = self.client.put('/api/update_auction/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the auction has been updated
        updated_auction = Auction.objects.get(id=self.auction.id)
        self.assertEqual(updated_auction.start_time, "2023-10-12T12:00:00Z")
        self.assertEqual(updated_auction.end_time, "2023-10-13T12:00:00Z")
        self.assertEqual(updated_auction.start_price, 200.0)
        self.assertEqual(updated_auction.item_name, "Updated Test Item")

    def test_update_auction_missing_auction_id(self):
        data = {
            "start_time": "2023-10-12T12:00:00Z",
        }
        response = self.client.put('/api/update_auction/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("auction_id is required", str(response.content))

    def test_update_auction_auction_not_found(self):
        data = {
            "auction_id": 999,  # Non-existent auction ID
            "start_time": "2023-10-12T12:00:00Z",
        }
        response = self.client.put('/api/update_auction/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("auction does not exist", str(response.content))

    def test_update_auction_invalid_date_format(self):
        data = {
            "auction_id": self.auction.id,
            "start_time": "2023-10-12",  # Invalid date format
        }
        response = self.client.put('/api/update_auction/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Enter a valid date/time.", str(response.content))

class DeleteAuctionTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Create an auction for testing
        self.auction = Auction.objects.create(
            start_time="2023-10-10T12:00:00Z",
            end_time="2023-10-11T12:00:00Z",
            start_price=100.0,
            item_name="Test Item"
        )

    def test_delete_auction_success(self):
        data = {
            "auction_id": self.auction.id,
        }
        response = self.client.delete('/api/delete_auction/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the auction has been deleted
        self.assertFalse(Auction.objects.filter(id=self.auction.id).exists())

    def test_delete_auction_missing_auction_id(self):
        data = {}
        response = self.client.delete('/api/delete_auction/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("auction_id is required", str(response.content))

    def test_delete_auction_auction_not_found(self):
        data = {
            "auction_id": 999,  # Non-existent auction ID
        }
        response = self.client.delete('/api/delete_auction/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("auction does not exist", str(response.content))

class GetUserTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Create an admin user for testing
        self.admin_user = User.objects.create(username="admin", email="admin@example.com", password="adminpassword", role="admin")
        self.admin_token = Token.objects.create(user_id=self.admin_user, token_value="admintoken")
        self.admin_token.save()

        # Create a regular user for testing
        self.user = User.objects.create(username="testuser", email="test@example.com", password="testpassword", role="user")
        self.user_token = Token.objects.create(user_id=self.user, token_value="usertoken")
        self.user_token.save()

    def test_get_user_as_admin_with_user_ids(self):
        data = {
            "token_value": "admintoken",
            "user_ids": [self.user.id],
        }
        response = self.client.get('/api/get_user/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the response contains user data
        self.assertIn("user", response.data)
        self.assertEqual(len(response.data["user"]), 1)

    def test_get_user_as_admin_without_user_ids(self):
        data = {
            "token_value": "admintoken",
        }
        response = self.client.get('/api/get_user/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the response contains user data
        self.assertIn("user", response.data)

    def test_get_user_as_admin_with_empty_user_ids(self):
        data = {
            "token_value": "admintoken",
            "user_ids": [],
        }
        response = self.client.get('/api/get_user/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the response contains user data for all users
        self.assertIn("user", response.data)
        self.assertEqual(len(response.data["user"]), User.objects.count())

    def test_get_user_as_admin_with_non_list_user_ids(self):
        data = {
            "token_value": "admintoken",
            "user_ids": "invalid",  # Invalid user IDs format
        }
        response = self.client.get('/api/get_user/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("user ID should be list", str(response.content))

    def test_get_user_as_user(self):
        data = {
            "token_value": "usertoken",
            "user_ids": [self.user.id],
        }
        response = self.client.get('/api/get_user/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Not valid", str(response.content))

    def test_get_user_missing_token_value(self):
        data = {
            "user_ids": [self.user.id],
        }
        response = self.client.get('/api/get_user/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("token_value is required", str(response.content))

    def test_get_user_invalid_token(self):
        data = {
            "token_value": "invalidtoken",  # Invalid token
            "user_ids": [self.user.id],
        }
        response = self.client.get('/api/get_user/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("token does not exist", str(response.content))

    def test_get_user_without_user_ids_as_admin(self):
        data = {
            "token_value": "admintoken",
        }
        response = self.client.get('/api/get_user/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the response contains user data for all users
        self.assertIn("user", response.data)
        self.assertEqual(len(response.data["user"]), User.objects.count())

class GetAuctionTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Create an admin user for testing
        self.admin_user = User.objects.create(username="admin", email="admin@example.com", password="adminpassword", role="admin")
        self.admin_token = Token.objects.create(user_id=self.admin_user, token_value="admintoken")
        self.admin_token.save()

        # Create a regular user for testing
        self.user = User.objects.create(username="testuser", email="test@example.com", password="testpassword", role="user")
        self.user_token = Token.objects.create(user_id=self.user, token_value="usertoken")
        self.user_token.save()

        # Create an auction for testing
        self.auction = Auction.objects.create(
            start_time="2023-10-10T12:00:00Z",
            end_time="2023-10-11T12:00:00Z",
            start_price=100.0,
            item_name="Test Item"
        )

    def test_get_auction_as_admin(self):
        data = {
            "token_value": "admintoken",
        }
        response = self.client.get('/api/get_auction/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the response contains auction data
        self.assertIn("auction", response.data)
        self.assertEqual(len(response.data["auction"]), Auction.objects.count())

    def test_get_auction_as_user(self):
        data = {
            "token_value": "usertoken",
        }
        response = self.client.get('/api/get_auction/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the response contains auction data for current auctions
        self.assertIn("auction", response.data)
        self.assertEqual(len(response.data["auction"]), Auction.get_current_auctions().count())

    def test_get_auction_invalid_role(self):
        data = {
            "token_value": "invalidtoken",  # Invalid token
        }
        response = self.client.get('/api/get_auction/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Not valid", str(response.content))

    def test_get_auction_missing_token_value(self):
        data = {}
        response = self.client.get('/api/get_auction/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("token_value is required", str(response.content))

    def test_get_auction_invalid_token(self):
        data = {
            "token_value": "invalidtoken",  # Invalid token
        }
        response = self.client.get('/api/get_auction/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("token does not exist", str(response.content))

class BidTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Create a user for testing
        self.user = User.objects.create(username="testuser", email="test@example.com", password="testpassword", role="user")
        self.user_token = Token.objects.create(user_id=self.user, token_value="usertoken")
        self.user_token.save()

        # Create an auction for testing
        self.auction = Auction.objects.create(
            start_time=timezone.now() - timezone.timedelta(days=1),
            end_time=timezone.now() + timezone.timedelta(days=1),
            start_price=100.0,
            item_name="Test Item"
        )

    def test_bid_success(self):
        data = {
            "token_value": "usertoken",
            "auction_id": self.auction.id,
            "bid_amount": 150.0,  # Replace with a valid bid amount
        }
        response = self.client.post('/api/bid/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check if the bid has been created
        self.assertTrue(Bid.objects.filter(auction_id=self.auction, user_id=self.user).exists())

    def test_bid_missing_token_value(self):
        data = {
            "auction_id": self.auction.id,
            "bid_amount": 150.0,
        }
        response = self.client.post('/api/bid/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("token_value is required", str(response.content))

    def test_bid_invalid_token(self):
        data = {
            "token_value": "invalidtoken",  # Invalid token
            "auction_id": self.auction.id,
            "bid_amount": 150.0,
        }
        response = self.client.post('/api/bid/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("token does not exist", str(response.content))

    def test_bid_invalid_role(self):
        data = {
            "token_value": "admintoken",  # Admin token
            "auction_id": self.auction.id,
            "bid_amount": 150.0,
        }
        response = self.client.post('/api/bid/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Not valid", str(response.content))

    def test_bid_missing_auction_id(self):
        data = {
            "token_value": "usertoken",
            "bid_amount": 150.0,
        }
        response = self.client.post('/api/bid/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("auction_id is required", str(response.content))

    def test_bid_invalid_auction_id(self):
        data = {
            "token_value": "usertoken",
            "auction_id": 999,  # Non-existent auction ID
            "bid_amount": 150.0,
        }
        response = self.client.post('/api/bid/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("auction does not exist", str(response.content))

    def test_bid_inactive_auction(self):
        # Create an inactive auction for testing
        inactive_auction = Auction.objects.create(
            start_time=timezone.now() - timezone.timedelta(days=2),
            end_time=timezone.now() - timezone.timedelta(days=1),
            start_price=100.0,
            item_name="Inactive Test Item"
        )

        data = {
            "token_value": "usertoken",
            "auction_id": inactive_auction.id,
            "bid_amount": 150.0,
        }
        response = self.client.post('/api/bid/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("auction is not active", str(response.content))

    def test_bid_missing_bid_amount(self):
        data = {
            "token_value": "usertoken",
            "auction_id": self.auction.id,
        }
        response = self.client.post('/api/bid/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("bid_amount is required", str(response.content))

    def test_bid_less_than_start_price(self):
        data = {
            "token_value": "usertoken",
            "auction_id": self.auction.id,
            "bid_amount": 50.0,  # Less than the start price
        }
        response = self.client.post('/api/bid/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("bid_amount is less than start_price", str(response.content))

class GetWinnerTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Create a user for testing
        self.user = User.objects.create(username="testuser", email="test@example.com", password="testpassword", role="user")
        self.user_token = Token.objects.create(user_id=self.user, token_value="usertoken")
        self.user_token.save()

        # Create an auction for testing
        self.auction = Auction.objects.create(
            start_time=timezone.now() - timezone.timedelta(days=2),
            end_time=timezone.now() - timezone.timedelta(days=1),
            start_price=100.0,
            item_name="Test Item"
        )

    def test_get_winner_success(self):
        # Create a bid for testing
        Bid.objects.create(
            auction_id=self.auction,
            user_id=self.user,
            bid_amount=150.0,  # Higher bid amount
        )

        data = {
            "auction_id": self.auction.id,
        }
        response = self.client.get('/api/get_winner/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("winner", response.data)
        self.assertEqual(response.data["winner"], self.user.username)

    def test_get_winner_no_winner(self):
        data = {
            "auction_id": self.auction.id,
        }
        response = self.client.get('/api/get_winner/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("winner", response.data)
        self.assertEqual(response.data["winner"], "No winner")

    def test_get_winner_missing_auction_id(self):
        data = {}
        response = self.client.get('/api/get_winner/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("auction_id is required", str(response.content))

    def test_get_winner_invalid_auction_id(self):
        data = {
            "auction_id": 999,  # Non-existent auction ID
        }
        response = self.client.get('/api/get_winner/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("auction does not exist", str(response.content))

    def test_get_winner_auction_not_ended(self):
        data = {
            "auction_id": self.auction.id,
        }
        response = self.client.get('/api/get_winner/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("auction is not ended", str(response.content))

    def test_get_winner_multiple_bids_same_amount(self):
        # Create multiple bids with the same bid amount for testing
        Bid.objects.create(
            auction_id=self.auction,
            user_id=self.user,
            bid_amount=150.0,
        )

        data = {
            "auction_id": self.auction.id,
        }
        response = self.client.get('/api/get_winner/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("winner", response.data)
        self.assertEqual(response.data["winner"], "No winner")
