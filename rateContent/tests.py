from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rateContent import models

class PlatformTesting(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="example", password="Password@123")
        self.token = Token.objects.get(user__username=self.user.username)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.stream = models.Platform.objects.create(name="Netflix", about="#BEST", website_url="http://NETFIX.com")

    def test_platform_create(self):
        data = {
            "name": "Netflix",
            "about": "#BEST",
            "website_url": "http://NETFIX.com"
        }
        url = reverse("platformView-list")
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_platform_list(self):
        url = reverse("platformView-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_platform_detail(self):
        url = reverse("platformView-detail", args=[self.stream.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TitleTesting(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="example", password="Password@123")
        self.token = Token.objects.get(user__username=self.user.username)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.stream = models.Platform.objects.create(name="Netflix", about="#BEST", website_url="http://NETFIX.com")
        self.title = models.TitleList.objects.create(title="LOL", storyline="Awesome storyline", active=True, platform=self.stream)

    def test_title_create(self):
        data = {
            "title": "LOL",
            "storyline": "Awesome storyline",
            "active": True,
            "platform": self.stream.id
        }
        url = reverse("titles-list")
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_title_list(self):
        url = reverse("titles-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_title_detail(self):
        url = reverse("title-detail", args=[self.title.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(models.TitleList.objects.count(), 1)
        self.assertEqual(models.TitleList.objects.get().title, 'LOL')


class ReviewTesting(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="example", password="Password@123")
        self.token = Token.objects.get(user__username=self.user.username)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.stream = models.Platform.objects.create(name="Netflix", about="#BEST", website_url="http://NETFIX.com")
        self.title = models.TitleList.objects.create(title="LOL", storyline="Awesome storyline", active=True, platform=self.stream)
        self.title2 = models.TitleList.objects.create(title="LOL", storyline="Awesome storyline", active=True, platform=self.stream)
        self.review = models.Review.objects.create(reviewer_name=self.user, rating=4, TitleList=self.title2, description="GGGGGG", active=True)

    def test_review_create(self):
        data = {
            "reviewer_name": self.user.id,
            "rating": 4,
            "TitleList": self.title.id,
            "description": "GGGGGGGGGGGGGGGGGGGGG",
            "active": True
        }
        url = reverse("review-create", args=[self.title.id])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Attempt to create a duplicate review
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEqual(models.Review.objects.count(), 2)  # The initial review in setUp and this one
        self.assertEqual(models.Review.objects.filter(rating=4).count(), 2)

    def test_review_anon(self):
        data = {
            "reviewer_name": self.user.id,
            "rating": 4,
            "title_list": self.title.id,
            "description": "GGGGGG",
            "active": True
        }
        self.client.force_authenticate(user=None)
        url = reverse("review-create", args=[self.title.id])
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  

    def test_review_update(self):
        data = {
            "reviewer_name": self.user.id,
            "rating": 1,
            "TitleList": self.title.id,
            "description": "G",
            "active": False
        }
        url = reverse("review-detail", args=[self.review.id])
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)  

        # Check the updated review
        self.review.refresh_from_db()
        self.assertEqual(self.review.rating, 1)
        self.assertEqual(self.review.description, "G")
        self.assertFalse(self.review.active)

    def test_review_list(self):
        url = reverse("title-reviews", args=[self.title.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_review_detail(self):
        url = reverse("review-detail", args=[self.review.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_review_user_reviews(self):
        username = self.user.username
        url = ("/reviews/username/?username="+username)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


