from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework import status
from .models import LoanRequest, LoanApproval, LoanFinePayment
from .serializers import (
    LoanRequestSerializer, 
    LoanApprovalSerializer, 
    LoanFinePaymentSerializer
)

class CreateLoanRequestView(generics.CreateAPIView):
    queryset = LoanRequest.objects.all()
    serializer_class = LoanRequestSerializer

class ListLoanRequestView(generics.ListAPIView):
    queryset = LoanRequest.objects.all()
    serializer_class = LoanRequestSerializer

class LoanRequestDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = LoanRequest.objects.all()
    serializer_class = LoanRequestSerializer

class LoanApprovalListCreateView(generics.ListCreateAPIView):
    queryset = LoanApproval.objects.all()
    serializer_class = LoanApprovalSerializer

class LoanApprovalDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = LoanApproval.objects.all()
    serializer_class = LoanApprovalSerializer

class LoanFinePaymentListCreateView(generics.ListCreateAPIView):
    queryset = LoanFinePayment.objects.all()
    serializer_class = LoanFinePaymentSerializer

class LoanFinePaymentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = LoanFinePayment.objects.all()
    serializer_class = LoanFinePaymentSerializer
