from rest_framework import viewsets
from .models import CustomUser
from .serializers import CustomUserSerializer
from rest_framework_simplejwt.views import TokenObtainPairView # type: ignore
from .serializers import MyTokenObtainPairSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.filter(is_deleted=False)  #  Solo usuarios activos
    serializer_class = CustomUserSerializer

    def perform_destroy(self, instance):
        """Sobreescribir borrado físico por lógico"""
        instance.delete()

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_users(request):
    q = request.GET.get('q', '')
    users = CustomUser.objects.filter(is_deleted=False, role='user')
    if q:
        users = users.filter(Q(first_name__icontains=q) | Q(last_name__icontains=q))
    data = [{"value": u.id, "label": f"{u.first_name} {u.last_name}"} for u in users]
    return Response(data)