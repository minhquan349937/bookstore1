from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from api.models import Cart, CartItem
from api.serializers import CartSerializer, CartItemSerializer
from django.db.models import F, Sum

@api_view(['GET'])
def api_root(request):
    return Response({'message': 'Welcome to Cart Service'})

# ============ CART OPERATIONS ============

@api_view(['GET', 'POST'])
def get_or_create_cart(request, user_id):
    """
    GET /carts/{user_id}/ - Get user's cart
    POST /carts/{user_id}/ - Create/get cart
    """
    cart, created = Cart.objects.get_or_create(user_id=user_id)
    serializer = CartSerializer(cart)
    return Response(serializer.data)

@api_view(['POST'])
def add_to_cart(request, user_id):
    """
    POST /carts/{user_id}/add_item/ - Add item to cart
    Body: {"book_id": 1, "quantity": 2, "price": 100000}
    """
    try:
        cart, created = Cart.objects.get_or_create(user_id=user_id)
        book_id = request.data.get('book_id')
        quantity = int(request.data.get('quantity', 1))
        price = request.data.get('price', 0)
        
        if price:
            price = float(price)
        else:
            price = 0
        
        # Check if item already in cart
        item, item_created = CartItem.objects.get_or_create(
            cart=cart,
            book_id=book_id,
            defaults={'quantity': quantity, 'price': price}
        )
        
        if not item_created:
            item.quantity += quantity
            item.save()
        
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=201)
    except Exception as e:
        return Response({'error': str(e)}, status=400)

@api_view(['POST'])
def remove_from_cart(request, user_id):
    """
    POST /carts/{user_id}/remove_item/ - Remove item from cart
    Body: {"book_id": 1}
    """
    try:
        cart = Cart.objects.get(user_id=user_id)
        book_id = request.data.get('book_id')
        CartItem.objects.filter(cart=cart, book_id=book_id).delete()
        
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=200)
    except Cart.DoesNotExist:
        return Response({'error': 'Cart not found'}, status=404)
    except Exception as e:
        return Response({'error': str(e)}, status=400)

@api_view(['POST'])
def update_cart_quantity(request, user_id):
    """
    POST /carts/{user_id}/update_quantity/ - Update item quantity
    Body: {"book_id": 1, "quantity": 5}
    """
    try:
        cart = Cart.objects.get(user_id=user_id)
        book_id = request.data.get('book_id')
        quantity = int(request.data.get('quantity', 1))
        
        if quantity <= 0:
            CartItem.objects.filter(cart=cart, book_id=book_id).delete()
        else:
            item = CartItem.objects.get(cart=cart, book_id=book_id)
            item.quantity = quantity
            item.save()
        
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=200)
    except Cart.DoesNotExist:
        return Response({'error': 'Cart not found'}, status=404)
    except CartItem.DoesNotExist:
        return Response({'error': 'Item not found in cart'}, status=404)
    except Exception as e:
        return Response({'error': str(e)}, status=400)

@api_view(['DELETE'])
def clear_cart(request, user_id):
    """
    DELETE /carts/{user_id}/clear_cart/ - Clear entire cart
    """
    try:
        cart = Cart.objects.get(user_id=user_id)
        CartItem.objects.filter(cart=cart).delete()
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=200)
    except Cart.DoesNotExist:
        return Response({'error': 'Cart not found'}, status=404)
    except Exception as e:
        return Response({'error': str(e)}, status=400)
