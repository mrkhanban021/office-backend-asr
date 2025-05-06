from .serializers import ToolsSerializers
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny
from .models import Tools


class ToolsApiList(ListCreateAPIView):
    queryset = Tools.objects.all()
    serializer_class = ToolsSerializers
    permission_classes = [AllowAny]


class ToolsApiListDetail(RetrieveUpdateDestroyAPIView):
    queryset = Tools.objects.all()
    serializer_class = ToolsSerializers
    permission_classes = [AllowAny]


