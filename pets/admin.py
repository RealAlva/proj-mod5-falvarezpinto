from django.contrib import admin
from .models import Pet, Post, Comment, Like


# Registrando el modelo Pet
@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ('name', 'species', 'breed', 'age', 'owner')
    search_fields = ('name', 'species', 'breed', 'owner__username')
    list_filter = ('species', 'breed')

# Registrando el modelo Post
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('content', 'created_at', 'pet', 'owner')
    search_fields = ('content', 'pet__name', 'owner__username')
    list_filter = ('created_at',)

admin.site.register(Comment)
admin.site.register(Like)
