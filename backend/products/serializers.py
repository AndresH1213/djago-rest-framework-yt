from rest_framework import serializers

from .models import Product

class ProductSerializer(serializers.ModelSerializer):
  discount = serializers.SerializerMethodField(read_only=True)
  class Meta:
    model = Product
    fields = [
      'title',
      'content',
      'price',
      'sale_price',
      # 'get_discount',
      'discount'
    ]
  
  def get_discount(self, obj):
    if not hasattr(obj, 'id'): return None
    if not isinstance(obj, Product): return None
    return obj.get_discount()

"""As we can actually modify the data that we are throwing back in the serializers
we can create more than one serializer per model and adjust each one to our needs"""