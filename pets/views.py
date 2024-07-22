from django.shortcuts import render
from rest_framework import viewsets
from .models import Pet, Post, Comment
from .serializers import PetSerializer, PostSerializer, CommentSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class PetViewSet(viewsets.ModelViewSet):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class PetPostsAPIView(APIView):
    def get(self, request, pet_id, format=None):
        # Filtrar las publicaciones por el ID de la mascota y ordenarlas por fecha de creación
        posts = Post.objects.filter(pet_id=pet_id).order_by('-created_at')
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
