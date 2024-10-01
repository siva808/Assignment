from rest_framework_simplejwt.views import TokenObtainPairView
from .models import *
from rest_framework import viewsets, serializers
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.decorators import action, api_view,permission_classes
from .permissions import *
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, permissions,generics
from .models import CustomUser
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .serializers import UserSerializer, MachineSerializer
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from .serializers import UserSerializer
from rest_framework import generics
from rest_framework.permissions import AllowAny
from .serializers import *
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
from datetime import timedelta
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class UserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MachineDataCreateView(generics.CreateAPIView):
    queryset = Machine.objects.all()
    serializer_class = MachineSerializer
    permission_classes = [permissions.IsAuthenticated]

class FieldViewSet(viewsets.ModelViewSet):
    queryset = Field.objects.all()
    serializer_class = FieldSerializer
    permission_classes = [permissions.IsAuthenticated]


class MachineDataListView(generics.ListAPIView):
    queryset = Machine.objects.all()
    serializer_class = MachineSerializer

class MachineHistoricalDataView(generics.ListAPIView):
    serializer_class = FieldSerializer

    def get_queryset(self):
        axis_id = self.kwargs['axis_id']
        fifteen_minutes_ago = timezone.now() - timedelta(minutes=15)
        return Field.objects.filter(axis__id=axis_id, timestamp__gte=fifteen_minutes_ago)

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        # Determine which permissions to use based on the action
        if self.action in ['create', 'update', 'destroy']:
            return [permissions.IsAuthenticated(), IsSuperAdminOrManager()]
        elif self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        return super().get_permissions()

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def current_user(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)



class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Customize your token claims here
        token['username'] = user.username
        token['role'] = user.role

        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    


class MachineDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Machine
        fields = ['id', 'timestamp', 'axis_value']

@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Ensure the user is authenticated
def historical_data(request):
    now = timezone.now()
    fifteen_minutes_ago = now - timedelta(minutes=15)
    data = Machine.objects.filter(timestamp__gte=fifteen_minutes_ago)
    serializer = MachineDataSerializer(data, many=True)
    return Response(serializer.data)
