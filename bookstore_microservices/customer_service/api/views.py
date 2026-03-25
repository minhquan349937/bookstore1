from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import CustomerProfile
from .serializers import (
    CustomerProfileSerializer,
    RegisterSerializer,
    LoginSerializer,
    UserSerializer
)

# ============ AUTHENTICATION VIEWS ============
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """Customer registration endpoint"""
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'token': token.key,
            'message': 'Đăng ký thành công'
        }, status=status.HTTP_201_CREATED)
    
    errors = {}
    for field, messages in serializer.errors.items():
        errors[field] = messages[0] if messages else 'Error'
    
    return Response(errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """Customer login endpoint"""
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        
        user = authenticate(username=username, password=password)
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'token': token.key,
                'message': 'Đăng nhập thành công'
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': 'Tên đăng nhập hoặc mật khẩu không đúng'
            }, status=status.HTTP_401_UNAUTHORIZED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request):
    """Get customer profile"""
    try:
        profile = CustomerProfile.objects.get(user=request.user)
        serializer = CustomerProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except CustomerProfile.DoesNotExist:
        return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def api_root(request):
    return Response({'service': 'Customer Service', 'status': 'online'})
