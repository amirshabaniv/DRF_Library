from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from .serializers import BookSerializer, BookRatingSerializer, AuthorSerializer, BookCommentSerializer, CategorySerializer
from .models import Book, BookRating, Author, Category
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from rest_framework import filters


class BookView(ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookRetrieveAndCommentView(APIView):

    def get(self, request, pk):
        book = Book.objects.get(pk=pk)
        srz_data = BookSerializer(instance=book)
        return Response(srz_data.data, status=status.HTTP_200_OK)
    
    @permission_classes([IsAuthenticated])
    def post(self, request, pk):
        srz_data = BookCommentSerializer(data=request.POST)
        if srz_data.is_valid():
            srz_data.save()
            return Response(srz_data.data, status=status.HTTP_201_CREATED)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)
    

class BookRatingViewSet(ModelViewSet):
    serializer_class = BookRatingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return BookRating.objects.filter(book_id = self.kwargs['book_pk'])

    def get_serializer_context(self):
        user_id = self.request.user.id
        book_id = self.kwargs["book_pk"]
        return {"user_id": user_id, "book_id": book_id}


class AuthorViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    serializer_class = AuthorSerializer
    queryset = Author.objects.all()


class HomeView(ListAPIView):
    serializer_class = BookSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'category__name']

    def get_queryset(self):
        return Book.objects.order_by('-published_date')[:20]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.all()
        authors = Author.objects.all()
        category_serializer = CategorySerializer(categories, many=True)
        author_serializer = AuthorSerializer(authors, many=True)
        context['categories'] = category_serializer.data
        context['authors'] = author_serializer.data
        return context