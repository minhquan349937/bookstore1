# api/views.py - CART SERVICE

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
import requests

class CartViewSet(viewsets.ModelViewSet):
    """
    ViewSet cho quản lý giỏ hàng
    
    Endpoints:
    - GET /api/carts/{customer_id}/ - Lấy giỏ hàng
    - POST /api/carts/ - Tạo giỏ hàng
    - PUT /api/carts/{customer_id}/ - Cập nhật giỏ hàng
    - DELETE /api/carts/{customer_id}/ - Xóa giỏ hàng
    """
    
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    lookup_field = 'customer_id'
    
    def get_queryset(self):
        """Trả về giỏ hàng của khách hàng"""
        customer_id = self.kwargs.get('customer_id')
        if customer_id:
            return Cart.objects.filter(customer_id=customer_id)
        return Cart.objects.all()
    
    @action(detail=True, methods=['post'])
    def add_item(self, request, customer_id=None):
        """
        Thêm sản phẩm vào giỏ hàng
        
        POST /api/carts/{customer_id}/add_item/
        Body:
        {
            "book_id": 1,
            "book_title": "Django for Beginners",
            "book_author": "William Vincent",
            "book_price": 29.99,
            "quantity": 2
        }
        """
        
        try:
            # Lấy hoặc tạo giỏ hàng
            cart, created = Cart.objects.get_or_create(customer_id=customer_id)
            
            book_id = request.data.get('book_id')
            quantity = request.data.get('quantity', 1)
            book_title = request.data.get('book_title')
            book_author = request.data.get('book_author')
            book_price = request.data.get('book_price')
            
            # Kiểm tra dữ liệu
            if not book_id or not book_title or not book_price:
                return Response(
                    {'error': 'Thiếu thông tin sách'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Kiểm tra xem sách đã trong giỏ chưa
            cart_item, item_created = CartItem.objects.get_or_create(
                cart=cart,
                book_id=book_id,
                defaults={
                    'book_title': book_title,
                    'book_author': book_author,
                    'book_price': book_price,
                    'quantity': quantity
                }
            )
            
            # Nếu đã tồn tại, tăng số lượng
            if not item_created:
                cart_item.quantity += int(quantity)
                cart_item.save()
            
            # Cập nhật tổng giỏ hàng
            self._update_cart_totals(cart)
            
            serializer = self.get_serializer(cart)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['post'])
    def remove_item(self, request, customer_id=None):
        """
        Xóa sản phẩm khỏi giỏ hàng
        
        POST /api/carts/{customer_id}/remove_item/
        Body:
        {
            "book_id": 1
        }
        """
        
        try:
            cart = Cart.objects.get(customer_id=customer_id)
            book_id = request.data.get('book_id')
            
            if not book_id:
                return Response(
                    {'error': 'Cần cung cấp book_id'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Xóa mặt hàng
            CartItem.objects.filter(cart=cart, book_id=book_id).delete()
            
            # Cập nhật tổng giỏ hàng
            self._update_cart_totals(cart)
            
            serializer = self.get_serializer(cart)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Cart.DoesNotExist:
            return Response(
                {'error': 'Giỏ hàng không tồn tại'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['post'])
    def update_quantity(self, request, customer_id=None):
        """
        Cập nhật số lượng sản phẩm
        
        POST /api/carts/{customer_id}/update_quantity/
        Body:
        {
            "book_id": 1,
            "quantity": 3
        }
        """
        
        try:
            cart = Cart.objects.get(customer_id=customer_id)
            book_id = request.data.get('book_id')
            quantity = request.data.get('quantity')
            
            if not book_id or quantity is None:
                return Response(
                    {'error': 'Cần cung cấp book_id và quantity'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            if int(quantity) < 1:
                return Response(
                    {'error': 'Số lượng phải lớn hơn 0'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Cập nhật số lượng
            CartItem.objects.filter(
                cart=cart,
                book_id=book_id
            ).update(quantity=quantity)
            
            # Cập nhật tổng giỏ hàng
            self._update_cart_totals(cart)
            
            serializer = self.get_serializer(cart)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Cart.DoesNotExist:
            return Response(
                {'error': 'Giỏ hàng không tồn tại'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['post'])
    def clear(self, request, customer_id=None):
        """
        Xóa toàn bộ giỏ hàng
        
        POST /api/carts/{customer_id}/clear/
        """
        
        try:
            cart = Cart.objects.get(customer_id=customer_id)
            CartItem.objects.filter(cart=cart).delete()
            
            # Reset cart totals
            cart.total_items = 0
            cart.total_price = 0
            cart.save()
            
            serializer = self.get_serializer(cart)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Cart.DoesNotExist:
            return Response(
                {'error': 'Giỏ hàng không tồn tại'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def _update_cart_totals(self, cart):
        """Cập nhật tổng tiền và số lượng giỏ hàng"""
        items = cart.items.all()
        
        total_items = sum(item.quantity for item in items)
        total_price = sum(item.subtotal for item in items)
        
        cart.total_items = total_items
        cart.total_price = total_price
        cart.save()
