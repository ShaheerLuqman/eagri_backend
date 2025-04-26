from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import LoanRequest
from .serializers import (
    LoanRequestSerializer, 
    LoanApprovalSerializer
)
from django.utils import timezone

class CreateLoanRequestView(generics.CreateAPIView):
    queryset = LoanRequest.objects.all()
    serializer_class = LoanRequestSerializer
    permission_classes = [IsAuthenticated]

class ListLoanRequestView(generics.ListAPIView):
    queryset = LoanRequest.objects.all()
    serializer_class = LoanRequestSerializer
    permission_classes = [IsAuthenticated]

class LoanRequestDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = LoanRequest.objects.all()
    serializer_class = LoanRequestSerializer
    permission_classes = [IsAuthenticated]

class LoanRequestByUserView(generics.ListAPIView):
    serializer_class = LoanRequestSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return LoanRequest.objects.filter(user_id=user_id)

class LoanApprovalView(generics.UpdateAPIView):
    queryset = LoanRequest.objects.all()
    serializer_class = LoanApprovalSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        if serializer.validated_data.get('status') == 'approved':
            serializer.validated_data['approved_at'] = timezone.now()

        self.perform_update(serializer)
        return Response(serializer.data)
