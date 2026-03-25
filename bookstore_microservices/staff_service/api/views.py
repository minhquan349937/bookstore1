from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from api.models import Staff
from api.serializers import (
    StaffRegisterSerializer,
    StaffLoginSerializer,
    StaffProfileSerializer
)

# ============ AUTHENTICATION VIEWS ============

@api_view(['GET'])
def api_root(request):
    return Response({'message': 'Welcome to the Staff API'})

@api_view(['POST'])
@permission_classes([AllowAny])
def staff_register(request):
    """
    POST /staff-users/register/ - Create new staff account
    """
    serializer = StaffRegisterSerializer(data=request.data)
    
    if serializer.is_valid():
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        staff = Staff.objects.get(user=user)
        
        return Response({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'token': token.key,
            'role': staff.role,
            'message': 'Đăng ký thành công'
        }, status=201)
    
    return Response(serializer.errors, status=400)

@api_view(['POST'])
@permission_classes([AllowAny])
def staff_login(request):
    """
    POST /staff-users/login/ - Authenticate staff member
    """
    serializer = StaffLoginSerializer(data=request.data)
    
    if serializer.is_valid():
        username = serializer.validated_data.get('username')
        password = serializer.validated_data.get('password')
        
        user = authenticate(username=username, password=password)
        
        if user:
            try:
                staff = Staff.objects.get(user=user)
                token, created = Token.objects.get_or_create(user=user)
                
                return Response({
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'token': token.key,
                    'role': staff.role,
                    'message': 'Đăng nhập thành công'
                }, status=200)
            except Staff.DoesNotExist:
                return Response({
                    'error': 'Staff profile not found'
                }, status=404)
        
        return Response({
            'error': 'Invalid credentials'
        }, status=401)
    
    return Response(serializer.errors, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def staff_profile(request):
    """
    GET /staff-users/profile/ - Get current staff profile
    Requires: Token authentication
    """
    try:
        staff = Staff.objects.get(user=request.user)
        serializer = StaffProfileSerializer(staff)
        return Response(serializer.data, status=200)
    except Staff.DoesNotExist:
        return Response({
            'error': 'Staff profile not found'
        }, status=404)
