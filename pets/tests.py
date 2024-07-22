from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Pet, Post, Comment
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

class PetModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.pet = Pet.objects.create(name='Fido', species='Dog', breed='Labrador', age=2, owner=self.user)

    def test_pet_creation(self):
        self.assertEqual(self.pet.name, 'Fido')
        self.assertEqual(self.pet.species, 'Dog')
        self.assertEqual(self.pet.breed, 'Labrador')
        self.assertEqual(self.pet.age, 2)
        self.assertEqual(self.pet.owner.username, 'testuser')

    def test_age_validation(self):
        with self.assertRaises(Exception):
            Pet.objects.create(name='Rex', species='Dog', breed='Bulldog', age=-1, owner=self.user)

class PostModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.pet = Pet.objects.create(name='Fido', species='Dog', breed='Labrador', age=2, owner=self.user)
        self.post = Post.objects.create(content='This is a test post', pet=self.pet, owner=self.user)

    def test_post_creation(self):
        self.assertEqual(self.post.content, 'This is a test post')
        self.assertEqual(self.post.pet.name, 'Fido')
        self.assertEqual(self.post.owner.username, 'testuser')

    def test_content_validation(self):
        post = Post(content='', pet=self.pet, owner=self.user)
        with self.assertRaises(ValidationError):
            post.full_clean()  # Esto ejecutará las validaciones del modelo

# Prueba para las vistas y las APIs
class PetAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.pet = Pet.objects.create(name='Fido', species='Dog', breed='Labrador', age=2, owner=self.user)

    def test_get_pets(self):
        url = reverse('pet-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Fido')

    def test_create_pet(self):
        url = reverse('pet-list')
        data = {
            'name': 'Rex',
            'species': 'Dog',
            'breed': 'Bulldog',
            'age': 3,
            'owner': self.user.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Pet.objects.count(), 2)

class PostAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.pet = Pet.objects.create(name='Fido', species='Dog', breed='Labrador', age=2, owner=self.user)
        self.post = Post.objects.create(content='This is a test post', pet=self.pet, owner=self.user)

    def test_get_posts(self):
        url = reverse('post-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['content'], 'This is a test post')

    def test_create_post(self):
        url = reverse('post-list')
        data = {
            'content': 'Another test post',
            'pet': self.pet.id,
            'owner': self.user.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 2)
