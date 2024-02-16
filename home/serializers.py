from rest_framework import serializers
from .models import Book, BookRating, Author, Category, BookComment
from statistics import mean

class BookRatingSerializer(serializers.ModelSerializer):

    class Meta:
        model = BookRating
        fields = ["id", "rating"]
    
    def create(self, validated_data):
        book_id = self.context["book_id"]
        user_id = self.context["user_id"]
        rating = BookRating.objects.create(book_id=book_id, user_id=user_id, **self.validated_data)
        return rating


class BookCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = BookComment
        fields = ['id', 'book', 'user', 'body', 'created_at']


class BookSerializer(serializers.ModelSerializer):
    stars_avg = serializers.SerializerMethodField(method_name='avg_stars')
    book_comments = BookCommentSerializer(many=True)

    class Meta:
        model = Book
        fields = ['id', 'name', 'author', 'isbn',
                  'date_of_release', 'category',
                  'summary', 'publisher', 'language',
                  'price', 'availability', 'cover_image',
                  'number_of_inventory', 'stars_avg', 'book_comments']

    def avg_stars(self, book:Book):
        items = book.book_ratings.all()
        if items.exists():
            avg = mean([item.rating for item in items])
            return avg
        return 0


class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Author
        fields = ['id', 'name', 'bio', 'author_books']

    

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'name']

