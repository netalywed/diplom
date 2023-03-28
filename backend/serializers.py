from rest_framework import serializers
from .models import Shop, Category, Product, ProductInfo, Parameter, ProductParameter, OrderItem, Order, Contact, User
from drf_writable_nested import WritableNestedModelSerializer


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ('id', 'city', 'street', 'house', 'structure', 'building', 'apartment', 'user', 'phone')
        read_only_fields = ('id',)
        extra_kwargs = {
            'user': {'write_only': True}
        }


class UserSerializer(serializers.ModelSerializer):
    contacts = ContactSerializer(read_only=True, many=True)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'company', 'position', 'contacts')
        read_only_fields = ('id',)


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ('id', 'name', )


class CategorySerializer(WritableNestedModelSerializer, serializers.ModelSerializer):
    shops = ShopSerializer(many=True)  # не надо?

    class Meta:
        model = Category
        fields = ('name', 'shops', )


class ParameterSerializer(serializers.ModelSerializer):   # он нужен?
    class Meta:
        model = Parameter
        fields = ('name',)


class ProductParameterSerializer(serializers.ModelSerializer):
    parameter_name = serializers.StringRelatedField()

    class Meta:
        model = ProductParameter
        fields = ('parameter_name', 'value',)


class ProductSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):
    category = serializers.StringRelatedField()

    class Meta:
        model = Product
        fields = ('name', 'category', )


class ProductInfoSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):
    product_parameters = ProductParameterSerializer(many=True)
    product = ProductSerializer(read_only=True)

    class Meta:
        model = ProductInfo
        fields = ('id', 'product', 'model', 'external_id', 'quantity', 'price', 'price_rrc', 'product_parameters')
        read_only_fields = ('id',)


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('id', 'product_info', 'quantity', 'order',)
        read_only_fields = ('id',)
        extra_kwargs = {
            'order': {'write_only': True}
        }


class OrderItemCreateSerializer(OrderItemSerializer):
    product_info = ProductInfoSerializer(read_only=True)


class OrderSerializer(serializers.ModelSerializer):
    ordered_items = OrderItemCreateSerializer(read_only=True, many=True)

    total_sum = serializers.IntegerField()
    contact = ContactSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'ordered_items', 'state', 'dt', 'total_sum', 'contact',)
        read_only_fields = ('id',)




