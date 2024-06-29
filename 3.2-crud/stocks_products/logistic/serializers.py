# from abc import ABC

from rest_framework import serializers

from .models import Product, Stock, StockProduct


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description']


class ProductPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockProduct
        fields = ['product', 'quantity', 'price']


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)

    class Meta:
        model = Stock
        fields = ['id', 'address', 'positions']

    def create(self, validated_data):
        # достаем связанные данные для других таблиц
        positions = validated_data.pop('positions')
        # создаем склад по его параметрам
        stock = super().create(validated_data)
        for position in positions:
            StockProduct.objects.create(stock=stock, **position)
        return stock

    def update(self, instance, validated_data):
        # достаем связанные данные для других таблиц
        positions = validated_data.pop('positions')

        instance.address = validated_data.get('address', instance.address)
        instance.save()

        # обновляем склад по его параметрам
        # stock = super().update(instance, validated_data)

        for position in positions:
            product = position.get('product')
            stock_product = instance.positions.filter(product=product).first()

            if stock_product:
                stock_product.quantity = \
                    position.get('quantity', stock_product.quantity)
                stock_product.price = \
                    position.get('price', stock_product.price)
                stock_product.save()
            else:
                StockProduct.objects.create(stock=instance, **position)

        return instance
