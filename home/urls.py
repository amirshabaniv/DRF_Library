from rest_framework_nested import routers
from . import views
from django.urls import path, include


router = routers.DefaultRouter()

router.register('authors', views.AuthorViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('', views.HomeView.as_view()),
    path('books/', views.BookView.as_view()),
    path('books/<int:pk>/', views.BookRetrieveAndCommentView.as_view()),
]