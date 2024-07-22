from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PetViewSet, PostViewSet, CommentViewSet, PetPostsAPIView
from django.urls import path, include

router = DefaultRouter()
router.register(r'pets', PetViewSet)
router.register(r'posts', PostViewSet)
router.register(r'comments', CommentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    #path('custom-api/', CustomAPIView.as_view(), name='custom-api'),
    path('pets/<int:pet_id>/posts/', PetPostsAPIView.as_view(), name='pet-posts'),
]
