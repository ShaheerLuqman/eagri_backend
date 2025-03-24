from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Q
from .models import  Product
from .serializers import ProductSerializer
from .models import Product, Order
from .serializers import ProductSerializer, OrderSerializer
import uuid
import cloudinary
from PIL import Image
from io import BytesIO
import cloudinary.uploader

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description', 'category']
    ordering_fields = ['price', 'created_at', 'stock_quantity']
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = Product.objects.all()
        
        # Filter by category
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category=category)

        # Filter by price range
        min_price = self.request.query_params.get('min_price', None)
        max_price = self.request.query_params.get('max_price', None)
        if min_price:
            queryset = queryset.filter(price__gte=float(min_price))
        if max_price:
            queryset = queryset.filter(price__lte=float(max_price))

        # Filter by stock availability
        in_stock = self.request.query_params.get('in_stock', None)
        if in_stock:
            queryset = queryset.filter(stock_quantity__gt=0)

        return queryset

    def compress_image(self, image):
        img = Image.open(image)
        
        # Resize if image is larger than 500x500 while maintaining aspect ratio
        if img.width > 500 or img.height > 500:
            # Calculate aspect ratio
            aspect_ratio = img.width / img.height
            
            if img.width > img.height:
                new_width = 500
                new_height = int(500 / aspect_ratio)
            else:
                new_height = 500
                new_width = int(500 * aspect_ratio)
                
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Convert to RGB if image is in RGBA mode
        if img.mode == 'RGBA':
            img = img.convert('RGB')
            
        # Create a BytesIO object to store the compressed image
        output = BytesIO()
        
        # Save the image with compression
        img.save(output, 
                format='JPEG', 
                quality=90,
                optimize=True)
        output.seek(0)
        
        return output

    def create(self, request, *args, **kwargs):
        try:
            # Validate required fields
            required_fields = ['name', 'price', 'category']
            for field in required_fields:
                if field not in request.data:
                    return Response(
                        {f"error": f"{field} is required"},
                        status=status.HTTP_400_BAD_REQUEST
                    )

            # Handle image upload to Cloudinary
            image = request.FILES.get('image')
            if image:
                # Compress image before upload
                compressed_image = self.compress_image(image)
                
                # Upload compressed image
                upload_result = cloudinary.uploader.upload(
                    compressed_image,
                    folder='eagri/products',
                    use_filename=True,
                    unique_filename=True
                )
                request.data['image_url'] = upload_result['secure_url']

            # Validate price and discounted_price
            if 'discounted_price' in request.data and request.data['discounted_price']:
                if float(request.data['discounted_price']) >= float(request.data['price']):
                    return Response(
                        {"error": "Discounted price must be less than regular price"},
                        status=status.HTTP_400_BAD_REQUEST
                    )

            # Create product
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)

            return Response(
                {"message": "Product created successfully", "data": serializer.data},
                status=status.HTTP_201_CREATED
            )

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=['get'])
    def on_sale(self, request):
        """Get products that are currently on sale"""
        products = self.get_queryset().filter(
            discounted_price__isnull=False
        ).exclude(discounted_price=0)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_category(self, request):
        category = request.query_params.get('category', None)
        if not category:
            return Response(
                {"error": "Category parameter is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        products = self.get_queryset().filter(category=category)
        if not products.exists():
            return Response(
                {"error": f"No products found in category: {category}"},
                status=status.HTTP_404_NOT_FOUND
            )
            
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        
        # Get top 3 related products from the same category
        related_products = Product.objects.filter(
            category=instance.category
        ).exclude(
            id=instance.id
        ).order_by('-created_at')[:3]
        
        related_serializer = self.get_serializer(related_products, many=True)
        
        response_data = {
            'product': serializer.data,
            'related_products': related_serializer.data
        }
        
        return Response(response_data)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        try:
            # Validate required fields
            required_fields = ['product', 'quantity', 'shipping_address', 'contact_number', 'payment_method']
            for field in required_fields:
                if field not in request.data:
                    return Response(
                        {"error": f"{field} is required"},
                        status=status.HTTP_400_BAD_REQUEST
                    )

            # Get product and validate stock
            product = Product.objects.get(id=request.data['product'])
            quantity = int(request.data['quantity'])

            if product.stock_quantity < quantity:
                return Response(
                    {"error": "Insufficient stock available"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Calculate prices
            unit_price = product.discounted_price if product.discounted_price else product.price
            total_amount = unit_price * quantity

            # Create order data
            order_data = {
                **request.data,
                'transaction_id': str(uuid.uuid4())[:10],
                'user_id': request.user.id if request.user.is_authenticated else None,
                'unit_price': unit_price,
                'total_amount': total_amount,
            }

            serializer = self.get_serializer(data=order_data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)

            # Update product stock
            product.stock_quantity -= quantity
            product.save()

            return Response(
                {"message": "Order placed successfully", "data": serializer.data},
                status=status.HTTP_201_CREATED
            )

        except Product.DoesNotExist:
            return Response(
                {"error": "Product not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        
        # Filter by user if authenticated
        if request.user.is_authenticated:
            queryset = queryset.filter(user_id=request.user.id)
            
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)