from rest_framework import generics
from .models import Book, Transaction
from .serializers import BookSerializer, TransactionSerializer
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

@permission_classes([AllowAny])
class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]


class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]


class BorrowBookView(generics.CreateAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        book = serializer.validated_data['book']
        if book.copies_available > 0:
            book.copies_available -= 1
            book.save()
            serializer.save(user=self.request.user)
        else:
            raise serializers.ValidationError("No copies available for checkout.")


class ReturnBookView(generics.UpdateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        transaction = self.get_object()
        book = transaction.book
        book.copies_available += 1
        book.save()
        serializer.save(return_date=models.DateTimeField(auto_now=True))

