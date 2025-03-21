from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework import status
from .models import LoanRequest
from .serializers import LoanRequestSerializer

class CreateLoanRequestView(generics.CreateAPIView):
    queryset = LoanRequest.objects.all()
    serializer_class = LoanRequestSerializer

class ListLoanRequestView(generics.ListAPIView):
    queryset = LoanRequest.objects.all()
    serializer_class = LoanRequestSerializer

class LoanRequestDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = LoanRequest.objects.all()
    serializer_class = LoanRequestSerializer
