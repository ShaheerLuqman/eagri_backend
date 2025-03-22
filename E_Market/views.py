from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Q
from .models import MarketItem, Product
from .serializers import MarketItemSerializer, ProductSerializer

class MarketItemViewSet(viewsets.ModelViewSet):
    queryset = MarketItem.objects.all()
    serializer_class = MarketItemSerializer

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