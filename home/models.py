from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()


class Author(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='media/author_images/')
    bio = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class Book(models.Model):
    name = models.CharField(max_length=200)
    author = models.ManyToManyField(Author, related_name='author_books')
    isbn = models.CharField(max_length=13, unique=True)
    date_of_release = models.DateTimeField()
    category = models.ManyToManyField(Category, related_name='category_books')
    summary = models.TextField()
    publisher = models.CharField(max_length=150)
    language = models.CharField(max_length=100)
    price = models.IntegerField()
    availability = models.BooleanField(default=True)
    cover_image = models.ImageField(upload_to='media/book_covers/')
    number_of_inventory = models.IntegerField()

    def __str__(self):
        return f'{self.name} written by {self.author}'


class BookLoan(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='book_bookloan')
    loan_date = models.DateField()
    return_date = models.DateField()
    returned = models.BooleanField(default=False)

    def __str__(self):
        return self.book


class BookRating(models.Model):
    RATING_CHOICES = (
        (1, '1 star'),
        (2, '2 stars'),
        (3, '3 stars'),
        (4, '4 stars'),
        (5, '5 stars')
    )
    
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name = 'book_ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=RATING_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('book', 'user')

    def __str__(self):
        return f"{self.user}'s {self.rating}-star rating for {self.book}"


class BookComment(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='book_comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comments')
    body = models.TextField()
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} wrote a comment about {self.book}'


    