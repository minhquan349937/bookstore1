from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.
@api_view(['GET'])
def api_root(request):
    return Response({'message': 'Welcome to the API'})
