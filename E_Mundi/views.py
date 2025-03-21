from rest_framework import viewsets
from .models import MundiModel
from .serializers import MundiModelSerializer

class MundiModelViewSet(viewsets.ModelViewSet):
    queryset = MundiModel.objects.all()
    serializer_class = MundiModelSerializer 