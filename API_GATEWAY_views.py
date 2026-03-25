# api/views.py - API GATEWAY

from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests
import logging

logger = logging.getLogger(__name__)

# URL của các services
SERVICES = {
    'books': 'http://localhost:8001/api/',
    'customers': 'http://localhost:8002/api/',
    'staff': 'http://localhost:8003/api/',
    'orders': 'http://localhost:8004/api/',
}

@api_view(['GET'])
def api_root(request):
    """API Gateway Root - Hiển thị danh sách các services"""
    return Response({
        'message': 'Chào mừng đến Bookstore Microservices API Gateway',
        'version': '1.0.0',
        'services': {
            'books': f"{SERVICES['books']}books/",
            'customers': f"{SERVICES['customers']}customers/",
            'staff': f"{SERVICES['staff']}staff/",
            'orders': f"{SERVICES['orders']}orders/",
        },
        'status': check_services_status()
    })

def check_services_status():
    """Kiểm tra trạng thái của tất cả services"""
    status_dict = {}
    
    for service_name, service_url in SERVICES.items():
        try:
            response = requests.get(service_url, timeout=2)
            status_dict[service_name] = 'OK' if response.status_code < 500 else 'ERROR'
        except requests.exceptions.ConnectionError:
            status_dict[service_name] = 'OFFLINE'
        except Exception as e:
            status_dict[service_name] = 'ERROR'
            logger.error(f"Error checking {service_name}: {str(e)}")
    
    return status_dict

@api_view(['GET'])
def health_check(request):
    """Health check endpoint"""
    return Response({
        'status': 'healthy',
        'services': check_services_status()
    })

@api_view(['POST'])
def create_order(request):
    """
    Endpoint tổng hợp để tạo đơn hàng
    
    Body:
    {
        "customer_id": 1,
        "items": [
            {"book_id": 1, "quantity": 2},
            {"book_id": 3, "quantity": 1}
        ],
        "shipping_address": "...",
        "payment_method": "card"
    }
    """
    
    try:
        data = request.data
        customer_id = data.get('customer_id')
        items = data.get('items', [])
        shipping_address = data.get('shipping_address')
        payment_method = data.get('payment_method', 'cash')
        
        # Kiểm tra khách hàng
        customer_response = requests.get(
            f"{SERVICES['customers']}customers/{customer_id}/",
            timeout=5
        )
        
        if customer_response.status_code != 200:
            return Response(
                {'error': 'Khách hàng không tồn tại'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        customer = customer_response.json()
        total_amount = 0
        order_items = []
        
        # Xử lý từng mặt hàng
        for item in items:
            book_id = item.get('book_id')
            quantity = item.get('quantity', 1)
            
            # Lấy thông tin sách
            book_response = requests.get(
                f"{SERVICES['books']}books/{book_id}/",
                timeout=5
            )
            
            if book_response.status_code != 200:
                return Response(
                    {'error': f'Sách ID {book_id} không tồn tại'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            book = book_response.json()
            
            # Kiểm tra tồn kho
            if book['stock'] < quantity:
                return Response(
                    {
                        'error': f'Không đủ hàng cho sách "{book["title"]}"'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            item_total = float(book['price']) * int(quantity)
            total_amount += item_total
            
            order_items.append({
                'book_id': book_id,
                'book_title': book['title'],
                'quantity': quantity,
                'unit_price': book['price'],
                'total_price': item_total
            })
            
            # Giảm tồn kho
            requests.post(
                f"{SERVICES['books']}books/{book_id}/decrease_stock/",
                json={'quantity': quantity},
                timeout=5
            )
        
        # Tạo đơn hàng trên Order Service
        order_data = {
            'customer_id': customer_id,
            'total_amount': total_amount,
            'shipping_address': shipping_address,
            'payment_method': payment_method,
        }
        
        order_response = requests.post(
            f"{SERVICES['orders']}orders/",
            json=order_data,
            timeout=5
        )
        
        if order_response.status_code != 201:
            return Response(
                {'error': 'Lỗi tạo đơn hàng'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        order = order_response.json()
        
        # Thêm items vào đơn hàng
        order['items'] = order_items
        
        # Cập nhật thống kê khách hàng
        requests.post(
            f"{SERVICES['customers']}customers/{customer_id}/update_total_spent/",
            json={'amount': total_amount},
            timeout=5
        )
        
        return Response(order, status=status.HTTP_201_CREATED)
    
    except requests.exceptions.Timeout:
        return Response(
            {'error': 'Timeout khi kết nối services'},
            status=status.HTTP_503_SERVICE_UNAVAILABLE
        )
    except Exception as e:
        logger.error(f"Error creating order: {str(e)}")
        return Response(
            {'error': f'Lỗi: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
