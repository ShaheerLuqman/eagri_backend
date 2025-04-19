from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import LoanRecord
from .serializers import LoanRecordSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class LoanRecordViewSet(viewsets.ModelViewSet):
    queryset = LoanRecord.objects.all()
    serializer_class = LoanRecordSerializer

    def create(self, request, *args, **kwargs):
        try:
            # Check if user exists before trying to create the record
            user_id = request.data.get('user')
            if not user_id:
                return Response(
                    {"error": "User ID is required"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            try:
                User.objects.get(id=user_id)
            except User.DoesNotExist:
                return Response(
                    {"error": f"User with ID {user_id} does not exist"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            return super().create(request, *args, **kwargs)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )