from rest_framework import mixins, viewsets,status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import action
from rest_framework.response import Response

from django.db import transaction
from django.utils import timezone

from .models import Borrowing
from .serializers import BorrowingSerializer, BorrowingCreateSerializer


class BorrowingViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer
    permission_classes = [IsAuthenticated]


    def get_queryset(self):
        queryset = Borrowing.objects.select_related(
            "book",
            "user",
        )

        # Non-admin users see only their own borrowings
        if not self.request.user.is_staff:
            queryset = queryset.filter(
                user=self.request.user
            )

        # Admin filter by user_id
        user_id = self.request.query_params.get("user_id")

        if self.request.user.is_staff and user_id:
            queryset = queryset.filter(
                user_id=user_id
            )

        is_active = self.request.query_params.get("is_active")

        if is_active is not None:
            if is_active.lower() == "true":
                queryset = queryset.filter(
                    actual_return_date__isnull=True
                )

            elif is_active.lower() == "false":
                queryset = queryset.filter(
                    actual_return_date__isnull=False
                )

        return queryset

    def get_serializer_class(self):
        if self.action == "create":
            return BorrowingCreateSerializer

        return BorrowingSerializer

    @transaction.atomic
    def perform_create(self, serializer):
        book = serializer.validated_data["book"]

        if book.inventory < 1:
            raise ValidationError("Book is not available")

        book.inventory -= 1
        book.save()

        serializer.save(
            user=self.request.user,
            borrow_date=timezone.now().date(),
        )

    @action(
        detail=True,
        methods=["post"],
        url_path="return",
    )

    @transaction.atomic
    def return_book(self, request, pk=None):
        borrowing = self.get_object()

        if borrowing.actual_return_date:
            raise ValidationError(
                "This borrowing has already been returned."
            )

        borrowing.actual_return_date = timezone.now().date()
        borrowing.save()

        borrowing.book.inventory += 1
        borrowing.book.save()

        serializer = BorrowingSerializer(borrowing)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )
