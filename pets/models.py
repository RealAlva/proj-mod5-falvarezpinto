from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Pet(models.Model):
    name = models.CharField(max_length=100)
    species = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)
    age = models.IntegerField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    def clean(self):
        if self.age < 0:
            raise ValidationError('La edad no puede ser negativa.')
        if not self.name:
            raise ValidationError('El nombre de la mascota no puede estar vacío.')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

class Post(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Post by {self.owner.username} on {self.created_at}'

    def clean(self):
        if not self.content:
            raise ValidationError('El contenido no puede estar vacío.')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

class Comment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.created_at}'

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} likes Post {self.post.id}'
